from pathlib import Path
import re

html = Path(r'C:\_proj\python_workspace\.blog\day0511_mysql_btree.html').read_text(encoding='utf-8')

# 모든 section id 찾기
sections = [(m.start(), m.group()) for m in re.finditer(r'<section id="[^"]+">', html)]
for pos, tag in sections:
    print(f'pos {pos:8d} : {tag}')

print(f'\n총 파일 길이: {len(html)}')
print('\n=== 파일 끝 500자 ===')
print(repr(html[-500:]))
