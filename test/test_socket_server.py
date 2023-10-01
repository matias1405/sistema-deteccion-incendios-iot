import socket
import time

def getIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    ip = s.getsockname()[0]
    s.close()
    return ip

ip = getIp()
#print("primera ip conseguida", ip)
ip = "192.168.0.7"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip, 2020))
print(ip)
s.listen(10)

while True: 
    COUNTER = 0
    print("while")
    (clientsocket, address) = s.accept()
    print(address)  
    try:
        while True:
            data = clientsocket.recv(128)
            data = data.decode()
            if len(data) > 0:
                print(data)
                COUNTER += 1
                print(COUNTER)
                if COUNTER > 15:
                    cadena = "STOP".encode()
                    clientsocket.send(cadena)
                else:
                    cadena = "OK".encode()
                    clientsocket.send(cadena)
        
    finally: 
        clientsocket.close()
    time.sleep(5)

s.close() 