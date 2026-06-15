# path : .study/write/tmp/day0523_runner.py
# 2026-05-28

'''
day0523 블로그 글 실행 검증 runner
- §01 : Figure·Axes 기초 — sin 곡선 저장 (numpy_test5 기반)
- §02 : histogram·boxplot — auto-mpg mpg 분포
- §03 : scatter·corr heatmap — auto-mpg 관계 시각화
- §04 : countplot·barplot — titanic 카테고리
- §05 : 시계열 line plot — DatetimeIndex (pandas_test8 기반)
'''

import os
import sys
import base64
import io
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # 비대화식 백엔드 (화면 없이 PNG 저장)
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

LOGS_DIR   = os.path.join(os.path.dirname(__file__), '..', '..', 'test', 'day0523', 'logs')
IMG_DIR    = LOGS_DIR
AUTO_MPG_PATH = r'c:\_proj\python_workspace\test_pandas\data\auto-mpg.data'
os.makedirs(LOGS_DIR, exist_ok=True)

# 한글 폰트 설정 (Windows)
plt.rcParams['font.family']      = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def write_log(filename, content):
    path = os.path.join(LOGS_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  → {path} 저장 완료')

def fig_to_b64(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=96, bbox_inches='tight')
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()

def load_auto_mpg():
    df = pd.read_csv(
        AUTO_MPG_PATH,
        sep=r'\s+', header=None,
        names=['mpg','cylinders','displacement','horsepower','weight',
               'acceleration','model_year','origin','car_name']
    )
    df['horsepower'] = pd.to_numeric(df['horsepower'], errors='coerce')
    return df.dropna(subset=['horsepower'])

# ─────────────────────────────────────────
# §01 : Figure·Axes 기초 (sin 곡선)
# ─────────────────────────────────────────
def section01():
    print('=' * 60)
    print('§01  Figure·Axes 기초 — sin 곡선')
    print('=' * 60)
    lines = []

    # numpy_test5.py 기반
    x   = np.linspace(-5, 5, 200)
    sin = np.sin(x)
    cos = np.cos(x)

    # plt.plot 방식 (pyplot 인터페이스)
    fig1, ax1 = plt.subplots(figsize=(6, 3))
    ax1.plot(x, sin, color='#52A97E', label='sin(x)')
    ax1.plot(x, cos, color='#E8875A', label='cos(x)', linestyle='--')
    ax1.axhline(0, color='gray', linewidth=0.8, linestyle=':')
    ax1.set_title('sin(x) · cos(x)')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.legend()
    b64_sin = fig_to_b64(fig1)
    plt.close(fig1)
    lines.append(f'sin·cos 그래프 base64 길이 : {len(b64_sin)} 문자')

    # PNG 저장
    png_path = os.path.join(IMG_DIR, '01_sin_cos.png')
    with open(png_path, 'wb') as f:
        f.write(base64.b64decode(b64_sin))
    lines.append(f'PNG 저장 : {png_path}')

    # base64 파일 저장 (HTML 삽입용)
    b64_path = os.path.join(IMG_DIR, '01_sin_cos_b64.txt')
    with open(b64_path, 'w', encoding='utf-8') as f:
        f.write(b64_sin[:80] + '...(이하 생략)')
    lines.append(f'base64 미리보기 저장 : {b64_path}')

    output = '\n'.join(lines)
    print(output)
    write_log('01_figure_axes.txt', output)

    return b64_sin

# ─────────────────────────────────────────
# §02 : histogram·boxplot
# ─────────────────────────────────────────
def section02():
    print()
    print('=' * 60)
    print('§02  histogram · boxplot (auto-mpg mpg)')
    print('=' * 60)
    lines = []

    df = load_auto_mpg()
    mpg = df['mpg']

    lines.append(f'mpg  count={mpg.count()}  mean={mpg.mean():.2f}  '
                 f'std={mpg.std():.2f}  min={mpg.min():.1f}  max={mpg.max():.1f}')

    fig, axes = plt.subplots(1, 2, figsize=(9, 3.5))

    # histogram
    axes[0].hist(mpg, bins=20, color='#52A97E', edgecolor='white', linewidth=0.5)
    axes[0].set_title('mpg 분포 (histogram)')
    axes[0].set_xlabel('mpg')
    axes[0].set_ylabel('count')

    # boxplot
    axes[1].boxplot(mpg, vert=True, patch_artist=True,
                   boxprops=dict(facecolor='#EBF7F1', color='#52A97E'),
                   medianprops=dict(color='#E8875A', linewidth=2))
    axes[1].set_title('mpg 이상값 확인 (boxplot)')
    axes[1].set_ylabel('mpg')

    plt.tight_layout()
    b64 = fig_to_b64(fig)
    plt.close(fig)

    png_path = os.path.join(IMG_DIR, '02_hist_box.png')
    with open(png_path, 'wb') as f:
        f.write(base64.b64decode(b64))
    lines.append(f'PNG 저장 : {png_path}  (base64 길이: {len(b64)} 문자)')

    output = '\n'.join(lines)
    print(output)
    write_log('02_hist_box.txt', output)

    return b64

# ─────────────────────────────────────────
# §03 : scatter + corr heatmap
# ─────────────────────────────────────────
def section03():
    print()
    print('=' * 60)
    print('§03  scatter + 상관행렬 heatmap')
    print('=' * 60)
    lines = []

    df = load_auto_mpg()
    numeric_cols = ['mpg', 'cylinders', 'displacement', 'horsepower', 'weight', 'acceleration']
    corr = df[numeric_cols].corr().round(3)

    lines.append('--- 상관행렬 ---')
    lines.append(str(corr))

    lines.append(f'\nmpg ↔ horsepower 상관계수 : {corr.loc["mpg","horsepower"]:.3f}')
    lines.append(f'mpg ↔ weight     상관계수 : {corr.loc["mpg","weight"]:.3f}')

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))

    # scatter
    axes[0].scatter(df['horsepower'], df['mpg'],
                   alpha=0.5, color='#5B9BD5', s=18)
    axes[0].set_xlabel('horsepower')
    axes[0].set_ylabel('mpg')
    axes[0].set_title('mpg vs horsepower')

    # heatmap
    import matplotlib.colors as mcolors
    im = axes[1].imshow(corr.values, cmap='RdYlGn', vmin=-1, vmax=1)
    axes[1].set_xticks(range(len(numeric_cols)))
    axes[1].set_yticks(range(len(numeric_cols)))
    axes[1].set_xticklabels(numeric_cols, rotation=45, ha='right', fontsize=8)
    axes[1].set_yticklabels(numeric_cols, fontsize=8)
    axes[1].set_title('상관행렬 heatmap')
    for i in range(len(numeric_cols)):
        for j in range(len(numeric_cols)):
            axes[1].text(j, i, f'{corr.values[i,j]:.2f}',
                        ha='center', va='center', fontsize=7,
                        color='black')
    plt.colorbar(im, ax=axes[1])

    plt.tight_layout()
    b64 = fig_to_b64(fig)
    plt.close(fig)

    png_path = os.path.join(IMG_DIR, '03_scatter_heatmap.png')
    with open(png_path, 'wb') as f:
        f.write(base64.b64decode(b64))
    lines.append(f'PNG 저장 : {png_path}  (base64 길이: {len(b64)} 문자)')

    output = '\n'.join(lines)
    print(output)
    write_log('03_scatter_heatmap.txt', output)

    return b64

