# build_practice03_html.py
# ml_practice03_svm_knn_nb.html 조립 — logs/*.txt(실제 실행 결과) + charts/*.png(base64) 주입
# 실행: c:\_proj\python_workspace\.venv\Scripts\python.exe build_practice03_html.py
#   (= GUIDE §11 run_all 역할: 터미널 값 직접 작성 금지, 로그에서 주입)
#   문체: ml_practice02_titanic.html / day0527_ml_intro.html 의 "의문→해결→새 의문" 서사 추적 방식.
import base64, html, pathlib, re

HERE = pathlib.Path(__file__).parent
LOGS = HERE / "logs"
CHARTS = HERE / "charts"
OUT = HERE.parent.parent / "blog" / "ml_practice03_svm_knn_nb.html"   # .study/blog/
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
    "@@TERM_00@@": term("00_three_problems"),
    "@@TERM_01@@": term("01_svm_letter_scaling"),
    "@@TERM_02@@": term("02_svm_kernel_confusion"),
    "@@TERM_03@@": term("03_postcode_lookup"),
    "@@TERM_04@@": term("04_knn_scaling"),
    "@@TERM_05@@": term("05_knn_k_sweep"),
    "@@TERM_06@@": term("06_nb_laplace"),
    "@@TERM_07@@": term("07_nb_report"),
    "@@CHART_SVM_SCALE@@": chart("ch_svm_scaling.png"),
    "@@CHART_SVM_CM@@": chart("ch_svm_confusion.png"),
    "@@CHART_POST@@": chart("ch_postcode.png"),
    "@@CHART_KNN@@": chart("ch_knn_ksweep.png"),
    "@@CHART_NB@@": chart("ch_nb_laplace.png"),
}

HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>파이썬 머신러닝 분류기 분석: 문제마다 다른 분류기 — SVM·KNN·나이브베이즈를 직접 확인해 본다</title>
  <meta name="description" content="SK 네트웍스 AI Family 32기 머신러닝 실습3(과제). '글자/우편번호는 SVM, 유방암은 KNN, 스팸은 나이브베이즈 — 왜 문제마다 분류기가 달라야 하나'를 따라가며 스케일링의 필요성, 커널 선택, k 튜닝, 거리 민감성, 조건부독립 가정·라플라스 스무딩을 sklearn 실측으로 검증한 기록.">
  <meta property="og:title" content="문제마다 다른 분류기 — SVM·KNN·나이브베이즈를 직접 확인해 본다">
  <meta property="og:description" content="스케일 안 한 SVM/KNN의 하락, 혼동되는 글자, 우편번호 조회기, k 선택, 라플라스 스무딩까지 실측으로 추적">
  <meta property="og:type" content="article">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="문제마다 다른 분류기 — SVM·KNN·나이브베이즈">
  <meta name="twitter:description" content="SVM 스케일링 → 커널·혼동행렬 → 우편번호 → KNN k선택 → 나이브베이즈 스무딩">
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
  <p class="eyebrow">Python · 머신러닝 실습3(과제) · 부트캠프</p>
  <h1>문제마다 다른 분류기 — SVM·KNN·나이브베이즈를 직접 확인해 본다</h1>
  <p class="deck">실습3 과제로 분류기 세 개를 한꺼번에 받았다 — 글자/우편번호는 <strong>SVM</strong>,
  유방암 진단은 <strong>KNN</strong>, 스팸 문자는 <strong>나이브베이즈</strong>.
  처음엔 "왜 굳이 문제마다 다른 분류기를 써야 하지?"가 의아했다. 이 글은 그 의문을 주어로 삼아 —
  스케일을 안 했더니 SVM과 KNN이 어떻게 낮아지는지, 글자는 어떤 글자와 헷갈리는지,
  k는 어떻게 고르는지, 나이브베이즈의 "조건부독립 가정"이 무엇을 포기하는지를 하나씩 부딪쳐 본 기록이다.
  모든 수치는 sklearn 으로 직접 돌린 결과이며 <code>random_state=42</code> 로 재현 가능하다.</p>
  <div class="meta-row">
    <span><strong>날짜</strong>2026-05-29</span>
    <span><strong>Python</strong>@@PY@@ · scikit-learn 1.8.0 · NumPy 2.4.4 · Pandas 3.0.2</span>
    <span><strong>OS</strong>Windows 11 Pro 25H2</span>
    <span><strong>IDE</strong>VS Code 1.117.0</span>
    <span><strong>HW</strong>Asrock x600 · Ryzen 8600G · 24GB LPDDR5 · RTX 4070 Super 12GB</span>
    <span><strong>커리큘럼</strong>교과목 2 · 단원 2 · 머신러닝 — 머신러닝_서포트백터머신구조.pdf</span>
  </div>
