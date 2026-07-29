"""
s1='hello world'
s2="你好，世界"
s3='''hello ,
wonderful
world!'''
print(s1)
print(s2)
print(s3)
"""

"""
s1='\'hello world!\''
s2='\\hello world!\\'
print(s1)
print(s2)
"""

"""
s1='\it \is \time \to \read \now'
s2=r'\it \is \time \to \read \now'
s3=R'\it \is \time \to \read \now'
print(s1)
print(s2)
print(s3)
"""

"""
s1='\141\142\143\x61\x62\x63'
s2='\u9a86\u660a'
print(s1)
print(s2)
"""

"""
s1='hello'+','+'world'
print(s1)
s2='!'*3
print(s2)
s1+=s2
print(s1)
s1*=2
print(s1)
"""

"""
s1='a whole new world'
s2='hello world'
print(s1==s2)
print(s1<s2)
print(s1=='hello world')
print(s2=='hello world')
print(s2!='hello world')
s3='骆驼'
print(ord('骆'))
print(ord('驼'))
s4='王大锤'
print(ord('王'))
print(ord('大'))
print(ord('锤'))
print(s3>=s4)
print(s3!=s4)
"""

"""
s1='hello world'
s2='goodbey,world'
print('wo' in s1)
print('wo' not in s2)
print(s2 in s1)
"""

"""
s='hello world'
print(len(s))
print(len('goodbey, world'))
"""

"""
s='abc123456'
n=len(s)
print(s[0],s[-n])
print(s[n-1],s[-1])
print(s[2],s[-7])
print(s[5],s[-4])
print(s[2:5])
print(s[-7:-4])
print(s[2:])
print(s[:2])
print(s[::2])
print(s[::-1])
"""

"""
s='hello'
for i in range(len(s)):
    print(s[i])
"""

"""
s='hello'
for elem in s:
    print(elem)
"""

s1='hello world'
print(s1.capitalize())
print(s1.title())
print(s1.upper())
s2='GOODBYE'
print(s2.lower())
print(s1)
print(s2)






























