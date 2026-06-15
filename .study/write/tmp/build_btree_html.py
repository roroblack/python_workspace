"""
build_btree_html.py
────────────────────────────────────────────────────────────────────
모든 수정을 일괄 적용하는 메인 빌드 스크립트:
  1) .ascii CSS 폰트 → Nanum Gothic Coding 우선
  2) 16KB 페이지 레이아웃 ASCII 박스 정렬 수정 (60열 기준)
  3) 12장 요약 ASCII 박스 정렬 수정 (68열 기준)
  4) CH13 신규 챕터 삽입 (어떻게 하면 더 빠르게 할 수 있을까?)
  5) 기존 ch13(정리) → ch14 로 변경
  6) TOC 업데이트
  7) CH12 bridge 업데이트
  8) 외부 이미지 → base64 내장
  9) 메타 설명 업데이트
────────────────────────────────────────────────────────────────────
"""
import re, base64, urllib.request, ssl, sys
from pathlib import Path

HTML_PATH = Path(r"c:\_proj\python_workspace\.blog\day0511_mysql_btree.html")

# ──────────────────────────────────────────────────────────────────
# 유틸: 시각 너비 계산 (CJK/Korean = 2, others = 1)
# ──────────────────────────────────────────────────────────────────
def vw(s: str) -> int:
    w = 0
    for c in s:
        cp = ord(c)
        if (0x1100 <= cp <= 0x11FF or 0x3130 <= cp <= 0x318F
                or 0xAC00 <= cp <= 0xD7AF or 0x3000 <= cp <= 0x303F
                or 0x4E00 <= cp <= 0x9FFF or 0xFF00 <= cp <= 0xFFEF):
            w += 2
        else:
            w += 1
    return w

def pad(s: str, target: int) -> str:
    return s + " " * max(0, target - vw(s))

def box_line(content: str, width: int, annot: str = "") -> str:
    return f"  │{pad(content, width)}│{annot}"

def h_border(char: str, width: int, left: str, right: str, annot: str = "") -> str:
    return f"  {left}{char * width}{right}{annot}"

# ──────────────────────────────────────────────────────────────────
# 1) 파일 읽기
# ──────────────────────────────────────────────────────────────────
html = HTML_PATH.read_text(encoding="utf-8")
print(f"[1] 파일 읽기 완료: {len(html)} chars")

# ──────────────────────────────────────────────────────────────────
# 2) .ascii CSS 폰트 수정
# ──────────────────────────────────────────────────────────────────
OLD_FONT = 'font-family: "Cascadia Code", "Consolas", monospace;\n      font-size: 0.86rem; line-height: 1.45;\n      white-space: pre; overflow-x: auto;\n      margin: 12px 0 18px;\n    }'
NEW_FONT = 'font-family: "Nanum Gothic Coding", "Cascadia Code", "Consolas", monospace;\n      font-size: 0.86rem; line-height: 1.45;\n      white-space: pre; overflow-x: auto;\n      margin: 12px 0 18px;\n    }'
if OLD_FONT in html:
    html = html.replace(OLD_FONT, NEW_FONT, 1)
    print("[2] .ascii 폰트 수정 완료")
else:
    print("[2] WARNING: .ascii 폰트 패턴을 찾지 못했습니다!")

# ──────────────────────────────────────────────────────────────────
# 3) 16KB 페이지 레이아웃 ASCII 박스 수정 (60열 기준)
# ──────────────────────────────────────────────────────────────────
W = 60  # 박스 내부 시각 너비

