import random 
import string
"""
all=string.digits+string.ascii_letters
def generate(*,len=4):
    return ''.join(random.choices(all,k=len))
for _ in range(5):
    print(generate(len=6))

def is_prime(num:int)->bool:
    for i in range(2,int(num**0.5)+1):
        if num%i==0:
            return False
    return True

def lcm(x:int ,y:int)->int:
    returnx*y/gcd(x,y)
def gcd(x:int ,y:int)->int:
    while y%x !=0:
        x,y=y%x,x
    return x
"""
redball=[i for i in range(1,34)]
blueball=[i for i in range(1,17)]
def choose():
    select_balls=random.sample(redball,6)
    select_balls.sort()
    select_balls.append(random.choice(blueball))
    return select_balls
def display(balls):
    for ball in balls[:-1]:
        print(f'\033[031m{ball:0>2d}\033[0m',end=' ')
    print(f'\033[034m{balls[-1]:0>2d}\033[0m',end=' ')
n= int(input('生成几注号码:'))
for _ in range(n):
    display(choose())