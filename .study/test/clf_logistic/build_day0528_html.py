# build_day0528_html.py
# day0528_classification_logistic.html 조립 — logs/*.txt(실제 실행 결과) + charts/*.png(base64) 주입
# 실행: c:\_proj\python_workspace\.venv\Scripts\python.exe build_day0528_html.py
#   (= GUIDE §11 run_all 역할: 터미널 값 직접 작성 금지, 로그에서 주입)
#   문체: interpreter_base64.html / day0527_ml_intro.html 의 "의문→해결→새 의문" 서사 추적 방식.
import base64, html, pathlib, re

HERE = pathlib.Path(__file__).parent
LOGS = HERE / "logs"
CHARTS = HERE / "charts"
OUT = HERE.parent.parent / "blog" / "day0528_classification_logistic.html"   # .study/blog/
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
    "@@TERM_00@@": term("00_task_kind"),
    "@@TERM_01@@": term("01_linear_on_labels"),
    "@@TERM_02@@": term("02_sigmoid"),
    "@@TERM_03@@": term("03_decision_boundary"),
    "@@TERM_04@@": term("04_multiclass"),
    "@@TERM_05@@": term("05_metrics_trap"),
    "@@CHART_01@@": chart("ch01_linear_vs_logistic.png"),
    "@@CHART_02@@": chart("ch02_sigmoid.png"),
    "@@CHART_03@@": chart("ch03_decision_boundary.png"),
    "@@CHART_05@@": chart("ch05_confusion_matrix.png"),
}

HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>파이썬 머신러닝 분석: 회귀로 분류를 풀 수 있을까 — 로지스틱 회귀가 '회귀'인 이유</title>
  <meta name="description" content="SK 네트웍스 AI Family 32기 머신러닝 Day2. '직선 회귀로 0/1 라벨을 예측하면 왜 안 되나', '이름이 회귀인데 왜 분류기인가', '정확도 98%면 좋은 모델인가'라는 의문을 따라가며 시그모이드·결정경계·softmax 다중분류·혼동행렬·정밀도/재현율을 sklearn 실행으로 검증한 기록.">
  <meta property="og:title" content="파이썬 머신러닝 분석: 회귀로 분류를 풀 수 있을까 — 로지스틱 회귀가 '회귀'인 이유">
  <meta property="og:description" content="직선은 확률을 [0,1] 밖으로 내보낸다 → 시그모이드 → 결정경계 → softmax → 정확도의 함정까지 실측 추적">
  <meta property="og:type" content="article">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="회귀로 분류를 풀 수 있을까 — 로지스틱 회귀가 '회귀'인 이유">
  <meta name="twitter:description" content="[0,1] 이탈 → 시그모이드 → 결정경계 → softmax → 혼동행렬·정밀도·재현율">
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
  <p class="eyebrow">Python · 머신러닝(교과목 2 · 단원 2) Day2 · 부트캠프</p>
  <h1>회귀로 분류를 풀 수 있을까 — 로지스틱 회귀가 '회귀'인 이유</h1>
  <p class="deck">Day1 은 회귀였다. <code>fit</code>이 직선의 계수·절편을 정하고, 그 직선으로 연속값을 예측했다.
  Day2 의 데이터는 정답이 <code>0</code> 아니면 <code>1</code>이다. 그렇다면 단순한 생각 하나 —
  <strong>그 직선 회귀를 0/1 라벨에 그대로 쓰면 안 될까?</strong> 이 글은 그 시도가 어디서 낮아지는지를 보고,
  낮아진 자리를 시그모이드로 메우고, "이름은 회귀인데 왜 분류기인가"를 결정경계로 풀고,
  마지막엔 "정확도 98%면 좋은 모델인가"라는 함정까지 따라간 기록이다.
  모든 수치는 sklearn 으로 직접 돌린 결과이며 <code>random_state=42</code>로 재현 가능하다.</p>
  <div class="meta-row">
    <span><strong>날짜</strong>2026-05-28</span>
    <span><strong>Python</strong>@@PY@@ · scikit-learn 1.8.0 · NumPy 2.4.4 · Pandas 3.0.2</span>
    <span><strong>OS</strong>Windows 11 Pro 25H2</span>
    <span><strong>IDE</strong>VS Code 1.117.0</span>
    <span><strong>HW</strong>Asrock x600 · Ryzen 8600G · 24GB LPDDR5 · RTX 4070 Super 12GB</span>
    <span><strong>커리큘럼</strong>교과목 2 · 단원 2 · 머신러닝 Day2 — 머신러닝_회귀모델_분류모델.pdf</span>
  </div>
