import streamlit as st 

st.title    ("제목") 
st.header   ("헤더") 
st.subheader("소제목") 
st.text     ("일반 텍스트") 
st.write    ("출력") 

#입력 요소: 
name    = st.text_input     ("이름 입력") 
age     = st.number_input   ("나이 입력", min_value=0, max_value=100) 
gender  = st.selectbox      ("성별 선택", ["남", "여"]) 
agree   = st.checkbox       ("동의합니다") 
btn     = st.button         ("확인") 

#출력 요소: 
st.success  ("성공 메시지") 
st.warning  ("경고 메시지") 
st.error    ("오류 메시지") 
