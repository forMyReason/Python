# HEADER   :
#   File     :   thread_0830.py
#   Create   :   2024/09/02
#   Author   :   LiDanyang 
#   Branch   :   lession
#   Descript :   学习使用python多线程代码存档

# Reference  :
#   1. https://xwu64.github.io/2019/12/12/Run-Multithread-Python-Program-Parallel/

# UPDATE  :
#   Last Edit  :   2024/09/02 15:35:26
#   Status     :   Need Review


import threading
import time
from multiprocessing import Process

def demo1(N):
    flag = True
    for i in range(N):
        flag = not flag
    print('end')

def test1(N):
    print("Single thread")
    demo1(N)
    demo1(N)

def test2(N):
    print("Two thread with Python threading library")
    # target表示运行函数，args表示传入的参数
    thread1 = threading.Thread(target=demo1,args=(N,))
    thread2 = threading.Thread(target=demo1,args=(N,))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

def test3(N):
    print("Two process with Python Multiprocessing library")
    p1 = Process(target=demo1,args=(N,))    # 创建进程
    p2 = Process(target=demo1,args=(N,))
    p1.start()      # 启动进程
    p2.start()
    p1.join()       # 等待进程结束
    p2.join()

t1 = time.time()
test3(int(1e9))
print(time.time() - t1)