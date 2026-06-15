# subway_reg_runner.py
# 머신러닝 실습1 (0527~0528) — 서울 지하철 이용객 수 예측 회귀 모델 시행착오 재현 실행기
# 실행: c:\_proj\python_workspace\.venv\Scripts\python.exe subway_reg_runner.py
# 결과: logs/{섹션명}.txt 저장 + 터미널 출력,  charts/*.png 생성
# 데이터: ../ml_workspace/from_colab/0528_data/subway/subway_train.csv, subway_test.csv (실측)
#   test.csv 에 정답(num_people)이 있으므로 그것으로 test R2 를 잰다.
#   모든 수치는 실제 실행 결과이며 random_state=42 로 재현 가능하다.

import sys, io, pathlib
from contextlib import redirect_stdout

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# 차트 한글 렌더링 (Windows 기본 한글 폰트)
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

HERE = pathlib.Path(__file__).parent
LOGS = HERE / "logs"; LOGS.mkdir(exist_ok=True)
CHARTS = HERE / "charts"; CHARTS.mkdir(exist_ok=True)
SEED = 42

DATA = pathlib.Path(r"c:\_proj\ml_workspace\from_colab\0528_data\subway")
TRAIN_CSV = DATA / "subway_train.csv"
TEST_CSV = DATA / "subway_test.csv"

# 단계별 R2 를 누적해 마지막에 막대그래프로 그린다.
STAGE_R2 = []   # (라벨, test R2)


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


def rmse(y, p):
    return float(np.sqrt(mean_squared_error(y, p)))


def load_clean():
    """train/test 적재 + 결측치 처리. 원본에는 station_name 결측(nan)과
    수치 결측이 섞여 있어 그대로 넣으면 LinearRegression 이 NaN 에서 멈춘다.
    수치는 train 평균으로, 역 이름은 'unknown' 으로 채운다(누수 방지: train 기준)."""
    tr = pd.read_csv(TRAIN_CSV)
    te = pd.read_csv(TEST_CSV)
    num_raw = ['visibility', 'precipitation', 'temperature']
    means = {c: pd.to_numeric(tr[c], errors='coerce').mean() for c in num_raw}
    for df in (tr, te):
        for c in num_raw:
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(means[c])
        df['station_name'] = df['station_name'].fillna('unknown')
    return tr, te


# ── §00: 데이터 적재 — 무엇을 가지고 무엇을 맞히나 ─────────────────────────
def s00_inspect():
    """subway_train.csv 를 적재해 컬럼·타입·타깃(num_people)의 분포를 확인한다.
    어떤 정보가 주어졌고(날씨·역·요일), 무엇을 예측해야 하는지 먼저 가른다."""
    tr = pd.read_csv(TRAIN_CSV)
    te = pd.read_csv(TEST_CSV)
    print(f"train 크기: {tr.shape}   test 크기: {te.shape}")
    print(f"컬럼: {list(tr.columns)}")
    print("\n[처음 3행]")
    print(tr.head(3).to_string(index=False))
    print("\n[타깃 num_people 분포]")
    y = tr['num_people']
    print(f"  min={y.min():.0f}  max={y.max():.0f}  mean={y.mean():.1f}  std={y.std():.1f}")
    print(f"  역 종류: {tr['station_name'].nunique()}개 → {list(tr['station_name'].unique())}")
    print(f"  요일 종류: {tr['day_of_week'].nunique()}개")
    print(f"  test.csv 에 정답(num_people) 존재? {'num_people' in te.columns}  → test R2 측정 가능")
    print("\n[결측치(NaN) — 깨끗하지 않은 데이터]")
    na = tr.isna().sum()
    for c in tr.columns:
        if na[c] > 0:
            print(f"  {c}: {na[c]}개 결측")
    print("  → station_name 결측(nan)·수치 결측이 섞여 있어 그대로 넣으면 LinearRegression 이 멈춘다.")


