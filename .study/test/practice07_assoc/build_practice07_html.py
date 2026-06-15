# build_practice07_html.py
# ml_practice07_association.html 조립 — logs/*.txt(실제 실행 결과) + charts/*.png(base64) 주입
# 실행: c:\_proj\python_workspace\.venv\Scripts\python.exe build_practice07_html.py
#   (= GUIDE §11 run_all 역할: 터미널 값 직접 작성 금지, 로그에서 주입)
#   서사: day0527_ml_intro.html 의 "의문→실험→결과→새 의문" 사슬 방식 그대로.
import base64, html, pathlib, re

HERE = pathlib.Path(__file__).parent
LOGS = HERE / "logs"
CHARTS = HERE / "charts"
OUT = HERE.parent.parent / "blog" / "ml_practice07_association.html"   # .study/blog/
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
    "@@TERM_00@@": term("00_load"),
    "@@TERM_01@@": term("01_item_freq"),
    "@@TERM_02@@": term("02_manual"),
    "@@TERM_02B@@": term("02b_intuition"),
    "@@TERM_03@@": term("03_rules"),
    "@@TERM_04@@": term("04_threshold"),
    "@@TERM_05@@": term("05_scatter_recommend"),
    "@@TERM_06@@": term("06_kmeans"),
    "@@TERM_07@@": term("07_imbalance"),
    "@@CHART_01@@": chart("ch01_item_freq.png"),
    "@@CHART_04@@": chart("ch04_threshold.png"),
    "@@CHART_05@@": chart("ch05_rules_scatter.png"),
    "@@CHART_06@@": chart("ch06_kmeans.png"),
    "@@CHART_07@@": chart("ch07_imbalance.png"),
}

HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>파이썬 장바구니 연관규칙 분석: support·confidence·lift부터 apriori·KMeans 세그먼트까지</title>
  <meta name="description" content="SK 네트웍스 AI Family 32기 머신러닝 실습7(과제). 9835건의 장바구니 거래에서 '함께 사는' 품목을 어떻게 찾는가 — 지지도·신뢰도·향상도의 정의를 수동 계산으로 검증하고, mlxtend apriori 로 규칙을 생성하며, min_support 임계값이 규칙 수를 어떻게 급증/소멸시키는지, lift>1 의 의미와 추천, KMeans 세그먼트까지 실제 실행으로 추적한 기록.">
  <meta property="og:title" content="파이썬 장바구니 연관규칙 분석: support·confidence·lift부터 apriori·KMeans까지">
  <meta property="og:description" content="함께 사는 품목을 어떻게 찾나 — 지지도·신뢰도·향상도, 임계값의 함정, lift>1 의 의미, 추천, 클러스터링을 실측으로 추적">
  <meta property="og:type" content="article">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="파이썬 장바구니 연관규칙 분석">
  <meta name="twitter:description" content="support·confidence·lift → 임계값 → lift>1 → 추천 → KMeans 세그먼트">
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
  <p class="eyebrow">Python · 머신러닝 실습7(과제) · 부트캠프</p>
  <h1>장바구니에서 '함께 사는' 품목을 어떻게 찾나 — 연관규칙으로 찾는다</h1>
  <p class="deck">9835장의 영수증 데이터가 주어졌다. 과제는 "함께 팔리는 품목 규칙을 찾아 추천 시스템을 만들라"는 것.
  그런데 "함께 잘 팔린다"는 직관을 <strong>숫자로 어떻게 정의</strong>하는가? 지지도·신뢰도·향상도라는 세 수가 그 답인데,
  이 글은 그 정의를 거래 리스트에서 직접 세어 검증하는 데서 출발해 — 임계값 하나로 규칙이 급증하거나 소멸하고,
  <code>lift=1.57</code>이 "우연보다 1.57배 함께 팔린다"는 뜻이 되며, 그 규칙이 추천과 세그먼트로 이어지는 과정을 따라간 기록이다.
  모든 수치는 mlxtend · scikit-learn 으로 직접 돌린 결과이며 <code>random_state=42</code>로 재현 가능하다.</p>
  <div class="meta-row">
    <span><strong>날짜</strong>2026-06-05</span>
    <span><strong>Python</strong>@@PY@@ · scikit-learn 1.8.0 · mlxtend 0.25.0 · pandas 3.0.2</span>
    <span><strong>OS</strong>Windows 11 Pro 25H2</span>
    <span><strong>IDE</strong>VS Code 1.117.0</span>
    <span><strong>HW</strong>Asrock x600 · Ryzen 8600G · 24GB LPDDR5 · RTX 4070 Super 12GB</span>
    <span><strong>커리큘럼</strong>머신러닝 실습7(과제) · 연관규칙분석 — 7_머신러닝_비지도학습알고리즘.pdf</span>
  </div>
</header>

