# Knowledge Map

이 폴더는 지금까지 쌓인 학습 자료를 다시 꺼내 쓰기 위한 지도다.

목표는 자료를 예쁘게 보관하는 것이 아니라, 다음 세 가지를 빠르게 할 수 있게 만드는 것이다.

- 내가 무엇을 배웠는지 한눈에 보기
- 특정 개념이 어느 원천 노트, 글, 실습, PDF와 연결되는지 찾기
- 복습 질문으로 기억을 다시 불러오기

## 중심 자료

이 시스템의 중심은 `.study/notes/`다.

블로그는 정리된 결과물이고, PDF는 강의 원본이며, test 폴더는 검증 기록이다. 하지만 내가 실제로 무엇을 궁금해했고 어디서 이해가 바뀌었는지는 대부분 `.study/notes/`에 남아 있다.

따라서 개념 카드는 항상 notes를 먼저 보고, 그 다음 블로그와 실습을 연결한다.

## 읽는 순서

1. [TIMELINE.md](TIMELINE.md): 날짜순 학습 흐름
2. [DOMAINS.md](DOMAINS.md): 분야별 지식 구조
3. [NOTES.md](NOTES.md): 원천 노트 인덱스
4. [INDEX.md](INDEX.md): 자동 수집된 전체 산출물 목록
5. [REVIEW.md](REVIEW.md): 복습 질문 큐
6. [concepts/](concepts/): 핵심 개념 카드
7. [projects/](projects/): 프로젝트 단위 회고와 연결 자료

## 자료의 역할

| 위치 | 역할 |
|---|---|
| `about.txt` | 날짜별 커리큘럼과 프로젝트 흐름 |
| `.study/pdf/` | 강의 원본 자료 |
| `.study/notes/` | 원천 노트, 대화, 추출 텍스트. 개념 카드의 1차 출처 |
| `.study/test/` | 실험 코드, 실행 로그, 차트 |
| `.study/blog/` | 블로그 중간 산출물 |
| `.blog/` | 최종 공개용 블로그 산출물 |
| `.study/HISTORY.md` | 작업 이력과 최근 맥락 |
| `.study/GUIDE.txt` | 블로그 작성 규칙 |

## 운영 원칙

- 전체 목록과 notes 목록은 자동 생성한다.
- 핵심 개념만 사람이 직접 카드로 정리한다.
- 카드 하나에는 정의, 질문, 직접 검증한 것, 연결 개념, 관련 notes, 관련 산출물을 넣는다.
- 복습은 글을 다시 읽는 방식보다 질문에 답하는 방식으로 한다.

## 주간 루틴

- 매일: 새로 배운 개념 1개를 `concepts/`에 카드로 추가
- 주 2회: [REVIEW.md](REVIEW.md)의 질문 5개를 직접 답해보기
- 주 1회: `scripts/build_index.py`를 실행해서 [NOTES.md](NOTES.md), [INDEX.md](INDEX.md) 갱신
- 한 단원이 끝날 때: [DOMAINS.md](DOMAINS.md)에 연결 관계 추가
