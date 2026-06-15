# build_practice06_html.py
# ml_practice06_pca.html 조립 — logs/*.txt(실제 실행 결과) + charts/*.png(base64) 주입
# 실행: c:\_proj\python_workspace\.venv\Scripts\python.exe build_practice06_html.py
#   (= GUIDE §11 run_all 역할: 터미널 값 직접 작성 금지, 로그에서 주입)
#   문체: interpreter_base64.html / ml_practice05_ann.html 의 "의문→해결→새 의문" 서사 추적.
import base64, html, pathlib, re

HERE = pathlib.Path(__file__).parent
LOGS = HERE / "logs"
CHARTS = HERE / "charts"
OUT = HERE.parent.parent / "blog" / "ml_practice06_pca.html"   # .study/blog/
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
    "@@TERM_00@@": term("00_high_dim"),
    "@@TERM_01@@": term("01_knn_baseline"),
    "@@TERM_02@@": term("02_curse"),
    "@@TERM_03@@": term("03_pca_sweep"),
    "@@TERM_05@@": term("05_cumulative_variance"),
    "@@TERM_06@@": term("06_pca_2d"),
    "@@TERM_07@@": term("07_scaler_before_pca"),
    "@@TERM_08@@": term("08_loss_point"),
    "@@TERM_09@@": term("09_cost_efficiency"),
    "@@TERM_10@@": term("10_reconstruction"),
    "@@CHART_SWEEP@@": chart("ch_sweep.png"),
    "@@CHART_CUMVAR@@": chart("ch_cumvar.png"),
    "@@CHART_SCATTER@@": chart("ch_scatter2d.png"),
    "@@CHART_RECON@@": chart("ch_recon.png"),
}

HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>파이썬 머신러닝 PCA 분석: 차원의 저주에 걸린 KNN을 주성분 축소로 되살리다</title>
  <meta name="description" content="SK 네트웍스 AI Family 32기 머신러닝 실습6(과제). '특성이 30·64개나 되는 고차원에서 거리 기반 KNN은 왜 흔들리나(차원의 저주)'라는 의문을 따라, 유방암·digits 데이터에 PCA를 적용한다. 표준화 선행의 필요성, 주성분 수를 바꿔가며 찾은 정확도 sweet spot, 설명분산과 분류 성능의 어긋남, 그리고 차원축소가 손해로 바뀌는 지점까지 sklearn 실측으로 검증한 기록.">
  <meta property="og:title" content="차원의 저주에 걸린 KNN을 PCA 주성분 축소로 되살리다">
  <meta property="og:description" content="고차원 KNN의 한계 → 표준화 → PCA n_components sweep → 정확도 sweet spot → 설명분산 vs 성능 → 정보 손실 지점을 실측으로 추적">
  <meta property="og:type" content="article">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="PCA + KNN 차원축소 실습">
  <meta name="twitter:description" content="차원의 저주 → 표준화 → n_components sweep → sweet spot → 정보 손실 지점">
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
figure.shot img { display:block; width:100%; height:auto; max-width:820px; margin:0 auto; }
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
  <p class="eyebrow">Python · 머신러닝 실습6(과제) · 부트캠프</p>
  <h1>차원의 저주에 걸린 KNN을 PCA 주성분 축소로 되살리다</h1>
  <p class="deck">실습6 과제는 차원 축소(PCA·LDA·t-SNE)였다. 그런데 출발선에서 의문이 하나 걸렸다 —
  <strong>특성이 30개·64개나 되는 고차원에서, 거리로 분류하는 KNN은 왜 흔들릴까?</strong>
  이 글은 그 의문을 주어로 삼아 — 거리 기반 KNN에 표준화가 왜 먼저여야 하는지,
  64차원에서 '가깝다'는 개념이 어떻게 흐려지는지(차원의 저주), PCA로 주성분 수를 바꿔가며
  정확도 sweet spot을 어떻게 찾는지, 설명분산(정보 보존)과 분류 성능이 왜 어긋나는지,
  그리고 차원축소가 이득에서 손해로 바뀌는 지점이 어디인지를 하나씩 부딪쳐 본 기록이다.
  과제 colab(digits + PCA/LDA/t-SNE)과 KNN 실습을 합쳐, 유방암·digits 두 데이터로
  sklearn <code>PCA</code>+<code>KNeighborsClassifier</code> 위에서 옮겨 검증했고
  모든 수치는 <code>random_state=42</code>로 재현된다.</p>
  <div class="meta-row">
    <span><strong>날짜</strong>2026-06-04</span>
    <span><strong>Python</strong>@@PY@@ · scikit-learn 1.8.0 · NumPy 2.4.4 · Pandas 3.0.2</span>
    <span><strong>OS</strong>Windows 11 Pro 25H2</span>
    <span><strong>IDE</strong>VS Code 1.117.0</span>
    <span><strong>HW</strong>Asrock x600 · Ryzen 8600G · 24GB LPDDR5 · RTX 4070 Super 12GB</span>
    <span><strong>커리큘럼</strong>교과목 2 · 단원 2 · 머신러닝 — 머신러닝_차원축소_앙상블.pdf</span>
  </div>
