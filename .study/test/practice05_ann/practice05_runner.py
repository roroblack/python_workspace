# practice05_runner.py
# 머신러닝 실습5(과제) — 인공신경망(ANN/MLP)으로 콘크리트 압축강도 예측 + 앙상블 비교
# 실행: c:\_proj\python_workspace\.venv\Scripts\python.exe practice05_runner.py
# 결과: logs/{섹션명}.txt 저장 + 터미널 출력,  charts/*.png 생성
#
# 데이터: c:\_proj\ml_workspace\from_colab\0602-s\concrete_stg.csv (콘크리트 압축강도 회귀, 1030행)
#   ※ 과제 colab 은 PyTorch 로 ANN 을 구현했으나(직접 nn.Module + Adam 루프),
#     이 runner 는 오프라인 재현성(고정 시드)을 위해 sklearn MLPRegressor 로 치환한다.
#     MLP 의 핵심(입력·은닉·출력층, 역전파, 활성함수, 스케일 의존성)은 동일하게 검증된다.

import sys, io, pathlib
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

from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

HERE = pathlib.Path(__file__).parent
LOGS = HERE / "logs"; LOGS.mkdir(exist_ok=True)
CHARTS = HERE / "charts"; CHARTS.mkdir(exist_ok=True)
SEED = 42
CSV = pathlib.Path(r"c:\_proj\ml_workspace\from_colab\0602-s\concrete_stg.csv")

FEATS = ["cement", "slag", "ash", "water", "superplastic", "coarseagg", "fineagg", "age"]
TARGET = "strength"


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


def load_data():
    """concrete_stg.csv 로드. 읽기 실패 시 sklearn 회귀 데이터로 폴백(사유 출력)."""
    if CSV.exists():
        df = pd.read_csv(CSV)
        return df[FEATS].values, df[TARGET].values, "concrete_stg.csv"
    # 폴백: 외부 csv 불가 시 내장 회귀 데이터
    from sklearn.datasets import fetch_california_housing
    print("[경고] concrete_stg.csv 를 찾지 못해 california_housing 으로 폴백")
    d = fetch_california_housing()
    return d.data, d.target, "california_housing(폴백)"


# ── §00: 데이터 진단 — 콘크리트 회귀 문제, 특성 스케일이 제각각 ──────────────
def s00_inspect():
    """과제 데이터 성격을 먼저 진단한다. 8개 배합 성분 + 양생일수로 압축강도(연속 실수)를
    예측하는 회귀 문제. 특성마다 단위·범위가 크게 달라 신경망 입력 전 스케일링이 필요함을 본다."""
    X, y, src = load_data()
    print(f"[데이터] {src}  shape: X={X.shape}, y={y.shape}")
    print(f"[목표 y] strength(압축강도, MPa)  min={y.min():.2f}  max={y.max():.2f}  "
          f"mean={y.mean():.2f}  std={y.std():.2f}  → 연속 실수 = 회귀")
    print("\n[특성별 스케일] 평균 / 표준편차 / 범위 — 단위가 제각각이다")
    print(f"  {'feature':>12} | {'mean':>9} | {'std':>9} | {'min':>7} | {'max':>8}")
    print("  " + "-" * 56)
    for i, name in enumerate(FEATS):
        col = X[:, i]
        print(f"  {name:>12} | {col.mean():9.2f} | {col.std():9.2f} | {col.min():7.1f} | {col.max():8.1f}")
    rng = X.max(axis=0) - X.min(axis=0)
    print(f"\n  특성 범위 폭 최대/최소 비율 ≈ {rng.max()/rng.min():.0f}배 "
          f"({FEATS[rng.argmax()]} vs {FEATS[rng.argmin()]}) → 스케일링 없이는 큰 특성이 학습을 지배")


# ── §01: MLP 베이스라인 — 스케일링 없이 vs StandardScaler 적용 ───────────────
def s01_scaling_effect():
    """동일한 MLPRegressor 를 ① 원본 그대로, ② StandardScaler 파이프라인으로 학습해
    test R2 를 비교한다. 신경망에 표준화가 '선택'이 아니라 '필수'임을 수치로 확인."""
    X, y, _ = load_data()
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=SEED)

    # ① 스케일링 없이
    raw = MLPRegressor(hidden_layer_sizes=(64, 64), activation="relu",
                       max_iter=2000, random_state=SEED)
    raw.fit(Xtr, ytr)
    r2_raw = r2_score(yte, raw.predict(Xte))

    # ② StandardScaler 파이프라인
    scaled = make_pipeline(StandardScaler(),
                           MLPRegressor(hidden_layer_sizes=(64, 64), activation="relu",
                                        max_iter=2000, random_state=SEED))
    scaled.fit(Xtr, ytr)
    r2_scaled = r2_score(yte, scaled.predict(Xte))

    print("동일 MLP(은닉 64-64, relu) — 표준화 유무만 다르게:")
    print(f"  ① 스케일링 없음        test R2 = {r2_raw:8.4f}   수렴 반복수 n_iter={raw.n_iter_}")
    print(f"  ② StandardScaler 적용  test R2 = {r2_scaled:8.4f}")
    print(f"  → 표준화로 R2 가 {r2_scaled - r2_raw:+.4f} 변화. 신경망은 입력 스케일에 민감하다.")

    fig, ax = plt.subplots(figsize=(5.6, 4))
    bars = ax.bar(["스케일링 없음", "StandardScaler"], [r2_raw, r2_scaled],
                  color=["#E8875A", "#52A97E"], width=0.55)
    ax.axhline(0, color="#999", lw=0.8)
    ax.set_ylabel("test R2"); ax.set_title("MLP — 표준화 유무에 따른 test R2")
    for b, v in zip(bars, [r2_raw, r2_scaled]):
        ax.text(b.get_x() + b.get_width() / 2, v + (0.02 if v >= 0 else -0.06),
                f"{v:.3f}", ha="center", fontsize=11)
    fig.tight_layout(); fig.savefig(CHARTS / "ch_scaling.png", dpi=110); plt.close(fig)
    print("[chart] ch_scaling.png 저장")


