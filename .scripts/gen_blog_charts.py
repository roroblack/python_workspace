"""Generate matplotlib charts for blog posts day0521/0522/0526."""
import os
import sys

os.makedirs('.blog/img/charts', exist_ok=True)

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.family'] = ['Malgun Gothic', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

OUT = '.blog/img/charts'
ACCENT = '#52A97E'
ACCENT2 = '#E8875A'
ACCENT3 = '#5B9BD5'
ACCENT4 = '#9178C4'

# ============ DAY 0521 ============
# CH03: vectorize vs loop bar chart
import timeit
arr_sizes = [1_000, 10_000, 100_000]
loop_times = []
vec_times = []
for n in arr_sizes:
    a = np.arange(n, dtype=float)
    def loop_sum():
        s = 0.0
        for x in a:
            s += x
        return s
    t1 = timeit.timeit(loop_sum, number=20) / 20
    t2 = timeit.timeit(lambda: np.sum(a), number=20) / 20
    loop_times.append(t1 * 1000)
    vec_times.append(t2 * 1000)

fig, ax = plt.subplots(figsize=(7, 4))
x = np.arange(len(arr_sizes))
w = 0.35
ax.bar(x - w/2, loop_times, w, label='Python for loop', color=ACCENT2)
ax.bar(x + w/2, vec_times, w, label='NumPy vectorize', color=ACCENT)
ax.set_yscale('log')
ax.set_xticks(x)
ax.set_xticklabels([f'{n:,}' for n in arr_sizes])
ax.set_xlabel('array size')
ax.set_ylabel('time per call (ms, log scale)')
ax.set_title('Loop vs NumPy vectorize — sum() benchmark')
ax.legend()
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig(f'{OUT}/d0521_ch03_vectorize.png', dpi=130)
plt.close(fig)
print('saved d0521_ch03')

# CH07: fillna 전략 비교 (titanic age)
titanic = sns.load_dataset('titanic')
age = titanic['age']
strategies = {
    'original (drop NaN)': age.dropna(),
    'fillna(0)': age.fillna(0),
    'fillna(mean)': age.fillna(age.mean()),
    'fillna(median)': age.fillna(age.median()),
}
fig, axes = plt.subplots(1, 4, figsize=(13, 3.5), sharey=True)
for ax, (name, s) in zip(axes, strategies.items()):
    ax.hist(s, bins=25, color=ACCENT3, edgecolor='white', alpha=0.85)
    ax.set_title(f'{name}\nmean={s.mean():.2f} std={s.std():.2f}', fontsize=10)
    ax.set_xlabel('age')
axes[0].set_ylabel('count')
plt.suptitle('Titanic age — fillna 전략별 분포 비교', fontsize=12, y=1.02)
plt.tight_layout()
plt.savefig(f'{OUT}/d0521_ch07_fillna.png', dpi=130, bbox_inches='tight')
plt.close(fig)
print('saved d0521_ch07')

# CH08: log1p 변환 fare vs age
fare = titanic['fare'].dropna()
age2 = titanic['age'].dropna()
fig, axes = plt.subplots(2, 2, figsize=(10, 6))
axes[0,0].hist(fare, bins=40, color=ACCENT2, edgecolor='white')
axes[0,0].set_title(f'fare original — skew={fare.skew():.2f}')
axes[0,1].hist(np.log1p(fare), bins=40, color=ACCENT, edgecolor='white')
axes[0,1].set_title(f'fare log1p — skew={np.log1p(fare).skew():.2f}')
axes[1,0].hist(age2, bins=30, color=ACCENT2, edgecolor='white')
axes[1,0].set_title(f'age original — skew={age2.skew():.2f}')
axes[1,1].hist(np.log1p(age2), bins=30, color=ACCENT4, edgecolor='white')
axes[1,1].set_title(f'age log1p — skew={np.log1p(age2).skew():.2f}  (역방향!)')
for ax in axes.flat:
    ax.set_ylabel('count')
plt.tight_layout()
plt.savefig(f'{OUT}/d0521_ch08_log.png', dpi=130)
plt.close(fig)
print('saved d0521_ch08')

# ============ DAY 0522 ============
# load auto-mpg
auto = pd.read_csv(
    'test_pandas/data/auto-mpg.data',
    sep=r'\s+', header=None,
    names=['mpg','cylinders','displacement','horsepower',
           'weight','acceleration','model_year','origin','car_name'],
    na_values=['?']
).dropna()