</header>

<main>
<nav class="flow">
  <h2>이 글의 흐름 — 하나의 의문에서 갈라져 나온 질문들</h2>
  <ol>
    <li><a href="#ch1">시작 — 30·64개 특성의 고차원, KNN은 무엇으로 분류하나</a></li>
    <li><a href="#ch2">표준화를 안 한 KNN은 단위 큰 특성에 끌려간다</a></li>
    <li><a href="#ch3">차원의 저주 — 64차원에서 '가깝다'는 개념이 흐려진다</a></li>
    <li><a href="#ch4">PCA 투입 — 주성분 수를 바꿔가며 정확도를 훑다</a></li>
    <li><a href="#ch5">sweet spot — 절반 차원으로 전체보다 잘 맞히는 지점</a></li>
    <li><a href="#ch6"><span class="turn">어긋남</span> — 설명분산(정보)과 분류 정확도는 같이 가지 않는다</a></li>
    <li><a href="#ch7">2D 투영 — 64차원을 평면에 눌러도 클래스가 갈라지나</a></li>
    <li><a href="#ch8">표준화 선행 — PCA 앞에 StandardScaler가 없으면 주성분이 독점된다</a></li>
    <li><a href="#ch9">가성비 — '최고 정확도'가 아니라 '충분한 정확도를 가장 적은 차원으로'</a></li>
    <li><a href="#ch10">복원 — 8차원으로 줄인 digits를 되돌리면 얼마나 선명한가</a></li>
    <li><a href="#ch11">정리 — 차원축소가 손해로 바뀌는 지점, 그리고 '고차원 KNN' 의문 회수</a></li>
  </ol>
</nav>

<!-- ===================== CH 01 ===================== -->
<section id="ch1">
  <h2 class="chap"><span class="num">CH 01</span>시작 — 고차원에서 KNN은 무엇으로 분류하나<a href="#ch1" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>실습6 과제지는 차원 축소를 주제로 했다 — "<code>load_digits()</code>의 64차원 데이터에 PCA·LDA·t-SNE를
  적용해 차원을 줄이고 시각화하라." 그리고 바로 앞 KNN 실습은 Wisconsin 유방암 데이터를 거리 기반 KNN으로 분류했다.
  두 실습을 나란히 놓자 의문이 하나 생겼다. KNN은 "가장 가까운 이웃 k개"를 찾아 다수결로 분류하는데,
  그 '거리'는 모든 특성을 축으로 한 공간에서 잰다. 유방암은 30축, digits는 64축이다.</p>

  <blockquote class="cite">
    "Classifier implementing the k-nearest neighbors vote. … the query point is assigned the data class
    which has the most representatives within the nearest neighbors of the point."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html" target="_blank" rel="noopener">KNeighborsClassifier</a> (이웃 다수결)</span>
  </blockquote>

  <h3 class="step">의문 → 기준</h3>
  <div class="qbox">
    <span class="label">의문</span>
    KNN이 흔들릴지 아닐지는 모델 취향이 아니라 <strong>특성 공간의 차원</strong>에서 나온다.
    그러니 먼저 — 내가 다룰 두 데이터는 정확히 몇 차원이고, 그 축들의 스케일은 고른가?
    그 진단이 "차원축소가 필요한 자리인지"의 첫 단서다.
  </div>

  <h3 class="step">테스트 — 두 데이터의 차원을 진단한다</h3>
  <div class="terminal">
    <div class="terminal-header">load_breast_cancer / load_digits — 특성 수·클래스·스케일 진단 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_00@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT</span>
    유방암은 30특성·2클래스, digits는 64특성(8×8 픽셀)·10클래스 — 둘 다 사람이 직접 그릴 수 없는 고차원이다.
    그리고 유방암은 'mean area'(143~2501)와 'mean smoothness'(0.05~0.16)처럼 단위가 천 배 넘게 벌어져 있다.
    KNN은 이 공간에서 유클리드 거리를 재는데, 단위가 제각각이면 거리는 큰 특성 하나가 좌우한다 — 첫 함정이다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 단위가 천 배 벌어진 특성들로 거리를 재면 어떤 일이 벌어질까?
    표준화를 한 KNN과 안 한 KNN의 정확도를 같은 30특성으로 맞붙여, 거리 기반 모델의 첫 전제를 확인한다.
  </div>
</section>

