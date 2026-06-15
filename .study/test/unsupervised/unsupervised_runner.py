# unsupervised_runner.py
# 머신러닝 Day7 (0605) — 비지도학습 섹션별 테스트 실행기
# 실행: c:\_proj\python_workspace\.venv\Scripts\python.exe unsupervised_runner.py
# 결과: logs/{섹션명}.txt 저장 + 터미널 출력,  charts/*.png 생성
# 데이터: sklearn 내장 load_iris(k-means) · 소규모 장바구니 거래 리스트(연관규칙)
#   ※ 0605-s 노트북은 PyTorch 구현(직접 cdist/argmin) + UCI iris CSV + groceries 거래.
#     여기서는 sklearn.cluster.KMeans 로 같은 흐름을 재현(고정 시드 42)하고,
#     연관규칙은 mlxtend 미설치 환경이라 작은 거래 리스트에 apriori 를 직접 구현(§16-C 사유 명시).

import sys, io, pathlib
from contextlib import redirect_stdout
from itertools import combinations

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import (silhouette_score, silhouette_samples,
                             adjusted_rand_score, normalized_mutual_info_score)
import pandas as pd

HERE = pathlib.Path(__file__).parent
LOGS = HERE / "logs"; LOGS.mkdir(exist_ok=True)
CHARTS = HERE / "charts"; CHARTS.mkdir(exist_ok=True)
SEED = 42

C_BLUE, C_ORANGE, C_GREEN, C_PURPLE = "#5B9BD5", "#E8875A", "#52A97E", "#9178C4"


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


# 공용: 표준화된 iris X 와 정답 y
def _iris_scaled():
    iris = load_iris()
    X = StandardScaler().fit_transform(iris.data)
    return iris, X, iris.target


# ── §00: 정답(y)을 가린다 — 지도 vs 비지도 ────────────────────────────────
def s00_no_labels():
    """지금까지(회귀·분류)는 정답 y 로 학습했다. 비지도학습은 y 없이 X 만으로 구조를 찾는다.
    iris 에서 y 를 가리고 X 만 남았을 때 무엇이 남는지 확인한다."""
    iris = load_iris()
    X, y = iris.data, iris.target
    print(f"iris X shape: {X.shape}  (특성 4개)")
    print(f"정답 y 가 있을 때(지도학습): 라벨 {np.unique(y)} = {list(iris.target_names)}")
    print("정답 y 를 가리면(비지도학습): 남는 것은 X 좌표뿐 — '몇 종인지'도 모른다.")
    print(f"  X 첫 3행:\n{np.round(X[:3], 2)}")
    print("→ 비지도학습의 질문: 정답 없이, 가까운 점끼리 묶을 수 있는가?")


# ── §01: k-means 한 번 — 중심·할당·반복 ───────────────────────────────────
def s01_kmeans_once():
    """KMeans(k=3) 를 표준화 iris 에 적용. 중심 3개, 각 점의 클러스터 할당,
    수렴까지 반복 횟수(n_iter_)와 inertia(중심까지 거리 제곱합)를 확인한다."""
    iris, X, y = _iris_scaled()
    km = KMeans(n_clusters=3, random_state=SEED, n_init=10).fit(X)
    labels = km.labels_
    print(f"클러스터 중심 shape: {km.cluster_centers_.shape}  (3개 중심 × 4특성, 표준화 공간)")
    uniq, cnt = np.unique(labels, return_counts=True)
    print("클러스터별 점 개수:")
    for c, n in zip(uniq, cnt):
        print(f"  클러스터 {c}: {n}개")
    print(f"수렴까지 반복 횟수 n_iter_ = {km.n_iter_}")
    print(f"inertia(중심까지 거리 제곱합) = {km.inertia_:.3f}")
    print(f"실제 품종별 개수(참고): {dict(zip(iris.target_names, np.bincount(y)))}")


