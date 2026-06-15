# path : .study/write/tmp/day0521_runner.py
# 2026-05-28

'''
day0521 블로그 글 실행 검증 runner
- §01 : dtype·NaN·Inf 탐지 (numpy_test7 기반)
- §02 : 벡터화 연산 성능 + hstack/vstack 에러 재현
- §03 : iloc vs loc 비교 (pandas_test2 기반)
- §04 : 결측값 처리 비교 fillna(0) vs fillna(mean)
- §05 : 변수 변환 astype / log / pd.cut 구간화
'''

import os
import sys
import numpy as np
import pandas as pd
import seaborn as sns
import time

LOGS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'test', 'day0521', 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)

def write_log(filename, content):
    path = os.path.join(LOGS_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  → {path} 저장 완료')

# ─────────────────────────────────────────
# §01 : dtype · NaN · Inf
# ─────────────────────────────────────────
def section01():
    print('=' * 60)
    print('§01  dtype · NaN · Inf 탐지')
    print('=' * 60)

    lines = []

    # 기본 dtype 자동 지정
    x1 = np.array([1, 2, 3])
    x2 = np.array([1.0, 2.0, 3.0])
    lines.append(f'int 배열  dtype : {x1.dtype}')
    lines.append(f'float 배열 dtype : {x2.dtype}')

    # 명시적 dtype 지정
    x3 = np.array([1, 2, 3], dtype='f')      # float32
    x4 = np.array(['서울', '부산경남'], dtype='U3')  # 유니코드 3글자 → 잘림
    lines.append(f"dtype='f'  → {x3.dtype}  값={x3}")
    lines.append(f"dtype='U3' → {x4.dtype}  값={x4}  (4글자 '부산경남' → 잘림)")

    # NaN / Inf 발생
    with np.errstate(divide='ignore', invalid='ignore'):
        arr_div = np.array([0, 1, -1, 0]) / np.array([1, 0, 0, 0])
    lines.append(f'0/0, 1/0, -1/0 나누기 결과 : {arr_div}')
    lines.append(f'np.log(0) = {np.log(np.float64(0))}')

    # NaN 전파 규칙
    a = np.array([1.0, np.nan, 3.0])
    lines.append(f'NaN 포함 배열 합 : {a + 10}')     # nan 전파
    lines.append(f'nan == nan : {np.nan == np.nan}') # False
    lines.append(f'np.isnan() 탐지 : {np.isnan(a)}')

    # Inf 탐지
    b = np.array([np.inf, -np.inf, 0.0, 5.0])
    lines.append(f'np.isinf() 탐지 : {np.isinf(b)}')
    lines.append(f'np.isfinite() 탐지 : {np.isfinite(b)}')

    output = '\n'.join(lines)
    print(output)
    write_log('01_dtype_nan.txt', output)

# ─────────────────────────────────────────
# §02 : 벡터화 연산 성능 비교 + vstack 에러 재현
# ─────────────────────────────────────────
def section02():
    print()
    print('=' * 60)
    print('§02  벡터화 연산 성능 비교 + hstack/vstack 에러 재현')
    print('=' * 60)

    lines = []

    # 성능 비교 (1만 개)
    x = np.arange(1, 10001)
    y = np.arange(10001, 20001)

    # 반복문
    z_loop = np.zeros_like(x)
    t0 = time.perf_counter()
    for idx in range(len(x)):
        z_loop[idx] = x[idx] + y[idx]
    t_loop = time.perf_counter() - t0

    # 벡터화
    t0 = time.perf_counter()
    z_vec = x + y
    t_vec = time.perf_counter() - t0

    lines.append(f'반복문   처리시간 : {t_loop*1000:.3f} ms  결과 앞 5개={z_loop[:5]}')
    lines.append(f'벡터화   처리시간 : {t_vec*1000:.4f} ms  결과 앞 5개={z_vec[:5]}')

    # hstack
    ar1 = np.ones((2, 3))
    ar2 = np.zeros((2, 4))
    h = np.hstack((ar1, ar2))
    lines.append(f'hstack (2×3)+(2×4) → shape={h.shape}')

    # vstack 성공
    br1 = np.ones((2, 3))
    br2 = np.zeros((3, 3))
    v = np.vstack([br1, br2])
    lines.append(f'vstack (2×3)+(3×3) → shape={v.shape}')

    # vstack 에러 재현 (열 수 불일치)
    try:
        bad = np.vstack([np.ones((3, 4)), np.ones((3, 5))])
    except ValueError as e:
        lines.append(f'vstack (3×4)+(3×5) → ValueError: {e}')

    # dstack
    cr1 = np.ones((3, 4))
    cr2 = np.zeros((3, 4))
    ds = np.dstack([cr1, cr2])
    lines.append(f'dstack (3×4)+(3×4) → shape={ds.shape}')

    output = '\n'.join(lines)
    print(output)
    write_log('02_vstack_error.txt', output)

# ─────────────────────────────────────────
# §03 : iloc vs loc 비교
# ─────────────────────────────────────────
def section03():
    print()
    print('=' * 60)
    print('§03  iloc vs loc 비교')
    print('=' * 60)

    lines = []

    s = pd.Series(
        [123456784, 5438297, 3425622, 2848820],
        index=['서울', '부산', '인천', '대구']
    )
    s.name = '인구'
    s.index.name = '도시'

    lines.append('--- 기본 Series ---')
    lines.append(str(s))

    # iloc vs loc
    lines.append(f'\ns.iloc[1]      = {s.iloc[1]}  (정수 위치 기반)')
    lines.append(f"s.loc['부산']  = {s.loc['부산']}  (라벨 기반)")
    lines.append(f's.iloc[1] == s.loc["부산"] : {s.iloc[1] == s.loc["부산"]}')

    # 다중 선택
    lines.append('\n--- 다중 선택 ---')
    lines.append(str(s.iloc[[0, 3, 1]]))

    # 조건부 인덱싱
    lines.append('\n--- 조건부 인덱싱 (300만 < 인구 < 500만) ---')
    lines.append(str(s[(300e4 < s) & (s < 500e4)]))

    # 슬라이싱
    lines.append('\n--- 슬라이싱 ---')
    lines.append(f"s[1:3]        = \n{s[1:3]}")
    lines.append(f"s['부산':'대구'] = \n{s['부산':'대구']}")

    output = '\n'.join(lines)
    print(output)
    write_log('03_iloc_vs_loc.txt', output)

# ─────────────────────────────────────────
# §04 : 결측값 처리 비교 (titanic)
# ─────────────────────────────────────────
def section04():
    print()
    print('=' * 60)
    print('§04  결측값 처리 비교 (titanic age 열)')
    print('=' * 60)

    lines = []

    titanic = sns.load_dataset('titanic')
    age = titanic['age']

    total   = len(age)
    missing = age.isna().sum()
    pct     = missing / total * 100

    lines.append(f'전체 행 수     : {total}')
    lines.append(f'결측값(NaN) 수 : {missing}  ({pct:.1f}%)')
    lines.append(f'mean           : {age.mean():.4f}')
    lines.append(f'median         : {age.median():.4f}')

    # 전략 비교
    age_fill0    = age.fillna(0)
    age_fill_mean = age.fillna(age.mean())
    age_fill_med  = age.fillna(age.median())
    age_drop      = age.dropna()

    def stat_line(label, s):
        return (f'{label:20s}  count={s.count():3d}  '
                f'mean={s.mean():.4f}  std={s.std():.4f}  '
                f'min={s.min():.1f}  max={s.max():.1f}')

    lines.append('\n--- 처리 전략별 통계 비교 ---')
    lines.append(stat_line('원본(NaN 포함)', age))
    lines.append(stat_line('fillna(0)',       age_fill0))
    lines.append(stat_line('fillna(mean)',    age_fill_mean))
    lines.append(stat_line('fillna(median)', age_fill_med))
    lines.append(stat_line('dropna()',        age_drop))

    output = '\n'.join(lines)
    print(output)
    write_log('04_fillna_compare.txt', output)

# ─────────────────────────────────────────
# §05 : 변수 변환 (astype / log / pd.cut)
# ─────────────────────────────────────────
def section05():
    print()
    print('=' * 60)
    print('§05  변수 변환 : astype · log 변환 · pd.cut 구간화')
    print('=' * 60)

    lines = []

    titanic = sns.load_dataset('titanic')
    age = titanic['age'].dropna()  # NaN 제거

    # astype
    fare = titanic['fare']
    lines.append(f'fare dtype 원본   : {fare.dtype}')
    fare_int = fare.astype('int64')
    lines.append(f'fare dtype 변환후 : {fare_int.dtype}  (소수점 잘림)')
    lines.append(f'fare 원본 앞3  : {list(fare[:3])}')
    lines.append(f'fare int 앞3   : {list(fare_int[:3])}')

    # log 변환 (왜도 제거)
    import math
    skew_orig = age.skew()
    age_log   = np.log1p(age)  # log(1+x) : 0값 안전
    skew_log  = age_log.skew()
    lines.append(f'\nlog 변환 전 age 왜도(skewness) : {skew_orig:.4f}')
    lines.append(f'log 변환 후 age 왜도(skewness) : {skew_log:.4f}')

    # pd.cut 구간화 (5구간)
    bins_labels = ['어린이(0-15)', '청소년(16-25)', '청년(26-35)', '중년(36-55)', '노년(56+)']
    age_cut = pd.cut(age, bins=[0, 15, 25, 35, 55, age.max() + 1], labels=bins_labels)
    counts  = age_cut.value_counts().sort_index()
    lines.append('\n--- pd.cut 5구간 value_counts() ---')
    for label, cnt in counts.items():
        lines.append(f'  {str(label):20s} : {cnt:3d}명')

    output = '\n'.join(lines)
    print(output)
    write_log('05_binning.txt', output)


if __name__ == '__main__':
    print('runner : day0521_data_preprocessing')
    print(f'Python {sys.version}')
    print()
    section01()
    section02()
    section03()
    section04()
    section05()
    print()
    print('모든 섹션 완료. logs/ 폴더 확인 바람.')