<!-- ===================== CH 02 ===================== -->
<section id="ch2">
  <h2 class="chap"><span class="num">CH 02</span>표준화 없는 KNN은 단위 큰 특성에 끌려간다<a href="#ch2" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    KNN의 거리는 모든 특성의 차이를 제곱해 더한다. 단위가 큰 'mean area'의 차이가 수백~수천이면,
    0.x 단위인 'mean smoothness'의 차이는 거리에 거의 묻힌다. 그렇다면
    <strong><code>StandardScaler</code>로 모든 특성을 평균0·표준편차1로 맞춘 KNN이, 안 맞춘 KNN보다 정확해야 한다.</strong>
  </div>

  <pre><code class="language-python"># path : .study/test/practice06_pca/practice06_runner.py §01 (발췌)
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

# ① 표준화 없이 — 원본 30특성 그대로
knn_raw = KNeighborsClassifier(n_neighbors=5).fit(Xtr, ytr)
print(accuracy_score(yte, knn_raw.predict(Xte)))

# ② StandardScaler 후 — train 으로만 fit(leakage 방지)
sc = StandardScaler().fit(Xtr)
knn_std = KNeighborsClassifier(n_neighbors=5).fit(sc.transform(Xtr), ytr)
print(accuracy_score(yte, knn_std.predict(sc.transform(Xte))))</code></pre>

  <h3 class="step">테스트</h3>
  <div class="terminal">
    <div class="terminal-header">KNeighborsClassifier(k=5) on breast_cancer — 표준화 유무 정확도 비교 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_01@@</pre>
  </div>

  <blockquote class="cite">
    "Standardize features by removing the mean and scaling to unit variance. … Many elements used in the
    objective function of a learning algorithm … assume that all features are centered around zero and have
    variance in the same order."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html" target="_blank" rel="noopener">StandardScaler</a></span>
  </blockquote>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">가설 통과</span>
    표준화 없이 0.9123, <code>StandardScaler</code> 후 0.9561 — 표준화만으로 +0.0439 올랐다.
    거리 기반 KNN에서 표준화는 '선택'이 아니라 '전제'다. 단위가 큰 'area'가 거리를 독점하던 것을,
    모든 특성을 같은 자에 올려 풀어 준 결과다.
  </div>

  <div class="bridge">
    <strong>그런데 의심이 하나 남았다</strong> — 표준화로 스케일 문제를 풀어도, 특성 수 자체가 64개면?
    축이 많아질수록 점들이 서로 '비슷하게 멀어진다'는 차원의 저주를 들었다. digits 64특성에서
    표준화를 해도 KNN이 흔들리는지, '가깝다'는 개념이 실제로 흐려지는지 직접 재 본다.
  </div>
</section>

<!-- ===================== CH 03 ===================== -->
<section id="ch3">
  <h2 class="chap"><span class="num">CH 03</span>차원의 저주 — '가깝다'가 흐려진다<a href="#ch3" class="anchor-link">#</a></h2>

  <h3 class="step">학습 → 가설</h3>
  <p>차원이 늘면 공간의 부피가 지수적으로 커지고, 같은 수의 점은 그 안에서 점점 듬성듬성해진다.
  그 결과 어떤 점에서 봐도 '가장 가까운 이웃'과 '가장 먼 점'의 거리 차이가 줄어든다 — 모두가 비슷하게 멀어진다.
  KNN은 '가깝다'에 기대는데, 그 개념이 흐려지면 분류의 근거가 약해진다.</p>
  <div class="qbox">
    <span class="label">가설</span>
    digits 64특성을 표준화한 공간에서, 각 점의 (최근접 이웃 거리 ÷ 최원접 점 거리)를 재면
    그 비율이 0에서 멀지 않게(즉 가까운 점과 먼 점의 거리가 크게 다르지 않게) 나올 것이다.
    그게 곧 차원의 저주의 흔적이다.
  </div>

  <blockquote class="cite">
    "In high-dimensional spaces … the contrast between the nearest and the farthest neighbor diminishes,
    which can make nearest-neighbor based methods less effective. This phenomenon is often referred to as
    the curse of dimensionality."
    <span class="src">— scikit-learn User Guide · <a href="https://scikit-learn.org/stable/modules/neighbors.html" target="_blank" rel="noopener">Nearest Neighbors</a> (고차원에서의 한계)</span>
  </blockquote>

  <h3 class="step">테스트</h3>
  <div class="terminal">
    <div class="terminal-header">KNeighborsClassifier(k=5) on digits 64특성 — 정확도·시간·최근접/최원접 거리비 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_02@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">관찰 결과</span>
    digits 64특성 표준화 KNN은 정확도 0.9639로 아직 쓸 만하다. 하지만 최근접/최원접 거리비가 0.0932 —
    가장 가까운 이웃조차 가장 먼 점 거리의 9%대까지 멀어져 있다. 64차원이라 점들이 전반적으로 듬성듬성하다는 신호다.
    게다가 64차원 전체로 거리를 재느라 학습+예측에 66ms가 들었다. 정확도·속도 모두 개선 여지가 있다는 뜻이다.
  </div>

  <div class="bridge">
    <strong>다음 가설</strong> — 64개 축 중 상당수는 서로 겹치거나 잡음일 것이다. 분산이 큰 '진짜 정보' 축
    몇 개만 남기면, 차원이 줄어 거리가 또렷해지고 정확도·속도가 같이 좋아지지 않을까? 그 도구가 PCA다.
  </div>