# ── §01: 바닥 확인 — 평균 예측 / 단일 약한 특성 ───────────────────────────
def s01_naive():
    """R2 의 '바닥'을 먼저 잰다. ① 무조건 평균만 예측하는 DummyRegressor → R2≈0,
    ② 강수량 한 개만 쓰는 LinearRegression → R2 거의 0. 출발선이 어디인지 못박는다."""
    tr, te = load_clean()
    ytr, yte = tr['num_people'].values, te['num_people'].values

    # ① 무조건 평균만 예측 (R2 의 정의상 바닥 ≈ 0)
    dummy = DummyRegressor(strategy='mean').fit(np.zeros((len(ytr), 1)), ytr)
    pd0 = dummy.predict(np.zeros((len(yte), 1)))
    r2_dummy = r2_score(yte, pd0)
    print(f"[① 평균만 예측 DummyRegressor]  test R2 = {r2_dummy:.4f}   (R2 의 바닥 ≈ 0)")
    print(f"    test RMSE = {rmse(yte, pd0):.1f}명")

    # ② 강수량 한 개만 (약한 단일 특성)
    xtr = tr[['precipitation']].values; xte = te[['precipitation']].values
    lr = LinearRegression().fit(xtr, ytr)
    p = lr.predict(xte)
    r2 = r2_score(yte, p)
    print(f"[② 강수량 1개만 LinearRegression]  test R2 = {r2:.4f}   ← 거의 설명 못 함")
    print(f"    test RMSE = {rmse(yte, p):.1f}명")
    print("→ 아무 정보 없이 평균만 찍으면 R2≈0. 약한 특성 하나로는 거의 못 벗어난다. 여기가 출발선.")
    STAGE_R2.append(("① 평균예측\n(바닥)", r2_dummy))


# ── §02: 날씨 전체 → 범주형(역·요일) One-Hot 추가 ─────────────────────────
def s02_encode():
    """먼저 날씨 4개를 다 넣은 선형모델(② 날씨 전체)을 보고, 그 다음 버렸던
    station_name·day_of_week 를 One-Hot 으로 되살린다(③). 무엇이 점수를 끌어올리나."""
    tr, te = load_clean()
    num_cols = ['visibility', 'precipitation', 'temperature', 'month']
    ytr, yte = tr['num_people'].values, te['num_people'].values

    # ② 날씨/달 전체
    lr0 = LinearRegression().fit(tr[num_cols].values, ytr)
    p0 = lr0.predict(te[num_cols].values)
    r2_0 = r2_score(yte, p0)
    print(f"[② 날씨/달 4개 LinearRegression]  test R2 = {r2_0:.4f}  RMSE={rmse(yte, p0):.1f}명")
    coefs = dict(zip(num_cols, lr0.coef_))
    print(f"    계수: " + ", ".join(f"{k}={v:.1f}" for k, v in coefs.items()))
    print("    → temperature 계수가 압도적. 기온이 이용객 수의 주된 신호였다.")
    STAGE_R2.append(("② 날씨전체\n(선형)", r2_0))

    # ③ + 역·요일 One-Hot
    cat_cols = ['station_name', 'day_of_week']
    ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    Xc_tr = ohe.fit_transform(tr[cat_cols]); Xc_te = ohe.transform(te[cat_cols])
    Xtr = np.hstack([tr[num_cols].values, Xc_tr])
    Xte = np.hstack([te[num_cols].values, Xc_te])
    lr = LinearRegression().fit(Xtr, ytr)
    p = lr.predict(Xte)
    r2 = r2_score(yte, p)
    print(f"\n[③ + 역·요일 One-Hot]  특성 {Xtr.shape[1]}개 (역 {ohe.categories_[0].size} + 요일 {ohe.categories_[1].size} + 숫자 4)")
    print(f"    train R2 = {lr.score(Xtr, ytr):.4f}   test R2 = {r2:.4f}   ← 크게 상승")
    print(f"    test RMSE = {rmse(yte, p):.1f}명")
    print("→ 날씨만으로 0.74, 거기에 '어느 역/무슨 요일'을 더하니 0.85 로 점프했다.")
    STAGE_R2.append(("③ One-Hot\n(역+요일)", r2))


