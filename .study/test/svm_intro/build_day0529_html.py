# build_day0529_html.py
# day0529_svm.html 조립 — logs/*.txt(실제 실행 결과) + charts/*.png(base64) 주입
# 실행: c:\_proj\python_workspace\.venv\Scripts\python.exe build_day0529_html.py
#   (= GUIDE §11 run_all 역할: 터미널 값 직접 작성 금지, 로그에서 주입)
#   문체: interpreter_base64.html / day0527·day0528 의 "의문→해결→새 의문" 서사 추적 방식.
import base64, html, pathlib, re

HERE = pathlib.Path(__file__).parent
LOGS = HERE / "logs"
CHARTS = HERE / "charts"
OUT = HERE.parent.parent / "blog" / "day0529_svm.html"   # .study/blog/
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
    "@@TERM_01@@": term("01_margin_support_vectors"),
    "@@TERM_02@@": term("02_why_max_margin"),
    "@@TERM_03@@": term("03_kernel_moons"),
    "@@TERM_04@@": term("04_circles"),
    "@@TERM_05@@": term("05_C_gamma_overfit"),
    "@@TERM_06@@": term("06_boundary_compare"),
    "@@CHART_MARGIN@@": chart("ch_margin.png"),
    "@@CHART_KERNEL@@": chart("ch_kernel.png"),
    "@@CHART_CGAMMA@@": chart("ch_cgamma.png"),
    "@@CHART_COMPARE@@": chart("ch_compare.png"),
}

HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>파이썬 머신러닝 분석: 가장 좋은 분류 경계란 무엇인가 — 마진·서포트 벡터·커널</title>
  <meta name="description" content="SK 네트웍스 AI Family 32기 머신러닝 Day3. '분류 경계를 가장 좋게 긋는다는 건 뭔가', '왜 가장 넓은 도로가 가장 안전한가', '직선으로 안 갈리는 데이터는 어쩌나'라는 의문을 따라 서포트 벡터 머신(SVM)의 마진 최대화·서포트 벡터·RBF 커널 트릭·C/gamma 과대적합을 sklearn 실행으로 검증한 기록.">
  <meta property="og:title" content="파이썬 머신러닝 분석: 가장 좋은 분류 경계란 무엇인가">
  <meta property="og:description" content="마진 최대화 → 서포트 벡터 → 커널 트릭(moons·circles) → C/gamma 과대적합 → 분류기 경계 비교, 실측으로 추적">
  <meta property="og:type" content="article">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="파이썬 머신러닝 분석: 가장 좋은 분류 경계란 무엇인가">
  <meta name="twitter:description" content="SVM 구조 — 마진·서포트 벡터·RBF 커널·C/gamma 과대적합을 sklearn 으로 추적">
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
  <p class="eyebrow">Python · 머신러닝(교과목 2 · 단원 2) Day3 · 부트캠프</p>
  <h1>가장 좋은 분류 경계란 무엇인가 — 마진·서포트 벡터·커널</h1>
  <p class="deck">분류기는 결국 두 무리 사이에 선을 하나 긋는다. 그런데 같은 데이터를 가르는 선은 무수히 많다.
  그중 <strong>'가장 좋은' 경계</strong>란 대체 무엇이고, 무엇이 그것을 정할까?
  이 글은 그 한 질문에서 출발해 — 가장 넓은 도로(마진)를 찾는 일,
  그 도로를 떠받치는 소수의 점(서포트 벡터), 직선으로 안 갈리는 데이터를 휘는 커널,
  그리고 경계를 너무 데이터에 붙였을 때의 하락까지 따라간 기록이다.
  모든 수치는 sklearn 으로 직접 돌린 결과이며 <code>random_state=42</code> 로 재현 가능하다.</p>
  <div class="meta-row">
    <span><strong>날짜</strong>2026-05-29</span>
    <span><strong>Python</strong>@@PY@@ · scikit-learn 1.8.0 · NumPy 2.4.4 · Pandas 3.0.2</span>
    <span><strong>OS</strong>Windows 11 Pro 25H2</span>
    <span><strong>IDE</strong>VS Code 1.117.0</span>
    <span><strong>HW</strong>Asrock x600 · Ryzen 8600G · 24GB LPDDR5 · RTX 4070 Super 12GB</span>
    <span><strong>커리큘럼</strong>교과목 2 · 단원 2 · 머신러닝 Day3 — 머신러닝_서포트백터머신구조.pdf</span>
  </div>