</section>

<!-- ===================== CH 04 ===================== -->
<section id="ch4">
  <h2 class="chap"><span class="num">CH 04</span>PCA 투입 — 주성분 수를 바꿔가며 훑다<a href="#ch4" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p><strong>PCA(주성분 분석)</strong>는 데이터의 분산이 가장 큰 방향(주성분)을 차례로 찾아, 그 축들로 데이터를 다시 표현한다.
  분산이 큰 축일수록 데이터를 더 많이 설명하므로, 앞쪽 몇 개 주성분만 남기면 정보를 거의 잃지 않고 차원을 줄일 수 있다.
  파이프라인은 <code>StandardScaler → PCA(n) → KNN</code> 순서다.</p>

  <blockquote class="cite">
    "Linear dimensionality reduction using Singular Value Decomposition of the data to project it to a lower
    dimensional space. … PCA … keeps only the most significant singular vectors to project the data to a
    lower dimensional space."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html" target="_blank" rel="noopener">PCA</a></span>
  </blockquote>

  <div class="qbox">
    <span class="label">가설</span>
    <code>n_components</code>를 2부터 전체까지 늘리며 KNN 정확도를 재면, 처음엔 가파르게 오르다가
    어느 지점부터 평평해질 것이다. 그 '꺾이는 지점' 부근이 적은 차원으로 충분한 정확도를 내는 후보다.
  </div>

  <h3 class="step">테스트 — n_components를 2~전체까지 sweep</h3>
  <div class="terminal">
    <div class="terminal-header">StandardScaler → PCA(n) → KNN(k=5) — 유방암·digits n_components 스위프 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_03@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">관찰 결과</span>
    유방암은 주성분 2개만으로도 0.9211, digits는 2개일 때 0.5222로 출발한다. 둘 다 주성분을 늘릴수록 오르다가
    유방암 15개·digits 40개 부근에서 최고가 되는다. "차원을 늘릴수록 좋다"가 끝까지 가지 않고
    중간에 정점이 있다는 것 — 그 정점이 sweet spot이다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 표로는 정점이 어렴풋하다. 전체 특성 KNN 정확도를 기준선으로 깔고
    sweep을 곡선으로 그려, "최소 차원으로 전체 이상"인 sweet spot을 눈으로 확정한다.
  </div>
</section>

<!-- ===================== CH 05 ===================== -->
<section id="ch5">
  <h2 class="chap"><span class="num">CH 05</span>sweet spot — 절반 차원으로 전체를 넘다<a href="#ch5" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 기준</h3>
  <div class="qbox">
    <span class="label">기준</span>
    좋은 <code>n_components</code>의 기준은 "전체 특성 KNN 정확도 이상을, 가능한 한 적은 차원으로" 내는 것이다.
    전체 특성 정확도를 점선 기준으로 깔고, PCA+KNN 곡선이 그 선을 넘는 가장 작은 차원을 찾는다.
  </div>

  <h3 class="step">테스트 — 기준선 위에서 sweep 곡선을 본다</h3>
  <figure class="shot">
    <img src="@@CHART_SWEEP@@" alt="유방암·digits의 PCA 주성분 수에 따른 KNN 정확도 곡선과 전체 특성 기준선">
    <figcaption>그림 0604-1 · 주성분 수 vs KNN 정확도 — 주황 점선은 전체 특성 KNN, 보라 원이 sweet spot(유방암 n=15, digits n=40)</figcaption>
  </figure>
  <p>곡선은 가설대로 가파르게 오르다 평평해진다. 그리고 두 데이터 모두 곡선의 정점이 전체 특성 기준선(주황 점선)을
  살짝 넘는다 — 차원을 줄였는데 오히려 더 잘 맞힌 것이다.</p>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT — sweet spot 확정</span>
    유방암은 30특성 전체 0.9561 → <strong>주성분 15개</strong>(설명분산 0.9868)에서 0.9649, 즉 절반(50%) 차원으로 +0.0088.
    digits는 64특성 전체 0.9639 → <strong>주성분 40개</strong>(설명분산 0.9516)에서 0.9722, 62% 차원으로 +0.0083.
    차원을 줄였는데 정확도가 올랐다. PCA가 잡음 축을 걷어내 거리를 또렷하게 만든 결과다.
  </div>

  <div class="bridge">
    <strong>그런데 이상하다</strong> — digits sweet spot인 주성분 40개의 설명분산은 0.9516, 즉 정보의 95%만 남았는데
    정확도는 오히려 전체(100% 정보)보다 높다. '정보를 더 많이 담을수록 더 잘 맞힌다'가 아니라는 뜻이다.
    설명분산과 분류 정확도는 정말 따로 노는가?
  </div>
