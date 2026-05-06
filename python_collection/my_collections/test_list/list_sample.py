# path(파일 경로) 로 표현 : my_collections\test_list\list_sample.py
# 함수들만 저장되어 있는 소스 파일 == 모듈(module) 이라고 함
# 모듈들을 모아놓은 폴더 == 패키지(package) 라고 함
# 모듈로 표현 : my_collections.test_list.list_sample

# 리스트(list) 사용 테스트용 함수들 제공 스크립트

'''
파이썬 리스트(list) 자료형
파이썬이 제공하는 군집 자료형임 (자바의 List 와 같은 자료형임)

개념 : 여러 종류의 값들을 순차적으로 저장하는 자료형임
저장 용량에 제한이 없음
저장되는 값의 종류에도 제한이 없음
저장 순서에 대한 순번(인덱스, index)가 있음 => 인덱싱, 슬라이싱 연산 가능함
'''

# 리스트 생성방법1 : list() 함수 사용
def make_list1():
    # print('make_list1() 함수 실행됨')
    lst = list()
    print(lst, type(lst), id(lst))

    return  # 함수 코드 맨 마지막에 반드시 존재함, 생략할 수 있음

# 리스트 생성방법2 : [] 대괄호 사용
def make_list2():
    lst = []
    print(lst, type(lst), id(lst))
    return

# list 자료형 특징 1 : 문자열(str)과 같이 인덱싱, 슬라이싱 연산이 가능함
# index (순번 : 저장 순서, 0부터 시작함)
# 인덱싱 표현 : 리스트변수[순번]
def list_indexing():
    lst = [1, 2, 3, 'python', 3.45, [11, 22, 33], True, False]
    print('0번째 기록된 값 조회 : ', lst[0])  # 1
    print('3번째 기록된 값 조회 : ', lst[3])  # python
    print('5번째 기록된 값 조회 : ', lst[5])  # [11, 22, 33]
    # return

# 슬라이싱 : 리스트에 저장된 데이터들 부분 추출
# 표현 : 리스트변수[시작인덱스:끝인덱스:간격]
# 시작인덱스부터 끝인덱스 - 1 위치까지 추출됨
# 간격은 생략되면 기본은 1임

# len(리스트변수) : 리스트에 저장된 데이터 갯수 리턴
def list_slicing():
    lst = [1, 2, 3, 'python', 3.45, [11, 22, 33], True, False]
    print('lst 에 저장된 데이터 갯수 : ', len(lst))  # 8
    # len()을 이용해서 마지막 위치의 값 조회에 활용할 수도 있음
    print('lst 에 저장된 마지막 인덱스 조회 : ', len(lst) - 1)  # 7
    print('lst 의 마지막 값 : ', lst[len(lst) - 1], lst[-1])  # False False
    print('lst 의 1번째부터 마지막 인덱스 앞 위치까지 부분 추출 : ', lst[1:len(lst) - 1:1])  # [2, 3, 'python', 3.45, [11, 22, 33], True] => list
    
    print('0번 인덱스부터 3번 인덱스까지 데이터 추출 : ', lst[0:4:1])  # [1, 2, 3, 'python'] -> list 로 반환됨
    print('0번 인덱스부터 3번 인덱스까지 데이터 추출 : ', lst[:4])  # [1, 2, 3, 'python'] 
    print('0번 인덱스부터 3번 인덱스까지 데이터 추출 : ', lst[:4:1])  # [1, 2, 3, 'python'] 
    print('0번 인덱스부터 3번 인덱스까지 데이터 추출 : ', lst[0:4])  # [1, 2, 3, 'python'] 
    return

# list 자료형 특징 2 : 요소(element, 리스트 안의 인덱스 위치의 데이터)의 값은 변경할 수 있음
# 변경할 값의 종류에 제한이 없다.
# 인덱스 이용함 => 리스트변수[인덱스] = 바꿀값
def change_element():
    lst = [1, 2, 3, 'python', 3.45, [11, 22, 33], True, False]   
    # 지역변수 (local variable) : 함수 안에서 만든 변수
    # 함수 실행(호출, call)시 생성됨, 함수 종료(반환, return)시 자동 소멸됨
    print('변경 전 : ', lst)
    lst[0] = 77
    print('변경 후 : ', lst)
    lst[1] = 'test'
    print('변경 후 : ', lst)
    lst[2] = [1.2, 2.3, 3.4]
    print('변경 후 : ', lst)
    return


