# build_day0527_html.py
# day0527_ml_intro.html 조립 — logs/*.txt(실제 실행 결과) + charts/*.png(base64) 주입
# 실행: c:\_proj\python_workspace\.venv\Scripts\python.exe build_day0527_html.py
#   (= GUIDE §11 run_all 역할: 터미널 값 직접 작성 금지, 로그에서 주입)
#   문체: interpreter_base64.html / retrospective_w4.html 의 "의문→해결→새 의문" 서사 추적 방식.
import base64, html, pathlib, re

HERE = pathlib.Path(__file__).parent
LOGS = HERE / "logs"
CHARTS = HERE / "charts"
OUT = HERE.parent.parent / "blog" / "day0527_ml_intro.html"   # .study/blog/
PYVER = "3.13.5"

def term(name):
    raw = (LOGS / f"{name}.txt").read_text(encoding="utf-8").splitlines()
    body = raw[3:] if len(raw) > 3 and raw[0].startswith("===") else raw
    return html.escape("\n".join(body).rstrip("\n"), quote=False)

def chart(fname):
    b = base64.b64encode((CHARTS / fname).read_bytes()).decode()
    return f"data:image/png;base64,{b}"

R = {
    "@@PY@@": PYVER,
    "@@TERM_00@@": term("00_workflow_taxonomy"),
    "@@TERM_01@@": term("01_three_points"),
    "@@TERM_02@@": term("02_fit_coef"),
    "@@TERM_03@@": term("03_standardize"),
    "@@TERM_04@@": term("04_split"),
    "@@TERM_05@@": term("05_overfit"),
    "@@TERM_06@@": term("06_ridge"),
    "@@TERM_07@@": term("07_metrics"),
    "@@CHART_02@@": chart("ch02_regression_line.png"),
    "@@CHART_03@@": chart("ch03_standardize.png"),
    "@@CHART_05@@": chart("ch05_overfit.png"),
    "@@CHART_06@@": chart("ch06_ridge.png"),
}

HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>파이썬 머신러닝 분석: model.fit() 한 줄은 무엇을 정하는가 — 회귀 직선은 어떻게 정해지나</title>
  <meta name="description" content="SK 네트웍스 AI Family 32기 머신러닝 Day1. '전체 R2가 그럴듯한데 왜 시험 점수는 낮을까', '모델을 더 키웠더니 왜 정반대로 낮아질까'라는 의문을 따라가며 최소제곱·train_test_split·과대적합·Ridge 규제·표준화·평가지표를 sklearn 실행으로 검증한 기록.">
  <meta property="og:title" content="파이썬 머신러닝 분석: model.fit() 한 줄은 무엇을 정하는가">
  <meta property="og:description" content="회귀 직선은 어떻게 정해지나 — R2의 함정, 과대적합 하락(test R2 −1132), Ridge 회복까지 실측으로 추적">
  <meta property="og:type" content="article">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="파이썬 머신러닝 분석: model.fit() 한 줄은 무엇을 정하는가">
  <meta name="twitter:description" content="R2의 함정 → 과대적합 하락 → Ridge 회복 → 표준화 → 평가지표">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Nanum+Gothic+Coding:wght@400;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
  <style>
@import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic+Coding:wght@400;700&display=swap');
:root {
  color-scheme: light;
  --ink:#1f2933; --muted:#667085; --line:#d7dee8;
  --paper:#ffffff; --surface:#ffffff;
  --accent:#52A97E; --accent-2:#E8875A; --accent-3:#5B9BD5; --accent-4:#9178C4;
  --accent-soft:#EBF7F1; --warn-soft:#FFF1E8;
  --code-bg:#1e1e1e; --code-ink:#e5e7eb;
  --shadow:none;
}
* { box-sizing:border-box; }
body { margin:0; background:var(--paper); color:var(--ink);
  font-family:"Nanum Gothic Coding","Segoe UI",Arial,sans-serif;
  line-height:1.78; font-size:16px; }
a { color:var(--accent-3); text-underline-offset:3px; }
.page { width:min(880px, calc(100% - 32px)); margin:0 auto; }
header.cover { padding:48px 0 24px; border-bottom:3px solid var(--ink); }
.eyebrow { font-size:0.9rem; color:var(--muted); letter-spacing:0.06em;
  text-transform:uppercase; margin:0 0 8px; }
