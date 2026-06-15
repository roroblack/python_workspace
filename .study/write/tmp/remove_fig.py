from pathlib import Path
import re
html = Path(r'c:\_proj\python_workspace\.blog\day0511_mysql_btree.html').read_text('utf-8')
# Remove the previously inserted figure block (if any)
new_html = re.sub(r'\n  <figure style="margin:24px 0.*?</figure>\n', '\n', html, flags=re.DOTALL)
if len(new_html) != len(html):
    Path(r'c:\_proj\python_workspace\.blog\day0511_mysql_btree.html').write_text(new_html, 'utf-8')
    print(f'제거 완료 ({len(new_html)//1024}KB)')
else:
    print(f'이미 없음 ({len(html)//1024}KB)')
