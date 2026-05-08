# path : app\\main.py

'''

기능 :
1. data/users.csv 파일에서 로그인 계정 정보를 읽어온다.
2. 사용자가 입력한 이메일과 비밀번호가 csv 의 값과 일치하면 로그인 성공
3. 로그인 실패시 팝업창에 오류 메시지 출력
4. 로그인 성공 후 csv 데이터 파일을 업로드하면 테이블과 통계 그래프를 출력한다.

라이브러리에 노란줄 뜰 때
해결 방법:
Ctrl+Shift+P → Python: Select Interpreter 입력
.venv 경로가 포함된 항목 선택:
python.exe

'''

from pathlib import Path # 운영체제의 안전한 파일 경로처리를 위한 표준 라이브러리

import pandas as pd                 # csv 읽기, 데이터 프레임 처리, 통계 계산 데이터 분석 라이브러리
import matplotlib.pyplot as plt     # 데이터 시각화 라이브러리
import streamlit as st              # 웹 화면 구성 애플리케이션 라이브러리

# 현재 파일 위치 : 프로젝트/app/main.py
BASE_DIR = Path(__file__).resolve().parents[1] # 프로젝트의 루트
# print('BASE_DIR                             : ', BASE_DIR) # 프로젝트의 루트 경로 출력
# print('__file__                             : ', __file__) # 현재 파일 경로 출력
# print('Path(__file__)                       : ', Path(__file__))
# print('Path(__file__).resolve()             : ', Path(__file__).resolve()) # 현재 파일의 절대 경로 출력
# print('Path(__file__).resolve().parents[0]  : ', Path(__file__).resolve().parents[0]) # 현재 파일의 부모 디렉토리 경로 출력
# print('Path(__file__).resolve().parents[1]  : ', Path(__file__).resolve().parents[1]) # 현재 파일의 조부모 디렉토리 경로 출력

# 사용자 계정 정보가 저장된 csv 파일 경로
USER_CSV_PATH = BASE_DIR / 'data' / 'users.csv'
# print('USER_CSV_PATH                       : ', USER_CSV_PATH) # 사용자 계정 정보가 저장된 csv 파일 경로 출력

# 1. 기본 페이지 설정
st.set_page_config(
    page_title  ='CSV 로그인 데이터 분석 앱',   # 웹 브라우저 탭에 표시되는 제목
    page_icon   ='🔐',                         # 웹 브라우저 탭에 표시되는 아이콘 (🔐 자물쇠 이모지)
    layout      = 'wide', # 'centered', 'wide'  # 웹 화면을 넓게 사용
)

# 2. 세션 상태 (로그인 상태 관리) 초기화 함수
def init_session_state()->None:                 # '->' 반환 자료형을 표시
    '''
    Streamlit 은 버튼 클릭이나 입력시 스크립트를 다시 실행함
    로그인 상태를 유지하려면 st.session_state 에 값을 저장해 두면 됨
    '''
    if 'logged_in'  not in st.session_state :
        st.session_state.logged_in = False          # 로그인 여부 저장 (현재 로그아웃 상태)

    if 'user_email' not in st.session_state :
        st.session_state.user_email = ''            # 로그인한 사용자의 이메일 저장

    if 'user_name'  not in st.session_state :
        st.session_state.user_name = ''             # 로그인한 사용자의 이름 저장
    
    if 'show_login_error' not in st.session_state :
        st.session_state.show_login_error = False   # 로그인 실패 팝업 표시 여부 저장
    
    return

#------------------------------------------------------

