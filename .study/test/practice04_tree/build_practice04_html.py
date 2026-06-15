# build_practice04_html.py
# ml_practice04_tree.html 조립 — logs/*.txt(실제 실행 결과) + charts/*.png(base64) 주입
# 실행: c:\_proj\python_workspace\.venv\Scripts\python.exe build_practice04_html.py
#   (= GUIDE §11 run_all 역할: 터미널 값 직접 작성 금지, 로그에서 주입)
#   head/CSS/컴포넌트는 build_day0527_html.py 를 그대로 복제. 문체는 interpreter/실습3 서사 추적 방식.
import base64, html, pathlib, re

HERE = pathlib.Path(__file__).parent
LOGS = HERE / "logs"
CHARTS = HERE / "charts"
OUT = HERE.parent.parent / "blog" / "ml_practice04_tree.html"   # .study/blog/
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
    "@@TERM_00@@": term("00_two_tasks"),
    "@@TERM_01@@": term("01_clf_baseline"),
    "@@TERM_02@@": term("02_clf_depth"),
    "@@TERM_03@@": term("03_clf_gridsearch"),
    "@@TERM_04@@": term("04_clf_importance"),
    "@@TERM_05@@": term("05_reg_baseline"),
    "@@TERM_06@@": term("06_reg_tuned"),
    "@@TERM_07@@": term("07_reg_importance"),
    "@@CHART_DEPTH@@": chart("ch_depth.png"),
    "@@CHART_IMP_CLF@@": chart("ch_importance_clf.png"),
    "@@CHART_REG_DEPTH@@": chart("ch_reg_depth.png"),
    "@@CHART_IMP_REG@@": chart("ch_importance_reg.png"),
}

HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>파이썬 결정트리·회귀트리 분석: 와인 분류의 과대적합부터 회귀트리 R2를 끌어올리기까지</title>
  <meta name="description" content="SK 네트웍스 AI Family 32기 머신러닝 실습4(과제). '깊이를 키워도 정확도가 왜 안 오를까', 'GridSearchCV가 고른 트리가 왜 시험에선 더 낮을까', '회귀트리 R2가 왜 음수로 낮아지고 어떻게 되살렸나'를 따라가며 DecisionTreeClassifier/Regressor·GridSearchCV·feature_importances 를 sklearn 실행으로 검증한 기록.">
  <meta property="og:title" content="파이썬 결정트리·회귀트리 분석: 와인 분류와 회귀트리 성능 향상">
  <meta property="og:description" content="와인 결정트리의 과대적합 → GridSearchCV의 함정 → 회귀트리 R2 -0.55에서 +0.20으로 되살리기까지 실측 추적">
  <meta property="og:type" content="article">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="파이썬 결정트리·회귀트리 분석: 와인 분류와 회귀트리 성능 향상">
  <meta name="twitter:description" content="과대적합 → GridSearchCV → 회귀트리 성능 향상(R2 -0.55→+0.20)">
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
  <p class="eyebrow">Python · 머신러닝 실습4(과제) · 부트캠프</p>
  <h1>와인 결정트리, 깊이를 키워도 안 오르던 정확도 — 그리고 회귀트리 R2를 음수에서 끌어올리기까지</h1>
  <p class="deck">실습4 과제는 트리 둘이었다 — 와인을 <strong>결정트리로 분류</strong>하고,
  화이트와인 품질을 <strong>회귀트리로 예측</strong>해 성능을 끌어올리는 것. 분류 트리는 첫 시도부터 정확도가 높아
  "튜닝할 게 있나" 싶었지만, 깊이를 키워도 점수가 꼼짝 않는 게 거꾸로 의문이었다. 반대로 회귀트리는
  기본값으로 돌리자 test R2가 <strong>음수</strong>로 크게 낮아졌다. 이 글은 두 트리에서 마주친 의문 —
  "깊이를 키워도 왜 안 오르나", "GridSearchCV가 고른 트리가 왜 시험에선 더 낮나", "회귀트리는 왜 낮아지고
  어떻게 되살리나" — 를 주어로 삼아 하나씩 부딪쳐 본 기록이다. 모든 수치는 sklearn 으로 직접 돌린 결과이며
  <code>random_state=42</code> 로 재현 가능하다.</p>
  <div class="meta-row">
    <span><strong>날짜</strong>2026-06-01</span>
    <span><strong>Python</strong>@@PY@@ · scikit-learn 1.8.0 · NumPy 2.4.4 · Pandas 3.0.2</span>
    <span><strong>OS</strong>Windows 11 Pro 25H2</span>
    <span><strong>IDE</strong>VS Code 1.117.0</span>
    <span><strong>HW</strong>Asrock x600 · Ryzen 8600G · 24GB LPDDR5 · RTX 4070 Super 12GB</span>
    <span><strong>커리큘럼</strong>교과목 2 · 단원 2 · 머신러닝 — 머신러닝_결정트리_회귀트리.pdf</span>
  </div>