</header>

<main>
<nav class="flow">
  <h2>이 글의 흐름 — 하나의 의문에서 갈라져 나온 세 과제</h2>
  <ol>
    <li><a href="#ch1">시작 — 왜 문제마다 분류기가 다른가 (데이터 성격부터 가른다)</a></li>
    <li><a href="#ch2"><span class="turn">막힘</span> — SVM 글자 분류, 스케일을 안 했더니</a></li>
    <li><a href="#ch3">커널 — linear로는 부족했다, 그리고 어떤 글자가 헷갈리나</a></li>
    <li><a href="#ch4">응용 — 같은 SVM 코드로 우편번호 조회기를 만들다</a></li>
    <li><a href="#ch5">KNN 유방암, 또 스케일에서 크게 낮아졌다</a></li>
    <li><a href="#ch6">k 고르기 — 1은 왜 위험하고, 암 진단은 무엇을 봐야 하나</a></li>
    <li><a href="#ch7">나이브베이즈 — 텍스트엔 왜 이 분류기인가 (조건부독립 가정)</a></li>
    <li><a href="#ch8">스무딩 — 본 적 없는 단어의 확률 0 문제, 그리고 정밀도/재현율</a></li>
    <li><a href="#ch9">정리 — '데이터 성격에 따라 분류기를 고른다'로 회수</a></li>
  </ol>
</nav>

<!-- ===================== CH 01 ===================== -->
<section id="ch1">
  <h2 class="chap"><span class="num">CH 01</span>시작 — 왜 문제마다 분류기가 다른가<a href="#ch1" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>실습3 과제지에는 분류기 세 개가 따로 떨어져 있었다 — SVM으로 글자/우편번호, KNN으로 유방암,
  나이브베이즈로 스팸. 같은 "분류"인데 왜 도구가 셋일까? 강의자료는 세 알고리즘의 장단점을 이렇게 갈라 둔다 —
  SVM은 "고차원에 강하지만 속도가 느리고 튜닝이 어렵다", KNN은 "가장 가까운 K개를 보고 분류한다",
  나이브베이즈는 "feature들이 서로 독립이라 가정 … 텍스트 분류에 강하다".</p>

  <blockquote class="cite">
    "Support Vector Machines are … effective in high dimensional spaces …
    still effective in cases where number of dimensions is greater than the number of samples."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/svm.html" target="_blank" rel="noopener">Support Vector Machines</a></span>
  </blockquote>

  <h3 class="step">의문 → 기준</h3>
  <div class="qbox">
    <span class="label">의문</span>
    분류기를 고르는 기준이 따로 있을 것이다. 그렇다면 그 기준은 모델이 아니라 <strong>데이터의 성격</strong>
    — 클래스가 몇 개인지, 특성이 연속인지 텍스트인지, 스케일이 제각각인지 — 에서 나와야 한다.
    세 과제의 데이터를 한자리에 놓고 성격부터 가르면, 왜 분류기가 갈리는지 첫 단서가 보일 것이다.
  </div>

  <h3 class="step">테스트 — 세 데이터의 성격을 진단한다</h3>
  <div class="terminal">
    <div class="terminal-header">ml_practice03_runner.py — 세 과제 데이터 성격(클래스수·특성성격·스케일) 진단 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_00@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">기준 확정</span>
    글자는 26클래스 정수 특성(다중클래스 경계 → SVM), 유방암은 30개 연속 특성에 스케일이 약 6800배 벌어진
    이진 문제(거리 기반 → KNN, 단 표준화 필수), 스팸은 단어 출현 0/1의 고차원 희소 텍스트(조건부독립 → 나이브베이즈).
    데이터 성격이 분류기를 부른다. 그런데 "거리/경계 기반"이라는 SVM·KNN의 공통점이 곧 공통의 함정도 만든다 — 스케일.
  </div>

  <div class="bridge">
    <strong>첫 과제로</strong> — SVM 글자 분류부터 손을 댔다. 그런데 데이터를 그대로 SVC에 넣었더니
    정확도가 어딘가 아쉬웠다. 강의자료가 말한 "고차원에 강함"은 어디 가고, 왜 이 정도일까?
  </div>
