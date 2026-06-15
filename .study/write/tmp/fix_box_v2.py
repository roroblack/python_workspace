"""
fix_box_v2.py
────────────────────────────────────────────────────────────────────
Nanum Gothic Coding 에서는 ASCII(U+0000-U+007F)만 1× 너비이고,
나머지 모든 문자(한글, 박스문자 ─ │ ┌ ┐, ▲ → 等)는 2× 너비임.
이를 감안해 올바른 new_vw() 로 16KB 박스와 12장 요약 박스를 재생성.

측정값(Playwright canvas measureText):
  ASCII 'A'  = 6.880px (1×)
  Korean '가' = 13.760px (2×)
  BoxDraw '─' = 13.760px (2×)  ← 이전 스크립트가 1×로 잘못 계산
  BoxDraw '│' = 13.760px (2×)

공식:
  border N개 ─: 시각 너비 = N × 2  (단위: ASCII 1글자 = 1단위)
  content 줄:   new_vw(content) = target = N × 2
  padding     = target - new_vw(content)
────────────────────────────────────────────────────────────────────
"""
from pathlib import Path

HTML_PATH = Path(r"c:\_proj\python_workspace\.blog\day0511_mysql_btree.html")

# ──────────────────────────────────────────────────────────────────
# 올바른 시각 너비: ASCII만 1×, 나머지 모두 2×
# ──────────────────────────────────────────────────────────────────
def new_vw(s: str) -> int:
    return sum(1 if ord(c) < 128 else 2 for c in s)

def pad_line(content: str, target: int) -> str:
    return content + " " * max(0, target - new_vw(content))

def box_line(content: str, target: int, annot: str = "") -> str:
    return f"  │{pad_line(content, target)}│{annot}"

def h_border(ch: str, n: int, left: str, right: str, annot: str = "") -> str:
    return f"  {left}{ch * n}{right}{annot}"

# ──────────────────────────────────────────────────────────────────
# 16KB 박스: N=30 → inner visual = 60 단위
#   (30개 ─ × 2u = 60u, 모든 content 줄 new_vw = 60)
# ──────────────────────────────────────────────────────────────────
N1 = 30          # ─ 개수
T1 = N1 * 2     # = 60  target visual width (new_vw 기준)

# 각 줄 new_vw 사전 확인
lines_16kb = [
    (' FIL Header (38B)  ─ FIL_PAGE_PREV / FIL_PAGE_NEXT ', ''),
    (' Page Header / Index Header', ''),
    (' infimum / supremum (가상 경계 레코드)', ''),
    (" record[0]  ─ id=10, name='alice', ...", '  ① 데이터 배열'),
    (" record[1]  ─ id=11, name='bob',   ...", ''),
    (" record[2]  ─ id=12, name='carol', ...", ''),
    ('      ...        (next_record 오프셋 사슬)', ''),
    ('', ''),
    ('           (Free space — 위에서 아래로 성장)', ''),
    ('', ''),
    ('      ▲ Page Directory: 4~8 레코드마다 슬롯', '  ② 슬롯 배열'),
    ('      │ slot[N-1] → record offset', '   (이진 탐색용)'),
    ('      │ slot[N-2] → record offset', ''),
    ('      │     ...', ''),
    ('      │ slot[1]   → infimum', ''),
    (' File Trailer (8B)', ''),
]

print(f"=== 16KB 박스 (N={N1}, target={T1}) ===")
max_vw = 0
for content, annot in lines_16kb:
    vw = new_vw(content)
    max_vw = max(max_vw, vw)
    pad = T1 - vw
    flag = "✓" if pad >= 0 else "✗ OVERFLOW"
    print(f"  vw={vw:3d} pad={pad:3d} {flag}  |  {repr(content[:45])}")
print(f"  max new_vw = {max_vw}, target = {T1}, margin = {T1-max_vw}")

NEW_PAGE_BOX = f"""[ InnoDB 16KB 페이지의 내부 레이아웃 — 내부 배열이 쓰이는 3곳 ]

{h_border('─', N1, '┌', '┐', '  offset 0')}
{box_line(' FIL Header (38B)  ─ FIL_PAGE_PREV / FIL_PAGE_NEXT ', T1)}
{h_border('─', N1, '├', '┤')}
{box_line(' Page Header / Index Header', T1)}
{h_border('─', N1, '├', '┤', '  ← Records 영역')}
{box_line(' infimum / supremum (가상 경계 레코드)', T1)}
{box_line(" record[0]  ─ id=10, name='alice', ...", T1, '  ① 데이터 배열')}
{box_line(" record[1]  ─ id=11, name='bob',   ...", T1)}
{box_line(" record[2]  ─ id=12, name='carol', ...", T1)}
{box_line('      ...        (next_record 오프셋 사슬)', T1)}
{box_line('', T1)}
{box_line('           (Free space — 위에서 아래로 성장)', T1)}
{box_line('', T1)}
{box_line('      ▲ Page Directory: 4~8 레코드마다 슬롯', T1, '  ② 슬롯 배열')}
{box_line('      │ slot[N-1] → record offset', T1, '   (이진 탐색용)')}
{box_line('      │ slot[N-2] → record offset', T1)}
{box_line('      │     ...', T1)}
{box_line('      │ slot[1]   → infimum', T1)}
{h_border('─', N1, '├', '┤')}
{box_line(' File Trailer (8B)', T1)}
{h_border('─', N1, '└', '┘', '  offset 16383')}

       ◀━━━━━━ Double Linked List ━━━━━━▶
   prev page                              next page

  * 중간 노드 페이지의 경우 record[i] 내부가
    (자식 페이지의 min PK, 자식 페이지 번호) 쌍 ─ ③ 라우팅 배열"""

