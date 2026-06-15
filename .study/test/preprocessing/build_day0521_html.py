# build_day0521_html.py
# day0521_data_preprocessing.html 조립 — logs/*.txt(실제 실행 결과) + charts/*.png(base64) 주입
# 실행: c:\_proj\python_workspace\.venv\Scripts\python.exe build_day0521_html.py
#   (= GUIDE §11 run_all 역할: 터미널 값 직접 작성 금지, 로그에서 주입)
#   문체: day0527_ml_intro.html 의 "의문→해결→예상 밖 결과→새 의문" 서사 추적 방식.
import base64, html, pathlib, re

HERE = pathlib.Path(__file__).parent
LOGS = HERE / "logs"
CHARTS = HERE / "charts"
OUT = HERE.parent.parent / "blog" / "day0521_data_preprocessing.html"   # .study/blog/
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
    "@@TERM_00@@": term("00_dtype_infer"),
    "@@TERM_01@@": term("01_unicode_trunc"),
    "@@TERM_02@@": term("02_nan_detect"),
    "@@TERM_03@@": term("03_impute_compare"),
    "@@TERM_04@@": term("04_astype"),
    "@@TERM_05@@": term("05_transform"),
    "@@CHART_IMPUTE@@": chart("ch_impute.png"),
    "@@CHART_LOG@@": chart("ch_logtransform.png"),
}

HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>파이썬 데이터 전처리 분석: dtype 추론 · 결측값 처리 · 변수 변환 — 모델에 넣기 전에</title>
  <meta name="description" content="SK 네트웍스 AI Family 32기 5주차 데이터 분석. 'ndarray는 왜 한 타입만 담나', '없는 값(NaN)은 어떻게 찾고 채우나', '평균으로 채우면 통계가 흔들리지 않나'라는 의문을 따라가며 numpy dtype 자동 추론·한글 U{n} 잘림·isna 탐지·dropna vs fillna(mean/median)·astype·log 변환을 실행으로 검증한 기록.">
  <meta property="og:title" content="파이썬 데이터 전처리 분석: dtype 추론 · 결측값 처리 · 변수 변환">
  <meta property="og:description" content="한글 U3 잘림('부산경남'→'부산경'), 평균 대치가 표준편차를 −10.5% 줄이는 함정, log 변환으로 왜도 4.79→0.39까지 실측으로 추적">
  <meta property="og:type" content="article">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="파이썬 데이터 전처리 분석: dtype 추론 · 결측값 처리 · 변수 변환">
  <meta name="twitter:description" content="dtype 추론 → 한글 U3 잘림 → NaN 탐지 → dropna vs fillna → astype → log 변환">
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
  <p class="eyebrow">Python · 5주차 · 교과목 2 단원 1 데이터 분석 · 부트캠프</p>
  <h1>데이터를 다듬다 — dtype·결측값·변수 변환, 모델에 넣기 전에</h1>
  <p class="deck">모델은 깨끗한 숫자만 먹는다. 그런데 현실 데이터는 타입이 제각각이고, 칸이 비어 있고(NaN), 분포가 한쪽으로 쏠려 있다.
  이 글은 <code>np.array([...])</code> 한 줄이 dtype 을 <strong>어떻게 혼자 정하는지</strong>를 묻는 데서 출발해 —
  한글이 조용히 잘리고, 비어 있는 값을 평균으로 채웠더니 분산이 줄어들고, 치우친 분포를 log 로 펴는 과정을 따라간 기록이다.
  모든 수치는 numpy·pandas 로 직접 돌린 결과이며 <code>seed=42</code>·seaborn titanic 으로 재현 가능하다.</p>
  <div class="meta-row">
    <span><strong>날짜</strong>2026-05-21</span>
    <span><strong>Python</strong>@@PY@@ · NumPy 2.4.4 · Pandas 3.0.2 · matplotlib 3.10.9</span>
    <span><strong>OS</strong>Windows 11 Pro 25H2</span>
    <span><strong>IDE</strong>VS Code 1.117.0</span>
    <span><strong>HW</strong>Asrock x600 · Ryzen 8600G · 24GB LPDDR5 · RTX 4070 Super 12GB</span>
    <span><strong>커리큘럼</strong>교과목 2 · 단원 1 · 데이터 분석 — 데이터전처리.pdf</span>
  </div>
