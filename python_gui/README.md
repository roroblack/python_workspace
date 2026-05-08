# README.md
# Streamlit 사용 연습 프로젝트

1. 프로젝트 폴더 만들기 => 폴더 열기
2. 터미널 열기 (cmd)
3. 가상환경 만들기
python -m venv .venv
활성화 안 된 경우
프롬프트 >.venv\Scripts\activate 엔터
활성화 되면 아래처럼 터미널에 표시 됨
(.venv) 프롬프트> 가상환경 활성화 상태임

4. 설치할 외부 모듈 목록 파일 만들어 설치하기 : requirements.txt
pip install -r requirements.txt

5. 웹 gui 프로그램 코드 작성
6. 실행
터미널 프로젝트 루트 > streamlit run 폴더명/소스파일명.py

# MacOS/Linux
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run 폴더명/파일명.py