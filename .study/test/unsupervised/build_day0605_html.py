# build_day0605_html.py
# day0605_unsupervised.html 조립 — logs/*.txt(실제 실행 결과) + charts/*.png(base64) 주입
# 실행: c:\_proj\python_workspace\.venv\Scripts\python.exe build_day0605_html.py
#   (= GUIDE §11 run_all 역할: 터미널 값 직접 작성 금지, 로그에서 주입 / §12 자체검증)
#   템플릿: build_day0527_html.py 의 head/CSS verbatim. 문체: interpreter "의문→해결→새 의문" 추적.
import base64, html, pathlib, re

HERE = pathlib.Path(__file__).parent
LOGS = HERE / "logs"
CHARTS = HERE / "charts"
OUT = HERE.parent.parent / "blog" / "day0605_unsupervised.html"   # .study/blog/
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
    "@@TERM_00@@": term("00_no_labels"),
    "@@TERM_01@@": term("01_kmeans_once"),
    "@@TERM_02@@": term("02_elbow"),
    "@@TERM_03@@": term("03_silhouette"),
    "@@TERM_04@@": term("04_vs_truth"),
    "@@TERM_05@@": term("05_scatter"),
    "@@TERM_06@@": term("06_association"),
    "@@TERM_08@@": term("08_lift_by_hand"),
    "@@TERM_09@@": term("09_init_compare"),
    "@@TERM_07@@": term("07_summary"),
    "@@CHART_ELBOW@@": chart("ch_elbow.png"),
    "@@CHART_SIL@@": chart("ch_silhouette.png"),
    "@@CHART_SCATTER@@": chart("ch_scatter.png"),
    "@@CHART_RULES@@": chart("ch_rules.png"),
    "@@CHART_LIFT_HAND@@": chart("ch_lift_hand.png"),
    "@@CHART_INIT@@": chart("ch_init.png"),
}

HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>파이썬 비지도학습 분석: 정답을 가린 k-means는 무엇을 묶는가 — k=3이 맞는가</title>
  <meta name="description" content="SK 네트웍스 AI Family 32기 머신러닝 Day7. 정답 y를 가린 채 가까운 점만으로 묶는 k-means에서 '클러스터 개수 k는 누가 정하나'를 따라간 기록. 엘보우와 실루엣이 정작 k=3이 아니라 k=2를 가리키는 예상과 다른 결과, 그래도 ARI 0.62로 품종과 겹치는 군집, 그리고 또 다른 비지도학습인 연관규칙(지지도·신뢰도·향상도)까지 sklearn 실행으로 검증한다.">
  <meta property="og:title" content="파이썬 비지도학습 분석: 정답을 가린 k-means는 무엇을 묶는가">
  <meta property="og:description" content="엘보우·실루엣이 k=3이 아니라 k=2를 가리키는 예상과 다른 결과 → ARI 0.62 → 연관규칙 lift 2.00까지 실측으로 추적">
  <meta property="og:type" content="article">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="파이썬 비지도학습 분석: 정답을 가린 k-means는 무엇을 묶는가">
  <meta name="twitter:description" content="비지도학습 — 정답 없이 묶기, k의 결정(엘보우·실루엣), 정답과의 비교(ARI), 연관규칙(지지도·신뢰도·향상도)">
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
  <p class="eyebrow">Python · 머신러닝(교과목 2 · 단원 2) Day7 · 부트캠프</p>
  <h1>정답을 가린 k-means는 무엇을 묶는가 — k=3이 맞는가</h1>
  <p class="deck">지금까지의 모든 모델은 정답 <code>y</code>를 보며 학습했다. 회귀의 <code>y</code>, 분류의 <code>y</code>.
  그런데 비지도학습은 그 <code>y</code>를 가린다. 정답 없이, 가까운 점끼리만 묶는다.
  이 글은 iris에서 정답을 가리고 <code>KMeans</code>를 돌린 데서 출발해 — "그래서 군집은 몇 개로 묶어야 하나"라는 질문이
  엘보우와 실루엣 앞에서 <strong>내가 알던 정답(3종)과 어긋나는</strong> 장면을 따라간 기록이다.
  그 어긋남이 무엇을 말하는지 정답과 직접 대조하고, 끝으로 또 다른 비지도학습인 연관규칙까지 본다.
  모든 수치는 sklearn으로 직접 돌린 결과이며 <code>random_state=42</code>로 재현 가능하다.</p>
  <div class="meta-row">
    <span><strong>날짜</strong>2026-06-05</span>
    <span><strong>Python</strong>@@PY@@ · scikit-learn 1.8.0 · NumPy 2.4.4 · Pandas 3.0.2</span>
    <span><strong>OS</strong>Windows 11 Pro 25H2</span>
    <span><strong>IDE</strong>VS Code 1.117.0</span>
    <span><strong>HW</strong>Asrock x600 · Ryzen 8600G · 24GB LPDDR5 · RTX 4070 Super 12GB</span>
    <span><strong>커리큘럼</strong>교과목 2 · 단원 2 · 머신러닝 Day7 — 머신러닝_비지도학습알고리즘.pdf</span>
  </div>
</header>

