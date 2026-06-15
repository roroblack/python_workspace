# build_day0601_html.py
# day0601_decision_tree.html 조립 — logs/*.txt(실제 실행 결과) + charts/*.png(base64) 주입
# 실행: c:\_proj\python_workspace\.venv\Scripts\python.exe build_day0601_html.py
#   (= GUIDE §11 run_all 역할: 터미널 값 직접 작성 금지, 로그에서 주입 → terminal div==body 보장)
#   문체: day0527_ml_intro / day0529_svm 의 "의문→해결→예상 밖→재해결" 서사 추적 방식.
import base64, html, pathlib, re

HERE = pathlib.Path(__file__).parent
LOGS = HERE / "logs"
CHARTS = HERE / "charts"
OUT = HERE.parent.parent / "blog" / "day0601_decision_tree.html"   # .study/blog/
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
    "@@TERM_00@@": term("00_why_tree"),
    "@@TERM_01@@": term("01_impurity"),
    "@@TERM_02@@": term("02_gini_vs_entropy"),
    "@@TERM_03@@": term("03_depth_overfit"),
    "@@TERM_04@@": term("04_pruning"),
    "@@TERM_05@@": term("05_importance_plot"),
    "@@TERM_06@@": term("06_regression_tree"),
    "@@TERM_07@@": term("07_regression_depth"),
    "@@CHART_01@@": chart("ch01_impurity.png"),
    "@@CHART_03@@": chart("ch03_depth_accuracy.png"),
    "@@CHART_05I@@": chart("ch05_importance.png"),
    "@@CHART_05T@@": chart("ch05_tree.png"),
    "@@CHART_06@@": chart("ch06_regression_step.png"),
}

HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>파이썬 결정트리·회귀트리 분석: if-else 질문은 무엇으로 데이터를 가르는가 — 지니·정보이득·과대적합·가지치기</title>
  <meta name="description" content="SK 네트웍스 AI Family 32기 머신러닝 Day4. '직선으로 못 가르는 데이터를 if-else 질문으로 나누면?', '어떤 기준으로 분할하나(지니/엔트로피)', '깊이를 키우면 왜 낮아지나'라는 의문을 따라가며 결정트리의 분할 기준·정보이득·과대적합·가지치기·회귀트리(잎의 평균)를 sklearn 실행으로 검증한 기록.">
  <meta property="og:title" content="파이썬 결정트리·회귀트리 분석: if-else 질문은 무엇으로 데이터를 가르는가">
  <meta property="og:description" content="지니 불순도·정보이득 → 깊이를 키우면 과대적합(잎이 샘플 1개까지) → 가지치기 → 회귀트리는 잎의 평균값(계단 함수)까지 실측으로 추적">
  <meta property="og:type" content="article">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="파이썬 결정트리·회귀트리 분석: if-else 질문은 무엇으로 데이터를 가르는가">
  <meta name="twitter:description" content="지니/정보이득 → 과대적합 → 가지치기 → 회귀트리(잎의 평균)">
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
  <p class="eyebrow">Python · 머신러닝(교과목 2 · 단원 2) Day4 · 부트캠프</p>
  <h1>if-else 질문은 무엇으로 데이터를 가르는가 — 결정트리의 분할 기준은 무엇인가</h1>
  <p class="deck">SVM은 데이터를 가르려고 평면 하나를 세웠다. 그런데 평면 하나로는 가르지 못하는 배치가 있다.
  결정트리는 다른 방식을 택한다 — <code>특성 ≤ 임계값?</code> 이라는 <strong>if-else 질문</strong>을 거듭해 영역을 잘게 쪼갠다.
  이 글은 그 질문 한 번이 <strong>무엇을 기준으로</strong> 정해지는지(지니 불순도·정보이득) 묻는 데서 출발해 —
  질문을 거듭할수록 train은 완벽해지는데 시험에서 낮아지고, 그 하락을 가지치기로 막고,
  같은 원리를 회귀(잎의 평균값)로까지 밀어붙인 기록이다.
  모든 수치는 sklearn으로 직접 돌린 결과이며 <code>random_state=42</code>로 재현 가능하다.</p>
  <div class="meta-row">
    <span><strong>날짜</strong>2026-06-01</span>
    <span><strong>Python</strong>@@PY@@ · scikit-learn 1.8.0 · NumPy 2.4.4 · Pandas 3.0.2</span>
    <span><strong>OS</strong>Windows 11 Pro 25H2</span>
    <span><strong>IDE</strong>VS Code 1.117.0</span>
    <span><strong>HW</strong>Asrock x600 · Ryzen 8600G · 24GB LPDDR5 · RTX 4070 Super 12GB</span>
    <span><strong>커리큘럼</strong>교과목 2 · 단원 2 · 머신러닝 Day4 — 머신러닝_결정트리_회귀트리.pdf</span>
  </div>
