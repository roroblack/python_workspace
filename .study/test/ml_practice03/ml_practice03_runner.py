# ml_practice03_runner.py
# 머신러닝 실습3(과제) — 문제마다 다른 분류기: SVM 글자/우편번호 · KNN 유방암 · 나이브베이즈 스팸
# 실행: c:\_proj\python_workspace\.venv\Scripts\python.exe ml_practice03_runner.py
# 결과: logs/{섹션명}.txt 저장 + 터미널 출력, charts/*.png 생성
#
# 데이터(실제 CSV 우선 — ../ml_workspace/from_colab/0529-s):
#   · data/opt_letterdata.csv  (UCI Letter Recognition, 20000행)  → SVM 다중클래스
#   · data/wisc_data.csv       (Wisconsin 유방암 진단, 569행)     → KNN 이진분류
#   · content/data/국가데이터처_나라통계_우편번호_20211110.csv (EUC-KR) → 우편번호 조회/분류
#   · 스팸: SMS Spam Collection 원본은 인터넷 다운로드(노트북 방식)라 오프라인 재현을 위해
#     sklearn 내장 20newsgroups 2개 주제(텍스트 스팸형 이진분류 대체)로 작성.
#     사유: 실습 노트북은 requests 로 UCI zip 다운로드 → 오프라인/시드 재현 불가. 텍스트
#     조건부독립 가정·CountVectorizer·라플라스 스무딩의 학습 목적은 동일하게 관찰 가능(§16-C 우선순위2).
#   ※ SVM/KNN 은 실습 노트북이 PyTorch 재구현이지만, 같은 알고리즘을 sklearn SVC/
#     KNeighborsClassifier 로 돌려 '스케일링 유무 차이'를 또렷이 관찰(워크스페이스 sklearn 1.8.0).

import sys, io, pathlib
from contextlib import redirect_stdout

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# 차트 한글 렌더링 (Windows 기본 한글 폰트) + 마이너스 깨짐 방지
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.datasets import fetch_20newsgroups
from sklearn.metrics import (accuracy_score, confusion_matrix, classification_report,
                             recall_score, precision_score)

HERE = pathlib.Path(__file__).parent
LOGS = HERE / "logs"; LOGS.mkdir(exist_ok=True)
CHARTS = HERE / "charts"; CHARTS.mkdir(exist_ok=True)
SEED = 42

DATA = pathlib.Path(r"c:\_proj\ml_workspace\from_colab\0529-s")
LETTER_CSV = DATA / "data" / "opt_letterdata.csv"
WISC_CSV = DATA / "data" / "wisc_data.csv"
POST_CSV = DATA / "content" / "data" / "국가데이터처_나라통계_우편번호_20211110.csv"


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


# ── §00: 세 과제를 가르는 질문 — 데이터 성격 진단 ─────────────────────────
def s00_three_problems():
    """SVM·KNN·NB 세 과제의 데이터를 한자리에 놓고 '무엇을 맞히는 문제인가'를 가른다.
    클래스 수·특성 수·특성 성격(연속/텍스트)이 분류기 선택의 첫 갈림길."""
    letter = pd.read_csv(LETTER_CSV)
    wisc = pd.read_csv(WISC_CSV)
    print("[글자 인식 — SVM]   opt_letterdata.csv")
    print(f"  행 {letter.shape[0]} · 특성 {letter.shape[1]-1}개(전부 정수형 픽셀통계) · "
          f"클래스 {letter['letter'].nunique()}개 (A~Z 다중클래스)")
    print(f"  특성 값 범위 예: xbox {letter['xbox'].min()}~{letter['xbox'].max()}, "
          f"y2bar {letter['y2bar'].min()}~{letter['y2bar'].max()}  (특성마다 범위 다름)")
    print()
    print("[유방암 진단 — KNN] wisc_data.csv")
    print(f"  행 {wisc.shape[0]} · 특성 {wisc.shape[1]-2}개(연속 실수) · "
          f"클래스 {wisc['diagnosis'].nunique()}개 {sorted(wisc['diagnosis'].unique())} (이진)")
    print(f"  특성 스케일 차이 예: area_mean 평균 {wisc['area_mean'].mean():.1f} vs "
          f"smoothness_mean 평균 {wisc['smoothness_mean'].mean():.4f}  (약 {wisc['area_mean'].mean()/wisc['smoothness_mean'].mean():.0f}배)")
    print()
    print("[스팸 분류 — NB]    텍스트(단어 출현 0/1) → 고차원 희소 특성, 이진 클래스")
    print("  → 세 과제는 '연속/정수/텍스트' 라는 특성 성격이 전부 다르다. 분류기도 달라야 한다.")


