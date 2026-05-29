# path : ./test_matplotlib/matplotlib_test2.py
# 2026-05-26
# 여러 종류의 그래프 확인 스크립트

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

def test_multiline_plot():
    '여러 개의 선 그리는 그래프 테스트'
    # 한글 폰트로 설정
    mpl.rc('font', family='NanumGothicCoding')
    mpl.rc('axes', unicode_minus=False) # 마이너스 기호가 깨지는 문제 해결

    x_data = [1, 2, 3, 4]
    y_data1 = [1, 4, 9, 16]
    y_data2 = [2, 5, 10, 17]

    plt.title("Multiline Plot") # 그래프 제목 지정 함수 (그래프 위에 표시됨)
    plt.plot(x_data, y_data1, label='SAMSUNG 전자')
    plt.plot(x_data, y_data2, label='SK_HYNIX')
    plt.legend() # 범례 표시
    plt.show() # 그래프를 화면에 표시하는 함수 (반드시 호출해야 그래프가 보임)

def test_scatter_plot():
    '산점도 (Scatter Plot) : 점 그래프 그리기'
    x = np.random.rand(50) # 0~1 사이의 난수 50개 생성
    y = np.random.rand(50) # 0~1 사이의 난수 50개 생성

    plt.title("Scatter Plot") # 그래프 제목 지정 함수 (그래프 위에 표시됨)
    plt.scatter(x, y) # 산점도 그리기
    plt.show() # 그래프를 화면에 표시하는 함수 (반드시 호출해야 그래프가 보임)

def test_bar_plot():
    '막대 그래프 그리기'
    x = ['A', 'B', 'C', 'D']
    y = [10, 25, 15, 30]

    plt.title("Bar Plot") # 그래프 제목 지정 함수 (그래프 위에 표시됨)
    plt.bar(x, y) # 막대 그래프 그리기
    plt.show() # 그래프를 화면에 표시하는 함수 (반드시 호출해야 그래프가 보임)

def test_barh_plot():
    '수평 막대 그래프 그리기'
    names = ['Python', 'Java', 'C', 'JavaScript']
    scores = [90, 85, 70, 88]
    
    plt.title("Horizontal Bar Plot") # 그래프 제목 지정 함수 (그래프 위에 표시됨)
    plt.barh(names, scores) # 수평 막대 그래프 그리기
    plt.show() # 그래프를 화면에 표시하는 함수 (반드시 호출해야 그래프가 보임)

def test_histogram():
    '히스토그램 그리기 : 분포 확인 그래프'
    data = np.random.randn(1000) # 평균이 0이고 표준편차가 1인 정규분포에서 난수 1000개 생성

    plt.title("Histogram") # 그래프 제목 지정 함수 (그래프 위에 표시됨)
    plt.hist(data, bins=20) # 히스토그램 그리기 (bins는 막대의 개수)
    plt.show() # 그래프를 화면에 표시하는 함수 (반드시 호출해야 그래프가 보임)

def test_pie_chart():
    '파이 차트 그리기'
    labels = ['Apple', 'Banana', 'Cherry', 'Grapes']
    sizes = [40, 30, 20, 10]

    plt.title("Pie Chart") # 그래프 제목 지정 함수 (그래프 위에 표시됨)
    plt.pie(sizes, labels=labels, autopct='%1.1f%%') # 파이 차트 그리기 (autopct는 퍼센트 표시 형식)
    plt.axis('equal') # 원형으로 표시하기 위해 축의 비율을 같게 설정
    plt.show() # 그래프를 화면에 표시하는 함수 (반드시 호출해야 그래프가 보임)

def test_subplot_basic():
    '서브플롯 그리기 : 여러 개의 그래프를 한 화면에 배치하기'
    # 1행 2열 형태로 그려보기
    x = [1, 2, 3, 4]
    y = [1, 4, 9, 16]

    # x = np.linspace(0, 10, 100) # 0부터 10까지 100개의 균등한 숫자 생성

    # plt.figure(figsize=(10, 6)) # 전체 그래프의 크기 설정

    # 첫 번째 서브플롯 (1행 2열 중 첫 번째)
    plt.subplot(1, 2, 1) # (행, 열, 위치)
    plt.title("Line")
    plt.plot(x, y)

    # 두 번째 서브플롯 (1행 2열 중 두 번째)
    plt.subplot(1, 2, 2) # (행, 열, 위치)
    plt.title("Bar")
    plt.bar(x, y)

    plt.tight_layout() # 서브플롯 간의 간격 조정
    plt.show() # 그래프를 화면에 표시하는 함수 (반드시 호출해야 그래프가 보임)

def test_subplots_object():
    '서브플롯 그리기 : plt.subplots() 함수를 사용해서 여러 개의 그래프를 한 화면에 배치하기'
  
    x_data = [1, 2, 3, 4]
    y_data1 = [1, 4, 9, 16]
    y_data2 = [2, 5, 10, 17]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4)) # (행, 열, 전체 그래프 크기)
    # fig   : 그래프 그려지는 윈도우 (창)        --> 1개
    # axes  : 창 안에 실제 그래프 그려지는 영역  --> 2개 (리스트 형태)

    # 첫 번째 서브플롯
    axes[0].plot(x_data, y_data1)
    axes[0].set_title("Line Plot")

    # 두 번째 서브플롯
    axes[1].bar(x_data, y_data2)
    axes[1].set_title("Bar Plot")

    plt.tight_layout() # 서브플롯 간의 간격 조정 # 배율적용
    plt.show() # 그래프를 화면에 표시하는 함수 (반드시 호출해야 그래프가 보임)

def test_subplot_2by2():
    '2x2 복합 시각화 (보고서용)'
    data = np.random.randn(100)

    fig, axes = plt.subplots(2, 2, figsize=(8, 6))
    # axes : 2행 2열이 리턴됨 -> 그래프 구역에 대한 인덱싱 : axes[0,0] == axes[0][0] (왼쪽 위)

    axes[0, 0].plot([1, 2, 3], [1, 4, 9])
    axes[0, 0].set_title('Line')

    axes[0, 1].bar(['A', 'B', 'C'], [1, 4, 9])
    axes[0, 1].set_title('Bar')

    axes[1, 0].scatter(np.random.rand(30), np.random.rand(30))
    axes[1, 0].set_title('Scatter')

    axes[1, 1].hist(data, bins=15)
    axes[1, 1].set_title('Histogram')

    plt.tight_layout() # 서브플롯 간의 간격 조정
    plt.show() # 그래프를 화면에 표시하는 함수 (반드시 호출해야 그래
    


#------------------------------------------------------------------------------main
if __name__ == "__main__":

    # test_multiline_plot()
    # test_scatter_plot()
    # test_bar_plot()
    # test_barh_plot()
    # test_histogram()
    # test_pie_chart()
    # test_subplot_basic()
    # test_subplots_object()
    test_subplot_2by2()