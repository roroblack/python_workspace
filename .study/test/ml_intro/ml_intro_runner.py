# ml_intro_runner.py
# 머신러닝 Day1 (0527) — 학습 프로세스 · 회귀 · 데이터 관리 섹션별 테스트 실행기
# 실행: c:\_proj\python_workspace\.venv\Scripts\python.exe ml_intro_runner.py
# 결과: logs/{섹션명}.txt 저장 + 터미널 출력,  charts/*.png 생성
# 데이터: sklearn 내장 diabetes(회귀)·iris(분류) — 외부 파일 의존 없이 재현 가능(고정 시드)
#   ※ 기존 샘플 없음: ../ml_workspace/from_colab/0527 코드는 iris 분류(RandomForest)라
#     회귀 데모는 내장 diabetes 로 새로 작성(§16-C 우선순위 2, 사유 명시).

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

from sklearn.datasets import load_diabetes, load_iris
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

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

# ── §00: 머신러닝 학습 프로세스 · 회귀 vs 분류 판별 ───────────────────────
def s00_workflow_taxonomy():
    """ML_sample.ipynb(0527) 의 흐름 '데이터 준비→탐색→전처리→학습→평가→예측→저장'을
    내장 데이터로 확인하고, 정답(y)의 형태로 회귀/분류를 판별한다."""
    diabetes = load_diabetes()
    iris = load_iris()
    print("[데이터 준비] diabetes(회귀용)  X shape:", diabetes.data.shape)
    print("[데이터 준비] iris(분류용)      X shape:", iris.data.shape)

    # 정답 y 의 형태로 문제 종류 판별
    def kind(y):
        uniq = np.unique(y)
        # 정답이 소수의 정수 라벨이면 분류, 연속 실수면 회귀
        is_classification = (len(uniq) <= 20) and np.all(uniq == uniq.astype(int))
        return "분류(Classification)" if is_classification else "회귀(Regression)"

    print(f"\ndiabetes y 예시 5개: {np.round(diabetes.target[:5], 1)}  → {kind(diabetes.target)}")
    print(f"iris     y 예시 5개: {iris.target[:5]}             → {kind(iris.target)}")
    print(f"iris 정답 라벨 종류: {np.unique(iris.target)} = {list(iris.target_names)}")

# ── §01: 회귀의 출발 — 세 점을 모두 지나는 직선은 없다 ────────────────────
def s01_three_points():
    """일직선이 아닌 세 점에 직선을 맞출 때, 모든 점을 지날 수는 없고
    '오차 제곱합(SSE)'을 최소화하는 직선이 최선임을 수치로 확인한다."""
    X = np.array([[1.0], [2.0], [3.0]])
    y = np.array([1.0, 3.0, 2.0])           # 일직선이 아님(꺾임)
    lr = LinearRegression().fit(X, y)
    pred = lr.predict(X)
    resid = y - pred
    print(f"세 점: {[ (float(a), float(b)) for a,b in zip(X.ravel(), y) ]}")
    print(f"최소제곱 직선: y = {lr.coef_[0]:.4f} x + {lr.intercept_:.4f}")
    print(f"각 점 예측값 : {np.round(pred,4)}")
    print(f"잔차(실제-예측): {np.round(resid,4)}  (모두 0이 될 수 없음 → 직선이 세 점을 다 지나지 못함)")
    print(f"오차 제곱합 SSE: {np.sum(resid**2):.4f}")

    # 직선을 일부러 다르게 그어보면 SSE 가 더 커진다 → fit 직선이 최소
    worse = (2.0 * X.ravel() + 0.0)
    print(f"임의 직선 y=2x 의 SSE: {np.sum((y-worse)**2):.4f}  (> 최소제곱 SSE)")

# ── §02: LinearRegression.fit 이 정하는 것(계수·절편) ─────────────────────
def s02_fit_coef():
    """diabetes 전체로 LinearRegression.fit → 모델이 '정한 것'은 각 특성의 계수와 절편.
    이 값들이 곧 예측식 y = w·x + b 를 만든다."""
    d = load_diabetes()
    X, y = d.data, d.target
    lr = LinearRegression().fit(X, y)
    print(f"특성 개수: {X.shape[1]}  → 계수도 {len(lr.coef_)}개")
    for name, w in zip(d.feature_names, lr.coef_):
        print(f"  계수[{name:>4}] = {w:10.3f}")
    print(f"절편(intercept) = {lr.intercept_:.3f}")
    print(f"전체 데이터 R2 = {lr.score(X, y):.4f}  (이것만 보면 '잘 맞춘 것'처럼 보인다)")

    # 회귀 산점도 + 직선 (bmi 특성 1개로 시각화)
    bmi = X[:, 2:3]
    lr1 = LinearRegression().fit(bmi, y)
    xs = np.linspace(bmi.min(), bmi.max(), 100).reshape(-1, 1)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(bmi, y, s=14, alpha=0.5, color="#5B9BD5", label="실제 데이터")
    ax.plot(xs, lr1.predict(xs), color="#E8875A", lw=2.5, label="최소제곱 직선")
    ax.set_xlabel("bmi (표준화된 값)"); ax.set_ylabel("질병 진행도 y")
    ax.set_title(f"회귀 직선 (R2={lr1.score(bmi,y):.3f})")
    ax.legend(); fig.tight_layout()
    fig.savefig(CHARTS / "ch02_regression_line.png", dpi=110); plt.close(fig)
    print("[chart] ch02_regression_line.png 저장")

