# path : my_collections\test_tuple\tuple_sample.py
# module : my_collections.test_tuple.tuple_sample

# 튜플(tuple) 자료형 : 리스트와 저장 방식은 같음
# 여러 종류의 값들을 순차적으로 저장하는 집합자료형임
# 리스트와 다른 점은 저장된 데이터 변경 불가능 => 상수 개념이 적용됨, 연산 속도가 빠름


def make_tuple():
    # 튜플 정의방법 1 : 소괄호 () 로 정의
    tp_1 = ()
    print(tp_1, type(tp_1))

    # 튜플 정의방법 2 : tuple() 함수 사용
    tp_2 = tuple()
    print(tp_2, type(tp_2))
    return

# 전역변수 ----------------------------
lst = [10, 20, 30]
tpl = (11, 22, 33)

# 튜플도 리스트와 동일하게 인덱싱, 슬라이싱 연산 가능함
def tuple_indexing():
    print(f'lst : {lst}, type : {type(lst)}')
    print(f'tpl : {tpl}, type : {type(tpl)}')

    print('0번째 앨리먼트 : ', lst[0], tpl[0])
    print('0번째부터 1번째까지의 데이터들 : ', lst[0:2], tpl[0:2])
    print('리스트 합치기 : ', lst + lst)
    print('튜플 합치기 : ', tpl + tpl)
    return

def tuple_caution():
    # 튜플과 리스트의 차이점 : 튜플의 값 변경 못 함
    print(f'lst : {lst}')
    lst[2] = 99
    print(f'lst : {lst}')  # 변경 확인됨

    # tpl[2] = 15  # TypeError: 'tuple' object does not support item assignment

    # 튜플 사용시 주의사항
    # 튜플 생성시 1개의 값만 가질 때는, 반드시 값 뒤에 콤마(,) 붙일 것
    tpl_1 = (1)
    print(f'tpl_1 : {tpl_1}, type : {type(tpl_1)}')   # tpl_1 : 1, type : <class 'int'>

    tpl_2 = (1,)
    print(f'tpl_2 : {tpl_2}, type : {type(tpl_2)}')   # tpl_2 : (1,), type : <class 'tuple'>

    # 튜플 생성시 저장 데이터가 1개일 때는 소괄호 생략해도 됨
    tpl_3 = 1,
    print(f'tpl_3 : {tpl_3}, type : {type(tpl_3)}') 

    # 참고 사항 : 하나의 변수에 소괄호 () 없이 여러 개의 값을 나열해서 대입하면 자동 튜플이 됨
    x = 1, 2, 3
    print(f'x : {x}, type : {type(x)}')

    # 참고 사항 : 함수에서 튜플을 리턴할 수 있음
    # return 원칙 : 값 1개만 함수 실행 맨마지막에 딱 한번 실행되어야 함
    # 반환값을 1개 이상 반환하고자 한다면, 튜플을 이용하면 됨

    # return (3, 5)   # 반환값 (return value)이 있는 함수가 됨
    return 4, 7

def tuple_builtin():
    # 튜플에 사용하는 내장함수
    # count() : 찾는 값의 갯수 조회
    # 튜플변수.count(찾는값)
    number_count = tpl.count(11)
    print(f'tpl 에 저장된 11의 갯수 : {number_count}')  # 1

    # index() : 찾는 값의 인덱스(순번) 조회
    # 튜플변수.index(찾는값) -> 찾는 값이 없으면 에러 발생함
    find_index = tpl.index(33)
    print(f'tpl 에 저장된 33의 순번 : {find_index}')  # 2

    # len(튜플변수) : 저장된 데이터 갯수 조회
    print(f'tpl 에 저장된 데이터 갯수 : {len(tpl)}')
    return