</header>

<main>
<nav class="flow">
  <h2>이 글의 흐름 — 하나의 질문에서 갈라져 나온 질문들</h2>
  <ol>
    <li><a href="#ch1">시작 — <code>np.array([...])</code>는 dtype 을 혼자 어떻게 정하나 (업캐스팅)</a></li>
    <li><a href="#ch2">dtype 을 직접 줬더니 한글이 조용히 잘렸다 (U3 잘림)</a></li>
    <li><a href="#ch3">표로 넘어가며 — '값이 없음'(NaN)은 왜 <code>==</code> 로 못 찾나</a></li>
    <li><a href="#ch4">두 갈래 — 비운 자리를 버릴까(dropna) 채울까(fillna)</a></li>
    <li><a href="#ch5"><span class="turn">예상과 다른 결과</span> — 평균으로 채웠더니 분산이 줄어들었다</a></li>
    <li><a href="#ch6">타입 바꾸기 — <code>astype</code> 은 무엇을 버리고 무엇을 아끼나</a></li>
    <li><a href="#ch7">분포 바꾸기 — 한쪽으로 쏠린 꼬리를 log 로 펴다</a></li>
    <li><a href="#ch8">정리 — 전처리는 모델이 쓸 수 있게 다듬는 일</a></li>
  </ol>
</nav>

<!-- ===================== CH 01 ===================== -->
<section id="ch1">
  <h2 class="chap"><span class="num">CH 01</span>시작 — np.array는 dtype을 혼자 어떻게 정하나<a href="#ch1" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>NumPy 실습의 첫 줄은 늘 <code>np.array([1, 2, 3])</code> 같은 모양이었다. 그런데 파이썬 리스트와 달리
  ndarray 는 <strong>모든 원소가 같은 타입(dtype)</strong>이어야 한다. 리스트는 정수·실수·문자를 섞어 담아도 되는데, ndarray 는 왜 한 타입만 담을까?
  같은 타입이어야 원소 하나하나가 메모리에서 같은 크기를 차지하고, 그래야 C 수준의 빠른 벡터 연산이 가능하기 때문이다.</p>

  <blockquote class="cite">
    "A numpy array is a grid of values, all of the same type … The array can be initialized
    from a Python list; the dtype is inferred from the elements unless explicitly specified."
    <span class="src">— NumPy 공식 문서 · <a href="https://numpy.org/doc/stable/reference/arrays.dtypes.html" target="_blank" rel="noopener">Data type objects (dtype)</a></span>
  </blockquote>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    한 배열에 한 타입만 담아야 한다면, 타입이 다른 값을 섞어 넣을 때 NumPy 는 <strong>전부를 담을 수 있는 가장 넓은 타입 하나</strong>로 끌어올릴(업캐스팅) 것이다.
    그렇다면 ① 정수만이면 <code>int64</code>, ② 실수가 하나라도 섞이면 <code>float64</code>, ③ 문자가 섞이면 전부 문자열이 되어야 한다.
    <code>test_numpy/numpy_test7.py</code> 의 자동 추론 사례로 확인한다.
  </div>

  <pre><code class="language-python"># path : .study/test/preprocessing/preprocessing_runner.py §00 (발췌)
import numpy as np

