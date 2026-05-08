# path : .\\function\\func_sample.py
# 파이썬에서 함수 만들어 사용하기 테스트 스크립트

'''

함수 (function) : 반복 사용되는 소스코드를 분리해 이름 붙인 것
파이썬에서 함수 만들기
def 함수명(매개변수): <== 매개변수 (parameter) 는 0 ~ n 개 가능
    함수가 실행할 코드
    ...
    return 혹은 return 값 혹은 return 여러개 값 <== 여러개 반환시 튜플로 반환 (단, 반환을 하나씩 받으면 튜플이 아니라 일반 변수로 각각 반환해줌)

    함수의 사용 (call, 호출) : 함수가 만들어진 형태 (signature) 에 맞게 사용해야 함
    ==> 함수 이름 틀리지 않아야 함 (대소문자 주의, _ (언더스코어) 갯수 확인)
    ==> 매개변수 갯수 일치되게 전달인자 (전달값, argument) 쓰자
    ==> 반환값 여부도 확인 : 반환값이 있는 함수는 다른 함수 안에 중첩 사용할 수 있음 ==> 함수명 (반환값이 있는 함수())

'''

# 아무런 기능이 없는 (처리할 코드가 준비중인) 빈 함수를 만들 떄는 pass 씀
def func_empty():
    pass

# 함수 이름 아래에 함수 설명 (description) 을 적어둘 수 있음. 따옴표 사용함
def hello():
    '이 함수는 함수 작성 연습용'
    print('Welcome!')
    print('함수명에 예약어, 공백 사용 못 함')
    return # 반환값 없는 리턴은 생략해도 됨

# 매개변수 있고, 반환값 있는 함수
def add(x, y):
    print('x : {}, y : {}:'.format(x, y))
    return x + y

# 파이썬에서는 여러개의 값을 리턴 가능 ==> 자동 튜플 반환
def func2(a, b):
    print(f'a : {a}, b : {b}')
    return a * 2, b * 2

# 이 스크립트를 실행 파일로 만들려면
if __name__ == '__main__':
    print('func_empty()     : ', func_empty())
    print('add(1, 2)        : ', add(1, 2))
    print('func2(3, 4)      : ', func2(3, 4))
    hello()
    print(type(classmethod)) # 클래스도 type 이라는 객체

    # 함수 설명(description) 을 확인 할 때 help(함수명) 사용
    help(hello)
    help(print)
    help(input)

    # 매개변수 있고 반환값 있는 함수 사용 (call)
    # 반환값 받을 변수 = 함수명(매개변수에게 전달할 값, 전달인자) ==> 매개변수 갯수가 일치해야 함
    result = add(10,20)
    print('result : ', result)
    print('result : ', add(10, 20)) # 반환값이 있는 함수는 다른 함수 안에 중첩 사용할 수 있음

    result2 = func2(100, 200)
    print('result2 : ', result2, type(result2)) # 튜플로 반환

    n1, n2 = func2(1000, 2000) # 튜플로 반환된 값을 각각 변수로 받을 수 있음
    print(n1, n2, type(n1), type(n2))


