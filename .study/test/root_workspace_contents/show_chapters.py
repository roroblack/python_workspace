import re
files = [
  ('0511_intro', '.blog/day0511_mysql_intro.html'),
  ('0511_btree', '.blog/day0511_mysql_btree.html'),
  ('0512', '.blog/day0512_mysql_constraints.html'),
  ('0513', '.blog/day0513_mysql_select_join.html'),
]
for k, path in files:
    html = open(path, encoding='utf-8').read()
    lines = html.split('\n')
    print(f'\n=== {k} ===')
    for i, line in enumerate(lines):
        if 'class="chap"' in line:
            ctx = ' '.join(lines[i:i+5])
            title = re.sub(r'<[^>]+>', ' ', ctx)
            title = re.sub(r'\s+', ' ', title).strip()[:120]
            print(' ', title)
