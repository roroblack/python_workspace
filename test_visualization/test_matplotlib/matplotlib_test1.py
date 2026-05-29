# path : matplotlib_test1.py
# 2026-05-26

# matplotlib 모듈 사용한 시각화 테스트 스크립트

# 패키지 추가 설치 : pip install matplotlib

import matplotlib as mpl
import matplotlib.pyplot as plt



def test_plot1():
    '간단한 plot 그리기 : 기본은 선 그래프 (line plot)'

    # 그래프를 표현할 데이터는 리스트 또는 배열이어야 함
    sample_data = [1, 4, 9, 16]

    plt.title("Line Plot") # 그래프 제목 지정 함수 (그래프 위에 표시됨)
    plt.plot(sample_data) # 선 그래프 만드는 함수 (y축값만 지정함) => x축은 자동으로 0, 1, 2, 3으로 지정됨
                                                                    # 리스트가 하나면 y축값으로 인식됨
    plt.show() # 그래프를 화면에 표시하는 함수 (반드시 호출해야 그래프가 보임)

def test_plot2():
    # title('표시할 그래프 제목')
    # x축 값도 함께 지정 : plot([x축값들],[y축값들])
    y_data = [1, 4, 9, 16]
    x_data = [10, 20, 30, 40]

    plt.title("x ticks") # 그래프 제목 지정 함수 (그래프 위에 표시됨)
    plt.plot(x_data, y_data) # 선 그래프 만드는 함수 (x축값과 y축값을 함께 지정함)
    plt.show() # 그래프를 화면에 표시하는 함수 (반드시 호출해야 그래프가 보임)

# 그래프에 한글을 사용하려면, 한글 폰트 파일을 다운받아서 사용함----------------------
import matplotlib.font_manager as fm

def test_fonts():
    # 라이브러리 자원 (설치한 패키지) 저장 폴더 경로 확인하기
    print(mpl.matplotlib_fname()) # matplotlib 라이브러리 자원 폴더 경로 확인하기
    # c:\Users\playdata2\Documents\python_workspace\test_visualization\.venv\Lib\site-packages\matplotlib\mpl-data\matplotlibrc

    # matplotlib 에서 다운받은 글꼴을 그래프(plot) 의 기본 글꼴로 사용하게 하려면
    # C:\Users\playdata2\Documents\python_workspace\test_visualization\.venv\Lib\site-packages\matplotlib\mpl-data\fonts\ttf
    # ttf 폴더 안에 다운받은 한글 폰트 파일을 복사해 넣어야 함

    # 글꼴 파일들 복사해 넣고 나서, matplotlib 캐시에 변경 내용을 반영해야 함
    # 1. 캐시 폴더 경로 확인하기
    print(mpl.get_cachedir()) # matplotlib 캐시 폴더 경로 확인하기
    # C:\Users\playdata2\.matplotlib
    # 2. 해당 위치의 캐시 파일을 직접 파일 탐색기에서 찾아내서 .matplotlib 폴더 삭제함 => 이전 폰트 정보를 기억하고 있기 때문에
        # 캐시 폴더를 삭제한 후, matplotlib 라이브러리를 다시 실행하면, 캐시 폴더가 새로 만들어지고, 새로 복사한 글꼴 파일이 반영됨 (없으면 컴퓨터 리부트)

def test_fonts2():
    # 폰트설정
    # 첫번쨰 방법 : rc.parameters 를 설정해서, 설정 이후에 그래프 작업 전체에 사용하게 함

    # 현재 사용되고 있는 폰트 종류와 글자 크기 확인
    print(mpl.rcParams['font.family'])
    print(mpl.rcParams['font.size'])

    # 한글 폰트로 설정
    mpl.rc('font', family='NanumGothicCoding')
    mpl.rc('axes', unicode_minus=False) # 마이너스 기호가 깨지는 문제 해결
    # axes 에 적용되는 유니코드 (0~65535) 숫자에 음수 부호 사용 해제를 지정함 (사용 못하게 함)

    # 그래프에 한글 사용 확인
    y_data = [1, 4, 9, 16]
    x_data = [10, 20, 30, 40]

    plt.title("한글 그래프 제목") # 그래프 제목 지정 함수 (그래프 위에 표시됨)
    plt.plot(x_data, y_data) # 선 그래프 만드는 함수 (x축값과 y축값을 함께 지정함)
    plt.xlabel("x축 이름") # x축 이름 지정 함수
    plt.ylabel("y축 이름") # y축 이름 지정 함수
    plt.show() # 그래프를 화면에 표시하는 함수 (반드시 호출해야 그래프가 보임)



def test_fonts3():
    # 그래프의 특정 부분만 원하는 글꼴로 설정 변경
    # 이용할 글꼴 파일의 위치는 어디든 상관 없음
    font_path = './fonts/NanumGothicCoding-Bold.ttf' # 사용할 글꼴 파일의 경로 지정
    font_prop = fm.FontProperties(fname=font_path) # 글꼴 파일 경로를 이용해서 글꼴 속성 객체 생성

    # 그래프에 한글 사용 확인
    y_data = [1, 4, 9, 16]
    x_data = [10, 20, 30, 40]

    plt.title("한글 그래프 제목", fontproperties=font_prop) # 그래프 제목 지정 함수 (그래프 위에 표시됨)
    plt.plot(x_data, y_data)
    plt.xlabel("x축 이름", fontproperties=font_prop)
    plt.ylabel("y축 이름", fontproperties=font_prop)
    plt.show()



def test_fonts4():
    # 각 객체마다 별도의 폰트 적용 : fontdict 인수에 넣어서 사용
    font1 = {'family': 'NanumGothicCoding',         'size': 24, 'color': 'blue',    'weight': 'bold'} # 제목에 적용할 폰트 설정
    font2 = {'family': 'NanumGothicCoding',         'size': 16, 'color': 'red',     'weight': 'bold'} # x축, y축 이름에 적용할 폰트 설정
    font3 = {'family': 'NanumGothicCoding',         'size': 12, 'color': 'green',   'weight': 'light'} # x축, y축 이름에 적용할 폰트 설정

    # 그래프에 한글 사용 확인
    y_data = [1, 4, 9, 16]
    x_data = [10, 20, 30, 40]

    plt.title("한글 그래프 제목", fontdict=font1)
    plt.plot(x_data, y_data)
    plt.xlabel("x축 이름", fontdict=font2)
    plt.ylabel("y축 이름", fontdict=font3)
    plt.show()



#--------------------------------------------------------------------------main

if __name__ == "__main__":

    # test_plot1()
    # test_plot2()
    # test_fonts()
    # test_fonts2()
    # test_fonts3()
    test_fonts4()

