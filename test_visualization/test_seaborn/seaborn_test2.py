import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

flights = sns.load_dataset('flights')
# 1949년부터 1960년까지 매월 항공편 승객 수에 대한 데이터셋
# 시계열데이터
print(flights.head())   # 데이터셋의 처음 5행을 출력하여 데이터 구조 확인하기
print(type(flights))    # 데이터셋의 타입 확인하기 (pandas.DataFrame)
print(flights.info())   # 데이터셋의 정보 확인하기 (열 이름, 데이터 타입, 결측치 여부 등)
# <class 'pandas.DataFrame'>
# RangeIndex: 144 entries, 0 to 143
# Data columns (total 3 columns):
#  #   Column      Non-Null Count  Dtype   
# ---  ------      --------------  -----   
#  0   year        144 non-null    int64   
#  1   month       144 non-null    category
#  2   passengers  144 non-null    int64   
# dtypes: category(1), int64(2)
# memory usage: 2.9 KB
# None

def test1():
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='year', y='passengers', data=flights)
                 
    plt.title('Number of Passengers Over Time')
    plt.xlabel('Year')
    plt.ylabel('Number of Passengers')
    plt.show( )

def test2():
    # 기존 전역 flights를 그대로 유지하기 위해 복사본을 사용
    flights2 = sns.load_dataset('flights')

    # 'year'와 'month' 열을 문자열로 변환 후 결합
    flights2['year'] = flights2['year'].astype(str)
    flights2['month'] = flights2['month'].astype(str)
    # 새로운 'date' 열 생성
    flights2['date'] = pd.to_datetime(flights2['year'] + '-' + flights2['month'])
    # date 순으로 정렬
    flights2 = flights2.sort_values('date')

    plt.figure(figsize=(12, 6))
    sns.lineplot(x='date', y='passengers', data=flights2)
    plt.title('Monthly Number of Passengers Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Passengers')
    plt.show()

def test3():
    '''
    히트맵 (Heatmap) : 데이터를 색상으로 표현해서 시각화한 그래프
    - 변수 간의 상관관계를 색으로 시각화함
    - 2차원 데이터를 나타내는데 씀
    '''
    # 'year'와 'month'로 그룹화하여 'passengers' 값 합계 계산
    flights_grouped = flights.groupby(['year', 'month']).sum( ).unstack(level=0)

    # 히트맵 생성
    plt.figure(figsize=(12, 8))
    sns.heatmap(flights_grouped['passengers'], annot=True,
    fmt="d",
    cmap="YlGnBu", linewidths=0.5)
    plt.show( )

if __name__ == '__main__':
    # test1()
    # test2()
    test3()