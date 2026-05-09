# path : fileio\\fileio_mission.py
# module : fileio.fileio_misson

import sys
sys.path.append('..')
from exception.user_exception import EmpNotFoundException, InvalidSalaryException, EmpFileNotFoundException

prompt = '''
        *** 직원 정보 관리 서비스 ***
        1. 새 직원정보 추가
        2. 직원정보 삭제
        3. 전체 출력
        4. 파일에 저장
        5. 파일로 부터 직원정보 읽어오기
        9. 서비스 끝내기
'''

emp_list = {}

import pickle
import os

def emp_process():

    while True:
        print(prompt)
        key = input()
        try:
            match key : 
                case '1' :
                    emp_add()
                case '2' :
                    emp_del()
                case '3' :
                    emp_print()
                case '4' :
                    emp_fileout()
                case '5' :
                    emp_filein()
                case '9' :
                    break
        except (EmpNotFoundException, InvalidSalaryException, EmpFileNotFoundException) as e:
            print(f"[오류] {e}")

    print('직원 관리 프로그램을 종료합니다.')
    return

def emp_add() :
    empid = str(input("사번 : "))
    empname = str(input("이름 : "))
    empno = str(input("주민번호 : "))
    email = str(input("이메일 : "))
    phone = str(input("전화번호 : "))
    try:
        salary = int(input("급여 : "))
    except ValueError:
        raise InvalidSalaryException()
    job = str(input("직급 : "))
    dept = str(input("부서 : "))

    global emp_list
    emp_list[empid] = [empname, empno, email, phone, salary, job, dept]
    print(f"사번 '{empid}' 직원 정보가 추가되었습니다.")

    return

def emp_del() :
    global emp_list
    del_id = str(input("삭제할 사번 : "))
    if del_id not in emp_list:
        raise EmpNotFoundException(del_id)
    del emp_list[del_id]
    print(f"{del_id} 번 사번의 직원 정보가 삭제되었습니다.")
    return

def emp_print() :
    global emp_list
    for empid, emp_info in emp_list.items():
        print(f"{empid} : {emp_info}")
    return

def emp_fileout() :
    global emp_list
    f = open("employees.dat", 'wb')
    pickle.dump(emp_list, f)
    f.close()
    return

def emp_filein():
    global emp_list
    filename = "employees.dat"
    if not os.path.exists(filename):
        raise EmpFileNotFoundException(filename)
    with open(filename, 'rb') as f:
        emp_list = pickle.load(f)
    print("직원 정보를 파일로부터 불러왔습니다.")
    return


'''
# 파일입출력, 반복문, 리스트, 딕셔너리 사용 실습문제 요구사항

while 문을 사용해서 prompt 가 반복해서 출력되도록 함
입력된 번호에 따라서 emp_list 에 아이템 추가, 삭제, 출력 처리하도록 함

prompt = 
        *** 직원 정보 관리 서비스 ***
        1. 새 직원정보 추가
        2. 직원정보 삭제
        3. 전체 출력
        4. 파일에 저장
        5. 파일로 부터 직원정보 읽어오기
        9. 서비스 끝내기
        
		
1 이 입력되면 리스트에 추가할 아이템 정보를 키보드로 입력받아서 추가함
  사번 : 200 (empid : str)
  이름 : 홍길순 (empname : str)
  주민번호 : 851225-1234567 (empno : str)
  이메일 : hong77@test.com (email : str)
  전화번호 : 010-1234-5678 (phone : str)
  급여 : 3800000 (salary : int)
  직급 : 대리 (job : str)
  부서 : 개발부 (dept : str)
  => 사번은 키로 해서 딕셔너리에 직원정보를 리스트로 저장함
     사번 : [사번, 이름, 주민번호, 이메일, 전화번호, 급여, 직급, 부서]
2 입력시 :
    삭제할 사번 : 200
    => 딕셔너리에서 해당 사번의 아이템 제거함
    => '200 번 사번의 직원 정보가 삭제되었습니다.' 출력함
3 입력시 :
    딕셔너리의 각 아이템의 정보를 한줄씩 출력되게 함
    사번 : [리스트 정보]
    사번 : [리스트 정보]
    ....
4 입력시 :
    딕셔너리 상태 그대로 파일에 저장되도록 함
    저장할 파일명 : employees.dat
    ==> 'employees.dat 파일에 성공적으로 저장되었습니다.' 출력됨
5 입력시 :
    읽을 파일명 : employees.dat
    => 파일의 내용을 읽어서 딕셔너리(emp_dict)에 저장하고 출력되게 함
9 입력시 :
    while 문 끝내면서 프로그램 종료되게 함
    => 종료시 '직원 관리 프로그램을 종료합니다.' 출력함

함수명 : emp_process()
'''