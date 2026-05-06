# file path : loop\\while_sample.py
# module    : loop.while_sample
# while 문 사용 테스트 스크립트

'''
while 반복에 대한 조건식: (콜론 주의)
  반복 실행할 구문들 (들여쓰기 주의)
    
반복에 대한 조건식은 무한 루프가 되지 않게 작성할 것
만약, 조건식 대신에 True를 사용한다면, 반드시 while 문 안에서 종료에 대한 break 문을 사용하여 반복문을 빠져나올 수 있도록 작성할 것

while True:
    반복 실행할 구문들 (들여쓰기 주의)
    if 종료 조건:
        break
'''



def safe_ord(value):
    try:
        return ord(value)
    except TypeError:
        return None  # 에러 대신 None을 반환하도록 설정

def test_while():
    num = 5
    while num > 0:
        print(f"num: {num}")
        num -= 1 # num = num - 1
    
    # 위 while 의 반복문 코드는 아래의 for 코드의 반복문과 같은 기능을 함
    num = 5
    for num in range(5, 0, -1):
        print(f"num: {num}")
    return



# 문자 하나를 입력 받아서, 그 문자의 유니코드를 출력 처리를 반복 실행되게 함
# 단, 입력한 문자가 '0' 이면 반복문을 빠져나오도록 함
def print_unicode():
    ch = '1'
    uni = '\0'

    while ch != '0':
        ch = input("문자 하나 입력 (종료하려면 '0' 입력): ") # 새 문자 입력 받음

        if ch != '0':
            uni = safe_ord(ch)
            print(f"입력한 문자: {ch}, 유니코드: {uni}")