</header>

<main>
<nav class="flow">
  <h2>이 글의 흐름 — 하나의 단순한 시도에서 갈라져 나온 질문들</h2>
  <ol>
    <li><a href="#ch1">시작 — Day1의 회귀를 0/1 라벨에 그대로 써 보면? (먼저 y로 회귀/분류를 가른다)</a></li>
    <li><a href="#ch2"><span class="turn">실패</span> — 직선의 예측이 확률의 영역 [0,1]을 벗어났다</a></li>
    <li><a href="#ch3">메우기 — 직선의 출력을 (0,1)로 가두는 함수, 시그모이드</a></li>
    <li><a href="#ch4"><span class="turn">의문 해소</span> — 이름은 '회귀'인데 왜 분류기인가 (결정경계)</a></li>
    <li><a href="#ch5">한 발 더 — 클래스가 3개라면? 시그모이드를 넘어 softmax</a></li>
    <li><a href="#ch6">정확도 98.8%, 이 한 숫자를 믿어도 되나</a></li>
    <li><a href="#ch7">두 개의 눈 — 정밀도와 재현율은 서로 다른 실수를 잡는다</a></li>
    <li><a href="#ch8">정리 — 회귀에서 분류로, 그리고 '잘함'의 기준</a></li>
  </ol>
</nav>

<!-- ===================== CH 01 ===================== -->
<section id="ch1">
  <h2 class="chap"><span class="num">CH 01</span>시작 — Day1의 회귀를 0/1 라벨에 그대로 써 보면<a href="#ch1" class="anchor-link">#</a></h2>

  <h3 class="step">학습 — 회귀와 분류는 정답 y가 가른다</h3>
  <p>Day1 에서 확인한 것은 한 문장이었다 — "문제의 종류는 정답 <code>y</code>가 결정한다." <code>y</code>가 연속 실수면 회귀,
  정해진 몇 개의 정수 라벨이면 분류다. Day2 의 데이터 두 개를 같은 판별 함수에 넣어 본다. <code>breast_cancer</code>(악성/양성)와
  <code>iris</code>(세 품종)다.</p>
  <div class="terminal">
    <div class="terminal-header">clf_logistic_runner.py §00 · load_breast_cancer/load_iris — y 형태로 분류 판별 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_00@@</pre>
  </div>
  <p>두 데이터 모두 <code>y</code>가 <code>[0 1]</code> 또는 <code>[0 1 2]</code>의 정수 라벨 — 둘 다 분류다. Day1 의 회귀와는 출발선이 다르다.</p>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    그런데 <code>breast_cancer</code>의 <code>y</code>는 단지 <code>0</code>과 <code>1</code>이라는 <em>숫자</em>다.
    그렇다면 Day1 에서 쓴 <code>LinearRegression</code>으로 이 0/1 숫자를 그대로 예측하면 안 될까?
    예측값이 0.5보다 크면 1, 작으면 0으로 잘라 쓰면 분류가 되지 않을까 — 만약 이게 통한다면
    분류를 위해 새 모델을 배울 필요가 없다. 통하는지 직접 본다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — "회귀 직선으로 0/1 라벨을 예측한다"는 이 단순한 가설을
    그대로 코드로 옮겨 본다. 직선이 내놓는 숫자가 정말 '확률'처럼 0과 1 사이에 들어오는지가 관건이다.
  </div>
</section>

<!-- ===================== CH 02 ===================== -->
<section id="ch2">
  <h2 class="chap"><span class="num">CH 02</span>실패 — 직선의 예측이 [0,1]을 벗어났다<a href="#ch2" class="anchor-link">#</a></h2>

  <h3 class="step">테스트 — 0/1 라벨에 직선을 맞춘다</h3>
  <p>분리력이 큰 특성 하나(<code>worst concave points</code>)로 <code>LinearRegression</code>을 0/1 라벨에 적합시키고,
  예측값의 범위를 본다. 가설이 통하려면 예측이 모두 [0,1] 안에 들어와야 한다.</p>

  <pre><code class="language-python"># path : .study/test/clf_logistic/clf_logistic_runner.py §01 (발췌)
