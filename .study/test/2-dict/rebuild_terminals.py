# rebuild_terminals.py
# logs/*.txt 의 실제 내용을 읽어서 dict.html 의 모든 터미널 블록을 교체한다.
# 모든 과정을 blog/tmp/rebuild_log.txt 에 기록한다.

import re, pathlib, html as html_mod, sys, datetime

BLOG = pathlib.Path(r"c:\_proj\python_workspace\.study\blog")
LOGS = pathlib.Path(r"c:\_proj\python_workspace\.study\test\2-dict\logs")
TMP  = BLOG / "tmp"
TMP.mkdir(exist_ok=True)

log_lines = []

def log(msg):
    print(msg)
    log_lines.append(msg)

log(f"=== rebuild_terminals.py 실행 시각: {datetime.datetime.now()} ===")
log(f"logs 폴더: {LOGS}")
log("")

# ── 1. 로그 파일 읽기 ──────────────────────────────────────────────────────
SECTIONS = [
    "01_create",
    "02_access",
    "03_mutate",
    "04_views",
    "05_order",
    "06_copy",
    "07_merge",
    "08_comprehension",
    "09_hash_sizeof",
    "10_employee",
    "11_runtime_error",
]

raw = {}
for sec in SECTIONS:
    p = LOGS / f"{sec}.txt"
    if p.exists():
        text = p.read_text(encoding="utf-8")
        raw[sec] = text
        log(f"[읽기 OK] {sec}.txt  ({len(text)} bytes)")
    else:
        log(f"[읽기 실패] {sec}.txt 없음")
        raw[sec] = ""

log("")

# ── 2. 터미널 블록 HTML 생성 ───────────────────────────────────────────────
# 특수 처리: t-hdr / t-sec / t-err 스팬

def escape(s):
    return html_mod.escape(s, quote=False)

def make_terminal_body(sec_name, text):
    """
    로그 텍스트를 terminal-body 내부 HTML로 변환.
    - ===...=== 줄 → t-hdr
    - # 로 시작하는 줄 → t-sec
    - RuntimeError: / TypeError: 포함 줄 → t-err
    - 나머지 → 그대로 escape
    """
    lines = text.splitlines()
    result = []
    for line in lines:
        esc = escape(line)
        if re.fullmatch(r'=+', line.strip()):
            result.append(f'<span class="t-hdr">{esc}</span>')
        elif line.strip().startswith("# "):
            result.append(f'<span class="t-sec">{esc}</span>')
        elif re.search(r'(TypeError|RuntimeError|KeyError):', line):
            result.append(f'<span class="t-err">{esc}</span>')
        else:
            result.append(esc)
    return "\n".join(result)

def make_terminal_div(label, body_html):
    return (
        '  <div class="terminal">\n'
        '    <div class="terminal-header">\n'
        '      <span class="t-dot t-dot-r"></span>'
        '<span class="t-dot t-dot-y"></span>'
        '<span class="t-dot t-dot-g"></span>\n'
        f'      <span class="t-label">{label}</span>\n'
        '    </div>\n'
        f'    <pre class="terminal-body">{body_html}</pre>\n'
        '  </div>'
    )

# 챕터별 라벨과 대응하는 섹션 이름
CHAPTER_MAP = [
    # (섹션명,           라벨)
    ("01_create",        "dict_runner.py §01 · Python 3.14.2 · PowerShell"),
    ("02_access",        "dict_runner.py §02 · Python 3.14.2 · PowerShell"),
    ("03_mutate",        "dict_runner.py §03 · Python 3.14.2 · PowerShell"),
    ("04_views",         "dict_runner.py §04 · Python 3.14.2 · PowerShell"),
    ("05_order",         "dict_runner.py §05 · Python 3.14.2 · PowerShell"),
    ("06_copy",          "dict_runner.py §06 · Python 3.14.2 · PowerShell"),
    ("07_merge",         "dict_runner.py §07 · Python 3.14.2 · PowerShell"),
    ("08_comprehension", "dict_runner.py §08 · Python 3.14.2 · PowerShell"),
    ("09_hash_sizeof",   "dict_runner.py §09 · Python 3.14.2 · PowerShell"),
    ("10_employee",      "dict_runner.py §10 · Python 3.14.2 · PowerShell"),
    ("11_runtime_error", "dict_runner.py §11 · Python 3.14.2 · PowerShell"),
]