# ── §02: k 는 몇 개? — 엘보우(inertia) ────────────────────────────────────
def s02_elbow():
    """정답이 없으니 k 를 알 수 없다. k=1..8 로 inertia 를 재면 보통 어느 지점에서
    감소폭이 꺾인다(엘보우). 꺾이는 k 가 클러스터 개수의 후보다."""
    iris, X, y = _iris_scaled()
    ks = list(range(1, 9))
    inertias = []
    print(f"{'k':>3} | {'inertia':>10} | {'감소폭Δ':>10}")
    print("-" * 32)
    prev = None
    for k in ks:
        km = KMeans(n_clusters=k, random_state=SEED, n_init=10).fit(X)
        inertias.append(km.inertia_)
        d = "" if prev is None else f"{prev - km.inertia_:10.2f}"
        print(f"{k:>3} | {km.inertia_:10.3f} | {d:>10}")
        prev = km.inertia_
    # 2차 차분으로 꺾임(엘보우) 위치 추정
    diffs = np.diff(inertias)               # 1차: 감소폭(음수)
    second = np.diff(diffs)                 # 2차: 감소폭의 변화
    elbow_k = ks[int(np.argmax(second)) + 1]
    print(f"\n2차 차분 최대 → 엘보우 추정 k = {elbow_k}")

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(ks, inertias, "o-", color=C_BLUE, lw=2)
    ax.axvline(elbow_k, color=C_ORANGE, ls="--", lw=1.5, label=f"엘보우 k={elbow_k}")
    ax.set_xlabel("클러스터 개수 k"); ax.set_ylabel("inertia (군집 내 거리 제곱합)")
    ax.set_title("엘보우 방법 — inertia 가 꺾이는 k")
    ax.legend(); fig.tight_layout()
    fig.savefig(CHARTS / "ch_elbow.png", dpi=110); plt.close(fig)
    print("[chart] ch_elbow.png 저장")


# ── §03: 실루엣 점수 — 분리/응집을 한 숫자로 ──────────────────────────────
def s03_silhouette():
    """엘보우는 눈대중이다. 실루엣 점수는 '같은 군집은 가깝고 다른 군집은 먼' 정도를
    -1~1 한 숫자로 잰다. k=2..8 에서 최댓값을 주는 k 가 또 하나의 후보다."""
    iris, X, y = _iris_scaled()
    ks = list(range(2, 9))
    scores = []
    print(f"{'k':>3} | {'silhouette':>11}")
    print("-" * 18)
    for k in ks:
        km = KMeans(n_clusters=k, random_state=SEED, n_init=10).fit(X)
        s = silhouette_score(X, km.labels_)
        scores.append(s)
        print(f"{k:>3} | {s:11.4f}")
    best_k = ks[int(np.argmax(scores))]
    print(f"\n실루엣 최댓값 → best k = {best_k} (score={max(scores):.4f})")

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(ks, scores, "s-", color=C_GREEN, lw=2)
    ax.axvline(best_k, color=C_ORANGE, ls="--", lw=1.5, label=f"best k={best_k}")
    ax.set_xlabel("클러스터 개수 k"); ax.set_ylabel("평균 실루엣 점수")
    ax.set_title("실루엣 점수 — 클수록 군집이 잘 분리")
    ax.legend(); fig.tight_layout()
    fig.savefig(CHARTS / "ch_silhouette.png", dpi=110); plt.close(fig)
    print("[chart] ch_silhouette.png 저장")


# ── §04: 군집이 실제 품종과 얼마나 맞나 — crosstab · ARI · NMI ────────────
def s04_vs_truth():
    """비지도라 군집 번호와 품종 번호는 의미가 다르다. 교차표로 대응을 보고,
    번호 순서에 무관한 ARI·NMI 로 '실제 품종과 얼마나 맞는지'를 잰다."""
    iris, X, y = _iris_scaled()
    km = KMeans(n_clusters=3, random_state=SEED, n_init=10).fit(X)
    labels = km.labels_
    ct = pd.crosstab(pd.Series(iris.target_names[y], name="실제품종"),
                     pd.Series(labels, name="클러스터"))
    print("교차표 (실제 품종 × 클러스터):")
    print(ct.to_string())
    ari = adjusted_rand_score(y, labels)
    nmi = normalized_mutual_info_score(y, labels)
    # 군집을 다수결 품종에 매핑한 '정확도'
    mapping = {}
    for c in np.unique(labels):
        mapping[c] = np.bincount(y[labels == c]).argmax()
    mapped = np.array([mapping[c] for c in labels])
    acc = (mapped == y).mean()
    print(f"\nAdjusted Rand Index(ARI) = {ari:.4f}  (1이면 완전 일치, 0이면 우연 수준)")
    print(f"Normalized Mutual Info(NMI) = {nmi:.4f}")
    print(f"다수결 매핑 정확도 = {acc:.4f}  ({int(acc*len(y))}/{len(y)})")
    print("→ 정답을 한 번도 안 봤는데, 군집이 품종과 상당히 겹친다.")


