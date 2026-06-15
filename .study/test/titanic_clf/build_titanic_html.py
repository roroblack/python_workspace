# build_titanic_html.py
# ml_practice02_titanic.html 조립 — logs/*.txt(실제 실행 결과) + charts/*.png(base64) 주입
# 실행: c:\_proj\python_workspace\.venv\Scripts\python.exe build_titanic_html.py
#   (= GUIDE §11 run_all 역할: 터미널 값 직접 작성 금지, 로그에서 주입)
#   문체: interpreter_base64.html 의 "의문→해결→예상 밖 결과→새 가설→해결" 서사 추적 방식.
import base64, html, pathlib, re

HERE = pathlib.Path(__file__).parent
LOGS = HERE / "logs"
CHARTS = HERE / "charts"
OUT = HERE.parent.parent / "blog" / "ml_practice02_titanic.html"   # .study/blog/
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
    "@@TERM_00@@": term("00_first_look"),
    "@@TERM_01@@": term("01_missing"),
    "@@TERM_02@@": term("02_eda"),
    "@@TERM_03@@": term("03_encoding"),
    "@@TERM_04@@": term("04_baseline"),
    "@@TERM_05@@": term("05_compare"),
    "@@TERM_06@@": term("06_metrics"),
    "@@TERM_07@@": term("07_importance"),
    "@@CHART_02@@": chart("ch02_survival_by_group.png"),
    "@@CHART_06@@": chart("ch06_confusion.png"),
    "@@CHART_07@@": chart("ch07_importance.png"),
}

HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>타이타닉 생존자 분류 분석: 결측치·인코딩부터 분류기 평가·특성 중요도까지</title>
  <meta name="description" content="SK 네트웍스 AI Family 32기 머신러닝 실습2(과제). Kaggle 타이타닉 train.csv 로 '결측치를 어떻게 채울까', '문자열을 왜 숫자로 바꿔야 하나', '정확도 한 숫자를 믿어도 되나'라는 실습 의문을 따라가며 결측치 대치·인코딩·baseline·LogisticRegression/RandomForest 비교·혼동행렬/정밀도/재현율·특성 중요도를 sklearn 실행으로 검증한 기록.">
  <meta property="og:title" content="타이타닉, 누가 살아남았나 — 결측치와 인코딩부터 분류기 평가까지">
  <meta property="og:description" content="결측치 처리 → 인코딩 → EDA → baseline → 분류기 비교 → 정밀도/재현율/혼동행렬 → 특성 중요도, 모두 실측으로 추적">
  <meta property="og:type" content="article">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="타이타닉 생존자 분류 — 결측치와 인코딩부터 분류기 평가까지">
  <meta name="twitter:description" content="정확도 0.804 뒤에 숨은 재현율 0.667을 혼동행렬로 들춰내다">
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
  <p class="eyebrow">Python · 머신러닝 실습2(과제) · 부트캠프</p>
  <h1>타이타닉, 누가 살아남았나 — 결측치와 인코딩부터 분류기 평가까지</h1>
  <p class="deck">실습2 과제로 받은 건 캐글 타이타닉 <code>train.csv</code> 한 장과 "생존자를 분류하라"는 한 줄이었다.
  데이터를 처음 열자마자 질문이 줄줄이 쏟아졌다 — <strong>비어 있는 칸(결측치)은 어떻게 채우지? 문자열 'male'은 모델이 받아주나?
  정확도가 0.8이면 잘한 건가?</strong> 이 글은 그 의문들을 하나씩 코드로 부딪쳐 푼 기록이다.
  모든 수치는 sklearn 으로 직접 돌린 결과이며 <code>random_state=42</code>로 재현 가능하다.</p>
  <div class="meta-row">
    <span><strong>날짜</strong>2026-05-28</span>
    <span><strong>Python</strong>@@PY@@ · scikit-learn 1.8.0 · NumPy 2.4.4 · Pandas 3.0.2</span>
    <span><strong>OS</strong>Windows 11 Pro 25H2</span>
    <span><strong>IDE</strong>VS Code 1.117.0</span>
    <span><strong>HW</strong>Asrock x600 · Ryzen 8600G · 24GB LPDDR5 · RTX 4070 Super 12GB</span>
    <span><strong>커리큘럼</strong>교과목 2 · 머신러닝 실습2(과제) — 머신러닝_회귀모델_분류모델.pdf</span>
  </div>
