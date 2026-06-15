# practice07_runner.py
# 머신러닝 실습7(과제) — 장바구니 연관규칙 분석 + (선택)클러스터링 섹션별 테스트 실행기
# 실행: c:\_proj\python_workspace\.venv\Scripts\python.exe practice07_runner.py
# 결과: logs/{섹션명}.txt 저장 + 터미널 출력, charts/*.png 생성
# 데이터: ../../../../ml_workspace/from_colab/0605-s/shop_groceries.csv
#         (Groceries 거래 데이터 9835건, 169품목 — 가변 길이 한 줄 = 한 장바구니)
#   ※ 도구: mlxtend(apriori/association_rules) 사용. 설치 확인됨(0.25.0).
#     mlxtend 가 없으면 거래 리스트로 support/confidence/lift 를 직접 계산하는
#     수동 경로(s02_manual)도 함께 둬 결과가 mlxtend 와 일치함을 검증한다.
#   ※ 클러스터링은 sklearn KMeans 로 품목 동시구매 프로파일을 세그먼트한다.

import sys, io, csv, pathlib, warnings, itertools
from contextlib import redirect_stdout

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
matplotlib.rcParams['font.family'] = 'Malgun Gothic'   # Windows 기본 한글 폰트
matplotlib.rcParams['axes.unicode_minus'] = False

from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
from sklearn.cluster import KMeans

HERE = pathlib.Path(__file__).parent
LOGS = HERE / "logs"; LOGS.mkdir(exist_ok=True)
CHARTS = HERE / "charts"; CHARTS.mkdir(exist_ok=True)
CSV = pathlib.Path(r"c:/_proj/ml_workspace/from_colab/0605-s/shop_groceries.csv")
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


# ── 거래 데이터 로딩(모듈 전역에서 한 번) ─────────────────────────────────
def load_transactions():
    with CSV.open(encoding="utf-8") as f:
        txns = [[i.strip() for i in row if i.strip()] for row in csv.reader(f)]
    return [t for t in txns if t]

TXNS = load_transactions()
_te = TransactionEncoder()
_arr = _te.fit_transform(TXNS)
ONEHOT = pd.DataFrame(_arr, columns=_te.columns_)   # 9835 x 169 one-hot


# ── §00: 데이터 적재 · 거래/품목 구조 파악 ────────────────────────────────
def s00_load():
    """장바구니 데이터는 행마다 길이가 다르다(한 줄 = 한 영수증).
    전체 거래 수·품목 수·바구니 크기 분포를 먼저 확인한다."""
    sizes = [len(t) for t in TXNS]
    print(f"[데이터] {CSV.name}")
    print(f"전체 거래 수(영수증): {len(TXNS)}")
    print(f"전체 품목 수(고유)  : {ONEHOT.shape[1]}")
    print(f"바구니 크기 — 최소 {min(sizes)} / 최대 {max(sizes)} / 평균 {np.mean(sizes):.2f}")
    print(f"one-hot 인코딩 행렬 shape: {ONEHOT.shape}")
    print("\n거래 예시 3건:")
    for t in TXNS[:3]:
        print("  -", ", ".join(t))


# ── §01: 품목 빈도(=단일 품목 지지도) 상위 ────────────────────────────────
def s01_item_freq():
    """support(A) = A 를 포함한 거래 비율. 단일 품목 support 는 곧 판매 빈도다.
    상위 품목을 막대그래프로 본다(실습문제 6)."""
    support = ONEHOT.mean().sort_values(ascending=False)
    top = support.head(15)
    print(f"{'품목':<28}{'support':>9}{'거래수':>8}")
    print("-" * 46)
    for item, s in top.items():
        print(f"{item:<28}{s:>9.4f}{int(s*len(TXNS)):>8d}")
    print(f"\n가장 많이 팔린 품목: {top.index[0]} (support={top.iloc[0]:.4f})")
    print(f"가장 적게 팔린 품목: {support.index[-1]} (support={support.iloc[-1]:.5f})")

    fig, ax = plt.subplots(figsize=(8, 4.6))
    ax.bar(top.index, top.values, color="#5B9BD5")
    ax.set_ylabel("support (거래 비율)")
    ax.set_title("상위 15개 품목 지지도(support)")
    plt.setp(ax.get_xticklabels(), rotation=55, ha="right", fontsize=8)
    fig.tight_layout(); fig.savefig(CHARTS / "ch01_item_freq.png", dpi=110); plt.close(fig)
    print("[chart] ch01_item_freq.png 저장")


