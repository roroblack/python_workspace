# practice06_runner.py
# 머신러닝 실습6(과제) — 차원 축소로 분류 파이프라인 개선 (PCA + KNN)
# 실행: c:\_proj\python_workspace\.venv\Scripts\python.exe practice06_runner.py
# 결과: logs/{섹션명}.txt 저장 + 터미널 출력,  charts/*.png 생성
# 데이터: sklearn 내장 load_breast_cancer(30특성)·load_digits(64특성) — 외부 의존 없이 재현(고정 시드 42)
#   ※ 과제 colab(0604-s) 은 digits + PCA/LDA/t-SNE, 그리고 pytorch_knn_breast_cancer 의
#     KNN 흐름을 합친 것. 여기서는 재현 가능한 오프라인 실행을 위해 sklearn KNeighborsClassifier +
#     PCA 로 옮겨, "고차원에서 KNN + 차원축소" 를 두 데이터로 직접 검증한다(§16-C 우선순위 2, 사유 명시).

import sys, io, time, pathlib
from contextlib import redirect_stdout

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# 차트 한글 렌더링 (Windows 기본 한글 폰트) — 폰트 경고 0 보장
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

from sklearn.datasets import load_breast_cancer, load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score

HERE = pathlib.Path(__file__).parent
LOGS = HERE / "logs"; LOGS.mkdir(exist_ok=True)
CHARTS = HERE / "charts"; CHARTS.mkdir(exist_ok=True)
SEED = 42
ACCENT = "#52A97E"; ORANGE = "#E8875A"; BLUE = "#5B9BD5"; PURPLE = "#9178C4"


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


def split_bc():
    d = load_breast_cancer()
    Xtr, Xte, ytr, yte = train_test_split(d.data, d.target, test_size=0.2,
                                          random_state=SEED, stratify=d.target)
    return d, Xtr, Xte, ytr, yte


def split_digits():
    d = load_digits()
    Xtr, Xte, ytr, yte = train_test_split(d.data, d.target, test_size=0.2,
                                          random_state=SEED, stratify=d.target)
    return d, Xtr, Xte, ytr, yte


# ── §00: 두 데이터의 차원 진단 — 고차원이란 무엇인가 ──────────────────────
def s00_high_dim():
    """KNN 은 거리 기반이다. 그 거리를 재는 '특성'이 몇 개인지부터 본다.
    유방암 30특성·digits 64특성 — 둘 다 시각적으로 한눈에 안 들어오는 고차원이다."""
    bc = load_breast_cancer()
    dg = load_digits()
    print("[데이터 1] load_breast_cancer (이진분류: 악성/양성)")
    print(f"   X shape = {bc.data.shape}  → 특성 {bc.data.shape[1]}개,  클래스 {len(np.unique(bc.target))}개")
    print(f"   특성 스케일(원본): min={bc.data.min():.4f}  max={bc.data.max():.2f}  → 단위 제각각")
    print(f"   예) 'mean area' 범위 {bc.data[:,3].min():.1f}~{bc.data[:,3].max():.1f}  vs"
          f" 'mean smoothness' 범위 {bc.data[:,4].min():.4f}~{bc.data[:,4].max():.4f}")
    print()
    print("[데이터 2] load_digits (다중분류: 손글씨 0~9)")
    print(f"   X shape = {dg.data.shape}  → 특성 {dg.data.shape[1]}개(8x8 픽셀),  클래스 {len(np.unique(dg.target))}개")
    print(f"   특성 스케일(원본): 각 픽셀 0~16 명암")
    print()
    print("두 데이터 모두 특성 수가 30·64 → 사람이 직접 그려 볼 수 없는 '고차원'.")
    print("KNN 은 이 30/64차원 공간에서 '가까운 이웃 k개'를 찾아 다수결로 분류한다.")