# ─────────────────────────────────────────
# §04 : countplot·barplot (titanic)
# ─────────────────────────────────────────
def section04():
    print()
    print('=' * 60)
    print('§04  countplot · barplot (titanic)')
    print('=' * 60)
    lines = []

    titanic = sns.load_dataset('titanic')

    # pclass 분포
    pclass_counts = titanic['pclass'].value_counts().sort_index()
    lines.append('--- pclass 빈도 ---')
    for k, v in pclass_counts.items():
        lines.append(f'  {k}등석 : {v}명')

    # pclass별 생존율
    surv_rate = titanic.groupby('pclass', observed=True)['survived'].mean().round(3)
    lines.append('\n--- pclass별 생존율 ---')
    for k, v in surv_rate.items():
        lines.append(f'  {k}등석 : {v:.1%}')

    fig, axes = plt.subplots(1, 2, figsize=(9, 3.5))

    # countplot (수동 barh)
    axes[0].bar(pclass_counts.index.astype(str),
                pclass_counts.values,
                color=['#52A97E', '#5B9BD5', '#E8875A'])
    axes[0].set_title('pclass 승객 수 (countplot)')
    axes[0].set_xlabel('객실 등급')
    axes[0].set_ylabel('count')

    # barplot: pclass별 생존율
    axes[1].bar(surv_rate.index.astype(str),
                surv_rate.values,
                color=['#52A97E', '#5B9BD5', '#E8875A'])
    axes[1].set_title('pclass별 평균 생존율 (barplot)')
    axes[1].set_xlabel('객실 등급')
    axes[1].set_ylabel('생존율')
    axes[1].set_ylim(0, 1)

    plt.tight_layout()
    b64 = fig_to_b64(fig)
    plt.close(fig)

    png_path = os.path.join(IMG_DIR, '04_countplot_barplot.png')
    with open(png_path, 'wb') as f:
        f.write(base64.b64decode(b64))
    lines.append(f'PNG 저장 : {png_path}  (base64 길이: {len(b64)} 문자)')

    output = '\n'.join(lines)
    print(output)
    write_log('04_countplot_barplot.txt', output)

    return b64

