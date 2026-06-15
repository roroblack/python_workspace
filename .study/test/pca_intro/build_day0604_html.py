# build_day0604_html.py
# day0604_dimensionality_reduction.html 조립 — logs/*.txt(실제 실행 결과) + charts/*.png(base64) 주입
# 실행: c:\_proj\python_workspace\.venv\Scripts\python.exe build_day0604_html.py
#   (= GUIDE §11 run_all 역할: 터미널 값 직접 작성 금지, 로그에서 주입)
#   문체: day0527_ml_intro / day0602_ensemble 의 "의문→해결→새 의문" 서사 추적 방식.
#   NOTE: Day6 PDF(머신러닝_차원축소_…)는 로컬에 없음 → sklearn PCA 공식문서로 근거 대체(§27-2).
import base64, html, pathlib, re

HERE = pathlib.Path(__file__).parent
LOGS = HERE / "logs"
CHARTS = HERE / "charts"
OUT = HERE.parent.parent / "blog" / "day0604_dimensionality_reduction.html"   # .study/blog/
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
    "@@TERM_00@@": term("00_curse"),
    "@@TERM_0A@@": term("0a_cov_by_hand"),
    "@@TERM_01@@": term("01_axes"),
    "@@TERM_02@@": term("02_explained"),
    "@@TERM_03@@": term("03_pca_2d"),
    "@@TERM_04@@": term("04_reconstruct"),
    "@@TERM_05@@": term("05_tsne"),
    "@@TERM_06@@": term("06_other"),
    "@@CHART_0A@@": chart("ch0a_cov_by_hand.png"),
    "@@CHART_01@@": chart("ch01_pca_axes.png"),
    "@@CHART_02@@": chart("ch02_cumvar.png"),
    "@@CHART_03@@": chart("ch03_pca_scatter.png"),
    "@@CHART_04@@": chart("ch04_reconstruct.png"),
    "@@CHART_05@@": chart("ch05_tsne.png"),
}

HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>파이썬 머신러닝 분석: 특성 64개를 2개로 줄이면 — PCA가 남기는 것</title>
  <meta name="description" content="SK 네트웍스 AI Family 32기 머신러닝 Day6. '특성이 수십·수백 개면 무엇이 문제인가(차원의 저주)', '정보를 최대한 지키며 차원을 줄이려면(PCA)', '몇 개의 주성분으로 충분한가', '비선형 군집은 PCA로 펴지나'라는 의문을 따라 차원의 저주·PCA 분산 축·누적 설명분산(90%→31개)·2D 시각화·재구성 정보손실·t-SNE 비교를 sklearn 실행으로 검증한 기록.">
  <meta property="og:title" content="파이썬 머신러닝 분석: 특성 64개를 2개로 줄이면 — PCA가 남기는 것">
  <meta property="og:description" content="차원의 저주 → PCA(분산 큰 축) → 누적 설명분산 90%→31개 → 2D 시각화 → 재구성 정보손실 → t-SNE 비교, 실측으로 추적">
  <meta property="og:type" content="article">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="파이썬 머신러닝 분석: 특성 64개를 2개로 줄이면 — PCA가 남기는 것">
  <meta name="twitter:description" content="차원의 저주 → PCA 분산 축 → 누적 설명분산 → 2D 시각화 → 재구성 손실 → t-SNE">
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
  <p class="eyebrow">Python · 머신러닝(교과목 2 · 단원 2) Day6 · 부트캠프</p>
  <h1>특성 64개를 2개로 줄이면 — PCA가 남기는 것</h1>
  <p class="deck">손글씨 숫자 한 장은 8×8, 곧 <strong>64개의 특성</strong>이다. 특성이 이렇게 많으면 무엇이 달라지는가 —
  거리가 희박해지고(차원의 저주), 그래프로 그릴 수도 없다. 그렇다면 <strong>정보를 최대한 지키면서 축을 줄일 수 있을까?</strong>
  이 글은 그 한 질문에서 출발해 — PCA가 분산이 가장 큰 축을 어떻게 찾는지, 64차원을 몇 개의 주성분으로 압축해야 하는지,
  단 2개 축에 투영했을 때 숫자 군집이 보이는지, 차원을 버린 만큼 정보가 어떻게 사라지는지, 그리고 PCA로 부족한 비선형 구조를
  t-SNE가 어떻게 메우는지를 직접 돌려 추적한 기록이다. 모든 수치는 sklearn 으로 직접 돌린 결과이며 <code>random_state=42</code> 로 재현 가능하다.</p>
  <div class="meta-row">
    <span><strong>날짜</strong>2026-06-04</span>
    <span><strong>Python</strong>@@PY@@ · scikit-learn 1.8.0 · NumPy 2.4.4 · Pandas 3.0.2</span>
    <span><strong>OS</strong>Windows 11 Pro 25H2</span>
    <span><strong>IDE</strong>VS Code 1.117.0</span>
    <span><strong>HW</strong>Asrock x600 · Ryzen 8600G · 24GB LPDDR5 · RTX 4070 Super 12GB</span>
    <span><strong>커리큘럼</strong>교과목 2 · 단원 2 · 머신러닝 Day6 — 차원 축소·시각화</span>
  </div>
