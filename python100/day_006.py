"""
import time
for i in range(3600):
    print('hello world')
    time.sleep(1)
"""
"""
total=0
for i in range(1,101):
    total+=i 
print(f'{total=}')
"""
"""
total=0;
for i in range(0,101,2):
    total +=i
print(f'{total=}')
"""
"""
print(sum(range(0,101,2)))
"""

"""
total=0
i=1
while i<=100:
    total+=i 
    i+=1
print(f'{total=}')
"""

"""
total =0
i=1
while i<=100:
    total+=i 
    i+=2
print(f'{total=}')
"""
"""
for i in range(1,10):
    for j in range(1,i+1):
        print(f'{i}x{j}={i*j} ',end='\t')
    print()
"""

tem=int(input('请输入一个整数：'))
m=1
for i in range(2,tem):
    if(tem%i==0):
        break;
    if(i==tem-1):
        print('yes;')
        m=0
if m:     
    print('no;')

"""
a=int(input('请输入第一个整数：'))
b=int(input('请输入第二个整数：'))
while c=a%b:
    a=b
    b=C
print(f'{b}')
"""
"""
import random
anser=random.randrange(1,101)
count=0
while True:
    a=int(input('请输入一个整数：'))
    count+=1
    if a>anser:
        print('小一点；')
    elif a<anser:
        print('大一点；')
    else  :
        print('猜对了；')
        print(f'你一共猜了{count}次.')
        break;
"""
