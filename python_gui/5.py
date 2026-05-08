import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt 
st.set_page_config( 
    page_title  =   "AI 직업훈련 학습관리 GUI", 
    page_icon   =   "🤖", 
    layout      =   "wide" 
) 
st.title                                ("AI 직업훈련 학습관리 GUI") 
st.write                                ("Streamlit 을 활용한 웹 GUI 예제입니다.") 
st.sidebar.header                       ("학습자 정보 입력") 
student_name    = st.sidebar.text_input ("이름") 
course          = st.sidebar.selectbox  ("과정 선택", ["Python 기초", "웹 개발", "AI 개발", "데이터 분석"]) 
attendance      = st.sidebar.slider     ("출석률", 0, 100, 80) # 0 부터 100까지, 기본값은 80
 
st.header                               ("과목 점수 입력") 
col1, col2, col3 = st.columns           (3) 
 
with col1: 
    python_score = st.number_input      ("Python 점수", min_value=0, max_value=100, value=85) 
with col2: 
    sql_score    = st.number_input      ("SQL 점수",    min_value=0, max_value=100, value=80) 
with col3: 
    ai_score     = st.number_input      ("AI 점수",     min_value=0, max_value=100, value=90) 
 
if st.button                            ("학습 결과 분석"): 
    scores = { 
        "과목": ["Python", "SQL", "AI"], 
        "점수": [python_score, sql_score, ai_score] 
    } 
 
    df          = pd.DataFrame   (scores) 
    avg_score   = df["점수"].mean() 
 
    st.subheader            ("1. 학습자 정보") 
    st.write                    (f"이름: {student_name if student_name else '미입력'}") 
    st.write                    (f"과정: {course}") 
    st.write                    (f"출석률: {attendance}%") 
 
    st.subheader            ("2. 점수 데이터") 
    st.dataframe                (df, width='stretch') 
 
    st.subheader            ("3. 평균 점수") 
    st.write                    (f"평균 점수: {avg_score:.2f}")  # 소수점 2자리까지 표시
 
    st.subheader            ("4. 점수 그래프") 
    fig, ax = plt.subplots() 
    ax.bar                      (df["과목"], df["점수"], color=["#1f77b4", "#ff7f0e", "#2ca02c"]) 
    ax.set_xlabel               ("Subject") 
    ax.set_ylabel               ("Score") 
    ax.set_title                ("Subject-wise Scores") 
    st.pyplot                   (fig) 

    st.subheader            ("5. 학습 피드백") 
    if      avg_score >= 90: 
        st.success              ("매우 우수한 성과입니다. 심화 프로젝트를 진행해도 좋습니다.") 
    elif    avg_score >= 75: 
        st.info                 ("양호한 성과입니다. 실습을 조금 더 강화하면 좋습니다.") 
    else: 
        st.warning              ("기초 복습과 반복 실습이 필요합니다.") 
else:
    st.info                 ("왼쪽 입력과 점수 입력 후 '학습 결과 분석' 버튼을 눌러주세요.")

# session_state 값이 새로고침 되어도 유지됨