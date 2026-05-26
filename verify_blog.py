import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\_proj\python_workspace\.blog\day0511_mysql_intro.html', encoding='utf-8') as f:
    content = f.read()

checks = [
    ('TOC ch4 B+Tree', '#ch4">PRIMARY KEY'),
    ('TOC ch5 ALTER', '#ch5">ALTER / DROP'),
    ('TOC ch6 INSERT', '#ch6">INSERT'),
    ('TOC ch7 final', '#ch7">최종 결론'),
    ('intro bridge CH06/CH07', 'CH01 ~ CH06'),
    ('CH03 bridge PK', 'B+Tree 성능 설계'),
    ('CH04 section id', 'id="ch4"'),
    ('CH04 title', 'PRIMARY KEY'),
    ('CH04 AUTO_INCREMENT', 'AUTO_INCREMENT PRIMARY KEY'),
    ('CH04 LAST_INSERT_ID', 'LAST_INSERT_ID()'),
    ('CH04 B+tree diagram', 'Root Node'),
    ('CH04 Clustered quote', 'GEN_CLUST_INDEX'),
    ('CH04 nextval', 'nextval'),
    ('CH04 GAP 현상', 'GAP 현상'),
    ('CH05 section id', 'id="ch5"'),
    ('CH05 ALTER/DROP', 'ALTER / DROP'),
    ('CH06 section id', 'id="ch6"'),
    ('CH07 section id', 'id="ch7"'),
    ('table PK row', 'B+Tree Clustered Index O(log n)'),
    ('qbox 여섯 챕터', 'DAY1 여섯 챕터 모두'),
    ('final 여섯 챕터를', '여섯 챕터를 그 한 줄로'),
    ('final CH04 무작위', 'CH04</strong> 무작위 PK'),
    ('final CH05 존재', 'CH05</strong> 존재하지 않는'),
    ('final CH06 부재', 'CH06</strong>'),
    ('footer innodb', 'innodb-index-types'),
]

ok = 0
fail = 0
for name, needle in checks:
    if needle in content:
        print(f'  OK   {name}')
        ok += 1
    else:
        print(f'  FAIL {name}  (missing: {repr(needle)})')
        fail += 1

print(f'\n{ok} OK, {fail} FAIL')
