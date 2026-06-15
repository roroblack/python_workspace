# build_day0602_html.py
# day0602_ensemble.html 조립 — logs/*.txt(실제 실행 결과) + charts/*.png(base64) 주입
# 실행: c:\_proj\python_workspace\.venv\Scripts\python.exe build_day0602_html.py
#   (= GUIDE §11 run_all 역할: 터미널 값 직접 작성 금지, 로그에서 주입 / §12 터미널 div==body 자가검증)
#   문체: day0527_ml_intro / day0529_svm 의 "의문→해결→새 의문" 서사 추적 방식.
import base64, html, pathlib, re

HERE = pathlib.Path(__file__).parent
LOGS = HERE / "logs"
CHARTS = HERE / "charts"
OUT = HERE.parent.parent / "blog" / "day0602_ensemble.html"   # .study/blog/
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
    "@@TERM_00@@": term("00_single_tree"),
    "@@TERM_01@@": term("01_bagging"),
    "@@TERM_02@@": term("02_random_forest"),
    "@@TERM_03@@": term("03_boosting"),
    "@@TERM_04@@": term("04_compare"),
    "@@TERM_05@@": term("05_feature_importance"),
    "@@CHART_NEST@@": chart("ch_n_estimators.png"),
    "@@CHART_CMP@@": chart("ch_model_compare.png"),
    "@@CHART_GAP@@": chart("ch_overfit_gap.png"),
    "@@CHART_IMP@@": chart("ch_feature_importance.png"),
}

HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>파이썬 머신러닝 분석: 트리 하나가 불안하다면 — 배깅·부스팅·랜덤포레스트로 모으는 법</title>
  <meta name="description" content="SK 네트웍스 AI Family 32기 머신러닝 Day5. '결정트리 하나는 왜 흔들리나', '여러 모델을 모으면 정말 나아지나', '분산을 줄이는 배깅과 편향을 줄이는 부스팅은 무엇이 다른가'라는 의문을 따라 단일 트리·BaggingClassifier·RandomForest·AdaBoost·GradientBoosting 의 정확도와 과대적합 gap, n_estimators 효과, 특성 중요도를 sklearn 실행으로 검증한 기록.">
  <meta property="og:title" content="파이썬 머신러닝 분석: 트리 하나가 불안하다면 — 앙상블로 모으는 법">
  <meta property="og:description" content="단일 트리의 분산 → 배깅으로 분산 줄이기 → 랜덤포레스트 → 부스팅으로 편향 줄이기 → 다섯 모델 정확도·과대적합 비교, 실측으로 추적">
  <meta property="og:type" content="article">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="파이썬 머신러닝 분석: 트리 하나가 불안하다면 — 앙상블로 모으는 법">
  <meta name="twitter:description" content="배깅(분산↓)·부스팅(편향↓)·랜덤포레스트를 sklearn 으로 비교 추적">
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
  <p class="eyebrow">Python · 머신러닝(교과목 2 · 단원 2) Day5 · 부트캠프</p>
  <h1>트리 하나가 불안하다면 — 배깅·부스팅·랜덤포레스트로 모으는 법</h1>
  <p class="deck">결정트리는 데이터를 가르는 규칙을 스스로 찾아 주지만, 그 트리 하나는 의외로 약하다 —
  학습 데이터를 통째로 과하게 학습하고(과대적합), 시드 하나만 바꿔도 정확도가 출렁인다.
  그렇다면 <strong>모델 하나가 흔들릴 때, 여러 개를 모으면 정말 나아질까?</strong>
  이 글은 그 한 질문에서 출발해 — 분산을 줄이는 배깅과 랜덤포레스트, 편향을 줄이는 부스팅(AdaBoost·GBM)을
  같은 데이터 위에 세워 놓고 정확도와 과대적합을 직접 비교한 기록이다.
  모든 수치는 sklearn 으로 직접 돌린 결과이며 <code>random_state=42</code> 로 재현 가능하다.</p>
  <div class="meta-row">
    <span><strong>날짜</strong>2026-06-02</span>
    <span><strong>Python</strong>@@PY@@ · scikit-learn 1.8.0 · NumPy 2.4.4 · Pandas 3.0.2</span>
    <span><strong>OS</strong>Windows 11 Pro 25H2</span>
    <span><strong>IDE</strong>VS Code 1.117.0</span>
    <span><strong>HW</strong>Asrock x600 · Ryzen 8600G · 24GB LPDDR5 · RTX 4070 Super 12GB</span>
    <span><strong>커리큘럼</strong>교과목 2 · 단원 2 · 머신러닝 Day5 — 머신러닝_알고리즘_앙상블.pdf</span>
  </div>