</header>

<main>
<nav class="flow">
  <h2>이 글의 흐름 — 질문 하나에서 갈라진 질문들</h2>
  <ol>
    <li><a href="#ch1">시작 — 직선으로 못 가르는 데이터를 <code>if-else</code> 질문으로 나누면?</a></li>
    <li><a href="#ch2">분할의 기준 — '어떤 질문'을 고를까(지니 불순도·정보이득)</a></li>
    <li><a href="#ch3">기준을 바꿔보다 — gini vs entropy, 무엇이 본질인가</a></li>
    <li><a href="#ch4"><span class="turn">예상과 다른 결과</span> — 질문을 거듭할수록(깊이↑) test가 더 안 오른다</a></li>
    <li><a href="#ch5">왜 멈췄나 — 과대적합, 잎이 샘플 1개까지 쪼개질 때</a></li>
    <li><a href="#ch6">되돌리기 — 가지치기(<code>max_depth</code>·<code>min_samples_leaf</code>)</a></li>
    <li><a href="#ch7">트리의 강점 — 중요도와 '규칙을 그림으로'(해석 가능성)</a></li>
    <li><a href="#ch8"><span class="turn">한 발 더</span> — 다수결을 평균으로 바꾸면? 회귀트리(계단 함수)</a></li>
    <li><a href="#ch9">정리 — 깊이는 회귀에서도 과대적합이다, 그리고 출발 의문 회수</a></li>
  </ol>
</nav>

<!-- ===================== CH 01 ===================== -->
<section id="ch1">
  <h2 class="chap"><span class="num">CH 01</span>시작 — 직선으로 못 가르는 데이터를 if-else로 나누면?<a href="#ch1" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>직전 수업(SVM)까지 분류기는 모두 데이터 사이에 <strong>경계 하나</strong>를 긋는 방식이었다 — 직선, 평면, 커널로 휜 면.
  그런데 경계 하나로는 원리적으로 못 가르는 배치가 있다. 가장 단순한 예가 XOR다 —
  대각선끼리 같은 클래스라, 어떤 직선을 그어도 한쪽엔 두 클래스가 섞인다.</p>
  <p>결정트리는 발상이 다르다. 경계 하나를 찾는 대신 <code>x1 ≤ 0.5?</code> 같은 <strong>축에 평행한 질문</strong>을
  하나씩 던져 공간을 직사각형으로 쪼갠다. 질문이 곧 노드이고, 더 나눌 게 없는 마지막 칸이 잎(leaf)이다.</p>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    한 직선으로 못 가르는 XOR도, <code>if-else</code> 질문 두 번이면 네 칸으로 완전히 분리될 것이다.
    그렇다면 결정트리는 XOR을 정확도 1.0으로 분류하고, 그 내부는 <strong>질문의 트리</strong>로 그려져야 한다.
    이게 통과하면 "직선이 아니라 질문으로 가른다"는 트리의 핵심이 확인된다.
  </div>

  <h3 class="step">테스트 — XOR에 트리를 세운다</h3>
  <div class="terminal">
    <div class="terminal-header">decision_tree_runner.py §00 · DecisionTreeClassifier(XOR) + export_text — 질문 트리 확인 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_00@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT — 가설 통과</span>
    XOR은 직선으로 못 가르지만, 트리는 깊이 2·잎 4개의 질문 묶음으로 정확도 1.0을 냈다.
    <code>export_text</code>가 출력한 <code>x1 ≤ 0.5 → x2 ≤ 0.5 → class 0</code> 식 규칙이 곧 모델의 전부다.
    그렇다면 다음 질문은 자명하다 — 트리는 수많은 가능한 질문 중 <strong>어떤 질문을 먼저 고를까?</strong>
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — XOR은 답이 뻔해서 질문 순서를 고민할 필요가 없었다.
    하지만 특성이 여러 개고 클래스가 섞여 있으면, "어느 특성을 어느 값에서 자를까"가 무수히 많다.
    트리는 이 선택을 무엇을 보고 하는가? 그 기준이 '불순도'다.
  </div>
