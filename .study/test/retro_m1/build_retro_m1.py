# build_retro_m1.py — 04~05월 월간 회고(retrospective_m1) 조립
# 실행: c:\_proj\python_workspace\.venv\Scripts\python.exe .study\test\retro_m1\build_retro_m1.py
# - day0527_ml_intro.html 의 <style> 블록을 그대로 재사용(동일 디자인 보장)
# - 로드맵 다이어그램(roadmap_0405.png)을 base64 인라인 삽입(§26)
# - 회고 서사(§19): 한 달 목표 → 단원별 배움·시행착오 → 종합 회수.  실측 수치는 검증된 글에서 인용.
import base64, io, re, pathlib

ROOT = pathlib.Path(r"c:\_proj\python_workspace")
STYLE_SRC = ROOT / ".study" / "blog" / "day0527_ml_intro.html"
DIAGRAM = ROOT / ".study" / "reports" / "assets" / "roadmap_0405.png"
OUT = ROOT / ".study" / "blog" / "retrospective_m1.html"

style = re.search(r"<style>.*?</style>", STYLE_SRC.read_text(encoding="utf-8"), re.S).group(0)
roadmap_b64 = "data:image/png;base64," + base64.b64encode(DIAGRAM.read_bytes()).decode()

HTML = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>한 달의 학습 여정 — 04~05월 종합 회고 (Python에서 머신러닝까지)</title>
  <meta name="description" content="SK 네트웍스 AI Family 32기 부트캠프 04~05월 월간 회고. Python 기초·OOP·실행모델, MySQL·B+Tree, 웹 크롤링, 팀 프로젝트, 데이터 분석(numpy·pandas·시각화), 머신러닝 입문(회귀·과대적합·규제·SVM)까지 한 달의 학습을 하나의 흐름으로 회수한다.">
  <meta property="og:title" content="한 달의 학습 여정 — 04~05월 종합 회고">
  <meta property="og:description" content="Python→DB→크롤링→팀플→데이터분석→머신러닝, 한 달의 학습을 한 흐름으로">
  <meta property="og:type" content="article">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="한 달의 학습 여정 — 04~05월 종합 회고">
  <meta name="twitter:description" content="Python에서 머신러닝까지, 한 달 학습 회고">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Nanum+Gothic+Coding:wght@400;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
  {style}
</head>
<body>
<div class="page">

<header class="cover">
  <p class="eyebrow">Python · 04~05월 종합 회고(Monthly) · 부트캠프</p>
  <h1>한 달의 학습 여정 — Python에서 머신러닝까지</h1>
  <p class="deck">SK 네트웍스 AI Family 32기 부트캠프의 첫 한 달(04월 말~05월) 회고다.
  주차 회고가 '그 주에 무엇을 했나'라면, 이 글은 한 달 전체를 관통하는 한 줄 질문 —
  <strong>"Python 기초에서 머신러닝까지, 한 달 안에 데이터 문제를 푸는 전 과정을 한 바퀴 돌 수 있을까?"</strong> — 을 놓고,
  흩어져 보이던 매주의 단원이 실은 하나의 흐름이었음을 회수한다.
  Python 기초에서 시작해 DB·크롤링·팀 프로젝트를 거쳐 데이터 분석과 머신러닝 입문까지,
  교과목1 전 과정과 교과목2의 시작을 하나의 흐름으로 잇는다.</p>
  <div class="meta-row">
    <span><strong>기간</strong>2026-04월 말 ~ 05-29</span>
    <span><strong>범위</strong>교과목1 전 과정 + 교과목2 단원1·2 시작</span>
    <span><strong>OS</strong>Windows 11 Pro 25H2</span>
    <span><strong>HW</strong>Asrock x600 · Ryzen 8600G · 24GB LPDDR5 · RTX 4070 Super 12GB</span>
    <span><strong>근거</strong>주차/일자 블로그 글 + 실습 기록(실측 재현)</span>
  </div>
</header>

