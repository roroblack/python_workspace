"""MySQL 명령어 체계 정리 블로그 HTML 생성 스크립트"""
import base64
from pathlib import Path

# ── 이미지 base64 인코딩 ──
img_path = Path('.blog/img/Gemini_Generated_Image_jax5b9jax5b9jax5.png')
img_b64 = base64.b64encode(img_path.read_bytes()).decode()
img_src = f'data:image/png;base64,{img_b64}'

CSS = """
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic+Coding:wght@400;700&display=swap');
    :root {
      color-scheme: light;
      --ink: #1f2933;
      --muted: #667085;
      --line: #d7dee8;
      --paper: #ffffff;
      --surface: #ffffff;
      --accent:      #52A97E;
      --accent-2:    #E8875A;
      --accent-3:    #5B9BD5;
      --accent-4:    #9178C4;
      --accent-soft: #EBF7F1;
      --warn-soft:   #FFF1E8;
      --code-bg: #1e1e1e;
      --code-ink: #e5e7eb;
      --shadow: none;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--paper);
      color: var(--ink);
      font-family: "Nanum Gothic Coding", "Segoe UI", Arial, sans-serif;
      line-height: 1.78;
      font-size: 16px;
    }
    a { color: var(--accent-3); text-underline-offset: 3px; }
    .page { width: min(880px, calc(100% - 32px)); margin: 0 auto; }

    header.cover {
      background: #ffffff;
      border-bottom: 3px solid var(--ink);
      padding: 64px 0 40px;
    }
    .cover .eyebrow {
      border-top: 4px solid var(--accent);
      padding-top: 10px;
      display: inline-block;
      color: var(--accent);
      font-weight: 800;
      font-size: 0.78rem;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      margin: 0 0 14px;
    }
    .cover h1 { margin: 0; font-size: clamp(1.9rem, 4.2vw, 3.1rem); line-height: 1.18; letter-spacing: -0.01em; }
    .cover .deck { margin: 18px 0 0; color: var(--muted); font-size: 1.05rem; }
    .meta-row {
      display: flex; flex-wrap: wrap; gap: 18px 28px;
      margin-top: 30px; padding-top: 18px;
      border-top: 2px solid var(--ink);
      color: var(--muted); font-size: 0.92rem;
    }
    .meta-row strong { color: var(--ink); margin-right: 6px; }

    main { padding: 36px 0 60px; }
    h2.chap {
      border-top: 3px solid var(--ink);
      padding-top: 16px;
      margin: 56px 0 8px;
      font-size: 1.55rem;
      letter-spacing: -0.01em;
      line-height: 1.25;
    }
    h2.chap .num {
      display: inline-block;
      color: var(--accent);
      font-size: 0.85rem;
      font-weight: 800;
      letter-spacing: 0.12em;
      margin-right: 10px;
      padding: 2px 8px;
      border: 2px solid var(--accent);
      border-radius: 0;
      vertical-align: middle;
    }
    h3.step { margin: 26px 0 8px; font-size: 1.08rem; color: var(--ink); }
    h3.step::before {
      content: "";
      display: inline-block;
      width: 4px; height: 1.1em;
      background: var(--accent);
      margin-right: 8px;
      vertical-align: text-bottom;
    }
    p { margin: 0 0 12px; }
    ul, ol { padding-left: 22px; margin: 6px 0 14px; }
    li { margin-bottom: 6px; }

    code { font-family: "Cascadia Code","Consolas","D2Coding",monospace; font-size: 0.92em; }
    :not(pre) > code { background: #EEF0F6; border: 1px solid #d8e0ea; border-radius: 0; padding: 1px 6px; color: #1f2933; }
    pre {
      margin: 12px 0 18px; overflow-x: auto;
      background: var(--code-bg); color: var(--code-ink);
      border-radius: 0; padding: 18px 20px;
      font-size: 0.9rem; line-height: 1.6; tab-size: 4; box-shadow: none;
    }
    pre code.language-sql, pre code.language-python { background: transparent; border: none; padding: 0; color: inherit; font-size: 1em; }

    .anchor-link {
      display: inline-block; margin-left: 8px; color: var(--accent);
      text-decoration: none; opacity: 0; font-size: 0.75em;
      vertical-align: middle; font-weight: 400; transition: opacity 0.15s;
    }
    h2.chap:hover .anchor-link { opacity: 1; }

    .qbox, .keypoint, .callout {
      border-radius: 0; padding: 16px 18px; margin: 14px 0 18px;
      border: 1px solid var(--line); background: var(--surface);
    }
    .qbox { border-left: 4px solid var(--accent-3); background: #EBF4FF; }
    .qbox .label { display: block; color: var(--accent-3); font-weight: 800; font-size: 0.84rem; letter-spacing: 0.06em; margin-bottom: 4px; }
    .keypoint { border-left: 4px solid var(--accent); background: var(--accent-soft); }
    .keypoint .label { display: block; color: var(--accent); font-weight: 800; font-size: 0.84rem; letter-spacing: 0.06em; margin-bottom: 4px; }
    .callout { border-left: 4px solid var(--accent-2); background: var(--warn-soft); }
    .callout .label { display: block; color: var(--accent-2); font-weight: 800; font-size: 0.84rem; letter-spacing: 0.06em; margin-bottom: 4px; }

    table { width: 100%; border-collapse: collapse; margin: 12px 0 18px; background: var(--surface); border: 1px solid var(--line); font-size: 0.95rem; }
    th, td { text-align: left; vertical-align: top; padding: 10px 12px; border-bottom: 1px solid var(--line); }
    th { background: #EEF0F5; color: #1f2933; font-weight: 800; }

    .toc { background: var(--surface); border: 1px solid var(--line); border-top: 3px solid var(--ink); border-radius: 0; padding: 18px 22px; margin: 24px 0 0; }
    .toc h4 { margin: 0 0 8px; font-size: 0.9rem; letter-spacing: 0.08em; color: var(--muted); text-transform: uppercase; }
    .toc ol { margin: 0; padding-left: 20px; }
    .toc ol li { margin-bottom: 4px; }
    .toc a { color: var(--ink); text-decoration: none; }
    .toc a:hover { color: var(--accent-3); }

    blockquote.cite {
      border: 1px solid #d8d0f0; border-left: 4px solid var(--accent-4);
      background: #F7F5FD; padding: 12px 16px; margin: 12px 0;
      border-radius: 0; font-size: 0.95rem; line-height: 1.65;
    }
    blockquote.cite .src { display: block; color: var(--muted); font-size: 0.85em; margin-top: 8px; }

    .bridge {
      border-left: 4px solid var(--muted); background: #F4F6F8;
      padding: 12px 16px; margin: 18px 0 8px;
      font-size: 0.92rem; line-height: 1.65; color: #3a4250;
    }
    .bridge strong { color: var(--ink); }

    footer { border-top: 2px solid var(--ink); color: var(--muted); padding: 26px 0 40px; font-size: 0.9rem; }
    footer .refs { padding-left: 20px; margin: 8px 0 0; }
    footer .refs li { margin-bottom: 6px; }

    .day-badge {
      display: inline-block; background: var(--ink); color: #ffffff;
      font-size: 0.72rem; font-weight: 800; letter-spacing: 0.1em;
      padding: 2px 8px; margin-right: 8px; vertical-align: middle;
    }

    .terminal { margin: 14px 0 22px; border-radius: 0; overflow: hidden; border: 1px solid #30363d; font-family: "Cascadia Code","Consolas","D2Coding",monospace; }
    .terminal-header { background: #161b22; border-bottom: 1px solid #30363d; padding: 9px 16px; font-size: 0.8rem; color: #8b949e; display: flex; align-items: center; gap: 8px; }
    .terminal-header::before { content: 'mysql>'; color: #4ec9b0; font-weight: 700; font-size: 0.78rem; letter-spacing: 0.02em; flex-shrink: 0; }
    .terminal-header .t-label { flex: 1; color: #8b949e; }
    pre.terminal-body { background: #0d1117; color: #e6edf3; margin: 0; padding: 16px 20px; border-radius: 0; font-size: 0.86rem; line-height: 1.6; white-space: pre; overflow-x: auto; }
    .t-err { color: #f85149; }
    .t-ok  { color: #3fb950; }
    .t-hdr { color: #6e7681; }
    .t-sec { color: #58a6ff; }

    .infographic-wrap {
      margin: 20px 0 24px;
      border: 1px solid var(--line);
      background: var(--surface);
    }
    .infographic-wrap img {
      display: block;
      width: 100%;
      height: auto;
    }
    .infographic-cap {
      padding: 8px 12px;
      border-top: 1px solid var(--line);
      font-size: 0.85rem;
      color: var(--muted);
    }
"""