from sklearn.linear_model import LinearRegression, LogisticRegression

x = bc.data[:, [27]]          # 특성 1개
y = bc.target.astype(float)   # 0=악성, 1=양성
lin = LinearRegression().fit(x, y)
pred = lin.predict(x)
print(pred.min(), pred.max())              # 직선의 예측 범위
print((pred < 0).sum(), (pred > 1).sum())  # [0,1] 을 벗어난 개수</code></pre>

  <div class="terminal">
    <div class="terminal-header">clf_logistic_runner.py §01 · LinearRegression vs LogisticRegression(0/1 라벨) — 출력 범위 비교 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_01@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_01@@" alt="0/1 라벨에 대한 선형회귀 직선과 로지스틱 곡선 비교">
    <figcaption>그림 0528-1 · 같은 0/1 데이터: 주황 직선은 위아래 점선(0·1)을 뚫고 나가고, 초록 시그모이드는 [0,1] 안에 갇힌다</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">FAILURE → CLUE</span>
    직선의 예측은 최소 <strong>−0.403</strong>, 최대 <strong>1.297</strong> — 0보다 작은 값이 40개, 1보다 큰 값이 88개 나왔다.
    "확률"이라면 음수나 1 초과는 있을 수 없다. 직선은 양 끝으로 무한히 뻗기 때문에 출력을 [0,1] 안에 가둘 방법이 없다.
    그래서 단순 가설은 성립하지 않았다. 그런데 같은 데이터를 <code>LogisticRegression</code>에 넣자 예측 확률은
    <strong>0.256~0.834</strong> — 항상 0과 1 사이였다. <strong>무엇이 출력을 가둔 걸까?</strong>
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 직선의 한계는 "출력을 [0,1] 안에 못 가둔다"는 것이었다.
    로지스틱 회귀는 직선을 버리지 않고, 그 출력을 어떤 함수로 한 번 더 감싸서 (0,1)로 압축한다.
    그 함수의 이름 — 시그모이드를 직접 들여다본다.
  </div>
</section>

<!-- ===================== CH 03 ===================== -->
<section id="ch3">
  <h2 class="chap"><span class="num">CH 03</span>메우기 — 출력을 (0,1)로 가두는 시그모이드<a href="#ch3" class="anchor-link">#</a></h2>

  <h3 class="step">학습 → 가설</h3>
  <p>로지스틱 회귀는 선형식 <code>z = w·x + b</code>를 <strong>그대로 둔다</strong>. 다만 그 <code>z</code>를
  <strong>시그모이드 함수</strong> <code>σ(z) = 1 / (1 + e^(−z))</code>로 한 번 감싼다. 이 함수는 입력이
  −∞이든 +∞이든 출력을 (0,1) 사이로 짓눌러 넣는다. 그래서 "회귀의 직선"은 살아 있되, 그 결과가 "확률"이 된다.</p>
  <div class="qbox">
    <span class="label">가설</span>
    시그모이드가 정말 출력을 가둔다면 — ① <code>z=0</code>일 때 정확히 0.5, ② <code>z</code>가 아무리 커져도 1을 넘지 않고,
    ③ 아무리 작아져도 0 아래로 내려가지 않아야 한다. 세 가지가 모두 성립하는지 수치로 확인한다.
  </div>

  <blockquote class="cite">
    "Logistic regression is named for the function used at the core of the method, the logistic function …
    an S-shaped curve that can take any real-valued number and map it into a value between 0 and 1, but never exactly at those limits."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression" target="_blank" rel="noopener">Logistic regression</a> (로지스틱 함수)</span>
  </blockquote>

  <h3 class="step">테스트 — 시그모이드 값을 직접 찍는다</h3>
  <div class="terminal">
    <div class="terminal-header">clf_logistic_runner.py §02 · sigmoid(z)=1/(1+e^-z) — z=0에서 0.5 · 극단에서도 [0,1] · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_02@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_02@@" alt="시그모이드 곡선">
    <figcaption>그림 0528-2 · 시그모이드 S자 곡선 — z=0에서 0.5(주황 점선), 양 끝에서 1·0에 수렴하되 닿지는 않는다</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT — 가설 통과</span>
    <code>σ(0)=0.5</code>, <code>σ(6)=0.9975</code>, <code>σ(−6)=0.0025</code>, 그리고 극단의 <code>±1e9</code>에서도 1.0·0.0 —
    세 조건이 모두 성립했다. 직선 <code>z = w·x + b</code>는 그대로 두고 시그모이드로 감싸기만 하면,
    CH 02 에서 [0,1]을 뚫고 나가던 출력이 정확히 확률의 영역에 갇힌다. <strong>이것이 로지스틱 회귀의 핵심 장치다.</strong>
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 출력이 확률이 됐다. 그런데 확률은 0.0~1.0 사이의 <em>연속값</em>이다.
    분류는 결국 "이건 0, 저건 1"이라는 <em>이산 결정</em>인데, 연속 확률에서 어떻게 딱 잘라 클래스를 정할까?
    바로 여기서 "이름은 회귀인데 왜 분류기로 쓰이는가"라는 의문이 풀린다.
  </div>
