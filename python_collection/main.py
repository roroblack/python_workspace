# main.py
# 파이썬의 군집(collection) 자료형 사용 테스트와 함수 만들어 사용하기 테스트용 스크립트
# 별도로 작성된 함수들을 가져다가 실행하는 목적의 스크립트임
# 실행용임 => 반드시 main (프로그램의 start 스위치임)이 있어야 함

# 별도로 작성된 파일(모듈) 안의 함수를 사용하려면, import 선언을 해야 함
# import 패키지명.하위패키지명.모듈명
# import my_collections.test_list.list_sample

# import 하는 모듈명이 길면 줄임말을 선언할 수 있음
# import 패키지명.하위패키지명.모듈명 as 줄임말
# import my_collections.test_list.list_sample as ls

'''
# 사용할 모듈 안의 원하는 대상만 임포트할 수도 있음
# from 패키지명.모듈명 import 대상이름 [as 대상에 대한 줄임말]
from my_collections.test_list.list_sample import make_list1, make_list2, list_indexing, list_slicing, change_element

if __name__ == '__main__':
    # 파이썬의 main 시그니처임
    # 프로그램이 시작되면 실행할 구문 또는 함수들을 실행하고자 하는 순서대로 작성해 나감
    print('프로그램 시작됨. =============================')
    # print('필요한 기능 동작')
    
    # import 한 모듈 안의 함수를 사용하려면
    # 패키지명.모듈명.함수명() 형식으로 작성해야 함
    # my_collections.test_list.list_sample.make_list1()  # 원하는 함수 실행(호출, call)시 import 한 모듈명.함수명() 으로 실행함
    # ls.make_list1()   # 모듈 줄임말.함수명() 으로 사용함

    # make_list1()  # 원하는 함수만 import 선언하면 함수명() 로 실행함
    # make_list2()
    # list_indexing()
    # list_slicing()
    change_element()

    print('프로그램 종료 : main 이 끝남 =====================')
'''

import my_collections.test_list.list_sample2 as ls2
import my_collections.test_list.list_mission1 as lm1
import my_collections.test_list.list_mission2 as lm2
import my_collections.test_tuple.tuple_sample as ts

if __name__ == '__main__':
    print('program start -------------------------------------')

    # 임포트한 모듈이 가진 전역변수 사용할 수 있음
    print(ls2.lst)
    # ls2.list_append()
    # ls2.list_remove()
    # ls2.list_insert()
    # ls2.list_pop()
    # ls2.list_extend()
    # ls2.list_reverse()
    # ls2.list_sort()
    # ls2.list_count()

    # lm1.practice()
    # lm1.practice_1()
    # lm1.practice_2()

    # ts.make_tuple()
    # ts.tuple_indexing()
    # ts.tuple_caution()
    # 튜플이 반환되는 경우 (리턴시 값을 가지고 온다면)
    # a, b = ts.tuple_caution()
    # print(f'a : {a}, b : {b}, type : {type(a)}, {type(b)}')

    # result = ts.tuple_caution()
    # print(f'result : {result}, type : {type(result)}')

    # ts.tuple_builtin()

    lm2.practice()

    print('program exit --------------------------------------')