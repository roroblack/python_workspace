# file path : test_dict\\dict_sample.py
# module    : test_dict.dict_sample

# 사전(dict) 자료형
# 자바의 Map, C++의 unordered_map 과 같은 자료구조로 키(key)와 값(value)으로 이루어진 자료형
# 사전은 중괄호({})로 표현하며, 키와 값은 콜론(:)으로 구분하고, 각 키-값 쌍은 쉼표(,)로 구분함
# 예시 : my_dict = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}

# dict 에서 key 는 변경되지 않는 값이어야함 (키는 지정하면 변경 불가)
# dict 에서 저장하는 value 는 데이터 제한 없음
# json, xml 로 변환할 때 많이 사용

def test_dict1():
    # dict 정의 방법 1 : dict() 함수 사용
    dct1 = dict({'name': 'aman', 'age': 33, 'city': 'seoul'})
    print(dct1, type(dct1))

    # dict 정의 방법 2 : 중괄호({}) 사용
    dct2 = {'name': 'Alice', 'age': 30, 'city': 'New York'}
    print(dct2, type(dct2))

    #---------------------------------------------------------

    # list 나 tuple 처럼 인덱스를 사용할 수 없음 (인덱스 없음)
    # key 를 이용해서 값 변경, 조회, 추가 가능 ==> 사전변수[키]
    # dict 의 저장 방식 : {키1: 값1, 키2: 값2, ...} 식으로 키, 값 쌍으로 저장함
    return

#------------------------------------------------

def test_dict2():
    dict1 = {'a':1, 'b':2, 'c':3}
    print(dict1, type(dict1))

    dict2 = {1:'python', 'a2':[1,2,3], (1, 2):345}
    print(dict2, type(dict2))

    # 값 변경 : 사전변수[존재하는 키] = 바꿀값
    # 변경시에는 저장되어 있는 키만 사용해야 함
    dict2['a'] = 105
    print(dict2, type(dict2))

    # 아이템 추가 : 사전변수[없는키] = 값
    # 저장되어 있지 않은 키를 사용함
    dict2[3] = [11, 22, 33]
    print(dict2, type(dict2))

    # 값 조회 : 사전변수[키]
    # 주의 : 없는 키로 조회시 키 KeyError 발생함
    # print(dict2['c']) # 'c' 는 없는 키라 KeyError 발생
    print(dict2['a'])
    return


#--------------------------------------------------