</header>

<main>
<nav class="flow">
  <h2>이 글의 흐름 — '가장 좋은 경계'라는 한 질문에서 갈라진 길</h2>
  <ol>
    <li><a href="#ch1">시작 — 같은 데이터를 가르는 선은 무수히 많다, 그중 무엇이 '가장 좋은' 경계인가</a></li>
    <li><a href="#ch2">마진 최대화 — 왜 '가장 넓은 도로'의 한가운데가 가장 안전한가</a></li>
    <li><a href="#ch3">서포트 벡터 — 경계를 정하는 건 단 몇 개의 점, 나머지는?</a></li>
    <li><a href="#ch4"><span class="turn">막힘</span> — 직선으로 도저히 안 갈리는 데이터를 만나다(커널 트릭)</a></li>
    <li><a href="#ch5">한 발 더 — RBF 가 정말 일반적인가, 동심원으로 한 번 더</a></li>
    <li><a href="#ch6"><span class="turn">예상과 다른 결과</span> — C·gamma 를 키웠더니 경계가 데이터에 달라붙어 크게 낮아졌다</a></li>
    <li><a href="#ch7">비교 — 로지스틱·KNN·SVM 의 경계 모양은 왜 다른가</a></li>
    <li><a href="#ch8">정리 — '가장 좋은 경계'의 답과 SVM 구조 한 문장</a></li>
  </ol>
</nav>

<!-- ===================== CH 01 ===================== -->
<section id="ch1">
  <h2 class="chap"><span class="num">CH 01</span>시작 — 무수히 많은 선 중 무엇이 '가장 좋은' 경계인가<a href="#ch1" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>오늘 실습은 우편번호·글자 이미지를 SVM 으로 분류하는 것이었다(<code>pytorch_svm_letter_classification.ipynb</code>).
  코드 주석은 SVM 을 이렇게 정의했다 — "각 클래스 사이에 한 직선(초평면, hyperplane)을 그어 데이터를 가른다."
  그런데 두 무리의 점을 칠판에 찍어 놓고 보면, 둘을 완벽히 가르는 직선은 <strong>하나가 아니라 무수히 많다</strong>.
  살짝 기울여도, 조금 위로 올려도 여전히 둘을 가른다.</p>

  <h3 class="step">의문</h3>
  <div class="qbox">
    <span class="label">의문</span>
    같은 데이터를 가르는 직선이 무수히 많다면, SVM 은 <strong>그중 어느 하나를 어떤 기준으로</strong> 고를까?
    "그냥 가르기만 하면 되는 것"이 아니라 "<strong>가장 좋게</strong> 가른다"고 했는데 —
    그 '가장 좋음'을 측정 가능한 양으로 정의할 수 있어야 한다. 이 질문이 오늘 글 전체의 출발점이다.
  </div>
  <p>경계가 '좋다/나쁘다'를 가르는 기준 후보는 하나뿐이다 — 경계가 양쪽 점들로부터 <strong>얼마나 여유 있게 떨어져 있는가</strong>.
  아슬아슬하게 점에 붙은 선은 새 점 하나만 들어와도 틀리기 쉽다. 그 '여유'를 SVM 은 <strong>마진(margin)</strong>이라 부른다.
  먼저 마진이 실제로 측정 가능한 숫자인지부터 확인한다.</p>

  <h3 class="step">테스트 — 선형 SVM 이 정한 경계의 마진을 꺼내 본다</h3>
  <p>선형 분리가 되는 깔끔한 예(iris 의 setosa vs versicolor, 꽃잎 길이·너비 2특성)에 선형 SVM 을 학습시키고,
  결정함수 <code>f(x)=w·x+b</code> 에서 마진 폭 <code>2/||w||</code> 와 경계를 떠받치는 점의 수를 직접 출력한다.</p>
  <div class="terminal">
    <div class="terminal-header">SVC(kernel='linear').fit(iris 2클래스) — 마진 폭 2/||w|| · 서포트 벡터 수 확인 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_01@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_MARGIN@@" alt="선형 SVM 결정경계와 마진 점선, 서포트 벡터를 표시한 산점도">
    <figcaption>그림 0529-1 · 실선=결정경계, 점선=마진 경계, 초록 테두리 점=서포트 벡터. 두 무리 사이 '가장 넓은 도로'의 한가운데에 경계가 놓인다</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT</span>
    '가장 좋음'은 측정 가능한 숫자였다 — <strong>마진 폭 1.419</strong>. 그리고 학습 정확도 100%.
    SVM 은 둘을 가르는 무수한 직선 중 이 마진을 <strong>최대로</strong> 만드는 단 하나를 골랐다.
    그렇다면 왜 하필 마진이 가장 넓은 선이 '가장 좋은' 선일까? 넓은 도로가 안전하다는 직관을 숫자로 확인해야 한다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 마진이 측정 가능하다는 것까지는 봤다. 그런데 "마진이 넓을수록 좋다"는
    아직 직관일 뿐이다. 경계를 일부러 옆으로 밀어 보면, 정말 마진이 가장 큰 위치가 SVM 이 고른 그 위치일까?
  </div>
