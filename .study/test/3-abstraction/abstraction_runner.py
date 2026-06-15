# abstraction_runner.py
# 파이썬 추상화(ABC, Protocol, Duck Typing) 섹션별 테스트 실행기
# 실행: c:\_proj\python_workspace\.venv\Scripts\python.exe abstraction_runner.py
# 결과: logs/{섹션명}.txt 에 저장 + 터미널에 출력

import sys, io, pathlib
from contextlib import redirect_stdout

# PowerShell cp949 → utf-8 강제 (em dash 등 특수문자 출력 대응)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

LOGS = pathlib.Path(__file__).parent / "logs"
LOGS.mkdir(exist_ok=True)

def run_section(name, fn):
    sep = "=" * 60
    buf = io.StringIO()
    print(sep); print(f"# {name}"); print(sep)
    with redirect_stdout(buf):
        try:
            fn()
        except Exception as e:
            print(f"{type(e).__name__}: {e}")
    out = buf.getvalue()
    sys.stdout.write(out)
    (LOGS / f"{name}.txt").write_text(
        sep + "\n" + f"# {name}" + "\n" + sep + "\n" + out,
        encoding="utf-8"
    )

# ── §00: C/C++ vtable vs Python 동적 디스패치 ─────────────────────────────
def s0_vtable_vs_python():
    """C/C++ vtable(정적 바인딩)과 Python 동적 디스패치(__dict__ 탐색)의 차이,
    덕 타이핑 선택 이유와 장단점을 실행으로 확인한다."""

    # 1. Python MRO (__mro__) 와 __dict__ 탐색 순서
    #    C++: 컴파일 타임에 vtable 완성 → 런타임에 포인터 역참조
    #    Python: 런타임에 __mro__ 순서대로 __dict__ 탐색 → 메서드 반환
    class Base:
        def method(self): print("Base.method() 호출")

    class Child(Base):
        def method(self): print("Child.method() 호출")

    print(f"Child.__mro__ : {[c.__name__ for c in Child.__mro__]}")
    print(f"'method' in Child.__dict__: {'method' in Child.__dict__}")
    print(f"'method' in Base.__dict__ : {'method' in Base.__dict__}")
    c = Child()
    c.method()   # Child.__dict__ 에 있으므로 Base 탐색 없이 바로 반환

    # 2. 덕 타이핑 — 타입 검사 없이 메서드 존재 여부만으로 동작
    class Duck:
        def quack(self): print("꽥꽥! (Duck)")

    class Person:
        def quack(self): print("꽥꽥 흉내냄 (Person) — Duck 상속 없음")

    class Stone: pass  # quack 없음

    def make_it_quack(thing):
        thing.quack()  # 타입 검사 없음 — AttributeError 면 실행 시 터짐

    for obj in [Duck(), Person()]:
        make_it_quack(obj)   # 둘 다 동작 — 덕 타이핑

    try:
        make_it_quack(Stone())
    except AttributeError as e:
        print(f"AttributeError: {e}")

    # 3. Python 동적 디스패치 — 런타임에 메서드 교체 가능 (C++ vtable은 불가)
    import types

    class Robot:
        def speak(self): print("로봇: 삐-뽀!")

    r = Robot()
    r.speak()   # 기본 구현

    # 런타임에 인스턴스 메서드만 교체 (클래스 전체 영향 없음)
    r.speak = types.MethodType(lambda self: print("로봇: 업그레이드됨!"), r)
    r.speak()   # 동일 객체인데 다른 메서드 — C++ vtable 에서는 불가능

    r2 = Robot()
    r2.speak()  # 새 인스턴스는 원래 메서드 유지

    # 4. 덕 타이핑 장단점 요약
    print("\n[덕 타이핑 장단점]")
    print("장점: 상속 계층 없이도 다형성 — 유연하고 재사용성 높음")
    print("단점: 구현 누락을 컴파일 타임에 잡지 못함 — 런타임 AttributeError")
    print("해결: ABC(명시적 강제) 또는 Protocol(구조적 타입 힌트)으로 보완")

