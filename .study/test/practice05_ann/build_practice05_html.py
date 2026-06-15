# build_practice05_html.py
# ml_practice05_ann.html 조립 — logs/*.txt(실제 실행 결과) + charts/*.png(base64) 주입
# 실행: c:\_proj\python_workspace\.venv\Scripts\python.exe build_practice05_html.py
#   (= GUIDE §11 run_all 역할: 터미널 값 직접 작성 금지, 로그에서 주입)
#   문체: day0527_ml_intro / ml_practice03_svm_knn_nb 의 "의문→해결→새 의문" 서사 추적 방식.
import base64, html, pathlib, re

HERE = pathlib.Path(__file__).parent
LOGS = HERE / "logs"
CHARTS = HERE / "charts"
OUT = HERE.parent.parent / "blog" / "ml_practice05_ann.html"   # .study/blog/
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
    "@@TERM_01@@": term("01_scaling_effect"),
    "@@TERM_02@@": term("02_grid"),
    "@@TERM_03@@": term("03_pred_actual"),
    "@@TERM_04@@": term("04_compare"),
    "@@CHART_SCALE@@": chart("ch_scaling.png"),
    "@@CHART_HIDDEN@@": chart("ch_hidden.png"),
    "@@CHART_PRED@@": chart("ch_pred_actual.png"),
    "@@CHART_CMP@@": chart("ch_compare.png"),
}

HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>파이썬 머신러닝 ANN 분석: 콘크리트 강도를 신경망으로 예측하고 트리 앙상블과 맞붙이다</title>
  <meta name="description" content="SK 네트웍스 AI Family 32기 머신러닝 실습5(과제). '트리·앙상블로도 풀던 회귀를 굳이 신경망으로?'라는 의문을 따라 콘크리트 압축강도를 MLP로 예측한다. 표준화가 신경망에 필수인 이유, 은닉층 크기·학습률 그리드서치, 예측-실제 잔차, 그리고 같은 데이터에서 RandomForest·GradientBoosting과의 R2 비교까지 sklearn 실측으로 검증한 기록.">
  <meta property="og:title" content="콘크리트 강도를 신경망으로 예측하고 트리 앙상블과 맞붙이다">
  <meta property="og:description" content="MLP 표준화의 필요성, 은닉층·학습률 그리드서치, 예측-실제 잔차, MLP vs RF/GBM R2 비교를 실측으로 추적">
  <meta property="og:type" content="article">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="콘크리트 강도 ANN 예측 + 앙상블 비교">
  <meta name="twitter:description" content="표준화 필요성 → 은닉층·학습률 그리드 → 예측-실제 → MLP vs RF/GBM">
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
  <p class="eyebrow">Python · 머신러닝 실습5(과제) · 부트캠프</p>
  <h1>콘크리트 강도를 신경망으로 예측하고, 트리 앙상블과 맞붙이다</h1>
  <p class="deck">실습5 과제는 인공신경망(ANN)으로 콘크리트 압축강도를 예측하는 회귀였다.
  그런데 출발선에서 의문이 하나 걸렸다 — <strong>트리·앙상블로도 잘 풀던 회귀를 굳이 신경망으로?</strong>
  이 글은 그 의문을 주어로 삼아 — 신경망에 표준화가 왜 '선택'이 아니라 '필수'인지,
  은닉층 크기와 학습률을 그리드서치로 어떻게 골랐는지, 예측이 어디서 빗나가는지,
  그리고 같은 데이터에서 RandomForest·GradientBoosting과 맞붙였을 때 신경망이 유리한 지점과
  치르는 비용이 무엇인지를 하나씩 부딪쳐 본 기록이다.
  과제 colab은 PyTorch로 짰지만, 여기서는 재현 가능한 오프라인 실행을 위해 sklearn
  <code>MLPRegressor</code>로 옮겼고 모든 수치는 <code>random_state=42</code>로 재현된다.</p>
  <div class="meta-row">
    <span><strong>날짜</strong>2026-06-02</span>
    <span><strong>Python</strong>@@PY@@ · scikit-learn 1.8.0 · NumPy 2.4.4 · Pandas 3.0.2</span>
    <span><strong>OS</strong>Windows 11 Pro 25H2</span>
    <span><strong>IDE</strong>VS Code 1.117.0</span>
    <span><strong>HW</strong>Asrock x600 · Ryzen 8600G · 24GB LPDDR5 · RTX 4070 Super 12GB</span>
    <span><strong>커리큘럼</strong>교과목 2 · 단원 2 · 머신러닝 — 머신러닝_알고리즘_앙상블.pdf</span>
  </div>
