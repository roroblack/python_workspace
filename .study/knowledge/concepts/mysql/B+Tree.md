# B+Tree

## 한 줄 정의

B+Tree는 디스크 기반 데이터베이스에서 범위 탐색과 삽입, 조회를 안정적으로 처리하기 위한 다진 탐색 트리 구조다.

## 왜 배웠나

MySQL InnoDB 인덱스가 왜 단순 이진트리나 해시가 아니라 B+Tree를 쓰는지 이해하기 위해 배웠다.

## 핵심 질문

- B+Tree는 왜 DB 인덱스에 적합한가?
- B-Tree와 B+Tree는 무엇이 다른가?
- 클러스터드 인덱스는 B+Tree와 어떻게 연결되는가?
- 범위 탐색에서 leaf node 연결이 왜 중요한가?

## 직접 검증한 것

- InnoDB 구조에서 클러스터드 인덱스, AHI, Buffer Pool의 역할을 나눠 보았다.
- INSERT 한 줄이 들어갈 때 여러 자료구조가 함께 움직이는 흐름을 추적했다.

## 헷갈리는 지점

- 해시는 단건 조회에는 강하지만 범위 탐색에는 약하다.
- B+Tree는 메모리 자료구조라기보다 디스크 페이지 접근을 줄이는 구조로 이해해야 한다.
- 클러스터드 인덱스는 보조 인덱스와 저장 위치의 의미가 다르다.

## 연결 개념

- InnoDB
- clustered index
- secondary index
- page split
- buffer pool
- adaptive hash index

## 관련 notes

- `.study/notes/04~05/0511 B+트리 - C 언어 문자열 출력 오류 수정 - Google Gemini.mhtml`

## 관련 산출물

- `.blog/day0511_mysql_btree.html`
- `.blog/mysql_commands.html`
- `.study/pdf/MySQL_서버구축및운영관리.pdf`
- `.study/pdf/MYSQL_고급.pdf`