# 각 섹션에 대해 생성할 새 터미널 블록 저장
new_blocks = {}
for sec, label in CHAPTER_MAP:
    body = make_terminal_body(sec, raw[sec])
    new_blocks[sec] = make_terminal_div(label, body)

# ── 3. HTML에서 기존 터미널 블록 교체 ─────────────────────────────────────
html_path = BLOG / "dict.html"
html = html_path.read_text(encoding="utf-8")

# 터미널 div 패턴: <div class="terminal">...</div>
# t-label 텍스트로 어느 섹션인지 구분
PATTERN = re.compile(
    r'  <div class="terminal">.*?</div>\s*\n?',
    re.DOTALL
)

matches = PATTERN.findall(html)
log(f"HTML에서 발견된 터미널 블록: {len(matches)}개")
for i, m in enumerate(matches):
    # t-label 에서 섹션 번호 추출
    label_m = re.search(r't-label.*?§(\d+)', m)
    sec_num = label_m.group(1) if label_m else "??"
    log(f"  [{i+1}] §{sec_num} — {len(m)}자")

# 섹션 번호 → 섹션명 매핑
NUM_TO_SEC = {
    "01": "01_create", "02": "02_access", "03": "03_mutate",
    "04": "04_views",  "05": "05_order",  "06": "06_copy",
    "07": "07_merge",  "08": "08_comprehension",
    "09": "09_hash_sizeof", "10": "10_employee", "11": "11_runtime_error",
}

replace_count = 0
def replacer(m):
    global replace_count
    block = m.group(0)
    label_m = re.search(r't-label[^>]*>dict_runner\.py §(\d+)', block)
    if not label_m:
        return block
    num = label_m.group(1)
    sec = NUM_TO_SEC.get(num)
    if not sec or sec not in new_blocks:
        return block
    replace_count += 1
    log(f"  교체: §{num} ({sec})")
    return new_blocks[sec] + "\n"

new_html = PATTERN.sub(replacer, html)
log(f"\n총 교체: {replace_count}개")

# ── 4. 저장 ───────────────────────────────────────────────────────────────
html_path.write_text(new_html, encoding="utf-8")
log(f"저장 완료: {html_path}")

# ── 5. 검증 ───────────────────────────────────────────────────────────────
log("\n=== 검증 ===")
remaining_figure = new_html.count('figure class="shot"')
terminal_count = new_html.count('<div class="terminal">')
log(f"figure.shot 잔여: {remaining_figure}")
log(f"terminal 블록 수: {terminal_count}")

# 각 섹션 텍스트가 실제로 들어있는지 확인
for sec, _ in CHAPTER_MAP:
    # 첫 번째 실제 출력 줄 (헤더 제외) 확인
    lines = raw[sec].splitlines()
    # === / # 줄 건너뛰고 첫 데이터 줄 찾기
    sample = ""
    for l in lines:
        if l.strip() and not l.strip().startswith("=") and not l.strip().startswith("#"):
            sample = l.strip()[:40]
            break
    if sample:
        found = sample in new_html or html_mod.escape(sample) in new_html
        log(f"  §{sec}: '{sample}' → {'✓ 있음' if found else '✗ 없음 (불일치!)'}")

# ── 6. 로그 파일 저장 ──────────────────────────────────────────────────────
log_text = "\n".join(log_lines)
(TMP / "rebuild_log.txt").write_text(log_text, encoding="utf-8")

# 실제 실행 텍스트 전체 저장 (참고용)
combined = ""
for sec in SECTIONS:
    combined += f"{'='*60}\n# {sec}\n{'='*60}\n"
    combined += raw.get(sec, "(없음)") + "\n\n"
(TMP / "full_output.txt").write_text(combined, encoding="utf-8")
print(f"\nblog/tmp 에 저장된 파일:")
for f in sorted(TMP.iterdir()):
    print(f"  {f.name}  ({f.stat().st_size} bytes)")