def html_doc(img_src: str) -> str:
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>MySQL 명령어 체계 정리 — DML · DDL · DCL · TCL 의 4분면</title>
  <meta name="description" content="MySQL 명령어를 DML·DDL·DCL·TCL 4분면으로 분류하고, SELECT 6절 파이프라인·제약조건·트랜잭션·권한까지 DAY1~DAY3 학습 내용을 한 파일에 통합 정리한다." />
  <meta property="og:title" content="MySQL 명령어 체계 정리 — DML · DDL · DCL · TCL 의 4분면" />
  <meta property="og:description" content="SELECT 6절 파이프라인·5대 제약조건·DCL/TCL 권한·트랜잭션까지 MySQL 전체 명령어 체계를 한 파일에 통합 정리." />
  <meta property="og:type" content="article" />
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:title" content="MySQL 명령어 체계 정리 — DML · DDL · DCL · TCL 의 4분면" />
  <meta name="twitter:description" content="MySQL 수백 가지 명령어를 4분면으로 나누면 각 분류의 책임과 트랜잭션 경계가 명확해진다." />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Nanum+Gothic+Coding:wght@400;700&display=swap" rel="stylesheet" />
  <style>{CSS}</style>
</head>
<body>

<header class="cover">
  <div class="page">
    <p class="eyebrow">MySQL · 3주차 · 통합 정리 · DAY1–DAY3</p>
    <h1>MySQL 명령어 체계 정리 — DML · DDL · DCL · TCL 의 4분면</h1>
    <p class="deck">
      DAY1(0511) 계정·스키마·자료형부터, DAY2(0512) 5대 제약조건, DAY3(0513) SELECT 6절 파이프라인까지 —
      학습한 모든 MySQL 명령어가 실제로 어떤 원칙으로 분류되는지, 인포그래픽 한 장에서 출발해
      각 분류의 책임·트랜잭션 경계·실행 예시로 사슬을 잇는다.
    </p>
    <div class="meta-row">
      <span><strong>작성일자</strong> 2026/05/25</span>
      <span><strong>과정</strong> SK Networks AI Family 32기 · MySQL DAY1~DAY3 통합</span>
      <span><strong>HW</strong> Asrock x600 · Ryzen 8600G · 24GB LPDDR5 · RTX 4070 Super 12GB</span>
      <span><strong>SW</strong> Windows 11 Pro 25H2 · MySQL 8.x · MySQL Workbench · PowerShell</span>
    </div>
    <nav class="toc">
      <h4>목차</h4>
      <ol>
        <li><a href="#ch1">MySQL 4분면 개요 — DML · DDL · DCL · TCL 의 분류 기준</a></li>
        <li><a href="#ch2">DML SELECT — 6절 실행 파이프라인과 함수</a></li>
        <li><a href="#ch3">DML 데이터 조작 — INSERT · UPDATE · DELETE · REPLACE</a></li>
        <li><a href="#ch4">DDL + 제약조건 — CREATE TABLE · ALTER · DROP · 5대 제약</a></li>
        <li><a href="#ch5">DCL + TCL — 권한(GRANT/REVOKE)과 트랜잭션(COMMIT/ROLLBACK)</a></li>
        <li><a href="#ch6">최종 정리 — 4분면 통합표와 결론</a></li>
      </ol>
    </nav>
  </div>
</header>

<main>
<div class="page">

