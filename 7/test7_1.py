# 주가 데이터 라이브러리 설치 및 회사별 종목 코드 추출
# pip install finance-datareader
import pandas as pd
import FinanceDataReader as fdr

def get_company_code(company_name):
df_krx = fdr.StockListing('KRX') # 한국 회사 목록 수집
company_info = df_krx[df_krx['Name'] == company_name]
if not company_info.empty: # company_name에 해당하는 회사가 있으면
return company_info['Code'].values[0]
else:
return None

# 사용법
company_name = "NAVER"

# company_name = "빙그레"
company_code = get_company_code(company_name)
print(f"{company_name}의 종목 코드는 {company_code}입니다.")