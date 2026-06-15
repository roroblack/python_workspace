import base64
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


OUT_DIR = Path(".")
WIDTH, HEIGHT = 1652, 792
FONT_REGULAR = "C:/Windows/Fonts/malgun.ttf"
FONT_BOLD = "C:/Windows/Fonts/malgunbd.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)


TITLE_FONT = font(24, True)
WEEK_FONT = font(16)
BOX_TITLE_FONT = font(19, True)
BOX_BODY_FONT = font(15)
LEGEND_FONT = font(15)


def text_width(draw, text, font_obj):
    if not text:
        return 0
    return draw.textbbox((0, 0), text, font=font_obj)[2]


def wrap_text(draw, text, font_obj, max_width):
    """Wrap Korean/English mixed text by pixels while preserving separator-friendly breaks."""
    if text_width(draw, text, font_obj) <= max_width:
        return [text]

    pieces = []
    token = ""
    for ch in text:
        token += ch
        if ch in " ·/-:":
            pieces.append(token)
            token = ""
    if token:
        pieces.append(token)

    lines = []
    current = ""
    for piece in pieces:
        candidate = current + piece
        if current and text_width(draw, candidate, font_obj) > max_width:
            lines.append(current.rstrip())
            current = piece.lstrip()
        else:
            current = candidate

    if current:
        lines.append(current.rstrip())

    # Fallback for very long unbroken chunks.
    fixed = []
    for line in lines:
        if text_width(draw, line, font_obj) <= max_width:
            fixed.append(line)
            continue
        current = ""
        for ch in line:
            candidate = current + ch
            if current and text_width(draw, candidate, font_obj) > max_width:
                fixed.append(current)
                current = ch
            else:
                current = candidate
        if current:
            fixed.append(current)
    return fixed


def rounded_box(draw, x, y, w, h, outline, fill, radius=6):
    draw.rounded_rectangle((x, y, x + w, y + h), radius=radius, fill=fill, outline=outline, width=2)


def draw_box(draw, x, y, w, title, body, color):
    pad_x = 20
    title_lines = wrap_text(draw, title, BOX_TITLE_FONT, w - pad_x * 2)
    body_lines = wrap_text(draw, body, BOX_BODY_FONT, w - pad_x * 2)
    h = 22 + len(title_lines) * 25 + 10 + len(body_lines) * 21 + 14
    rounded_box(draw, x, y, w, h, color, "#eef6fd" if color == "#5aa0df" else "#edf8f1" if color == "#4fb281" else "#fff4ec")

    cy = y + 17
    for line in title_lines:
        draw.text((x + pad_x, cy), line, font=BOX_TITLE_FONT, fill="#1f2937")
        cy += 25
    cy += 8
    for line in body_lines:
        draw.text((x + pad_x, cy), line, font=BOX_BODY_FONT, fill="#3c4a5e")
        cy += 21
    return h


def main():
    img = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(img)

    grid_color = "#d6deea"
    title = "SK 네트웍스 AI Family 32기 — 04~05월 학습 로드맵 (교과목1 전 과정 + 교과목2 시작)"
    title_w = text_width(draw, title, TITLE_FONT)
    draw.text(((WIDTH - title_w) / 2, 12), title, font=TITLE_FONT, fill="#1f2937")

    week_w = WIDTH / 6
    weeks = [
        ("1주차", "~04/30"),
        ("2주차", "05/04~08"),
        ("3주차", "05/11~15"),
        ("4주차", "05/16~19"),
        ("5주차", "05/20~26"),
        ("6주차", "05/27~"),
    ]
    for i in range(7):
        x = int(i * week_w)
        draw.line((x, 79, x, 779), fill=grid_color, width=1)
    for i, (label, date) in enumerate(weeks):
        cx = int(i * week_w + week_w / 2)
        draw.text((cx - text_width(draw, label, WEEK_FONT) / 2, 98), label, font=WEEK_FONT, fill="#53617a")
        draw.text((cx - text_width(draw, date, WEEK_FONT) / 2, 121), date, font=WEEK_FONT, fill="#53617a")

    blue = "#5aa0df"
    green = "#4fb281"
    orange = "#f18455"

    draw_box(
        draw,
        13,
        163,
        497,
        "교과목1 · 단원1 Python",
        "logic·collection·fileio · oop·module·package·gui·streamlit",
        blue,
    )
    draw_box(
        draw,
        499,
        267,
        320,
        "교과목1 · 단원2 DB(MySQL)",
        "intro·B+Tree·제약·SELECT·JOIN·서브쿼리",
        blue,
    )
    draw_box(
        draw,
        745,
        372,
        310,
        "교과목1 · 단원3 Web Crawling",
        "static·dynamic·selector·HTML 파싱",
        blue,
    )
    draw_box(
        draw,
        843,
        470,
        300,
        "교과목1 단위 프로젝트(팀)",
        "SKN32-1st-3Team · 수집·ERD·웹앱·발표",
        orange,
    )
    draw_box(
        draw,
        990,
        592,
        350,
        "교과목2 · 단원1 데이터분석",
        "numpy·pandas·전처리·이상치·정규화·시각화",
        green,
    )
    draw_box(
        draw,
        1160,
        688,
        475,
        "교과목2 · 단원2 머신러닝",
        "Day1 회귀·데이터관리 / Day2 분류·로지스틱 / Day3 SVM",
        green,
    )

    lx, ly = 21, 696
    draw.rounded_rectangle((lx, ly, lx + 305, ly + 76), radius=4, fill="white", outline="#c7c7c7", width=1)
    legend_items = [
        (blue, "교과목1 · 프로그래밍과 데이터 기초"),
        (green, "교과목2 · 데이터분석·머신러닝"),
        (orange, "단위 프로젝트"),
    ]
    for idx, (color, label) in enumerate(legend_items):
        y = ly + 8 + idx * 24
        draw.rectangle((lx + 7, y, lx + 37, y + 13), fill="#eef6fd" if color == blue else "#edf8f1" if color == green else "#fff4ec", outline=color, width=2)
        draw.text((lx + 49, y - 3), label, font=LEGEND_FONT, fill="#1f2937")

    out_png = OUT_DIR / "roadmap_fixed.png"
    out_txt = OUT_DIR / "roadmap_fixed_base64.txt"
    img.save(out_png)
    out_txt.write_text("data:image/png;base64," + base64.b64encode(out_png.read_bytes()).decode("ascii"), encoding="ascii")
    print(out_png.resolve())
    print(out_txt.resolve())


if __name__ == "__main__":
    main()