<!-- ============================================================ 도입 다리 -->
<div class="bridge" style="margin-top:18px">
  <strong>이 노트가 추적하는 한 줄 의문</strong> —
  MySQL Workbench 를 처음 열면 수백 개의 명령어가 보인다.
  <code>SELECT</code> · <code>CREATE</code> · <code>GRANT</code> · <code>COMMIT</code> 은 전혀 다른 맥락에서 쓰이는데 —
  왜 SQL 은 이 명령어들을 하나의 언어로 묶어두었는가?
  CH01 에서 분류 기준을 세우고, CH02~CH05 에서 각 분면의 핵심을 추적한 뒤, CH06 에서 통합 회수한다.
</div>


<!-- ============================================================ CH01 -->
<section id="ch1">
  <h2 class="chap">
    <span class="num">CH 01</span>
    <span class="day-badge">개요</span>MySQL 4분면 — DML · DDL · DCL · TCL 의 분류 기준<a href="#ch1" class="anchor-link">#</a>
  </h2>

  <h3 class="step">학습 — 인포그래픽으로 보는 전체 지도</h3>
  <p>
    아래 인포그래픽은 MySQL 명령어를 4개의 서브언어로 분류한다.
    각 분면은 "무엇을 대상으로, 무슨 권한으로, 트랜잭션 안에 있는가" 를 기준으로 나뉜다.
  </p>
  <div class="infographic-wrap">
    <img src="{img_src}" alt="MySQL SQL Commands &amp; Functions — DML·DDL·DCL·TCL 4분면 인포그래픽" />
    <p class="infographic-cap">MySQL SQL Commands &amp; Functions 분류 인포그래픽 (Gemini Generated)</p>
  </div>

  <table>
    <thead>
      <tr>
        <th>분류</th><th>풀네임</th><th>대상</th><th>트랜잭션</th><th>대표 명령어</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>DML</strong></td>
        <td>Data Manipulation Language</td>
        <td>행(Row) 데이터</td>
        <td>ROLLBACK 가능</td>
        <td><code>SELECT · INSERT · UPDATE · DELETE · REPLACE</code></td>
      </tr>
      <tr>
        <td><strong>DDL</strong></td>
        <td>Data Definition Language</td>
        <td>구조(테이블·스키마)</td>
        <td>묵시적 COMMIT (롤백 불가)</td>
        <td><code>CREATE · ALTER · DROP · TRUNCATE · RENAME</code></td>
      </tr>
      <tr>
        <td><strong>DCL</strong></td>
        <td>Data Control Language</td>
        <td>사용자 권한</td>
        <td>묵시적 COMMIT</td>
        <td><code>GRANT · REVOKE</code></td>
      </tr>
      <tr>
        <td><strong>TCL</strong></td>
        <td>Transaction Control Language</td>
        <td>트랜잭션 경계</td>
        <td>트랜잭션 그 자체를 제어</td>
        <td><code>COMMIT · ROLLBACK · SAVEPOINT</code></td>
      </tr>
    </tbody>
  </table>

  <blockquote class="cite">
    SQL statements are divided into categories: DML statements affect data rows, DDL statements
    define or modify database objects and cause an implicit commit, DCL statements manage user privileges,
    and TCL statements control transaction boundaries.
    <span class="src">— <a href="https://dev.mysql.com/doc/refman/8.0/en/sql-statements.html" target="_blank" rel="noopener">MySQL Reference Manual § SQL Statements</a></span>
  </blockquote>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    4분면 분류는 단순한 그룹핑이 아니다 — 각 분면은 <strong>"명령 실행 후 취소할 수 있는가"</strong> 라는 트랜잭션 가역성으로
    정확히 갈라진다. DML 은 ROLLBACK 으로 되돌릴 수 있지만, DDL · DCL 은 묵시적 COMMIT 이 수반돼 되돌릴 수 없다.
    이 차이가 SQL 을 "신중하게 쓰는 언어" 로 만드는 핵심 설계다.
  </div>

  <h3 class="step">테스트 — DDL 의 묵시적 COMMIT 확인</h3>
  <div class="terminal">
    <div class="terminal-header"><span class="t-label">DDL 묵시적 COMMIT — ROLLBACK 으로 되돌릴 수 없음 확인</span></div>
    <pre class="terminal-body"><span class="t-hdr">-- DML은 ROLLBACK 가능</span>
START TRANSACTION;
INSERT INTO employee VALUES (999, '테스트');
ROLLBACK;
<span class="t-ok">-- 999번 행이 사라짐 (정상)</span>

<span class="t-hdr">-- DDL은 묵시적 COMMIT → ROLLBACK 불가</span>
START TRANSACTION;
INSERT INTO employee VALUES (999, '테스트');
<span class="t-err">CREATE TABLE test_ddl (id INT);</span>  <span class="t-hdr">-- ← 이 DDL이 묵시적 COMMIT 발동</span>
ROLLBACK;
<span class="t-hdr">-- 999번 행이 남아있음 — DDL이 앞선 DML까지 커밋시킴</span>
+-----+--------+
| id  | name   |
+-----+--------+
| 999 | 테스트 |   <span class="t-err">-- ROLLBACK 이 무효화됨</span>
+-----+--------+</pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT</span>
    4분면 분류의 핵심 기준은 <strong>트랜잭션 가역성</strong>이다.
    DML = 행 조작 · 가역, DDL = 구조 변경 · 불가역(묵시적 COMMIT), DCL = 권한 변경 · 불가역, TCL = 가역성 자체를 제어.
    명령어가 어느 분면인지 알면, "이 명령이 실수였을 때 되돌릴 수 있는가" 를 즉시 판단할 수 있다.
  </div>
  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 4분면 중 가장 복잡하고 자주 쓰이는 것이 DML 의 <code>SELECT</code> 다.
    6개 절로 이루어진 파이프라인의 실행 순서가 작성 순서와 다르다 — 그 이유를 CH02 에서 추적한다.
  </div>
</section>


