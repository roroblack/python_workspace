# path : .\\function\\func_saple3.py

# 파이썬 함수 만들기에서 매개변수들 설정 테스트 스크립트

def tmax(a, b) :
    '두 개의 값을 전달 받아서 둘 중 큰 값을 리턴하는 함수. call by value 방식'
    print(f'a : {a}, b : {b}, type : {type(a)}, {type(b)}')
    # if a > b : return a # 이건 리턴 2번이라 권장 x
    # else : return b

    result = 0
    
    if a > b :
        result = a
    else :
        result = b

    return result


def func_callby_value():
    'tmax() 함수 테스트용. 매개변수와 전달인자 갯수 일치 확인용 함수'

    result = tmax(10, 20) # call by value 방식
    print('큰 값 : ', result)
    result = tmax(10.5, 20.5)
    print('큰 값 : ', result)

    print('큰 값 : ', tmax('M', 'm')) # call by value 방식

    # 전달 값과 매개변수 갯수가 다를 경우
    # result2 = tmax(120)           # TypeError: tmax() missing 1 required positional argument: 'b'     ==> 매개변수 갯수 일치 안 함
    # result3 = tmax(10, 20, 30)    # TypeError: tmax() takes 2 positional arguments but 3 were given   ==> 매개변수 갯수 일치 안 함
#----------------------------------------

# 파이썬에서 군집자료형을 전달받는 매개변수는 주소를 받는다
def list_in_max(plist) :
    '리스트 객체를 전달 받아서, 저장된 값들 중 가장 큰 값을 찾아내서 리턴하는 함수'
    print(f'plist : {plist}, 주소 : {id(plist)}')
    max = plist[0]
    for item in plist[1:]:
        if item > max:
            max = item
    return max
#----------------------------------------

# 함수 호출시 함수쪽으로 주소를 전달 : call by address (call by reference)
def func_callby_reference():
    '함수 쪽으로 주소 전달 테스트용 함수'
    
    nlist = [45, 2, 442, 11, 2848, 27, 277]
    print(f'nlist : {nlist}, 주소 : {id(nlist)}')

    result = list_in_max(nlist)
    print('nlist 에 저장된 값들 중 가장 큰 값 : ', result) # call by value 면 주소가 다름
#----------------------------------------

# 기본 매개변수 : 기본값 (default) 을 가진 매개변수
# def 함수명 (매개변수 = 기본값, ...):
# 주의 : 뒤쪽 (오른쪽 끝) 매개변수부터 기본값 지정해야 함
#   즉, def 함수명(매개변수, 매개변수, ... 매개변수 = 기본값, 매개변수 = 기본값)    # ok    # 함수(값, 값)
#       def 함수명(매개변수 = 기본값, ... , 매개변수, 매개변수)                     # error # 함수(, 값, 값)
#       def 함수명(매개변수, 매개변수 = 기본값, 매개변수)                           # error # 함수(값, , 값)

# 해당 함수 실행시 기본값이 있는 매개변수는 생략 가능
# 전달값이 없으면 준비된 기본값을 사용함
# def tmin(a, b, c = 0) => 실행시 : tmin(10, 20), tmin(10, 20, 30) 모두 가능
# def tmin(a,, b=0, c=0) ==> 실행시 : tmin(10), tmin(10, 20), tmin(10, 20, 30) 모두 가능
def tmin(a = 0, b = 0, c = 0) : # 실행시 : tmin(), tmin(10), tmin(10, 20), tmin(10, 20, 30)
    '세 개의 값을 전달 받아서 셋 중 가장 작은 값을 리턴하는 함수. call by value 방식'
    print(f'a : {a}, b : {b}, c : {c}, type : {type(a)}, {type(b)}, {type(c)}')
    min = a
    if a < b and a < c:
        min = a
    elif b < c : # and b < a 이게 위에 식에 내포되어 있음
        min = b
    else :
        min = c
    return min
#----------------------------------------

def func_default_param() :
    '기본값 매개변수가 있는 함수 사용 테스트'
    print('가장 작은 값 : ', tmin(12, 3, 45))
    print('가장 작은 값 : ', tmin(12, 3))
    print('가장 작은 값 : ', tmin(12))
    print('가장 작은 값 : ', tmin())
#----------------------------------------

# 재귀 호출 함수 (Recursive Call Function)
# 함수 안에서 자신을 호출
# 주의 : 무한 루프가 되지 않게 종료 조건이 반드시 필요함
# 파이썬은 무한루프에 빠지면 일정 구간 1000회 이상 반복되면 RecursionError: maximum recursion depth exceeded in comparison 에러 발생
def fectorial(n) :
    print(n, ' * ', end='') # end=''  # 줄바꿈 없게
    if n == 0 :
        return 1
    else :
        return n * fectorial(n-1) # 재귀 호출
#----------------------------------------




if __name__ == '__main__':
    func_callby_value()
    func_callby_reference()
    func_default_param()

    print('\n10f : ', fectorial(10))