# ── §02: support/confidence/lift 의 정의 — 수동 계산으로 검증 ──────────────
def s02_manual():
    """mlxtend 가 내놓는 support/confidence/lift 가 정의 그대로인지,
    거래 리스트에서 직접 센 값과 비교한다. (도구 없이도 같은 수가 나와야 한다)
        support(A→B) = count(A∪B)/N
        confidence    = support(A∪B)/support(A)
        lift          = confidence / support(B)"""
    N = len(TXNS)
    sets = [set(t) for t in TXNS]

    def sup(items):
        items = set(items)
        return sum(1 for s in sets if items <= s) / N

    A, B = {"whole milk"}, {"yogurt"}
    s_a, s_b, s_ab = sup(A), sup(B), sup(A | B)
    conf = s_ab / s_a
    lift = conf / s_b
    print("[수동 계산] 규칙 whole milk -> yogurt")
    print(f"  support(whole milk)        = {s_a:.4f}")
    print(f"  support(yogurt)            = {s_b:.4f}")
    print(f"  support(whole milk,yogurt) = {s_ab:.4f}")
    print(f"  confidence = sup(A,B)/sup(A) = {conf:.4f}")
    print(f"  lift = confidence/sup(B)     = {lift:.4f}")

    # mlxtend 로 같은 규칙을 뽑아 대조
    fi = apriori(ONEHOT, min_support=0.01, use_colnames=True)
    rules = association_rules(fi, metric="confidence", min_threshold=0.01)
    m = rules[(rules["antecedents"] == frozenset({"whole milk"})) &
              (rules["consequents"] == frozenset({"yogurt"}))].iloc[0]
    print("\n[mlxtend] 같은 규칙")
    print(f"  support={m.support:.4f}  confidence={m.confidence:.4f}  lift={m.lift:.4f}")
    print(f"  → 수동 계산과 일치: "
          f"{np.allclose([s_ab, conf, lift], [m.support, m.confidence, m.lift], atol=1e-4)}")