# ── §01: SVM 글자 분류 — 스케일링을 안 하면? ─────────────────────────────
def s01_svm_letter_scaling():
    """SVM(RBF)은 거리 기반이라 특성 스케일에 민감하다. 같은 SVC 를 '스케일 없이' vs
    'StandardScaler 적용' 으로 돌려 글자 인식 정확도가 얼마나 벌어지는지 직접 본다.
    (속도 위해 6000행 표본 — 시드 고정으로 재현 가능)"""
    df = pd.read_csv(LETTER_CSV)
    df = df.sample(n=6000, random_state=SEED).reset_index(drop=True)
    X = df.drop(columns=["letter"]).values.astype(float)
    le = LabelEncoder()
    y = le.fit_transform(df["letter"].values)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=SEED, stratify=y)

    # ① 스케일 없이 RBF SVM
    svm_raw = SVC(kernel="rbf", C=1.0, gamma="scale", random_state=SEED).fit(Xtr, ytr)
    acc_raw = accuracy_score(yte, svm_raw.predict(Xte))

    # ② StandardScaler 적용 후 동일 RBF SVM (train fit, test transform)
    sc = StandardScaler().fit(Xtr)
    svm_sc = SVC(kernel="rbf", C=1.0, gamma="scale", random_state=SEED).fit(sc.transform(Xtr), ytr)
    acc_sc = accuracy_score(yte, svm_sc.predict(sc.transform(Xte)))

    print(f"표본 {len(df)}행 · 클래스 {len(le.classes_)}개(A~Z) · train {len(Xtr)} / test {len(Xte)}")
    print(f"① RBF SVM  스케일 없음        : test 정확도 = {acc_raw:.4f}")
    print(f"② RBF SVM  StandardScaler 적용: test 정확도 = {acc_sc:.4f}")
    print(f"   차이(스케일링 효과)         : {acc_sc - acc_raw:+.4f}")

    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(["스케일 없음", "표준화 적용"], [acc_raw, acc_sc],
                  color=["#E8875A", "#52A97E"])
    ax.set_ylim(0, 1.0); ax.set_ylabel("test 정확도")
    ax.set_title(f"RBF SVM 글자 분류 — 스케일링 효과 (+{acc_sc-acc_raw:.3f})")
    for b, v in zip(bars, [acc_raw, acc_sc]):
        ax.text(b.get_x()+b.get_width()/2, v+0.01, f"{v:.3f}", ha="center")
    fig.tight_layout(); fig.savefig(CHARTS / "ch_svm_scaling.png", dpi=110); plt.close(fig)
    print("[chart] ch_svm_scaling.png 저장")


