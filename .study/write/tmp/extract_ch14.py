from pathlib import Path
import base64, re

html = Path(r"c:\_proj\python_workspace\.blog\day0511_mysql_btree.html").read_text(encoding="utf-8")
sec = html.find('<section id="ch14">')
chunk = html[sec:sec+200000]

m = re.search(r'data:image/([^;]+);base64,([A-Za-z0-9+/=]+)', chunk)
if m:
    fmt = m.group(1)
    b64 = m.group(2)
    print(f"포맷: {fmt}, base64 길이: {len(b64)}")
    if "svg" in fmt:
        svg_text = base64.b64decode(b64).decode("utf-8")
        out = Path(r"c:\_proj\python_workspace\.study\write\tmp\ch14_current.svg")
        out.write_text(svg_text, encoding="utf-8")
        print(f"SVG 저장 완료: {len(svg_text)} chars → {out}")

        # text 요소 추출
        texts = re.findall(r'<text[^>]*>(.+?)</text>', svg_text, re.DOTALL)
        print(f"\n=== 텍스트 요소 총 {len(texts)}개 ===")
        for t in texts:
            clean = re.sub(r'<[^>]+>', '', t).strip()
            if clean:
                print(f"  {clean}")

        # connector 라벨 (rect+text 쌍으로 나타나는 칩 라벨)
        paths = re.findall(r'<path d="M ([^"]+)"[^/]*/>', svg_text)
        print(f"\n=== path(연결선) 총 {len(paths)}개 ===")
        for p in paths[:20]:
            print(f"  M {p[:80]}")
    else:
        print("PNG 또는 다른 이미지 형식")
else:
    print("base64 이미지 없음")
    print(chunk[:500])