<!-- ============================================================ CH02 -->
<section id="ch2">
  <h2 class="chap">
    <span class="num">CH 02</span>
    <span class="day-badge">DML</span>DML SELECT — 6절 실행 파이프라인과 함수<a href="#ch2" class="anchor-link">#</a>
  </h2>

  <h3 class="step">학습 — 6절의 실행 순서</h3>
  <table>
    <thead><tr><th>실행 순서</th><th>절</th><th>역할</th></tr></thead>
    <tbody>
      <tr><td>1</td><td><code>FROM</code> / <code>JOIN</code></td><td>대상 테이블(들)을 묶어 가상 테이블을 만든다</td></tr>
      <tr><td>2</td><td><code>WHERE</code></td><td>행 단위 필터링 (그룹 형성 전 — 별칭 사용 불가)</td></tr>
      <tr><td>3</td><td><code>GROUP BY</code></td><td>같은 키를 가진 행을 그룹으로 묶는다</td></tr>
      <tr><td>4</td><td><code>HAVING</code></td><td>그룹 단위 필터링 (그룹 형성 후)</td></tr>
      <tr><td>5</td><td><code>SELECT</code></td><td>꺼낼 컬럼·계산·별칭을 결정</td></tr>
      <tr><td>6</td><td><code>ORDER BY</code></td><td>최종 정렬 — 별칭·순번 모두 사용 가능</td></tr>
    </tbody>
  </table>
  <p>
    핵심 함수 4종류:
  </p>
  <table>
    <thead><tr><th>종류</th><th>대표 함수</th><th>용도</th></tr></thead>
    <tbody>
      <tr><td>집계</td><td><code>COUNT() · SUM() · AVG() · MAX() · MIN()</code></td><td>GROUP BY 와 함께 그룹 통계 계산</td></tr>
      <tr><td>문자열</td><td><code>CONCAT() · SUBSTR() · LENGTH() · TRIM()</code></td><td>문자열 조작·결합</td></tr>
      <tr><td>날짜</td><td><code>NOW() · DATEDIFF() · DATE_FORMAT()</code></td><td>날짜 연산·포맷</td></tr>
      <tr><td>윈도우</td><td><code>RANK() OVER() · ROW_NUMBER() OVER()</code></td><td>그룹을 유지하면서 행별 순위 계산</td></tr>
    </tbody>
  </table>

  <pre><code class="language-sql">-- ① 별칭은 ORDER BY(6단계)에서만 사용 가능, WHERE(2단계)에서는 불가
SELECT emp_id 사번, salary*12 연봉
FROM employee
ORDER BY 연봉 DESC;    -- ok

SELECT emp_id, salary*12 연봉
FROM employee
WHERE 연봉 > 50000000;  -- ERROR 1054: Unknown column '연봉' in 'where clause'

-- ② INNER JOIN — 매칭 안 되는 행은 제거됨
SELECT e.emp_id, e.emp_name, d.dept_name
FROM employee e
JOIN department d ON e.dept_id = d.dept_id;

-- ③ NULL 오염 방지 — IFNULL / COALESCE
SELECT emp_id, emp_name,
       (salary + salary * IFNULL(bonus_pct, 0)) * 12 AS "1년 연봉"
FROM employee;

SELECT emp_name, COALESCE(phone, email, '연락처 없음') AS 연락처
FROM employee;

-- ④ 집계 + GROUP BY + HAVING
SELECT dept_id, AVG(salary) AS 평균급여
FROM employee
GROUP BY dept_id
HAVING AVG(salary) > 4000000
ORDER BY 평균급여 DESC;</code></pre>

  <blockquote class="cite">
    The order in which clauses are processed by the database engine is different from the order in which
    they are written. Understanding the logical processing order is crucial for predicting query behavior,
    especially regarding the use of aliases.
    <span class="src">— <a href="https://dev.mysql.com/doc/refman/8.0/en/select.html" target="_blank" rel="noopener">MySQL Reference Manual § 13.2.13 SELECT Statement</a></span>
  </blockquote>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    WHERE 는 2단계, SELECT 는 5단계다 — 그렇다면 SELECT 절에서 정의한 별칭은 WHERE 에서 쓸 수 없어야 한다.
    반대로 ORDER BY 는 6단계이므로 별칭과 SELECT 절 순번을 모두 받아야 한다.
    JOIN 의 행 손실은 INNER JOIN 의 "매칭 미포함 정책" 에서 온다 — LEFT JOIN 으로 바꾸면 행이 살아나지만
    반대편 컬럼 자리에 NULL 이 들어온다.
  </div>

  <h3 class="step">테스트 — 별칭 규칙 · JOIN 행 손실 · IFNULL</h3>
  <div class="terminal">
    <div class="terminal-header"><span class="t-label">SELECT 6절 핵심 검증 — 별칭·JOIN 행 손실·IFNULL 복구</span></div>
    <pre class="terminal-body"><span class="t-hdr">-- WHERE 별칭 사용 시도</span>
<span class="t-err">ERROR 1054 (42S22): Unknown column '연봉' in 'where clause'</span>

<span class="t-hdr">-- INNER JOIN employee JOIN department</span>
+----------+          +----------+
| count(*) |          | count(*) |
+----------+          +----------+
|       22 |    →     |       19 |   <span class="t-hdr">-- NULL dept_id 3명 탈락</span>
+----------+          +----------+

<span class="t-hdr">-- IFNULL 미적용 vs 적용</span>
| 이미희  | 7000000 |  NULL | <span class="t-err">     NULL</span> |   <span class="t-hdr">← 미적용</span>
| 이미희  | 7000000 |  NULL | <span class="t-ok">84000000</span> |   <span class="t-hdr">← IFNULL(bonus_pct,0) 적용</span></pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT</span>
    SELECT 6절은 파이프라인이다. <strong>실행 순서가 WHERE → SELECT → ORDER BY</strong> 이기 때문에
    "WHERE 에서 별칭 사용 불가" 는 문법 제약이 아니라 파이프라인 순서의 논리적 결과다.
    JOIN 의 행 손실, NULL 의 산술 오염, IFNULL/COALESCE 의 필요성 — 이 세 가지가 한 파이프라인 안에서 이어진다.
  </div>
  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — SELECT 가 데이터를 "꺼내는" 도구라면,
    INSERT · UPDATE · DELETE · REPLACE 는 데이터를 "넣고 · 바꾸고 · 지우는" 도구다.
    이 셋 모두 ROLLBACK 가능한 DML 이지만 — 행 단위와 테이블 단위의 차이가 있다.
  </div>
