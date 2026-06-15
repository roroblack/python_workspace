# day0511_mysql_btree.html 작업 완료 보고서
작성일: 2026-05-25

---

## 1. 작업 개요

`c:\_proj\python_workspace\.blog\day0511_mysql_btree.html` (MySQL B+Tree 심층 분석)에
다음 세 가지 작업을 수행함.

| # | 요청 내용 | 상태 |
|---|-----------|------|
| 1 | CH13 신규 챕터(최적화) 추가 | ✅ 완료 |
| 2 | 5개 외부 이미지 base64 내장 | ✅ 완료 |
| 3 | ASCII 박스 정렬 수정 (줄이 맞지 않음) | ✅ 완료 |

---

## 2. 근본 원인 분석 — ASCII 박스 정렬 불일치

### 문제
브라우저에서 박스 내용 줄의 오른쪽 `│` 위치가 제각각으로 흔들림.

### 원인 파악 과정
Playwright `canvas.measureText`로 Nanum Gothic Coding 폰트의 실제 문자 너비를 직접 측정.

```
측정 결과 (font-size: 18px, Nanum Gothic Coding):
  ASCII 'A'   →  6.880px   (1×)
  한글  '가'  → 13.760px   (2×)
  박스  '─'   → 13.760px   (2×)  ← 구버전 코드가 1×로 계산하고 있었음!
  박스  '│'   → 13.760px   (2×)
  화살표 '→'  → 13.760px   (2×)
  기호  '▲'   → 13.760px   (2×)
  비율: dash/ascii = 2.000
```

### 결론
**모든 non-ASCII (U+0080 이상) 문자가 2× 너비로 렌더링**된다.
구버전 `vw()` 함수는 "박스 경계 문자(─ │ ┌ ┐ …) = 1×"로 잘못 계산하고 있었으며,
이로 인해 `─`를 N개 쓴 border는 실제 N×2 units이지만 content는 N units로 계산해
패딩이 절반밖에 안 됨.

---

## 3. 수정 내역

### 3-1. 올바른 시각 너비(visual width) 공식

```python
# 구버전 (WRONG)
def vw(s):
    return sum(2 if Korean/CJK else 1 for c in s)
    # 박스 경계 문자를 1×로 계산 → 정렬 불일치

# 신버전 (CORRECT)
def new_vw(s: str) -> int:
    return sum(1 if ord(c) < 128 else 2 for c in s)
    # ASCII만 1×, 나머지 전부 2× → 브라우저 실제 렌더링과 일치
```

### 3-2. 수정된 박스 파라미터

| 박스 | N (border ─ 개수) | target = N×2 | 내용 줄 수 |
|------|-------------------|--------------|-----------|
| InnoDB 16KB 페이지 레이아웃 | 30 | 60 | 16줄 |
| 12장 사슬 전체 회수 요약 | 34 | 68 | 21줄 |

### 3-3. 수정 스크립트
`c:\_proj\python_workspace\.study\write\tmp\fix_box_v2.py` 실행 완료

---

## 4. 검증 결과

### 4-1. Python new_vw 검증 (fix_box_v2.py)

```
=== 생성된 16KB 박스 검증 ===
  [✓] vw=60  ' FIL Header (38B)  ─ FIL_PAGE_PREV / FIL'   (× 16줄 전체)

=== 생성된 12장 박스 검증 ===
  [✓] vw=68  '  CH01-02:  MySQL 의 자료구조 ─ B+Tree ...'   (× 21줄 전체)
```

### 4-2. 브라우저 DOM 픽셀 측정 (Playwright)

```
16KB 박스: 모든 content 줄 → 413px (오차 0px)
12장 박스: 모든 content 줄 → 468px (오차 0px)
```

브라우저에서 혼합 텍스트(한글+박스문자+ASCII) 줄이 모두 동일 픽셀 너비로 일치함.

---

## 5. 내용·스타일 검증 결과

### §2 서사 사슬 구조
- 총 14개 챕터 (CH01–CH14) 모두 정상
- CH14(정리): bridge 없음 → GUIDE.txt §8 규칙 준수 ("마지막 챕터 뒤에는 bridge 없음")

### §4 CSS 팔레트
- `--accent: #52A97E` ✓, `--accent-2: #E8875A` ✓, `--accent-3: #5B9BD5` ✓, `--accent-4: #9178C4` ✓

### §5 터미널 블록
- 맥 dot(t-dot-r/y/g) 0건 ✓
- terminal-header/terminal-body 쌍 8/8 ✓

### §6 코드 블록
- language-cpp: 6개, language-sql: 9개, language-python: 1개

### §7 챕터 h2 형식
- 14개 h2.chap 전부 `span.num` + `anchor-link` 포함 ✓

### 내용 사실 확인
| 사실 | 결과 |
|------|------|
| FIL Header (38B) | ✓ |
| File Trailer (8B) | ✓ |
| 16KB 페이지 | ✓ |
| B+Tree 분기 ~1000 | ✓ |
| Innodb_buffer_pool_read_requests | ✓ |
| Using index (커버링 인덱스) | ✓ |
| right-only split | ✓ |
| dict_table_t::autoinc | ✓ |
| btr0cur.cc | ✓ |
| innodb_buffer_pool_size | ✓ |

### blockquote.cite 인용
- 총 11개, MySQL 8.0 공식 문서(8건) + PlanetScale + GitHub mysql-server

### CH13 신규 챕터
- 길이: 7,600자
- 커버링 인덱스 / EXPLAIN / 복합 인덱스 / Buffer Pool / Using index 전부 포함 ✓

---

## 6. GUIDE.txt §22 규칙 업데이트

파일: `c:\_proj\python_workspace\.study\GUIDE.txt`

### 변경 내용 (§22 ASCII 다이어그램 정렬 규칙)

**삭제된 잘못된 규칙:**
```
박스 경계 문자 (│ ─ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼) → 1 visual col  ← 틀린 규칙 삭제
ASCII 및 기타 모든 문자                   → 1 visual col
(Korean/CJK 구분 vw() 함수)
```

**추가된 올바른 규칙:**
```
ASCII (U+0000–U+007F)     → 1 visual col
나머지 전부 (U+0080 이상)  → 2 visual cols
(박스문자 ─ │ ┌도 전부 2×)

def new_vw(s: str) -> int:
    return sum(1 if ord(c) < 128 else 2 for c in s)

N개 ─ 사용 시 → target = N × 2
```

---

## 7. 최종 파일 상태

| 파일 | 크기 | 상태 |
|------|------|------|
| `.blog/day0511_mysql_btree.html` | 1,531 KB | ✅ 완성 (CH01–CH14) |
| `.study/write/tmp/fix_box_v2.py` | — | 실행 완료 (재사용 가능) |
| `.study/GUIDE.txt` (§22) | — | 규칙 수정 완료 |

---

## 8. 잔여 이슈

없음. 모든 검증 통과.