</header>

<main>
<nav class="flow">
  <h2>이 글의 흐름 — '특성이 너무 많다'는 불편에서 갈라져 나온 질문들</h2>
  <ol>
    <li><a href="#ch1">시작 — 특성이 수십·수백 개면 무엇이 문제인가 (차원의 저주)</a></li>
    <li><a href="#ch2">공분산 행렬을 손으로 — 왜 XᵀX 가 (d×d) 변수 '지도'가 되나</a></li>
    <li><a href="#ch3">PCA란 무엇인가 — 정보를 지키며 줄이려면, 분산이 가장 큰 축으로</a></li>
    <li><a href="#ch4">몇 개로? — 차원 수는 뭘 기준으로 정하나 (누적 설명분산)</a></li>
    <li><a href="#ch5">2D로 줄여 본다 — 단 2개 축에 숫자 군집이 드러날까</a></li>
    <li><a href="#ch6"><span class="turn">대가</span> — 차원을 줄이면 무조건 성능이 좋아지나 (재구성·정보 손실)</a></li>
    <li><a href="#ch7"><span class="turn">한계</span> — 직선 투영으로 못 펴는 군집, t-SNE 맛보기</a></li>
    <li><a href="#ch8">비교 — PCA vs LDA vs t-SNE, 무엇이 다른가</a></li>
    <li><a href="#ch9">일반화 — iris·breast_cancer 에서도 같은 원리가 통하나</a></li>
    <li><a href="#ch10">정리 — '차원을 줄인다'가 정한 것 한 문장</a></li>
  </ol>
</nav>

<!-- ===================== CH 01 ===================== -->
<section id="ch1">
  <h2 class="chap"><span class="num">CH 01</span>시작 — 특성이 많으면 무엇이 문제인가<a href="#ch1" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>차원 축소 실습의 입력은 늘 표 한 장이었다 — 행은 샘플, 열은 특성. 그런데 열이 11개(와인), 64개(손글씨), 수백 개까지
  늘어나면 "특성이 많을수록 정보가 많아 좋은 것 아닌가?"라는 직관이 먼저 든다. 강의에서 반복된 경고는 그 반대였다 —
  <strong>차원의 저주(curse of dimensionality)</strong>. 특성이 늘수록 데이터는 빈 공간에 흩어지고, 거리 기반 판단이 낮아진다.</p>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    "차원이 늘면 거리가 희박해진다"가 사실이라면, 무작위 점들을 <code>d</code>차원에 뿌렸을 때
    <strong>가장 가까운 이웃</strong>과 <strong>가장 먼 점</strong>의 거리 대비가 <code>d</code>가 커질수록 0에 수렴해야 한다.
    즉 "누가 가깝고 누가 먼지"의 구분이 사라져야 한다. <code>d</code>를 2 → 500으로 올리며 직접 재 본다.
  </div>

  <h3 class="step">테스트 — 차원을 올리며 최근접/최원접 거리를 잰다</h3>
  <pre><code class="language-python"># path : .study/test/pca_intro/pca_intro_runner.py §00 (발췌)
from sklearn.metrics import pairwise_distances
import numpy as np

rng = np.random.RandomState(42)
for d in [2, 10, 50, 100, 500]:
    X = rng.rand(200, d)              # [0,1]^d 균등 분포 200점
    D = pairwise_distances(X); np.fill_diagonal(D, np.inf)
    nearest = D.min(axis=1).mean()    # 평균 최근접 이웃 거리
    print(d, nearest)                 # 차원이 커질수록 대비가 줄어든다</code></pre>
  <div class="terminal">
    <div class="terminal-header">pca_intro_runner.py §00 · pairwise_distances(rand d차원) — 차원↑ 거리 희박화 확인 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_00@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT</span>
    2차원에서 (최원−최근)/최근 대비가 28.4였는데, 500차원에선 0.14로 쪼그라들었다. 차원이 커질수록
    모든 점이 비슷하게 멀어져 <strong>'가까운 이웃'이라는 개념이 무의미</strong>해진다. 게다가 사람은 3차원 너머를 못 본다 —
    그러니 특성이 많을 때는 <strong>정보를 최대한 지키면서 차원을 줄이는 도구</strong>가 필요하다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 그런데 "정보를 지키며 줄인다"는 말이 모순처럼 들린다. 축을 버리면 정보도 버려질 텐데,
    어떤 축을 버려야 손해가 가장 작을까? 줄이는 기준이 있어야 한다. 그 기준을 만드는 첫 단계가 변수들끼리의 관계를 한 장의 표로 요약한
    <strong>공분산 행렬</strong>인데, 식이 <code>C = Xᵀ_c X_c / (n−1)</code> 라는 낯선 모양이다. 이것부터 손으로 뜯어 본다.
  </div>
</section>

