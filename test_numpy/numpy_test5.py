# path : numpy_test5.py
# numpy 모듈의 배열을 이용한 그래프 그리기

import numpy as np
import matplotlib.pyplot as plt

# linspace() 함수 : 시작값과 끝값을 지정하여, 그 사이의 값을 균등 간격으로 생성하는 함수
# linspace(시작값, 끝값, 생성할 값의 갯수)
x = np.linspace(-5, 5, 50) # -5 ~ 5 사이의 값을 균등 간격으로 50개 생성
sin = np.sin(x)
plt.plot(x, sin, label='sin(x)')
plt.legend()
# plt.show()
print("---------------------------------------")

# 데이터 셈플링 (표본 추출) : choice() 함수 사용
# np.random.choice(값의 배열, size=None, replace=True, p=None)
# a : 배열변수 (배열값을 사용해도 됨), 정수 숫자 (range(정수) 범위의 랜덤값을 만듦)
# size : 정수숫자, 추출할 데이터 갯수 지정
# replace : True 아님 False, 같은 값 여러번 선택 가능(True) | 불가능 (False)
# p : 배열변수나 배열 표기, 각 값의 선택 확률을 지정함 (단, 확률의 합계는 1이어야 함)

ch1 = np.random.choice(5, 5, replace=True) # shuffle() 과 같음
# 5 : range(5) 로 적용됨 => 0 ~ 4 사이의 랜덤변수 5개 발생. 중복 안됨
print(ch1)
print(type(ch1))

ch2 = np.random.choice(5, 3, replace=False) # 중복 허용됨
print(ch2)
print(type(ch2))

ch3 = np.random.choice(5, 10)
print(ch3)
print(type(ch3))
print("---------------------------------------")

ch4 = np.random.choice(5, 10, p=[0.1, 0, 0.3, 0.6, 0])
# 0~4 사이의 정수 10개 추출 ( 중복 가능)
# p=[0.1(숫자0의 선택확률), 0(숫자 1의 선택확률), 0.3(숫자 2의 선택확률), 0.6(숫자 3의 선택확률), 0(숫자 4의 선택확률)]
# 유사하게 선택됨
print(ch4)
print("---------------------------------------")

# numpy 에서 난수 생성함수 3가지 : rand(), randn(), randint()
# rand(갯수) : 0.0 <= 난수 < 1.0 사이의 균일한 확률분포로 난수를 갯수만큼 발생함
r1 = np.random.rand(10)
print(r1)
print(type(r1))

r2 = np.random.rand(3, 5) # 3행 5열의 2차원 배열로 생성하고,15 개의 난수가 발생
print(r2)
print(type(r2), r2.shape, r2.ndim)
print("---------------------------------------")

# randn(갯수)
# 기댓값이 0이고 표준편차가 1인 표준정규분포를 따르는 난수를 생성함
# 표준정규분포 : 숫자들이 가운데로 많이 모이고 양쪽으로 갈수록 점점 적어지는 모양으로 말함 (종모양)
# 기댓값 == 평균
# 숫자들이 0을 중심으로 모여있다는 뜻
# 표준편차는 값이 퍼져있는 정도를 의미함
# 표준편차(평균의 차이)가 1이면, 값들이 -1 <= 0 <= 1 범위의 값이 많이 모여있다는 의미임
r3 = np.random.randn(10) # 1차원배열로 값 10개 생성
print(r3)
print(type(r3), r3.shape, r3.ndim)

r4 = np.random.randn(3, 5) # 3행 5열의 2차원 배열로 값 15개 생성
print(r4)
print(type(r4), r4.shape, r4.ndim)
print("---------------------------------------")

# randint(low, high=None, size=None, dtype=int)
# low <= 난수 < high 사이의 정수 난수를 size 만큼 생성하며 배열 생성
# high 가 생략되면 0 ~ low 까지의 범위에서 값 발생함
r5 = np.random.randint(10, size=10) # 0 이상 10 미만의 정수 난수 10개 생성
print(r5)
print(type(r5), r5.shape, r5.ndim)

r6 = np.random.randint(10, 20, size=10) # 10 이상 20 미만의 정수 난수 10개 생성
print(r6)
print(type(r6), r6.shape, r6.ndim)

r7 = np.random.randint(10, 20, size=(3, 5)) # 10 이상 20 미만의 정수 난수 15개 생성
print(r7)
print(type(r7), r7.shape, r7.ndim)
print("---------------------------------------")


