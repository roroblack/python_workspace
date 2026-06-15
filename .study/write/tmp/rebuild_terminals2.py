# rebuild_terminals2.py — zero-width space 제거 + 전체 터미널 블록 교체
import re, pathlib, html as html_mod, datetime

BLOG = pathlib.Path(r"c:\_proj\python_workspace\.study\blog")
LOGS = pathlib.Path(r"c:\_proj\python_workspace\.study\test\2-dict\logs")
TMP  = BLOG / "tmp"
TMP.mkdir(exist_ok=True)

SECTIONS = [
    "01_create", "02_access", "03_mutate", "04_views",
    "05_order",  "06_copy",   "07_merge",  "08_comprehension",
    "09_hash_sizeof", "10_employee", "11_runtime_error",
]

NUM_TO_SEC = {f"{i+1:02d}": s for i, s in enumerate(SECTIONS)}
# 특수: 섹션 이름 맨 앞 2자리가 순서 번호
for s in SECTIONS:
    NUM_TO_SEC[s[:2]] = s

# ── 1. 로그 읽기 ──────────────────────────────────────────────────────────
raw = {}
for sec in SECTIONS:
    p = LOGS / f"{sec}.txt"
    raw[sec] = p.read_text(encoding="utf-8") if p.exists() else ""
    print(f"  [로그] {sec}.txt: {len(raw[sec])} bytes")

# ── 2. 터미널 body HTML 생성 ──────────────────────────────────────────────
def make_body(text):
    lines = text.splitlines()
    result = []
    for line in lines:
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
    num = sec.split("_")[0]  # "01", "02" ...
    label = f"dict_runner.py §{num} · Python 3.14.2 · PowerShell"
    body  = make_body(raw[sec])
    return (
        '  <div class="terminal">\n'
        '    <div class="terminal-header">\n'
        '      <span class="t-dot t-dot-r"></span>'
        '<span class="t-dot t-dot-y"></span>'
        '<span class="t-dot t-dot-g"></span>\n'
        f'      <span class="t-label">{label}</span>\n'
        '    </div>\n'
        f'    <pre class="terminal-body">{body}</pre>\n'
        '  </div>'
    )

blocks = {sec: make_block(sec) for sec in SECTIONS}

# ── 3. HTML 로드 → zero-width space 제거 ─────────────────────────────────
html_path = BLOG / "dict.html"
html = html_path.read_text(encoding="utf-8")
before_len = len(html)

# U+200B (zero-width space) 제거
html = html.replace("\u200b", "")
print(f"\nzero-width space 제거: {before_len - len(html)}자")

# ── 4. 터미널 블록 교체 (순서대로) ─────────────────────────────────────────
# 모든 <div class="terminal">...</div> 블록을 찾아서
# t-label의 섹션 번호로 대응하는 블록으로 교체
PATTERN = re.compile(r'  <div class="terminal">.*?</div>(?=\s*\n)', re.DOTALL)

matches_found = PATTERN.findall(html)
print(f"발견된 터미널 블록: {len(matches_found)}개")

count = 0
def replacer(m):
    global count
    block = m.group(0)
    # t-label에서 §NN 추출 (이제 zero-width space 없음)
    lm = re.search(r'§(\d+)', block)
    if not lm:
        print(f"  [skip] §번호 없음: {block[:60]!r}")
        return block
    num = lm.group(1)
    sec = NUM_TO_SEC.get(num)
    if not sec:
        print(f"  [skip] 알 수 없는 섹션 번호: §{num}")
        return block
    count += 1
    print(f"  [교체] §{num} ({sec})")
    return blocks[sec]

html = PATTERN.sub(replacer, html)
print(f"\n총 교체: {count}개")

# ── 5. 저장 ──────────────────────────────────────────────────────────────
html_path.write_text(html, encoding="utf-8")
print(f"저장 완료: {html_path}")

# ── 6. 검증 ──────────────────────────────────────────────────────────────
print("\n=== 검증 ===")
for sec in SECTIONS:
    lines = raw[sec].splitlines()
    sample = ""
    for l in lines:
        if l.strip() and not l.strip().startswith("=") and not l.strip().startswith("#"):
            sample = l.strip()[:50]
            break
    if sample:
        escaped = html_mod.escape(sample, quote=False)
        found = (sample in html) or (escaped in html)
        status = "✓" if found else "✗ 불일치!"
        print(f"  §{sec}: '{sample[:40]}' → {status}")

# ── 7. 로그 저장 ─────────────────────────────────────────────────────────
combined = f"=== rebuild_terminals2.py {datetime.datetime.now()} ===\n\n"
for sec in SECTIONS:
    combined += f"{'='*60}\n# {sec}\n{'='*60}\n{raw[sec]}\n\n"
(TMP / "full_output.txt").write_text(combined, encoding="utf-8")
print(f"\nblog/tmp/full_output.txt 갱신 완료")
print(f"zero-width space 제거된 HTML 저장 완료")
