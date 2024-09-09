# HEADER   :
#   File     :   thread_temp.py
#   Create   :   2024/09/02
#   Author   :   LiDanyang 
#   Branch   :   lession
#   Descript :   Python3的multiprocessing多进程


# Reference  :
#   1. https://www.cnblogs.com/lizm166/p/14658484.html

# UPDATE  :
#   Last Edit  :   2024/09/02 15:37:13
#   Status     :   Coding

from multiprocessing import Process
import time

# class MyProcess(Process):
#     def __init__(self,arg):
#         super(MyProcess,self).__init__()
#         self.arg = arg
#     # Process继承并覆盖run()
#     def run(self):
#         print('say hi',self.arg)
#         time.sleep(1)

# if __name__ == '__main__':
#     for i in range(10):
#         p = MyProcess(i)
#         p.start()
#         p.join()


# 例子1
# def foo(i):
#     print('say hi', i)
#     time.sleep(1)

# time0 = time.time()
# if __name__ == '__main__':
#     for i in range(5):
#         p = Process(target=foo, args=(i,))
#         p.start()
#         p.join()
# print("--" + str(time.time()-time0))
# 因为两个线程是并列的，所以每次执行执行主线程都会 print 一次


## 例子2
def foo(i):
    print('say hi', i)
    time.sleep(1)

if __name__ == '__main__':
    p_list = []
    for i in range(10):
        p = Process(target=foo,args=(i,))
        p.daemon = True     #守护进程，看不懂
        p_list.append(p)

    for p in p_list:
        p.start()
    for p in p_list:
        p.join()

    print("main process end")