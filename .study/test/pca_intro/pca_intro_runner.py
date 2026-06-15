# pca_intro_runner.py
# 머신러닝 Day6 (0604) — 차원 축소와 시각화(PCA) 섹션별 테스트 실행기
# 실행: c:\_proj\python_workspace\.venv\Scripts\python.exe pca_intro_runner.py
# 결과: logs/{섹션명}.txt 저장 + 터미널 출력,  charts/*.png 생성
# 데이터: sklearn 내장 load_digits(64차원)·load_iris·load_breast_cancer — 외부 파일 의존 없이 재현 가능(고정 시드)
#   ※ 기존 샘플 참고: ../ml_workspace/from_colab/0604-s/dimensionality_reduction.ipynb 는
#     Wine Quality(11특성) 기준 PCA/LDA/t-SNE/UMAP/AE 흐름이라, 차원의 저주를 또렷이 보이려고
#     64차원 내장 digits 로 새로 구성(§16-C 우선순위 2, 사유 명시). PCA/explained_variance/t-SNE 개념은 동일.

import sys, io, pathlib
from contextlib import redirect_stdout

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# 차트 한글 렌더링 (Windows 기본 한글 폰트) — 폰트 경고 0개 목표
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

from sklearn.datasets import load_digits, load_iris, load_breast_cancer
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics import pairwise_distances

HERE = pathlib.Path(__file__).parent
LOGS = HERE / "logs"; LOGS.mkdir(exist_ok=True)
CHARTS = HERE / "charts"; CHARTS.mkdir(exist_ok=True)
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


# ── §00: 차원의 저주 — 차원이 늘수록 거리가 한 점으로 몰린다 ────────────────
def s00_curse():
    """특성이 수십·수백 개면 무엇이 문제인가? 차원이 커질수록 무작위 점들 사이의
    거리가 거의 같아져(최근접/최원접 비율 → 1) '가깝다'는 개념 자체가 희박해진다."""
    rng = np.random.RandomState(SEED)
    print(f"{'차원 d':>6} | {'평균 최근접거리':>14} | {'평균 최원접거리':>14} | {'(최원-최근)/최근':>16}")
    print("-" * 64)
    for d in [2, 10, 50, 100, 500]:
        X = rng.rand(200, d)                 # [0,1]^d 균등 분포 200점
        D = pairwise_distances(X)
        np.fill_diagonal(D, np.inf)
        nearest = D.min(axis=1)              # 각 점의 최근접 이웃 거리
        D2 = pairwise_distances(X)
        np.fill_diagonal(D2, -np.inf)
        farthest = D2.max(axis=1)            # 각 점의 최원접 거리
        contrast = (farthest.mean() - nearest.mean()) / nearest.mean()
        print(f"{d:>6} | {nearest.mean():14.4f} | {farthest.mean():14.4f} | {contrast:16.4f}")
    print("\n→ 차원 d가 커질수록 최근접거리와 최원접거리의 대비가 줄어든다(거리 희박화).")
    print("  '가까운 이웃'이 의미를 잃으니, 차원을 줄이려는 동기가 생긴다.")


