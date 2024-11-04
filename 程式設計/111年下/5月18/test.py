import socket
s = socket.socket()
host = socket.gethostname()
port  = 2022
s.bind((host, port))
s.listen( 5 )

conn1, addr = s.accept()
print('Got connection from ', addr)
str = 'Thank you for connecting'
str = str.encode()
conn1.send( str )
try:
    while True:
        msg = conn1.recv( 1024 ).decode("utf-8")
        print(msg)
        if msg == 'EXIT':
            print( 'client want to disconnect!!') 
            conn1.send( 'bye bye!!'.encode())
            conn1.close()
            break
except:
    s.close()

print('Server is down!')