run_section("00_vtable_vs_python", s0_vtable_vs_python)

# ── §01: 덕 타이핑 — class_oop3.py 기반 ────────────────────────────────
def s1_duck_typing():
    # class_oop3.py 의 Animal/Dog/Cat 상속 구조 — ABC 없이 덕 타이핑으로 동작
    class Animal:
        def speak(self): print("동물이 소리를 냅니다.")

    class Dog(Animal):
        def speak(self): print("강아지가 멍멍 짖습니다.")

    class Cat(Animal):
        def speak(self): print("고양이가 야옹 웁니다.")

    # class_oop3.py 의 다형성 테스트 그대로 재현
    animals = [Dog(), Cat(), Animal()]
    for an in animals:
        an.speak()

    # ABC 없으면 speak() 구현 누락을 강제할 수 없음 → 호출 시점에 터짐
    class Snail: pass   # speak() 구현 안 함 (달팽이는 소리를 안 냄)

    try:
        Snail().speak()
    except AttributeError as e:
        print(f"AttributeError: {e}")

    print("→ ABC 없는 덕 타이핑: 구현 누락은 호출 시점에 발생")

run_section("01_duck_typing", s1_duck_typing)

# ── §02: ABC 로 인터페이스 강제 — class_oop4.py 기반 + move() 추가 ────────
def s2_abc_basic():
    from abc import ABC, abstractmethod

    # class_oop4.py 기반: speak() 하나만 있던 것에 move() 추가
    class Animal(ABC):
        @abstractmethod
        def speak(self): pass

        @abstractmethod
        def move(self): pass        # class_oop4.py 에는 없는 두 번째 추상 메서드

        def breathe(self):          # 구현된 메서드는 상속됨 (공통 로직)
            print("  (숨쉬는 중...)")

    # class_oop4.py 원본의 Dog·Cat 에 move() 구현 추가
    class Dog(Animal):
        def speak(self): print("강아지가 멍멍 짖습니다.")
        def move(self):  print("강아지가 네 발로 달립니다.")

    class Cat(Animal):
        def speak(self): print("고양이가 야옹 웁니다.")
        def move(self):  print("고양이가 살금살금 걷습니다.")

    for a in [Dog(), Cat()]:
        a.speak(); a.move(); a.breathe()

    # move() 미구현 케이스
    class Fish(Animal):
        def speak(self): print("물고기는 소리가 없습니다.")
        # move() 없음

    try:
        Fish()
    except TypeError as e:
        print(f"TypeError: {e}")

    # Animal() 직접 인스턴스화 (class_oop4.py 에서 주석 처리되어 있던 부분)
    try:
        Animal()
    except TypeError as e:
        print(f"TypeError: {e}")

run_section("02_abc_basic", s2_abc_basic)

# ── §03: abstractmethod + property — class_oop2.py MyBox·MyList 기반 ABC ──
def s3_abc_decorators():
    from abc import ABC, abstractmethod

    # class_oop2.py 의 MyBox·MyList·MyNumber 를 ABC 로 추상화
    # 원본은 각자 독립 클래스였지만, ABC 로 공통 인터페이스를 강제
    class AbstractCollection(ABC):
        @abstractmethod
        def __len__(self) -> int: pass

        @abstractmethod
        def __contains__(self, item) -> bool: pass

        @abstractmethod
        def __getitem__(self, index): pass

        def describe(self):             # 공통 구현 — 서브클래스 모두 사용 가능
            print(f"  항목 수: {len(self)}")

    # class_oop2.py 의 MyBox — __len__, __contains__ 에 __getitem__ 추가
    class MyBox(AbstractCollection):
        def __init__(self, items):      self.items = items
        def __len__(self):              return len(self.items)
        def __contains__(self, item):   return item in self.items
        def __getitem__(self, index):   return self.items[index]

    # class_oop2.py 의 MyList — __getitem__, __str__ + ABC 인터페이스 완성
    class MyList(AbstractCollection):
        def __init__(self, data):       self.data = data
        def __len__(self):              return len(self.data)
        def __contains__(self, item):   return item in self.data
        def __getitem__(self, index):   return self.data[index]
        def __str__(self):              return str(self.data)  # 원본 유지

    box = MyBox([10, 20, 30])
    lst = MyList(['a', 'b', 'c'])

    for col in [box, lst]:
        col.describe()
        print(f"  {type(col).__name__}[0] = {col[0]}")

    print(f"20 in box: {20 in box}")
    print(f"'b' in lst: {'b' in lst}")
    print(f"str(lst)  = {lst}")

    # __getitem__ 미구현 시도
    class IncompleteCol(AbstractCollection):
        def __len__(self): return 0
        def __contains__(self, item): return False
        # __getitem__ 없음

    try:
        IncompleteCol()
    except TypeError as e:
        print(f"TypeError: {e}")