</header>

<main>
<nav class="flow">
  <h2>이 글의 흐름 — '트리 하나'의 불안에서 갈라져 나온 질문들</h2>
  <ol>
    <li><a href="#ch1">시작 — 단일 결정트리는 왜 불안한가 (외우고, 흔들린다)</a></li>
    <li><a href="#ch2">배깅 — 부트스트랩으로 여러 트리를 모으면 <span class="turn">분산</span>이 줄까</a></li>
    <li><a href="#ch3">랜덤포레스트 — 특성까지 무작위로, 그리고 트리는 몇 개면 충분한가</a></li>
    <li><a href="#ch4"><span class="turn">방향 전환</span> — 분산이 아니라 편향을 줄이는 부스팅(AdaBoost·GBM)</a></li>
    <li><a href="#ch5">한 자리 비교 — 단일 트리 vs 배깅 vs RF vs AdaBoost vs GBM</a></li>
    <li><a href="#ch6">과대적합은 정말 줄었나 — train−test gap 으로 다시 보기</a></li>
    <li><a href="#ch7">덤으로 얻는 것 — 랜덤포레스트가 알려 주는 특성 중요도</a></li>
    <li><a href="#ch8">정리 — 언제 무엇을 쓰나, 그리고 '모으면 나아진다'의 조건</a></li>
  </ol>
</nav>

<!-- ===================== CH 01 ===================== -->
<section id="ch1">
  <h2 class="chap"><span class="num">CH 01</span>시작 — 단일 결정트리는 왜 불안한가<a href="#ch1" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>결정트리는 데이터를 가장 잘 가르는 질문을 위에서부터 차례로 던진다. 맨 위가 <strong>루트 노드</strong>,
  더 갈라지지 않는 끝이 <strong>터미널(리프) 노드</strong>다. 깊이에 제한을 두지 않으면 트리는 train 데이터의
  마지막 한 점까지 통과하도록 계속 갈라진다. 편하지만 위험하다 — <code>fit</code> 한 그 데이터는 100% 맞히면서
  처음 보는 데이터에서는 오류하기 쉽다.</p>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    깊이 제한 없는 단일 트리는 ① train 정확도가 1.0에 붙고(외운다), ② <code>random_state</code>만 바꿔도
    test 정확도가 눈에 띄게 출렁일 것이다(구조가 데이터에 민감 = <strong>분산이 크다</strong>).
    이 두 가지가 확인되면 "트리 하나는 불안하다"는 진단이 선다.
  </div>
  <p><code>load_breast_cancer</code>(악성/양성 진단, 특성 30개)로 단일 트리를 세우고, train/test 정확도와
  깊이·리프 수를 본 뒤, 시드만 0~9로 바꿔 가며 test 정확도가 얼마나 흔들리는지 측정한다.</p>

  <pre><code class="language-python"># path : .study/test/ensemble/ensemble_runner.py §00 (발췌)
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

full = DecisionTreeClassifier(random_state=42).fit(Xtr, ytr)
print(accuracy_score(ytr, full.predict(Xtr)))   # train acc
print(accuracy_score(yte, full.predict(Xte)))   # test acc
print(full.get_depth(), full.get_n_leaves())     # 깊이 · 터미널 노드 수

accs = [accuracy_score(yte, DecisionTreeClassifier(random_state=s).fit(Xtr, ytr).predict(Xte))
        for s in range(10)]
print(accs.std())                                # seed 만 바꿨을 때의 출렁임</code></pre>

  <h3 class="step">테스트</h3>
  <div class="terminal">
    <div class="terminal-header">ensemble_runner.py §00 · DecisionTreeClassifier — train 외움 · seed별 분산 확인 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_00@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT — 가설 통과</span>
    train acc 1.0000(완전히 외웠다)인데 test acc 0.9231, 과대적합 gap +0.0769. 그리고 시드만 0~9로 바꿨을 뿐인데
    test acc 가 0.9091~0.9371 사이에서 출렁이고 표준편차가 0.0104였다. <strong>트리 하나는 외우고, 흔들린다.</strong>
  </div>

  <div class="bridge">
    <strong>여기서 떠오른 생각</strong> — 시드마다 트리가 제각각 다른 답을 낸다면, 그 답들의 <em>평균</em>은
    개별 트리보다 덜 흔들리지 않을까? 같은 데이터를 조금씩 다르게 보여 준 여러 트리를 모아 투표시키면 어떻게 될까.
  </div>
