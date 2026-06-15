# build_subway_html.py
# ml_practice01_subway.html 조립 — logs/*.txt(실제 실행 결과) + charts/*.png(base64) 주입
# 실행: c:\_proj\python_workspace\.venv\Scripts\python.exe build_subway_html.py
#   (= GUIDE §11 run_all 역할: 터미널 값 직접 작성 금지, 로그에서 주입)
#   문체: interpreter_base64.html 의 "의문→해결→예상 밖 결과→재해결" 서사 추적 방식.
import base64, html, pathlib, re

HERE = pathlib.Path(__file__).parent
LOGS = HERE / "logs"
CHARTS = HERE / "charts"
OUT = HERE.parent.parent / "blog" / "ml_practice01_subway.html"   # .study/blog/
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
    "@@TERM_00@@": term("00_inspect"),
    "@@TERM_01@@": term("01_naive"),
    "@@TERM_02@@": term("02_encode"),
    "@@TERM_03@@": term("03_date_scale"),
    "@@TERM_04@@": term("04_rf"),
    "@@TERM_05@@": term("05_target_encoding"),
    "@@TERM_06@@": term("06_guard_overfit"),
    "@@TERM_07@@": term("07_summary"),
    "@@CHART_IMP@@": chart("ch_importance.png"),
    "@@CHART_PRED@@": chart("ch_pred_actual.png"),
    "@@CHART_R2@@": chart("ch_r2_stages.png"),
}

HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>파이썬 머신러닝 실습1: 서울 지하철 이용객 수 예측 — R2 0에서 0.85까지, 무엇을 바꿨나</title>
  <meta name="description" content="SK 네트웍스 AI Family 32기 머신러닝 실습1. 서울 지하철 이용객 수를 회귀로 예측하며 '평균만 찍으면 R2 0, 무엇을 더해야 오를까', '더 강한 모델로 바꿨더니 왜 점수가 오히려 떨어졌나'를 따라간 기록. 결측치 처리·One-Hot·날짜 파싱·스케일링·타깃 인코딩·log1p·RandomForest·GradientBoosting을 실제 train/test로 검증.">
  <meta property="og:title" content="파이썬 머신러닝 실습1: 지하철 이용객 수를 예측하다">
  <meta property="og:description" content="R2 0에서 0.85까지, 그리고 '더 강한 모델이 더 기대와 다른 결과 — 실측으로 추적한 회귀 튜닝 기록">
  <meta property="og:type" content="article">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="파이썬 머신러닝 실습1: 지하철 이용객 수를 예측하다">
  <meta name="twitter:description" content="R2 0 → 0.74 → 0.85, 그리고 트리 모델이 오히려 떨어진 예상과 다른 결과">
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
  <p class="eyebrow">Python · 머신러닝 실습1 · 부트캠프</p>
  <h1>지하철 이용객 수를 예측하다 — R2 0에서 0.85까지, 무엇을 바꿨나</h1>
  <p class="deck">머신러닝 첫 실습 과제는 서울 지하철 이용객 수를 회귀로 예측하는 것이었다.
  날씨와 역 이름, 요일이 주어졌고 맞혀야 할 건 그날 그 역의 이용객 수.
  처음엔 "평균만 찍으면 <code>R2</code>가 0"이라는 바닥에서 출발해 특성을 하나씩 더하며 0.85까지 끌어올렸다.
  그런데 더 강한 모델(RandomForest·GradientBoosting)로 갈아탔더니 점수가 <strong>오히려 떨어졌다.</strong>
  이 글은 그 "왜 더 낮아졌나"를 끝까지 추적한 기록이다. 모든 수치는 실제 <code>subway_train.csv</code>로
  돌린 결과이며 <code>random_state=42</code>로 재현 가능하다.</p>
  <div class="meta-row">
    <span><strong>날짜</strong>2026-05-27~28</span>
    <span><strong>Python</strong>@@PY@@ · scikit-learn 1.8.0 · NumPy 2.4.4 · Pandas 3.0.2</span>
    <span><strong>OS</strong>Windows 11 Pro 25H2</span>
    <span><strong>IDE</strong>VS Code 1.117.0</span>
    <span><strong>HW</strong>Asrock x600 · Ryzen 8600G · 24GB LPDDR5 · RTX 4070 Super 12GB</span>
    <span><strong>커리큘럼</strong>교과목 2 · 머신러닝 실습1 — 지하철 이용객 수 예측 회귀</span>
  </div>