<main>
<nav class="flow">
  <h2>이 글의 흐름 — '함께 산다'를 숫자로 정의하는 길</h2>
  <ol>
    <li><a href="#ch1">시작 — 9835장의 영수증, '함께 산다'를 무엇으로 재나</a></li>
    <li><a href="#ch2">품목 빈도 — 단일 품목의 지지도(support)부터</a></li>
    <li><a href="#ch3"><span class="turn">왜 쏠리나</span> — 품목 분포의 불균등을 지니계수로 재다</a></li>
    <li><a href="#ch4">정의부터 확인한다 — support·confidence·lift 를 손으로 세어 본다</a></li>
    <li><a href="#ch5"><span class="turn">직관</span> — lift&gt;1은 무슨 뜻인가, 합집합 기호인데 왜 교집합인가</a></li>
    <li><a href="#ch6">규칙 생성 — apriori 로 빈발 itemset 을 뽑고 lift 로 줄 세우다</a></li>
    <li><a href="#ch7">임계값(min_support)을 어떻게 정하나, 규칙이 급증하고 소멸한다</a></li>
    <li><a href="#ch8"><span class="turn">의미</span> — lift 로 만든 추천과 confidence 의 함정</a></li>
    <li><a href="#ch9"><span class="turn">한 발 더</span> — 규칙을 넘어, KMeans 로 장바구니를 세그먼트하다</a></li>
    <li><a href="#ch10">정리 — '함께 산다'의 정의와 과제 보고서 회수</a></li>
  </ol>
</nav>

<!-- ===================== CH 01 ===================== -->
<section id="ch1">
  <h2 class="chap"><span class="num">CH 01</span>시작 — '함께 산다'를 무엇으로 재나<a href="#ch1" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>과제로 받은 <code>shop_groceries.csv</code>는 형태가 낯설었다. 일반적인 표(고정된 열)가 아니라
  <strong>행마다 길이가 다른</strong> 파일이다 — 한 줄이 영수증 한 장이고, 쉼표로 구분된 품목들이 그 바구니의 내용물이다.
  <code>pandas.read_csv</code>를 그냥 부르면 "Expected 4 fields, saw 5"로 성립하지 않는다. 거래는 가변 길이라는 게 첫 단서다.</p>

  <h3 class="step">의문</h3>
  <div class="qbox">
    <span class="label">의문</span>
    과제의 목표는 "함께 팔리는 품목을 찾으라"는 것이다. 그런데 <strong>'함께 잘 팔린다'를 숫자로 어떻게 정의</strong>할까?
    그 전에 — 이 데이터에는 거래가 몇 건, 품목이 몇 종 있고, 한 바구니에는 보통 몇 개가 담기나?
    규칙을 논하기 전에 데이터의 골격부터 잡아야 한다.
  </div>

  <h3 class="step">테스트 — 거래/품목 구조를 센다</h3>
  <p>가변 길이 행은 <code>csv.reader</code>로 한 줄씩 리스트로 읽고, mlxtend <code>TransactionEncoder</code>로
  거래×품목 one-hot 행렬(True/False)로 바꾼다. 이 행렬이 이후 모든 계산의 입력이다.</p>
  <pre><code class="language-python"># path : .study/test/practice07_assoc/practice07_runner.py §00 (발췌)
import csv
from mlxtend.preprocessing import TransactionEncoder

with open("shop_groceries.csv", encoding="utf-8") as f:
    txns = [[i.strip() for i in row if i.strip()] for row in csv.reader(f)]

te = TransactionEncoder()
arr = te.fit_transform(txns)            # 거래 x 품목 one-hot (True/False)
onehot = pd.DataFrame(arr, columns=te.columns_)
print("전체 거래 수:", len(txns), " 품목 수:", onehot.shape[1])</code></pre>
  <div class="terminal">
    <div class="terminal-header">practice07_runner.py §00 · csv.reader + TransactionEncoder — 거래/품목 구조 파악 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_00@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT</span>
    거래 <strong>9835건</strong>, 고유 품목 <strong>169종</strong>, 바구니 크기는 1~32개(평균 4.41)다.
    가변 길이 거래는 <code>TransactionEncoder</code>로 <strong>9835×169 one-hot 행렬</strong>이 됐다.
    이제 이 행렬 위에서 '함께 산다'를 숫자로 정의할 차례다. 그 첫걸음은 가장 단순한 양 —
    한 품목이 얼마나 자주 팔리나(지지도)부터다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — one-hot 행렬에서 한 열의 평균(True 비율)이 곧 그 품목의 지지도다.
    먼저 단일 품목 지지도를 줄 세워 "무엇이 가장 많이 팔리나"를 보고, 거기서 규칙으로 확장한다.
  </div>
</section>

