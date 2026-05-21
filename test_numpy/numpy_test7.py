# path : numpy_test7.py
# 2026-05-21

import numpy as np

# 배열 생성시에 array() 함수 사용
# array() 함수 사용시에 dtype 매개변수를 이용해서, 배열에 저장되는 값의 종류를 명시할 수 있음
# dtype 을 사용하지 않으면, 자동으로 기록되는 값의 자료형이 지정됨
x1 = np.array([1, 2, 3]) # 정수형 배열
print(x1.dtype) # int64
print(type(x1))

x2 = np.array([1.0, 2.0, 3.0]) # 실수형 배열
print(x2.dtype) # float64
print(type(x2))

# 배열 생성시 dtype 인수에 자료형을 지정할 경우
# 제공되는 접두사 뒤에 바이트 (또는 비트)수를 지정함. Ex) int64, float64
# 문자타입 (char type) 접두사 뒤에는 글자수를 지정할 수 있음
# b : boolean
# i : integer
# f : float
# u : unsigned integer (부호 없는 정수 : 0과 양수는 그대로 사용. 음수를 양수로 변환한 정수)
# ex) -128 ~ 127 사이의 정수는 int8, 0 ~ 255 사이의 정수는 uint8
# c : complex (복소수)
# O : object (객체)
# S : string (문자열), 1byte : 1글자
# U : unicode (유니코드), 4byte : 1글자
# 사용 예 : i8 (정수 8바이트 == int64), f4 (실수 4바이트 == float32), S5 (문자열 5글자), U24 (유니코드 24글자)

x3 = np.array([1, 2, 3], dtype='f') # 실수형 배열로 생성
print(x3.dtype) # float32
print(type(x3)) # [1. 2. 3.] <class 'numpy.ndarray'>
print(x3) # [1. 2. 3.]
print(x3[0] + x3[1]) # 1.0 2.0 3.0 : float + float => float

x4 = np.array([1, 2, 3], dtype='U') # 정수형 배열로 생성
print(x4.dtype)                     # <U1 : 유니코드 1글자
print(type(x4))                     # <class 'numpy.ndarray'>
print(x4)                           # ['1' '2' '3']
print(x4[0] + x4[1])                # 1 2 3 : 문자열 + 문자열 => 문자열

# inf 와 nan
# numpy 에서 무한대를 표현하기 위해 np.inf (infinity) 라는 상수를 제공함
# 정의할 수 없는 숫자를 표현하기 위해 np.nan (not a number 줄임말)
# 예 : 1을 0으로 나누는 경우, 0 에 대한 로그값 계산시 무한대인 np.inf 가 결과로 표시됨
# 예 : 0을 0으로 나누는 경우, np.nan 이 표시

print(np.array([0, 1, -1, 0]) / np.array([1, 0, 0, 0])) # [0. inf -inf nan]
# RuntimeWarning: divide by zero encountered in divide
# RuntimeWarning: invalid value encountered in divide

print(np.log(0)) # -inf
# RuntimeWarning: divide by zero encountered in log

print(np.exp(-np.inf)) # 0.0 : e 를 무한대로 작은수만큼 제곱하라는 뜻 => 0에 가까운 수가 됨
# np.inf : 무한대를 의미함
# -np.inf : -무한대를 의미함
# np.exp(x) : e 를 x 제곱한 값을 계산하는 함수
