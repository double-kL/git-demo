"""
class student:
    def __init__(self,name,age):
        self.name=name
        self.age=age
    def study(self,course_name):
        print(f'学生正在学习{course_name}.')
    def play(self):
        print(f'学生正在玩游戏.')

stu1=student()
stu2=student()
print(stu1)
print(stu2)
print(hex(id(stu1)),hex(id(stu2)))
student.study(stu1,'python程序设计')
stu1.study('python程序设计')
student.play(stu2)
stu2.play()
stu3=student('小明',18)
stu4=student('小美',28)
stu3.study('python程序设计')
stu4.play()

import time
class clock:
    def __init__(self,hour=0,minute=0,second=0):
        self.hour=hour
        self.min=minute
        self.sec=second
    def run(self):
        self.sec+=1
        if self.sec==60:
            self.sec=0
            self.min+=1
            if self.min==60:
                self.min=0
                self.hour+=1
                if self.hour==24:
                    self.hour=0
    def show(self):
        return f'{self.hour:0>2d}:{self.min:0>2d}:{self.sec:0>2d}'
clock1=clock(23,59,58)
while True:
    print(clock1.show())
    time.sleep(1)
    clock1.run()
"""
class Point:
    def __init__(self,x=0,y=0):
        self.x,self.y=x,y
    def distance_to(self,other):
        dx=self.x-other.x
        dy=self.y-other.y
        return (dx**2+dy**2)**0.5
    def __str__(self):    
        return f'({self.x},{self.y})'
p1=Point(3,5)
p2=Point(6,9)
print(p1)
print(p2)
print(p1.distance_to(p2))