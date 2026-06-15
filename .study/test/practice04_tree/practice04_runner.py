# practice04_runner.py
# 머신러닝 실습4(과제) — 결정트리(분류)·회귀트리 섹션별 테스트 실행기
# 실행: c:\_proj\python_workspace\.venv\Scripts\python.exe practice04_runner.py
# 결과: logs/{섹션명}.txt 저장 + 터미널 출력,  charts/*.png 생성
#
# 데이터:
#   · 분류: sklearn 내장 load_wine (13특성·3품종)  — DecisionTreeClassifier
#   · 회귀: UCI winequality-white.csv (화이트와인 품질, 11특성) — DecisionTreeRegressor
#       ※ 회귀 과제(회귀트리_실습문제.txt)가 실제로 쓴 데이터셋이라 동일하게 사용.
#         네트워크 의존을 없애려 1회 받은 CSV 를 data/ 에 캐시한다(고정 분할로 재현 가능).
#   고정 시드 random_state=42.

import sys, io, pathlib, urllib.request
from contextlib import redirect_stdout

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# 차트 한글 렌더링 (Windows 기본 한글 폰트) — 폰트 경고 0
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

from sklearn.datasets import load_wine
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, plot_tree
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix, r2_score,
                             mean_squared_error, mean_absolute_error)

HERE = pathlib.Path(__file__).parent
LOGS = HERE / "logs"; LOGS.mkdir(exist_ok=True)
CHARTS = HERE / "charts"; CHARTS.mkdir(exist_ok=True)
DATA = HERE / "data"; DATA.mkdir(exist_ok=True)
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

# ── 회귀용 화이트와인 데이터(과제와 동일) 로드 + 캐시 ────────────────────────
def load_white_wine():
    cache = DATA / "winequality-white.csv"
    if not cache.exists():
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-white.csv"
        cache.write_bytes(urllib.request.urlopen(url, timeout=20).read())
    df = pd.read_csv(cache, sep=';')
    df.columns = [c.replace(" ", "_") for c in df.columns]
    return df

# ───────────────────────────────────────────────────────────────────────────
# §00: 두 과제 데이터의 성격 — 분류(load_wine) vs 회귀(white wine quality)
# ───────────────────────────────────────────────────────────────────────────
def s00_two_tasks():
    """결정트리 과제는 분류, 회귀트리 과제는 연속값 예측이다.
    같은 '트리'인데 무엇이 다른지 — 정답 y 의 형태로 먼저 가른다."""
    wine = load_wine()
    print("[분류 과제] sklearn load_wine")
    print(f"  X shape: {wine.data.shape}  (행 {wine.data.shape[0]} · 특성 {wine.data.shape[1]}개)")
    print(f"  y 라벨 종류: {np.unique(wine.target)} = {list(wine.target_names)}")
    print(f"  클래스별 개수: {np.bincount(wine.target)}  → 소수의 정수 라벨 = 분류")

    df = load_white_wine()
    print("\n[회귀 과제] UCI winequality-white.csv")
    print(f"  X shape: {df.drop('quality',axis=1).shape}  (행 {len(df)} · 특성 11개)")
    q = df['quality']
    print(f"  y(quality) 값 범위: {q.min()}~{q.max()}, 고유값 {sorted(q.unique())}")
    print(f"  y 평균 {q.mean():.3f} · 표준편차 {q.std():.3f}  → 순서가 있는 연속형 점수 = 회귀")

# ───────────────────────────────────────────────────────────────────────────
# §01: 분류 결정트리 baseline — 기본 트리의 정확도와 과대적합
# ───────────────────────────────────────────────────────────────────────────
def s01_clf_baseline():
    """기본 DecisionTreeClassifier(제약 없음)를 wine 에 그대로 fit.
    과제 문제1 의 5개 지표(Acc/Precision/Recall/F1/혼동행렬)를 출력하고,
    train 정확도와 test 정확도의 격차로 과대적합 여부를 본다."""
    wine = load_wine()
    X, y = wine.data, wine.target
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=SEED, stratify=y)

    clf = DecisionTreeClassifier(random_state=SEED)   # 제약 없음(기본값)
    clf.fit(Xtr, ytr)
    pred = clf.predict(Xte)

    acc = accuracy_score(yte, pred)
    prec = precision_score(yte, pred, average='weighted')
    rec = recall_score(yte, pred, average='weighted')
    f1 = f1_score(yte, pred, average='weighted')

    print("[기본 결정트리 — 제약 없음(max_depth=None)]")
    print(f"  트리 깊이 : {clf.get_depth()},  리프(터미널) 노드 수 : {clf.get_n_leaves()}")
    print(f"  train 정확도 : {clf.score(Xtr, ytr):.4f}")
    print(f"  test  정확도 : {acc:.4f}")
    print(f"  과대적합 신호(train-test): {clf.score(Xtr,ytr)-acc:+.4f}")
    print("\n[문제1 — 성능지표 5종]")
    print(f"  Accuracy  : {acc:.4f}")
    print(f"  Precision : {prec:.4f}")
    print(f"  Recall    : {rec:.4f}")
    print(f"  F1-score  : {f1:.4f}")
    print("  Confusion Matrix:")
    print(confusion_matrix(yte, pred))

