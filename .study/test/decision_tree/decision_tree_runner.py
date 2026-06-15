# decision_tree_runner.py
# 머신러닝 Day4 (0601) — 결정트리와 회귀트리 섹션별 테스트 실행기
# 실행: c:\_proj\python_workspace\.venv\Scripts\python.exe decision_tree_runner.py
# 결과: logs/{섹션명}.txt 저장 + 터미널 출력,  charts/*.png 생성
# 데이터: sklearn 내장 iris(분류)·wine(분류) + 1차원 합성곡선(회귀트리 계단 시각화)
#   ※ 수업 실습 코드(../ml_workspace/from_colab/0601-s)는 PyTorch + German Credit 기반이라
#     결정트리의 분할 기준(지니/엔트로피)·과대적합·feature_importances_ 를 또렷이 보이려고
#     sklearn 내장 iris/wine 으로 새로 작성한다(§16-C 우선순위 2, 사유 명시).

import sys, io, pathlib
from contextlib import redirect_stdout

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# 차트 한글 렌더링 (Windows 기본 한글 폰트)
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

from sklearn.datasets import load_iris, load_wine
from sklearn.tree import (DecisionTreeClassifier, DecisionTreeRegressor,
                          export_text, plot_tree)
from sklearn.model_selection import train_test_split

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


# ── §00: 직선으로 못 가르는 데이터 — if-else 질문으로 나눈다 ────────────────
def s00_why_tree():
    """선형 경계 하나로는 못 가르는 배치도, 축에 평행한 if-else 질문을 거듭하면
    영역을 직사각형으로 쪼개 분리할 수 있다. 그 '질문 한 번'이 트리의 노드다."""
    # XOR 형태: 한 직선으로는 절대 못 가르는 4분면 배치
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
    y = np.array([0, 1, 1, 0])  # 대각선끼리 같은 클래스 (XOR)
    print("XOR 배치 — 한 직선으로는 0/1 을 가를 수 없는 데이터:")
    for (a, b), label in zip(X, y):
        print(f"  x1={a:.0f}, x2={b:.0f}  → 클래스 {label}")

    # if-else 질문(결정트리)은 축에 평행한 분할을 거듭해 정확히 가른다
    tree = DecisionTreeClassifier(random_state=SEED).fit(X, y)
    print(f"\n결정트리 학습 정확도: {tree.score(X, y):.4f}  (XOR 도 완벽 분리)")
    print(f"트리 깊이(depth): {tree.get_depth()},  잎(leaf) 개수: {tree.get_n_leaves()}")
    print("\n트리가 만든 if-else 규칙:")
    print(export_text(tree, feature_names=['x1', 'x2']))


# ── §01: 어떤 기준으로 분할? — 지니 불순도 / 엔트로피 정보이득 ──────────────
def s01_impurity():
    """노드를 '어떤 질문으로' 나눌지는 자식 노드의 불순도(섞인 정도)를 가장 많이
    낮추는 질문으로 정한다. 지니 불순도와 엔트로피를 직접 계산해 그 의미를 본다."""
    def gini(counts):
        n = sum(counts)
        p = [c / n for c in counts]
        return 1.0 - sum(pi * pi for pi in p)

    def entropy(counts):
        n = sum(counts)
        h = 0.0
        for c in counts:
            if c == 0:
                continue
            pi = c / n
            h -= pi * np.log2(pi)
        return h

    print("불순도 = 한 노드 안에 클래스가 얼마나 섞여 있나 (0=순수)")
    for label, counts in [("완전 순수 [50,0]", [50, 0]),
                          ("약간 섞임 [40,10]", [40, 10]),
                          ("반반 [25,25]", [25, 25])]:
        print(f"  {label:<18} gini={gini(counts):.4f}  entropy={entropy(counts):.4f}")

    # 정보이득(IG) = 부모 불순도 - 가중평균(자식 불순도)
    parent = [50, 50]
    # 어떤 질문이 두 자식을 [50,10],[0,40] 로 가른다고 하자
    left, right = [50, 10], [0, 40]
    nL, nR = sum(left), sum(right)
    n = nL + nR
    ig = gini(parent) - (nL / n * gini(left) + nR / n * gini(right))
    print(f"\n부모 [50,50] gini={gini(parent):.4f}")
    print(f"분할 후 자식: 왼쪽{left} gini={gini(left):.4f}, 오른쪽{right} gini={gini(right):.4f}")
    print(f"가중평균 자식 불순도 = {nL/n*gini(left)+nR/n*gini(right):.4f}")
    print(f"정보이득(불순도 감소량) = {ig:.4f}  ← 트리는 이 값이 가장 큰 질문을 고른다")

    # 불순도 곡선 차트
    ps = np.linspace(1e-6, 1 - 1e-6, 200)
    gini_curve = 1 - (ps ** 2 + (1 - ps) ** 2)
    ent_curve = -(ps * np.log2(ps) + (1 - ps) * np.log2(1 - ps))
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(ps, gini_curve, color="#52A97E", lw=2.2, label="지니 불순도")
    ax.plot(ps, ent_curve, color="#9178C4", lw=2.2, label="엔트로피")
    ax.set_xlabel("클래스 1의 비율 p"); ax.set_ylabel("불순도")
    ax.set_title("불순도는 p=0.5(반반)에서 최대, p=0/1(순수)에서 0")
    ax.legend(); fig.tight_layout()
    fig.savefig(CHARTS / "ch01_impurity.png", dpi=110); plt.close(fig)
    print("\n[chart] ch01_impurity.png 저장")