# ──────────────────────────────────────────────────────────────────
# 12장 요약 박스: N=34 → inner visual = 68 단위
# ──────────────────────────────────────────────────────────────────
N2 = 34
T2 = N2 * 2     # = 68

summary_lines = [
    '  CH01-02:  MySQL 의 자료구조 ─ B+Tree (페이지 16KB, 분기 ~1000)',
    '            B-Tree 대비 (1) 리프에만 데이터 (2) 리프 이중 링크드',
    '            → 10억 행이 3회 I/O 안에',
    '  CH03-04:  3회마저 줄이는 3가지 가속 장치',
    '            ① 클러스터드 인덱스  ② AHI  ③ Buffer Pool',
    '  CH05-07:  ① 클러스터드 인덱스',
    '            - 리프 페이지 == 데이터 페이지 (테이블 자체가 인덱스)',
    '            - 페이지 내 이진 탐색 (Page Directory 슬롯 배열)',
    '            - 리프간 양방향 링크드 (FIL_PAGE_PREV / NEXT)',
    '            - 페이지 분할 (middle / right-only)',
    '  CH08:     ② AHI ─ 자주 쓰는 키 → 글로벌 해시 테이블 ($O(1)$)',
    '            카운터 임계 도달 시 자동 빌드, 점 조회만 가속',
    '  CH09:     ③ Buffer Pool ─ LRU / Flush / Free 3개 링크드 리스트',
    '            한 페이지가 여러 리스트에 동시 연결 (multi-linking)',
    '  CH10:     INSERT 한 줄이 동시에 만드는 6단계',
    '            Log Buffer → Page Directory 이진탐색 → LRU/Flush 동시',
    '            연결 → AHI 등록 → Redo Log SSD write 후 COMMIT',
    '  CH11:     AUTO_INCREMENT ─ dict_table_t::autoinc 카운터',
    '            단조 증가 PK → right-only split → 단편화 ≈ 0',
    '  CH12:     동시성 ─ 과거 mutex → 현재 락프리(std::atomic) +',
    '            파티셔닝(AHI parts · BP instances) + mtr 묶음 Redo Log',
]

print(f"\n=== 12장 요약 박스 (N={N2}, target={T2}) ===")
max_vw2 = 0
for s in summary_lines:
    vw = new_vw(s)
    max_vw2 = max(max_vw2, vw)
    pad = T2 - vw
    flag = "✓" if pad >= 0 else "✗ OVERFLOW"
    print(f"  vw={vw:3d} pad={pad:3d} {flag}  |  {repr(s[:50])}")
print(f"  max new_vw = {max_vw2}, target = {T2}, margin = {T2-max_vw2}")

