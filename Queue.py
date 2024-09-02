# HEADER   :
#   File     :   thread.py
#   Create   :   2024/09/02
#   Author   :   LiDanyang 
#   Branch   :   lession
#   Descript :   由于线程是不能返回值的，所以使用Queue来存储返回值

# UPDATE  :
#   Last Edit  :   2024/09/02 15:22:18
#   Status     :   Reviewing

import threading
import time
from queue import Queue

def job(list,q):
    for i in range(len(list)):
        list[i] = list[i] ** 2
    # return list
    q.put(list)

# 多线程中，线程是不能返回一个值的，所以使用Queue来存储返回值
def multithreading():
    q = Queue()     # 之后要在Queue中放入一个返回值，替代return的功能
    threads = []    # 线程组
    data=[[1,2,3],[3,4,5],[4,4,4],[5,5,5]]
    for i in range(4):
        t = threading.Thread(target=job , args= (data[i] , q))
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()        # 等到所有线程运行完成
    result = []
    for _ in range(4):
        #从队列中按顺序拿出并放入result中
        result.append(q.get())
    print(result)

if __name__ == '__main__':
    multithreading()