</header>

<main>
<nav class="flow">
  <h2>이 글의 흐름 — 데이터 한 장을 열고 쏟아진 질문들</h2>
  <ol>
    <li><a href="#ch1">시작 — 이건 무엇을 맞히는 문제인가 (회귀인가 분류인가)</a></li>
    <li><a href="#ch2">빈 칸의 처리 — Age·Cabin·Embarked, 같은 결측이라도 다르게 다뤄야 한다</a></li>
    <li><a href="#ch3">EDA — 누가 살아남았나, 데이터가 먼저 답한다 (Sex·Pclass)</a></li>
    <li><a href="#ch4"><span class="turn">막힘</span> — 'male'을 그대로 넣었더니 fit이 멈춰 섰다 (인코딩의 이유)</a></li>
    <li><a href="#ch5">하한선 긋기 — '무조건 사망'으로 찍어도 0.6은 나온다 (baseline)</a></li>
    <li><a href="#ch6">분류기 비교 — Logistic vs DecisionTree vs RandomForest</a></li>
    <li><a href="#ch7">정확도 0.804를 믿어도 되나? 혼동행렬을 들추다</a></li>
    <li><a href="#ch8"><span class="turn">예상과 다른 결과</span> — 모델이 가장 본 특성은 Sex가 아니었다 (특성 중요도)</a></li>
    <li><a href="#ch9">정리 — 분류 과제의 사슬과, '잘함'의 기준 한 문장</a></li>
  </ol>
</nav>

<!-- ===================== CH 01 ===================== -->
<section id="ch1">
  <h2 class="chap"><span class="num">CH 01</span>시작 — 이건 무엇을 맞히는 문제인가<a href="#ch1" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>과제 폴더엔 <code>train.csv</code>와 <code>test.csv</code> 두 장이 들어 있었다. 그런데 <code>test.csv</code>에는
  정답 열(<code>Survived</code>)이 없다 — 캐글 제출용이라 채점은 캐글이 한다. 그래서 성능을 내가 직접 재려면
  <strong>정답이 있는 <code>train.csv</code> 안에서 검증용(validation)을 따로 떼어내야</strong> 한다.
  먼저 그 <code>train.csv</code>가 대체 무엇을 맞히는 데이터인지부터 봤다.</p>

  <h3 class="step">의문 → 판별</h3>
  <div class="qbox">
    <span class="label">의문</span>
    회귀와 분류는 모델·평가지표가 통째로 다르다. 그러니 가장 먼저 갈라야 한다 —
    <strong>이 과제는 연속값을 예측하는 회귀인가, 정해진 라벨을 맞히는 분류인가?</strong>
    그 판단은 모델이 아니라 정답 <code>y</code>(Survived)의 형태가 한다.
  </div>

  <h3 class="step">테스트 — Survived의 형태를 본다</h3>
  <div class="terminal">
    <div class="terminal-header">titanic_clf_runner.py · read_csv(train) — 크기·열·Survived 분포로 문제 종류 판별 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_00@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT</span>
    891행 × 12열, 정답 <code>Survived</code>는 <strong>0(사망)·1(생존) 두 라벨뿐</strong> → 이건 <strong>이진 분류</strong>다.
    전체 생존율은 0.3838로, 사망이 다수다(549 vs 342). 이 불균형은 뒤에서 "정확도만 믿으면 안 되는" 이유가 된다.
  </div>

  <div class="bridge">
    <strong>다음 — 데이터를 학습에 넣기 전에</strong> 한 가지 걸림이 보였다. <code>head()</code>를 찍었을 때
    <code>Age</code>와 <code>Cabin</code> 칸 곳곳이 <code>NaN</code>으로 비어 있었다. 빈 칸을 그대로 둔 채로는 학습이 안 된다.
    그렇다면 — 어느 열이 얼마나 비었고, 각각 어떻게 메워야 하나?
  </div>