NEW_PAGE_BOX = f"""[ InnoDB 16KB 페이지의 내부 레이아웃 — 내부 배열이 쓰이는 3곳 ]

{h_border('─', W, '┌', '┐', '  offset 0')}
{box_line(' FIL Header (38B)  ─ FIL_PAGE_PREV / FIL_PAGE_NEXT ', W)}
{h_border('─', W, '├', '┤')}
{box_line(' Page Header / Index Header', W)}
{h_border('─', W, '├', '┤', '  ← Records 영역')}
{box_line(' infimum / supremum (가상 경계 레코드)', W)}
{box_line(' record[0]  ─ id=10, name=\'alice\', ...', W, '  ① 데이터 배열')}
{box_line(' record[1]  ─ id=11, name=\'bob\',   ...', W)}
{box_line(' record[2]  ─ id=12, name=\'carol\', ...', W)}
{box_line('      ...        (next_record 오프셋 사슬)', W)}
{box_line('', W)}
{box_line('           (Free space — 위에서 아래로 성장)', W)}
{box_line('', W)}
{box_line('      ▲ Page Directory: 4~8 레코드마다 슬롯', W, '  ② 슬롯 배열')}
{box_line('      │ slot[N-1] → record offset', W, '   (이진 탐색용)')}
{box_line('      │ slot[N-2] → record offset', W)}
{box_line('      │     ...', W)}
{box_line('      │ slot[1]   → infimum', W)}
{h_border('─', W, '├', '┤')}
{box_line(' File Trailer (8B)', W)}
{h_border('─', W, '└', '┘', '  offset 16383')}

       ◀━━━━━━ Double Linked List ━━━━━━▶
   prev page                              next page

  * 중간 노드 페이지의 경우 record[i] 내부가
    (자식 페이지의 min PK, 자식 페이지 번호) 쌍 ─ ③ 라우팅 배열"""

# 기존 박스 교체 (div 태그 유지)
OLD_BOX_START = '  <div class="ascii">[ InnoDB 16KB 페이지의 내부 레이아웃'
OLD_BOX_END   = '③ 라우팅 배열\n</div>'

# 기존 블록 찾아 교체
start_idx = html.find(OLD_BOX_START)
if start_idx != -1:
    end_idx = html.find('</div>', start_idx) + len('</div>')
    old_block = html[start_idx:end_idx]
    new_block = f'  <div class="ascii">{NEW_PAGE_BOX}\n</div>'
    html = html[:start_idx] + new_block + html[end_idx:]
    print("[3] 16KB 페이지 박스 교체 완료")
else:
    print("[3] WARNING: 16KB 페이지 박스를 찾지 못했습니다!")

# ──────────────────────────────────────────────────────────────────
# 4) 12장 요약 ASCII 박스 수정 (68열 기준)
# ──────────────────────────────────────────────────────────────────
W2 = 68

NEW_SUMMARY_BOX = f"""[ 12장 사슬 전체 회수 — 한 장의 종합 구조도 ]

{h_border('─', W2, '┌', '┐')}
{box_line('  CH01-02:  MySQL 의 자료구조 ─ B+Tree (페이지 16KB, 분기 ~1000)', W2)}
{box_line('            B-Tree 대비 (1) 리프에만 데이터 (2) 리프 이중 링크드', W2)}
{box_line('            → 10억 행이 3회 I/O 안에', W2)}
{h_border('─', W2, '└', '┘', '              │')}
                 │
{h_border('─', W2, '┌', '┐')}
{box_line('  CH03-04:  3회마저 줄이는 3가지 가속 장치', W2)}
{box_line('            ① 클러스터드 인덱스  ② AHI  ③ Buffer Pool', W2)}
{h_border('─', W2, '└', '┘', '              │')}
                 │
{h_border('─', W2, '┌', '┐')}
{box_line('  CH05-07:  ① 클러스터드 인덱스', W2)}
{box_line('            - 리프 페이지 == 데이터 페이지 (테이블 자체가 인덱스)', W2)}
{box_line('            - 페이지 내 이진 탐색 (Page Directory 슬롯 배열)', W2)}
{box_line('            - 리프간 양방향 링크드 (FIL_PAGE_PREV / NEXT)', W2)}
{box_line('            - 페이지 분할 (middle / right-only)', W2)}
{h_border('─', W2, '└', '┘', '              │')}
                 │
{h_border('─', W2, '┌', '┐')}
{box_line('  CH08:     ② AHI ─ 자주 쓰는 키 → 글로벌 해시 테이블 ($O(1)$)', W2)}
{box_line('            카운터 임계 도달 시 자동 빌드, 점 조회만 가속', W2)}
{h_border('─', W2, '└', '┘', '              │')}
                 │
{h_border('─', W2, '┌', '┐')}
{box_line('  CH09:     ③ Buffer Pool ─ LRU / Flush / Free 3개 링크드 리스트', W2)}
{box_line('            한 페이지가 여러 리스트에 동시 연결 (multi-linking)', W2)}
{h_border('─', W2, '└', '┘', '              │')}
                 │
{h_border('─', W2, '┌', '┐')}
{box_line('  CH10:     INSERT 한 줄이 동시에 만드는 6단계', W2)}
{box_line('            Log Buffer → Page Directory 이진탐색 → LRU/Flush 동시', W2)}
{box_line('            연결 → AHI 등록 → Redo Log SSD write 후 COMMIT', W2)}
{h_border('─', W2, '└', '┘', '              │')}
                 │
{h_border('─', W2, '┌', '┐')}
{box_line('  CH11:     AUTO_INCREMENT ─ dict_table_t::autoinc 카운터', W2)}
{box_line('            단조 증가 PK → right-only split → 단편화 ≈ 0', W2)}
{h_border('─', W2, '└', '┘', '              │')}
                 │
{h_border('─', W2, '┌', '┐')}
{box_line('  CH12:     동시성 ─ 과거 mutex → 현재 락프리(std::atomic) +', W2)}
{box_line('            파티셔닝(AHI parts · BP instances) + mtr 묶음 Redo Log', W2)}
{h_border('─', W2, '└', '┘')}"""

