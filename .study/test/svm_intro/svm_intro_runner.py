# svm_intro_runner.py
# 머신러닝 Day3 (0529) — 서포트 벡터 머신(SVM) 구조 섹션별 테스트 실행기
# 실행: c:\_proj\python_workspace\.venv\Scripts\python.exe svm_intro_runner.py
# 결과: logs/{섹션명}.txt 저장 + 터미널 출력,  charts/*.png 생성
# 데이터: sklearn 내장 iris(2클래스 추출)·make_moons·make_circles — 외부 파일 없이 재현(고정 시드 42)
#   ※ 수업 실습(../ml_workspace/from_colab/0529-s/pytorch_svm_*.ipynb)은 UCI Letter 글자 분류
#     (LinearSVM·RBF Random Fourier Features)였다. 여기서는 같은 개념(마진·서포트 벡터·RBF 커널·
#     C/gamma)을 2D 로 눈에 보이게 검증하려고 sklearn SVC 로 새로 작성(§16-C 우선순위 2, 사유 명시).

import sys, io, pathlib
from contextlib import redirect_stdout

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# 차트 한글 렌더링 (Windows 기본 한글 폰트) — 폰트 경고 0 목표
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

from sklearn.svm import SVC
from sklearn.datasets import load_iris, make_moons, make_circles
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline

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


def _mesh(X, h=0.02, pad=0.5):
    x0, x1 = X[:, 0].min() - pad, X[:, 0].max() + pad
    y0, y1 = X[:, 1].min() - pad, X[:, 1].max() + pad
    xx, yy = np.meshgrid(np.arange(x0, x1, h), np.arange(y0, y1, h))
    return xx, yy


# 선형 분리 가능한 2D 2클래스 데이터 (iris 의 setosa vs versicolor, 꽃잎 길이·너비)
def _iris_2class():
    iris = load_iris()
    mask = iris.target < 2                 # setosa(0) vs versicolor(1) — 선형 분리 가능
    X = iris.data[mask][:, [2, 3]]         # petal length, petal width
    y = iris.target[mask]
    return X, y, ("petal length(cm)", "petal width(cm)"), ("setosa", "versicolor")


# ── §01: 마진과 서포트 벡터 — 선형 SVM 이 정하는 경계 ─────────────────────
def s01_margin_support_vectors():
    """선형 SVM 은 두 클래스 사이 '가장 넓은 도로(마진)'의 한가운데에 경계를 둔다.
    경계를 떠받치는 점(서포트 벡터)의 개수와 마진 폭을 직접 꺼내 본다."""
    X, y, _, _ = _iris_2class()
    Xs = StandardScaler().fit_transform(X)
    clf = SVC(kernel="linear", C=1.0).fit(Xs, y)
    # 마진 폭 = 2 / ||w||  (결정함수 f(x)=w·x+b, 서포트 벡터에서 |f|=1)
    w = clf.coef_[0]
    margin = 2.0 / np.linalg.norm(w)
    print(f"데이터: iris setosa vs versicolor, 표준화된 꽃잎 2특성, 표본 {len(y)}개")
    print(f"학습 정확도: {clf.score(Xs, y):.4f}")
    print(f"가중치 w = {np.round(w, 4)},  ||w|| = {np.linalg.norm(w):.4f}")
    print(f"마진 폭(2/||w||) = {margin:.4f}")
    print(f"서포트 벡터 개수: {clf.n_support_} (클래스별), 합계 {clf.support_vectors_.shape[0]}개")
    print(f"전체 {len(y)}개 중 경계를 정하는 점은 {clf.support_vectors_.shape[0]}개뿐 "
          f"({clf.support_vectors_.shape[0]/len(y)*100:.1f}%)")

    # 시각화: 결정경계 + 마진 점선 + 서포트 벡터 강조
    fig, ax = plt.subplots(figsize=(6, 4.6))
    ax.scatter(Xs[y == 0, 0], Xs[y == 0, 1], c="#5B9BD5", s=30, label="setosa")
    ax.scatter(Xs[y == 1, 0], Xs[y == 1, 1], c="#E8875A", s=30, label="versicolor")
    sv = clf.support_vectors_
    ax.scatter(sv[:, 0], sv[:, 1], s=170, facecolors="none",
               edgecolors="#52A97E", linewidths=2.0, label="서포트 벡터")
    xx, yy = _mesh(Xs)
    Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
    ax.contour(xx, yy, Z, levels=[-1, 0, 1], colors=["#999", "#1f2933", "#999"],
               linestyles=["--", "-", "--"], linewidths=[1, 2, 1])
    ax.set_xlabel("표준화된 petal length"); ax.set_ylabel("표준화된 petal width")
    ax.set_title(f"선형 SVM — 마진 폭 {margin:.3f}, 서포트 벡터 {sv.shape[0]}개")
    ax.legend(loc="upper left", fontsize=8); fig.tight_layout()
    fig.savefig(CHARTS / "ch_margin.png", dpi=110); plt.close(fig)
    print("[chart] ch_margin.png 저장")