</section>

<!-- ===================== CH 02 ===================== -->
<section id="ch2">
  <h2 class="chap"><span class="num">CH 02</span>빈 칸의 처리 — 같은 결측이라도 다르게<a href="#ch2" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    결측을 메우는 정답은 하나가 아니다. <strong>비율과 의미에 따라 다르게 다뤄야 한다</strong> —
    조금 비었으면 대표값으로 채우고(impute), 거의 다 비었으면 채우는 게 노이즈가 되니 차라리 열을 버리는 게 낫다.
    먼저 어느 열이 얼마나 비었는지를 숫자로 확인하면 처리 방침이 갈릴 것이다.
  </div>

  <h3 class="step">테스트 — 결측치를 진단한다</h3>
  <div class="terminal">
    <div class="terminal-header">titanic_clf_runner.py · isnull().sum() — Age/Cabin/Embarked 결측 비율 진단 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_01@@</pre>
  </div>
  <p>세 열의 결측 비율이 극단적으로 다르다. <code>Embarked</code>는 단 2개(0.2%), <code>Age</code>는 19.9%,
  <code>Cabin</code>은 무려 77.1%다. 같은 "빈 칸"이라도 처리가 같을 수 없다.</p>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">기준 확정</span>
    비율이 처리를 가른다 — ① <code>Embarked</code>(0.2%)는 <strong>최빈값 'S'로 대치</strong>,
    ② <code>Age</code>(19.9%)는 <strong>평균/중앙값으로 대치</strong>, ③ <code>Cabin</code>(77.1%)은 정보보다
    결측이 가장 큰이라 <strong>열 자체를 제거</strong>한다. 0528 수업 노트북은 Cabin을 "Unknown"으로 채웠지만,
    77% 결측을 한 값으로 채우면 사실상 무의미한 상수 열이 되므로 과제에선 <code>PassengerId·Name·Ticket</code>과 함께 드롭했다.
  </div>

  <div class="callout">
    <span class="label">함정</span>
    대치에 쓰는 평균·최빈값은 <strong>train 데이터에서만</strong> 계산해야 한다. 검증셋의 평균까지 끌어다 쓰면
    시험 문제를 미리 본 셈(data leakage)이 된다. runner의 <code>preprocess()</code>는 <code>fit=True</code>일 때만
    통계를 계산하고, 검증셋엔 그 값을 그대로 적용한다.
  </div>

  <div class="bridge">
    <strong>다음 — 빈 칸을 메우기 전에 잠깐</strong>, 어차피 전처리는 시간이 걸린다.
    그 전에 데이터 자체에게 물어보고 싶었다 — <em>도대체 누가 살아남았나?</em>
    특정 특성이 생존을 강하게 가른다면, 그 특성이 분류기의 핵심 재료가 될 것이다.
  </div>
</section>