<!-- ===================== CH 02 ===================== -->
<section id="ch2">
  <h2 class="chap"><span class="num">CH 02</span>품목 빈도 — 단일 품목의 지지도<a href="#ch2" class="anchor-link">#</a></h2>

  <h3 class="step">학습 → 의문</h3>
  <p><strong>지지도(support)</strong>는 전체 거래 중 어떤 품목(집합)을 포함한 거래의 비율이다.
  단일 품목이라면 <code>support(A) = A를 산 거래 수 / 전체 거래 수</code> — 곧 판매 빈도다.
  one-hot 행렬에서는 한 열의 평균(<code>onehot.mean()</code>)이 바로 이 값이다.</p>
  <div class="qbox">
    <span class="label">의문</span>
    이 데이터에서 가장 많이 팔린 품목과 가장 적게 팔린 품목의 지지도 격차는 얼마나 클까?
    품목 분포가 고르다면 규칙도 고르게 나오겠지만, 한쪽으로 쏠려 있다면 소수의 인기 품목이 규칙을 지배할 것이다.
  </div>

  <h3 class="step">테스트 — 상위 품목 지지도</h3>
  <div class="terminal">
    <div class="terminal-header">practice07_runner.py §01 · onehot.mean() — 단일 품목 지지도 상위 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_01@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_01@@" alt="상위 15개 품목 지지도 막대그래프">
    <figcaption>그림 1 · 상위 15개 품목 지지도 — whole milk 가 0.2555 로 가장 큰, 빠르게 감소하는 롱테일</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">관찰 결과</span>
    가장 많이 팔린 품목은 <strong>whole milk(support 0.2555)</strong> — 네 거래 중 한 번꼴이다.
    그 뒤로 other vegetables(0.194)·rolls/buns(0.184)·soda(0.174)가 따른다. 반대로 꼬리 끝의
    <code>sound storage medium</code>은 support 0.0001(거래 1건)에 불과하다. <strong>분포는 전혀 고르지 않고
    소수 인기 품목에 쏠린 롱테일</strong>이다. 그래서 규칙도 인기 품목 주변에서 먼저 나타날 것이다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — "분포는 고르지 않다"고 말했지만 이건 인상이지 수치가 아니다.
    얼마나 고르지 않은지, 무엇을 기준으로 "쏠렸다"고 말할 수 있는지 — 다음 챕터에서 점유율과 지니계수로 정량화한다.
  </div>
</section>

<!-- ===================== CH 03 ===================== -->
<section id="ch3">
  <h2 class="chap"><span class="num">CH 03</span>왜 쏠리나 — 품목 분포의 불균등을 재다<a href="#ch3" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 가설</h3>
  <p>CH 02에서 "분포가 고르지 않다"고 적었지만, 그건 막대그래프를 본 인상일 뿐이다.
  169품목이 완전히 균등하게 팔린다면 각 품목의 판매 점유율은 <code>1/169 ≈ 0.59%</code>로 같아야 한다.
  실제 점유율이 이 기준선에서 얼마나 벗어나는지를 재면 "쏠림"을 수치로 말할 수 있다.</p>
  <div class="qbox">
    <span class="label">가설</span>
    품목 분포는 균등(각 0.59%)이 아니라 소수 인기 품목에 쏠려 있을 것이다. 가설이 맞다면
    ① 상위 몇 품목이 균등 기준선보다 몇 배 높은 점유율을 갖고, ② 상위 소수가 전체 판매의 큰 몫을 차지하며,
    ③ 불균등 척도인 <strong>지니계수가 0(완전균등)에서 뚜렷이 떨어져</strong> 0.5를 넘을 것이다.
    top-4 점유율·누적 점유율·지니계수를 실제 데이터로 센다.
  </div>

  <h3 class="step">테스트 — 점유율·누적 점유율·지니계수</h3>
  <p>각 품목이 등장한 거래 수를 세어 판매 점유율을 구하고, 상위 N품목의 누적 점유율과
  분포 불균등의 표준 척도인 <strong>지니계수</strong>(0=완전균등, 1=완전독점)를 계산한다.</p>
  <pre><code class="language-python"># path : .study/test/practice07_assoc/practice07_runner.py §07 (발췌)
counts = onehot.sum().sort_values(ascending=False)   # 품목별 등장 거래 수
total  = counts.sum()
share  = counts / total                              # 품목별 판매 점유율
uniform = 1 / len(counts)                            # 완전 균등 시 점유율(=1/169)

top4_share = counts.head(4).sum() / total            # 상위 4품목 합산 점유율
# 지니계수: 0=완전균등, 1=완전독점
vals = np.sort(counts.values.astype(float)); n = len(vals); cum = np.cumsum(vals)
gini = (n + 1 - 2 * (cum.sum() / cum[-1])) / n
print(top4_share, gini)</code></pre>
  <div class="terminal">
    <div class="terminal-header">practice07_runner.py §07 · 품목 점유율·누적·지니계수 — 분포 불균등 정량화 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_07@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_07@@" alt="상위 20품목 점유율과 균등선, 그리고 로렌츠 곡선">
    <figcaption>그림 2 · (좌) 상위 20품목 점유율 — 점선이 완전 균등 시 0.59% (우) 로렌츠 곡선이 균등선에서 멀수록 불균등</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">가설 통과</span>
    분포는 균등이 아니었다. 1위 whole milk 의 점유율은 5.79%로 균등 기준선(0.59%)의 <strong>9.8배</strong>고,
    상위 4품목(전체의 2.4%)이 판매의 <strong>18.31%</strong>를 차지했다. 상위 20품목(11.8%)이 50.38%로
    절반을 넘는다. 불균등 척도인 <strong>지니계수는 0.6331</strong>로 0.5를 분명히 웃돌았다 —
    소수 인기 품목 쏠림이 수치로 확인된다.
  </div>

  <div class="callout">
    <span class="label">왜 균등하지 않나</span>
    품목 점유율이 균등하지 않은 건 데이터 오류가 아니라 구매 행동의 자연스러운 성질이다.
    우유·채소·빵 같은 생필품은 거의 모든 장바구니에 들어가고, 특수 품목은 드물게 팔린다.
    이 쏠림이 곧 다음 분석의 전제다 — 인기 품목은 support 가 높아 규칙 상위에 자주 오르지만,
    그게 "관련 있어서"인지 "원래 흔해서"인지는 support 만으로 가릴 수 없다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 단일 품목의 빈도와 쏠림은 봤다. 과제의 핵심은 "A를 사면 B도 산다"는
    <em>두 품목의 관계</em>다. 그 관계를 재는 confidence·lift 가 정확히 무엇인지 — 도구를 믿기 전에 손으로 세어 확인한다.
  </div>