# 3. 사용자 csv 읽기 함수
# csv 파일은 매번 새로 읽을 필요가 없으므로 캐시 처리함
@st.cache_data # 캐시 데코레이터 : 함수의 결과를 저장하여 동일한 입력에 대해 빠르게 반환 (데이터 로딩 최적화)
def load_users() -> pd.DataFrame:
    '''
    data/users.csv 파일에서 로그인 계정 정보를 읽어오는 함수
    (csv 파일을 읽어서 pandas DataFrame 으로 반환)
    '''

    if not USER_CSV_PATH.exists():
        # 파일이 없으면 로그인 불가 -> 앱 실행을 중단 & 오류 출력
        st.error(f"사용자 csv 파일이 없습니다: {USER_CSV_PATH}") # 오류 메시지 출력
        st.stop() # 앱 실행 중단
    # if ---------------------------

    users_df = pd.read_csv(USER_CSV_PATH)               # csv 파일을 pandas DataFrame 으로 읽어오기

    # 필수 컬럼 존재 여부 확인 (이메일, 비밀번호 칼럼)
    required_columns = {'email', 'password', 'name'}    # 필수 컬럼 리스트
    if not required_columns.issubset(users_df.columns): # 컬럼 일치여부 확인 issubseet()
        st.error    ('users.csv 파일에는 emainl, password, name 컬럼이 모두 포함되어야 합니다.') # 오류 메시지 출력
        st.stop     () # 앱 실행 중단
    # if ---------------------------

    # 비교를 위해 문자열 타입으로 변환
    users_df['email'    ]    = users_df['email'      ].astype(str).str.strip()
    users_df['password' ]    = users_df['password'   ].astype(str).str.strip()
    users_df['name'     ]    = users_df['name'       ].astype(str).str.strip()

    return users_df

#------------------------------------------------------

# 4. 로그인 검증 함수
def check_login(email: str, password: str) -> tuple[bool, str]:
    '''
    입력한 이메일 / 비밀번호가 users.csv 에 있는지 확인
    반환값
    - (True, 사용자 이름) : 로그인 성공
    - (False, '')         : 로그인 실패
    '''
    users_df = load_users()

    # 입력값 앞뒤 공백 제거
    email       = email.strip()
    password    = password.strip()

    # email 과 password 가 모두 일치하는지 검사
    matched = users_df[(users_df['email'] == email) & (users_df['password'] == password)]

    if not matched.empty :
        # 일치하는 값이 있다면 사용자 이름 반환
        return True, matched.iloc[0]['name'] # 로그인 성공 인덱서
    # if ---------------------------

    return False, '' # 로그인 실패
#------------------------------------------------------

# 5. 로그인 실패 팝업창
@st.dialog('로그인 실패')
def login_error_dialog() -> None:
    '로그인 실패 메시지를 팝업창으로 출력'
    st.error('아이디나 암호가 일치하지 않습니다. 확인하고 다시 입력하세요.')

    # 닫기 버튼 클릭시 팝업 상태를 False 로 바꾸고 화면을 다시 실행함
    if st.button('닫기'):
        st.session_state.show_login_error = False
        st.rerun()
#------------------------------------------------------

# 6. 로그인 화면 구성
def show_login_page() -> None:
    '로그인 화면 출력'
    st.title('로그인 하세요.')
    st.write('이메일과 비밀번호를 입력 하세요.')

    # 로그인 폼 영역
    with st.form('login_form'):
        email       = st.text_input('이메일 : ', placeholder='example@example.com') # 이메일 입력 필드 # 회색으로 깔려있는 글자가 placeholder
        password    = st.text_input('비밀번호 : ', type='password', placeholder='비밀번호를 입력하세요') # 비밀번호 입력 필드 (입력값이 보이지 않도록 type='password' 설정)
        submitted   = st.form_submit_button('로그인') # 로그인 버튼

        # 로그인 버튼 클릭시 검증
        if submitted:
            success, user_name = check_login(email, password) 

            if success:
                # 로그인 성공시 세션 상태 업데이트
                st.session_state.logged_in          = True
                st.session_state.user_name          = user_name
                st.session_state.user_email         = email
                st.session_state.show_login_error   = False
                st.rerun()
            else:
                # 로그인 실패 팝업 표시
                st.session_state.show_login_error = True

        # 로그인 실패 상태이면 팝업 함수 호출
        if st.session_state.show_login_error:
            login_error_dialog()
        
        with st.expander('테스트 계정 보기'):
            st.code('admin@example.com/1234\nstudent@example.com/pass123\nteacher@example.com/teach123')
#------------------------------------------------------

# 7. 업로드 csv 데이터 파일 읽기 함수
def read_uploaded_csv(uploaded_file) -> pd.DataFrame:
    '사용자가 업로드한 csv 데이터 파일을 읽어서 pandas 의 DataFrame 으로 만들어서 리턴하는 함수'
    try:
        return pd.read_csv(uploaded_file) # 업로드된 파일을 pandas DataFrame 으로 읽어서 반환
    except UnicodeDecodeError:
        # 한글 Windows csv 가 cp949 로 저장된 경우에 대비함
        uploaded_file.seek(0) # 파일 포인터를 처음으로 되돌림
        return pd.read_csv(uploaded_file, encoding='cp949')