</header>

<main>
<nav class="flow">
  <h2>이 글의 흐름 — 하나의 점수를 끌어올리려던 시도들</h2>
  <ol>
    <li><a href="#ch1">시작 — 무엇을 맞히나, 그리고 데이터가 깨끗하지 않다</a></li>
    <li><a href="#ch2">바닥 — 평균만 찍으면 R2는 정확히 0이다</a></li>
    <li><a href="#ch3">첫 상승 — 날씨를 넣자 0.74, 그런데 무엇이 끌어올렸나</a></li>
    <li><a href="#ch4">큰 점프 — '어느 역, 무슨 요일'을 One-Hot으로 살리다 (0.85)</a></li>
    <li><a href="#ch5">천장 — 날짜를 풀고 스케일링해도 0.855에서 멈춘다</a></li>
    <li><a href="#ch6"><span class="turn">예상과 다른 결과</span> — 더 강한 모델(RandomForest)로 바꿨더니 점수가 떨어졌다</a></li>
    <li><a href="#ch7"><span class="turn">강한 신호도 안 통한다</span> — 역별 요일 평균과 log1p를 넣어도 선형을 못 넘다</a></li>
    <li><a href="#ch8">왜 낮아졌나 — 과대적합, 그리고 작은 데이터의 교훈</a></li>
    <li><a href="#ch9">정리 — 단계별 R2를 한 장에, 그리고 '무엇을 바꿨나'의 답</a></li>
  </ol>
</nav>

<!-- ===================== CH 01 ===================== -->
<section id="ch1">
  <h2 class="chap"><span class="num">CH 01</span>시작 — 무엇을 맞히나, 그리고 데이터가 깨끗하지 않다<a href="#ch1" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>실습 데이터는 <code>subway_train.csv</code>(900행)와 정답이 포함된 <code>subway_test.csv</code>(300행)다.
  각 행은 어느 날(<code>date</code>), 무슨 요일(<code>day_of_week</code>), 몇 월(<code>month</code>), 어느 역(<code>station_name</code>),
  그리고 그날의 가시거리·강수량·기온이 주어지고, 맞혀야 할 값은 <code>num_people</code> — 그 역의 이용객 수다.
  test에 정답이 있으니 <strong>test R2를 직접 잴 수 있다</strong>는 점이 다행이었다.</p>

  <h3 class="step">의문 → 점검</h3>
  <div class="qbox">
    <span class="label">의문</span>
    회귀를 시작하기 전에, 데이터부터 믿어도 될까? 컬럼이 비어 있거나 타입이 섞여 있으면
    <code>fit</code>은 시작도 못 한다. <strong>결측치가 있는지, 타깃의 분포가 어떤지</strong>를 먼저 확인한다.
  </div>
  <div class="terminal">
    <div class="terminal-header">subway_reg_runner.py §00 · read_csv/isna — 컬럼·타깃 분포·결측치 확인 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_00@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT</span>
    타깃 <code>num_people</code>은 7261~18186명, 평균 약 12557명의 연속값 → <strong>회귀</strong> 문제다.
    그런데 데이터가 깨끗하지 않았다 — <code>station_name</code> 5개, <code>visibility</code> 8개가 결측(NaN)이다.
    이걸 그대로 <code>LinearRegression</code>에 넣으면 "Input X contains NaN"으로 멈춘다.
    수치는 train 평균으로, 역 이름은 <code>'unknown'</code>으로 채우는 전처리를 먼저 깔고 출발한다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 전처리를 끝냈으니 이제 모델을 세운다.
    그런데 "잘했다"를 판단하려면 기준선이 필요하다. 아무것도 학습하지 않은 모델은 몇 점일까?
    그 바닥을 먼저 못 박아야 이후의 상승이 의미를 가진다.
  </div>