# ── §02b: lift 직관 — 독립 기대치(P(A)P(B)) vs 실제, confidence 의 함정 ────
def s02b_lift_intuition():
    """lift>1 이 직관적으로 무엇인지를 실제 규칙 수치로 분해한다.
        · 분모 P(A)P(B) = '두 품목이 독립일 때(우연) 함께 담길 기대 비율'
        · 분자 support(A,B) = '실제로 함께 담긴 비율' = P(A∩B)
        · lift = 분자/분모 = '우연 대비 몇 배 더(덜) 함께 사나'
    기호는 합집합(∪)이지만 계산은 교집합(∩, 동시 구매)이라는 점,
    confidence 만 보면 21.9% 라 낮아 보여도 lift 로 보면 의미가 있다는 점을
    whole milk -> yogurt 실데이터로 보인다."""
    N = len(TXNS)
    sets = [set(t) for t in TXNS]

    def sup(items):
        items = set(items)
        return sum(1 for s in sets if items <= s) / N

    A, B = {"whole milk"}, {"yogurt"}
    s_a, s_b = sup(A), sup(B)
    s_ab = sup(A | B)              # A∪B 표기 = 둘을 합친 묶음의 지지도 = 실제 동시구매 P(A∩B)
    indep = s_a * s_b             # 독립(우연) 기대치
    conf = s_ab / s_a
    lift = conf / s_b

    print("[규칙] whole milk -> yogurt — lift 가 무엇을 재는지 분해")
    print(f"  P(whole milk)          = {s_a:.4f}  ({s_a*100:.2f}%)")
    print(f"  P(yogurt)              = {s_b:.4f}  ({s_b*100:.2f}%)")
    print("-" * 60)
    print("  분모 = 독립일 때 기대(우연히 함께 담길 비율) = P(A)*P(B)")
    print(f"        {s_a:.4f} * {s_b:.4f} = {indep:.4f}  ({indep*100:.2f}%)")
    print("  분자 = 실제 함께 담긴 비율 = support(A∪B) = P(A∩B)")
    print(f"        {s_ab:.4f}  ({s_ab*100:.2f}%)")
    print("-" * 60)
    print(f"  lift = 분자 / 분모 = {s_ab:.4f} / {indep:.4f} = {lift:.4f}")
    print(f"  → '우연이라면 {indep*100:.2f}%만 함께 담겨야 정상인데 실제로는 "
          f"{s_ab*100:.2f}% 담겼다' = {lift:.2f}배.")

    print("\n[confidence 의 함정] '21.9%뿐인데 왜 의미 있나'")
    print(f"  confidence(whole milk→yogurt) = {conf:.4f}  ({conf*100:.1f}%)")
    print(f"  → 우유 산 사람의 {conf*100:.1f}% 만 yogurt 를 샀다. 낮아 보인다.")
    print(f"  하지만 yogurt 자체의 기저 비율 P(B)={s_b*100:.1f}% 와 비교하면")
    print(f"  {conf*100:.1f}% > {s_b*100:.1f}% — yogurt 평균 구매율보다 "
          f"{lift:.2f}배 높다. 그래서 의미가 있다.")

    print("\n[기호 ∪ vs 의미 ∩] support(A∪B) 를 직접 두 방식으로 센다")
    inter = sum(1 for s in sets if ("whole milk" in s and "yogurt" in s)) / N   # 교집합(AND)
    union = sum(1 for s in sets if ("whole milk" in s or "yogurt" in s)) / N    # 진짜 합집합(OR)
    print(f"  동시 구매(AND, 교집합 ∩) 비율 = {inter:.4f}")
    print(f"  둘 중 하나라도(OR, 합집합 ∪) 비율 = {union:.4f}")
    print(f"  support(A∪B) 가 가리키는 값 = {s_ab:.4f}")
    print(f"  → support(A∪B) == AND(교집합) 값과 같다: {np.isclose(s_ab, inter)}")
    print("  기호는 '두 품목을 합친 itemset' 이라 ∪ 로 쓰지만,")
    print("  그 itemset 을 '모두 포함한' 거래를 세므로 계산은 교집합(∩)이다.")


# ── §03: 빈발 itemset + 규칙 생성, lift 상위 규칙 ──────────────────────────
def s03_rules():
    """apriori 로 빈발 itemset 을 뽑고 association_rules 로 규칙을 만든 뒤
    lift 내림차순 상위 규칙을 본다. lift>1 이면 두 품목이 '독립일 때보다
    함께 더 잘 팔린다'는 뜻이다."""
    fi = apriori(ONEHOT, min_support=0.01, use_colnames=True)
    rules = association_rules(fi, metric="confidence", min_threshold=0.20)
    print(f"min_support=0.01, min_confidence=0.20 기준")
    print(f"빈발 itemset 수: {len(fi)}   생성 규칙 수: {len(rules)}")

    def fmt(s):
        return "{" + ", ".join(sorted(s)) + "}"

    print("\n[lift 상위 10개 규칙]")
    print(f"{'선행(antecedent)':<40}{'후행':<22}{'sup':>7}{'conf':>7}{'lift':>7}")
    print("-" * 84)
    for r in rules.sort_values("lift", ascending=False).head(10).itertuples():
        print(f"{fmt(r.antecedents):<40}{fmt(r.consequents):<22}"
              f"{r.support:>7.4f}{r.confidence:>7.3f}{r.lift:>7.3f}")

    best = rules.sort_values("lift", ascending=False).iloc[0]
    print(f"\n최고 lift 규칙 : {fmt(best.antecedents)} -> {fmt(best.consequents)}")
    print(f"  support={best.support:.4f} confidence={best.confidence:.3f} lift={best.lift:.3f}")
    best_s = rules.sort_values("support", ascending=False).iloc[0]
    print(f"최고 support 규칙: {fmt(best_s.antecedents)} -> {fmt(best_s.consequents)} (support={best_s.support:.4f})")
    best_c = rules.sort_values("confidence", ascending=False).iloc[0]
    print(f"최고 confidence 규칙: {fmt(best_c.antecedents)} -> {fmt(best_c.consequents)} (confidence={best_c.confidence:.3f})")