# ─────────────────────────────────────────
# §05 : 시계열 line plot
# ─────────────────────────────────────────
def section05():
    print()
    print('=' * 60)
    print('§05  시계열 line plot (DatetimeIndex)')
    print('=' * 60)
    lines = []

    # pandas_test8.py 기반 — 2024-01 ~ 2024-06 가상 판매 데이터
    np.random.seed(42)
    date_range = pd.date_range('2024-01-01', periods=90, freq='D')
    sales = pd.Series(
        np.random.randint(80, 150, size=90) + np.arange(90) * 0.5,  # 약간의 증가 추세
        index=date_range,
        name='일별 판매량'
    )

    lines.append(f'DatetimeIndex  freq={sales.index.freq}  dtype={sales.index.dtype}')
    lines.append(f'기간 : {sales.index[0].date()} ~ {sales.index[-1].date()}')
    lines.append(f'mean={sales.mean():.1f}  min={sales.min():.0f}  max={sales.max():.0f}')

    # 문자열 날짜와 비교
    str_dates = ['2024-01-01', '2024-01-02', '2024-01-03']
    str_idx = pd.Index(str_dates)
    dt_idx  = pd.to_datetime(str_dates)
    lines.append(f'\n문자열 인덱스 dtype : {str_idx.dtype}')
    lines.append(f'DatetimeIndex dtype : {dt_idx.dtype}')
    lines.append('→ 문자열은 정렬·간격 계산 불가, DatetimeIndex 변환 필수')

    fig, axes = plt.subplots(2, 1, figsize=(9, 5), sharex=False)

    # 일별 라인
    axes[0].plot(sales.index, sales.values, color='#5B9BD5', linewidth=1)
    axes[0].set_title('일별 판매량 (DatetimeIndex)')
    axes[0].set_ylabel('판매량')

    # 주별 리샘플
    weekly = sales.resample('W').mean()
    axes[1].plot(weekly.index, weekly.values, color='#52A97E', linewidth=1.5, marker='o', markersize=4)
    axes[1].set_title('주별 평균 판매량 (resample W)')
    axes[1].set_ylabel('평균 판매량')
    axes[1].set_xlabel('날짜')

    plt.tight_layout()
    b64 = fig_to_b64(fig)
    plt.close(fig)

    png_path = os.path.join(IMG_DIR, '05_timeseries.png')
    with open(png_path, 'wb') as f:
        f.write(base64.b64decode(b64))
    lines.append(f'PNG 저장 : {png_path}  (base64 길이: {len(b64)} 문자)')

    output = '\n'.join(lines)
    print(output)
    write_log('05_timeseries.txt', output)

    return b64


if __name__ == '__main__':
    print('runner : day0523_data_visualization')
    print(f'Python {sys.version}')
    print()
    b64_01 = section01()
    b64_02 = section02()
    b64_03 = section03()
    b64_04 = section04()
    b64_05 = section05()

    # base64 딕셔너리 저장 (HTML 작성용)
    b64_dict = {
        '01_sin_cos':           b64_01,
        '02_hist_box':          b64_02,
        '03_scatter_heatmap':   b64_03,
        '04_countplot_barplot': b64_04,
        '05_timeseries':        b64_05,
    }
    import json
    dict_path = os.path.join(LOGS_DIR, '_b64_dict.json')
    with open(dict_path, 'w', encoding='utf-8') as f:
        json.dump(b64_dict, f)
    print(f'\n모든 섹션 완료. base64 딕셔너리 : {dict_path}')