# ── §02: SVM 커널 비교 — linear vs rbf, 혼동되는 글자 ─────────────────────
def s02_svm_kernel_confusion():
    """표준화한 글자 데이터에 linear 커널과 rbf 커널을 둘 다 적용해 정확도를 비교하고,
    혼동행렬에서 '가장 많이 혼동되는 글자쌍'을 뽑는다(과제: Confusion Matrix 분석)."""
    df = pd.read_csv(LETTER_CSV).sample(n=6000, random_state=SEED).reset_index(drop=True)
    X = df.drop(columns=["letter"]).values.astype(float)
    le = LabelEncoder(); y = le.fit_transform(df["letter"].values)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=SEED, stratify=y)
    sc = StandardScaler().fit(Xtr)
    Xtr_s, Xte_s = sc.transform(Xtr), sc.transform(Xte)

    lin = SVC(kernel="linear", C=1.0, random_state=SEED).fit(Xtr_s, ytr)
    rbf = SVC(kernel="rbf", C=1.0, gamma="scale", random_state=SEED).fit(Xtr_s, ytr)
    lin_pred, rbf_pred = lin.predict(Xte_s), rbf.predict(Xte_s)
    acc_lin, acc_rbf = accuracy_score(yte, lin_pred), accuracy_score(yte, rbf_pred)
    print(f"linear 커널 test 정확도 = {acc_lin:.4f}")
    print(f"rbf    커널 test 정확도 = {acc_rbf:.4f}   (비선형 경계가 더 잘 맞음)")

    def top_confusions(y_true, y_pred, k=3):
        cm = confusion_matrix(y_true, y_pred)
        np.fill_diagonal(cm, 0)
        pairs = []
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                if cm[i, j] > 0:
                    pairs.append((le.classes_[i], le.classes_[j], int(cm[i, j])))
        pairs.sort(key=lambda t: -t[2])
        return pairs[:k]

    print("\n[linear] 가장 많이 혼동된 글자쌍 TOP3 (실제→예측, 횟수):")
    for a, b, c in top_confusions(yte, lin_pred):
        print(f"   {a} → {b} : {c}회")
    print("[rbf]    가장 많이 혼동된 글자쌍 TOP3 (실제→예측, 횟수):")
    for a, b, c in top_confusions(yte, rbf_pred):
        print(f"   {a} → {b} : {c}회")

    # rbf 혼동행렬 히트맵
    cm = confusion_matrix(yte, rbf_pred)
    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(cm, cmap="Greens")
    ax.set_xticks(range(26)); ax.set_xticklabels(le.classes_, fontsize=7)
    ax.set_yticks(range(26)); ax.set_yticklabels(le.classes_, fontsize=7)
    ax.set_xlabel("예측 글자"); ax.set_ylabel("실제 글자")
    ax.set_title(f"RBF SVM 혼동행렬 (정확도 {acc_rbf:.3f})")
    fig.colorbar(im, fraction=0.046)
    fig.tight_layout(); fig.savefig(CHARTS / "ch_svm_confusion.png", dpi=110); plt.close(fig)
    print("[chart] ch_svm_confusion.png 저장")