# ── §04: 임계값(min_support) 이 규칙 수에 주는 영향 ───────────────────────
def s04_threshold():
    """임계값을 어떻게 정하나? min_support 를 0.005→0.05 로 올리며
    빈발 itemset 과 규칙 수를 센다. 너무 낮으면 규칙 폭발, 너무 높으면 0개."""
    supports = [0.005, 0.01, 0.02, 0.05]
    fi_counts, rule_counts = [], []
    print(f"{'min_support':>12}{'빈발itemset수':>14}{'규칙수(conf>=0.2)':>18}")
    print("-" * 46)
    for s in supports:
        fi = apriori(ONEHOT, min_support=s, use_colnames=True)
        rl = association_rules(fi, metric="confidence", min_threshold=0.20)
        fi_counts.append(len(fi)); rule_counts.append(len(rl))
        print(f"{s:>12.4f}{len(fi):>14d}{len(rl):>18d}")
    print("\n→ min_support 가 오를수록 빈발 itemset·규칙 수가 급감(단조 감소).")
    print("  너무 낮으면 규칙 폭발(해석 불가), 너무 높으면 0개에 수렴.")

    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.plot(supports, fi_counts, "o-", color="#5B9BD5", label="빈발 itemset 수")
    ax.plot(supports, rule_counts, "s-", color="#E8875A", label="규칙 수")
    ax.set_xlabel("min_support"); ax.set_ylabel("개수(로그 스케일)")
    ax.set_yscale("log"); ax.set_title("min_support↑ → 규칙 수 급감")
    ax.legend(); fig.tight_layout()
    fig.savefig(CHARTS / "ch04_threshold.png", dpi=110); plt.close(fig)
    print("[chart] ch04_threshold.png 저장")


# ── §05: 규칙 산점도(support vs confidence, 색=lift) + 추천 ────────────────
def s05_scatter_recommend():
    """규칙들을 support-confidence 평면에 흩뿌리고 lift 로 색을 입힌다.
    오른쪽 위(높은 support·confidence)·진한 색(높은 lift)이 좋은 규칙이다.
    이어서 한 품목을 넣으면 lift 순으로 함께 살 품목을 추천한다(실습문제 5)."""
    fi = apriori(ONEHOT, min_support=0.01, use_colnames=True)
    rules = association_rules(fi, metric="confidence", min_threshold=0.20)

    fig, ax = plt.subplots(figsize=(6.6, 4.6))
    sc = ax.scatter(rules["support"], rules["confidence"],
                    c=rules["lift"], cmap="viridis", s=24, alpha=0.8)
    ax.set_xlabel("support"); ax.set_ylabel("confidence")
    ax.set_title("규칙 분포 — support vs confidence (색=lift)")
    fig.colorbar(sc, ax=ax, label="lift")
    fig.tight_layout(); fig.savefig(CHARTS / "ch05_rules_scatter.png", dpi=110); plt.close(fig)
    print("[chart] ch05_rules_scatter.png 저장")

    def recommend(item, k=5):
        sub = rules[rules["antecedents"] == frozenset({item})]
        sub = sub.sort_values("lift", ascending=False).head(k)
        return [(set(r.consequents), r.confidence, r.lift) for r in sub.itertuples()]

    for target in ["whole milk", "yogurt"]:
        print(f"\n[추천] '{target}' 를 산 고객에게 (lift 상위 5)")
        for cons, conf, lift in recommend(target):
            name = ", ".join(sorted(cons))
            print(f"  → {name:<24} confidence={conf:.3f}  lift={lift:.3f}")


