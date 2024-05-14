# author:jiangxinwujiangjin
# enconding = 'UTF-8'
import socket
#创建socket对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(s)

#建立连接请求
s.connect(('127.0.0.1', 9999))

#传输数据(已经建立好连接)
while True:
    input_data = input('请说你要干什么:')
    s.send(input_data.encode('utf-8'))
    if input_data == 'exit':
        break
    #接收服务端发来的消息
    data = s.recv(1024)
    print(data.decode('utf-8'))

#关闭连接
s.close()