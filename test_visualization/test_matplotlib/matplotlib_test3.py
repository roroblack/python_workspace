# path : matplotlib_test3.py
# 2026-05-26
# matplotlib pyplot 의 그래프별 속성 / 인수 사용 테스트

import os
import math
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 공통 유틸 함수 : 한글 폰트 설정 (시스템에 설치 | 로컬 폰트파일 설정 모두 가능)
#       기본값 지정된 매개변수 있는 함수로 작성함
# 함수 사용시 : 
#       값이 전달오면 매개변수가 받아서 사용함
#       값 전달이 없으면 지정된 기본값 사용함
def setup_korean_font(prefer_family: str = 'NanumGothicCoding',
                      local_font_path: str = './fonts/NanumGothicCoding.ttf',
                      local_bold_path: str = './fonts/NanumGothicCoding-Bold.ttf') -> None :
    '''
    목적 : 
    - 그래프 제목 / 축 라벨 등에 한글이 꺠지지 않게 폰트 설정
    - 시스템에 'NanumGothicCoding' 폰트가 설치되어 있으면, ./fonts 폴더의 ttf 파일을 직접 지정해서 해결
    - mpl.rc('font', family='NanumGothicCoding') : matplotlib 기본 폰트 지정
    - mpl.rc('axes', unicode_minus=False) : 마이너스 기호가 깨지는 문제 해결 (방지 처리)
    '''

    # 한글 폰트로 설정
    mpl.rc('axes', unicode_minus=False) # 마이너스 기호가 깨지는 문제 해결

    # 1) 시스템 폰트로 설정 시도
    mpl.rc('font', family=prefer_family)

    # 2) 실제로 해당 글꼴(font family) 이 있는지 검사 (없으면 로컬 폰트로 강제 적용)
    available = set(f.name for f in fm.fontManager.ttflist)
    if (prefer_family not in available) : # mpl 폰트 목록에 전달받은 글꼴이 없으면
        # 로컬 폰트 파일이 존재하면, 그 글꼴로 지정 처리함
        if os.path.exists(local_font_path) :
            font_prop = fm.FontProperties(fname=local_font_path)
            mpl.rcParams['font.family'] = font_prop.get_name()
        
        elif os.path.exists(local_bold_path) :
            bold_prop = fm.FontProperties(fname=local_bold_path)
            mpl.rcParams['font.family'] = bold_prop.get_name()

        else :
            print(f"'{prefer_family}' 폰트가 시스템에 설치되어 있지 않습니다. 로컬 폰트 파일을 사용합니다.")
            # 로컬 폰트 파일로 강제 적용
            # font_prop = fm.FontProperties(fname=local_font_path)
            # bold_prop = fm.FontProperties(fname=local_bold_path)
            # mpl.rc('font', family=font_prop.get_name())
            # mpl.rc('axes', unicode_minus=False) # 마이너스 기호가 깨지는 문제 해결
        