</section>

<!-- ===================== CH 04 ===================== -->
<section id="ch4">
  <h2 class="chap"><span class="num">CH 04</span>정의부터 확인한다 — support·confidence·lift 를 손으로<a href="#ch4" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    mlxtend 가 내놓는 confidence·lift 는 특별한 비법이 아니라 정의 그대로의 산술일 것이다. 즉 거래 리스트에서
    직접 센 값과 정확히 일치해야 한다. 검증식은 셋이다 —
    <code>support(A→B)=count(A∪B)/N</code>, <code>confidence=support(A∪B)/support(A)</code>,
    <code>lift=confidence/support(B)</code>. <code>whole milk→yogurt</code>로 수동·도구 값이 같으면 가설 통과다.
  </div>

  <blockquote class="cite">
    "support … is an indication of how frequently the itemset appears in the dataset.
    The confidence … is an indication of how often the rule has been found to be true.
    The lift … is the ratio of the observed support to that expected if X and Y were independent."
    <span class="src">— mlxtend 공식 문서 · <a href="https://rasbt.github.io/mlxtend/user_guide/frequent_patterns/association_rules/" target="_blank" rel="noopener">association_rules (support/confidence/lift 정의)</a></span>
  </blockquote>

  <h3 class="step">테스트 — 손 계산 vs mlxtend</h3>
  <pre><code class="language-python"># path : .study/test/practice07_assoc/practice07_runner.py §02 (발췌)
N = len(txns); sets = [set(t) for t in txns]
def sup(items): return sum(1 for s in sets if set(items) <= s) / N

s_a, s_b, s_ab = sup({"whole milk"}), sup({"yogurt"}), sup({"whole milk","yogurt"})
conf = s_ab / s_a            # confidence
lift = conf / s_b            # lift
print(conf, lift)            # ← mlxtend 결과와 대조</code></pre>
  <div class="terminal">
    <div class="terminal-header">practice07_runner.py §02 · 수동 support/confidence/lift vs mlxtend — 정의 검증 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_02@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">가설 통과</span>
    <code>whole milk→yogurt</code>: 수동 계산 support 0.0560·confidence 0.2193·lift 1.5717 이,
    mlxtend 값과 <strong>소수점 넷째 자리까지 정확히 일치(allclose=True)</strong>했다.
    confidence 0.219 는 "whole milk 산 사람의 21.9%가 yogurt도 샀다", lift 1.572 는
    "두 품목이 독립이라 가정했을 때보다 1.57배 자주 함께 산다"는 뜻이다. 정의는 특별한 비법이 아니라 셋의 산술이었다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 손 계산으로 confidence 0.219·lift 1.572 라는 숫자는 얻었다.
    그런데 confidence 0.219 는 "21.9%뿐"이라 낮아 보이고, lift 1.572 의 "1.57배"는 무엇 대비 1.57배인지 모호하다.
    게다가 정의식에 쓰인 <code>support(A∪B)</code>는 합집합 기호인데 의미는 동시 구매다. 이 셋을 실수치로 분해한다.
  </div>
</section>

<!-- ===================== CH 05 ===================== -->
<section id="ch5">
  <h2 class="chap"><span class="num">CH 05</span>직관 — lift&gt;1의 뜻과, 합집합 기호인데 왜 교집합인가<a href="#ch5" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">의문</span>
    같은 규칙 <code>whole milk→yogurt</code>를 두고 세 가지가 걸린다.
    ① <strong>lift 1.572 는 무엇 대비 1.57배</strong>인가 — "상관없으면 이만큼만 함께 사야 하는데 더 샀다"의 그 기준은 얼마인가?
    ② confidence는 0.219, 즉 <strong>21.9%뿐인데 왜 "의미 있다"</strong>고 보나?
    ③ 정의식 <code>support(A∪B)</code>는 합집합(∪) 기호인데 왜 의미는 교집합(동시 구매)인가?
    세 값을 거래 리스트에서 직접 세어 분해하면 답이 나올 것이다.
  </div>

  <h3 class="step">테스트 — 독립 기대치 분해 · confidence 함정 · ∪ vs ∩</h3>
  <p>lift 의 분모 <code>P(A)·P(B)</code>는 "두 품목이 독립(우연)일 때 함께 담길 기대 비율"이다.
  분자 <code>support(A∪B)</code>는 "실제로 함께 담긴 비율". 둘을 따로 출력해 비교하고,
  같은 거래에서 AND(교집합)·OR(합집합)을 직접 세어 <code>support(A∪B)</code>가 어느 쪽과 같은지 확인한다.</p>
  <pre><code class="language-python"># path : .study/test/practice07_assoc/practice07_runner.py §02b (발췌)
