# pandas_test7.py

# 인터넷 상의 데이터베이스 자료 읽어오기
# 추가 설치 필요 : pandas-datareader  (임포트시 모듈명 : pandas_datareader)
# 데이터베이스 자료 제공하는 사이트 확인 필요함 (유료 사이트 주의)
'''
참조 : https://pandas-datareader.readthedocs.io/en/latest/index.html
사이트 종류 확인 : https://pandas-datareader.readthedocs.io/en/latest/readers/index.html
사이트 종류 : FRED, Farma/French, World Bank, OECD, Eurostat, EDGAR index, TSP Fund Data,
                Oanda currency historical rate, Nasdaq Trader Symbol Definitions  등
'''

import pandas as pd
import numpy as np

# 데이터 검색을 위한 날짜 지정할 때 datetime 모듈 이용할 수 있음
import datetime as dt

# 날짜는 datetime 함수를 이용해도 되고, 문자열로 지정해도 됨
# 내부적으로 자동으로 dateutil 패키지가 사용되어 날짜가 됨
# dt_start = dt.datetime(2015, 1, 1)
# dt_end = '2016, 6, 30'    # dateutil 에 의해 자동 날짜가 됨
dt_start = dt.datetime(2023, 1, 1)
dt_end = dt.datetime(2024, 6, 30)

# data_source = '읽어올 웹사이트 url' 지정함
# 제공되는 url 은 해당 웹사이트에 가서 직접 확인 필요함
# pandas_datareader 패키지가 제공하는 기본 웹사이트 정보 읽어오기 함수가 있음

# FRED 사이트의 데이터베이스에서
# 미국 국가총생산 (GDP), 모든 항목이 포함된 소비자가격지수(CPAUCSL),
# 식료품 및 연료를 제외한 소비자가격지수(CPILESL) 를 가져온다면,
# data_source 에 각 데이터에 대한 url 을 지정하면 됨
#  https://fred.stlouisfed.org/series/GDP
#   https://fred.stlouisfed.org/series/CPIAUCSL
#   https://fred.stlouisfed.org/series/CPILFESL
# pdr.get_data_fred() 함수 사용하면, 자동 data_source 가 FRED 로 설정됨

# 사용방법 1 :
from pandas_datareader import data as pdr

gdp = pdr.DataReader('GDP', 'fred', dt_start, dt_end)
print(gdp)
print(gdp.head())

# python 3.11 까지만 사용할 수 있는 코드임
# python 3.11 이후에서는 pandas-datareader 에서 distutils 없애버렸음 => ModuleNotFoundError: No module named 'distutils'
# 해결방법 : 별도 패키지 추가 설치 필요함
# pip install setuptools
# pip install distutils  => 실패시 파이선 3.11 사용 권장 => 3.13 그대로 사용해도 됨
'''
해결 방법 : 가상환경 지우고 새 가상환경 만들기함 (파이썬 3.11 로 만듦)
터미널에서 >
deactivate 가상환경이름
rmdir 가상환경폴더명
예 >
deactivate .venv
rmdir .venv => 엔터

3.11로 가상환경 다시 만들기함 (가상환경 충돌 발생할 수 있으므로, vscode 다시 시작함)
python -3.11 -m venv 가상환경이름
예 >
py -3.11 -m venv .venv
활성화 확인
.venv\Scripts\activate 엔터

pip uninstall numpy pandas pandas_datareader -y
pip install numpy==1.24.4 pandas==1.5.3 pandas_datareader==0.10.0
'''

# 사용방법 2 :
import pandas_datareader as pdr

gdp = pdr.get_data_fred('GDP', start=dt_start, end=dt_end)
print(gdp)
print(gdp.head())

# 데이터 코드에 리스트를 넣으면, 여러 개의 항목별 데이터를 동시에 가져옴
# inflation = pdr.get_data_fred(['CPIAUCSL', 'CPILFESL'], start=dt_start, end=dt_end)
# print(inflation)

# 데이터프레임의 고급 인덱싱
# 데이터프레임은 2차원배열임 : (행인덱스, 열인덱스)

# loc 인덱서 (인덱싱 속성)
# 라벨 기반의 2차원 인덱싱에 사용
# 데이터프레임.loc[행라벨] 또는 [행라벨, 열라벨]
df = pd.DataFrame(np.arange(10, 22).reshape(3, 4), index=['a', 'b', 'c'], columns=['A', 'B', 'C', 'D'])
print(df)
print(df.loc['a'])  # 한 행 인덱싱, 세로로 출력
print(df.loc['b':'c'])  # 슬라이싱, 가로로 출력
# print(df['a'])  # KeyError: 'a'  => 반드시 loc 사용
print(df['b':'c'])  # 슬라이싱에는 loc 인덱서 사용 안 해도 됨
# print(df[['b', 'c']])  # 슬라이싱이 아닌 행라벨을 리스트로 나열한 인덱싱시 KeyError: ('b', 'c') 발생함
print(df.loc[['b', 'c']])

print(df.A > 15)  # 비교연산 결과인 False, False, True 로 출력됨
print(df.loc[df.A > 15])

# 인덱스 값을 반환하는 함수를 사용할 수도 있음
# 예 : A열의 값이 12보다 큰 행들만 선택하는 경우
def select_row(df):
    return df.A > 12

# 함수 사용 인덱싱
print(select_row(df))
print(df.loc[select_row(df)])  # True 가 리턴된 행의 값들이 출력됨

# 인덱싱에 행과 열을 적용한 경우
print(df.loc['a', 'A'])  # 10 : 값 1개 추출
print(df.loc['a', :])   # print(df.loc['a'] 과 같음
print(df.loc[['a', 'b'], ['B', 'D']])

# boolean 값으로 인덱싱할 수도 있음
print(df.loc[df.A > 10, ['C', 'D']])

# iloc 인덱서
# 순서를 나타내는 정수 기반의 2차원 인덱싱에 사용함
print(df.iloc[0, 1])  # 0행1열의 값 : 11
print(df.iloc[:2, 2])  # 0행2열, 1행2열 인덱싱
print(df.iloc[0, -2:])  # 0행2열, 0행3열 인덱싱
print(df.iloc[2:3, 1:3])  #2행1열, 2행2열 인덱싱
print(df.iloc[-1])  # 2차원배열인데 인덱스가 하나이면 행을 선택함, -1 : 끝에서 첫번째 (마지막 행)

df.iloc[-1] = df.iloc[-1] * 2  # 인덱싱과 백터화연산 적용 가능
print(df)