def test_line_detail():
    '''
    plt.plot() 을 다양한 인수로 변형하는 실습
    [핵심 인수]
    - x, y          :   x축, y축 데이터                             (리스트, 배열, 판다스 Series 등)
    - marker        :   각 데이터 포인트에 찍히는 점의 모양 지정    ('o', 's', '^', 'D', 'x', '+', '*', 등)
    - color         :   선 색상 지정                                (색상 이름, HEX 코드, RGB 튜플 등)
    - linestyle     :   선 스타일(종류)                             ('-', '--', '-.', ':', 'None', ' ', '')
    - linewidth     :   선의 굵기                                   (숫자, 기본값은 1.0)
    - alpha         :   투명도                                      (0.0 (투명) ~ 1.0 (불투명))
    - label         :   범례(legend)에 표시할 이름 지정             (범례 표시하려면 plt.legend() 도 함께 호출해야 함)
    '''

    setup_korean_font() # 한글 폰트 설정

    x = [1, 2, 3, 4]
    y1 = [2, 3, 5, 7]
    y2 = [2, 5, 10, 17]

    plt.figure(figsize=(8, 4)) # figure(창) 그래프 크기 설정 (가로, 세로 인치 단위)

    plt.plot(x, y1, 
                marker='o',             # 점 모양 : 원
                linestyle='-',          # 선 스타일 : 실선
                linewidth=2,            # 선 굵기 : 2
                alpha=0.8,              # 투명도 : 0.8 (80% 불투명)
                color='blue',           # 선 색상 : 파란색
                label='소수 수열')      # 범례에 표시할 이름 : '소수 수열'
    plt.plot(x, y2,
                marker='s',                 # 점 모양 : 사각형
                linestyle='--',             # 선 스타일 : 점선
                linewidth=2,                # 선 굵기 : 2
                alpha=0.6,                  # 투명도 : 0.6 (60% 불투명)
                color='red',                # 선 색상 : 빨간색
                label='비교 수열')          # 범례에 표시할 이름 : '비교 수열'
    
    plt.title("선 그래프 : 마커/선스타일/투명도/범례") # 그래프 제목 지정 함수 (그래프 위에 표시됨)
    plt.xlabel("x축") # x축 이름 지정 함수
    plt.ylabel("y축") # y축 이름 지정 함수
    plt.grid(True, linestyle=':', color='gray', alpha=0.4) # 격자선 표시 (선 스타일, 색상, 투명도 지정)
    plt.legend()  # 범례 표시

    plt.show()    # 그래프 출력

# 2) 선 그래프 : 특정 점만 값 표시 (annotate / text)
def test_line_annotate_specific_points():
    '''
    특정 값만 선 위에 값 표시하는 실습 (예: 최대값, 임계치 초과 지정)
    [핵심함수 / 인수]
    - plt.annotate(text, xy=(x, y), xytext=(dx, dy), textcoords='offset points', arrowprops=None...) : 특정 점에 화살표와 함께 텍스트로 값 표시
        - text          : 표시할 텍스트 내용 (문자열)
        - xy            : 화살표가 가리키는 점의 좌표 (x, y)
        - xytext        : 텍스트 위치 좌표 (x, y)
        - textcoords    : 텍스트 좌표 시스템 ('offset points', 'data', 'axes fraction' 등)
        - arrowprops    : 화살표 스타일 지정 (dict 형태로 선 스타일, 색상 등 설정)
    - plt.text(x, y, text, fontsize=12, color='black', ha='center', va='bottom') : 특정 위치에 텍스트로 값 표시 (화살표 없이)
    '''

    setup_korean_font() # 한글 폰트 설정

    x = list(range(1, 11))
    y = [v * v - 3 * v + 5 for v in x] # y = x^2 - 3x + 5

    plt.figure(figsize=(8, 4))
    plt.plot(x, y, marker='D', linestyle='-', label='y = x^2 - 3x + 5')

    plt.title("선 그래프 : 특정 값만 라벨링(annotate)")
    plt.xlabel("X")
    plt.ylabel("Y")


    # 최대값에 화살표와 함께 텍스트 표시
    # max_index = y.index(max(y))
    max_index = max(range(len(y)), key=lambda i: y[i])
    # range(len(y)) : 0 ~ 9 까지의 인덱스 생성
    max_x, max_y = x[max_index], y[max_index]


    plt.annotate(
        f"최대값: {max_y:.2f}", 
        xy=(max_x, max_y),                              # 화살표가 가리키는 점의 좌표
        xytext=(0, 20),                                 # 텍스트를 데이터 점에서 (10, 20) 떨어진 위치로 이동
        textcoords='offset points',                     # xytext 단위를 포인트로 해석
        arrowprops=dict(arrowstyle='->', linewidth=1.5, color='red')   # 화살표 모양, 굵기
        )
    
    # 예 : 임계치 (y >= 50) 인 지점만 텍스트로 표시
    for xi, yi in zip(x, y):
        if yi >= 50:
            plt.text(xi, yi, str(yi)) # (x, y) 에 문자열 표시 (50 초과시)

    plt.grid(True, linestyle=':', color='gray', alpha=0.4)

    plt.legend()
    plt.show()    # 그래프 출력

