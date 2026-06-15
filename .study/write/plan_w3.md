# 3주차 학습 계획 — 약점 보완 & 구체 액션

## 약점 자가진단 (1·2주차 회고 기반)

- **테스트 코드 전무** — 이번 2주 내내 어떤 파일에도 `unittest` / `pytest` 를 쓴 적이 없다. "가설 통과" 를 선언하면서 자동화된 테스트로 뒷받침한 것이 하나도 없다는 뜻이다.
- **match/case 깊이 부족** — guard 조건(`case x if x > 0`), 구조 분해(`case [x, y]`) 를 실습하지 못했다.
- **제너레이터 · iterator 프로토콜 미학습** — `__iter__`/`__next__` 를 직접 구현한 적이 없다. python_collection 에서 list 메서드만 다뤘다.
- **타입 힌트 미활용** — 모든 코드가 타입 힌트 없이 작성됐다. abstraction.html CH04의 Protocol 학습과 연계해 적용 연습이 필요하다.

## 3주차 구체 계획

1. **테스트 코드 작성** — 기존 미션 파일(`input_mission1.py`, `list_mission1.py` 등) 중 최소 3개에 `unittest.TestCase` 추가. 회고의 "가설·결론" 구조를 테스트 케이스로 표현하는 연습.
2. **SQL · pandas 연결** — `python_fileio` 의 CSV R/W 를 pandas DataFrame 과 연결해 실습. 새 의문: "SQL JOIN 과 DataFrame merge 는 내부적으로 어떻게 다른가?"
3. **타입 힌트 소급 적용** — `python_module/module/my_module.py` 의 함수들에 파라미터 · 반환 타입 힌트 추가.
4. **제너레이터 학습** — `python_collection/` 에 `__iter__`/`__next__` 직접 구현 파일 추가.
