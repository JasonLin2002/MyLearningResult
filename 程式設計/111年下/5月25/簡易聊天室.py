import socket
import threading
name = ""
def recv(sock, addr):
    global name
    print('addr', addr)
    print('name', name)
    print('sock', sock)
    sock.sendto(name.encode('utf-8'), addr)
    while True:
        data = sock.recv(1024)
        recvMsg = data.decode('utf-8')
        print(recvMsg)

        if recvMsg.lower() == 'EXIT'.lower():
            break

def send(sock, addr):
    while True:
        string = input('')
        message = name + ' : ' + string
        data = message.encode('utf-8')
        sock.sendto(data, addr)
        if string.lower() == 'EXIT'.lower():
            break
print("--------歡迎來到聊天室，輸入'EXIT'退出聊天室--------")
name = input('請輸入你的名稱:')
print('------------------------%s----------------------- % name')
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = "127.0.0.1"
port = 2022
server = (host, port)
tr = threading.Thread(target=recv, args=(s,server), daemon=True)
ts = threading.Thread(target=send, args=(s, server))
tr.start()
ts.start()
ts.join()
s.close