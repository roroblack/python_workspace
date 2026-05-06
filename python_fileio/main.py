#main.py
# 프로젝트 (애플리케이션 application) 의 진입점 (entry point) 이 되는 파일
# 프로젝트를 실행하는 스크립트
# CLI (Command Line Interface) 환경에서 실행되는 스크립트       : 터미널 글자
# GUI (Graphical User Interface) 환경에서 실행되는 스크립트     : 윈도우 창
# 1 바이트 문자 인코딩 방식 : ASCII (영문자, 숫자, 특수문자)
# 2 바이트 문자 인코딩 방식 : UTF-8 (영문자, 숫자, 특수문자, 한글 등 모든 문자)

from unittest import case

import fileio_sample.fileio_module  as fm
import fileio_sample.fileio_module2 as fm2
import loop.while_sample            as wl

loop_sw = True

def menu():
    global loop_sw
    menu_prompt = '''
              ---menu---
              1. 파일 저장 테스트 1 실행
              2. while 반복문 사용 테스트 1
              3. 파일 읽기 테스트 실행
              4. while 반복문 사용 테스트 2 : 문자 유니코드 입력 & 출력
              5. 파일 저장 테스트 2 실행
              6. 파일 이어쓰기 테스트 실행
              7. os 모듈의 함수 확인 1
              8. 파일 읽기 테스트 2 : 한 줄씩 저장
              9. 파일 읽기 테스트 3 : 여러 줄 저장
              10. 리스트와 튜플과 딕셔너리를 파일에 저장하기
              11. 파일에  이진데이터 저장하기
              12. 파일에서 이진데이터 읽어오기
              0. 프로그램 종료
              '''

    while loop_sw:

        print(menu_prompt)
        key = str(input("select menu: "))

        match key:
            case '1':
                print("run test_fwrite()")
                fm.test_fwrite()

            case '2':
                print("run test_while()")
                wl.test_while()

            case '3':
                print("run test_fread()")
                fm.test_fread()

            case '4':
                print("run print_unicode()")
                wl.print_unicode()

            case '5':
                print("run test_fwrite2()")
                fm.test_fwrite2()

            case '6':
                print("run test_append()")
                fm.test_append()

            case '7':
                print("run test_osmodule()")
                fm.test_osmodule()

            case '8':
                print("run test_fread2()")
                fm.test_fread2()

            case '9':
                print("run test_fread3()")
                fm.test_fread3()

            case '10':
                print("run test_writelines()")  
                fm.test_writelines()

            case '11':
                print("run test_binary_fileio()")
                fm2.test_binary_fileio()

            case '12':
                print("run test_binary_fileio2()")
                fm2.test_binary_fileio2()

            case '0':
                print("---end_menu---")
                loop_sw = False
                break

            case _:
                print("잘못된 메뉴 선택입니다. 다시 선택해주세요.")
        
''' 
        if key == '1':
            print("run test_fwrite()")
            fm.test_fwrite()

        elif key == '2':
            print("run test_fread()")
            # fm.test_fread()

        elif key == '0':
            print("---end_menu---")
            loop_sw = False
            break
        
        else:
            print("잘못된 메뉴 선택입니다. 다시 선택해주세요.")
'''

        

if __name__ == "__main__": # 메인이 시작 된 건가 확인하는 부분
    # pass # 아직 내용 없음을 알림
    print("Hello, World!")
    print("start  of the program")

    loop_sw = True
    
    menu() # 메뉴 함수 실행
    
    print("end of the program")
