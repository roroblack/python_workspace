# §12 검증 스크립트 — retrospective_w5.html
import re, pathlib
p = pathlib.Path(r"c:\_proj\python_workspace\.study\blog\retrospective_w5.html")
h = p.read_text(encoding="utf-8")

http_img = re.findall(r'<img[^>]+src="https?://', h)
b64_img  = h.count('src="data:image/')
zwsp     = h.count('​')
figshot  = h.count('figure.shot') + len(re.findall(r'<figure class="shot"', h))
placeholders = re.findall(r'@@[A-Z0-9_]+@@', h) + re.findall(r'(TODO|TBD|PLACEHOLDER|\bXXX\b)', h)
notes_leak = re.findall(r'\.study[\\/]notes', h)
chaps    = h.count('h2 class="chap"')
anchors  = len(re.findall(r'<h2 class="chap">.*?class="anchor-link"', h, re.S))
qbox     = h.count('class="qbox"')
keypoint = h.count('class="keypoint"')
prism_css = 'prism-tomorrow.min.css' in h
prism_js  = 'prism-core.min.js' in h and 'prism-autoloader.min.js' in h
seo = all(s in h for s in ['name="description"','property="og:title"','name="twitter:card"'])
term_div = h.count('<div class="terminal">')
term_body = h.count('class="terminal-body"')

print("=== retrospective_w5.html §12 검증 ===")
print(f"외부 URL img       : {len(http_img)}  (0이어야 함) {'OK' if not http_img else 'FAIL'}")
print(f"base64 img         : {b64_img}")
print(f"zero-width space   : {zwsp}  {'OK' if zwsp==0 else 'FAIL'}")
print(f"figure.shot 잔여   : {figshot}  (없어야 함) {'OK' if figshot==0 else 'FAIL'}")
print(f"미치환 placeholder : {placeholders}  {'OK' if not placeholders else 'FAIL'}")
print(f".study/notes 누출  : {notes_leak}  {'OK' if not notes_leak else 'FAIL'}")
print(f"챕터 수            : {chaps}  | 앵커링크: {anchors}  {'OK' if chaps==anchors else 'FAIL'}")
print(f"qbox / keypoint    : {qbox} / {keypoint}")
print(f"terminal div/body  : {term_div} / {term_body}  {'OK' if term_div==term_body else 'FAIL'}")
print(f"Prism css / js     : {prism_css} / {prism_js}  {'OK' if prism_css and prism_js else 'FAIL'}")
print(f"SEO 메타           : {seo}  {'OK' if seo else 'FAIL'}")
print(f"파일 크기          : {len(h)//1024} KB")