<main>
<nav class="flow">
  <h2>이 글의 흐름 — '정답을 가린다'에서 갈라져 나온 질문들</h2>
  <ol>
    <li><a href="#ch1">시작 — 정답 <code>y</code>를 가리면 무엇이 남나 (지도 vs 비지도)</a></li>
    <li><a href="#ch2">k-means의 동작 — 중심을 정하고, 모으고, 다시 계산(반복)</a></li>
    <li><a href="#ch3">k는 몇 개? — 엘보우(inertia 꺾임)로 후보를 찾다</a></li>
    <li><a href="#ch4"><span class="turn">예상과 다른 결과</span> — 실루엣도 3이 아니라 2를 가리켰다</a></li>
    <li><a href="#ch5">그렇다면 정답과 얼마나 맞나 — 군집을 품종과 대조(ARI)</a></li>
    <li><a href="#ch6">어디서 갈렸나 — 2D로 내려 군집과 품종을 나란히 보다</a></li>
    <li><a href="#ch7">컴퓨터는 첫 중심점을 어떻게 잡나 — random vs k-means++</a></li>
    <li><a href="#ch8">다른 비지도 — 연관규칙(지지도·신뢰도·향상도)</a></li>
    <li><a href="#ch9">lift를 손으로 — 왜 10%여야 하는데 15%나 같이 샀나</a></li>
    <li><a href="#ch10">신뢰도가 낮은데 왜 의미가 있나 — confidence vs lift</a></li>
    <li><a href="#ch11">∪로 쓰는데 왜 의미는 ∩인가 — 그리고 왜 규칙 '집합'인가</a></li>
    <li><a href="#ch12">정리 — 지도 vs 비지도, 그리고 '정답이 없다'의 의미</a></li>
  </ol>
</nav>

<!-- ===================== CH 01 ===================== -->
<section id="ch1">
  <h2 class="chap"><span class="num">CH 01</span>시작 — 정답 y를 가리면 무엇이 남나<a href="#ch1" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>지난 며칠은 늘 <code>model.fit(X, y)</code>였다. 회귀는 연속값 <code>y</code>, 분류는 라벨 <code>y</code>를 보며
  "정답에 가깝게" 파라미터를 정했다. 그런데 현실의 데이터에는 정답이 붙어 있지 않은 경우가 더 많다.
  고객 거래 로그, 센서 신호, 문서 더미 — 누가 일일이 라벨을 달아 주지 않는다.
  <strong>비지도학습</strong>은 그 상황을 다룬다. 정답 <code>y</code> 없이 <code>X</code>의 구조만으로 데이터를 묶거나(군집),
  함께 나타나는 패턴을 찾는다(연관규칙).</p>

  <h3 class="step">의문</h3>
  <div class="qbox">
    <span class="label">Q</span>
    iris는 원래 정답(3품종)이 있는 데이터다. 그 <code>y</code>를 일부러 가려 보자.
    <strong>남는 것은 무엇이고, 정답 없이 무엇을 할 수 있을까?</strong> 이 질문이 오늘 글 전체의 출발점이다.
  </div>
  <p>iris의 <code>target</code>을 치우고 <code>data</code>만 남기면, 손에 쥔 것은 점 150개의 4차원 좌표뿐이다.
  "이게 몇 종인지"조차 모른다. 그렇다면 좌표만으로 — 가까운 점끼리 묶을 수 있을까?</p>

  <h3 class="step">테스트 — y를 가리고 X만 남긴다</h3>
  <div class="terminal">
    <div class="terminal-header">unsupervised_runner.py §00 · load_iris — y 제거 후 남는 것 확인 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_00@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT</span>
    정답을 가리면 남는 것은 <code>X</code> 좌표뿐이다. 비지도학습의 첫 질문은 "<strong>가까운 점끼리 묶을 수 있는가</strong>"다.
    가장 단순한 답이 k-means — "중심을 정하고, 가까운 점을 그 중심에 모은다". 그런데 중심을 어떻게 정하지?
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 중심을 모르는데 점을 모으고, 점을 모아야 중심을 알 수 있다.
    닭이 먼저냐 달걀이 먼저냐다. k-means는 이 순환을 어떻게 푸는가?
  </div>
</section>

<!-- ===================== CH 02 ===================== -->
<section id="ch2">
  <h2 class="chap"><span class="num">CH 02</span>k-means의 동작 — 중심·할당·재계산의 반복<a href="#ch2" class="anchor-link">#</a></h2>

  <h3 class="step">학습 → 가설</h3>
  <p>k-means는 순환을 <strong>반복</strong>으로 푼다. ① 중심 k개를 아무 데나 찍고 → ② 각 점을 가장 가까운 중심에 할당 →
  ③ 할당된 점들의 평균으로 중심을 다시 계산 → ②③을 중심이 거의 안 움직일 때까지 반복. 이때 줄여 나가는 양이
  <strong>inertia</strong>(각 점에서 자기 중심까지 거리의 제곱합)다.</p>
  <div class="qbox">
    <span class="label">가설</span>
    iris를 표준화한 뒤 <code>KMeans(k=3)</code>를 돌리면 ① 중심 3개(4차원)가 나오고,
    ② 150개 점이 세 군집으로 갈리며, ③ 몇 번의 반복만에 수렴할 것이다(<code>n_iter_</code>가 작다).
  </div>

  <blockquote class="cite">
    "The KMeans algorithm clusters data by trying to separate samples in n groups of equal variance,
    minimizing a criterion known as the inertia or within-cluster sum-of-squares."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/clustering.html#k-means" target="_blank" rel="noopener">Clustering · K-means</a></span>
  </blockquote>

  <pre><code class="language-python"># path : .study/test/unsupervised/unsupervised_runner.py §01 (발췌)
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