</header>

<main>
<nav class="flow">
  <h2>이 글의 흐름 — 두 트리에서 갈라져 나온 의문들</h2>
  <ol>
    <li><a href="#ch1">시작 — 같은 '트리'인데 분류와 회귀는 무엇이 다른가 (y 형태로 가른다)</a></li>
    <li><a href="#ch2">분류 baseline — 기본 트리 정확도 0.963, 그런데 train은 1.0이다</a></li>
    <li><a href="#ch3"><span class="turn">의외</span> — 깊이를 3·5·7·10·None으로 키워도 test 정확도가 안 움직인다</a></li>
    <li><a href="#ch4"><span class="turn">예상과 다른 결과</span> — GridSearchCV가 고른 '최적' 트리가 시험에선 오히려 낮았다</a></li>
    <li><a href="#ch5">트리의 해석 — 루트 노드는 어떤 특성으로 와인을 가르나(feature importance)</a></li>
    <li><a href="#ch6"><span class="turn">하락</span> — 회귀트리를 기본값으로 돌렸더니 test R2가 음수였다</a></li>
    <li><a href="#ch7">되살리기 — 깊이를 묶고 리프를 키워 R2를 음수에서 +0.20으로</a></li>
    <li><a href="#ch8">정리 — 트리의 성능은 '얼마나 안 자라게 두느냐'에 달렸다로 회수</a></li>
  </ol>
</nav>

<!-- ===================== CH 01 ===================== -->
<section id="ch1">
  <h2 class="chap"><span class="num">CH 01</span>시작 — 분류 트리와 회귀 트리는 무엇이 다른가<a href="#ch1" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>실습4 과제지에는 트리가 둘 있었다. 하나는 <code>DecisionTreeClassifier</code>로 와인을 품종으로 <strong>분류</strong>하고,
  다른 하나는 회귀 모델로 화이트와인 품질(<code>quality</code>) 점수를 <strong>예측</strong>해 성능을 끌어올리는 과제였다.
  같은 "트리"라는 단어를 쓰는데, 한쪽은 라벨을 맞히고 한쪽은 숫자를 맞힌다. 둘을 가르는 기준은 모델이 아니라
  정답 <code>y</code>의 형태다 — <code>y</code>가 소수의 정수 라벨이면 분류, 순서가 있는 연속 점수면 회귀다.</p>

  <h3 class="step">의문 → 기준</h3>
  <div class="qbox">
    <span class="label">의문</span>
    트리는 결국 "조건으로 데이터를 둘로 가르는" 구조 하나다. 그렇다면 분류 트리와 회귀 트리의 차이는
    <strong>리프(터미널) 노드가 무엇을 내놓는가</strong>에 있을 것이다 — 분류는 라벨, 회귀는 평균값.
    두 과제의 <code>y</code>를 한자리에 놓고 성격부터 갈라 두면, 뒤에서 두 트리가 왜 다르게 행동하는지 첫 단서가 보인다.
  </div>

  <h3 class="step">테스트 — 두 데이터의 y를 가른다</h3>
  <div class="terminal">
    <div class="terminal-header">practice04_runner.py §00 · load_wine vs winequality-white — y 형태로 분류/회귀 판별 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_00@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">기준 확정</span>
    <code>load_wine</code>은 178행·13특성에 라벨 <code>[0 1 2]</code> 세 품종 → <strong>분류</strong>.
    화이트와인은 4898행·11특성에 <code>quality</code> 3~9의 순서 점수(평균 5.878) → <strong>회귀</strong>.
    분류 트리의 리프는 "다수결 라벨"을, 회귀 트리의 리프는 "그 안에 떨어진 샘플들의 평균"을 내놓는다.
    먼저 분류 트리부터 손을 댔다 — 그리고 첫 줄에서부터 예상과 다른 장면을 만났다.
  </div>

  <div class="bridge">
    <strong>첫 과제로</strong> — 와인을 기본 <code>DecisionTreeClassifier</code>에 아무 제약 없이 넣어 봤다.
    과제 문제1이 요구한 5개 지표(Accuracy·Precision·Recall·F1·혼동행렬)를 찍는 단순 작업이었는데,
    정확도가 생각보다 너무 높게 나와서 오히려 멈칫했다.
  </div>