# ───────────────────────────────────────────────────────────────────────────
# §02: max_depth 튜닝 — 깊이를 키울수록 train↑ test 정체/하락
# ───────────────────────────────────────────────────────────────────────────
def s02_clf_depth():
    """과제 문제2. max_depth 를 3·5·7·10·None 으로 바꾸며 train/test 정확도를 비교한다.
    '깊이가 너무 크면 어떤 문제가 생기나'를 수치로 확인 — 과대적합."""
    wine = load_wine()
    X, y = wine.data, wine.target
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=SEED, stratify=y)

    depths = [3, 5, 7, 10, None]
    tr_scores, te_scores, leaves = [], [], []
    print(f"{'max_depth':>9} | {'train acc':>9} | {'test acc':>9} | {'리프수':>6}")
    print("-" * 44)
    for d in depths:
        clf = DecisionTreeClassifier(max_depth=d, random_state=SEED).fit(Xtr, ytr)
        tr, te = clf.score(Xtr, ytr), clf.score(Xte, yte)
        tr_scores.append(tr); te_scores.append(te); leaves.append(clf.get_n_leaves())
        print(f"{str(d):>9} | {tr:9.4f} | {te:9.4f} | {clf.get_n_leaves():6d}")

    xlabels = [str(d) for d in depths]
    xs = range(len(depths))
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(xs, tr_scores, "o-", color="#5B9BD5", label="train 정확도")
    ax.plot(xs, te_scores, "s-", color="#E8875A", label="test 정확도")
    ax.set_xticks(list(xs)); ax.set_xticklabels(xlabels)
    ax.set_xlabel("max_depth"); ax.set_ylabel("정확도")
    ax.set_title("깊이↑ → train은 1.0, test는 정체 (과대적합)")
    ax.legend(); ax.set_ylim(0.8, 1.02); fig.tight_layout()
    fig.savefig(CHARTS / "ch_depth.png", dpi=110); plt.close(fig)
    print("[chart] ch_depth.png 저장")

# ───────────────────────────────────────────────────────────────────────────
# §03: GridSearchCV — 깊이/리프/분할/기준을 교차검증으로 고른다
# ───────────────────────────────────────────────────────────────────────────
def s03_clf_gridsearch():
    """과제 문제2~5(max_depth·min_samples_split·min_samples_leaf·criterion)를
    손으로 하나씩 바꾸는 대신, GridSearchCV 로 조합을 한 번에 탐색해
    교차검증(cv=5) 기준 최적 파라미터를 고른다."""
    wine = load_wine()
    X, y = wine.data, wine.target
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=SEED, stratify=y)

    param_grid = {
        "max_depth": [3, 4, 5, 7, 10, None],
        "min_samples_split": [2, 5, 10, 20],
        "min_samples_leaf": [1, 5, 10],
        "criterion": ["gini", "entropy"],
    }
    base = DecisionTreeClassifier(random_state=SEED)
    gs = GridSearchCV(base, param_grid, cv=5, scoring="accuracy", n_jobs=1)
    gs.fit(Xtr, ytr)

    n_combos = (len(param_grid["max_depth"]) * len(param_grid["min_samples_split"])
                * len(param_grid["min_samples_leaf"]) * len(param_grid["criterion"]))
    print(f"탐색한 조합 수: {n_combos}개 × cv 5겹 = {n_combos*5}회 적합")
    print(f"best params : {gs.best_params_}")
    print(f"best cv 정확도 : {gs.best_score_:.4f}  (5겹 교차검증 평균)")

    base_default = DecisionTreeClassifier(random_state=SEED).fit(Xtr, ytr)
    best = gs.best_estimator_
    print("\n[기본 트리 vs GridSearch 최적 트리 — test 정확도]")
    print(f"  기본(제약 없음) test 정확도 : {base_default.score(Xte, yte):.4f}  (깊이 {base_default.get_depth()})")
    print(f"  최적 트리       test 정확도 : {best.score(Xte, yte):.4f}  (깊이 {best.get_depth()})")
    print(f"  개선폭 : {best.score(Xte,yte)-base_default.score(Xte,yte):+.4f}")

