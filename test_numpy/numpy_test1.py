# path : numpy_test1.py
# numpy 모듈 : 행렬 배열을 다루기 위한 모듈

'''

배열의 특징 (리스트와 다른점)
1. 처음부터 저장개수 정함 (차이)
2. 한종류 데이터만 저장 (차이)
3. 리스트처럼 idx 씀

'''

import numpy as np
# 1차원 배열 다루기 : numpy.array() 함수 사용 (한가지 종류로만 저장된 리스트를 초기값으로 사용 가능)
# 배열 변수 = np.array([list])
# 배열 변수는 배열객체의 주소를 가짐 : 배열 레퍼런스 (주소 저장 변수)
# 정수 [실수] 논리값으로 구성됨

ar = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

print(ar)
print(ar.dtype, type(ar))
print(len(ar))


# 배열은 백터화 (각 인덱스별로) 연산이 가능하다. 
# 리스트일 때 백터화 연산 예
datalist = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(type(datalist))

# 리스트 안의 각 값을 모두 2배 증가처리 연산을 수행한다면
double_datalist = []
for data in datalist:
    double_datalist.append(data * 2)

print(double_datalist)

print(ar * 2)

# 배열의 백터화 연산은 비교연산, 논리연산, 산술연산 모두 가능함
# Ndarray 클래스에 각연산자에 대한 연산자 오버로딩 메소드가 제공
ar1 = np.array([0, 1, 2])
ar2 = np.array([10, 20, 30])

print(2 * ar1 + ar2) # 2 * ar1[0] + ar1[0] + 2 * ar1[1] + ar1[1] + ...
# [10, 22, 34]

print(ar1 == 2) # ar1[0] == 2, ar1[1] == 2, ar1[2] == 2
# [False, False, True]

print((ar1 == 1) & (ar2 == 20)) # [False, True, False] & [False, True, False] => [False, True, False]

# 1 차원 배열의 각 인덱스 위치의 값(요소, element)에 접근 : 인덱싱 (Indexing)
for index in range(0, ar.size):
    print(index, ' : ', ar[index])
    
