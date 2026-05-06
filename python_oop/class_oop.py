# pass : ./class_oop.py
# 파이썬에서 객체 지향 프로그래밍(OOP) 적용
'''
객체지향 프로그래밍에서는 클래스 멤버 구성이 중요함
field(멤버 변수), method(멤버 함수), constructor(생성자), destructor(소멸자)

- oop 에서 사용되는 기술 (3대 특징) 도 적용해야 함
    1. 캡슐화   (encapsulation)     : 객체의 속성과 행동을 하나로 묶고, 외부에서 접근을 제한하는 것
    2. 상속     (inheritance)       : 기존 클래스에서 새로운 클래스를 만들어 기존 클래스의 속성과 행동을 재사용하는 것
    3. 다형성   (polymorphism)      : 동일한 인터페이스를 사용하여 서로 다른 데이터 타입의 객체를 처리할 수 있는 능력

'''

# oop 적용 기술 1 : 캡슐화 (encapsulation)
# 캡슐화 : 데이터 보호가 목적임. 필드에 접근 제한을 설정함
# 필드에 접근 제한자(access modifier) 설정
# private (비공개), protected (보호), public (공개)

# 파이썬에서는 접근 제한자가 명시적으로 존재하지 않지만, 관례적으로 다음과 같이 사용됨
# 클레스를 자료형(type)으로 만든 변수 == 레퍼런스 변수라고 함 : 클래스로 만들어진 객체의 주소를 가짐
# 사용 형태 : 레퍼런스.필드명 클래스명.필드명
# 래퍼런스.메소드명, 클래스명.메소드명()

# public    : 기본값 public          (예: name, age)
# protected : 이름 앞에 단일 밑줄(_)을 붙여서 표시    (예: _name, _age)   - 이는 해당 필드나 메서드가 클래스 내부에서 사용되어야 함을 나타냄
# private   : 이름 앞에 이중 밑줄(__)을 붙여서 표시   (예: __name, __age) - 클래스 밖에서 접근 x. 내부에서만 o
# 하지만, 이름 맹글링(name mangling)을 통해 private 에 접근 가능 (예: _ClassName__fieldName)

class PClass :
    # field (private)
    __num = 10

    # constructor 추가 : 매개변수 있는 생성자를 작성함
    # 파이썬에서 생성자 오버로딩 못함.
    # def __init__ (self) : pass  # self == this. 매개변수 없는 기본 생성자
    # def __init__ (self) : self.__num = 0 # 에러남 (pref = PClass() ) - TypeError: PClass() takes no arguments
    def __init__ (self, num) : self.__num = num 

    # method (public)
    def set_num (self, num) :
        self.__num = num

    def get_num (self) : return self.__num
#-------------------------------------------------------------------------

# 클래스 맴버 사용 : 레퍼런스변수 = 클래스명() 또는 래퍼런스 = 클래스명(전달값)
# pref = PClass() # 매개변수 없는 기본 생성자 자동 실행됨. 메모리에 객체 공간 할당하고 주소를 리턴함
# print("pref가 가진 주소 : ", id(pref)) # pref가 가진 주소 :  140432489441344
# print('인스턴스 안의 __num 값 : ', pref.get_num()) # 0

# 클래스 밖에서 필드 접근 확인
# # print('인스턴스 안의 __num 값 : ', pref.__num) # 접근 금지라 에러남 (AttributeError: 'PClass' object has no attribute '__num')
# print('인스턴스 안의 __num 값 : ', pref._PClass__num)

# 생성자 (constructor)
# 객체 인스턴스가 메모리에 할당 될 때 필드값 초기화가 목적인 함수
# 생성자가 없으면 내부에서 기본 생성자 (매개변수 없는) 자동으로 작동
# 직접 생성한다면 __init__ 로 작성해야 함
# 파이썬은 생성자 오버로딩 불가(overloading)
# 주로 매개변수 있는 생성자를 추가 작성함
pref2 = PClass(20)
print('pref2가 가진 주소 : ', id(pref2)) # pref2가 가진 주소 :  140432489441344
print('인스턴스 안의 __num 값 : ', pref2.get_num())