# 3) 막대 그래프 : 막대별 색 다르게 지정. edgecolor + hatch 
def test_bar_colors_each_hatch() :
    '''
    bar 그래프에서 막대별 색상, edgecolor, hatch 패턴을 다르게 지정하는 실습
    [핵심함수 / 인수]
    - plt.bar(x, height, color='blue', edgecolor='black', linewidth=1.5, hatch='/', label='라벨') : 막대 그래프 생성
        - x          : 막대 위치            (카테고리 라벨 리스트도 가능)
        - height     : 막대의 높이          (숫자 리스트)
        - color      : 막대 색상            (색상 이름, HEX 코드, RGB 튜플 등)
        - edgecolor  : 막대 테두리 색상     (단일 문자열 또는 색상 리스트로 막대별 생상 지정)
        - linewidth  : 막대 테두리 굵기     (숫자, 기본값은 1.0)
        - hatch      : 막대 패턴            ('/', '\', '|', '-', '+', 'x', 'o', 'O', '.', '*')
        - label      : 범례에 표시할 이름
    '''

    setup_korean_font() # 한글 폰트 설정

    categories = ['A', 'B', 'C', 'D', 'E']
    values = [10, 15, 7, 12, 6]
    colors = ['red', 'orange', 'green', 'blue', 'purple']
    hatches  = ['/', '\\', '|', '-', '+']

    plt.figure(figsize=(8, 4))
    bars = plt.bar(categories, values, 
                   color=colors, 
                   edgecolor='black', 
                   linewidth=1.2, 
                   hatch=hatches[0], 
                   label='데이터') # 막대 그래프 생성
    
    # 막대별 hatch 지정
    for bar, hatch in zip(bars, hatches):
        bar.set_hatch(hatch)

    plt.title("막대 그래프 : 막대별 색상/패턴 지정")
    plt.xlabel("카테고리")
    plt.ylabel("값")

    plt.grid(True, linestyle=':', color='gray', alpha=0.4) # y축만 표시

    plt.legend()
    plt.show()    # 그래프 

# 4) 막대그래프 : 값 라벨(막대 위 숫자표시) 정렬 / 축범위
def test_bar_value_labels_ylim() :
    '''
    막대 위에 값을 표시 (레포트/대시 보드에서 아주 많이 사용)
    - plt.text(x, y, ha='center', va='bottom')
        - ha (horizontal alignment) : 텍스트의 수평 정렬 방식 ('center', 'left', 'right')
        - va (vertical alignment)   : 텍스트의 수직 정렬 방식 ('top', 'center', 'bottom')
    - plt.ylim(min, max) : y축 범위 설정 (라벨이 잘리지 않게 하기 위함)
    '''

    setup_korean_font() # 한글 폰트 설정

    x = ['1분기', '2분기', '3분기', '4분기']
    y = [120, 80, 150, 130]

    plt.figure(figsize=(8, 4))
    bars = plt.bar(x, y, color='skyblue', edgecolor='black', linewidth=1.2, label='매출')

    # 값 라벨 표시
    for bar in bars:
        h = bar.get_height() # 막대의 높이 (값)
        cx = bar.get_x() + bar.get_width() / 2 # 막대의 중앙 x 좌표
        plt.text(cx, h, f'{h}', ha='center', va='bottom') # 막대 위에 값 표시 (중앙 정렬, 아래쪽 정렬)

    plt.title("막대 그래프 : 값 라벨 + y축 범위 설정")
    plt.xlabel("분기")
    plt.ylabel("매출")

    # 라벨이 잘리지 않게 y축 범위에 여유를 줌
    plt.ylim(0, max(y) * 1.2) # y축 범위 설정 (라벨이 잘리지 않게 하기 위함)
    plt.grid(axis='y', linestyle=':', alpha=0.4)
    plt.legend()
    plt.show()    # 그래프 출력