# ── §05: 군집을 2D로 — PCA 산점도 ─────────────────────────────────────────
def s05_scatter():
    """4차원은 그릴 수 없다. PCA 로 2D 로 내려, k-means 군집과 실제 품종을
    나란히 그려 어디서 갈리는지 본다."""
    iris, X, y = _iris_scaled()
    km = KMeans(n_clusters=3, random_state=SEED, n_init=10).fit(X)
    labels = km.labels_
    pca = PCA(n_components=2, random_state=SEED)
    P = pca.fit_transform(X)
    cen = pca.transform(km.cluster_centers_)
    print(f"PCA 2D 설명 분산 비율: {np.round(pca.explained_variance_ratio_, 4)} "
          f"(합 {pca.explained_variance_ratio_[:2].sum():.4f})")

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
    for c in np.unique(labels):
        m = labels == c
        axes[0].scatter(P[m, 0], P[m, 1], s=18, alpha=0.8, label=f"군집 {c}")
    axes[0].scatter(cen[:, 0], cen[:, 1], c="k", marker="X", s=130, label="중심")
    axes[0].set_title("k-means 군집 (정답 안 봄)")
    axes[0].set_xlabel("PC1"); axes[0].set_ylabel("PC2"); axes[0].legend(fontsize=8)
    for t in range(3):
        m = y == t
        axes[1].scatter(P[m, 0], P[m, 1], s=18, alpha=0.8, label=iris.target_names[t])
    axes[1].set_title("실제 품종 (정답)")
    axes[1].set_xlabel("PC1"); axes[1].set_ylabel("PC2"); axes[1].legend(fontsize=8)
    fig.tight_layout(); fig.savefig(CHARTS / "ch_scatter.png", dpi=110); plt.close(fig)
    print("[chart] ch_scatter.png 저장")


