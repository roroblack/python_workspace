# clf_logistic_runner.py
# 머신러닝 Day2 (0528) — 회귀모델에서 분류모델로, 로지스틱 회귀 섹션별 테스트 실행기
# 실행: c:\_proj\python_workspace\.venv\Scripts\python.exe clf_logistic_runner.py
# 결과: logs/{섹션명}.txt 저장 + 터미널 출력,  charts/*.png 생성
# 데이터: sklearn 내장 breast_cancer(2분류)·iris(3분류) — 외부 파일 의존 없이 재현 가능(고정 시드)
#   ※ 기존 샘플 없음: ../ml_workspace/from_colab/0528 코드는 PyTorch 회귀(tips) 중심이라
#     "회귀로 분류를 풀면 왜 안 되나 → 로지스틱 회귀" 데모는 sklearn 으로 새로 작성
#     (§16-C 우선순위 2, 사유 명시).

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

from sklearn.datasets import load_breast_cancer, load_iris
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.metrics import (accuracy_score, confusion_matrix,
                             classification_report, precision_score, recall_score)

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


# ── §00: 회귀 vs 분류 — 정답 y 의 형태로 문제를 가른다 ─────────────────────
def s00_task_kind():
    """Day1 은 회귀(연속값 y)였다. Day2 의 데이터는 y 가 0/1 또는 라벨이다.
    같은 판별 함수로 breast_cancer(악성/양성)·iris(3품종)가 '분류'임을 확인한다."""
    bc = load_breast_cancer()
    iris = load_iris()

    def kind(y):
        uniq = np.unique(y)
        is_clf = (len(uniq) <= 20) and np.all(uniq == uniq.astype(int))
        return "분류(Classification)" if is_clf else "회귀(Regression)"

    print("[breast_cancer] X shape:", bc.data.shape, " 라벨:", np.unique(bc.target),
          "=", list(bc.target_names))
    print("  y 예시 10개:", bc.target[:10], "->", kind(bc.target))
    print("[iris]          X shape:", iris.data.shape, " 라벨:", np.unique(iris.target),
          "=", list(iris.target_names))
    print("  y 예시 10개:", iris.target[:10], "->", kind(iris.target))
    print()
    print("핵심: 회귀의 y 는 연속 실수, 분류의 y 는 정해진 몇 개의 정수 라벨이다.")
    print("Day2 의 질문 — 그렇다면 회귀(직선)로 0/1 라벨을 예측하면 무슨 일이 벌어지나?")