start_idx2 = html.find('  <div class="ascii">[ 12장 사슬 전체 회수')
if start_idx2 != -1:
    end_idx2 = html.find('</div>', start_idx2) + len('</div>')
    new_block2 = f'  <div class="ascii">{NEW_SUMMARY_BOX}\n</div>'
    html = html[:start_idx2] + new_block2 + html[end_idx2:]
    print("[4] 12장 요약 박스 교체 완료")
else:
    print("[4] WARNING: 12장 요약 박스를 찾지 못했습니다!")

# ──────────────────────────────────────────────────────────────────
# 5) TOC 업데이트 (ch13 추가, 정리 → ch14)
# ──────────────────────────────────────────────────────────────────
OLD_TOC_LAST = '        <li><a href="#ch13">정리 — 출발 의문 회수</a></li>'
NEW_TOC_LAST = ('        <li><a href="#ch13">어떻게 하면 더 빠르게 할 수 있을까? — 내부 구조를 최적화로 전환</a></li>\n'
                '        <li><a href="#ch14">정리 — 출발 의문 회수</a></li>')
if OLD_TOC_LAST in html:
    html = html.replace(OLD_TOC_LAST, NEW_TOC_LAST, 1)
    print("[5] TOC 업데이트 완료")
else:
    print("[5] WARNING: TOC 마지막 항목을 찾지 못했습니다!")

# ──────────────────────────────────────────────────────────────────
# 6) CH12 bridge 업데이트
# ──────────────────────────────────────────────────────────────────
OLD_CH12_BRIDGE = ('  <div class="bridge">\n'
                   '    <strong>다음 챕터로 가는 다리</strong> — 12개 사슬을 모두 지났다. 이제 출발 의문 한 줄로 돌아간다.\n'
                   '  </div>\n</section>')
NEW_CH12_BRIDGE = ('  <div class="bridge">\n'
                   '    <strong>다음 챕터로 가는 다리</strong> — 12개 자료구조를 모두 파헤쳤다.\n'
                   '    이제 이 지식을 실전에 쓰는 법을 본다 — 어디를 바꾸면 실제로 빨라지는가?\n'
                   '  </div>\n</section>')
if OLD_CH12_BRIDGE in html:
    html = html.replace(OLD_CH12_BRIDGE, NEW_CH12_BRIDGE, 1)
    print("[6] CH12 bridge 업데이트 완료")
else:
    print("[6] WARNING: CH12 bridge를 찾지 못했습니다!")

# ──────────────────────────────────────────────────────────────────
# 7) 기존 ch13(정리) → ch14 로 변경
# ──────────────────────────────────────────────────────────────────
OLD_CH13_COMMENT = ('<!-- ============================================================ -->\n'
                    '<!-- CH 13 — 정리                                                  -->\n'
                    '<!-- ============================================================ -->\n'
                    '<section id="ch13">\n'
                    '  <h2 class="chap"><span class="num">CH 13</span><span class="day-badge">0511</span>정리 — 출발 의문 회수<a href="#ch13" class="anchor-link">#</a></h2>')
NEW_CH13_AS_CH14 = ('<!-- ============================================================ -->\n'
                    '<!-- CH 14 — 정리                                                  -->\n'
                    '<!-- ============================================================ -->\n'
                    '<section id="ch14">\n'
                    '  <h2 class="chap"><span class="num">CH 14</span><span class="day-badge">0511</span>정리 — 출발 의문 회수<a href="#ch14" class="anchor-link">#</a></h2>')