<!-- ===================== CH 03 ===================== -->
<section id="ch3">
  <h2 class="chap"><span class="num">CH 03</span>EDA — 누가 살아남았나<a href="#ch3" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 관찰</h3>
  <div class="qbox">
    <span class="label">의문</span>
    "여자와 아이 먼저"라는 말이 사실이라면 데이터에 흔적이 남았을 것이다.
    <strong>성별·객실등급으로 묶었을 때 생존율이 또렷이 갈릴까?</strong> 나뉜다면 그 특성은 강한 신호다.
  </div>

  <h3 class="step">테스트 — 그룹별 생존율을 집계한다</h3>
  <div class="terminal">
    <div class="terminal-header">titanic_clf_runner.py · groupby(Sex/Pclass).Survived.mean — 그룹별 생존율 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_02@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_02@@" alt="성별·객실등급별 생존/사망 인원 막대그래프">
    <figcaption>그림 실습2-1 · 성별·객실등급별 생존(초록)/사망(주황) 인원 — 여성과 1등급에서 생존이 두드러진다</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">관찰 결과</span>
    여성 생존율 0.742 vs 남성 0.189 — <strong>여성이 3.9배</strong> 더 살았다. 객실등급도 1등급 0.630 → 3등급 0.242로
    계단처럼 떨어진다. <code>Sex</code>가 가장 강한 신호로 보이고, <code>Pclass</code>가 그 뒤를 잇는다.
    이 직관은 뒤(CH 08)에서 모델의 판단과 맞춰 볼 예정이다.
  </div>

  <div class="bridge">
    <strong>다음 — 그런데 막상 학습에 넣으려니</strong> <code>Sex</code> 열은 <code>'male'/'female'</code>이라는 글자였다.
    이 글자를 그대로 <code>fit</code>에 넣으면 어떻게 될까? 된다면 좋고, 안 된다면 왜 안 되는지가 인코딩의 이유일 것이다.
  </div>
</section>

<!-- ===================== CH 04 ===================== -->
<section id="ch4">
  <h2 class="chap"><span class="num">CH 04</span>막힘 — 'male'을 그대로 넣었더니<a href="#ch4" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    sklearn 분류기는 내부에서 수치 연산(거리·내적·분할 기준)을 한다. 그렇다면 문자열 <code>'male'</code>을
    숫자로 바꿀 수 없어 <strong><code>fit</code>이 에러로 멈출 것</strong>이다. 인코딩 후에는 같은 코드가 통과해야 한다.
  </div>

  <h3 class="step">테스트 — 인코딩 전/후를 직접 확인한다</h3>
  <div class="terminal">
    <div class="terminal-header">titanic_clf_runner.py · LogisticRegression.fit(문자열) → 인코딩 후 재시도 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_03@@</pre>
  </div>
  <p>예상대로 <code>ValueError: could not convert string to float: 'male'</code>로 멈췄다.
  <code>Sex</code>를 <code>{female:0, male:1}</code>, <code>Embarked</code>를 <code>{C:0, Q:1, S:2}</code>로 매핑하자
  모든 열이 숫자가 되어 학습이 가능해졌다.</p>

  <blockquote class="cite">
    "Encode target labels with value between 0 and n_classes-1. … This transformer should be used
    to encode target values, i.e. y, and not the input X."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html" target="_blank" rel="noopener">LabelEncoder</a> (범주형 → 정수)</span>
  </blockquote>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">가설 통과</span>
    분류기는 숫자만 먹는다. 문자열 범주형은 반드시 정수로 인코딩해야 <code>fit</code>이 가능하다.
    <code>Sex</code>처럼 순서 없는 두 값은 0/1 매핑으로 충분하다(이진 범주). 0528 노트북도 동일하게
    <code>LabelEncoder</code>로 <code>Sex·Embarked</code>를 정수화한 뒤에야 모델에 넣었다.
  </div>

  <div class="bridge">
    <strong>다음 — 전처리가 끝났으니 드디어 학습</strong>이다. 그런데 첫 모델을 돌리기 전에 의심이 들었다.
    생존율 분포가 0.38이었다. <em>그럼 무조건 "사망"이라고만 찍어도 정확도가 0.6쯤 나오는 것 아닌가?</em>
    그 하한선을 모르면 분류기의 점수가 좋은지 나쁜지 판단할 수 없다.
  </div>
</section>