# ── §03: 데이터 관리 ① 표준화(StandardScaler) ────────────────────────────
def s03_standardize():
    """StandardScaler 는 각 특성을 평균0·표준편차1 로 바꾼다(z = (x-μ)/σ).
    스케일이 제각각인 특성을 같은 자에 올려 규제·거리 기반 모델이 공정해진다."""
    d = load_diabetes()
    # 일부러 스케일이 다른 특성 2개를 만들어 비교
    rng = np.random.RandomState(SEED)
    raw = np.column_stack([d.data[:, 2] * 1000, d.data[:, 8] * 0.001])  # bmi(크게), s5(작게)
    print("표준화 전 — 평균/표준편차:")
    print(f"  특성A: mean={raw[:,0].mean():10.4f}  std={raw[:,0].std():10.4f}")
    print(f"  특성B: mean={raw[:,1].mean():10.6f}  std={raw[:,1].std():10.6f}")
    scaled = StandardScaler().fit_transform(raw)
    print("표준화 후 — 평균/표준편차(≈0, ≈1):")
    print(f"  특성A: mean={scaled[:,0].mean():+.2e}  std={scaled[:,0].std():.4f}")
    print(f"  특성B: mean={scaled[:,1].mean():+.2e}  std={scaled[:,1].std():.4f}")

    fig, axes = plt.subplots(1, 2, figsize=(8, 3.4))
    axes[0].hist(raw[:,0], bins=30, color="#5B9BD5", alpha=0.8)
    axes[0].set_title("표준화 전 (특성 A 스케일 큼)")
    axes[1].hist(scaled[:,0], bins=30, color="#52A97E", alpha=0.8)
    axes[1].set_title("표준화 후 (평균0·표준편차1)")
    for ax in axes: ax.set_ylabel("빈도")
    fig.tight_layout(); fig.savefig(CHARTS / "ch03_standardize.png", dpi=110); plt.close(fig)
    print("[chart] ch03_standardize.png 저장")

# ── §04: 데이터 관리 ② train_test_split ──────────────────────────────────
def s04_split():
    """전부로 학습하면 '외운' 성능만 본다. train_test_split 으로 시험용 데이터를
    떼어내야 '처음 보는 데이터'에 대한 진짜 성능(test R2)을 알 수 있다."""
    d = load_diabetes()
    X, y = d.data, d.target
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=SEED)
    lr = LinearRegression().fit(Xtr, ytr)
    print(f"train 크기: {Xtr.shape[0]}개,  test 크기: {Xte.shape[0]}개")
    print(f"train R2 = {lr.score(Xtr, ytr):.4f}")
    print(f"test  R2 = {lr.score(Xte, yte):.4f}   ← 처음 보는 데이터에 대한 진짜 성능")
    print(f"두 값의 차이(과대적합 신호): {lr.score(Xtr,ytr)-lr.score(Xte,yte):+.4f}")

# ── §05: 과대적합 신호 — 차수를 올리면 train↑ test↓ ──────────────────────
def s05_overfit():
    """다항 특성 차수를 올리면 train R2 는 1.0 에 가깝게 오르지만 test R2 는 무너진다.
    '왜 점수가 더 낮아졌어?' 의 정체 = 모델이 train 을 외워버린 과대적합."""
    d = load_diabetes()
    # bmi, bp 두 특성만 사용(차수 효과를 또렷하게)
    X = d.data[:, [2, 3]]; y = d.target
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=SEED)
    degs = [1, 2, 3, 5, 7, 9]
    tr_scores, te_scores = [], []
    print(f"{'차수':>4} | {'train R2':>9} | {'test R2':>9}")
    print("-" * 30)
    for deg in degs:
        model = make_pipeline(PolynomialFeatures(deg), StandardScaler(), LinearRegression())
        model.fit(Xtr, ytr)
        tr, te = model.score(Xtr, ytr), model.score(Xte, yte)
        tr_scores.append(tr); te_scores.append(te)
        flag = "  ← test 무너짐" if te < 0 else ""
        print(f"{deg:>4} | {tr:9.4f} | {te:9.4f}{flag}")

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(degs, tr_scores, "o-", color="#5B9BD5", label="train R2")
    ax.plot(degs, te_scores, "s-", color="#E8875A", label="test R2")
    ax.axhline(0, color="#999", lw=0.8, ls="--")
    ax.set_xlabel("다항 특성 차수(degree)"); ax.set_ylabel("R2")
    ax.set_title("차수↑ → train↑ / test↓ (과대적합)")
    ax.legend(); ax.set_ylim(-1.5, 1.1); fig.tight_layout()
    fig.savefig(CHARTS / "ch05_overfit.png", dpi=110); plt.close(fig)
    print("[chart] ch05_overfit.png 저장")

