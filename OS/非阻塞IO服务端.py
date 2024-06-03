# author:jiangxinwujiangjin
# enconding = 'UTF-8'
"""
非阻塞I/O模型（NOBlockingIOModel）会把socket对象的recv,accept等方法从阻塞变成非阻塞，长期占用CPU资源，CPU长期处于空转状态，CPU资源利用率低
"""
import socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #避免端口占用
server.bind(('127.0.0.1', 8080))
server.listen(5)
server.setblocking(False) #用于设置socket的阻塞模式

c_list = []
d_list = []

while True:
    try:
        client, address = server.accept()
        c_list.append(client)
    except BlockingIOError: #以下的子程序是没有拿到连接对象和地址时做的事情
        for conn in c_list:
            try:
                data = conn.recv(1024) #阻塞报错也是BlockingIOError
                if not data: #如果发送数据为空，断开与客户端的连接
                    conn.close()
                    d_list.append(data)
                conn.send(data.upper()) #这里是给客户端发送数据的子程序部分
            except BlockingIOError:
                pass #继续从列表里拿连接对象进行处理
            except ConnectionResetError: #客户端异常断开连接（windows系统出现的问题）
                conn.close()
                d_list.append(conn)
            for conn in d_list:
                c_list.remove(conn)
            d_list.clear()