# ── §06: 다른 비지도 — 연관규칙(장바구니 분석) ────────────────────────────
def s06_association():
    """k-means 외의 비지도학습. 거래 묶음에서 'A 사면 B 산다' 규칙을 찾는다.
    지지도(support)·신뢰도(confidence)·향상도(lift)를 작은 거래 리스트에서 직접 계산한다.
    (mlxtend 미설치 → apriori 를 직접 구현)"""
    # 작은 장바구니 거래 (0605-s groceries 흐름을 축소한 예시)
    transactions = [
        {"우유", "빵", "버터"},
        {"우유", "빵"},
        {"우유", "기저귀", "맥주", "달걀"},
        {"빵", "버터", "기저귀", "맥주"},
        {"우유", "빵", "버터", "기저귀"},
        {"맥주", "기저귀"},
        {"우유", "빵", "버터"},
        {"빵", "버터"},
        {"우유", "기저귀", "맥주"},
        {"빵", "달걀"},
    ]
    N = len(transactions)
    items = sorted({i for t in transactions for i in t})
    print(f"거래 수 N = {N},  품목 = {items}")

    def support(itemset):
        s = set(itemset)
        cnt = sum(1 for t in transactions if s <= t)
        return cnt / N

    MIN_SUP = 0.2
    # 1-itemset 빈발
    freq = {frozenset([i]): support([i]) for i in items}
    freq = {k: v for k, v in freq.items() if v >= MIN_SUP}
    all_freq = dict(freq)
    # 2,3-itemset (apriori: 빈발 항목 조합만)
    base_items = sorted({next(iter(k)) for k in freq})
    for size in (2, 3):
        cands = [frozenset(c) for c in combinations(base_items, size)]
        level = {c: support(c) for c in cands}
        level = {k: v for k, v in level.items() if v >= MIN_SUP}
        all_freq.update(level)
        if not level:
            break
    print(f"\n빈발 itemset (support>={MIN_SUP}): {len(all_freq)}개")
    for s, v in sorted(all_freq.items(), key=lambda kv: -kv[1]):
        print(f"  {sorted(s)}  support={v:.2f}")

    # 규칙 생성: A -> B
    MIN_CONF = 0.6
    rules = []
    for itemset, sup in all_freq.items():
        if len(itemset) < 2:
            continue
        for r in range(1, len(itemset)):
            for ante in combinations(sorted(itemset), r):
                ante = frozenset(ante)
                cons = itemset - ante
                conf = sup / support(ante)
                lift = conf / support(cons)
                if conf >= MIN_CONF:
                    rules.append((ante, cons, sup, conf, lift))
    rules.sort(key=lambda x: -x[4])
    print(f"\n연관규칙 (confidence>={MIN_CONF}), lift 내림차순:")
    print(f"{'규칙':<22}{'support':>9}{'confidence':>12}{'lift':>8}")
    print("-" * 52)
    for ante, cons, sup, conf, lift in rules:
        rule = f"{{{','.join(sorted(ante))}}}->{{{','.join(sorted(cons))}}}"
        print(f"{rule:<22}{sup:>9.2f}{conf:>12.2f}{lift:>8.2f}")

    best = rules[0]
    print(f"\n최고 향상도 규칙: {{{','.join(sorted(best[0]))}}} -> {{{','.join(sorted(best[1]))}}}")
    print(f"  lift={best[4]:.2f} (>1 → 함께 살 확률이 우연보다 {best[4]:.2f}배)")

    # 차트: 규칙 lift 막대
    fig, ax = plt.subplots(figsize=(7, 4.2))
    names = [f"{{{','.join(sorted(a))}}}→{{{','.join(sorted(c))}}}" for a, c, *_ in rules]
    lifts = [r[4] for r in rules]
    ypos = np.arange(len(names))
    colors = [C_GREEN if l >= 1 else C_ORANGE for l in lifts]
    ax.barh(ypos, lifts, color=colors)
    ax.axvline(1.0, color="#999", ls="--", lw=1)
    ax.set_yticks(ypos); ax.set_yticklabels(names, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("향상도(lift)"); ax.set_title("연관규칙 향상도 — 점선(lift=1)=우연")
    fig.tight_layout(); fig.savefig(CHARTS / "ch_rules.png", dpi=110); plt.close(fig)
    print("[chart] ch_rules.png 저장")


# ── §07: 지도 vs 비지도 정리 ──────────────────────────────────────────────
def s07_summary():
    """오늘 다룬 비지도학습을 지도학습과 한 표로 정리한다."""
    rows = [
        ("입력", "X + 정답 y", "X 만 (정답 없음)"),
        ("목표", "y 예측(회귀/분류)", "구조 발견(군집/규칙)"),
        ("예시", "LinearRegression·RandomForest", "KMeans·연관규칙"),
        ("평가", "R2·정확도·정밀도", "inertia·실루엣·(ARI는 정답 있을 때만)"),
        ("정답 비교", "항상 가능", "보통 불가 — 오늘은 iris라 예외적으로 가능"),
    ]
    w = 12
    print(f"{'항목':<{w}}{'지도학습':<32}{'비지도학습'}")
    print("-" * 76)
    for k, a, b in rows:
        print(f"{k:<{w}}{a:<32}{b}")


# ── §08: lift 손계산 — 기대(독립) vs 실제 ─────────────────────────────────
def s08_lift_by_hand():
    """연관규칙의 세 숫자를 작은 거래로 손계산해 직관을 세운다.
    핵심 질문 둘:
      (1) "둘이 아무 상관 없다면 10%만 같이 사야 하는데 왜 15%나 같이 샀지?"
          → lift = 실제 동시구매율 / 기대(독립) 동시구매율 = P(A∩B)/(P(A)P(B))
      (2) "조건을 만족한 사람 중 고작 9%만 샀는데 왜 의미가 있지?"
          → confidence 가 낮아도 결과 상품 B의 단독 지지도 P(B)가 더 작으면 lift>1.
    값은 모두 거래 리스트를 직접 세어 계산한다(하드코딩 없음)."""
    # 우유·요거트 직관용 거래 20건: 우유 10건(P=0.5), 요거트 4건(P=0.2),
    # 우유∩요거트 3건(실제 0.15). 기대(독립)는 0.5*0.2=0.10.
    T1 = [
        {"우유", "요거트"}, {"우유", "요거트"}, {"우유", "요거트"},
        {"우유"}, {"우유"}, {"우유"}, {"우유"}, {"우유"}, {"우유"}, {"우유"},
        {"요거트"},
        {"빵"}, {"빵"}, {"빵"}, {"빵"}, {"빵"}, {"빵"}, {"빵"}, {"빵"}, {"빵"},
    ]
    N1 = len(T1)

    def sup(itemset, T):
        s = set(itemset)
        return sum(1 for t in T if s <= t) / len(T)

    pA = sup({"우유"}, T1)
    pB = sup({"요거트"}, T1)
    pAB = sup({"우유", "요거트"}, T1)
    expected = pA * pB
    conf = pAB / pA
    lift = pAB / expected
    print("[직관 1] 우유 → 요거트  (거래 N =", N1, ")")
    print(f"  P(우유)        = {pA:.2f}   (우유가 든 거래 비율)")
    print(f"  P(요거트)      = {pB:.2f}   (요거트가 든 거래 비율)")
    print(f"  기대 동시구매  = P(우유)*P(요거트) = {pA:.2f}*{pB:.2f} = {expected:.2f}  (= 10%)")
    print(f"  실제 동시구매  = P(우유∩요거트)     = {pAB:.2f}  (= 15%)")
    print(f"  confidence     = P(우유∩요거트)/P(우유) = {pAB:.2f}/{pA:.2f} = {conf:.2f}")
    print(f"  lift           = 실제/기대 = {pAB:.2f}/{expected:.2f} = {lift:.2f}")
    print('  → "상관 없다면 10%만 같이 사야 하는데 15%나 샀다" = 기대보다', f"{lift:.1f}배.")
    print(f"  부호 점검: 기호는 P(A∪B)로 쓰지만(두 상품을 한 바구니 set으로 합침),")
    print(f"            실제로 세는 것은 둘을 '동시에' 산 거래수 = 교집합 P(A∩B).")

    # 직관 2: confidence 는 낮은데 lift 는 큰 경우.
    # A=만두, B=굴소스. 만두 거래는 많고(자주 사니 conf 분모 큼) → conf 낮음.
    # 그러나 굴소스 단독 지지도 P(B)가 아주 작아 → lift 큼.
    T2 = (
        [{"만두", "굴소스"}] * 4        # 동시구매 4건
        + [{"만두"}] * 36             # 만두만 36건 → 만두 총 40건
        + [{"라면"}] * 56             # 잡음(굴소스·만두 없음)
    )  # 총 96건. 굴소스 총 4건 → P(B)≈0.042
    N2 = len(T2)
    pA2 = sup({"만두"}, T2)
    pB2 = sup({"굴소스"}, T2)
    pAB2 = sup({"만두", "굴소스"}, T2)
    conf2 = pAB2 / pA2
    lift2 = pAB2 / (pA2 * pB2)
    print("\n[직관 2] 만두 → 굴소스  (거래 N =", N2, ")")
    print(f"  P(만두)   = {pA2:.4f}")
    print(f"  P(굴소스) = {pB2:.4f}   (단독으로는 거의 안 팔리는 희귀 상품)")
    print(f"  confidence = P(만두∩굴소스)/P(만두) = {pAB2:.4f}/{pA2:.4f} = {conf2:.4f}  (≈{conf2*100:.0f}%)")
    print(f"  lift = confidence / P(굴소스) = {conf2:.4f}/{pB2:.4f} = {lift2:.2f}")
    print(f'  → "조건 만족한 사람 중 {conf2*100:.0f}%만 샀는데 왜 의미?" : 분모 P(굴소스)={pB2:.3f}가')
    print(f"     워낙 작아, 낮은 confidence라도 lift는 {lift2:.1f}배로 커진다.")

    # 차트: 기대(독립) vs 실제 동시구매율 막대 — 직관 1
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(["기대(독립)\nP(우유)·P(요거트)", "실제\nP(우유∩요거트)"],
                  [expected, pAB], color=[C_ORANGE, C_GREEN], width=0.55)
    ax.axhline(expected, color="#999", ls="--", lw=1)
    for b, v in zip(bars, [expected, pAB]):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.004, f"{v:.2f}",
                ha="center", va="bottom", fontsize=11)
    ax.set_ylim(0, max(expected, pAB) * 1.4)
    ax.set_ylabel("동시 구매 비율")
    ax.set_title(f"우유→요거트 : 기대 {expected:.2f} vs 실제 {pAB:.2f}  (lift={lift:.2f})")
    fig.tight_layout(); fig.savefig(CHARTS / "ch_lift_hand.png", dpi=110); plt.close(fig)
    print("\n[chart] ch_lift_hand.png 저장")