# ── §01: 회귀로 분류를 풀면? — 직선은 확률을 [0,1] 밖으로 내보낸다 ──────────
def s01_linear_on_labels():
    """0/1 라벨을 LinearRegression 으로 적합하면, 예측값이 0보다 작거나 1보다 커진다.
    '확률'로 해석할 수 없는 값이 나오는 것 — 회귀를 분류에 그대로 쓰면 안 되는 1차 근거."""
    bc = load_breast_cancer()
    # 가장 분리력이 큰 단일 특성 하나로 1차원 데모(직선의 한계를 또렷이)
    x = bc.data[:, [27]]            # 'worst concave points'
    y = bc.target.astype(float)     # 0=malignant, 1=benign
    lin = LinearRegression().fit(x, y)
    pred = lin.predict(x)
    below = (pred < 0).sum()
    above = (pred > 1).sum()
    print(f"LinearRegression 으로 0/1 라벨 적합 (특성 1개)")
    print(f"  예측값 범위: min={pred.min():.3f}  max={pred.max():.3f}")
    print(f"  0 미만 예측: {below}개,  1 초과 예측: {above}개  (확률이라면 불가능한 값)")
    print(f"  -> 직선은 위/아래로 무한히 뻗으므로 출력을 [0,1] 안에 가둘 수 없다.")

    # 같은 데이터에 로지스틱(시그모이드)을 적합하면 확률은 항상 [0,1]
    log = LogisticRegression().fit(x, y)
    proba = log.predict_proba(x)[:, 1]
    print(f"\nLogisticRegression 의 예측 확률 범위: min={proba.min():.3f}  max={proba.max():.3f}")
    print(f"  -> 시그모이드를 거쳐 항상 0~1 사이. 같은 데이터인데 출력이 '확률'이 됐다.")

    xs = np.linspace(x.min(), x.max(), 300).reshape(-1, 1)
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    ax.scatter(x, y, s=12, alpha=0.35, color="#5B9BD5", label="실제 라벨(0/1)")
    ax.plot(xs, lin.predict(xs), color="#E8875A", lw=2.2, label="선형회귀(직선)")
    ax.plot(xs, log.predict_proba(xs)[:, 1], color="#52A97E", lw=2.4, label="로지스틱(시그모이드)")
    ax.axhline(0, color="#999", lw=0.8, ls="--")
    ax.axhline(1, color="#999", lw=0.8, ls="--")
    ax.set_xlabel("worst concave points (특성값)"); ax.set_ylabel("y / 예측")
    ax.set_title("0/1 라벨: 직선은 [0,1] 을 벗어나고, 시그모이드는 갇힌다")
    ax.legend(loc="center right", fontsize=8); fig.tight_layout()
    fig.savefig(CHARTS / "ch01_linear_vs_logistic.png", dpi=110); plt.close(fig)
    print("[chart] ch01_linear_vs_logistic.png 저장")


# ── §02: 시그모이드 — 직선의 출력을 (0,1) 로 가두는 함수 ───────────────────
def s02_sigmoid():
    """로지스틱 회귀는 선형식 z = w·x + b 를 그대로 두고, 시그모이드 σ(z)=1/(1+e^-z) 로
    감싸 출력을 (0,1) 에 가둔다. z=0 에서 0.5, z→±∞ 에서 1/0 에 수렴함을 수치로 확인."""
    def sigmoid(z):
        # np.clip 으로 exp 오버플로 방지 (수치적으로 안전한 시그모이드)
        z = np.clip(z, -500, 500)
        return 1.0 / (1.0 + np.exp(-z))
    for z in [-6, -2, -1, 0, 1, 2, 6]:
        print(f"  sigma({z:>2}) = {sigmoid(z):.6f}")
    print()
    print(f"  sigma(0)    = {sigmoid(0):.4f}   (z=0 -> 정확히 0.5, 결정의 경계)")
    print(f"  sigma(-1e9) = {sigmoid(-1e9):.4f}   sigma(+1e9) = {sigmoid(1e9):.4f}  (극단에서도 [0,1])")

    z = np.linspace(-8, 8, 400)
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    ax.plot(z, sigmoid(z), color="#52A97E", lw=2.6)
    ax.axhline(0.5, color="#E8875A", lw=1.0, ls="--", label="0.5 (결정 임계값)")
    ax.axvline(0, color="#999", lw=0.8, ls="--")
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlabel("z = w·x + b (선형식의 출력)"); ax.set_ylabel("σ(z) = 확률")
    ax.set_title("시그모이드 — 직선(-무한~+무한)을 확률(0~1)로 압축")
    ax.legend(fontsize=8); fig.tight_layout()
    fig.savefig(CHARTS / "ch02_sigmoid.png", dpi=110); plt.close(fig)
    print("[chart] ch02_sigmoid.png 저장")