# ── §02: 은닉층 크기 / 학습률 그리드서치 ─────────────────────────────────────
def s02_grid():
    """과제의 그리드서치(노드·층·학습률)를 sklearn GridSearchCV(5-fold)로 재현한다.
    은닉층 크기와 learning_rate_init 가 성능에 미치는 영향을 보고 best 조합을 자동 선택."""
    X, y, _ = load_data()
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=SEED)

    pipe = make_pipeline(StandardScaler(),
                         MLPRegressor(activation="relu", max_iter=3000,
                                      early_stopping=False, random_state=SEED))
    grid = {
        "mlpregressor__hidden_layer_sizes": [(20,), (50,), (50, 50), (64, 64), (100, 100)],
        "mlpregressor__learning_rate_init": [0.001, 0.01],
    }
    gs = GridSearchCV(pipe, grid, scoring="r2", cv=5, n_jobs=-1)
    gs.fit(Xtr, ytr)

    res = pd.DataFrame(gs.cv_results_)
    res = res.sort_values("rank_test_score")
    print(f"그리드: 은닉층 5종 x 학습률 2종 = {len(res)}개 조합, 5-fold CV (scoring=R2)")
    print(f"{'hidden':>12} | {'lr':>6} | {'CV R2(mean)':>11} | {'CV std':>7}")
    print("-" * 46)
    for _, r in res.iterrows():
        h = r["param_mlpregressor__hidden_layer_sizes"]
        lr = r["param_mlpregressor__learning_rate_init"]
        print(f"{str(h):>12} | {lr:>6} | {r['mean_test_score']:11.4f} | {r['std_test_score']:7.4f}")

    best = gs.best_params_
    best_h = best["mlpregressor__hidden_layer_sizes"]
    best_lr = best["mlpregressor__learning_rate_init"]
    test_r2 = r2_score(yte, gs.predict(Xte))
    print(f"\n[best] hidden={best_h}, lr={best_lr}  → CV R2={gs.best_score_:.4f}, "
          f"holdout test R2={test_r2:.4f}")

    # 은닉 구조별 best(학습률 무관 최고) test R2 막대
    sizes = [(20,), (50,), (50, 50), (64, 64), (100, 100)]
    labels = ["20", "50", "50-50", "64-64", "100-100"]
    bar_r2 = []
    for h in sizes:
        sub = res[res["param_mlpregressor__hidden_layer_sizes"] == h]
        bar_r2.append(sub["mean_test_score"].max())
    fig, ax = plt.subplots(figsize=(6.2, 4))
    ax.bar(labels, bar_r2, color="#5B9BD5", width=0.6)
    ax.set_ylabel("CV R2 (best lr)"); ax.set_xlabel("은닉층 구조")
    ax.set_title("은닉층 크기 vs CV R2")
    ax.set_ylim(min(bar_r2) - 0.05, 1.0)
    for i, v in enumerate(bar_r2):
        ax.text(i, v + 0.005, f"{v:.3f}", ha="center", fontsize=10)
    fig.tight_layout(); fig.savefig(CHARTS / "ch_hidden.png", dpi=110); plt.close(fig)
    print("[chart] ch_hidden.png 저장")


