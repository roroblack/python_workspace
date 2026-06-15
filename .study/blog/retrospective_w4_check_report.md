# retrospective_w4.html 점검 보고서

- 점검 대상: `c:\_proj\python_workspace\.blog\retrospective_w4.html`
- 점검 기준:
  - `c:\_proj\python_workspace\.study\GUIDE.txt`
  - `c:\_proj\python_workspace\.study\blog\blog_w4.txt`
  - 실제 구현 코드
    - `c:\_proj\crawling_project\SKN32-1st-3Team\app.py`
    - `c:\_proj\crawling_project\SKN32-1st-3Team\data\repository.py`
    - `c:\_proj\crawling_project\SKN32-1st-3Team\data\db.py`
    - `c:\_proj\crawling_project\SKN32-1st-3Team\crawling\crawler_molit.py`
    - `c:\_proj\crawling_project\SKN32-1st-3Team\crawling\crawler_faq.py`
    - `c:\_proj\crawling_project\SKN32-1st-3Team\dbscript\dbscript_table.sql`
- 점검일: 2026-05-25

## 종합 판정
부분 충족.

현재 HTML은 `blog_w4.txt`의 큰 목차와 핵심 서사는 대부분 반영되어 있고, 메타 태그·팔레트·base64 이미지 같은 기본 형식도 대체로 맞다. 다만 `GUIDE.txt`의 핵심 규칙 두 가지가 명확히 깨져 있고, CH06의 디버깅 코드 설명 중 일부가 실제 구현과 다르게 적혀 있어 `GUIDE 기준 완전 통과` 또는 `실제 코드 정확 반영 완료` 상태로 보기는 어렵다.

## 1. 기준별 요약 판정

| 기준 | 판정 | 메모 |
|---|---|---|
| GUIDE 헤드/SEO/CSS 기본 규칙 | 통과 | 메타 태그, 폰트, Prism, 팔레트 반영 확인 |
| GUIDE 이미지 base64 규칙 | 통과 | `img src="data:image/` 9건, 외부 이미지 0건 |
| GUIDE 서사 사슬 기본 뼈대 | 부분 충족 | CH01~CH09, qbox/keypoint/bridge는 있음 |
| GUIDE 인라인 인용 규칙 | 미충족 | 본문 `blockquote.cite` 사용 0건 |
| GUIDE 터미널 블록 규칙 | 미충족 | `div.terminal` 0건, `pre.terminal-body` 1건 |
| blog_w4.txt 섹션 0~8 큰 구조 반영 | 대체로 통과 | 0~8이 CH01~CH09로 확장 반영됨 |
| blog_w4.txt 세부 일정/작업 항목 보존 | 부분 충족 | 일부 일자별 세부 항목이 요약되며 누락됨 |
| 디버깅 코드 실제 구현 반영 | 부분 충족 | 일부는 정확, 일부는 파일/구현 위치가 다름 |

## 2. 주요 발견 사항

### 2-1. GUIDE 터미널 규칙 위반
심각도: 높음

근거:
- GUIDE 체크리스트: `c:\_proj\python_workspace\.study\GUIDE.txt:314`
  - `div.terminal 수 == pre.terminal-body 수 (중복 없음)`
- 현재 HTML: `c:\_proj\python_workspace\.blog\retrospective_w4.html:442`
  - `<pre class="terminal-body">전체 작업 수 : 14 ...</pre>` 단독 존재
- 패턴 점검 결과:
  - `div.terminal = 0`
  - `pre.terminal-body = 1`

판정:
- GUIDE §5/§12 기준으로는 명백한 실패다.
- 현재 CH05의 작업 요약 블록은 실제 러너 출력이 아니라 수기 요약 블록 형태이고, `terminal-header`, `t-label`, `PS>` 구조도 없다.

### 2-2. GUIDE 인라인 인용 규칙 미충족
심각도: 높음

근거:
- GUIDE 인라인 인용 요구:
  - `c:\_proj\python_workspace\.study\GUIDE.txt:92`
  - `c:\_proj\python_workspace\.study\GUIDE.txt:119`
  - `c:\_proj\python_workspace\.study\GUIDE.txt:416`
- 현재 HTML 본문 패턴 점검 결과:
  - `<blockquote class="cite">` 본문 사용 0건
  - CSS 정의만 존재 (`retrospective_w4.html:85` 부근)
  - 글 끝 `ref-chain`만 존재 (`retrospective_w4.html:676`)

판정:
- GUIDE는 주장 등장 자리에서 인라인 인용을 넣도록 요구하는데, 현재 글은 챕터 본문 인라인 인용 없이 마지막 `ref-chain`에만 출처를 몰아 넣었다.
- 따라서 `공신력 확보 규칙`은 부분 충족이 아니라 미충족으로 보는 것이 맞다.

### 2-3. CH06 `_item_to_params` 코드가 실제 소스와 다름
심각도: 높음