X = StandardScaler().fit_transform(load_iris().data)   # 표준화(거리 기반이라 필수)
km = KMeans(n_clusters=3, random_state=42, n_init=10).fit(X)
print(km.cluster_centers_.shape)   # 중심 3개 × 4특성
print(km.n_iter_)                  # 수렴까지 반복 횟수
print(km.inertia_)                 # 군집 내 거리 제곱합</code></pre>

  <h3 class="step">테스트</h3>
  <div class="terminal">
    <div class="terminal-header">unsupervised_runner.py §01 · KMeans(k=3) — 중심·할당·반복 수·inertia · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_01@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">가설 통과</span>
    중심 3개(3×4), 군집 크기 53·50·47, 단 <strong>4번</strong> 반복만에 수렴(<code>n_iter_=4</code>), inertia 139.82.
    실제 품종은 50·50·50인데 군집은 53·50·47로 비슷하게 차이가 났다 — 그럴듯하다.
    그런데 여기엔 함정이 있다. <strong>나는 답이 3개인 걸 알아서 <code>k=3</code>을 넣었다.</strong> 정답을 모른다면?
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 비지도학습의 본질은 "정답을 모른다"는 것이다.
    그렇다면 <code>k</code>는 누가 정하나? 데이터 스스로 적정 <code>k</code>를 말해 주는 신호가 있어야 한다.
  </div>
</section>

<!-- ===================== CH 03 ===================== -->
<section id="ch3">
  <h2 class="chap"><span class="num">CH 03</span>k는 몇 개? — 엘보우로 후보를 찾다<a href="#ch3" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    <code>k</code>를 키울수록 군집은 잘게 쪼개져 inertia는 무조건 줄어든다(k=점 개수면 0). 하지만 "진짜 군집 수"를 넘어서면
    줄어드는 폭이 확 꺾일 것이다. 그 <strong>꺾이는 지점(엘보우)</strong>이 적정 <code>k</code> 후보다. iris라면 3에서 꺾여야 한다.
  </div>
  <p><code>k=1..8</code>로 inertia를 재고, 감소폭(Δ)이 어디서 급격히 작아지는지 본다.</p>

  <h3 class="step">테스트</h3>
  <div class="terminal">
    <div class="terminal-header">unsupervised_runner.py §02 · KMeans k=1..8 — inertia 감소폭으로 엘보우 추정 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_02@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_ELBOW@@" alt="k에 따른 inertia 엘보우 곡선">
    <figcaption>그림 0605-1 · k=2에서 감소폭이 377→83으로 급감 — 곡선의 팔꿈치가 k=2에 잡힌다</figcaption>
  </figure>

  <h3 class="step">관찰 — 3이 아니라 2에서 꺾였다</h3>
  <div class="keypoint">
    <span class="label">예상 밖</span>
    감소폭은 k=2에서 377.64, k=3에서 82.54, k=4에서 25.73. 가장 크게 꺾이는 곳은 <strong>k=3이 아니라 k=2</strong>다
    (2차 차분 최대도 k=2). 정답이 3종인 걸 알면서도, 데이터가 말하는 "가장 또렷한 분리"는 두 덩어리였다.
    엘보우 하나로는 미심쩍다 — 다른 기준으로 교차 확인해야 한다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 엘보우는 곡선을 눈으로 읽는 방법이라 주관적이다.
    분리 정도를 숫자 하나로 주는 객관적 지표가 있을까? 실루엣 점수다. 그건 3을 가리켜 줄까?
  </div>
</section>

<!-- ===================== CH 04 ===================== -->
<section id="ch4">
  <h2 class="chap"><span class="num">CH 04</span>예상과 다른 결과 — 실루엣도 2를 가리켰다<a href="#ch4" class="anchor-link">#</a></h2>

  <h3 class="step">학습 → 가설</h3>
  <p><strong>실루엣 점수</strong>는 각 점에 대해 "자기 군집 안 평균 거리(a)"와 "가장 가까운 다른 군집까지 평균 거리(b)"를 비교해
  <code>(b−a)/max(a,b)</code>로 잰다. +1에 가까우면 잘 뭉치고 잘 떨어진 것, 0이면 경계에 걸친 것이다.</p>
  <div class="qbox">
    <span class="label">가설</span>
    iris의 진짜 군집이 3개라면 <code>k=3</code>에서 평균 실루엣이 최댓값이어야 한다. <code>k=2..8</code>로 재서 확인한다.
  </div>

  <blockquote class="cite">
    "The Silhouette Coefficient is calculated using the mean intra-cluster distance (a) and
    the mean nearest-cluster distance (b) for each sample … The best value is 1 and the worst value is -1."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/generated/sklearn.metrics.silhouette_score.html" target="_blank" rel="noopener">silhouette_score</a></span>
  </blockquote>

  <h3 class="step">테스트</h3>
  <div class="terminal">
    <div class="terminal-header">unsupervised_runner.py §03 · silhouette_score k=2..8 — 최댓값 k 확인 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_03@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_SIL@@" alt="k에 따른 평균 실루엣 점수">
    <figcaption>그림 0605-2 · 평균 실루엣은 k=2에서 0.582로 최고, k=3은 0.460 — 두 지표가 같은 답(2)을 가리킨다</figcaption>
  </figure>

  <h3 class="step">관찰 — 가설이 성립하지 않았다, 그런데 그게 정보다</h3>
  <div class="keypoint">
    <span class="label">FAILURE → CLUE</span>
    실루엣 최댓값은 k=2(0.5818)이고 k=3은 0.4599로 더 낮다. 엘보우와 실루엣이 <strong>나란히 2를 가리켰다</strong>.
    "iris는 3종이니 k=3"이라는 내 가설이 맞지 않은 것이다. 하지만 이건 오류가 아니라 신호다 —
    데이터 좌표 위에서는 <strong>두 덩어리(한 종 + 나머지 두 종이 붙은 덩어리)</strong>가 세 덩어리보다 더 또렷하게 분리된다는 뜻이다.
    그렇다면 k=3으로 묶었을 때, 실제 품종과는 정확히 어디서 어긋날까?
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 지표가 2를 권해도, 우리는 정답(3종)을 안다.
    k=3 군집을 실제 품종과 직접 대조하면, 실루엣이 왜 k=2를 더 선호했는지가 숫자로 드러날 것이다.
  </div>