s_a, s_b = sup({"whole milk"}), sup({"yogurt"})
indep = s_a * s_b               # 분모: 독립일 때 기대(우연) 비율
s_ab  = sup({"whole milk","yogurt"})   # 분자: 실제 동시 구매 비율
lift  = s_ab / indep            # = confidence / s_b 와 동일

inter = mean(milk AND yogurt)   # 교집합(동시 구매)
union = mean(milk OR  yogurt)   # 진짜 합집합(둘 중 하나라도)
print(s_ab == inter)            # support(A∪B) 가 교집합과 같은가?</code></pre>
  <div class="terminal">
    <div class="terminal-header">practice07_runner.py §02b · P(A)P(B) 독립기대 vs 실제 · ∪ vs ∩ — lift 직관 분해 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_02B@@</pre>
  </div>

  <h3 class="step">결론(중간) — ① lift&gt;1의 뜻</h3>
  <div class="keypoint">
    <span class="label">KEY POINT</span>
    두 품목이 독립이라면 함께 담길 기대 비율은 <code>P(A)·P(B)=0.2555×0.1395=0.0356</code>, 곧 <strong>3.56%</strong>다.
    그런데 실제 동시 구매 비율은 <strong>5.60%</strong>였다. "상관없으면 3.56%만 함께 사야 정상인데 5.60% 샀다" —
    그 비율 <code>5.60/3.56 = 1.572</code>가 lift 다. lift&gt;1 은 <strong>우연 기대치보다 더 자주 함께 산다</strong>는 뜻이고,
    1.572 의 "1.57배"는 바로 이 독립 기대치 대비 배수다.
  </div>

  <h3 class="step">결론(중간) — ② confidence 21.9%의 함정</h3>
  <div class="keypoint">
    <span class="label">KEY POINT</span>
    confidence 0.219 만 보면 "우유 산 사람의 21.9%만 yogurt 를 샀으니 약하다"고 읽기 쉽다. 하지만 비교 기준이 빠졌다.
    yogurt 의 기저 구매율 <code>P(B)</code>는 <strong>14.0%</strong>다. 우유를 산 집단에서는 그 비율이 <strong>21.9%</strong>로 올라간다 —
    yogurt 평균보다 1.57배 높다. confidence 는 절대 크기가 아니라 <strong>기저 비율과의 비교(=lift)</strong>로 읽어야 의미가 드러난다.
  </div>

  <h3 class="step">결론(중간) — ③ 합집합 기호인데 교집합인 이유</h3>
  <div class="keypoint">
    <span class="label">KEY POINT</span>
    같은 거래에서 동시 구매(AND)는 0.0560, 둘 중 하나라도(OR)는 0.3390이었고, <code>support(A∪B)</code>가 가리킨 값은
    0.0560 — <strong>AND(교집합)와 같았다(allclose=True)</strong>. 기호가 ∪ 인 건 "whole milk 와 yogurt 를 합친
    <strong>하나의 itemset {whole milk, yogurt}</strong>"를 뜻하기 때문이고, 그 itemset 을 <em>모두 포함한</em> 거래를 세므로
    계산은 교집합(∩, 동시 구매)이 된다. 규칙을 "집합(Set)"으로 쓰는 이유도 같다 — 순서·중복이 없는 품목 묶음이기 때문이다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 정의와 직관은 한 규칙으로 확인했다. 하지만 169품목의 모든 조합을 손으로 셀 수는 없다.
    빈발한 품목 집합만 골라 효율적으로 규칙을 만드는 게 apriori 다. 도구로 전체 규칙을 뽑아 lift 로 줄 세운다.
  </div>
</section>

<!-- ===================== CH 06 ===================== -->
<section id="ch6">
  <h2 class="chap"><span class="num">CH 06</span>규칙 생성 — apriori 와 lift 줄 세우기<a href="#ch6" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>품목 169종의 가능한 부분집합은 천문학적이라 전수 조사가 불가능하다. <strong>apriori</strong>는
  "빈발하지 않은 집합의 상위 집합도 빈발할 수 없다"는 성질로 가지치기해, <code>min_support</code> 이상인
  빈발 itemset 만 효율적으로 찾는다. 거기서 <code>association_rules</code>가 confidence 기준으로 규칙을 만든다.</p>

  <blockquote class="cite">
    "Apriori is a popular algorithm for extracting frequent itemsets …
    The apriori property … all subsets of a frequent itemset must also be frequent."
    <span class="src">— mlxtend 공식 문서 · <a href="https://rasbt.github.io/mlxtend/user_guide/frequent_patterns/apriori/" target="_blank" rel="noopener">apriori</a></span>
  </blockquote>

  <h3 class="step">테스트 — min_support 0.01, lift 상위 규칙</h3>
  <pre><code class="language-python"># path : .study/test/practice07_assoc/practice07_runner.py §03 (발췌)
from mlxtend.frequent_patterns import apriori, association_rules