</header>

<main>
<nav class="flow">
  <h2>이 글의 흐름 — 하나의 의문에서 갈라져 나온 질문들</h2>
  <ol>
    <li><a href="#ch1">시작 — 트리로 풀던 회귀를 왜 신경망으로? (데이터 성격부터 본다)</a></li>
    <li><a href="#ch2">신경망의 구조 — 입력·은닉·출력층과 역전파, 무엇이 직선을 넘게 하나</a></li>
    <li><a href="#ch3">표준화를 안 했더니 MLP 성능이 낮았다</a></li>
    <li><a href="#ch4">튜닝 — 은닉층 크기·학습률 그리드서치, 클수록 좋은 게 아니었다</a></li>
    <li><a href="#ch5">잔차 — 예측은 어디서 빗나가나 (극단 강도의 평균 회귀)</a></li>
    <li><a href="#ch6"><span class="turn">맞대결</span> — 같은 데이터, MLP vs RandomForest vs GradientBoosting</a></li>
    <li><a href="#ch7">왜 트리가 이겼나 — 신경망이 유리한 지점과 치르는 비용</a></li>
    <li><a href="#ch8">정리 — '굳이 신경망?'에 대한 답으로 회수</a></li>
  </ol>
</nav>

<!-- ===================== CH 01 ===================== -->
<section id="ch1">
  <h2 class="chap"><span class="num">CH 01</span>시작 — 트리로 풀던 회귀를 왜 신경망으로<a href="#ch1" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>실습5 과제지는 한 문장으로 시작했다 — "콘크리트 배합 성분과 양생 일수로 압축강도를 예측하는 회귀 모델을
  <strong>인공신경망(ANN)</strong>으로 만드시오." 그런데 바로 앞 실습들에서 같은 종류의 회귀를 결정트리·랜덤포레스트로
  이미 풀어 봤다. 앙상블 강의자료도 "여러 모델의 투표로 정답을 찾는다"는 트리 계열 앙상블을 깊게 다뤘다.
  그러니 신경망 과제를 받자마자 떠오른 건 기술이 아니라 의심이었다.</p>

  <blockquote class="cite">
    "Class MLPRegressor implements a multi-layer perceptron (MLP) that trains using backpropagation
    with no activation function in the output layer … it can also be seen as using the identity function
    as activation function. Therefore, it uses the square error as the loss function."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/neural_networks_supervised.html" target="_blank" rel="noopener">Neural network models (supervised) · Regression</a></span>
  </blockquote>

  <h3 class="step">의문 → 기준</h3>
  <div class="qbox">
    <span class="label">의문</span>
    신경망을 쓸지 말지의 기준은 모델 취향이 아니라 <strong>데이터의 성격</strong>에서 나와야 한다.
    그렇다면 먼저 — 이 콘크리트 데이터는 어떤 회귀인가? 특성은 몇 개이고 스케일은 고른가, 표본은 충분한가.
    그 진단이 "신경망이 이길 자리인지"의 첫 단서가 된다.
  </div>

  <h3 class="step">테스트 — 데이터의 성격을 진단한다</h3>
  <p>과제 데이터 <code>concrete_stg.csv</code>를 그대로 읽어 목표값의 분포와 8개 입력 특성의 스케일을 진단한다.</p>
  <div class="terminal">
    <div class="terminal-header">concrete_stg.csv — 콘크리트 강도 회귀 데이터 성격(분포·특성 스케일) 진단 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_00@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">기준 확정</span>
    1030행 · 연속 목표값(강도 2.33~82.6 MPa) · 8개 수치 특성 회귀다. 특성 범위 폭이 최대 약 14배(cement vs superplastic)로 벌어져 있다 —
    거리·가중합 기반인 신경망이 그대로 먹으면 큰 특성이 학습을 지배한다. 표본이 1030개로 그리 많지 않다는 점도 기억해 둔다.
    이 두 사실(스케일 불균형 · 중간 규모 표본)이 뒤 챕터에서 곧장 발목을 잡는다.
  </div>

  <div class="bridge">
    <strong>그 전에 짚을 것</strong> — "신경망이 트리와 뭐가 다른가"를 알아야 비교가 의미 있다.
    트리는 if-else로 공간을 자르고, 신경망은 층을 쌓아 곡면을 그린다. 그 '층'과 '역전파'가 정확히 무엇을 하는지부터 본다.
  </div>