</section>

<!-- ===================== CH 05 ===================== -->
<section id="ch5">
  <h2 class="chap"><span class="num">CH 05</span>정답과 얼마나 맞나 — 군집 vs 품종(ARI)<a href="#ch5" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    군집 번호(0·1·2)와 품종 번호는 의미가 다르다(비지도라 라벨이 임의다). 그래서 정확도를 바로 못 쓴다.
    교차표로 대응을 보고, 라벨 순서에 무관한 <strong>ARI</strong>로 일치도를 재면 — setosa는 완벽히, versicolor·virginica는
    일부 섞여 ARI가 1보다 꽤 낮게 나올 것이다.
  </div>
  <p><code>pd.crosstab</code>으로 품종×군집을 보고, <code>adjusted_rand_score</code>·<code>normalized_mutual_info_score</code>로 잰다.</p>

  <blockquote class="cite">
    "The Rand Index … is adjusted for chance … ARI is 1.0 for a perfect match and close to 0.0 for random labelings,
    regardless of the number of clusters and samples."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/clustering.html#rand-index" target="_blank" rel="noopener">Clustering · Rand index</a></span>
  </blockquote>

  <h3 class="step">테스트</h3>
  <div class="terminal">
    <div class="terminal-header">unsupervised_runner.py §04 · crosstab · ARI · NMI — 군집을 실제 품종과 대조 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_04@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">가설 통과 — 어긋남의 원인</span>
    교차표가 답을 보여 준다. setosa 50개는 한 군집(클러스터 1)에 <strong>완벽히</strong> 모였다.
    하지만 versicolor는 39/11, virginica는 14/36으로 두 군집에 섞였다 — 둘이 좌표상 겹치기 때문이다.
    그래서 ARI=0.6201, NMI=0.6595, 다수결 매핑 정확도 0.833(125/150). 정답을 한 번도 안 보고도 이만큼 맞춘다.
    그리고 CH 04의 수수께끼가 풀린다 — <strong>versicolor·virginica가 한 덩어리로 붙어 있어 k=2가 더 또렷했던 것</strong>이다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 숫자로는 "섞였다"까지 봤다. 그런데 정확히 공간의 어디서 섞였나?
    4차원은 못 그리니, 2차원으로 내려 군집과 품종을 나란히 눈으로 본다.
  </div>
</section>

<!-- ===================== CH 06 ===================== -->
<section id="ch6">
  <h2 class="chap"><span class="num">CH 06</span>어디서 갈렸나 — 2D 산점도<a href="#ch6" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 관찰</h3>
  <div class="qbox">
    <span class="label">의문</span>
    특성이 4개라 그대로는 그릴 수 없다. PCA로 분산이 가장 큰 두 축(PC1·PC2)에 투영해 2D로 내리면,
    k-means 군집과 실제 품종이 <strong>어느 경계에서 갈라지는지</strong> 눈으로 확인할 수 있을까?
  </div>
  <p>PCA 2D가 원래 분산을 얼마나 보존하는지부터 확인하고, 같은 좌표 위에 군집과 품종을 나란히 찍는다.</p>

  <h3 class="step">테스트</h3>
  <div class="terminal">
    <div class="terminal-header">unsupervised_runner.py §05 · PCA(2) + KMeans 산점도 — 설명 분산 비율 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_05@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_SCATTER@@" alt="PCA 2D 위 k-means 군집과 실제 품종 비교 산점도">
    <figcaption>그림 0605-3 · 왼쪽=k-means 군집(정답 안 봄), 오른쪽=실제 품종 — 왼쪽 아래 한 덩어리(setosa)는 완벽, 오른쪽 두 덩어리 경계가 흐릿하다</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">관찰 결과</span>
    PC1·PC2 두 축이 원래 분산의 95.8%(0.7296+0.2285)를 담는다 — 2D 그림을 믿어도 된다.
    그림에서 setosa는 멀리 떨어진 한 덩어리라 누구나 갈라낸다. 반면 versicolor·virginica는 가운데서 맞닿아 있어
    k-means가 직선 경계로 자르며 일부를 반대편에 넘긴다. <strong>CH 05의 39/11·14/36이 바로 이 경계의 점들</strong>이다.
    "군집 = 품종"이 아니라 "군집 = 좌표상 가까운 무리"임을 그림이 다시 못 박는다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 여기까지 k-means를 믿고 썼는데, 한 가지를 건너뛰었다.
    CH 02에서 "중심 k개를 아무 데나 찍고"라고 했지만, 그 "아무 데나"가 결과를 바꾸지는 않나?
    실제 컴퓨터는 첫 중심점을 어떻게 잡는지부터 확인한다.
  </div>
</section>