print(np.array([1, 2, 3]).dtype)        # 정수만
print(np.array([1.0, 2.0, 3.0]).dtype)  # 실수만
print(np.array([1, 2, 3.0]).dtype)      # 정수+실수 → ?
print(np.array([1, 2, '3']).dtype)      # 숫자+문자 → ?</code></pre>

  <h3 class="step">테스트</h3>
  <div class="terminal">
    <div class="terminal-header">preprocessing_runner.py §00 · np.array dtype 자동 추론 — 업캐스팅 규칙 확인 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_00@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT — 가설 통과</span>
    가설대로다. 정수만 → <code>int64</code>, 실수 하나 섞임 → <code>float64</code>(업캐스팅), 문자 섞임 → 전부 문자열.
    특히 <code>[1, 2, '3']</code>이 <code>&lt;U21</code>(유니코드 문자열)이 된 게 인상적이다 — 숫자 2개가 문자 하나에 끌려가 전부 문자가 됐다.
    그리고 한번 정해진 dtype 은 고정이라, <code>int64</code> 배열에 <code>9.7</code>을 넣어도 소수점이 잘려 <code>9</code>로 저장된다.
  </div>

  <div class="bridge">
    <strong>여기서 한 가지가 걸렸다</strong> — 자동 추론이 이렇게 똑똑하다면, 반대로 내가 dtype 을 <em>직접</em> 정해 주면 더 안전하지 않을까?
    메모리를 아끼려고 <code>'U3'</code>(유니코드 3글자)처럼 칸 크기를 못 박아 보기로 했다. 그런데 그 선택이 함정이었다.
  </div>
</section>

<!-- ===================== CH 02 ===================== -->
<section id="ch2">
  <h2 class="chap"><span class="num">CH 02</span>dtype을 직접 주면 한글이 잘린다<a href="#ch2" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>dtype 문자열 <code>'U3'</code>은 "유니코드 3글자짜리 칸"을 뜻한다. 영어든 한글이든 NumPy 의 유니코드 문자열은
  <strong>글자 단위로 1칸</strong>을 쓴다(내부적으로는 글자당 4바이트인 UCS4). 그러니 <code>'U3'</code>은 3글자까지만 담는 칸이다.
  <code>test_numpy/numpy_test8.py</code> 에서 <code>'ABCDE'</code>가 <code>U4</code> 칸에서 잘리던 현상을 한글로 옮겨 확인한다.</p>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    <code>'부산경남'</code>은 4글자다. 이걸 <code>dtype='U3'</code> 배열에 넣으면 — 에러가 나거나, 아니면 <strong>네 번째 글자 '남'이 조용히 잘릴</strong> 것이다.
    만약 잘린다면 그건 에러보다 더 위험하다. 프로그램은 멀쩡히 돌고, 데이터만 틀려 있을 테니.
  </div>

  <h3 class="step">테스트</h3>
  <div class="terminal">
    <div class="terminal-header">preprocessing_runner.py §01 · np.array dtype='U3' — 한글 4번째 글자 잘림 확인 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_01@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">FAILURE → CLUE</span>
    예상이 맞았다. <code>'부산경남'</code>이 <code>U3</code> 칸에서 <code>'부산경'</code>으로 잘렸다 — <strong>에러 한 줄 없이</strong>.
    반대로 dtype 을 안 주면 NumPy 가 가장 긴 문자열('부산경남' 4글자)에 맞춰 <code>&lt;U4</code>로 자동 결정해 안전했다.
    "메모리를 아끼려고 칸을 못 박는" 최적화가 도리어 데이터 손실을 부른 것이다.
  </div>

  <div class="callout">
    <span class="label">함정</span>
    문자열 dtype 의 잘림은 <code>ValueError</code>를 내지 않는다. 한글·이름·주소처럼 길이가 가변인 텍스트 열은
    고정 <code>U{n}</code> 대신 dtype 을 추론에 맡기거나 pandas 의 <code>object</code>/<code>string</code> 타입으로 두는 편이 안전하다.
  </div>

  <div class="bridge">
    <strong>한 단계 올라간다</strong> — 여기까지는 한 종류의 값만 담는 ndarray 얘기였다.
    하지만 실제 분석 데이터는 열마다 타입이 다른 <em>표</em>(pandas DataFrame)다. 그리고 표에는 ndarray 엔 없던 새 문제가 있다 — 칸이 아예 비어 있는 것(NaN).
    잘림이 "값이 틀린" 문제였다면, 이제 "값이 없는" 문제를 마주한다.
  </div>
