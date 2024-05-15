# author:jiangxinwujiangjin
# enconding = 'UTF-8'
import socket
import subprocess
#创建socket对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP协议

#绑定地址
s.bind(('127.0.0.1', 20001))

print('ready')
#进入监听状态
s.listen(5)

#从全连接队列中取出建立好的请求
conn, addr = s.accept()

#开始收发数据
while True:
    try:
        cmd = conn.recv(1024) #接收远程计算机发来的消息
    except:
        break
    if not cmd:
        break
#传入cmd命令并执行终端命令
    obj = subprocess.Popen(cmd.decode('utf-8'),shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out_res = obj.stdout.read() #windows下使用gbk编码
    out_err = obj.stderr.read() #windows下使用gbk编码


    # 固定头部长度为8字节,头部信息包含的是要发数据的大小
    data_size = len(out_res) + len(out_err)
    # 发送数据的长度（头部（固定字节））
    headers = bytes(str(data_size).encode('utf-8')).zfill(8)
    print(headers)
    conn.send(headers)
    conn.send(out_res)
    conn.send(out_err)
    print(len(out_res),len(out_err))

#关闭连接
conn.close()