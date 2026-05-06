# file path : fileio_sample/fileio_module.py
# module    : fileio_sample.fileio_module

# 파이썬의 기본 파일 입출력은 텍스트 파일 입출력임 (*.txt)
# 텍스트가 아닌 자료형의 파일을 다룰 때는 pickle 모듈 활용함
# 바이너리(이진 데이터 : binary) 형식의 파일을 취급할 때 pickle 모듈 사용함
# 파일 열기 모드 : wb, rb, ab 로 표기해야 함

import os
import pickle

def test_binary_fileio():
    data = {1:'python', 2:'java', 3:'c++'}
    print(data)

    f = open("btest.dat", 'wb') # 바이너리 파일로 열기
    # write(str) 사용 못 함 ==> 파일에 이진 데이터로 기록해야 함
    pickle.dump(data, f) # data 객체를 바이너리 형식으로 파일에 기록
    f.close()

def test_binary_fileio2():
    f = open("btest.dat", 'rb') # 바이너리 파일로 열기
    read_data = pickle.load(f) # 파일에서 바이너리 형식으로 기록된 객체를 읽어서 data 변수에 저장
    print(read_data)
    f.close()

    print(read_data)
    print(type(read_data)) # wb 는 해당 객체타입 그대로 기록함 : <class 'dict'>