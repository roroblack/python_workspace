import pandas as pd
import FinanceDataReader as fdr

def get_company_code(company_name):
df_krx = fdr.StockListing('KRX') # 한국 회사 목록 수집
company_info = df_krx[df_krx['Name'] == company_name]
if not company_info.empty: # company_name에 해당하는 회사가 있으면
return company_info['Code'].values[0]
else:
return None

import matplotlib.pyplot as plt
# 회사 이름 --> 회사 코드 --> 데이터 다운받기
naver_code = get_company_code('NAVER')
naver = fdr.DataReader(naver_code)
naver.dropna( )
# 회사 이름 --> 회사 코드 --> 데이터 다운받기
kakao_code = get_company_code('카카오')
kakao = fdr.DataReader(kakao_code)
kakao.dropna( )

# 종가 그리기(1)
close_list = naver['Close'].to_list( )
#date_list = naver.index.strftime('%Y-%m-%d').tolist( )
plt.plot(close_list, c='violet', label='Naver')
close_list = kakao['Close'].to_list( )
#date_list = naver.index.strftime('%Y-%m-%d').tolist( )
plt.plot(close_list, c='blue', label='Kakao’)
# 종가 그리기(2)
naver['Close'].plot(c='violet', label='Naver')
kakao['Close'].plot(c='blue', label='Kakao')
plt.legend( )
plt.show( )