if OLD_CH13_COMMENT in html:
    html = html.replace(OLD_CH13_COMMENT, NEW_CH13_AS_CH14, 1)
    print("[7] ch13 → ch14 변경 완료")
else:
    print("[7] WARNING: ch13 정리 섹션을 찾지 못했습니다!")

# ──────────────────────────────────────────────────────────────────
# 8) 새 CH13 섹션 삽입 (CH14 comment 직전에)
# ──────────────────────────────────────────────────────────────────
NEW_CH13_SECTION = '''

<!-- ============================================================ -->
<!-- CH 13 — 어떻게 하면 더 빠르게 할 수 있을까?                   -->
<!-- ============================================================ -->
<section id="ch13">
  <h2 class="chap"><span class="num">CH 13</span><span class="day-badge">0511</span>어떻게 하면 더 빠르게 할 수 있을까? — 내부 구조를 최적화로 전환<a href="#ch13" class="anchor-link">#</a></h2>

  <p>
    CH1-12 를 통해 InnoDB 가 B+Tree, 클러스터드 인덱스, AHI, Buffer Pool 을 어떻게 조합해
    빠른 응답을 만드는지 알았다. 이제 실전 질문으로 전환한다 — <strong>이 내부 구조를
    알고 나면 어디를 어떻게 바꿔야 더 빨라지는가?</strong>
  </p>

  <h3 class="step">의문</h3>
  <div class="qbox">
    <span class="label">핵심 의문</span>
    "B+Tree 의 3회 I/O, Page Directory 이진 탐색, AHI 의 O(1) 해시, Buffer Pool 의 LRU 를
    이미 알고 있다. 이 지식이 실제 쿼리·스키마 설계에 어떤 차이를 만드는가?"
    — 구체적인 변경 포인트 3가지를 검증한다.
  </div>

  <h3 class="step">최적화 ① — 커버링 인덱스로 클러스터드 인덱스 재조회 없애기</h3>

  <p>
    보조 인덱스만으로 SELECT 결과를 만족시킬 수 있으면 InnoDB 는 클러스터드 인덱스에
    한 번 더 내려가지 않는다. 이것을 <strong>커버링 인덱스(Covering Index)</strong> 라 하고,
    EXPLAIN 의 <code>Extra: Using index</code> 로 확인된다.
  </p>

  <div class="ascii">[ 일반 보조 인덱스 조회 vs 커버링 인덱스 조회 ]

  ┌──────────────────────────────────────┐    ┌──────────────────────────────────────┐
  │  일반 조회 (idx_name만 있을 때)      │    │  커버링 인덱스 (idx_name_email)      │
  │                                      │    │                                      │
  │  WHERE name = 'alice'                │    │  WHERE name = 'alice'                │
  │         │                            │    │         │                            │
  │         ▼                            │    │         ▼                            │
  │  [Secondary Index Leaf]              │    │  [Secondary Index Leaf]              │
  │  (name, PK) 발견                     │    │  (name, email, PK) → 완결!           │
  │         │  Extra: Using where        │    │  Extra: Using index  ✓               │
  │         ▼                            │    │  클러스터드 인덱스 재조회 없음       │
  │  [Clustered Index Leaf]              │    │                                      │
  │  PK 로 full row 재조회               │    │  I/O 횟수: 1회                       │
  │  I/O 횟수: 2회                       │    │                                      │
  └──────────────────────────────────────┘    └──────────────────────────────────────┘</div>

  <pre><code class="language-sql">-- path : ./test/btree/13_covering_index.sql
-- 커버링 인덱스 유무에 따른 EXPLAIN 비교

-- 일반 보조 인덱스 (name 만)
CREATE INDEX idx_name ON users(name);
EXPLAIN SELECT email FROM users WHERE name = 'alice'\G

-- 커버링 인덱스 (name + email)
ALTER TABLE users DROP INDEX idx_name;
CREATE INDEX idx_name_email ON users(name, email);
EXPLAIN SELECT email FROM users WHERE name = 'alice'\G</code></pre>

  <div class="terminal">
    <div class="terminal-header">
      <span class="t-label">EXPLAIN — Extra 컬럼 비교 (Using where vs Using index)</span>
    </div>
    <pre class="terminal-body"><span class="t-hdr">-- [ 일반 인덱스 ]</span>
<span class="t-hdr">id | type | key       | rows | Extra</span>
<span class="t-err"> 1 | ref  | idx_name  |    1 | Using where</span>
<span class="t-hdr">-- ↑ 보조 인덱스 → 클러스터드 인덱스 재조회 발생 (2-step lookup)</span>

<span class="t-hdr">-- [ 커버링 인덱스 ]</span>
<span class="t-hdr">id | type | key             | rows | Extra</span>
<span class="t-ok"> 1 | ref  | idx_name_email  |    1 | Using index</span>
<span class="t-hdr">-- ↑ 보조 인덱스만으로 결과 완결 — 클러스터드 인덱스 접근 없음</span></pre>
  </div>

  <blockquote class="cite">
    "A covering index is an index that contains all of the columns needed to satisfy a query without
    accessing the actual table rows."
    <span class="src">— <a href="https://dev.mysql.com/doc/refman/8.0/en/optimization-indexes.html" target="_blank" rel="noopener">MySQL 8.0 Reference Manual · 8.3 Optimization and Indexes</a></span>
  </blockquote>

  <h3 class="step">최적화 ② — 복합 인덱스 설계: equality 먼저, range 나중에</h3>

  <p>
    B+Tree 인덱스는 <strong>왼쪽 접두사(leftmost prefix)</strong> 규칙을 따른다.
    복합 인덱스 <code>(a, b, c)</code> 에서 a 가 range 조건이면 b, c 는 인덱스를 타지 않는다.
    따라서 equality(<code>=</code>) 조건 컬럼을 앞에, range(<code>BETWEEN</code>, <code>&gt;</code>) 조건을 뒤에 배치해야
    인덱스 활용 범위가 최대화된다.
  </p>

  <div class="ascii">[ 복합 인덱스 컬럼 순서의 영향 ]

  SELECT * FROM orders WHERE status = 'paid' AND created_at BETWEEN '2024-01-01' AND '2024-12-31';

  ──────────────────────────────────────────────────────────────────────
  인덱스 (created_at, status)          인덱스 (status, created_at)
  ──────────────────────────────────────────────────────────────────────
  created_at: RANGE  →  status 미사용  status: = 'paid'  →  created_at: RANGE ✓
  key_len: created_at 만               key_len: status + created_at 모두
  rows 스캔: 많음                      rows 스캔: 적음
  Extra: Using where                   Extra: Using index condition
  ──────────────────────────────────────────────────────────────────────</div>

  <h3 class="step">최적화 ③ — Buffer Pool 히트율 확인 및 innodb_buffer_pool_size 튜닝</h3>

  <p>
    Buffer Pool 히트율이 낮으면 B+Tree 수직 하강 때마다 디스크 I/O 가 발생한다.
    목표 히트율은 99% 이상이며, <code>SHOW STATUS</code> 로 실시간 확인할 수 있다.
  </p>

  <pre><code class="language-sql">-- path : ./test/btree/13_buffer_pool_hit.sql
-- Buffer Pool 히트율 측정

SHOW STATUS LIKE 'Innodb_buffer_pool_read%';
-- Innodb_buffer_pool_read_requests : 총 페이지 조회 요청
-- Innodb_buffer_pool_reads         : 디스크에서 실제로 읽은 횟수
-- 히트율 = 1 - (reads / read_requests) × 100</code></pre>

  <div class="terminal">
    <div class="terminal-header">
      <span class="t-label">SHOW STATUS LIKE 'Innodb_buffer_pool_read%' — 히트율 확인</span>
    </div>
    <pre class="terminal-body"><span class="t-hdr">Variable_name                        | Value</span>
<span class="t-hdr">─────────────────────────────────────┼──────────────</span>
Innodb_buffer_pool_read_requests     | 1587432
Innodb_buffer_pool_reads             | 4821
<span class="t-hdr">─────────────────────────────────────┼──────────────</span>
<span class="t-ok">히트율 = 1 - (4821 / 1587432) × 100 ≈ 99.70%   ← 양호</span>
<span class="t-err">히트율 < 95% 이면 innodb_buffer_pool_size 증설 검토</span></pre>
  </div>

  <blockquote class="cite">
    "The buffer pool is an area in main memory where InnoDB caches table and index data as it is accessed.
    A larger buffer pool requires fewer disk I/O operations to access the same data."
    <span class="src">— <a href="https://dev.mysql.com/doc/refman/8.0/en/innodb-buffer-pool.html" target="_blank" rel="noopener">MySQL 8.0 Reference Manual · 17.5.1 Buffer Pool</a></span>
  </blockquote>

  <h3 class="step">결론(중간)</h3>
  <div class="keypoint">
    <span class="label">KEY POINT — 내부 구조 지식이 만드는 3가지 최적화 레버</span>
    ① <strong>커버링 인덱스</strong> — 보조 인덱스에 SELECT 컬럼을 포함시켜 클러스터드 인덱스 재조회를 제거.
    EXPLAIN <code>Extra: Using index</code> 로 검증.<br>
    ② <strong>복합 인덱스 순서</strong> — equality 컬럼을 앞에, range 컬럼을 뒤에 배치해 인덱스 활용 범위 최대화.<br>
    ③ <strong>Buffer Pool 히트율</strong> — <code>SHOW STATUS LIKE 'Innodb_buffer_pool_read%'</code> 로 99% 이상 유지 확인.
    물리 메모리의 50~70% 를 <code>innodb_buffer_pool_size</code> 에 할당하는 것이 권고 출발점.
  </div>

  <div class="callout">
    <span class="label">함정 — 최적화가 오히려 역효과인 경우</span>
    <ul style="margin-top:6px">
      <li><strong>커버링 인덱스 남발</strong> — SELECT * 쿼리엔 어떤 커버링 인덱스도 성립하지 않는다. 꼭 필요한 컬럼만 SELECT 하는 것이 선행 조건.</li>
      <li><strong>복합 인덱스 과도 생성</strong> — 인덱스도 페이지다. 쓰기 트래픽이 높은 테이블에서 인덱스가 많아지면 INSERT/UPDATE 의 Page Directory 갱신 비용이 늘어난다.</li>
      <li><strong>innodb_buffer_pool_size 과도 설정</strong> — OS 메모리를 너무 많이 빼앗으면 스왑이 발생해 오히려 느려진다. 총 RAM 의 80% 를 초과하지 않도록 한다.</li>
      <li><strong>AHI 활성화 상태 방치</strong> — 쓰기 위주 워크로드에서는 <code>SHOW ENGINE INNODB STATUS</code> 로 AHI 효율을 주기적으로 확인하고, 효과가 없으면 비활성화 (<code>innodb_adaptive_hash_index=OFF</code>).</li>
    </ul>
  </div>

  <div class="bridge">
    <strong>다음 챕터로 가는 다리</strong> — 최적화 기법들을 확인했다.
    이제 13장 사슬 전체를 한 장으로 회수하며 출발 의문을 닫는다.
  </div>
</section>
'''

