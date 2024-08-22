import threading

def job_1():
    global A,lock
    lock.acquire()      # 锁上
    for i in range(10):
        A += 1
        print('job_1',A)
    lock.release()      # 解锁

def job_2():
    global A,lock
    lock.acquire()      # 锁上
    for i in range(10):
        A += 10
        print('---------job_2',A)
    lock.release()

if __name__ == '__main__':
    lock = threading.Lock()
    A = 0
    t1 = threading.Thread(target=job_1)
    t2 = threading.Thread(target=job_2)

    t1.start()
    t2.start()
    t1.join()
    t2.join()

# 使用进程锁之后，单独执行某一线程