</section>

<!-- ===================== CH 02 ===================== -->
<section id="ch2">
  <h2 class="chap"><span class="num">CH 02</span>마진 최대화 — 왜 '가장 넓은 도로'의 한가운데인가<a href="#ch2" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    SVM 경계를 양쪽으로 평행이동시키면, 한쪽 클래스에 가까워지면서 '가장 가까운 점까지의 거리'가 줄어들 것이다.
    이동량 0(= SVM 경계)에서 그 최소 거리가 <strong>가장 클</strong> 것이다 — 즉 SVM 경계가 곧 마진 최대 위치라는 뜻이다.
  </div>
  <p>왜 마진이 넓어야 안전한가? 경계에서 가장 가까운 점이 곧 "다음에 틀릴 위험이 가장 큰 점"이기 때문이다.
  그 점까지의 거리를 최대로 벌려 두면, 데이터에 약간의 흔들림(노이즈)이 와도 경계를 넘지 않는다.
  경계를 평행이동시키며 양쪽 클래스의 최근접 거리를 직접 재 본다.</p>

  <h3 class="step">테스트 — 경계를 평행이동하며 최근접 거리를 잰다</h3>
  <div class="terminal">
    <div class="terminal-header">SVM 경계 평행이동 — 양쪽 클래스 최근접 거리 비교(마진 최대 위치 확인) · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_02@@</pre>
  </div>

  <blockquote class="cite">
    "Support vector machines … are effective in high dimensional spaces.
    The support vectors are the data points that lie closest to the decision surface (or hyperplane).
    Intuitively, a good separation is achieved by the hyperplane that has the largest distance
    to the nearest training-data points of any class (so-called functional margin),
    since in general the larger the margin the lower the generalization error of the classifier."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/svm.html" target="_blank" rel="noopener">Support Vector Machines</a> (마진과 일반화)</span>
  </blockquote>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">가설 통과</span>
    이동량 0(SVM 경계)에서 최근접 거리 <strong>0.6413</strong> 으로 가장 컸고, 좌우로 0.6 밀면 0.2494·0.2156 까지 줄었다.
    옆으로 밀수록 한쪽 점에 아슬아슬하게 붙는다 — 마진 최대 = "양쪽에서 가장 멀리 떨어진 한가운데".
    이것이 공식 문서가 말한 "larger the margin the lower the generalization error"의 핵심이다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 마진은 '가장 가까운 점'까지의 거리로 정해졌다. 그렇다면 경계를 실제로
    결정하는 건 그 가장 가까운 점들뿐이고, 멀리 떨어진 점들은 경계에 아무 영향도 안 주는 것 아닐까?
  </div>
</section>