</section>

<!-- ===================== CH 02 ===================== -->
<section id="ch2">
  <h2 class="chap"><span class="num">CH 02</span>분할의 기준 — 지니 불순도와 정보이득<a href="#ch2" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>트리가 질문을 고르는 기준은 <strong>불순도(impurity)</strong>다. 한 노드에 클래스가 얼마나 섞여 있는지를
  하나의 숫자로 잰다. 반반으로 섞이면 최대, 한 클래스만 있으면 0(순수)이다.
  대표적으로 <strong>지니 불순도</strong>(<code>1 − Σpᵢ²</code>)와 <strong>엔트로피</strong>(<code>−Σpᵢ·log₂pᵢ</code>)가 있다.</p>

  <blockquote class="cite">
    "Gini impurity … and log loss (entropy) … are measures of the quality of a split.
    The feature and threshold that yield the largest reduction in impurity are chosen at each node."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/tree.html#mathematical-formulation" target="_blank" rel="noopener">Decision Trees — Mathematical formulation</a></span>
  </blockquote>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    트리는 "분할 후 자식들의 불순도를 가장 많이 떨어뜨리는 질문"을 고른다(=정보이득 최대).
    그렇다면 부모를 [50,50](가장 섞임, gini 0.5)에서 한쪽을 순수하게 떼어내는 질문은
    <strong>큰 양수의 정보이득</strong>을 낼 것이다. 직접 계산해 그 직관을 수치로 확인한다.
  </div>

  <h3 class="step">테스트 — 불순도와 정보이득을 손으로 계산한다</h3>
  <div class="terminal">
    <div class="terminal-header">decision_tree_runner.py §01 · 지니/엔트로피·정보이득 직접 계산 — 분할 기준 검증 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_01@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_01@@" alt="지니 불순도와 엔트로피 곡선">
    <figcaption>그림 0601-1 · 불순도는 p=0.5(반반)에서 최대, p=0/1(순수)에서 0 — 지니와 엔트로피는 모양이 닮았다</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT — 가설 통과</span>
    [25,25] 반반일 때 gini 0.5·entropy 1.0으로 최대, [50,0] 순수일 때 둘 다 0.
    부모 [50,50](gini 0.5)을 [50,10]·[0,40]으로 가르면 가중평균 자식 불순도가 0.1667로 떨어져
    <strong>정보이득 0.3333</strong>. 트리는 매 노드에서 이 값이 가장 큰 (특성·임계값)을 탐욕적으로 고른다.
    그런데 곡선 그림에서 보듯 지니와 엔트로피는 모양이 거의 같다 — 그럼 어느 쪽을 써도 같은 결과일까?
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 기준식이 다르면 트리도 달라져야 할 것 같다.
    하지만 곡선이 저렇게 닮았다면, gini로 키운 트리와 entropy로 키운 트리의 성능 차이는
    생각보다 작을지 모른다. 같은 iris로 두 기준을 맞붙여 본다.
  </div>
</section>

