# path : loop\\while_mission.py
# module : loop.while_mission

import sys
sys.path.append('..')
from exception.user_exception import InvalidScoreException, InvalidIndexException

sungjuk_list = [[12, '홍길동', 98], [15, '김유신', 87], [23, '황지니', 45]]

def sungjuk_process():
    prompt = '''
            *** 원하는 메뉴 번호를 선택하세요. ***
            1. 추가
            2. 삭제
            3. 출력
            4. 끝내기
        '''
    loop_sw = True
    
    while loop_sw:
        print(prompt)
        key = str(input("select menu: "))
        try:
            match key:
                case '1':
                    add()
                case '2':
                    delete()
                case '3':
                    print_sungjuk()
                case '4':
                    loop_sw = False
        except (InvalidScoreException, InvalidIndexException, ValueError) as e:
            print(f"[오류] {e}")

    print("성적관리 프로그램이 종료되었습니다.")
    return


def add():
    sno = int(input("번호 : "))
    sname = str(input("이름 : "))
    try:
        score = int(input("점수 : "))
    except ValueError:
        raise InvalidScoreException()
    if not (0 <= score <= 100):
        raise InvalidScoreException()

    global sungjuk_list
    sungjuk_list.append([sno, sname, score])
    print("새로운 학생정보가 추가되었습니다.")
    
    return

def delete():
    global sungjuk_list

    lst_len = len(sungjuk_list)

    print(f"현재 저장된 아이템의 갯수는 {lst_len}개 입니다.")
    
    try:
        del_idx = int(input("제거할 아이템의 순번 : "))
    except ValueError:
        raise InvalidIndexException(-1, lst_len)

    if 0 <= del_idx < lst_len:
        del sungjuk_list[del_idx]
        print("{}번 위치의 아이템이 제거되었습니다.\n현재 저장된 아이템의 갯수는 {}개 입니다.".format(del_idx, len(sungjuk_list)))
    else:
        raise InvalidIndexException(del_idx, lst_len)
        
    return

def print_sungjuk():
    global sungjuk_list
    
    lst_len = len(sungjuk_list)

    # for idx in range(lst_len): print(f"{idx} : {sungjuk_list[idx]}")
    for idx, item in enumerate(sungjuk_list): print(f"{idx} : {item}")

    return

'''
# path : loop\\while_mission.py
# module : loop.while_mission

함수명 : sungjuk_process()
prompt 변수를 while 문으로 반복해서 출력하면서, 입력되는 번호에 따라
sungjuk_list 의 아이템을 추가하거나 삭제하거나 출력되게 작성하시오.

sungjuk_list = [[12, '홍길동', 98], [15, '김유신', 87], [23, '황지니', 45]]
prompt =
            *** 원하는 메뉴 번호를 선택하세요. ***
            1. 추가
            2. 삭제
            3. 출력
            4. 끝내기
		
1 입력 : 리스트에 아이템 값들을 입력받아 추가함
  번호 : 24 (sno : int)
  이름 : 이순신 (sname : str)
  점수 : 100 (score : int)
  ==> 리스트에 추가 처리함    ==> 새로운 학생정보가 추가되었습니다.  출력함
2 입력 : 리스트의 인덱스 위치의 아이템 제거함
  현재 저장된 아이템의 갯수는 3개 입니다.  출력함
  제거할 아이템의 순번 : 3    ==> 입력받은 인덱스 위치의 아이템 제거함
  ==> 3번 위치의 아이템이 제거되었습니다.  출력함   ==> 현재 저장된 아이템의 갯수는 2개 입니다.  출력함
  ==> 잘못된 인덱스 입력시 :   '순번이 잘못 입력되었습니다. 확인하고 다시 입력하세요.' 출력함
3 입력 : 저장된 리스트 정보 아이템별로 출력함
  0 : [12, '홍길동', 98]
  1 : [15, '김유신', 87]
  2 : .......
4 입력 : while 반복 종료함
  성적관리 프로그램이 종료되었습니다.  출력함

'''