</section>

<!-- ===================== CH 02 ===================== -->
<section id="ch2">
  <h2 class="chap"><span class="num">CH 02</span>배깅 — 모으면 분산이 줄까<a href="#ch2" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p><strong>배깅(Bagging, Bootstrap Aggregating)</strong>은 train 에서 <em>복원 추출</em>로 매번 다른 표본(부트스트랩)을
  뽑아 같은 모델을 여러 개 독립적으로 학습시킨 뒤, 분류는 다수결로 합친다. 핵심은 "여러 추정량의 평균은 개별보다
  분산이 작다"는 통계의 성질이다.</p>

  <blockquote class="cite">
    "A Bagging classifier is an ensemble meta-estimator that fits base classifiers each on random subsets
    of the original dataset and then aggregate their individual predictions … to form a final prediction.
    Such a meta-estimator can typically be used as a way to reduce the variance of a black-box estimator."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.BaggingClassifier.html" target="_blank" rel="noopener">BaggingClassifier</a></span>
  </blockquote>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    CH 01의 그 불안한 트리를 <code>BaggingClassifier</code>로 100개 모으면, ① test 정확도는 단일 트리보다 오르고,
    ② 시드별 출렁임(표준편차)은 단일 트리의 0.0104보다 작아질 것이다. 분산을 줄이는 게 배깅의 일이니까.
  </div>

  <h3 class="step">테스트</h3>
  <div class="terminal">
    <div class="terminal-header">ensemble_runner.py §01 · BaggingClassifier(트리100) — 단일 트리 대비 정확도·분산 비교 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_01@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT — 가설 통과</span>
    배깅 test acc 0.9510 (단일 트리 0.9231 → <strong>+0.0280</strong>). 시드별 표준편차는 0.0104 → <strong>0.0066</strong>으로
    줄었다. 정확도는 오르고 출렁임은 작아졌다 — 가설대로 <strong>배깅은 분산을 깎는다</strong>.
    다만 train acc 는 여전히 1.0000이라 gap 은 남아 있다.
  </div>

  <div class="bridge">
    <strong>한 발 더</strong> — 배깅한 트리들은 같은 특성을 비슷하게 보다 보니 서로 닮아 있다(상관이 높다).
    닮은 것들을 평균 내면 분산이 덜 줄어든다. 트리들을 <em>더 서로 다르게</em> 만들 방법이 있다면 효과가 더 클 텐데?
  </div>
</section>

