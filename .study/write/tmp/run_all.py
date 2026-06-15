# run_all.py
# ================================================================
# dict.html 터미널 출력 재생성 스크립트
# 실행 방법:
#   c:\_proj\python_workspace\.venv\Scripts\python.exe run_all.py
#
# 순서:
#   1. dict_runner.py 실행 → logs/*.txt 생성
#   2. logs/*.txt 읽어서 dict.html 터미널 블록 교체
#   3. 잔여 pre 블록 버그 정리
#   4. 검증 결과 출력
# ================================================================
import re, pathlib, html as html_mod, subprocess, sys, datetime, shutil

BASE  = pathlib.Path(__file__).parent
BLOG  = BASE.parent / "blog" if (BASE.parent / "blog").exists() else BASE.parent.parent / ".study" / "blog"
ROOT  = pathlib.Path(r"c:\_proj\python_workspace\.study")
BLOG  = ROOT / "blog"
TEST  = ROOT / "test" / "2-dict"
LOGS  = TEST / "logs"
TMP   = BLOG / "tmp"
HTML  = BLOG / "dict.html"
RUNNER = TEST / "dict_runner.py"
PYTHON = pathlib.Path(r"c:\_proj\python_workspace\.venv\Scripts\python.exe")

TMP.mkdir(exist_ok=True)

log_lines = []
def log(msg):
    print(msg)
    log_lines.append(msg)

log(f"=== run_all.py 시작 {datetime.datetime.now()} ===\n")

# ── STEP 1: dict_runner.py 실행 ──────────────────────────────────────────
log("STEP 1: dict_runner.py 실행")
result = subprocess.run(
    [str(PYTHON), str(RUNNER)],
    cwd=str(TEST)
)
if result.returncode != 0:
    log("[ERROR] dict_runner.py 실행 실패")
    sys.exit(1)
log(f"  → logs/*.txt 생성 완료\n")

# ── STEP 2: logs/*.txt 읽기 ────────────────────────────────────────────────
SECTIONS = [
    "01_create", "02_access", "03_mutate", "04_views",
    "05_order",  "06_copy",   "07_merge",  "08_comprehension",
    "09_hash_sizeof", "10_employee", "11_runtime_error",
]
NUM_TO_SEC = {s[:2]: s for s in SECTIONS}

log("STEP 2: 로그 파일 읽기")
raw = {}
for sec in SECTIONS:
    p = LOGS / f"{sec}.txt"
    raw[sec] = p.read_text(encoding="utf-8") if p.exists() else ""
    log(f"  {sec}.txt: {len(raw[sec])} bytes")
log("")

# ── STEP 3: 터미널 블록 HTML 생성 ─────────────────────────────────────────
def make_body(text):
    result = []
    for line in text.splitlines():
        esc = html_mod.escape(line, quote=False)
        if re.fullmatch(r'=+', line.strip()):
            result.append(f'<span class="t-hdr">{esc}</span>')
        elif line.strip().startswith("# "):
            result.append(f'<span class="t-sec">{esc}</span>')
        elif re.search(r'(TypeError|RuntimeError|KeyError):', line):
            result.append(f'<span class="t-err">{esc}</span>')
        else:
            result.append(esc)
    return "\n".join(result)

def make_block(sec):
    num = sec.split("_")[0]
    label = f"dict_runner.py §{num} · Python 3.14.2 · PowerShell"
    body  = make_body(raw[sec])
    return (
        '  <div class="terminal">\n'
        '    <div class="terminal-header">\n'
        f'      <span class="t-label">{label}</span>\n'
        '    </div>\n'
        f'    <pre class="terminal-body">{body}</pre>\n'
        '  </div>'
    )

blocks = {sec: make_block(sec) for sec in SECTIONS}

# ── STEP 4: HTML 교체 ─────────────────────────────────────────────────────
log("STEP 3: dict.html 터미널 블록 교체")
html = HTML.read_text(encoding="utf-8")

# zero-width space 제거
zwsp = html.count("\u200b")
html = html.replace("\u200b", "")
log(f"  zero-width space 제거: {zwsp}개")

TERMINAL_PATTERN = re.compile(r'  <div class="terminal">.*?</div>(?=\s*\n)', re.DOTALL)
count = [0]

def replacer(m):
    block = m.group(0)
    lm = re.search(r'§(\d+)', block)
    if not lm:
        return block
    num = lm.group(1)
    sec = NUM_TO_SEC.get(num)
    if not sec:
        return block
    count[0] += 1
    log(f"  [교체] §{num} ({sec})")
    return blocks[sec]

html = TERMINAL_PATTERN.sub(replacer, html)
log(f"  총 교체: {count[0]}개\n")

# ── STEP 5: 잔여 pre 정리 ─────────────────────────────────────────────────
log("STEP 4: 잔여 orphan pre 정리")

# 4칸 들여쓰기 잔여
ORF4 = re.compile(r'  </div>\n    <pre class="terminal-body">.*?</pre>\n  </div>', re.DOTALL)
r4 = [0]
def rm4(m): r4[0] += 1; return '  </div>'
html = ORF4.sub(rm4, html)

# 0칸 들여쓰기 잔여
ORF0 = re.compile(r'  </div>\n<pre class="terminal-body">.*?</pre>\n  </div>', re.DOTALL)
r0 = [0]
def rm0(m): r0[0] += 1; return '  </div>'
html = ORF0.sub(rm0, html)

log(f"  잔여 제거 (4칸): {r4[0]}개  (0칸): {r0[0]}개\n")

# ── STEP 6: 저장 & 검증 ───────────────────────────────────────────────────
HTML.write_text(html, encoding="utf-8")
log(f"저장 완료: {HTML}\n")

log("=== 검증 ===")
div_c = html.count('<div class="terminal">')
pre_c = html.count('<pre class="terminal-body">')
ok = "✓" if div_c == pre_c == 11 else "✗"
log(f"{ok} div.terminal={div_c}  pre.terminal-body={pre_c}")

for sec in SECTIONS:
    lines = raw[sec].splitlines()
    sample = next((l.strip()[:50] for l in lines
                   if l.strip() and not l.strip().startswith("=") and not l.strip().startswith("#")), "")
    if sample:
        escaped = html_mod.escape(sample, quote=False)
        found = (sample in html) or (escaped in html)
        log(f"  §{sec}: '{sample[:40]}' → {'✓' if found else '✗ 불일치!'}")

# ── STEP 7: tmp 로그·파일 저장 ─────────────────────────────────────────────
combined = f"=== run_all.py {datetime.datetime.now()} ===\n\n"
for sec in SECTIONS:
    combined += f"{'='*60}\n# {sec}\n{'='*60}\n{raw[sec]}\n\n"
(TMP / "full_output.txt").write_text(combined, encoding="utf-8")

# 로그 파일 갱신
for sec in SECTIONS:
    p = LOGS / f"{sec}.txt"
    if p.exists():
        shutil.copy(p, TMP / f"{sec}.txt")

(TMP / "run_all_log.txt").write_text("\n".join(str(x) for x in log_lines), encoding="utf-8")
log(f"\nblog/tmp 갱신 완료")
log(f"=== 완료 {datetime.datetime.now()} ===")
