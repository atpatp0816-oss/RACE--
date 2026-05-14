#기본 함수
def greet(name):
    return f"안녕,{name}"


print(greet("유리"))

#여러값 반환 tuple
def calc(a,b):
    return a+b,a*b
print(calc(5,4))

total, product = calc(3,4)
print(total, product)

class Student:
    def __init__(self,name:str,score:int):
        self.name = name
        self.score = score
    def get_grade(self)->str:
        return'A' if self.score>= 90 else 'B'
    def __str__(self)-> str:
        return f'{self.name}:{self.score}점'   

s1=Student('박태현',100)
print(s1.get_grade())
print(s1.__str__())