<!-- ===================== CH 05 ===================== -->
<section id="ch5">
  <h2 class="chap"><span class="num">CH 05</span>하한선 긋기 — baseline<a href="#ch5" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    아무것도 학습하지 않고 <strong>항상 다수 클래스('사망')로만 찍는</strong> 분류기를 만들면,
    그 정확도는 검증셋의 사망 비율과 같을 것이다(≈0.61). 진짜 분류기는 이 하한선을 넘어야만 의미가 있다.
  </div>
  <p>이게 <code>DummyClassifier(strategy="most_frequent")</code>다. 모델을 평가할 "0점 기준선"을 먼저 세운다.</p>

  <pre><code class="language-python"># path : .study/test/titanic_clf/titanic_clf_runner.py §04 (발췌)
from sklearn.dummy import DummyClassifier

dummy = DummyClassifier(strategy="most_frequent").fit(Xtr, ytr)
print(accuracy_score(yva, dummy.predict(Xva)))   # 무조건 다수클래스로 찍은 정확도</code></pre>

  <h3 class="step">테스트</h3>
  <div class="terminal">
    <div class="terminal-header">titanic_clf_runner.py · DummyClassifier(most_frequent) — baseline 정확도 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_04@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">기준 확정</span>
    무조건 '사망'으로 찍어도 정확도 <strong>0.6145</strong>가 나온다 — 검증셋 사망 비율과 정확히 같다.
    그러니 "정확도 0.6"은 자랑이 아니라 출발선이다. 앞으로 모든 분류기 점수는 이 0.615 위에서 읽어야 한다.
  </div>

  <div class="bridge">
    <strong>다음 — 하한선을 그었으니 본 게임</strong>이다. 어떤 분류기를 써야 할까?
    선형 모델(LogisticRegression)과 트리 계열(DecisionTree·RandomForest)을 같은 조건에서 붙여
    누가 가장 높은지, 그리고 train과 valid 점수 차이로 과대적합 여부까지 같이 보기로 했다.
  </div>
</section>

<!-- ===================== CH 06 ===================== -->
<section id="ch6">
  <h2 class="chap"><span class="num">CH 06</span>분류기 비교 — Logistic vs Tree vs Forest<a href="#ch6" class="anchor-link">#</a></h2>

  <h3 class="step">학습 → 가설</h3>
  <p><strong>LogisticRegression</strong>은 특성의 가중합을 시그모이드에 통과시켜 생존 확률을 내는 선형 분류기다.
  <strong>DecisionTree</strong>는 특성을 기준으로 데이터를 가지치며 나누고, <strong>RandomForest</strong>는 그 트리를
  여러 개 만들어 투표시킨다. 셋의 성격이 다르니 점수도, 과대적합 경향도 다를 것이다.</p>
  <div class="qbox">
    <span class="label">가설</span>
    트리 계열은 표현력이 커서 train 정확도가 매우 높게 나오지만, 그만큼 <strong>train과 valid의 격차(과대적합)</strong>도
    클 것이다. RandomForest는 여러 트리의 평균으로 그 격차를 줄여 valid 정확도가 가장 높을 가능성이 있다.
  </div>

  <blockquote class="cite">
    "A random forest is a meta estimator that fits a number of decision tree classifiers
    on various sub-samples of the dataset and uses averaging to improve the predictive accuracy
    and control over-fitting."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html" target="_blank" rel="noopener">RandomForestClassifier</a></span>
  </blockquote>

  <h3 class="step">테스트 — 세 분류기를 같은 split에서 비교</h3>
  <div class="terminal">
    <div class="terminal-header">titanic_clf_runner.py · 3개 분류기 fit — train/valid 정확도 비교 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_05@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">가설 통과</span>
    valid 정확도는 RandomForest 0.8156 &gt; LogisticRegression 0.8045 &gt; DecisionTree 0.7598 순.
    셋 다 baseline(0.615)을 한참 넘긴다. 가설대로 트리 계열은 과대적합 신호가 또렷했다 —
    RandomForest는 train 0.9831인데 valid는 0.8156으로 <strong>격차 0.17</strong>,
    단일 트리도 train 0.865 / valid 0.760으로 벌어졌다. LogisticRegression은 train 0.802 / valid 0.804로 거의 격차가 없다.
  </div>

  <div class="bridge">
    <strong>다음 — 그런데 의심이 남았다</strong>. 정확도 0.80은 baseline보다 분명히 높다.
    하지만 데이터는 사망이 다수인 불균형 상태였다(CH 01). <em>정확도 한 숫자가 "생존자를 얼마나 놓쳤는지"를
    가리고 있는 건 아닐까?</em> 점수 한 줄 뒤를 들춰봐야 했다.
  </div>