# ── §01: KNN 베이스라인 — 표준화 없이 / 표준화 하고 (전체 특성) ────────────
def s01_knn_baseline():
    """KNN 은 거리 기반이므로 특성 스케일에 직접 휘둘린다.
    유방암 30특성 전체로, 표준화 없이 vs StandardScaler 적용 후 정확도를 비교한다."""
    d, Xtr, Xte, ytr, yte = split_bc()
    k = 5

    # ① 표준화 없이
    knn_raw = KNeighborsClassifier(n_neighbors=k).fit(Xtr, ytr)
    acc_raw = accuracy_score(yte, knn_raw.predict(Xte))

    # ② StandardScaler 후 (leakage 방지: train 으로만 fit)
    sc = StandardScaler().fit(Xtr)
    knn_std = KNeighborsClassifier(n_neighbors=k).fit(sc.transform(Xtr), ytr)
    acc_std = accuracy_score(yte, knn_std.predict(sc.transform(Xte)))

    print(f"[유방암 30특성 · KNN(k={k}) 베이스라인]")
    print(f"  표준화 없이(raw)      test 정확도 = {acc_raw:.4f}")
    print(f"  StandardScaler 적용   test 정확도 = {acc_std:.4f}")
    print(f"  표준화로 인한 향상     = {acc_std - acc_raw:+.4f}")
    print()
    print("거리 기반 KNN 에서 'mean area'(수백~수천)가 'mean smoothness'(0.x)를 압도해")
    print("표준화 없이는 큰 단위 특성 하나가 거리를 거의 결정한다 → 표준화가 선행이어야 한다.")


# ── §02: 차원의 저주 — 표준화한 전체 특성 KNN 의 한계 ─────────────────────
def s02_curse():
    """표준화를 해도 특성이 64개(digits)면 모든 점이 서로 '비슷하게 멀어'진다(차원의 저주).
    digits 64특성 전체 KNN 정확도와 학습+예측 시간을 베이스라인으로 기록한다."""
    d, Xtr, Xte, ytr, yte = split_digits()
    sc = StandardScaler().fit(Xtr)
    Xtr_s, Xte_s = sc.transform(Xtr), sc.transform(Xte)

    t0 = time.perf_counter()
    knn = KNeighborsClassifier(n_neighbors=5).fit(Xtr_s, ytr)
    pred = knn.predict(Xte_s)
    elapsed = (time.perf_counter() - t0) * 1000
    acc = accuracy_score(yte, pred)

    # 차원의 저주 관찰: 표준화 공간에서 train 점들의 최근접/최원접 이웃 거리 비율
    from sklearn.metrics import pairwise_distances
    Dtr = pairwise_distances(Xtr_s[:300])
    np.fill_diagonal(Dtr, np.inf)
    nearest = Dtr.min(axis=1)
    np.fill_diagonal(Dtr, -np.inf)
    farthest = Dtr.max(axis=1)
    ratio = float(np.mean(nearest / farthest))

    print(f"[digits 64특성 · 표준화 후 KNN(k=5)]")
    print(f"  test 정확도          = {acc:.4f}")
    print(f"  학습+예측 시간       = {elapsed:.1f} ms")
    print(f"  특성 수              = {Xtr.shape[1]}개 (전체)")
    print()
    print(f"[차원의 저주 신호] train 300점의 (최근접거리 / 최원접거리) 평균 = {ratio:.4f}")
    print("  → 1에 가까울수록 '가까운 점'과 '먼 점'의 구분이 흐려진다.")
    print("  64차원에서는 이 비율이 커서, KNN 이 의지하는 '가깝다'는 개념 자체가 약해진다.")


# ── §03: PCA n_components 스위프 — 정확도 vs 주성분 수 ────────────────────
def s03_pca_sweep():
    """PCA 로 차원을 줄여가며 KNN 정확도가 어떻게 변하는지 추적한다.
    표준화 → PCA(n) → KNN 파이프라인으로 두 데이터 모두 n 을 바꿔가며 sweet spot 을 찾는다."""
    for tag, splitter, max_feat in [("유방암", split_bc, 30), ("digits", split_digits, 64)]:
        d, Xtr, Xte, ytr, yte = splitter()
        ks = [c for c in [2, 3, 5, 8, 10, 15, 20, 30, 40, 50, 64] if c <= max_feat]
        print(f"[{tag} {max_feat}특성] 표준화 → PCA(n) → KNN(k=5)")
        print(f"  {'n_comp':>7} | {'test acc':>9} | {'설명분산누적':>12}")
        print("  " + "-" * 36)
        results = []
        for n in ks:
            sc = StandardScaler().fit(Xtr)
            pca = PCA(n_components=n, random_state=SEED).fit(sc.transform(Xtr))
            Ztr = pca.transform(sc.transform(Xtr))
            Zte = pca.transform(sc.transform(Xte))
            knn = KNeighborsClassifier(n_neighbors=5).fit(Ztr, ytr)
            acc = accuracy_score(yte, knn.predict(Zte))
            evr = float(pca.explained_variance_ratio_.sum())
            results.append((n, acc, evr))
            print(f"  {n:>7} | {acc:9.4f} | {evr:11.4f}")
        best = max(results, key=lambda r: r[1])
        print(f"  → 최고 정확도: n_components={best[0]}  acc={best[1]:.4f}  (설명분산 {best[2]:.4f})")
        print()


