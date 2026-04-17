
"""

print(8/5)
print(8//5)
print(2*3)
print(2**3)
print(10)
print(a:=10)
print(a)
f=float(input('请输入华氏温度：'))
d=(f-32)/1.8
print('%.1f华氏温度=%.1f摄氏温度'%(f,d))

"""
"""
radius=float(input('请输入圆3的半径：'))
c=2*3.1415*radius
s=3.1415*radius*radius
print('周长：%.2f'% c)
print('面积：%.2f'% s)
"""

"""
import math
r=float(input('请输入面积：'))
c=2*r*math.pi
s=math.pi*r**2
print(f'{c=:.2f}')
print(f'{s=:.2f}')
"""

year=int(input('请输入年份：'))
is_leap=year%400==0 or (year%4==0 and year%100!=0)
print(f'{is_leap=}')