</section>

<!-- ===================== CH 02 ===================== -->
<section id="ch2">
  <h2 class="chap"><span class="num">CH 02</span>바닥 — 평균만 찍으면 R2는 정확히 0이다<a href="#ch2" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    어떤 입력이 들어와도 <strong>무조건 train 평균만 예측</strong>하는 모델은, 분산을 전혀 설명하지 못하니
    test R2가 0 근처일 것이다. 거기에 약한 특성(강수량) 하나만 넣어도 거의 못 벗어날 것이다.
    이게 "출발선"이고, 이후 모든 상승은 이 0과 비교해 읽는다.
  </div>
  <p>R2의 정의가 그렇다 — 평균을 예측하는 모델의 R2는 정확히 0이 기준이다. 직접 확인한다.</p>

  <pre><code class="language-python"># path : .study/test/subway_reg/subway_reg_runner.py §01 (발췌)
from sklearn.dummy import DummyRegressor

dummy = DummyRegressor(strategy='mean').fit(Xtr_dummy, ytr)
print(r2_score(yte, dummy.predict(Xte_dummy)))   # 평균만 예측 → R2 ≈ 0

lr = LinearRegression().fit(tr[['precipitation']], ytr)   # 강수량 1개
print(r2_score(yte, lr.predict(te[['precipitation']])))   # 거의 0</code></pre>

  <div class="terminal">
    <div class="terminal-header">subway_reg_runner.py §01 · DummyRegressor / 강수량 1개 — R2 바닥 확인 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_01@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT — 출발선 확정</span>
    평균만 예측하면 test R2 <strong>−0.0056</strong>(≈0, RMSE 1774명), 강수량 한 개만 쓰면 <strong>0.0260</strong>.
    여기가 바닥이다. 비가 오나 안 오나 지하철은 타니, 강수량 하나로는 사람 수가 거의 안 나뉜다.
    그렇다면 무엇을 더해야 점수가 오를까?
  </div>

  <div class="bridge">
    <strong>다음 시도</strong> — 일단 손에 쥔 숫자형 특성(가시거리·강수량·기온·월)을 전부 넣어 본다.
    날씨 네 개를 다 넣으면 바닥에서 얼마나 올라올까? 그리고 그중 무엇이 실제로 점수를 끌어올릴까?
  </div>
</section>