</section>

<!-- ===================== CH 03 ===================== -->
<section id="ch3">
  <h2 class="chap"><span class="num">CH 03</span>표로 넘어가며 — NaN은 왜 ==로 못 찾나<a href="#ch3" class="anchor-link">#</a></h2>

  <h3 class="step">학습</h3>
  <p>pandas 는 '값이 없음'을 <code>NaN</code>(Not a Number)으로 표시한다. 직관적으로는 <code>x == np.nan</code> 으로 찾으면 될 것 같다.
  그런데 NaN 에는 기묘한 규칙이 하나 있다 — <strong>NaN 은 자기 자신과도 같지 않다</strong>. IEEE 754 부동소수점 표준이 그렇게 정했다.</p>

  <blockquote class="cite">
    "Because NaN is not equal to any value, including itself, comparisons … always evaluate to False.
    Use <code>isna()</code> / <code>isnull()</code> to detect missing values."
    <span class="src">— pandas 공식 문서 · <a href="https://pandas.pydata.org/docs/user_guide/missing_data.html" target="_blank" rel="noopener">Working with missing data</a></span>
  </blockquote>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    <code>np.nan == np.nan</code> 이 <code>False</code> 라면, <code>==</code> 로는 결측을 절대 못 찾는다.
    대신 <code>isna()</code> 가 칸마다 True/False 를 돌려주고, <code>.sum()</code> 으로 합치면 열별 결측 개수가 나올 것이다.
    실데이터(seaborn titanic)에서 어느 열이 얼마나 비었는지 세어 본다.
  </div>

  <h3 class="step">테스트</h3>
  <div class="terminal">
    <div class="terminal-header">preprocessing_runner.py §02 · isna().sum() — titanic 열별 결측 탐지 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_02@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT</span>
    <code>np.nan == np.nan</code> 은 <code>False</code> — <code>==</code> 로는 못 찾는다. <code>isna().sum()</code> 으로 세니
    <code>deck</code> 688개, <code>age</code> 177개(전체 891행의 <strong>19.9%</strong>), <code>embarked</code> 2개가 비어 있었다.
    <code>age</code> 의 1/5 가 빈 칸이라니 — 이걸 그냥 두면 평균·모델 계산이 전부 NaN 으로 전염된다. 어떻게든 처리해야 한다.
  </div>

  <div class="bridge">
    <strong>그래서 선택의 갈림길이다</strong> — 빈 칸이 있는 행을 통째로 <em>버릴까</em>(dropna), 아니면 어떤 값으로 <em>채울까</em>(fillna)?
    버리면 데이터가 줄고, 채우면 없던 값을 지어낸다. 둘 중 무엇이, 언제 옳은가? 통계로 직접 비교해 본다.
  </div>
</section>

<!-- ===================== CH 04 ===================== -->
<section id="ch4">
  <h2 class="chap"><span class="num">CH 04</span>두 갈래 — 버릴까(dropna) 채울까(fillna)<a href="#ch4" class="anchor-link">#</a></h2>

  <h3 class="step">의문 → 비교</h3>
  <p>같은 <code>age</code> 열에 다섯 전략을 적용해 통계(개수·평균·표준편차·중앙값)를 한 줄씩 찍어 비교한다:
  ① 원본(NaN 포함), ② <code>dropna()</code>, ③ <code>fillna(mean)</code>, ④ <code>fillna(median)</code>, ⑤ <code>fillna(0)</code>.</p>
  <div class="qbox">
    <span class="label">기준</span>
    "좋은 처리"의 기준을 먼저 세운다 — 결측을 메우되 <strong>원래 분포를 최대한 덜 왜곡</strong>해야 한다.
    그렇다면 ⑤ <code>fillna(0)</code>는 나이에 0을 꽂으니 평균을 끌어내려 탈락일 것이고, ③ 평균 대치가 가장 무난할 거라 예상했다.
  </div>

  <pre><code class="language-python"># path : .study/test/preprocessing/preprocessing_runner.py §03 (발췌)