# ── §04: sweet spot 시각화 — n_components vs 정확도 + 베이스라인 ──────────
def s04_sweet_spot_chart():
    """§03 의 sweep 을 차트로 그려 'sweet spot'(최소 주성분으로 최대 정확도)을 눈으로 확인.
    전체 특성 KNN 정확도(점선)와 비교해 차원축소가 손해가 아닌 구간을 표시한다."""
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    for ax, (tag, splitter, max_feat) in zip(axes, [("유방암(30특성)", split_bc, 30),
                                                    ("digits(64특성)", split_digits, 64)]):
        d, Xtr, Xte, ytr, yte = splitter()
        sc = StandardScaler().fit(Xtr)
        Xtr_s, Xte_s = sc.transform(Xtr), sc.transform(Xte)
        full = accuracy_score(yte, KNeighborsClassifier(5).fit(Xtr_s, ytr).predict(Xte_s))
        ks = [c for c in [2, 3, 5, 8, 10, 15, 20, 30, 40, 50, 64] if c <= max_feat]
        accs = []
        for n in ks:
            pca = PCA(n_components=n, random_state=SEED).fit(Xtr_s)
            knn = KNeighborsClassifier(5).fit(pca.transform(Xtr_s), ytr)
            accs.append(accuracy_score(yte, knn.predict(pca.transform(Xte_s))))
        best_i = int(np.argmax(accs))
        ax.plot(ks, accs, "o-", color=ACCENT, label="PCA+KNN test 정확도")
        ax.axhline(full, color=ORANGE, lw=1.6, ls="--", label=f"전체 특성 KNN ({full:.3f})")
        ax.scatter([ks[best_i]], [accs[best_i]], s=120, facecolors="none",
                   edgecolors=PURPLE, linewidths=2.2, zorder=5,
                   label=f"sweet spot n={ks[best_i]}")
        ax.set_title(f"{tag} — 주성분 수 vs 정확도")
        ax.set_xlabel("PCA n_components"); ax.set_ylabel("test 정확도")
        ax.legend(fontsize=8); ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(CHARTS / "ch_sweep.png", dpi=110); plt.close(fig)
    print("[chart] ch_sweep.png 저장 (두 데이터 n_components vs 정확도 + 베이스라인)")

    # sweet spot 수치 로그
    for tag, splitter, max_feat in [("유방암", split_bc, 30), ("digits", split_digits, 64)]:
        d, Xtr, Xte, ytr, yte = splitter()
        sc = StandardScaler().fit(Xtr)
        Xtr_s, Xte_s = sc.transform(Xtr), sc.transform(Xte)
        full = accuracy_score(yte, KNeighborsClassifier(5).fit(Xtr_s, ytr).predict(Xte_s))
        ks = [c for c in [2, 3, 5, 8, 10, 15, 20, 30, 40, 50, 64] if c <= max_feat]
        accs, evrs = [], []
        for n in ks:
            pca = PCA(n_components=n, random_state=SEED).fit(Xtr_s)
            accs.append(accuracy_score(yte, KNeighborsClassifier(5).fit(
                pca.transform(Xtr_s), ytr).predict(pca.transform(Xte_s))))
            evrs.append(float(pca.explained_variance_ratio_.sum()))
        bi = int(np.argmax(accs))
        print(f"  [{tag}] 전체 {max_feat}특성 acc={full:.4f}  →  sweet spot n={ks[bi]} "
              f"acc={accs[bi]:.4f} (설명분산 {evrs[bi]:.4f}) : "
              f"{ks[bi]}/{max_feat}={ks[bi]/max_feat:.0%} 차원으로 {accs[bi]-full:+.4f}")


