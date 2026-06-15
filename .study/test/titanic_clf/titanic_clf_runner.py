# titanic_clf_runner.py
# 머신러닝 실습2 (과제) — 타이타닉 생존자 분류 섹션별 테스트 실행기
# 실행: c:\_proj\python_workspace\.venv\Scripts\python.exe titanic_clf_runner.py
# 결과: logs/{섹션명}.txt 저장 + 터미널 출력,  charts/*.png 생성
# 데이터: ../ml_workspace/from_colab/0528_data/titanic/train.csv (Kaggle Titanic, 891행)
#   ※ test.csv 는 정답(Survived) 라벨이 없으므로, train.csv 에서 검증용(validation)을
#     분리(stratify, random_state=42)해 성능을 측정한다. 모든 수치 재현 가능(고정 시드).
#   ※ 0528 수업 노트북(타이타닉분류모델.ipynb)은 동일 전처리(fillna/LabelEncoder/
#     StandardScaler/8:2 split) 위에서 PyTorch 신경망을 썼다. 과제에서는 같은 전처리
#     위에 sklearn 분류기(Logistic / RandomForest)를 올려 평가·해석을 파고든다.

import sys, io, pathlib
from contextlib import redirect_stdout

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# 차트 한글 렌더링 (Windows 기본 한글 폰트)
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, classification_report, confusion_matrix)

HERE = pathlib.Path(__file__).parent
LOGS = HERE / "logs"; LOGS.mkdir(exist_ok=True)
CHARTS = HERE / "charts"; CHARTS.mkdir(exist_ok=True)
DATA = pathlib.Path(r"c:\_proj\ml_workspace\from_colab\0528_data\titanic\train.csv")
SEED = 42

def run_section(name, fn):
    sep = "=" * 60
    buf = io.StringIO()
    print(sep); print(f"# {name}"); print(sep)
    with redirect_stdout(buf):
        try:
            fn()
        except Exception as e:
            print(f"{type(e).__name__}: {e}")
    out = buf.getvalue()
    sys.stdout.write(out)
    (LOGS / f"{name}.txt").write_text(sep + "\n" + f"# {name}" + "\n" + sep + "\n" + out, encoding="utf-8")

def load_raw():
    """원본 train.csv 를 매번 새로 읽어 섹션 간 오염을 막는다."""
    return pd.read_csv(DATA)

# ── 공통 전처리 (0528 노트북 흐름과 동일) ────────────────────────────────
COL_DEL = ["PassengerId", "Name", "Ticket", "Cabin"]
COL_NUM = ["Age", "Fare"]
COL_CAT = ["Pclass", "Sex", "SibSp", "Parch", "Embarked"]
COL_Y = "Survived"

def preprocess(df, scaler=None, fit=True, age_fill=None, fare_fill=None, emb_fill=None):
    """결측치 채움 → Sex/Embarked 인코딩 → Age/Fare 표준화 → X, y 반환.
    train 통계(평균/최빈값/scaler)만 학습하고 valid 엔 그대로 적용(누수 방지)."""
    df = df.copy()
    if fit:
        age_fill = df["Age"].mean()
        fare_fill = df["Fare"].median()
        emb_fill = df["Embarked"].mode()[0]
    df["Age"] = df["Age"].fillna(age_fill)
    df["Fare"] = df["Fare"].fillna(fare_fill)
    df["Embarked"] = df["Embarked"].fillna(emb_fill)
    # 범주형 → 정수 (Sex: female/male, Embarked: C/Q/S)
    df["Sex"] = df["Sex"].map({"female": 0, "male": 1}).astype(int)
    df["Embarked"] = df["Embarked"].map({"C": 0, "Q": 1, "S": 2}).astype(int)
    X = df.drop(COL_DEL + [COL_Y], axis=1)
    y = df[COL_Y]
    if fit:
        scaler = StandardScaler().fit(X[COL_NUM])
    X = X.copy()
    X[COL_NUM] = scaler.transform(X[COL_NUM])
    return X, y, scaler, (age_fill, fare_fill, emb_fill)

