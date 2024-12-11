import socket
import time
s = socket.socket()
host = socket.gethostname()
port = 2022
s.connect((host, port))
print(s.recv (1024))
s.send('Hi, I am Jack'.encode()) 
time.sleep( 5 )
s.send('EXIT'.encode() )
time.sleep( 2)
print(s.recv (1024).decode("utf-8" ) )
#time.sleep( 5 )
s.close()