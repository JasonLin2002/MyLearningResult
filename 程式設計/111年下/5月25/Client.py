import socket
import time
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 2022
s.connect(('10.22.185.163', port))
print(s.recv(1024))
s.send('你媽在地板上抽'.encode()) 
time.sleep( 5 )
x=input()
s.send(x.encode())
time.sleep( 2 )
print(s.recv(1024).decode("utf-8"))
#time.sleep( 5 )
s.close()