# ── §02: 왜 '가장 넓은 도로'인가 — 경계를 평행이동하면 마진이 줄어든다 ─────
def s02_why_max_margin():
    """같은 데이터를 가르는 여러 직선 중 SVM 직선만이 마진을 최대화한다.
    SVM 경계를 일부러 평행이동시킨 후보들과 '가장 가까운 점까지의 거리'를 비교한다."""
    X, y, _, _ = _iris_2class()
    Xs = StandardScaler().fit_transform(X)
    clf = SVC(kernel="linear", C=1.0).fit(Xs, y)
    w = clf.coef_[0]; b = clf.intercept_[0]
    nw = np.linalg.norm(w)

    def min_dist(shift):
        # 경계를 b 방향으로 shift 만큼 평행이동했을 때, 두 클래스 점 중 가장 가까운 거리
        f = (Xs @ w + (b + shift)) / nw
        d0 = np.abs(f[y == 0]).min()   # 클래스0 중 가장 가까운 점
        d1 = np.abs(f[y == 1]).min()   # 클래스1 중 가장 가까운 점
        return d0, d1, min(d0, d1)

    print("같은 두 클래스를 모두 가르되, 경계를 평행이동한 후보들의 '가장 가까운 점까지 거리':")
    print(f"{'이동량':>8} | {'클래스0 최근접':>12} | {'클래스1 최근접':>12} | {'마진(둘 중 작은값)':>16}")
    print("-" * 60)
    best = None
    for shift in [-0.6, -0.3, 0.0, 0.3, 0.6]:
        d0, d1, m = min_dist(shift)
        tag = "  ← SVM 경계" if abs(shift) < 1e-9 else ""
        if best is None or m > best[1]:
            best = (shift, m)
        print(f"{shift:>8.1f} | {d0:12.4f} | {d1:12.4f} | {m:16.4f}{tag}")
    print(f"\n마진이 가장 큰 위치: 이동량 {best[0]:.1f} (= SVM 경계, 이동 0). "
          f"옆으로 밀면 한쪽 클래스에 가까워져 마진이 줄어든다.")