# ── §0A: 공분산 행렬을 손으로 — 왜 XᵀX 가 (d×d) '지도'가 되나 ───────────────
def s0a_cov_by_hand():
    """노트의 의문: 두 변수의 곱을 더했는데 왜 (d×d) 행렬이 변수 사이의 '지도'가 되나.
    [6][2]·[2][6] 모양을 곱했는데 왜 [4][4]가 나오나. 왜 하필 Xᵀ_c X_c 인가.
    45도로 뻗은 점 3개로 공분산 행렬을 손으로 계산해 np.cov 와 맞춰 본다."""
    # 노트에서 그대로 가져온 작은 예제: 키-몸무게처럼 같이 커지는 2변수 3샘플
    X = np.array([[2.0, 3.0],
                  [4.0, 5.0],
                  [6.0, 7.0]])              # (n=3 행=샘플, d=2 열=변수)
    n, d = X.shape
    print(f"원본 X (행=샘플 {n}, 열=변수 {d}):")
    print(X)

    # Step 1. 변수별 평균
    mu = X.mean(axis=0)
    print(f"\nStep1 변수 평균 μ = {mu}  (열 방향 평균: 변수1, 변수2)")

    # Step 2. 중심화 — 평균을 빼서 원점으로
    Xc = X - mu
    print("Step2 중심화 Xc = X - μ:")
    print(Xc)

    # Step 3. 손 계산: 공분산 행렬은 (d×d). 각 칸 = 변수 i,j 편차곱의 합 / (n-1)
    #   shape 추적: Xc.T 는 (d×n)=(2×3), Xc 는 (n×d)=(3×2) → (2×3)@(3×2)=(2×2)=(d×d)
    print(f"\nStep3 shape 추적: Xc.T{Xc.T.shape} @ Xc{Xc.shape} -> (d×d)={ (Xc.T @ Xc).shape }")
    print("  → n(샘플 수)이 곱셈 안에서 사라지고 변수 개수 d×d 칸만 남는다.")
    C_hand = np.zeros((d, d))
    for i in range(d):
        for j in range(d):
            # 변수 i 편차와 변수 j 편차를 샘플마다 곱해 더하고 (n-1)로 나눈다
            s = float(np.sum(Xc[:, i] * Xc[:, j]))
            C_hand[i, j] = s / (n - 1)
            print(f"  C[{i}][{j}] = Σ(Xc[:,{i}]·Xc[:,{j}]) / (n-1) = {s:.1f}/{n-1} = {C_hand[i, j]:.4f}")
    print("\n손 계산 공분산 행렬 C_hand:")
    print(C_hand)

    # 행렬식 한 줄로 같은 값
    C_mat = (Xc.T @ Xc) / (n - 1)
    print("\n행렬식 (Xc.T @ Xc)/(n-1):")
    print(C_mat)

    # np.cov 와 대조 (rowvar=False: 열이 변수)
    C_np = np.cov(X, rowvar=False)
    print("\nnp.cov(X, rowvar=False):")
    print(C_np)
    print(f"\n손 계산 == 행렬식 == np.cov ? {np.allclose(C_hand, C_mat) and np.allclose(C_hand, C_np)}")

    # 의미: 대각선=각 변수의 분산, 비대각선=두 변수가 같이 움직이는 정도(공분산)
    print(f"\n대각선 C[0][0]={C_hand[0,0]:.1f}(변수1 분산), C[1][1]={C_hand[1,1]:.1f}(변수2 분산)")
    print(f"비대각선 C[0][1]={C_hand[0,1]:.1f} = C[1][0]={C_hand[1,0]:.1f}  (두 변수의 관계, 대칭)")
    print(f"비대각선이 양수이고 분산과 같은 크기 → 두 변수가 거의 완전히 같이 커진다.")

    # 고유값 분해 — 이 (d×d) 지도에서 주성분 축이 나온다
    eigval, eigvec = np.linalg.eigh(C_hand)       # 대칭행렬용, 오름차순
    order = np.argsort(eigval)[::-1]
    eigval, eigvec = eigval[order], eigvec[:, order]
    print(f"\n고유값 분해: λ = {np.round(eigval, 4)}  (분산이 큰 축 순)")
    print(f"첫 고유벡터(PC1) = {np.round(eigvec[:, 0], 4)}  ≈ [1/√2, 1/√2] = 45도 방향")
    print(f"설명분산비 PC1 = {eigval[0] / eigval.sum():.4f}  → 한 축으로 분산 전부를 담는다.")

    # 시각화: 원본 점·중심화 점·PC1 방향
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.6))
    axes[0].scatter(X[:, 0], X[:, 1], s=80, color="#5B9BD5")
    axes[0].scatter(*mu, s=120, marker="x", color="#E8875A")
    axes[0].set_title("원본 3점 + 평균(×)"); axes[0].set_xlabel("변수1"); axes[0].set_ylabel("변수2")
    axes[0].grid(alpha=0.3)
    axes[1].scatter(Xc[:, 0], Xc[:, 1], s=80, color="#52A97E")
    v = eigvec[:, 0] * np.sqrt(eigval[0])
    axes[1].annotate("", xy=v, xytext=-v,
                     arrowprops=dict(arrowstyle="<->", color="#9178C4", lw=2.5))
    axes[1].text(*(v * 1.1), "PC1", color="#9178C4", fontweight="bold")
    axes[1].axhline(0, color="#aaa", lw=0.8); axes[1].axvline(0, color="#aaa", lw=0.8)
    axes[1].set_aspect("equal"); axes[1].set_title("중심화 점 + 고유벡터 PC1(45도)")
    axes[1].set_xlabel("변수1 편차"); axes[1].set_ylabel("변수2 편차")
    fig.suptitle("공분산 행렬을 손으로 — Xc.T@Xc/(n-1) = [[4,4],[4,4]], PC1 = 45도")
    fig.tight_layout(); fig.savefig(CHARTS / "ch0a_cov_by_hand.png", dpi=110); plt.close(fig)
    print("[chart] ch0a_cov_by_hand.png 저장")


