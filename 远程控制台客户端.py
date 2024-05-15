# author:jiangxinwujiangjin
# enconding = 'UTF-8'
import socket
#创建socket对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#客户端与服务端建立连接
s.connect(('127.0.0.1', 20001))

#开始收发数据
while True:
    cmd = input('请输入终端命令：').strip()
    try:
        s.send(cmd.encode('gbk'))  # 使用gbk解码
    except:
        break
    finally:
        print('发送完成')
    if not cmd:
        continue
    if cmd == 'exit':
        break
    #接收头部
    data_size = int(s.recv(8).decode('utf-8'))
    print(data_size)
    recv_size = 0
    data = b''
    while recv_size < data_size:
        res = s.recv(1024)
        recv_size += len(res)
        #累加数据
        data += res
    print(data.decode('utf-8'))
    print(len(data))