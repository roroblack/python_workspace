# path      :   .\\module\\my_module.py
# module    :   module.my_module.py         (패키지명.모듈명)
# 사용자 정의 모듈

# 전역변수와 함수와 클래스들을 작성해 놓은 파이썬 소스 파일
# 실행 코드는 포함하지 않아야 함 (main 이 있으면 x)
# 자주 반복적으로 쓰는 코드를 따로 작성해 놓고 필요시 가져다 쓰는 파일
# 장점 1 : 소스코드 중복 줄임
# 장점 2 : 유지보수 편리 (코드 수정이 필요한 경우 모듈만 수정하면 됨)
# 장점 3 : 애플리케이션 구조 설정이 편해짐



#-------------------------------------------------------------------------
# 전역 변수 (Global Variable : 함수 밖에 작성한 변수)
PI = 3.141592
count = 10
#-------------------------------------------------------------------------


# 함수 (function : 특정 작업을 수행하는 코드 블록
# 매개함수 (호출 끝나면 사라짐)
def sum(a, b):
    '두 수를 전달 받아서 합을 리턴'
    return a + b

def sub(a, b):
    '두 수를 전달 받아서 차를 리턴'
    return a - b

def mul(a, b):
    '두 수를 전달 받아서 곱을 리턴'
    return a * b

def div(a, b):
    '두 수를 전달 받아서 몫을 리턴'
    if b == 0:
        raise Exception("0으로 나눌 수 없습니다.")
    return a / b

def mod(a, b):
    '두 수를 전달 받아서 나머지를 리턴'
    if b == 0:
        raise Exception("0으로 나눌 수 없습니다.")
    return a % b
# sub..() -----------------------------------------------------------------

def max(*args) : # 여러 개의 값을 받는 매게변수 : 가변 매게변수 (Variable-length Argument)
    '가변 매게변수를 사용해서 전달받은 값들 중에 가장 큰 값을 리턴'
    try :
        max_value = args[0]
        for data in args[1:] :
            if max_value < data :
                max_value = data
            # if ---------------
        # for -------------------

        return max_value
    except IndexError :
        print("처리할 데이터 없음")
        pass
        # raise Exception("최소한 하나 이상의 값을 전달해야 합니다.")
# max() -----------------------------------------------------------------



def min(*args) : # 여러 개의 값을 받는 매게변수 : 가변 매게변수 (Variable-length Argument)
    '가변 매게변수를 사용해서 전달받은 값들 중에 가장 작은 값을 리턴'
    try :
        min_value = args[0]
        for data in args[1:] :
            if min_value > data :
                min_value = data
            # if ---------------
        # for -------------------

        return min_value
    except IndexError :
        print("처리할 데이터 없음")
        pass
# min() -----------------------------------------------------------------

def strlen(st=None) :
    '문자열을 전달 받아서 글자 갯수 리턴'
    slen = 0
    if st != None : # st가 값을 가지고 있다면
        for ch in st : # 참 동안 반복
            slen += 1

    # slen = len(st)
    return slen
# strlen() -----------------------------------------------------------------



#--------------------------------------------------------------------------
if __name__ == "__main__": # 직접 실행하지 않으면 실행 안되는 부분
    print("모듈을 직접 실행")
    a = 10
    b = 20
    print(sum(a, b), sub(a, b), mul(a, b), div(a, b), mod(a, b))