# ── §05: 누적 설명분산 — 몇 개 주성분이 정보를 얼마나 담나 ─────────────────
def s05_cumulative_variance():
    """explained_variance_ratio_ 누적 곡선으로 '몇 개 주성분이 분산(정보) 몇 %를 담는지' 본다.
    정확도 sweet spot 과 비교해 '정보 보존'과 '분류 성능'이 일치하지 않을 수 있음을 확인한다."""
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    for ax, (tag, splitter, max_feat) in zip(axes, [("유방암(30특성)", split_bc, 30),
                                                    ("digits(64특성)", split_digits, 64)]):
        d, Xtr, Xte, ytr, yte = splitter()
        sc = StandardScaler().fit(Xtr)
        pca = PCA(random_state=SEED).fit(sc.transform(Xtr))
        cum = np.cumsum(pca.explained_variance_ratio_)
        xs = np.arange(1, len(cum) + 1)
        ax.plot(xs, cum, "-", color=BLUE, lw=2)
        # 90% / 95% 도달 지점
        n90 = int(np.searchsorted(cum, 0.90) + 1)
        n95 = int(np.searchsorted(cum, 0.95) + 1)
        ax.axhline(0.90, color=ORANGE, lw=1, ls=":")
        ax.axhline(0.95, color=PURPLE, lw=1, ls=":")
        ax.axvline(n90, color=ORANGE, lw=1, ls=":")
        ax.set_title(f"{tag} — 누적 설명분산\n(90%: {n90}개, 95%: {n95}개 주성분)")
        ax.set_xlabel("주성분 수"); ax.set_ylabel("누적 설명분산 비율")
        ax.grid(alpha=0.25)
        print(f"[{tag}] 전체 {max_feat}특성 중 — "
              f"분산 90% 보존: {n90}개 주성분,  95% 보존: {n95}개 주성분,  99% 보존: "
              f"{int(np.searchsorted(cum, 0.99) + 1)}개")
        print(f"   주성분 1개만으로 {cum[0]:.1%}, 2개로 {cum[1]:.1%} 의 분산을 설명")
    fig.tight_layout()
    fig.savefig(CHARTS / "ch_cumvar.png", dpi=110); plt.close(fig)
    print("[chart] ch_cumvar.png 저장 (누적 설명분산 곡선)")


# ── §06: 2D PCA 산점도 — 64차원이 평면에서도 갈라지나 ─────────────────────
def s06_pca_2d_scatter():
    """주성분 2개(설명분산이 적어도)로 평면에 투영해, 클래스가 시각적으로 분리되는지 본다.
    digits 10클래스 / 유방암 2클래스 — 2D 에서의 분리가 KNN 가능성의 직관적 단서."""
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))

    # 유방암 2D
    d, Xtr, Xte, ytr, yte = split_bc()
    sc = StandardScaler().fit(Xtr)
    p2 = PCA(n_components=2, random_state=SEED).fit(sc.transform(Xtr))
    Z = p2.transform(sc.transform(Xtr))
    for cls, name, c in [(0, "악성(malignant)", ORANGE), (1, "양성(benign)", ACCENT)]:
        m = ytr == cls
        axes[0].scatter(Z[m, 0], Z[m, 1], s=12, alpha=0.6, color=c, label=name)
    axes[0].set_title(f"유방암 → PC1·PC2 투영\n(2개로 설명분산 {p2.explained_variance_ratio_.sum():.1%})")
    axes[0].set_xlabel("PC1"); axes[0].set_ylabel("PC2"); axes[0].legend(fontsize=8)

    # digits 2D
    d2, Xtr2, Xte2, ytr2, yte2 = split_digits()
    sc2 = StandardScaler().fit(Xtr2)
    p2d = PCA(n_components=2, random_state=SEED).fit(sc2.transform(Xtr2))
    Z2 = p2d.transform(sc2.transform(Xtr2))
    sca = axes[1].scatter(Z2[:, 0], Z2[:, 1], c=ytr2, cmap="tab10", s=12, alpha=0.7)
    axes[1].set_title(f"digits 0~9 → PC1·PC2 투영\n(2개로 설명분산 {p2d.explained_variance_ratio_.sum():.1%})")
    axes[1].set_xlabel("PC1"); axes[1].set_ylabel("PC2")
    fig.colorbar(sca, ax=axes[1], label="숫자 라벨", ticks=range(10))
    fig.tight_layout()
    fig.savefig(CHARTS / "ch_scatter2d.png", dpi=110); plt.close(fig)

    print(f"[유방암] PC1+PC2 설명분산 = {p2.explained_variance_ratio_.sum():.4f} "
          f"(PC1={p2.explained_variance_ratio_[0]:.4f}, PC2={p2.explained_variance_ratio_[1]:.4f})")
    print(f"[digits] PC1+PC2 설명분산 = {p2d.explained_variance_ratio_.sum():.4f} "
          f"(PC1={p2d.explained_variance_ratio_[0]:.4f}, PC2={p2d.explained_variance_ratio_[1]:.4f})")
    print("유방암 2클래스는 2D 에서도 두 덩어리로 갈라지나, digits 10클래스는 일부만 분리된다.")
    print("[chart] ch_scatter2d.png 저장 (2D PCA 산점도)")