</section>

<!-- ===================== CH 02 ===================== -->
<section id="ch2">
  <h2 class="chap"><span class="num">CH 02</span>분류 baseline — 정확도 0.963, 그런데 train은 1.0<a href="#ch2" class="anchor-link">#</a></h2>

  <h3 class="step">테스트 — 제약 없는 기본 트리</h3>
  <p>과제 문제1 그대로, 기본값(<code>max_depth=None</code>)의 트리를 train(70%)으로 학습해 test(30%)에서 5개 지표를 찍는다.
  계층 분할(<code>stratify=y</code>)로 세 품종 비율을 train/test에 똑같이 유지했다.</p>

  <pre><code class="language-python"># path : .study/test/practice04_tree/practice04_runner.py §01 (발췌)
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3,
                                      random_state=42, stratify=y)
clf = DecisionTreeClassifier(random_state=42)   # 제약 없음(기본값)
clf.fit(Xtr, ytr)
print(clf.score(Xtr, ytr))   # train 정확도
print(clf.score(Xte, yte))   # test 정확도</code></pre>

  <div class="terminal">
    <div class="terminal-header">practice04_runner.py §01 · DecisionTreeClassifier(wine) — Acc/Precision/Recall/F1/혼동행렬 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_01@@</pre>
  </div>

  <h3 class="step">관찰</h3>
  <div class="keypoint">
    <span class="label">관찰 결과</span>
    test 정확도 0.9630, 정밀도 0.9662·재현율 0.9630·F1 0.9632. 혼동행렬을 보면 52개 중 50개를 맞혔다.
    그런데 <strong>train 정확도가 1.0000</strong>이다. 트리가 train 데이터를 한 점도 틀리지 않고 외웠다는 뜻이다.
    train-test 격차 +0.037은 작지만, "train을 완벽히 외웠다"는 신호 자체는 과대적합의 전형이다.
  </div>

  <div class="bridge">
    <strong>여기서 의문이 생겼다</strong> — train을 외울 정도면 트리가 너무 깊은 게 아닐까? 과제 문제2는 마침
    <code>max_depth</code>를 3·5·7·10·None으로 바꿔 비교하라고 한다. 깊이를 줄이면 외움이 풀리면서 test가 오를 거라 기대했다.
  </div>
</section>

