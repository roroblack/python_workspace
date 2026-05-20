# path : numpy_test3.py

import numpy as np

# 전치연산 : T 속성 사용함 => 2차원배열명.T
# 2차원 배열의 행과 열을 서로 바꿀 때 사용함 => 2행 3열.T => 3행 2열
ar = np.array([[1, 2, 3], [4, 5, 6]])
print("ar : ", ar, ar.shape)
print(ar.T)
print(ar.T.shape)
print("---------------------------------------")

# 1차원 배열은 전치연산 못 함
# 1차원 배열을 다차원배열로 변경할 수 있음
# reshape() 메소드 사용 => 전체 크기(갯수)는 바뀌지 않음
ar = np.arange(12) # 0 ~ 11 까지의 정수로 구성된 1차원 배열
print("ar : ", ar, ar.shape)
print(type(ar))
print(ar.ndim, ar.size)
print("---------------------------------------")

#3행 4열의 2차원배열로 바꾸기 
br = ar.reshape(3, 4)
print(br, br.ndim, br.size)
print(br.T)
print(np.transpose(br))
print(np.swapaxes(br, 0, 1))
print("---------------------------------------")

# reshape() 사용시에 면, 행, 열 갯수를 지정하지 않고 -1로 표기 가능
# -1로 표시된 항목은 내부 계산에 의해 갯수가 자동 설정됨
br2 = ar.reshape(3, -1) # 3행, 열 갯수는 자동 계산됨 => 4열
print(br2, br2.ndim, br2.size)
print (br2.shape)
print("---------------------------------------")

# 1차원 배열을 3차원 배열로 바꾸기
br3 = ar.reshape(2,2,-1)
print(br3, br3.shape)

br4 = ar.reshape(2, -1, 3)
print(br4, br4.shape)
print("---------------------------------------")

# flatten(), ravel() 함수 c
# reshape 의 반대일을 함. 다차원 배열을 1차원 배열로 바꿔주는 함수
print('br : ', br.shape)   # br : (3, 4)
print(br.flatten())
print(br.ravel())

print('br3 : ', br3.shape)   # br3 : (2, 2, 3)
print(br3.flatten())
print(br3.ravel())
print("---------------------------------------")

# newaxis 함수
# 배열의 차원을 1 증가 시키는 함수
# 1차원 배열 => 2차원 배열 => 3차원 배열
# 예 : 값의 갯수가 5개인 1차원 배열을 2차원으로 바꿀 때 (5, 1) 또는 (1, 5)로 변경 가능함
# 1차원 배열 [값 5개] 과 2차원 배열 [[값 5개]] 는 같은 값이지만, 차원이 다름
xr = np.arange(5) # 5 개 : 0 ~ 4 까지의 정수 수열로 초기화된 배열 객체 생성됨
print(xr)
print(xr.shape) # (5,)
print(xr.reshape(1, 5)) # 1행 5열의
print(xr.reshape(5, 1)) # 5행 1열의 2차원 배열로 변경
print("---------------------------------------")

# 총 값의 갯수가 같은 배열에 대해 차원만 1 증가 시키는 경우, newaxis 사용 가능
print(xr[:, np.newaxis]) # [행, 열] 을 의미함. => 값들이 행이됨 => 5행 1열이 됨
print(xr[:, np.newaxis].shape)
# : (콜론) 의미는 모든 값 (처음부터 끝까지 슬라이싱함)
print(xr[np.newaxis, :]) # 1행 5열이 됨
print(xr[np.newaxis, :].shape)