age = titanic['age']
age.dropna()                 # 빈 행을 버린다
age.fillna(age.mean())       # 평균으로 채운다
age.fillna(age.median())     # 중앙값으로 채운다
age.fillna(0)                # 0으로 채운다 (대조군)</code></pre>

  <h3 class="step">테스트</h3>
  <div class="terminal">
    <div class="terminal-header">preprocessing_runner.py §03 · dropna vs fillna(mean/median/0) — 통계 비교 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_03@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">관찰 결과</span>
    예상대로 <code>fillna(0)</code>는 평균을 29.70 → <strong>23.80</strong>으로 끌어내려 분포를 망쳤다(탈락).
    <code>dropna()</code>는 통계가 원본과 똑같지만(NaN 은 어차피 계산에서 빠지므로) 891행이 714행으로 줄었다.
    <code>fillna(mean)</code>은 평균을 <strong>29.6991 그대로</strong> 유지했다 — 평균값을 넣었으니 당연하다. 무난해 보인다.
  </div>

  <div class="bridge">
    <strong>그런데 표를 다시 보다 멈칫했다</strong> — <code>fillna(mean)</code>의 평균은 그대로인데,
    <em>표준편차</em>가 원본 14.5265 에서 13.0020 으로 줄어 있었다. 평균을 안 흔든다더니, 왜 흩어짐은 줄었지? 이게 다음 챕터의 의문이다.
  </div>
</section>

<!-- ===================== CH 05 ===================== -->
<section id="ch5">
  <h2 class="chap"><span class="num">CH 05</span>예상과 다른 결과 — 평균으로 채웠더니 분산이 줄었다<a href="#ch5" class="anchor-link">#</a></h2>

  <h3 class="step">답을 찾아서</h3>
  <p>평균 대치가 평균을 안 흔드는 건 당연하다 — 평균값 자체를 넣으니까. 그런데 표준편차(분산)가 줄어든 건 처음엔 직관에 어긋났다.
  이유는 이렇다: 표준편차는 "각 값이 평균에서 얼마나 흩어졌나"의 척도인데, 결측 177칸에 <strong>전부 평균값</strong>을 꽂으면
  그 177개는 평균과의 거리가 정확히 0 이다. 흩어짐 0 인 값을 잔뜩 더하니, 전체 흩어짐의 평균(분산)이 희석돼 줄어드는 것이다.</p>

  <div class="keypoint">
    <span class="label">의문 해소</span>
    원본 std 14.5265 → 평균 대치 후 13.0020, 약 <strong>−10.5%</strong>. 같은 값을 177번 꽂은 대가다.
    즉 평균 대치는 "중심(평균)은 보존하되 <strong>퍼짐(분산)은 인위적으로 축소</strong>한다." 분산을 과소평가하면
    이후 신뢰구간·상관·모델의 불확실성 추정이 전부 낙관적으로 치우친다. 무난해 보이던 선택에 숨은 비용이 있었던 것이다.
  </div>

  <figure class="shot">
    <img src="@@CHART_IMPUTE@@" alt="결측 대치 전/후 나이 분포 히스토그램 — 평균/중앙값 자리에 막대가 솟음">
    <figcaption>그림 0521-1 · 결측 대치 전/후 분포 — fillna(mean)·fillna(median) 모두 채운 값 자리(점선=평균)에 막대가 인위적으로 솟는다</figcaption>
  </figure>

  <p>중앙값 대치(<code>fillna(median)</code>)도 같은 방향이다 — 28.0 자리에 막대가 솟고 std 가 13.0197 로 줄었다.
  평균보다 이상치에 덜 휘둘린다는 장점은 있으나, "한 값을 반복해 꽂아 분산을 줄인다"는 구조적 한계는 똑같다.</p>

  <div class="bridge">
    <strong>결측은 일단락됐다</strong> — 이제 값은 다 채워졌다. 다음은 채워진 값들의 <em>타입</em>과 <em>모양</em>이다.
    실수로 들어온 요금을 정수로 바꾸거나, 문자 범주를 더 가벼운 타입으로 바꾸는 일 — <code>astype</code> 은 그 과정에서 무엇을 버리고 무엇을 아낄까?
  </div>
