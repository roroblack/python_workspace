"""
GUIDE.txt 정리 스크립트
- §4 / §15 CSS 팔레트 중복 제거 (§15에서 제거, §4가 정본)
- §12 이미지 체크 항목 업데이트
- §13 이미지 금지 규칙 업데이트
- §22(터미널 헤더) → §24 로 번호 수정 (기존 §22 ASCII 와 충돌)
- §23(코드 예제) → §25 로 번호 수정
- 새 §26 이미지 삽입 규칙 추가
- 파일 헤더 경로 수정 + 목차 추가
"""
from pathlib import Path

src = Path(r"C:\_proj\python_workspace\.study\GUIDE.txt")
text = src.read_text(encoding="utf-8")

# ── 1. 헤더 경로 수정 ────────────────────────────────────────────
text = text.replace(
    "# 파일 위치: c:\\_proj\\python_workspace\\.study\\blog\\GUIDE.txt",
    "# 파일 위치: c:\\_proj\\python_workspace\\.study\\GUIDE.txt",
)

# ── 2. §4 팔레트 주석 업데이트 ────────────────────────────────────
text = text.replace(
    "  ※ §15 디자인 스타일 가이드와 동일한 팔레트 사용 (구버전 #0f766e 금지)",
    "  ※ 이 팔레트가 기준값. 구버전 #0f766e 사용 금지. §15 에 폰트·Swiss Style 규칙 있음.",
)

# ── 3. §12 이미지 체크 항목 수정 ──────────────────────────────────
text = text.replace(
    "  [ ] img/*.png 참조 0개 (이미지 대신 텍스트 블록)",
    "  [ ] 외부 URL img src 0개 (모든 이미지는 data:image base64 인라인 — §26)",
)

# ── 4. §13 이미지 금지 규칙 수정 ──────────────────────────────────
text = text.replace(
    "  ✗ 이미지 파일(png) 생성 후 HTML에 삽입 — 텍스트 블록 사용",
    "  ✗ HTML 이미지를 외부 URL(src=\"http...\") 로 삽입 — 반드시 base64 인라인으로 교체 (→ §26)",
)

# ── 5. §15 중복 팔레트 블록 제거 ──────────────────────────────────
OLD_PALETTE_BLOCK = """  [ 포인트 색상 팔레트 (파스텔 톤 4색) ]
  :root {
    --accent:      #52A97E;   /* 파스텔 초록  — 챕터번호·강조·keypoint */
    --accent-2:    #E8875A;   /* 파스텔 오랜지 — callout·경고·accent-2 */
    --accent-3:    #5B9BD5;   /* 파스텔 파랑  — qbox·링크·accent-3 */
    --accent-4:    #9178C4;   /* 파스텔 보라  — 추가 강조·accent-4 */
    --accent-soft: #EBF7F1;   /* 초록 배경 tint (keypoint bg) */
    --warn-soft:   #FFF1E8;   /* 오랜지 배경 tint (callout bg) */
  }

  qbox 배경: #EBF4FF  (파란 tint)
  table th 배경: #EEF0F5 / color: #1f2933
  inline code 배경: #EEF0F6

  [ 컬러별 용도 ]
  초록(--accent)  : 챕터 번호 배지, h3.step::before, keypoint 왼쪽 선, .eyebrow
  오랜지(--accent-2): callout 왼쪽 선, 경고 텍스트
  파랑(--accent-3): qbox 왼쪽 선, a 링크, 질문 레이블
  보라(--accent-4): 필요 시 추가 강조 요소에 사용"""

NEW_PALETTE_BLOCK = """  [ 포인트 색상 팔레트 ]
  → CSS 변수 전체 정의 및 컬러별 용도는 §4 참조.
    컴포넌트별 배경색 요약:
      qbox 배경: #EBF4FF  (파란 tint)
      table th 배경: #EEF0F5 / color: #1f2933
      inline code 배경: #EEF0F6"""

if OLD_PALETTE_BLOCK in text:
    text = text.replace(OLD_PALETTE_BLOCK, NEW_PALETTE_BLOCK)
    print("§15 팔레트 블록 제거 완료")
