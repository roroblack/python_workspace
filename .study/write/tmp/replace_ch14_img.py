from pathlib import Path
import base64, re

# 이미지 파일 읽기
img_path = Path(r"C:\_proj\python_workspace\.study\blog\img\1627512681894679593.jpg")
b64 = base64.b64encode(img_path.read_bytes()).decode()
data_uri = f"data:image/jpeg;base64,{b64}"

html_path = Path(r"C:\_proj\python_workspace\.blog\day0511_mysql_btree.html")
html = html_path.read_text(encoding="utf-8")

# CH14 섹션 내의 figure.diagram img src만 교체
sec_start = html.find('<section id="ch14">')
sec_end = html.find('</section>', sec_start) + len('</section>')
ch14 = html[sec_start:sec_end]

# 기존 img src 교체 (data:image/... 형태)
new_ch14 = re.sub(
    r'(<figure class="diagram"[^>]*>.*?<img[^>]+src=")[^"]*(")',
    lambda m: m.group(1) + data_uri + m.group(2),
    ch14,
    flags=re.DOTALL
)

# alt 텍스트도 업데이트
new_ch14 = re.sub(
    r'(<img[^>]+alt=")[^"]*(")',
    r'\1MySQL InnoDB B+Tree & Buffer Pool Engine 고수준 아키텍처 다이어그램\2',
    new_ch14
)

# figcaption 업데이트
new_ch14 = re.sub(
    r'(<figcaption[^>]*>)[^<]*(</figcaption>)',
    r'\1MySQL InnoDB 고수준 아키텍처 — B+Tree Index Manager · AHI · Buffer Pool · Transaction Log · Persistent Storage 구성요소 흐름\2',
    new_ch14
)

new_html = html[:sec_start] + new_ch14 + html[sec_end:]
html_path.write_text(new_html, encoding="utf-8")
print("완료: CH14 이미지 교체됨")
print(f"새 base64 길이: {len(b64)}")