<!-- ===================== CH 07 (k-means 초기화) ===================== -->
<section id="ch7">
  <h2 class="chap"><span class="num">CH 07</span>컴퓨터는 첫 중심점을 어떻게 잡나 — random vs k-means++<a href="#ch7" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 가설</h3>
  <p>교재 예제는 "초기 중심점1을 (1,1), 중심점2를 (8,8)로 가정하자"처럼 사람이 손으로 시작점을 찍어 준다.
  하지만 실제 sklearn은 사람이 안 찍어도 알아서 시작한다. 그 시작점을 어떻게 정하느냐가 문제다 —
  k-means는 중심을 옮겨 가며 inertia를 줄이는데, 시작 위치가 나쁘면 더 못 줄인 채 멈추는
  <strong>국소 최솟값(local minimum)</strong>에 갇힐 수 있다.</p>
  <div class="qbox">
    <span class="label">가설</span>
    가장 단순한 시작은 데이터 점 중 k개를 <strong>무작위(random)</strong>로 고르는 것이다.
    이건 운이 나쁘면 두 시작점이 한쪽에 몰려 나쁜 군집에서 멈춘다.
    <code>k-means++</code>는 "이미 고른 중심에서 먼 점일수록 다음 중심으로 뽑힐 확률을 높여" 시작점을 퍼뜨린다.
    같은 데이터에 초기화를 한 번만(<code>n_init=1</code>) 주고 시드 10개씩 돌리면,
    k-means++ 쪽이 나쁜 국소 최솟값에 갇히는 빈도가 더 낮을 것이다.
  </div>

  <blockquote class="cite">
    "‘k-means++’ … selects initial cluster centroids using sampling based on an empirical probability
    distribution of the points' contribution to the overall inertia. This technique speeds up convergence."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html" target="_blank" rel="noopener">KMeans · init</a></span>
  </blockquote>

  <pre><code class="language-python"># path : .study/test/unsupervised/unsupervised_runner.py §09 (발췌)
for s in range(10):
    # 초기화 효과만 보려고 n_init=1 (sklearn 기본은 10번 시도 후 최선 선택)
    km_r = KMeans(n_clusters=3, init="random",    n_init=1, random_state=s).fit(X)
    km_p = KMeans(n_clusters=3, init="k-means++", n_init=1, random_state=s).fit(X)
    print(km_r.inertia_, km_p.inertia_)   # 시드별 수렴 inertia 비교</code></pre>

  <h3 class="step">테스트</h3>
  <div class="terminal">
    <div class="terminal-header">unsupervised_runner.py §09 · KMeans init=random vs k-means++ — 시드별 수렴 inertia · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_09@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_INIT@@" alt="초기화 방식별 시드별 수렴 inertia 비교">
    <figcaption>그림 0605-5 · 시드별 수렴 inertia — 점선이 최선값(139.82). random은 한 시드(s=5)에서 191.0으로 크게 튀었다</figcaption>
  </figure>

  <h3 class="step">관찰 — iris에선 차이가 작지만, 갇히는 자리는 분명히 있다</h3>
  <div class="keypoint">
    <span class="label">관찰 결과</span>
    평균 inertia는 random 145.47, k-means++ 145.44로 거의 같았다. iris는 군집이 또렷해 초기화에 덜 민감한 편이다.
    그래도 random은 시드 5에서 191.0으로 한 번 크게 튀어 나쁜 자리에 갇혔다.
    191.0이라는 같은 국소 최솟값은 k-means++ 쪽에서도 시드 9에 한 번 나타났다 —
    <strong>초기화를 한 번만 주면 어느 방식이든 나쁜 자리에 갇힐 수 있다</strong>는 뜻이다.
    그래서 sklearn 기본값은 init='k-means++'에 더해 <code>n_init</code>으로 여러 번 시작해 그중 최선을 고른다(CH 02의 n_init=10).
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — k-means는 "점을 묶는" 비지도학습이었다.
    비지도학습엔 다른 결도 있다 — "함께 나타나는 것을 묶는" 일. 장바구니에서 'A를 사면 B도 산다'를 찾는 연관규칙이다.
  </div>
</section>

