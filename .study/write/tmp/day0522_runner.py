# path : .study/write/tmp/day0522_runner.py
# 2026-05-28

'''
day0522 블로그 글 실행 검증 runner
- §01 : MultiIndex 생성·조작 (pandas_test4 기반)
- §02 : auto-mpg describe() (전처리 포함)
- §03 : IQR vs Z-score 이상값 탐지 비교
- §04 : 이상값 처리 3전략 비교 (제거/대체/캡핑)
- §05 : MinMax vs Standard 정규화 비교
'''

import os
import sys
import numpy as np
import pandas as pd

LOGS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'test', 'day0522', 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)

AUTO_MPG_PATH = r'c:\_proj\python_workspace\test_pandas\data\auto-mpg.data'

def write_log(filename, content):
    path = os.path.join(LOGS_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  → {path} 저장 완료')

def load_auto_mpg():
    df = pd.read_csv(
        AUTO_MPG_PATH,
        sep=r'\s+', header=None,
        names=['mpg','cylinders','displacement','horsepower','weight',
               'acceleration','model_year','origin','car_name']
    )
    df['horsepower'] = pd.to_numeric(df['horsepower'], errors='coerce')
    return df

# ─────────────────────────────────────────
# §01 : MultiIndex 생성·조작
# ─────────────────────────────────────────
def section01():
    print('=' * 60)
    print('§01  MultiIndex 생성·조작')
    print('=' * 60)
    lines = []

    np.random.seed(0)
    df = pd.DataFrame(
        np.round(np.random.rand(6, 4), 2),
        columns=[['A', 'A', 'B', 'B'], ['C1', 'C2', 'C3', 'C4']],
        index=[['M', 'M', 'M', 'F', 'F', 'F'],
               ['id_1', 'id_2', 'id_3', 'id_1', 'id_2', 'id_3']]
    )
    df.columns.names = ['Cidx1', 'Cidx2']
    df.index.names   = ['Gidx1', 'Gidx2']

    lines.append('--- 다중 인덱스 DataFrame ---')
    lines.append(str(df))

    lines.append('\n--- 컬럼 A 그룹만 선택 ---')
    lines.append(str(df['A']))

    lines.append('\n--- 그룹 M 행만 선택 ---')
    lines.append(str(df.loc['M']))

    lines.append('\n--- stack(Cidx1) ---')
    lines.append(str(df.stack('Cidx1')))

    lines.append('\n--- unstack(Gidx2) ---')
    lines.append(str(df.unstack('Gidx2')))

    output = '\n'.join(lines)
    print(output)
    write_log('01_multiindex.txt', output)

# ─────────────────────────────────────────
# §02 : auto-mpg describe()
# ─────────────────────────────────────────
def section02():
    print()
    print('=' * 60)
    print('§02  auto-mpg describe()')
    print('=' * 60)
    lines = []

    df = load_auto_mpg()

    lines.append(f'shape : {df.shape}')
    lines.append(f'\nhorsepower 결측값 수 : {df["horsepower"].isna().sum()}')
    lines.append('(원본 "?" → NaN 변환 후)')

    lines.append('\n--- 수치형 컬럼 describe() ---')
    desc = df.describe().round(4)
    lines.append(str(desc))

    lines.append('\n--- horsepower 분포 ---')
    hp = df['horsepower'].dropna()
    lines.append(f'count={hp.count()}  mean={hp.mean():.2f}  '
                 f'std={hp.std():.2f}  min={hp.min():.1f}  max={hp.max():.1f}')
    lines.append(f'Q1={hp.quantile(0.25):.1f}  '
                 f'median={hp.median():.1f}  '
                 f'Q3={hp.quantile(0.75):.1f}')

    output = '\n'.join(lines)
    print(output)
    write_log('02_describe_distribution.txt', output)

# ─────────────────────────────────────────
# §03 : IQR vs Z-score 이상값 탐지 비교
# ─────────────────────────────────────────
def section03():
    print()
    print('=' * 60)
    print('§03  IQR vs Z-score 이상값 탐지 비교 (horsepower)')
    print('=' * 60)
    lines = []

    df = load_auto_mpg()
    hp = df['horsepower'].dropna()

    # IQR 방식
    Q1  = hp.quantile(0.25)
    Q3  = hp.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    iqr_mask  = (hp < lower) | (hp > upper)
    iqr_count = iqr_mask.sum()

    lines.append(f'IQR 방식')
    lines.append(f'  Q1={Q1:.1f}  Q3={Q3:.1f}  IQR={IQR:.1f}')
    lines.append(f'  하한={lower:.1f}  상한={upper:.1f}')
    lines.append(f'  이상값 개수 : {iqr_count}')
    if iqr_count > 0:
        lines.append(f'  이상값 목록 : {sorted(hp[iqr_mask].unique())}')

    # Z-score 방식
    mu  = hp.mean()
    sig = hp.std()
    z   = (hp - mu) / sig
    z_mask  = z.abs() > 3
    z_count = z_mask.sum()

    lines.append(f'\nZ-score 방식 (|Z| > 3)')
    lines.append(f'  mean={mu:.2f}  std={sig:.2f}')
    lines.append(f'  이상값 개수 : {z_count}')
    if z_count > 0:
        lines.append(f'  이상값 목록 : {sorted(hp[z_mask].unique())}')

    # 비교
    both = hp[iqr_mask & z_mask]
    only_iqr = hp[iqr_mask & ~z_mask]
    only_z   = hp[~iqr_mask & z_mask]
    lines.append(f'\n두 방식 모두 탐지  : {len(both)}개')
    lines.append(f'IQR 만 탐지        : {len(only_iqr)}개')
    lines.append(f'Z-score 만 탐지    : {len(only_z)}개')

    output = '\n'.join(lines)
    print(output)
    write_log('03_outlier_iqr_zscore.txt', output)

# ─────────────────────────────────────────
# §04 : 이상값 처리 3전략 비교
# ─────────────────────────────────────────
def section04():
    print()
    print('=' * 60)
    print('§04  이상값 처리 3전략 비교 (horsepower)')
    print('=' * 60)
    lines = []

    df = load_auto_mpg()
    hp = df['horsepower'].dropna()

    Q1  = hp.quantile(0.25)
    Q3  = hp.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    # 전략 1 : 제거 (IQR 범위 밖 제거)
    hp_drop = hp[(hp >= lower) & (hp <= upper)]

    # 전략 2 : 중앙값 대체
    hp_replace = hp.copy()
    median_val = hp.median()
    hp_replace[(hp < lower) | (hp > upper)] = median_val

    # 전략 3 : 캡핑 (Winsorizing)
    hp_clip = hp.clip(lower=lower, upper=upper)

    def stat(label, s):
        return (f'{label:20s}  count={s.count():3d}  '
                f'mean={s.mean():.2f}  std={s.std():.2f}  '
                f'min={s.min():.1f}  max={s.max():.1f}')

    lines.append('--- 이상값 처리 전략별 통계 ---')
    lines.append(stat('원본(이상값 포함)', hp))
    lines.append(stat('제거(dropna/mask)', hp_drop))
    lines.append(stat('중앙값 대체',       hp_replace))
    lines.append(stat('캡핑(Winsorize)',   hp_clip))

    output = '\n'.join(lines)
    print(output)
    write_log('04_outlier_handling.txt', output)

# ─────────────────────────────────────────
# §05 : MinMax vs Standard 정규화 비교
# ─────────────────────────────────────────
def section05():
    print()
    print('=' * 60)
    print('§05  MinMax vs Standard 정규화 비교')
    print('=' * 60)
    lines = []

    df = load_auto_mpg()
    df_clean = df.dropna(subset=['horsepower']).copy()

    cols = ['mpg', 'horsepower', 'weight']

    # Pandas 직접 계산
    lines.append('--- MinMax 정규화 (pandas 직접 계산) ---')
    for col in cols:
        s = df_clean[col]
        mm = (s - s.min()) / (s.max() - s.min())
        lines.append(f'{col:14s}  min={mm.min():.4f}  max={mm.max():.4f}  mean={mm.mean():.4f}')

    lines.append('\n--- 표준화(StandardScaler) (pandas 직접 계산) ---')
    for col in cols:
        s = df_clean[col]
        st = (s - s.mean()) / s.std()
        lines.append(f'{col:14s}  mean={st.mean():.4f}  std={st.std():.4f}  min={st.min():.3f}  max={st.max():.3f}')

    # sklearn 버전
    from sklearn.preprocessing import MinMaxScaler, StandardScaler
    X = df_clean[cols].values

    mm_scaler = MinMaxScaler()
    st_scaler = StandardScaler()
    X_mm = mm_scaler.fit_transform(X)
    X_st = st_scaler.fit_transform(X)

    lines.append('\n--- sklearn MinMaxScaler 결과 (앞 3행) ---')
    for row in X_mm[:3]:
        lines.append('  ' + '  '.join(f'{v:.4f}' for v in row))

    lines.append('\n--- sklearn StandardScaler 결과 (앞 3행) ---')
    for row in X_st[:3]:
        lines.append('  ' + '  '.join(f'{v:.4f}' for v in row))

    output = '\n'.join(lines)
    print(output)
    write_log('05_normalization_compare.txt', output)


if __name__ == '__main__':
    print('runner : day0522_outlier_normalization')
    print(f'Python {sys.version}')
    print()
    section01()
    section02()
    section03()
    section04()
    section05()
    print()
    print('모든 섹션 완료. logs/ 폴더 확인 바람.')
