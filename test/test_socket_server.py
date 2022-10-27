import socket
def getIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    ip = s.getsockname()[0]
    s.close()
    return ip

ip = getIp()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip, 2020))
print(ip)
s.listen(1)
(clientsocket, address) = s.accept()
print(address)

try:
    while True:
        data= clientsocket.recv(256)
        if len(data.decode()) > 0:
            print(data.decode())
        if data == "sabado":
            break

finally: 
    clientsocket.close()
    s.close()      