# ── §03: SVM 응용 — 우편번호 조회기(주소 → 우편번호 / 우편번호 → 주소) ──────
def s03_postcode_lookup():
    """과제3: 우편번호 분류/조회기. 시·구·동을 입력하면 우편번호를, 우편번호를 입력하면
    주소를 돌려준다. 52543건 우편 데이터(EUC-KR)를 사전(dict)으로 색인해 즉시 조회한다.
    ('분류'의 본질 = 입력을 정해진 라벨로 매핑 — 여기선 주소↔우편번호 매핑으로 구현)"""
    df = pd.read_csv(POST_CSV, encoding="euc-kr")
    print(f"우편번호 데이터: {df.shape[0]}건 · 컬럼 {list(df.columns)}")
    df = df.dropna(subset=["우편번호", "도이름", "시군구이름", "읍면동이름"])

    # 우편번호 → 대표 주소
    code_to_addr = (df.drop_duplicates("우편번호")
                      .set_index("우편번호")["전체주소"].to_dict())

    # 주소키(시 구 동) → 우편번호 목록
    def addr_key(r):
        return f"{r['도이름']} {r['시군구이름']} {r['읍면동이름']}"
    df = df.assign(_key=df.apply(addr_key, axis=1))
    addr_to_codes = df.groupby("_key")["우편번호"].apply(lambda s: sorted(int(v) for v in s.unique())).to_dict()

    print(f"색인 완료: 우편번호 {len(code_to_addr)}개, 주소키 {len(addr_to_codes)}개\n")

    print("[조회 ① 우편번호 → 주소]")
    for code in [137926, 600092]:
        print(f"   {code} → {code_to_addr.get(code, '(없음)')}")

    print("\n[조회 ② 주소(시 구 동) → 우편번호]")
    samples = list(addr_to_codes.items())[:1]
    # 실제 존재하는 키로 시연
    seoul_keys = [k for k in addr_to_codes if "서초구 서초1동" in k][:1]
    for k in seoul_keys + [samples[0][0]]:
        codes = addr_to_codes[k]
        head = codes[:5]
        print(f"   '{k}' → 우편번호 {len(codes)}개 {head}{' ...' if len(codes) > 5 else ''}")

    # 도(시도)별 우편번호 분포 차트 (분류 라벨 분포 시각화)
    by_do = df.groupby("도이름")["우편번호"].nunique().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.barh(by_do.index[::-1], by_do.values[::-1], color="#5B9BD5")
    ax.set_xlabel("우편번호 개수"); ax.set_title("시도별 우편번호 분포 (상위 10)")
    fig.tight_layout(); fig.savefig(CHARTS / "ch_postcode.png", dpi=110); plt.close(fig)
    print("\n[chart] ch_postcode.png 저장")


# ── §04: KNN 유방암 — 스케일 안 하면 거리가 망가진다 ──────────────────────
def s04_knn_scaling():
    """KNN 은 '가까운 K개 이웃'으로 분류 — 거리가 핵심이다. 유방암 데이터는 area(수백)와
    smoothness(0.x)처럼 스케일이 제각각이라, 표준화 없이는 큰 특성이 거리를 독점한다.
    스케일 유무로 정확도·재현율(recall) 차이를 본다. 암 진단은 놓치면 안 되니 recall 중요."""
    df = pd.read_csv(WISC_CSV)
    X = df.drop(columns=["id", "diagnosis"]).values.astype(float)
    y = (df["diagnosis"].values == "M").astype(int)   # 악성(M)=1, 양성(B)=0
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=SEED, stratify=y)

    knn_raw = KNeighborsClassifier(n_neighbors=5).fit(Xtr, ytr)
    p_raw = knn_raw.predict(Xte)

    sc = StandardScaler().fit(Xtr)
    knn_sc = KNeighborsClassifier(n_neighbors=5).fit(sc.transform(Xtr), ytr)
    p_sc = knn_sc.predict(sc.transform(Xte))

    print(f"유방암 진단: train {len(Xtr)} / test {len(Xte)} · 악성(M) 비율 {y.mean():.3f}")
    print(f"① KNN(k=5) 스케일 없음 : 정확도 {accuracy_score(yte,p_raw):.4f} · "
          f"악성 recall {recall_score(yte,p_raw):.4f}")
    print(f"② KNN(k=5) 표준화 적용 : 정확도 {accuracy_score(yte,p_sc):.4f} · "
          f"악성 recall {recall_score(yte,p_sc):.4f}")
    print(f"   → 표준화로 정확도 {accuracy_score(yte,p_sc)-accuracy_score(yte,p_raw):+.4f}, "
          f"recall {recall_score(yte,p_sc)-recall_score(yte,p_raw):+.4f}")
    print("\n[표준화 KNN 혼동행렬]  (행=실제 [양성,악성], 열=예측)")
    print(confusion_matrix(yte, p_sc))


