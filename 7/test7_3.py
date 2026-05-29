import FinanceDataReader as fdr
import matplotlib.pyplot as plt
code = get_company_code('삼성전자')
df = fdr.DataReader(code, '2020-01-01', '2022-12-31’)
# df = fdr.DataReader('005930', '2024-01')
# 날짜와 종가 데이터 추출
dates = df.index
close_prices = df['Close']
# 그래프 그리기
plt.figure(figsize=(10, 5))
# plt.plot(dates, close_prices, label='Close Price', color='blue’)
plt.plot(dates, close_prices, # 라인 플롯 그리기
linestyle='-', # 라인 스타일
color='purple', # 라인 색상
linewidth=2, # 라인 두께
label='Sample Data', # 범례 레이블
alpha=0.8, # 투명도
)
# 그래프 제목과 레이블 추가
plt.title('Samsung Electronics Stock Close Price')
plt.xlabel('Date')
plt.ylabel('Close Price(KRW)')
plt.legend( )
# x축 레이블 회전
plt.xticks(rotation=45)
# 그래프 보여주기
plt.grid( )
plt.tight_layout( )
plt.show( )