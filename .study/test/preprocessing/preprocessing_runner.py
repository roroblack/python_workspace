# preprocessing_runner.py
# 데이터 전처리 Day(0521) — numpy dtype 추론 · pandas 결측값 처리 · 변수 변환 섹션별 실행기
# 실행: c:\_proj\python_workspace\.venv\Scripts\python.exe preprocessing_runner.py
# 결과: logs/{섹션명}.txt 저장 + 터미널 출력, charts/*.png 생성
# 소재: test_numpy/numpy_test7~8.py(dtype·NaN·U{n} 잘림), test_pandas/pandas_test5.py(NaN·cut),
#       seaborn titanic(결측값 실데이터). 고정 시드(42)로 재현 가능.

import sys, io, pathlib
from contextlib import redirect_stdout

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# 차트 한글 렌더링 (Windows 기본 한글 폰트) — 폰트 경고 방지
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

import seaborn as sns

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

# ── §00: ndarray 는 왜 한 타입만 담나 — dtype 자동 추론 ────────────────────
def s00_dtype_infer():
    """np.array() 에 dtype 을 안 주면 NumPy 가 자동으로 하나의 dtype 을 정한다.
    정수만이면 int64, 실수가 하나라도 섞이면 float64 로 업캐스팅된다(test_numpy/numpy_test7.py)."""
    x1 = np.array([1, 2, 3])
    x2 = np.array([1.0, 2.0, 3.0])
    x3 = np.array([1, 2, 3.0])              # 정수 + 실수 혼합
    x4 = np.array([1, 2, '3'])              # 숫자 + 문자열 혼합
    print(f"np.array([1, 2, 3])      → dtype={x1.dtype}   (정수만 → 정수)")
    print(f"np.array([1.0,2.0,3.0])  → dtype={x2.dtype} (실수만 → 실수)")
    print(f"np.array([1, 2, 3.0])    → dtype={x3.dtype}  값={x3}  (실수 하나 → 업캐스팅)")
    print(f"np.array([1, 2, '3'])    → dtype={x4.dtype}     값={x4}  (문자 섞이면 전부 문자)")
    print()
    # 한 배열은 한 dtype: 원소 하나를 바꿔도 dtype 이 따라 바뀌지 않는다
    x1[0] = 9.7
    print(f"int64 배열에 9.7 대입 후: {x1}  (소수점이 잘려 9 로 저장 — dtype 불변)")

# ── §01: dtype 을 명시하면 — U{n} 유니코드 잘림 함정 ──────────────────────
def s01_unicode_trunc():
    """dtype='U{n}' 은 '유니코드 n글자' 칸을 만든다. 한글도 1글자=1칸이라
    칸보다 긴 문자열은 조용히 잘린다(test_numpy/numpy_test8.py 의 U4 사례 확장)."""
    u3 = np.array(['서울', '부산경남'], dtype='U3')   # '부산경남'은 4글자
    u4 = np.array(['서울', '부산경남'], dtype='U4')
    print(f"dtype='U3' : {u3}   ← '부산경남'(4글자) 네 번째 글자 '남' 잘림")
    print(f"dtype='U4' : {u4}   ← 4칸 → 온전히 저장")
    print()
    # dtype 을 안 주면 가장 긴 문자열에 맞춰 자동 결정된다
    auto = np.array(['서울', '부산경남'])
    print(f"dtype 미지정 → {auto.dtype}  {auto}  (가장 긴 '부산경남' 4글자에 맞춰 <U4)")
    print()
    # 잘림은 에러가 아니라 '조용한 데이터 손실' — 칸이 작으면 대입도 잘린다
    box = np.zeros(2, dtype='U2')
    box[0] = '대한민국'
    print(f"U2 칸에 '대한민국' 대입 → {box[0]!r}  (앞 2글자만, 에러 없음 → 위험)")

# ── §02: 표 데이터의 '값이 없음' — NaN 탐지(isna/sum) ─────────────────────
def s02_nan_detect():
    """pandas 표에서 '값이 없음'은 NaN 으로 표시된다. NaN==NaN 은 False 라
    == 비교로는 못 찾고 isna()/isnull() 로 탐지한다(test_pandas/pandas_test5.py)."""
    print(f"np.nan == np.nan : {np.nan == np.nan}   (자기 자신과도 다름 → == 로 못 찾음)")
    print()
    titanic = sns.load_dataset('titanic')
    na_count = titanic.isna().sum()
    print("titanic 열별 결측값 개수 (isna().sum()):")
    print(na_count[na_count > 0].to_string())
    print()
    total = len(titanic)
    age_na = titanic['age'].isna().sum()
    print(f"전체 행 수: {total}")
    print(f"age 결측: {age_na}개 ({age_na/total*100:.1f}%)  ← 거의 1/5 가 비어 있음")