# ── §02: gini vs entropy — 기준을 바꾸면 결과가 달라지나 ────────────────────
def s02_gini_vs_entropy():
    """분할 기준(criterion)을 gini 와 entropy 로 바꿔 같은 iris 를 학습한다.
    둘은 철학은 다르지만 실제 분류 정확도는 거의 같다 — 어느 쪽이 본질인가."""
    iris = load_iris()
    Xtr, Xte, ytr, yte = train_test_split(iris.data, iris.target, test_size=0.3,
                                          random_state=SEED, stratify=iris.target)
    print(f"{'criterion':>10} | {'train acc':>9} | {'test acc':>9} | {'depth':>5} | {'leaves':>6}")
    print("-" * 52)
    for crit in ["gini", "entropy"]:
        clf = DecisionTreeClassifier(criterion=crit, random_state=SEED).fit(Xtr, ytr)
        print(f"{crit:>10} | {clf.score(Xtr,ytr):9.4f} | {clf.score(Xte,yte):9.4f} | "
              f"{clf.get_depth():5d} | {clf.get_n_leaves():6d}")
    print("\n→ 두 기준 모두 train 은 1.0(완벽 암기), test 는 거의 동일.")
    print("  분할 기준의 선택보다, 트리를 '얼마나 깊게' 키우느냐가 성능을 가른다.")


# ── §03: 깊이를 키우면? — 과대적합, 잎이 1개 샘플까지 ──────────────────────
def s03_depth_overfit():
    """max_depth 를 1→None 으로 키우며 train/test 정확도를 본다. 깊이를 무한정 키우면
    train 은 1.0 까지 오르지만(잎마다 샘플 1개) test 는 정체·하락 → 과대적합."""
    iris = load_iris()
    Xtr, Xte, ytr, yte = train_test_split(iris.data, iris.target, test_size=0.3,
                                          random_state=SEED, stratify=iris.target)
    depths = [1, 2, 3, 4, 5, 6, None]
    tr_scores, te_scores, xs = [], [], []
    print(f"{'max_depth':>9} | {'train acc':>9} | {'test acc':>9} | {'leaves':>6} | gap")
    print("-" * 56)
    for i, d in enumerate(depths):
        clf = DecisionTreeClassifier(max_depth=d, random_state=SEED).fit(Xtr, ytr)
        tr, te = clf.score(Xtr, ytr), clf.score(Xte, yte)
        tr_scores.append(tr); te_scores.append(te)
        xs.append(i)
        label = "None(무제한)" if d is None else str(d)
        print(f"{label:>9} | {tr:9.4f} | {te:9.4f} | {clf.get_n_leaves():6d} | {tr-te:+.4f}")

    fig, ax = plt.subplots(figsize=(6.4, 4))
    ax.plot(xs, tr_scores, "o-", color="#5B9BD5", label="train 정확도")
    ax.plot(xs, te_scores, "s-", color="#E8875A", label="test 정확도")
    ax.set_xticks(xs)
    ax.set_xticklabels(["1", "2", "3", "4", "5", "6", "None"])
    ax.set_xlabel("max_depth (트리 최대 깊이)"); ax.set_ylabel("정확도")
    ax.set_title("깊이↑ → train 1.0 으로 암기, test 는 더 안 오름(과대적합)")
    ax.legend(); ax.set_ylim(0.6, 1.05); fig.tight_layout()
    fig.savefig(CHARTS / "ch03_depth_accuracy.png", dpi=110); plt.close(fig)
    print("\n[chart] ch03_depth_accuracy.png 저장")