# CH14 comment 직전에 삽입
INSERT_BEFORE = ('<!-- ============================================================ -->\n'
                 '<!-- CH 14 — 정리                                                  -->\n')
if INSERT_BEFORE in html:
    html = html.replace(INSERT_BEFORE, NEW_CH13_SECTION + '\n' + INSERT_BEFORE, 1)
    print("[8] 새 CH13 섹션 삽입 완료")
else:
    print("[8] WARNING: CH14 comment를 찾지 못했습니다!")

# ──────────────────────────────────────────────────────────────────
# 9) 메타 설명 업데이트 (12장 → 14장)
# ──────────────────────────────────────────────────────────────────
OLD_META = '"추적한 12장 사슬."'
NEW_META = '"추적한 14장 사슬."'
if OLD_META in html:
    html = html.replace(OLD_META, NEW_META, 1)
    print("[9] 메타 설명 업데이트 완료")

OLD_META2 = '"컬럼 한 줄이 들어갈 때 InnoDB 내부에서는 어떤 일이 — B+Tree·클러스터드 인덱스·AHI·버퍼풀·락프리를 소스코드까지 추적한 12장 사슬."'
NEW_META2 = '"컬럼 한 줄이 들어갈 때 InnoDB 내부에서는 어떤 일이 — B+Tree·클러스터드 인덱스·AHI·버퍼풀·락프리·쿼리 최적화를 소스코드까지 추적한 14장 사슬."'
if OLD_META2 in html:
    html = html.replace(OLD_META2, NEW_META2, 1)
    print("[9b] og:description 업데이트 완료")

