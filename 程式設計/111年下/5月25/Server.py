import socket
s = socket.socket()
host = socket.gethostname()
port = 2022
s.bind(('10.22.185.179', 2022))
s.listen(5)

conn1, addr = s.accept()
print('Got connection from ', addr)

try:
    while True:
        str = input()
        str = str.encode()
        conn1.send( str )
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