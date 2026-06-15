# path : c:\_proj\python_workspace\.study\write\tmp\gen_day0523_html.py
# 2026-05-23 — day0523 블로그 HTML 생성 (base64 이미지 내장)
# b64_dict.json 을 읽어 각 챕터 img src에 삽입

import json
import pathlib

BASE = pathlib.Path(r"c:\_proj\python_workspace")
B64_JSON = BASE / ".study" / "test" / "day0523" / "logs" / "_b64_dict.json"
OUT_HTML = BASE / ".study" / "blog" / "day0523_data_visualization.html"

with open(B64_JSON, encoding="utf-8") as f:
    b64 = json.load(f)

k01 = b64["01_sin_cos"]
k02 = b64["02_hist_box"]
k03 = b64["03_scatter_heatmap"]
k04 = b64["04_countplot_barplot"]
k05 = b64["05_timeseries"]

HTML = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Matplotlib·Seaborn으로 배우는 데이터 시각화 — SK 네트웍스 AI 32기 5주차</title>
  <meta name="description" content="SK 네트웍스 AI Family 32기 부트캠프 5주차 실습 기록. Matplotlib Figure·Axes 구조, histogram·boxplot, scatter·heatmap, countplot·barplot, DatetimeIndex 시계열 시각화를 실제 차트 이미지와 함께 정리.">
  <meta property="og:title" content="Matplotlib·Seaborn으로 배우는 데이터 시각화">
  <meta property="og:description" content="Figure·Axes 기초 → hist·box → scatter·heatmap → countplot·barplot → 시계열 라인차트">
  <meta property="og:type" content="article">
  <meta name="twitter:card" content="summary">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Nanum+Gothic+Coding:wght@400;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
  <style>
:root {{
  color-scheme: light;
  --ink:#1f2933; --muted:#667085; --line:#d7dee8;
  --paper:#ffffff; --surface:#ffffff;
  --accent:#52A97E; --accent-2:#E8875A; --accent-3:#5B9BD5; --accent-4:#9178C4;
  --accent-soft:#EBF7F1; --warn-soft:#FFF1E8;
  --code-bg:#1e1e1e; --code-ink:#e5e7eb;
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--paper); color:var(--ink);
  font-family:"Nanum Gothic Coding","Segoe UI",Arial,sans-serif;
  line-height:1.78; font-size:16px; }}
a {{ color:var(--accent-3); text-underline-offset:3px; }}
.page {{ width:min(880px, calc(100% - 32px)); margin:0 auto; }}
header.cover {{ padding:48px 0 24px; border-bottom:3px solid var(--ink); }}
.eyebrow {{ font-size:0.9rem; color:var(--muted); letter-spacing:0.06em;
  text-transform:uppercase; margin:0 0 8px; }}