<!-- ===================== CH 03 ===================== -->
<section id="ch3">
  <h2 class="chap"><span class="num">CH 03</span>기준을 바꿔보다 — gini vs entropy<a href="#ch3" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 비교</h3>
  <p>분할 기준은 <code>criterion</code> 인자 하나로 바꾼다. 같은 iris·같은 시드에서 <code>gini</code>와 <code>entropy</code>만 갈아끼우고
  train·test 정확도, 트리 깊이, 잎 개수를 나란히 찍어 본다. 기준식의 차이가 결과로 얼마나 드러나는지 보려는 것이다.</p>

  <pre><code class="language-python"># path : .study/test/decision_tree/decision_tree_runner.py §02 (발췌)
from sklearn.tree import DecisionTreeClassifier

for crit in ["gini", "entropy"]:
    clf = DecisionTreeClassifier(criterion=crit, random_state=42).fit(Xtr, ytr)
    print(crit, clf.score(Xtr, ytr), clf.score(Xte, yte),
          clf.get_depth(), clf.get_n_leaves())</code></pre>

  <h3 class="step">테스트</h3>
  <div class="terminal">
    <div class="terminal-header">decision_tree_runner.py §02 · criterion gini vs entropy(iris) — 기준 교체 영향 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_02@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">관찰 결과</span>
    두 기준 모두 train 정확도 1.0(완전 암기). test는 gini 0.9333, entropy 0.8889로 비슷한 수준이고
    잎 개수는 둘 다 8로 같다. 기준식의 철학(불순도 vs 정보 엔트로피)은 다르지만,
    <strong>실제 분류 결과를 가르는 더 큰 변수는 criterion이 아니라 "트리를 얼마나 깊게 키우느냐"</strong>였다.
    train이 둘 다 1.0이라는 게 마음에 걸린다 — 완벽한 암기는 좋은 신호가 아닐 수 있다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — train 1.0이 나왔다는 건 트리가 학습 데이터를 끝까지 쪼갰다는 뜻이다.
    더 깊이 쪼갤수록 train은 완벽해질 텐데, 처음 보는 데이터(test)도 같이 좋아질까?
    SVM·회귀에서 봤던 그 함정이 트리에도 있는지 깊이를 직접 키워 본다.
  </div>
</section>

<!-- ===================== CH 04 ===================== -->
<section id="ch4">
  <h2 class="chap"><span class="num">CH 04</span>예상과 다른 결과 — 깊이를 키워도 test가 더 안 오른다<a href="#ch4" class="anchor-link">#</a></h2>

  <h3 class="step">실험 — max_depth를 1에서 None(무제한)까지</h3>
  <p><code>max_depth</code>를 1·2·3·…·None으로 키우며 train/test 정확도와 잎 개수를 같이 찍는다.
  기대는 "깊을수록 둘 다 상승"이었다.</p>
  <div class="terminal">
    <div class="terminal-header">decision_tree_runner.py §03 · max_depth↑(iris) — train↑ / test 정체 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_03@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_03@@" alt="max_depth에 따른 train/test 정확도 곡선">
    <figcaption>그림 0601-2 · 깊이↑ → train은 1.0까지 오르는데 test는 depth 3에서 정점(0.9778) 후 오히려 내려앉는다</figcaption>
  </figure>

  <h3 class="step">관찰 — 생각과 달랐다</h3>
  <div class="keypoint">
    <span class="label">FAILURE → CLUE</span>
    train 정확도는 깊이를 키울수록 0.6667 → 1.0으로 단조 상승한다(잎 2→8개).
    그런데 test는 <strong>depth 3에서 0.9778로 가장 높았다</strong>가, depth 4에서 0.8889로 떨어지고
    그 뒤로는 0.9333에 갇힌다. 깊이를 더 줘도 train만 외울 뿐 test는 보상이 없다.
    "더 깊게 = 더 좋게"가 맞지 않은 것이다. 이 깨짐이 다음 의문을 끌고 간다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — depth 5부터 train이 1.0으로 못 박혔다.
    이건 트리가 학습 데이터를 잎마다 거의 한 점까지 쪼갰다는 신호다. 이 현상에는 이름이 있다 —
    회귀에서 만났던 그 과대적합이, 트리에서는 '잎의 분해'라는 더 노골적인 모습으로 나타난다.
  </div>
