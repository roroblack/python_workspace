# run_all_abstraction.py
# abstraction.html 의 터미널 블록을 실제 실행 결과로 교체하는 스크립트
# 실행: & "c:\_proj\python_workspace\.venv\Scripts\python.exe" "c:\_proj\python_workspace\.study\blog\tmp\run_all_abstraction.py"

import subprocess, sys, re, pathlib

PYTHON   = r"c:\_proj\python_workspace\.venv\Scripts\python.exe"
RUNNER   = r"c:\_proj\python_workspace\.study\test\3-abstraction\abstraction_runner.py"
LOGS_DIR = pathlib.Path(r"c:\_proj\python_workspace\.study\test\3-abstraction\logs")
HTML     = pathlib.Path(r"c:\_proj\python_workspace\.study\blog\abstraction.html")

SECTIONS = [
    "00_vtable_vs_python",
    "01_duck_typing",
    "02_abc_basic",
    "03_abc_decorators",
    "04_protocol",
    "05_abc_vs_protocol",
    "06_internals",
    "07_payment_system",
    "08_bootcamp_link",
]

# ── 1. runner 실행 ──────────────────────────────────────────────────────────
print("=== abstraction_runner.py 실행 중 ===")
result = subprocess.run(
    [PYTHON, RUNNER],
    capture_output=True, text=True, encoding="utf-8", errors="replace"
)
if result.returncode != 0:
    print("[STDERR]", result.stderr)
    sys.exit(1)
print(result.stdout)
print("=== runner 완료 ===\n")

# ── 2. HTML 로드 ────────────────────────────────────────────────────────────
html = HTML.read_text(encoding="utf-8")
html = html.replace('\u200b', '')   # zero-width space 제거

# ── 3. 로그 → HTML 터미널 블록 교체 ─────────────────────────────────────────
def read_log_body(name: str) -> str:
    """로그에서 헤더(=== # name ===) 제거 후 본문만 반환"""
    txt = (LOGS_DIR / f"{name}.txt").read_text(encoding="utf-8")
    lines = txt.splitlines()
    # 첫 3줄이 === / # name / === 헤더이므로 제거
    body_lines = lines[3:]
    return "\n".join(body_lines)

def escape_html(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

for name in SECTIONS:
    raw_body = read_log_body(name)

    # t-err 처리: TypeError:, AttributeError: 포함 줄에 색상 스팬 적용
    colored_lines = []
    for line in raw_body.splitlines():
        if re.search(r'(TypeError|AttributeError|RuntimeError|ValueError):', line):
            colored_lines.append(f'<span class="t-err">{escape_html(line)}</span>')
        else:
            colored_lines.append(escape_html(line))
    colored_body = "\n".join(colored_lines)

    # 기존 pre.terminal-body 교체 or 없으면 삽입 (damaged HTML 복구 포함)
    # (?:...) 로 pre 부분을 optional 처리 → fresh HTML / damaged HTML 모두 대응
    pattern = (
        r'(<div class="terminal-header"><span class="t-label">'
        + re.escape(name) +
        r'</span></div>)'
        r'(?:\s*<pre class="terminal-body">.*?</pre>)?'
    )
    new_pre = f'<pre class="terminal-body">{colored_body}</pre>'
    replacement = r'\g<1>' + '\n  ' + new_pre
    new_html, count = re.subn(pattern, replacement, html, flags=re.DOTALL)

    if count == 0:
        print(f"[WARN] 섹션 '{name}' 을 HTML에서 찾지 못했습니다.")
    else:
        html = new_html
        print(f"[OK] {name} 교체 완료")

# ── 4. orphan <pre> 정리 ────────────────────────────────────────────────────
# abstraction.html은 신규 파일이므로 orphan 발생 가능성이 있는 경우만 정리:
# 터미널 헤더 div가 닫힌 직후, pre.terminal-body가 .terminal div 바깥에 있는 경우
# 구조: </div>\n</div>\n<pre class="terminal-body"> → 잔여물 제거
html = re.sub(
    r'(</div>\n</div>)\s*<pre class="terminal-body">.*?</pre>',
    r'\1',
    html, flags=re.DOTALL
)

# ── 5. HTML 저장 ────────────────────────────────────────────────────────────
HTML.write_text(html, encoding="utf-8")
print(f"\n[SAVED] {HTML}")

# ── 6. 검증 ─────────────────────────────────────────────────────────────────
term_count = html.count('class="terminal"')
body_count = html.count('class="terminal-body"')
print(f"\n=== 검증 ===")
print(f"div.terminal      : {term_count}")
print(f"pre.terminal-body : {body_count}")
if term_count == body_count == len(SECTIONS):
    print(f"[PASS] 모두 {len(SECTIONS)}개로 일치")
else:
    print(f"[WARN] 불일치! sections={len(SECTIONS)}, terminal={term_count}, body={body_count}")

zw = html.count('\u200b')
print(f"zero-width space  : {zw}")
mac_dots = html.count('t-dot-r')
print(f"Mac dots          : {mac_dots}")
print("=== 검증 완료 ===")