</section>

<!-- ===================== CH 02 ===================== -->
<section id="ch2">
  <h2 class="chap"><span class="num">CH 02</span>막힘 — SVM 글자 분류, 스케일을 안 했더니<a href="#ch2" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    RBF SVM은 두 점 사이의 거리(<code>exp(-γ‖x−x'‖²)</code>)로 유사도를 잰다. 특성마다 값 범위가 다르면
    범위가 큰 특성이 거리를 독점한다. 그러니 <code>StandardScaler</code>로 모든 특성을 평균0·표준편차1로 맞추면
    같은 데이터·같은 SVC라도 정확도가 올라야 한다. 글자 데이터로 '스케일 없음 vs 표준화'를 나란히 돌려 확인한다.
  </div>

  <pre><code class="language-python"># path : .study/test/ml_practice03/ml_practice03_runner.py §01 (발췌)
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler

# 스케일 없이 RBF SVM
svm_raw = SVC(kernel="rbf", gamma="scale", random_state=42).fit(Xtr, ytr)

# train으로만 fit한 스케일러를 test엔 transform만 (data leakage 방지)
sc = StandardScaler().fit(Xtr)
svm_sc = SVC(kernel="rbf", gamma="scale", random_state=42).fit(sc.transform(Xtr), ytr)
print(svm_raw.score(Xte, yte))           # 스케일 없음
print(svm_sc.score(sc.transform(Xte), yte))  # 표준화 적용</code></pre>

  <h3 class="step">테스트</h3>
  <div class="terminal">
    <div class="terminal-header">ml_practice03_runner.py §01 · SVC(rbf) 스케일 없음 vs StandardScaler — 글자 정확도 비교 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_01@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_SVM_SCALE@@" alt="스케일 없음과 표준화 적용 SVM 정확도 막대 비교">
    <figcaption>그림 1 · RBF SVM 글자 분류 — 표준화만으로 test 정확도 0.875 → 0.901 (+0.025)</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">가설 통과</span>
    같은 데이터·같은 RBF SVM인데 스케일 없음 0.8753, 표준화 0.9007. 모델은 한 글자도 바꾸지 않고
    <strong>특성을 같은 자에 올렸을 뿐</strong>인데 정확도가 +0.0253 올랐다. 거리 기반 모델에서 표준화는 옵션이 아니라 전제다.
  </div>

  <div class="bridge">
    <strong>그래도 0.90이다</strong> — 26개 글자를 가르기엔 아직 아쉽다. 지금 쓴 건 RBF 커널인데,
    더 단순한 linear 커널이면 어떨까? 그리고 0.10의 오차는 대체 <em>어떤 글자끼리</em> 헷갈린 걸까?
  </div>
</section>

<!-- ===================== CH 03 ===================== -->
<section id="ch3">
  <h2 class="chap"><span class="num">CH 03</span>커널 — linear로는 부족했다, 어떤 글자가 헷갈리나<a href="#ch3" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 비교</h3>
  <div class="qbox">
    <span class="label">가설</span>
    글자 모양 경계는 직선 하나로 가를 수 없는 비선형일 것이다. 그렇다면 linear 커널보다
    RBF 커널(곡면 경계)의 정확도가 높아야 한다. 또 혼동행렬의 대각선을 지우고 가장 큰 칸을 뽑으면
    "가장 많이 혼동되는 글자쌍"이 드러날 것이다 — 과제2가 요구한 분석이다.
  </div>

  <h3 class="step">테스트 — 커널 비교 + 혼동 글자쌍 추출</h3>
  <div class="terminal">
    <div class="terminal-header">ml_practice03_runner.py §02 · SVC linear vs rbf · confusion_matrix 혼동쌍 TOP3 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_02@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_SVM_CM@@" alt="RBF SVM 26x26 혼동행렬 히트맵">
    <figcaption>그림 2 · RBF SVM 혼동행렬(26×26) — 대각선이 진하고, 비대각 칸이 혼동된 글자쌍</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">관찰 결과</span>
    linear 0.8347 < rbf 0.9007 — 글자 경계는 역시 비선형이라 곡면 커널이 더 낫다.
    가장 많이 혼동된 쌍은 linear에서 <strong>O↔H, Q→G</strong>, rbf에서 <strong>P→F, H→O, C→G</strong>.
    모양이 닮은 글자끼리(둥근 O·Q·G·C, 세로획 H·P·F) 헷나뉜다는 게 수치로 확인된다.
    SVM의 약점인 "속도 느림·튜닝"은 커널·γ 선택으로 나타나고, 그 보상이 이 비선형 경계다.
  </div>

  <div class="bridge">
    <strong>여기서 욕심이 생겼다</strong> — 글자를 분류하는 이 SVM 골격을, 과제3의 우편번호 문제에 그대로 쓸 수 있을까?
    "입력을 정해진 라벨로 매핑한다"는 분류의 본질만 보면, 주소↔우편번호도 같은 문제로 보인다.
  </div>
</section>

<!-- ===================== CH 04 ===================== -->
<section id="ch4">
  <h2 class="chap"><span class="num">CH 04</span>응용 — 같은 골격으로 우편번호 조회기를 만들다<a href="#ch4" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 설계</h3>
  <div class="qbox">
    <span class="label">의문</span>
    과제3은 "우편물의 우편번호를 읽어 분류하고, 우편번호↔주소를 오갈 수 있게" 하라고 했다.
    글자 SVM이 16개 픽셀 통계를 26라벨로 매핑했듯, 우편번호 문제도 결국 <strong>주소(시·구·동) ↔ 우편번호</strong>의
    매핑이다. 52,543건 실제 우편 데이터를 색인하면, 양방향 조회가 즉시 되어야 한다.
  </div>
  <p>전국 우편번호 CSV(EUC-KR 인코딩, 국가데이터처)를 읽어 <code>우편번호→주소</code>와
  <code>"도 시군구 읍면동"→우편번호 목록</code> 두 사전을 만든다. 분류기의 "예측"을 데이터 색인으로 구현한 셈이다.</p>

  <pre><code class="language-python"># path : .study/test/ml_practice03/ml_practice03_runner.py §03 (발췌)
df = pd.read_csv(POST_CSV, encoding="euc-kr")          # 전국 우편번호 (EUC-KR)
code_to_addr = df.drop_duplicates("우편번호").set_index("우편번호")["전체주소"].to_dict()
df["_key"] = df["도이름"] + " " + df["시군구이름"] + " " + df["읍면동이름"]
addr_to_codes = df.groupby("_key")["우편번호"].apply(lambda s: sorted(s.unique())).to_dict()
print(code_to_addr[137926])                  # 우편번호 → 주소
print(addr_to_codes["서울특별시 서초구 서초1동"])  # 주소 → 우편번호 목록</code></pre>

  <h3 class="step">테스트</h3>
  <div class="terminal">
    <div class="terminal-header">ml_practice03_runner.py §03 · 우편번호 CSV(EUC-KR) 색인 — 양방향 조회 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_03@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_POST@@" alt="시도별 우편번호 분포 막대 그래프">
    <figcaption>그림 3 · 시도별 우편번호 분포(상위 10) — 분류 라벨(우편번호)이 지역마다 얼마나 많은지</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">정리</span>
    우편번호 31,357개·주소키 6,005개를 색인해, <code>137926 → 서울특별시 서초구 서초1동</code>,
    <code>'서울특별시 서초구 서초1동' → 16개 우편번호</code>가 즉시 나온다. 모든 클래스(우편번호)에
    표본이 충분하고 입력이 정확히 라벨로 떨어지는 문제에선, 학습형 분류기보다 <strong>색인(룩업)</strong>이 정확하고 빠르다 —
    이것도 "데이터 성격에 맞는 도구 선택"의 한 사례다.
  </div>

  <div class="bridge">
    <strong>SVM 과제를 마치고</strong> 두 번째 분류기 KNN으로 넘어갔다. 유방암 진단 데이터를 KNN에 그대로 넣었는데 —
    CH 02에서 본 그 장면이 또 나왔다. 스케일을 안 했더니 또 낮아진 것이다.
  </div>
</section>

<!-- ===================== CH 05 ===================== -->
<section id="ch5">
  <h2 class="chap"><span class="num">CH 05</span>KNN 유방암도 스케일에서 크게 낮아졌다<a href="#ch5" class="anchor-link">#</a></h2>

  <h3 class="step">학습 → 가설</h3>
  <p>KNN은 "가장 가까운 K개 이웃의 다수결"로 분류한다. 거리가 전부다. 유방암 데이터는
  <code>area_mean</code>(수백)과 <code>smoothness_mean</code>(0.x)이 약 6800배나 차이 났다(CH 01).
  표준화 없이 유클리드 거리를 재면 <code>area</code> 하나가 거리를 거의 다 결정하고, 나머지 29개 특성은 묻힌다.</p>
  <div class="qbox">
    <span class="label">가설</span>
    KNN(k=5)을 스케일 없이 / 표준화로 각각 돌리면, 표준화 쪽이 정확도뿐 아니라
    <strong>악성 재현율(recall)</strong>도 높을 것이다. 암 진단에선 "악성을 양성으로 놓치는 것(FN)"이 가장 위험하니 recall이 핵심 지표다.
  </div>

  <blockquote class="cite">
    "Standardize features by removing the mean and scaling to unit variance.
    Many estimators … behave badly if the individual features do not more or less
    look like standard normally distributed data."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html" target="_blank" rel="noopener">StandardScaler</a></span>
  </blockquote>

  <h3 class="step">테스트</h3>
  <div class="terminal">
    <div class="terminal-header">ml_practice03_runner.py §04 · KNeighborsClassifier(k=5) 스케일 유무 — 정확도·악성 recall · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_04@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">가설 통과</span>
    스케일 없음 정확도 0.9301·악성 recall 0.9057 → 표준화 정확도 0.9720·recall 0.9811.
    recall이 +0.0755 오른 게 특히 중요하다 — 표준화 전엔 악성 53건 중 5건을 놓쳤지만, 표준화 후엔 1건만 놓쳤다.
    SVM에서 본 함정(CH 02)이 KNN에서 똑같이, 더 심각한으로 반복됐다. 거리 기반 분류기의 공통 전제는 표준화다.
  </div>

  <div class="bridge">
    <strong>이제 KNN 고유의 손잡이</strong> — k다. k=5로 좋은 결과를 봤지만, k=1이나 k=25면 어떻게 달라질까?
    너무 작으면 노이즈 한 점에 휘둘리고, 너무 크면 경계가 뭉개진다고 들었다. 직접 1~25를 쓸어 본다.
  </div>
</section>

<!-- ===================== CH 06 ===================== -->
<section id="ch6">
  <h2 class="chap"><span class="num">CH 06</span>k 고르기 — 1은 왜 위험하고, 암은 무엇을 봐야 하나<a href="#ch6" class="anchor-link">#</a></h2>

  <h3 class="step">실험 → 관찰</h3>
  <p>k를 1부터 25까지(홀수) 바꿔가며 train 정확도·test 정확도·악성 recall을 같이 찍는다.
  k=1은 "가장 가까운 한 점"만 보므로 train은 완벽히 외우지만(과대적합 신호), test에선 노이즈에 약하다.</p>
  <div class="terminal">
    <div class="terminal-header">ml_practice03_runner.py §05 · KNN k 1~25 sweep — train/test 정확도·악성 recall · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_05@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_KNN@@" alt="k에 따른 train/test 정확도와 악성 recall 곡선">
    <figcaption>그림 4 · k↑ → train 정확도는 1.0에서 내려오고, test/recall은 k=3 부근에서 정점</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">기준 확정</span>
    k=1은 train 정확도 1.0(완전 암기)이지만 test 0.9371로 떨어진다 — 전형적 과대적합.
    최적은 <strong>k=3</strong>(test 정확도 0.9790·악성 recall 0.9811)이었다. 다만 k가 커지면
    recall이 0.94→0.91로 흔들리는 구간이 있어, 암 진단에선 정확도만이 아니라 <strong>recall을 함께 보고 k를 골라야</strong> 한다.
    "가까운 K개"라는 한 줄 규칙의 K가 곧 모델 복잡도 손잡이였다.
  </div>

  <div class="bridge">
    <strong>두 거리 기반 분류기</strong>(SVM·KNN)를 마치니 공통점이 또렷했다 — 스케일·복잡도 튜닝이 핵심.
    그런데 세 번째 과제 스팸은 특성이 "단어"다. 수천 개 단어를 거리로 잴 수도, 경계로 가를 수도 없다. 왜 여기선 나이브베이즈일까?
  </div>
</section>

<!-- ===================== CH 07 ===================== -->
<section id="ch7">
  <h2 class="chap"><span class="num">CH 07</span>나이브베이즈 — 텍스트엔 왜 이 분류기인가<a href="#ch7" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>나이브베이즈는 베이즈 정리로 <code>P(클래스|문서) ∝ P(클래스)·∏ P(단어ᵢ|클래스)</code>를 계산한다.
  여기서 "naive(순진한)"는 <strong>모든 단어가 클래스 안에서 서로 독립</strong>이라고 가정한다는 뜻이다.
  실제 언어에서 "free"와 "prize"는 함께 등장하니 독립은 거짓이다 — 그런데도 잘 된다.</p>

  <blockquote class="cite">
    "Naive Bayes methods are a set of supervised learning algorithms based on applying Bayes' theorem
    with the 'naive' assumption of conditional independence between every pair of features …
    they have worked quite well in many real-world situations, famously document classification and spam filtering."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/naive_bayes.html" target="_blank" rel="noopener">Naive Bayes</a></span>
  </blockquote>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    단어 수천 개는 SVM·KNN엔 고차원·희소라 부담이지만, 나이브베이즈는 각 단어 확률을 곱하기만 하면 되니
    빠르고 텍스트에 강할 것이다. <code>CountVectorizer(binary=True)</code>로 단어 출현을 0/1로 만든 뒤
    <code>BernoulliNB</code>로 이진 텍스트 분류(스팸형)를 돌려, 고차원 희소에서도 잘 동작하는지 본다.
  </div>
  <p>실습 노트북은 UCI SMS 스팸셋을 인터넷에서 받아 쓰지만(오프라인 재현 불가), 여기선 sklearn 내장
  20newsgroups 두 주제를 스팸형 이진 텍스트로 대체했다 — 조건부독립·DTM·스무딩의 학습 목적은 동일하다.</p>

  <h3 class="step">테스트 — 정밀도/재현율과 특징 단어</h3>
  <div class="terminal">
    <div class="terminal-header">ml_practice03_runner.py §07 · BernoulliNB · classification_report — 정밀도/재현율·클래스 단어 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_07@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">관찰 결과</span>
    2,297개 단어 특성(고차원 희소)에서도 정확도 0.872·정밀도 0.883·재현율 0.872로 단숨에 분류했다.
    클래스별 특징 단어(car/cars vs use/used)가 각 주제와 맞아떨어진다. 독립 가정은 비현실적이지만,
    분류 순위만 맞으면 되므로 텍스트에서 실용적으로 강하다 — 강의자료의 "텍스트 분류 강함"이 수치로 확인됐다.
  </div>

  <div class="bridge">
    <strong>그런데 가정 하나가 걸렸다</strong> — 학습 때 한 번도 안 나온 단어가 test에 등장하면
    <code>P(단어|클래스)=0</code>이 되어 확률 전체가 0으로 낮아진다. 과제1이 요구한 라플라스 스무딩이 바로 이 구멍을 메운다.
  </div>
</section>

<!-- ===================== CH 08 ===================== -->
<section id="ch8">
  <h2 class="chap"><span class="num">CH 08</span>스무딩 — 확률 0 문제, 그리고 무엇으로 '잘함'을 재나<a href="#ch8" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    라플라스 스무딩은 모든 단어 빈도에 <code>α</code>를 더해 확률이 정확히 0이 되는 걸 막는다.
    과제 표대로 <code>α</code>를 0 / 0.1 / 0.5 / 1.0으로 바꾸면, α=0(스무딩 없음)보다 약간의 스무딩이 정확도를 올릴 것이다.
  </div>

  <blockquote class="cite">
    "In Laplace smoothing, alpha controls the additive smoothing. Setting alpha to a value greater than 0
    accounts for features not present in the learning samples and prevents zero probabilities."
    <span class="src">— scikit-learn 공식 문서 · <a href="https://scikit-learn.org/stable/modules/naive_bayes.html#bernoulli-naive-bayes" target="_blank" rel="noopener">Bernoulli Naive Bayes / smoothing</a></span>
  </blockquote>

  <h3 class="step">테스트 — 라플라스 스무딩 sweep</h3>
  <div class="terminal">
    <div class="terminal-header">ml_practice03_runner.py §06 · BernoulliNB alpha 0/0.1/0.5/1.0 — 정확도 비교 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_06@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_NB@@" alt="라플라스 스무딩 alpha에 따른 정확도 곡선">
    <figcaption>그림 5 · 라플라스 스무딩 — α=0 보다 α=0.1에서 정확도가 가장 높다</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">가설 통과</span>
    α=0일 때 0.8657에서, α=0.1에서 0.8796으로 가장 높고 α를 더 키우면 다시 살짝 내려간다.
    스무딩 없이는 본 적 없는 단어가 확률을 0으로 만들지만, 작은 α가 그 구멍을 메워 일반화가 좋아진 것이다.
    과제 표(SMS 스팸셋 0.9806→0.9835)와 데이터는 달라도 <strong>"약간의 스무딩이 최적"</strong>이라는 경향은 똑같다.
    분류 성능은 정확도 한 숫자가 아니라 <strong>정밀도·재현율</strong>까지 봐야 한다(CH 07) — 스팸을 놓침(recall) vs 정상을 스팸 처리(정밀도).
  </div>

  <div class="bridge">
    <strong>세 과제를 모두 끝냈다</strong> — SVM·KNN·나이브베이즈. 이제 출발 의문으로 돌아갈 차례다.
    왜 문제마다 분류기가 달라야 했나?
  </div>
</section>

<!-- ===================== CH 09 ===================== -->
<section id="ch9">
  <h2 class="chap"><span class="num">CH 09</span>정리 — 데이터 성격에 따라 분류기를 고른다<a href="#ch9" class="anchor-link">#</a></h2>

  <h3 class="step">최종 결론 — 출발 의문 회수</h3>
  <p>CH 01의 의문 "왜 문제마다 분류기가 다른가"의 답은, 세 과제를 직접 확인해 보니 분명했다 —
  분류기는 데이터의 성격이 부르고, 각 분류기는 그 성격에 맞는 손잡이와 전제를 갖는다.</p>

  <table>
    <tr><th>과제</th><th>데이터 성격</th><th>분류기</th><th>핵심 손잡이 / 전제</th><th>실측</th></tr>
    <tr><td>글자(A~Z)</td><td>16정수 특성·26클래스·비선형 경계</td><td><strong>SVM</strong>(RBF)</td><td>표준화 전제 · 커널/γ</td><td class="hl">rbf 0.9007 (linear 0.8347)</td></tr>
    <tr><td>우편번호</td><td>주소↔코드 정확 매핑·라벨 충분</td><td>색인(룩업)</td><td>학습 불필요·즉시 조회</td><td>31,357코드 양방향</td></tr>
    <tr><td>유방암</td><td>30연속 특성·스케일 6800배차·이진</td><td><strong>KNN</strong></td><td>표준화 필수 · k 선택 · recall</td><td class="hl">k=3, 정확도 0.979·recall 0.981</td></tr>
    <tr><td>스팸/텍스트</td><td>단어 0/1·고차원 희소·이진</td><td><strong>나이브베이즈</strong></td><td>조건부독립 가정 · 라플라스 α</td><td class="hl">α=0.1 정확도 0.8796</td></tr>
  </table>

  <div class="keypoint">
    <span class="label">FINAL CONCLUSION</span>
    거리·경계 기반(SVM·KNN)은 <strong>표준화가 전제</strong>다 — 안 하면 큰 특성이 거리를 독점해 낮아진다(CH 02·05, 두 번 반복된 함정).
    SVM은 커널로 비선형 경계를 얻고(CH 03), KNN은 k로 복잡도를 조절하며(CH 06), 둘 다 곱셈이 아니라 기하로 분류한다.
    반면 나이브베이즈는 거리·경계 대신 <strong>확률의 곱</strong>으로 가르기에 고차원 희소 텍스트에 강하고(CH 07),
    조건부독립이라는 비현실적 가정의 구멍은 라플라스 스무딩이 메운다(CH 08). 성능은 회귀처럼 한 숫자가 아니라
    문제에 맞는 지표(암은 recall, 스팸은 정밀도/재현율)로 재야 한다.
  </div>

  <h3 class="step">한 문장으로</h3>
  <div class="keypoint">
    <span class="label">ONE-LINER</span>
    "어떤 분류기를 쓸까"는 모델이 아니라 <strong>데이터가 정한다</strong> —
    특성이 연속이고 스케일이 제각각이면 표준화 후 거리/경계(KNN·SVM),
    텍스트처럼 고차원 희소면 확률의 곱(나이브베이즈), 라벨이 정확히 떨어지면 색인.
  </div>

  <div class="ref-chain">
    <p class="ref-title">📚 전체 근거 출처</p>
    <ol>
      <li><strong>공식 문서</strong>
        <a href="https://scikit-learn.org/stable/modules/svm.html" target="_blank" rel="noopener">scikit-learn · SVM</a>,
        <a href="https://scikit-learn.org/stable/modules/neighbors.html#classification" target="_blank" rel="noopener">KNeighborsClassifier</a>,
        <a href="https://scikit-learn.org/stable/modules/naive_bayes.html" target="_blank" rel="noopener">Naive Bayes</a>,
        <a href="https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html" target="_blank" rel="noopener">StandardScaler</a>.</li>
      <li><strong>데이터셋</strong>
        <code>../ml_workspace/from_colab/0529-s/data/opt_letterdata.csv</code>(UCI Letter Recognition, 20000행),
        <code>wisc_data.csv</code>(Wisconsin 유방암, 569행),
        <code>content/data/국가데이터처_나라통계_우편번호_20211110.csv</code>(전국 우편번호, EUC-KR).</li>
      <li><strong>workspace 코드</strong>
        <code>0529-s/pytorch_svm_letter_classification*.ipynb</code>, <code>pytorch_knn_breast_cancer.ipynb</code>,
        <code>pytorch_naive_bayes_sms_spam.ipynb</code> : 과제 원본 흐름(스케일링·커널·스무딩).</li>
      <li><strong>강의자료</strong>
        <code>.study/pdf/머신러닝_서포트백터머신구조.pdf</code> (SVM 마진·초평면, KNN, 나이브베이즈 배경).</li>
      <li><strong>실행 검증</strong>
        <code>.study/test/ml_practice03/ml_practice03_runner.py §00~§07</code>
        → <code>logs/*.txt</code>, <code>charts/*.png</code> (고정 시드 42, 재현 가능).</li>
    </ol>
  </div>
</section>
</main>

<footer>
  <p>SK 네트웍스 AI Family 32기 · 교과목 2 단원 2 머신러닝 실습3(과제) (2026-05-29)</p>
  <p>모든 터미널 출력은 <code>.study/test/ml_practice03/ml_practice03_runner.py</code> 실제 실행 결과이며,
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
print(f"파일: {OUT}")
print(f"terminal div: {n_term} | terminal-body: {n_body} | (일치={n_term==n_body})")
print(f"외부 URL img: {len(http_imgs)} (0이어야 함) | base64 img: {b64_imgs}")
print(f"zero-width space: {zwsp} (0이어야 함)")
print(f"chap: {HTML.count('h2 class=\"chap\"')} | qbox: {HTML.count('class=\"qbox\"')} | keypoint: {HTML.count('class=\"keypoint\"')}")
print(f"미치환 placeholder: {leftover} | 크기: {len(HTML)//1024} KB")