<main>
<nav class="flow">
  <h2>이 글의 흐름 — 한 달을 한 줄 목표로 묶다</h2>
  <ol>
    <li><a href="#ch0">도입 — 한 달의 목표와 학습 로드맵</a></li>
    <li><a href="#ch1">1주차 · 생각을 코드로 — Python 기초·OOP, "한 줄씩 실행"이 맞는가</a></li>
    <li><a href="#ch2">3주차 · 데이터를 저장·질의하다 — MySQL과 인덱스가 빠른 이유</a></li>
    <li><a href="#ch3">3~4주차 · 데이터를 모으다 — 정적·동적 크롤링</a></li>
    <li><a href="#ch4">4주차 · 처음으로 팀으로 만들다 — 단위 프로젝트</a></li>
    <li><a href="#ch5">5주차 · 데이터를 읽다 — numpy·pandas·전처리·시각화</a></li>
    <li><a href="#ch6">6주차 · 데이터로 예측하다 — 머신러닝 입문</a></li>
    <li><a href="#ch7">종합 회고 — 한 달 전 못 하던 것 / 지금 하는 것 / 다음</a></li>
  </ol>
</nav>

<div class="bridge">
  <strong>도입</strong> — 한 달의 커리큘럼은 도구(Python)에서 시작해 예측(머신러닝)으로 끝났다.
  매주 다른 단원을 달리다 보면 조각조각 흩어져 보이지만, 한 달이 지나 되짚으니
  각 단원이 다음 단원의 재료가 되는 하나의 흐름이었다. 먼저 한 달의 전체 지도를 펼쳐 놓고 시작한다.
</div>

<section id="ch0">
  <h2 class="chap"><span class="num">MAP</span>한 달의 학습 로드맵<a href="#ch0" class="anchor-link">#</a></h2>
  <p>한 달은 크게 두 교과목으로 나뉜다. <strong>교과목1(프로그래밍·데이터 기초)</strong>에서
  Python → DB → 크롤링 → 팀 프로젝트를 4주에 걸쳐 끝냈고,
  <strong>교과목2(데이터분석·머신러닝)</strong>에서 데이터 분석을 거쳐 머신러닝에 막 들어섰다.</p>
  <figure class="shot">
    <img src="{roadmap_b64}" alt="04~05월 학습 로드맵 — 교과목1 전 과정 + 교과목2 시작">
    <figcaption>그림 M1-1 · 6주차 학습 로드맵 — 교과목별 트랙(파랑=프로그래밍 기초, 초록=데이터분석·ML, 주황=팀 프로젝트)</figcaption>
  </figure>
  <div class="keypoint">
    <span class="label">한 줄 지도</span>
    "도구를 배운다(Python) → 데이터를 다룬다(DB·크롤링) → 함께 만든다(팀플) →
    데이터를 읽는다(분석) → 데이터로 예측한다(ML)." 각 단계가 다음 단계의 재료가 됐다.
  </div>
</section>

<section id="ch1">
  <h2 class="chap"><span class="num">W1·2</span>생각을 코드로 — Python 기초·OOP<a href="#ch1" class="anchor-link">#</a></h2>
  <h3 class="step">그 주의 목표</h3>
  <p>"문법을 외우는" 게 아니라 "왜 이렇게 동작하는가"를 묻기로 했다. 자료형·제어문·컬렉션에서
  시작해 객체지향과 모듈까지 갔고, 마지막엔 streamlit 로그인 앱을 직접 만들었다.</p>
  <h3 class="step">가장 컸던 의문 두 개</h3>
  <p>① <strong>"dict 는 어떻게 한 번에 값을 찾나?"</strong> — 해시 테이블과 O(1) 조회를 CPython 수준까지 파고들었다
  (<a href="day0527_ml_intro.html">dict 분석 글</a> 계열). ② <strong>"파이썬은 정말 한 줄씩 실행되나?"</strong> —
  디버거·dis·HEX로 검증하니 답은 "블록을 바이트코드로 컴파일하고 PVM이 명령어 단위로 실행"이었다.
  교과서의 한 문장("인터프리터=한 줄씩")이 어디서 깨지는지를 처음으로 내 손으로 확인한 경험이다.</p>
  <div class="keypoint">
    <span class="label">배운 점</span>
    문법보다 <strong>"동작의 근거를 공식 문서·소스로 추적하는 습관"</strong>이 이 주의 진짜 수확이었다.
    이 습관이 이후 모든 글의 뼈대(의문→가설→검증→결론)가 됐다.
  </div>
  <div class="bridge"><strong>다음으로</strong> — 코드로 데이터를 다루게 되니, 데이터를 '어디에 어떻게 저장·질의하나'가 다음 질문이 됐다.</div>