fi = apriori(onehot, min_support=0.01, use_colnames=True)
rules = association_rules(fi, metric="confidence", min_threshold=0.20)
rules.sort_values("lift", ascending=False).head(10)   # lift 상위</code></pre>
  <div class="terminal">
    <div class="terminal-header">practice07_runner.py §03 · apriori + association_rules — lift 상위 10 규칙 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_03@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT</span>
    min_support 0.01 에서 빈발 itemset 333개 → 규칙 234개가 나왔다. lift 최고 규칙은
    <strong>{citrus fruit, other vegetables} → {root vegetables}</strong>(support 0.0104·confidence 0.359·<strong>lift 3.295</strong>).
    상위 규칙이 대부분 채소류(root vegetables·other vegetables) 조합인 게 눈에 띈다 — 신선식품을 함께 담는 장바구니다.
    한편 support 최고 규칙은 {other vegetables}→{whole milk}(support 0.0748)로, 인기 품목 조합은 흔하지만 lift 는 낮다.
  </div>

  <div class="bridge">
    <strong>여기서 멈칫했다</strong> — 234개라는 규칙 수는 <code>min_support</code>를 0.01로 정했기 때문에 나온 값이다.
    그 임계값을 다르게 잡았다면? 0.005 였다면, 0.05 였다면 규칙은 몇 개가 됐을까? 임계값은 무엇을 기준으로 정하나?
  </div>
</section>

<!-- ===================== CH 07 ===================== -->
<section id="ch7">
  <h2 class="chap"><span class="num">CH 07</span>임계값을 어떻게 정하나<a href="#ch7" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    <code>min_support</code>를 올리면 통과하는 빈발 itemset 이 줄고, 그로부터 만들어지는 규칙도 단조 감소할 것이다.
    너무 낮으면 규칙이 급증해 해석 불가, 너무 높으면 0개로 소멸 — 임계값은 그 사이에서 타협하는 손잡이라는 가설이다.
    0.005 → 0.01 → 0.02 → 0.05 로 올리며 itemset·규칙 수를 센다.
  </div>

  <h3 class="step">테스트 — 임계값 스윕</h3>
  <div class="terminal">
    <div class="terminal-header">practice07_runner.py §04 · min_support 0.005~0.05 스윕 — itemset/규칙 수 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_04@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_04@@" alt="min_support에 따른 빈발 itemset 수와 규칙 수 (로그 스케일)">
    <figcaption>그림 3 · min_support↑ → 빈발 itemset·규칙 수가 로그 스케일에서도 가파르게 급감</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">가설 통과</span>
    빈발 itemset 은 <strong>1001 → 333 → 122 → 31</strong>, 규칙 수는 <strong>892 → 234 → 73 → 6</strong>으로
    임계값이 오를수록 단조 급감했다. 0.005 의 892개 규칙은 사람이 다 읽을 수 없고, 0.05 의 6개는 너무 빈약하다.
    임계값은 "해석 가능한 규칙 수"와 "충분한 거래 빈도"가 만나는 지점에서 타협하는 손잡이였다 —
    이 데이터에선 0.01~0.02 가 그 균형점이다.
  </div>

  <div class="callout">
    <span class="label">함정</span>
    support 만 보면 인기 품목 쌍이 무조건 상위에 온다(흔하니까). 하지만 그건 "둘이 정말 관련 있어서"가 아니라
    "둘 다 워낙 자주 팔려서"일 수 있다. CH 05에서 본 lift 가 이 함정을 가려내며, 다음 챕터의 추천이 그것을 활용한다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 규칙 수는 임계값으로 조절했고, lift 의 의미는 CH 05에서 분해했다.
    이제 그 lift 를 실제로 써 본다 — 한 품목을 넣으면 무엇을 추천해야 하나? confidence 정렬과 lift 정렬은 어떻게 갈리나?
  </div>
</section>