# ── §03: 결정경계 — '회귀'인데 분류기인 이유 ──────────────────────────────
def s03_decision_boundary():
    """로지스틱 회귀는 확률(연속값)을 '회귀'하지만, σ(z)=0.5 즉 z=0 인 선을 경계로
    클래스를 가른다. 그래서 출력은 회귀, 쓰임은 분류. 2특성 평면에서 경계를 그린다."""
    bc = load_breast_cancer()
    # 시각화를 위해 특성 2개만 사용
    feat = [0, 27]   # mean radius, worst concave points
    X = bc.data[:, feat]; y = bc.target
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3,
                                          random_state=SEED, stratify=y)
    model = make_pipeline(StandardScaler(), LogisticRegression())
    model.fit(Xtr, ytr)
    acc = accuracy_score(yte, model.predict(Xte))
    print(f"2특성 로지스틱 회귀 — test 정확도: {acc:.4f}")
    print(f"사용 특성: {[bc.feature_names[i] for i in feat]}")

    # 표준화된 공간에서 학습한 계수로 경계식 확인
    clf = model.steps[-1][1]
    w = clf.coef_[0]; b = clf.intercept_[0]
    print(f"학습된 선형식(표준화 공간): z = {w[0]:.3f}·x1 + {w[1]:.3f}·x2 + {b:.3f}")
    print(f"결정경계는 z=0 인 직선 (σ(z)=0.5). z>0 이면 클래스1, z<0 이면 클래스0.")

    # 등고선으로 경계 그리기
    xmin, xmax = X[:, 0].min() - 1, X[:, 0].max() + 1
    ymin, ymax = X[:, 1].min() - 0.01, X[:, 1].max() + 0.01
    xx, yy = np.meshgrid(np.linspace(xmin, xmax, 300),
                         np.linspace(ymin, ymax, 300))
    grid = np.c_[xx.ravel(), yy.ravel()]
    prob = model.predict_proba(grid)[:, 1].reshape(xx.shape)
    fig, ax = plt.subplots(figsize=(6.2, 4.4))
    cs = ax.contourf(xx, yy, prob, levels=20, cmap="RdYlGn", alpha=0.55)
    ax.contour(xx, yy, prob, levels=[0.5], colors="#1f2933", linewidths=2.0)
    ax.scatter(X[y == 0, 0], X[y == 0, 1], s=12, color="#b03a2e",
               edgecolor="none", alpha=0.7, label="악성(0)")
    ax.scatter(X[y == 1, 0], X[y == 1, 1], s=12, color="#196f3d",
               edgecolor="none", alpha=0.7, label="양성(1)")
    fig.colorbar(cs, ax=ax, label="P(양성)")
    ax.set_xlabel("mean radius"); ax.set_ylabel("worst concave points")
    ax.set_title(f"결정경계(검은선=확률0.5) — test 정확도 {acc:.3f}")
    ax.legend(loc="upper right", fontsize=8); fig.tight_layout()
    fig.savefig(CHARTS / "ch03_decision_boundary.png", dpi=110); plt.close(fig)
    print("[chart] ch03_decision_boundary.png 저장")


# ── §04: 다중분류 — 시그모이드를 넘어 softmax/OvR 로 3클래스 ───────────────
def s04_multiclass():
    """클래스가 3개 이상이면 로지스틱 회귀는 multinomial(softmax) 로 각 클래스 확률을
    구하고, 그 합은 1 이 된다. iris 3품종으로 확률 분포와 정확도를 확인한다."""
    iris = load_iris()
    X, y = iris.data, iris.target
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2,
                                          random_state=SEED, stratify=y)
    model = make_pipeline(StandardScaler(),
                          LogisticRegression(max_iter=1000))
    model.fit(Xtr, ytr)
    acc = accuracy_score(yte, model.predict(Xte))
    print(f"iris 3클래스 로지스틱 회귀 — test 정확도: {acc:.4f}")
    clf = model.steps[-1][1]
    print(f"계수 shape: {clf.coef_.shape}  (클래스 {clf.coef_.shape[0]}개 × 특성 {clf.coef_.shape[1]}개)")
    print(f"  -> 2분류는 경계 1개, 3분류는 클래스별 점수 3개 중 최댓값으로 결정.\n")
    proba = model.predict_proba(Xte[:4])
    print("test 표본 4개의 클래스별 확률(softmax, 행 합=1):")
    print(f"  {'setosa':>10} {'versicolor':>12} {'virginica':>12}   합")
    for row in proba:
        print(f"  {row[0]:>10.4f} {row[1]:>12.4f} {row[2]:>12.4f}   {row.sum():.3f}")