<!-- ===================== CH 02 (공분산 손 계산) ===================== -->
<section id="ch2">
  <h2 class="chap"><span class="num">CH 02</span>공분산 행렬을 손으로 — XᵀX 가 왜 (d×d) 지도가 되나<a href="#ch2" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>PCA의 출발점은 <strong>공분산 행렬</strong>이다. 표준화한 데이터의 공분산 행렬을 고유값 분해하면 그 고유벡터가 곧 주성분 축이 된다.
  그런데 공식 <code>C = (1/(n−1)) · Xᵀ_c X_c</code> 를 처음 보면 막힌다. <code>X_c</code>는 변수별 평균을 빼서 중심화한 데이터인데,
  여기서 세 가지가 걸린다 — ① 변수끼리의 곱을 더한 것일 뿐인데 왜 그게 <strong>(d×d) 행렬</strong>이 되나, ② 그 행렬이 어떻게 변수 사이의
  '지도'라는 건가, ③ 왜 하필 <code>Xᵀ_c</code> 를 앞에 두고 곱하나.</p>

  <p>shape 부터 따져 보면 실마리가 잡힌다. 데이터 <code>X_c</code> 는 <code>(n×d)</code>(행=샘플 n, 열=변수 d)다.
  <code>Xᵀ_c</code> 는 <code>(d×n)</code>. 둘을 <code>(d×n)·(n×d)</code> 로 곱하면 가운데의 <code>n</code> 이 사라지고 결과는 <code>(d×d)</code> 가 된다.
  즉 <strong>샘플이 100만 개여도 변수가 2개면 공분산 행렬은 언제나 2×2</strong>다. 결과 행렬의 <code>(i,j)</code> 칸은 "변수 i의 편차 × 변수 j의 편차"를
  모든 샘플에 대해 더한 값 — 두 변수가 같이 움직이는 정도다. 그래서 대각선은 각 변수의 분산, 비대각선은 두 변수의 관계가 되어
  행렬 전체가 변수 사이의 관계를 담은 한 장의 지도가 된다.</p>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    45도로 나란히 커지는 점 3개 <code>[2,3], [4,5], [6,7]</code> 로 직접 해 보자. 평균을 빼 중심화하면 <code>[−2,−2], [0,0], [2,2]</code> 가 되고,
    <code>Xᵀ_c X_c / (n−1)</code> 를 손으로 칸칸이 채우면 <strong>[[4,4],[4,4]]</strong> 가 나와야 한다. 그리고 그 행렬을 <code>np.cov</code> 와
    NumPy 행렬곱이 모두 같은 값으로 재현해야 한다. 또 이 행렬을 고유값 분해하면 한 축(<code>λ=8</code>)에 분산이 다 몰리고 그 방향은 45도여야 한다.
  </div>

  <h3 class="step">테스트 — 칸칸이 손 계산하고 np.cov 와 맞춘다</h3>
  <pre><code class="language-python"># path : .study/test/pca_intro/pca_intro_runner.py §0A (발췌)
import numpy as np
X = np.array([[2.,3.], [4.,5.], [6.,7.]])     # (n=3 행=샘플, d=2 열=변수)
n, d = X.shape
mu = X.mean(axis=0)                            # 변수별 평균 [4, 5]
Xc = X - mu                                    # 중심화 [[-2,-2],[0,0],[2,2]]

# 손 계산: 각 칸 = 변수 i,j 편차곱의 합 / (n-1)  → (d×d) 모양이 나온다
C_hand = np.zeros((d, d))
for i in range(d):
    for j in range(d):
        C_hand[i, j] = np.sum(Xc[:, i] * Xc[:, j]) / (n - 1)

print(Xc.T.shape, Xc.shape)                    # (d,n)@(n,d) → n이 사라지고 (d,d)
print(C_hand)                                  # 손 계산
print(np.cov(X, rowvar=False))                 # NumPy 와 대조
eigval, eigvec = np.linalg.eigh(C_hand)        # 고유값 분해 → 주성분 축</code></pre>
  <div class="terminal">
    <div class="terminal-header">pca_intro_runner.py §0A · Xc.T@Xc/(n-1) 손 계산 vs np.cov — (d×d) 구조·45도 PC1 확인 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_0A@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_0A@@" alt="3개 점으로 손 계산한 공분산 행렬과 45도 PC1 고유벡터">
    <figcaption>그림 0604-1 · 왼쪽 원본 3점과 평균(×), 오른쪽 중심화 점 위의 PC1 고유벡터 — 공분산 [[4,4],[4,4]], λ=[8,0], PC1=45도</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">가설 통과</span>
    손으로 채운 네 칸이 모두 <code>8.0/2 = 4.0</code> 이라 <strong>[[4,4],[4,4]]</strong> 가 나왔고, NumPy 행렬곱·<code>np.cov</code> 와 완전히 일치했다.
    <code>(d×n)·(n×d)</code> 곱에서 <code>n</code> 이 사라져 변수 개수만큼의 <code>(d×d)</code> 칸만 남는다는 것이 핵심이다. 비대각선 값 4가 대각선(분산)과 같다는 건
    두 변수가 거의 완전히 같이 움직인다는 뜻이고, 고유값 분해 결과 한 축(<code>λ=8</code>)이 분산을 전부 담으며 그 방향이 <code>[0.707, 0.707]</code>, 곧 45도였다.
    공분산 행렬이 변수 사이의 '지도'라는 말이 이 한 예제로 손에 잡힌다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 2변수 예제에선 고유벡터를 손으로 뽑았지만, 변수가 수십·수백 개면 손 계산은 불가능하다.
    sklearn 의 <code>PCA</code> 가 바로 이 공분산 구조(정확히는 SVD)로 "분산이 가장 큰 축"을 찾아 준다. 길게 뻗은 구름에 걸어 확인한다.
  </div>