<!-- ===================== CH 03 ===================== -->
<section id="ch3">
  <h2 class="chap"><span class="num">CH 03</span>의외 — 깊이를 바꿔도 test가 안 움직인다<a href="#ch3" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    깊이를 줄이면 train의 "외움"이 풀리니, 얕은 트리(depth 3)는 train 정확도가 1.0보다 낮아지는 대신
    test 정확도는 더 높아질 것이다. 반대로 깊이를 키우면 test가 떨어질 것이다 — CH 02에서 본 과대적합 논리대로라면.
  </div>

  <h3 class="step">테스트 — 깊이를 3·5·7·10·None으로</h3>
  <div class="terminal">
    <div class="terminal-header">practice04_runner.py §02 · max_depth 3·5·7·10·None — train/test 정확도 비교 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_02@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_DEPTH@@" alt="max_depth에 따른 train/test 정확도 곡선">
    <figcaption>그림 1 · 깊이↑ → train 정확도는 0.992에서 1.0으로 차오르지만, test 정확도는 0.9630에 완전히 고정</figcaption>
  </figure>

  <h3 class="step">관찰 — 가설이 절반만 맞았다</h3>
  <div class="keypoint">
    <span class="label">PARTIAL OK</span>
    깊이를 키울수록 train 정확도가 0.9919 → 1.0으로 오르는 건 가설대로다(트리가 점점 더 외운다).
    그런데 <strong>test 정확도는 5개 깊이 전부 0.9630으로 똑같았다.</strong> 깊이 3에서 이미 리프 7개로 충분했고,
    그 위로 갈라진 노드들은 train의 노이즈만 더 외웠을 뿐 test 판정을 바꾸지 못했다. wine 데이터(178행·3품종)는
    경계가 또렷해서, 얕은 트리만으로도 test에서 거의 한계 성능에 닿아 있었던 것이다.
  </div>

  <div class="bridge">
    <strong>그렇다면 손튜닝의 한계다</strong> — 과제 문제2~5는 <code>max_depth</code>, <code>min_samples_split</code>,
    <code>min_samples_leaf</code>, <code>criterion</code>을 하나씩 바꿔 보라고 한다. 그런데 하나씩 바꾸면 다른 값과의
    조합 효과를 못 본다. 네 가지를 동시에 훑어 교차검증으로 최적 조합을 고르는 도구가 <code>GridSearchCV</code>다.
  </div>
</section>

<!-- ===================== CH 04 ===================== -->
<section id="ch4">
  <h2 class="chap"><span class="num">CH 04</span>예상과 다른 결과 — GridSearchCV가 고른 트리가 시험에선 낮았다<a href="#ch4" class="anchor-link">#</a></h2>

  <h3 class="step">학습 → 가설</h3>
  <p><code>GridSearchCV</code>는 파라미터 격자(grid)의 모든 조합을 <strong>교차검증(cross-validation)</strong>으로 평가해
  평균 점수가 가장 높은 조합을 고른다. 한 번의 train/test 분할에 운이 좌우되지 않도록, train을 다시 5겹으로 쪼개
  돌아가며 검증한다.</p>

  <blockquote class="cite">
    "GridSearchCV exhaustively generates candidates from a grid of parameter values …
    cross-validation is then used to evaluate each candidate and the best combination is retained."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/grid_search.html" target="_blank" rel="noopener">Tuning the hyper-parameters (GridSearchCV)</a></span>
  </blockquote>

  <div class="qbox">
    <span class="label">가설</span>
    네 파라미터(<code>max_depth</code>·<code>min_samples_split</code>·<code>min_samples_leaf</code>·<code>criterion</code>)를
    144개 조합으로 훑어 5겹 교차검증으로 고르면, 그 "최적" 트리는 기본 트리보다 test 정확도가 같거나 높을 것이다.
  </div>

  <h3 class="step">테스트</h3>
  <div class="terminal">
    <div class="terminal-header">practice04_runner.py §03 · GridSearchCV(cv=5) — best params · best cv 정확도 · test 비교 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_03@@</pre>
  </div>

  <h3 class="step">관찰 — 예상 밖이었다</h3>
  <div class="keypoint">
    <span class="label">FAILURE → CLUE</span>
    GridSearchCV가 고른 최적 조합은 <code>criterion='entropy', max_depth=3, min_samples_leaf=1, min_samples_split=5</code>,
    5겹 교차검증 평균 정확도 <strong>0.8860</strong>이었다. 그런데 이 "최적" 트리의 test 정확도는 <strong>0.9074</strong>로,
    기본 트리의 0.9630보다 오히려 <strong>0.0556 낮았다.</strong> 가설이 성립하지 않았다.
  </div>
  <p>왜 이런 일이 생겼나. 핵심은 데이터가 작다는 것이다. wine은 train이 124행뿐이라, 5겹으로 쪼개면 한 겹의
  검증셋이 25행 안팎이다. 이 작은 검증셋에서 잰 "평균 0.886"과, 우리가 따로 떼어 둔 단 한 번의 test 분할(54행)에서
  잰 "0.963"은 둘 다 표본이 작아 흔들린다. GridSearchCV는 "교차검증 점수가 가장 높은" 조합을 고를 뿐,
  내가 들고 있는 그 특정 test 분할에서 1등을 보장하지 않는다.</p>

  <div class="callout">
    <span class="label">함정</span>
    "GridSearchCV가 고른 게 무조건 최고"가 아니다. 데이터가 작으면 교차검증 점수도 test 점수도 분산이 커서,
    CV 1등이 test 1등과 어긋날 수 있다. GridSearchCV가 주는 건 <strong>한 번의 분할 운에 덜 휘둘리는 추정치</strong>이지,
    특정 test 점수의 최댓값이 아니다. 그래서 작은 데이터일수록 CV 점수와 test 점수를 함께 보고 판단해야 한다.
  </div>

  <div class="bridge">
    <strong>분류 트리는 여기서 정리됐다</strong> — wine은 얕은 트리만으로도 천장에 닿아 튜닝 여지가 작았다.
    그렇다면 트리가 "무엇을 보고" 와인을 갈랐는지(과제 문제6·7)를 들여다보면, 이 높은 정확도의 원인이 보일 것이다.
  </div>