</section>

<!-- ===================== CH 04 ===================== -->
<section id="ch4">
  <h2 class="chap"><span class="num">CH 04</span>의문 해소 — '회귀'인데 왜 분류기인가<a href="#ch4" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">의문</span>
    로지스틱 회귀는 사실 <strong>확률(연속값)을 회귀</strong>한다 — 이름의 '회귀'는 거짓말이 아니다.
    그런데 우리는 이걸 <strong>분류기</strong>로 쓴다. 비밀은 임계값에 있을 것이다 —
    <code>σ(z)=0.5</code>, 즉 <code>z=0</code>인 지점을 경계로 한쪽은 클래스1, 반대쪽은 클래스0으로 가른다면,
    2차원 평면에서 그 경계는 하나의 <strong>직선</strong>으로 나타나야 한다.
  </div>
  <p>특성 2개(<code>mean radius</code>, <code>worst concave points</code>)로 로지스틱 회귀를 학습시키고,
  확률이 0.5가 되는 선 — 결정경계 — 을 평면에 그려 본다.</p>

  <div class="terminal">
    <div class="terminal-header">clf_logistic_runner.py §03 · 2특성 LogisticRegression — 결정경계 z=0 · test 정확도 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_03@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_03@@" alt="로지스틱 회귀 결정경계 등고선">
    <figcaption>그림 0528-3 · 색은 P(양성) 확률의 연속 등고선, 검은 선은 확률 0.5의 결정경계 — 회귀(색)와 분류(검은 선)가 한 그림 안에 있다</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT — 의문 해소</span>
    학습된 선형식은 <code>z = −2.406·x1 + −2.981·x2 + 0.973</code>이고, 결정경계는 그 <code>z=0</code>인 직선이다.
    <strong>모델이 정하는 것(연속 확률)은 회귀이고, 그 확률에 0.5라는 칼을 대는 순간 분류가 된다.</strong>
    그래서 이름은 '회귀'지만 쓰임은 분류기 — 두 정체가 한 그림(그림 0528-3) 안에 공존한다.
    2특성만으로도 test 정확도 0.918 이 나왔다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 지금까지는 클래스가 둘(0/1)이었다. 그래서 경계 하나면 충분했다.
    그런데 <code>iris</code>처럼 클래스가 셋이라면? 시그모이드는 "0이냐 1이냐"의 이진 게이트인데,
    세 갈래는 어떻게 가를까? 노트에 "아이리스는 0·1·2 세 라벨인데 시그모이드 하나로 되나?"라고 적어 둔 의문을 푼다.
  </div>
</section>