run_section("03_abc_decorators", s3_abc_decorators)

# ── §04: Protocol — class_oop3.py Animal/Dog/Cat 기반 Speakable ───────────
def s4_protocol():
    from typing import Protocol, runtime_checkable

    # class_oop3.py 의 Animal/Dog/Cat 덕 타이핑을 Protocol 로 공식화
    @runtime_checkable
    class Speakable(Protocol):
        def speak(self) -> None: ...

    # class_oop3.py 원본 클래스 그대로
    class Animal:
        def speak(self): print("동물이 소리를 냅니다.")

    class Dog(Animal):
        def speak(self): print("강아지가 멍멍 짖습니다.")

    class Cat(Animal):
        def speak(self): print("고양이가 야옹 웁니다.")

    # Animal 상속 없이도 speak() 만 있으면 Speakable (구조적 서브타이핑)
    class Robot:
        def speak(self): print("삐-뽀-삐-뽀!")

    class Snail: pass   # speak() 없음

    # isinstance 검사 (runtime_checkable)
    for obj in [Animal(), Dog(), Cat(), Robot(), Snail()]:
        ok = isinstance(obj, Speakable)
        print(f"{type(obj).__name__:8} isinstance Speakable: {ok}")

    # 타입 힌트로 Speakable 활용 — class_oop3.py 의 for an in animals: an.speak() 패턴과 동일
    print("--- make_noise() ---")
    def make_noise(thing: Speakable):
        thing.speak()

    for thing in [Dog(), Cat(), Robot()]:
        make_noise(thing)

    # Speakable 없는 객체에 make_noise 시도
    try:
        make_noise(Snail())
    except AttributeError as e:
        print(f"AttributeError: {e}")

run_section("04_protocol", s4_protocol)

# ── §05: ABC vs Protocol 선택 기준 ───────────────────────────────────────
def s5_abc_vs_protocol():
    from abc import ABC, abstractmethod
    from typing import Protocol

    # ABC: 클래스 계층 + 공통 구현 공유 목적
    class Serializable(ABC):
        @abstractmethod
        def to_json(self) -> str: pass

        def save(self, path: str):   # ABC는 구현 로직 포함 가능
            print(f"  → {path} 에 저장: {self.to_json()}")

    class User(Serializable):
        def __init__(self, name): self.name = name
        def to_json(self): return f'{{"name":"{self.name}"}}'

    u = User("Alice")
    u.save("users.json")

    # Protocol: 기존 클래스를 수정하지 않고 "인터페이스" 확인
    class Closeable(Protocol):
        def close(self) -> None: ...

    class FileHandle:
        def close(self): print("  FileHandle.close()")

    class DBConnection:
        def close(self): print("  DBConnection.close()")

    def cleanup(resource: Closeable):
        resource.close()

    # FileHandle, DBConnection 은 Closeable 을 상속하지 않아도 호환
    for r in [FileHandle(), DBConnection()]:
        cleanup(r)

    print("ABC는 공통 구현 상속, Protocol은 상속 없이 구조만 맞추면 OK")

run_section("05_abc_vs_protocol", s5_abc_vs_protocol)

