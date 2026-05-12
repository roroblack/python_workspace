# allocation.py
# 변수 할당 확인용 소스 파일
"""
파이썬에서의 변수 공간에 값 기록하는 메모리 할당(memory allocation)
- 파이썬의 변수 할당은 동적 할당임
- 동적(Runtime 시 : 실행시) 메모리(RAM)에 변수 공간 만들고 값을 기록하는 것
- 코드 구문 : 
    변수명 = 기록할값
    변수명 = 계산식
- 주의 사항 :
    변수명
    (= 값 없으면 에러임, 할당 안 된 상태임)    
"""
num = 1 + 2
print('num 변수가 가진 값 : ', num)

# 변수 할당시 = (대입연산자) 사용함
# 대입연산자는 반드시 왼쪽에 변수, 오른쪽에 값 또는 계산식 위치함
# 값 = 변수 (에러)
# 100 = a  # SyntaxError: cannot assign to literal here. Maybe you meant '==' instead of '='?

# 한번에 여러 개의 변수에 값을 할당할 수도 있음
# x = 10
# y = 20
# z = 30
x, y, z = 10, 20, 30
print(x, y, z)
print(x, y, z, sep='|')  # sep (seperator) : 구분자 (출력값들 사이에 구분할 기호문자 지정시 사용)
print(x, y, z, sep=', ')

# 한 개의 값을 여러 변수에 할당할 수도 있음
k = m = n = 77
print(k, m, n, sep=',')

# 한 줄(line)에 하나의 문장 작성이 원칙임
# 필요시 한 줄에 여러 문장을 작성한다면, 세미콜론(;)으로 구분함
# num1 = 12
# num2 = 24
num1 = 12 ; num2 = 24
print(num1, num2)

# 두 변수의 값 교환
first, second = 123, 456
print('first : ', first, ', second : ', second)

first, second = second, first  # swap 공식 필요없음
print('first : ', first, ', second : ', second)

# = (순수대입연산자)
# 복합대입연산자 : 산술대입연산자가 주로 사용됨
# 파이썬의 산술연산자 : +, -, *, /(나누었을때의 몫이 실수형), //(나누었을때의 몫이 정수형), %(mod, 나머지), **(제곱연산)
# +=, -=, *=, /=, //=, %=, **=
# 메모리의 변수 공간에 직접 연산하므로, 연산 처리 속도가 빠름 (사용 권장함)
value = 100
print('value : ', value)

# 10 증가 : value = value + 10 보다 빠름
value += 10
print('value : ', value)

# 5 감소 : value = value - 5
value -= 5
print('value : ', value)

# 2배 증가 : value = value * 2
value *= 2
print('value : ', value)

# 2배 감소 : value = value / 2
# value /= 2   # 나누기한 몫만 리턴, 결과형은 실수형(float) : 105.0
value //= 2    # 나누기한 몫만 리턴, 결과형은 정수형(int) : 105
print('value : ', value)

# 제곱연산 : **
value **= 2
print('value : ', value)

# 파이썬 코드 문장은 한 줄에 작성하는 것이 원칙임
# 문장이 길어서 한 줄에 작성이 불편할 경우에는 여러 줄로 나눌 수도 있음
# 단, 문장이 끊어지는 부분에 반드시 백슬러시(\)를 표시해야 함
print('파이썬은 인터프리터 언어이다.  스크립트 언어이기도 하다. 해석기로 한 줄씩 읽으면서 실행되는 방식의 언어이다.')

print('파이썬은 인터프리터 언어이다.' \
'  스크립트 언어이기도 하다. ' \
'해석기로 한 줄씩 읽으면서 실행되는 방식의 언어이다.')