</section>

<section id="ch2">
  <h2 class="chap"><span class="num">W3</span>데이터를 저장·질의하다 — MySQL<a href="#ch2" class="anchor-link">#</a></h2>
  <h3 class="step">그 주의 목표 · 의문</h3>
  <p>SELECT·DML·DDL·조인·서브쿼리로 데이터를 질의하는 법을 익혔다. 가장 인상 깊었던 의문은
  <strong>"인덱스는 왜 빠른가?"</strong> — 답을 찾다 <strong>B+Tree</strong> 구조(균형 트리·리프 연결 리스트·범위 검색)까지 들어갔다
  (<a href="day0521_data_preprocessing.html">일자별 글 계열</a>의 0511~0513 MySQL 편).</p>
  <div class="keypoint">
    <span class="label">배운 점</span>
    "빠르다"는 막연한 말 뒤에 <strong>자료구조(B+Tree)</strong>가 있다는 것. 제약조건·트랜잭션(TCL)으로
    데이터 무결성을 지키는 감각도 이때 잡혔다.
  </div>
  <div class="bridge"><strong>다음으로</strong> — 저장된 데이터를 질의하는 법을 알았으니, '바깥의 데이터를 직접 모으는' 크롤링으로.</div>
</section>

<section id="ch3">
  <h2 class="chap"><span class="num">W3·4</span>데이터를 모으다 — 웹 크롤링<a href="#ch3" class="anchor-link">#</a></h2>
  <h3 class="step">학습 · 시행착오</h3>
  <p>정적 크롤링(requests·BeautifulSoup)과 동적 크롤링(Selenium/Playwright·선택자)을 나눠 배웠다.
  핵심 의문은 <strong>"정적으로 안 긁히는 페이지는 왜 그런가?"</strong> — JS로 나중에 그려지는 DOM은
  HTML 응답에 없으니, 브라우저를 띄워 렌더링 후 긁어야 한다는 것을 직접 부딪쳐 알았다.</p>
  <div class="keypoint">
    <span class="label">배운 점</span>
    "데이터가 어디에, 언제 존재하는가"(응답 시점 vs 렌더 시점)를 구분하는 눈. 이게 다음 주 팀 프로젝트의 수집 단계로 바로 이어졌다.
  </div>
  <div class="bridge"><strong>다음으로</strong> — 혼자 도구를 익혔으니, 이제 '팀으로 하나의 결과물'을 만들 차례였다.</div>
</section>

<section id="ch4">
  <h2 class="chap"><span class="num">W4</span>처음으로 팀으로 만들다 — 단위 프로젝트<a href="#ch4" class="anchor-link">#</a></h2>
  <h3 class="step">프로젝트 · 시행착오</h3>
  <p>교과목1 단위 프로젝트로 팀 "물로간다"(SKN32-1st-3Team)를 진행했다 — 데이터 수집 → ERD 설계 →
  웹앱 구현 → 테스트 → 발표. SQLAlchemy·Altair·Playwright를 실제 협업 코드에서 처음 써봤고,
  스키마 설계와 PK 책임 분리 같은 '혼자 할 땐 안 보이던' 문제를 만났다.</p>
  <div class="keypoint">
    <span class="label">배운 점</span>
    개념(DB·크롤링)이 <strong>하나의 동작하는 제품</strong>으로 합쳐질 때 생기는 간극 — 설계·역할 분담·통합 —
    을 처음 체감했다. 기술보다 "연결"이 어렵다는 것.
  </div>
  <div class="bridge"><strong>다음으로</strong> — 데이터를 모으고 저장했으니, 이제 그 데이터를 '읽고 이해하는' 분석으로 넘어갔다(교과목2).</div>
</section>

