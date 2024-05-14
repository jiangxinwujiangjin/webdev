# author:jiangxinwujiangjin
# enconding = 'UTF-8'
import socket
#创建socket对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#绑定地址(服务端) 127.0.0.1是回环地址，只能本机测试使用 0.0.0.0：本机所有Ip
s.bind(('127.0.0.1', 9999))
#监听请求连接 listen状态：无半连接请求
s.listen(5)
print('waiting for a connection')
#取出连接请求（从全连接队列中取出），开始服务
conn, addr = s.accept()
print('Connected object', conn)
print('Address', addr)
#数据传输,接收客户端传来的数据（通过循环来多次通信）
while True:
    try:
        data = conn.recv(1024)
    except:
        break
    print('客户端发来的数据',data.decode('utf-8'))
    # 服务器发送消息给客户端
    conn.send('你好啊，我们建立了连接请求了啊'.encode('utf-8'))

#结束服务
conn.close()