<!-- ===================== CH 05 ===================== -->
<section id="ch5">
  <h2 class="chap"><span class="num">CH 05</span>한 발 더 — 클래스가 3개라면, softmax<a href="#ch5" class="anchor-link">#</a></h2>

  <h3 class="step">학습 → 가설</h3>
  <p>시그모이드는 "양성일 확률 하나"를 내놓는 이진 함수다. 클래스가 셋이면 로지스틱 회귀는
  <strong>softmax</strong>로 확장된다 — 각 클래스마다 점수 <code>z_k</code>를 계산하고, 그것을 지수화해 전체로 나눠
  <em>세 확률의 합이 정확히 1</em>이 되게 만든다. 그리고 가장 높은 확률의 클래스를 답으로 고른다.</p>
  <div class="qbox">
    <span class="label">가설</span>
    클래스가 3개면 로지스틱 회귀의 계수는 <code>(3, 특성수)</code> 모양이 되고(클래스마다 한 줄),
    각 표본의 세 클래스 확률을 더하면 1.0이 되어야 한다. <code>iris</code>로 확인한다.
  </div>

  <blockquote class="cite">
    "In the multiclass case, the training algorithm uses the one-vs-rest (OvR) scheme … or
    the multinomial loss; the latter computes probabilities that sum to one across all classes via the softmax function."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html" target="_blank" rel="noopener">LogisticRegression</a> (multiclass / softmax)</span>
  </blockquote>

  <h3 class="step">테스트 — iris 3품종</h3>
  <div class="terminal">
    <div class="terminal-header">clf_logistic_runner.py §04 · iris 3클래스 LogisticRegression — softmax 확률(행 합=1) · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_04@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT — 가설 통과</span>
    계수 shape 는 <code>(3, 4)</code> — 클래스 3개 × 특성 4개로, 클래스마다 한 줄의 선형식을 가진다.
    표본 4개의 세 클래스 확률은 모두 합이 정확히 <strong>1.000</strong>이었다(softmax). test 정확도는 0.933.
    이진 경계 하나로 가르던 시그모이드가, 세 갈래에선 "클래스별 점수 중 최댓값"으로 자연스럽게 확장됐다.
  </div>

  <div class="callout">
    <span class="label">workspace 메모</span>
    이 multiclass·이진 로지스틱은 BigQuery ML 에서도 똑같다 — 구글 ML 실습에서 작성한
    <code>CREATE MODEL ... OPTIONS(model_type='logistic_reg', input_label_cols=['label'])</code>가 바로 이 모델이다.
    방문자가 "구매할지(1)/안 할지(0)"를 예측하는 같은 로지스틱 회귀를 SQL 한 줄로 부르는 것뿐이다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 이진이든 다중이든 분류 모델을 만들었다. 그런데 Day1 의 회귀는
    "잘함"을 R2 하나로 봤다. 분류도 "정확도" 한 숫자면 충분할까? 노트에 "정확도 98%면 끝 아니야?"라고
    적어 둔 그 의심을, 의료 데이터로 직접 검증한다.
  </div>
</section>

<!-- ===================== CH 06 ===================== -->
<section id="ch6">
  <h2 class="chap"><span class="num">CH 06</span>정확도 98.8%, 믿어도 되나<a href="#ch6" class="anchor-link">#</a></h2>

  <h3 class="step">실험 → 관찰</h3>
  <p>전체 특성으로 <code>breast_cancer</code>를 로지스틱 회귀로 분류하고, 먼저 정확도 한 숫자를 본다.
  그 다음 같은 결과를 <strong>혼동행렬(confusion matrix)</strong>로 펼친다 — 정확도가 한 덩어리로 뭉뚱그린 것을,
  "무엇을 무엇으로 착각했는가"의 네 칸으로 분해한다.</p>

  <div class="terminal">
    <div class="terminal-header">clf_logistic_runner.py §05 · breast_cancer LogisticRegression — accuracy · confusion_matrix · classification_report · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_05@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_05@@" alt="혼동행렬 히트맵">
    <figcaption>그림 0528-4 · 혼동행렬 — 대각선(63·106)은 맞힌 것, 비대각선(악성→양성 1건)은 틀린 것. 정확도는 이 네 칸을 한 숫자로 뭉친 것이다</figcaption>
  </figure>

  <h3 class="step">관찰 — 한 숫자가 가린 것</h3>
  <div class="keypoint">
    <span class="label">관찰 결과</span>
    정확도는 <strong>0.988</strong> — 한 숫자만 보면 거의 완벽하다. 하지만 혼동행렬을 펼치니
    "<strong>실제 악성인데 양성이라 판정한 1건</strong>"이 드러났다(<code>[악성][예측:양성]=1</code>).
    암 진단에서 이 1건은 "암 환자를 정상이라 돌려보낸" 가장 위험한 실수다. 정확도 0.988은 이 실수를
    105건의 정답 속에 묻어 버린다. <strong>한 숫자는 '어떤 실수'를 하는지를 말해 주지 않는다.</strong>
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 혼동행렬은 실수의 종류를 보여 줬지만, 네 칸의 숫자를 매번 눈으로
    해석하긴 번거롭다. 이 "놓친 악성"과 "잘못 부른 악성"을 각각 한 비율로 요약하는 두 지표 —
    재현율과 정밀도 — 가 필요하다.
  </div>
