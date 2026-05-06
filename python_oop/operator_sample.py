# path : ./operator_sample.py
# 연산자 (operator) : 값 계산에 사용되는 기호

'''

[종류(우선순위)로 구분]
최우선 연산자(1) : '()', '.', '[]' (배열기호, 인덱싱)
단항 연산자(2) : '+' (양수 부호), '-', 'not' (부정), '~' (비트 반전), '++', '--' (증감 연산자), '!' (논리 부정), '~' (tield, 비트 반전)
https://docs.python.org/ko/3/reference/expressions.html#operator-precedence
최우선, 단항, 이항 (비교), 삼항 (? : ), 대입 (=), 나열 (,)

1 : 괄호들
2 : 인덱스
3 : await x
4 : **
5 : +x, -x, ~x
6 : *, /, //, %
7 : +, -
8 : <<, >>
9 : & (비트 AND)
10 : ^ (비트 XOR)
11 : | (비트 OR)
12 : in, not in, is, is not, <, <=, >, >=, !=, ==
13 : not x
14 : and
15 : or
16 : if - else
17 : lambda
18 : := (walrus operator)

[기능으로 구분]

'''


# bool 자료형 확인
def func_bool () :
    flag = True
    print("flag : ", flag, type(flag)) # flag :  True

    # 파이썬에서는 대소문자 구분함
    # flag2 = false # NameError: name 'false' is not defined

    # bool() 함수 : 값의 논리 상태를 확인할 떄 사용
    print('문자가 있는 문자열 : ', bool("Hello"))   # 문자가 있는 문자열 :  True
    print('문자가 없는 문자열 : ', bool(""))        # 문자가 없는 문자열 :  False

    # bool() : 값이 저장되어 있는지, 비어 있는지 확인하는 용도로도 사용
    print('result : ', bool({'a':10, 'b':20}))      # result :  True
    print('result : ', bool({}))                    # result :  False

    # 0을 제외한 모든 값은 True로 간주됨
    print('0 : ', bool(0))                          # 0              :  False
    print('0.0 : ', bool(0.0))                      # 0.0            :  False
    print('0j : ', bool(0j))                        # 0j             :  False
    print('0이 아닌 정수 : ', bool(10))             # 0이 아닌 정수  :  True
    print('0이 아닌 실수 : ', bool(0.1))            # 0이 아닌 실수  :  True
    print('0이 아닌 복소수 : ', bool(0.1j))         # 0이 아닌 복소수:  True
    print('0을 제외한 모든 값 : ', bool([0, 0.0, 0j, "", {}, []])) # 0을 제외한 모든 값 :  True

    # 비교(관계) 연산자 확인
    # 값 연산자 비교값 => 결과는 True 또는 False
def op_compare () :
    print('1 == 1 : ', 1 == 1) # 1 == 1 :  True
    print('1 == 2 : ', 1 == 2) # 1 == 2 :  False

    print('1 > 0 : ', 1 > 0)   # 1 > 0 :  True
    print('1 < 2 : ', 1 < 2)   # 1 < 2 :  True

    print('1 >= 1 : ', 1 >= 1) # 1 >= 1 :  True
    print('1 != 0 : ', 1 != 0) # 1 != 0 :  True

# 논리 연산자 : 논리값 (True, False) 를 계산에 사용하는 연산자
# and, or, not
def op_logical () :
    a = 1
    b = 2

    print(a > 0 and b > 1)      # True and True => True (최종 결과)
    print(a == 0 or b != 1)     # False or True => True (최종 결과)

    # and 연산자 특징 :
    # 앞 and 뒤 : 앞이 false 면 뒤는 계산 안함 (short-circuit evaluation)
    # 앞이 True 면 뒤 계산함
    # 이 성질을 이용하는 짧은 조건문이 있음 (모든 스크립트에서 사용함)
    print('a' and 'b') # 앞이 True 라 뒤 'b' 출력
    print('' and 'b')  # 앞이 False 라 뒤 계산 안해서 '' 출력
    print('a' and 'b' and 'c') # 앞이 True 라 뒤 'b' 출력, 'b'도 True 라 뒤 'c' 출력

    # or 연산자 특징 :
    # 앞 or 뒤 : 앞이 True 면 뒤는 계산 안함 (short-circuit evaluation)
    # 앞이 False 면 뒤 계산함
    print('a' or 'b') # 앞이 True 라 뒤 계산 안해서 'a' 출력
    

#------------------------------
if __name__ == "__main__" :
    func_bool()
    op_compare()
    op_logical()