</section>

<!-- ===================== CH 02 ===================== -->
<section id="ch2">
  <h2 class="chap"><span class="num">CH 02</span>신경망의 구조 — 입력·은닉·출력층과 역전파<a href="#ch2" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>MLP(다층 퍼셉트론)는 세 종류의 층으로 이뤄진다 — <strong>입력층</strong>(특성 8개를 그대로 받음),
  <strong>은닉층</strong>(가중합 뒤 활성함수로 비선형을 만듦), <strong>출력층</strong>(회귀라 활성함수 없이 실수 하나를 냄).
  핵심은 은닉층의 활성함수다. 활성함수가 없으면 층을 아무리 쌓아도 선형 변환의 합성이라 결국 직선 하나로 낮아진다.
  <code>relu</code>·<code>tanh</code> 같은 비선형이 끼어야 비로소 휘어진 곡면을 그릴 수 있다 — 트리가 못 그리는 매끈한 곡면을.</p>
  <p>학습은 <strong>역전파(backpropagation)</strong>로 한다. 예측과 정답의 오차(회귀는 제곱오차)를 각 가중치에 대해 미분해
  기울기를 구하고, 그 반대 방향으로 가중치를 조금씩 옮긴다. "조금씩"의 보폭이 <strong>학습률(learning rate)</strong>이다.
  과제 colab이 PyTorch로 짠 <code>optimizer.zero_grad → loss.backward → optimizer.step</code> 루프가 바로 이것이고,
  sklearn <code>MLPRegressor</code>는 같은 일을 한 줄 <code>fit</code> 안에서 한다.</p>

  <blockquote class="cite">
    "MLP trains using Stochastic Gradient Descent, Adam, or L-BFGS. … Starting from initial random weights,
    multi-layer perceptron (MLP) minimizes the loss function by repeatedly updating these weights."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/neural_networks_supervised.html" target="_blank" rel="noopener">Neural network models — training</a></span>
  </blockquote>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    그렇다면 트리 앙상블로는 다소 거칠던 곡면을, 비선형 은닉층을 가진 MLP는 더 매끈하게 맞출 여지가 있다.
    다만 그 가중합이 공정하려면 입력 특성이 같은 척도여야 한다 — CH 01에서 본 14배 스케일 차이가 그대로면
    신경망은 제 실력을 못 낸다. 이 가설을 다음 챕터에서 '표준화 유무'로 직접 가른다.
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">관찰 결과</span>
    신경망의 표현력은 "비선형 활성함수를 끼운 층의 누적"에서 나오고, 그 학습은 "오차를 미분해 가중치를
    학습률만큼 옮기는 역전파"로 이뤄진다. 즉 신경망의 성능을 좌우하는 손잡이는 <strong>은닉층 구조(폭·깊이)·
    활성함수·학습률</strong>, 그리고 그 모든 것의 전제인 <strong>입력 스케일</strong>이다. 손잡이 중 가장 먼저 만질 것은 스케일이다.
  </div>

  <div class="bridge">
    <strong>첫 손잡이</strong> — 표준화부터 점검한다. 강의자료는 거리·규제 기반 모델에 표준화가 필요하다고 했는데,
    신경망도 그 부류인지 같은 MLP를 '원본 vs 표준화'로 나란히 돌려 R2 차이로 확인한다.
  </div>