</section>

<!-- ===================== CH 06 ===================== -->
<section id="ch6">
  <h2 class="chap"><span class="num">CH 06</span>타입 바꾸기 — astype은 무엇을 버리고 아끼나<a href="#ch6" class="anchor-link">#</a></h2>

  <h3 class="step">학습 → 가설</h3>
  <p><code>astype</code> 은 열의 dtype 을 바꾼다. CH 01 에서 본 "<code>int64</code> 칸에 9.7 을 넣으면 9 로 잘린다"는 규칙이
  열 단위로 똑같이 적용될 것이다. 또 문자 범주열(<code>sex</code> 같은)을 <code>category</code> 타입으로 바꾸면 메모리를 크게 아낄 수 있다고 배웠다.</p>
  <div class="qbox">
    <span class="label">가설</span>
    ① <code>fare</code>(실수)를 <code>astype('int64')</code> 하면 소수점이 <strong>반올림이 아니라 버림</strong>으로 사라진다.
    ② <code>sex</code>(두 종류 문자열)를 <code>category</code> 로 바꾸면 같은 문자열을 코드로 압축해 메모리가 크게 준다.
  </div>

  <blockquote class="cite">
    "<code>astype</code> casts a pandas object to a specified dtype. Converting float to integer
    truncates toward zero. <code>category</code> dtype stores the data as integer codes plus a small
    set of categories, which can dramatically reduce memory for repeated string values."
    <span class="src">— pandas 공식 문서 · <a href="https://pandas.pydata.org/docs/user_guide/basics.html#object-conversion" target="_blank" rel="noopener">Basics — object conversion / dtypes</a></span>
  </blockquote>

  <h3 class="step">테스트</h3>
  <div class="terminal">
    <div class="terminal-header">preprocessing_runner.py §04 · astype(int64) 버림 · category 메모리 절약 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_04@@</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">가설 통과</span>
    <code>71.2833 → 71</code>, <code>7.925 → 7</code> — 반올림이면 8 이 됐을 값이 7 로 <strong>버려졌다</strong>(0 방향 절삭).
    그리고 <code>sex</code> 열은 <code>object</code> 11,452 bytes → <code>category</code> 1,050 bytes 로 <strong>90.8% 절약</strong>됐다.
    반복되는 문자열을 정수 코드 + 작은 범주표로 압축한 효과다. astype 은 "정밀도를 버려 무게를 아끼는" 거래다.
  </div>

  <div class="bridge">
    <strong>마지막 질문</strong> — 타입은 정리했다. 그런데 <code>fare</code> 분포 자체가 한쪽으로 심하게 쏠려 있었다(소수 부자가 평균을 끌어올림).
    이렇게 치우친(왜도 큰) 분포는 많은 모델이 싫어한다. 분포의 <em>모양</em>을 바꿀 방법은 없을까?
  </div>
</section>