NEW_SUMMARY_BOX = f"""[ 12장 사슬 전체 회수 — 한 장의 종합 구조도 ]

{h_border('─', N2, '┌', '┐')}
{box_line('  CH01-02:  MySQL 의 자료구조 ─ B+Tree (페이지 16KB, 분기 ~1000)', T2)}
{box_line('            B-Tree 대비 (1) 리프에만 데이터 (2) 리프 이중 링크드', T2)}
{box_line('            → 10억 행이 3회 I/O 안에', T2)}
{h_border('─', N2, '└', '┘', '              │')}
                 │
{h_border('─', N2, '┌', '┐')}
{box_line('  CH03-04:  3회마저 줄이는 3가지 가속 장치', T2)}
{box_line('            ① 클러스터드 인덱스  ② AHI  ③ Buffer Pool', T2)}
{h_border('─', N2, '└', '┘', '              │')}
                 │
{h_border('─', N2, '┌', '┐')}
{box_line('  CH05-07:  ① 클러스터드 인덱스', T2)}
{box_line('            - 리프 페이지 == 데이터 페이지 (테이블 자체가 인덱스)', T2)}
{box_line('            - 페이지 내 이진 탐색 (Page Directory 슬롯 배열)', T2)}
{box_line('            - 리프간 양방향 링크드 (FIL_PAGE_PREV / NEXT)', T2)}
{box_line('            - 페이지 분할 (middle / right-only)', T2)}
{h_border('─', N2, '└', '┘', '              │')}
                 │
{h_border('─', N2, '┌', '┐')}
{box_line('  CH08:     ② AHI ─ 자주 쓰는 키 → 글로벌 해시 테이블 ($O(1)$)', T2)}
{box_line('            카운터 임계 도달 시 자동 빌드, 점 조회만 가속', T2)}
{h_border('─', N2, '└', '┘', '              │')}
                 │
{h_border('─', N2, '┌', '┐')}
{box_line('  CH09:     ③ Buffer Pool ─ LRU / Flush / Free 3개 링크드 리스트', T2)}
{box_line('            한 페이지가 여러 리스트에 동시 연결 (multi-linking)', T2)}
{h_border('─', N2, '└', '┘', '              │')}
                 │
{h_border('─', N2, '┌', '┐')}
{box_line('  CH10:     INSERT 한 줄이 동시에 만드는 6단계', T2)}
{box_line('            Log Buffer → Page Directory 이진탐색 → LRU/Flush 동시', T2)}
{box_line('            연결 → AHI 등록 → Redo Log SSD write 후 COMMIT', T2)}
{h_border('─', N2, '└', '┘', '              │')}
                 │
{h_border('─', N2, '┌', '┐')}
{box_line('  CH11:     AUTO_INCREMENT ─ dict_table_t::autoinc 카운터', T2)}
{box_line('            단조 증가 PK → right-only split → 단편화 ≈ 0', T2)}
{h_border('─', N2, '└', '┘', '              │')}
                 │
{h_border('─', N2, '┌', '┐')}
{box_line('  CH12:     동시성 ─ 과거 mutex → 현재 락프리(std::atomic) +', T2)}
{box_line('            파티셔닝(AHI parts · BP instances) + mtr 묶음 Redo Log', T2)}
{h_border('─', N2, '└', '┘')}"""

# ──────────────────────────────────────────────────────────────────
# HTML 교체
# ──────────────────────────────────────────────────────────────────
html = HTML_PATH.read_text(encoding='utf-8')
print(f"\n[파일 읽기] {len(html)} chars")

# 16KB 박스 교체
start1 = html.find('  <div class="ascii">[ InnoDB 16KB 페이지의 내부 레이아웃')
if start1 != -1:
    end1 = html.find('</div>', start1) + len('</div>')
    html = html[:start1] + f'  <div class="ascii">{NEW_PAGE_BOX}\n</div>' + html[end1:]
    print("[16KB 박스] 교체 완료")
else:
    print("[16KB 박스] WARNING: 시작점을 찾지 못함!")

# 12장 요약 박스 교체
start2 = html.find('  <div class="ascii">[ 12장 사슬 전체 회수')
if start2 != -1:
    end2 = html.find('</div>', start2) + len('</div>')
    html = html[:start2] + f'  <div class="ascii">{NEW_SUMMARY_BOX}\n</div>' + html[end2:]
    print("[12장 박스] 교체 완료")
else:
    print("[12장 박스] WARNING: 시작점을 찾지 못함!")

HTML_PATH.write_text(html, encoding='utf-8')
print(f"[저장] {HTML_PATH} ({len(html.encode('utf-8'))//1024}KB)")

# ──────────────────────────────────────────────────────────────────
# 검증: 실제 생성된 박스의 new_vw 확인
# ──────────────────────────────────────────────────────────────────
print("\n=== 생성된 16KB 박스 검증 ===")
idx = html.find('InnoDB 16KB')
block = html[idx:html.find('</div>', idx)]
for line in block.split('\n'):
    stripped = line.rstrip()
    if '│' in stripped:
        first = stripped.index('│')
        last = stripped.rindex('│')
        if first != last:
            inside = stripped[first+1:last]
            actual = new_vw(inside)
            flag = "✓" if actual == T1 else f"✗ {actual} ≠ {T1}"
            print(f"  [{flag}] vw={actual}  {repr(inside[:40])}")

print("\n=== 생성된 12장 박스 검증 ===")
idx2 = html.find('12장 사슬 전체 회수')
block2 = html[idx2:html.find('</div>', idx2)]
all_ok = True
for line in block2.split('\n'):
    stripped = line.rstrip()
    if '│' in stripped:
        first = stripped.index('│')
        last = stripped.rindex('│')
        if first != last:
            inside = stripped[first+1:last]
            actual = new_vw(inside)
            flag = "✓" if actual == T2 else f"✗ {actual} ≠ {T2}"
            if actual != T2:
                all_ok = False
            print(f"  [{flag}] vw={actual}  {repr(inside[:50])}")

print(f"\n12장 박스 전체 {'✓ 통과' if all_ok else '✗ 일부 실패'}")