</section>

<!-- ===================== CH 03 ===================== -->
<section id="ch3">
  <h2 class="chap"><span class="num">CH 03</span>표준화를 안 하면 MLP 성능이 낮다<a href="#ch3" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    은닉층의 가중합 <code>Σ wᵢxᵢ</code>는 값이 큰 특성에 끌려간다. cement(수백 단위)와 superplastic(한 자리 단위)이
    같은 망에 들어가면 큰 특성이 기울기를 독점해 학습이 한쪽으로 쏠린다. 그러니 <code>StandardScaler</code>로
    모든 특성을 평균0·표준편차1로 맞추면, <strong>같은 데이터·같은 MLP라도 test R2가 올라야 한다.</strong>
  </div>
  <p>과제 colab도 학습 전 Min-Max 정규화를 먼저 했었다. 그 한 줄이 정말 성능을 가르는지, 표준화만 빼고 똑같이 돌려 본다.</p>

  <pre><code class="language-python"># path : .study/test/practice05_ann/practice05_runner.py §01 (발췌)
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

# (1) 스케일링 없이 — 원본 특성을 그대로 MLP에 투입
raw = MLPRegressor(hidden_layer_sizes=(64, 64), activation="relu",
                   max_iter=2000, random_state=42).fit(Xtr, ytr)

# (2) StandardScaler 파이프라인 — 표준화 후 동일 MLP
scaled = make_pipeline(StandardScaler(),
                       MLPRegressor(hidden_layer_sizes=(64, 64), activation="relu",
                                    max_iter=2000, random_state=42)).fit(Xtr, ytr)
print(r2_score(yte, raw.predict(Xte)))      # 스케일링 없음
print(r2_score(yte, scaled.predict(Xte)))   # 표준화 적용</code></pre>

  <h3 class="step">테스트</h3>
  <div class="terminal">
    <div class="terminal-header">practice05_runner.py §01 · MLPRegressor — 표준화 유무 test R2 비교 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_01@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_SCALE@@" alt="MLP 표준화 유무에 따른 test R2 막대 비교">
    <figcaption>그림 P5-1 · 같은 MLP(64-64, relu) — 스케일링 없음 R2 0.839 vs StandardScaler 0.903</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">가설 통과</span>
    스케일링 없음 test R2 <strong>0.8393</strong> → StandardScaler <strong>0.9025</strong>, <strong>+0.0632</strong> 상승.
    표준화는 신경망에서 장식이 아니라 성능의 전제였다. 트리 앙상블이라면 분기 기준이 단조변환에 불변이라 표준화가
    거의 의미 없지만, 가중합·기울기로 학습하는 신경망은 다르다 — 이게 "트리는 안 했는데 신경망은 해야 하는" 첫 차이다.
  </div>

  <div class="callout">
    <span class="label">함정</span>
    표준화는 <strong>train으로만 <code>fit</code></strong>하고 test엔 <code>transform</code>만 해야 한다.
    <code>make_pipeline</code>은 교차검증·예측 시 이 분리를 자동으로 지켜 줘서, test 통계가 train에 새어드는
    누수(data leakage)를 막는다. 그래서 스케일러를 손으로 붙이기보다 파이프라인에 묶었다.
  </div>

  <div class="bridge">
    <strong>다음 손잡이</strong> — 표준화로 바닥은 깔았다. 이제 은닉층을 더 키우거나 학습률을 바꾸면 더 오를까?
    과제의 그리드서치를 sklearn으로 재현해, "클수록 좋다"는 직관이 맞는지 확인한다.
  </div>
