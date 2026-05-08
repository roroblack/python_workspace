# path      :   .\\module\\used_module.py
# module    :   module.used_module
# 파이썬에서 모듈 만들어 사용 테스트 스크립트

# 모듈 (module) : 파이썬 소스 파일이다. (파일명.py)
# 파일명이 곧 모듈명
# 모듈용 소스 파일에는 함수와 젼역변수가 저장되면 됨
# 모듈이 제공하는 함수와 전역변수를 사용하려면, import 문을 선언해야 함
# import 모듈명 또는 import 패키지명.모듈명 [as 줄임말 - 생략 가능]
# 모듈명.함수명() 또는 모듈명.전역변수명 또는 모듈줄임말.함수명 또는 모듈줄임말.전역변수명

# 파이썬이 제공하는 표준 모듈 사용
import keyword
# keyword.py 파일을 의미함
# C:\Users\playdata2\AppData\Local\Python\pythoncore-3.14-64\Lib\keyword.py

print(keyword.kwlist) # 파이썬에서 예약어로 사용되는 단어들을 리스트로 리턴하는 함수
# 모듈명.전역변수

# 모듈은 다른 파이썬 파일에서 사용될 수 있게 함수와 전역변수를 따로 저장해서 제공하는 소스 파일임

# 모듈 임포트시에 모듈명에 대한 줄임말을 같이 선언할 수 있음
# import 패키지명.모듈명 as 줄임말
import keyword as kw

print(kw.kwlist)                                    # 줄임말.전역변수
print(kw.__file__)                                  # 모듈이 저장된 파일의 경로를 리턴하는 전역변수

# 현재 설치되어 있는 모듈 확인
help('modules')                                     # 설치된 모듈의 목록을 보여주는 함수

# 모듈 설명 참조
# help('random')                                    # random 모듈의 설명을 보여주는 함수

# 파이썬이 제공하는 표준 모듈들-------------------------------------------------------------------
import os                                           # 파일이나 디렉토리 관련된 기능을 제공하는 모듈
print(os.getcwd())                                  # 현재 작업 디렉토리의 경로를 리턴하는 함수

import time
print(time.localtime())                             # 현재 시간을 구조체로 리턴하는 함수
time.sleep(1)                                       # 1초 동안 프로그램을 일시 정지하는 함수


import random
print(random.random())                              # 0.0 이상 1.0 미만의 난수(실수)를 리턴하는 함수
print(random.randint(1, 10))                        # 1 이상 10 이하의 난수(정수)를 리턴하는 함수
print(random.randrange(1, 10, 2))                   # 1 <= (2간격의 정수) < 10

import math # 수학 계산 관련 기능을 제공
print(math.pi)                                      # 원주율을 리턴하는 전역변수
print(math.sqrt(2))                                 # 2의 제곱근을 리턴하는 함수
print('5! = ', math.factorial(5))                   # 5의 팩토리얼을 리턴하는 함수

import calendar # 달력 관련 기능을 제공하는 모듈
print(calendar.prmonth(2024, 6))                      # 2024년 6월의 달력을 문자열로 리턴하는 함수

# __name__ : 현재 실행되고 있는 모듈 이름 확인
print(__name__) # __main__ : main 모듈 이름 출력
# 프로그램을 실행하면 기본으로 파일은 main 모듈이 됨
# 즉, main 만 실행할 수 있다는 뜻

#---------------------------------------------------------------------------------------------
# 사용자 정의 모듈 사용하기
# 모듈 파일과 사용 파일이 같은 폴더 안에 있으면 파일명만 사용
import my_module as my

print('더하기 : ',  my.sum(10, 20)) # 매개변수가 2개이면, 전달값도 2개여야 함 (반드시 갯수 일치해야 함)
print('빼기 : ',    my.sub(10, 20))
print('곱하기 : ',  my.mul(10, 20))
print('나누기 : ',  my.div(10, 20))
print('나머지 : ',  my.mod(10, 20))
print('최대값 : ',  my.max(10, 20, 30, 40, 50))


try :
    print('나누기한 나머지 : ',  my.mod(10, 0))
except ZeroDivisionError as zde :
    print(zde)
    pass # 프로그램을 중지하지 않고 계속 실행

print('최대값 : ',  my.max())                   # 가변 매개변수는 전달값이 없어도 됨 (0개 이상)
print('최대값 : ',  my.max(10))                 # 가변 매개변수는 전달값이 1개 이상이어야 함 (최소한 하나 이상의 값을 전달해야 함)
print('최대값 : ',  my.max(10, 20, 30, 40, 50))

print('최소값 : ',  my.min())                   
print('최소값 : ',  my.min(10))                 
print('최소값 : ',  my.min(10, 20, 30, 40, 50)) 

print('글자 갯수    : ',  my.strlen())           
print('글자 갯수    : ',  my.strlen("module test"))

print('my 원주율    : ',  my.pi)                 
print('카운트       : ',  my.count)

# 외부 모듈을 사용하려면
# 1. vscode 에서는 프로젝트 안에 가상환경을 생성함
# 터미널에서 현재 프로젝트 폴더>python -m venv venv 가상환경폴더명

# 2. 가상환경 활성화 (activate) : 자동으로 활성화됨
# 자동 활성화 안 될 경우 직접 활성화 시킴
# ps 터미널 > ./가상환경폴더명/scripts/Activate.ps1 입력하고 엔터
# cmd 터미널 > ./가상환경폴더명/scripts/activate.bat 입력하고 엔터
# (가상환경이름) 현재 프로젝트 경로> 표시되면 가상환경 활성화 된 것임

# 3. 터미널에서 외부 모듈 설치      : pip install 모듈명
# python --version (혹은 -V)        : 파이썬 버전 확인
# pip list                          : 설치된 모듈 목록 확인
# 설치 예 > pip install requests    (pip 는 가능한 최신 버전으로)
# pip install numpy, pandas (, matplotlib, scikit-learn, tensorflow, pytorch, flask, django) 등등
# 설치후 import 할 때 노란밑줄 뜨면 아직 로드중임

import requests # HTTP 요청을 보내는 기능을 제공하는 외부 모듈
import numpy as np # 수치 계산과 배열 처리를 위한 외부 모듈
import pandas as pd # 데이터 분석과 조작을 위한 외부 모듈