# ── §04: 가지치기 — max_depth / min_samples_leaf 로 일반화 회복 ────────────
def s04_pruning():
    """무제한 트리(과대적합) vs 가지치기(max_depth·min_samples_leaf) 비교.
    적절히 가지치기하면 train 정확도는 조금 내려가도 test 정확도는 유지/상승한다."""
    iris = load_iris()
    Xtr, Xte, ytr, yte = train_test_split(iris.data, iris.target, test_size=0.3,
                                          random_state=SEED, stratify=iris.target)
    configs = [
        ("무제한(과대적합)", dict()),
        ("max_depth=3", dict(max_depth=3)),
        ("min_samples_leaf=5", dict(min_samples_leaf=5)),
        ("max_depth=3 + leaf>=5", dict(max_depth=3, min_samples_leaf=5)),
    ]
    print(f"{'설정':<22} | {'train':>7} | {'test':>7} | {'leaves':>6}")
    print("-" * 52)
    for name, kw in configs:
        clf = DecisionTreeClassifier(random_state=SEED, **kw).fit(Xtr, ytr)
        print(f"{name:<22} | {clf.score(Xtr,ytr):7.4f} | {clf.score(Xte,yte):7.4f} | "
              f"{clf.get_n_leaves():6d}")
    print("\n→ 잎을 줄이면(가지치기) train 암기는 풀리고 test 일반화는 유지된다.")


# ── §05: 트리의 장점 — feature_importances_ + 규칙을 그림으로 ──────────────
def s05_importance_plot():
    """결정트리는 '어떤 특성이 분류에 중요했나'(불순도 감소 합)를 숫자로 주고,
    규칙 전체를 그림 한 장으로 보여준다 — 해석 가능성이 트리의 핵심 강점."""
    iris = load_iris()
    clf = DecisionTreeClassifier(max_depth=3, random_state=SEED).fit(iris.data, iris.target)
    print("feature_importances_ (불순도 감소 기여도, 합=1):")
    order = np.argsort(clf.feature_importances_)[::-1]
    for i in order:
        bar = "█" * int(round(clf.feature_importances_[i] * 40))
        print(f"  {iris.feature_names[i]:<20} {clf.feature_importances_[i]:.4f} {bar}")
    top = iris.feature_names[order[0]]
    print(f"\n가장 중요한 특성: {top} (importance={clf.feature_importances_[order[0]]:.4f})")

    # (1) 특성 중요도 막대
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.barh([iris.feature_names[i] for i in order],
            [clf.feature_importances_[i] for i in order], color="#52A97E")
    ax.invert_yaxis(); ax.set_xlabel("중요도 (불순도 감소 합)")
    ax.set_title("iris 특성 중요도 — petal 두 특성이 분류를 지배")
    fig.tight_layout(); fig.savefig(CHARTS / "ch05_importance.png", dpi=110); plt.close(fig)
    print("[chart] ch05_importance.png 저장")

    # (2) 트리 다이어그램 (규칙을 그림으로)
    fig, ax = plt.subplots(figsize=(11, 6))
    plot_tree(clf, feature_names=iris.feature_names, class_names=list(iris.target_names),
              filled=True, rounded=False, fontsize=9, ax=ax)
    ax.set_title("iris 결정트리 (max_depth=3) — 각 노드가 하나의 if-else 질문")
    fig.tight_layout(); fig.savefig(CHARTS / "ch05_tree.png", dpi=110); plt.close(fig)
    print("[chart] ch05_tree.png 저장")


