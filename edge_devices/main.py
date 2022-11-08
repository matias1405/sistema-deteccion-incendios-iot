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
import math

#=============== definicion de constantes ======================================

ID_DISPOSITIVO = 1

#Pines analogicos
PIN_STEMPERATURA = 35 #gpio 35 y pin nro 6 
PIN_SHUMO = 34 #gpio 34 y pin nro 5 
PIN_SFLAMA = 22 #gpio 22 y pin nro 36
PIN_SBATERIA = 33  #en discusion si agregar el circuito o no
#Pines digitales
PIN_LED_VERDE = 2 #led integrado en la placa del esp32

WIFI_NAME = "ESP32-AP"
PASSWORD = "changeit"
ADDRS = ('192.168.4.1', 2020)
TIEMPO_PUB = 6
TEMP_MAX = 57
VEL_AUMENT_TEMP_MAX = 8.3
TENSION_BATERIA_MIN = 3.1

#============== definicion de clases ========================================

class SensorTemperatura:
    """
    Mide temperaturas en grados centigrados y los almacena en listas.
    lista_temp[0] es temperatura hace un minuto
    lista_temp[1] es temperatiura hace 30 segundos
    lista_temp[2] es la temperatura actual
    Tambien mide el cambio de temperatura en un minuto y la temperatura actual
    """
    def __init__(self, n_pin):

        self.pin_s_temperatura = m.ADC(m.Pin(n_pin, m.Pin.IN))
        self.pin_s_temperatura.atten(m.ADC.ATTN_2_5DB)
        temp_inicial = self.pin_s_temperatura.read_uv()/10000
        self.lista_temp = [temp_inicial, temp_inicial, temp_inicial]

    def medir(self):
        self.temp = self.pin_s_temperatura.read_uv()/10000
        time.sleep(1)
        self.temp += self.pin_s_temperatura.read_uv()/10000
        time.sleep(1)
        self.temp += self.pin_s_temperatura.read_uv()/10000
        self.medir_cambio(self.temp/3)  #temperatura en °C
        


    def add(self, temp):
        self.lista_temp.append(temp)

    def remove(self):
        self.lista_temp.pop(0)

    def medir_cambio(self, temp):
        self.add(temp)
        self.remove()
        #lista_temp[0] es temperatura hace un minuto
        self.cambio = (self.lista_temp[2]-self.lista_temp[0])
        if self.cambio > VEL_AUMENT_TEMP_MAX:
            estado.temperatura(True)
        elif self.lista_temp[2] > TEMP_MAX:
            estado.temperatura(True)
        else:
            estado.temperatura(False)
        #prueba con read
        #self.temp_analog = self.pin_s_temperatura.read()#* 3.3 / 4096
        #max = 11.158*(self.temp_analog**(-0.274))
        #xself.temp_analog= self.temp_analog/4095*max

class SensorHumo:
    """
    Mide la concentracion de humo en ppm
    """
    def __init__(self, n_pin):
        self.pin_s_humo = m.ADC(m.Pin(n_pin, m.Pin.IN))
        self.pin_s_humo.atten(m.ADC.ATTN_11DB)
        self.calculos()
        self.medir_humo()

    def calculos(self):
        voltaje_i = self.pin_s_humo.read_uv()/1000000
        #voltaje_i = voltaje_i * 3.3 / 4096
        self.R0 = 1000 * (5 - voltaje_i) / voltaje_i
        self.R0 = self.R0 / 9.7
        self.x1 = math.log10(200)
        self.y1 = math.log10(3.43)
        x2 = math.log10(10000)
        y2 = math.log10(0.61)
        self.curva = (y2 - self.y1)/(x2 - self.x1)

    
    def medir_humo(self):
        voltaje_i = self.pin_s_humo.read_uv()/1000000
        RS = 1000 * (5 - voltaje_i) / voltaje_i
        ratio = RS/self.R0
        exponente = (math.log10(ratio)-self.y1)/self.curva
        exponente = exponente + self.x1
        self.ppm = 10**exponente



class SensorFlama:
    """
    Detecta la presencia de flama
    """
    def __init__(self, n_pin):
        self.pin_s_flama = m.Pin(n_pin, m.Pin.IN) 
        self.presencia_flama = False

    def medir_flama(self):
        self.presencia_flama = self.pin_s_flama.value()
        if(self.presencia_flama == 1):
            estado.flama(False)
        else:
            estado.flama(True)