h1 { font-size:2rem; line-height:1.32; margin:6px 0 12px; letter-spacing:-0.01em; }
.deck { font-size:1.05rem; color:#374151; margin:0 0 18px; }
.meta-row { display:flex; flex-wrap:wrap; gap:12px 18px;
  font-size:0.92rem; color:var(--muted); padding-top:10px;
  border-top:1px solid var(--line); }
.meta-row strong { color:var(--ink); margin-right:4px; }
main { padding:36px 0 60px; }
nav.toc { border-top:3px solid var(--ink); border-bottom:1px solid var(--line);
  padding:14px 0 18px; margin:0 0 30px; }
nav.toc h2 { font-size:0.95rem; letter-spacing:0.06em;
  text-transform:uppercase; color:var(--muted); margin:0 0 8px; }
nav.toc ol { margin:0; padding-left:1.3em; font-size:0.95rem; }
nav.toc a { color:var(--ink); text-decoration:none; border-bottom:1px dashed transparent; }
nav.toc a:hover { border-bottom-color:var(--accent-3); }
section { margin:48px 0 0; }
h2.chap { font-size:1.45rem; margin:0 0 14px; padding:14px 0 8px;
  border-top:3px solid var(--ink); }
h2.chap .num { display:inline-block; border:2px solid var(--accent-2);
  color:var(--accent-2); padding:1px 8px; font-size:0.8rem;
  margin-right:10px; vertical-align:middle; letter-spacing:0.04em; }
h2.chap .anchor-link { float:right; color:var(--muted); font-weight:400;
  text-decoration:none; opacity:0; transition:opacity .15s; }
h2.chap:hover .anchor-link { opacity:1; }
h3.step { margin:22px 0 10px; font-size:1.05rem; letter-spacing:0.04em;
  color:var(--accent-3); border-left:4px solid var(--accent-3); padding-left:10px; }
p { margin:10px 0; }
ul, ol { padding-left:1.4em; }
li { margin:4px 0; }
strong { color:var(--ink); }
.qbox { border-left:4px solid var(--accent-3); background:#EBF4FF;
  padding:12px 16px; margin:14px 0; }
.qbox .label { display:inline-block; background:var(--accent-3); color:#fff;
  padding:1px 8px; font-size:0.78rem; font-weight:700;
  margin-right:10px; letter-spacing:0.04em; }
.keypoint { border-left:4px solid var(--accent); background:var(--accent-soft);
  padding:12px 16px; margin:14px 0; }
.keypoint .label { display:inline-block; background:var(--accent); color:#fff;
  padding:1px 8px; font-size:0.78rem; font-weight:700;
  margin-right:10px; letter-spacing:0.04em; }
.callout { border-left:4px solid var(--accent-2); background:var(--warn-soft);
  padding:12px 16px; margin:14px 0; }
.callout .label { display:inline-block; background:var(--accent-2); color:#fff;
  padding:1px 8px; font-size:0.78rem; font-weight:700;
  margin-right:10px; letter-spacing:0.04em; }
.bridge { border-left:4px solid var(--muted); background:#F4F6F9;
  padding:10px 14px; margin:18px 0 4px; font-size:0.94rem; color:#374151; }
.bridge strong { color:var(--ink); }
blockquote.cite { border-left:4px solid var(--accent-4); background:#F7F5FD;
  padding:12px 16px; margin:14px 0; font-style:normal; }
blockquote.cite .src { display:block; color:var(--muted);
  font-size:0.9em; margin-top:6px; }
code { font-family:"Cascadia Code","Consolas","D2Coding",monospace;
  background:#EEF0F6; padding:1px 5px; font-size:0.92em; }
pre { background:var(--code-bg); color:var(--code-ink); padding:16px;
  overflow-x:auto; font-size:0.88rem; line-height:1.55; margin:14px 0;
  border:1px solid #2a2a2a; }
pre code { background:transparent; padding:0; color:inherit;
  font-family:"Cascadia Code","Consolas","D2Coding",monospace; }
.terminal { margin:14px 0; border:1px solid #2a2a2a; }
.terminal-header { background:#2d2d2d; color:#cbd5e1; padding:6px 12px;
  font-size:0.82rem; font-family:"Cascadia Code","Consolas",monospace; }
.terminal-header::before { content:'PS> '; color:var(--accent-2); font-weight:700; }
.terminal-body { background:#1e1e1e; color:#e5e7eb; padding:14px 16px;
  margin:0; overflow-x:auto; font-size:0.86rem; line-height:1.55;
  font-family:"Cascadia Code","Consolas","D2Coding",monospace; white-space:pre; }
table { border-collapse:collapse; width:100%; margin:14px 0; font-size:0.95rem; }
th, td { border:1px solid var(--line); padding:6px 10px; text-align:left; vertical-align:top; }
th { background:#EEF0F5; color:var(--ink); }
.hl { background:#EBF7F1; }
footer { padding:30px 0 60px; border-top:3px solid var(--ink); margin-top:50px;
  color:var(--muted); font-size:0.9rem; }
footer p { margin:6px 0; }
.ref-chain { border-left:4px solid var(--accent-4); background:#F7F5FD;
  padding:14px 18px; margin:24px 0; }
.ref-chain .ref-title { color:var(--accent-4); font-weight:700;
  margin:0 0 8px; letter-spacing:0.04em; }
.ref-chain ol { padding-left:1.4em; margin:0; }
.ref-chain li { margin:4px 0; font-size:0.93rem; }
figure.shot { margin:14px 0 18px; border:1px solid var(--line); background:#fff; padding:8px; }
figure.shot img { display:block; width:100%; height:auto; max-width:760px; margin:0 auto; }
figure.shot figcaption { margin-top:8px; font-size:0.86rem; color:var(--muted); text-align:center; letter-spacing:0.02em; }
.flow { border-top:3px solid var(--ink); border-bottom:1px solid var(--line);
  padding:14px 0 18px; margin:0 0 30px; }
.flow h2 { font-size:0.95rem; letter-spacing:0.06em; text-transform:uppercase; color:var(--muted); margin:0 0 10px; }
.flow ol { margin:0; padding-left:1.3em; }
.flow li { margin:6px 0; }
.flow .turn { color:var(--accent-2); font-weight:700; }
  </style>
</head>
<body>
<div class="page">

<header class="cover">
  <p class="eyebrow">Python · 머신러닝(교과목 2 · 단원 2) Day1 · 부트캠프</p>
  <h1>model.fit() 한 줄은 무엇을 정하는가 — 회귀 직선은 어떻게 정해지나</h1>
  <p class="deck">머신러닝 첫날, 모든 예제의 한가운데에는 <code>model.fit(X, y)</code> 한 줄이 있었다.
  "데이터를 넣으면 알아서 학습된다"는 말은 편하지만, 그 한 줄이 <strong>정확히 무엇을 정하는지</strong>는 가려져 있다.
  이 글은 그 한 줄을 묻는 데서 출발해 — 그럴듯해 보이던 점수가 시험에서 무너지고,
  모델을 키웠더니 오히려 더 무너지고, 그 하락을 회복하는 과정을 따라간 기록이다.
  모든 수치는 sklearn 으로 직접 돌린 결과이며 <code>random_state=42</code> 로 재현 가능하다.</p>
  <div class="meta-row">
    <span><strong>날짜</strong>2026-05-27</span>
    <span><strong>Python</strong>@@PY@@ · scikit-learn 1.8.0 · NumPy 2.4.4 · Pandas 3.0.2</span>
    <span><strong>OS</strong>Windows 11 Pro 25H2</span>
    <span><strong>IDE</strong>VS Code 1.117.0</span>
    <span><strong>HW</strong>Asrock x600 · Ryzen 8600G · 24GB LPDDR5 · RTX 4070 Super 12GB</span>
    <span><strong>커리큘럼</strong>교과목 2 · 단원 2 · 머신러닝 Day1 — 머신러닝_학습방법_데이터관리.pdf</span>
  </div>
</header>

<main>
<nav class="flow">
  <h2>이 글의 흐름 — 하나의 질문에서 갈라져 나온 질문들</h2>
  <ol>
    <li><a href="#ch1">시작 — <code>fit(X, y)</code>는 무엇을 정하나 (먼저, 이건 회귀인가 분류인가)</a></li>
    <li><a href="#ch2">fit이 정하는 것 — 모든 점을 지나는 직선은 없다, 그런데 전체 R2는 그럴듯하다</a></li>
    <li><a href="#ch3">그 점수를 믿어도 되나? 시험지를 따로 떼어 보다</a></li>
    <li><a href="#ch4">모델을 더 키웠더니 점수가 정반대로 무너졌다</a></li>
    <li><a href="#ch5">왜 낮아졌나 — 과대적합, 그리고 지하철 실습에서 만났던 그 현상</a></li>
    <li><a href="#ch6">되살리기 — 복잡도는 둔 채 계수만 누르는 규제(Ridge)</a></li>
    <li><a href="#ch7"><span class="turn">한 발 더</span> — 규제가 공정하려면, 특성이 같은 자에 있어야 했다(표준화)</a></li>
    <li><a href="#ch8">정리 — '잘한다'의 기준과, fit이 정한 것 한 문장</a></li>
  </ol>
</nav>

<!-- ===================== CH 01 ===================== -->
<section id="ch1">
  <h2 class="chap"><span class="num">CH 01</span>시작 — fit(X, y)는 무엇을 정하나<a href="#ch1" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>첫 수업에서 받은 <code>ML_sample.ipynb</code>는 주석 한 줄로 전체 흐름을 정의했다 —
  "데이터 준비 → 탐색 → 전처리 → <strong>학습(fit)</strong> → 평가 → 예측 → 저장". 코드로 보면 학습은 늘 같은 모양이었다:
  <code>model.fit(X, y)</code>. 데이터(<code>X</code>)와 정답(<code>y</code>)을 넣으면 모델이 "학습된다". 그런데 무엇이?</p>

  <h3 class="step">의문</h3>
  <div class="qbox">
    <span class="label">Q</span>
    <code>fit</code>이 끝난 모델은 분명 어떤 값을 손에 쥐고 있을 것이다. 그 값이 곧 예측의 근거일 텐데 —
    <strong>그 값은 무엇이고, 어떤 기준으로 정해질까?</strong> 이 질문 하나가 오늘 글 전체의 출발점이다.
  </div>
  <p>그런데 답을 찾기 전에 갈림길이 하나 있다. 회귀와 분류는 <code>fit</code>이 정하는 것의 성격이 다르다.
  그러니 먼저 — <strong>내가 받은 데이터가 회귀 문제인지 분류 문제인지부터</strong> 갈라야 한다.
  그 판단은 모델이 아니라 정답 <code>y</code>가 한다. <code>y</code>가 연속적인 실수면 회귀, 정해진 몇 개의 라벨이면 분류다.</p>

  <h3 class="step">테스트 — y의 형태로 문제를 가른다</h3>
  <p>sklearn 내장 데이터 두 개의 <code>y</code>를 같은 함수에 넣어 자동 판별해 본다. <code>diabetes</code>(질병 진행도)와 <code>iris</code>(붓꽃 품종)다.</p>
  <div class="terminal">
    <div class="terminal-header">ml_intro_runner.py §00 · load_diabetes/load_iris — y 형태로 회귀/분류 판별 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_00@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT</span>
    문제의 종류는 정답 <code>y</code>가 결정한다. <code>diabetes.target</code>은 연속값 → 회귀,
    <code>iris.target</code>은 <code>[0 1 2]</code> 세 라벨 → 분류. 오늘은 <strong>회귀</strong>를 끝까지 파고들며
    "fit이 무엇을 정하는가"를 추적한다. 회귀의 <code>fit</code>은 흔히 "직선을 긋는다"고 한다 —
    그렇다면 점들이 일직선이 아니면 그 직선은 대체 어떻게 정해질까?
  </div>
</section>

<!-- ===================== CH 02 ===================== -->
<section id="ch2">
  <h2 class="chap"><span class="num">CH 02</span>fit이 정하는 것 — 모든 점을 지나는 직선은 없다<a href="#ch2" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    점이 일직선 위에 있지 않으면 어떤 직선도 모든 점을 지날 수 없다.
    그렇다면 <code>fit</code>은 "모든 점을 지나는 직선"이 아니라 "<strong>오차가 가장 작은 직선</strong>"을 찾는 것이어야 한다.
    꺾인 세 점 (1,1)·(2,3)·(3,2)로 확인하자 — fit 직선의 오차 제곱합(SSE)이 임의 직선보다 작으면 가설은 통과다.
  </div>

  <h3 class="step">테스트 — 세 점에 직선을 맞춰 본다</h3>
  <div class="terminal">
    <div class="terminal-header">ml_intro_runner.py §01 · LinearRegression.fit(3점) — 최소제곱 SSE 최소 확인 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_01@@</pre>
  </div>
  <p>잔차는 <code>[-0.5, 1.0, -0.5]</code> — 0이 아니다. 직선은 세 점을 다 지나지 못한다.
  하지만 fit 직선의 SSE 1.5는 임의 직선 <code>y=2x</code>의 SSE 18.0보다 훨씬 작다. 가설대로다.</p>

  <blockquote class="cite">
    "LinearRegression fits a linear model … to minimize the residual sum of squares
    between the observed targets in the dataset, and the targets predicted by the linear approximation."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html" target="_blank" rel="noopener">LinearRegression</a> (최소제곱)</span>
  </blockquote>

  <h3 class="step">한 발 더 — 그래서 fit이 손에 쥐는 값은?</h3>
  <p>특성이 여러 개면 예측식은 <code>y = w1·x1 + … + wp·xp + b</code> 꼴이다. fit이 끝나면 모델은
  각 특성의 <strong>계수(<code>coef_</code>)</strong>와 <strong>절편(<code>intercept_</code>)</strong>을 쥔다.
  이 숫자들이 예측식의 전부다. 특성 10개짜리 diabetes 전체로 fit 해서 그 값을 꺼내 본다.</p>
  <div class="terminal">
    <div class="terminal-header">ml_intro_runner.py §02 · LinearRegression.fit(diabetes) — 계수·절편·R2 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_02@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_02@@" alt="diabetes bmi 특성에 대한 회귀 직선 산점도">
    <figcaption>그림 0527-1 · bmi 특성 하나로 그린 최소제곱 직선 (R2=0.344) — 점들은 직선 주변에 넓게 흩어진다</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT</span>
    "학습한다 = SSE를 최소화하는 계수·절편을 정한다." 특성 10개 → 계수 10개 + 절편 1개.
    그리고 전체 데이터 R2가 <strong>0.5177</strong>로 찍혔다. 절반 넘게 설명한다니, 그럴듯해 보인다.
  </div>

  <div class="bridge">
    <strong>여기서 멈칫했다</strong> — 이 0.5177은 <em>학습에 쓴 그 데이터로 다시 잰</em> 점수다.
    답안지를 외운 학생을 그 답안지로 시험 보는 것과 뭐가 다른가? 이 점수를 믿어도 될까?
  </div>
</section>

<!-- ===================== CH 03 ===================== -->
<section id="ch3">
  <h2 class="chap"><span class="num">CH 03</span>그 점수를 믿어도 되나<a href="#ch3" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    데이터의 일부를 <strong>시험용(test)</strong>으로 떼어 두고, 나머지(train)로만 학습한 뒤 시험을 보면,
    test 점수는 train 점수보다 낮게 나올 것이다. 그 차이가 곧 "외운 정도"의 신호다.
  </div>
  <p>이게 <code>train_test_split</code>이다. <code>ML_sample.ipynb</code>에서도 가장 먼저 import 한 도구였는데,
  그때는 "그냥 나누는 거"로만 알았다. 왜 나눠야 하는지를 점수로 직접 확인한다.</p>

  <pre><code class="language-python"># path : .study/test/ml_intro/ml_intro_runner.py §04 (발췌)
from sklearn.model_selection import train_test_split

Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
lr = LinearRegression().fit(Xtr, ytr)   # train으로만 학습
print(lr.score(Xtr, ytr))               # train R2
print(lr.score(Xte, yte))               # test R2 ← 처음 보는 데이터</code></pre>

  <h3 class="step">테스트</h3>
  <div class="terminal">
    <div class="terminal-header">ml_intro_runner.py §04 · train_test_split — train R2 vs test R2 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_04@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT</span>
    train R2 0.5279, test R2 0.4526. 가설대로 test가 낮다 — 전체로 잰 0.5177은 살짝 부풀려진 점수였다.
    다만 선형 모델에선 격차가 +0.0753로 아직 작다. 그래서 단순한 생각이 들었다 —
    <strong>모델을 더 똑똑하게(복잡하게) 만들면 점수가 더 오르지 않을까?</strong>
  </div>

  <div class="bridge">
    <strong>다음 시도</strong> — 특성을 제곱·세제곱으로 늘려(다항 특성) 모델의 표현력을 키워 본다.
    더 유연한 곡선이면 데이터를 더 잘 맞출 테니, test 점수도 같이 오를 거라고 기대했다.
  </div>
</section>

<!-- ===================== CH 04 ===================== -->
<section id="ch4">
  <h2 class="chap"><span class="num">CH 04</span>반전 — 모델을 더 키웠더니 점수가 무너졌다<a href="#ch4" class="anchor-link">#</a></h2>

  <h3 class="step">테스트 — 차수를 1에서 9까지 올린다</h3>
  <p>다항 특성의 차수(degree)를 올리며 train R2와 test R2를 같이 찍어 본다. 기대는 "둘 다 완만히 상승"이었다.</p>
  <div class="terminal">
    <div class="terminal-header">ml_intro_runner.py §05 · PolynomialFeatures degree↑ — train↑ / test↓ · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_05@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_05@@" alt="다항 차수에 따른 train/test R2 곡선">
    <figcaption>그림 0527-2 · 차수↑ → train R2는 오르는데 test R2는 음수로 하락 (degree 9에서 test R2 ≈ −1133)</figcaption>
  </figure>

  <h3 class="step">관찰 — 생각과 정반대였다</h3>
  <div class="keypoint">
    <span class="label">FAILURE → CLUE</span>
    train R2는 차수를 올릴수록 0.42 → 0.51로 올라간다. 그런데 test R2는 0.33에서 출발해
    차수 7에서 <strong>−39.6</strong>, 차수 9에서 <strong>−1132.87</strong>로 크게 낮아졌다.
    더 똑똑하게 만들었다고 믿은 모델이 처음 보는 데이터 앞에서 크게 낮아진 것이다.
    "복잡하게 = 더 좋게"라는 직관이 깨졌다. 가설이 깨진 그 자리가 다음 의문이다.
  </div>

  <div class="bridge">
    <strong>이 장면, 처음이 아니다</strong> — 며칠 전 지하철 이용객 예측 실습에서 똑같은 일을 겪었다.
    특성을 늘리고 모델을 키울수록 train 손실은 줄어드는데 test 점수(R2)는 오히려 떨어졌고,
    노트에 "왜 더 낮아졌지?"라고 적어 두었다. 그때 답을 못 냈던 그 현상의 원인을 지금 찾는다.
  </div>
</section>

<!-- ===================== CH 05 ===================== -->
<section id="ch5">
  <h2 class="chap"><span class="num">CH 05</span>왜 낮아졌나 — 과대적합이란<a href="#ch5" class="anchor-link">#</a></h2>

  <h3 class="step">답을 찾아서</h3>
  <p>train은 좋아지는데 test가 무너지는 현상에는 이름이 있었다 — <strong>과대적합(overfitting)</strong>.
  모델이 train 데이터의 진짜 패턴뿐 아니라 우연한 노이즈까지 과하게 학습해서, 외운 적 없는 데이터 앞에서 제대로 맞히지 못하는 상태다.
  차수를 올린다는 건 모델에게 "더 구불구불한 곡선을 그릴 자유"를 준 것이고, 그 자유로 train 점들을 일일이 통과하느라
  일반적인 추세를 잃은 것이다.</p>

  <blockquote class="cite">
    "If a model performs much better on training data than on unseen test data,
    the model is overfitting — it has learned patterns specific to the training set,
    including noise, that do not generalize."
    <span class="src">— scikit-learn User Guide · <a href="https://scikit-learn.org/stable/modules/cross_validation.html" target="_blank" rel="noopener">Cross-validation / generalization</a></span>
  </blockquote>

  <h3 class="step">정리 — 지하철 실습의 의문이 풀렸다</h3>
  <p>지하철 실습에서 특성을 마구 늘렸을 때 test R2가 떨어진 것도 같은 원리였다.
  그때 노트에 적은 "왜 더 낮아졌지?"의 답은 "모델이 train을 외워서, 일반화가 깨졌기 때문"이다.
  복잡도(자유도)는 무조건 이득이 아니라 <strong>train 적합과 일반화 사이의 트레이드오프</strong>라는 것 —
  이게 그날 못 본 한 줄이었다.</p>

  <div class="keypoint">
    <span class="label">의문 해소</span>
    "복잡하게 만들수록 좋다"가 아니라 "복잡할수록 train만 잘하고 test는 낮아질 위험이 커진다."
    그렇다면 방법은 둘이다 — ① 복잡도를 도로 줄이거나, ② 복잡도는 둔 채 모델이 데이터에 과하게 반응하지 못하게 누르거나.
    ②가 가능하다면 더 우아하다. 정말 될까?
  </div>

  <div class="bridge">
    <strong>다음 가설</strong> — 과대적합한 모델은 계수가 비정상적으로 커진다(작은 입력 변화에 과하게 반응하려고).
    그렇다면 차수 9를 그대로 두고 <em>계수가 커지는 것에 벌점</em>만 매기면, 하락을 막을 수 있지 않을까?
  </div>
</section>

<!-- ===================== CH 06 ===================== -->
<section id="ch6">
  <h2 class="chap"><span class="num">CH 06</span>되살리기 — 계수만 누르는 규제(Ridge)<a href="#ch6" class="anchor-link">#</a></h2>

  <h3 class="step">학습 → 가설</h3>
  <p><strong>Ridge 회귀</strong>는 손실에 <code>α · (계수 제곱합)</code> 벌점을 더한다. 계수가 커지면 손해가 되니,
  모델은 계수를 작게 유지하려 한다. <code>α</code>(규제 강도)를 키울수록 계수는 0 쪽으로 눌린다.</p>
  <div class="qbox">
    <span class="label">가설</span>
    CH 04에서 무너진 9차 모델 그대로, <code>α</code>만 0 → 10으로 키우면
    계수 크기(L2 norm)는 줄고 test R2는 음수에서 양수로 회복될 것이다.
  </div>

  <blockquote class="cite">
    "Ridge regression addresses some of the problems of Ordinary Least Squares
    by imposing a penalty on the size of the coefficients.
    The complexity parameter alpha ≥ 0 controls the amount of shrinkage."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/linear_model.html#ridge-regression" target="_blank" rel="noopener">Ridge regression</a></span>
  </blockquote>

  <h3 class="step">테스트</h3>
  <div class="terminal">
    <div class="terminal-header">ml_intro_runner.py §06 · Ridge(alpha) — 계수 축소 · test R2 회복 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_06@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_06@@" alt="Ridge alpha에 따른 test R2와 계수 크기 변화">
    <figcaption>그림 0527-3 · α↑ → 계수 L2 norm 13196→50으로 급감, test R2는 −1133에서 +0.34로 회복</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">가설 통과</span>
    α=0(규제 없음)일 때 계수 norm 13196·test R2 −1132.87 → α=10일 때 계수 norm 49.93·test R2 +0.3372.
    모델 구조(9차)는 그대로 둔 채 <strong>계수만 눌러서</strong> 하락을 회복시켰다. 이게 규제의 핵심이다.
  </div>

  <div class="bridge">
    <strong>그런데 의심이 하나 남았다</strong> — Ridge는 "계수 제곱합"에 벌점을 매긴다.
    특성마다 단위(스케일)가 제각각이면, 단위가 큰 특성의 계수는 원래 작고 단위가 작은 특성의 계수는 원래 크다.
    그 상태로 계수 크기에 똑같이 벌점을 매기면 <em>불공정</em>하지 않나? 내 Ridge 파이프라인엔 왜 <code>StandardScaler</code>가 끼어 있었지?
  </div>
</section>

<!-- ===================== CH 07 ===================== -->
<section id="ch7">
  <h2 class="chap"><span class="num">CH 07</span>한 발 더 — 규제가 공정하려면(표준화)<a href="#ch7" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>CH 06의 파이프라인은 사실 <code>PolynomialFeatures → StandardScaler → Ridge</code> 순서였다.
  <strong>표준화(StandardScaler)</strong>는 각 특성을 <code>z = (x − μ) / σ</code>로 바꿔 평균 0·표준편차 1의 같은 자에 올린다.
  이걸 Ridge 앞에 둔 이유가 바로 위의 의심에 대한 답이다 — 계수에 공정하게 벌점을 매기려면 특성들이 같은 척도여야 한다.</p>

  <div class="qbox">
    <span class="label">가설</span>
    스케일이 1000배 차이 나는 두 특성에 <code>StandardScaler</code>를 적용하면,
    둘 다 평균≈0·표준편차≈1로 맞춰져 같은 자에 올라설 것이다. (분포의 모양은 그대로, 척도만 바뀐다)
  </div>

  <blockquote class="cite">
    "Standardize features by removing the mean and scaling to unit variance.
    Many estimators … behave badly if the individual features do not more or less
    look like standard normally distributed data."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html" target="_blank" rel="noopener">StandardScaler</a></span>
  </blockquote>

  <h3 class="step">테스트</h3>
  <div class="terminal">
    <div class="terminal-header">ml_intro_runner.py §03 · StandardScaler.fit_transform — 평균0·표준편차1 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_03@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_03@@" alt="표준화 전/후 분포 히스토그램 비교">
    <figcaption>그림 0527-4 · 표준화 전(스케일 큼)과 후(평균0·표준편차1) — 분포의 모양은 그대로, 축(척도)만 통일</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT</span>
    표준화 후 두 특성 모두 평균≈0(1e-17 수준)·표준편차 1.0으로 정렬됐다. 분포의 '모양'은 그대로다.
    그래서 거리 기반 모델(KNN·SVM)과 규제(Ridge·Lasso)가 특정 특성에 휘둘리지 않는다 —
    CH 06의 Ridge가 제대로 동작한 숨은 전제가 이것이었다.
  </div>

  <div class="callout">
    <span class="label">함정</span>
    표준화는 <strong>train으로만 <code>fit</code></strong>하고 test엔 <code>transform</code>만 해야 한다.
    test의 평균·표준편차를 미리 반영하면 시험 문제를 미리 본 셈(data leakage)이 된다.
  </div>

  <div class="bridge">
    <strong>마지막 질문</strong> — 직선을 세우고(최소제곱), 시험을 보고(split), 하락을 막았다(규제+표준화).
    그런데 지금까지 "잘한다/못한다"를 R2 하나로만 봤다. 회귀가 아니라 분류라면? '잘함'을 무엇으로 재야 하나?
  </div>
</section>

<!-- ===================== CH 08 ===================== -->
<section id="ch8">
  <h2 class="chap"><span class="num">CH 08</span>정리 — '잘한다'의 기준과 fit이 정한 것<a href="#ch8" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 관찰</h3>
  <div class="qbox">
    <span class="label">의문</span>
    회귀는 R2·MSE·MAE로 "얼마나 가깝나"를 본다. 그런데 분류는 정확도 한 숫자로 충분할까?
    iris 3품종을 RandomForest로 분류해 클래스별로 뜯어보면, 정확도에 가려진 약점이 드러날까?
  </div>
  <p>분류 예시는 0527 <code>ML_sample.ipynb</code>와 동일한 <code>iris + RandomForestClassifier</code> 흐름으로 맞췄다.</p>
  <div class="terminal">
    <div class="terminal-header">ml_intro_runner.py §07 · r2/MSE/MAE · classification_report — 회귀·분류 지표 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_07@@</pre>
  </div>
  <p>정확도는 0.900으로 깔끔해 보인다. 하지만 클래스별로 보면 versicolor 재현율 0.900, virginica 재현율 0.800 —
  virginica 10개 중 2개를 versicolor로 잘못 봤다(혼동행렬의 <code>[2 8]</code>). 정확도 한 숫자가 이 불균형을 덮고 있었다.
  이래서 분류는 <strong>정밀도·재현율</strong>을 함께 봐야 한다 — "맞다고 한 것 중 진짜 맞은 비율"(정밀도)과
  "진짜 정답 중 찾아낸 비율"(재현율)은 서로 다른 실수를 잡아낸다.</p>

  <h3 class="step">최종 결론 — 출발 의문 회수</h3>
  <div class="keypoint">
    <span class="label">FINAL CONCLUSION</span>
    CH 01의 질문 "<code>model.fit(X, y)</code>는 무엇을 정하는가"의 답:
    <strong>fit은 (표준화된) X에서 손실(SSE)을 최소화하는 계수와 절편을 정한다.</strong>
    그 직선은 모든 점을 지나지 않고(CH 02), 학습 데이터 점수는 부풀려져 있으며(CH 03),
    복잡도를 키우면 오히려 무너지고(CH 04~05), 규제로 계수를 눌러 되살리되(CH 06)
    그 규제가 공정하려면 표준화가 전제였다(CH 07). 그리고 그 성능은 회귀면 R2/MSE/MAE,
    분류면 정밀도/재현율로 — 한 숫자에 속지 않게 — 재야 한다(CH 08).
  </div>

  <h3 class="step">한 문장으로</h3>
  <div class="keypoint">
    <span class="label">ONE-LINER</span>
    "데이터를 넣으면 알아서 학습된다"의 실체는 — <strong>처음 보는 데이터에서도 무너지지 않도록,
    전처리된 특성 위에서 손실을 최소화하는 파라미터를 정하는 일</strong>이다.
    그래서 머신러닝의 절반은 모델이 아니라 데이터 관리(split·표준화)와 일반화(규제)에 있다.
  </div>

  <div class="ref-chain">
    <p class="ref-title">📚 전체 근거 출처</p>
    <ol>
      <li><strong>공식 문서</strong>
        <a href="https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html" target="_blank" rel="noopener">scikit-learn · LinearRegression</a>(최소제곱),
        <a href="https://scikit-learn.org/stable/modules/linear_model.html#ridge-regression" target="_blank" rel="noopener">Ridge regression</a>,
        <a href="https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html" target="_blank" rel="noopener">StandardScaler</a>,
        <a href="https://scikit-learn.org/stable/modules/cross_validation.html" target="_blank" rel="noopener">generalization/CV</a>.</li>
      <li><strong>workspace</strong>
        <code>../ml_workspace/from_colab/0527/ml_sample.py</code> : 수업 ML 흐름(준비→…→저장),
        <code>iris + RandomForestClassifier + classification_report</code>.</li>
      <li><strong>강의자료</strong>
        <code>.study/pdf/머신러닝_학습방법_데이터관리.pdf</code> (배경지식).</li>
      <li><strong>실행 검증</strong>
        <code>.study/test/ml_intro/ml_intro_runner.py §00~§07</code>
        → <code>logs/*.txt</code>, <code>charts/*.png</code> (고정 시드 42, 재현 가능).</li>
    </ol>
  </div>

  <div class="bridge">
    <strong>다음 글 예고</strong> — 지하철 이용객 예측 실습 자체(특성을 어떻게 바꿔가며 R2를 끌어올렸는지)는
    의문과 시행착오가 많아 별도의 실습 기록으로 따로 정리한다. 이어지는 Day2에서는 회귀를 넘어
    분류·로지스틱 회귀로 들어간다.
  </div>
</section>
</main>

<footer>
  <p>SK 네트웍스 AI Family 32기 · 교과목 2 단원 2 머신러닝 Day1 (2026-05-27)</p>
  <p>모든 터미널 출력은 <code>.study/test/ml_intro/ml_intro_runner.py</code> 실제 실행 결과이며,
  <code>random_state=42</code>로 재현 가능하다. 차트는 base64 인라인으로 삽입했다.</p>
</footer>

</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
</body>
</html>
"""

for k, v in R.items():
    HTML = HTML.replace(k, v)
HTML = HTML.replace("​", "")  # zero-width space 제거(§5⑥)
OUT.write_text(HTML, encoding="utf-8")

# ── 검증(§12) ──
n_term = HTML.count('<div class="terminal">')
n_body = HTML.count('class="terminal-body"')
http_imgs = re.findall(r'<img[^>]+src="https?://', HTML)
b64_imgs = HTML.count('src="data:image/')
leftover = re.findall(r'@@[A-Z0-9_]+@@', HTML)
print(f"파일: {OUT}")
print(f"terminal div: {n_term} | terminal-body: {n_body} | (일치={n_term==n_body})")
print(f"외부 URL img: {len(http_imgs)} (0이어야 함) | base64 img: {b64_imgs}")
print(f"chap: {HTML.count('h2 class=\"chap\"')} | qbox: {HTML.count('class=\"qbox\"')} | keypoint: {HTML.count('class=\"keypoint\"')}")
print(f"미치환 placeholder: {leftover} | 크기: {len(HTML)//1024} KB")
