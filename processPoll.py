# HEADER   :
#   File     :   processPoll.py
#   Create   :   2024/09/03
#   Author   :   LiDanyang 
#   Branch   :   lession
#   Descript :   学习进程池

from multiprocessing import Pool , cpu_count
import os
import time

def long_time_task(i):
    print('子进程：{}'.format(os.getpgid() , i))
    time.sleep(2)
    print("结果: {}".format(8 ** 20))


if __name__=='__main__':
    print("CPU内核数:{}".format(cpu_count()))
    print('当前母进程: {}'.format(os.getpid()))

    start = time.time()
    p = Pool(4)

    for i in range(5):
        p.apply_async(long_time_task,args=(i,))
        # 向进程池提交需要执行的函数与参数

    print('等待所有子进程完成')

    # 关闭进程池，使其不接受新任务
    p.close()

    # 主进程阻塞等待子进程的退出，等待所有子进程执行完毕
    p.join()

    end = time.time()

    print("总共用时{}秒".format((end-start)))