</section>


<!-- ============================================================ CH03 -->
<section id="ch3">
  <h2 class="chap">
    <span class="num">CH 03</span>
    <span class="day-badge">DML</span>DML 데이터 조작 — INSERT · UPDATE · DELETE · REPLACE<a href="#ch3" class="anchor-link">#</a>
  </h2>

  <h3 class="step">학습 — 4가지 조작의 책임 분리</h3>
  <pre><code class="language-sql">-- INSERT: 새 행 추가
INSERT INTO employee (emp_id, emp_name, salary, dept_id)
VALUES (100, '홍길동', 5000000, '90');

-- 다중 INSERT (한 번에 여러 행)
INSERT INTO employee VALUES
  (101, '김유신', 4500000, '20'),
  (102, '이순신', 6000000, '90');

-- UPDATE: 기존 행 수정 (WHERE 필수 — 없으면 전체 갱신)
UPDATE employee
SET salary = salary * 1.1
WHERE dept_id = '90';

-- DELETE: 행 삭제 (ROLLBACK 가능, 구조 유지)
DELETE FROM employee
WHERE emp_id = 999;

-- REPLACE: INSERT + DELETE 의 조합(Upsert)
-- PK/UNIQUE 충돌 시 기존 행을 DELETE 하고 새 행을 INSERT
REPLACE INTO employee VALUES (100, '홍길동_수정', 5500000, '90');

-- TRUNCATE: DDL 분류 — 전체 행 삭제 + 구조 유지
-- ROLLBACK 불가, AUTO_INCREMENT 리셋
TRUNCATE TABLE temp_log;</code></pre>

  <blockquote class="cite">
    <code>REPLACE</code> works exactly like <code>INSERT</code>, except that if an old row in the table has
    the same value as a new row for a <code>PRIMARY KEY</code> or a <code>UNIQUE</code> index, the old row
    is deleted before the new row is inserted.
    <span class="src">— <a href="https://dev.mysql.com/doc/refman/8.0/en/replace.html" target="_blank" rel="noopener">MySQL Reference Manual § 13.2.12 REPLACE Statement</a></span>
  </blockquote>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    DELETE 와 TRUNCATE 는 둘 다 "행을 지운다" 지만 분류가 다르다(DML vs DDL) — 그 차이는
    <strong>트랜잭션 가역성</strong>에서 드러난다.
    DELETE 는 ROLLBACK 으로 복구 가능하고, TRUNCATE 는 묵시적 COMMIT 이므로 복구 불가다.
    UPDATE 에서 WHERE 를 빠뜨리면 전체 행이 갱신되므로 — "가장 위험한 한 줄" 은 <code>UPDATE 테이블 SET 컬럼=값;</code> 이다.
  </div>

  <h3 class="step">테스트 — DELETE(DML) vs TRUNCATE(DDL) 롤백 차이</h3>
  <div class="terminal">
    <div class="terminal-header"><span class="t-label">DELETE vs TRUNCATE — 트랜잭션 롤백 차이 확인</span></div>
    <pre class="terminal-body"><span class="t-hdr">-- DELETE는 ROLLBACK 가능</span>
START TRANSACTION;
DELETE FROM temp_log WHERE log_date &lt; '2026-01-01';
ROLLBACK;
SELECT COUNT(*) FROM temp_log;
<span class="t-ok">+----------+
| count(*) |
+----------+
|      150 |   ← 행이 복구됨
+----------+</span>

<span class="t-hdr">-- TRUNCATE는 DDL → 묵시적 COMMIT → ROLLBACK 불가</span>
START TRANSACTION;
TRUNCATE TABLE temp_log;   <span class="t-err">-- 여기서 묵시적 COMMIT</span>
ROLLBACK;
SELECT COUNT(*) FROM temp_log;
<span class="t-err">+----------+
| count(*) |
+----------+
|        0 |   ← 복구 안 됨
+----------+</span></pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT</span>
    DML 4종의 책임: INSERT = 추가, UPDATE = 수정, DELETE = 행 단위 삭제(가역),
    REPLACE = PK/UK 충돌 시 DELETE+INSERT 조합(Upsert).
    TRUNCATE 는 외형이 DELETE 와 비슷하지만 DDL 이므로 롤백 불가 — 분류 구분이 실무 안전의 핵심이다.
  </div>
  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 데이터를 넣고 꺼내는 도구를 다 봤다. 그런데 테이블 자체를 어떻게 정의하는가?
    DDL — CREATE TABLE · ALTER · DROP — 과, 그 위에 얹히는 5대 제약조건이 CH04 의 주제다.
  </div>
</section>


<!-- ============================================================ CH04 -->
<section id="ch4">
  <h2 class="chap">
    <span class="num">CH 04</span>
    <span class="day-badge">DDL</span>DDL + 제약조건 — CREATE TABLE · ALTER · DROP · 5대 제약<a href="#ch4" class="anchor-link">#</a>
  </h2>

  <h3 class="step">학습 — DDL 명령어 구조</h3>
  <pre><code class="language-sql">-- CREATE: 구조 생성