class Bateria:
    """
    Mide el nivel de tension de la bateria e informa si es baja
    """
    def __init__(self, n_pin):
        self.pin_s_bateria = m.ADC(m.Pin(n_pin, m.Pin.IN))
        self.pin_s_bateria.atten(m.ADC.ATTN_11DB)
        self.medir_bateria()

    def medir_bateria(self):
        self.carga = self.pin_s_bateria.read()
        self.tension_bateria = self.carga * 3.3 / 4096
        if self.tension_bateria <= TENSION_BATERIA_MIN:
            estado.bateria(False)
        else:
            estado.bateria(True)


class Estado:
    """
    almacena dos lista: la primera almacena el estado dado por los ssensores
    de temperatura, flama y humo.
    la segunda lista almacena el estado de la bateria. 
    """
    def __init__(self):
        self.lista_estado = [False, False, False]
        self.estado_bateria = True
        self.suma = 0

    def temperatura(self, x):
        self.lista_estado[0] = x

    def flama(self, x):
        self.lista_estado[1] = x

    def humo(self, x):
        self.lista_estado[2] = x

    def bateria(self, x):
        self.estado_bateria = x
    
    def verificar(self):
        self.suma = sum(self.lista_estado)
        if self.suma >= 2:
            incendio()
        if not self.estado_bateria:
            bateria_baja()
        self.notificar()

    def notificar(self):
        string_temperatura_0 = f'temperatura_0: {s_temperatura.lista_temp[0]:.2f}'
        s.send(string_temperatura_0.encode())
        time.sleep(1)
        string_temperatura_1 = f'temperatura_1: {s_temperatura.lista_temp[1]:.2f}'
        s.send(string_temperatura_1.encode())
        time.sleep(1)
        string_temperatura_2 = f'temperatura_2: {s_temperatura.lista_temp[2]:.2f}'
        s.send(string_temperatura_2.encode())
        time.sleep(1)
        string_humo = f'ppm de humo en el aire: {s_humo.ppm:.2f}'
        s.send(string_humo.encode())
        time.sleep(1)
        string_flama = f'presencia de flama: {estado.lista_estado[1]}'
        s.send(string_flama.encode())
        #time.sleep(1)
        #string_bateria = f'bateria: {s_bateria.tension_bateria}'
        #s.send(string_bateria.encode())
        #print(self.lista_estado)
        #print(self.estado_bateria)

#============== definicion de funciones ========================================

def incendio():
    pass


def bateria_baja():
    pass


#============== inicio del programa ============================================

#creacion del objeto led
led = m.Pin(PIN_LED_VERDE, m.Pin.OUT)
led.off()

#conexion al wifi, si no hay conexion despues de 6 segundos empieza el led a
#parpadear

wf = network.WLAN(network.STA_IF)
wf.active(False)
time.sleep(1)
wf.active(True)
if not wf.isconnected():
    print('connecting to network...')
    wf.connect(WIFI_NAME, PASSWORD)
    count = 0
    while not wf.isconnected():
        time.sleep(0.5)
        count += 1
        if count > 12:
            led.value(count%2)

print('network config:', wf.ifconfig())
#creo el socket cliente
s = socket.socket()

led.on()
time.sleep(1)

s.connect(ADDRS)

led.off()

estado = Estado()

#creacion de los objetos para los sensores
s_temperatura = SensorTemperatura(PIN_STEMPERATURA)
time.sleep(1)
print("sensor de temperatura creado")
s_humo = SensorHumo(PIN_SHUMO)
time.sleep(1)
s_flama = SensorFlama(PIN_SFLAMA)
time.sleep(1)
s_bateria = Bateria(PIN_SBATERIA)
print("sensor de bateria creado")
led.on()

while True:
    print(".")
    time.sleep(TIEMPO_PUB/2) 
    s_temperatura.medir()
    s_humo.medir_humo()
    s_flama.medir_flama()
    s_bateria.medir_bateria()
    print(".")
    time.sleep(TIEMPO_PUB/2)
    s_temperatura.medir()
    estado.verificar()


