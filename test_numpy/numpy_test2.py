# path : numpy_test2.py
# numpy 는 Ndarray 클래스를 사용함 : C언어로 만든 내부 로직을 제공함
# type 을 확인하면, 배열의 자료형은 numpy Ndarray
# Ndarray : N-Dimensional Array 의 줄임말 (N차원 배열)
# 1차원 배열부터 다차원 배열을 다룰 수 있음

import numpy as np

# 2차원 배열 만들기
# 1차원 배열 여러 개 (값의 갯수가 같아야 함) 을 하나로 묶으면 => 2차원 배열이 됨
# 1차원 배열 == 백터 (vector)
# 2차원 배열 == 행렬 (matrix) : 행과 열로 구성된 행렬(표) 형태
# [list], [list], [list], ... => list of list 의 형태 (단, 리스트 안의 값 갯수가 같아야함)

tar = np.array([[1, 2, 3], [4, 5, 6]])
print(tar)
print(len(tar), tar.size, np.size(tar))
print(len(tar[0])) # 3 - 0행 안의 값(열) 갯수
print(tar.size, np.size(tar)) # 6 : 총 값 갯수
print("---------------------------------------")

# 2차원배열의 각 값(요소)에 접근 (인덱싱) : 배열변수[행순번][열순번]
# 행 (row, 제 2축) : 세로방향 순번
# 열 (column, 제 1축) : 가로방향 순번
# 2중 for 문 사용
for r_index in range(0, len(tar)): # range(2) --> 1, 2 : 행 반복
    for c_index in range(len(tar[r_index])): # range(3) --> 1, 2, 3 : 열 반복
        print("tar[{}][{}] : {}".format(r_index, c_index, tar[r_index][c_index]))
print("---------------------------------------")

# 3차원배열
# 값의 종류가 같고, 행과 열의 갯수가 같은 2차원 배열들의 묶음
# 면(깊이,depth), 행(줄row,높이), 열(칸,column) 로 구성됨 => Tensor (텐서)라고 함
thar = np.array([[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]], 
                 [[13, 14, 15, 16],[17, 18, 19, 20], [21, 22, 23, 24]]])

print(thar)
print(len(thar))        # 2 : 면의 갯수
print(len(thar[1]))     # 3 : 행의 갯수 (1면의)
print(len(thar[0][0]))  # 4 : 열의 갯수
print("---------------------------------------")

# 3차원 배열 안의 각 값(요소)를 다루려면 (인덱싱) : 배열 변수 [면순번][행순번][열순번]
# 3중 for 문 사용
for d_index in range(len(thar)): # range(2) --> 1, 2 : 면 반복
    for r_index in range(len(thar[d_index])): # range(3) --> 1, 2, 3 : 행 반복
        for c_index in range(len(thar[d_index][r_index])): # range(4) --> 1, 2, 3, 4 : 열 반복
            print("thar[{}][{}][{}] : {}".format(
                d_index, r_index, c_index, 
                thar[d_index][r_index][c_index]))
        print("---------------------------------------")
print("---------------------------------------")

# 배열의 차원(ndim)과 크기(shape) 알아내기
# 배열변수.ndim, 배열변수.shape
print(tar.ndim, tar.shape) # 2, (2, 3) : 2차원 배열, 2행 3열
print(thar.ndim, thar.shape) # 3, (2, 3, 4) : 3차원 배열, 2면 3행 4열
print("---------------------------------------")

# 1차원 배열의 ndim, shape 확인
ar = np.array([1,2,3]) # 1차원 배열
print(ar.ndim, ar.shape) # 1, (3,) : 1차원 배열, 3개의 요소
print("---------------------------------------")

# 2차원 배열의 인덱싱 : 배열변수[행순번][열순번] == 배열변수[행순번, 열순번]
# 콤마 (,)로 구분하여 이용 가능 => 축(axis) 라고 함 (거의 이 방식을 많이 씀)
# 행(x축), 열(y축), 면(z축)
print('0행0열의 값 : ', tar[0][0], tar[0, 0]) # [1, 2, 3]
print('1행0열의 값 : ', tar[1][0], tar[1, 0]) # [4, 5, 6]
print('마지막행의 마지막열 값 : ', tar[-1][-1], tar[-1, -1])

arr = np.ones((2, 3)) # 2행 3열의 모든 값이 1인 배열
print(arr.ndim, arr.shape) # 2, (2, 3) : 2차원 배열, 2행 3열
print(arr)

arr = np.zeros((3, 4)) # 3행 4열의 모든 값이 0인 배열
print(arr.ndim, arr.shape) # 2, (3, 4) : 2차원 배열, 3행 4열
print(arr)

arr = np.full((2, 3), 7) # 2행 3열의 모든 값이 7인 배열
print(arr.ndim, arr.shape) # 2, (2, 3) : 2차원 배열, 2행 3열
print(arr)

arr = np.empty((2, 3)) # 2행 3열의 모든 값이 쓰레기값. (최신버전에선 0으로)
print(arr.ndim, arr.shape) # 2, (2, 3) : 2차원 배열, 2행 3열
print(arr)
print("---------------------------------------")