# ── §05: 분류 평가 — 정확도 한 숫자의 함정(정밀도·재현율·혼동행렬) ─────────
def s05_metrics_trap():
    """정확도 하나로는 '어떤 실수를 하는지' 가 가려진다. 불균형 데이터에서
    혼동행렬·정밀도·재현율이 정확도와 어떻게 달라지는지 의료 시나리오로 확인한다.
    (암 진단: 악성을 놓치는 것 = 재현율 저하가 가장 치명적)"""
    bc = load_breast_cancer()
    X, y = bc.data, bc.target   # 0=악성(malignant), 1=양성(benign)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3,
                                          random_state=SEED, stratify=y)
    model = make_pipeline(StandardScaler(),
                          LogisticRegression(max_iter=5000))
    model.fit(Xtr, ytr)
    pred = model.predict(Xte)

    acc = accuracy_score(yte, pred)
    cm = confusion_matrix(yte, pred)
    print(f"전체 정확도(accuracy): {acc:.4f}   <- 한 숫자로는 깔끔해 보인다")
    print("\n혼동행렬 (행=실제, 열=예측 / 라벨 0=악성 1=양성):")
    print("            예측:악성  예측:양성")
    print(f"  실제:악성   {cm[0,0]:>7d}   {cm[0,1]:>8d}")
    print(f"  실제:양성   {cm[1,0]:>7d}   {cm[1,1]:>8d}")

    # '악성(0)' 을 양성 클래스로 보는 관점 — 놓치면 안 되는 쪽
    prec_mal = precision_score(yte, pred, pos_label=0)
    rec_mal = recall_score(yte, pred, pos_label=0)
    fn = cm[0, 1]  # 악성인데 양성이라 한 것 = 놓친 암
    print(f"\n[악성(0) 기준] 정밀도={prec_mal:.4f}  재현율={rec_mal:.4f}")
    print(f"  놓친 악성(FN, 암인데 정상이라 판정): {fn}건")
    print(f"  -> 정확도 {acc:.3f} 가 높아도, 재현율이 이 'FN' 의 위험을 따로 드러낸다.")

    print("\nclassification_report:")
    print(classification_report(yte, pred,
          target_names=["악성(malignant)", "양성(benign)"], digits=3))

    fig, ax = plt.subplots(figsize=(4.8, 4.2))
    im = ax.imshow(cm, cmap="Blues")
    ax.set_xticks([0, 1]); ax.set_yticks([0, 1])
    ax.set_xticklabels(["악성", "양성"]); ax.set_yticklabels(["악성", "양성"])
    ax.set_xlabel("예측"); ax.set_ylabel("실제")
    ax.set_title("혼동행렬 (breast_cancer)")
    for i in range(2):
        for j in range(2):
            ax.text(j, i, cm[i, j], ha="center", va="center",
                    color="white" if cm[i, j] > cm.max() / 2 else "#1f2933",
                    fontsize=14, fontweight="bold")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(CHARTS / "ch05_confusion_matrix.png", dpi=110); plt.close(fig)
    print("[chart] ch05_confusion_matrix.png 저장")


if __name__ == "__main__":
    run_section("00_task_kind", s00_task_kind)
    run_section("01_linear_on_labels", s01_linear_on_labels)
    run_section("02_sigmoid", s02_sigmoid)
    run_section("03_decision_boundary", s03_decision_boundary)
    run_section("04_multiclass", s04_multiclass)
    run_section("05_metrics_trap", s05_metrics_trap)
    print("\n완료: logs/*.txt, charts/*.png 생성")