<!-- ===================== CH 03 ===================== -->
<section id="ch3">
  <h2 class="chap"><span class="num">CH 03</span>첫 상승 — 날씨를 넣자 0.74, 무엇이 끌어올렸나<a href="#ch3" class="anchor-link">#</a></h2>

  <h3 class="step">실험 → 관찰</h3>
  <p>숫자형 네 개(<code>visibility·precipitation·temperature·month</code>)를 모두 <code>LinearRegression</code>에 넣었다.
  바닥이 0이었으니, 0.1만 올라도 의미가 있다고 생각했는데 — 결과는 예상을 크게 웃돌았다.</p>
  <div class="terminal">
    <div class="terminal-header">subway_reg_runner.py §02 · LinearRegression(날씨4개) → +역·요일 One-Hot · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_02@@</pre>
  </div>
  <p>날씨 네 개만으로 test R2가 <strong>0.7380</strong>까지 뛰었다. 그런데 계수를 뜯어보니 답이 보였다 —
  <code>temperature</code>의 계수(약 150.8)가 다른 특성을 가장 크다. 강수량은 음수(−64.1)로 "비 오면 약간 줄지만",
  결국 이용객 수를 끌어올린 주역은 <strong>기온</strong>이었다. 추운 날과 더운 날의 통행량이 다른 것이다.</p>

  <blockquote class="cite">
    "LinearRegression fits a linear model with coefficients w = (w1, …, wp)
    to minimize the residual sum of squares between the observed targets …
    and the targets predicted by the linear approximation."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html" target="_blank" rel="noopener">LinearRegression</a></span>
  </blockquote>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">관찰 결과</span>
    날씨/달 4개 → test R2 0.7380. 그중 <code>temperature</code> 하나가 거의 다 했다.
    바닥(0)에서 한 번에 0.74로 올라온 것이다. 하지만 여기엔 우리가 <em>버린</em> 정보가 있다 —
    "어느 역인가", "무슨 요일인가". 잠실역과 강남역의 통행량이 같을 리 없는데, 그 범주형을 통째로 빼고 있었다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 버렸던 <code>station_name</code>과 <code>day_of_week</code>를
    되살려야 한다. 문제는 이게 숫자가 아니라 글자(범주형)라는 것. 선형모델이 먹을 수 있게
    숫자로 바꾸는 방법이 <strong>One-Hot 인코딩</strong>이다. 이걸 넣으면 점수가 얼마나 오를까?
  </div>
</section>

<!-- ===================== CH 04 ===================== -->
<section id="ch4">
  <h2 class="chap"><span class="num">CH 04</span>큰 점프 — '어느 역, 무슨 요일'을 One-Hot으로 살리다<a href="#ch4" class="anchor-link">#</a></h2>

  <h3 class="step">학습 → 가설</h3>
  <p><strong>One-Hot 인코딩</strong>은 범주 하나를 0/1 열 여러 개로 펼친다. 역 5종(+unknown)은 6개 열,
  요일 7종은 7개 열이 되어, 모델은 "이 행이 강남역인가? 금요일인가?"를 각각의 가중치로 학습할 수 있다.</p>
  <div class="qbox">
    <span class="label">가설</span>
    이용객 수를 실제로 가르는 건 날씨보다 "어느 역, 무슨 요일"일 것이다.
    이 범주형을 One-Hot으로 되살리면 test R2가 0.74에서 눈에 띄게 더 오를 것이다.
  </div>

  <blockquote class="cite">
    "Encode categorical features as a one-hot numeric array. …
    this creates a binary column for each category and returns a sparse or dense array."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html" target="_blank" rel="noopener">OneHotEncoder</a></span>
  </blockquote>

  <h3 class="step">테스트 — §02 출력의 후반부</h3>
  <p>위 §02 터미널의 <code>[③ + 역·요일 One-Hot]</code> 블록이 이 결과다. 특성은 17개(역 6 + 요일 7 + 숫자 4)로 늘었다.</p>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">가설 통과</span>
    One-Hot으로 역·요일을 살리니 test R2가 <strong>0.7380 → 0.8543</strong>으로 올랐다(RMSE 905→675명).
    가설대로 "어느 역/무슨 요일"이 날씨보다 강한 신호였다. train R2 0.8651, test R2 0.8543 —
    격차가 +0.011로 거의 없다. 선형모델이 데이터를 깔끔하게, 과대적합 없이 설명하고 있다는 뜻이다.
  </div>

  <div class="bridge">
    <strong>다음 시도</strong> — 그런데 <code>day_of_week</code> 컬럼이 실제 날짜와 어긋났을 가능성이 있었다.
    그렇다면 <code>date</code> 문자열에서 진짜 요일을 직접 뽑고, 일(day)도 추가하고, 스케일까지 맞추면
    0.855를 더 밀어올릴 수 있지 않을까?
  </div>
</section>

