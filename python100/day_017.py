 
import random
import time
"""
def download(filename):
    start=time.time()
    print(f'开始下载{filename}')
    
    end=time.time()
    print(f'{filename}下载完成')
    print(f'花费时间：{end-start}')

def upload(filename):
    start=time.time()
    print(f'开始上传{filename}')
    time.sleep(random.random()*6)
    end=time.time()
    print(f'{filename}上传完成')
    print(f'花费时间：{end-start}')

 
download('MySQL从删库到跑路.avi')
upload('Python从入门到住院.pdf')

def download(filename):
    print(f'开始下载{filename}')
    print(f'{filename}下载完成')
def upload(filename):
    print(f'开始上传{filename}')
    time.sleep(random.random()*6)
    print(f'{filename}上传完成')
def record_time(func):
    def wrapper(*args,**kwargs):
        start=time.time()
        result=func(*args,**kwargs)
        end=time.time()
        print(f'{func.__name__}执行时间：{end-start:.2f}秒')
        return result
    return wrapper
download=record_time(download)
upload=record_time(upload)
download('MySQL从删库到跑路.avi')
upload('Python从入门到住院.pdf')

from functools import  wraps
def record_time(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        start=time.time()
        result=func(*args,**kwargs)
        end=time.time()
        print(f'{func.__name__}执行时间：{end-start:.2f}秒')
        return result
    return wrapper
@record_time
def download(filename):
    print(f'开始下载{filename}')
    print(f'{filename}下载完成')
@record_time
def upload(filename):
    print(f'开始上传{filename}')
    time.sleep(random.random()*6)
    print(f'{filename}上传完成')
download('MySQL从删库到跑路.avi')
upload('Python从入门到住院.pdf')
download.__wrapped__('MySQL从删库到跑路')
upload.__wrapped__('Python从入门到住院')

def fac(num):
    if num in (0,1):
        return 1
    return num*fac(num-1)
print(fac(5))

def fib(n):
    if n in (1,2):
        return 1
    return fib(n-1)+fib(n-2)
for i in range(1,21):
    print(fib(i))

def fib(n):
    a,b=0,1
    for _ in range(n):
        a,b=b,a+b
    return a
print(fib(51))
"""
 
from functools import lru_cache
@lru_cache()
def fib(n):
    if n in (1,2):
        return 1
    return fib(n-1)+fib(n-2)
for i in range(1,100):
    print(fib(i))