# ── §03: 선형으로 안 갈리는 데이터 — RBF 커널 트릭 ────────────────────────
def s03_kernel_moons():
    """초승달(make_moons)처럼 직선 하나로 못 가르는 데이터에서 선형 SVM 은 실패하고,
    RBF 커널은 비선형 경계를 그려 해결한다. 두 모델의 test 정확도를 비교한다."""
    X, y = make_moons(n_samples=300, noise=0.20, random_state=SEED)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=SEED)

    lin = make_pipeline(StandardScaler(), SVC(kernel="linear", C=1.0)).fit(Xtr, ytr)
    rbf = make_pipeline(StandardScaler(), SVC(kernel="rbf", C=1.0, gamma="scale")).fit(Xtr, ytr)
    print("make_moons (noise=0.20) — 직선으로 가를 수 없는 데이터")
    print(f"  선형 커널 SVM  test 정확도 = {lin.score(Xte, yte):.4f}")
    print(f"  RBF  커널 SVM  test 정확도 = {rbf.score(Xte, yte):.4f}")
    print(f"  → RBF 가 선형보다 {(rbf.score(Xte,yte)-lin.score(Xte,yte))*100:+.1f}%p 높다")

    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    for ax, model, title in [(axes[0], lin, "선형 커널 (직선)"),
                             (axes[1], rbf, "RBF 커널 (곡선)")]:
        xx, yy = _mesh(X, h=0.02, pad=0.4)
        Z = model.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
        ax.contourf(xx, yy, Z, alpha=0.18, cmap="coolwarm")
        ax.scatter(X[y == 0, 0], X[y == 0, 1], c="#5B9BD5", s=12)
        ax.scatter(X[y == 1, 0], X[y == 1, 1], c="#E8875A", s=12)
        acc = model.score(Xte, yte)
        ax.set_title(f"{title}  acc={acc:.3f}")
        ax.set_xticks([]); ax.set_yticks([])
    fig.tight_layout(); fig.savefig(CHARTS / "ch_kernel.png", dpi=110); plt.close(fig)
    print("[chart] ch_kernel.png 저장")


# ── §04: RBF 가 사상하는 공간 — circles 로 한 번 더 확인 ───────────────────
def s04_circles():
    """동심원(make_circles)도 직선으로 못 가른다. RBF 커널이 '거리 기반 유사도'로
    안쪽 원과 바깥 원을 분리함을 정확도로 확인한다(커널 트릭의 일반성)."""
    X, y = make_circles(n_samples=300, noise=0.08, factor=0.4, random_state=SEED)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=SEED)
    lin = make_pipeline(StandardScaler(), SVC(kernel="linear")).fit(Xtr, ytr)
    rbf = make_pipeline(StandardScaler(), SVC(kernel="rbf", gamma="scale")).fit(Xtr, ytr)
    print("make_circles (동심원) — 안쪽 원 vs 바깥 원")
    print(f"  선형 커널 SVM  test 정확도 = {lin.score(Xte, yte):.4f}  (직선으론 동심원 분리 불가)")
    print(f"  RBF  커널 SVM  test 정확도 = {rbf.score(Xte, yte):.4f}")


# ── §05: C·gamma 를 키우면 — 과대적합 경계 ────────────────────────────────
def s05_C_gamma_overfit():
    """C(오분류 허용)와 gamma(RBF 영향 반경)를 키우면 경계가 train 에 딱 달라붙어
    train 정확도는 오르지만 test 정확도는 떨어진다(과대적합). 수치로 확인한다."""
    X, y = make_moons(n_samples=300, noise=0.30, random_state=SEED)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=SEED)
    sc = StandardScaler().fit(Xtr)
    Xtr_s, Xte_s = sc.transform(Xtr), sc.transform(Xte)

    print("RBF SVM — C·gamma 를 키우며 train/test 정확도 (make_moons, noise=0.30)")
    print(f"{'C':>8} | {'gamma':>8} | {'train acc':>10} | {'test acc':>9}")
    print("-" * 46)
    settings = [(1.0, 0.5), (1.0, 5.0), (100.0, 5.0), (1000.0, 50.0)]
    rows = []
    for C, g in settings:
        m = SVC(kernel="rbf", C=C, gamma=g).fit(Xtr_s, ytr)
        tr, te = m.score(Xtr_s, ytr), m.score(Xte_s, yte)
        rows.append((C, g, tr, te))
        flag = "  ← 과대적합(train↑ test↓)" if (tr - te) > 0.10 else ""
        print(f"{C:>8} | {g:>8} | {tr:10.4f} | {te:9.4f}{flag}")
    base = rows[0]; worst = max(rows, key=lambda r: r[2] - r[3])
    print(f"\n적당한 (C={base[0]}, gamma={base[1]}): train {base[2]:.4f} / test {base[3]:.4f} (격차 {base[2]-base[3]:+.4f})")
    print(f"과한   (C={worst[0]}, gamma={worst[1]}): train {worst[2]:.4f} / test {worst[3]:.4f} (격차 {worst[2]-worst[3]:+.4f})")

    # 시각화: gamma 작음 vs 큼
    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    for ax, (C, g, title) in zip(axes, [(1.0, 0.5, "C=1, gamma=0.5 (매끈)"),
                                        (1000.0, 50.0, "C=1000, gamma=50 (과대적합)")]):
        m = SVC(kernel="rbf", C=C, gamma=g).fit(Xtr_s, ytr)
        xx, yy = _mesh(Xtr_s, h=0.02, pad=0.4)
        Z = m.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
        ax.contourf(xx, yy, Z, alpha=0.18, cmap="coolwarm")
        ax.scatter(Xtr_s[ytr == 0, 0], Xtr_s[ytr == 0, 1], c="#5B9BD5", s=12)
        ax.scatter(Xtr_s[ytr == 1, 0], Xtr_s[ytr == 1, 1], c="#E8875A", s=12)
        ax.set_title(f"{title}  test={m.score(Xte_s,yte):.3f}")
        ax.set_xticks([]); ax.set_yticks([])
    fig.tight_layout(); fig.savefig(CHARTS / "ch_cgamma.png", dpi=110); plt.close(fig)
    print("[chart] ch_cgamma.png 저장")