</section>

<!-- ===================== CH 03 ===================== -->
<section id="ch3">
  <h2 class="chap"><span class="num">CH 03</span>PCA란 무엇인가 — 분산이 가장 큰 축으로<a href="#ch3" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>앞 챕터에서 손으로 만든 공분산 행렬을 고유값 분해하면 주성분이 나왔다. <strong>PCA(주성분 분석)</strong>는 그 과정을 자동화한,
  정답 <code>y</code>를 쓰지 않는 비지도 차원 축소다. 핵심 아이디어는 한 문장이다 —
  데이터가 가장 넓게 퍼진 방향(분산이 큰 방향)일수록 정보를 많이 담고 있으니, 그 방향을 새 축(주성분)으로 삼는다.
  PC1은 분산이 가장 큰 방향, PC2는 그에 직교하면서 그다음으로 분산이 큰 방향이다.</p>

  <blockquote class="cite">
    "Linear dimensionality reduction using Singular Value Decomposition of the data
    to project it to a lower dimensional space. … The components are sorted by explained_variance_."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html" target="_blank" rel="noopener">sklearn.decomposition.PCA</a></span>
  </blockquote>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    한 방향으로 길게 뻗은 2D 구름에 PCA를 걸면, <strong>PC1은 그 긴 방향과 거의 나란</strong>하고
    PC1 하나의 설명분산비가 가장 크게 클 것이다. 즉 2개 축 중 1개만 남겨도 정보 대부분이 살아남는다.
  </div>

  <h3 class="step">테스트 — 길게 뻗은 구름에 주성분을 그어 본다</h3>
  <div class="terminal">
    <div class="terminal-header">pca_intro_runner.py §01 · PCA(2D 구름) — PC1 방향·설명분산비 확인 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_01@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_01@@" alt="2D 데이터 구름 위에 그린 PC1·PC2 주성분 화살표">
    <figcaption>그림 0604-2 · 길게 뻗은 구름의 PC1(주황)은 가장 넓게 퍼진 방향, PC2(초록)는 직교 방향 — PC1 설명분산비 0.9952</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">가설 통과</span>
    PC1 방향 <code>[0.94, 0.34]</code>가 구름이 뻗은 방향과 나란했고, PC1 한 축의 설명분산비가 <strong>0.9952</strong>였다.
    2개 축 중 PC1 하나만 남기면 분산의 99.5%가 보존된다 — "정보를 지키며 줄인다"의 실체는
    <strong>분산이 작은(=정보가 적은) 축부터 버리는 것</strong>이었다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 2차원이야 1개만 남기면 되지만, 64차원 손글씨 숫자는 어떨까?
    64개 주성분 중 분산을 90% 지키려면 몇 개를 남겨야 할까? 버려도 되는 축이 정말 많을까?
  </div>
</section>

<!-- ===================== CH 04 ===================== -->
<section id="ch4">
  <h2 class="chap"><span class="num">CH 04</span>몇 개로? — 차원 수는 뭘 기준으로 정하나<a href="#ch4" class="anchor-link">#</a></h2>

  <h3 class="step">학습 → 가설</h3>
  <p>주성분을 찾는 법은 알았는데, 그렇다면 <strong>몇 개를 남길지(차원 수)는 무엇을 기준으로 정하나?</strong> 정답 라벨도 없는데
  64개 중 31개인지 40개인지를 어떻게 고르나 — 이게 차원 축소에서 가장 먼저 막히는 실무 의문이다. 기준은 <strong>누적 설명분산 비율</strong>이다.
  주성분은 설명분산이 큰 순서로 정렬돼 나오므로, <code>explained_variance_ratio_</code>를 앞에서부터
  누적(<code>np.cumsum</code>)하면 "주성분 k개로 전체 분산의 몇 %를 지키는지" 곡선이 그려진다. 보통 80~95% 를 지키는 선에서 가성비로 끊는다.</p>
  <div class="qbox">
    <span class="label">가설</span>
    64차원 digits 에서 픽셀 특성은 서로 상관이 크다(이웃 픽셀은 같이 밝다). 그렇다면 분산은 앞쪽 주성분에 몰려 있을 것이고,
    <strong>90% 분산을 지키는 데 64개보다 훨씬 적은 주성분</strong>이면 충분할 것이다.
  </div>

  <pre><code class="language-python"># path : .study/test/pca_intro/pca_intro_runner.py §02 (발췌)
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np