# ── §06: (선택) KMeans 로 품목 동시구매 세그먼트 ──────────────────────────
def s06_kmeans():
    """상위 품목들의 동시구매 패턴(거래 x 품목 one-hot)으로 거래를 KMeans 군집화한다.
    각 군집의 대표 품목을 보면 '음료/유제품 바구니', '신선식품 바구니' 같은
    세그먼트가 드러난다. k 는 4 로 두고 inertia 와 군집별 상위 품목을 본다."""
    support = ONEHOT.mean().sort_values(ascending=False)
    top_items = support.head(20).index.tolist()
    X = ONEHOT[top_items].astype(float).values
    km = KMeans(n_clusters=4, random_state=SEED, n_init=10).fit(X)
    labels = km.labels_
    print(f"KMeans k=4, 특성=상위20품목, 거래 {X.shape[0]}건")
    print(f"inertia(군집 내 제곱합): {km.inertia_:.1f}")
    print(f"군집 크기: {np.bincount(labels).tolist()}")
    print("\n[군집별 대표 품목 — 군집 내 평균 구매율 상위 4]")
    for c in range(4):
        centroid = km.cluster_centers_[c]
        order = np.argsort(centroid)[::-1][:4]
        rep = ", ".join(f"{top_items[i]}({centroid[i]:.2f})" for i in order)
        print(f"  군집 {c} (n={int((labels==c).sum())}): {rep}")

    # 두 축(상위 2품목)으로 군집 시각화
    fig, ax = plt.subplots(figsize=(6.2, 4.4))
    jit = np.random.RandomState(SEED).normal(0, 0.03, size=X[:, :2].shape)
    ax.scatter(X[:, 0] + jit[:, 0], X[:, 1] + jit[:, 1], c=labels,
               cmap="Set2", s=10, alpha=0.5)
    ax.set_xlabel(top_items[0]); ax.set_ylabel(top_items[1])
    ax.set_title("KMeans 거래 세그먼트 (상위2품목 축)")
    fig.tight_layout(); fig.savefig(CHARTS / "ch06_kmeans.png", dpi=110); plt.close(fig)
    print("[chart] ch06_kmeans.png 저장")