</section>

<!-- ===================== CH 05 ===================== -->
<section id="ch5">
  <h2 class="chap"><span class="num">CH 05</span>왜 멈췄나 — 과대적합, 잎이 샘플 1개까지<a href="#ch5" class="anchor-link">#</a></h2>

  <h3 class="step">답을 찾아서</h3>
  <p>train은 1.0인데 test가 따라오지 못하는 현상의 이름은 <strong>과대적합(overfitting)</strong>이다.
  트리에서는 그 메커니즘이 특히 적나라하다 — 분할을 멈추지 않으면, 트리는 모든 잎이
  <strong>한 클래스(극단적으로는 샘플 1개)</strong>가 될 때까지 쪼갠다. 그러면 train은 당연히 100% 맞지만,
  그건 데이터의 패턴이 아니라 우연한 위치까지 외운 것이라 처음 보는 데이터엔 쓸모가 없다.</p>

  <blockquote class="cite">
    "Decision trees can create over-complex trees that do not generalise the data well.
    This is called overfitting. Mechanisms such as pruning, setting the minimum number of samples
    required at a leaf node or setting the maximum depth of the tree are necessary to avoid this problem."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/tree.html#tips-on-practical-use" target="_blank" rel="noopener">Decision Trees — Tips on practical use</a></span>
  </blockquote>

  <p>CH 04의 로그가 정확히 이 그림이었다 — depth 5에서 잎 8개·train 1.0. 잎이 더 늘 수 없을 만큼
  데이터를 잘게 갈라놓고 보니, 정작 test에서는 depth 3짜리 단순한 트리(잎 5개)보다 못했다.
  복잡도는 공짜가 아니라 <strong>train 적합과 일반화 사이의 트레이드오프</strong>였다.</p>

  <div class="keypoint">
    <span class="label">의문 해소</span>
    "깊게 쪼갤수록 좋다"가 아니라 "깊게 쪼갤수록 train만 외우고 일반화는 깨질 위험이 커진다."
    공식 문서가 직접 처방까지 적어 줬다 — <strong>가지치기, <code>min_samples_leaf</code>, <code>max_depth</code></strong>.
    그렇다면 이 손잡이들을 실제로 돌리면 낮아진 test가 회복될까?
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 깊이를 강제로 제한하거나, 잎이 일정 샘플 수 이상이어야만
    분할을 허용하면 트리가 덜 외울 것이다. CH 04에서 정점이던 depth 3, 그리고 <code>min_samples_leaf</code>를
    직접 걸어 무제한 트리와 비교한다.
  </div>
</section>

<!-- ===================== CH 06 ===================== -->
<section id="ch6">
  <h2 class="chap"><span class="num">CH 06</span>되돌리기 — 가지치기로 일반화 회복<a href="#ch6" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    무제한 트리(잎 8개·과대적합)에 <code>max_depth=3</code> 또는 <code>min_samples_leaf=5</code>를 걸면,
    잎 개수가 줄고 train 정확도는 조금 내려가도 <strong>test 정확도는 유지되거나 오를 것</strong>이다.
    즉 train을 약간 포기하는 대가로 일반화를 산다.
  </div>

  <h3 class="step">테스트 — 네 가지 가지치기 설정 비교</h3>
  <div class="terminal">
    <div class="terminal-header">decision_tree_runner.py §04 · max_depth·min_samples_leaf(iris) — 가지치기 효과 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_04@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">가설 통과</span>
    무제한 트리는 train 1.0·test 0.9333·잎 8개. 반면 <code>max_depth=3</code>은 train 0.9810으로 내려가는 대신
    <strong>test 0.9778로 가장 높고 잎은 5개</strong>로 단순하다. train을 0.019만큼 양보하고 test 일반화를 산 것이다.
    가지치기는 "트리를 일부러 덜 똑똑하게 만들어 더 잘 맞히게" 하는 의도적인 단순화이다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 여기까지 트리를 "정확도를 내는 분류기"로만 봤다.
    하지만 트리에는 SVM·신경망에 없는 결정적 강점이 하나 있다 — 만든 규칙을 사람이 읽을 수 있다는 것.
    가지친 트리가 정확히 무엇을 보고 결정했는지, 숫자와 그림으로 꺼내 본다.
  </div>