</section>

<!-- ===================== CH 06 ===================== -->
<section id="ch6">
  <h2 class="chap"><span class="num">CH 06</span>어긋남 — 설명분산과 정확도는 같이 가지 않는다<a href="#ch6" class="anchor-link">#</a></h2>

  <h3 class="step">학습 → 가설</h3>
  <p><code>explained_variance_ratio_</code>는 각 주성분이 전체 분산(정보)의 몇 %를 설명하는지다. 이걸 누적하면
  "주성분 n개로 정보 몇 %를 보존하는가"가 나온다. 그런데 PCA의 분산은 '클래스를 잘 가르는 방향'이 아니라
  '데이터가 가장 넓게 퍼진 방향'이다 — 둘은 다를 수 있다.</p>
  <div class="qbox">
    <span class="label">가설</span>
    누적 설명분산이 90~95%에 도달하는 주성분 수와, KNN 정확도가 최고가 되는 주성분 수는
    일치하지 않을 것이다. 정보 보존량(분산)과 분류 성능은 서로 다른 목표이기 때문이다.
  </div>

  <h3 class="step">테스트 — 누적 설명분산 곡선</h3>
  <div class="terminal">
    <div class="terminal-header">PCA.explained_variance_ratio_ 누적 — 분산 90/95/99% 도달 주성분 수 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_05@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_CUMVAR@@" alt="유방암·digits의 누적 설명분산 곡선과 90/95% 도달 지점">
    <figcaption>그림 0604-2 · 누적 설명분산 — 유방암은 7개로 90%, digits는 31개로 90%. 곡선이 가파를수록 적은 주성분에 정보가 몰린다</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">가설 통과 — 어긋남 확인</span>
    유방암은 주성분 1개에 분산 44.4%가 몰려 7개로 90%를 보존한다. 하지만 KNN 정확도 정점은 15개(설명분산 98.7%)였다 —
    정보 90%로는 부족했다. digits는 더 극명하다. 분산 95% 보존에 40개가 필요한데, 정확도 정점도 마침 40개 부근이지만
    그 40개의 설명분산(95%)이 전체(100%)보다 정확도가 높다. <strong>정보를 더 담는 것과 더 잘 맞히는 것은 다른 문제</strong>다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 그렇다면 정보의 21~63%밖에 안 담는 주성분 2개로 평면에 눌러 보면,
    클래스가 눈으로 갈라지긴 할까? 차원축소의 가장 직관적인 결과물인 2D 투영을 직접 그려 본다.
  </div>
</section>

<!-- ===================== CH 07 ===================== -->
<section id="ch7">
  <h2 class="chap"><span class="num">CH 07</span>2D 투영 — 평면에 눌러도 갈라지나<a href="#ch7" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 관찰</h3>
  <div class="qbox">
    <span class="label">의문</span>
    주성분 2개(PC1·PC2)만으로 30·64차원을 평면에 투영하면, 클래스가 시각적으로 분리될까?
    분리가 또렷하면 그 데이터는 적은 차원에 구조가 있다는 뜻이고, 뭉개지면 2D로는 부족하다는 뜻이다.
  </div>

  <h3 class="step">테스트 — PC1·PC2 평면 산점도</h3>
  <div class="terminal">
    <div class="terminal-header">PCA(n_components=2) — 유방암·digits PC1/PC2 설명분산 비율 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_06@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_SCATTER@@" alt="유방암 2클래스와 digits 10클래스의 PC1-PC2 2D 산점도">
    <figcaption>그림 0604-3 · 2D PCA 투영 — 유방암(왼쪽)은 두 클래스가 거의 갈라지고, digits(오른쪽)는 일부 숫자만 분리된다</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">관찰 결과</span>
    유방암은 PC1+PC2가 분산의 63.4%를 담고, 2D에서 악성·양성이 두 덩어리로 거의 갈라진다 —
    그래서 CH 04에서 주성분 2개만으로도 0.92가 나왔다. 반면 digits는 PC1+PC2가 21.7%뿐이라
    10개 숫자가 평면에서 상당히 겹친다 — 그래서 2개일 때 정확도가 0.52로 낮았다.
    2D 분리 정도가 곧 적은 차원에서의 분류 가능성을 예고한다.
  </div>

  <div class="bridge">
    <strong>되짚어 본 전제</strong> — 지금까지 PCA 앞에 항상 <code>StandardScaler</code>를 뒀다. 그런데 PCA는
    '분산이 큰 축'을 찾는다. 표준화를 빼면 단위 큰 특성이 분산을 독점해 주성분을 차지하지 않을까? 직접 확인한다.
  </div>