# ── §01: PCA — 분산이 가장 큰 축을 찾는다 ─────────────────────────────────
def s01_axes():
    """PCA의 정의: 데이터의 분산이 가장 큰 방향을 첫 주성분(PC1)으로,
    그에 직교하면서 다음으로 분산이 큰 방향을 PC2로 잡는다. 길게 뻗은 2D 구름으로 확인한다."""
    rng = np.random.RandomState(SEED)
    # 한 방향으로 길게 뻗은 상관 있는 2D 데이터
    base = rng.randn(300, 2)
    X = base @ np.array([[3.0, 1.0], [1.0, 0.6]])   # 선형 변환으로 늘이고 기울임
    pca = PCA(n_components=2, random_state=SEED).fit(X)
    print("입력 분산(축별):", np.round(X.var(axis=0), 4))
    print("주성분 방향(행=PC):")
    for i, comp in enumerate(pca.components_):
        print(f"  PC{i+1} 방향 = {np.round(comp, 4)}  설명분산비 = {pca.explained_variance_ratio_[i]:.4f}")
    print(f"PC1 한 축만으로 설명되는 분산 비율 = {pca.explained_variance_ratio_[0]:.4f}")

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.scatter(X[:, 0], X[:, 1], s=12, alpha=0.4, color="#5B9BD5", label="데이터")
    mean = X.mean(axis=0)
    colors = ["#E8875A", "#52A97E"]
    for i, comp in enumerate(pca.components_):
        v = comp * np.sqrt(pca.explained_variance_[i]) * 2.5
        ax.annotate("", xy=mean + v, xytext=mean,
                    arrowprops=dict(arrowstyle="->", color=colors[i], lw=2.5))
        ax.text(*(mean + v * 1.08), f"PC{i+1}", color=colors[i], fontweight="bold")
    ax.set_aspect("equal"); ax.set_title("PCA — 분산이 가장 큰 축(PC1)부터 찾는다")
    ax.set_xlabel("x1"); ax.set_ylabel("x2"); ax.legend()
    fig.tight_layout(); fig.savefig(CHARTS / "ch01_pca_axes.png", dpi=110); plt.close(fig)
    print("[chart] ch01_pca_axes.png 저장")


# ── §02: 몇 개의 주성분으로? — explained_variance_ratio 누적 ───────────────
def s02_explained():
    """64차원 digits 를 PCA full 로 분해하고 누적 설명분산을 본다.
    90%/95% 분산을 보존하려면 64개 중 몇 개의 주성분이 필요한지 수치로 확인한다."""
    d = load_digits()
    X = StandardScaler().fit_transform(d.data)      # 64차원 표준화
    print(f"원본 차원: {X.shape[1]}  (8x8 손글씨 숫자 이미지)")
    pca = PCA(random_state=SEED).fit(X)
    ratio = pca.explained_variance_ratio_
    cum = np.cumsum(ratio)
    print(f"PC1 설명분산비 = {ratio[0]:.4f},  PC1~2 누적 = {cum[1]:.4f}")
    for thr in [0.80, 0.90, 0.95, 0.99]:
        k = int(np.searchsorted(cum, thr) + 1)
        print(f"  누적 분산 {int(thr*100)}% 이상 보존 → 주성분 {k:>2}개 필요 (64개 중)")

    fig, ax = plt.subplots(figsize=(7, 4.5))
    xs = np.arange(1, len(cum) + 1)
    ax.plot(xs, cum, "-", color="#5B9BD5", lw=2)
    for thr, c in [(0.90, "#E8875A"), (0.95, "#9178C4")]:
        k = int(np.searchsorted(cum, thr) + 1)
        ax.axhline(thr, color=c, ls="--", lw=1, label=f"{int(thr*100)}% (k={k})")
        ax.axvline(k, color=c, ls=":", lw=1)
    ax.set_xlabel("주성분 개수"); ax.set_ylabel("누적 설명분산 비율")
    ax.set_title("digits 64차원 — 누적 설명분산 곡선")
    ax.legend(loc="lower right"); ax.set_ylim(0, 1.02)
    fig.tight_layout(); fig.savefig(CHARTS / "ch02_cumvar.png", dpi=110); plt.close(fig)
    print("[chart] ch02_cumvar.png 저장")


