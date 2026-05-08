# streamlit 사용 : 로그인 기능과  csv 파일 업로드 및 데이터 분석 프로젝트

## 로그인을 위한 테스트 계정
| email                 | password |
| admin@example.com,        1234,           관리자
| student@example.com,      pass123,        수강생
| teacher@example.com,      teach123,       강사

## 실행
python -m venv .venv
pip install -r requirements.txt
streamlit run app/main.py

## 프로젝트 구조
프로젝트명 : streamlit_login_csv_project

streamlit_login_csv_project
    |- .venv                 # 가상환경 폴더
    |- requirements.txt      # 외부모듈 설치 목록 파일
    |- README.md             # 프로젝트 설명 파일
    |- data\
        |- sample_sales.csv  # 데이터 분석용 데이터 파일
        |- users.csv         # 로그인할 사용자 정보 저장 파일
    |- app\
        |- main.py           # gui 코드 파일

## 기능 설명
로그인 계정은 'data\users.csv' 파일에서 읽어옴
로그인 실패시 팝업에 '아이디와 암호가 일치하지 않습니다. 확인하고 다시 입력하세요.' 출력하고, 닫기 버튼 누르면 다시 로그인 페이지 표시되게 함
로그인 성공 후에 csv 파일을 업로드하면 데이터 테이블, 기본 통계, 선 그래프, 막대 그래프, 히스토그램을 출력

## 배포 방법
Github 에 프로젝트를 업로드한 뒤 streamlit community cloud 에서 새 앱을 만들고 실행파일을 업로드 함

# 작성팀정보, 작성일자 .. 등등 다양한 정보 담을 수 있음