</section>

<!-- ===================== CH 07 ===================== -->
<section id="ch7">
  <h2 class="chap"><span class="num">CH 07</span>트리의 강점 — 중요도와 규칙을 그림으로<a href="#ch7" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>트리는 학습이 끝나면 <code>feature_importances_</code>를 준다 — 각 특성이 분할에서 깎아낸
  불순도 감소량의 합(전체 합=1로 정규화)이다. 또 <code>plot_tree</code>로 트리 전체를
  <strong>질문의 그림</strong>으로 그릴 수 있다. 이 해석 가능성이 트리가 실무에서 사랑받는 이유다.</p>

  <blockquote class="cite">
    "The relative rank (i.e. depth) of a feature used as a decision node in a tree
    can be used to assess the relative importance of that feature … this is the feature importance."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/ensemble.html#feature-importance-evaluation" target="_blank" rel="noopener">Feature importance evaluation</a></span>
  </blockquote>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    iris를 분류할 때 꽃잎(petal) 길이·너비가 결정적일 것이다(품종을 가르는 건 주로 꽃잎이므로).
    그렇다면 <code>feature_importances_</code>에서 petal 두 특성이 중요도 대부분을 차지하고,
    꽃받침(sepal)은 거의 0일 것이다. 그리고 트리 그림의 루트 질문도 petal 기준이어야 한다.
  </div>

  <h3 class="step">테스트</h3>
  <div class="terminal">
    <div class="terminal-header">decision_tree_runner.py §05 · feature_importances_ + plot_tree(iris) — 중요도·규칙 시각화 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_05@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_05I@@" alt="iris 특성 중요도 막대 그래프">
    <figcaption>그림 0601-3 · 특성 중요도 — petal length 0.586 · petal width 0.414, sepal 두 특성은 정확히 0</figcaption>
  </figure>
  <figure class="shot">
    <img src="@@CHART_05T@@" alt="iris 결정트리 다이어그램(max_depth=3)">
    <figcaption>그림 0601-4 · 같은 트리를 그림으로 — 각 노드가 하나의 if-else 질문, 색은 다수 클래스를 나타낸다</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT — 가설 통과</span>
    중요도는 <strong>petal length 0.5856 · petal width 0.4144</strong>, sepal 두 특성은 정확히 0.0000.
    트리는 꽃받침을 아예 보지 않고 꽃잎만으로 iris 세 품종을 갈랐다. 게다가 그 규칙은
    <code>plot_tree</code> 그림 한 장으로 전부 드러난다 — "왜 이렇게 분류했나"를 설명할 수 있는 모델,
    이것이 블랙박스인 SVM·신경망과 분명히 다른 점이다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 여기까지 트리는 클래스를 맞히는 분류기였다.
    잎에서 다수결로 클래스를 정했는데 — 그 다수결을 <em>평균</em>으로 바꾸면 연속값도 예측할 수 있지 않을까?
    그게 회귀트리다. 분할 원리는 그대로 두고 잎의 출력만 바꿔 본다.
  </div>
</section>

