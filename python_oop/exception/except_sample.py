# path : ./exception/except_sample.py
# module : exception.except_sample
# 파이썬에서의 예외 처리 (Exception Handling) test 스크립트

'''

예외 : 소스 코드로 해결할 수 있는 에러 (코드로 해결할 수 없는 에러는 오류 (Error) 라고 함)
에러의 종류 :
    - system error : 소스코드로 해결 불가
        메모리 부족, 저장장치 공간 부족, 네트워크 연결 실패, 배터리 전원 부족(SystemExit), 하드웨어 고장 등
    - syntax error : 문법적으로 잘못된 코드 작성
        개발툴에서 자동 검사 가능, 구문을 수정해서 해결
    - runtime error : 실행시 발생
        사용자 입력 오류 등으로 에러 발생하면 코드 수정해서 해결함 ==> 예외 처리 (Exception Handling)
    
에러 처리 방법 :
    - if 조건문으로 에러 상황을 예측해서 미리 조치
        => 예외 상황 (예측된 에러 상황) 을 처리하는 별도의 구문이 있음 : 예외 처리 구문 사용을 권장 

'''


from xxlimited import new


def test_error () :
    '에러 발생 예제 테스트 함수'
    # print('test error) # SyntaxError: EOL while scanning string literal - 직접 수정해야 함

    a = 10
    b = 0
    # c = a / b # ZeroDivisionError: division by zero           => RuntimeError

    # 4 + new * 3 # NameError: name 'new' is not defined 

    # lst = [1, 2]
    # print(lst[2]) # IndexError: list index out of range       => RuntimeError

    # dct = {'a': 10, 'b': 20}
    # print(dct   ['c']) # KeyError: 'c'                        => RuntimeError
#---------------------------------------------------------------------------------



# 런타임 에러 중에 사용자가 입력값을 잘못 입력하는 경우
def test_input_error () :
    '입력 오류 관련 에러 예제 테스트 함수'
    # num = int(input('정수를 입력 : ')) # 문자나 논리값을 입력했다면 ValueError: invalid literal for int() with base 10: '입력값' => RuntimeError
    # if 문으로 처리할 수 없는 에러 발생 상황인 경우 ==> 예외 처리 구문 사용 권장

    # 해결법 1 : 입력 따로 조건 처리로 형변환 따로 작성
    num = input('정수를 입력하세요 : ')
    if num.isdecimal() : # 정수 10진수인가 체크. 맞으면 True 반환
        num = int(num)
        print(num, type(num))
    else :
        print('정수 숫자만 입력해야 합니다. 다시 입력하세요.')
#---------------------------------------------------------------------------------

# 해결법 2 : 예외 처리 구문 사용
'''

try :
    런타임 에러 발생 가능성이 있는 구문들 또는 일반 구문들

except :
    에러가 발생 했을 떄 실행할 구문(들)

'''
def test_input_error2() :
    '입력 오류 관련 에러 예제 테스트 함수 - 예외 처리 구문 사용'
    try :
        num = int(input('정수를 입력하세요 : '))
        print(num, type(num))
    except ValueError : # ValueError 라는 에러가 발생했을 때 실행할 구문 작성
        print('정수 숫자만 입력해야 합니다. 다시 입력하세요.')
#------------------------------------------------------------------------------

# 예외 처리시 except 에 pass 를 사용하면
# 오류 발생시 프로그램을 멈추지 않고 계속 동작되게 할 수 있음
def except_pass () :
    '예외 처리 구문에서 except 에 pass 사용 예제 테스트 함수'
    lst = ['1', '2', 1, 2, 3.14, True, 'hello']
    digit_num = []

    print(lst)

    # lst 에서 숫자만 골라서 digit_num 에 저장하기
    for idx in range(len(lst)) : # len(lst) 저장 갯수 리턴 => range(갯수) : 0 ~ 갯수 - 1 까지의 숫자를 생성하는 함수 [0,1,2,3,4,5,6]
        try :
            digit_num.append(int(lst[idx])) # 실수는 소수 버리면서 형변환
        except:
            pass
    # for-----------------------------------

    print(digit_num)
#------------------------------------------------------------------------------

# finally : 예외 발생과 상관 없이 반드시 실행할 구문을 작성하는 영역
import math # 수학 계산 관련 함수 제공 모듈
def test_finally() :
    'finally 구문 사용 테스트 함수'
    try :                                               # 예외 발생 가능 구문 작성 영역
        radius = float(input('원의 반지름 입력 : '))
    except Exception as e:                                            # 에러가 발생시 처리 구문 작성 영역
        print('숫자만 입력해야 합니다.', e)
    else :                                              # 예외가 발생하지 않을시 실행할 구문 작성 영역 (반드시 except 다음에 사용)
        print('반지름 : ', radius)
        print('원의 면적 : ', math.pi * math.pow(radius, 2))
    finally :                                           # 예외 발생과 상관 없이 반드시 실행할 구문 작성 영역
        print('예외 처리 구문 테스트 종료')



# 실행 테스트----------------------------------------------------------------
if __name__ == "__main__" :
    test_error()
    # test_input_error()
    # test_input_error2()
    except_pass()
    test_finally()