# ───────────────────────────────────────────────────────────────────────────
# §04: Feature Importance(분류) — 트리는 어떤 특성으로 나누나
# ───────────────────────────────────────────────────────────────────────────
def s04_clf_importance():
    """과제 문제6. 최적 트리의 feature_importances_ 를 정렬해 가장 중요한 특성을 찾는다.
    루트 노드에서 처음 데이터를 가르는 특성이 보통 중요도 상위에 온다."""
    wine = load_wine()
    X, y = wine.data, wine.target
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=SEED, stratify=y)
    clf = DecisionTreeClassifier(max_depth=4, random_state=SEED).fit(Xtr, ytr)

    imp = clf.feature_importances_
    order = np.argsort(imp)[::-1]
    names = np.array(wine.feature_names)
    print("[특성 중요도 — 내림차순]")
    for i in order:
        bar = "#" * int(round(imp[i] * 40))
        print(f"  {names[i]:<22} {imp[i]:.4f}  {bar}")
    # 루트 노드가 사용한 특성
    root_feat = wine.feature_names[clf.tree_.feature[0]]
    print(f"\n루트 노드가 처음 가른 특성: {root_feat}")
    print(f"가장 중요한 특성        : {names[order[0]]} ({imp[order[0]]:.4f})")

    top = order[:8][::-1]
    fig, ax = plt.subplots(figsize=(6.6, 4))
    ax.barh([names[i] for i in top], [imp[i] for i in top], color="#52A97E")
    ax.set_xlabel("중요도(feature_importances_)")
    ax.set_title("wine 분류 — 상위 8개 특성 중요도")
    fig.tight_layout(); fig.savefig(CHARTS / "ch_importance_clf.png", dpi=110); plt.close(fig)
    print("[chart] ch_importance_clf.png 저장")

# ───────────────────────────────────────────────────────────────────────────
# §05: 회귀트리 baseline — 화이트와인 품질을 연속값으로 예측(성능 향상 전)
# ───────────────────────────────────────────────────────────────────────────
def s05_reg_baseline():
    """회귀 과제 데이터(화이트와인 품질)를 DecisionTreeRegressor 로 예측한다.
    제약 없는 기본 트리는 train 을 거의 외워서 test R2 가 낮게(혹은 음수에 가깝게) 나온다 —
    이것이 '성능 향상 전' 기준선."""
    df = load_white_wine()
    X = df.drop("quality", axis=1).values
    y = df["quality"].values
    # 과제와 동일한 고정 분할(앞 3749 train / 나머지 test)
    Xtr, Xte = X[:3749], X[3749:]
    ytr, yte = y[:3749], y[3749:]

    reg = DecisionTreeRegressor(random_state=SEED)   # 제약 없음
    reg.fit(Xtr, ytr)
    p = reg.predict(Xte)
    print("[기본 회귀트리 — 제약 없음(max_depth=None)]")
    print(f"  트리 깊이 : {reg.get_depth()},  리프 노드 수 : {reg.get_n_leaves()}")
    print(f"  train R2 : {reg.score(Xtr, ytr):.4f}  (거의 1.0 = train 을 외움)")
    print(f"  test  R2 : {r2_score(yte, p):.4f}")
    print(f"  test RMSE: {np.sqrt(mean_squared_error(yte, p)):.4f}")
    print(f"  test MAE : {mean_absolute_error(yte, p):.4f}")
    print(f"  과대적합 신호(train-test R2): {reg.score(Xtr,ytr)-r2_score(yte,p):+.4f}")