<!-- ===================== CH 08 ===================== -->
<section id="ch8">
  <h2 class="chap"><span class="num">CH 08</span>한 발 더 — 다수결을 평균으로, 회귀트리<a href="#ch8" class="anchor-link">#</a></h2>

  <h3 class="step">학습 → 가설</h3>
  <p>분류트리의 잎은 그 칸에 모인 샘플의 <strong>다수 클래스</strong>를 출력했다.
  회귀트리는 같은 구조에서 잎의 출력만 바꾼다 — 그 칸에 모인 샘플들의 <strong>평균값</strong>이다.
  그래서 예측은 직선이나 곡선이 아니라, 칸마다 값이 일정한 <strong>계단 함수</strong>가 된다.</p>
  <div class="qbox">
    <span class="label">가설</span>
    <code>sin</code> 곡선 데이터에 회귀트리를 맞추면, 예측은 잎 개수만큼의 수평 구간으로 이뤄진 계단이 될 것이다.
    <code>max_depth=2</code>면 잎 4개 → 서로 다른 예측값 4개, <code>max_depth=5</code>면 더 잘게 쪼개진 계단이어야 한다.
  </div>

  <blockquote class="cite">
    "Decision trees can also be applied to regression problems, using the DecisionTreeRegressor class …
    each leaf predicts the mean target value of the training samples reaching that leaf."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/tree.html#regression" target="_blank" rel="noopener">Decision Trees — Regression</a></span>
  </blockquote>

  <h3 class="step">테스트 — sin 곡선에 회귀트리를 맞춘다</h3>
  <div class="terminal">
    <div class="terminal-header">decision_tree_runner.py §06 · DecisionTreeRegressor(sin) — 잎의 평균값·계단 예측 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_06@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_06@@" alt="회귀트리의 계단 함수 예측(depth 2 vs 5)">
    <figcaption>그림 0601-5 · 회귀트리 예측은 계단 함수 — depth=2는 4칸, depth=5는 30칸으로 sin에 더 밀착</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">가설 통과</span>
    <code>depth=2</code>는 잎 4개 → 예측값 4종(각 잎의 평균), <code>depth=5</code>는 잎 30개 → 예측값 30종.
    예측이 정확히 계단 함수다. 분할 원리는 분류와 똑같고 <strong>잎의 출력만 다수결→평균</strong>으로 바뀐 것이다.
    그런데 depth=5의 계단이 sin에 너무 밀착해 보인다 — 분류에서 본 그 과대적합이 회귀에도 있지 않을까?
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 계단이 잘게 쪼개질수록 train 데이터엔 더 밀착한다.
    그렇다면 회귀트리도 깊이를 키우면 train 오차는 0으로 가고 test 오차는 다시 커질 것이다.
    분류에서 본 법칙이 회귀에서도 같은지 오차(MSE)로 못 박는다.
  </div>
</section>

