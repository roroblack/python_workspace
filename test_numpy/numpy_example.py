# path : numpy_example.py
# numpy 활용 예제
# 2026-05-21

import numpy as np

A = np.array([[1, 2, 3], 
              [4, 5, 6], 
              [7, 8, 9]])
x = np.array([10, 20, 30])
# np.dot(A, x)
print(np.dot(A, x)) # [140 320 500]
print("---------------------------------------")



# 행렬을 열백터 또는 행백터로 바꾸어 계산하기
v1 = A[:, 0]
v2 = A[:, 1]
v3 = A[:, 2]
print(np.dot(x[0], v1) + np.dot(x[1], v2) + np.dot(x[2], v3)) # 140 + 400 + 900 = 1440
print("---------------------------------------")

# 크기가 다른 행렬의 곱셈
# m x n 행렬과 n x p 행렬의 곱 결과는 m x p 행렬이 됨
# dot() 함수 사용 가능함
# 그냥 곱하기하면 에러임
A = np.array([[1, 2, 3], [4, 5, 6]])
B = np.array([[1, 2], [3, 4], [5, 6]])
print(np.dot(A, B)) # [[22 28] [49 64]]
# print(A * B) # 에러남 ValueError: operands could not be broadcast together with shapes (2,3) (3,2)
print("---------------------------------------")

# 스칼라와 벡터의 곱셈
V = np.array([[1], [2], [3]]) # 3행 1열 (열백터)
a = 10 
print(V * a) # np.dot(a, V) 와 같음 [[10] [20] [30]]
print("---------------------------------------")

# 연립방정식의 해 구하기
# Ax = b => x + ATb
A = np.array([[4, 3], [3, 2]])
b = np.array([23, 16])
# A 의 역행렬 구함 ( = 오른쪽으로 이항시키기 위함)
invA = np.linalg.inv(A) # inv(행렬) => 역행렬 변환
x = np.dot(invA, b)
print(x) # [2. 5.]
print(np.allclose(np.dot(A, x), b)) # True : 해가 옳바름
print("---------------------------------------")

# solve() 로 해를 구할 수도 있음 : 선형방정식의 개수와 미지수의 개수가 같은 경우
x = np.linalg.solve(A, b)
print(x) # [2. 5.]

#lstsq() 로 해를 구할 수도 있음 : 선형방정식의 개수와 미지수의 개수가 같거나 다른 경우
A = np.array([[1, 4, 3], [1, 3, 2]])
b = np.array([23, 16])
x = np.linalg.lstsq(A, b, rcond=None)[0] # lstsq() 함수는 해가 여러개일 수 있기 때문에, 해가 담긴 배열과 잔차(residuals) 등이 담긴 배열을 반환함. [0] 은 해가 담긴 배열을 의미함
print(x) # [-1. 3. 4.]   

# 행렬식 [A] 구하기 :
A = np.array([[1, 4], [1, 3]])
print(np.linalg.det(A)) # -1.0  
print("---------------------------------------")

# 3 x 3 정방행렬의 행렬식 구하기
A = np.array([[8, 5, 3], [4, 1, 6], [7, 10, 9]])
print(np.linalg.det(A)) # -278.99999999999994
print("---------------------------------------")

# 예제 1 : 반 학생들의 성적으로 등수 매기기
score = np.array([80, 75, 100, 90, 60])
desc_idx = score.argsort()[::-1] # 내림차순정렬한 인덱스 배열 생성
rank = np.empty_like(score) # score 와 같은 크기의 배열을 생성함. 값은 쓰레기값이 들어있음
rank[desc_idx] = np.arange(1, len(score) + 1) # 1 ~ 5 까지의 정수 배열 생성
print(score)
print(rank) # [3 4 1 2 5]
print("---------------------------------------")

# 두 행렬의 곱 : dot(A, B)
# 주의 : 작은 크기에 큰 크기를 곱하면 에러
A = np.array([[8, 5, 3], [4, 1, 6], [7, 10, 9]])
B = np.array([[0, 3], [1, 4], [2, 5]])
print(np.dot(A, B)) # [[22 28] [49 64] [82 118]]
# print(np.dot(B, A)) # ValueError: shapes (3,2) and (3,3) not aligned: 2 (dim 1) != 3 (dim 0)
print("---------------------------------------")