"""
t1=(35,12,98)
t2=('骆驼',45,True,'成都')

print(type(t1))
print(type(t2))

print(len(t1))
print(len(t2))

print(t1[0])
print(t1[2])
print(t2[-1])

print(t2[:2])
print(t2[::3])

for tem in t1:
    print(tem)

print(12 in t1)
print('hao' in t2)
print('hao' not in t2)

t3=t1+t2
print(t3)

print(t1==t3)
print(t1>=t3)
print(t1<(35,11,99))
"""

"""
a=()
print(type(a))
b=('hello')
print(type(b))
c=(100)
print(type(c))
d=('hello',)
print(type(d))
e=(100,)
print(type(e))
"""

"""
a=1,10,100
print(type(a))
print(a)
i,j,k=a
print(i,j,k)
"""

"""
a=1,10,100
i,j=a
i,j,k,l=a
"""

"""
a=1,10,100,1000
i,j,*k=a 
print(i,j,k)
i,*j,k=a
print(i,j,k)
*i,j,k=a
print(i,j,k)
*i,j=a
print(i,j)
i,*j=a
print(i,j)
i,j,k,*l=a
print(i,j,k,l)
i,j,k,l,*m=a
print(i,j,k,l,m)
"""

"""
a,b,*c=range(1,10)
print(a,b,c)
a,b,c=[1,10,100]
print(a,b,c)
a,*b,c='hello'
print(a,b,c)
"""

"""
a=1
b=2
print(a,b)
a,b=b,a
print(a,b)
"""

"""
import timeit
print('%.3f 秒'% timeit.timeit('[1,2,3,4,5,6,7,8,9]',number=10000000))
print('%.3f 秒'% timeit.timeit('(1,2,3,4,5,6,7,8,9)',number=10000000))
"""

a=('骆驼',45,True,'成都')
print(list(a))
b=['apple','banana','orange']
print(tuple(b))





