else:
    print("§15 팔레트 블록을 찾지 못함 — 수동 확인 필요")

# ── 6. 중복 §22(터미널 헤더) → §24 ───────────────────────────────
text = text.replace(
    " 22. 터미널 헤더 레이블(t-label) 규칙 (2026-05-24 추가)",
    " 24. 터미널 헤더 레이블(t-label) 규칙 (2026-05-24 추가)",
)

# ── 7. §23(코드 예제) → §25 ──────────────────────────────────────
text = text.replace(
    " 23. 코드 예제 작성 스타일 규칙 (2026-05-24 추가)",
    " 25. 코드 예제 작성 스타일 규칙 (2026-05-24 추가)",
)

# ── 8. 새 §26 이미지 삽입 규칙 추가 (파일 끝) ─────────────────────
NEW_SECTION = """
======================================================================
 26. 이미지 삽입 규칙 — base64 인라인 필수 (2026-05-25 추가)
======================================================================

  HTML 블로그 파일에 삽입하는 모든 이미지는 외부 URL(src="http...") 을
  사용하지 않고 반드시 base64 data URI 형식으로 인라인 삽입한다.
  외부 URL 이미지는 서버 정책 변경·링크 만료·CORS 차단으로 언제든
  깨질 수 있다. base64 인라인은 파일 단독으로 완결되어 영구 보존된다.

  ─────────────────────────────────
  규칙
  ─────────────────────────────────
  ✓ 모든 <img> src 는 data:image/TYPE;base64,XXXX... 형식으로 삽입
  ✓ 파일 완성 전 검증: src="http" 패턴이 <img> 태그에 없어야 한다
  ✗ <img src="https://..."> — 금지 (스크립트·스타일시트 CDN URL 은 허용)
  ✗ <img src="./img/파일명.png"> — 상대경로 금지 (Blogger 에서 깨짐)

  ─────────────────────────────────
  변환 절차
  ─────────────────────────────────
  1. 이미지 파일 확보 (다운로드 또는 로컬 파일)
       python: data = urllib.request.urlopen(url).read()
               또는 Path(local_path).read_bytes()

  2. base64 인코딩
       b64 = base64.b64encode(data).decode()

  3. MIME 타입 확인
       PNG  → data:image/png;base64,
       JPEG → data:image/jpeg;base64,
       WebP → data:image/webp;base64,
       SVG  → data:image/svg+xml;base64,
       GIF  → data:image/gif;base64,

  4. HTML에 삽입
       <img src="data:image/png;base64,{b64}"
            alt="설명"
            style="display:block;width:100%;height:auto;max-width:800px;margin:0 auto;" />

  ─────────────────────────────────
  변환 스크립트 패턴 (write/tmp/*.py)
  ─────────────────────────────────
  from pathlib import Path
  import base64, urllib.request

  def url_to_b64(url: str) -> tuple[str, str]:
      \"\"\"URL에서 이미지 다운로드 후 (mime_type, b64_str) 반환\"\"\"
      data = urllib.request.urlopen(url, timeout=15).read()
      ext  = url.rsplit('.', 1)[-1].lower()
      mime = {'png':'image/png','jpg':'image/jpeg','jpeg':'image/jpeg',
              'webp':'image/webp','gif':'image/gif','svg':'image/svg+xml'
             }.get(ext, 'image/png')
      return mime, base64.b64encode(data).decode()

  def file_to_b64(path: str) -> tuple[str, str]:
      \"\"\"로컬 파일을 base64로 변환\"\"\"
      data = Path(path).read_bytes()
      ext  = path.rsplit('.', 1)[-1].lower()
      mime = {'png':'image/png','jpg':'image/jpeg','jpeg':'image/jpeg',
              'webp':'image/webp'}.get(ext, 'image/png')
      return mime, base64.b64encode(data).decode()

  ─────────────────────────────────
  검증
  ─────────────────────────────────
  # 외부 URL img src 검사 (0이어야 통과)
  import re
  html = Path('파일.html').read_text(encoding='utf-8')
  hits = re.findall(r'<img[^>]+src="https?://', html)
  assert len(hits) == 0, f"외부 URL img 발견: {hits}"

  # 이미지 naturalWidth 브라우저 검증 (Playwright)
  imgs = await page.$$('figure img')
  for img in imgs:
      nat = await img.evaluate('el => ({w:el.naturalWidth,h:el.naturalHeight,ok:el.complete})')
      assert nat['ok'] and nat['w'] > 0, f"이미지 깨짐: {nat}"

  ─────────────────────────────────
  예외 — CDN 스크립트·스타일시트
  ─────────────────────────────────
  Prism.js CDN 등 <script src="https://..."> 와
  <link rel="stylesheet" href="https://..."> 는 외부 URL 유지.
  이미지(<img>) 와 <video>/<audio> src 만 base64 대상이다.
"""

