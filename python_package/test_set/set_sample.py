# path : ./test_set/set_sample.py

# 집합 (set) 자료형
# 교집합(&), 합집합(|), 차집합(-), 대칭차집합(^)
# 저장 방식은 중복 저장 불가, 순서 없음 (인덱싱 못 함, 순번 index 없음)

# set 정의 방법 1 : {} 중괄호 사용
def test1() :
    set1 = {1, 2, 3, 1, 2}
    print('set1 : ', set1)

# set 정의 방법 2 : set() 함수 사용
def test2():
    set1 = set()
    print('set1 : ', set1)

# set 에 문자열을 저장하는 경우
def test3():
    set1 = set('hello')
    print('set1 : ', set1, type(set1))

    set2 = set('python')
    print('set2 : ', set2, type(set2))

# set 에 list 저장 가능
# 리스트 자체는 값 순서대로 저장함 ==> set 이 저장 순서를 유지하게 하는 방법
def test4():
    set1 = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
    print('set1 : ', set1, type(set1))
    set2 = set([4, 5, 6, 7, 8, 9, 10])
    print('set2 : ', set2, type(set2))

    # set 자료형은 집합 연산이 가능. 합집합, 교집합, 차집합, 대칭차집합
    # 교(곱)집합                                        : & 연산자 또는 intersection() 메서드 사용
    print('set1 & set2 : ', set1 & set2)
    print('intersection : ', set1.intersection(set2))
    # 합집합                                            : | 연산자 또는 union() 메서드 사용
    print('set1 | set2 : ', set1 | set2)
    print('union : ', set1.union(set2))
    # 차집합                                            : - 연산자 또는 difference() 메서드 사용
    print('set1 - set2 : ', set1 - set2)
    print('difference : ', set1.difference(set2))
    # 대칭차집합                                        : ^ 연산자 또는 symmetric_difference() 메서드 사용
    print('set1 ^ set2 : ', set1 ^ set2)
    print('symmetric_difference : ', set1.symmetric_difference(set2))

    # 값 추가, 삭제
    # 값 하나 추가 : add() 메서드 사용
    set1.add(99)
    print('set1 에 add 한 결과 : ', set1)
    # 값 여러 개 추가 : update() 메서드 사용
    set1.update([88, 777, 66, 83])
    print('set1 에 update 한 결과 : ', set1)
    # 값 하나 삭제 : remove() 메서드 사용
    set1.remove(777)
    print('set1 에 remove 한 결과 : ', set1)
    # 값 여러 개 삭제 : difference_update() 메서드 사용
    set1.difference_update([88, 66])
    print('set1 에 difference_update 한 결과 : ', set1)

def test5() :
    # list 의 값 중복을 제거할 때 set() 이용 가능
    lst = [1,1,1,1,1,2,2,2,3,3,3,33,4,4,4,44,4,5,6,6,7,7,8,8,9,9,9]
    set1 = set(lst)
    print('중복 제거 후 set : ', set1)

if __name__ == '__main__' :
    test1()
    test2()
    test3()
    test4()
    test5()