<!-- ===================== CH 07 ===================== -->
<section id="ch7">
  <h2 class="chap"><span class="num">CH 07</span>분포 바꾸기 — 쏠린 꼬리를 log로 펴다<a href="#ch7" class="anchor-link">#</a></h2>

  <h3 class="step">학습 → 가설</h3>
  <p>오른쪽으로 긴 꼬리를 가진(양의 왜도) 분포는 <strong>로그 변환</strong>으로 대칭에 가깝게 펼 수 있다.
  큰 값일수록 log 가 더 세게 압축하기 때문이다. fare 에는 0 원 승객도 있으니 <code>np.log1p</code>(= log(1+x))를 써서 0 을 안전하게 처리한다.</p>
  <div class="qbox">
    <span class="label">가설</span>
    <code>fare</code> 는 소수 고가 티켓 때문에 왜도가 크다. <code>log1p</code> 변환 후 왜도가 <strong>0 에 가깝게(대칭) 줄어들</strong> 것이다.
    또 연속값인 <code>age</code> 를 <code>pd.cut</code> 으로 구간(범주)으로 묶으면 해석이 쉬워질 것이다.
  </div>

  <h3 class="step">테스트</h3>
  <div class="terminal">
    <div class="terminal-header">preprocessing_runner.py §05 · log1p 왜도 감소 · pd.cut 구간화 · Python @@PY@@ · PowerShell</div>
    <pre class="terminal-body">@@TERM_05@@</pre>
  </div>
  <figure class="shot">
    <img src="@@CHART_LOG@@" alt="log 변환 전/후 fare 분포 — 오른쪽 꼬리가 펴짐">
    <figcaption>그림 0521-2 · 변수 변환 전/후 — 왜도 4.79 의 쏠린 fare 가 log1p 후 0.39 로, 종 모양에 가깝게 펴진다</figcaption>
  </figure>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">가설 통과</span>
    <code>fare</code> 왜도가 <strong>4.7873 → 0.3949</strong>로 떨어졌다 — 오른쪽 꼬리가 펴져 거의 대칭이 됐다.
    그리고 <code>pd.cut</code> 은 연속된 나이를 5개 구간(어린이~노년)으로 묶어, 청소년(218명)·청년(196명)이 가장 많다는 걸 한눈에 보이게 했다.
    log 는 분포의 <em>모양</em>을, cut 은 변수의 <em>척도(연속→범주)</em>를 바꾼다.
  </div>

  <div class="bridge">
    <strong>이제 사슬이 닫힌다</strong> — 타입을 정하고(dtype), 빈 칸을 채우고(NaN), 타입을 바꾸고(astype), 분포를 펴기까지(log/cut).
    출발점이었던 "<code>np.array([...])</code>는 dtype 을 어떻게 정하나"의 의문이, 어느새 데이터 전처리 전체의 지도가 됐다.
  </div>
</section>