# CH03: auto-mpg describe — boxplot 모든 수치 컬럼
num = auto.select_dtypes(include='number').drop(columns=['model_year','origin'])
fig, ax = plt.subplots(figsize=(8, 4))
ax.boxplot([num[c] for c in num.columns], labels=num.columns, patch_artist=True,
           boxprops=dict(facecolor='#EBF4FF'))
ax.set_title('auto-mpg — 수치 컬럼 분포 (boxplot)')
ax.tick_params(axis='x', rotation=20)
plt.tight_layout()
plt.savefig(f'{OUT}/d0522_ch03_describe.png', dpi=130)
plt.close(fig)
print('saved d0522_ch03')

# CH04: horsepower IQR vs Z-score
hp = auto['horsepower']
Q1 = hp.quantile(0.25); Q3 = hp.quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5*IQR; upper = Q3 + 1.5*IQR
z = (hp - hp.mean()) / hp.std()

fig, axes = plt.subplots(1, 2, figsize=(11, 4))
axes[0].hist(hp, bins=30, color=ACCENT3, edgecolor='white', alpha=0.85)
axes[0].axvline(lower, color=ACCENT2, ls='--', label=f'IQR 하한={lower:.1f}')
axes[0].axvline(upper, color=ACCENT2, ls='--', label=f'IQR 상한={upper:.1f}')
axes[0].set_title('horsepower — IQR 방식')
axes[0].set_xlabel('horsepower'); axes[0].set_ylabel('count')
axes[0].legend()

axes[1].scatter(range(len(hp)), z, c=[ACCENT2 if abs(v) > 3 else ACCENT3 for v in z], s=14)
axes[1].axhline(3, color='red', ls='--', alpha=0.5)
axes[1].axhline(-3, color='red', ls='--', alpha=0.5)
axes[1].set_title('horsepower — Z-score 방식')
axes[1].set_xlabel('index'); axes[1].set_ylabel('Z-score')
plt.tight_layout()
plt.savefig(f'{OUT}/d0522_ch04_iqr_z.png', dpi=130)
plt.close(fig)
print('saved d0522_ch04')

# CH05: 3 전략 boxplot 비교
median_val = hp.median()
hp_drop = hp[(hp >= lower) & (hp <= upper)]
hp_replace = hp.copy()
hp_replace[(hp_replace < lower) | (hp_replace > upper)] = median_val
hp_clip = hp.clip(lower=lower, upper=upper)

fig, ax = plt.subplots(figsize=(8, 4))
ax.boxplot([hp, hp_drop, hp_replace, hp_clip],
           labels=['원본', '제거(drop)', '중앙값 대체', '캡핑(clip)'],
           patch_artist=True,
           boxprops=dict(facecolor='#EBF7F1'))
ax.set_title('horsepower — 이상값 처리 3전략 결과 비교')
ax.set_ylabel('horsepower')
plt.tight_layout()
plt.savefig(f'{OUT}/d0522_ch05_strategies.png', dpi=130)
plt.close(fig)
print('saved d0522_ch05')

# CH06: 상관행렬 heatmap
corr = num.corr()
fig, ax = plt.subplots(figsize=(7, 5.5))
sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
            linewidths=0.5, ax=ax, vmin=-1, vmax=1)
ax.set_title('auto-mpg 상관행렬 (Pearson)')
plt.tight_layout()
plt.savefig(f'{OUT}/d0522_ch06_corr.png', dpi=130)
plt.close(fig)
print('saved d0522_ch06')

# CH07: MinMax vs Standard 스케일링 결과
from sklearn.preprocessing import MinMaxScaler, StandardScaler
mpg = auto[['mpg']]
mm = MinMaxScaler().fit_transform(mpg).flatten()
ss = StandardScaler().fit_transform(mpg).flatten()

fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))
axes[0].hist(mpg, bins=25, color=ACCENT3, edgecolor='white')
axes[0].set_title(f'원본 mpg\nmean={mpg.values.mean():.2f} std={mpg.values.std():.2f}')
axes[1].hist(mm, bins=25, color=ACCENT, edgecolor='white')
axes[1].set_title(f'MinMaxScaler\nmean={mm.mean():.2f} std={mm.std():.2f}')
axes[2].hist(ss, bins=25, color=ACCENT4, edgecolor='white')
axes[2].set_title(f'StandardScaler\nmean={ss.mean():.2f} std={ss.std():.2f}')
for ax in axes:
    ax.set_xlabel('value'); ax.set_ylabel('count')
plt.tight_layout()
plt.savefig(f'{OUT}/d0522_ch07_scaling.png', dpi=130)
plt.close(fig)
print('saved d0522_ch07')

