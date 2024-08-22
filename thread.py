# lession branch

import threading
import time
# threading 和 thread 啥区别？
from queue import Queue

def thread_job():
    print("1111")

def job(list,q):
    for i in range(len(list)):
        list[i] = list[i] ** 2
    # return list
    q.put(list)

# 多线程中，线程是不能返回一个值的
def multithreading():
    # 定义一个Queue
    q = Queue()     # 之后要在Queue中放入一个返回值，替代return的功能
    threads = []
    data=[[1,2,3],[3,4,5],[4,4,4],[5,5,5]]
    for i in range(4):
        t = threading.Thread(target=job , args= (data[i] , q))
        t.start()
        threads.append(t)
    for thread in threads:
        # 等到所有线程运行完成
        thread.join()
    result = []
    for _ in range(4):
        #从队列中按顺序拿出一个
        result.append(q.get())
    print(result)

# def main():
#     added_thread = threading.Thread(target=thread_job)
#     added_thread.start()
#     added_thread.join()
#     print(threading.active_count())
#     print(threading.enumerate())
#     print(threading.current_thread())

if __name__ == '__main__':
    multithreading()



# 【100秒学会Python多线程threading】 https://www.bilibili.com/video/BV1Pm4y1J7b8/
# import time
# import threading

# def worker(name):
#     for i in range(5):
#         print(name,i)
#         time.sleep(0.5)

# name 是啥？
# t1 = threading.Thread(target=worker,args=('A', ))
# t2 = threading.Thread(target=worker,args=('B', ))
# t1.start()
# t1.join()       # 等待某线程执行完成之后再往下运行
# t2.start()
# # worker("B")
# print("完成")