# finalize_dict_html.py
# 1) <code> 블록 내 <span class="comment"> 제거 + language-python 추가
# 2) h2.chap 헤딩에 앵커 링크 추가
# 3) </body> 앞에 Prism.js JS CDN 추가
import re, pathlib

HTML = pathlib.Path(r"c:\_proj\python_workspace\.study\blog\dict.html")
html = HTML.read_text(encoding="utf-8")

# ─────────────────────────────────────────────────────────────────────────────
# 1. Python code 블록: <pre><code>...<span class="comment">...</span>...</code></pre>
#    span 제거 후 class="language-python" 추가
#    (C 코드 블록 CH11 은 <span class="comment">이 있지만 language-python 달지 않음)
# ─────────────────────────────────────────────────────────────────────────────

def strip_comment_spans(code_text):
    """<span class="comment">...</span> 태그 제거 (내용은 보존)"""
    return re.sub(r'<span class="comment">(.*?)</span>', r'\1', code_text, flags=re.DOTALL)

# <pre><code> 블록 중 "// " 또는 "struct " 로 시작하는 줄이 없는 것만 Python으로 처리
def is_python_block(code_inner):
    first_lines = code_inner[:500]
    return not any(x in first_lines for x in ["struct ", "uint8_t", "#define DKIX", "Py_ssize_t", "PERTURB_SHIFT", "char       dk"])

count_py = 0
def process_code_block(m):
    global count_py
    inner = m.group(1)  # <code> 태그 내부 내용
    if is_python_block(inner):
        cleaned = strip_comment_spans(inner)
        count_py += 1
        return f'<pre><code class="language-python">{cleaned}</code></pre>'
    else:
        # C 블록: span 유지, language-c 만 추가
        return m.group(0)  # 변경 없음

html = re.sub(
    r'<pre><code(?! class)>(.*?)</code></pre>',
    process_code_block,
    html,
    flags=re.DOTALL
)
print(f"Python 코드블록 language-python 적용: {count_py}개")

# ─────────────────────────────────────────────────────────────────────────────
# 2. h2.chap 에 앵커 링크 추가
#    패턴: <section id="chN"> ... <h2 class="chap"><span class="num">CH NN</span>제목</h2>
# ─────────────────────────────────────────────────────────────────────────────

def add_anchor(m):
    ch_id = m.group(1)   # e.g. "ch1"
    heading = m.group(2) # h2 내부 텍스트
    if 'anchor-link' in heading:
        return m.group(0)  # 이미 있으면 skip
    # </h2> 앞에 앵커 삽입
    new_heading = heading.rstrip()
    if new_heading.endswith('</h2>'):
        new_heading = new_heading[:-5] + f'<a href="#{ch_id}" class="anchor-link">#</a></h2>'
    return f'<section id="{ch_id}">' + m.group(0)[m.group(0).index('<h2'):].__class__.__name__ and '' or '' + m.group(0).replace(heading, new_heading)

# 더 간단한 접근: section id 를 앞에서 찾아 h2 에 앵커 추가
count_anchor = 0
def add_section_anchor(m):
    global count_anchor
    ch_id = m.group(1)
    h2_content = m.group(2)
    if 'anchor-link' in h2_content:
        return m.group(0)
    new_h2 = h2_content + f'<a href="#{ch_id}" class="anchor-link">#</a>'
    count_anchor += 1
    return m.group(0).replace(h2_content, new_h2)

# <section id="chN"> 바로 뒤에 나오는 <h2 class="chap">...</h2> 찾기
html = re.sub(
    r'<section id="(ch\d+)">[^<]*<h2 class="chap">(<span[^>]*>CH[^<]*</span>[^<]*(?:<code>[^<]*</code>[^<]*)*)</h2>',
    add_section_anchor,
    html
)
print(f"앵커 링크 추가: {count_anchor}개")

# ─────────────────────────────────────────────────────────────────────────────
# 3. </body> 앞에 Prism.js JS 삽입
# ─────────────────────────────────────────────────────────────────────────────
PRISM_JS = '''  <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>'''

if 'prism-core.min.js' not in html:
    html = html.replace('</body>', PRISM_JS + '\n</body>')
    print("Prism.js JS 삽입 완료")
else:
    print("Prism.js JS 이미 있음")

HTML.write_text(html, encoding="utf-8")
print("저장 완료")