</section>

<!-- ===================== CH 04 ===================== -->
<section id="ch4">
  <h2 class="chap"><span class="num">CH 04</span>튜닝 — 은닉층 크기·학습률 그리드서치<a href="#ch4" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>그리드서치는 후보 조합을 격자처럼 깔고 하나도 빼지 않고 다 돌려, 검증 성적이 가장 좋은 조합을 고르는 방법이다.
  꼼꼼하지만 조합이 늘면 시간이 급증한다. 과제 colab은 PyTorch로 Epoch·LR·노드·층·활성함수까지 216개 조합을 돌렸는데,
  여기서는 핵심 축인 <strong>은닉층 크기 5종 × 학습률 2종</strong>을 5-fold 교차검증으로 좁혀 재현했다.</p>
  <div class="qbox">
    <span class="label">의문 → 가설</span>
    은닉 노드를 늘릴수록 표현력이 커지니 단조롭게 좋아질까? 과제 보고서는 "노드 50개 이상이면 과적합·기울기 소실·
    연산 증가"를 경고했다. 그렇다면 가장 큰 (100,100)이 항상 1등은 아닐 것이고, 학습률이 너무 크면 큰 망에서 오히려 흔들릴 것이다.
  </div>

  <h3 class="step">테스트 — 10개 조합을 교차검증으로 줄세운다</h3>
  <div class="terminal">
    <div class="terminal-header">practice05_runner.py §02 · GridSearchCV(MLP) — 은닉층·학습률 5-fold CV R2 정렬 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_02@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_HIDDEN@@" alt="은닉층 구조별 CV R2 막대그래프">
    <figcaption>그림 P5-2 · 은닉층 구조별 최고 CV R2 — 폭을 키우면 오르지만 학습률에 따라 순위가 뒤집힌다</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">관찰 결과</span>
    최고 조합은 <strong>hidden=(100,100), lr=0.001 → CV R2 0.8808</strong>, holdout test R2 <strong>0.9035</strong>.
    그런데 같은 (64,64)라도 lr 0.001은 CV R2 0.8706, lr 0.01은 0.8228로 <strong>학습률이 은닉층 크기보다 순위를 더 흔들었다.</strong>
    큰 망에 큰 학습률을 물리면 보폭이 커서 최저점을 지나쳐 흔들린 것 — "클수록 좋다"가 아니라 "폭은 학습률과 짝을 맞춰야 한다"가 정답이었다.
    과제가 경고한 대로 무작정 키우는 게 답은 아니었다.
  </div>

  <div class="bridge">
    <strong>그래서 의심</strong> — CV R2 0.88, test R2 0.90이면 꽤 높다. 하지만 R2 한 숫자는 "전반적으로 잘 맞는다"만 말한다.
    어디서 틀리는지는 안 보인다. 예측을 실제값과 점으로 찍어, 빗나가는 구간을 직접 들여다본다.
  </div>
</section>

