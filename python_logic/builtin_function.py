# builtin_function.py
# 파이썬이 제공하는 내장함수 확인용 소스 파일

'''
파이썬이 제공하는 내장함수는 기본으로 제공됨
별도의 import 선언하지 않고 바로 사용함
max, min, type, len, range, str, int, float, print, input 등
'''

# type(값 | 변수명) -> 값의 자료형을 리턴하는 함수임 (class <자료형>)
# len(값 | 변수명) -> 길이(저장된 값의 갯수) 리턴하는 함수임
a = 'abcd'
b = [1, 2, 3, 4, 5]
print(type(a), len(a), type(b), len(b))

# max(값들 | 변수) -> 가장 큰 값(최대값) 리턴 함수
print(max('abcdefg'))  # g
print(max('123456789')) # 9

# min(값들 | 변수) -> 가장 작은 값(최소값) 리턴 함수
print(min('abcdefg'))  # a
print(min('123456789')) # 1

# 주석 (comment) : 코드의 내용 이해를 돕기 위한 설명 문구
# 한 줄 주석
'''
여러 줄 주석
작은 따옴표 또는 큰 따옴표를 앞뒤에 3개씩 표시함
파이썬에서는 single quotation or double quotation 은 동일하게 취급함
'''
"""
여러 줄 주석
"""

# abs(값 | 변수) -> 절대값 리턴
print(abs(-10))  # 10

# 파이썬에서는 변수는 반드시 값을 가져야 생성이 됨 (메모리에 할당)
# num   # NameError: name 'num' is not defined. Did you mean: 'sum'?
# print(num)

# 파이썬에서는 변수에 기록할 값의 종류(data type : 자료형)을 정하지 않음
# Java : 자료형 변수명 = 기록할 값;
# Python : 변수명 = 기록할값  => 변수방에 기록된 값에 따라 변수의 자료형이 정해짐 : 동적 할당
value = 100
print(value, type(value))

value = 'python'
print(value, type(value))

value = 3.14
print(value, type(value))

value = False
print(value, type(value))

# 변수 제거 : del 변수명
del value
print(value, type(value))  # NameError: name 'value' is not defined. Did you mean: 'False'?