# ── §05: KNN — k 선택(과소/과대적합) ─────────────────────────────────────
def s05_knn_k_sweep():
    """k(이웃 수)를 1~25 로 바꿔가며 train/test 정확도와 악성 recall 을 본다.
    k 가 너무 작으면 노이즈에 민감(과대적합), 너무 크면 경계가 뭉개진다. 최적 k 를 찾는다."""
    df = pd.read_csv(WISC_CSV)
    X = df.drop(columns=["id", "diagnosis"]).values.astype(float)
    y = (df["diagnosis"].values == "M").astype(int)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=SEED, stratify=y)
    sc = StandardScaler().fit(Xtr)
    Xtr_s, Xte_s = sc.transform(Xtr), sc.transform(Xte)

    ks = list(range(1, 26, 2))
    tr_acc, te_acc, te_rec = [], [], []
    print(f"{'k':>3} | {'train acc':>9} | {'test acc':>8} | {'악성 recall':>10}")
    print("-" * 40)
    for k in ks:
        m = KNeighborsClassifier(n_neighbors=k).fit(Xtr_s, ytr)
        a_tr = m.score(Xtr_s, ytr)
        p = m.predict(Xte_s)
        a_te = accuracy_score(yte, p); r = recall_score(yte, p)
        tr_acc.append(a_tr); te_acc.append(a_te); te_rec.append(r)
        print(f"{k:>3} | {a_tr:9.4f} | {a_te:8.4f} | {r:10.4f}")
    best_i = int(np.argmax(te_acc))
    print(f"\n최적 k = {ks[best_i]} (test 정확도 {te_acc[best_i]:.4f}, 악성 recall {te_rec[best_i]:.4f})")

    fig, ax = plt.subplots(figsize=(6.5, 4))
    ax.plot(ks, tr_acc, "o-", color="#5B9BD5", label="train 정확도")
    ax.plot(ks, te_acc, "s-", color="#E8875A", label="test 정확도")
    ax.plot(ks, te_rec, "^--", color="#9178C4", label="악성 recall")
    ax.axvline(ks[best_i], color="#52A97E", lw=1, ls=":")
    ax.set_xlabel("k (이웃 수)"); ax.set_ylabel("점수")
    ax.set_title("KNN — k에 따른 정확도/재현율 (유방암)")
    ax.legend(); fig.tight_layout()
    fig.savefig(CHARTS / "ch_knn_ksweep.png", dpi=110); plt.close(fig)
    print("[chart] ch_knn_ksweep.png 저장")


# ── §06: 나이브베이즈 스팸 — 라플라스 스무딩 sweep ────────────────────────
def s06_nb_laplace():
    """나이브베이즈는 단어 출현을 조건부독립으로 가정해 텍스트를 빠르게 분류한다.
    과제: 라플라스 스무딩 alpha 를 0/0.1/0.5/1.0 로 바꿔 정확도를 비교한다.
    데이터: 20newsgroups 2개 주제(전자제품 광고성 vs 일반)로 스팸형 이진 텍스트 분류 대체."""
    cats = ["rec.autos", "sci.electronics"]
    tr = fetch_20newsgroups(subset="train", categories=cats,
                            remove=("headers", "footers", "quotes"), random_state=SEED)
    te = fetch_20newsgroups(subset="test", categories=cats,
                            remove=("headers", "footers", "quotes"), random_state=SEED)
    vec = CountVectorizer(lowercase=True, stop_words="english",
                          token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z]+\b",
                          min_df=5, binary=True)
    Xtr = vec.fit_transform(tr.data); Xte = vec.transform(te.data)
    ytr, yte = tr.target, te.target
    print(f"텍스트 분류: train {Xtr.shape[0]} / test {Xte.shape[0]} · "
          f"단어 특성 {Xtr.shape[1]}개(고차원 희소) · 클래스 {cats}")
    print(f"\n{'Laplace(alpha)':>14} | {'Accuracy':>9}")
    print("-" * 28)
    alphas = [0.0, 0.1, 0.5, 1.0]
    accs = []
    for a in alphas:
        # alpha=0 은 log(0) 방지를 위해 BernoulliNB 가 경고하므로 force_alpha 로 그대로 적용
        nb = BernoulliNB(alpha=a if a > 0 else 1e-10, force_alpha=True).fit(Xtr, ytr)
        acc = accuracy_score(yte, nb.predict(Xte))
        accs.append(acc)
        print(f"{a:>14} | {acc:9.4f}")
    best = int(np.argmax(accs))
    print(f"\n최고 정확도: alpha={alphas[best]} → {accs[best]:.4f}  "
          f"(스무딩이 미등장 단어 확률 0 문제를 완화)")

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot([str(a) for a in alphas], accs, "o-", color="#52A97E")
    ax.set_xlabel("라플라스 스무딩 alpha"); ax.set_ylabel("test 정확도")
    ax.set_title("나이브베이즈 — 라플라스 스무딩 효과")
    for x, v in zip(range(len(alphas)), accs):
        ax.text(x, v, f"{v:.4f}", ha="center", va="bottom", fontsize=9)
    fig.tight_layout(); fig.savefig(CHARTS / "ch_nb_laplace.png", dpi=110); plt.close(fig)
    print("[chart] ch_nb_laplace.png 저장")


