"""
height=float(input('请输入身高（m）:'))
weight=float(input('请输入体重(kg):'))
BMI=weight/(height**2)
if 18.5<=BMI<24 :
    print(f'{BMI=:.1f}')
    print('你的身体相当棒；')
else :
    print('你的身体不够好哦；')
"""



"""
height=float(input('请输入身高（m）:'))
weight=float(input('请输入体重(kg):'))
BMI=weight/(height**2)
print(f'{BMI=:.2f}')
if BMI<18.5:
    print('太轻了；')
elif BMI<24:
    print('体态相当好：')
elif BMI<27:
    print('你的体重过重；')
elif BMI<30:
    print('你已经轻度肥胖；')
elif BMI<35:
    print('你已经中度肥胖；')
else :
    print('你已经重度肥胖；')
"""
"""
status_code=int(input('响应状态码：'))
match status_code:
    case 400: description='Bad Request'
    case 401: description='Unauthoried'
    case 403: description='Forbidden'
    case 404: description='Not Found'
    case 405: description='Method Not Allowed'
    case 418: description='I am a teapot'
    case 429: description='Too many requests'
    case _: description='Unknow Status Code'
print('状态码描述：',description)
"""
"""
x=float(input('请输入x:'))
if x>1:
    y=3*x-5
elif x>=-1:
    y=x+2
else :
    y=5*x+3
print(f'{y=:.2f}')
"""
"""
a=float(input('请输入成绩：'))
if a>=90:
    grade='A'
elif a>=80:
    grade='B'
elif a>=70:
    grade='C'
elif a>=60:
    grade='D'
else:
    grade='E'
print(f'{grade=}')
"""
print('接下来输入三角形三边长度：')
a=float(input('a='))
b=float(input('b='))
c=float(input('c='))
if b+c>a and a+c>b and a+b>c:
    long=a+b+c;
    p=long/2;
    s=(p*(p-a)*(p-b)*(p-c))**0.5
    print(f'周长:{long=:.2f}')
    print(f'面积:{s=:.2f}')
else :
    print('不能构成三角形；')




















