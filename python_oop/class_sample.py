# path : ./class_sample.py
# 파이썬에서 클래스 만들어 사용하기

# 파이썬은 객체지향, 절차지향, 함수형 프로그래밍 모두 지원하는 다중 패러다임 언어임 (multi-paradigm language)
# 하이브리드 언어
# 객체지향 : 클래스
# 절차지향 : 작성된 순서로 작동
# 함수형 : 함수

# 파이썬에서 클래스 만들기
'''
class 클래스명:
    맴버변수 = 초기값
    
    def 맴버함수명(self, 매개변수1, 매개변수2, *가변매개변수 ...):
        필드에 대한 값 처리에 대한 코드 작성
        self.맴버벼누 = 변경 할 값 | 계산식
        return self.필드명 또는 return 결과값

- 매개변수 self : 자바, C++, C# 의 this. 
'''

# 클래스 이름은 첫글자로 영어대문자 권장 (Naming Rule, 자바스크립트와 같음)
class SClass :
    pass # 맴버가 없는 빈 클래스 작성할 수 있음
# 빈 클래스는 실행시 namespace 가 할당됨 => 이름만 있어도 메모리 공간이 할당됨

# 클래스 사용 : 객체 (인스턴스, 오브젝트) 생성 (메모리에 클래스에 대한 객체 공간 (instance) 할당)
ref1 = SClass()
ref2 = SClass()

print("ref1이 가진 주소 : ", id(ref1)) # ref1이 가진 주소
print("ref2가 가진 주소 : ", id(ref2)) # ref2가 가진 주소

# 파이썬은 실행할 때(동적으로) 맴버변수(필드)를 추가할 수 있음
ref1.score = 100 # ref1 객체에 score 라는 맴버변수 추가하고 100 할당
print("ref1이 가진 score 값 : ", ref1.score) # ref1이 가진 score 값 :  100
# ref2 객체에는 score 라는 맴버변수가 없어서 에러남 ==> 둘이 다른 객체로 생성된 걸 확인
#  (dict 로 클래스가 생성되는 구조상 그렇게 됨)
# #print("ref2가 가진 score 값 : ", ref2.score) # AttributeError: 'SClass' object has no attribute 'score'