# 5) 파이 차트 : explode
def test_pie_explode_autopct() :
    '''
    pie 그래프 변형 실습 (한 조각 떨어뜨리고 퍼센트 표시)
    [핵심 함수 / 인수]
    - plt.pie(x, labels=labels, autopct='%1.1f%%', explode=explode) : 파이 차트 생성
        - x             : 각 조각의 크기                                        (숫자 리스트)
        - labels        : 각 조각의 라벨                                        (문자열 리스트)
        - autopct       : 각 조각에 퍼센트 표시 형식                            (예: '%1.1f%%'는 소수점 1자리까지 퍼센트 표시)
        - startangle    : 파이 차트의 시작 각도                                 (기본값은 0, 시계 방향으로 증가)
                                                                                (예: 90으로 설정하면, 12시 방향부터 시작)
        - explode       : 각 조각을 원에서 얼마나 떨어뜨릴지 지정하는 리스트    (숫자 리스트, 0은 원과 붙어있음, 0.1은 10% 만큼 떨어짐)
                                                                                (예: [0, 0.1, 0, 0] : 두 번쨰 조각만 튀어나옴)
    '''
    setup_korean_font() # 한글 폰트 설정

    labels  = ['국어', '영어', '수학', '과학']
    sizes   = [25, 30, 20, 25]

    explode = [0, 0.12, 0, 0]  # 두 번째 조각만 튀어나옴

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, explode=explode, shadow=True) # 파이 차트 생성 (startangle로 시작 각도 조정, explode로 조각 튀어나오게 설정, shadow로 그림자 효과)
    plt.title("파이 차트 : explode + autopct + shadow")
    plt.show()

# 6) 파이 차트 : 도넛 스타일로 변형
def test_pie_donut_style() :
    '''
    pie 를 도넛 형태로 변형하는 실습
    [핵심 인수]
    - wedgeprops=dict(width=0.4) : width 를 주면 가운데가 뚫린 도넛 형태가 됨
    '''

    setup_korean_font() # 한글 폰트 설정

    labels  = ['국어', '영어', '수학', '과학']
    sizes   = [25, 30, 20, 25]
    
    plt.figure(figsize=(6, 6))
    wedges, texts, autotexts = plt.pie(sizes, labels=labels, autopct='%1.0f%%', startangle=90, wedgeprops=dict(width=0.6), shadow=True)
                                     # wedgeprops로 조각의 너비 조정 (width=0.6는 원의 60% 너비로 조각 생성)
    plt.title("파이 차트 : 도넛 스타일")
    plt.show()

# 7) 산점도 : 점 크기 / 투명도 / 모양 + 기준선
def test_scatter_size_alpha_marker() :
    '''
    산점도에서 점의 크기, 투명도, 모양을 다양하게 지정하는 실습
    [핵심 함수 / 인수]
    - plt.scatter(x, y, s=100, alpha=0.5, marker='o', color='blue', edgecolor='black') : 산점도 생성
        - x          : x축 데이터 (숫자 리스트)
        - y          : y축 데이터 (숫자 리스트)
        - s          : 점의 크기 (숫자 또는 숫자 리스트)
        - alpha      : 점의 투명도 (0.0 ~ 1.0)
        - marker     : 점의 모양 ('o', 's', '^', 'D', 'x', '+', '*', 등)
        - color      : 점의 색상 (색상 이름, HEX 코드, RGB 튜플 등)
        - edgecolor  : 점 테두리 색상 (색상 이름, HEX 코드, RGB 튜플 등)
    '''

    setup_korean_font() # 한글 폰트 설정

    x = [1, 2, 3, 4, 5, 6]
    y = [2,1, 5, 7, 11, 13]
    sizes = [30, 60, 80, 130, 400, 500] # 점 크기 리스트

    plt.figure(figsize=(8, 4))
    plt.scatter(x, y, s=sizes, alpha=0.6, marker='^', color='skyblue', edgecolor='black') # 산점도 생성
    plt.title("산점도 : 점 크기/투명도/모양 지정")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True, linestyle=':', color='gray', alpha=0.4)
    plt.show()


#--------------------------------------------------------------------------main
if __name__ == "__main__":
    # 선 그래프
    # test_line_detail()
    # test_line_annotate_specific_points()

    # 막대 그래프
    # test_bar_colors_each_hatch()
    # test_bar_value_labels_ylim()

    # 파이 차트
    # test_pie_explode_autopct()
    # test_pie_donut_style()

    # 산점도
    test_scatter_size_alpha_marker()