<!-- ===================== CH 08 (연관규칙) ===================== -->
<section id="ch8">
  <h2 class="chap"><span class="num">CH 08</span>다른 비지도 — 연관규칙(장바구니 분석)<a href="#ch8" class="anchor-link">#</a></h2>

  <h3 class="step">학습 → 가설</h3>
  <p>연관규칙은 거래 묶음에서 <code>A → B</code> 형태의 규칙을 찾는다. 세 숫자로 판단한다 —
  <strong>지지도(support)</strong>: 전체 거래 중 A·B가 함께 든 비율, <strong>신뢰도(confidence)</strong>:
  A를 산 거래 중 B도 산 비율(<code>support(A∪B)/support(A)</code>), <strong>향상도(lift)</strong>:
  신뢰도를 B의 기본 지지도로 나눈 값(<code>confidence/support(B)</code>). lift&gt;1이면 "A가 B 구매 확률을 우연 이상으로 높인다"는 뜻이다.</p>
  <div class="qbox">
    <span class="label">가설</span>
    작은 거래 10건에 apriori(빈발 itemset → 규칙)를 직접 돌리면, "기저귀↔맥주"처럼 함께 잘 사는 조합이
    <strong>lift&gt;1</strong>로 또렷이 드러날 것이다. (mlxtend 미설치라 직접 구현)
  </div>

  <blockquote class="cite">
    "Lift … is the ratio of the observed support to that expected if the two rules were independent.
    A lift value greater than 1 indicates that the two items occur together more often than expected by chance."
    <span class="src">— scikit-learn 외부 라이브러리 · <a href="https://rasbt.github.io/mlxtend/user_guide/frequent_patterns/association_rules/" target="_blank" rel="noopener">mlxtend · association_rules (lift 정의)</a></span>
  </blockquote>

  <h3 class="step">테스트</h3>
  <div class="terminal">
    <div class="terminal-header">unsupervised_runner.py §06 · apriori 직접 구현 — support·confidence·lift 계산 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_06@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_RULES@@" alt="연관규칙별 향상도 막대그래프">
    <figcaption>그림 0605-4 · 규칙별 향상도 — 점선(lift=1)=우연. {기저귀}→{맥주} 등 상위 규칙이 lift 2.0으로 우뚝하다</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">가설 통과</span>
    최고 향상도 규칙은 <code>{기저귀} → {맥주}</code>로 support 0.40·confidence 0.80·<strong>lift 2.00</strong>.
    역방향 <code>{맥주} → {기저귀}</code>는 confidence 1.00(맥주 산 거래는 전부 기저귀도 샀다)·lift 2.00이다.
    반대로 <code>{우유} → {빵}</code>은 lift 0.95로 1보다 작다 — 빵은 워낙 자주 팔려서(support 0.70)
    우유를 산다고 빵 구매가 더 늘진 않는다. <strong>신뢰도만 보면 속고, lift로 우연을 걸러야 한다.</strong>
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 표가 lift 0.95, 2.00 같은 숫자를 뱉었지만, 그 숫자가 "왜" 그렇게 나오는지는
    아직 손으로 따라가 보지 않았다. 작은 거래 한 묶음에 support·confidence·lift를 직접 세어 보면,
    "왜 10%여야 정상인데 15%나 같이 샀나"라는 질문에 숫자로 답할 수 있다.
  </div>
</section>

<!-- ===================== CH 09 (lift 손계산) ===================== -->
<section id="ch9">
  <h2 class="chap"><span class="num">CH 09</span>lift를 손으로 — 왜 10%여야 하는데 15%나 같이 샀나<a href="#ch9" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">의문</span>
    lift가 1보다 크다는 게 직관적으로 와닿지 않는다. 우유를 50% 거래에서, 요거트를 20% 거래에서 산다고 하자.
    두 상품이 아무 상관이 없다면, 우연히 한 바구니에 같이 담길 확률은 <code>0.5 × 0.2 = 0.1</code>,
    즉 <strong>10%면 정상</strong>이다. 그런데 실제로 15%가 같이 샀다면 — 그 5%p는 어디서 왔나?
  </div>
  <p>이 질문에 답하려면 lift의 분자·분모를 직접 세어 봐야 한다.
  lift = 실제 동시구매율 / 기대(독립) 동시구매율 = <code>P(A∩B) / (P(A)·P(B))</code>.
  거래 20건을 직접 만들어(우유 10건·요거트 4건·둘 다 3건) 손으로 센다.</p>

  <h3 class="step">테스트</h3>
  <div class="terminal">
    <div class="terminal-header">unsupervised_runner.py §08 · support·confidence·lift 손계산 — 기대(독립) vs 실제 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_08@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_LIFT_HAND@@" alt="우유→요거트 기대 동시구매율과 실제 동시구매율 막대 비교">
    <figcaption>그림 0605-6 · 왼쪽=상관 없다면 나와야 할 기대 0.10, 오른쪽=실제 0.15 — 그 비율 1.50이 lift다</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">관찰 결과</span>
    P(우유)=0.50, P(요거트)=0.20이니 둘이 무관하면 기대 동시구매율은 0.10이다. 실제는 0.15였다.
    lift = 0.15 / 0.10 = <strong>1.50</strong>. "상관 없다면 10%만 나와야 하는데 15%나 같이 샀다"는 말이
    곧 "기대보다 1.5배"라는 뜻이다. lift의 분모가 바로 "아무 상관 없을 때의 우연 확률(독립 기대치)"이고,
    분자가 실제 데이터에 찍힌 동시구매율이다. lift=1이면 우연과 같고, 1보다 크면 기대를 넘어 함께 산 것이다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — lift가 "실제/기대"임을 봤다. 그런데 같은 결과를 confidence로 보면
    숫자가 작아 헷갈리는 경우가 있다. 신뢰도가 10%밖에 안 되는 규칙이 왜 버려지지 않고 의미를 가질까?
  </div>
</section>

<!-- ===================== CH 10 (confidence vs lift) ===================== -->
<section id="ch10">
  <h2 class="chap"><span class="num">CH 10</span>신뢰도가 낮은데 왜 의미가 있나 — confidence vs lift<a href="#ch10" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">의문</span>
    어떤 규칙은 confidence가 10%다. "조건(A)을 만족한 사람 중 고작 10%만 B를 샀다"는 뜻인데,
    그런 규칙이 왜 의미가 있다고 할까? 10%면 버려야 하는 것 아닌가?
  </div>
  <p>핵심은 confidence를 혼자 보면 안 되고 결과 상품 B의 단독 지지도 P(B)와 함께 봐야 한다는 점이다.
  <code>lift = confidence / P(B)</code>이므로, B가 원래 아주 드물게 팔리는 상품(P(B)가 작음)이면
  confidence가 낮아도 lift는 커진다. 만두(자주 팔림)→굴소스(드물게 팔림) 거래로 확인한다.
  <em>이 §08 출력의 둘째 블록이 그 계산이다.</em></p>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">관찰 결과</span>
    만두→굴소스의 confidence는 0.10(10%)으로 낮다. 그런데 굴소스 단독 지지도 P(굴소스)=0.042로 워낙 작다.
    lift = 0.10 / 0.042 = <strong>2.40</strong>. "조건 만족한 사람 중 10%만 샀다"는 사실은,
    굴소스가 원래 4%만 팔리던 희귀 상품임을 감안하면 "기대보다 2.4배 더 샀다"가 된다.
    confidence는 절대 비율이라 인기 없는 상품끼리의 끈끈한 관계를 놓친다.
    lift는 그 P(B)를 분모로 깔아 "기저 확률 대비 얼마나 끌어올렸나"를 본다 — 그래서 둘을 같이 본다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — support·confidence·lift를 손으로 다 따라갔다. 마지막으로 표기 하나가 남았다.
    공식에 <code>support(A∪B)</code>처럼 합집합(∪) 기호가 나오는데, 실제로 세는 건 "둘 다 산" 교집합이다.
    왜 ∪로 쓰고 ∩으로 세나? 그리고 왜 결과를 규칙이 아니라 규칙 '집합'이라 부르나?
  </div>
