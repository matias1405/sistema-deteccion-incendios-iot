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

#============== definicion de clases ========================================

#============== definicion de funciones ========================================

#============== inicio del programa ============================================

#creacion del objeto led
led = m.Pin(PIN_LED_VERDE, m.Pin.OUT)
led.off()

ap = network.WLAN(network.AP_IF) # create access-point interface
ap.config(ssid=WIFI_NAME) # set the SSID of the access point
ap.config(key=PASSWORD)
ap.config(max_clients=10) # set how many clients can connect to the network
ap.active(True)
print(ap.ifconfig())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.close()


