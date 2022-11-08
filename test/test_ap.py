# -*- coding: utf-8 -*-


# Universidad Tecnológica Nacional - Facultad Regional Tucumán
# Proyecto Final de grado
# Sistema de Alarma contra Incendios basado en Tecnologías de IoT
# Dessarolladores:
#    + Matías Alfaro - matiasalfaro1405@gmail.com
#    + Romina Farías - romii12mf@gmail.com

import machine as m
import network
import socket
import time

#=============== definicion de constantes ======================================

WIFI_NAME = "ESP32-AP"
PASSWORD = "changeit"

PIN_LED_VERDE = 2

#============== definicion de clases ========================================

#============== definicion de funciones ========================================

#============== inicio del programa ============================================

#creacion del objeto led
led = m.Pin(PIN_LED_VERDE, m.Pin.OUT)
led.off()

ap = network.WLAN(network.AP_IF) # create access-point interface
ap.active(False)
time.sleep(1)
ap.config(essid=WIFI_NAME) # set the SSID of the access point
ap.config(password=PASSWORD)
ap.config(authmode=3)
ap.config(max_clients=10) # set how many clients can connect to the network
ap.active(True)
while ap.active() == False:
    pass

print('Connection successful')
print(ap.ifconfig())


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = ap.ifconfig()[0]
s.bind((ip, 2020))
print(ip)
s.listen(1)
(clientsocket, address) = s.accept()
print(address)

try:
    for i in range(3):
        print(".")
        time.sleep(5)
    while True:
        data= clientsocket.recv(256)
        data = data.decode()
        if len(data) > 0:
            print(data)
        if data == "sabado":
            break
        if "flama" in data: 
            print("--------------------------------------------------------------------")

finally: 
    clientsocket.close()
    s.close() 


#for i in range(10):
#    print(".")
#    time.sleep(5)