</section>

<!-- ===================== CH 05 ===================== -->
<section id="ch5">
  <h2 class="chap"><span class="num">CH 05</span>트리의 해석 — 루트 노드는 어떤 특성으로 가르나<a href="#ch5" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>트리의 장점은 "왜 그렇게 판단했는지"를 들여다볼 수 있다는 것이다. 루트 노드는 전체 데이터를 처음 가르는 분기로,
  여기서 불순도(지니/엔트로피)를 가장 크게 줄이는 특성이 선택된다. <code>feature_importances_</code>는 각 특성이
  트리 전체에서 불순도를 줄인 양을 합산해 0~1로 정규화한 값이다.</p>

  <blockquote class="cite">
    "The importance of a feature is computed as the (normalized) total reduction of the criterion
    brought by that feature. It is also known as the Gini importance."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html#sklearn.tree.DecisionTreeClassifier.feature_importances_" target="_blank" rel="noopener">DecisionTreeClassifier.feature_importances_</a></span>
  </blockquote>

  <h3 class="step">테스트 — 특성 중요도와 루트 노드</h3>
  <div class="terminal">
    <div class="terminal-header">practice04_runner.py §04 · feature_importances_ · tree_.feature[0] — 중요 특성·루트 노드 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_04@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_IMP_CLF@@" alt="wine 분류 트리의 상위 특성 중요도 막대그래프">
    <figcaption>그림 2 · wine 분류(depth 4) — flavanoids·color_intensity·proline 세 특성에 중요도가 거의 다 몰려 있다</figcaption>
  </figure>

  <h3 class="step">관찰</h3>
  <div class="keypoint">
    <span class="label">관찰 결과</span>
    중요도는 <code>flavanoids</code>(0.405)와 <code>color_intensity</code>(0.397)에 거의 다 몰렸고, 루트 노드가
    처음 데이터를 가른 특성은 <code>color_intensity</code>였다. 13개 특성 중 7개는 중요도 0 — 트리가 아예 안 쓴 것이다.
    높은 정확도의 원인은 여기 있었다: wine 품종은 소수의 화학 성분(플라보노이드·색 강도·프롤린)만으로도 거의 갈라진다.
    그래서 깊은 트리가 필요 없었고(CH 03), 튜닝 여지도 작았다(CH 04).
  </div>

  <div class="bridge">
    <strong>이제 두 번째 트리로</strong> — 분류 트리는 데이터가 쉬워 과대적합이 잘 드러나지 않았다.
    회귀 과제(화이트와인 품질)는 정반대였다. 같은 트리 계열인 <code>DecisionTreeRegressor</code>를 기본값으로 돌리자마자,
    CH 02에서 살짝 비쳤던 "외움"이 이번엔 숨김없이 터졌다.
  </div>