CREATE TABLE employee (
    emp_id    INT          PRIMARY KEY AUTO_INCREMENT,
    emp_name  VARCHAR(50)  NOT NULL,
    salary    INT          CHECK (salary > 0),
    dept_id   CHAR(2),
    CONSTRAINT fk_emp_dept FOREIGN KEY (dept_id)
        REFERENCES department(dept_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ALTER: 구조 변경 (컬럼 추가/수정/삭제, 제약 추가/삭제)
ALTER TABLE employee ADD COLUMN email VARCHAR(100);
ALTER TABLE employee MODIFY COLUMN emp_name VARCHAR(100) NOT NULL;
ALTER TABLE employee DROP COLUMN email;

-- DROP: 테이블/스키마 전체 제거 (복구 불가)
DROP TABLE IF EXISTS temp_log;
DROP DATABASE IF EXISTS test_db;</code></pre>

  <p>5대 제약조건 요약:</p>
  <table>
    <thead>
      <tr><th>제약</th><th>잘못된 행의 정의</th><th>대표 에러</th><th>레벨</th></tr>
    </thead>
    <tbody>
      <tr>
        <td><code>NOT NULL</code></td>
        <td>값이 비어있는 행</td>
        <td><code>ERROR 1048</code></td>
        <td>컬럼 레벨만</td>
      </tr>
      <tr>
        <td><code>UNIQUE</code></td>
        <td>단일/복합 키가 중복된 행</td>
        <td><code>ERROR 1062</code></td>
        <td>컬럼/테이블</td>
      </tr>
      <tr>
        <td><code>PRIMARY KEY</code></td>
        <td>식별자가 비었거나 중복된 행</td>
        <td><code>1062</code> / <code>1048</code></td>
        <td>한 테이블 1개 한정</td>
      </tr>
      <tr>
        <td><code>CHECK</code></td>
        <td>식이 FALSE 인 행 (결정론적 식만)</td>
        <td><code>ERROR 3819</code></td>
        <td>컬럼/테이블 (InnoDB)</td>
      </tr>
      <tr>
        <td><code>FOREIGN KEY</code></td>
        <td>부모가 제공하지 않는 값을 가진 행</td>
        <td><code>ERROR 1452</code></td>
        <td>테이블 권장 (InnoDB 필수)</td>
      </tr>
    </tbody>
  </table>

  <blockquote class="cite">
    DDL statements (<code>CREATE</code>, <code>ALTER</code>, <code>DROP</code>, <code>TRUNCATE</code>,
    <code>RENAME</code>) implicitly end any transaction that is currently active before they
    execute. They cannot be rolled back.
    <span class="src">— <a href="https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html" target="_blank" rel="noopener">MySQL Reference Manual § 13.3.3 Statements That Cause an Implicit Commit</a></span>
  </blockquote>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    5대 제약조건은 각각 서로 다른 종류의 "잘못된 행" 을 정의한다.
    NOT NULL = 값의 부재, UNIQUE = 중복, PRIMARY KEY = 식별 실패, CHECK = 도메인 위반, FOREIGN KEY = 참조 무결성 위반.
    이 5개를 모두 설계에 반영하면 "자료형이 통과시켜도 의미상 잘못된 행" 을 차단할 수 있다.
    단 — FK 는 <strong>InnoDB 엔진에서만 실제 작동</strong>하고, MyISAM 에서는 조용히 무시된다.
  </div>

  <h3 class="step">테스트 — 5대 제약 에러 코드 종합</h3>
  <div class="terminal">
    <div class="terminal-header"><span class="t-label">5대 제약 위반 에러 코드 — NOT NULL / UNIQUE / PK / CHECK / FK</span></div>
    <pre class="terminal-body"><span class="t-hdr">-- NOT NULL 위반</span>
<span class="t-err">ERROR 1048 (23000): Column 'emp_name' cannot be null</span>

<span class="t-hdr">-- UNIQUE 위반</span>
<span class="t-err">ERROR 1062 (23000): Duplicate entry '100' for key 'employee.PRIMARY'</span>

<span class="t-hdr">-- CHECK 위반 (salary > 0)</span>
<span class="t-err">ERROR 3819 (HY000): Check constraint 'employee_chk_1' is violated.</span>

<span class="t-hdr">-- FOREIGN KEY 위반 (부모 없는 dept_id)</span>
<span class="t-err">ERROR 1452 (23000): Cannot add or update a child row: a foreign key constraint fails
(`mydb`.`employee`, CONSTRAINT `fk_emp_dept` FOREIGN KEY (`dept_id`)
 REFERENCES `department` (`dept_id`))</span>

<span class="t-hdr">-- 다중 PK 정의 시도</span>
<span class="t-err">ERROR 1068 (42000): Multiple primary key defined</span></pre>
  </div>

  <div class="callout">
    <span class="label">CAUTION — FK 의 숨은 함정</span>
    <code>ENGINE=InnoDB</code> 를 명시하지 않으면 MyISAM 엔진이 사용될 수 있다.
    MyISAM 에서는 FK 정의가 문법 오류 없이 받아들여지지만 <strong>실제로 무시</strong>된다 —
    부모에 없는 값을 자식에 넣어도 에러가 발생하지 않는다.
    모든 CREATE TABLE 에 <code>ENGINE=InnoDB</code> 를 명시하는 것이 필수다.
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT</span>
    DDL 은 구조를 정의하고 제약은 그 구조 위에 "의미 규칙" 을 얹는다.
    자료형(DAY1)은 셀 단위 차단, 제약(DAY2)은 행 단위 차단 — 층층이 쌓인다.
    DROP 은 구조 전체를 날리므로 "가장 강한 DDL" 이고, TRUNCATE 는 구조를 남기고 모든 행만 지우므로 "가장 강한 DML 유사 DDL" 이다.
  </div>
  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 데이터와 구조를 다뤘다면 마지막으로 "누가 이 명령을 실행할 수 있는가" 와
    "어디까지를 한 작업 단위로 묶는가" — DCL 과 TCL 이 남았다.
  </div>
</section>


<!-- ============================================================ CH05 -->
<section id="ch5">
  <h2 class="chap">
    <span class="num">CH 05</span>
    <span class="day-badge">DCL·TCL</span>DCL + TCL — 권한(GRANT/REVOKE)과 트랜잭션(COMMIT/ROLLBACK)<a href="#ch5" class="anchor-link">#</a>
  </h2>

  <h3 class="step">학습 — DCL: 권한 제어</h3>
  <pre><code class="language-sql">-- GRANT: 권한 부여
-- 형식: GRANT 권한 ON 스키마.테이블 TO 사용자@호스트
GRANT SELECT, INSERT ON mydb.employee TO 'homework'@'localhost';
GRANT ALL PRIVILEGES ON mydb.* TO 'admin'@'%';

-- REVOKE: 권한 회수
REVOKE INSERT ON mydb.employee FROM 'homework'@'localhost';

-- 부여된 권한 확인
SHOW GRANTS FOR 'homework'@'localhost';

-- 권한 변경을 즉시 적용 (캐시 갱신)
FLUSH PRIVILEGES;</code></pre>

  <h3 class="step">학습 — TCL: 트랜잭션 제어</h3>
  <pre><code class="language-sql">-- 트랜잭션 시작
START TRANSACTION;    -- 또는 BEGIN;

-- 작업 수행
INSERT INTO orders VALUES (1001, '2026-05-25', 5000000);
UPDATE inventory SET stock = stock - 1 WHERE product_id = 'A100';

-- SAVEPOINT: 되돌릴 지점 지정
SAVEPOINT before_update;

UPDATE orders SET amount = 6000000 WHERE order_id = 1001;

-- SAVEPOINT 로 부분 롤백
ROLLBACK TO SAVEPOINT before_update;
-- 이 시점부터 before_update 이후의 UPDATE 만 취소됨

-- 전체 영구 저장
COMMIT;

-- 전체 취소
ROLLBACK;</code></pre>

  <blockquote class="cite">
    <code>GRANT</code> and <code>REVOKE</code> cause an implicit commit. Each <code>SAVEPOINT</code>
    sets a named point within a transaction. <code>ROLLBACK TO SAVEPOINT</code> rolls the transaction
    back to the named savepoint without terminating the transaction.
    <span class="src">— <a href="https://dev.mysql.com/doc/refman/8.0/en/savepoint.html" target="_blank" rel="noopener">MySQL Reference Manual § 13.3.4 SAVEPOINT, ROLLBACK TO SAVEPOINT, and RELEASE SAVEPOINT Statements</a></span>
  </blockquote>

  <h3 class="step">의문 → 가설</h3>
  <div class="qbox">
    <span class="label">가설</span>
    SAVEPOINT 는 트랜잭션을 "전체 or 전무(All-or-Nothing)" 가 아닌 <strong>"부분 롤백 가능"</strong> 으로 만든다.
    복잡한 배치 작업에서 오류 발생 시 처음부터 다시 하지 않고 안전 지점으로 되돌아갈 수 있다.
    DCL(GRANT/REVOKE) 는 묵시적 COMMIT 을 발동시키므로 — 트랜잭션 중간에 GRANT 를 실행하면
    앞선 DML 이 의도치 않게 커밋되어 버린다.
  </div>

  <h3 class="step">테스트 — SAVEPOINT 부분 롤백 / GRANT 묵시적 COMMIT</h3>
  <div class="terminal">
    <div class="terminal-header"><span class="t-label">SAVEPOINT ROLLBACK TO · GRANT 묵시적 COMMIT 확인</span></div>
    <pre class="terminal-body"><span class="t-hdr">-- SAVEPOINT 부분 롤백</span>
START TRANSACTION;
INSERT INTO orders VALUES (1001, '2026-05-25', 5000000);
SAVEPOINT sp1;
UPDATE orders SET amount = 9999999 WHERE order_id = 1001;
ROLLBACK TO SAVEPOINT sp1;   <span class="t-hdr">-- UPDATE만 취소</span>
COMMIT;
SELECT amount FROM orders WHERE order_id = 1001;
<span class="t-ok">+---------+
| amount  |
+---------+
| 5000000 |   ← UPDATE 취소됨, INSERT 는 커밋됨
+---------+</span>

<span class="t-hdr">-- GRANT 는 묵시적 COMMIT → 앞선 DML 도 함께 커밋됨</span>
START TRANSACTION;
DELETE FROM temp_log WHERE log_date &lt; '2026-01-01';
<span class="t-err">GRANT SELECT ON mydb.* TO 'test'@'localhost';</span>   <span class="t-hdr">← 묵시적 COMMIT 발동</span>
ROLLBACK;   <span class="t-hdr">-- 이미 커밋됨, ROLLBACK 무효</span>
<span class="t-err">-- temp_log 행이 사라진 채로 유지됨</span></pre>
  </div>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT</span>
    TCL 은 DML 의 작업 단위를 <strong>명시적으로 제어</strong>하는 유일한 수단이다.
    COMMIT = 영구 저장, ROLLBACK = 전체 취소, SAVEPOINT = 부분 취소 지점.
    DCL(GRANT/REVOKE) 는 묵시적 COMMIT 을 발동시키므로 — 중요한 DML 트랜잭션 도중에는 GRANT 를 섞지 않도록 주의해야 한다.
    사용자 계정은 <code>'user'@'host'</code> 페어로 관리되며, root 는 모든 권한을 가지지만 프로덕션에서는 최소 권한 원칙(GRANT 로 필요한 권한만)을 따른다.
  </div>
  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — DML · DDL · DCL · TCL 의 네 분면을 모두 돌았다.
    이제 인포그래픽의 4분면이 "각자 다른 책임과 트랜잭션 경계를 가진 이유" 로 통합된다.
  </div>
</section>


<!-- ============================================================ CH06 -->
<section id="ch6">
  <h2 class="chap">
    <span class="num">CH 06</span>최종 정리 — 4분면 통합표와 결론<a href="#ch6" class="anchor-link">#</a>
  </h2>

  <h3 class="step">최종 정리</h3>
  <p>
    출발 의문은 — "MySQL 의 수백 가지 명령어는 어떤 원칙으로 분류되고, 각 분류는 왜 독립적으로 존재하는가?" 였다.
    CH01 ~ CH05 에서 각 분면을 추적한 결과를 한 표로 회수한다.
  </p>
  <table>
    <thead>
      <tr>
        <th>분류</th>
        <th>조작 대상</th>
        <th>트랜잭션</th>
        <th>대표 명령어</th>
        <th>실수 시 복구</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>DML</strong></td>
        <td>행(Row) 데이터</td>
        <td>명시적 — COMMIT/ROLLBACK 으로 제어</td>
        <td><code>SELECT · INSERT · UPDATE · DELETE · REPLACE</code></td>
        <td>ROLLBACK 가능</td>
      </tr>
      <tr>
        <td><strong>DDL</strong></td>
        <td>테이블·스키마 구조</td>
        <td>묵시적 COMMIT 자동 발동</td>
        <td><code>CREATE · ALTER · DROP · TRUNCATE · RENAME</code></td>
        <td>불가 — 신중하게</td>
      </tr>
      <tr>
        <td><strong>DCL</strong></td>
        <td>사용자 권한</td>
        <td>묵시적 COMMIT 자동 발동</td>
        <td><code>GRANT · REVOKE · FLUSH PRIVILEGES</code></td>
        <td>불가 — 신중하게</td>
      </tr>
      <tr>
        <td><strong>TCL</strong></td>
        <td>트랜잭션 경계</td>
        <td>트랜잭션을 제어하는 명령 자체</td>
        <td><code>COMMIT · ROLLBACK · SAVEPOINT</code></td>
        <td>SAVEPOINT 로 부분 복구</td>
      </tr>
    </tbody>
  </table>

  <p>SELECT 핵심 함수 분류 정리:</p>
  <table>
    <thead><tr><th>함수 종류</th><th>대표 함수</th><th>주의점</th></tr></thead>
    <tbody>
      <tr><td>집계</td><td><code>COUNT · SUM · AVG · MAX · MIN</code></td><td>GROUP BY 없이 쓰면 전체가 한 그룹</td></tr>
      <tr><td>문자열</td><td><code>CONCAT · SUBSTR · TRIM · LENGTH</code></td><td>NULL 포함 시 CONCAT 결과가 NULL</td></tr>
      <tr><td>날짜</td><td><code>NOW() · DATEDIFF() · DATE_FORMAT()</code></td><td>CHECK 제약에 사용 불가(비결정론)</td></tr>
      <tr><td>NULL 처리</td><td><code>IFNULL(expr, default) · COALESCE(e1,e2,...)</code></td><td>산술 전 반드시 적용</td></tr>
      <tr><td>윈도우</td><td><code>RANK() OVER(PARTITION BY … ORDER BY …)</code></td><td>집계 함수와 달리 행이 줄어들지 않음</td></tr>
    </tbody>
  </table>

  <h3 class="step">최종 결론</h3>
  <div class="keypoint">
    <span class="label">FINAL CONCLUSION</span>
    MySQL 명령어가 4분면으로 나뉜 이유는 — 각 분면이 <strong>서로 다른 "되돌릴 수 있는가"</strong> 를 가지기 때문이다.
    DML 은 가역(ROLLBACK), DDL·DCL 은 불가역(묵시적 COMMIT), TCL 은 가역성 자체를 제어한다.
    이 원칙을 알면 — "실수로 DROP 해도 복구되나?" → 안 된다(DDL) 는 답이 즉시 나온다.
    "SELECT 에서 별칭을 WHERE 에 쓰면 안 되는 이유" → 실행 순서(WHERE=2단계, SELECT=5단계)의 파이프라인 논리.
    "FK 가 작동 안 하는 이유" → ENGINE=InnoDB 미지정(MyISAM 의 묵시적 무시).
    인포그래픽의 4분면이 보여주는 것은 단순한 명령어 목록이 아니라 — <strong>MySQL 이 데이터 안전을 층층이 설계한 구조</strong>다.
  </div>
</section>

</div>
</main>

<footer>
  <div class="page">
    <p><strong>참고 링크</strong></p>
    <ul class="refs">
      <li><a href="https://dev.mysql.com/doc/refman/8.0/en/sql-statements.html" target="_blank" rel="noopener">MySQL Reference Manual § SQL Statements</a></li>
      <li><a href="https://dev.mysql.com/doc/refman/8.0/en/select.html" target="_blank" rel="noopener">MySQL Reference Manual § 13.2.13 SELECT Statement</a></li>
      <li><a href="https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html" target="_blank" rel="noopener">MySQL Reference Manual § 13.3.3 Statements That Cause an Implicit Commit</a></li>
      <li><a href="https://dev.mysql.com/doc/refman/8.0/en/savepoint.html" target="_blank" rel="noopener">MySQL Reference Manual § 13.3.4 SAVEPOINT</a></li>
      <li><a href="https://dev.mysql.com/doc/refman/8.0/en/create-table-foreign-keys.html" target="_blank" rel="noopener">MySQL Reference Manual § 13.1.20.5 FOREIGN KEY Constraints</a></li>
      <li><a href="https://dev.mysql.com/doc/refman/8.0/en/replace.html" target="_blank" rel="noopener">MySQL Reference Manual § 13.2.12 REPLACE Statement</a></li>
    </ul>
    <p style="margin-top:18px"><strong>통합 소스 파일</strong></p>
    <ul class="refs">
      <li>day0511_mysql_intro.html — 계정·스키마·자료형·B+Tree 입문 (DAY1)</li>
      <li>day0511_mysql_btree.html — B+Tree 내부 구조 심화 (DAY1)</li>
      <li>day0512_mysql_constraints.html — 5대 제약조건 (DAY2)</li>
      <li>day0513_mysql_select_join.html — SELECT 6절·WHERE·JOIN·NULL 함수 (DAY3)</li>
    </ul>
    <p style="margin-top:18px"><strong>소스 코드</strong></p>
    <ul class="refs" style="margin-top:4px">
      <li><a href="https://github.com/roroblack/python_workspace" target="_blank" rel="noopener">GitHub — roroblack/python_workspace</a></li>
      <li><a href="https://roroblack.github.io/python_workspace" target="_blank" rel="noopener">GitHub Pages — 블로그 목록</a></li>
    </ul>
  </div>
</footer>

<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
</body>
</html>'''

html = html_doc(img_src)

out_path = Path('.blog/mysql_commands.html')
out_path.write_text(html, encoding='utf-8')
print(f'생성 완료: {out_path}  ({len(html):,} bytes)')
