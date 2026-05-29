# path : ./test_matplotlib/matplotlib_test4.py
# 2026-05-26
# pandas DataFrame  과 시각화 연계 처리 테스트 스크립트

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from pathlib import Path



def test_csv_load(csv_path: str) -> pd.DataFrame :
    '''
    함수 실행시 읽을 csv 파일 경로를 전달 받아서, csv 파일을 읽어서 DataFrame 을 리턴하는 함수
    '''
    df = pd.read_csv(csv_path) # csv 파일 읽어서 DataFrame 으로 저장하기
    print(df) # DataFrame 내용 확인하기
    print(df.head()) # DataFrame 내용 확인하기
    print(df.info()) # DataFrame 내용 확인하기
    return df



def get_numeric_columns(df):
    '''
    DataFrame 에서 숫자형 데이터가 저장된 열의 이름을 리스트로 리턴하는 함수
    '''
    numeric_cols = df.select_dtypes(include='number').columns.tolist()  # 숫자형 데이터가 저장된 열의 이름을 리스트로 저장하기
    print('Numeric columns:', numeric_cols)                             # 숫자형 데이터가 저장된 열의 이름 확인하기
    return numeric_cols



def test_dataframe_hist_subplot(df):
    '수치형 컬럼 갯수 만큼 히스토그램 subplot 자동 생성하는 함수'
    numeric_cols    = get_numeric_columns(df)   # 숫자형 데이터가 저장된 열의 이름을 리스트로 저장하기
    num_cols        = len(numeric_cols)         # 5개 - 숫자형 데이터가 저장된 열의 개수 확인하기

    # 서브플롯 생성하기 (num_cols 개의 열에 대해 1행 num_cols열 형태로 생성)
    fig, axes = plt.subplots(num_cols, 1, figsize=(6, 4 * num_cols)) # 서브플롯 생성하기 (1행 num_cols열 형태로 생성)

    if num_cols == 1:
        axes = [axes] # 서브플롯이 하나인 경우에도 리스트 형태로 만들어주기

    for ax, col in zip(axes, numeric_cols):
        ax.hist(df[col], bins=10) # 각 열에 대한 히스토그램 그리기
        ax.set_title(f'Histogram of {col}', pad=20) # 각 서브플롯에 제목 설정하기
        ax.set_xlabel(col) # x축 레이블 설정하기
        ax.set_ylabel('Count') # y축 레이블 설정하기

    fig.subplots_adjust(hspace=0.3) # 서브플롯 간 수직 간격 조정
    fig.tight_layout(pad=5.0) # 레이아웃 조정하기
    # plt.legend() # 범례 표시하기
    plt.show() # 그래프를 화면에 표시하는 함수 (반드시 호출해야 그래프가 보임)

def test_dataframe_boxplot_subplot(df):
    '수치형 컬럼 갯수 만큼 박스플롯 subplot 자동 생성하는 함수'
    numeric_cols    = get_numeric_columns(df)   # 숫자형 데이터가 저장된 열의 이름을 리스트로 저장하기
    num_cols        = len(numeric_cols)         # 5개 - 숫자형 데이터가 저장된 열의 개수 확인하기

    # 서브플롯 생성하기 (num_cols 개의 열에 대해 1행 num_cols열 형태로 생성)
    fig, axes = plt.subplots(1, num_cols, figsize=(5 * num_cols, 4)) # 서브플롯 생성하기 (1행 num_cols열 형태로 생성)

    if num_cols == 1:
        axes = [axes] # 서브플롯이 하나인 경우에도 리스트 형태로 만들어주기

    for ax, col in zip(axes, numeric_cols):
        ax.boxplot(df[col]) # 각 열에 대한 박스플롯 그리기
        ax.set_title(f'Boxplot of {col}', pad=20) # 각 서브플롯에 제목 설정하기
        # ax.set_xlabel(col) # x축 레이블 설정하기
        ax.set_ylabel(col) # y축 레이블 설정하기

    fig.subplots_adjust(hspace=0.5) # 서브플롯 간 수직 간격 조정
    fig.tight_layout(pad=5.0) # 레이아웃 조정하기
    # plt.legend() # 범례 표시하기
    plt.show() # 그래프를 화면에 표시하는 함수 (반드시 호출해야 그래프가 보임)

def test_dataframe_groupby_subplot(df, category_col):    
    '범주형 컬럼을 기준 숫자데이터 컬럼 평균에 대한 bar plot 생성 함수'
    numeric_cols = get_numeric_columns(df)
    grouped = df.groupby(category_col)[numeric_cols].mean() # 범주형 컬럼을 기준으로 숫자데이터 컬럼의 평균 계산하기

    grouped.plot(kind='bar', figsize=(8, 4), title=f'Average by {category_col}') # 그룹화된 데이터에 대한 막대 그래프 그리기
    plt.ylabel('Mean Value') # y축 레이블 설정하기
    plt.show() # 그래프를 화면에 표시하는 함수 (반드시 호출해야 그래프가 보임)





print("-----------------------------0")
if __name__ == "__main__":
    # 현재 py 파일 기준 경로 생성
    BASE_DIR = Path(__file__).resolve().parent.parent
    # csv_path = './data/sample.csv'
    csv_path = BASE_DIR / 'data' / 'sample.csv' # csv 파일 경로 생성하기
    print(Path(__file__).resolve()) # 현재 py 파일의 절대 경로 확인하기
    print(BASE_DIR) # 현재 py 파일 기준 경로 확인하기
    print(csv_path) # csv 파일 경로 확인하기
    # C:\Users\playdata2\Documents\python_workspace\test_visualization\test_matplotlib\matplotlib_test4.py
    # C:\Users\playdata2\Documents\python_workspace\test_visualization
    # C:\Users\playdata2\Documents\python_workspace\test_visualization\data\sample.csv
    print("-----------------------------1")

    df = test_csv_load(csv_path)
    print(df)
    print(type(df))
    print("-----------------------------2")

    get_numeric_columns(df)
    print("-----------------------------3")

    # test_dataframe_hist_subplot(df)
    print("-----------------------------4")

    # test_dataframe_boxplot_subplot(df)
    print("-----------------------------5")

    # 범주형 (categorical) 컬럼이 있는 경우만 실행함
    test_dataframe_groupby_subplot(df, 'age_category') #df.category_col)
    print("-----------------------------6")
