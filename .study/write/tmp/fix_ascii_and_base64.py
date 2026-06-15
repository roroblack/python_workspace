"""
fix_ascii_and_base64.py
─────────────────────────────────────────────────────────────────────
1. ASCII 박스 줄 너비 분석 및 자동 정렬
2. 외부 이미지 URL → base64 내장 변환
─────────────────────────────────────────────────────────────────────
"""
import re, base64, urllib.request, sys, os
from pathlib import Path

HTML_PATH = Path(r"c:\_proj\python_workspace\.blog\day0511_mysql_btree.html")

def visual_width(s: str) -> int:
    """CJK/Korean chars = 2 visual cols, others = 1"""
    w = 0
    for c in s:
        cp = ord(c)
        if (0x1100 <= cp <= 0x11FF  # Hangul Jamo
            or 0x3130 <= cp <= 0x318F  # Hangul Compatibility Jamo
            or 0xAC00 <= cp <= 0xD7AF  # Hangul Syllables (most common)
            or 0x3000 <= cp <= 0x303F  # CJK Symbols
            or 0x4E00 <= cp <= 0x9FFF  # CJK Unified Ideographs
            or 0xFF00 <= cp <= 0xFFEF  # Halfwidth/Fullwidth Forms
        ):
            w += 2
        else:
            w += 1
    return w

def pad_to_width(s: str, target: int) -> str:
    """Pad string s with spaces to reach target visual width"""
    vw = visual_width(s)
    if vw < target:
        return s + " " * (target - vw)
    return s

# ─── 1. 분석: 16KB 페이지 레이아웃 박스 ───────────────────────────
print("=" * 70)
print("STEP 1: 16KB 페이지 레이아웃 박스 분석")
print("=" * 70)

content = HTML_PATH.read_text(encoding="utf-8")

# 16KB 페이지 box 찾기 (line 891 부근)
box_start = content.find("[ InnoDB 16KB 페이지의 내부 레이아웃")
box_end = content.find("</div>", box_start)
box_text = content[box_start:box_end]

# 박스 경계선 너비 측정 (┌ 또는 └ 로 시작하는 줄)
border_line = None
for line in box_text.split("\n"):
    stripped = line.strip()
    if stripped.startswith("┌") or stripped.startswith("└"):
        # 내부 ─ 수 세기
        inner = stripped[1:-1]  # Remove corners
        border_width = visual_width(inner)
        print(f"Border line ({stripped[:5]}...): inner visual width = {border_width}")
        border_line = inner
        break

if border_line:
    BOX_WIDTH = visual_width(border_line)
    print(f"Target box interior visual width = {BOX_WIDTH}\n")
    
    # 각 내용 줄 분석
    print("내용 줄별 시각 너비 분석:")
    print("-" * 70)
    for i, line in enumerate(box_text.split("\n")):
        stripped = line.rstrip()
        if "│" in stripped:
            # │ 와 │ 사이 내용 추출 (가장 왼쪽과 오른쪽 │)
            first = stripped.index("│")
            last = stripped.rindex("│")
            if first != last:
                inside = stripped[first+1:last]
                vw = visual_width(inside)
                diff = vw - BOX_WIDTH
                status = "✓" if diff == 0 else f"{'+'if diff>0 else ''}{diff}"
                print(f"  [{status:>5}] vw={vw:3d} | {inside[:55]!r}")

# ─── 2. 12장 요약 박스 분석 ───────────────────────────────────────
print("\n" + "=" * 70)
print("STEP 2: 12장 사슬 요약 박스 분석")
print("=" * 70)

box_start2 = content.find("[ 12장 사슬 전체 회수")
box_end2 = content.find("</div>", box_start2)
box_text2 = content[box_start2:box_end2]

border_line2 = None
for line in box_text2.split("\n"):
    stripped = line.strip()
    if stripped.startswith("┌") or stripped.startswith("└"):
        inner = stripped[1:-1]
        border_width2 = visual_width(inner)
        print(f"Border line: inner visual width = {border_width2}")
        border_line2 = inner
        break

if border_line2:
    BOX_WIDTH2 = visual_width(border_line2)
    print(f"Target box interior visual width = {BOX_WIDTH2}\n")
    print("내용 줄별 시각 너비 분석:")
    print("-" * 70)
    for i, line in enumerate(box_text2.split("\n")):
        stripped = line.rstrip()
        if "│" in stripped:
            first = stripped.index("│")
            last = stripped.rindex("│")
            if first != last:
                inside = stripped[first+1:last]
                vw = visual_width(inside)
                diff = vw - BOX_WIDTH2
                status = "✓" if diff == 0 else f"{'+'if diff>0 else ''}{diff}"
                print(f"  [{status:>5}] vw={vw:3d} | {inside[:65]!r}")

# ─── 3. 이미지 URL 추출 ────────────────────────────────────────────
print("\n" + "=" * 70)
print("STEP 3: 이미지 URL 추출")
print("=" * 70)

img_urls = re.findall(r'<img src="(https?://[^"]+)"', content)
for i, url in enumerate(img_urls, 1):
    print(f"  [{i}] {url[:80]}")

print(f"\n총 {len(img_urls)}개 외부 이미지 URL")