# ── §07: 표준화 선행 여부 — PCA 앞 StandardScaler 의 효과 ─────────────────
def s07_scaler_before_pca():
    """PCA 는 '분산이 큰 축'을 찾는다. 표준화 없이 PCA 하면 단위 큰 특성이 주성분을 독점한다.
    유방암에서 [표준화→PCA→KNN] vs [표준화 없이→PCA→KNN] 정확도를 같은 n 으로 비교한다."""
    d, Xtr, Xte, ytr, yte = split_bc()
    print(f"[유방암] PCA(n) → KNN(k=5) — 표준화 선행 여부 비교")
    print(f"  {'n_comp':>7} | {'표준화O acc':>11} | {'표준화X acc':>11} | {'차이':>8}")
    print("  " + "-" * 46)
    for n in [2, 5, 10, 15, 30]:
        # 표준화 O
        sc = StandardScaler().fit(Xtr)
        pca = PCA(n_components=n, random_state=SEED).fit(sc.transform(Xtr))
        acc_o = accuracy_score(yte, KNeighborsClassifier(5).fit(
            pca.transform(sc.transform(Xtr)), ytr).predict(pca.transform(sc.transform(Xte))))
        # 표준화 X (원본에 바로 PCA)
        pca2 = PCA(n_components=n, random_state=SEED).fit(Xtr)
        acc_x = accuracy_score(yte, KNeighborsClassifier(5).fit(
            pca2.transform(Xtr), ytr).predict(pca2.transform(Xte)))
        print(f"  {n:>7} | {acc_o:11.4f} | {acc_x:11.4f} | {acc_o-acc_x:+8.4f}")
    print()
    # 표준화 없이 PCA 하면 PC1 이 분산을 거의 독점
    pca_raw = PCA(random_state=SEED).fit(Xtr)
    pca_std = PCA(random_state=SEED).fit(StandardScaler().fit_transform(Xtr))
    print(f"  표준화 없이 PCA: PC1 설명분산 = {pca_raw.explained_variance_ratio_[0]:.4f} "
          f"(단위 큰 'area' 특성이 독점)")
    print(f"  표준화 후   PCA: PC1 설명분산 = {pca_std.explained_variance_ratio_[0]:.4f} "
          f"(특성들이 고르게 기여)")


# ── §08: 정보 손실 지점 — 차원축소가 손해로 바뀌는 곳 ─────────────────────
def s08_loss_point():
    """차원축소가 항상 이득은 아니다. 주성분을 과하게 줄이면(예: 2~3개) 정확도가 꺾인다.
    digits 에서 전체 64특성·sweet spot·과소(2개) 세 지점을 같은 KNN 으로 비교한다."""
    d, Xtr, Xte, ytr, yte = split_digits()
    sc = StandardScaler().fit(Xtr)
    Xtr_s, Xte_s = sc.transform(Xtr), sc.transform(Xte)

    def acc_at(n):
        if n is None:  # 전체 특성
            knn = KNeighborsClassifier(5).fit(Xtr_s, ytr)
            return accuracy_score(yte, knn.predict(Xte_s)), 1.0
        pca = PCA(n_components=n, random_state=SEED).fit(Xtr_s)
        knn = KNeighborsClassifier(5).fit(pca.transform(Xtr_s), ytr)
        return (accuracy_score(yte, knn.predict(pca.transform(Xte_s))),
                float(pca.explained_variance_ratio_.sum()))

    full_acc, _ = acc_at(None)
    print("[digits 64특성] 차원축소 정도에 따른 정확도 — 어디서 손해로 바뀌나")
    print(f"  {'설정':>16} | {'test acc':>9} | {'설명분산':>9} | {'vs 전체':>9}")
    print("  " + "-" * 52)
    print(f"  {'전체 64특성':>16} | {full_acc:9.4f} | {'1.0000':>9} | {'(기준)':>9}")
    for label, n in [("PCA 40개(sweet)", 40), ("PCA 20개", 20), ("PCA 10개", 10),
                     ("PCA 5개", 5), ("PCA 3개", 3), ("PCA 2개(과소)", 2)]:
        a, e = acc_at(n)
        print(f"  {label:>16} | {a:9.4f} | {e:9.4f} | {a-full_acc:+9.4f}")
    print()
    print("주성분을 2~3개까지 줄이면 분산은 일부만 남아 정확도가 또렷이 꺾인다.")
    print("→ 차원축소의 이득(잡음 제거·속도)과 손실(정보 손실)이 교차하는 지점이 있다.")


