import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        s.connect(('192.168.1.9', 10000))
    except ConnectionRefusedError:
        time.sleep(0.5)
        print('.')
        continue
    break
while True:
    mensaje = s.recv(128)
    print(mensaje.decode())