# ── §07: 나이브베이즈 — 정밀도/재현율 + 핵심 단어 ────────────────────────
def s07_nb_report():
    """스팸 분류는 정확도만으로 부족하다 — 정상을 스팸으로(정밀도) vs 스팸을 놓침(재현율).
    classification_report 로 클래스별 정밀도·재현율을 보고, 각 클래스 특징 단어를 확인한다."""
    cats = ["rec.autos", "sci.electronics"]
    tr = fetch_20newsgroups(subset="train", categories=cats,
                            remove=("headers", "footers", "quotes"), random_state=SEED)
    te = fetch_20newsgroups(subset="test", categories=cats,
                            remove=("headers", "footers", "quotes"), random_state=SEED)
    vec = CountVectorizer(lowercase=True, stop_words="english",
                          token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z]+\b",
                          min_df=5, binary=True)
    Xtr = vec.fit_transform(tr.data); Xte = vec.transform(te.data)
    feats = vec.get_feature_names_out()
    nb = BernoulliNB(alpha=1.0).fit(Xtr, tr.target)
    pred = nb.predict(Xte)
    print(f"정확도 = {accuracy_score(te.target, pred):.4f}")
    print(f"정밀도(macro) = {precision_score(te.target, pred, average='macro'):.4f} · "
          f"재현율(macro) = {recall_score(te.target, pred, average='macro'):.4f}")
    print("\n[classification_report]")
    print(classification_report(te.target, pred, target_names=cats, digits=3))
    print("[혼동행렬] 행=실제, 열=예측")
    print(confusion_matrix(te.target, pred))

    # 각 클래스에서 조건부확률이 높은(특징적) 단어 상위 8개
    logp = nb.feature_log_prob_   # shape (2, n_features)
    print("\n[클래스별 특징 단어 TOP8 — log P(word=1|class) 기준]")
    for ci, name in enumerate(cats):
        top = np.argsort(logp[ci])[-8:][::-1]
        print(f"   {name:>16}: {', '.join(feats[t] for t in top)}")


if __name__ == "__main__":
    run_section("00_three_problems", s00_three_problems)
    run_section("01_svm_letter_scaling", s01_svm_letter_scaling)
    run_section("02_svm_kernel_confusion", s02_svm_kernel_confusion)
    run_section("03_postcode_lookup", s03_postcode_lookup)
    run_section("04_knn_scaling", s04_knn_scaling)
    run_section("05_knn_k_sweep", s05_knn_k_sweep)
    run_section("06_nb_laplace", s06_nb_laplace)
    run_section("07_nb_report", s07_nb_report)
    print("\n완료: logs/*.txt, charts/*.png 생성")