<section id="ch5">
  <h2 class="chap"><span class="num">W5</span>데이터를 읽다 — 데이터 분석<a href="#ch5" class="anchor-link">#</a></h2>
  <h3 class="step">학습 흐름</h3>
  <p>numpy(벡터화·dtype·shape) → pandas 전처리(결측값·변수 변환) → 이상치(IQR)·정규화(MinMax/Standard) →
  시각화(matplotlib·seaborn)로 이어졌다. 자세한 회수는 <a href="retrospective_w5.html">5주차 회고</a>에 정리했다.</p>
  <h3 class="step">기억에 남는 실측</h3>
  <div class="keypoint">
    <span class="label">관찰</span>
    auto-mpg에서 mpg–weight 상관 <strong>−0.832</strong>(무거울수록 연비↓), IQR로 이상치를 가르면
    (Q1=75·Q3=126·IQR=51) 같은 데이터에서 IQR 10개 vs Z-score 5개로 <strong>기준에 따라 이상치 개수가 달라진다</strong>는 것.
    "전처리는 모델 전의 잡일"이 아니라 <strong>결과를 좌우하는 선택</strong>임을 데이터로 봤다.
  </div>
  <div class="bridge"><strong>다음으로</strong> — 데이터를 읽을 수 있게 되니, 마지막 질문이 남았다: 이 데이터로 '예측'할 수 있는가?</div>
</section>

<section id="ch6">
  <h2 class="chap"><span class="num">W6</span>데이터로 예측하다 — 머신러닝 입문<a href="#ch6" class="anchor-link">#</a></h2>
  <h3 class="step">한 줄 의문에서 시작한 6주차</h3>
  <p>"<code>model.fit(X, y)</code>는 무엇을 정하나?"에서 출발해 회귀·분류·SVM까지 사흘을 달렸다
  (<a href="day0527_ml_intro.html">Day1 회귀</a> · <a href="day0528_classification_logistic.html">Day2 분류·로지스틱</a> ·
  <a href="day0529_svm.html">Day3 SVM</a>, 실습 <a href="ml_practice01_subway.html">지하철</a>·<a href="ml_practice02_titanic.html">타이타닉</a>·<a href="ml_practice03_svm_knn_nb.html">SVM·KNN·NB</a>).</p>
  <h3 class="step">가장 크게 깨진 직관</h3>
  <div class="callout">
    <span class="label">반전</span>
    "모델을 더 복잡하게 만들면 더 좋아진다"는 직관이 맞지 않았다. 다항 차수를 9로 올리자
    train R2는 올랐지만 <strong>test R2가 −1132</strong>로 하락(과대적합). 지하철 실습에서도 강한 모델(RandomForest)이
    오히려 R2를 떨어뜨리고 단순 One-Hot 선형회귀가 <strong>R2 0.855</strong>로 더 나았다. "복잡함 ≠ 좋음"을 몸으로 배웠다.
  </div>
  <div class="keypoint">
    <span class="label">배운 점</span>
    머신러닝의 절반은 모델이 아니라 <strong>데이터 관리(표준화·train_test_split)와 일반화(규제)</strong>에 있다.
    Ridge로 계수를 누르자(13196→50) test R2가 −1132에서 +0.34로 회복됐다.
    평가도 한 숫자에 속으면 안 된다 — 정확도 0.988에도 악성 1건을 놓쳤고(재현율이 그걸 잡았다),
    SVM은 circles 데이터에서 선형 0.42 vs RBF 1.0으로 <strong>문제에 맞는 도구</strong>의 중요성을 보여줬다.
  </div>
  <div class="bridge"><strong>그래서</strong> — 한 달 전의 질문으로 돌아갈 때가 됐다.</div>
</section>