#------------------------------------------------------


# 8. 데이터 분석 화면 구성
def show_dashboard_page() -> None:
    '로그인 성공 후 표시되는 데이터 분석 페이지'
    st.title('로그인 성공 - CSV 데이터 분석 대시보드')

    # 상단에 사용자 정보와 로그아웃 버튼 표시
    col1, col2 = st.columns([4, 1]) # 4:1 비율로 두 개의 열 생성
    with col1:
        st.success(f'{st.session_state.user_name}님 로그인 성공 : {st.session_state.user_email}') 
    with col2:
        if st.button('로그아웃'):
            st.session_state.logged_in = False
            st.session_state.user_name = ''
            st.session_state.user_email = ''
            st.session_state.show_login_error = False
            # show_login_page() # 로그인 페이지로 돌아가기
            st.rerun()

    st.divider() # 구분선

    # 파일 업로드 위젯
    uploaded_file = st.file_uploader(
        '분석할 CSV 데이터 파일을 선택 하세요.',
        type=['csv'],
        help='예: data/sample_sales.csv 파일을 업로드해서 테스트 할 수 있습니다.',
    )

    if uploaded_file is None:
        st.info('CSV 파일을 업로드하면 테이블과 통계 그래프가 표시됩니다.')
        st.write('프로젝트에 포함된 예제 데이터 파일 : data/sample_sales.csv')
        return
    
    # 업로드한 파일 읽기
    df = read_uploaded_csv(uploaded_file)

    st.subheader('1. 읽어온 데이터 테이블')
    st.dataframe(df, use_container_width=True)
    
    st.subheader('2. 기본 데이터 정보')
    col1, col2, col3 = st.columns(3)
    col1.metric('행 갯수', len(df))
    col2.metric('열 갯수', len(df.columns))
    col3.metric('결측치 갯수', int(df.isna().sum().sum())) # 결측치 총 갯수 계산 # 결측치는 이상한 값

    st.subheader('3. 숫자 컬럼 통계 요약')
    numeric_df = df.select_dtypes(include='number')

    if numeric_df.empty:
        st.warning('숫자형 컬럼이 없어서 통계 그래프를 표시할 수 없습니다.')
        return

    # 숫자형 컬럼의 통계값 표시
    st.dataframe(numeric_df.describe(), use_container_width=True)

    st.subheader('4. 통계 그래프')

    # 그래프로 표시할 숫자 컬럼 선택
    selected_column = st.selectbox(
        '그래프로 표시할 숫자 컬럼을 선택하세요 :',
        numeric_df.columns,
    )

    # 그래프 종류 선택
    chart_type = st.radio(
        '그래프 종류를 선택하세요 :',
        ['선 그래프', '막대 그래프', '히스토그램'],
        horizontal=True,
    )

    if chart_type == '선 그래프':
       # 선택한 컬럼의 값을 선 그래프로 표시
       st.line_chart(numeric_df[selected_column])

    elif chart_type == '막대 그래프':
        # 선택 컬럼의 값을 막대 그래프로 출력
        st.bar_chart(numeric_df[selected_column])

    # elif chart_type == '히스토그램':
    else:
        # 히스토그램은 matplotlib 으로 그래서 출력
        fig, ax = plt.subplots() # plot 이 그래프로 그려라는 뜻
        ax.hist(numeric_df[selected_column].dropna(), bins=10) # dropna() 는 결측치 제거
        ax.set_title(f'{selected_column} Histogram')
        ax.set_xlabel(selected_column)
        ax.set_ylabel('Frequency')
        st.pyplot(fig)
#------------------------------------------------------



# 9. 메인 실행 흐름
def main() -> None:
    '앱의 시작 함수'
    init_session_state()

    # 로그인 여부에 따라 다른 화면 표시
    if st.session_state.logged_in:
        show_dashboard_page()
    else:
        show_login_page()
#------------------------------------------------------

# 이 파일을 직접 실행할 떄 
if __name__ == '__main__':
    main()