def dict_test_func():
    'dict 내장함수 활용' # 함수 설명은 함수 바로 밑에 '' 이렇게 작성

    # 아래 dict1 처럼 세로로 생성도 가능
    dict1 = {
        'a':10,
        'b':25,
        'c':77
    }
    print(dict1, type(dict1))

    # 키에 대한 리스트 만들기 : keys() 함수 사용
    print('dict1 의 키 목록: ', dict1.keys()) # dict1 의 키 목록 출력

    # 값에 대한 리스트 만들기 : values() 함수 사용
    print('dict1 의 값 목록: ', dict1.values()) # dict1 의 값 목록 출력

    # (키-값) 쌍 == (item) 에 대한 리스트 만들기 : items() 함수 사용
    print('dict1 의 키-값 쌍 목록: ', dict1.items()) # dict1 의 키-값 쌍 목록 출력


    # 사전과 사전을 합치기 : update() 함수 사용
    # 사전1.update(사전2) ==> 사전1 을 변경함
    # 사전1 과 사전2에 동일한 키가 있을 경우에는, 사전 1의 해당 키의 값이 사전2의 값으로 변경됨
    dict2 = {'name':'갤럭시', 'price': 999, 'tax': 0.1}
    dict3 = {'content':'스마트폰', 'price': 899, 'maker':'삼성', 'ids': [1,2,3]}
    print('dict2: ', dict2)
    print('dict3: ', dict3)

    dict2.update(dict3) # dict2 에 dict3 의 키-값 쌍을 추가함
    print('dict2 에 dict3 의 키-값 쌍 추가 후 dict2: ', dict2) # dict2 에 dict3 의 키-값 쌍이 추가된 dict2 출력


    # pop(key) 함수 : 해당 키에 대한 아이템을 꺼내며 제거함
    tax = dict2.pop('tax') # dict2 에서 'tax' 키에 대한 아이템을 꺼내며 제거함
    print('dict2 에서 tax 키 제거 후 dict2: ', dict2)
    print('꺼낸 tax 값: ', tax)


    # clear() 함수 : dict 의 모든 아이템 제거
    dict1.clear() # dict1 의 모든 아이템 제거
    print('dict1 의 모든 아이템 제거 후 dict1: ', dict1) # dict1 의 모든 아이템 제거된 dict1 출력


    # copy() 함수 : dict 의 얕은 복사본을 만듦
    dict4 = dict3.copy() # 새로운 객체를 만들지만 얕은 복사
    print('dict3: ', dict3, id(dict3))
    print('dict4: ', dict4, id(dict4))

    dict5 = dict3 # dict3 의 얕은 복사본을 dict5 에 저장
    print('dict3: ', dict3, id(dict3))  # dict3 의 id 출력
    print('dict5: ', dict5, id(dict5))  # dict5 의 id 출력 (dict3 와 dict5 는 같은 객체를 참조하므로 id 가 같음)

    # copy() 가 불변 자료형 제외하면 얕은 복사임을 테스트
    dict4['price'] = 799 # dict4 의 'price' 키의 값을 799 로 변경
    print('dict3: ', dict3, id(dict3))
    print('dict4: ', dict4, id(dict4))
    dict4['ids'].append(4) # dict4 의 'ids' 키의 값인 리스트에 4 추가
    print('dict3: ', dict3, id(dict3)) # dict3 의 'ids' 키의 값인 리스트에도 4 가 추가됨 (copy() 는 얕은 복사이므로)
    print('dict4: ', dict4, id(dict4))



    # in 연산자 : dict 에 키가 존재하는지 여부를 확인할 때 사용함
    print('price 있는가?', 'price' in dict2) # dict2 에 'price' 키가 존재하는지 여부 출력 (True)
    print('tax 있는가?', 'tax' in dict2)   # dict2 에 'tax' 키가 존재하는지 여부 출력 (False)

    # 값 존재여부 ==> 값 in 사전변수.values() : dict 의 값 목록에서 값이 존재하는지 여부를 확인할 때 사용함
    print('갤럭시 있는가?', '갤럭시' in dict2.values()) # dict2 의 값 목록에서 '갤럭시' 가 존재하는지 여부 출력 (True)
    print('0.1 있는가?', 0.1 in dict2.values()) # dict2 의 값 목록에서 0.1 이 존재하는지 여부 출력 (False)

    # 키로 값 조회 : 사전변수[키] 또는 사전변수.get(키) 사용
    print('price 값 조회: ', dict2['price']) # dict2 의 'price' 키에 대한 값 조회
    print('price 값 조회: ', dict2.get('price')) # dict2 의 'price' 키에 대한 값 조회 (get() 함수 사용)
    # print('없는키 조회: ', dict2['없는키']) # 없는 키 조회시 KeyError 발생
    print('없는 키 조회: ', dict2.get('없는키', '기본값')) # 없는 키 조회시 기본값 반환
    print('tax :', dict3.get('tax')) # Nono 반환

    # del 사전변수[키] : 해당 키에 대한 아이템을 제거함
    del dict2['maker'] # dict2 에서 'maker' 키에 대한 아이템 제거
    print('dict2 에서 maker 키 제거 후 dict2: ', dict2)
    

    return



#--------------------------------------------------

if __name__ == "__main__":
    print("start test_dict_sample.py")

    print("---test_dict1()---")
    test_dict1()

    print("---test_dict2()---")
    test_dict2()

    print("---dict_test_func()---")
    dict_test_func()

    print("---end---")