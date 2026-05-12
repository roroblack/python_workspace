# input_mission2.py
# 입력 연습2
'''
키보드로 값을 입력받아 요구조건대로 처리하고 출력되게 코드를 작성하시오.
기본값을 가진 변수 생성 할당해 둠 :
    total_point = 12500
입력 내용 :
    고객 이름 : 황지니 (custom_name : str)
    결재 금액 : 3000000 (price : int)
처리 내용 :
    결재금액의 5 % 를 포인트(point : float)로 처리
    계산된 포인트를 누적포인트(total_point)에 증가 연산 처리함
출력 내용 :
    황지니 고객님의 사용금액은 3000000 원, 발생 포인트는 15000
    현재 이용하실 수 있는 누적포인트는 162500 점입니다.
'''
total_point = 12500

custom_name = input("고객 이름 : ")
price = int(input("결제 금액 : "))

point = price * 0.05  # int * float ==> float 으로 자동으로 형변환됨
total_point += point

# 기본 출력
print(custom_name, " 고객님의 사용금액은 ", price, " 원, 발생 포인트는 ", int(point))
print("현재 이용하실 수 있는 누적포인트는 ", int(total_point), " 점입니다.")

# format() 사용
print('{} 고객님의 사용금액은 {} 원, 발생 포인트는 {}'.format(custom_name, price, int(point)))
print("현재 이용하실 수 있는 누적포인트는 {} 점 입니다.".format(int(total_point)))

# f-string 포매팅 사용 : print(f'출력문장 {변수명} 출력문장')
print(f'{custom_name} 고객님의 사용금액은 {price} 원, 발생 포인트는 {int(point)}')
print(f'현재 이용하실 수 있는 누적포인트는 {int(total_point)} 점 입니다.')