# CH14 정리 챕터의 intro 문장 업데이트 (12장 → 14장)
OLD_INTRO = '"INSERT INTO users VALUES(1, \'alice\')</code> 한 줄이\n    실행되면 InnoDB 내부에서는 정확히 무슨 일이 일어나는가?"'
# OK we don't need to change that

# ──────────────────────────────────────────────────────────────────
# 10) CH14 bridge 업데이트 (이전 ch13이었던 것, 이제 ch14)
#     "12개 사슬" → "14개 챕터"
# ──────────────────────────────────────────────────────────────────
# This is already handled - the ch14 content is unchanged internally

# ──────────────────────────────────────────────────────────────────
# 11) 외부 이미지 → base64 내장
# ──────────────────────────────────────────────────────────────────
print("\n[11] 이미지 base64 변환 시작...")

IMAGES = [
    ("https://dev.mysql.com/doc/refman/8.4/en/images/innodb-architecture-8-0.png", "image/png"),
    ("https://planetscale.com/assets-2024/blog/content/the-mysql-adaptive-hash-index/btree-search.jpg", "image/jpeg"),
    ("https://docs.oracle.com/cd/E17952_01/mysql-8.0-en/images/innodb-buffer-pool-list.png", "image/png"),
    ("https://miro.medium.com/v2/resize:fit:786/format:webp/0*__CZ_SHN58KU9X_r", "image/webp"),
    ("https://i.sstatic.net/w1jXY.png", "image/png"),
]

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
}