<!-- ===================== CH 03 ===================== -->
<section id="ch3">
  <h2 class="chap"><span class="num">CH 03</span>서포트 벡터 — 경계를 정하는 단 몇 개의 점<a href="#ch3" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    마진이 '가장 가까운 점까지의 거리'라면, 경계를 떠받치는 점은 마진 경계 위에 놓인 <strong>소수의 점</strong>뿐이고,
    그 안쪽 깊숙이 있는 점들은 옮기거나 지워도 경계가 변하지 않을 것이다. CH 01 의 100개 표본 중 경계를 정하는
    점은 극히 일부여야 한다.
  </div>
  <p>CH 01 의 로그를 다시 보면 답은 이미 거기 있었다. 표본 100개 중 <code>support_vectors_</code> 로 잡힌 점은 단 4개.
  이 4개가 마진 경계(점선) 위에 정확히 놓여 경계를 '떠받친다'. 그래서 이름이 <strong>서포트 벡터</strong>다.</p>

  <blockquote class="cite">
    "The decision function is fully specified by a (usually small) subset of training samples, the support vectors."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/svm.html#svc" target="_blank" rel="noopener">SVC — support vectors</a></span>
  </blockquote>

  <h3 class="step">관찰 — 그림 0529-1 의 초록 테두리 점</h3>
  <p>그림 0529-1 에서 초록 테두리가 둘린 점이 바로 그 4개다. 마진 경계(점선) 위에 정확히 걸려 있다.
  나머지 96개 점은 도로 안쪽 깊숙이 있어, 위치를 바꿔도 가장 가까운 점이 아니므로 경계에 영향을 못 준다.</p>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT</span>
    경계를 정하는 건 전체의 <strong>4%(4개)</strong>뿐. 이것이 SVM 이 고차원·소표본에서도 효율적인 이유다 —
    모델은 모든 점이 아니라 경계에 걸친 서포트 벡터만 기억하면 된다. 그래서 "서포트 벡터 머신"이다.
    그런데 여기까지는 직선 하나로 깔끔히 갈리는 데이터였다. 직선으로 도저히 안 갈리는 데이터라면?
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 마진도 서포트 벡터도 "직선이 존재한다"는 전제 위에 있었다.
    실습의 글자 이미지처럼 두 무리가 서로 엉켜 어떤 직선으로도 못 가르는 데이터라면, 마진 최대화는 아예 출발조차 못 한다.
    이때 SVM 은 무엇을 하는가?
  </div>
</section>

<!-- ===================== CH 04 ===================== -->
<section id="ch4">
  <h2 class="chap"><span class="num">CH 04</span>막힘 — 직선으로 안 갈리는 데이터(커널 트릭)<a href="#ch4" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    초승달 두 개가 맞물린 모양(make_moons)은 어떤 직선으로도 못 가른다. 선형 SVM 은 여기서 정확도가 낮을 것이다.
    반면 <strong>RBF 커널</strong>은 데이터를 더 높은 차원으로 사상(寫像)해 그 공간에서 직선을 그어, 원래 공간에서는
    <strong>휘어진 경계</strong>로 보이게 만들어 높은 정확도를 낼 것이다.
  </div>
  <p>커널 트릭의 핵심은 "실제로 고차원 좌표를 계산하지 않고, 두 점의 <strong>유사도(커널 함수)</strong>만으로
  고차원에서의 내적을 대신한다"는 것이다. RBF 커널 <code>exp(-gamma·||x-x'||²)</code> 은 가까운 점끼리 큰 유사도를 준다.</p>

  <blockquote class="cite">
    "When the decision boundary is not linear, … the kernel trick maps the inputs into
    high-dimensional feature spaces. … the radial basis function (RBF) kernel."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/svm.html#kernel-functions" target="_blank" rel="noopener">Kernel functions</a></span>
  </blockquote>

  <h3 class="step">테스트 — 같은 moons 에 선형 vs RBF</h3>
  <div class="terminal">
    <div class="terminal-header">make_moons — SVC(linear) vs SVC(rbf) test 정확도 비교 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_03@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_KERNEL@@" alt="make_moons 데이터에 선형 커널 직선 경계와 RBF 커널 곡선 경계 비교">
    <figcaption>그림 0529-2 · 같은 초승달 데이터 — 선형 커널은 직선으로 한계, RBF 커널은 곡선으로 두 달을 감싼다</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">가설 통과</span>
    선형 커널 test 정확도 0.9000 → RBF 커널 0.9333. 직선의 한계를 RBF 가 휘어진 경계로 넘었다.
    여기서 실습의 <code>RBFFeatureSVMClassifier</code>(Random Fourier Features)가 왜 필요했는지 이해됐다 —
    글자 이미지의 픽셀 특징도 직선으로는 안 갈리기 때문이다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — moons 에서 3.3%p 차이는 크지 않았다. RBF 가 정말 일반적인 해법인지,
    선형으로는 거의 불가능한 더 극단적인 모양(동심원)에서 다시 확인해 본다.
  </div>
</section>