# ── §03: 날짜를 푼다 + 스케일링 — 그런데 왜 더 안 오르나 ───────────────────
def s03_date_scale():
    """date 문자열에서 실제 요일(dayofweek)·일(day)을 뽑아 추가하고 StandardScaler 적용.
    특성을 더 넣었는데도 선형모델의 test R2 는 정체된다 — 선형의 한계를 드러낸다."""
    tr, te = load_clean()

    def add_date(df):
        df = df.copy()
        d = pd.to_datetime(df['date'])
        df['actual_dow'] = d.dt.dayofweek   # date 에서 직접 뽑은 진짜 요일
        df['day'] = d.dt.day
        return df
    tr, te = add_date(tr), add_date(te)

    num_cols = ['visibility', 'precipitation', 'temperature', 'month', 'actual_dow', 'day']
    cat_cols = ['station_name', 'day_of_week']
    ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    Xc_tr = ohe.fit_transform(tr[cat_cols]); Xc_te = ohe.transform(te[cat_cols])

    scaler = StandardScaler()
    Xn_tr = scaler.fit_transform(tr[num_cols])      # train 으로만 fit
    Xn_te = scaler.transform(te[num_cols])          # test 는 transform 만 (누수 방지)
    Xtr = np.hstack([Xn_tr, Xc_tr]); Xte = np.hstack([Xn_te, Xc_te])
    ytr, yte = tr['num_people'].values, te['num_people'].values

    lr = LinearRegression().fit(Xtr, ytr)
    p = lr.predict(Xte)
    r2 = r2_score(yte, p)
    print(f"date 파싱으로 추가한 특성: actual_dow(진짜 요일), day(일)")
    print(f"StandardScaler 는 train 으로만 fit, test 엔 transform 만 (data leakage 방지)")
    print(f"train R2 = {lr.score(Xtr, ytr):.4f}")
    print(f"test  R2 = {r2:.4f}   ← 특성을 더 넣었는데도 거의 그대로")
    print(f"test RMSE = {rmse(yte, p):.1f}명")
    print("→ 선형모델은 '역×요일' 같은 상호작용을 곱으로 표현하지 못한다. 선형의 천장에 닿았다.")
    STAGE_R2.append(("④ 날짜+스케일\n(선형)", r2))


# ── §04: 비선형 모델 — RandomForest 로 갈아탄다 ───────────────────────────
def s04_rf():
    """선형의 한계를 넘기 위해 RandomForestRegressor 로 교체. 트리는 '역과 요일의
    조합'을 분기로 자연히 잡아낸다. 같은 특성으로 모델만 바꿨을 때의 점프를 본다."""
    tr, te = load_clean()

    def add_date(df):
        df = df.copy(); d = pd.to_datetime(df['date'])
        df['actual_dow'] = d.dt.dayofweek; df['day'] = d.dt.day
        return df
    tr, te = add_date(tr), add_date(te)

    le = LabelEncoder()
    tr['stat_idx'] = le.fit_transform(tr['station_name'])
    te['stat_idx'] = te['station_name'].apply(lambda x: le.transform([x])[0] if x in le.classes_ else 0)
    feat = ['visibility', 'precipitation', 'temperature', 'month', 'actual_dow', 'day', 'stat_idx']
    Xtr, ytr = tr[feat].values, tr['num_people'].values
    Xte, yte = te[feat].values, te['num_people'].values

    rf = RandomForestRegressor(n_estimators=300, random_state=SEED, n_jobs=-1).fit(Xtr, ytr)
    p = rf.predict(Xte)
    r2 = r2_score(yte, p)
    print(f"모델: RandomForestRegressor(n_estimators=300)  특성: {feat}")
    print(f"train R2 = {rf.score(Xtr, ytr):.4f}")
    print(f"test  R2 = {r2:.4f}   ← 기대와 달리 선형(0.855)보다 떨어졌다 (?!)")
    print(f"test RMSE = {rmse(yte, p):.1f}명")
    print("\n[특성 중요도]")
    for name, imp in sorted(zip(feat, rf.feature_importances_), key=lambda x: -x[1]):
        print(f"  {name:>14}: {imp:.4f}")
    print(f"train R2 {rf.score(Xtr, ytr):.3f} ≫ test R2 {r2:.3f} — 격차 {rf.score(Xtr,ytr)-r2:+.3f}. 과대적합 신호.")
    print("→ 더 강한 모델로 바꿨는데 점수가 내려갔다. '왜 더 낮아졌나'의 정체를 다음에서 잡는다.")
    STAGE_R2.append(("⑤ RandomForest\n(비선형)", r2))

    # 특성 중요도 차트
    order = np.argsort(rf.feature_importances_)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh([feat[i] for i in order], rf.feature_importances_[order], color="#52A97E")
    ax.set_title("RandomForest 특성 중요도")
    ax.set_xlabel("중요도"); fig.tight_layout()
    fig.savefig(CHARTS / "ch_importance.png", dpi=110); plt.close(fig)
    print("[chart] ch_importance.png 저장")


