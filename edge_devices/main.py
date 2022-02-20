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

NRO_DISPOSITIVO = 1

#Pines analogicos
PIN_SFLAMA = 32
PIN_BATERIA = 33
PIN_SHUMO = 34
PIN_STEMPERATURA = 35
#Pines digitales
PIN_LED_VERDE = 36

WIFI_NAME = "WIFI_SIST_P_INCENDIOS"
PASSWORD = "MANCHITA14"
ADDRS = ('192.168.0.14', 2020)

TIEMPO_PUB = 60
TEMP_MAX = 57
VEL_AUMENT_TEMP_MAX = 8.3
FLAMA_MAX = 616842138483
TENSION_BATERIA_MIN = 3.1

#============== definicion de clases ========================================

class Cola_Temperatura:
    def __init__(self):
        self.lista_temp = []

    def medir():
        temp = s_temperatura.read_uv() #valor en uvoltios
        self.medir_cambio(temp/10000)  #temperatura en °C

    def add(self, temp):
        self.lista_temp.append(temp)

    def remove(self):
        self.lista_temp.pop(0)

    def medir_cambio(self, temp):
        self.add(temp)
        if len(self.lista_temp) > 3:
            self.remove()
        if len(self.lista_temp) >= 3:
            cambio = (self.lista_temp[2]-self.lista_temp[0])
            if cambio > VEL_AUMENT_TEMP_MAX:
                estado.temperatura(True)
            elif self.lista_temp[2] > TEMP_MAX:
                estado.temperatura(True)
            else:
                estado.temperatura(False)


class Estado:
    def __init__(self)
        self.list_estado = [False, False, False]
        self.estado_bateria = True

    def temperatura(self, x):
        self.list_estado[0] = x

    def flama(self, x):
        self.list_estado[1] = x

    def humo(self, x):
        self.list_estado[2] = x

    def bateria(x):
        self.estado_bateria = x


#============== definicion de funciones ========================================

def medir_flama():
    tamaño = s_flama.read()


def medir_humo():
    humo = s_humo.read()


def medir_bateria():
    carga = s_bateria.read()
    tension_bateria = carga * 3.3 / 4096
    if tension_bateria <= TENSION_BATERIA_MIN:
        estado.estado_bateria(False)
    else:
        estado.estado_bateria(True)


def verificar():
    suma = sum(self.list_estado)
    if suma >= 2:
        incendio()
    if not estado.estado_bateria:
        bateria_baja()


def incendio():
    pass


def bateria_baja():
    pass


#============== inicio del programa ============================================

#creacion del objeto led
led = Pin(PIN_LED_VERDE, Pin.OUT)
led.off()

#conexion al wifi, si no hay conexion despues de 6 segundos empieza el led a
#parpadear
wf = network.WLAN(network.STA_IF)
wf.active(True)
wf.connect(WIFI_NAME, PASSWORD)
count = 0
while not wf.isconnected():
    time.sleep(0.5)
    count += 1
    if count > 12:
        led.value(count%2)

#creo el socket cliente, si la conexion es exitosa enciende el led por 3 seg
s = socket.socket()
while True:
    try:
        s.connect(ADDRS)
    except ConnectionRefusedError:
        time.sleep(0.5)
        continue
    break
led.on()
time.sleep(3)
led.off()

#creacion de los objetos para los sensores
s_flama = m.ADC(Pin(PIN_SFLAMA))
s_flama.atten(m.ADC.ATTN_11DB)
s_humo = m.ADC(Pin(PIN_SHUMO))
s_humo.atten(m.ADC.ATTN_11DB)
s_temperatura = m.ADC(Pin(PIN_STEMPERATURA))
s_temperatura.atten(m.ADC.ATTN_2_5DB)
s_bateria = m.ADC(Pin(PIN_BATERIA))
s_bateria.atten(m.ADC.ATTN_11DB)

estado = Estado()
temperatura = Cola_Temperatura()


while(True):
    time.sleep(TIEMPO_PUB/2)
    temperatura.medir()
    time.sleep(TIEMPO_PUB/2)
    temperatura.medir()
    medir_flama()
    medir_humo()
    medir_bateria()
    verificar()
