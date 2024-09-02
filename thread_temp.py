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

class MyProcess(Process):
    def __init__(self,arg):
        super(MyProcess,self).__init__()
        self.arg = arg
    # Process继承并覆盖run()
    def run(self):
        print('say hi',self.arg)
        time.sleep(1)

if __name__ == '__main__':
    for i in range(10):
        p = MyProcess(i)
        p.start()
        p.join()