text = text.rstrip() + "\n" + NEW_SECTION

# ── 9. 파일 맨 앞에 목차 추가 ─────────────────────────────────────
TOC = """# 기술 블로그 HTML 작성 AI 가이드
# 파일 위치: c:\\_proj\\python_workspace\\.study\\GUIDE.txt
# 마지막 정리: 2026-05-25

====================================================================
 목차
====================================================================
 §0   환경 정보
 §1   파일 레이아웃
 §2   글 구조 — 서사 사슬
 §3   HTML 헤드 필수 태그
 §4   CSS 변수 팔레트  ← 색상 기준값 정본
 §5   터미널 블록 규칙
 §6   코드 블록 규칙
 §7   챕터 h2 헤더 규칙
 §8   박스 컴포넌트
 §9   표지(header.cover) 필수 항목
 §10  제목 작성 원칙
 §11  run_all.py 표준 구조
 §12  검증 체크리스트
 §13  금지 목록
 §14  새 주제 시작 체크리스트
 §15  디자인 스타일 가이드 (폰트·Swiss Style·§4 참조)
 §16  새 주제 시작 전 사전 고찰  ← §15 뒤에 있어야 하나, 파일 내 §21 이후 위치
 §17  레퍼런스 명시 및 공신력 확보 규칙
 §18  자습 글 vs 부트캠프 글 구분 표기
 §19  회고(Retrospective) 글 작성 규칙
 §20  결과물 저장 경로 규칙
 §21  구글 블로그(Blogger) 업로드 형식 규칙
 §22  ASCII 다이어그램 정렬 규칙
 §24  터미널 헤더 레이블(t-label) 규칙
 §25  코드 예제 작성 스타일 규칙
 §26  이미지 삽입 규칙 — base64 인라인 필수  ← 2026-05-25 추가

 ※ §16 이 §21 이후에 위치한 것은 역사적 추가 순서에 따른 것으로, 내용상 §15 다음으로 참고.

"""

# 기존 헤더 3줄을 TOC로 교체
OLD_HEADER = """# 기술 블로그 HTML 작성 AI 가이드
# Python 기술 블로그 · 작성 규칙 전집
# — dict.html 프로젝트를 통해 확립된 모든 규칙 —
# 파일 위치: c:\\_proj\\python_workspace\\.study\\GUIDE.txt"""

text = text.replace(OLD_HEADER, TOC.rstrip(), 1)

src.write_text(text, encoding="utf-8")
print(f"완료. 줄 수: {len(text.splitlines())}")

# 검증
verify = src.read_text(encoding="utf-8")
checks = {
    "§26 추가됨": "26. 이미지 삽입 규칙" in verify,
    "팔레트 중복 제거됨": "--accent:      #52A97E" not in verify.split("======================================================================\n 15.")[1][:2000],
    "§4 팔레트 유지됨": "--accent:   #52A97E" in verify,
    "§12 img check 수정됨": "외부 URL img src 0개" in verify,
    "§13 이미지 규칙 수정됨": "base64 인라인으로 교체" in verify,
    "§24 존재함": "24. 터미널 헤더" in verify,
    "§25 존재함": "25. 코드 예제" in verify,
    "§22(구 중복) 제거됨": verify.count(" 22. ") == 1,
    "목차 존재함": "목차" in verify,
}
for k, v in checks.items():
    print(f"  {'✓' if v else '✗'} {k}")
