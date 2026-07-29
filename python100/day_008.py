"""
import random
f1=0
f2=0
f3=0
f4=0
f5=0
f6=0
for _ in range(6000):
    tem=random.randrange(1,7)
    match tem:
        case 1:
            f1+=1
            
        case 2:
            f2+=1
             
        case 3:
            f3+=1
             
        case 4:
            f4+=1
            
        case 5:
            f5+=1 
             
        case 6:
            f6+=1
            
print(f'1:{f1}')
print(f'2:{f2}')
print(f'3:{f3}')
print(f'4:{f4}')
print(f'5:{f5}')
print(f'6:{f6}')
"""

"""
items1=[35,12,99,88,55,]
items2=['python','java','go','kotlin']
items3=[100,12.3,'python',True]
print(items1)
print(items2)
print(items3)
"""

"""
items4=list(range(1,10))
items5=list('hello')
print(items4)
print(items5)
"""

"""
items5=[35,12,99,45,66]
items6=[45,58,29]
items7=['python','java','javascript']
print(items5+items6)
print(items6+items7)
items5+=items6
print(items5)
"""

"""
items5=[35,12,99,45,66]
items6=[45,58,29]
items7=['python','java','javascript']
print(items7*2)
print(items6*3)
items7*=2
print(items7)
"""

"""
items5=[35,12,99,45,66]
items6=[45,58,29]
items7=['python','java','javascript']
print(35 in items5)
print(35 not in items5)
print('python1' in items7)
print('python' in items7)
"""

"""
items8=['apple','waxberry','pitaya','peach','watermelon']
print(items8[0])
print(items8[-5])
print(items8[4])
print(items8[-1])
items8[4]='hhhhhh'
print(items8[-1])
items8[-1]='eeeeee'
print(items8[4])
"""

"""
items8=['apple','waxberry','pitaya','peach','watermelon']
items8[2]='durian'
items8[-4]='strawberry'
print(items8[0:6:1])
print(items8[-5:-1:1])
print(items8[0:4:2])
print(items8[-1:-5:-1])
items8[1:3]=['x','o']
print(items8)
"""

"""
num1=[1,2,3,4]
num2=list(range(1,5))
num3=[3,2,1]
print(num1==num2)
print(num1!=num2)
print(num1<=num3)
print(num2>=num3)
"""

"""
languages=['python','java','c++','kotlin']
for index in range(len(languages)):
    print(languages[index])
for language in languages:
    print(language)
"""

import random
count=[0]*6
for _ in range(6000):
    tem=random.randrange(1,7)
    count[tem-1]+=1
for i in range(1,7):
    print(f'{i}:{count[i-1]}')




