# ── §06: __abstractmethods__ 와 ABCMeta 내부 ─────────────────────────────
def s6_internals():
    from abc import ABC, abstractmethod, ABCMeta

    class ILogger(ABC):
        @abstractmethod
        def log(self, msg: str): pass
        @abstractmethod
        def flush(self): pass

    # 미완성 클래스의 __abstractmethods__ 확인
    print(f"ILogger.__abstractmethods__ = {ILogger.__abstractmethods__}")

    class FileLogger(ILogger):
        def log(self, msg): print(f"  [FILE] {msg}")
        def flush(self):    print("  [FILE] flush")

    print(f"FileLogger.__abstractmethods__ = {FileLogger.__abstractmethods__}")

    fl = FileLogger()
    fl.log("테스트 메시지"); fl.flush()

    # ABCMeta 직접 사용
    class IWriter(metaclass=ABCMeta):
        @abstractmethod
        def write(self, data): pass

    print(f"IWriter.__abstractmethods__ = {IWriter.__abstractmethods__}")
    print(f"type(IWriter) = {type(IWriter)}")

run_section("06_internals", s6_internals)

# ── §07: 실전 — 결제 시스템 (ABC 계층 설계) ─────────────────────────────
def s7_payment_system():
    from abc import ABC, abstractmethod
    import datetime

    class PaymentGateway(ABC):
        """모든 결제 수단의 추상 기반 클래스"""

        @abstractmethod
        def charge(self, amount: int) -> bool:
            """결제 시도. 성공 True, 실패 False"""

        @abstractmethod
        def refund(self, amount: int) -> bool:
            """환불. 성공 True, 실패 False"""

        def process(self, amount: int):          # 공통 로직 포함
            ts = datetime.datetime.now().strftime("%H:%M:%S")
            ok = self.charge(amount)
            status = "성공" if ok else "실패"
            print(f"  [{ts}] {type(self).__name__} {amount:,}원 결제 {status}")

    class CreditCard(PaymentGateway):
        def __init__(self, card_no):  self.card_no = card_no[-4:]
        def charge(self, amount):
            print(f"    카드 *{self.card_no}: {amount:,}원 청구")
            return True
        def refund(self, amount):
            print(f"    카드 *{self.card_no}: {amount:,}원 취소")
            return True

    class BankTransfer(PaymentGateway):
        def __init__(self, acct): self.acct = acct[-4:]
        def charge(self, amount):
            print(f"    계좌 {self.acct}: {amount:,}원 이체")
            return True
        def refund(self, amount):
            print(f"    계좌 {self.acct}: 환불은 수동 처리")
            return False

    gateways = [
        CreditCard("1234-5678-9012-3456"),
        BankTransfer("110-123-456789"),
    ]
    for gw in gateways:
        gw.process(50000)

    # 미완성 게이트웨이
    class BrokenGateway(PaymentGateway):
        def charge(self, amount): return False
        # refund 없음

    try:
        BrokenGateway()
    except TypeError as e:
        print(f"TypeError: {e}")

run_section("07_payment_system", s7_payment_system)

# ── §08: 부트캠프 실습 코드와의 연결 ─────────────────────────────────────
def s8_bootcamp_link():
    from abc import ABC, abstractmethod

    # class_oop4.py 그대로 + 추상 클래스 직접 인스턴스화 에러 확인
    class Animal(ABC):
        @abstractmethod
        def speak(self): pass

    class Dog(Animal):
        def speak(self): print("강아지가 멍멍 짖습니다.")

    class Cat(Animal):
        def speak(self): print("고양이가 야옹 웁니다.")

    animals = [Dog(), Cat()]
    for an in animals:
        an.speak()

    # Animal() 직접 생성 시도
    try:
        Animal()
    except TypeError as e:
        print(f"TypeError: {e}")

    # isinstance 로 ABC 검사
    d = Dog()
    print(f"isinstance(Dog(), Animal): {isinstance(d, Animal)}")
    print(f"issubclass(Dog, Animal):   {issubclass(Dog, Animal)}")

run_section("08_bootcamp_link", s8_bootcamp_link)

print("\n모든 섹션 완료")