X = StandardScaler().fit_transform(load_digits().data)   # 64차원 표준화
pca = PCA(random_state=42).fit(X)
cum = np.cumsum(pca.explained_variance_ratio_)           # 누적 설명분산
for thr in [0.90, 0.95]:
    k = int(np.searchsorted(cum, thr) + 1)
    print(thr, k)                                        # 90%/95%에 필요한 주성분 수</code></pre>
  <div class="terminal">
    <div class="terminal-header">pca_intro_runner.py §02 · PCA.explained_variance_ratio_ 누적 — 90/95% 임계 주성분 수 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_02@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_02@@" alt="digits 64차원 누적 설명분산 곡선과 90%·95% 임계선">
    <figcaption>그림 0604-3 · 누적 설명분산 곡선 — 90% 보존에 31개, 95% 보존에 40개 주성분 (64개 중)</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">가설 통과</span>
    PC1 하나가 분산의 12.0%, 누적으로 <strong>90%는 31개 · 95%는 40개</strong> 주성분이면 닿았다. 64개를 31개로 줄여도
    분산의 9할을 지킨다 — 특성의 절반을 버려도 정보의 대부분이 남는다는 뜻이다. 다만 2개 축(2D)만 쓰면 누적분산은
    겨우 21.6%다. 그래도 시각화에는 2D가 필요하다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 분산의 21.6%밖에 못 담는 2개 축으로 그림을 그리면 무엇이 보일까?
    정보의 4/5를 버린 그 평면에서 숫자 0~9 군집이 정말 눈에 드러날까?
  </div>
</section>

<!-- ===================== CH 05 ===================== -->
<section id="ch5">
  <h2 class="chap"><span class="num">CH 05</span>2D로 줄여 본다 — 군집이 드러날까<a href="#ch5" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    64차원을 2개 주성분으로 투영하면 누적분산은 21.6%뿐이라 군집이 완벽히 갈리진 않겠지만,
    <strong>같은 숫자끼리는 가까이, 다른 숫자끼리는 멀리</strong> 모이는 큰 덩어리 구조 정도는 드러날 것이다.
  </div>

  <h3 class="step">테스트 — 2개 주성분에 투영해 색으로 본다</h3>
  <div class="terminal">
    <div class="terminal-header">pca_intro_runner.py §03 · PCA(n_components=2).fit_transform — 2D 군집 윤곽 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_03@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_03@@" alt="digits PCA 2D 산점도, 색으로 구분한 숫자 라벨 0~9">
    <figcaption>그림 0604-4 · PCA 2D 산점도(색=숫자 라벨) — 0·6 같은 일부 숫자는 또렷이 갈리지만, 가운데에서 여러 숫자가 겹친다</figcaption>
  </figure>

  <h3 class="step">관찰 → 정리</h3>
  <div class="keypoint">
    <span class="label">PARTIAL OK</span>
    2개 축이 담은 분산은 21.6%뿐인데도 0, 6 같은 숫자는 모서리에 또렷한 덩어리를 이뤘다. 군집 윤곽은 가설대로 드러났다.
    하지만 가운데에서는 여러 숫자가 뒤엉켜 깔끔히 갈리지 않는다 — <strong>큰 구조는 보이되, 세밀한 경계는 흐릿하다.</strong>
    이게 정보 4/5를 버린 2D 그림의 한계다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — "정보를 버렸다"는 말을 눈으로 본 셈인데, 그 손실을 숫자로 정확히 잴 수는 없을까?
    2개·8개·32개 주성분으로 줄였다가 <em>다시 원래 64차원으로 복원</em>하면, 버린 만큼 그림이 흐려질 것이다.
  </div>
</section>

<!-- ===================== CH 06 ===================== -->
<section id="ch6">
  <h2 class="chap"><span class="num">CH 06</span>대가 — 줄이면 무조건 성능이 좋아지나<a href="#ch6" class="anchor-link">#</a></h2>

  <h3 class="step">학습 → 가설</h3>
  <p>여기서 한 번 짚고 넘어갈 의문이 있다 — <strong>차원을 줄이면 무조건 성능이 좋아지나?</strong> 노이즈가 줄고 과적합이 완화되니
  좋아질 것 같지만, 답은 "아니오"다. 차원을 줄이는 과정에는 <strong>필연적으로 정보 손실</strong>이 따르기 때문에, 무작정 줄이면 오히려
  필요한 정보까지 버려 성능이 낮아진다. 그래서 보통 설명 가능한 분산을 80~95% 유지하는 선에서 멈춘다. 이 손실의 실체를 눈으로 재 본다.</p>
  <p>PCA는 한쪽으로만 가는 길이 아니다. k개 축에 투영(<code>transform</code>)했다가
  <code>inverse_transform</code>으로 다시 원래 공간으로 되돌릴 수 있다. 되돌린 데이터와 원본의 차이(재구성 오차)가
  곧 "버린 축에 들어 있던 정보"의 양이다.</p>
  <div class="qbox">
    <span class="label">가설</span>
    숫자 이미지를 k개 주성분으로 압축했다 복원하면, <strong>k가 작을수록 재구성 MSE가 커지고</strong> 숫자가 더 뭉개질 것이다.
    그리고 그 MSE 감소 곡선은 CH 04의 누적 설명분산 곡선과 같은 방향으로 움직일 것이다. 정보 손실이 0이 아니라는 것이
    "무조건 좋아지지는 않는다"의 근거가 된다.
  </div>

  <h3 class="step">테스트 — k별로 복원해 MSE와 그림을 본다</h3>
  <div class="terminal">
    <div class="terminal-header">pca_intro_runner.py §04 · PCA.inverse_transform(k) — 재구성 MSE·정보 손실 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_04@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_04@@" alt="주성분 k개로 복원한 손글씨 숫자 비교 — k가 클수록 선명">
    <figcaption>그림 0604-5 · 같은 숫자를 k=2·8·16·32·64로 복원 — k가 커질수록 원본에 가까워진다(k=64에서 MSE 0)</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">가설 통과</span>
    k=2에서 재구성 MSE 13.42(누적분산 28.5%)였다가, k=32에서 0.63(96.6%), k=64에서 0.0(100%)으로 떨어졌다.
    버린 주성분만큼 정보가 사라지고 그만큼 숫자가 뭉개진다 — <strong>차원 축소는 공짜가 아니라 정보와 차원을 맞바꾸는 거래</strong>다.
    그래서 "줄이면 무조건 성능이 좋아지나"의 답은 아니오다. 너무 적은 k는 필요한 정보까지 버린다.
    어디서 멈출지는 CH 04의 누적분산 곡선이 정해 준다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 그런데 PCA는 분산이 큰 <em>직선</em> 방향만 본다. 군집이 곡선으로 휘감겨 있으면
    직선 투영으로는 펴지지 않을 텐데, CH 05에서 가운데가 엉킨 것도 그 탓 아닐까? 비선형 구조를 펴는 도구가 따로 있을까?
  </div>