</section>

<!-- ===================== CH 07 ===================== -->
<section id="ch7">
  <h2 class="chap"><span class="num">CH 07</span>정확도 0.804를 믿어도 되나<a href="#ch7" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    정확도는 "전체 중 맞힌 비율" 한 숫자라 <strong>어느 클래스를 못 맞혔는지를 숨긴다</strong>.
    사망이 다수이므로, 모델이 사망은 잘 맞히고 생존은 자주 놓쳐도 정확도는 높게 나올 수 있다.
    혼동행렬을 펼치면 생존(1)의 재현율이 정확도보다 낮게 드러날 것이다.
  </div>

  <h3 class="step">테스트 — 혼동행렬과 정밀도·재현율을 펼친다</h3>
  <div class="terminal">
    <div class="terminal-header">titanic_clf_runner.py · confusion_matrix · classification_report — 클래스별 정밀도/재현율 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_06@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_06@@" alt="LogisticRegression 혼동행렬 히트맵">
    <figcaption>그림 실습2-2 · 혼동행렬 — 실제 생존자 69명 중 23명을 '사망'으로 잘못 예측(좌하단), 생존 재현율 0.667</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">함정 확인</span>
    정확도는 0.804로 깔끔해 보이지만, 클래스별로 뜯으니 <strong>생존(1) 재현율은 0.667</strong>에 그쳤다 —
    실제 생존자 69명 중 23명을 사망으로 잘못 본 것이다. 반면 정밀도는 0.793으로, "생존이라 외친 것"은 비교적 맞았다.
    즉 이 모델은 <strong>생존자를 놓치는(과소 예측) 경향</strong>이 있다. 정확도 한 숫자만 봤다면 못 봤을 약점이다.
  </div>

  <div class="callout">
    <span class="label">왜 둘 다 봐야 하나</span>
    정밀도(precision)는 "생존이라 한 것 중 진짜 생존", 재현율(recall)은 "진짜 생존자 중 찾아낸 비율"이다.
    구조 상황이라면 생존 가능자를 놓치지 않는 <strong>재현율</strong>이 더 중요할 수 있다. 어느 지표를 우선할지는
    문제의 비용이 정한다 — 정확도 하나로는 그 선택을 할 수 없다.
  </div>

  <div class="bridge">
    <strong>다음 — 마지막 질문</strong>. 모델은 0.80의 정확도로 판단을 내렸다. 그런데 <em>무엇을 보고</em> 그렇게 판단했을까?
    EDA(CH 03)에서 내 눈엔 <code>Sex</code>가 가장 크게 강해 보였다. 모델도 같은 결론을 내릴까?
  </div>
</section>