<!-- ===================== CH 05 ===================== -->
<section id="ch5">
  <h2 class="chap"><span class="num">CH 05</span>잔차 — 예측은 어디서 빗나가나<a href="#ch5" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    예측값을 실제값에 대해 산점도로 찍으면, 정확한 모델일수록 점이 <code>y=x</code> 직선에 붙는다.
    표본이 적은 <strong>극단 강도(아주 약하거나 아주 강한 콘크리트)</strong> 구간에서는 점이 선에서 더 벌어질 것이다 —
    데이터가 적은 쪽을 모델이 평균 쪽으로 끌어당겨 예측하는 회귀의 일반적 경향 때문이다.
  </div>
  <p>과제 보고서의 도전 과제 5(실제값-예측값 scatter)와 같은 진단을, best 구조 MLP로 수치까지 붙여 확인한다.</p>

  <h3 class="step">테스트</h3>
  <div class="terminal">
    <div class="terminal-header">practice05_runner.py §03 · MLP 예측 — R2·corr·MAE 및 중간/극단 구간 오차 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_03@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_PRED@@" alt="MLP 실제값 대 예측값 산점도, y=x 기준선">
    <figcaption>그림 P5-3 · 실제값 vs 예측값 — 점들이 y=x 주변에 모이되, 양 끝(극단 강도)에서 더 흩어진다</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">가설 통과</span>
    best MLP test R2 <strong>0.8873</strong>, 상관계수 <strong>0.9436</strong>, MAE <strong>4.12 MPa</strong>.
    여기서 상관계수(0.94)는 "방향이 같이 움직인다"만 말하지 "얼마나 정확히 같은 값인지"는 MAE/MSE가 말한다 —
    둘은 목적이 다른 지표다. 그리고 중간 구간 MAE 4.00 vs 극단 구간 MAE 4.60으로,
    가설대로 <strong>극단 강도에서 오차가 더 크다.</strong> 평균으로 당겨 예측하는 회귀의 한계가 그대로 드러났다.
  </div>

  <div class="bridge">
    <strong>핵심 질문으로</strong> — 표준화하고, 튜닝하고, 잔차까지 봤다. test R2 0.89. 그런데 출발 의문이 아직 남았다 —
    같은 데이터를 트리 앙상블에 그냥 넣으면 몇이 나올까? 신경망이 이 수고를 한 만큼 더 잘했을까?
  </div>
</section>

<!-- ===================== CH 06 ===================== -->
<section id="ch6">
  <h2 class="chap"><span class="num">CH 06</span>맞대결 — MLP vs RandomForest vs GradientBoosting<a href="#ch6" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    같은 train/test 분할에서 세 모델을 돌린다. 신경망은 표준화·튜닝을 거쳐 R2 0.89까지 왔다.
    트리 앙상블(RandomForest=배깅, GradientBoosting=부스팅)은 스케일링 없이 기본 설정으로도
    그 정도는 따라올 것이다 — 어쩌면 더 높을지도. 표 형태의 중간 규모 데이터는 트리 계열이 강하다고 들었기 때문이다.
  </div>

  <blockquote class="cite">
    "Gradient Tree Boosting … is a generalization of boosting to arbitrary differentiable loss functions.
    GBRT is an accurate and effective off-the-shelf procedure that can be used for both regression and
    classification problems in a variety of areas."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/ensemble.html#gradient-tree-boosting" target="_blank" rel="noopener">Ensembles · Gradient Tree Boosting</a></span>
  </blockquote>

  <h3 class="step">테스트 — 세 모델을 나란히 돌린다</h3>
  <div class="terminal">
    <div class="terminal-header">practice05_runner.py §04 · MLP vs RandomForest vs GradientBoosting — test R2·MAE·학습시간 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_04@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_CMP@@" alt="세 모델의 test R2 막대 비교">
    <figcaption>그림 P5-4 · test R2 — MLP 0.887 &lt; RandomForest 0.917 &lt; GradientBoosting 0.923</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">예상과 일치 — 그러나 뼈아프게</span>
    test R2: MLP <strong>0.8873</strong> &lt; RandomForest <strong>0.9165</strong> &lt; GradientBoosting <strong>0.9234</strong>.
    MAE도 MLP 4.12 vs RF 3.15 vs GBM 3.12로 트리 앙상블이 앞섰다. 게다가 GBM은 표준화도, 그리드서치 수고도 없이
    기본 설정으로 더 높은 점수를 더 짧은 학습시간에 냈다. 신경망이 치른 모든 수고(표준화·튜닝)에도, 이 데이터에서는 트리 앙상블이 더 나은 성능을 보였다.
  </div>

  <div class="bridge">
    <strong>그러면 의문이 뒤집힌다</strong> — "굳이 신경망?"이 "그럼 신경망은 언제 쓰나?"가 됐다.
    왜 이 데이터에서 트리가 이겼고, 신경망은 어디서 유리한지 — 비교 결과를 원리로 설명해 본다.
  </div>
