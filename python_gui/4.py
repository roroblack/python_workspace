# 4.py
# streamlit 예제 3 - CSV 파일 업로드 및 데이터 분석

import streamlit    as st 
import pandas       as pd 
 
st.set_page_config              (page_title="CSV Upload App", page_icon="📁") 
 
st.title                        ("CSV File Upload Example") 
 
uploaded_file = st.file_uploader("Upload a CSV / JSON / XML file", type=["csv", "json", "xml"]) 
 
if uploaded_file is not None:
    file_type = uploaded_file.name.split(".")[-1].lower()

    if file_type == "csv":
        df = pd.read_csv    (uploaded_file)
    elif file_type == "json":
        df = pd.read_json   (uploaded_file)
    elif file_type == "xml":
        df = pd.read_xml    (uploaded_file)

    st.success          (f"{file_type.upper()} file upload successful")
    df = df.convert_dtypes()  # 컬럼 타입 자동 정리 (ArrowInvalid 방지)
    st.write            ("### Data Preview")
    st.dataframe        (df, width='stretch')
    st.write            ("### Basic Statistics")
    st.write            (df.describe())
else:
    st.info             ("No file has been uploaded yet.")