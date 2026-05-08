# path : .\\function\\func_sample2.py

# 변수 생성과 사용 영역 (지역, 스코프 : scope, 생존범위)
# 지역 변수 (Local variable) 와 전역 변수 (Global variable)

def func1():
    num = 10 # 함수 안에서 만든 변수 : 지역변수 (함수 실행될 떄 만들어짐. 함수 종료되면 자동 소멸됨)
    print(f'num : {num}')

# 지역변수는 함수 밖에서 사용 못함
# print(f'num : {num}') # NameError: name 'num' is not defined

# 파이썬에서의 전역변수 : 함수 밖에서 만든 변수
gnum = 100 # 전역변수 (선언된 위치 아래에서 어디서나 사용 가능함)
print(f'gnum : {gnum}')

def func_global():
    print(f'gnum : {gnum}') # UnboundLocalError: local variable 'gnum' referenced before assignment
    # 파이썬에서 전역변수는 선언한 다음 위치부터 어디서나 사용 가능함
    # 파이썬에서는 변수 = 값 선언 구문은 새로운 변수 생성(할당) 임
    gnum = 200
    print(f'gnum : {gnum}') # error 발생

def func_global1():
    # 전역변수 값의 변경을 원한다면 gnum 에 대한 전역 선언이 필요
    global gnum
    print(f'gnum : {gnum}')
    gnum = 200
    print(f'gnum : {gnum}')



# 함수의 매개변수 (parameter)는 전달받은 값을 사용만 함
# 함수 호출부(실행위치)의 변수 값 변경 못 함
# 전달 받은 값이 군집자료형(collection) 이면 아이템(element) 변경 가능
def func_list(plist) : # 전달은 리스트 객체의 주소를 받는 변수 (레퍼런스)
    print('plist 가 받은 주소 : ', id(plist))
    print('before : ', plist)
    plist[1] = 10
    print('after : ', plist)




if __name__ == '__main__':
    
    func1()
    # func_global()
    # func_global1()

    lst = [1, 2, 3] # 리스트 변수 (리스트 객체의 주소를 가짐. 레퍼런스임)
    print('lst 가 참조하는 리스트 객체의 주소 : ', id(lst))
    print('before lst : ', lst)

    func_list(lst) # 함수 실행 : 전달 인자가 주소임 (call by reference)
    print('after lst : ', lst)



