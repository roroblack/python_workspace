# 2.py
# streamlit 예제 1 - 기본 입력/출력 요소

import streamlit as st 
import pickle as pk

st.set_page_config(page_title="파이썬 GUI 예제", page_icon="🖥️", layout="centered") 

st.title    ("파이썬 Streamlit GUI 예제") 
st.write    ("사용자 입력을 받아 화면에 출력하는 웹 GUI입니다.") 

name    = st.text_input     ("이름을 입력하세요") 
age     = st.number_input   ("나이를 입력하세요",   min_value=0, max_value=120, step=1) 
major   = st.selectbox      ("전공을 선택하세요",   ["컴퓨터공학", "정보통신", "전자공학", "AI", "기타"]) 
memo    = st.text_area      ("자기소개를 입력하세요") 

if st.button("확인"): 
    if name.strip() == "":                                  # strip()으로 공백 제거 후 빈 문자열인지 확인
        st.warning  ("이름을 입력하세요.") 
    else: 
        st.success  ("입력이 완료되었습니다.") 
        st.write    ("### 입력 결과")
        st.write    (f"이름:        {name}") 
        st.write    (f"나이:        {age}") 
        st.write    (f"전공:        {major}, {type(major)}") 
        st.write    (f"자기소개:    {memo}")

if st.button("데이터 저장"):
    if name.strip() == "":                                  # strip()으로 공백 제거 후 빈 문자열인지 확인
        st.warning("이름을 입력하세요.")
    else:
        lst = [name, age, major, memo]
        f = open("./data/data.pkl", "wb")
        pk.dump(lst, f)
        f.close()
        st.success  ("데이터 저장이 완료되었습니다.") 

if st.button("데이터 불러오기"):
    try:
        f = open("./data/data.pkl", "rb")
        data = pk.load(f)
        f.close()
        st.write("### 저장된 데이터")
        st.write(data)
        st.success  ("데이터 불러오기가 완료되었습니다.") 

    except FileNotFoundError:
        st.error("저장된 데이터가 없습니다.")