<!-- ===================== CH 03 ===================== -->
<section id="ch3">
  <h2 class="chap"><span class="num">CH 03</span>랜덤포레스트 — 특성까지 무작위로<a href="#ch3" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p><strong>랜덤포레스트</strong>는 배깅에 한 가지를 더한다 — 각 분기에서 전체 특성이 아니라 <em>무작위로 고른 일부 특성</em>
  안에서만 최선의 분할을 찾는다. 그러면 트리마다 보는 곳이 달라져 서로 덜 닮고(상관↓), 평균의 분산 감소 효과가 커진다.</p>

  <blockquote class="cite">
    "In random forests … each tree in the ensemble is built from a sample drawn with replacement …
    when splitting each node during the construction of a tree, the best split is found either from all input features
    or a random subset of size <code>max_features</code>. … the bias … increases slightly … but, due to averaging,
    its variance also decreases, usually more than compensating."
    <span class="src">— scikit-learn User Guide · <a href="https://scikit-learn.org/stable/modules/ensemble.html#random-forests" target="_blank" rel="noopener">Random forests</a></span>
  </blockquote>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    트리를 많이 모을수록 test 정확도가 오르지만 무한히 오르진 않고 <strong>어느 지점에서 수렴</strong>할 것이다
    (배깅 계열은 트리를 더 넣어도 과대적합이 폭주하지 않는다). <code>n_estimators</code>를 1→400으로 늘려 확인한다.
  </div>

  <h3 class="step">테스트</h3>
  <div class="terminal">
    <div class="terminal-header">ensemble_runner.py §02 · RandomForestClassifier — n_estimators 1→400 정확도 수렴 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_02@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_NEST@@" alt="n_estimators 증가에 따른 test 정확도 곡선">
    <figcaption>그림 0602-1 · 트리 1개(0.9231) → 100개 부근에서 0.9580으로 올라 평탄해진다 — 더 넣어도 수렴, 낮아지지 않음</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT — 가설 통과</span>
    트리 1개일 때 0.9231 → 100개에서 0.9580 → 200·400개도 0.9580으로 평탄했다(향상 +0.0350).
    트리를 더 넣는다고 부스팅처럼 과대적합으로 낮아지지 않고 <strong>완만히 수렴</strong>한다. "트리는 많을수록 안전하되,
    수익은 체감"이라는 게 랜덤포레스트의 성격이다.
  </div>

  <div class="bridge">
    <strong>방향을 바꿔 본다</strong> — 배깅·랜덤포레스트는 트리들을 <em>나란히 독립</em>으로 키워 분산을 줄였다.
    그런데 train acc 는 여전히 1.0이다. 분산이 아니라 <em>편향</em> 자체를 줄이려면? 트리를 나란히가 아니라
    <strong>순서대로</strong> 세워, 앞 모델이 틀린 곳을 뒤 모델이 메우게 하면 어떨까.
  </div>
</section>

<!-- ===================== CH 04 ===================== -->
<section id="ch4">
  <h2 class="chap"><span class="num">CH 04</span>방향 전환 — 편향을 줄이는 부스팅<a href="#ch4" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p><strong>부스팅(Boosting)</strong>은 약한 학습기(weak learner, 예: 깊이 1짜리 '그루터기')를 <em>순차로</em> 쌓는다.
  <strong>AdaBoost</strong>는 앞 모델이 틀린 샘플에 가중치를 더 줘 다음 모델이 그쪽에 집중하게 하고,
  <strong>GradientBoosting</strong>은 앞 단계의 <em>잔차(오차)</em>를 다음 트리가 예측하도록 이어 붙인다.
  배깅이 분산을 줄였다면, 부스팅은 약한 모델을 합쳐 <strong>편향</strong>을 줄인다.</p>

  <blockquote class="cite">
    "The core principle of AdaBoost is to fit a sequence of weak learners … on repeatedly modified versions of the data.
    The predictions … are then combined through a weighted majority vote … The data modifications … consist of
    applying weights to each of the training samples."
    <span class="src">— scikit-learn User Guide · <a href="https://scikit-learn.org/stable/modules/ensemble.html#adaboost" target="_blank" rel="noopener">AdaBoost</a></span>
  </blockquote>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    깊이 1짜리 그루터기 하나는 단일 깊은 트리만 못하다. 하지만 그것을 AdaBoost로 200개 순차로 모으면
    단일 트리(0.9231)를 <strong>넘어설</strong> 것이다. GradientBoosting(깊이3·200개)도 마찬가지로 강해질 것이다.
  </div>

  <h3 class="step">테스트</h3>
  <div class="terminal">
    <div class="terminal-header">ensemble_runner.py §03 · AdaBoost / GradientBoosting — 약한 학습기를 순차로 모으기 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_03@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT — 가설 통과</span>
    깊이1 그루터기 하나는 0.9231에 불과했지만, AdaBoost로 200개 순차로 모으니 <strong>0.9720</strong>까지 올랐다.
    GradientBoosting(깊이3·200개)은 0.9580. 약한 모델을 "이전 오차에 집중"시키며 쌓는 것만으로 강한 모델이 됐다 —
    이게 편향을 줄이는 부스팅의 핵심이다.
  </div>

  <div class="bridge">
    <strong>이제 한자리에 모은다</strong> — 분산을 줄인 쪽(배깅·RF)과 편향을 줄인 쪽(AdaBoost·GBM),
    그리고 출발점이던 단일 트리를 <em>같은 train/test 위</em>에 세워 정확도를 직접 겨뤄 본다.
  </div>
</section>