# ── §00: 데이터 첫 관찰 — 무엇을 맞히는 문제이고 어떤 열이 있나 ────────────
def s00_first_look():
    """train.csv 를 읽어 형태·열·정답(Survived)을 관찰한다.
    정답이 0/1 두 라벨이므로 이 과제는 '분류'다(연속값 예측 아님)."""
    df = load_raw()
    print(f"행/열 크기: {df.shape[0]}행 × {df.shape[1]}열")
    print(f"열 목록: {list(df.columns)}")
    print()
    print("정답(Survived) 분포:")
    vc = df["Survived"].value_counts().sort_index()
    print(f"  0(사망) = {vc[0]}명,  1(생존) = {vc[1]}명")
    print(f"  전체 생존율 = {df['Survived'].mean():.4f}")
    print(f"  정답 라벨 종류 = {sorted(df['Survived'].unique())} → 2개뿐 → 분류(Classification)")

# ── §01: 결측치 진단 — 어느 열에 얼마나 비어 있나 ─────────────────────────
def s01_missing():
    """fit 전에 결측치를 진단한다. Age·Cabin·Embarked 세 열이 비어 있고,
    Cabin 은 대부분 결측이라 채우기보다 버리는 편이 낫다는 판단 근거를 본다."""
    df = load_raw()
    miss = df.isnull().sum()
    miss = miss[miss > 0]
    print("결측치가 있는 열 (개수 / 비율):")
    for col, n in miss.items():
        print(f"  {col:<9} {n:>4}개  ({n/len(df)*100:5.1f}%)")
    print()
    print(f"Cabin 결측 비율이 {df['Cabin'].isnull().mean()*100:.1f}% → 채워 넣기보다 제거(COL_DEL) 대상")
    print(f"Age 는 {df['Age'].isnull().mean()*100:.1f}% → 평균/중앙값으로 대치(impute)")
    print(f"Embarked 는 {df['Embarked'].isnull().sum()}개뿐 → 최빈값('{df['Embarked'].mode()[0]}')으로 대치")

# ── §02: EDA — 어떤 특성이 생존을 가르나 (Sex, Pclass) ────────────────────
def s02_eda():
    """성별·객실등급별 생존율을 교차표로 본다. 특정 특성이 생존을 강하게
    가른다면, 그 특성은 분류기에 큰 정보가 된다."""
    df = load_raw()
    print("성별(Sex) 별 생존율:")
    g = df.groupby("Sex")["Survived"].agg(["mean", "count"])
    for sex, row in g.iterrows():
        print(f"  {sex:<7} 생존율 {row['mean']:.3f}  (n={int(row['count'])})")
    print()
    print("객실등급(Pclass) 별 생존율:")
    g2 = df.groupby("Pclass")["Survived"].agg(["mean", "count"])
    for pc, row in g2.iterrows():
        print(f"  {pc}등급  생존율 {row['mean']:.3f}  (n={int(row['count'])})")
    print()
    print(f"여성 생존율({g.loc['female','mean']:.3f})이 남성({g.loc['male','mean']:.3f})의 "
          f"{g.loc['female','mean']/g.loc['male','mean']:.1f}배 → Sex 가 가장 강한 신호로 보인다")

    # 차트: Sex / Pclass 별 생존/사망 카운트
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.8))
    for ax, col, title in [(axes[0], "Sex", "성별"), (axes[1], "Pclass", "객실등급")]:
        ct = df.groupby([col, "Survived"]).size().unstack(fill_value=0)
        ct.plot(kind="bar", ax=ax, color=["#E8875A", "#52A97E"], width=0.7)
        ax.set_title(f"{title}별 생존/사망"); ax.set_xlabel(title); ax.set_ylabel("인원수")
        ax.legend(["사망(0)", "생존(1)"]); ax.tick_params(axis="x", rotation=0)
    fig.tight_layout(); fig.savefig(CHARTS / "ch02_survival_by_group.png", dpi=110); plt.close(fig)
    print("[chart] ch02_survival_by_group.png 저장")

