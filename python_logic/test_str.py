# test_str.py
# 파이썬에서 문자열 다루기

# 파이썬에서 문자열(str)은 시퀀스(sequence : 순차나열자료형)로 취급됨
# 순차자료형은 나열된 값의 순번(인덱스, index)이 매겨짐, 0부터 시작됨
# 동일한 시퀀스 자료형인 리스트(list), 튜플(tuple), 배열(array), 시리즈(Series) 들도 동일하게 적용됨

# 문자 선택 연산자 (인덱싱) : 문자열변수[인덱스순번]
ss = 'Hi,-python'

print('첫번째 글자 : ', ss[0])  # H
print('다섯번째 글자 (인덱스 4) : ', ss[4])   # p
print('뒤에서 부터 첫번째 글자 (마지막 글자) : ', ss[-1])   # n

# 문자열 범위 선택 연산자 (슬라이싱) : 문자열값 부분 추출시 사용
# 문자열변수[시작인덱스:끝인덱스:간격]
# 끝인덱스는 끝인덱스 - 1 위치까지 추출됨
# 간격은 생략시 기본값이 1임
# 시작인덱스 생략시 기본값은 0임
# 끝인덱스 생략시 기본값은 마지막인덱스 + 1임 => ss[:] 문자열 전체를 의미함

print(ss[0:3])  # 0, 1, 2 => 3글자 추출 : Hi,
print(ss[0:5:2])  # 0, 2, 4 => 3글자 추출 : H,p

# 슬라이싱을 이용해서 문자열을 역순으로 정렬할 수도 있음
print(ss)
print(ss[::-1])  # 문자열 전체임, 간격이 음수이면 뒤에서부터 추출임

# 슬라이싱과 연결 연산 (+)을 혼합해서 사용 가능함
n1 = 'abcdef'
n2 = '12345'
n3 = n1[0:3] + n2[1:]
print(n3)  # abc2345

# 문자열 반복 연산자 : * 반복할 횟수
print('Hello!' * 3)

# 문자 처리 내장함수
# upper() : 영문자일 때 대문자로 변환
# lower() : 영문자일 때 소문자롤 변환
tt = 'apple'
print(tt)
print(id(tt))  # tt 가 참조하는 문자열의 메모리 위치 (주소 번지로 이해하면 됨)

# 파이썬에서도 기록된 문자열값은 변경할 수 없음 (immutable)
# tt[1] = 'b'  # TypeError: 'str' object does not support item assignment

tt = 'banana'
print(tt)
print(id(tt))

print(tt.upper())  # tt가 참조하는 문자열을 cpu가 읽어가서 대문자로 변환하고, 메모리에 새로 기록함
print(id(tt.upper()))  # 주소 확인
print(tt)  # 원래 문자열 확인

tt2 = 'ORANGE'
print(tt2.lower())

# swapcase(), capitalize()
tt3 = 'tEst stR pyTHOn'

print(tt3)
print(tt3.swapcase())  # 소문자는대문자로, 대문자는 소문자로 변환
print(tt3.capitalize())  # 문장의 첫글자만 대문자로, 나머지는 소문자로 변환
print(tt3.title())  # 각 단어의 첫글자를 대문자로 변환

# strip(), lstrip(), rstrip()
tt4 = '       test str values    '

print('|', tt4, '|', sep='')   # sep='' 출력값들 사이의 공백 구분자 없앴음
print('|', tt4.strip(), '|', sep='')  # 문자열 앞 뒤 공백 제거함
print('|', tt4.lstrip(), '|', sep='')  # 문자열 앞(왼쪽) 공백 제거함
print('|', tt4.rstrip(), '|', sep='')  # 문자열 뒤(오른쪽) 공잭 제거함

# split(), splitlines()
tt5 = 'abc-def-ghi-f'

print(tt5)
print(tt5.split('-'))  # split('구분문자') : 구분문자를 기준으로 문자값들을 분리함
# 여러 개의 분리된 문자값들을 리스트(list, []로 표현)로 반환함

# splitlines() : 줄(line) 단위로 분리해서 (한 줄씩 분리함) 리스트로 반환함
tt6 = '''python
java
c++
javascript
'''

print(tt6)
print(tt6.splitlines())

# index(), find() : 글자 위치(인덱스, 순번) 조회
print(tt5.index('e'))  # 문자열 안에 있는 'e'의 인덱스 조회
# 없는 문자 조회하면 에러남
# print(tt5.index('k'))  # ValueError: substring not found
print(tt5.find('k'))  # 없는 문자 조회시 -1 리턴함

# 이 외의 문자 관련 함수들을 확인하고자 한다면
print(len(dir(str)))
print(dir(str))
