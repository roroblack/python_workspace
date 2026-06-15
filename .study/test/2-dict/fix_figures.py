# fix_figures.py — 남은 figure.shot 3개를 terminal 블록으로 교체
import re, pathlib

HTML = pathlib.Path(r"c:\_proj\python_workspace\.study\blog\dict.html")
html = HTML.read_text(encoding="utf-8")

TERMINAL_WRAPPER = """\
  <div class="terminal">
    <div class="terminal-header">
      <span class="t-dot t-dot-r"></span><span class="t-dot t-dot-y"></span><span class="t-dot t-dot-g"></span>
      <span class="t-label">{label}</span>
    </div>
    <pre class="terminal-body">{body}</pre>
  </div>"""

BODIES = {
    "dict_10_employee": (
        "dict_runner.py §10 · Python 3.14.2 · PowerShell",
        """\
<span class="t-hdr">============================================================</span>
<span class="t-sec"># 10_employee</span>
<span class="t-hdr">============================================================</span>
&gt;&gt; 전체 출력
  200 : ['홍길순', '851225-2234567', 'hong@test.com', '010-1234-5678', 3800000, '대리', '개발부']
  201 : ['김철수', '900101-1234567', 'kim@test.com', '010-2222-3333', 4200000, '과장', '개발부']
  202 : ['이영희', '920510-2345678', 'lee@test.com', '010-7777-8888', 3500000, '사원', '기획부']
&gt;&gt; 201 삭제 후
  200 : ['홍길순', '851225-2234567', 'hong@test.com', '010-1234-5678', 3800000, '대리', '개발부']
  202 : ['이영희', '920510-2345678', 'lee@test.com', '010-7777-8888', 3500000, '사원', '기획부']
&gt;&gt; pickle round-trip 동등성: True
&gt;&gt; 불러온 키 목록      : ['200', '202']"""
    ),
    "dict_11_runtime_error": (
        "dict_runner.py §11 · Python 3.14.2 · PowerShell",
        """\
<span class="t-hdr">============================================================</span>
<span class="t-sec"># 11_runtime_error</span>
<span class="t-hdr">============================================================</span>
<span class="t-err">RuntimeError: dictionary changed size during iteration</span>"""
    ),
    "dict_09_hash_sizeof": (
        "dict_runner.py §09 · Python 3.14.2 · PowerShell",
        """\
<span class="t-hdr">============================================================</span>
<span class="t-sec"># 09_hash_sizeof</span>
<span class="t-hdr">============================================================</span>
len -&gt; sys.getsizeof(dict)
  len= 0  size=64 bytes
  len= 1  size=224 bytes
  len= 2  size=224 bytes
  len= 3  size=224 bytes
  len= 4  size=224 bytes
  len= 5  size=224 bytes
  len= 6  size=352 bytes
  len= 7  size=352 bytes
  len= 8  size=352 bytes
  len= 9  size=352 bytes
  len=10  size=352 bytes
  len=11  size=632 bytes
  len=12  size=632 bytes
  len=13  size=632 bytes
  len=14  size=632 bytes
  len=15  size=632 bytes
  len=16  size=632 bytes
hash('python') = -217981081291864475
hash(42)       = 42
hash((1,2,3))  = 529344067295497451
<span class="t-err">hash(list) -&gt; TypeError: unhashable type: 'list'</span>"""
    ),
}

for img_stem, (label, body) in BODIES.items():
    pattern = (
        r'  <figure class="shot">\s*'
        r'<img src="img/' + re.escape(img_stem) + r'\.png"[^>]*/>\s*'
        r'<figcaption>.*?</figcaption>\s*'
        r'</figure>'
    )
    replacement = TERMINAL_WRAPPER.format(label=label, body=body)
    before = html.count('<figure class="shot">')
    html = re.sub(pattern, replacement, html, flags=re.DOTALL)
    after = html.count('<figure class="shot">')
    print(f"{img_stem}: {before} → {after} (교체 {'성공' if before>after else '실패'})")

HTML.write_text(html, encoding="utf-8")
total = html.count('<figure class="shot">')
print(f"\n최종 남은 figure.shot: {total}")
