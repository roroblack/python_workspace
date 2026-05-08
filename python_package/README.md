## README.md

# mypackage
간단한 Python 패키지 만들어 사용하기 예제입니다.

## 기능
- sum()
- sub()
- mul()
- div()
- mod()
- max()
- min()
- strlen()
- hello()

## 프로젝트 구조
python_package/
|- README.md
|- setup.py
|- pyproject.toml
|- mypackage/
    |- mymodule.py
    |- message.py
    |- __init__.py


# 패키지 설치
pip install .

# 패키지 설치 확인
- 가상환경 폴더\Libs\패키지명
pip list

pip show my_package

# 배포용 wheel 파일 생성
..> python -m build
=> dist/ 폴더 생김