<!-- ===================== CH 05 ===================== -->
<section id="ch5">
  <h2 class="chap"><span class="num">CH 05</span>한 발 더 — RBF 는 정말 일반적인가(동심원)<a href="#ch5" class="anchor-link">#</a></h2>

  <h3 class="step">테스트 — 동심원(circles)에서 선형 vs RBF</h3>
  <p>안쪽 원과 바깥 원으로 이뤄진 동심원은 어떤 직선으로도 절대 못 가른다(직선은 원의 안팎을 동시에 가를 수 없다).
  여기서 선형 커널은 거의 무작위 수준일 것이고, RBF 는 '중심에서의 거리'를 사실상 학습해 완벽히 가를 것이다.</p>
  <div class="terminal">
    <div class="terminal-header">make_circles — SVC(linear) vs SVC(rbf) test 정확도 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_04@@</pre>
  </div>

  <h3 class="step">관찰</h3>
  <div class="keypoint">
    <span class="label">KEY POINT</span>
    선형 커널 test 정확도 <strong>0.4222</strong> — 동전 던지기보다 못하다(직선으로는 동심원이 원리적으로 불가능).
    같은 데이터에 RBF 커널은 <strong>1.0000</strong>. RBF 는 점들 사이 거리(유사도)를 쓰므로 "중심에 가까운가/먼가"를
    자연히 잡아낸다. 커널 트릭은 특정 모양에만 통하는 요령이 아니라 비선형 일반 해법임이 확인됐다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — RBF 가 강력하다면, 더 세게 휘게 만들면 항상 좋아질까?
    RBF 의 자유도를 키우는 손잡이가 <code>C</code> 와 <code>gamma</code> 다. 이 둘을 끝까지 올려 본다 —
    Day1 의 다항 회귀에서 차수를 올렸을 때처럼, 또 낮아지지 않을까?
  </div>
</section>

<!-- ===================== CH 06 ===================== -->
<section id="ch6">
  <h2 class="chap"><span class="num">CH 06</span>예상과 다른 결과 — C·gamma 를 키웠더니 경계가 크게 낮아졌다<a href="#ch6" class="anchor-link">#</a></h2>

  <h3 class="step">학습 → 가설</h3>
  <p><code>C</code> 는 "오분류를 얼마나 봐주지 않을지"(클수록 train 오류에 엄격 → 마진을 좁혀서라도 다 맞히려 함),
  <code>gamma</code> 는 "한 점의 영향이 미치는 반경"(클수록 각 점 주변만 좁게 반응)이다.
  둘을 키우면 경계가 train 점 하나하나에 달라붙는다.</p>
  <div class="qbox">
    <span class="label">가설</span>
    <code>C</code> 와 <code>gamma</code> 를 크게 키우면 train 정확도는 1.0 에 가깝게 오르지만, 경계가 train 노이즈까지
    과하게 학습해 test 정확도는 오히려 떨어질 것이다(과대적합). 적당한 값과 과한 값의 train-test 격차를 비교한다.
  </div>

  <blockquote class="cite">
    "The C parameter trades off correct classification of training examples against maximization
    of the decision function's margin. … the gamma parameter defines how far the influence of a single
    training example reaches. … if gamma is too large, the radius of the area of influence of the support
    vectors only includes the support vector itself … and the model will overfit."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/auto_examples/svm/plot_rbf_parameters.html" target="_blank" rel="noopener">RBF SVM parameters (C, gamma)</a></span>
  </blockquote>

  <h3 class="step">테스트 — C·gamma 를 키우며 train/test</h3>
  <div class="terminal">
    <div class="terminal-header">SVC(rbf) C·gamma sweep — train↑ test↓ 과대적합 확인(make_moons noise=0.30) · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_05@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_CGAMMA@@" alt="작은 C/gamma 의 매끈한 경계와 큰 C/gamma 의 과대적합 경계 비교">
    <figcaption>그림 0529-3 · 왼쪽(C=1, gamma=0.5)은 매끈한 경계, 오른쪽(C=1000, gamma=50)은 점마다 섬처럼 둘러싸 train 에 과대적합</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">FAILURE → CLUE</span>
    적당한 (C=1, gamma=0.5): train 0.8905 / test 0.8778 — 격차 +0.0127 로 건강하다.
    과한 (C=1000, gamma=50): train <strong>1.0000</strong> / test <strong>0.8111</strong> — 격차 +0.1889 로 벌어졌다.
    train 을 완벽히 맞히려 경계를 점마다 섬처럼 둘렀더니, 처음 보는 데이터에서 크게 낮아졌다.
    Day1 의 다항 차수↑ 과대적합과 똑같은 함정 — '더 유연하게 = 더 좋게'가 아니다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — SVM 의 RBF 경계는 매끄러운 곡선이었다. 그런데 같은 데이터를
    로지스틱 회귀나 KNN 으로 가르면 경계 모양이 어떻게 다를까? 모델마다 '가장 좋은 경계'의 정의가 다른 것 아닐까?
  </div>