<!-- ===================== CH 08 ===================== -->
<section id="ch8">
  <h2 class="chap"><span class="num">CH 08</span>의미 — lift 로 만든 추천과 confidence 의 함정<a href="#ch8" class="anchor-link">#</a></h2>

  <h3 class="step">학습 → 가설</h3>
  <p>CH 05에서 lift 가 "독립 기대치 대비 배수"임을 분해했다. 추천은 그 lift 를 쓰는 일이다 —
  한 품목을 넣고 후행 품목을 <code>confidence</code> 순으로 줄 세울지, <code>lift</code> 순으로 줄 세울지에 따라
  결과가 갈린다. confidence 는 절대 비율이라 흔한 품목이 위로 오고, lift 는 흔함을 보정한다.</p>
  <div class="qbox">
    <span class="label">가설</span>
    추천은 lift 가 높은 후행 품목을 고르면 된다. lift 가 confidence 의 "흔함 보정판"이라면,
    한 품목을 넣었을 때 lift 순 추천은 단순 인기 품목이 아니라 <strong>그 품목과 진짜 관련 있는 품목</strong>을 집어낼 것이다.
  </div>

  <blockquote class="cite">
    "A lift value greater than 1 indicates that the two items occur together more often
    than would be expected if they were statistically independent."
    <span class="src">— mlxtend 공식 문서 · <a href="https://rasbt.github.io/mlxtend/user_guide/frequent_patterns/association_rules/" target="_blank" rel="noopener">association_rules (lift 해석)</a></span>
  </blockquote>

  <h3 class="step">테스트 — 규칙 분포와 lift 순 추천</h3>
  <p>전체 규칙을 support–confidence 평면에 흩뿌리고 lift 로 색을 입힌 뒤, 한 품목을 넣어 lift 순으로 추천한다.</p>
  <div class="terminal">
    <div class="terminal-header">practice07_runner.py §05 · 규칙 산점도 + recommend(lift 정렬) — 추천 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_05@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_05@@" alt="규칙 support vs confidence 산점도, 색은 lift">
    <figcaption>그림 4 · 규칙 분포 — 오른쪽 위(높은 support·confidence)이면서 진한 색(높은 lift)이 좋은 규칙</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">가설 통과</span>
    <code>whole milk</code>를 산 고객에게 추천된 1순위는 lift 1.572 의 <strong>yogurt</strong>,
    <code>yogurt</code>에는 lift 2.000 의 <strong>tropical fruit</strong>가 1순위로 나왔다.
    confidence 만 보면 whole milk(0.402)가 더 높지만, "whole milk 는 원래 다 사는 흔한 품목"이라
    lift 로 보정하면 순위가 내려간다 — lift 가 "흔함의 착시"를 걷어낸 것이다. 추천은 lift 정렬이 정답이었다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 규칙은 "A→B" 쌍 단위 관계다. 그런데 한 발 물러서서
    <em>장바구니 자체를 유형별로 묶을</em> 수는 없을까? 규칙(쌍)이 아니라 거래(바구니)를 군집화하면 고객 세그먼트가 보인다.
  </div>
</section>

<!-- ===================== CH 09 ===================== -->
<section id="ch9">
  <h2 class="chap"><span class="num">CH 09</span>한 발 더 — KMeans 로 장바구니 세그먼트<a href="#ch9" class="anchor-link">#</a></h2>

  <h3 class="step">학습 → 가설</h3>
  <p>연관규칙이 "품목 쌍의 관계"라면, <strong>클러스터링</strong>은 "거래 전체의 닮음"을 본다.
  상위 20품목의 one-hot 벡터를 특성으로 KMeans 를 돌리면, 비슷한 품목 조합을 담은 거래끼리 같은 군집에 모인다.
  과제 7번(다른 분석으로 확장)의 비지도학습 갈래다.</p>
  <div class="qbox">
    <span class="label">가설</span>
    거래를 KMeans(k=4)로 묶으면, 각 군집의 중심(평균 구매율)에서 "음료 중심 바구니", "유제품 바구니",
    "신선식품 바구니" 같은 <strong>해석 가능한 세그먼트</strong>가 드러날 것이다.
  </div>

  <blockquote class="cite">
    "The KMeans algorithm clusters data by trying to separate samples in n groups of equal variance,
    minimizing a criterion known as the inertia or within-cluster sum-of-squares."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/clustering.html#k-means" target="_blank" rel="noopener">K-means clustering</a></span>
  </blockquote>

  <h3 class="step">테스트 — k=4 군집과 대표 품목</h3>
  <div class="terminal">
    <div class="terminal-header">practice07_runner.py §06 · KMeans(k=4) — 군집별 대표 품목·inertia · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_06@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_06@@" alt="KMeans 거래 세그먼트 산점도">
    <figcaption>그림 5 · KMeans 거래 세그먼트 — 상위 2품목(whole milk·other vegetables) 축으로 본 군집 분리</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">가설 통과</span>
    k=4 군집은 각각 <strong>soda 중심(군집0)</strong>, <strong>whole milk 중심(군집1)</strong>,
    <strong>other vegetables 중심(군집2)</strong>, 그리고 인기 품목이 없는 <strong>희소 바구니(군집3, n=5017)</strong>로 차이가 났다.
    상위 품목 하나가 군집을 정의하는(중심값 1.00) 구조 — 즉 "그 품목을 산 거래" 묶음이다. 연관규칙(쌍)과
    클러스터링(거래 묶음)은 같은 데이터를 다른 각도에서 보는 셈이다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 분포 불균등(CH03)·정의(CH04)·직관(CH05)·규칙(CH06)·임계값(CH07)·lift 추천(CH08)·세그먼트(CH09)를 모두 거쳤다.
    이제 출발 의문 "함께 산다를 무엇으로 재나"로 돌아가, 과제 보고서 문항에 답하며 글을 닫는다.
  </div>
</section>