# ── §03: 2D로 줄여 군집을 눈으로 본다 — PCA 2D scatter ────────────────────
def s03_pca_2d():
    """64차원을 단 2개 주성분으로 투영하면 숫자 0~9 군집이 눈에 보일까?
    PCA 2D는 단 2개 축이라 설명분산은 얼마 안 되지만, 큰 덩어리 구조는 드러난다."""
    d = load_digits()
    X = StandardScaler().fit_transform(d.data)
    pca = PCA(n_components=2, random_state=SEED)
    Z = pca.fit_transform(X)
    print(f"PCA 2D 설명분산비: PC1={pca.explained_variance_ratio_[0]:.4f}, "
          f"PC2={pca.explained_variance_ratio_[1]:.4f}, "
          f"합={pca.explained_variance_ratio_.sum():.4f}")
    print("→ 2개 축만으로는 전체 분산의 일부만 담지만, 군집 윤곽은 확인 가능하다.")

    fig, ax = plt.subplots(figsize=(7, 6))
    sc = ax.scatter(Z[:, 0], Z[:, 1], c=d.target, cmap="tab10", s=12, alpha=0.7)
    ax.set_xlabel("PC1"); ax.set_ylabel("PC2")
    ax.set_title("digits PCA 2D — 색=숫자 라벨 0~9")
    fig.colorbar(sc, ax=ax, ticks=range(10), label="숫자 라벨")
    fig.tight_layout(); fig.savefig(CHARTS / "ch03_pca_scatter.png", dpi=110); plt.close(fig)
    print("[chart] ch03_pca_scatter.png 저장")


# ── §04: 정보 손실 — k개 주성분으로 복원하면 얼마나 흐려지나 ────────────────
def s04_reconstruct():
    """PCA는 k개 축에 투영했다가 다시 원래 공간으로 되돌릴 수 있다(inverse_transform).
    k가 작을수록 복원 오차가 커진다 — 차원 축소가 곧 정보 손실임을 재구성 오차로 확인한다."""
    d = load_digits()
    X = d.data.astype(float)                  # 원본 픽셀(0~16) — 시각 복원을 위해 비표준화
    print(f"{'k(주성분)':>9} | {'누적설명분산':>12} | {'평균 재구성 MSE':>16}")
    print("-" * 46)
    ks = [2, 8, 16, 32, 64]
    recons = {}
    for k in ks:
        pca = PCA(n_components=k, random_state=SEED).fit(X)
        Z = pca.transform(X)
        Xr = pca.inverse_transform(Z)         # k차원 → 64차원 복원
        mse = np.mean((X - Xr) ** 2)
        evr = pca.explained_variance_ratio_.sum()
        recons[k] = Xr
        print(f"{k:>9} | {evr:12.4f} | {mse:16.4f}")
    print("→ k가 작을수록 복원 MSE가 커진다 = 버린 주성분만큼 정보가 사라진다.")

    # 숫자 한 개를 k별로 복원해 시각 비교
    idx = 0
    fig, axes = plt.subplots(1, len(ks) + 1, figsize=(2.1 * (len(ks) + 1), 2.4))
    axes[0].imshow(X[idx].reshape(8, 8), cmap="gray_r"); axes[0].set_title("원본(64D)")
    for ax, k in zip(axes[1:], ks):
        ax.imshow(recons[k][idx].reshape(8, 8), cmap="gray_r")
        ax.set_title(f"k={k}")
    for ax in axes:
        ax.set_xticks([]); ax.set_yticks([])
    fig.suptitle("PCA 재구성 — 주성분 k개로 되돌린 숫자 (정보 손실)")
    fig.tight_layout(); fig.savefig(CHARTS / "ch04_reconstruct.png", dpi=110); plt.close(fig)
    print("[chart] ch04_reconstruct.png 저장")