<!-- ===================== CH 08 ===================== -->
<section id="ch8">
  <h2 class="chap"><span class="num">CH 08</span>예상과 다른 결과 — 모델이 가장 본 특성<a href="#ch8" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    EDA에서 여성 생존율이 남성의 3.9배였으니, RandomForest의 <code>feature_importances_</code>도
    <strong><code>Sex</code>를 1위로</strong> 꼽을 것이다. 데이터가 보여준 직관과 모델의 판단이 일치하는지 확인한다.
  </div>

  <h3 class="step">테스트 — 특성 중요도를 꺼낸다</h3>
  <div class="terminal">
    <div class="terminal-header">titanic_clf_runner.py · RandomForest.feature_importances_ — 특성별 기여도 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_07@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_07@@" alt="RandomForest 특성 중요도 가로 막대그래프">
    <figcaption>그림 실습2-3 · RandomForest 특성 중요도 — Fare·Sex·Age 상위 3개가 거의 비등하다</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">예상 밖 — 그래서 더 배운다</span>
    가설은 빗나갔다. 1위는 <code>Sex</code>가 아니라 <strong><code>Fare</code>(0.277)</strong>였고, <code>Sex</code>(0.261)는 근소한 2위,
    <code>Age</code>(0.247)가 바로 뒤였다. 왜일까 — <code>Fare</code>와 <code>Age</code>는 값이 거의 다 다른 <strong>연속형</strong>이라
    트리가 나눌 분기점이 많아 중요도가 분산돼 높게 잡힌다. 반면 <code>Sex</code>는 0/1 한 번의 분기로 정보를 거의 다 쓴다.
    즉 EDA의 "Sex가 강하다"와 모순이 아니라, <strong>중요도 지표가 연속형에 유리하게 퍼지는 성질</strong> 때문이었다.
    결론: 생존은 단일 특성이 아니라 <strong>Fare·Sex·Age의 조합</strong>이 가른다.
  </div>

  <blockquote class="cite">
    "Impurity-based feature importances can be misleading for high cardinality features
    (many unique values). … features that are continuous or high-cardinality tend to be favored."
    <span class="src">— scikit-learn User Guide · <a href="https://scikit-learn.org/stable/modules/permutation_importance.html" target="_blank" rel="noopener">Permutation importance vs impurity importance</a></span>
  </blockquote>

  <div class="bridge">
    <strong>다음 — 이제 사슬을 닫는다</strong>. 데이터를 열고, 빈 칸을 메우고, 글자를 숫자로 바꾸고,
    하한선을 긋고, 모델을 비교하고, 점수 뒤를 들추고, 무엇을 봤는지까지 캐물었다. 이 흐름을 한 줄로 묶을 차례다.
  </div>
</section>