# ── §06: 회귀트리 — 잎의 '평균값'으로 예측한다(계단 함수) ──────────────────
def s06_regression_tree():
    """분류트리가 잎에서 '다수결'을 하듯, 회귀트리는 잎에 속한 샘플들의 '평균값'을
    예측으로 내놓는다. 그래서 예측이 직선이 아니라 계단 함수가 된다."""
    rng = np.random.RandomState(SEED)
    X = np.sort(5 * rng.rand(120, 1), axis=0)
    y = np.sin(X).ravel() + rng.normal(0, 0.1, X.shape[0])  # sin 곡선 + 노이즈

    xs = np.linspace(0, 5, 500).reshape(-1, 1)
    fig, ax = plt.subplots(figsize=(6.6, 4.2))
    ax.scatter(X, y, s=14, color="#cbd5e1", label="데이터(sin+노이즈)")
    colors = {2: "#5B9BD5", 5: "#E8875A"}
    for depth in [2, 5]:
        reg = DecisionTreeRegressor(max_depth=depth, random_state=SEED).fit(X, y)
        pred = reg.predict(xs)
        ax.plot(xs, pred, color=colors[depth], lw=2.2, label=f"회귀트리 depth={depth}")
        print(f"depth={depth}: 잎 {reg.get_n_leaves()}개  "
              f"→ 예측값 종류 {len(np.unique(reg.predict(xs)))}개 (각 잎의 평균값)")
    ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.set_title("회귀트리는 잎의 평균값을 출력 → 계단 함수")
    ax.legend(); fig.tight_layout()
    fig.savefig(CHARTS / "ch06_regression_step.png", dpi=110); plt.close(fig)
    print("\n→ 깊을수록 계단이 잘게 쪼개져 데이터에 더 밀착(과대적합 위험).")
    print("[chart] ch06_regression_step.png 저장")


# ── §07: 회귀트리 깊이 효과 — train/test 오차로 본 과대적합 ────────────────
def s07_regression_depth():
    """회귀트리도 깊이를 키우면 train 오차는 0 으로 가지만 test 오차는 어느 깊이부터
    다시 커진다. 회귀에서도 '깊이 = 과대적합'이라는 같은 법칙이 작동함을 수치로 확인."""
    rng = np.random.RandomState(SEED)
    X = np.sort(5 * rng.rand(200, 1), axis=0)
    y = np.sin(X).ravel() + rng.normal(0, 0.15, X.shape[0])
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=SEED)

    from sklearn.metrics import mean_squared_error
    print(f"{'max_depth':>9} | {'train MSE':>10} | {'test MSE':>10} | {'leaves':>6}")
    print("-" * 48)
    for d in [1, 2, 3, 5, 8, None]:
        reg = DecisionTreeRegressor(max_depth=d, random_state=SEED).fit(Xtr, ytr)
        tr = mean_squared_error(ytr, reg.predict(Xtr))
        te = mean_squared_error(yte, reg.predict(Xte))
        label = "None" if d is None else str(d)
        flag = "  ← train 0 암기" if tr < 1e-6 else ""
        print(f"{label:>9} | {tr:10.5f} | {te:10.5f} | {reg.get_n_leaves():6d}{flag}")
    print("\n→ 깊이 무제한이면 train MSE≈0(잎=샘플1개) 이지만 test MSE 는 다시 커진다.")


if __name__ == "__main__":
    run_section("00_why_tree", s00_why_tree)
    run_section("01_impurity", s01_impurity)
    run_section("02_gini_vs_entropy", s02_gini_vs_entropy)
    run_section("03_depth_overfit", s03_depth_overfit)
    run_section("04_pruning", s04_pruning)
    run_section("05_importance_plot", s05_importance_plot)
    run_section("06_regression_tree", s06_regression_tree)
    run_section("07_regression_depth", s07_regression_depth)
    print("\n완료: logs/*.txt, charts/*.png 생성")
