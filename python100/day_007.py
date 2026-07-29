"""
for i in range(3,101):
    a=1
    for j in range(2,i):
        if(i%j==0):
            a=0
            break
    if a==1:
        print(f'{i}')
"""

"""
a=0
b=1
for _ in range(1,21):
    a,b=b,a+b
    print(a)
"""
"""
import  math
for i in range(100,1000):
    j=i
    a=1
    while j//10:
        a=a+1
        j=j//10
    j=i
    sum=0
    while j>0:
        sum=sum+(j%10)**a
        j=j//10
    if sum==i:
        print(i)
"""
"""
num=int(input('请输入一个整数:'))
sum=0
while num>0:
    sum=(num%10)+sum*10
    num=num//10
print(sum)
"""

"""
for g in range(1,21):
    for m in range(1,35):
        for x in range(0,100,3):
            if 100==(5*g+3*m+x/3) and ((g+m+x)==100):
                print(f'公鸡：{g},母鸡：{m}，小鸡：{x}')
"""

"""
import random
money=1000
while money>0:
    print(f'你的余额为{money}')
    bet=int(input('请输入你的赌注：'))
    a=1
     
    r1=random.randrange(1,7)
    r2=random.randrange(1,7)
    sum=r1+r2
    if sum==7 or sum==11:
        a=2
        break
    if sum==2 or sum==3 or sum==12:
        a=3
        break
    while a==1:
        r1=random.randrange(1,7)
        r2=random.randrange(1,7)
        if sum==r1+r2:
            a=2
            break
        if r1+r2==7:
            a=3
            break
    if a==2:
        money=money+bet
    if a==3:
        money=money-bet
print('你破产了，游戏结束；')       
"""


