# 소멸자 (destructor)
# 객체 인스턴스가 메모리에서 해제될 때 자동으로 호출되는 함수
# 파이썬에서는 __del__ 메서드로 소멸자를 정의할 수 있지만, 일반적으로 명시적으로 소멸자를 작성하는 경우는 드뭄
# 해당 객체 관련 메모리나 자원들의 공유 설정. 점유 설정 등을 해제할 때
'''
class 클래스명:
    def __del__(self):
        # 해당 클래스 객체가 소멸될 때 같이 제거 또는 해제할 내용에 대한 코드 작성
        pass
'''

class Var :
    # field (private)
    __num = 100

    # constructor
    def __init__ (self, n) :
        print("Var 클래스 객체가 생성됨 : ", id(self))
        self.__num = n

    # destructor
    def __del__ (self) :
        print("Var 클래스 객체가 소멸됨 : ", id(self))

    # method : getter and setter
    def set_num (self, n) : 
        print("Var 클래스 객체가 가진 주소 (setter) : ", id(self))
        self.__num = n

    def get_num (self) : 
        print("Var 클래스 객체가 가진 주소 (getter) : ", id(self))
        return self.__num

# Var---------------------------------------------------------------------

# 클래스 객체 생성 : 생성자가 자동 실행됨
v1 = Var(50) # 추가된 매개변수 있는 생성자가 적용됨
v2 = Var(99)

print("v1이 가진 주소 : ", id(v1)) # v1이 가진 주소 :  140432489441344
print("v2가 가진 주소 : ", id(v2)) # v2가 가진 주소 :  140432489441344

# 필드값 변경 : setter 메소드 사용
print("setter 전 v1이 가진 num 값 : ", v1.get_num(), id(v1))
print("setter 전 v2가 가진 num 값 : ", v2.get_num(), id(v2))
v1.set_num(500)
v2.set_num(999)

# 필드값 확인 : getter 메소드 사용
print("setter 후 v1이 가진 num 값 : ", v1.get_num(), id(v1)) # v1이 가진 num 값 :  500
print("setter 후 v2가 가진 num 값 : ", v2.get_num(), id(v2)) # v2가 가진 num 값 :  999
#--------------------------------------------------------------------------------------

# 정적 메소드 (static method) : 클래스명.메소드명() 으로 호출하는 메소드
# 프로그램 실행시 정적 메모리 (static memory) 영역에 저장되는 메소드를 말함
# 메소드 작성시 메소드 이름 위에 장식자 (decorator == 어노테이션 : annotation) 
# @staticmethod 를 붙여서 작성함
# self 가 없는 메소드임 ==> 메소드 사용 :  클래스명.메소드명() 으로 호출함

class C : 
    def ham(self, x, y) : # self 가 자동으로 주소를 전달받음
        print('instance method : ', x, y)

class D :
    @staticmethod
    def spam(x, y) : # 프로그램 실행시 static 메모리에 자동 로딩됨. self 없어야 함
        print('static or class method : ', x, y)


# static method 는 사용시 객체 레퍼런스 (인스턴스의 주소) 없이 그냥 실행 됨 ==> self 가 없기 떄문
# 클래스명.메소드명(전달값) 으로 호출함
D.spam(10, 20)

# static method 를 instance method 처럼 써도 됨
dref = D()
dref.spam(30, 40)

# instance method 사용
# 아래는 self 가 없는 method 인 ham() 에 self 호출 안되서 에러남
# C.ham(11, 22) # TypeError: ham() missing 1 required positional argument: 'y'
# 해결법 : self 에 직접 주소 전달하면 됨
cref = C()
cref.ham(11, 20)        # cref 가 가진 주소를 self 매게변수에게 자동 전달
C.ham(cref, 11, 20)     # 단, 이 방식은 cref 를 생성하는 것처럼 인스턴스를 사전에 어딘가에서 생성해야 쓸 수 있고 과하게 변칙적인 방법



#-------------------------------------------------------------------------
if __name__ == "__main__" :
    # 객체 생성
    p1 = PClass(0) # 매개변수 있는 생성자 호출
    print(p1.get_num()) # 0

    p1.set_num(200)
    print(p1.get_num()) # 200