</section>

<!-- ===================== CH 07 ===================== -->
<section id="ch7">
  <h2 class="chap"><span class="num">CH 07</span>한계 — PCA로 못 펴는 군집, t-SNE 맛보기<a href="#ch7" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>PCA는 선형 투영이다 — 평면에 그림자를 떨어뜨리는 것과 같아서, 곡면 위에 말려 있는 군집은 겹쳐 보일 수 있다.
  <strong>t-SNE</strong>는 발상이 다르다. 전역 분산이 아니라 <strong>각 점의 가까운 이웃 관계(국소 거리)</strong>를 저차원에서도
  최대한 보존하려 한다. 그래서 같은 군집은 더 단단히 뭉치는 경향이 있다.</p>

  <blockquote class="cite">
    "t-SNE … converts similarities between data points to joint probabilities and tries to minimize
    the Kullback-Leibler divergence between the joint probabilities of the low-dimensional embedding
    and the high-dimensional data. … It is highly recommended to use another dimensionality reduction
    method (e.g. PCA) to reduce the number of dimensions if the number of features is very high."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html" target="_blank" rel="noopener">sklearn.manifold.TSNE</a></span>
  </blockquote>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    같은 digits 데이터를 PCA 2D와 t-SNE 2D로 각각 펼친 뒤 "동일 라벨 평균거리 / 타 라벨 평균거리" 비율을 재면,
    <strong>t-SNE의 비율이 더 작을 것</strong>(같은 숫자끼리 상대적으로 더 가까이 뭉침)이다.
  </div>

  <h3 class="step">테스트 — PCA 2D vs t-SNE 2D 군집 응집도</h3>
  <div class="terminal">
    <div class="terminal-header">pca_intro_runner.py §05 · TSNE vs PCA 2D — 동일/타 라벨 거리 비율 비교 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_05@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_05@@" alt="digits 데이터의 PCA 2D와 t-SNE 2D 임베딩 산점도 비교">
    <figcaption>그림 0604-6 · 같은 데이터, 왼쪽 PCA 2D(엉킴) vs 오른쪽 t-SNE 2D — t-SNE에서 숫자별 섬이 또렷하게 분리된다</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">가설 통과</span>
    응집 비율(낮을수록 잘 뭉침)이 PCA 2D 0.5207 → t-SNE 2D <strong>0.2496</strong>으로 절반 가까이 줄었다.
    t-SNE 그림에서는 숫자마다 또렷한 섬이 떨어져 보인다. 다만 t-SNE는 <strong>시각화 전용</strong>이다 —
    축 자체엔 의미가 없고 <code>transform</code>으로 새 데이터를 넣을 수 없어, 모델 전처리에는 PCA를 쓰고 t-SNE는 눈으로 보는 데만 쓴다.
  </div>

  <div class="callout">
    <span class="label">함정</span>
    t-SNE의 좌표 절대값·축·군집 간 거리는 해석하면 안 된다. "어떤 점이 어떤 점과 이웃인가"(국소 구조)만 의미가 있고,
    섬과 섬 사이의 간격은 <code>perplexity</code> 등 하이퍼파라미터에 따라 달라진다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — PCA와 t-SNE 를 나란히 봤더니 둘의 성격이 꽤 달랐다. 그러면 수업에서 같이 등장한
    <strong>LDA</strong> 까지 셋을 한자리에 놓고 "언제 무엇을 쓰나"를 정리해 둘 필요가 있다. 짧게 비교한다.
  </div>
</section>