<!-- ===================== CH 05 ===================== -->
<section id="ch5">
  <h2 class="chap"><span class="num">CH 05</span>천장 — 날짜를 풀고 스케일링해도 0.855에서 멈춘다<a href="#ch5" class="anchor-link">#</a></h2>

  <h3 class="step">실험 → 관찰</h3>
  <p><code>pd.to_datetime(date).dt.dayofweek</code>로 날짜에서 진짜 요일을 뽑고, 일(day)도 특성에 넣었다.
  그리고 수치 특성에 <code>StandardScaler</code>를 적용했다 — 단, train으로만 <code>fit</code>하고 test엔 <code>transform</code>만
  해서 시험 정보가 새지 않게(data leakage 방지) 했다.</p>
  <div class="terminal">
    <div class="terminal-header">subway_reg_runner.py §03 · date 파싱 + StandardScaler — 선형 천장 확인 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_03@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">관찰 결과 — 천장</span>
    특성을 더 넣고 스케일까지 맞췄는데 test R2는 <strong>0.8543 → 0.8550</strong>, 사실상 제자리였다.
    선형모델은 "이 역이면서 동시에 이 요일일 때"의 상호작용을 곱으로 표현하지 못한다.
    가중치의 <em>합</em>으로만 예측하는 구조라 여기가 선형의 천장이다.
  </div>

  <div class="bridge">
    <strong>여기서 자연스러운 생각</strong> — 그럼 더 똑똑한, 비선형 모델로 바꾸면 되지 않나?
    트리 기반 모델은 "강남역 AND 금요일"을 분기로 자연히 잡는다. RandomForest로 갈아타면
    당연히 0.855를 넘어설 거라 기대했다. 결과는 정반대였다.
  </div>
</section>

<!-- ===================== CH 06 ===================== -->
<section id="ch6">
  <h2 class="chap"><span class="num">CH 06</span>예상과 다른 결과 — 더 강한 모델로 바꿨더니 점수가 떨어졌다<a href="#ch6" class="anchor-link">#</a></h2>

  <h3 class="step">실험 — 같은 특성, 모델만 RandomForest로</h3>
  <p>특성은 그대로 두고 모델만 <code>RandomForestRegressor(n_estimators=300)</code>로 바꿨다.
  트리 300그루가 역·요일·날씨의 상호작용을 분기로 잡아낼 테니, 선형의 0.855는 가볍게 넘으리라 기대했다.</p>
  <div class="terminal">
    <div class="terminal-header">subway_reg_runner.py §04 · RandomForestRegressor — train≫test 격차 · 특성 중요도 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_04@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_IMP@@" alt="RandomForest 특성 중요도 막대그래프">
    <figcaption>그림 1 · RandomForest 특성 중요도 — temperature(0.73)가 압도, 역(stat_idx)은 0.017에 불과</figcaption>
  </figure>

  <h3 class="step">관찰 — 예상과 달랐다</h3>
  <div class="keypoint">
    <span class="label">FAILURE → CLUE</span>
    test R2가 <strong>0.8550 → 0.7063</strong>으로 <em>떨어졌다.</em> 더 강한 모델로 바꿨는데 점수가 내려간 것이다.
    단서는 train R2 0.9557 ≫ test R2 0.7063 — 격차가 <strong>+0.249</strong>로 벌어졌다.
    선형모델에선 격차가 거의 0이었는데, 트리는 train을 train에 과하게 맞춰졌다. 이게 바로 노트에 "왜 더 낮아졌지?"라고
    적었던 그 현상이다. 가설("강한 모델 = 더 높은 점수")이 맞지 않은 자리가 다음 의문을 만든다.
  </div>

  <div class="bridge">
    <strong>다음 시도</strong> — 어쩌면 특성이 부족해서일 수 있다. 강의에서 배운 "강한 신호" 특성,
    즉 <strong>역별 요일 평균 이용객 수</strong>(target encoding)를 직접 만들어 넣고, 편차가 큰 타깃엔
    <code>log1p</code>를 씌우면 트리가 선형을 넘을 수 있지 않을까?
  </div>