HTML 서술 위치:
- `c:\_proj\python_workspace\.blog\retrospective_w4.html:543`

현재 HTML 내용 요약:
- `Repository._item_to_params()`가 `region` 문자열을 꺼내 `region_id`로 바꿔 넣는다고 설명함.
- 예시 코드에는 `_region_to_id()` 호출이 들어가 있음.

실제 소스:
- `c:\_proj\crawling_project\SKN32-1st-3Team\data\repository.py:131`
- 실제 구현은 아래처럼 단순 필터만 한다.

```python
    def _item_to_params(self, item, column_names: list[str]) -> dict:
        raw = asdict(item)
        return {k: v for k, v in raw.items() if k in column_names}
```

추가 확인:
- `repository.py` 내부 `_region_to_id` 없음
- 패턴 점검 결과 `regionToIdRepo=False`

판정:
- CH06의 핵심 코드 설명이 현재 저장소의 실제 구현과 일치하지 않는다.
- `region -> region_id` 변환 책임은 현재 `Repository`가 아니라 `data/db.py::save_car_registrations()`에 있다.

### 2-4. UPSERT 구현 위치 설명이 틀림
심각도: 높음

HTML 서술 위치:
- `c:\_proj\python_workspace\.blog\retrospective_w4.html:512`
- `c:\_proj\python_workspace\.blog\retrospective_w4.html:570`

실제 구현 위치:
- `c:\_proj\crawling_project\SKN32-1st-3Team\data\db.py:311`

실제 코드:
```python
INSERT INTO car_registrations (region_id, stat_year, count)
VALUES (:rid, :year, :cnt)
ON DUPLICATE KEY UPDATE count = VALUES(count)
```

추가 확인:
- `repository.py`에는 `ON DUPLICATE KEY UPDATE` 없음
- 점검 결과:
  - `onDupRepo=False`
  - `onDupDb=True`

판정:
- UPSERT 자체는 실제로 존재한다.
- 하지만 글은 `Repository` 중심 설명으로 읽히고, CH06 코드 문맥도 저장 계층의 책임 위치를 혼동하게 만든다.
- 즉, `내용의 취지`는 맞지만 `실제 구현 위치` 설명은 틀렸다.

### 2-5. CH06의 국토부 크롤링 버그 코드 예시는 실제 코드가 아니라 개념 설명 수준
심각도: 중간

HTML 서술 위치:
- `c:\_proj\python_workspace\.blog\retrospective_w4.html:549` 이후

현재 HTML 내용 요약:
- `수소` 시작 행을 찾고 `전기`, `LPG`를 만날 때까지 범위를 잡아 `계` 열을 합산하는 식의 예시를 듦.

실제 구현 위치:
- `c:\_proj\crawling_project\SKN32-1st-3Team\crawling\crawler_molit.py:319`

실제 코드는 다음 조건을 사용한다.
```python
if vehicle != "소계" or usage != "계":
    continue
```

판정:
- 현재 구현은 `연료 섹션 범위를 직접 start/end로 자르는 방식`이 아니라, 공식 subtotal row (`소계` / `계`)만 읽는 방식이다.
- HTML에 `개념적 표현`이라고 적어 두긴 했지만, 사용자 요청이 `실제 코드가 잘 들어가 있나`였다는 점을 기준으로 보면 정확한 코드 반영이라고 보긴 어렵다.

### 2-6. CH03의 FAQ 크롤러 파일 설명이 현재 트리와 맞지 않음
심각도: 중간

HTML 위치:
- `c:\_proj\python_workspace\.blog\retrospective_w4.html:324`
  - `crawler_faq.py             # ev.or.kr FAQ 크롤러`