<!-- ===================== CH 08 (PCA vs LDA vs t-SNE 비교) ===================== -->
<section id="ch8">
  <h2 class="chap"><span class="num">CH 08</span>비교 — PCA vs LDA vs t-SNE<a href="#ch8" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>차원 축소라고 다 같은 일을 하는 게 아니다. 수업에서 함께 나온 세 기법은 "무엇을 최대로 보존하느냐"가 서로 다르다.
  <strong>PCA</strong>는 정답 라벨을 쓰지 않고 데이터 <em>전체의 분산</em>이 가장 큰 직교 축을 찾는 비지도 기법이다.
  <strong>LDA(선형 판별 분석)</strong>는 라벨을 쓰는 지도 기법으로, <em>클래스 사이 분산은 크게, 클래스 내부 분산은 작게</em> 만드는 축을 찾아
  분류에 유리하도록 줄인다. <strong>t-SNE</strong>는 분산이 아니라 <em>각 점의 국소 이웃 관계</em>를 저차원에서도 보존하려는 비선형 시각화 기법이다.</p>

  <blockquote class="cite">
    "Linear Discriminant Analysis … is a supervised method, using known class labels."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/lda_qda.html" target="_blank" rel="noopener">Linear and Quadratic Discriminant Analysis</a></span>
  </blockquote>

  <h3 class="step">의문 → 비교</h3>
  <div class="qbox">
    <span class="label">의문</span>
    셋 다 "차원을 줄인다"인데 왜 따로 배우나? 핵심 갈림은 두 가지다 — ① 정답 라벨을 쓰는가(지도/비지도),
    ② 선형 축인가 비선형 매핑인가, 그리고 ③ 전처리에 재사용 가능한가, 아니면 그림용인가. 표로 한자리에 정리한다.
  </div>

  <h3 class="step">정리 — 세 기법 한눈에</h3>
  <table>
    <thead>
      <tr><th>구분</th><th>PCA</th><th>LDA</th><th>t-SNE</th></tr>
    </thead>
    <tbody>
      <tr><td>라벨 사용</td><td>비지도 (y 불필요)</td><td class="hl">지도 (y 필수)</td><td>비지도 (y 불필요)</td></tr>
      <tr><td>최대로 보존하는 것</td><td>데이터 전체 분산</td><td>클래스 간 분리도<br>(클래스 간↑ / 내부↓)</td><td>국소 이웃 관계</td></tr>
      <tr><td>선형/비선형</td><td>선형 투영</td><td>선형 투영</td><td class="hl">비선형 매핑</td></tr>
      <tr><td>축소 차원 한계</td><td>원래 차원 d 까지</td><td>클래스 수 − 1 까지</td><td>보통 2~3 (시각화)</td></tr>
      <tr><td>새 데이터 transform</td><td>가능</td><td>가능</td><td class="hl">불가 (매번 다시 학습)</td></tr>
      <tr><td>주 용도</td><td>전처리·압축·노이즈 제거</td><td>분류 전 차원 축소</td><td>군집 구조 시각화</td></tr>
    </tbody>
  </table>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">정리</span>
    셋의 갈림은 "무엇을 최대로 남기느냐"다. <strong>PCA는 분산</strong>(라벨 없이 압축·전처리),
    <strong>LDA는 클래스 분리</strong>(라벨로 분류에 유리하게 — 그래서 클래스 수−1 차원까지만),
    <strong>t-SNE는 이웃 관계</strong>(비선형, 그림 전용이라 <code>transform</code> 불가). 모델 입력 전처리에는 PCA/LDA를,
    군집을 눈으로 보는 데는 t-SNE를 쓴다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 비교까지 끝냈다. 이제 출발 데이터였던 64차원 digits 만이 아니라,
    특성 수가 다른 iris(4개)·breast_cancer(30개)에서도 "분산 큰 축부터 남긴다"는 PCA 원리가 통하는지 확인한다.
  </div>
</section>

<!-- ===================== CH 09 ===================== -->
<section id="ch9">
  <h2 class="chap"><span class="num">CH 09</span>일반화 — 다른 데이터에서도 통하나<a href="#ch9" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    PCA의 압축률은 데이터의 특성 간 상관 정도에 달려 있다. 특성이 적고 잘 정리된 iris(4특성)는 2D만으로도 분산 대부분을 담겠지만,
    특성이 많고 상관 구조가 복잡한 breast_cancer(30특성)는 <strong>2D 보존 분산이 더 낮고 90%에 필요한 주성분도 더 많을 것</strong>이다.
  </div>

  <h3 class="step">테스트 — iris·breast_cancer 의 2D 보존 분산과 90% 임계</h3>
  <div class="terminal">
    <div class="terminal-header">pca_intro_runner.py §06 · PCA(iris/breast_cancer) — 2D 보존 분산·90% 임계 주성분 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_06@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT</span>
    iris 는 2개 주성분이 분산의 <strong>95.8%</strong>를 담아 90%에 2개면 충분했지만, breast_cancer 는 2D가 <strong>63.2%</strong>만 담고
    90%에 7개가 필요했다. 같은 PCA라도 데이터의 상관 구조에 따라 압축률이 달라진다 — "몇 개로 줄일지"에 정답은 없고,
    <strong>누적 설명분산 곡선을 보고 데이터마다 정하는 것</strong>이 원리다.
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 차원의 저주에서 출발해 PCA·누적분산·2D 시각화·재구성·t-SNE까지 왔다.
    이제 출발 의문 "특성이 많으면 무엇이 문제이고, 어떻게 줄이는가"로 돌아가 한 문장으로 닫는다.
  </div>