</section>

<!-- ===================== CH 11 (집합 표기) ===================== -->
<section id="ch11">
  <h2 class="chap"><span class="num">CH 11</span>∪로 쓰는데 왜 의미는 ∩인가 — 그리고 왜 규칙 '집합'인가<a href="#ch11" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 정리</h3>
  <div class="qbox">
    <span class="label">의문</span>
    confidence 공식은 <code>support(A∪B) / support(A)</code>로 적는다. 합집합(∪)이라면 "A 또는 B를 산 거래"여야 할 것 같은데,
    실제로 세는 건 "A와 B를 <strong>둘 다</strong> 산 거래" — 교집합(∩)이다. 왜 기호와 의미가 어긋나 보일까?
  </div>
  <p>어긋난 게 아니라 두 관점이 한 식에 겹쳐 있다. ∪는 <strong>아이템 관점</strong>,
  ∩은 <strong>거래 관점</strong>이다.</p>
  <ul>
    <li><strong>왜 ∪로 쓰나(아이템 관점)</strong> — <code>support(X)</code>의 X는 "한 바구니에 들어 있어야 할 아이템들의 집합(set)"이다.
    A={우유}와 B={요거트}를 합쳐 하나의 아이템 세트 <code>A∪B={우유,요거트}</code>를 만들고,
    "이 세트를 통째로 포함한 거래 비율"을 support로 잰다. 그래서 아이템을 합치는 ∪로 표기한다.</li>
    <li><strong>왜 ∩으로 세나(거래 관점)</strong> — 그 "세트를 통째로 포함한 거래"를 확률 언어로 옮기면,
    우유를 산 거래 집합과 요거트를 산 거래 집합이 <strong>겹치는</strong> 부분, 즉 <code>P(우유 산 거래 ∩ 요거트 산 거래)</code>다.
    아이템을 합칠수록(∪) 그걸 다 포함하는 거래는 좁아진다(∩). 기호는 아이템을 합치는 ∪, 세는 값은 거래의 교집합 ∩.</li>
  </ul>
  <p>그래서 CH 09의 손계산에서 분자를 <code>P(A∩B)</code>로 적은 것이고,
  같은 양을 빈발 itemset 공식에서는 <code>support(A∪B)</code>로 적는다 — 가리키는 거래 묶음은 동일하다.</p>

  <h3 class="step">왜 규칙이 아니라 규칙 '집합(Set)'인가</h3>
  <div class="keypoint">
    <span class="label">정리</span>
    apriori를 한 번 돌리면 규칙 하나가 아니라 수십·수백 개의 규칙이 한꺼번에 나온다.
    {기저귀}→{맥주}, {맥주}→{기저귀}, {버터}→{빵} … CH 08의 표가 그 <strong>규칙 집합</strong>이다.
    알고리즘은 "이 한 규칙이 맞나"를 푸는 게 아니라, 빈발 itemset 전체를 훑어 support·confidence·lift 기준을 통과한
    규칙을 모두 모아 집합으로 돌려준다. 그래서 결과를 규칙 하나가 아니라 규칙 집합으로 다룬다.
    표기의 ∪/∩도, '규칙 집합'도, 바탕은 같다 — 연관규칙은 처음부터 끝까지 <strong>집합(set) 위의 연산</strong>이다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — k-means(점 묶기)와 연관규칙(함께 나타나는 것 엮기)을 끝까지 따라갔다.
    이제 둘을 지도학습과 한 표로 세우고, "정답이 없다"가 평가에서 무엇을 바꾸는지로 글을 닫는다.
  </div>
</section>

