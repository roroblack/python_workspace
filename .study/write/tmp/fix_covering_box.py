"""
Task 1: Fix the two-column ASCII box for 커버링 인덱스 comparison.
         Old system: N=38 dashes, ─=1 unit → inner=38 (WRONG)
         New system: N=22 dashes, ─=2 units → inner=44 (max_content_vw=32)
"""
from pathlib import Path
import re

# ─── Visual width function ────────────────────────────────────────
def vw(s: str) -> int:
    return sum(1 if ord(c) < 128 else 2 for c in s)

# ─── Box builder ─────────────────────────────────────────────────
N       = 22       # number of ─ per box  →  inner visual = N×2 = 44
TARGET  = N * 2    # = 44
GAP     = '    '   # 4 ASCII spaces between boxes

def bl(left: str, right: str) -> str:
    """Build a single content line:  '  │{left_pad}│    │{right_pad}│' """
    lp = ' ' * max(0, TARGET - vw(left))
    rp = ' ' * max(0, TARGET - vw(right))
    return f'  │{left}{lp}│{GAP}│{right}{rp}│'

top    = f'  ┌{"─"*N}┐{GAP}┌{"─"*N}┐'
sep    = f'  ├{"─"*N}┤{GAP}├{"─"*N}┤'
bottom = f'  └{"─"*N}┘{GAP}└{"─"*N}┘'
empty  = bl('', '')

# ─── Box content ─────────────────────────────────────────────────
lines = [
    top,
    bl('  일반 조회 (idx_name만 있을 때)',   '  커버링 인덱스 (idx_name_email)'),
    bl('  (Secondary Index + 2-step)',       '  (Covering Index — 1-step)'),
    empty,
    bl('  WHERE name = \'alice\'',            '  WHERE name = \'alice\''),
    bl('         │',                          '         │'),
    bl('         ▼',                          '         ▼'),
    bl('  [Secondary Index Leaf]',            '  [Secondary Index Leaf]'),
    bl('  (name, PK) 발견',                   '  (name, email, PK) → 완결!'),
    bl('         │  Extra: Using where',      '  Extra: Using index  OK'),
    bl('         ▼',                          '  클러스터드 인덱스 재조회 없음'),
    bl('  [Clustered Index Leaf]',            ''),
    bl('  PK 로 full row 재조회',             '  I/O 횟수: 1회'),
    bl('  I/O 횟수: 2회',                     ''),
    bottom,
]

# ─── Verification ────────────────────────────────────────────────
print(f'N={N}, TARGET={TARGET}')
print()
print('=== 생성된 박스 ===')
for ln in lines:
    line_vw = vw(ln)
    print(f'vw={line_vw:3d} │ {ln}')

# Verify all lines same visual width
widths = [vw(ln) for ln in lines]
assert len(set(widths)) == 1, f'불일치: {set(widths)}'
print(f'\n모든 줄 vw={widths[0]} ✓')

# ─── Build replacement text ───────────────────────────────────────
new_box_inner = '\n'.join(lines)

# ─── Replace in HTML ─────────────────────────────────────────────
HTML = Path(r'c:\_proj\python_workspace\.blog\day0511_mysql_btree.html')
html = HTML.read_text('utf-8')

# Find the existing ASCII block for 커버링 인덱스 comparison
# It's inside <div class="ascii">[ 일반 보조 인덱스 조회 vs 커버링...
pattern = r'(<div class="ascii">\[ 일반 보조 인덱스 조회 vs 커버링 인덱스 조회 \]\n\n)(.*?)(\n</div>)'
m = re.search(pattern, html, re.DOTALL)
if not m:
    print('ERROR: 박스를 찾지 못했습니다')
    exit(1)

old_body = m.group(2)
print(f'\n[교체 전 줄 수] {len(old_body.splitlines())}줄')

new_html = html[:m.start()] + m.group(1) + new_box_inner + m.group(3) + html[m.end():]
HTML.write_text(new_html, 'utf-8')
print(f'[저장] {HTML} ({HTML.stat().st_size // 1024}KB)')