</section>

<!-- ===================== CH 08 ===================== -->
<section id="ch8">
  <h2 class="chap"><span class="num">CH 08</span>표준화 선행 — 없으면 주성분이 독점된다<a href="#ch8" class="anchor-link">#</a></h2>

  <h3 class="step">학습 → 가설</h3>
  <p>PCA는 분산이 큰 방향을 주성분으로 잡는다. 표준화를 안 하면 단위가 큰 'area' 특성의 원본 분산이
  가장 큰이라, PC1이 사실상 그 특성 하나를 가리키게 된다. 다른 특성의 정보는 뒤로 밀린다.</p>
  <div class="qbox">
    <span class="label">가설</span>
    유방암에서 <code>StandardScaler→PCA→KNN</code>과 <code>표준화 없이→PCA→KNN</code>을 같은 <code>n</code>으로 비교하면,
    표준화 쪽 정확도가 높고, 표준화 없는 쪽은 PC1이 분산을 거의 독점할 것이다.
  </div>

  <h3 class="step">테스트</h3>
  <div class="terminal">
    <div class="terminal-header">PCA(n) → KNN(k=5) on breast_cancer — 표준화 선행 유무 비교 · PC1 분산 독점 확인 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_07@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">가설 통과</span>
    표준화 없이 PCA를 하면 PC1 하나가 분산의 <strong>98.1%</strong>를 독점한다 — 단위 큰 'area'가 주성분을 삼킨 것이다.
    표준화 후엔 PC1이 44.4%로 내려가 다른 특성도 고르게 기여한다. 정확도도 주성분 15개에서 표준화가 +0.0526 앞선다.
    PCA에서 표준화는 KNN에서와 또 다른 이유로 '전제'다 — 거리 때문이 아니라 분산 독점을 막기 위해서.
  </div>

  <div class="callout">
    <span class="label">함정</span>
    표준화든 PCA든 <strong>train으로만 <code>fit</code></strong>하고 test엔 <code>transform</code>만 해야 한다.
    test의 평균·분산·주성분을 미리 반영하면 시험 문제를 미리 본 셈(data leakage)이 된다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 표준화·PCA로 거리를 또렷하게 만들었다. 그렇다면 실제로
    주성분 수를 정할 때는 무엇을 기준으로 삼아야 하나? '최고 정확도 한 점'만 보는 게 맞는지,
    아니면 '적은 차원으로 충분한 정확도'라는 가성비 기준이 따로 있는지 확인한다.
  </div>
</section>

<!-- ===================== CH 09 ===================== -->
<section id="ch9">
  <h2 class="chap"><span class="num">CH 09</span>가성비 — 최고 정확도가 아니라 충분한 정확도를 적은 차원으로<a href="#ch9" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 기준</h3>
  <p>CH 04~05는 정확도가 가장 높은 주성분 수(sweet spot)를 찾았다. 그런데 실무에서 차원 수를 정하는
  기준은 한 가지가 아니다. 정보를 얼마나 보존하느냐(누적 설명분산), 정확도가 전체와 얼마나 가까우냐,
  그리고 차원 하나당 정확도가 얼마냐(가성비)가 서로 다른 답을 가리킨다.</p>
  <div class="qbox">
    <span class="label">의문 → 기준</span>
    digits 64특성에서 세 기준을 같이 잰다 — ① 누적 설명분산 85·95% 도달 차원,
    ② 전체 특성 정확도의 −1%p 이내로 들어오는 <strong>가장 적은</strong> 차원, ③ 차원당 정확도(acc/n)가 최대인 차원.
    이 셋이 한 점으로 모이지 않는다면, '가성비 좋은 n'은 단일 정답이 아니라 목적에 따른 선택이라는 뜻이다.
  </div>

  <pre><code class="language-python"># path : .study/test/practice06_pca/practice06_runner.py §09 (발췌)
# ① 누적 설명분산이 85/95%에 도달하는 차원
pca_full = PCA(random_state=42).fit(Xtr_s)
cum = np.cumsum(pca_full.explained_variance_ratio_)
n85 = int(np.searchsorted(cum, 0.85) + 1)
n95 = int(np.searchsorted(cum, 0.95) + 1)

# ② 전체 정확도의 -1%p 이내로 들어오는 '최소' 차원
enough = next((n for n, a, e in rows if a >= full - 0.01), None)