</section>

<!-- ===================== CH 07 ===================== -->
<section id="ch7">
  <h2 class="chap"><span class="num">CH 07</span>왜 트리가 이겼나 — 신경망이 유리한 지점과 비용<a href="#ch7" class="anchor-link">#</a></h2>

  <h3 class="step">답을 찾아서</h3>
  <p>이 데이터는 <strong>표 형태(정형)의 중간 규모(1030행) · 특성 8개</strong>다. 트리 앙상블이 이런 데이터에 강한 이유는 분명하다 —
  분기 기준이 특성의 크기·단위에 불변이라 표준화가 필요 없고, 비선형·특성 간 상호작용(예: 물-시멘트 비율 효과)을
  if-else 분기로 자연스럽게 잡으며, 표본이 적어도 배깅(분산↓)·부스팅(편향↓)이 안정적으로 작동한다.
  GradientBoosting은 약한 트리를 순차적으로 오차에 맞춰 쌓아 편향을 집요하게 줄이는데, 정형 회귀에서 이 방식이
  자주 최강의 기본기를 보인다.</p>

  <blockquote class="cite">
    "Decision trees … require little data preparation. Other techniques often require data normalization …
    Note however that this module does not support missing values."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/tree.html" target="_blank" rel="noopener">Decision Trees · Advantages</a></span>
  </blockquote>

  <h3 class="step">정리 — 신경망이 치른 비용과 유리한 자리</h3>
  <p>신경망은 이 자리에서 비용을 더 치렀다 — 표준화가 필수였고(CH 03), 은닉층·학습률을 짝지어 튜닝해야 했으며(CH 04),
  학습시간도 더 길었다(CH 06). 그런데도 점수가 낮았다. 신경망이 유리한 곳은 따로 있다 —
  픽셀·텍스트·음성처럼 <strong>특성 간 구조가 복잡하고 표본이 아주 많은</strong> 비정형 데이터, 그리고 표현 학습이 필요한 문제다.
  과제의 큰 그리드서치(216조합·17분)가 보여준 것도 결국 "신경망은 손이 많이 가는 모델"이라는 사실이었다.</p>

  <div class="keypoint">
    <span class="label">의문 해소</span>
    "굳이 신경망?"의 답: <strong>이 정형·중간 규모 회귀에서는 트리 앙상블이 더 적은 수고로 더 높은 점수를 낸다.</strong>
    신경망은 표준화·튜닝·연산이라는 비용을 치르는 대신, 그 비용이 정당화되는 자리(대규모 비정형·표현 학습)에서 진가를 낸다.
    과제가 ANN을 시킨 이유는 "이 데이터에서 최강이라서"가 아니라 "신경망의 구조와 학습을 손으로 익히기 위해서"였다.
  </div>

  <div class="bridge">
    <strong>마지막으로</strong> — 출발 의문을 회수하고, 한 문장으로 닫는다.
  </div>
</section>

