# path : my_collections\test_list\list_sample2.py
# module : my_collections.test_list.list_sample2
# 함수 만들기를 이용한 리스트 자료형 사용 테스트 스크립트

# 리스트 자료형 특징 3 : 리스트를 다루는 함수(메소드)들이 제공됨
# 리스트변수.함수명(전달인자)
# append() : 뒤에 추가 (저장 데이터 갯수가 증가함)
# insert() : 원하는 위치에 추가  (저장 데이터 갯수가 증가함, 해당 위치의 기존 데이터는 뒤로 이동됨)
# remove() : 삭제
# pop() : 꺼내면서(반환됨) 리스트에 제거
# reverse() : 리스트 안의 데이터 순서를 반대로 뒤집음
# clear() : 리스트 비움 (저장 데이터 모두 삭제됨)

# 함수 밖에서 선언한 변수 => 전역변수 (Global Variable)
# 이 파일 안의 모든 함수들이 사용할 수 있음
# 다른 파일에서 사용할 수도 있음 => 단, 파일(모듈)을 import 선언하면 됨, 모듈명.전역변수명
# 전역변수는 선언한 위치 아래쪽에서 사용할 수 있음
lst = [1, 3.5, 'list', True, 20, ['a', 'b', 'c']]
lst_1 = [1.2, 1.4, 1.2, 1.3]

# append() : 리스트 뒤로 추가, 마지막 인덱스가 증가됨
# 리스트변수.append(추가할 앨리먼트)
def list_append():
    print(f'before : {lst}')
    print(f'length : {len(lst)}')

    lst.append(456)

    print(f'after : {lst}')
    print(f'after : {len(lst)}')

    return

# remove() : 지정한 앨리먼트를 제거함, 갯수 줄어듦
# 리스트변수.remove(제거할앨리먼트)
def list_remove():
    lst.remove(20)
    print(f'after : {lst}')
    print(f'after : {len(lst)}')

    # 제거할 앨리먼트가 여러 개인 경우
    print(f'before lst_1 : {lst_1}')
    print(f'before length : {len(lst_1)}')

    lst_1.remove(1.2)  # 앞에서부터 검색해서 첫번째로 만나는 대상을 삭제함

    print(f'after lst_1 : {lst_1}')
    print(f'after length : {len(lst_1)}')

    return

# insert() : 리스트 안의 원하는 위치에 추가
# 리스트변수.insert(위치인덱스, 추가할 앨리먼트)
def list_insert():
    lst.insert(1, '추가 문자열')
    print(f'after : {lst}')
    print(f'after : {len(lst)}')
    return

# pop() : 인덱스 위치의 값을 꺼냄 (제거)
# [값 받을 변수 =] 리스트변수.pop() <= 마지막 위치의 값을 빼냄 (제거)
# [값 받을 변수 =] 리스트변수.pop(index) <= 지정한 index 위치의 값을 빼냄 (제거)
def list_pop():
    save_data = lst.pop()
    print(f'after : {lst}')
    print(f'after : {len(lst)}')
    print(f'save_data : {save_data}')

    lst.pop(3)
    print(f'after : {lst}')
    print(f'after : {len(lst)}')
    return

# extend() : 기존 리스트 뒤쪽에 다른 리스트를 추가해서 리스트를 확장함
# 리스트변수.extend(추가할 리스트변수)
def list_extend():
    lst.extend(lst_1)
    print(f'after : {lst}')
    print(f'after : {len(lst)}')
    return

# reverse() : 리스트의 저장 순서를 반대로 뒤집기함
# 리스트변수.reverse()
def list_reverse():
    lst.reverse()
    print(f'after : {lst}')
    print(f'after : {len(lst)}')
    return

# sort() : 리스트의 저장 값들을 오름차순정렬 처리함
# 주의 : 한 가지 종류의 값들로만 저장되어 있을 때 사용할 수 있음
def list_sort():
    # lst.sort()  # TypeError: '<' not supported between instances of 'str' and 'float'
    
    lst_int = [6, 3, 9, 12, 2, 34, 1]
    print(f'before sort : {lst_int}')
    lst_int.sort()  # 기본 오름차순정렬임 (1234순, abcd순, 가나다라순)
    print(f'after sort : {lst_int}')
    lst_int.sort(reverse=True)   # 내림차순정렬, reverse=False 기본값으로 생략함
    print(f'after sort : {lst_int}')

    lst_str = ['orange', 'apple', 'melon', 'banana', 'kiwi']
    print(f'before sort : {lst_str}')
    lst_str.sort()  # 기본 오름차순정렬임 (1234순, abcd순, 가나다라순)
    print(f'after sort : {lst_str}')
    lst_str.sort(reverse=True)   # 내림차순정렬, reverse=False 기본값으로 생략함
    print(f'after sort : {lst_str}')

    lst_kr = ['파이썬', '데이터베이스', '웹크롤링', '데이터처리', '데이터분석', '초거대언어모델']
    print(f'before sort : {lst_kr}')
    lst_kr.sort()  # 기본 오름차순정렬임 (1234순, abcd순, 가나다라순)
    print(f'after sort : {lst_kr}')
    lst_kr.sort(reverse=True)   # 내림차순정렬, reverse=False 기본값으로 생략함
    print(f'after sort : {lst_kr}')

    return

# count() : 리스트에 저장된 같은 값의 갯수 조회
# 리스트변수.count(찾을값)
def list_count():
    print(f'lst : {lst}')
    print(f'lst 에 저장된 정수 1의 갯수 : {lst.count(1)}')
    return