<!-- ===================== CH 05 ===================== -->
<section id="ch5">
  <h2 class="chap"><span class="num">CH 05</span>한 자리 비교 — 다섯 모델을 겨루다<a href="#ch5" class="anchor-link">#</a></h2>

  <h3 class="step">실험 → 관찰</h3>
  <p>같은 <code>train_test_split</code>(시드 42) 위에서 다섯 모델을 한 번에 학습시켜 test 정확도와
  과대적합 gap(train−test)을 함께 찍는다. "여러 모델을 모으면 단일 트리보다 나은가"의 직접 답이다.</p>
  <div class="terminal">
    <div class="terminal-header">ensemble_runner.py §04 · 단일트리/배깅/RF/AdaBoost/GBM — test 정확도·gap 일괄 비교 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_04@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_CMP@@" alt="다섯 모델의 test 정확도 막대 비교">
    <figcaption>그림 0602-2 · 단일 트리(0.923)가 가장 낮고, 모든 앙상블이 그 위에 — 이 데이터에선 AdaBoost(0.972)가 최고</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">관찰 결과</span>
    단일 트리 0.9231이 바닥, 배깅 0.9510 · 랜덤포레스트 0.9580 · GBM 0.9580 · AdaBoost 0.9720 순으로
    <strong>모든 앙상블이 단일 트리를 넘었다</strong>. 이 데이터·이 설정에서는 부스팅(AdaBoost)이 가장 높았다.
    "모으면 나아진다"는 일단 사실로 확인된다 — 그런데 <em>왜</em> 나아졌나? 정확도만으로는 분산을 줄인 건지
    편향을 줄인 건지 구분되지 않는다.
  </div>

  <div class="bridge">
    <strong>다음 질문</strong> — 정확도가 오른 이유를 보려면 train 과 test 의 <em>차이</em>를 봐야 한다.
    과대적합이 줄어서 오른 거라면, 앙상블의 gap 이 단일 트리의 +0.0769보다 작아야 한다. 정말 그런가?
  </div>
</section>

<!-- ===================== CH 06 ===================== -->
<section id="ch6">
  <h2 class="chap"><span class="num">CH 06</span>과대적합은 정말 줄었나<a href="#ch6" class="anchor-link">#</a></h2>

  <h3 class="step">관찰 → 정리</h3>
  <p>CH 05 표의 gap 열을 다시 본다. 흥미롭게도 다섯 모델 모두 train acc 는 1.0000이다 —
  그렇다면 gap 의 차이는 전적으로 <strong>test 가 얼마나 따라왔느냐</strong>로 결정된다. gap 이 작다는 건
  "외운 만큼 처음 보는 데이터에서도 통했다"는 뜻이다.</p>
  <figure class="shot">
    <img src="@@CHART_GAP@@" alt="모델별 과대적합 gap 막대">
    <figcaption>그림 0602-3 · 과대적합 gap(train−test) — 단일 트리 0.077이 가장 크고, 앙상블로 갈수록 줄어 AdaBoost가 0.028로 최소</figcaption>
  </figure>

  <div class="callout">
    <span class="label">함정</span>
    "train acc 가 1.0이니 모두 똑같이 과대적합"이라고 읽으면 안 된다. 과대적합의 실질은 <em>train 과 test 의 격차</em>다.
    train 이 1.0이어도 test 가 거의 따라오면(gap 작음) 일반화는 좋은 것이다. 단일 트리의 1.0과 앙상블의 1.0은 성격이 다르다.
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT — 가설 통과</span>
    과대적합 gap: 단일 트리 +0.0769 → 배깅 +0.0490 → RF +0.0420 = GBM +0.0420 → AdaBoost +0.0280.
    <strong>모든 앙상블의 gap 이 단일 트리보다 작다</strong>. 정확도가 오른 건 우연이 아니라 과대적합이 실제로
    완화됐기 때문이다 — 배깅·RF는 분산을 깎아서, 부스팅은 편향까지 줄이며 test 를 끌어올려서.
  </div>

  <div class="bridge">
    <strong>덤이 하나 있다</strong> — 랜덤포레스트는 정확도만 주는 게 아니라, 학습 과정에서 "어떤 특성이 분류에
    크게 기여했나"를 <em>부산물</em>로 알려 준다. 30개 특성 중 무엇이 악성/양성 진단을 갈랐는지 들여다본다.
  </div>
</section>