# ── §03: 인코딩 — 왜 문자열을 숫자로 바꿔야 하나 ──────────────────────────
def s03_encoding():
    """sklearn 분류기는 문자열('male'/'female')을 직접 못 받는다.
    인코딩 전 상태로 fit 하면 에러가 나는지 직접 확인하고, 인코딩 후 형태를 본다."""
    df = load_raw()
    df["Age"] = df["Age"].fillna(df["Age"].mean())
    df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])
    X_raw = df[["Pclass", "Sex", "Age", "Fare", "Embarked"]]
    y = df["Survived"]
    print("인코딩 전 — 문자열 그대로 LogisticRegression.fit 시도:")
    try:
        LogisticRegression().fit(X_raw, y)
        print("  (학습 성공? — 예상 밖)")
    except Exception as e:
        msg = str(e).splitlines()[0]
        print(f"  {type(e).__name__}: {msg}")
    print()
    print("인코딩 후 — Sex/Embarked 를 정수로 매핑:")
    df["Sex"] = df["Sex"].map({"female": 0, "male": 1})
    df["Embarked"] = df["Embarked"].map({"C": 0, "Q": 1, "S": 2})
    enc = df[["Pclass", "Sex", "Age", "Fare", "Embarked"]].head(5)
    print(enc.to_string())
    print("  → 모든 열이 숫자 → 이제 fit 가능")

# ── §04: baseline — 아무것도 안 배운 분류기의 정확도 ──────────────────────
def s04_baseline():
    """DummyClassifier(최빈 클래스만 찍기)로 '하한선'을 만든다.
    이보다 못한 모델은 의미가 없다. 분류기의 정확도는 이 기준 위에서 읽어야 한다."""
    df = load_raw()
    Xtr, Xva, ytr, yva, sc, fills = split_and_prep(df)
    dummy = DummyClassifier(strategy="most_frequent").fit(Xtr, ytr)
    acc = accuracy_score(yva, dummy.predict(Xva))
    print(f"train 다수 클래스 = {ytr.mode()[0]} (사망)")
    print(f"무조건 '사망'으로 찍는 baseline 정확도 = {acc:.4f}")
    print(f"  → 검증셋의 사망 비율과 같다({(yva==0).mean():.4f}). 분류기는 이 {acc:.3f}를 넘겨야 의미가 있다.")

def split_and_prep(df):
    """원본 df → train/valid 분리 후 train 통계로만 전처리(누수 방지)."""
    tr, va = train_test_split(df, test_size=0.2, random_state=SEED, stratify=df["Survived"])
    Xtr, ytr, sc, fills = preprocess(tr, fit=True)
    age_f, fare_f, emb_f = fills
    Xva, yva, _, _ = preprocess(va, scaler=sc, fit=False,
                                age_fill=age_f, fare_fill=fare_f, emb_fill=emb_f)
    return Xtr, Xva, ytr, yva, sc, fills

# ── §05: 분류기 비교 — Logistic vs DecisionTree vs RandomForest ───────────
def s05_compare():
    """같은 전처리·같은 split 위에서 세 분류기의 검증 정확도를 비교한다.
    baseline(0.616)을 넘는지, 어느 모델이 가장 높은지 확인한다."""
    df = load_raw()
    Xtr, Xva, ytr, yva, sc, fills = split_and_prep(df)
    models = {
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=SEED),
        "DecisionTree(depth5)": DecisionTreeClassifier(max_depth=5, random_state=SEED),
        "RandomForest(200)": RandomForestClassifier(n_estimators=200, random_state=SEED),
    }
    print(f"{'모델':<22} | {'train 정확도':>11} | {'valid 정확도':>11}")
    print("-" * 52)
    for name, m in models.items():
        m.fit(Xtr, ytr)
        tr_acc = accuracy_score(ytr, m.predict(Xtr))
        va_acc = accuracy_score(yva, m.predict(Xva))
        print(f"{name:<22} | {tr_acc:>11.4f} | {va_acc:>11.4f}")
    print()
    print("관찰: DecisionTree/RandomForest 는 train 정확도가 valid 보다 크게 높다(과대적합 경향).")
    print("      세 모델 모두 baseline(0.616)은 넘긴다.")

