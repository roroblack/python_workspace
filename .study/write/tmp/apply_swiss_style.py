"""
apply_swiss_style.py
모든 blog HTML 파일에 Swiss International Style CSS 를 일괄 적용
"""
import re, pathlib

BLOG = pathlib.Path(r"c:\_proj\python_workspace\.study\blog")

# ──────────────────────────────────────────────
# 공통 치환 규칙  (old, new)  — 단순 문자열 대체
# ──────────────────────────────────────────────
SIMPLE = [
    # 1. 배경 크림색 → 순수 흰색
    ("--paper: #fbfaf7;",   "--paper: #ffffff;"),

    # 2. 그림자 제거
    ("--shadow: 0 14px 32px rgba(31, 41, 51, 0.08);", "--shadow: none;"),

    # 3. header 그라디언트 → 흰 배경 + 굵은 테두리
    (
        "background: linear-gradient(180deg, #ffffff 0%, #f4f7f9 100%);\n"
        "      border-bottom: 1px solid var(--line);",
        "background: #ffffff;\n"
        "      border-bottom: 3px solid var(--ink);"
    ),

    # 4. pre 코드블록: 각진 모서리 + 그림자 제거
    (
        "      border-radius: 8px;\n"
        "      padding: 18px 20px;\n"
        "      font-size: 0.9rem;\n"
        "      line-height: 1.6;\n"
        "      tab-size: 4;\n"
        "      box-shadow: var(--shadow);",
        "      border-radius: 0;\n"
        "      padding: 18px 20px;\n"
        "      font-size: 0.9rem;\n"
        "      line-height: 1.6;\n"
        "      tab-size: 4;\n"
        "      box-shadow: none;"
    ),

    # 5. terminal 컨테이너: 각진 + 그림자 제거 + 테두리 추가
    (
        "      border-radius: 8px;\n"
        "      overflow: hidden;\n"
        "      box-shadow: var(--shadow);",
        "      border-radius: 0;\n"
        "      overflow: hidden;\n"
        "      box-shadow: none;\n"
        "      border: 1px solid #30363d;"
    ),

    # 6. terminal-body 각진 모서리
    ("border-radius: 0 0 8px 8px;", "border-radius: 0;"),

    # 7. qbox/keypoint/callout 각진
    (
        "    .qbox, .keypoint, .callout {\n"
        "      border-radius: 8px;",
        "    .qbox, .keypoint, .callout {\n"
        "      border-radius: 0;"
    ),

    # 8. chapter 번호 배지: 각진 + 테두리 두껍게
    (
        "      border: 1px solid var(--accent);\n"
        "      border-radius: 4px;",
        "      border: 2px solid var(--accent);\n"
        "      border-radius: 0;"
    ),

    # 9. inline code 각진
    (
        "      border-radius: 4px;\n"
        "      padding: 1px 6px;",
        "      border-radius: 0;\n"
        "      padding: 1px 6px;"
    ),

    # 10. TOC 각진 + 상단 굵은 선
    (
        "      border: 1px solid var(--line);\n"
        "      border-radius: 8px;\n"
        "      padding: 18px 22px;",
        "      border: 1px solid var(--line);\n"
        "      border-top: 3px solid var(--ink);\n"
        "      border-radius: 0;\n"
        "      padding: 18px 22px;"
    ),

    # 11. ASCII 다이어그램 각진
    (
        "      border-radius: 8px;\n"
        "      font-family: \"Cascadia Code\", \"Consolas\", monospace;",
        "      border-radius: 0;\n"
        "      font-family: \"Cascadia Code\", \"Consolas\", monospace;"
    ),

    # 12. meta-row 테두리 강화
    ("border-top: 1px solid var(--line);", "border-top: 2px solid var(--ink);"),
]

# ──────────────────────────────────────────────
# 정규식 치환 — h2.chap 에 상단 굵은 선 추가
# ──────────────────────────────────────────────
H2_OLD = r"(    h2\.chap \{)\n(      margin: \d+px 0 \d+px;)"
H2_NEW = (
    r"\1\n"
    r"      border-top: 3px solid var(--ink);\n"
    r"      padding-top: 16px;\n"
    r"\2"
)

# eyebrow 에 상단 색상 선 추가
EYEBROW_OLD = r"(\.cover \.eyebrow \{)"
EYEBROW_NEW = (
    r"\1\n"
    r"      border-top: 4px solid var(--accent);\n"
    r"      padding-top: 10px;\n"
    r"      display: inline-block;"
)

# ──────────────────────────────────────────────
# h2.chap margin 값이 파일마다 다를 수 있어서
# 범용 정규식으로 처리
# ──────────────────────────────────────────────
def apply(path: pathlib.Path):
    if not path.exists():
        print(f"[SKIP] {path.name} — not found")
        return

    html = path.read_text(encoding="utf-8")
    original = html

    # 단순 치환
    for old, new in SIMPLE:
        html = html.replace(old, new)

    # h2.chap 상단 선 추가 (아직 추가 안 된 경우만)
    if "border-top: 3px solid var(--ink);" not in html.split("h2.chap")[1].split("}")[0] if "h2.chap" in html else True:
        html = re.sub(H2_OLD, H2_NEW, html)

    # eyebrow 상단 선 (아직 없는 경우만)
    if "border-top: 4px solid var(--accent)" not in html:
        html = re.sub(EYEBROW_OLD, EYEBROW_NEW, html)

    if html == original:
        print(f"[NOCHANGE] {path.name}")
    else:
        path.write_text(html, encoding="utf-8")
        print(f"[OK] {path.name} 적용 완료")


# ──────────────────────────────────────────────
# interpreter.html 전용 추가 치환
# (qbox 가 한 줄 선언 형식이라 별도 처리)
# ──────────────────────────────────────────────
def fix_interpreter(path: pathlib.Path):
    if not path.exists():
        return
    html = path.read_text(encoding="utf-8")
    # .qbox 가 한 줄 선언 형식일 경우
    html = html.replace(
        ".qbox { border-left: 4px solid var(--accent-3); background: #EBF4FF; }",
        ".qbox { border-left: 4px solid var(--accent-3); background: #EBF4FF; border-radius: 0; }"
    )
    # th border-radius (없을 수도 있지만 안전하게)
    html = html.replace(
        "    th { background: #EEF0F5; color: #1f2933; font-weight: 800; }",
        "    th { background: #EEF0F5; color: #1f2933; font-weight: 800; border-radius: 0; }"
    )
    path.write_text(html, encoding="utf-8")


# ──────────────────────────────────────────────
# 실행
# ──────────────────────────────────────────────
targets = [
    BLOG / "abstraction.html",
    BLOG / "dict.html",
    BLOG / "interpreter.html",
    BLOG / "index.html",
]

for t in targets:
    apply(t)

fix_interpreter(BLOG / "interpreter.html")

# ──────────────────────────────────────────────
# 검증: border-radius 8px 잔여 확인
# ──────────────────────────────────────────────
print("\n=== 검증 ===")
for t in targets:
    if not t.exists():
        continue
    html = t.read_text(encoding="utf-8")
    # CSS 영역만 검사 (</style> 이전)
    css_part = html.split("</style>")[0] if "</style>" in html else html
    r8 = css_part.count("border-radius: 8px")
    shadow = css_part.count("box-shadow: var(--shadow)")
    grad = "linear-gradient" in css_part
    print(f"  {t.name}: border-radius:8px={r8}  shadow_var={shadow}  gradient={grad}")

print("\n완료")
