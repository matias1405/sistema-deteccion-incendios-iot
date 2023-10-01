import socket
import time
import random

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        s.connect(('192.168.0.5', 2020))
    except ConnectionRefusedError:
        time.sleep(0.5)
        print('.')
        continue
    break
while True:
    temperatura = random.randint(1, 100)
    humo = random.randint(100, 10000)
    mensaje = f'temperatura={temperatura}&humo={humo}'
    print(mensaje)
    s.send(mensaje.encode())