# ── §09: k-means 초기 중심 — random vs k-means++ ──────────────────────────
def s09_init_compare():
    """'실제 컴퓨터는 처음 중심점을 어떻게 잡나?' 두 방식을 직접 비교한다.
    random: 데이터 점 중 k개를 무작위로 골라 시작 → 운에 따라 나쁜 국소최솟값에 갇힐 수 있다.
    k-means++: 첫 중심 뒤로 '멀리 떨어진 점일수록 높은 확률'로 다음 중심을 뽑아 퍼뜨린다.
    같은 데이터에 n_init=1(=초기화 한 번만)로 여러 시드를 돌려 수렴 inertia·반복수를 비교한다."""
    iris, X, y = _iris_scaled()
    seeds = list(range(10))

    def run(init):
        recs = []
        for s in seeds:
            km = KMeans(n_clusters=3, init=init, n_init=1, random_state=s).fit(X)
            recs.append((km.inertia_, km.n_iter_))
        return recs

    rand = run("random")
    pp = run("k-means++")
    rand_in = [r[0] for r in rand]; rand_it = [r[1] for r in rand]
    pp_in = [r[0] for r in pp]; pp_it = [r[1] for r in pp]

    print("초기화 1회(n_init=1)로 시드 10개씩 — 수렴 inertia / 반복수")
    print(f"{'seed':>4} | {'random inertia':>15} {'iter':>5} | {'k-means++ inertia':>18} {'iter':>5}")
    print("-" * 60)
    for s, r, p in zip(seeds, rand, pp):
        print(f"{s:>4} | {r[0]:>15.3f} {r[1]:>5} | {p[0]:>18.3f} {p[1]:>5}")
    print("-" * 60)
    print(f"{'평균':>4} | {np.mean(rand_in):>15.3f} {np.mean(rand_it):>5.1f} | "
          f"{np.mean(pp_in):>18.3f} {np.mean(pp_it):>5.1f}")
    print(f"{'최악':>4} | {np.max(rand_in):>15.3f} {'':>5} | {np.max(pp_in):>18.3f} {'':>5}")
    print(f"{'최선':>4} | {np.min(rand_in):>15.3f} {'':>5} | {np.min(pp_in):>18.3f} {'':>5}")
    bad_rand = sum(1 for v in rand_in if v > min(pp_in) + 1e-6)
    print(f"\nrandom 초기화가 최선 inertia({min(pp_in):.3f})보다 나쁜 시드 수: "
          f"{bad_rand}/{len(seeds)}")
    print(f"k-means++ 평균 반복수 {np.mean(pp_it):.1f} vs random 평균 {np.mean(rand_it):.1f}")
    print("→ k-means++는 중심을 멀리 퍼뜨려 시작하므로 시드별 inertia가 더 고르고,")
    print("  나쁜 국소최솟값에 갇히는 빈도가 낮다. sklearn 기본값이 'k-means++'인 이유.")

    # 차트: 시드별 수렴 inertia 점 비교
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.scatter(seeds, rand_in, color=C_ORANGE, s=50, label="random", zorder=3)
    ax.scatter(seeds, pp_in, color=C_GREEN, s=50, marker="s",
               label="k-means++", zorder=3)
    ax.axhline(min(pp_in), color="#999", ls="--", lw=1, label=f"최선 inertia {min(pp_in):.1f}")
    ax.set_xlabel("random_state (초기화 시드)")
    ax.set_ylabel("수렴 inertia (작을수록 좋음)")
    ax.set_title("초기화 방식별 수렴 inertia — random vs k-means++ (n_init=1)")
    ax.legend(fontsize=9); fig.tight_layout()
    fig.savefig(CHARTS / "ch_init.png", dpi=110); plt.close(fig)
    print("\n[chart] ch_init.png 저장")


if __name__ == "__main__":
    run_section("00_no_labels", s00_no_labels)
    run_section("01_kmeans_once", s01_kmeans_once)
    run_section("02_elbow", s02_elbow)
    run_section("03_silhouette", s03_silhouette)
    run_section("04_vs_truth", s04_vs_truth)
    run_section("05_scatter", s05_scatter)
    run_section("06_association", s06_association)
    run_section("08_lift_by_hand", s08_lift_by_hand)
    run_section("09_init_compare", s09_init_compare)
    run_section("07_summary", s07_summary)
    print("\n완료: logs/*.txt, charts/*.png 생성")
