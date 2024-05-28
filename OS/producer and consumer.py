# author:jiangxinwujiangjin
# enconding = 'UTF-8'
from multiprocessing import Process,Queue,Lock,JoinableQueue
import time
import random

"""
JoinableQueue在Queue的基础上添加了一个程序计数器（队列中数据的个数），每往队列put数据，计数器+1，
调用一次task_done()。计数器-1
当计数器为0时，就会走join（）后的代码
"""


def producer(name,food,q): #生产者：制造数据，并把数据往消息队列中放
    for i in range(8):
        time.sleep(random.randint(1,3))
        print(f'producer{name}is producing {food}{i}')
        q.put(f'{food}{i}') #往消息队列里添加数据
        print(q,type(q))

def consumer(name,q): #x消费者，处理数据，往消息队列里拿数据处理
    while True:
        food = q.get()  #get()方法会阻塞，等待队列中有新数据传入然后继续从队列中拿数据
        time.sleep(random.randint(1,3))
        print(f'consumer{name}is consuming {food}')
        q.task_done() #计数器-1
        if food == 'cookies is over':
            break

#消息队列：媒介


if __name__ == '__main__':
    q = JoinableQueue()
    p1= Process(target=producer, args=('塔兹米','艇仔粥',q))
    p2 = Process(target=producer, args=('玛英','辣椒炒肉',q))
    c1 = Process(target=consumer, args=('杨锦添',q))
    c2 = Process(target=consumer,args=('克劳德',q))
    p1.start()
    p2.start()
    c1.start()
    c2.start()
    c1.daemon = True #因为消费者进程中get()方法会阻塞，所以要将消费者设置为守护进程，当主进程结束时消费者进程跟着结束
    c2.daemon = True

    p1.join() #防止消费者处理数据过快而生产者生产数据慢导致队列为空直接走q.join()
    p2.join()
    #q.put('cookies is over') #结束消费者（有多少个消费者就要put 'cookies is over'多少次）
    q.join() #结束主进程，生产者进程



