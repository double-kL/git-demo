"""
def calc(init_value,op_func,*args,**kwargs):
    items=list(args)+list(kwargs.values())
    result=init_value
    for item in items:
        if type(item) in (int,float):
            result=op_func(result,item)
    return result

def add(x,y):
    return x+y
def mul(x,y):
    return x*y
print(calc(0,add,1,2,3,4,5))
print(calc(1,mul,1,2,3,4,5))

def is_even(num):
    return num%2==0
def square(num):
    return num**2
old_nums=[35,12,8,99,60,52]
new_nums=list(map(square,filter(is_even,old_nums)))
print(new_nums)

old_nums=[35,12,8,99,60,52]
new_nums=list(num**2 for num in old_nums if num%2==0)
print(new_nums)

old_strings=['in','apple','zoo','waxberry','pear']
new_strings=sorted(old_strings,key=len)
print(new_strings)

old_nums=[35,12,8,99,60,52]
new_nums=list(map(lambda x:x**2,filter(lambda x:x%2==0,old_nums)))
print(new_nums)

import functools
import operator
fac=lambda n:functools.reduce(operator.mul,range(2,n+1),1)
is_prime=lambda x:all(map(lambda f:x%f,range(2,int(x**0.5)+1)))
print(fac(6))
print(is_prime(37))
"""
import functools
int2=functools.partial(int,base=2)
int8=functools.partial(int,base=8)
int16=functools.partial(int,base=16)
print(int('1001'))
print(int2('1001'))
print(int8('1001'))
print(int16('1001'))
