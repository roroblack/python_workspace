from pathlib import Path
import re

html = Path(r'c:\_proj\python_workspace\.blog\day0511_mysql_btree.html').read_text('utf-8')

print('=== GUIDE §2 서사 사슬 구조 검증 ===')
sections = re.findall(r'<section id="(ch\d+)">(.*?)</section>', html, re.DOTALL)
print(f'총 챕터 수: {len(sections)}')

for sec_id, body in sections:
    has_qbox = 'class="qbox"' in body
    has_keypoint = 'class="keypoint"' in body
    has_bridge = 'class="bridge"' in body
    has_h3step = 'class="step"' in body
    has_cite = 'class="cite"' in body
    print(f'  {sec_id}: qbox={has_qbox} keypoint={has_keypoint} bridge={has_bridge} cite={has_cite}')

print()
print('=== GUIDE §4 CSS 팔레트 검증 ===')
for k in ['--accent: #52A97E', '--accent-2: #E8875A', '--accent-3: #5B9BD5', '--accent-4: #9178C4']:
    print(f'  {"✓" if k in html else "✗ MISSING"} {k}')

print()
print('=== GUIDE §5 터미널 블록 검증 ===')
mac_dot = html.count('t-dot-r') + html.count('t-dot-y') + html.count('t-dot-g')
print(f'맥 dot: {"✗ 발견" if mac_dot > 0 else "✓ 없음"} ({mac_dot}건)')
tb = html.count('class="terminal-body"')
th = html.count('class="terminal-header"')
print(f'terminal-header={th}, terminal-body={tb} 쌍 {"✓" if th == tb else "✗ 불일치"}')

print()
print('=== GUIDE §6 코드 블록 ===')
for lang in ['language-cpp', 'language-sql', 'language-python']:
    print(f'  {lang}: {html.count(lang)}개')

print()
print('=== GUIDE §7 챕터 h2 형식 ===')
h2s = re.findall(r'<h2 class="chap">(.*?)</h2>', html, re.DOTALL)
print(f'h2.chap: {len(h2s)}개')
for h in h2s:
    has_num = 'class="num"' in h
    has_anchor = 'class="anchor-link"' in h
    title = re.sub(r'<[^>]+>', '', h).strip()[:55]
    st = '✓' if has_num and has_anchor else '!'
    print(f'  {st} num={has_num} anchor={has_anchor} | {title}')

print()
print('=== 내용 사실 확인 ===')
facts = {
    'FIL Header (38B)': 'FIL Header (38B)' in html,
    'File Trailer (8B)': 'File Trailer (8B)' in html,
    '16KB 페이지': '16KB' in html,
    'B+Tree 분기 ~1000': '~1000' in html,
    'Innodb_buffer_pool_read_requests': 'Innodb_buffer_pool_read_requests' in html,
    'Using index (커버링)': 'Using index' in html,
    'right-only split': 'right-only split' in html,
    'dict_table_t::autoinc': 'dict_table_t::autoinc' in html,
    'btr0cur.cc': 'btr0cur.cc' in html,
    'EXPLAIN ANALYZE': 'EXPLAIN ANALYZE' in html,
    'innodb_buffer_pool_size': 'innodb_buffer_pool_size' in html,
}
for k, v in facts.items():
    print(f'  {"✓" if v else "✗ MISSING"} {k}')

print()
print('=== blockquote.cite 인용 수 ===')
cites = re.findall(r'<blockquote class="cite">(.*?)</blockquote>', html, re.DOTALL)
print(f'  총 인용: {len(cites)}개')
for c in cites:
    src = re.search(r'<span class="src">(.*?)</span>', c, re.DOTALL)
    src_text = re.sub(r'<[^>]+>', '', src.group(1)).strip()[:60] if src else '(없음)'
    print(f'  - {src_text}')

print()
print('=== ASCII 박스 수 ===')
ascii_divs = re.findall(r'<div class="ascii">', html)
print(f'  총 .ascii 박스: {len(ascii_divs)}개')

print('\n=== CH13 신규 챕터 구조 확인 ===')
ch13_match = re.search(r'<section id="ch13">(.*?)</section>', html, re.DOTALL)
if ch13_match:
    body = ch13_match.group(1)
    print(f'  길이: {len(body):,}자')
    # 커버링 인덱스, 복합 인덱스, Buffer Pool 히트율 포함 여부
    checks = ['커버링 인덱스', 'EXPLAIN', 'innodb_buffer_pool', '복합 인덱스', 'Using index']
    for c in checks:
        print(f'  {"✓" if c in body else "✗"} {c}')