h1 {{ font-size:2rem; line-height:1.32; margin:6px 0 12px; letter-spacing:-0.01em; }}
.deck {{ font-size:1.05rem; color:#374151; margin:0 0 18px; }}
.meta-row {{ display:flex; flex-wrap:wrap; gap:12px 18px;
  font-size:0.92rem; color:var(--muted); padding-top:10px;
  border-top:1px solid var(--line); }}
.meta-row strong {{ color:var(--ink); margin-right:4px; }}
main {{ padding:36px 0 60px; }}
nav.toc {{ border-top:3px solid var(--ink); border-bottom:1px solid var(--line);
  padding:14px 0 18px; margin:0 0 30px; }}
nav.toc h2 {{ font-size:0.95rem; letter-spacing:0.06em;
  text-transform:uppercase; color:var(--muted); margin:0 0 8px; }}
nav.toc ol {{ list-style:none; padding:0; margin:0;
  display:grid; grid-template-columns:repeat(2,1fr); gap:4px 16px; font-size:0.95rem; }}
nav.toc a {{ color:var(--ink); text-decoration:none; border-bottom:1px dashed transparent; }}
nav.toc a:hover {{ border-bottom-color:var(--accent-3); }}
section {{ margin:48px 0 0; }}
h2.chap {{ font-size:1.45rem; margin:0 0 14px; padding:14px 0 8px;
  border-top:3px solid var(--ink); }}
h2.chap .num {{ display:inline-block; border:2px solid var(--accent-4);
  color:var(--accent-4); padding:1px 8px; font-size:0.8rem;
  margin-right:10px; vertical-align:middle; letter-spacing:0.04em; }}
h2.chap .anchor-link {{ float:right; color:var(--muted); font-weight:400;
  text-decoration:none; opacity:0; transition:opacity .15s; }}
h2.chap:hover .anchor-link {{ opacity:1; }}
h3.step {{ margin:22px 0 10px; font-size:1.05rem; letter-spacing:0.04em;
  color:var(--accent-3); border-left:4px solid var(--accent-3); padding-left:10px; }}
p {{ margin:10px 0; }}
ul, ol {{ padding-left:1.4em; }}
li {{ margin:4px 0; }}
strong {{ color:var(--ink); }}
.qbox {{ border-left:4px solid var(--accent-3); background:#EBF4FF;
  padding:12px 16px; margin:14px 0; }}
.qbox .label {{ display:inline-block; background:var(--accent-3); color:#fff;
  padding:1px 8px; font-size:0.78rem; font-weight:700;
  margin-right:10px; letter-spacing:0.04em; }}
.keypoint {{ border-left:4px solid var(--accent); background:var(--accent-soft);
  padding:12px 16px; margin:14px 0; }}
.keypoint .label {{ display:inline-block; background:var(--accent); color:#fff;
  padding:1px 8px; font-size:0.78rem; font-weight:700;
  margin-right:10px; letter-spacing:0.04em; }}
.bridge {{ border-left:4px solid var(--muted); background:#F4F6F9;
  padding:10px 14px; margin:18px 0 4px; font-size:0.94rem; color:#374151; }}
.bridge strong {{ color:var(--ink); }}
blockquote.cite {{ border-left:4px solid var(--accent-4); background:#F7F5FD;
  padding:12px 16px; margin:14px 0; font-style:normal; }}
blockquote.cite .src {{ display:block; color:var(--muted);
  font-size:0.9em; margin-top:6px; }}
code {{ font-family:"Cascadia Code","Consolas","D2Coding",monospace;
  background:#EEF0F6; padding:1px 5px; font-size:0.92em; }}
pre {{ background:var(--code-bg); color:var(--code-ink); padding:16px;
  overflow-x:auto; font-size:0.88rem; line-height:1.55; margin:14px 0;
  border:1px solid #2a2a2a; }}
pre code {{ background:transparent; padding:0; color:inherit;
  font-family:"Cascadia Code","Consolas","D2Coding",monospace; }}
.terminal {{ margin:14px 0; border:1px solid #2a2a2a; }}
.terminal-header {{ background:#2d2d2d; color:#cbd5e1; padding:6px 12px;
  font-size:0.82rem; font-family:"Cascadia Code","Consolas",monospace; }}
.terminal-header::before {{ content:'PS> '; color:var(--accent-4); font-weight:700; }}
.terminal-body {{ background:#1e1e1e; color:#e5e7eb; padding:14px 16px;
  margin:0; overflow-x:auto; font-size:0.86rem; line-height:1.55;
  font-family:"Cascadia Code","Consolas","D2Coding",monospace; white-space:pre; }}
.ascii {{ font-family:"Nanum Gothic Coding","Cascadia Code","Consolas",monospace;
  white-space:pre; line-height:1.6; font-size:0.88rem;
  background:#F8F9FA; border:1px solid var(--line);
  padding:14px 16px; margin:14px 0; overflow-x:auto; }}
.chart-wrap {{ margin:16px 0; border:1px solid var(--line); padding:4px; }}
.chart-wrap img {{ width:100%; height:auto; display:block; }}
.chart-caption {{ font-size:0.85rem; color:var(--muted); margin:4px 8px 8px;
  font-style:italic; }}
table {{ border-collapse:collapse; width:100%; margin:14px 0; font-size:0.95rem; }}
th, td {{ border:1px solid var(--line); padding:6px 10px; text-align:left; vertical-align:top; }}
th {{ background:#EEF0F5; color:var(--ink); }}
footer {{ padding:30px 0 60px; border-top:3px solid var(--ink); margin-top:50px;
  color:var(--muted); font-size:0.9rem; }}
footer p {{ margin:6px 0; }}
.ref-chain {{ border-left:4px solid var(--accent-4); background:#F7F5FD;
  padding:14px 18px; margin:24px 0; }}
.ref-chain .ref-title {{ color:var(--accent-4); font-weight:700;
  margin:0 0 8px; letter-spacing:0.04em; }}
.ref-chain ol {{ padding-left:1.4em; margin:0; }}
.ref-chain li {{ margin:4px 0; font-size:0.93rem; }}
  </style>
</head>
<body>
<div class="page">

<header class="cover">
  <p class="eyebrow">Python · 5주차 · 교과목 2 · 데이터 분석</p>
  <h1>Matplotlib·Seaborn으로 배우는 데이터 시각화</h1>
  <p class="deck">이 글은 SK 네트웍스 AI Family 32기 부트캠프 5주차 수업 실습 기록이다.
  Matplotlib의 Figure·Axes 구조를 시작으로 histogram·boxplot, scatter·heatmap,
  countplot·barplot, DatetimeIndex 기반 시계열 시각화까지 — 실제로 생성한 차트 이미지와
  함께 각 시각화 기법의 쓰임새와 해석 방법을 정리한다.</p>
  <div class="meta-row">
    <span><strong>날짜</strong>2026-05-23</span>
    <span><strong>Python</strong>3.13.5 · NumPy 2.4.4 · Pandas 3.0.2</span>
    <span><strong>패키지</strong>matplotlib 3.10.9 · seaborn 0.13.2</span>
    <span><strong>OS</strong>Windows 11 Pro 25H2</span>
    <span><strong>IDE</strong>VS Code 1.117.0</span>
    <span><strong>커리큘럼</strong>교과목 2 · 단원 1 · 데이터 분석 — 데이터전처리.pdf 시각화 파트</span>
  </div>
</header>

<main>
<nav class="toc">
  <h2>목차</h2>
  <ol>
    <li><a href="#ch1">CH 01 — Matplotlib Figure·Axes 기초</a></li>
    <li><a href="#ch2">CH 02 — Histogram · Boxplot (분포 탐색)</a></li>
    <li><a href="#ch3">CH 03 — Scatter Plot · Correlation Heatmap</a></li>
    <li><a href="#ch4">CH 04 — Countplot · Barplot (범주형 시각화)</a></li>
    <li><a href="#ch5">CH 05 — 시계열 Line Plot · DatetimeIndex</a></li>
    <li><a href="#ch6">CH 06 — 시각화 선택 가이드 · FINAL CONCLUSION</a></li>
  </ol>
</nav>

<div class="bridge">
  <strong>도입</strong> — "데이터를 보기 좋게 그린다"가 아니라 "데이터를 제대로 읽는다"가 시각화의 목적이다.
  오늘 실습에서는 각 차트 유형이 어떤 질문에 답하는지를 기준으로 탐색한다:
  분포는 어떤가(histogram·boxplot), 변수 간 관계는(scatter·heatmap),
  범주별 차이는(countplot·barplot), 시간에 따른 변화는(timeseries).
</div>

<!-- ===================== CH 01 ===================== -->
<section id="ch1">
  <h2 class="chap"><span class="num">CH 01</span>Matplotlib Figure·Axes 기초<a href="#ch1" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>Matplotlib의 객체 계층은 <strong>Figure → Axes → Artist</strong> 순서다.
  <code>Figure</code>는 전체 캔버스이고, <code>Axes</code>(축)가 실제 차트 영역이다.
  <code>plt.subplots(nrows, ncols)</code>로 여러 Axes를 격자 배열로 생성할 수 있다.
  GUI 없이 PNG로 저장하려면 반드시 <code>matplotlib.use('Agg')</code>를 먼저 호출한다.</p>

  <pre><code class="language-python"># path : test_numpy/numpy_test5.py (발췌)
# 2026-05-23

import matplotlib
matplotlib.use('Agg')  # 서버·스크립트 환경 — GUI 없이 PNG 저장
import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
x = np.linspace(0, 2 * np.pi, 200)
axes[0].plot(x, np.sin(x), color='#52A97E', label='sin')
axes[1].plot(x, np.cos(x), color='#5B9BD5', label='cos')
for ax in axes:
    ax.legend()
    ax.set_xlabel('x')
fig.suptitle('sin · cos 곡선', fontsize=14)
fig.tight_layout()
plt.savefig('01_sin_cos.png', dpi=100)</code></pre>

  <blockquote class="cite">
    "The <code>Figure</code> is the top-level container. Each <code>Axes</code> is an
    individual plot. Always call <code>tight_layout()</code> to prevent overlapping labels."
    <span class="src">— Matplotlib 공식 문서 · <a href="https://matplotlib.org/stable/users/explain/figure/figure_intro.html" target="_blank" rel="noopener">Figure introduction</a></span>
  </blockquote>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    "<code>plt.plot()</code>과 <code>ax.plot()</code>은 결과가 같을까?"<br>
    → 결과는 같지만 <code>ax.plot()</code> 방식(OOP API)이 권장된다.
    <code>plt.plot()</code>은 현재 활성 Axes에 그리므로 여러 서브플롯이 있을 때 혼동이 생긴다.
    <strong>명시적 ax 참조</strong>가 실무에서 안전하다.
  </div>

  <h3 class="step">테스트 — 차트 결과</h3>
  <div class="terminal">
    <div class="terminal-header">day0523_runner.py §01 · Python 3.13.5 · PowerShell — Figure·Axes sin/cos 생성</div>
    <pre class="terminal-body">sin·cos 그래프 base64 길이 : 36584 문자
PNG 저장 : .study/test/day0523/logs/01_sin_cos.png</pre>
  </div>
  <div class="chart-wrap">
    <img src="data:image/png;base64,{k01}" alt="sin·cos 곡선 — Matplotlib subplots(1,2) 예시">
  </div>
  <p class="chart-caption">▲ Figure.subplots(1,2)로 두 Axes 생성 — 왼쪽 sin(초록), 오른쪽 cos(파랑)</p>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT</span>
    Matplotlib은 <strong>Figure → Axes → Artist</strong> 계층이다.
    <code>ax.plot()</code> OOP API가 다중 서브플롯 환경에서 명확하다.
    서버 환경에서 PNG 저장 시 반드시 <code>matplotlib.use('Agg')</code>를 최상단에 선언한다.
  </div>

  <div class="bridge">
    Figure·Axes 기초를 파악했다 → 이제 실제 데이터의 분포를 histogram·boxplot으로 탐색한다.
  </div>
</section>

<!-- ===================== CH 02 ===================== -->
<section id="ch2">
  <h2 class="chap"><span class="num">CH 02</span>Histogram · Boxplot — 분포 탐색<a href="#ch2" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p><strong>Histogram</strong>은 연속형 변수의 빈도 분포를 시각화한다. 빈(bin) 수에 따라
  형태가 달라지므로 Sturges·Freedman-Diaconis 규칙 또는 직접 테스트해 결정한다.
  <strong>Boxplot</strong>은 중앙값, Q1~Q3(IQR), 최대·최솟값, 이상값(flier)을 동시에 보여준다.
  분포 비교나 이상값 탐지의 시각적 보완에 유용하다.</p>

  <blockquote class="cite">
    "A box plot summarizes data distribution: the box spans Q1 to Q3,
    the line in the box is the median, and the whiskers extend to
    1.5×IQR beyond the quartiles."
    <span class="src">— Matplotlib 공식 문서 · <a href="https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.boxplot.html" target="_blank" rel="noopener">Axes.boxplot</a></span>
  </blockquote>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    "histogram의 bin 수가 결과 해석에 얼마나 영향을 미칠까?"<br>
    → bin이 너무 적으면 분포 형태를 놓치고, 너무 많으면 노이즈가 강조된다.
    auto-mpg mpg(count=392, mean=23.45)는 대략 20~30개 bin이 적당하다.
  </div>

  <h3 class="step">테스트 — 차트 결과</h3>
  <div class="terminal">
    <div class="terminal-header">day0523_runner.py §02 · Python 3.13.5 · PowerShell — auto-mpg mpg histogram·boxplot</div>
    <pre class="terminal-body">mpg  count=392  mean=23.45  std=7.81  min=9.0  max=46.6
PNG 저장 : .study/test/day0523/logs/02_hist_box.png  (base64 길이: 23440 문자)</pre>
  </div>
  <div class="chart-wrap">
    <img src="data:image/png;base64,{k02}" alt="auto-mpg mpg histogram + boxplot">
  </div>
  <p class="chart-caption">▲ 왼쪽: bins=25 histogram — 오른쪽: boxplot (이상값 플라이어 표시)</p>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT</span>
    histogram은 분포 전체 형태를, boxplot은 요약 통계(중앙·사분위·이상값)를 보여준다.
    두 차트를 나란히 배치하면 <strong>분포 형태와 이상값을 동시에 파악</strong>할 수 있다.
  </div>

  <div class="bridge">
    분포 탐색을 마쳤다 → 두 변수 간 관계를 scatter plot과 heatmap으로 탐색한다.
  </div>
</section>

<!-- ===================== CH 03 ===================== -->
<section id="ch3">
  <h2 class="chap"><span class="num">CH 03</span>Scatter Plot · Correlation Heatmap<a href="#ch3" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p><strong>Scatter plot</strong>은 두 연속형 변수의 관계(방향·강도)를 점으로 표현한다.
  세 번째 변수를 color 또는 size로 매핑하면 3차원 관계도 탐색 가능하다.
  <strong>Correlation Heatmap</strong>은 모든 수치형 변수 쌍의 상관계수를 격자 색상으로 표현한다.
  강한 음의 상관(-0.8 이하)은 분석에서 다중공선성 문제의 신호가 될 수 있다.</p>

  <blockquote class="cite">
    "Seaborn's <code>heatmap()</code> visualizes a matrix of values as a color-encoded grid,
    commonly used to display correlation matrices."
    <span class="src">— Seaborn 공식 문서 · <a href="https://seaborn.pydata.org/generated/seaborn.heatmap.html" target="_blank" rel="noopener">seaborn.heatmap</a></span>
  </blockquote>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    "연비(mpg)와 마력(horsepower)의 상관관계는 어떤 방향일까?"<br>
    → 마력이 높을수록 연비가 낮아지는 음의 상관이 예상된다.
    runner 결과: corr(mpg, horsepower) = -0.778 — 예상과 일치.
    weight는 더 강한 음의 상관(-0.832)이 실측됐다.
  </div>

  <h3 class="step">테스트 — 차트 결과</h3>
  <div class="terminal">
    <div class="terminal-header">day0523_runner.py §03 · Python 3.13.5 · PowerShell — scatter + 상관행렬 heatmap</div>
    <pre class="terminal-body">mpg ↔ horsepower 상관계수 : -0.778
mpg ↔ weight     상관계수 : -0.832
PNG 저장 : .study/test/day0523/logs/03_scatter_heatmap.png  (base64 길이: 81252 문자)</pre>
  </div>
  <div class="chart-wrap">
    <img src="data:image/png;base64,{k03}" alt="auto-mpg scatter plot(mpg vs horsepower) + 상관행렬 heatmap">
  </div>
  <p class="chart-caption">▲ 왼쪽: mpg vs horsepower scatter (r=-0.778) — 오른쪽: 6×6 상관행렬 heatmap</p>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT</span>
    상관계수가 -0.8 이하인 변수 쌍(mpg↔weight)은 회귀 모델 학습 전
    다중공선성(VIF) 확인이 필요하다. heatmap은 변수 선택의 1차 필터링에 활용한다.
  </div>

  <div class="bridge">
    연속형 변수 관계를 파악했다 → 범주형 변수(pclass, 생존)의 분포를 countplot·barplot으로 탐색한다.
  </div>
</section>

<!-- ===================== CH 04 ===================== -->
<section id="ch4">
  <h2 class="chap"><span class="num">CH 04</span>Countplot · Barplot — 범주형 시각화<a href="#ch4" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p><strong>Countplot</strong>은 범주별 빈도(count)를 막대로 나타낸다.
  hue 파라미터로 두 범주 변수의 조합을 비교할 수 있다.
  <strong>Barplot</strong>은 범주별 집계값(mean, sum 등)과 신뢰구간을 함께 표시한다.
  오차 막대(errorbar)가 내장돼 신뢰도를 함께 시각화할 수 있다.</p>

  <blockquote class="cite">
    "A bar plot represents an estimate of central tendency for a numeric variable with
    the height of each rectangle and provides some indication of the uncertainty around
    that estimate using error bars."
    <span class="src">— Seaborn 공식 문서 · <a href="https://seaborn.pydata.org/generated/seaborn.barplot.html" target="_blank" rel="noopener">seaborn.barplot</a></span>
  </blockquote>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    "titanic pclass별 생존율은 명확한 차이가 있을까?"<br>
    → 1등석 승객의 생존율이 3등석보다 유의미하게 높을 것이다.
    runner 결과: 1등석 63.0%, 2등석 47.3%, 3등석 24.2% — 가설 확인.
  </div>

  <h3 class="step">테스트 — 차트 결과</h3>
  <div class="terminal">
    <div class="terminal-header">day0523_runner.py §04 · Python 3.13.5 · PowerShell — countplot · barplot (titanic pclass)</div>
    <pre class="terminal-body">--- pclass 빈도 ---
  1등석 : 216명
  2등석 : 184명
  3등석 : 491명

--- pclass별 생존율 ---
  1등석 : 63.0%
  2등석 : 47.3%
  3등석 : 24.2%
PNG 저장 : .study/test/day0523/logs/04_countplot_barplot.png  (base64 길이: 21388 문자)</pre>
  </div>
  <div class="chart-wrap">
    <img src="data:image/png;base64,{k04}" alt="titanic pclass countplot + pclass별 생존율 barplot">
  </div>
  <p class="chart-caption">▲ 왼쪽: 등급별 승객 수 countplot — 오른쪽: pclass별 평균 생존율 barplot (95% CI 표시)</p>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT</span>
    countplot은 "얼마나 있는가", barplot은 "얼마나 높은가(평균)"를 답한다.
    barplot의 오차 막대는 신뢰구간이므로 겹치는 경우 차이가 통계적으로 유의미하지 않을 수 있다.
  </div>

  <div class="bridge">
    범주형 시각화를 완료했다 → 시간 축이 있는 시계열 데이터를 DatetimeIndex와 함께 시각화한다.
  </div>
</section>

<!-- ===================== CH 05 ===================== -->
<section id="ch5">
  <h2 class="chap"><span class="num">CH 05</span>시계열 Line Plot · DatetimeIndex<a href="#ch5" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p><strong>DatetimeIndex</strong>는 날짜·시간을 인덱스로 사용하는 Pandas 자료구조다.
  <code>pd.date_range(start, end, freq='D')</code>로 생성하며, 날짜 간격·집계·슬라이싱이
  문자열 인덱스보다 훨씬 강력하다.
  matplotlib/seaborn은 DatetimeIndex를 x축으로 인식해 날짜 레이블을 자동으로 포맷한다.</p>

  <pre><code class="language-python"># path : test_numpy/numpy_test10.py (발췌)
# 2026-05-23

dates = pd.date_range(start='2024-01-01', end='2024-03-30', freq='D')
ts = pd.Series(np.random.randint(100, 200, size=len(dates)), index=dates)

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(ts.index, ts.values, color='#52A97E', linewidth=1.2)
ax.set_title('2024 Q1 — 일별 더미 시계열')
ax.set_xlabel('날짜')
ax.set_ylabel('값')
fig.autofmt_xdate()   # x축 날짜 레이블 자동 회전</code></pre>

  <blockquote class="cite">
    "Pandas DatetimeIndex enables powerful time-series functionality:
    date resampling, frequency-based slicing, and automatic plot formatting."
    <span class="src">— Pandas 공식 문서 · <a href="https://pandas.pydata.org/docs/user_guide/timeseries.html" target="_blank" rel="noopener">Time series / date functionality</a></span>
  </blockquote>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    "문자열 날짜 인덱스와 DatetimeIndex는 시각화 결과가 다를까?"<br>
    → 문자열 인덱스는 x축을 단순 범주(categorical)로 처리해 날짜 간격이 무시된다.
    DatetimeIndex는 실제 시간 간격을 반영하므로 누락 날짜가 있으면 공백이 생긴다.
  </div>

  <h3 class="step">테스트 — 차트 결과</h3>
  <div class="terminal">
    <div class="terminal-header">day0523_runner.py §05 · Python 3.13.5 · PowerShell — 시계열 line plot + DatetimeIndex</div>
    <pre class="terminal-body">DatetimeIndex  freq=&lt;Day&gt;  dtype=datetime64[us]
기간 : 2024-01-01 ~ 2024-03-30
mean=134.8  min=84  max=180

문자열 인덱스 dtype : str
DatetimeIndex dtype : datetime64[us]
→ 문자열은 정렬·간격 계산 불가, DatetimeIndex 변환 필수
PNG 저장 : .study/test/day0523/logs/05_timeseries.png  (base64 길이: 77848 문자)</pre>
  </div>
  <div class="chart-wrap">
    <img src="data:image/png;base64,{k05}" alt="2024-01-01~03-30 시계열 line plot (DatetimeIndex)">
  </div>
  <p class="chart-caption">▲ 2024-01-01~03-30 일별 시계열 — DatetimeIndex 기반 x축 날짜 레이블 자동 포맷</p>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT</span>
    시계열 데이터는 반드시 <code>pd.to_datetime()</code>으로 인덱스를 변환한 후 시각화한다.
    <code>fig.autofmt_xdate()</code>로 x축 날짜 레이블 겹침을 방지한다.
  </div>

  <div class="bridge">
    5가지 시각화 유형을 모두 실습했다 → 어떤 상황에 어떤 차트를 쓸지 가이드라인을 정리하고 마무리한다.
  </div>
</section>

<!-- ===================== CH 06 ===================== -->
<section id="ch6">
  <h2 class="chap"><span class="num">CH 06</span>시각화 선택 가이드 · FINAL CONCLUSION<a href="#ch6" class="anchor-link">#</a></h2>

  <p>오늘 실습한 5가지 차트의 사용 기준을 정리한다.</p>

  <div class="ascii">
  ┌──────────────────────────────────────────────────────────┐
  │  데이터 종류별 시각화 선택 가이드                        │
  ├──────────────┬───────────────────────────────────────────┤
  │  목적        │  차트                                     │
  ├──────────────┼───────────────────────────────────────────┤
  │  분포 탐색   │  histogram / boxplot                      │
  │  변수 간 관계│  scatter plot / heatmap                   │
  │  범주 빈도   │  countplot / barplot                      │
  │  시간 변화   │  line plot (DatetimeIndex)                │
  │  비율 비교   │  barplot(normalized) / pie(지양)          │
  └──────────────┴───────────────────────────────────────────┘</div>

  <div class="keypoint">
    <span class="label">FINAL CONCLUSION</span>
    <ol>
      <li><strong>Figure·Axes 계층</strong> : OOP API(<code>ax.plot()</code>) 방식으로 명시적 Axes 참조.
        <code>matplotlib.use('Agg')</code>는 서버·스크립트 환경에서 필수.</li>
      <li><strong>분포 탐색</strong> : histogram(형태)과 boxplot(요약·이상값)을 나란히 사용.
        bin 수는 데이터에 맞게 테스트해 결정한다.</li>
      <li><strong>상관 분석</strong> : scatter는 두 변수, heatmap은 다변수 관계 탐색.
        |r| > 0.8이면 다중공선성 주의.</li>
      <li><strong>범주형 비교</strong> : countplot(빈도)과 barplot(평균+CI)은 질문이 다르다.
        오차 막대가 겹치면 차이가 통계적으로 유의하지 않을 수 있다.</li>
      <li><strong>시계열</strong> : 문자열 날짜 인덱스는 사용 금지.
        <code>pd.to_datetime()</code> 변환 후 DatetimeIndex로 작업한다.</li>
    </ol>
  </div>

  <div class="ref-chain">
    <p class="ref-title">참고 자료 (REF-CHAIN)</p>
    <ol>
      <li><strong>Matplotlib 공식 문서</strong>
        <a href="https://matplotlib.org/stable/users/explain/figure/figure_intro.html" target="_blank" rel="noopener">Figure introduction</a>
        — Figure·Axes·Artist 계층 설명</li>
      <li><strong>Matplotlib 공식 문서</strong>
        <a href="https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.boxplot.html" target="_blank" rel="noopener">Axes.boxplot</a>
        — IQR 기반 whisker 범위 설명</li>
      <li><strong>Seaborn 공식 문서</strong>
        <a href="https://seaborn.pydata.org/generated/seaborn.heatmap.html" target="_blank" rel="noopener">seaborn.heatmap</a>
        — annot, cmap, fmt 파라미터</li>
      <li><strong>Seaborn 공식 문서</strong>
        <a href="https://seaborn.pydata.org/generated/seaborn.barplot.html" target="_blank" rel="noopener">seaborn.barplot</a>
        — errorbar 신뢰구간 포함 막대 그래프</li>
      <li><strong>Pandas 공식 문서</strong>
        <a href="https://pandas.pydata.org/docs/user_guide/timeseries.html" target="_blank" rel="noopener">Time series / date functionality</a>
        — DatetimeIndex, date_range, freq 파라미터</li>
      <li><strong>workspace 확인</strong>
        <code>test_numpy/numpy_test5.py</code> — matplotlib 기초 실습</li>
      <li><strong>실행 검증</strong>
        <code>day0523_runner.py §01~§05</code>
        → <code>.study/test/day0523/logs/0*.png</code> + <code>_b64_dict.json</code></li>
    </ol>
  </div>
</section>

</main>

<footer>
  <p>SK 네트웍스 AI Family 32기 · 교과목 2 단원 1 · 2026-05-23</p>
  <p>Python 3.13.5 · NumPy 2.4.4 · Pandas 3.0.2 · matplotlib 3.10.9 · seaborn 0.13.2 · VS Code 1.117.0 · Windows 11 Pro 25H2</p>
</footer>

</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
</body>
</html>"""

OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
OUT_HTML.write_text(HTML, encoding="utf-8")
print(f"HTML 저장 완료 : {OUT_HTML}")
print(f"파일 크기     : {OUT_HTML.stat().st_size:,} bytes")

if __name__ == "__main__":
    pass
