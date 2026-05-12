# using_input.py
# 파이썬에서 실행시 키보드로 값 입력받기 : input() 함수 사용 테스트
# 입력값 기록할 변수 = input('입력을 위한 메세지 문장')

# 입력을 위한 메세지 없이 실행 테스트
# num = input()
# num = input('숫자를 입력하세요 : ')
# print('num : ', num, type(num))

# 파이썬의 input() 함수로 입력 들어오는 값은 모두 문자형(str) 이다.
# print(num + 100)  # TypeError: can only concatenate str (not "int") to str
# 숫자와 문자는 계산할 수 없음

# 입력된 숫자형문자를 숫자형으로 변환하고자 한다면 형변환함수 사용함
# 정수로 변환 : int('정수형문자')
# 실수로 변환 : float('실수형문자')
# inum = int(num)
# print('inum : ', inum, type(inum))
# print('더하기 : ', inum + 100)

# 입력 예 : 
# 정수 2개를 입력받아서, 사칙연산 결과 출력 처리
first = int(input('첫번째 정수 : '))
second = int(input('두번째 정수 : '))

# 파이썬에서 제공하는 기본 출력 함수 : print() 사용 연습
# 사용 1 : 출력 내용을 , 로 구분해서 나열
print('first : ', first, ', second : ', second)

# 사용 2 : f'str' (format string) 사용 => 변수를 적용하려면 : f'출력문장 {변수명}'
print(f'더하기 결과 : {first} + {second} = {first + second}')

# 사용 3 : format() 함수 이용 => 주의 : 순서와 갯수가 반드시 일치해야 함
print('빼기 결과 : {} - {} = {}'.format(first, second, first - second))

# 사용 4 : format() 함수와 순번(index)을 이용 => 실수형 값의 소숫점 아래 자릿수도 지정할 수 있음 {:.2f}
print('나누기한 몫 : {2} / {0} = {1:.2f}'.format(second, first / second, first))

print(f'{first} ** 3 = {first ** 3}')

