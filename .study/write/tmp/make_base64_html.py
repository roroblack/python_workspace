"""
make_base64_html.py
interpreter.html 의 img/ 상대경로 이미지를
최적화(리사이즈 + WebP 압축)해 base64 로 내장한 단일 HTML 을 생성한다.

출력: .study/blog/<주제>_base64.html
      → 구글 블로그(Blogger) 포스트 에디터 HTML 탭에 직접 붙여넣기 가능한 형식
      → <html>/<head>/<body> wrapper 없음, <style> @import 폰트 포함

최적화 규칙:
  - 최대 너비 960px (초과 시 비율 유지 리사이즈)
  - WebP quality=72 로 재압축
  - base64 로 인코딩해 <img src="data:image/webp;base64,..."> 로 치환
"""

import base64
import io
import re
import sys
from pathlib import Path

from PIL import Image

# 인수로 소스 파일명 지정 가능 (기본값: interpreter.html)
src_name = sys.argv[1] if len(sys.argv) > 1 else "interpreter.html"
stem     = Path(src_name).stem                     # 확장자 없는 파일명

SRC_HTML  = Path(__file__).resolve().parents[3] / ".blog" / src_name
IMG_DIR   = Path(__file__).resolve().parents[3] / ".blog" / "img"
OUT_HTML  = Path(__file__).resolve().parents[3] / ".study" / "blog" / f"{stem}_base64.html"

MAX_WIDTH = 9999   # 리사이즈 없음 — 원본 해상도 유지
QUALITY   = 100   # WebP 최고 품질 (lossless 모드 활성화)

FONT_IMPORT = "@import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic+Coding:wght@400;700&display=swap');"
PRISM_CSS   = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" />'
PRISM_SCRIPTS = (
    '<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>\n'
    '<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>'
)


def img_to_b64(name: str) -> str:
    path = IMG_DIR / name
    with Image.open(path) as im:
        if im.mode in ("RGBA", "P"):
            im = im.convert("RGBA")
        else:
            im = im.convert("RGB")
        # 리사이즈 (MAX_WIDTH=9999 → 실질적으로 원본 해상도 유지)
        if im.width > MAX_WIDTH:
            ratio = MAX_WIDTH / im.width
            im = im.resize(
                (MAX_WIDTH, int(im.height * ratio)),
                Image.LANCZOS,
            )
        buf = io.BytesIO()
        # lossless WebP = 원본과 동일한 무손실 품질, PNG보다 작아 Blogger 1MB 한계 이내
        im.save(buf, format="WEBP", lossless=True, method=6)
        raw = buf.getvalue()
    b64 = base64.b64encode(raw).decode()
    return f"data:image/webp;base64,{b64}"


html = SRC_HTML.read_text(encoding="utf-8")

total_before = 0
total_after  = 0

def replace_img(m: re.Match) -> str:
    global total_before, total_after
    quote = m.group(1)
    name  = m.group(2)
    orig_path = IMG_DIR / name
    total_before += orig_path.stat().st_size if orig_path.exists() else 0
    data_uri = img_to_b64(name)
    total_after += len(data_uri) * 3 // 4  # base64 → 바이트 추정
    print(f"  {name:45s} → {len(data_uri)//1024} KB (b64)")
    return f"src={quote}{data_uri}{quote}"

html_b64 = re.sub(r'src=(["\'])img/([^"\']+)\1', replace_img, html)

# ── Blogger 형식으로 변환 ────────────────────────────────────────────
# 1) <style> 블록에 @import 추가 (Blogger는 <link> 를 무시하므로 필수)
html_b64 = re.sub(
    r'(<style>)\s*\n',
    f'\\1\n    {FONT_IMPORT}\n',
    html_b64,
    count=1,
)

# 2) <script> 태그 추출 (소스 HTML에 있다면 수집, 없으면 빈 리스트)
scripts = re.findall(r'<script[^>]*(?:/>|>.*?</script>)', html_b64, re.DOTALL)

# 2-1) Prism.js 스크립트가 소스에 없으면 항상 추가
prism_core_present = any('prism-core' in s for s in scripts)
if not prism_core_present:
    scripts = [PRISM_SCRIPTS]

# 2-2) lightbox 스크립트 추가
LIGHTBOX_SCRIPT = """\
<script>
(function(){
  /* ── lightbox ── */
  var overlay = document.createElement('div');
  overlay.id = 'lb-overlay';
  overlay.style.cssText = [
    'display:none','position:fixed','inset:0','z-index:9999',
    'background:rgba(0,0,0,.82)','cursor:zoom-out',
    'align-items:center','justify-content:center'
  ].join(';');
  var img = document.createElement('img');
  img.id = 'lb-img';
  img.style.cssText = [
    'max-width:92vw','max-height:92vh','object-fit:contain',
    'border:2px solid #fff','box-shadow:0 0 40px rgba(0,0,0,.6)',
    'transition:transform .15s'
  ].join(';');
  overlay.appendChild(img);
  document.body.appendChild(overlay);

  function open(src){ img.src=src; overlay.style.display='flex'; }
  function close(){ overlay.style.display='none'; img.src=''; }
  overlay.addEventListener('click', close);
  document.addEventListener('keydown', function(e){ if(e.key==='Escape') close(); });

  /* figure img 클릭 → lightbox */
  document.addEventListener('click', function(e){
    var t = e.target;
    if(t.tagName==='IMG' && t.closest('figure')){ e.preventDefault(); open(t.src); }
  });

  /* figure img hover cursor */
  var style = document.createElement('style');
  style.textContent = 'figure img { cursor:zoom-in; transition:opacity .15s; } figure img:hover { opacity:.85; }';
  document.head.appendChild(style);
})();
</script>"""
scripts.append(LIGHTBOX_SCRIPT)

# 3) <style> 블록 추출
style_match = re.search(r'(<style>.*?</style>)', html_b64, re.DOTALL)
style_block = style_match.group(1) if style_match else ''

# 4) <body> 본문만 추출 후 내장된 <script> 제거
body_match = re.search(r'<body[^>]*>(.*)</body>', html_b64, re.DOTALL)
body_raw   = body_match.group(1).strip() if body_match else html_b64
body_clean = re.sub(r'<script[^>]*(?:/>|>.*?</script>)', '', body_raw, flags=re.DOTALL).strip()

# 5) Blogger 최종 조합:
#    Prism CSS <link> → <style> 블록 → 본문 → Prism <script> + lightbox <script>
blogger_out  = PRISM_CSS + '\n\n'
blogger_out += style_block + '\n\n'
blogger_out += body_clean + '\n\n'
blogger_out += '\n'.join(scripts)
# ─────────────────────────────────────────────────────────────────────

OUT_HTML.write_text(blogger_out, encoding="utf-8")

file_kb = OUT_HTML.stat().st_size // 1024
print(f"\n원본 이미지 합계 : {total_before//1024} KB")
print(f"내장 후 추정 합계: {total_after//1024} KB")
print(f"출력 파일 크기   : {file_kb} KB")
print(f"출력 위치        : {OUT_HTML}")
print(f"형식             : Blogger 포스트 에디터 직접 붙여넣기 가능 (wrapper 없음)")