# ── §05: 타깃 인코딩 + log1p — '역별 요일 평균'을 특성으로 ─────────────────
def s05_target_encoding():
    """결정적 한 수: '이 역의 이 요일 평균 이용객 수'(target encoding)를 특성으로 직접
    넣고, 편차가 큰 타깃에 log1p 를 적용한다. 모델은 잔차만 학습하면 되어 R2 가 급등."""
    tr, te = load_clean()

    def add_date(df):
        df = df.copy(); d = pd.to_datetime(df['date'])
        df['actual_dow'] = d.dt.dayofweek; df['month'] = d.dt.month; df['day'] = d.dt.day
        return df
    tr, te = add_date(tr), add_date(te)

    # train 으로만 그룹 평균(매핑) 학습 — test 에 적용 시 누수 없음
    stat_avg = tr.groupby('station_name')['num_people'].mean().to_dict()
    dow_map = tr.groupby(['station_name', 'actual_dow'])['num_people'].mean().to_dict()
    month_map = tr.groupby(['station_name', 'month'])['num_people'].mean().to_dict()
    g_mean = float(np.mean(list(stat_avg.values())))

    def enc(df):
        df = df.copy()
        df['stat_dow_avg'] = df.apply(
            lambda r: dow_map.get((r['station_name'], r['actual_dow']),
                                  stat_avg.get(r['station_name'], g_mean)), axis=1)
        df['stat_month_avg'] = df.apply(
            lambda r: month_map.get((r['station_name'], r['month']),
                                    stat_avg.get(r['station_name'], g_mean)), axis=1)
        return df
    tr, te = enc(tr), enc(te)

    feat = ['visibility', 'precipitation', 'temperature', 'month', 'actual_dow', 'day',
            'stat_dow_avg', 'stat_month_avg']
    Xtr = tr[feat].values; Xte = te[feat].values
    ytr_raw = tr['num_people'].values; yte = te['num_people'].values
    ytr = np.log1p(ytr_raw)   # 로그 변환: 편차 큰 타깃을 안정화

    rf = RandomForestRegressor(n_estimators=300, max_depth=15,
                               min_samples_leaf=3, random_state=SEED, n_jobs=-1).fit(Xtr, ytr)
    p = np.expm1(rf.predict(Xte))   # 예측 후 역변환
    r2 = r2_score(yte, p)
    print(f"추가 특성: stat_dow_avg(역×요일 평균), stat_month_avg(역×월 평균)  + log1p(타깃)")
    print(f"train R2(log) = {rf.score(Xtr, ytr):.4f}")
    print(f"test  R2 = {r2:.4f}   ← '치트키' 특성을 넣어도 선형(0.855)을 못 넘는다")
    print(f"test RMSE = {rmse(yte, p):.1f}명   MAE = {mean_absolute_error(yte, p):.1f}명")
    print("→ 역별 요일 평균을 직접 넣어줘도, 900행·약한 신호에서는 트리가 여전히 노이즈를 외운다.")
    STAGE_R2.append(("⑥ 타깃인코딩\n+log1p", r2))

    # 예측 vs 실제 산점도
    fig, ax = plt.subplots(figsize=(5.2, 5))
    ax.scatter(yte, p, s=16, alpha=0.5, color="#5B9BD5")
    lim = [min(yte.min(), p.min()), max(yte.max(), p.max())]
    ax.plot(lim, lim, color="#E8875A", lw=1.8, ls="--", label="완벽 예측선")
    ax.set_xlabel("실제 이용객 수"); ax.set_ylabel("예측 이용객 수")
    ax.set_title(f"예측 vs 실제 (test R2={r2:.3f})")
    ax.legend(); fig.tight_layout()
    fig.savefig(CHARTS / "ch_pred_actual.png", dpi=110); plt.close(fig)
    print("[chart] ch_pred_actual.png 저장")