</section>

<!-- ===================== CH 07 ===================== -->
<section id="ch7">
  <h2 class="chap"><span class="num">CH 07</span>두 개의 눈 — 정밀도와 재현율<a href="#ch7" class="anchor-link">#</a></h2>

  <h3 class="step">학습 — 서로 다른 실수를 잡는 두 지표</h3>
  <p>같은 혼동행렬을 두 방향으로 읽는다. <strong>재현율(recall)</strong>은 "<em>진짜 악성</em> 중 몇 %를 찾아냈나" —
  놓친 환자(FN)에 민감하다. <strong>정밀도(precision)</strong>는 "<em>악성이라 부른 것</em> 중 몇 %가 진짜였나" —
  헛경보(FP)에 민감하다. 암 진단처럼 놓치면 심각한 문제에선 재현율이, 스팸 분류처럼 헛경보가 거슬리는 문제에선
  정밀도가 더 중요해진다.</p>

  <blockquote class="cite">
    "The precision is the ability of the classifier not to label as positive a sample that is negative,
    and the recall is the ability of the classifier to find all the positive samples."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html" target="_blank" rel="noopener">classification_report</a> (precision / recall)</span>
  </blockquote>

  <h3 class="step">의문 → 관찰</h3>
  <div class="qbox">
    <span class="label">의문</span>
    CH 06 의 <code>classification_report</code> 출력에서 클래스별 정밀도·재현율을 읽으면,
    정확도 0.988 하나로는 보이지 않던 클래스별 강·약점이 드러날 것이다. 특히 "악성을 놓친 1건"이
    재현율 숫자에 어떻게 반영되는지를 본다.
  </div>
  <p>출력(위 §05 터미널)의 악성 클래스 행을 보면 정밀도·재현율이 모두 <code>0.984</code>다.
  악성 64건 중 63건을 찾아 재현율 <code>63/64 = 0.984</code>, 악성이라 부른 64건 중 63건이 진짜라 정밀도도 <code>0.984</code>.
  놓친 1건이 곧 재현율을 1.0에서 0.984로 끌어내린 그 1건이다.</p>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT</span>
    정밀도와 재현율은 같은 결과를 다른 각도에서 본다 — 하나는 "헛부른 것", 하나는 "놓친 것"을 벌한다.
    그래서 분류 평가는 정확도 한 숫자가 아니라 <strong>혼동행렬 → 클래스별 정밀도·재현율 → (둘의 조화평균인) F1</strong>로
    내려가야, 모델이 <em>어떤</em> 실수를 하는지가 보인다. "정확도 98%면 끝"이라는 생각은, 그 8%가 어디서 나는지를 묻지 않은 것이다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 직선의 실패(CH02)에서 시작해 시그모이드(CH03)·결정경계(CH04)·
    softmax(CH05)로 분류기를 세우고, 정확도의 함정(CH06)을 정밀도·재현율(CH07)로 넘었다.
    이제 출발 의문 — "회귀로 분류를 풀 수 있을까" — 로 돌아간다.
  </div>
</section>