</section>

<!-- ===================== CH 07 ===================== -->
<section id="ch7">
  <h2 class="chap"><span class="num">CH 07</span>강한 신호도 안 통한다 — 역별 요일 평균과 log1p<a href="#ch7" class="anchor-link">#</a></h2>

  <h3 class="step">학습 → 가설</h3>
  <p><strong>타깃 인코딩</strong>은 "이 역의 이 요일 평균 이용객 수"를 train에서 미리 계산해 특성으로 넣는 기법이다.
  모델은 그 평균(베이스라인)에서 날씨에 따른 <em>잔차</em>만 학습하면 되니 유리하다. 편차가 큰 타깃엔
  <code>log1p</code>를 씌워 분포를 안정화하고, 예측 후 <code>expm1</code>로 되돌린다.</p>
  <div class="qbox">
    <span class="label">가설</span>
    <code>stat_dow_avg</code>(역×요일 평균)·<code>stat_month_avg</code>(역×월 평균)를 넣고 <code>log1p</code>까지 적용하면,
    모델이 잔차만 학습하면 되므로 CH 06에서 떨어진 0.706이 선형의 0.855를 넘어설 것이다.
  </div>
  <p>매핑(그룹 평균)은 <strong>train으로만</strong> 계산해 test에 적용했다 — test 평균을 미리 보면 누수가 되기 때문이다.</p>
  <div class="terminal">
    <div class="terminal-header">subway_reg_runner.py §05 · target encoding + log1p · RandomForest — 예측 vs 실제 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_05@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_PRED@@" alt="예측값 대 실제값 산점도">
    <figcaption>그림 2 · 예측 vs 실제 (test R2=0.708) — 점들이 완벽 예측선 주변에 모이지만 흩어짐이 남아 있다</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">FAILURE → CLUE</span>
    강한 특성에 log1p까지 넣었는데도 test R2는 <strong>0.7078</strong> — 여전히 선형의 0.855에 못 미친다.
    train R2(log) 0.9135로 train은 잘 맞히지만 test가 안 따라온다. 특성을 더 줘도 트리는
    900행짜리 작은 데이터에서 노이즈를 외우는 경향이 남았다. 문제는 특성이 아니라 <strong>모델 자체</strong>였다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — train만 잘하고 test가 낮아지는 이 현상엔 이름이 있다.
    그 이름을 정확히 부르고, 트리의 복잡도를 눌러(깊이 제한·규제) 격차를 줄여 본다.
    그래도 선형을 못 넘는다면, 거기서 배울 교훈은 분명해진다.
  </div>
</section>

