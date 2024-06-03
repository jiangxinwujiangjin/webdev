#异步回调机制
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
import time
import os 
pool = ProcessPoolExecutor(4)#不传参的话，默认开设的进程数量是当前cpu的核数
def task(name):
    print(name,os.getpid()) 
    time.sleep(2) # 模拟I/O阻塞
    return name + 10

def call_back(res): #任务完成后立即执行的操作
    print('call back',res.result())

if __name__ == '__main__':
    #往进程池里提交任务
    for i in range(20):
        future = pool.submit(task,i) #往任务队列中添加任务，submit后会立即返回future对象
        future.add_done_callback(call_back) #添加回调函数（自动把完成的future传进去）
    pool.shutdown(wait=True) #等待pool中的Process/Thread执行完成并关闭