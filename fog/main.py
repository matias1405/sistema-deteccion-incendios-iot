# -*- coding: utf-8 -*-


# Universidad Tecnológica Nacional - Facultad Regional Tucumán
# Proyecto Final de grado
# Sistema de Alarma contra Incendios basado en Tecnologías de IoT
# Dessarolladores:
#    + Matías Alfaro - matiasalfaro1405@gmail.com
#    + Romina Farías - romii12mf@gmail.com

import socket
import utime
import machine as m
import network
import math
import random
import urequests
from gpio_lcd import GpioLcd

#=============== definicion de constantes ======================================

SSID = ["ESP 32", "ESP 32", "ALFARO"]
PASSWORD = ["romi1234", "1234matias", "MATIAS64P13"]
SERVER_IP = ['192.168.135.10', '192.168.102.10', '192.168.100.10']
GATEWAY = ['192.168.135.194', '192.168.102.163', '192.168.100.1']

PORT = 2020

URL_BASE = "http://ec2-18-231-161-247.sa-east-1.compute.amazonaws.com:1880/"

#============== definicion de clases ========================================

class Estado:
    """
    almacena dos lista: la primera almacena el estado dado por los ssensores
    de temperatura, flama y humo.
    """
    def __init__(self):
        self.lista_estado = [False, False, False]
        self.situacion_incendio = False

    def temperatura(self, x):
        self.lista_estado[1] = x

    def flama(self, x):
        self.lista_estado[2] = x

    def humo(self, x):
        self.lista_estado[0] = x
    
    def evaluar(self):
        if sum(self.lista_estado) >= 1:
            if not self.situacion_incendio:
                self.situacion_incendio = True
                url = URL_BASE + f'estado?estado=INCENDIO'
                print(url)
                response = urequests.get(url)
                print(response.text)
        else:
            if self.situacion_incendio:
                self.situacion_incendio = False
                url = URL_BASE + f'estado?estado=OK'
                print(url)
                response = urequests.get(url)
                print(response.text)


#============== definicion de funciones ========================================

def imprimir(cadena, x=0, y=0, limpiar=True):
    if limpiar:
        lcd.clear()
    lcd.move_to(x,y)
    lcd.putstr(cadena)
    utime.sleep(0.2)

#============== inicio del programa ============================================

lcd = GpioLcd(rs_pin=m.Pin(14),
              enable_pin=m.Pin(13),
              d4_pin=m.Pin(32),
              d5_pin=m.Pin(25),
              d6_pin=m.Pin(27),
              d7_pin=m.Pin(26),
              num_lines=2, num_columns=16)

imprimir("Iniciando...", 0, 0, True)

sta_if = network.WLAN(network.STA_IF)
utime.sleep(1)
sta_if.active(False)
utime.sleep(1)
sta_if.active(True)
utime.sleep(1)

imprimir("Conectando...", 0, 0, True)

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
            utime.sleep(1)
            sta_if.active(True)
            utime.sleep(1)    
    except Exception as e:
        print(e)
        

# Si no se logra conectar, se desactiva el modo WiFi
if not sta_if.isconnected():
    imprimir("No se pudo\nconectar al WiFi", 0, 0, True)
    sta_if.active(False)
else:
    print("red: ", SSID[red])
    imprimir("Red conectada", 0, 0, True)
    imprimir(SSID[red], 0, 1, False)
    utime.sleep(3)

print(sta_if.ifconfig())
configuracion = sta_if.ifconfig()
estado = Estado()

if SERVER_IP[red] != configuracion[0]:
    sta_if.ifconfig((SERVER_IP[red], configuracion[1], configuracion[2], configuracion[3]))
    utime.sleep(3)
nueva_configuracion = sta_if.ifconfig()
ip = nueva_configuracion[0]
imprimir(ip, 0, 0, True)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((ip, 2020))
    print(ip)
    s.listen(10)
    while True:
        (clientsocket, address) = s.accept()
        print(address)  
        imprimir("Cliente \nconectado", 0, 0, True)
        try:
            while True:
                data = clientsocket.recv(128)
                data = data.decode()
                #print("data: ", data)
                if len(data) > 0:
                    medidas = data.split("&")
                    if float(medidas[1]) > 58: #temperatura
                        estado.temperatura(True)
                    else:
                        estado.temperatura(False)
                    #print(".")
                    if int(medidas[0]) > 1000: #humo
                        estado.humo(True)
                    else:
                        estado.humo(False)
                    #print(".")
                    if int(medidas[2]): #pdf
                        cadena = f"T:{medidas[1]}^C  Pdf:SI"
                        estado.flama(True)
                    else:
                        cadena = f"T:{medidas[1]}^C  Pdf:NO"
                        estado.flama(False)
                    #print(".")
                    imprimir(cadena, 0, 0, True)   
                    cadena = f'Humo:{medidas[0]} ppm'
                    imprimir(cadena, 0, 1, False)
                    url = URL_BASE + f'sensores?humo={medidas[0]}&temp={medidas[1]}&pdf={medidas[2]}'
                    #print(url)
                    response = urequests.get(url)
                    #print(response.text)
                    estado.evaluar()
                    if estado.situacion_incendio:
                        cadena = "INCENDIO".encode()
                        clientsocket.send(cadena)
                    else:
                        cadena = "OK".encode()
                        clientsocket.send(cadena)
                    #print("....")
        except Exception as e:
            print(e) 
        finally:
            clientsocket.close()
            imprimir("Cliente \nno conectado", 0, 0, True)
            utime.sleep(1)
finally:
    s.close() 