# ── §06: 정확도만으로 충분한가 — 정밀도·재현율·혼동행렬 ───────────────────
def s06_metrics():
    """정확도 한 숫자는 '누구를 놓쳤는지'를 숨긴다. 가장 균형 잡힌 모델로
    혼동행렬·정밀도·재현율·F1 을 클래스별로 뜯어본다."""
    df = load_raw()
    Xtr, Xva, ytr, yva, sc, fills = split_and_prep(df)
    clf = LogisticRegression(max_iter=1000, random_state=SEED).fit(Xtr, ytr)
    pred = clf.predict(Xva)
    acc = accuracy_score(yva, pred)
    print(f"LogisticRegression 검증 정확도 = {acc:.4f}")
    print()
    print("혼동행렬 (행=실제, 열=예측):")
    cm = confusion_matrix(yva, pred)
    print(f"            예측:사망  예측:생존")
    print(f"  실제:사망 {cm[0,0]:>8}  {cm[0,1]:>9}")
    print(f"  실제:생존 {cm[1,0]:>8}  {cm[1,1]:>9}")
    print()
    print("생존(1) 클래스 기준 지표:")
    print(f"  정밀도(precision) = {precision_score(yva, pred):.4f}  (생존이라 예측한 것 중 진짜 생존)")
    print(f"  재현율(recall)    = {recall_score(yva, pred):.4f}  (진짜 생존자 중 찾아낸 비율)")
    print(f"  F1                = {f1_score(yva, pred):.4f}")
    print()
    print(classification_report(yva, pred, target_names=["사망(0)", "생존(1)"], digits=3))

    # 혼동행렬 히트맵
    fig, ax = plt.subplots(figsize=(4.6, 4))
    im = ax.imshow(cm, cmap="Greens")
    ax.set_xticks([0, 1]); ax.set_yticks([0, 1])
    ax.set_xticklabels(["예측:사망", "예측:생존"]); ax.set_yticklabels(["실제:사망", "실제:생존"])
    for i in range(2):
        for j in range(2):
            ax.text(j, i, cm[i, j], ha="center", va="center",
                    color="white" if cm[i, j] > cm.max() / 2 else "#1f2933", fontsize=15, fontweight="bold")
    ax.set_title(f"혼동행렬 (LogisticRegression, acc={acc:.3f})")
    fig.tight_layout(); fig.savefig(CHARTS / "ch06_confusion.png", dpi=110); plt.close(fig)
    print("[chart] ch06_confusion.png 저장")

# ── §07: 해석 — 어떤 특성이 생존을 가장 크게 갈랐나(특성 중요도) ──────────
def s07_importance():
    """RandomForest 의 feature_importances_ 로 '모델이 무엇을 보고 판단했는지'를 읽는다.
    EDA(§02)에서 Sex 가 강해 보였는데, 모델도 같은 결론을 내는지 확인한다."""
    df = load_raw()
    Xtr, Xva, ytr, yva, sc, fills = split_and_prep(df)
    rf = RandomForestClassifier(n_estimators=200, random_state=SEED).fit(Xtr, ytr)
    imp = pd.Series(rf.feature_importances_, index=Xtr.columns).sort_values(ascending=False)
    print("RandomForest 특성 중요도 (높을수록 생존 판단에 크게 기여):")
    for feat, v in imp.items():
        bar = "█" * int(v * 50)
        print(f"  {feat:<9} {v:.4f}  {bar}")
    print()
    print(f"가장 중요한 특성: {imp.index[0]} ({imp.iloc[0]:.3f})")
    print(f"의외: EDA 에서 가장 강해 보인 Sex({imp['Sex']:.3f})보다 Fare({imp['Fare']:.3f})가 근소하게 위.")
    print(f"  상위 3개(Fare·Sex·Age)가 거의 비슷하게 기여 → 단일 특성이 아니라 조합이 생존을 가른다.")

    fig, ax = plt.subplots(figsize=(6, 4))
    imp_sorted = imp.sort_values()
    ax.barh(imp_sorted.index, imp_sorted.values, color="#5B9BD5")
    ax.set_xlabel("중요도(feature importance)")
    ax.set_title("RandomForest 특성 중요도")
    fig.tight_layout(); fig.savefig(CHARTS / "ch07_importance.png", dpi=110); plt.close(fig)
    print("[chart] ch07_importance.png 저장")

if __name__ == "__main__":
    run_section("00_first_look", s00_first_look)
    run_section("01_missing", s01_missing)
    run_section("02_eda", s02_eda)
    run_section("03_encoding", s03_encoding)
    run_section("04_baseline", s04_baseline)
    run_section("05_compare", s05_compare)
    run_section("06_metrics", s06_metrics)
    run_section("07_importance", s07_importance)
    print("\n완료: logs/*.txt, charts/*.png 생성")