# ── §07: 상품 분포 불균형 정량화 — top-N 점유율 · 지니계수 ────────────────
def s07_imbalance():
    """'왜 품목 분포가 균등하지 않은가'를 수치로 본다.
    169품목이 고르게 팔린다면 각 품목의 판매 점유율은 1/169≈0.59% 로 같아야 한다.
    실제로는 소수 인기 품목에 쏠려 있는지 — top-N 점유율, top4 vs 나머지 비율,
    그리고 분포 불균등의 표준 척도인 지니계수(Gini)로 정량화한다."""
    # 품목별 '구매 건수'(품목이 등장한 거래 수). support 와 비례하지만 여기선 빈도로 본다.
    counts = ONEHOT.sum().sort_values(ascending=False)
    total = counts.sum()                       # 전체 품목 등장 횟수(= 모든 바구니 크기 합)
    n_items = len(counts)
    share = counts / total                     # 각 품목의 판매 점유율
    uniform = 1.0 / n_items                     # 완전 균등 시 점유율

    print(f"고유 품목 수: {n_items}   전체 품목 등장 횟수: {int(total)}")
    print(f"완전 균등 분포라면 품목별 점유율 = 1/{n_items} = {uniform*100:.2f}%")
    print("\n[상위 4개 품목 점유율]")
    print(f"{'품목':<22}{'등장수':>8}{'점유율':>9}{'균등대비':>9}")
    print("-" * 48)
    top4 = counts.head(4)
    for item, c in top4.items():
        sh = c / total
        print(f"{item:<22}{int(c):>8d}{sh*100:>8.2f}%{sh/uniform:>8.1f}배")

    top4_share = top4.sum() / total
    rest_share = 1 - top4_share
    print(f"\nTop 4 합산 점유율 : {top4_share*100:.2f}%  (전체 {n_items}품목 중 4개)")
    print(f"나머지 {n_items-4}품목 점유율: {rest_share*100:.2f}%")
    print(f"Top4 vs 나머지 비율: {top4_share/rest_share:.2f} : 1")
    print(f"top1(whole milk) 등장수 {int(counts.iloc[0])} / top4째 등장수 "
          f"{int(top4.iloc[-1])} = {counts.iloc[0]/top4.iloc[-1]:.2f}배 차이")

    # top-N 누적 점유율
    print("\n[누적 점유율 — 적은 품목이 매출 대부분을 차지하나]")
    for n in (4, 10, 20, 50):
        cum = counts.head(n).sum() / total
        print(f"  상위 {n:>3}품목({n/n_items*100:4.1f}%) → 누적 점유율 {cum*100:5.2f}%")

    # 지니계수(불균등 척도): 0=완전균등, 1=완전독점
    vals = np.sort(counts.values.astype(float))
    n = len(vals)
    cum = np.cumsum(vals)
    gini = (n + 1 - 2 * (cum.sum() / cum[-1])) / n
    print(f"\n지니계수(Gini, 0=완전균등 1=완전독점): {gini:.4f}")
    print("→ 0.5 를 크게 웃돌면 소수 품목 쏠림이 뚜렷하다는 뜻이다.")

    # 차트: (좌) 상위 20품목 점유율 막대 + 균등선, (우) 로렌츠 곡선
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.4))
    top20 = counts.head(20)
    ax1.bar(range(len(top20)), (top20 / total * 100).values, color="#E8875A")
    ax1.axhline(uniform * 100, color="#5B9BD5", ls="--", lw=1.4,
                label=f"완전 균등 시 {uniform*100:.2f}%")
    ax1.set_xticks(range(len(top20)))
    ax1.set_xticklabels(top20.index, rotation=55, ha="right", fontsize=7)
    ax1.set_ylabel("판매 점유율 (%)")
    ax1.set_title("상위 20품목 점유율 vs 균등 분포")
    ax1.legend(fontsize=8)

    lorenz = np.concatenate([[0], cum / cum[-1]])
    x = np.linspace(0, 1, len(lorenz))
    ax2.plot(x, lorenz, color="#52A97E", lw=1.8, label="로렌츠 곡선(실제)")
    ax2.plot([0, 1], [0, 1], color="#9178C4", ls="--", lw=1.2, label="완전 균등선")
    ax2.fill_between(x, lorenz, x, color="#EBF7F1")
    ax2.set_xlabel("하위→상위 품목 누적 비율")
    ax2.set_ylabel("판매량 누적 비율")
    ax2.set_title(f"품목 판매 불균등 (지니={gini:.3f})")
    ax2.legend(fontsize=8, loc="upper left")
    fig.tight_layout()
    fig.savefig(CHARTS / "ch07_imbalance.png", dpi=110); plt.close(fig)
    print("[chart] ch07_imbalance.png 저장")


if __name__ == "__main__":
    run_section("00_load", s00_load)
    run_section("01_item_freq", s01_item_freq)
    run_section("02_manual", s02_manual)
    run_section("02b_intuition", s02b_lift_intuition)
    run_section("03_rules", s03_rules)
    run_section("04_threshold", s04_threshold)
    run_section("05_scatter_recommend", s05_scatter_recommend)
    run_section("06_kmeans", s06_kmeans)
    run_section("07_imbalance", s07_imbalance)
    print("\n완료: logs/*.txt, charts/*.png 생성")