<!-- ===================== CH 08 ===================== -->
<section id="ch8">
  <h2 class="chap"><span class="num">CH 08</span>왜 낮아졌나 — 과대적합과 작은 데이터의 교훈<a href="#ch8" class="anchor-link">#</a></h2>

  <h3 class="step">답을 찾아서</h3>
  <p>train은 0.95인데 test는 0.70 — 이 격차의 이름은 <strong>과대적합(overfitting)</strong>이다.
  트리 300그루가 train 데이터의 진짜 패턴뿐 아니라 우연한 노이즈까지 과하게 학습해서, 처음 보는 test에서 오류한다.
  특히 데이터가 900행으로 작고 신호(주로 기온)가 약할 때, 자유도 높은 모델은 외울 여지가 너무 많다.</p>

  <blockquote class="cite">
    "Learning the parameters of a prediction function and testing it on the same data
    is a methodological mistake … This situation is called overfitting."
    <span class="src">— scikit-learn User Guide · <a href="https://scikit-learn.org/stable/modules/cross_validation.html" target="_blank" rel="noopener">Cross-validation: evaluating estimator performance</a></span>
  </blockquote>

  <h3 class="step">실험 — 복잡도를 누른다(GradientBoosting + 깊이 제한)</h3>
  <p>그렇다면 모델 복잡도를 줄이면 격차가 좁혀질까? <code>GradientBoostingRegressor</code>에 <code>max_depth=4</code>,
  <code>learning_rate=0.05</code>, <code>subsample=0.8</code>로 규제를 걸고 RandomForest와 train↔test 격차를 비교했다.</p>
  <div class="terminal">
    <div class="terminal-header">subway_reg_runner.py §06 · GradientBoosting(depth=4) vs RandomForest — 과대적합 격차 비교 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_06@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">의문 해소</span>
    깊이를 제한한 GradientBoosting도 test R2 <strong>0.6773</strong>으로 선형(0.855)을 넘지 못했다.
    노트에 적었던 "왜 더 낮아졌지?"의 답은 이것이다 — <strong>모델이 강해서가 아니라, 데이터가 작고
    신호가 약하면 강한 모델은 과대적합으로 오히려 손해</strong>를 본다. 복잡도는 공짜가 아니다.
  </div>

  <div class="callout">
    <span class="label">함정</span>
    "더 강한 모델 = 더 좋은 점수"는 흔한 착각이다. 트리 앙상블·딥러닝이 유리한 건 데이터가 충분히 크고
    신호가 풍부할 때다. 900행·약한 신호에서는 <strong>단순한 모델(One-Hot 선형)이 규제 효과 덕에 더 잘 일반화</strong>한다.
    모델 선택은 데이터 크기와 신호 강도에 종속된다.
  </div>

  <div class="bridge">
    <strong>마지막 챕터로</strong> — 바닥(0)에서 시작해 0.855까지 올렸다가, 강한 모델에서 0.68로 떨어진 전 과정을
    한 장의 그래프로 모아 본다. 무엇을 바꿨을 때 점수가 뛰고, 무엇이 오히려 깎아먹었는지가 한눈에 보인다.
  </div>
</section>