<!-- ===================== CH 10 ===================== -->
<section id="ch10">
  <h2 class="chap"><span class="num">CH 10</span>정리 — 정의와 과제 보고서 회수<a href="#ch10" class="anchor-link">#</a></h2>

  <h3 class="step">최종 결론 — 출발 의문 회수</h3>
  <div class="keypoint">
    <span class="label">FINAL CONCLUSION</span>
    CH 01의 질문 "'함께 산다'를 무엇으로 재나"의 답: <strong>지지도(얼마나 자주 함께 나타나나)·
    신뢰도(A를 산 사람 중 B도 산 비율)·향상도(우연 대비 몇 배나 함께 사나)</strong> 세 수다.
    이 정의는 손 계산과 mlxtend 가 정확히 일치(CH04)했고, 독립 기대치 대비 배수로 lift 를 분해했으며(CH05),
    apriori 로 234개 규칙을 뽑아(CH06), 임계값이 규칙 수를 1001→31 itemset 으로 좌우하며(CH07),
    lift 가 "흔함의 착시"를 걷어내 추천을 만들고(CH08), KMeans 가 같은 데이터를 거래 묶음으로 재해석(CH09)했다.
    품목 분포는 지니계수 0.6331의 쏠림(CH03)이라, 인기 품목의 support 우위가 곧 관련성은 아니라는 점이 lift 의 필요성을 받쳐 줬다.
  </div>

  <h3 class="step">과제 보고서 문항 회수</h3>
  <table>
    <thead><tr><th>보고서 문항</th><th>실측 결과</th></tr></thead>
    <tbody>
      <tr><td>사용 데이터셋</td><td>shop_groceries.csv (Groceries 장바구니 거래)</td></tr>
      <tr><td>전체 거래 수</td><td>9,835건</td></tr>
      <tr><td>전체 상품 수</td><td>169종</td></tr>
      <tr class="hl"><td>가장 많이 판매된 상품</td><td>whole milk (support 0.2555)</td></tr>
      <tr><td>품목 분포 불균등</td><td>Top4 점유율 18.31%, 지니계수 0.6331 (균등 0.59% 대비 whole milk 9.8배)</td></tr>
      <tr><td>생성 규칙 수</td><td>234개 (min_support 0.01, confidence ≥ 0.20)</td></tr>
      <tr><td>최고 support 규칙</td><td>{other vegetables} → {whole milk} (0.0748)</td></tr>
      <tr><td>최고 confidence 규칙</td><td>{citrus fruit, root vegetables} → {other vegetables} (0.586)</td></tr>
      <tr class="hl"><td>최고 lift 규칙</td><td>{citrus fruit, other vegetables} → {root vegetables} (lift 3.295)</td></tr>
      <tr><td>추천 시스템 결과</td><td>whole milk→yogurt(1순위), yogurt→tropical fruit(1순위) — lift 정렬</td></tr>
      <tr><td>비즈니스 활용</td><td>신선식품(채소류) 교차 진열·번들, 인기 품목 옆 lift 높은 품목 배치</td></tr>
    </tbody>
  </table>

  <h3 class="step">한 문장으로</h3>
  <div class="keypoint">
    <span class="label">ONE-LINER</span>
    "함께 산다"는 직관의 실체는 — <strong>지지도로 빈도를 재고, 신뢰도로 방향을 재고, 향상도로
    '우연이 아님'을 가려내는 일</strong>이다. 그래서 좋은 규칙은 support 가 충분하고 lift 가 1을 확실히 넘는 규칙이며,
    추천은 confidence 가 아니라 lift 로 줄 세워야 흔함의 착시를 피한다.
  </div>

  <div class="ref-chain">
    <p class="ref-title">📚 전체 근거 출처</p>
    <ol>
      <li><strong>공식 문서</strong>
        <a href="https://rasbt.github.io/mlxtend/user_guide/frequent_patterns/apriori/" target="_blank" rel="noopener">mlxtend · apriori</a>,
        <a href="https://rasbt.github.io/mlxtend/user_guide/frequent_patterns/association_rules/" target="_blank" rel="noopener">association_rules</a>(support/confidence/lift 정의),
        <a href="https://scikit-learn.org/stable/modules/clustering.html#k-means" target="_blank" rel="noopener">scikit-learn · K-means</a>.</li>
      <li><strong>데이터셋</strong>
        <code>../ml_workspace/from_colab/0605-s/shop_groceries.csv</code> (Groceries 거래 9835건·169품목),
        과제 정의 <code>연관규칙분석_실습문제.txt</code>(실습문제 1~7).</li>
      <li><strong>강의자료</strong>
        <code>7_머신러닝_비지도학습알고리즘.pdf</code> (연관규칙·클러스터링 배경지식).</li>
      <li><strong>실행 검증</strong>
        <code>.study/test/practice07_assoc/practice07_runner.py §00~§07</code>
        → <code>logs/*.txt</code>, <code>charts/*.png</code> (고정 시드 42, 재현 가능).</li>
    </ol>
  </div>

  <div class="bridge">
    <strong>도구 메모</strong> — 연관규칙 계산은 mlxtend 0.25.0(apriori·association_rules)을 사용했고,
    support·confidence·lift 정의는 거래 리스트로 직접 계산해 mlxtend 값과 일치함을 확인했다(CH03).
    과제 7번의 확장 후보(UCI Online Retail)는 같은 파이프라인으로 적용 가능하다.
  </div>
</section>
</main>

<footer>
  <p>SK 네트웍스 AI Family 32기 · 머신러닝 실습7(과제) 연관규칙분석 (2026-06-05)</p>
  <p>모든 터미널 출력은 <code>.study/test/practice07_assoc/practice07_runner.py</code> 실제 실행 결과이며,
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
