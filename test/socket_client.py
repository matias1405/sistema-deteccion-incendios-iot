import socket
import time
import random

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        #s.connect(('192.168.135.67', 2020)) #romi
        s.connect(('192.168.102.10', 2020)) 
    except ConnectionRefusedError:
        time.sleep(0.5)
        print('.')
        continue
    break
while True:
    temperatura = random.randint(1, 100)
    humo = random.randint(100, 10000)
    pdf = random.randint(0,1)
    #mensaje = f'{temperatura}'
    mensaje = f'humo={humo}&temperatura={temperatura}&pdf={pdf}'
    print(mensaje)
    s.send(mensaje.encode())
    time.sleep(10)
