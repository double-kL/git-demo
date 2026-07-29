"""
languages=['python','java','c++']
languages.append('javascript')
print(languages)
languages.insert(1,'SQL')
print(languages)
"""

"""
languages=['python','SQL','java','c++','javascript']
if 'java' in languages:
    languages.remove('java')
if 'swift' in languages:
    languages.remove('swift')
print(languages)
languages.pop()
tem=languages.pop(1)
print(tem)
languages.append(tem)
print(languages)
languages.clear()
print(languages)
"""

"""
languages=['python','c++','python']
languages.remove('python')
print(languages)
"""

"""
item1=['python','c++','c']
del item1[1]
print(item1)
"""

"""
item1=['python','java','java','c++','kotlin','python']
print(item1.index('python'))
print(item1.index('python',1))
print(item1.count('python'))
print(item1.count('kotlin'))
print(item1.count('swift'))
"""

"""
print(item1.index('java',3))
"""

"""
item1=['python','java','c++','kotlin','swift']
item1.sort()
print(item1)
item1.reverse()
print(item1)
"""

"""
item1=[]
for i in range(1,100):
    if i%3==0 or i%5==0:
        item1.append(i)
print(item1)
"""

"""
item1=[i for i in range(1,100) if i%3==0 or i%5==0]
print(item1)
"""

"""
num1=[35,12,97,64,55]
num2=[]
for num in num1:
    num2.append(num**2)
print(num2)
"""

"""
num1=[35,12,97,64,55]
num2=[num**2 for num in num1]
print(num2)
"""

"""
num1=[35,12,97,64,55]
num2=[]
for num in num1:
    if num>50:
        num2.append(num)
print(num2)
"""

"""
num1=[35,12,97,64,55]
num2=[i for i in num1 if i>50]
print(num2)
"""

"""
scores=[[95,83,92],[80,75,82],[92,97,90],[80,78,69],[65,66,89]]
print(scores[0])
print(scores[0][1])
"""

"""
scores=[]
for _ in range(5):
    tem=[]
    for _ in range(3):
        score=int(input('请输入：'))
        tem.append(score)
    scores.append(tem)
print(scores)
"""

"""
import random
scores=[[random.randrange(60,101) for _ in range(3)] for _ in range(5)]
print(scores)
"""

"""
import random
red_ball=list(range(1,34))
selected_red_balls=[]
for _ in range(6):
    ball=random.randrange(len(red_ball))
    selected_red_balls.append(red_ball.pop(ball))
selected_red_balls.sort()
for ball in selected_red_balls:
    print(f'\033[031m{ball:0>2d}\033[0m',end=' ')
blue_ball=random.randrange(1,17)
print(f'\033[034m{blue_ball:0>2d}\033[0m')
"""

"""
import random
n=int(input('生成几注号码'))
red_ball=[i for i in range(1,34)]
blue_ball=[i for i in range(1,17)]
for _ in range(n):
    selected_red_balls=random.sample(red_ball,6)
    selected_red_balls.sort()
    for ball in selected_red_balls:
        print(f'\033[031m{ball:0>2d}\033[0m',end=' ')
    selected_blue_balls=random.choice(blue_ball)
    print(f'\033[034m{selected_blue_balls:0>2d}\033[0m')
"""


import random
from rich.console import Console
from rich.table import Table
console=Console()
n=int(input('生成几注号码'))
red_ball=[i for i in range(1,34)]
blue_ball=[i for i in range(1,17)]
table=Table(show_header=True)
for col_name in ('序号','红球','蓝球'):
    table.add_column(col_name, justify='center')
for i in range(n):
    selected_red_balls=random.sample(red_ball,6)
    selected_red_balls.sort()
    selected_blue_balls=random.choice(blue_ball)
    table.add_row(
        str(i+1),
        f'[red]{" ".join([f"{ball:0>2d}" for ball in selected_red_balls])}[/red]',
        f'[blue]{selected_blue_balls:0>2d}[/blue]',
    )
console.print(table)






