<!-- ===================== CH 07 ===================== -->
<section id="ch7">
  <h2 class="chap"><span class="num">CH 07</span>덤으로 얻는 것 — 특성 중요도<a href="#ch7" class="anchor-link">#</a></h2>

  <h3 class="step">학습 → 의문</h3>
  <p>트리는 각 분기에서 불순도(지니/엔트로피)를 가장 많이 줄이는 특성을 고른다. 그 "불순도를 줄인 양"을
  모든 트리에 걸쳐 합치면 특성별 기여도가 나온다 — 이게 <code>feature_importances_</code>다. 전체 합은 1이 된다.</p>
  <div class="qbox">
    <span class="label">의문</span>
    breast_cancer 30개 특성 중, 랜덤포레스트(트리 300개)가 가장 크게 의지한 특성 상위 10개는 무엇이며,
    그 중요도의 합은 정말 1로 정규화되어 있을까?
  </div>

  <blockquote class="cite">
    "The relative rank (i.e. depth) of a feature used as a decision node in a tree can be used to assess
    the relative importance of that feature … features used at the top of the tree contribute to the final
    prediction decision of a larger fraction of the input samples."
    <span class="src">— scikit-learn User Guide · <a href="https://scikit-learn.org/stable/modules/ensemble.html#feature-importance-evaluation" target="_blank" rel="noopener">Feature importance evaluation</a></span>
  </blockquote>

  <h3 class="step">테스트</h3>
  <div class="terminal">
    <div class="terminal-header">ensemble_runner.py §05 · RandomForest.feature_importances_ — 상위 10 특성 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_05@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_IMP@@" alt="랜덤포레스트 특성 중요도 상위 10 막대">
    <figcaption>그림 0602-4 · worst perimeter·worst area·worst concave points 가 상위 — 종양 외곽 크기/오목점이 진단을 크게 갈랐다</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT</span>
    중요도 합 = 1.0000으로 정규화돼 있고, 상위는 <code>worst perimeter</code>(0.1457)·<code>worst area</code>(0.1441)·
    <code>worst concave points</code>(0.1146)였다. 종양 외곽의 크기와 오목한 점 개수가 악성/양성을 가르는 핵심이었다.
    앙상블은 성능뿐 아니라 <strong>"무엇이 중요했나"라는 해석</strong>까지 덤으로 준다.
  </div>

  <div class="bridge">
    <strong>마지막 정리로</strong> — 분산을 줄이는 길과 편향을 줄이는 길, 그리고 그 덤까지 봤다.
    그럼 실제로 언제 무엇을 골라야 하나? 출발 질문 "모델 하나가 흔들릴 때 모으면 나아지는가"로 돌아간다.
  </div>
</section>

