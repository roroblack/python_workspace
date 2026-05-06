# path : ./class_oop2.py
# oop 에서의 연산자 오버로딩 (operator overloading) (operator overwriting 은 상속시 메소드 재정의)

# 오버로딩  : 클래스 안에서 이름이 같은 메소드 중복 작성(정의)
# 파이썬에서는 생성자와 메소드는 오버로딩 안 됨 => 작성은 할 수 있으나, 마지막에 작성된 것으로 덮어쓰기 됨 (overwriting)
# C++, 파이썬 에서는 값 계산에 사용되는 연산자를 객체 간의 연산으로 재정의할 수 있음
# 연산자 : 값 계산에 사용되는 기호
# 객체 간의 연산은 불가능함
# 클래스 안에 연사자와 관련된 예약어를 사용해서, 객체 간의 연산이 가능하도록 기존 연산자에 대한 메소드를 추가 작성하는 것

'''

객체와 객체간 연산과 객체와 값의 연산이 있음
객체 + 값 (객체)    : __add__(self(앞의 객체의 주소받음), 값 또는 객체(뒤의 객체의 주소받음))
    return self.필드 + 값 또는 return self.필드 + other.필드
객체 - 값 (객체)    : __sub__(self, other)
객체 * 값 (객체)    : __mul__(self, other)
객체 / 값 (객체)    : __truediv__(self, other)
객체 // 값 (객체)   : __floordiv__(self, other)
객체 % 값 (객체)    : __mod__(self, other)
객체 ** 값 (객체)   : __pow__(self, other)
객체 == 값 (객체)   : __eq__(self, other)
객체 != 값 (객체)   : __ne__(self, other)
객체 > 값 (객체)    : __gt__(self, other)
객체 >= 값 (객체)   : __ge__(self, other)
객체 < 값 (객체)    : __lt__(self, other)
객체 <= 값 (객체)   : __le__(self, other)
객체 & 값 (객체)    : __and__(self, other)
객체 | 값 (객체)    : __or__(self, other)
객체 ^ 값 (객체)    : __xor__(self, other)
객체 << 값 (객체)   : __lshift__(self, other)
객체 >> 값 (객체)   : __rshift__(self, other)
객체 ~ 값 (객체)    : __invert__(self)

시퀀스나 맵 타입에 대해서도 연산자 오버로딩 가능함

타입 변환 관련 메소드 오버로딩
__int__(self) : 
    return int(self.필드) 또는 return int(계산식)

__float__(self) :
    return float(self.필드) 또는 return float(계산식)

__bool__(self) :
    return bool(self.필드명)

'''

class OOP :
    # field
    __num = 0

    # constructor
    def __init__ (self, num) : self.__num = num

    # method 연산자 오버로딩 메소드 추가
    def __add__(self, value) : 
        '+ 연산자를 메소드로 오버로딩 처리'
        return self.__num + value
    
    def __sub__(self, value) :
        '- 연산자를 메소드로 오버로딩 처리'
        return self.__num - value
    
    def __mul__(self, value) :
        '* 연산자를 메소드로 오버로딩 처리'
        return self.__num * value
    
    def __truediv__(self, value) :
        '/ 연산자를 메소드로 오버로딩 처리'
        return self.__num / value
    
    def __floordiv__(self, value) :
        '// 연산자를 메소드로 오버로딩 처리'
        return self.__num // value
    
    #getter
    def ger_num (self) : return self.__num
print('# class OOP -----------------------------------------------------------------')

# 클래스 객체 생성
ref = OOP(100)
print('ref가 참조하는 인스턴스 안의 __num 값 : ', ref.ger_num()) # ref가 참조하는 인스턴스 안의 __num 값 :  100

# 객체와 값의 연산 (기본적으로 객체와 값의 연산은 불가능)
# print('ref > 30 :', ref > 30 ) // 주소랑 값의 연산은 불가능 => TypeError

print('ref + 30 :', ref + 30) # ref + 30 : 130
print('ref - 30 :', ref - 30) # ref - 30 : 70
print('ref * 30 :', ref * 30) # ref * 30 : 3000
print('ref / 30 :', ref / 30) # ref / 30 : 3.3333333333333335

# len() : 길이(저장된 값의 갯수)를 구하는 내장함수
# 리스트, 튜플, 문자열 같은 시퀀스 자료형에 주로 사용
# 연산자 오버로딩으로 추가할 수 있음
class MyNumber :
    def __init__(self, value)   : self.value = value # 필드 동적 추가
    def __len__(self)           : return self.value
print('# class MyNumber -----------------------------------------------------------------')

ref = MyNumber(10)
print('len() : ', len(ref)) # len() :  10

# in 연산자 오버로딩도 가능
class MyBox :
    def __init__(self, items) : self.items = items
    
    def __len__(self) : return len(self.items)

    def __contains__(self, item):
        return item in self.items
    
print('# class MyBox -----------------------------------------------------------------')

box = MyBox([1, 2, 3])
print('len(box) : ', len(box)) # len(box) :  3
print(2 in box) # True
print(4 in box) # False

# 인덱싱 : [index] 연산자 오버로딩
class MyList :
    def __init__(self, data) : self.data = data

    def __len__(self) : return len(self.data)
    
    def __getitem__(self, index) : return self.data[index]

    def __str__(self) : return str(self.data) # 자바의 toString() 과 같은 역할.
print('# class MyList -----------------------------------------------------------------')

mylst = MyList([10, 20, 30])
print(len(mylst)) # 3
print(mylst[0])   # 10
print(mylst[1])   # 20
print(mylst[2])   # 30
print(mylst)      # [10, 20, 30]