<section id="ch7">
  <h2 class="chap"><span class="num">FIN</span>종합 회고 — 출발 목표 회수<a href="#ch7" class="anchor-link">#</a></h2>
  <h3 class="step">영역별로 한 달을 한 줄로</h3>
  <table>
    <tr><th>영역</th><th>핵심 학습</th><th>대표 실측·결과</th></tr>
    <tr><td>Python</td><td>OOP·모듈·실행 모델</td><td>"한 줄씩 실행"은 비유 — 블록 컴파일→PVM</td></tr>
    <tr><td>데이터 저장</td><td>SQL 질의 + 인덱스 원리</td><td>B+Tree로 범위 검색이 빠른 이유</td></tr>
    <tr><td>데이터 수집</td><td>정적·동적 크롤링</td><td>응답 시점 vs 렌더 시점 구분</td></tr>
    <tr><td>협업</td><td>단위 프로젝트 완주</td><td>수집→ERD→웹앱→발표 통합</td></tr>
    <tr class="hl"><td>데이터 분석</td><td>전처리·이상치·시각화</td><td>corr −0.832, IQR vs Z-score 이상치 개수 차이</td></tr>
    <tr class="hl"><td>예측(ML)</td><td>fit·과대적합·규제·평가</td><td>test R2 −1132→+0.34(Ridge), 정확도 0.988 뒤 누락</td></tr>
  </table>
  <div class="keypoint">
    <span class="label">FINAL — 출발 의문 회수</span>
    "Python 기초에서 머신러닝까지, 한 달 안에 데이터 문제를 푸는 전 과정을 한 바퀴 돌 수 있을까?" —
    <strong>데이터를 모으고(크롤링) · 저장·질의하고(SQL) · 읽고(분석) · 예측하고(ML) · 그 결과를 의심하는(평가)</strong>
    한 바퀴를 단원별 실측으로 직접 돌았다. 무엇보다 "왜 이렇게 동작하나"를 공식 문서와 실행으로 검증하는
    습관이 이 한 달을 하나의 흐름으로 꿰는 축이었다.
  <h3 class="step">다음 달 과제</h3>
  <p>머신러닝 Day4~7(결정트리·앙상블·차원축소·비지도학습)을 마치고, 교과목3(LLM)·교과목4(앱 개발)로 들어간다.
  "예측"에서 "언어를 다루는 모델"과 "서비스로 배포"까지가 다음 한 달의 질문이 될 것이다.</p>

  <div class="ref-chain">
    <p class="ref-title">📚 이 회고가 종합한 글 (주차/일자 기록)</p>
    <ol>
      <li><strong>Python(1·2주차)</strong> dict·abstraction·interpreter, retrospective_w1w2</li>
      <li><strong>MySQL(3주차)</strong> day0511~day0513, retrospective_w3</li>
      <li><strong>크롤링(3·4주차)</strong> day0514·day0515</li>
      <li><strong>팀 프로젝트(4주차)</strong> day0516_0519_team_project, retrospective_w4</li>
      <li><strong>데이터 분석(5주차)</strong> day0520~day0526, <a href="retrospective_w5.html">retrospective_w5</a></li>
      <li><strong>머신러닝(6주차)</strong> day0527·day0528·day0529 + 실습1~3(지하철·타이타닉·SVM/KNN/NB)</li>
      <li><strong>학습 로드맵</strong> <code>.study/reports/retrospective_0405_plan_20260603.txt</code> · 다이어그램 roadmap_0405.png</li>
    </ol>
  </div>
</section>
</main>

<footer>
  <p>SK 네트웍스 AI Family 32기 · 04~05월 종합 회고 (Monthly Retrospective M1)</p>
  <p>각 영역의 실측 수치(상관 −0.832, test R2 −1132→+0.34, 지하철 R2 0.855, SVM circles 0.42 vs 1.0 등)는
  해당 일자/실습 글의 실제 실행 결과를 인용한 것이다. 로드맵 다이어그램은 base64 인라인으로 삽입했다.</p>
</footer>

</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
</body>
</html>
"""

HTML = HTML.replace("​", "")
OUT.write_text(HTML, encoding="utf-8")

# 검증(§12)
import re as _re
ext = _re.findall(r'<img[^>]+src="https?://', HTML)
b64 = HTML.count('src="data:image/')
chap = HTML.count('h2 class="chap"')
print(f"파일: {OUT}")
print(f"chapters: {chap} | flow box: {'class=\"flow\"' in HTML} | base64 img: {b64} | 외부 URL img: {len(ext)}")
print(f"zero-width: {HTML.count(chr(0x200b))} | .study/notes leak: {'.study/notes' in HTML}")
print(f"size KB: {len(HTML)//1024}")
# 다이어그램 base64 유효성
m = _re.search(r'data:image/png;base64,([^\"]+)', HTML)
print("roadmap PNG valid:", base64.b64decode(m.group(1))[:8] == b'\x89PNG\r\n\x1a\n')