<!-- ===================== CH 08 ===================== -->
<section id="ch8">
  <h2 class="chap"><span class="num">CH 08</span>정리 — '굳이 신경망?'에 대한 답<a href="#ch8" class="anchor-link">#</a></h2>

  <h3 class="step">최종 결론 — 출발 의문 회수</h3>
  <div class="keypoint">
    <span class="label">FINAL CONCLUSION</span>
    CH 01의 질문 "트리로 풀던 회귀를 왜 신경망으로?"의 답:
    신경망(MLP)은 비선형 은닉층과 역전파로 곡면을 그리지만(CH 02), 그 가중합이 제 실력을 내려면
    표준화가 전제이고(CH 03, R2 0.839→0.903), 은닉층 폭과 학습률을 짝지어 튜닝해야 하며(CH 04, best (100,100)·lr 0.001 → test R2 0.9035),
    그렇게 얻은 test R2 0.887도(CH 05) 같은 데이터의 RandomForest 0.917·GradientBoosting 0.923에는 못 미쳤다(CH 06).
    정형·중간 규모 회귀에서는 트리 앙상블이 더 싸게 더 낫다(CH 07).
  </div>

  <h3 class="step">한 문장으로</h3>
  <div class="keypoint">
    <span class="label">ONE-LINER</span>
    "인공신경망으로 콘크리트 강도 예측"의 실체는 — <strong>표준화된 입력 위에서 비선형 층을 역전파로 학습시켜
    R2 0.89까지 끌어올리는 일이지만, 이 정형 데이터에서는 손이 덜 가는 트리 앙상블이 R2 0.92로 더 잘했다는 것</strong>이다.
    그래서 모델 선택의 절반은 알고리즘이 아니라 데이터의 성격(정형/비정형·규모)을 읽는 데 있다.
  </div>

  <div class="ref-chain">
    <p class="ref-title">📚 전체 근거 출처</p>
    <ol>
      <li><strong>공식 문서</strong>
        <a href="https://scikit-learn.org/stable/modules/neural_networks_supervised.html" target="_blank" rel="noopener">scikit-learn · Neural network models (supervised)</a>(MLP·역전파·회귀 손실),
        <a href="https://scikit-learn.org/stable/modules/ensemble.html#gradient-tree-boosting" target="_blank" rel="noopener">Gradient Tree Boosting</a>,
        <a href="https://scikit-learn.org/stable/modules/tree.html" target="_blank" rel="noopener">Decision Trees(전처리 불필요)</a>,
        <a href="https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html" target="_blank" rel="noopener">StandardScaler</a>.</li>
      <li><strong>데이터셋</strong>
        <code>../ml_workspace/from_colab/0602-s/concrete_stg.csv</code> : 콘크리트 압축강도 회귀(1030행, 8특성, 목표 strength MPa).</li>
      <li><strong>workspace 과제</strong>
        <code>0602-s/ANN_torch-실습.ipynb</code>·<code>ANN_실습문제.md</code>·<code>ANN_그리드서치_결과.md</code> :
        PyTorch ANN 구현과 216조합 그리드서치 보고서(본 글의 sklearn 재현 대상).</li>
      <li><strong>강의자료</strong>
        <code>.study/pdf/머신러닝_알고리즘_앙상블.pdf</code> (배깅·부스팅·랜덤포레스트 배경지식).</li>
      <li><strong>실행 검증</strong>
        <code>.study/test/practice05_ann/practice05_runner.py §00~§04</code>
        → <code>logs/*.txt</code>, <code>charts/*.png</code> (고정 시드 42, 재현 가능).</li>
    </ol>
  </div>

  <div class="bridge">
    <strong>덧붙임</strong> — 과제 colab의 PyTorch 버전은 Adam·AdamW·ReduceLROnPlateau·EarlyStopping·Dropout·BatchNorm까지
    더 넓게 실험했고(그 결과 best corr 0.9601), 이 글은 그 여정의 핵심(표준화·튜닝·앙상블 비교)을 재현 가능한 sklearn으로 압축한 기록이다.
  </div>
</section>
</main>

<footer>
  <p>SK 네트웍스 AI Family 32기 · 교과목 2 단원 2 머신러닝 실습5 과제 — 인공신경망(ANN) 콘크리트 강도 예측 (2026-06-02)</p>
  <p>모든 터미널 출력은 <code>.study/test/practice05_ann/practice05_runner.py</code> 실제 실행 결과이며,
  <code>random_state=42</code>로 재현 가능하다. 차트는 base64 인라인으로 삽입했다.
  과제 colab의 PyTorch ANN을 재현 가능한 sklearn <code>MLPRegressor</code>로 옮겨 검증했다.</p>
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
