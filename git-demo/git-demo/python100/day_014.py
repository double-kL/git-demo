"""
from math import factorial as f


m=int(input('m= '))
n=int(input('n= '))

def fac(num):
    result=1
    for n in  range(1,num+1):
        result*=n
    return result
fm=1
for num in range(1,m+1):
    fm*=num
fn=1
for num in range(1,n+1):
    fn*=num
fk=1
for num in range(1,m-n+1):
    fk*=num
print(fm/(fk*fn))
print(fac(m)/(fac(n)*fac(m-n)))

print(f(m)/(f(n)*f(m-n)))

def judgement(a,b,c,):
    return a+b
print(judgement(3,4,5))
print(judgement(1,2,3))
print(judgement(b=2,c=3,a=1))
print(judgement(c=5,b=4,a=3))

from random import randrange
def roll_dice(n=2):
    total=0
    for _ in range(n):
        total+=randrange(1,7)
    return total
print(roll_dice())
print(roll_dice(3))

def add(a=0,b=0,c=0):
    return a+b+c
print(add())
print(add(1))
print(add(1,2))
print(add(1,2,3))

def add(*args):
    total=0
    for val in args:
        if type(val) in (int ,float):
            total+=val
    return total
print(add())
print(add(1))
print(add(1,2,3))
print(add(1,2,'hello',3.45,6))

def foo(*args,**kwargs):
    print(args)
    print(kwargs)
foo(3,2.1,True,name='luohao',age=43,gpa=4.95)
"""
 