<!-- ===================== CH 09 ===================== -->
<section id="ch9">
  <h2 class="chap"><span class="num">CH 09</span>정리 — 깊이는 회귀에서도 과대적합이다<a href="#ch9" class="anchor-link">#</a></h2>

  <h3 class="step">실험 → 해석</h3>
  <p>회귀트리의 <code>max_depth</code>를 키우며 train/test MSE를 같이 찍는다.
  분류에서 "깊이 = 과대적합"이었다면, 회귀에서도 train MSE는 0으로, test MSE는 어느 깊이부터 다시 커져야 한다.</p>
  <div class="terminal">
    <div class="terminal-header">decision_tree_runner.py §07 · DecisionTreeRegressor max_depth↑ — train/test MSE · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_07@@</pre>
  </div>

  <h3 class="step">최종 결론 — 출발 의문 회수</h3>
  <div class="keypoint">
    <span class="label">FINAL CONCLUSION</span>
    회귀트리도 똑같았다 — 깊이를 키우면 train MSE는 <strong>0.11019 → 0.00000</strong>(무제한, 잎 140개=샘플 1개씩)으로 떨어지지만,
    test MSE는 <code>max_depth=5</code>의 0.03703에서 바닥을 친 뒤 무제한에선 0.04377로 다시 올라간다.
    CH 01의 출발 의문 "if-else 질문은 무엇으로 데이터를 가르는가"의 답:
    <strong>트리는 매 노드에서 불순도(분류) 또는 분산(회귀)을 가장 많이 줄이는 (특성·임계값)을 탐욕적으로 골라 공간을 쪼개고,
    잎에서 다수결(분류)·평균(회귀)으로 답한다.</strong> 그리고 그 쪼갬을 멈추지 않으면 train은 완벽히 외우되 일반화는 낮아진다 —
    그래서 트리의 핵심 손잡이는 <code>max_depth</code>·<code>min_samples_leaf</code> 같은 가지치기다.
  </div>

  <h3 class="step">한 문장으로</h3>
  <div class="keypoint">
    <span class="label">ONE-LINER</span>
    결정트리는 <strong>"불순도를 가장 많이 줄이는 if-else 질문"의 사슬</strong>이고,
    그 사슬을 적당한 길이에서 끊는 일(가지치기)이 곧 일반화다. 회귀트리는 같은 사슬의 잎에서
    다수결 대신 평균을 낼 뿐이며 — 트리가 SVM·신경망과 다른 단 하나의 무기는, 만든 규칙을 그림으로 펼쳐 설명할 수 있다는 점이다.
  </div>

  <div class="ref-chain">
    <p class="ref-title">📚 전체 근거 출처</p>
    <ol>
      <li><strong>공식 문서</strong>
        <a href="https://scikit-learn.org/stable/modules/tree.html#mathematical-formulation" target="_blank" rel="noopener">scikit-learn · Decision Trees(지니/엔트로피·분할 기준)</a>,
        <a href="https://scikit-learn.org/stable/modules/tree.html#tips-on-practical-use" target="_blank" rel="noopener">Tips on practical use(과대적합·가지치기)</a>,
        <a href="https://scikit-learn.org/stable/modules/tree.html#regression" target="_blank" rel="noopener">Regression(회귀트리)</a>,
        <a href="https://scikit-learn.org/stable/modules/ensemble.html#feature-importance-evaluation" target="_blank" rel="noopener">Feature importance</a>.</li>
      <li><strong>workspace</strong>
        <code>../ml_workspace/from_colab/0601-s/decision_tree_torch.ipynb</code>(채무불이행 분류 실습 — 결정트리 맥락),
        <code>regression_tree_torch.ipynb</code> · <code>회귀트리_성능향상.ipynb</code>(회귀트리 실습).</li>
      <li><strong>강의자료</strong>
        <code>머신러닝_결정트리_회귀트리.pdf</code> (교과목 2 · 단원 2 · Day4 배경지식).</li>
      <li><strong>실행 검증</strong>
        <code>.study/test/decision_tree/decision_tree_runner.py §00~§07</code>
        → <code>logs/*.txt</code>, <code>charts/*.png</code> (고정 시드 42, 재현 가능).</li>
    </ol>
  </div>

  <div class="bridge">
    <strong>다음 글 예고</strong> — 트리 하나는 가지치기를 해도 불안정하다(데이터가 조금만 바뀌어도 트리가 통째로 흔들린다).
    이 약점을 여러 트리의 투표로 메우는 것이 다음 수업의 앙상블(배깅·랜덤포레스트·부스팅)이다.
  </div>
</section>
</main>

<footer>
  <p>SK 네트웍스 AI Family 32기 · 교과목 2 단원 2 머신러닝 Day4 (2026-06-01)</p>
  <p>모든 터미널 출력은 <code>.study/test/decision_tree/decision_tree_runner.py</code> 실제 실행 결과이며,
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
notes_leak = HTML.count(".study/notes") + HTML.count("notes/06")
bad_frames = [w for w in ["비전공", "초보", "처음 배우", "문외한", "print 정도", "엑셀 수준"] if w in HTML]
figure_shot_imgs = HTML.count('<figure class="shot">')
print(f"파일: {OUT}")
print(f"terminal div: {n_term} | terminal-body: {n_body} | (일치={n_term==n_body})")
print(f"외부 URL img: {len(http_imgs)} (0이어야 함) | base64 img: {b64_imgs} | figure.shot: {figure_shot_imgs}")
print(f"chap: {HTML.count('h2 class=\"chap\"')} | qbox: {HTML.count('class=\"qbox\"')} | keypoint: {HTML.count('class=\"keypoint\"')}")
print(f"미치환 placeholder: {leftover} | zero-width: {zwsp} | notes 누출: {notes_leak} | 입문자 프레이밍: {bad_frames}")
print(f"크기: {len(HTML)//1024} KB")
