# author:jiangxinwujiangjin
# enconding = 'UTF-8'
"""
实现TCP服务端并发，开多个进程/线程服务客户端，通过自定义一个run方法来实现不同来绑定不同的主机Ip
"""
import socket
from threading import Thread
def connect_tcp(conn): #实现通信循环
    while True:
        try:
            data = conn.recv(1024)
            if not data: # 发空问题
                break
            print(data.decode('utf-8'))
            response = input('请输入你想给客户端说的话')
            conn.send(response.encode('utf-8'))
        except:
            break
    conn.close() #结束与服务端连接的对象

def run(ip,addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip,addr))
    s.listen(8)
    while True: #每获取一个请求，就开一个线程
        conn, addr = s.accept() #获取连接对象
        Thread(target=connect_tcp, args=(conn,)).start()

if __name__ == '__main__':
    ip = '127.0.0.1'
    addr = 10001
    run(ip,addr)