# ── §06: 과대적합을 누른다 — GradientBoosting + 깊이/리프 제한 ─────────────
def s06_guard_overfit():
    """RF 의 train≫test 격차를 줄이기 위해 GradientBoosting 으로 바꾸고 트리 깊이·
    리프 최소표본을 제한한다. train/test 격차(과대적합)를 함께 출력해 일반화를 확인."""
    tr, te = load_clean()

    def add_date(df):
        df = df.copy(); d = pd.to_datetime(df['date'])
        df['actual_dow'] = d.dt.dayofweek; df['month'] = d.dt.month; df['day'] = d.dt.day
        return df
    tr, te = add_date(tr), add_date(te)
    stat_avg = tr.groupby('station_name')['num_people'].mean().to_dict()
    dow_map = tr.groupby(['station_name', 'actual_dow'])['num_people'].mean().to_dict()
    month_map = tr.groupby(['station_name', 'month'])['num_people'].mean().to_dict()
    g_mean = float(np.mean(list(stat_avg.values())))

    def enc(df):
        df = df.copy()
        df['stat_dow_avg'] = df.apply(lambda r: dow_map.get((r['station_name'], r['actual_dow']),
                                      stat_avg.get(r['station_name'], g_mean)), axis=1)
        df['stat_month_avg'] = df.apply(lambda r: month_map.get((r['station_name'], r['month']),
                                        stat_avg.get(r['station_name'], g_mean)), axis=1)
        return df
    tr, te = enc(tr), enc(te)
    feat = ['visibility', 'precipitation', 'temperature', 'month', 'actual_dow', 'day',
            'stat_dow_avg', 'stat_month_avg']
    Xtr, Xte = tr[feat].values, te[feat].values
    ytr = np.log1p(tr['num_people'].values); yte = te['num_people'].values

    print(f"{'모델':<34} | {'train R2':>9} | {'test R2':>9} | {'격차':>7}")
    print("-" * 72)
    # 규제 없는 RF (얕은 비교군)
    rf = RandomForestRegressor(n_estimators=300, random_state=SEED, n_jobs=-1).fit(Xtr, ytr)
    tr_r2 = r2_score(np.expm1(ytr), np.expm1(rf.predict(Xtr)))
    te_r2 = r2_score(yte, np.expm1(rf.predict(Xte)))
    print(f"{'RandomForest(규제 없음)':<28} | {tr_r2:9.4f} | {te_r2:9.4f} | {tr_r2-te_r2:+7.4f}")

    # GradientBoosting (깊이·리프 제한 = 규제)
    gb = GradientBoostingRegressor(n_estimators=500, max_depth=4, learning_rate=0.05,
                                   min_samples_leaf=3, subsample=0.8, random_state=SEED).fit(Xtr, ytr)
    p = np.expm1(gb.predict(Xte))
    gtr = r2_score(np.expm1(ytr), np.expm1(gb.predict(Xtr)))
    gte = r2_score(yte, p)
    print(f"{'GradientBoosting(depth=4,lr=.05)':<28} | {gtr:9.4f} | {gte:9.4f} | {gtr-gte:+7.4f}")
    print(f"\n최종 GradientBoosting test → R2={gte:.4f}  RMSE={rmse(yte,p):.1f}명  MAE={mean_absolute_error(yte,p):.1f}명")
    print("→ 깊이를 제한해도 트리 계열은 이 데이터에서 선형(0.855)을 못 넘었다.")
    print("→ 교훈: 데이터가 작고 신호가 약하면 '더 강한 모델'이 정답이 아니다. 단순+규제가 이긴다.")
    STAGE_R2.append(("⑦ GBM\n(규제)", gte))


# ── §07: 전 단계 R2 정리 막대그래프 ───────────────────────────────────────
def s07_summary():
    """①~⑥ 단계의 test R2 를 한 장에 모아, 무엇을 바꿨을 때 점수가 뛰었는지 보여준다."""
    print("단계별 test R2 누적:")
    for label, r2 in STAGE_R2:
        bar = "#" * max(0, int(r2 * 40)) if r2 > 0 else ""
        print(f"  {label.replace(chr(10),' '):<24} R2={r2:7.4f} {bar}")

    labels = [s[0] for s in STAGE_R2]
    vals = [s[1] for s in STAGE_R2]
    colors = ["#E8875A" if v < 0.3 else "#5B9BD5" if v < 0.7 else "#52A97E" for v in vals]
    fig, ax = plt.subplots(figsize=(8, 4.2))
    bars = ax.bar(range(len(vals)), vals, color=colors)
    ax.set_xticks(range(len(labels))); ax.set_xticklabels(labels, fontsize=8.5)
    ax.set_ylabel("test R2"); ax.set_ylim(0, 1.0)
    best = max(vals)
    ax.axhline(best, color="#9178C4", lw=1, ls="--")
    ax.text(len(vals) - 0.5, best + 0.01, f"최고 {best:.3f}", ha="right", fontsize=8, color="#9178C4")
    ax.set_title("단계별 test R2 — 무엇을 바꿨을 때 점수가 뛰었나")
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, max(v, 0) + 0.015, f"{v:.3f}",
                ha="center", fontsize=8.5)
    fig.tight_layout(); fig.savefig(CHARTS / "ch_r2_stages.png", dpi=110); plt.close(fig)
    print("[chart] ch_r2_stages.png 저장")


if __name__ == "__main__":
    run_section("00_inspect", s00_inspect)
    run_section("01_naive", s01_naive)
    run_section("02_encode", s02_encode)
    run_section("03_date_scale", s03_date_scale)
    run_section("04_rf", s04_rf)
    run_section("05_target_encoding", s05_target_encoding)
    run_section("06_guard_overfit", s06_guard_overfit)
    run_section("07_summary", s07_summary)
    print("\n완료: logs/*.txt, charts/*.png 생성")