<!-- ===================== CH 12 (정리) ===================== -->
<section id="ch12">
  <h2 class="chap"><span class="num">CH 12</span>정리 — 지도 vs 비지도, '정답이 없다'의 의미<a href="#ch12" class="anchor-link">#</a></h2>

  <h3 class="step">관찰 → 정리</h3>
  <p>오늘 다룬 비지도학습을 지도학습과 한 표로 세운다. 핵심 차이는 입력에 정답 <code>y</code>가 있느냐 하나지만,
  그 하나가 목표·알고리즘·<strong>평가</strong>를 전부 바꾼다.</p>
  <div class="terminal">
    <div class="terminal-header">unsupervised_runner.py §07 · 지도 vs 비지도 요약표 — 입력·목표·평가 비교 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_07@@</pre>
  </div>
  <p>가장 중요한 줄은 "평가"다. 지도학습은 정답이 있으니 R2·정확도로 바로 채점한다.
  비지도학습은 정답이 없으니 inertia·실루엣처럼 <strong>데이터 내부의 응집·분리</strong>로만 평가한다.
  오늘 ARI를 쓸 수 있었던 건 iris가 예외적으로 정답을 가진 데이터였기 때문이고, 진짜 비지도 현장에선 그 채점지가 없다.</p>

  <h3 class="step">최종 결론 — 출발 의문 회수</h3>
  <div class="keypoint">
    <span class="label">FINAL CONCLUSION</span>
    CH 01의 질문 "정답을 가리면 무엇이 남고, 무엇을 할 수 있나"의 답:
    <strong>남는 건 X 좌표뿐이고, 할 수 있는 건 가까운 것끼리 묶거나(k-means) 함께 나타나는 것을 엮는(연관규칙) 일이다.</strong>
    그 과정에서 k는 데이터가 엘보우·실루엣으로 권하되(둘 다 k=2를 권했다), 그 권고가 내가 아는 정답(3종)과 어긋날 수 있음을 봤다(CH 03~04).
    어긋남은 오류가 아니라 "versicolor·virginica가 좌표상 겹친다"는 정보였고(CH 05~06),
    첫 중심점은 random보다 k-means++로 퍼뜨려 잡되 iris에선 그 차이가 작았다(CH 07).
    연관규칙에선 신뢰도가 아니라 lift로 우연을 걸러야 했고(CH 08), lift는 "실제/기대"임을 손으로 확인했다(CH 09~11).
  </div>

  <h3 class="step">한 문장으로</h3>
  <div class="keypoint">
    <span class="label">ONE-LINER</span>
    비지도학습의 핵심은 "정답이 없다"가 아니라 — <strong>정답이 없으니, 데이터가 스스로 드러내는 구조를 읽고
    그 구조가 내 선입견(k=3)과 다를 때 데이터 쪽을 믿는 법</strong>을 배우는 일이다.
  </div>

  <div class="ref-chain">
    <p class="ref-title">📚 전체 근거 출처</p>
    <ol>
      <li><strong>공식 문서</strong>
        <a href="https://scikit-learn.org/stable/modules/clustering.html#k-means" target="_blank" rel="noopener">scikit-learn · K-means(inertia)</a>,
        <a href="https://scikit-learn.org/stable/modules/generated/sklearn.metrics.silhouette_score.html" target="_blank" rel="noopener">silhouette_score</a>,
        <a href="https://scikit-learn.org/stable/modules/clustering.html#rand-index" target="_blank" rel="noopener">Adjusted Rand Index</a>,
        <a href="https://rasbt.github.io/mlxtend/user_guide/frequent_patterns/association_rules/" target="_blank" rel="noopener">mlxtend · association rules(lift)</a>.</li>
      <li><strong>workspace</strong>
        <code>../ml_workspace/from_colab/0605-s/uci_iris_torch_kmeans_clustering_colab.ipynb</code>(k-means·실루엣·ARI 흐름),
        <code>torch_association_rules.ipynb</code>(지지도·신뢰도·향상도 정의).</li>
      <li><strong>강의자료</strong>
        <code>.study/pdf/머신러닝_비지도학습알고리즘.pdf</code> (배경지식).</li>
      <li><strong>실행 검증</strong>
        <code>.study/test/unsupervised/unsupervised_runner.py §00~§09</code>
        → <code>logs/*.txt</code>, <code>charts/*.png</code> (고정 시드 42, 재현 가능).</li>
    </ol>
  </div>

  <div class="bridge">
    <strong>다음 글 예고</strong> — 0605-s의 PyTorch 직접 구현(<code>torch.cdist</code>로 거리 계산, GPU 텐서 k-means)과
    online-retail 대규모 거래의 apriori 최적화(X·Xᵀ 행렬곱으로 쌍 카운트)는 의문과 시행착오가 많아 별도 실습 기록으로 정리한다.
  </div>
</section>
</main>

<footer>
  <p>SK 네트웍스 AI Family 32기 · 교과목 2 단원 2 머신러닝 Day7 (2026-06-05)</p>
  <p>모든 터미널 출력은 <code>.study/test/unsupervised/unsupervised_runner.py</code> 실제 실행 결과이며,
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

# ── orphan pre 정리(§5⑦) ──
import re as _re
HTML = _re.sub(r'  </div>\n    <pre class="terminal-body">.*?</pre>\n  </div>', '  </div>', HTML, flags=_re.DOTALL)
HTML = _re.sub(r'  </div>\n<pre class="terminal-body">.*?</pre>\n  </div>', '  </div>', HTML, flags=_re.DOTALL)

OUT.write_text(HTML, encoding="utf-8")

# ── 검증(§12) ──
n_term = HTML.count('<div class="terminal">')
n_body = HTML.count('class="terminal-body"')
http_imgs = re.findall(r'<img[^>]+src="https?://', HTML)
b64_imgs = HTML.count('src="data:image/')
leftover = re.findall(r'@@[A-Z0-9_]+@@', HTML)
zwsp = HTML.count('​')
print(f"파일: {OUT}")
print(f"terminal div: {n_term} | terminal-body: {n_body} | (일치={n_term==n_body})")
print(f"외부 URL img: {len(http_imgs)} (0이어야 함) | base64 img: {b64_imgs}")
print(f"chap: {HTML.count('h2 class=\"chap\"')} | qbox: {HTML.count('class=\"qbox\"')} | keypoint: {HTML.count('class=\"keypoint\"')}")
print(f"zero-width space: {zwsp} | 미치환 placeholder: {leftover} | 크기: {len(HTML)//1024} KB")
