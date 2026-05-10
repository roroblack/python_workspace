# naming.py

# 식별자 : 개발자가 지어주는 이름
# 변수 (variable) : 프로그램 구동시 메모리(RAM)에 값 기록하는 공간(방)
# 함수 (function) : 반복 사용되는 코드를 별도로 분리 작성해서 이름 붙여준 것 (소스 코드의 조각 코드들)
# 모듈 (module) : 함수들을 모아 놓은 파일
# 클래스 (class) : 파이썬은 객체지향형 스크립트 언어임

# 파이썬의 이름 작성 규칙 : 식별자 조건 (Naming Rule)
# 1. 대소문자 구분함 : name 과 Name 과 NAME 은 다른 이름임
NAME = '홍길동'
name = '이순신'
Name = '황진이'
print(NAME, name, Name)

# 2. 이름에 첫글자에 숫자 사용 못 함 : 1num (에러)
# 1num = 100   # SyntaxError: invalid decimal literal
# print(1num, type(1num))

# 3. 이름의 첫글자는 문자 또는 _ (underscore) 만 사용할 수 있음
_score = 100.0
print(_score, type(_score))

# 4. _를 제외한 기호문자, 공백 사용 못 함
# num& = 12  # SyntaxError: invalid syntax
# print(num&)

# 5. 이름 중간 또는 끝에는 숫자 사용할 수 있음 : num1, first1_num
num1 = 10
num2 = 20
print(num1 > num2)  # 10 > 20 => False

# 6. 예약어 (프로그램 언어가 사용하기 위해 별도로 정해 놓은 단어들, keyword)는 이름으로 사용할 수 없음
# True = 1  # SyntaxError: cannot assign to True
true = 1
print(true, type(true))

# 예약어 확인 : keyword 모듈에서 제공됨 => import 해서 사용함
import keyword

print(keyword.kwlist)
print(len(keyword.kwlist))  # 35개의 예약어 정해져 있음