</section>

<!-- ===================== CH 10 ===================== -->
<section id="ch10">
  <h2 class="chap"><span class="num">CH 10</span>정리 — '차원을 줄인다'가 정한 것<a href="#ch10" class="anchor-link">#</a></h2>

  <h3 class="step">출발 의문 회수</h3>
  <p>CH 01의 질문은 "특성이 수십·수백 개면 무엇이 문제이고, 정보를 지키며 줄일 수 있는가"였다.
  답은 사슬을 따라 모였다 — 차원이 커지면 거리가 희박해지고 그릴 수도 없다(CH 01),
  그 줄이는 기준의 출발점인 공분산 행렬을 손으로 뜯어 <code>XᵀX</code>가 (d×d) 지도가 되는 이유를 확인하고(CH 02),
  분산이 큰 축부터 남기는 PCA로 줄이되(CH 03), 얼마나 남길지는 누적 설명분산이 정하고(CH 04),
  2개 축이면 군집 윤곽은 보이되 세부는 흐리며(CH 05), 버린 만큼 정보가 사라져 줄이면 무조건 좋아지지는 않고(CH 06),
  직선으로 못 펴는 비선형 구조는 t-SNE로 눈으로 보며(CH 07), PCA·LDA·t-SNE 의 쓰임이 갈린다(CH 08).
  그리고 그 압축률은 데이터마다 다르다(CH 09).</p>

  <h3 class="step">최종 결론</h3>
  <div class="keypoint">
    <span class="label">FINAL CONCLUSION</span>
    <strong>PCA가 정하는 것은 '분산이 가장 큰 직교 축들과, 그 위에 데이터를 투영한 좌표'다.</strong>
    차원 축소는 정보를 공짜로 압축하는 마술이 아니라, 분산이 작은 축(=정보가 적은 축)부터 버려
    <strong>정보 손실과 차원을 맞바꾸는 거래</strong>이며, 어디서 멈출지는 누적 설명분산 곡선이 알려 준다.
    PCA는 전처리·압축에, t-SNE는 비선형 군집을 눈으로 확인하는 시각화에 쓴다.
  </div>

  <h3 class="step">한 문장으로</h3>
  <div class="keypoint">
    <span class="label">ONE-LINER</span>
    "차원을 줄인다"의 실체는 — <strong>데이터가 가장 많이 퍼진 방향부터 골라 남기고, 덜 퍼진 방향을 버려
    정보를 최대한 지키며 축을 줄이는 일</strong>이다. 64차원 손글씨도 31개 축이면 분산의 9할이 남았고, 2개 축이면 눈으로 볼 수 있었다.
  </div>

  <div class="ref-chain">
    <p class="ref-title">📚 전체 근거 출처</p>
    <ol>
      <li><strong>공식 문서</strong>
        <a href="https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html" target="_blank" rel="noopener">scikit-learn · PCA</a>(분산 최대 축·explained_variance_ratio_),
        <a href="https://scikit-learn.org/stable/modules/decomposition.html#pca" target="_blank" rel="noopener">Decomposition User Guide</a>,
        <a href="https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html" target="_blank" rel="noopener">TSNE</a>(국소 구조·KL divergence·시각화 전용),
        <a href="https://scikit-learn.org/stable/modules/lda_qda.html" target="_blank" rel="noopener">LDA/QDA</a>(지도 차원 축소·클래스 분리),
        <a href="https://scikit-learn.org/stable/auto_examples/applications/plot_digits_denoising.html" target="_blank" rel="noopener">PCA inverse_transform 예제</a>.</li>
      <li><strong>workspace</strong>
        <code>../ml_workspace/from_colab/0604-s/dimensionality_reduction.ipynb</code> : 수업 차원 축소 흐름(PCA→LDA→t-SNE→UMAP→Autoencoder).</li>
      <li><strong>강의자료</strong>
        Day6 차원 축소 PDF 는 로컬에 미보유 → 위 sklearn 공식 문서로 근거를 대체했다(배경지식).</li>
      <li><strong>실행 검증</strong>
        <code>.study/test/pca_intro/pca_intro_runner.py §00~§06</code>
        → <code>logs/*.txt</code>, <code>charts/*.png</code> (고정 시드 42, 재현 가능).</li>
    </ol>
  </div>

  <div class="bridge">
    <strong>다음 글 예고</strong> — PCA·t-SNE 는 정답 없이 구조를 찾는 비지도 학습의 입구였다.
    이어지는 Day7 에서는 같은 비지도 계열의 k-means 군집화와 연관규칙으로 들어간다.
  </div>
</section>
</main>

<footer>
  <p>SK 네트웍스 AI Family 32기 · 교과목 2 단원 2 머신러닝 Day6 (2026-06-04)</p>
  <p>모든 터미널 출력은 <code>.study/test/pca_intro/pca_intro_runner.py</code> 실제 실행 결과이며,
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