# ③ 차원당 정확도(가성비) 최댓값
best_eff = max(rows, key=lambda r: r[1] / r[0])
print(n85, n95, enough, best_eff)</code></pre>

  <h3 class="step">테스트 — 세 기준을 한 표에서 본다</h3>
  <div class="terminal">
    <div class="terminal-header">PCA(n) → KNN(k=5) on digits — 설명분산·전체대비·차원당 정확도 3기준 비교 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_09@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">관찰 결과 — 기준마다 답이 다르다</span>
    digits 전체 64특성 정확도는 0.9639다. ① 정보 85% 보존은 25개, 95%는 40개 주성분이 필요하다.
    ② 전체의 −1%p(0.9539) 이내로 들어오는 가장 적은 차원은 15개(0.9556)다. ③ 차원당 정확도(acc/n)는
    n=2에서 0.261로 가장 크지만, 그때 정확도는 0.5222로 쓰기 어렵다. 차원당 정확도 하나만 보면
    극단으로 낮은 차원을 가리키므로, 정보 보존·충분한 정확도 기준과 함께 봐야 한다.
    digits에서 '가성비'로 고를 만한 자리는 정보 85%·정확도 −1%p를 함께 만족하는 15~25개 구간이다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 15·8차원처럼 적은 주성분이 '충분하다'고 했는데, 그렇게 줄인 데이터는
    원래 이미지로 얼마나 되돌아올까? 8차원으로 압축한 digits를 복원해 원본과의 픽셀 오차와 이미지를 직접 본다.
  </div>
</section>

<!-- ===================== CH 10 ===================== -->
<section id="ch10">
  <h2 class="chap"><span class="num">CH 10</span>복원 — 8차원으로 줄인 digits를 되돌리면<a href="#ch10" class="anchor-link">#</a></h2>

  <h3 class="step">학습 → 의문</h3>
  <p>PCA는 <code>transform</code>으로 줄인 데이터를 <code>inverse_transform</code>으로 원래 차원(64픽셀)에 되돌릴 수 있다.
  주성분이 적을수록 되돌린 이미지에서 정보가 더 많이 빠진다. 줄인 차원이 '충분한지'를 정확도가 아니라
  복원 품질로도 볼 수 있다.</p>
  <div class="qbox">
    <span class="label">의문 → 관찰</span>
    digits를 PCA 32·8·4·2차원으로 줄였다가 <code>inverse_transform</code>으로 복원해 원본과의 픽셀 MSE를 잰다.
    주성분이 적을수록 MSE가 커질 것이고, 8차원 복원 이미지가 숫자를 알아볼 만큼 선명한지 직접 본다.
    test에는 <code>transform</code>만 적용해 학습 주성분으로만 복원한다(누설 방지).
  </div>

  <blockquote class="cite">
    "inverse_transform(X) — Transform data back to its original space. … Return an input X_original whose
    transform would be X."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html" target="_blank" rel="noopener">PCA.inverse_transform</a></span>
  </blockquote>

  <h3 class="step">테스트 — 차원별 복원 MSE</h3>
  <div class="terminal">
    <div class="terminal-header">PCA(n) → inverse_transform on digits — 차원별 복원 픽셀 MSE · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_10@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_RECON@@" alt="digits 원본과 PCA 8차원·2차원 복원 이미지 3행 비교">
    <figcaption>그림 0604-4 · 복원 비교 — 위 원본(64픽셀), 가운데 PCA 8차원 복원, 아래 PCA 2차원 복원(테스트셋 앞 8개)</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">관찰 결과</span>
    복원 픽셀 MSE는 32차원 2.08, 8차원 7.74, 4차원 10.36, 2차원 14.23으로 주성분이 적을수록 커진다.
    8차원은 설명분산이 0.5316, 즉 정보의 절반 안팎만 남았는데도 복원 이미지에서 숫자의 큰 획은 살아 있어
    대부분 알아볼 수 있다. 반면 2차원(설명분산 0.2170)은 윤곽이 뭉개져 숫자 구분이 어렵다.
    CH 04에서 8차원 KNN 정확도가 0.9222, 2차원이 0.5222였던 것과 같은 방향이다 —
    복원이 선명한 차원일수록 분류도 잘 된다.
  </div>

  <div class="bridge">
    <strong>마지막 질문</strong> — 8차원은 복원도 분류도 쓸 만했지만 2차원은 정보가 너무 빠졌다.
    그렇다면 차원은 무조건 줄일수록 좋은가? 이득이 손해로 바뀌는 지점을 끝까지 밀어 본다.
  </div>
</section>

