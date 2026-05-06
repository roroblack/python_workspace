# file path : fileio_sample\\fileio_module.py
# module    : fileio_sample.fileio_module

# 파이썬에서의 파일입출력 처리 테스트용 스크립트 (함수들만 저장된 모듈 파일)
# 파이썬에서의 파일입출력
# open() -> f.write() read() close() flush() -> close()

"""
파일 변수 = open("디렉토리명\\파일명.확장자", '모드 w, r, a, x, b, t, +')
파일입출력의 기본은 텍스트(문자) 파일 입출력임
열기모드 
(
    w(t:기본), wt, wb 등 : 파일이 존재할 때는 덮어쓰기, 존재하지 않을 때는 새로 생성하여 쓰기
    x, xt, xb           : 파일이 존재하지 않을 때만 새로 생성하여 쓰기. 존재할 때는 에러
    r(t:기본), rt, rb 등 : 파일이 존재할 때만 읽기, 존재하지 않을 때는 에러
    a, at, ab           : 파일이 존재할 때는 이어쓰기, 존재하지 않을 때는 새로 생성하여 쓰기
)

"""


# 1. 파일 만들고 값 기록 저장 테스트
import os

def test_fwrite():
    # f = open("testa.txt", 'w') # MS949 라 한글 깨짐
    # f = open("testa.txt", 'wt', encoding='utf-8') # 텍스트 파일의 인코딩을 utf-8 로 지정하여 열기
    f = open("testa.txt", 'wt', encoding='UTF-8') # 텍스트 파일의 인코딩을 utf-8 로 지정하여 열기
    f.write("test file writing check...\n")
    f.write("2026-05-04 10:39:00\n")
    f.write("파일에 저장 확인용") # 텍스트 파일의 기본 인코딩은 os 를 따름. windows os 는 'MS949' (ISO-8859-1) 인코딩을 기본으로 사용함. utf-8 인코딩이 아님. 그래서 한글이 깨질 수 있음.
    f.write("★★★★★★★★★★★★★★★★★★★★★★★★\n")
    f.close()

    print(os.getcwd()) # 현재 작업 디렉토리 경로 출력
    print(os.listdir()) # 현재 작업 디렉토리의 파일과 디렉토리 목록 출력



# 1.1 파일 읽기 테스트
def test_fread():
    f = open("testa.txt", 'rt', encoding='utf-8') # 텍스트 파일의 인코딩을 utf-8 로 지정하여 열기
    print(f.read()) # 파일 전체 읽기
    f.close()



# 2. 원하는 디렉토리에 파일을 만들려면
# open 함수 첫번쨰 전달인자(전달값(argument): 함수의 매개변수(papameter)로 전달되는 값)에 디렉토리 경로를 포함하여 작성하면 됨
# 예시 : open("C:\\Users\\playdata2\\Documents\\python_workspace\\python_fileio\\testb.txt", 'w') # C 드라이브의 Users 폴더의 playdata2 폴더의 Documents 폴더의 python_workspace 폴더의 python_fileio 폴더에 testb.txt 파일이 만들어짐
# 주의 : 백슬러시(\)는 반드시 두개 써야 함

def test_fwrite2():
    f = open("fileio_sample\\testb.txt", 'x', encoding='utf-8') # 덮어쓰기 방지용으로 사용
    f.write("test file writing check 2 ...\n")
    f.write("2026-05-04 10:39:00\n")
    f.write("파일에 저장 확인용")
    f.write("★★★★★★★★★★★★★★★★★★★★★★★★\n")
    f.close()

    f = open("fileio_sample\\testb.txt", 'rt+', encoding='utf-8') # 이어쓰기 모드로 열기
    print(f.read()) # 파일 전체 읽기
    f.close()
    return


def test_append():
    f = open("fileio_sample\\testb.txt", 'at+', encoding='utf-8') # 이어쓰기 모드로 열기
    f.write(input("추가할 내용 입력: ") + "\n") # 사용자로부터 추가할 내용 입력 받아서 파일에 기록
    f.write("★★★★★★★★★★★★★★★★★★★★★★★★\n")
    f.seek(0)  # 커서를 맨 앞으로 강제 이동
    print(f.read()) # 파일 전체 읽기
    
    f.close()

    return