<!-- ===================== CH 08 ===================== -->
<section id="ch8">
  <h2 class="chap"><span class="num">CH 08</span>정리 — 전처리란 모델이 먹을 수 있게 다듬는 일<a href="#ch8" class="anchor-link">#</a></h2>

  <h3 class="step">최종 결론 — 출발 의문 회수</h3>
  <div class="keypoint">
    <span class="label">FINAL CONCLUSION</span>
    CH 01 의 질문 "<code>np.array([...])</code>는 dtype 을 혼자 어떻게 정하나"에서 출발해 도착한 곳:
    <strong>전처리란 타입·결측·분포라는 세 축에서 데이터를 모델이 먹을 수 있게 다듬는 일</strong>이다.
    타입은 자동 추론이 가장 안전하고(직접 <code>U3</code> 을 박으면 한글이 잘린다 — CH 02),
    결측은 버리거나 채우되 평균 대치는 분산을 −10.5% 줄이는 숨은 비용이 있으며(CH 04~05),
    <code>astype</code> 은 정밀도를 버려 메모리(−90.8%)를 아끼고(CH 06),
    <code>log</code>·<code>cut</code> 은 분포의 모양과 척도를 바꾼다(CH 07).
  </div>

  <h3 class="step">한 문장으로</h3>
  <div class="keypoint">
    <span class="label">ONE-LINER</span>
    "데이터를 넣으면 알아서 된다"는 없다 — <strong>모든 전처리는 무언가를 얻기 위해 무언가를 버리는 거래</strong>다.
    잘림은 글자를, 평균 대치는 분산을, astype 은 정밀도를, log 는 원래 척도를 버린다.
    전처리를 안다는 건 그 거래의 비용을 알고 고른다는 뜻이다.
  </div>

  <table>
    <thead><tr><th>전처리</th><th>도구</th><th>얻는 것</th><th>버리는 것(비용)</th></tr></thead>
    <tbody>
      <tr><td>dtype 고정</td><td><code>dtype='U3'</code></td><td>메모리 예측</td><td class="hl">긴 한글 잘림(데이터 손실)</td></tr>
      <tr><td>결측 채우기</td><td><code>fillna(mean)</code></td><td>행 수 보존</td><td class="hl">분산 축소(−10.5%)</td></tr>
      <tr><td>결측 버리기</td><td><code>dropna()</code></td><td>분포 왜곡 없음</td><td>표본 감소(891→714)</td></tr>
      <tr><td>타입 변환</td><td><code>astype('category')</code></td><td>메모리 −90.8%</td><td>(int 변환 시) 소수점 버림</td></tr>
      <tr><td>분포 변환</td><td><code>np.log1p</code></td><td>왜도 4.79→0.39</td><td>원래 척도 해석 어려움</td></tr>
    </tbody>
  </table>

  <div class="ref-chain">
    <p class="ref-title">📚 전체 근거 출처</p>
    <ol>
      <li><strong>공식 문서</strong>
        <a href="https://numpy.org/doc/stable/reference/arrays.dtypes.html" target="_blank" rel="noopener">NumPy · Data type objects(dtype)</a>(업캐스팅·U{n}),
        <a href="https://pandas.pydata.org/docs/user_guide/missing_data.html" target="_blank" rel="noopener">pandas · Working with missing data</a>(NaN·isna),
        <a href="https://pandas.pydata.org/docs/user_guide/basics.html#object-conversion" target="_blank" rel="noopener">pandas · dtypes/astype</a>.</li>
      <li><strong>workspace</strong>
        <code>test_numpy/numpy_test7.py</code>·<code>numpy_test8.py</code>(dtype 추론·U{n} 잘림),
        <code>test_pandas/pandas_test5.py</code>(count/NaN·pd.cut).</li>
      <li><strong>강의자료</strong>
        <code>.study/pdf/데이터전처리.pdf</code> (배경지식).</li>
      <li><strong>실행 검증</strong>
        <code>.study/test/preprocessing/preprocessing_runner.py §00~§05</code>
        → <code>logs/*.txt</code>, <code>charts/*.png</code> (seed 42 · seaborn titanic, 재현 가능).</li>
    </ol>
  </div>
</section>
</main>

<footer>
  <p>SK 네트웍스 AI Family 32기 · 교과목 2 단원 1 데이터 분석 — 데이터 전처리 (2026-05-21)</p>
  <p>모든 터미널 출력은 <code>.study/test/preprocessing/preprocessing_runner.py</code> 실제 실행 결과이며,
  <code>seed=42</code>·seaborn titanic 으로 재현 가능하다. 차트는 base64 인라인으로 삽입했다.</p>
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
notes_leak = re.findall(r'\.study[/\\]notes', HTML)
figure_shot_unfilled = re.findall(r'figure\.shot', HTML)
print(f"파일: {OUT}")
print(f"terminal div: {n_term} | terminal-body: {n_body} | (일치={n_term==n_body})")
print(f"외부 URL img: {len(http_imgs)} (0이어야 함) | base64 img: {b64_imgs}")
print(f"zero-width space: {zwsp} (0이어야 함)")
print(f"chap: {HTML.count('h2 class=\"chap\"')} | qbox: {HTML.count('class=\"qbox\"')} | keypoint: {HTML.count('class=\"keypoint\"')}")
print(f".study/notes 누출: {len(notes_leak)} (0이어야 함)")
print(f"미치환 placeholder: {leftover} | 크기: {len(HTML)//1024} KB")