# ── §03: dropna vs fillna — 통계가 어떻게 흔들리나 ────────────────────────
def s03_impute_compare():
    """결측을 다루는 두 길: dropna(행 삭제) vs fillna(채우기). titanic age 로
    평균/표준편차/중앙값이 전략마다 어떻게 달라지는지 실수치로 비교한다."""
    titanic = sns.load_dataset('titanic')
    age = titanic['age']
    mean_v, med_v = age.mean(), age.median()

    age_drop  = age.dropna()
    age_mean  = age.fillna(mean_v)
    age_med   = age.fillna(med_v)
    age_zero  = age.fillna(0)

    def stat(label, s):
        print(f"{label:16s} count={s.count():4d}  mean={s.mean():7.4f}  "
              f"std={s.std():7.4f}  median={s.median():5.1f}")

    print(f"원본 mean={mean_v:.4f}, median={med_v:.1f}\n")
    stat("원본(NaN포함)", age)
    stat("dropna()",     age_drop)
    stat("fillna(mean)", age_mean)
    stat("fillna(median)", age_med)
    stat("fillna(0)",    age_zero)
    print()
    # 핵심 관찰: 평균 대치는 평균은 그대로 두지만 표준편차(분산)를 줄인다
    print(f"fillna(mean) 의 평균: {age_mean.mean():.4f}  (원본 평균과 동일 — 평균은 안 흔듦)")
    print(f"표준편차 변화: 원본 {age.std():.4f} → mean대치 {age_mean.std():.4f}  "
          f"({(age_mean.std()-age.std())/age.std()*100:+.1f}%)")
    print(f"  → 같은 값(평균)을 {age.isna().sum()}번 꽂으니 흩어짐이 줄어 분산이 작아진다.")

    # 차트: 대치 전/후 분포 비교
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.4), sharey=True)
    bins = np.linspace(0, 80, 33)
    axes[0].hist(age.dropna(), bins=bins, color="#5B9BD5", alpha=0.85)
    axes[0].set_title("원본 (NaN 제외)")
    axes[1].hist(age_mean, bins=bins, color="#E8875A", alpha=0.85)
    axes[1].set_title(f"fillna(mean={mean_v:.1f})")
    axes[2].hist(age_med, bins=bins, color="#52A97E", alpha=0.85)
    axes[2].set_title(f"fillna(median={med_v:.0f})")
    for ax in axes:
        ax.set_xlabel("나이"); ax.axvline(mean_v, color="#9178C4", lw=1, ls="--")
    axes[0].set_ylabel("빈도")
    fig.suptitle("결측 대치 전/후 분포 — 평균 자리에 막대가 솟는다", y=1.02)
    fig.tight_layout()
    fig.savefig(CHARTS / "ch_impute.png", dpi=110, bbox_inches="tight"); plt.close(fig)
    print("[chart] ch_impute.png 저장")

# ── §04: 변수 타입 변환 — astype ─────────────────────────────────────────
def s04_astype():
    """astype 은 열의 dtype 을 바꾼다. float→int 는 소수점을 버리고(반올림 아님),
    숫자→문자, 문자→숫자(pd.to_numeric) 변환의 차이를 확인한다."""
    titanic = sns.load_dataset('titanic')
    fare = titanic['fare']
    print(f"fare dtype 원본 : {fare.dtype}")
    fare_int = fare.astype('int64')
    print(f"fare dtype 변환 : {fare_int.dtype}  (소수점 '버림' — 반올림 아님)")
    print(f"원본 앞 5개 : {[round(v,4) for v in fare[:5]]}")
    print(f"int  앞 5개 : {list(fare_int[:5])}")
    print()
    # category 변환 — 메모리 절약
    sex = titanic['sex']
    mem_obj = sex.memory_usage(deep=True)
    mem_cat = sex.astype('category').memory_usage(deep=True)
    print(f"sex object  메모리: {mem_obj:>7,} bytes")
    print(f"sex category 메모리: {mem_cat:>7,} bytes  ({(1-mem_cat/mem_obj)*100:.1f}% 절약)")

# ── §05: 분포 변환 — log 변환과 구간화(cut) ──────────────────────────────
def s05_transform():
    """치우친(오른쪽 꼬리) 분포는 log 변환으로 대칭에 가깝게 만든다.
    연속값을 cut 으로 구간(범주)으로 묶으면 해석이 쉬워진다."""
    titanic = sns.load_dataset('titanic')
    fare = titanic['fare']
    fare_log = np.log1p(fare)                 # log(1+x): fare=0 안전
    print(f"fare 왜도(skew) 변환 전 : {fare.skew():.4f}  (오른쪽으로 크게 치우침)")
    print(f"fare 왜도(skew) 변환 후 : {fare_log.skew():.4f}  (log1p 후 대칭에 근접)")
    print()
    # cut: 나이 구간화
    age = titanic['age'].dropna()
    labels = ['어린이(0-15)', '청소년(16-25)', '청년(26-35)', '중년(36-55)', '노년(56+)']
    age_cut = pd.cut(age, bins=[0, 15, 25, 35, 55, age.max() + 1], labels=labels)
    print("pd.cut 나이 5구간 value_counts():")
    for label, cnt in age_cut.value_counts().sort_index().items():
        print(f"  {str(label):14s} : {cnt:3d}명")

    # 차트: log 변환 전/후 분포
    fig, axes = plt.subplots(1, 2, figsize=(8, 3.4))
    axes[0].hist(fare, bins=40, color="#E8875A", alpha=0.85)
    axes[0].set_title(f"변환 전 fare (왜도 {fare.skew():.2f})")
    axes[0].set_xlabel("fare")
    axes[1].hist(fare_log, bins=40, color="#52A97E", alpha=0.85)
    axes[1].set_title(f"log1p(fare) 후 (왜도 {fare_log.skew():.2f})")
    axes[1].set_xlabel("log(1+fare)")
    axes[0].set_ylabel("빈도")
    fig.suptitle("변수 변환 전/후 — 치우친 꼬리가 펴진다", y=1.02)
    fig.tight_layout()
    fig.savefig(CHARTS / "ch_logtransform.png", dpi=110, bbox_inches="tight"); plt.close(fig)
    print("[chart] ch_logtransform.png 저장")

if __name__ == "__main__":
    run_section("00_dtype_infer", s00_dtype_infer)
    run_section("01_unicode_trunc", s01_unicode_trunc)
    run_section("02_nan_detect", s02_nan_detect)
    run_section("03_impute_compare", s03_impute_compare)
    run_section("04_astype", s04_astype)
    run_section("05_transform", s05_transform)
    print("\n완료: logs/*.txt, charts/*.png 생성")