# ── §09: 가성비 기준 — '최고 정확도'가 아니라 '충분한 정확도를 가장 적은 차원으로' ──
def s09_cost_efficiency():
    """주성분 수를 정하는 기준은 '최고 정확도 한 점'만이 아니다.
    누적 설명분산(85/95%) 도달 차원, 정확도가 전체의 -1%p 이내로 들어오는 최소 차원,
    그리고 차원당 정확도(가성비)를 같이 보고 '가성비 좋은' n 을 고른다(digits)."""
    d, Xtr, Xte, ytr, yte = split_digits()
    sc = StandardScaler().fit(Xtr)
    Xtr_s, Xte_s = sc.transform(Xtr), sc.transform(Xte)
    full = accuracy_score(yte, KNeighborsClassifier(5).fit(Xtr_s, ytr).predict(Xte_s))

    # 전체 차원 PCA 로 누적 분산 곡선 → 85/95% 도달 차원
    pca_full = PCA(random_state=SEED).fit(Xtr_s)
    cum = np.cumsum(pca_full.explained_variance_ratio_)
    n85 = int(np.searchsorted(cum, 0.85) + 1)
    n95 = int(np.searchsorted(cum, 0.95) + 1)

    ks = [2, 3, 5, 8, 10, 15, 20, 30, 40, 50, 64]
    rows = []
    for n in ks:
        pca = PCA(n_components=n, random_state=SEED).fit(Xtr_s)
        acc = accuracy_score(yte, KNeighborsClassifier(5).fit(
            pca.transform(Xtr_s), ytr).predict(pca.transform(Xte_s)))
        evr = float(pca.explained_variance_ratio_.sum())
        rows.append((n, acc, evr))

    # 기준 ①: 정확도가 전체의 -1%p 이내로 들어오는 '최소' 차원
    tol = 0.01
    enough = next((n for n, a, e in rows if a >= full - tol), ks[-1])
    # 기준 ②: 차원당 정확도(정확도/차원) = 가성비
    best_eff = max(rows, key=lambda r: r[1] / r[0])

    print("[digits 64특성] 주성분 수를 어떤 기준으로 고를까 — 가성비 관점")
    print(f"  전체 64특성 KNN 정확도(기준선) = {full:.4f}")
    print(f"  {'n_comp':>7} | {'test acc':>9} | {'설명분산':>9} | {'acc/차원':>10}")
    print("  " + "-" * 44)
    for n, a, e in rows:
        mark = "  ←충분(전체-1%p 이내 최소)" if n == enough else ""
        print(f"  {n:>7} | {a:9.4f} | {e:9.4f} | {a/n:10.5f}{mark}")
    print()
    print(f"[기준 ① 누적 설명분산] 85% 보존: {n85}개 주성분,  95% 보존: {n95}개")
    print(f"[기준 ② 충분한 정확도] 전체({full:.4f})의 -{tol*100:.0f}%p 이내를 내는 최소 차원 = {enough}개")
    print(f"[기준 ③ 차원당 정확도] acc/차원 최댓값 = n={best_eff[0]} (acc={best_eff[1]:.4f}, {best_eff[1]/best_eff[0]:.5f}/차원)")
    print()
    print("'최고 정확도'와 '가성비'는 다른 기준이다. 차원당 정확도는 적은 차원에 유리하므로")
    print("극단으로 낮은 n 을 가리킨다 — 정보 보존(85/95%)·충분한 정확도 기준과 함께 봐야 한다.")


