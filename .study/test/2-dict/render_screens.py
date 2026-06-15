"""logs/*.txt 출력을 코드 블록 스타일 PNG 로 렌더링한다 (UI 크롬 없음)."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(__file__)
LOG_DIR = os.path.join(HERE, "logs")
OUT_DIR = os.path.normpath(os.path.join(HERE, "..", "..", "blog", "img"))
os.makedirs(OUT_DIR, exist_ok=True)

# 코드 블록 팔레트
ACCENT_BLUE = (0, 122, 204)
CODE_BG = (30, 30, 30)
CODE_FG = (204, 204, 204)
CODE_HEADING = (97, 175, 239)
CODE_ERROR = (244, 135, 113)
CODE_DIM = (128, 128, 128)
LABEL_BG = (37, 37, 38)
LABEL_FG = (150, 150, 150)

PADDING_X = 20
PADDING_Y = 16
LINE_HEIGHT = 22
FONT_SIZE = 16
LABEL_H = 28


def font(paths, size):
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def f_mono(size=FONT_SIZE):
    return font([
        r"C:\Windows\Fonts\consola.ttf",
        r"C:\Windows\Fonts\cour.ttf",
    ], size)


def f_kr(size=FONT_SIZE):
    return font([
        r"C:\Windows\Fonts\malgun.ttf",
        r"C:\Windows\Fonts\NanumGothic.ttf",
    ], size)


def f_ui(size=13):
    return font([
        r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\malgun.ttf",
    ], size)


def colour_for(line: str):
    s = line.lstrip()
    if s.startswith("=" * 8):
        return CODE_DIM
    if s.startswith("# "):
        return CODE_HEADING
    if any(t in line for t in ("Error", "Traceback", "TypeError",
                                "KeyError", "RuntimeError")):
        return CODE_ERROR
    return CODE_FG


def render(text: str, out_path: str, name: str):
    kr = f_kr()

    lines = text.splitlines() or [""]

    # 최대 너비 측정
    dummy = Image.new("RGB", (10, 10))
    d = ImageDraw.Draw(dummy)
    max_w = 0
    for ln in lines:
        bbox = d.textbbox((0, 0), ln, font=kr)
        max_w = max(max_w, bbox[2] - bbox[0])

    width = max(900, max_w + PADDING_X * 2)
    height = PADDING_Y + LINE_HEIGHT * len(lines) + PADDING_Y

    img = Image.new("RGB", (width, height), CODE_BG)
    drw = ImageDraw.Draw(img)

    # 코드 라인 출력
    cy = PADDING_Y
    for ln in lines:
        col = colour_for(ln)
        drw.text((PADDING_X, cy), ln, font=kr, fill=col)
        cy += LINE_HEIGHT

    img.save(out_path, "PNG")
    return out_path


def main():
    for fn in sorted(os.listdir(LOG_DIR)):
        if not fn.endswith(".txt"):
            continue
        name = os.path.splitext(fn)[0]
        with open(os.path.join(LOG_DIR, fn), "r", encoding="utf-8") as f:
            text = f.read()
        out = os.path.join(OUT_DIR, f"dict_{name}.png")
        render(text, out, name)
        print("wrote", out)


if __name__ == "__main__":
    main()