# ── §05: 비선형 구조 — PCA로 부족한 곳, t-SNE 맛보기 ──────────────────────
def s05_tsne():
    """PCA는 직선 투영이라 비선형으로 휘감긴 군집을 잘 못 편다.
    t-SNE는 이웃 관계(국소 거리)를 보존하려 해서 같은 숫자끼리 더 또렷이 뭉친다 — 둘을 같은 데이터로 비교한다."""
    d = load_digits()
    X = StandardScaler().fit_transform(d.data)
    y = d.target

    pca2 = PCA(n_components=2, random_state=SEED).fit_transform(X)

    tsne = TSNE(n_components=2, perplexity=30, init="pca",
                learning_rate="auto", random_state=SEED)
    emb = tsne.fit_transform(X)
    print(f"t-SNE 수렴 KL divergence: {tsne.kl_divergence_:.4f}")

    # 군집 분리도를 한 숫자로: 같은 라벨 평균거리 / 다른 라벨 평균거리 (작을수록 잘 뭉침)
    def separation(Z):
        Z = StandardScaler().fit_transform(Z)         # 스케일 통일 후 공정 비교
        D = pairwise_distances(Z)
        same = np.array([D[i][y == y[i]].mean() for i in range(len(Z))]).mean()
        diff = np.array([D[i][y != y[i]].mean() for i in range(len(Z))]).mean()
        return same, diff, same / diff
    ps, pd_, pr = separation(pca2)
    ts, td, tr = separation(emb)
    print(f"PCA   2D: 동일라벨 평균거리={ps:.3f}, 타라벨={pd_:.3f}, 비율(낮을수록 응집)={pr:.4f}")
    print(f"t-SNE 2D: 동일라벨 평균거리={ts:.3f}, 타라벨={td:.3f}, 비율(낮을수록 응집)={tr:.4f}")
    print("→ t-SNE의 동일/타 라벨 거리 비율이 더 작다 = 같은 숫자끼리 더 또렷이 뭉쳤다.")

    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    for ax, Z, title in [(axes[0], pca2, "PCA 2D (선형 투영)"),
                         (axes[1], emb, "t-SNE 2D (이웃 보존)")]:
        sc = ax.scatter(Z[:, 0], Z[:, 1], c=y, cmap="tab10", s=10, alpha=0.7)
        ax.set_title(title); ax.set_xticks([]); ax.set_yticks([])
    fig.colorbar(sc, ax=axes, ticks=range(10), label="숫자 라벨", shrink=0.8)
    fig.savefig(CHARTS / "ch05_tsne.png", dpi=110, bbox_inches="tight"); plt.close(fig)
    print("[chart] ch05_tsne.png 저장")


# ── §06: 다른 데이터에서도 — iris / breast_cancer 차원 축소 ────────────────
def s06_other():
    """digits 외 데이터에서도 같은 원리가 성립하는지 확인한다.
    iris(4특성)·breast_cancer(30특성)를 2D PCA로 줄였을 때 보존 분산과 군집 분리를 본다."""
    for name, loader in [("iris(4특성·3클래스)", load_iris),
                         ("breast_cancer(30특성·2클래스)", load_breast_cancer)]:
        ds = loader()
        X = StandardScaler().fit_transform(ds.data)
        pca = PCA(n_components=2, random_state=SEED).fit(X)
        full = PCA(random_state=SEED).fit(X)
        cum = np.cumsum(full.explained_variance_ratio_)
        k90 = int(np.searchsorted(cum, 0.90) + 1)
        print(f"[{name}]")
        print(f"  PCA 2D 보존 분산 = {pca.explained_variance_ratio_.sum():.4f}")
        print(f"  90% 분산 보존에 필요한 주성분 = {k90}개 (전체 {X.shape[1]}개 중)")


if __name__ == "__main__":
    run_section("00_curse", s00_curse)
    run_section("0a_cov_by_hand", s0a_cov_by_hand)
    run_section("01_axes", s01_axes)
    run_section("02_explained", s02_explained)
    run_section("03_pca_2d", s03_pca_2d)
    run_section("04_reconstruct", s04_reconstruct)
    run_section("05_tsne", s05_tsne)
    run_section("06_other", s06_other)
    print("\n완료: logs/*.txt, charts/*.png 생성")
