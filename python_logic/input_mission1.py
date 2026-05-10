# input_mission1.py
# 입력 연습 1 : 
'''
신상 정보를 입력받아, 각 변수에 저장하시오. 변수명은 임의대로 지정함
이름(str), 나이(int), 성별(str, 남|여 로 입력), 키(float), 몸무게(float)
각 변수의 값을 아래의 형식으로 출력하는 코드를 작성하시오. 3가지 방식 모두 사용해 봄
홍길동은 27세 남자이고, 키는 178.5cm 몸무게는 72.0kg 입니다.
'''
name = input('이름 : ')
age = int(input('나이 : '))
gender = input('성별 [남/여] : ')
height = float(input('키 : '))
weight = float(input('몸무게 : '))

print(name, '은', age, '세', gender, '자이고, 키는', height, 'cm 몸무게는 ', weight, 'kg 입니다.')

# f'str' 이용한 출력문
print(f'{name}은 {age}세 {gender}자이고, 키는 {height} cm 몸무게는 {weight} kg 입니다.')

# format() 함수를 이용한 출력문
print('{}은 {}세 {}자이고, 키는 {:.1f} cm 몸무게는 {:.1f} kg 입니다.'.format(name, age, gender, height, weight))

# format() 함수와 순번을 적용한 출력문
print('{1}은 {0}세 {2}자이고, 키는 {3:.1f} cm 몸무게는 {4:.1f} kg 입니다.'.format(age, name, gender, height, weight))
