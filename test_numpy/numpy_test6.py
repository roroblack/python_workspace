# path : numpy_test6.py

import numpy as np

# 기술 통계 (descriptive statistics) : 통계 계산용 함수를 말함
# 데이터 갯수(count), 평균(mean), average), 분산(variance), 표준편차(standard deviation)
# 최대값(maximum), 최소값(minimum), 중앙값(median), 사분위수(quartiles) 등등이 있음

x = np.random.randint(-10, 50, size = 30) # -10 ~ 49 사이의 정수 30개 발생
print(x)

# 데이터 갯수 : len()
print(len(x))

# 평균 : np.mean(배열변수)
print(np.mean(x))

# 분산 : np.var(배열변수)
print("var : ", np.var(x))
print("unbiased var : ", np.var(x, ddof=1)) # 비편향분산

# 표준편차 : np.std(배열변수)
print("ss : ", np.std(x))

# 최대값 : np.max(배열변수)
# 최소값 : np.min(배열변수)
# 중앙값 : np.median(배열변수)
print("max : ", np.max(x))
print("min : ", np.min(x))
print("median : ", np.median(x))

# 사분위수 : np.percentile(배열변수, [25, 50, 75])
# 데이터를 오름차순정렬 했을 떄, 1/4, 2/4 (== 중앙값), 3/4, 4/4 (== 최대값) 위치에 있는 값들을 말함
# 1사분위, 2사분위, 3사분위, 4사분위 (최대값) 라고도 함
# 데이터 갯수가 100개 이면, 1사분위는 25번째 값이 됨
print("quartiles : ", np.percentile(x, 0))          # 최소값
print("quartiles : ", np.percentile(x, 25))         # 1/4
print("quartiles : ", np.percentile(x, 50))         # 2/4 (== 중앙값)
print("quartiles : ", np.percentile(x, 75))         # 3/4
print("quartiles : ", np.percentile(x, 100))        # 4/4 (== 최대값)


# 난수 발생과 카운팅
# 난수 (random number) : 프로세스가 임의로 발생하는 수
# numpy 의 random 서브패키지에서 함수들이 제공됨

# np.random.seed(인수)
# seed : 난수의 시작값
# 인수 : 정수 >= 0 사용함
np.random.seed(0) # 난수의 시작값 지정과 랜덤값 고정
# 설정 이후 한번 발생된 랜덤값이 계속 동일한 값이 발생됨 확인함

print(np.random.rand(5)) # 0.0 <= 난수 < 1.0 실수형숫자 5개 발생
# 시드 적용 전 :
# [0.27166867 0.54937979 0.50184348 0.65881047 0.68929445]
# [0.38033911 0.5216288  0.21754864 0.46148575 0.46906498]
# 시드 적용 후 :
# [0.5488135  0.71518937 0.60276338 0.54488318 0.4236548 ]
# [0.5488135  0.71518937 0.60276338 0.54488318 0.4236548 ]

# 데이터 섞기 : shuffle() 함수 사용
x = np.arange(10)
print(x) # [0 1 2 3 4 5 6 7 8 9]
np.random.shuffle(x)
print(x) # [3 1 8 7 9 0 6 4 2 5]