# ============ DAY 0526 ============
# CH01: sin·cos
x = np.linspace(0, 2*np.pi, 200)
fig, ax = plt.subplots(figsize=(8, 3.5))
ax.plot(x, np.sin(x), label='sin(x)', color=ACCENT, linewidth=2)
ax.plot(x, np.cos(x), label='cos(x)', color=ACCENT2, linewidth=2, linestyle='--')
ax.set_xlabel('x'); ax.set_ylabel('y')
ax.set_title('Matplotlib Figure·Axes — sin / cos')
ax.legend(); ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUT}/d0526_ch01_sincos.png', dpi=130)
plt.close(fig)
print('saved d0526_ch01')

# CH03: histogram + boxplot
age3 = titanic['age'].dropna()
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
ax1.hist(age3, bins=20, edgecolor='white', color=ACCENT, alpha=0.85)
ax1.set_title('Titanic Age — Histogram (bins=20)')
ax1.set_xlabel('age'); ax1.set_ylabel('count')
ax2.boxplot(age3, vert=True, patch_artist=True,
            boxprops=dict(facecolor='#EBF4FF'))
ax2.set_title('Titanic Age — Boxplot')
ax2.set_ylabel('age')
plt.tight_layout()
plt.savefig(f'{OUT}/d0526_ch03_dist.png', dpi=130)
plt.close(fig)
print('saved d0526_ch03')

# CH04: scatter + heatmap
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
ax1.scatter(auto['weight'], auto['mpg'], alpha=0.5, c=ACCENT3, s=20, edgecolor='none')
ax1.set_xlabel('weight'); ax1.set_ylabel('mpg')
ax1.set_title('weight vs mpg — scatter')
sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
            linewidths=0.5, ax=ax2, vmin=-1, vmax=1, cbar=False)
ax2.set_title('auto-mpg correlation heatmap')
plt.tight_layout()
plt.savefig(f'{OUT}/d0526_ch04_scatter_heatmap.png', dpi=130)
plt.close(fig)
print('saved d0526_ch04')

# CH05: countplot + barplot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))
sns.countplot(data=titanic, x='pclass', hue='sex', ax=ax1,
              palette=[ACCENT3, ACCENT2])
ax1.set_title('선실 등급별 승객 수 (성별 구분)')
ax1.set_xlabel('pclass'); ax1.set_ylabel('count')
sns.barplot(data=titanic, x='pclass', y='fare', ax=ax2, color=ACCENT)
ax2.set_title('선실 등급별 평균 운임 (±95% CI)')
ax2.set_xlabel('pclass'); ax2.set_ylabel('mean fare')
plt.tight_layout()
plt.savefig(f'{OUT}/d0526_ch05_categorical.png', dpi=130)
plt.close(fig)
print('saved d0526_ch05')

# CH06: 시계열 rolling
np.random.seed(42)
dates = pd.date_range('2024-01-01', periods=365, freq='D')
vals = np.cumsum(np.random.randn(365)) + 100
s = pd.Series(vals, index=dates)
rolling = s.rolling(30).mean()
fig, ax = plt.subplots(figsize=(11, 4))
ax.plot(s.index, s.values, alpha=0.35, label='daily', color=ACCENT3)
ax.plot(rolling.index, rolling.values, linewidth=2.5,
        label='30-day MA', color=ACCENT2)
ax.set_title('2024 random walk — 30-day moving average')
ax.legend(); ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(f'{OUT}/d0526_ch06_timeseries.png', dpi=130)
plt.close(fig)
print('saved d0526_ch06')

# CH09: 2x2 dashboard
fig, axes = plt.subplots(2, 2, figsize=(11, 7), constrained_layout=True)
axes = axes.flatten()
axes[0].hist(age3, bins=20, color=ACCENT, edgecolor='white', alpha=0.85)
axes[0].set_title('Age Distribution')
axes[1].boxplot(age3, patch_artist=True, boxprops=dict(facecolor='#EBF4FF'))
axes[1].set_title('Age Boxplot')
sns.countplot(data=titanic, x='pclass', hue='sex', ax=axes[2],
              palette=[ACCENT3, ACCENT2])
axes[2].set_title('Pclass × Sex Count')
axes[3].scatter(titanic['age'].fillna(0), titanic['fare'],
                alpha=0.3, s=14, c=ACCENT4)
axes[3].set_title('Age vs Fare')
axes[3].set_xlabel('age'); axes[3].set_ylabel('fare')
plt.suptitle('Titanic — 4-Chart Dashboard', fontsize=13)
plt.savefig(f'{OUT}/d0526_ch09_dashboard.png', dpi=130, bbox_inches='tight')
plt.close(fig)
print('saved d0526_ch09')

print('ALL DONE')