</section>

<!-- ===================== CH 06 ===================== -->
<section id="ch6">
  <h2 class="chap"><span class="num">CH 06</span>하락 — 회귀트리 기본값의 test R2가 음수였다<a href="#ch6" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>회귀트리는 분류트리와 구조가 같되, 분할 기준이 불순도가 아니라 <strong>분산(또는 MSE)</strong>이고,
  리프가 내놓는 값은 라벨이 아니라 그 안에 떨어진 샘플들의 <strong>평균</strong>이다. 제약을 안 주면 트리는
  리프마다 샘플 한두 개가 남을 때까지 자라서 train을 통째로 외운다.</p>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    제약 없는 회귀트리(<code>max_depth=None</code>)는 train을 거의 외워 train R2가 1.0에 닿을 것이다.
    그러면 test R2는 분류 때보다 훨씬 크게 떨어질 것이다 — 회귀는 연속값이라 "외운 평균"이 처음 보는 샘플에서 더 크게 빗나가므로.
  </div>

  <h3 class="step">테스트 — 제약 없는 회귀트리</h3>
  <div class="terminal">
    <div class="terminal-header">practice04_runner.py §05 · DecisionTreeRegressor(winequality) — train/test R2·RMSE·MAE · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_05@@</pre>
  </div>

  <h3 class="step">관찰 — 예상보다 더 나빴다</h3>
  <div class="keypoint">
    <span class="label">FAILURE → CLUE</span>
    제약 없는 회귀트리는 깊이 <strong>28</strong>, 리프 <strong>1031개</strong>까지 자라 train R2 1.0000 — train을 완전히 외웠다.
    그 결과 test R2는 <strong>−0.5465</strong>. R2가 음수라는 건 "그냥 전체 평균값으로 찍는 것보다도 못하다"는 뜻이다.
    train-test R2 격차가 +1.55로, CH 02 분류 트리의 +0.037과는 차원이 다른 하락다. 외움(과대적합)의 위력이 회귀에서
    숨김없이 드러났다.
  </div>

  <div class="bridge">
    <strong>되살릴 차례다</strong> — CH 03에서 분류 트리는 깊이를 줄여도 test가 안 변했지만, 그건 데이터가 쉬워서였다.
    회귀트리는 깊이가 하락의 직접 원인이니, 깊이를 묶고 리프 최소 샘플을 키우면 일반화가 살아날 것이다.
  </div>
</section>