# 파이썬에서 파일이나 디렉토리 다루기
# os 모듈이 제공하는 함수를 사용함
def test_osmodule():
    print(os.getlogin())    # 현재 로그인한 사용자 계정 이름 출력
    print(os.getcwd())      # 현재 작업 디렉토리 경로 출력
    print(os.listdir())     # 현재 작업 디렉토리의 파일과 디렉토리 목록 출력

    system_user = os.getlogin()
    work_dir = 'C:\\Users\\' + system_user + '\\Desktop\\python'

    # 디렉토리 만들기 : os.mkdir('만들 디렉토리경로와 디렉토리명')
    # os.mkdir(work_dir) # 주의 : 같은 이름의 디렉토리가 있으면 에러남

    # 작업 디렉토리 변경하기 : os.chdir('변경할 디렉토리명을 경로 포함해서 작성')
    os.chdir(work_dir)
    print(os.getcwd()) # 작업 디렉토리가 변경되었는지 확인

    # 변경한 디렉토리에 파일 저장
    f = open("sample.txt", 'w', encoding='utf-8')
    f.write("파이썬으로 디렉토리 만들고, 거기 파일 생성해서 저장\n")

    st = '''변경된 디렉토리에 파일 생성하고
유니코드로 인코딩된 문자열을 기록 저장
확인함'''

    f.write(st)
    f.close()

    

    # 시스템 환경변수, 디렉토리, 파일 다루기
    # listdir() : 현재 작업 디렉토리 안의 파일들과 하위 디렉토리 목록 조회
    print(os.listdir(os.getcwd()))
    print(os.listdir("."))          # 현재 작업 디렉토리
    print(os.listdir("../"))        # 현재 작업 디렉토리의 상위 디렉토리

    # rename() : 디렉토리나 파일 이름 변경하기
    # os.rename("testa.txt", "sample_a.txt") # sample.txt 파일 이름을 sample_renamed.txt 로 변경

    # path.exists() : 디렉토리나 파일이 존재하는지 여부 확인하기
    print(os.path.exists("example.txt")) # example.txt 파일이 존재하는지 여부 확인. 없으면 False 리턴
    print(os.path.exists("sample.txt")) # sample.txt 파일이 존재하는지 여부 확인

    # path.abspath() : 디렉토리나 파일의 절대 경로 구하기
    print(os.path.abspath("sample.txt")) # sample.txt 파일의 절대 경로

    # path.basename(), dirname(), split() : 파일명, 경로명, 두 개 분리
    current_path = os.path.abspath("sample.txt")
    print('current_path : ', current_path)
    print('basename : ', os.path.basename(current_path)) # 파일명.확장자 추출
    print('dirname : ', os.path.dirname(current_path))   # 경로명 추출
    print('split : ', os.path.split(current_path))       # 경로명과 파일명.확장자 분리하여 튜플로 리턴

    # path.splitdrive(), splitext() : 경로에서 드라이브명만, 확장자만 추출
    print(os.path.splitdrive(current_path)) # 드라이브명과 나머지 경로로 분리하여 튜플로 리턴
    print(os.path.splitext(current_path))   # 파일명과 확장자로 분리하여 튜플로 리턴

    return

#-------------------------------------------------


# 4. r (rt)        : 읽기 전용
# 주의              : 대상 파일이 없으면 에러
# read() 함수       : 파일 전체 읽기
# readline() 함수   : 파일 한 줄씩 읽기. 읽을 라인이 없으면 None 리턴
# readlines() 함수  : 모든 라인을 줄단위(아이템)로 읽어서 리스트로 리턴. 아이템 없으면 빈 리스트 리턴
def test_fread2():
    print(os.getcwd()) # 현재 작업 디렉토리 경로 출력
    f = open("sample.txt", 'rt', encoding='utf-8')
    print(f.read()) # 파일 전체 읽기
    
    f.seek(0) # 커서를 맨 앞으로 강제 이동
    
    # 파일의 내용을 한 줄씩 읽어서 처리한다면
    while f != None:
        line = f.readline() # 파일에서 한 줄 읽기
        # if not line : break
        if line == '': break # 읽을 라인이 없으면 (None 이면) 빈 문자열이 리턴됨

        # print() 함수의 end 매개변수의 기본값 '\n' 제거함
        print(f"{f.tell()}" + line, end='') # 줄바꿈 문자가 이미 포함되어 있으므로 end=''로 설정하여 줄바꿈이 중복되지 않도록 함

    f.close()
    return

def test_fread3():
    f = open("sample.txt", 'rt', encoding='utf-8')
    lines = f.readlines() # 파일의 모든 라인을 줄단위로 읽어서 리스트로 리턴
    print(lines) # 리스트로 출력됨
    f.close()
    return



# 5. 리스트, 튜플, 딕셔너리 등에 저장한 데이터들을 파일에 저장
# writelines() 사용
def test_writelines():
    tp = ('첫번쨰', '두 번째', '세 번째')
    ls = ['첫번쨰', '두 번째', '세 번째']
    dct = {
        'line1': '첫 번째 줄입니다.',
        'line2': '두 번째 줄입니다.',
        'line3': '세 번째 줄입니다.'
    }
    f = open("list.txt", 'w', encoding='utf-8')
    f.writelines(tp)
    f.write("\n") # writelines() 함수는 줄바꿈 문자를 자동으로 추가하지 않으므로, 줄바꿈이 필요한 경우에는 명시적으로 추가해주어야 함
    f.writelines(ls)
    f.write("\n")
    f.writelines(dct.values())
    f.write("\n")
    f.close()




"""
# 파일 열기
# f = open("test.txt", 'w') # 현재 디렉토리에 test.txt 파일이 만들어짐
# 파일에 문자열 기록하기
# f.write("Hello, World!\n")
# f.write("This is a test file.\n")
# f.write("Python file I/O is easy.\n")
# 파일 닫기
# f.close()
"""
  