실제 파일 트리:
- `c:\_proj\crawling_project\SKN32-1st-3Team\crawling\` 아래에는 `crawler_faq.py`만 존재
- 현재 `crawler_faq.py`는 `EvFaqCrawler`, `HyundaiFaqCrawler`, `crawl_all_faqs`, `crawl_all_and_save`를 모두 포함한다.

판정:
- CH03의 구조 설명은 현재 저장소 구조와 1:1로 맞지 않는다.
- 최소한 `crawler_faq.py = ev.or.kr 전용`으로 읽히는 표현은 수정이 필요하다.

### 2-7. blog_w4.txt의 4번 섹션 세부 작업 항목이 일부 요약되며 빠짐
심각도: 중간

원문 요구 (`blog_w4.txt` 4번 섹션)에는 아래 항목이 개별적으로 들어 있다.
- 그래프 가독성 향상
- 추이와 신규등록수 그래프선 추가
- 지역별 등록현황 그래프 % / 파이그래프 / 차트 추가
- 파이썬 개발환경 공유
- 현재 년도 n월까지만 표시하는 기능 추가
- 충전소 기능 통합
- FAQ 출처를 답변 뒤에 추가

현재 HTML CH05에서는 일정표와 브런치 전략 중심으로 정리되어 있고, 위 세부 변경사항 대부분이 개별 항목으로 남아 있지 않다.

판정:
- 큰 흐름은 살아 있지만, 사용자가 요구한 `줄이지 말 것` 기준에서는 축약이 발생했다.

### 2-8. 이미지 규칙은 통과했지만, 수집한 자산 전체 반영 관점에서는 1장 비어 있음
심각도: 낮음

패턴 점검 결과:
- `dataImage=9`
- 외부 이미지 `src="http..."` 없음

판정:
- GUIDE §26 기준으로는 통과다.
- 다만 이번 작업에서 수집한 스크린샷 자산 수(10장) 기준으로 보면 최종 HTML에는 9장만 들어갔다. 서울 강조 바 차트 1장이 빠진 상태다.

## 3. 실제 코드 반영이 확인된 항목

아래 항목들은 현재 HTML 서술과 실제 구현의 방향이 대체로 일치한다.

- `st.session_state["stat_month"]` 존재
  - `c:\_proj\crawling_project\SKN32-1st-3Team\app.py:308`
- `year_range_saved` 쉐도우 키 존재
  - `c:\_proj\crawling_project\SKN32-1st-3Team\app.py:421`, `422`, `436`
- `_station_key` 생성 및 선택 동기화 존재
  - `c:\_proj\crawling_project\SKN32-1st-3Team\app.py:788` 이후
- FAQ `~` 치환 존재
  - `c:\_proj\crawling_project\SKN32-1st-3Team\app.py:350`
- FAQ 폴백 5개 존재
  - `c:\_proj\crawling_project\SKN32-1st-3Team\app.py` 중 `FAQ_FALLBACK`
- `ON DUPLICATE KEY UPDATE` 실제 구현 존재
  - `c:\_proj\crawling_project\SKN32-1st-3Team\data\db.py:311`
- `crawl_stat`의 `CHECK (target_type in ...)` 스키마 존재
  - `c:\_proj\crawling_project\SKN32-1st-3Team\dbscript\dbscript_table.sql`

## 4. blog_w4.txt 섹션별 반영 상태

| blog_w4.txt 항목 | 반영 상태 | 메모 |
|---|---|---|
| 0. 팀프로젝트 시작 & 팀 구성 | 반영 | 팀명/프로젝트명/역할/팀장 담당 반영 |
| 1. 처음 한 일: db 구조 만들기 | 반영 | ERD부터 시작, 초기 아이디어, 기각 항목 반영 |
| 2. erd 구조 완성 및 프로젝트 구성 논의 | 반영 | 초기 ERD/최종 ERD/base64/폴더 구성 반영 |
| 3. 프로토타입 공유 | 반영 | Streamlit, DB, FAQ, 지도 기능 반영 |
| 4. 팀원간 논의·미팅·브런치·살 붙이기 | 부분 반영 | 일정/브런치는 반영, 세부 작업 변화는 일부 누락 |
| 5. 디버깅 목록 | 부분 반영 | 목록은 반영, 코드 예시 일부는 실제 구현과 불일치 |
| 6. 발표 준비 | 반영 | 발표 역할, 마지막 날 문제, Q&A 부족 반영 |
| 7. 돌아보는 시간 | 반영 | 배운 점/개선점/감사 반영 |
| 8. 총 정리 | 반영 | CH09 총정리로 회수 |

## 5. 결론

현재 `retrospective_w4.html`은 아래 두 기준을 분리해서 봐야 한다.

1. 글의 큰 구성과 재료 반영 여부
- `blog_w4.txt`의 큰 뼈대는 잘 반영됐다.
- 팀 결성, ERD, 프로토타입, 협업, 디버깅, 발표, 회고, 총정리까지 흐름은 유지된다.

2. GUIDE 완전 준수 + 실제 코드 정확 반영 여부
- 아직 미완이다.
- 특히 아래 4개는 재작성 또는 최소 수정이 필요하다.
  - 인라인 인용 0건
  - 터미널 블록 규칙 위반
  - `_item_to_params` 코드 설명 오기
  - UPSERT 구현 위치 오기

최종 판정:
- `글 골격과 내용 확장`: 합격
- `GUIDE 완전 준수`: 불합격
- `디버깅 코드 실제 반영`: 부분 합격

## 6. 우선 수정 권장 순서

1. CH05의 수기 `terminal-body`를 실제 `div.terminal` 블록으로 교체하거나, GUIDE 예외로 뺄지 명확히 정리
2. CH01~CH08 본문에 최소 1개씩 `blockquote.cite` 인라인 출처 추가
3. CH06의 `_item_to_params` 설명을 실제 `repository.py` 코드 기준으로 수정
4. CH06의 UPSERT 설명 위치를 `data/db.py::save_car_registrations()` 기준으로 수정
5. CH05에 `blog_w4.txt` 4번 항목의 세부 변경사항(그래프/FAQ 출처/충전소 통합 등)을 복원
6. 필요하면 빠진 스크린샷 1장까지 추가