# ── §03: best MLP 예측값 vs 실제값 (잔차 진단) ───────────────────────────────
def s03_pred_actual():
    """best 구조 MLP 의 예측을 실제값과 산점도로 비교한다. y=x 선에 점이 붙을수록 정확.
    과제 보고서가 지적한 '극단 강도 구간의 예측 정확도 저하'를 직접 확인한다."""
    X, y, _ = load_data()
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=SEED)
    model = make_pipeline(StandardScaler(),
                          MLPRegressor(hidden_layer_sizes=(64, 64), activation="relu",
                                       learning_rate_init=0.01, max_iter=3000, random_state=SEED))
    model.fit(Xtr, ytr)
    pred = model.predict(Xte)
    r2 = r2_score(yte, pred)
    corr = float(np.corrcoef(yte, pred)[0, 1])
    print(f"best MLP(64-64, relu, lr=0.01) holdout test:")
    print(f"  R2   = {r2:.4f}")
    print(f"  상관계수(corr) = {corr:.4f}")
    print(f"  MSE  = {mean_squared_error(yte, pred):.3f}   (원단위 MPa^2)")
    print(f"  MAE  = {mean_absolute_error(yte, pred):.3f}  MPa")
    # 극단 구간 오차
    lo_mask = yte < np.percentile(yte, 10)
    hi_mask = yte > np.percentile(yte, 90)
    mid_mask = ~(lo_mask | hi_mask)
    mae_ext = mean_absolute_error(np.r_[yte[lo_mask], yte[hi_mask]],
                                  np.r_[pred[lo_mask], pred[hi_mask]])
    mae_mid = mean_absolute_error(yte[mid_mask], pred[mid_mask])
    print(f"  MAE(중간 강도 구간) = {mae_mid:.2f}  vs  MAE(상·하위 10% 극단) = {mae_ext:.2f} MPa")
    print("  → 극단 강도(아주 약하거나 강한)에서 오차가 더 크다(평균 회귀 경향)")

    fig, ax = plt.subplots(figsize=(5.6, 5.4))
    ax.scatter(yte, pred, s=18, alpha=0.5, color="#5B9BD5", label="예측 결과")
    lo, hi = float(min(yte.min(), pred.min())), float(max(yte.max(), pred.max()))
    ax.plot([lo, hi], [lo, hi], "--", color="#E8875A", lw=2, label="완벽예측 y=x")
    ax.set_xlabel("실제 강도 (MPa)"); ax.set_ylabel("예측 강도 (MPa)")
    ax.set_title(f"MLP 실제값 vs 예측값 (R2={r2:.3f})")
    ax.legend(); fig.tight_layout()
    fig.savefig(CHARTS / "ch_pred_actual.png", dpi=110); plt.close(fig)
    print("[chart] ch_pred_actual.png 저장")


# ── §04: 같은 데이터를 RandomForest / GradientBoosting 과 비교 ───────────────
def s04_compare():
    """같은 train/test 분할에서 MLP vs RandomForest vs GradientBoosting 의 test R2/MAE 를 나란히
    비교한다. 트리 앙상블은 스케일링 없이도 강하다 — 신경망이 빛나는 지점과 비용을 가른다."""
    X, y, _ = load_data()
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=SEED)

    models = {
        "MLP(64-64,scaled)": make_pipeline(
            StandardScaler(),
            MLPRegressor(hidden_layer_sizes=(64, 64), activation="relu",
                         learning_rate_init=0.01, max_iter=3000, random_state=SEED)),
        "RandomForest": RandomForestRegressor(n_estimators=300, random_state=SEED, n_jobs=-1),
        "GradientBoosting": GradientBoostingRegressor(n_estimators=300, random_state=SEED),
    }
    import time
    rows = []
    print(f"{'model':>20} | {'test R2':>8} | {'MAE(MPa)':>9} | {'fit(s)':>7}")
    print("-" * 54)
    for name, m in models.items():
        t0 = time.time()
        m.fit(Xtr, ytr)
        dt = time.time() - t0
        pred = m.predict(Xte)
        r2 = r2_score(yte, pred); mae = mean_absolute_error(yte, pred)
        rows.append((name, r2, mae, dt))
        print(f"{name:>20} | {r2:8.4f} | {mae:9.3f} | {dt:7.2f}")

    print("\n→ 트리 앙상블(RF/GBM)은 스케일링 없이 바로 높은 R2. MLP 는 표준화·튜닝을 거쳐야 경쟁권.")

    fig, ax = plt.subplots(figsize=(6.4, 4))
    names = [r[0] for r in rows]; r2s = [r[1] for r in rows]
    bars = ax.bar(names, r2s, color=["#52A97E", "#5B9BD5", "#9178C4"], width=0.6)
    ax.set_ylabel("test R2"); ax.set_title("MLP vs RandomForest vs GradientBoosting")
    ax.set_ylim(0, 1.0)
    for b, v in zip(bars, r2s):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.01, f"{v:.3f}", ha="center", fontsize=11)
    plt.setp(ax.get_xticklabels(), rotation=12, ha="right")
    fig.tight_layout(); fig.savefig(CHARTS / "ch_compare.png", dpi=110); plt.close(fig)
    print("[chart] ch_compare.png 저장")


if __name__ == "__main__":
    run_section("00_inspect", s00_inspect)
    run_section("01_scaling_effect", s01_scaling_effect)
    run_section("02_grid", s02_grid)
    run_section("03_pred_actual", s03_pred_actual)
    run_section("04_compare", s04_compare)
    print("\n완료: logs/*.txt, charts/*.png 생성")
