"""
export_blogger.py
.blog/ 폴더의 HTML 을 Blogger 붙여넣기용으로 변환한다.
  - img/... 상대경로 → 절대 GitHub Pages URL
  - 결과는 .study/write/tmp/blogger_export/ 에 저장

사용법:
  python export_blogger.py                  # 전체 HTML 변환
  python export_blogger.py interpreter.html # 특정 파일만
"""

import re
import sys
from pathlib import Path

BLOG_DIR = Path(__file__).resolve().parents[3] / ".blog"
OUT_DIR  = Path(__file__).resolve().parents[3] / ".study" / "blog"
BASE_URL = "https://roroblack.github.io/python_workspace"


def convert(html_path: Path) -> Path:
    text = html_path.read_text(encoding="utf-8")

    # src="img/..." 또는 src='img/...' → 절대 URL
    text = re.sub(
        r"(src=[\"'])img/",
        rf"\1{BASE_URL}/img/",
        text
    )

    out_path = OUT_DIR / html_path.name
    out_path.write_text(text, encoding="utf-8")
    return out_path


targets = (
    [BLOG_DIR / sys.argv[1]] if len(sys.argv) > 1
    else sorted(BLOG_DIR.glob("*.html"))
)

for p in targets:
    if not p.exists():
        print(f"  NOT FOUND: {p}")
        continue
    out = convert(p)
    print(f"  OK  {p.name}  →  {out}")

print(f"\n출력 폴더: {OUT_DIR}")
