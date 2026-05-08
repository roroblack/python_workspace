# 3.py
# streamlit 예제 2 - 데이터 시각화

import streamlit            as st 
import pandas               as pd 
import matplotlib.pyplot    as plt 

st.set_page_config  (page_title="Data Visualization App", page_icon="📊", layout="wide") 
st.title            ("Streamlit Data Visualization Example") 
 
data = { 
    "Subject": ["Python", "SQL", "Spring Boot", "React", "AI"], 
    "Score": [85, 78, 92, 88, 95] 
} 
 
df = pd.DataFrame   (data) # 데이터프레임 생성 == 표 만들어라
# print(df)
 
st.subheader        ("1. Data Table") 
st.dataframe        (df, use_container_width=True) 
 
st.subheader        ("2. Data Summary") 
st.write            (df.describe(include="all"))            # 통계 요약 기준 함수 describe() - 숫자형 데이터는 평균, 표준편차, 최소값, 최대값 등 요약 / 범주형 데이터는 고유값 개수, 최빈값 등 요약
 
st.subheader        ("3. Bar Chart") 
fig, ax = plt.subplots()                                    # 그래프 영역 표시 (시각화 - 나중에 따로 배울 것)
ax.bar              (df["Subject"], df["Score"]) 
ax.set_xlabel       ("Subject")                             # 시각화 한글 설정은 폰트 설정 필요 (나중에)
ax.set_ylabel       ("Score") 
ax.set_title        ("Score by Subject") 
st.pyplot           (fig) 