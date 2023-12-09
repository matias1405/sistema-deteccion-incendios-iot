import socket
import utime
import machine as m
import network
import math
import random
import urequests


SSID = ["MOVISTAR WIFI2276", "Galaxy S23 FE 3B0E", "ALFARO"]
PASSWORD = ["romi1234", "1234matias", "MATIAS64P13"]
SERVER_IP = ['172.20.1.10', '192.168.102.10', '192.168.100.10']
PORT = 2020

sta_if = network.WLAN(network.STA_IF)
utime.sleep(2)
sta_if.active(False)
utime.sleep(2)
sta_if.active(True)
utime.sleep(2)

for i in range(3):
    try:
        if sta_if.isconnected():
            break
        print("red_: ", SSID[i])
        sta_if.connect(SSID[i], PASSWORD[i])
        # Espera a que se establezca la conexión WiFi
        tiempo_inicial = utime.time()
        red = i
        while not sta_if.isconnected() and utime.time() - tiempo_inicial < 10:
            print(".")
            utime.sleep_ms(200)
        if not sta_if.isconnected():
            sta_if.active(False)
            utime.sleep(2)
            sta_if.active(True)
            utime.sleep(2)    
    except Exception as e:
        print(e)
        
print("red: ", SSID[red])
# Si no se logra conectar, se desactiva el modo WiFi
if not sta_if.isconnected():
    print('No se pudo conectar al WiFi')
    sta_if.active(False)

print('network config:', sta_if.ifconfig())
ip = sta_if.ifconfig()[0]

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
            try:
                data = clientsocket.recv(128)
                data = data.decode()
                if len(data) > 0:
                    print(data)
                    url = f"http://ec2-18-231-161-247.sa-east-1.compute.amazonaws.com:1880/sensores?temperatura={float(data)}&humo=62400&pdf=1"
                    response = urequests.get(url)
                    print(response.text)
                    COUNTER += 1
                    print(COUNTER)
                    if COUNTER > 15:
                        cadena = "STOP".encode()
                        clientsocket.send(cadena)
                    else:
                        cadena = "OK".encode()
                        clientsocket.send(cadena)
            except OSError as e:
                print(e)
    finally: 
        clientsocket.close()
    utime.sleep(5)

s.close() 