<!-- ===================== CH 08 ===================== -->
<section id="ch8">
  <h2 class="chap"><span class="num">CH 08</span>정리 — 언제 무엇을 쓰나<a href="#ch8" class="anchor-link">#</a></h2>

  <h3 class="step">비교 → 결정</h3>
  <p>두 갈래의 앙상블은 줄이는 대상이 다르다. 같은 "모으기"라도 목적이 다르므로 쓰임도 다르다.</p>
  <table>
    <thead>
      <tr><th>구분</th><th>배깅 / 랜덤포레스트</th><th>부스팅 (AdaBoost · GBM)</th></tr>
    </thead>
    <tbody>
      <tr><td>학습 방식</td><td>여러 모델을 <strong>병렬·독립</strong>으로</td><td>약한 모델을 <strong>순차</strong>로</td></tr>
      <tr><td>주로 줄이는 것</td><td class="hl">분산(variance)</td><td class="hl">편향(bias)</td></tr>
      <tr><td>기반 모델</td><td>깊은(강한) 트리</td><td>얕은(약한) 트리·그루터기</td></tr>
      <tr><td>트리 수↑ 영향</td><td>완만히 수렴, 잘 안 하락</td><td>너무 많으면 과대적합 위험</td></tr>
      <tr><td>이 실험 test acc</td><td>배깅 0.951 · RF 0.958</td><td>AdaBoost 0.972 · GBM 0.958</td></tr>
      <tr><td>언제</td><td>불안정한 모델 안정화·기본 강력 베이스라인</td><td>마지막 정확도 한 끗·정형 데이터 상위권</td></tr>
    </tbody>
  </table>

  <h3 class="step">최종 결론 — 출발 의문 회수</h3>
  <div class="keypoint">
    <span class="label">FINAL CONCLUSION</span>
    CH 01의 질문 "<strong>모델 하나가 흔들릴 때, 여러 개를 모으면 정말 나아지는가</strong>"의 답: <strong>그렇다, 단 방식에 따라 줄이는 것이 다르다.</strong>
    단일 트리는 외우고 흔들렸다(test 0.9231·gap +0.0769·시드 표준편차 0.0104). 배깅은 부트스트랩으로 분산을 깎았고
    (0.9510·gap +0.0490·표준편차 0.0066), 랜덤포레스트는 특성 무작위로 트리를 더 다르게 만들어 0.9580으로 수렴시켰다.
    부스팅은 약한 트리를 순차로 모아 편향까지 줄여 AdaBoost 0.9720까지 올렸다. 다섯 모델 모두 train 1.0이었지만
    <strong>gap 은 앙상블로 갈수록 작아졌다</strong> — 정확도 상승은 과대적합 완화의 결과였다.
  </div>

  <h3 class="step">한 문장으로</h3>
  <div class="keypoint">
    <span class="label">ONE-LINER</span>
    "여러 모델을 모으면 나아진다"의 실체는 — <strong>흔들리는 모델은 병렬로 모아 분산을 깎고(배깅·RF),
    약한 모델은 순차로 모아 편향을 줄인다(부스팅)</strong>는 것. 그래서 앙상블의 첫 질문은 "모델을 키울까"가 아니라
    "<strong>내 모델은 분산이 문제인가, 편향이 문제인가</strong>"이다.
  </div>

  <div class="ref-chain">
    <p class="ref-title">📚 전체 근거 출처</p>
    <ol>
      <li><strong>공식 문서</strong>
        <a href="https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.BaggingClassifier.html" target="_blank" rel="noopener">scikit-learn · BaggingClassifier</a>(분산 감소),
        <a href="https://scikit-learn.org/stable/modules/ensemble.html#random-forests" target="_blank" rel="noopener">Random forests</a>,
        <a href="https://scikit-learn.org/stable/modules/ensemble.html#adaboost" target="_blank" rel="noopener">AdaBoost</a>,
        <a href="https://scikit-learn.org/stable/modules/ensemble.html#gradient-boosting" target="_blank" rel="noopener">Gradient Boosting</a>,
        <a href="https://scikit-learn.org/stable/modules/ensemble.html#feature-importance-evaluation" target="_blank" rel="noopener">Feature importance</a>.</li>
      <li><strong>workspace</strong>
        <code>../ml_workspace/from_colab/0602-s/decision_tree_torch_random_forest_added.ipynb</code> 및
        <code>_bagging_added / _adaboost_added / _gradient_boosting_added.ipynb</code>
        : 수업 앙상블 흐름(DecisionTree → Bagging/RF/AdaBoost/GBM, <code>n_estimators</code>·<code>feature_importances_</code>).</li>
      <li><strong>강의자료</strong>
        <code>.study/pdf/머신러닝_알고리즘_앙상블.pdf</code> (배경지식).</li>
      <li><strong>실행 검증</strong>
        <code>.study/test/ensemble/ensemble_runner.py §00~§05</code>
        → <code>logs/*.txt</code>, <code>charts/*.png</code> (고정 시드 42, 재현 가능).</li>
    </ol>
  </div>
</section>
</main>

<footer>
  <p>SK 네트웍스 AI Family 32기 · 교과목 2 단원 2 머신러닝 Day5 (2026-06-02)</p>
  <p>모든 터미널 출력은 <code>.study/test/ensemble/ensemble_runner.py</code> 실제 실행 결과이며,
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
print(f"파일: {OUT}")
print(f"terminal div: {n_term} | terminal-body: {n_body} | (일치={n_term==n_body})")
print(f"외부 URL img: {len(http_imgs)} (0이어야 함) | base64 img: {b64_imgs}")
print(f"chap: {HTML.count('h2 class=\"chap\"')} | qbox: {HTML.count('class=\"qbox\"')} | keypoint: {HTML.count('class=\"keypoint\"')}")
print(f"zero-width space: {zwsp} | 미치환 placeholder: {leftover} | 크기: {len(HTML)//1024} KB")