# ── §06: 규제(Ridge) — 계수를 줄여 test 성능을 되살린다 ───────────────────
def s06_ridge():
    """Ridge 는 손실에 'α·(계수 제곱합)' 벌점을 더해 계수를 작게 눌러 과대적합을 막는다.
    같은 9차 모델에서 α 를 키우면 계수 크기는 줄고 test R2 는 회복된다."""
    d = load_diabetes()
    X = d.data[:, [2, 3]]; y = d.target
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=SEED)
    alphas = [0.0, 0.001, 0.01, 0.1, 1.0, 10.0]
    coef_norms, te_scores = [], []
    print(f"{'alpha':>8} | {'test R2':>9} | {'계수크기(L2norm)':>16}")
    print("-" * 42)
    for a in alphas:
        reg = Ridge(alpha=a) if a > 0 else LinearRegression()
        model = make_pipeline(PolynomialFeatures(9), StandardScaler(), reg)
        model.fit(Xtr, ytr)
        coef = model.steps[-1][1].coef_
        norm = float(np.linalg.norm(coef))
        te = model.score(Xte, yte)
        coef_norms.append(norm); te_scores.append(te)
        print(f"{a:>8} | {te:9.4f} | {norm:16.2f}")

    fig, ax1 = plt.subplots(figsize=(6, 4))
    xs = range(len(alphas))
    ax1.plot(xs, te_scores, "s-", color="#52A97E", label="test R2")
    ax1.set_xticks(list(xs)); ax1.set_xticklabels([str(a) for a in alphas])
    ax1.set_xlabel("Ridge alpha (규제 강도)"); ax1.set_ylabel("test R2", color="#52A97E")
    ax2 = ax1.twinx()
    ax2.plot(xs, coef_norms, "o--", color="#9178C4", label="계수 크기")
    ax2.set_ylabel("계수 L2 norm", color="#9178C4")
    ax1.set_title("alpha↑ → 계수↓ → test R2 회복")
    fig.tight_layout(); fig.savefig(CHARTS / "ch06_ridge.png", dpi=110); plt.close(fig)
    print("[chart] ch06_ridge.png 저장")

# ── §07: 평가지표 — 회귀(R2·MSE·MAE)와 분류(정밀도·재현율) ────────────────
def s07_metrics():
    """회귀는 '얼마나 가깝나'(R2·MSE·MAE), 분류는 '골고루 잘 맞히나'(정밀도·재현율).
    분류 예시는 0527 ML_sample 흐름과 동일한 iris+RandomForest 로 확인한다."""
    # 회귀 지표
    d = load_diabetes()
    Xtr, Xte, ytr, yte = train_test_split(d.data, d.target, test_size=0.2, random_state=SEED)
    lr = LinearRegression().fit(Xtr, ytr)
    p = lr.predict(Xte)
    print("[회귀 지표]")
    print(f"  R2  = {r2_score(yte, p):.4f}  (1에 가까울수록 좋음)")
    print(f"  MSE = {mean_squared_error(yte, p):.2f}")
    print(f"  MAE = {mean_absolute_error(yte, p):.2f}  (평균 절대 오차)")

    # 분류 지표 (iris) — 정밀도/재현율
    iris = load_iris()
    Xtr, Xte, ytr, yte = train_test_split(iris.data, iris.target, test_size=0.2,
                                          random_state=SEED, stratify=iris.target)
    clf = RandomForestClassifier(n_estimators=100, random_state=SEED).fit(Xtr, ytr)
    pred = clf.predict(Xte)
    print("\n[분류 지표] iris + RandomForest")
    print(classification_report(yte, pred, target_names=iris.target_names, digits=3))
    print("혼동행렬(confusion matrix):")
    print(confusion_matrix(yte, pred))

if __name__ == "__main__":
    run_section("00_workflow_taxonomy", s00_workflow_taxonomy)
    run_section("01_three_points", s01_three_points)
    run_section("02_fit_coef", s02_fit_coef)
    run_section("03_standardize", s03_standardize)
    run_section("04_split", s04_split)
    run_section("05_overfit", s05_overfit)
    run_section("06_ridge", s06_ridge)
    run_section("07_metrics", s07_metrics)
    print("\n완료: logs/*.txt, charts/*.png 생성")