<!-- ===================== CH 07 ===================== -->
<section id="ch7">
  <h2 class="chap"><span class="num">CH 07</span>되살리기 — R2를 음수에서 +0.20으로<a href="#ch7" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    회귀트리가 낮아진 직접 원인은 무한정 자란 깊이다. <code>max_depth</code>를 작게 묶으면 test R2가 음수에서 양수로
    올라오되, 어느 깊이에서 최고가 되고 다시 떨어지는 <strong>봉우리</strong> 모양이 나올 것이다.
    거기에 <code>min_samples_leaf</code>(리프 최소 샘플)·<code>max_features</code>까지 GridSearchCV로 함께 고르면 최선의 조합이 잡힌다.
  </div>

  <blockquote class="cite">
    "max_depth: The maximum depth of the tree. … min_samples_leaf: The minimum number of samples
    required to be at a leaf node. … used to control over-fitting."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html" target="_blank" rel="noopener">DecisionTreeRegressor</a> (깊이·리프 제약)</span>
  </blockquote>

  <h3 class="step">테스트 — 깊이 곡선 + GridSearchCV</h3>
  <div class="terminal">
    <div class="terminal-header">practice04_runner.py §06 · max_depth 곡선 + GridSearchCV(r2) — baseline R2 → 튜닝 R2 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_06@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_REG_DEPTH@@" alt="회귀트리 max_depth에 따른 train/test R2 곡선">
    <figcaption>그림 3 · 회귀트리 깊이↑ → train R2는 1.0으로 차오르지만 test R2는 깊이 4에서 정점(0.207) 후 음수로 추락. 튜닝 후 test R2(점선)는 그 정점 부근에 안착</figcaption>
  </figure>

  <h3 class="step">관찰 — 봉우리가 나타났다</h3>
  <div class="keypoint">
    <span class="label">가설 통과</span>
    test R2는 깊이 4에서 <strong>0.2069</strong>로 최고가 되고, 깊이를 더 키우자 0.16 → 0.05 → −0.09 → (None)−0.55로 추락했다 —
    가설대로 봉우리 모양이다. GridSearchCV가 고른 조합은 <code>max_depth=3, min_samples_leaf=50, min_samples_split=2</code>,
    이 튜닝 트리의 test R2는 <strong>0.1982</strong>, RMSE는 baseline 0.9704 → <strong>0.6987</strong>로 줄었다.
    baseline 대비 R2 개선폭은 <strong>+0.7447</strong>(−0.5465 → +0.1982) — 음수에서 양수로 회복시켰다.
  </div>
  <p>다만 분류 때(CH 04)와 똑같은 겸손도 필요하다. 깊이 4 단독은 test R2 0.2069로 GridSearch가 고른 0.1982보다 약간 높다.
  GridSearchCV는 여전히 "test 점수 최댓값"이 아니라 "교차검증으로 본 안정적인 선택"을 줄 뿐이다. 중요한 건 단일 최고점이
  아니라, 깊이를 묶는 것만으로 −0.55의 하락을 +0.20 영역으로 끌어올렸다는 사실이다.</p>

  <div class="bridge">
    <strong>마지막으로</strong> — 회복한 회귀트리는 와인 품질을 무엇으로 갈랐을까? 분류 때(CH 05)처럼
    <code>feature_importances_</code>를 보면, 과제 답안에서 NN 가중치 기준 1등이었던 그 특성이 트리에서도 1등인지 확인할 수 있다.
  </div>
</section>