# ── §10: PCA 복원 — 8차원·2차원으로 줄인 digits 를 inverse_transform 으로 되돌리면 ──
def s10_reconstruction():
    """차원을 줄이면 정보가 빠진다. 그 손실을 눈으로 보려고 PCA 로 8·2차원까지 압축한 뒤
    inverse_transform 으로 64픽셀 이미지로 복원해, 원본과의 픽셀 MSE 와 복원 이미지를 비교한다.
    '8차원 복원이 얼마나 선명한가'를 MSE 수치와 이미지로 직접 확인한다."""
    d, Xtr, Xte, ytr, yte = split_digits()
    sc = StandardScaler().fit(Xtr)
    Xtr_s, Xte_s = sc.transform(Xtr), sc.transform(Xte)

    def recon_mse(n):
        pca = PCA(n_components=n, random_state=SEED).fit(Xtr_s)
        Zte = pca.transform(Xte_s)
        Xte_rec_s = pca.inverse_transform(Zte)            # 표준화 공간에서 복원
        Xte_rec = sc.inverse_transform(Xte_rec_s)         # 원래 픽셀 스케일로 역변환
        mse = float(np.mean((Xte - Xte_rec) ** 2))        # 픽셀(0~16) 기준 MSE
        evr = float(pca.explained_variance_ratio_.sum())
        return mse, evr, Xte_rec

    print("[digits 64픽셀] PCA 차원 축소 → inverse_transform 복원 — 원본과의 픽셀 MSE")
    print(f"  {'설정':>14} | {'설명분산':>9} | {'복원 MSE(픽셀²)':>15}")
    print("  " + "-" * 46)
    recs = {}
    for label, n in [("PCA 32개", 32), ("PCA 8개", 8), ("PCA 4개", 4), ("PCA 2개", 2)]:
        mse, evr, rec = recon_mse(n)
        recs[n] = rec
        print(f"  {label:>14} | {evr:9.4f} | {mse:15.4f}")
    print()
    print("주성분이 많을수록 복원 MSE 가 작아진다(원본에 가까워진다).")
    print("8차원은 설명분산이 절반 안팎이라 큰 획은 살지만 세부는 뭉개진다 — MSE 로 그 정도가 드러난다.")

    # 복원 이미지 비교: 원본 vs PCA-8 vs PCA-2 (테스트셋 앞 8개)
    pca8 = PCA(n_components=8, random_state=SEED).fit(Xtr_s)
    pca2 = PCA(n_components=2, random_state=SEED).fit(Xtr_s)
    rec8 = sc.inverse_transform(pca8.inverse_transform(pca8.transform(Xte_s)))
    rec2 = sc.inverse_transform(pca2.inverse_transform(pca2.transform(Xte_s)))
    ncol = 8
    fig, axes = plt.subplots(3, ncol, figsize=(11, 4.4))
    rows_img = [("원본 64픽셀", Xte), ("PCA 8차원 복원", rec8), ("PCA 2차원 복원", rec2)]
    for r, (rlabel, data) in enumerate(rows_img):
        for c in range(ncol):
            ax = axes[r, c]
            ax.imshow(data[c].reshape(8, 8), cmap="gray_r", vmin=0, vmax=16)
            ax.set_xticks([]); ax.set_yticks([])
            if c == 0:
                ax.set_ylabel(rlabel, fontsize=9, rotation=90, labelpad=8)
            if r == 0:
                ax.set_title(str(int(yte[c])), fontsize=10)
    fig.suptitle("digits 복원 비교 — 원본 vs PCA 8차원 vs PCA 2차원 (테스트셋 앞 8개)", fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(CHARTS / "ch_recon.png", dpi=110); plt.close(fig)
    print("[chart] ch_recon.png 저장 (원본/PCA8/PCA2 복원 이미지 3행 비교)")


if __name__ == "__main__":
    run_section("00_high_dim", s00_high_dim)
    run_section("01_knn_baseline", s01_knn_baseline)
    run_section("02_curse", s02_curse)
    run_section("03_pca_sweep", s03_pca_sweep)
    run_section("04_sweet_spot", s04_sweet_spot_chart)
    run_section("05_cumulative_variance", s05_cumulative_variance)
    run_section("06_pca_2d", s06_pca_2d_scatter)
    run_section("07_scaler_before_pca", s07_scaler_before_pca)
    run_section("08_loss_point", s08_loss_point)
    run_section("09_cost_efficiency", s09_cost_efficiency)
    run_section("10_reconstruction", s10_reconstruction)
    print("\n완료: logs/*.txt, charts/*.png 생성")
