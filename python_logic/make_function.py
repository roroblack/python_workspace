# make_function.py
# 파이썬에서 함수 만들기
# def 키워드 사용함

'''
def 함수명(매개변수, ........):
    # 들여쓰기로 함수의 실행 코드가 작성되어야 함 (* 중요 *)
    소스 구문들
    return 결과값
'''

def hello(name):
    print(f'안녕하세요! {name}님')
    return

def check_type():
    a = 1
    b = '1'
    c = 1.1
    d = True
    e = 99999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
    f = 4 + 1j
    print(type(a), type(b), type(c), type(d), type(e), type(f))
    return

# 파이썬에서의 main은 아래와 같이 표현함
if __name__ == '__main__':
    # 프로그램 시작하면 실행할 내용이나 함수를 구문으로 작성함
    print('프로그램 시작!')

    # 함수 실행 : 함수명(전달값)
    hello('홍길동')
    check_type()

    a = '안녕'
    b = '하세요'
    print(a + b)  # 문자 + 문자 : 문자 합치기임 (string concaternation)

    print('프로그램 종료!')