<!-- ===================== CH 08 ===================== -->
<section id="ch8">
  <h2 class="chap"><span class="num">CH 08</span>정리 — 트리 성능은 '얼마나 안 자라게 두느냐'에 달렸다<a href="#ch8" class="anchor-link">#</a></h2>

  <h3 class="step">테스트 — 회귀트리의 중요 특성</h3>
  <div class="terminal">
    <div class="terminal-header">practice04_runner.py §07 · 회귀트리 feature_importances_ · 루트 노드 — 와인 품질 결정 특성 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_07@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_IMP_REG@@" alt="화이트와인 품질 회귀트리의 상위 특성 중요도 막대그래프">
    <figcaption>그림 4 · 화이트와인 품질 회귀(depth 6) — alcohol 한 특성이 중요도 0.53으로 압도, 루트 노드도 alcohol</figcaption>
  </figure>
  <p>회귀트리도 <code>alcohol</code>을 루트 노드로 골랐고 중요도 0.5335로 가장 큰 비중이었다. 과제에서 PyTorch 신경망의
  첫 층 가중치 절댓값 평균으로 봤을 때도 <code>alcohol</code>(0.1814)이 1등이었는데, 완전히 다른 모델인 회귀트리가
  같은 결론에 닿았다. 알코올 도수가 화이트와인 품질을 가르는 가장 강한 신호라는 게 모델을 가로질러 일관되게 나타난 것이다.</p>

  <h3 class="step">최종 결론 — 출발 의문 회수</h3>
  <div class="keypoint">
    <span class="label">FINAL CONCLUSION</span>
    CH 01의 의문 "분류 트리와 회귀 트리는 무엇이 다른가"의 답: 구조는 같고, <strong>리프가 라벨을 내놓느냐 평균을 내놓느냐</strong>가 다르다.
    그리고 둘을 관통하는 한 가지 — <strong>트리의 성능은 모델을 키우는 게 아니라 '얼마나 안 자라게 두느냐'에 달렸다.</strong>
    분류는 데이터가 쉬워 얕은 트리로도 0.963에 닿았고 깊이를 키워도 변화가 없었으며(CH 03), GridSearchCV조차 그 천장을
    넘지 못했다(CH 04). 회귀는 깊이를 풀자 R2가 −0.55로 하락했고(CH 06), 깊이를 3으로 묶자 +0.20으로 회복됐다(CH 07).
    그리고 두 트리 모두 소수의 핵심 특성(분류=flavanoids·color_intensity, 회귀=alcohol)만으로 판단했다(CH 05·08).
  </div>

  <h3 class="step">한 문장으로</h3>
  <div class="keypoint">
    <span class="label">ONE-LINER</span>
    "트리를 튜닝한다"의 실체는 — <strong>분할을 어디서 멈출지(깊이·리프·분할 최소 샘플)를 정해 train을 외우지 못하게 묶는 일</strong>이고,
    그 묶음의 정도는 데이터가 쉬운지(wine)·어려운지(white wine)에 따라 다르다. GridSearchCV는 그 묶음을 한 번의 분할 운에
    덜 휘둘리게 골라 주는 도구이되, 작은 데이터에선 그 추천을 test 점수와 함께 의심하며 봐야 한다.
  </div>

  <div class="ref-chain">
    <p class="ref-title">📚 전체 근거 출처</p>
    <ol>
      <li><strong>공식 문서</strong>
        <a href="https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html" target="_blank" rel="noopener">scikit-learn · DecisionTreeClassifier</a>,
        <a href="https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html" target="_blank" rel="noopener">DecisionTreeRegressor</a>,
        <a href="https://scikit-learn.org/stable/modules/grid_search.html" target="_blank" rel="noopener">GridSearchCV</a>,
        <a href="https://scikit-learn.org/stable/modules/tree.html" target="_blank" rel="noopener">Decision Trees</a>.</li>
      <li><strong>workspace</strong>
        <code>../ml_workspace/from_colab/0601-s/</code> : 의사결정트리·회귀트리 과제 문제지와 풀이
        (<code>의사결정트리_실습문제1.txt</code>, <code>회귀트리_실습문제.txt</code>, <code>회귀트리_성능향상.ipynb</code>).</li>
      <li><strong>데이터셋</strong>
        sklearn 내장 <code>load_wine</code>(분류, 178×13),
        UCI <code>winequality-white.csv</code>(회귀, 4898×11, 과제 동일 데이터).</li>
      <li><strong>강의자료</strong>
        <code>.study/pdf/머신러닝_결정트리_회귀트리.pdf</code> (배경지식).</li>
      <li><strong>실행 검증</strong>
        <code>.study/test/practice04_tree/practice04_runner.py §00~§07</code>
        → <code>logs/*.txt</code>, <code>charts/*.png</code> (고정 시드 42, 재현 가능).</li>
    </ol>
  </div>
</section>
</main>

<footer>
  <p>SK 네트웍스 AI Family 32기 · 교과목 2 단원 2 머신러닝 실습4(과제) — 결정트리·회귀트리 (2026-06-01)</p>
  <p>모든 터미널 출력은 <code>.study/test/practice04_tree/practice04_runner.py</code> 실제 실행 결과이며,
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
zw = HTML.count("​")
print(f"파일: {OUT}")
print(f"terminal div: {n_term} | terminal-body: {n_body} | (일치={n_term==n_body})")
print(f"외부 URL img: {len(http_imgs)} (0이어야 함) | base64 img: {b64_imgs}")
print(f"chap: {HTML.count('h2 class=\"chap\"')} | qbox: {HTML.count('class=\"qbox\"')} | keypoint: {HTML.count('class=\"keypoint\"')}")
print(f"zero-width space: {zw} | 미치환 placeholder: {leftover} | 크기: {len(HTML)//1024} KB")