# ── §06: 경계 모양 비교 — SVM vs LogisticRegression vs KNN ────────────────
def s06_boundary_compare():
    """같은 make_moons 데이터에 세 분류기를 학습해 경계의 '모양'과 test 정확도를 비교한다.
    로지스틱=직선, KNN=울퉁불퉁, RBF SVM=매끄러운 곡선."""
    X, y = make_moons(n_samples=300, noise=0.20, random_state=SEED)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=SEED)
    models = {
        "LogisticRegression": make_pipeline(StandardScaler(), LogisticRegression()),
        "KNN(k=5)": make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5)),
        "SVM(RBF)": make_pipeline(StandardScaler(), SVC(kernel="rbf", gamma="scale")),
    }
    print("같은 make_moons 에서 세 분류기 test 정확도 + 경계 모양")
    print(f"{'모델':>20} | {'test acc':>9} | 경계 모양")
    print("-" * 56)
    shapes = {"LogisticRegression": "직선(선형)", "KNN(k=5)": "조각조각(국소적)", "SVM(RBF)": "매끄러운 곡선"}
    fitted = {}
    for name, m in models.items():
        m.fit(Xtr, ytr)
        fitted[name] = m
        print(f"{name:>20} | {m.score(Xte, yte):9.4f} | {shapes[name]}")

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    for ax, (name, m) in zip(axes, fitted.items()):
        xx, yy = _mesh(X, h=0.02, pad=0.4)
        Z = m.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
        ax.contourf(xx, yy, Z, alpha=0.18, cmap="coolwarm")
        ax.scatter(X[y == 0, 0], X[y == 0, 1], c="#5B9BD5", s=10)
        ax.scatter(X[y == 1, 0], X[y == 1, 1], c="#E8875A", s=10)
        ax.set_title(f"{name}\nacc={m.score(Xte,yte):.3f}")
        ax.set_xticks([]); ax.set_yticks([])
    fig.tight_layout(); fig.savefig(CHARTS / "ch_compare.png", dpi=110); plt.close(fig)
    print("[chart] ch_compare.png 저장")


if __name__ == "__main__":
    run_section("01_margin_support_vectors", s01_margin_support_vectors)
    run_section("02_why_max_margin", s02_why_max_margin)
    run_section("03_kernel_moons", s03_kernel_moons)
    run_section("04_circles", s04_circles)
    run_section("05_C_gamma_overfit", s05_C_gamma_overfit)
    run_section("06_boundary_compare", s06_boundary_compare)
    print("\n완료: logs/*.txt, charts/*.png 생성")