<!-- ===================== CH 09 ===================== -->
<section id="ch9">
  <h2 class="chap"><span class="num">CH 09</span>정리 — 단계별 R2와 '무엇을 바꿨나'의 답<a href="#ch9" class="anchor-link">#</a></h2>

  <h3 class="step">관찰 → 정리</h3>
  <div class="terminal">
    <div class="terminal-header">subway_reg_runner.py §07 · 단계별 test R2 누적 — 무엇을 바꿨을 때 점수가 뛰었나 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_07@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_R2@@" alt="단계별 test R2 막대그래프">
    <figcaption>그림 3 · 단계별 test R2 — ①0(바닥)→②0.74(날씨)→③0.85(One-Hot)→④0.855(천장)→⑤⑥⑦ 트리에서 하락</figcaption>
  </figure>

  <table>
    <thead><tr><th>단계</th><th>바꾼 것</th><th>모델</th><th>test R2</th></tr></thead>
    <tbody>
      <tr><td>①</td><td>평균만 예측</td><td>DummyRegressor</td><td>≈ 0 (−0.006)</td></tr>
      <tr><td>②</td><td>날씨/달 4개</td><td>LinearRegression</td><td>0.738</td></tr>
      <tr class="hl"><td>③</td><td>+ 역·요일 One-Hot</td><td>LinearRegression</td><td>0.854</td></tr>
      <tr class="hl"><td>④</td><td>+ 날짜 파싱·스케일링</td><td>LinearRegression</td><td><strong>0.855</strong> (최고)</td></tr>
      <tr><td>⑤</td><td>모델 교체</td><td>RandomForest</td><td>0.706 ↓</td></tr>
      <tr><td>⑥</td><td>+ 타깃 인코딩·log1p</td><td>RandomForest</td><td>0.708</td></tr>
      <tr><td>⑦</td><td>깊이 제한·규제</td><td>GradientBoosting</td><td>0.677 ↓</td></tr>
    </tbody>
  </table>

  <h3 class="step">최종 결론 — 출발 질문 회수</h3>
  <div class="keypoint">
    <span class="label">FINAL CONCLUSION</span>
    "R2 0에서 무엇을 바꿔야 오를까"의 답: <strong>점수를 끌어올린 건 더 강한 모델이 아니라 '특성'이었다.</strong>
    바닥(0)에서 날씨를 넣어 0.74(주역은 기온), 거기에 역·요일을 One-Hot으로 살려 0.85로 올랐다.
    반대로 RandomForest·GradientBoosting으로 모델을 키운 단계(⑤⑥⑦)는 과대적합으로 점수를 깎아먹었다.
    이 데이터에서 가장 정확한 모델은 <strong>One-Hot 인코딩을 더한 단순 LinearRegression(0.855)</strong>이었다.
  </div>

  <h3 class="step">한 문장으로</h3>
  <div class="keypoint">
    <span class="label">ONE-LINER</span>
    "성능을 올린다"는 건 모델을 키우는 일이 아니라 — <strong>데이터에 맞는 특성을 찾고(역·요일),
    데이터 크기에 맞는 복잡도의 모델을 고르는 일</strong>이다. 900행·약한 신호에서는 단순+규제가 강력함을 더 낫다.
  </div>

  <div class="ref-chain">
    <p class="ref-title">📚 전체 근거 출처</p>
    <ol>
      <li><strong>공식 문서</strong>
        <a href="https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html" target="_blank" rel="noopener">scikit-learn · LinearRegression</a>(최소제곱),
        <a href="https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html" target="_blank" rel="noopener">OneHotEncoder</a>,
        <a href="https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html" target="_blank" rel="noopener">RandomForestRegressor</a>,
        <a href="https://scikit-learn.org/stable/modules/cross_validation.html" target="_blank" rel="noopener">overfitting / generalization</a>.</li>
      <li><strong>workspace</strong>
        <code>../ml_workspace/from_colab/0528_data/subway/subway_train.csv·subway_test.csv</code> (실측 데이터),
        <code>../ml_workspace/from_colab/0528-s/_subway_tune.py</code> (튜닝 흐름: target encoding·log1p·트리 앙상블).</li>
      <li><strong>강의자료</strong>
        <code>.study/pdf/머신러닝_학습방법_데이터관리.pdf</code> (전처리·데이터 관리 배경지식).</li>
      <li><strong>실행 검증</strong>
        <code>.study/test/subway_reg/subway_reg_runner.py §00~§07</code>
        → <code>logs/*.txt</code>, <code>charts/*.png</code> (고정 시드 42, 재현 가능).</li>
    </ol>
  </div>
</section>
</main>

<footer>
  <p>SK 네트웍스 AI Family 32기 · 교과목 2 머신러닝 실습1 — 지하철 이용객 수 예측 회귀 (2026-05-27~28)</p>
  <p>모든 터미널 출력은 <code>.study/test/subway_reg/subway_reg_runner.py</code> 실제 실행 결과이며,
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
zwsp = HTML.count("​")
shot_left = HTML.count("figure.shot")  # 잔여 placeholder 텍스트 검사용(실제 figure는 class="shot")
print(f"파일: {OUT}")
print(f"terminal div: {n_term} | terminal-body: {n_body} | (일치={n_term == n_body})")
print(f"외부 URL img: {len(http_imgs)} (0이어야 함) | base64 img: {b64_imgs}")
print(f"chap: {HTML.count('h2 class=\"chap\"')} | qbox: {HTML.count('class=\"qbox\"')} | keypoint: {HTML.count('class=\"keypoint\"')}")
print(f"zero-width space: {zwsp} (0이어야 함)")
print(f"미치환 placeholder: {leftover} | 크기: {len(HTML) // 1024} KB")