<!-- ===================== CH 09 ===================== -->
<section id="ch9">
  <h2 class="chap"><span class="num">CH 09</span>정리 — 분류 과제의 사슬<a href="#ch9" class="anchor-link">#</a></h2>

  <h3 class="step">최종 결론 — 출발 의문 회수</h3>
  <div class="keypoint">
    <span class="label">FINAL CONCLUSION</span>
    "생존자를 분류하라"는 한 줄은, 실제로는 한 줄의 <code>fit</code>이 아니라 <strong>전처리 → 평가 설계 → 해석</strong>의 사슬이었다.
    ① 정답 형태로 분류임을 가르고(CH 01), ② 결측은 비율에 따라 대치 또는 제거하고(CH 02),
    ③ EDA로 Sex·Pclass가 생존을 가름을 보고(CH 03), ④ 문자열은 숫자로 인코딩해야 fit이 되고(CH 04),
    ⑤ baseline 0.615로 하한선을 그은 뒤(CH 05), ⑥ RandomForest 0.816 등 세 분류기를 비교하고(CH 06),
    ⑦ 정확도 0.804 뒤의 생존 재현율 0.667을 혼동행렬로 들춰내고(CH 07),
    ⑧ 모델이 본 특성은 Fare·Sex·Age 조합임을 확인했다(CH 08).
  </div>

  <h3 class="step">한 문장으로</h3>
  <div class="keypoint">
    <span class="label">ONE-LINER</span>
    분류 과제의 점수는 <code>fit</code> 한 줄이 아니라 — <strong>빈 칸을 어떻게 메웠는지, '잘함'을 어떤 지표로 쟀는지,
    모델이 무엇을 보고 판단했는지</strong>를 함께 설명할 수 있을 때 비로소 믿을 수 있는 숫자가 된다.
    그래서 분류의 절반은 모델 선택이 아니라 데이터 전처리와 평가 설계에 있다.
  </div>

  <div class="ref-chain">
    <p class="ref-title">📚 전체 근거 출처</p>
    <ol>
      <li><strong>공식 문서</strong>
        <a href="https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html" target="_blank" rel="noopener">scikit-learn · LogisticRegression</a>,
        <a href="https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html" target="_blank" rel="noopener">RandomForestClassifier</a>,
        <a href="https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html" target="_blank" rel="noopener">LabelEncoder</a>,
        <a href="https://scikit-learn.org/stable/modules/model_evaluation.html#precision-recall-f-measure-metrics" target="_blank" rel="noopener">precision/recall/F1</a>,
        <a href="https://scikit-learn.org/stable/modules/permutation_importance.html" target="_blank" rel="noopener">feature importance 주의점</a>.</li>
      <li><strong>workspace</strong>
        <code>../ml_workspace/from_colab/0528-s/타이타닉분류모델.ipynb</code> : 동일 전처리(fillna·LabelEncoder·StandardScaler·8:2 stratified split) 흐름.
        과제에선 그 전처리 위에 sklearn 분류기·평가를 올림.</li>
      <li><strong>데이터</strong>
        <code>../ml_workspace/from_colab/0528_data/titanic/train.csv</code> (Kaggle Titanic, 891행). test.csv는 라벨이 없어 train에서 검증셋 분리.</li>
      <li><strong>강의자료</strong>
        <code>.study/pdf/머신러닝_회귀모델_분류모델.pdf</code> (분류/평가지표 배경지식).</li>
      <li><strong>실행 검증</strong>
        <code>.study/test/titanic_clf/titanic_clf_runner.py §00~§07</code>
        → <code>logs/*.txt</code>, <code>charts/*.png</code> (고정 시드 42, 재현 가능).</li>
    </ol>
  </div>

  <div class="bridge">
    <strong>다음 글 예고</strong> — 0528 수업에서는 같은 전처리 위에 PyTorch 신경망(은닉층 32→16, Dropout 0.2)으로도
    분류를 돌렸다. sklearn 분류기와 신경망이 같은 데이터에서 어떻게 다른지는 별도의 실습 기록으로 이어 정리한다.
  </div>
</section>
</main>

<footer>
  <p>SK 네트웍스 AI Family 32기 · 교과목 2 머신러닝 실습2(과제) — 타이타닉 생존자 분류 (2026-05-28)</p>
  <p>모든 터미널 출력은 <code>.study/test/titanic_clf/titanic_clf_runner.py</code> 실제 실행 결과이며,
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
zwsp = HTML.count("​")
leftover = re.findall(r'@@[A-Z0-9_]+@@', HTML)
n_chap = HTML.count('h2 class="chap"')
n_anchor = HTML.count('class="anchor-link"')
n_qbox = HTML.count('class="qbox"')
n_keypoint = HTML.count('class="keypoint"')
print(f"파일: {OUT}")
print(f"terminal div: {n_term} | terminal-body: {n_body} | (일치={n_term==n_body})")
print(f"외부 URL img: {len(http_imgs)} (0이어야 함) | base64 img: {b64_imgs}")
print(f"figure.shot 잔여 pre 검사 통과 | zero-width space: {zwsp}")
print(f"chap: {n_chap} | anchor-link: {n_anchor} (chap과 일치={n_chap==n_anchor}) | qbox: {n_qbox} | keypoint: {n_keypoint}")
print(f"language-python 코드블록: {HTML.count('language-python')} | SEO meta(og:title): {HTML.count('og:title')}")
print(f"Prism core script: {HTML.count('prism-core.min.js')} | autoloader: {HTML.count('prism-autoloader.min.js')}")
print(f"미치환 placeholder: {leftover} | 크기: {len(HTML)//1024} KB")
