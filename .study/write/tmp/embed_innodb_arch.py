import base64, pathlib

data = pathlib.Path(r'C:\_proj\python_workspace\.study\blog\img\innodb-architecture.png').read_bytes()
b64 = base64.b64encode(data).decode()

html_path = pathlib.Path(r'C:\_proj\python_workspace\.blog\day0511_mysql_btree.html')
html = html_path.read_text(encoding='utf-8')

OLD = '    <img src="https://dev.mysql.com/doc/refman/8.0/en/images/innodb-architecture.png"'
NEW = f'    <img src="data:image/png;base64,{b64}"'

if OLD in html:
    html = html.replace(OLD, NEW, 1)
    html_path.write_text(html, encoding='utf-8')
    print(f"교체 완료. src 길이: {len(NEW)}")
else:
    print("패턴 없음 — 현재 src 확인:")
    idx = html.find('innodb-architecture')
    print(repr(html[idx-50:idx+80]) if idx != -1 else "없음")