<!-- ===================== CH 11 ===================== -->
<section id="ch11">
  <h2 class="chap"><span class="num">CH 11</span>정리 — 손해로 바뀌는 지점, 그리고 의문 회수<a href="#ch11" class="anchor-link">#</a></h2>

  <h3 class="step">테스트 — 차원을 극단까지 줄여 본다</h3>
  <p>digits 64특성을 전체·sweet spot·과소(2~3개)까지 줄여 가며 같은 KNN으로 정확도를 비교한다.
  어디서 차원축소의 이득이 정보 손실로 뒤집히는지 본다.</p>
  <div class="terminal">
    <div class="terminal-header">PCA(n) → KNN(k=5) on digits — 전체·sweet·과소(2~3) 정확도 비교 · 정보 손실 지점 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_08@@</pre>
  </div>

  <h3 class="step">관찰 — 이득이 손해로 바뀌는 지점</h3>
  <div class="keypoint">
    <span class="label">관찰 결과</span>
    digits에서 주성분 40개(sweet)는 전체보다 +0.0083, 20개는 −0.0111, 10개는 −0.0194로 완만히 떨어진다.
    그런데 5개에서 −0.1333, 3개 −0.2444, 2개에서는 <strong>−0.4417</strong>로 하락한다. 설명분산이 21.7%까지 줄면
    클래스를 가를 정보 자체가 사라진 것이다. 차원축소는 '잡음 제거'와 '정보 손실'이 교차하는 구간이 있고,
    그 교차점을 넘어 줄이면 손해다.
  </div>

  <h3 class="step">최종 결론 — 출발 의문 회수</h3>
  <div class="keypoint">
    <span class="label">FINAL CONCLUSION</span>
    CH 01의 질문 "<strong>고차원에서 거리 기반 KNN은 왜 흔들리고, 어떻게 되살리나</strong>"의 답:
    KNN은 단위가 제각각이면 큰 특성에 끌려가고(CH 02), 차원이 많으면 '가깝다'가 흐려진다(CH 03).
    PCA로 분산 큰 축만 남기면(CH 04) 잡음이 걷혀 적은 차원으로 전체보다 잘 맞히는 sweet spot이 생긴다(CH 05).
    단, 정보 보존(설명분산)과 분류 정확도는 별개이고(CH 06), 2D 분리 정도가 적은 차원의 가능성을 예고하며(CH 07),
    PCA 앞 표준화는 분산 독점을 막는 전제다(CH 08). 주성분 수는 최고 정확도 한 점이 아니라
    정보 보존·전체 대비 정확도·가성비를 함께 봐야 하고(CH 09), 줄인 차원의 복원 품질이 분류 가능성과 같이 간다(CH 10).
    그리고 차원은 무조건 줄일수록 좋은 게 아니라 정보 손실로 뒤집히는 지점이 있다(CH 11).
  </div>

  <h3 class="step">한 문장으로</h3>
  <div class="keypoint">
    <span class="label">ONE-LINER</span>
    "차원을 줄인다"의 실체는 — <strong>분산이 큰 '진짜 정보' 축만 남겨, 거리 기반 모델이 잡음에 흔들리지 않게
    하되, 정보 손실로 뒤집히기 직전까지만 줄이는 일</strong>이다. 그래서 PCA+KNN의 핵심은
    '몇 개를 남길까'를 정보량이 아니라 검증 정확도로 정하는 데 있다.
  </div>

  <div class="ref-chain">
    <p class="ref-title">📚 전체 근거 출처</p>
    <ol>
      <li><strong>공식 문서</strong>
        <a href="https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html" target="_blank" rel="noopener">scikit-learn · KNeighborsClassifier</a>(이웃 다수결),
        <a href="https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html" target="_blank" rel="noopener">PCA</a>(SVD 차원축소·explained_variance_ratio_),
        <a href="https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html" target="_blank" rel="noopener">StandardScaler</a>,
        <a href="https://scikit-learn.org/stable/modules/neighbors.html" target="_blank" rel="noopener">Nearest Neighbors</a>(고차원 한계).</li>
      <li><strong>workspace</strong>
        <code>../ml_workspace/from_colab/0604-s/dimensionality_reduction_practice_completed_모범답안.ipynb</code>
        (digits + PCA/LDA/t-SNE 과제),
        <code>pytorch_knn_breast_cancer.ipynb</code>(KNN·표준화 흐름).</li>
      <li><strong>강의자료</strong>
        <code>.study/pdf/머신러닝_차원축소_앙상블.pdf</code> (배경지식).</li>
      <li><strong>실행 검증</strong>
        <code>.study/test/practice06_pca/practice06_runner.py §00~§10</code>
        → <code>logs/*.txt</code>, <code>charts/*.png</code> (고정 시드 42, 재현 가능).</li>
    </ol>
  </div>
</section>
</main>

<footer>
  <p>SK 네트웍스 AI Family 32기 · 교과목 2 단원 2 머신러닝 실습6(과제) 차원 축소 (2026-06-04)</p>
  <p>모든 터미널 출력은 <code>.study/test/practice06_pca/practice06_runner.py</code> 실제 실행 결과이며,
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
print(f"zero-width space: {HTML.count(chr(0x200b))}")