<!-- ===================== CH 08 ===================== -->
<section id="ch8">
  <h2 class="chap"><span class="num">CH 08</span>정리 — 회귀에서 분류로, 그리고 '잘함'의 기준<a href="#ch8" class="anchor-link">#</a></h2>

  <h3 class="step">최종 결론 — 출발 의문 회수</h3>
  <div class="keypoint">
    <span class="label">FINAL CONCLUSION</span>
    CH 01 의 질문 "<strong>Day1의 회귀 직선을 0/1 라벨에 그대로 쓸 수 있을까</strong>"의 답:
    <strong>그대로는 안 된다 — 직선의 출력이 확률의 영역 [0,1]을 벗어나기 때문이다(CH02).</strong>
    그러나 직선을 버릴 필요는 없었다. 선형식 <code>z=w·x+b</code>는 그대로 두고 시그모이드로 감싸 출력을 (0,1)로 가두면(CH03),
    그것이 로지스틱 회귀다. 모델이 정하는 것은 <em>확률(회귀)</em>이고, 그 확률에 0.5의 칼을 대면 <em>분류</em>가 된다 —
    이것이 "이름은 회귀, 쓰임은 분류기"의 핵심이었다(CH04). 클래스가 셋 이상이면 softmax 로 확장되고(CH05),
    그 성능은 정확도 한 숫자가 아니라 혼동행렬·정밀도·재현율로 — '어떤 실수를 하는가'까지 — 재야 한다(CH06~07).
  </div>

  <h3 class="step">한 문장으로</h3>
  <div class="keypoint">
    <span class="label">ONE-LINER</span>
    "로지스틱 회귀는 왜 회귀라 불리는데 분류기인가"의 답은 — <strong>직선으로 '확률'을 회귀하고,
    그 확률에 임계값을 그어 '클래스'를 가르기 때문</strong>이다. 그래서 회귀에서 분류로 넘어가는 다리는
    새 모델이 아니라 <em>시그모이드라는 함수 하나</em>였고, 분류를 평가하는 눈은 정확도 하나가 아니라 <em>둘(정밀도·재현율)</em>이었다.
  </div>

  <div class="ref-chain">
    <p class="ref-title">📚 전체 근거 출처</p>
    <ol>
      <li><strong>공식 문서</strong>
        <a href="https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression" target="_blank" rel="noopener">scikit-learn · Logistic regression</a>(로지스틱 함수),
        <a href="https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html" target="_blank" rel="noopener">LogisticRegression</a>(multiclass/softmax),
        <a href="https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html" target="_blank" rel="noopener">classification_report</a>(precision/recall).</li>
      <li><strong>workspace</strong>
        <code>../ml_workspace/from_colab/0528/</code> : Day2 회귀·분류 핸즈온(PyTorch tips 회귀),
        <code>google_ai_ml_engineering/.../bq2.sql</code> : BigQuery ML <code>model_type='logistic_reg'</code> 실제 모델 생성 SQL.</li>
      <li><strong>강의자료</strong>
        <code>.study/pdf/머신러닝_회귀모델_분류모델.pdf</code> (배경지식).</li>
      <li><strong>실행 검증</strong>
        <code>.study/test/clf_logistic/clf_logistic_runner.py §00~§05</code>
        → <code>logs/*.txt</code>, <code>charts/*.png</code> (고정 시드 42, 재현 가능).</li>
    </ol>
  </div>

  <div class="bridge">
    <strong>다음 글 예고</strong> — 로지스틱 회귀는 선형 결정경계였다. 다음 Day3 에서는 경계를 최대 마진으로 긋는
    서포트 벡터 머신(SVM)으로, 그리고 비선형 경계로 들어간다.
  </div>
</section>
</main>

<footer>
  <p>SK 네트웍스 AI Family 32기 · 교과목 2 단원 2 머신러닝 Day2 (2026-05-28)</p>
  <p>모든 터미널 출력은 <code>.study/test/clf_logistic/clf_logistic_runner.py</code> 실제 실행 결과이며,
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
n_chap = HTML.count('h2 class="chap"')
n_qbox = HTML.count('class="qbox"')
n_kp = HTML.count('class="keypoint"')
n_anchor = HTML.count('class="anchor-link"')
print(f"파일: {OUT}")
print(f"terminal div: {n_term} | terminal-body: {n_body} | (일치={n_term==n_body})")
print(f"외부 URL img: {len(http_imgs)} (0이어야 함) | base64 img: {b64_imgs}")
print(f"chap: {n_chap} | qbox: {n_qbox} | keypoint: {n_kp} | anchor: {n_anchor}")
print(f"zero-width space: {zwsp} (0이어야 함)")
print(f"미치환 placeholder: {leftover} | 크기: {len(HTML)//1024} KB")