</section>

<!-- ===================== CH 07 ===================== -->
<section id="ch7">
  <h2 class="chap"><span class="num">CH 07</span>비교 — 로지스틱·KNN·SVM 의 경계 모양<a href="#ch7" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 비교</h3>
  <div class="qbox">
    <span class="label">의문</span>
    같은 make_moons 데이터에 로지스틱 회귀·KNN·RBF SVM 을 학습하면, 셋의 경계 '모양'과 test 정확도가 어떻게 갈릴까?
    각 모델이 '경계를 긋는 철학'이 다르다면 그 차이가 그림으로 드러날 것이다.
  </div>
  <p>로지스틱 회귀는 선형 모델이라 직선(평면) 경계, KNN 은 이웃 다수결이라 점들에 따라 조각조각 울퉁불퉁한 경계,
  SVM(RBF)은 마진을 최대화하는 매끄러운 곡선 경계를 그린다. 셋을 같은 데이터에 올려 본다.</p>

  <h3 class="step">테스트 — 세 분류기 한자리에서</h3>
  <div class="terminal">
    <div class="terminal-header">make_moons — LogisticRegression / KNN(k=5) / SVC(rbf) test 정확도·경계 모양 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_06@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_COMPARE@@" alt="로지스틱 직선 경계, KNN 조각 경계, SVM RBF 곡선 경계 비교">
    <figcaption>그림 0529-4 · 왼쪽부터 로지스틱(직선) · KNN(조각조각) · SVM RBF(매끄러운 곡선) — 같은 데이터, 다른 철학의 경계</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">관찰 결과</span>
    로지스틱 0.9000(직선이라 두 달의 곡선 경계를 못 따라감), KNN(k=5) 0.9889(국소 다수결이라 곡선을 잘 따라가지만
    경계가 울퉁불퉁), SVM(RBF) 0.9333(매끄러운 곡선). 정확도 1등이 KNN 이라고 SVM 이 진 건 아니다 —
    SVM 의 강점은 <strong>마진으로 경계를 매끄럽고 안정적으로</strong> 두어 노이즈에 덜 흔들린다는 데 있다.
    '가장 좋은 경계'의 정의가 모델마다 다르다는 것이 그림으로 드러났다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 이제 출발 의문으로 돌아갈 차례다.
    "같은 데이터를 가르는 무수한 선 중 무엇이 가장 좋은 경계인가"에 SVM 은 어떤 답을 내놓았나, 한 줄로 묶는다.
  </div>
</section>

