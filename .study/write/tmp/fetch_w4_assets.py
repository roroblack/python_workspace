"""Fetch sheet CSVs + encode all ERD/screenshot images to base64 for retrospective_w4."""
from __future__ import annotations
import base64, json, urllib.request, ssl
from pathlib import Path

ROOT = Path(r"c:\_proj\python_workspace")
OUT = ROOT / ".study" / "write" / "tmp" / "w4_assets"
OUT.mkdir(parents=True, exist_ok=True)

SHEET_ID = "10QCpgSJE9i5_fRU6IW2nIoNO0pWymVEwm7qnRn2TKaQ"
SHEETS = {
    "tasks_gid471644863": "471644863",
    "debug_gid1542101365": "1542101365",
}

UA = {"User-Agent": "Mozilla/5.0"}
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
        return r.read()

# 1) sheet CSV
for name, gid in SHEETS.items():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
    try:
        data = fetch(url)
        path = OUT / f"{name}.csv"
        path.write_bytes(data)
        print(f"[OK] {name}: {len(data)} bytes -> {path}")
    except Exception as e:
        print(f"[FAIL] {name}: {e}")

# 2) Discord initial ERD (may fail if token expired)
DISCORD_URL = (
    "https://cdn.discordapp.com/attachments/1504712295891079259/"
    "1505204973707853834/3a98db8f-b136-466c-ad9f-484f2388138a.png"
    "?ex=6a13aa1f&is=6a12589f"
    "&hm=40e364e3f8bcebe798e77d04321fd69b4ffb0242488ea7ff69c83a31f97c0bc8&"
)
try:
    data = fetch(DISCORD_URL)
    (OUT / "erd_initial.png").write_bytes(data)
    print(f"[OK] erd_initial.png: {len(data)} bytes")
except Exception as e:
    print(f"[FAIL] erd_initial.png: {e}")

# 3) Encode local SKN32 assets to base64
ASSETS = ROOT.parent / "crawling_project" / "SKN32-1st-3Team" / "assets"
img_b64: dict[str, dict] = {}

def encode(p: Path, key: str):
    if not p.exists():
        print(f"[MISS] {p}")
        return
    raw = p.read_bytes()
    ext = p.suffix.lower().lstrip(".")
    mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
            "webp": "image/webp", "gif": "image/gif"}.get(ext, "image/png")
    img_b64[key] = {
        "mime": mime,
        "size": len(raw),
        "b64": base64.b64encode(raw).decode("ascii"),
        "src_path": str(p),
    }
    print(f"[ENC] {key}: {len(raw)} bytes")

encode(ASSETS / "ERD.png", "erd_final")
encode(ASSETS / "대시보드.png", "dashboard_home")
encode(ASSETS / "수소차등록현황.png", "registration_trend")
encode(ASSETS / "지역별등록현황-바.png", "region_bar")
encode(ASSETS / "지역별등록현황-바-서울.png", "region_bar_seoul")
encode(ASSETS / "지역별등록현황-파이.png", "region_pie")
encode(ASSETS / "수소차충전소.png", "station_map")
encode(ASSETS / "수소차충전소-목록선택-서울특별시양재그린카스테이션.png", "station_detail")
encode(ASSETS / "사이드바-필터-세이브&로드.png", "sidebar")

# encode discord image if downloaded
di = OUT / "erd_initial.png"
if di.exists():
    encode(di, "erd_initial")

(OUT / "images.json").write_text(json.dumps(img_b64), encoding="utf-8")
print(f"\nTotal images: {len(img_b64)}; JSON -> {OUT/'images.json'}")