# ───────────────────────────────────────────────────────────────────────────
# §06: 회귀트리 성능 향상 — 깊이·리프·분할기준 튜닝(GridSearchCV)
# ───────────────────────────────────────────────────────────────────────────
def s06_reg_tuned():
    """깊이를 제한하고 리프 최소 샘플을 키우면 회귀트리의 일반화가 살아난다.
    먼저 max_depth 를 훑어 곡선을 보고, GridSearchCV 로 최적 조합을 골라
    test R2 가 baseline 대비 얼마나 오르는지 확인한다(성능 향상 전→후)."""
    df = load_white_wine()
    X = df.drop("quality", axis=1).values
    y = df["quality"].values
    Xtr, Xte = X[:3749], X[3749:]
    ytr, yte = y[:3749], y[3749:]

    base = DecisionTreeRegressor(random_state=SEED).fit(Xtr, ytr)
    base_r2 = r2_score(yte, base.predict(Xte))

    depths = [2, 3, 4, 5, 6, 8, 10, None]
    tr_r2, te_r2 = [], []
    print(f"{'max_depth':>9} | {'train R2':>9} | {'test R2':>9}")
    print("-" * 34)
    for d in depths:
        r = DecisionTreeRegressor(max_depth=d, random_state=SEED).fit(Xtr, ytr)
        tr, te = r.score(Xtr, ytr), r.score(Xte, yte)
        tr_r2.append(tr); te_r2.append(te)
        print(f"{str(d):>9} | {tr:9.4f} | {te:9.4f}")

    param_grid = {
        "max_depth": [3, 4, 5, 6, 7, 8],
        "min_samples_leaf": [1, 5, 10, 20, 50],
        "min_samples_split": [2, 10, 20],
        "max_features": [None, "sqrt", 0.7],
    }
    gs = GridSearchCV(DecisionTreeRegressor(random_state=SEED),
                      param_grid, cv=5, scoring="r2", n_jobs=1)
    gs.fit(Xtr, ytr)
    best = gs.best_estimator_
    tuned_r2 = r2_score(yte, best.predict(Xte))

    print(f"\nbest params : {gs.best_params_}")
    print(f"best cv R2   : {gs.best_score_:.4f}  (5겹 교차검증 평균)")
    print("\n[성능 향상 전 → 후 — test 기준]")
    print(f"  baseline(제약 없음) test R2 : {base_r2:.4f}  (깊이 {base.get_depth()})")
    print(f"  튜닝 회귀트리       test R2 : {tuned_r2:.4f}  (깊이 {best.get_depth()})")
    print(f"  R2 개선폭 : {tuned_r2-base_r2:+.4f}")
    print(f"  baseline RMSE {np.sqrt(mean_squared_error(yte, base.predict(Xte))):.4f}"
          f" → 튜닝 RMSE {np.sqrt(mean_squared_error(yte, best.predict(Xte))):.4f}")

    xs = range(len(depths))
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(xs, tr_r2, "o-", color="#5B9BD5", label="train R2")
    ax.plot(xs, te_r2, "s-", color="#E8875A", label="test R2")
    ax.axhline(tuned_r2, color="#52A97E", lw=1.6, ls="--", label=f"튜닝 후 test R2={tuned_r2:.3f}")
    ax.set_xticks(list(xs)); ax.set_xticklabels([str(d) for d in depths])
    ax.set_xlabel("max_depth"); ax.set_ylabel("R2")
    ax.set_title("회귀트리 깊이↑ → train R2는 1.0, test R2는 정점 후 하락")
    ax.legend(fontsize=8); fig.tight_layout()
    fig.savefig(CHARTS / "ch_reg_depth.png", dpi=110); plt.close(fig)
    print("[chart] ch_reg_depth.png 저장")

# ───────────────────────────────────────────────────────────────────────────
# §07: 회귀트리 Feature Importance — 와인 품질을 가르는 특성
# ───────────────────────────────────────────────────────────────────────────
def s07_reg_importance():
    """튜닝한 회귀트리의 feature_importances_ 로 와인 품질에 가장 큰 영향을 주는
    특성을 찾는다. 과제 답안(NN 가중치 기준)에서는 alcohol 이 1등이었다 — 트리도 같은가?"""
    df = load_white_wine()
    feat = list(df.drop("quality", axis=1).columns)
    X = df.drop("quality", axis=1).values
    y = df["quality"].values
    Xtr = X[:3749]; ytr = y[:3749]
    reg = DecisionTreeRegressor(max_depth=6, min_samples_leaf=20, random_state=SEED).fit(Xtr, ytr)

    imp = reg.feature_importances_
    order = np.argsort(imp)[::-1]
    names = np.array(feat)
    print("[회귀트리 특성 중요도 — 내림차순]")
    for i in order:
        bar = "#" * int(round(imp[i] * 40))
        print(f"  {names[i]:<22} {imp[i]:.4f}  {bar}")
    root_feat = feat[reg.tree_.feature[0]]
    print(f"\n루트 노드가 처음 가른 특성: {root_feat}")
    print(f"가장 중요한 특성        : {names[order[0]]} ({imp[order[0]]:.4f})")

    top = order[:8][::-1]
    fig, ax = plt.subplots(figsize=(6.6, 4))
    ax.barh([names[i] for i in top], [imp[i] for i in top], color="#9178C4")
    ax.set_xlabel("중요도(feature_importances_)")
    ax.set_title("화이트와인 품질 회귀 — 상위 8개 특성")
    fig.tight_layout(); fig.savefig(CHARTS / "ch_importance_reg.png", dpi=110); plt.close(fig)
    print("[chart] ch_importance_reg.png 저장")

if __name__ == "__main__":
    run_section("00_two_tasks", s00_two_tasks)
    run_section("01_clf_baseline", s01_clf_baseline)
    run_section("02_clf_depth", s02_clf_depth)
    run_section("03_clf_gridsearch", s03_clf_gridsearch)
    run_section("04_clf_importance", s04_clf_importance)
    run_section("05_reg_baseline", s05_reg_baseline)
    run_section("06_reg_tuned", s06_reg_tuned)
    run_section("07_reg_importance", s07_reg_importance)
    print("\n완료: logs/*.txt, charts/*.png 생성")