<!-- ===================== CH 08 ===================== -->
<section id="ch8">
  <h2 class="chap"><span class="num">CH 08</span>정리 — '가장 좋은 경계'의 답과 SVM 구조<a href="#ch8" class="anchor-link">#</a></h2>

  <h3 class="step">최종 결론 — 출발 의문 회수</h3>
  <div class="keypoint">
    <span class="label">FINAL CONCLUSION</span>
    CH 01 의 질문 "무수한 선 중 무엇이 가장 좋은 경계인가"의 답:
    <strong>SVM 은 두 클래스에서 가장 가까운 점까지의 거리(마진)를 최대로 만드는 경계를 고른다.</strong>
    그 경계는 마진 경계 위 소수의 <strong>서포트 벡터</strong>(CH 01·03 에서 100개 중 4개)만으로 정해지고(CH 03),
    직선으로 못 가르는 데이터는 <strong>커널 트릭</strong>으로 휘며(moons 0.90→0.93, circles 0.42→1.00, CH 04~05),
    단 <code>C·gamma</code> 를 과하게 키우면 경계가 데이터에 달라붙어 낮아진다(test 0.88→0.81, CH 06).
    다른 분류기와 달리 SVM 은 '가장 넓은 마진'을 기준으로 삼는다(CH 07).
  </div>

  <h3 class="step">한 문장으로</h3>
  <div class="keypoint">
    <span class="label">ONE-LINER</span>
    SVM 의 구조는 — <strong>"양쪽 무리에서 가장 멀리 떨어진 한가운데(마진 최대) 경계를, 경계에 걸친 소수의
    서포트 벡터로 정의하고, 직선으로 안 되면 커널로 공간을 휘어 같은 일을 한다"</strong>는 한 문장으로 요약된다.
    그래서 SVM 은 데이터를 외우는 게 아니라 <em>경계의 여유</em>를 최대화하는 모델이다.
  </div>

  <table>
    <thead><tr><th>개념</th><th>한 줄 정의</th><th>실측 근거(이 글)</th></tr></thead>
    <tbody>
      <tr><td>마진(margin)</td><td>경계에서 가장 가까운 점까지 거리 ×2</td><td>1.419, 이동 0 에서 최대(CH 02)</td></tr>
      <tr class="hl"><td>서포트 벡터</td><td>마진 경계 위에서 경계를 떠받치는 점</td><td>100개 중 4개(4%)</td></tr>
      <tr><td>RBF 커널 트릭</td><td>고차원 사상으로 비선형 경계</td><td>moons 0.93, circles 1.00</td></tr>
      <tr><td>C · gamma</td><td>유연성 손잡이(과하면 과대적합)</td><td>test 0.88 → 0.81</td></tr>
    </tbody>
  </table>

  <div class="ref-chain">
    <p class="ref-title">📚 전체 근거 출처</p>
    <ol>
      <li><strong>공식 문서</strong>
        <a href="https://scikit-learn.org/stable/modules/svm.html" target="_blank" rel="noopener">scikit-learn · Support Vector Machines</a>(마진·서포트 벡터),
        <a href="https://scikit-learn.org/stable/modules/svm.html#kernel-functions" target="_blank" rel="noopener">Kernel functions</a>(RBF),
        <a href="https://scikit-learn.org/stable/auto_examples/svm/plot_rbf_parameters.html" target="_blank" rel="noopener">RBF SVM parameters</a>(C·gamma).</li>
      <li><strong>workspace</strong>
        <code>../ml_workspace/from_colab/0529-s/pytorch_svm_letter_classification.ipynb</code> :
        수업 실습(LinearSVM 초평면 분리 · RBFFeatureSVMClassifier 글자/우편번호 분류).</li>
      <li><strong>강의자료</strong>
        <code>.study/pdf/머신러닝_서포트백터머신구조.pdf</code> (2. 서포트 벡터 머신 알고리즘, 배경지식).</li>
      <li><strong>실행 검증</strong>
        <code>.study/test/svm_intro/svm_intro_runner.py §01~§06</code>
        → <code>logs/*.txt</code>, <code>charts/*.png</code> (고정 시드 42, 재현 가능).</li>
    </ol>
  </div>

  <div class="bridge">
    <strong>다음 글 예고</strong> — SVM 의 글자/우편번호 분류 실습 자체(특징 표준화·학습 곡선·정확도 튜닝)는
    의문과 시행착오가 많아 별도의 실습 기록으로 정리한다. 이어지는 Day 에서는 거리 기반 이웃(KNN)과
    확률 기반 나이브 베이즈로 분류기의 다른 갈래를 본다.
  </div>
</section>
</main>

<footer>
  <p>SK 네트웍스 AI Family 32기 · 교과목 2 단원 2 머신러닝 Day3 (2026-05-29)</p>
  <p>모든 터미널 출력은 <code>.study/test/svm_intro/svm_intro_runner.py</code> 실제 실행 결과이며,
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
shot = HTML.count('figure class="shot"')
chap = HTML.count('h2 class="chap"')
qbox = HTML.count('class="qbox"')
keyp = HTML.count('class="keypoint"')
zwsp = HTML.count("​")
print(f"파일: {OUT}")
print(f"terminal div: {n_term} | terminal-body: {n_body} | (일치={n_term==n_body})")
print(f"외부 URL img: {len(http_imgs)} (0이어야 함) | base64 img: {b64_imgs} | figure.shot: {shot}")
print(f"chap: {chap} | qbox: {qbox} | keypoint: {keyp} | zero-width space: {zwsp}")
print(f"미치환 placeholder: {leftover} | 크기: {len(HTML)//1024} KB")