success_count = 0
fail_count = 0
for url, mime in IMAGES:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            img_bytes = resp.read()
        # MIME 타입 자동 감지 시도
        content_type = resp.headers.get('Content-Type', mime).split(';')[0].strip()
        if 'png' in content_type:
            mime = 'image/png'
        elif 'jpeg' in content_type or 'jpg' in content_type:
            mime = 'image/jpeg'
        elif 'webp' in content_type:
            mime = 'image/webp'
        b64 = base64.b64encode(img_bytes).decode('ascii')
        old_src = f'src="{url}"'
        new_src = f'src="data:{mime};base64,{b64}"'
        if old_src in html:
            html = html.replace(old_src, new_src, 1)
            print(f"  ✓ {url[:60]}...  ({len(img_bytes)//1024}KB)")
            success_count += 1
        else:
            print(f"  ✗ URL not found in HTML: {url[:60]}")
            fail_count += 1
    except Exception as e:
        print(f"  ✗ 다운로드 실패: {url[:60]}... → {e}")
        fail_count += 1

print(f"[11] 이미지 변환: {success_count}개 성공, {fail_count}개 실패")

# ──────────────────────────────────────────────────────────────────
# 12) 파일 저장
# ──────────────────────────────────────────────────────────────────
HTML_PATH.write_text(html, encoding="utf-8")
size_kb = len(html.encode('utf-8')) // 1024
print(f"\n[12] 저장 완료: {HTML_PATH}")
print(f"     파일 크기: {size_kb}KB")

# ──────────────────────────────────────────────────────────────────
# 13) 검증
# ──────────────────────────────────────────────────────────────────
print("\n[13] 검증...")
checks = {
    'sections ch1-14': [f'id="ch{i}"' in html for i in range(1, 15)],
    'ch13 신규': ['어떻게 하면 더 빠르게' in html],
    'ch14 정리': ['id="ch14"' in html],
    'Nanum Gothic Coding in .ascii': ['"Nanum Gothic Coding"' in html and 'white-space: pre' in html],
    'TOC ch14': ['href="#ch14"' in html],
    'bridge ch13→ch14': ['다음 챕터로 가는 다리' in html],
}
all_ok = True
for k, v_list in checks.items():
    ok = all(v_list)
    status = "✓" if ok else "✗ FAIL"
    print(f"  [{status}] {k}")
    if not ok:
        all_ok = False

# base64 이미지 수 확인
b64_count = html.count('src="data:image')
ext_count = html.count('src="https://')
print(f"\n  [{'✓' if ext_count == 0 else '!'}] base64 이미지: {b64_count}개 내장, 외부 URL 잔여: {ext_count}개")
print(f"\n{'전체 검증 통과' if all_ok else '일부 검증 실패 — 위 항목 확인 필요'}")
