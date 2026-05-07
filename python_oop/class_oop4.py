# path : ./class_oop4.py
# 파이썬의 추상화 테스트

from abc import ABC, abstractmethod

class Animal(ABC) :
    @abstractmethod
    def speak(self) :
        pass

class Dog(Animal) :
    def speak(self) :
        print("강아지가 멍멍 짖습니다.")

class Cat(Animal) :
    def speak(self) :
        print("고양이가 야옹 웁니다.")

# 추상화 테스트
animals = [
    Dog(),
    Cat(), 
    # Animal() # 추상 클래스는 객체 생성 불가능해서 에러남 (TypeError: Can't instantiate abstract class Animal with abstract methods speak)
]

for an in animals :
    an.speak()
