# path : pandas_test5.py
# 데이터프레임조작
# 2026-05-22


import pandas as pd
import numpy as np
import seaborn as sns

# 데이터 갯수 세기 : count()
# NaN 은 제외됨
s = pd.Series(range(10))
print(s)
s[3] = np.nan
print(s)
print(s.count()) # 9
print("----------------------------------------------------------")

# DataFrame 에 count 는 각 열별 데이터 갯수임
# 데이터프레임에 값이 누락된 부분을 찾을 
np.random.seed(0)
df = pd.DataFrame(np.random.randint(5, size=(4, 4)), dtype=float)
print(df)
df.iloc[2, 3] = np.nan
print(df.count()) # 열별로 갯수 셈. 세로로 출력
print("----------------------------------------------------------")

# 타이타닉호 승객 데이터를 데이터프레임으로 만듦
titanic = sns.load_dataset('titanic')
print(titanic.head()) # [5 rows x 15 columns]
print("----------------------------------------------------------")

# 카테고리 갯수 세기 : value_counts()
# 시리즈의 값이 정수 | 문자열로 된 카테고리 갯수를 리턴함
# 카테고리 : 기록된 값을 종류별로 구분한 것
# print(titanic.value_counts())
np.random.seed(1)
s2 = pd.Series(np.random.randint(6, size=100)) # 0~5 사이의 정수 100개
print(s2.tail()) # 마지막 5개 출력
print(s2.value_counts()) # 기록된 값 별로 갯수 카운트함
print("----------------------------------------------------------")

# 데이터프레임에는 value_counts() 함수가 없음 
# 각 열(하나의 시리즈임)마다 별도로 적용해야 함
print(df)
print(df[0].value_counts())
print("----------------------------------------------------------")

# 정렬 : sort_index(), sort_values()
# sort_index() : 값을 정렬하고 나서 index 배치를 리턴
# sort_values() : 정렬하고 난 값들을 리턴

# s2 시리즈의 값에 따라 데이터 갯수를 인덱스로 정렬한다면
print(s2.value_counts())
print(s2.value_counts().sort_index()) # 인덱스 오름차순으로 정렬
print("----------------------------------------------------------")

# NaN 이 있는 경우에는 정렬하면 NaN 이 가장 나중에 배치됨
print(s)
print(s.sort_values()) # 값으로 정렬
print("----------------------------------------------------------")

# 내림차순정렬하려면, ascending=False 옵션 사용
print(s.sort_values(ascending=False)) # NaN 은 마지막에 위치함
print("----------------------------------------------------------")


# 데이터프레임처럼 여러 컬럼(열, 시리즈)을 가진 경우
# sort_values() 로 정렬시에 by 인수로 정렬 기준이 되는 컬럼(열)을 지정함
print(df)
print(df.sort_values(by=3)) # 3번 열을 기준으로 정렬
print("----------------------------------------------------------")


# 행, 열 합계 : sum()
# 행과 열의 합계를 구할 때 sum(axis = 1 | 0)
# axis 인수에는 합계로 없어지는 방향축으 지정함 : 0(행), 1(열)
np.random.seed(1)
df2 = pd.DataFrame(np.random.randint(10, size=(4, 8)))
print(df2)
print("----------------------------------------------------------")

# 행방향으로 합계를 구할 때는 sum(axis=1) 로 지정
print(df2.sum(axis=1)) # 행별 합계 => 열이 축소됨 (0개 => 1개)
print("----------------------------------------------------------")

# 열방향으로 합계를 구할 때, 컬럼을 하나 추가해서 합계를 기록 저장할 수 있음
df2['RowSum'] = df2.sum(axis=1)
print(df2)
print("----------------------------------------------------------")

# 열별 합계
print(df2.sum()) # axis=0 이 기본값이므로 생략 가능
print("----------------------------------------------------------")

# 합계 행을 추가한다면
df2.loc['colTotal', :] = df2.sum()
print(df2)
print("----------------------------------------------------------")

# 집계함수에 apply() 함수 적용 가능
# sum() : 합계, mean() : 평균, count() : 갯수 등
# apply()
# 행이나 열단위로 좀 더 복잡한 계산을 적용해야 할 때 쓰는 함수
# 복잡한 계산식은 사용자정의함수로 작성 or 람다함수(이름없는 함수)를 사용
df3 = pd.DataFrame({
    'A': [1, 2, 3, 5, 10],
    'B': [4, 5, 6, 7, 8],
    'C': [7, 8, 9, 10, 11]
})
print(df3)
print("----------------------------------------------------------")





#-------------------------------------------------------------------
# 예: 각 열의 최대값과 최소값의 차이를 구한다면
print(df3.apply(lambda x: x.max() - x.min()))
print("----------------------------------------------------------1")

# 예: 각 행의 최대값과 최소값의 차이를 구한다면
print(df3.apply(lambda x: x.max() - x.min(), axis=1))
print("----------------------------------------------------------2")

# 예: 각 열에 대해 어떤 값이 얼마나 사용되는지를 확인한다면
print(df3.apply(lambda x: x.value_counts(), axis=0))
print("----------------------------------------------------------3")

# 타이타닉호의 승객 중 20살을 기준으로
# 20살 이상이면 성인 (adult), 20살 미만이면 미성년자 (child)로 구별하고
# 라벨링된 컬럼을 추가해서 표시되게 한다면
titanic['성인구분'] = titanic.apply(lambda r: 'adult' if r.age >= 20 else 'child', axis=1)
print(titanic.tail(10))
print("----------------------------------------------------------4")

# fillna() 함수
# NaN 을 원하는 값으로 바꿀 때 사용
print(df3)
print(df3.apply(lambda x: x.value_counts(), axis=0).fillna(0.0).astype(int))
print("----------------------------------------------------------5")
# astype(자료형) 함수 : 전체 데이터의 자료형을 바꿀 때 사용

# 실수형 값을 카테고리 값(컬럼단위)으로 변환
# cut() 함수 : 실수값을 경계선으로 지정하는 경우에 사용 (분류)
# qcut() 함수 : 갯수가 똑같은 구간으로 분류할 때 사용

# 예: 나이 데이터를 가진 리스트의 경우
ages = [0, 2, 10, 21, 23, 37, 31, 61, 20, 41, 32, 101]
# cut() 을 사용해서 카테고리(열) 값으로 변경할 수 있음
# bins 인수로 분류하는 기준값을 지정함, 기준을 벗어나는 값은 NaN이 됨
bins = [1, 20, 30, 50, 70, 100]
labels = ['미성년자', '청년', '중년', '장년', '노년']
result = pd.cut(ages, bins=bins, labels=labels)
print(result)  # 분류된 결과 출력
print(type(result))  # <class 'pandas.core.arrays.categorical.Categorical'>
print("----------------------------------------------------------6")

# cut() 의 반환 자료형이 Categorical 클래스 객체임
# 이 객체는 categories 속성으로 라벨 문자열을, codes 속성으로 정수로 인코딩된 값을 확인할 수 있음
print(result.categories)  # Index(['미성년자', '청년', '중년', '장년', '노년'], dtype='object')
print(result.codes)  # [-1  0  0  1  1  2  2  3  0  2  2 -1]
print("----------------------------------------------------------7")

# 위 결과를 데이터프레임에 적용한다면
df4 = pd.DataFrame(ages, columns=['age'])
print(df4)
df4['age_category'] = pd.cut(ages, bins=bins, labels=labels)
print(df4)
print("----------------------------------------------------------8")
