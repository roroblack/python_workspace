# path : main_mission.py
# module : main_mission

import loop.while_mission as wm
import fileio.fileio_mission as fm

prompt = '''
	*** 파이썬 과제 1 ***
	1. while 실습문제
	2. fileio 실습문제
	9. 과제 실행 테스트 끝내기
 '''


def menu():
    loop_sw = True
    
    while loop_sw:

        print(prompt)
        key = str(input("select menu: "))

        match key:
            case '1':
                wm.sungjuk_process()
            case '2':
                fm.emp_process()
            case '9':
                loop_sw = False
            

    return key



if __name__ == "__main__":
    # pass
    # print("---start---")
    menu()
    # print("---end---")
    