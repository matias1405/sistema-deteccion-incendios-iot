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

ID_DISPOSITIVO = 1

#Pines analogicos
PIN_SFLAMA = 22
PIN_BATERIA = 33
PIN_SHUMO = 34
PIN_STEMPERATURA = 35
#Pines digitales
PIN_LED_VERDE = 2

WIFI_NAME = "WiFi-Arnet-6jbs"
PASSWORD = "j3ygefpf"
ADDRS = ('192.168.0.14', 2020)

TIEMPO_PUB = 60
TEMP_MAX = 57
VEL_AUMENT_TEMP_MAX = 8.3
FLAMA_MAX = 616842138483
TENSION_BATERIA_MIN = 3.1

#============== definicion de clases ========================================

class Cola_Temperatura:
    """Pila de temperaturas en grados centigrados.
    lista_temp[0] es temperatura hace un minuto
    lista_temp[1] es temperatiura hace 30 segundos
    lista_temp[1] es la temperatura actual
    mide el cambio de temperatura en un minuto y la temperatura actual"""
    def __init__(self):
        self.lista_temp = []

    def medir(self):
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
        if len(self.lista_temp) >= 3: #lista_temp[0] es temperatura hace un minuto
            cambio = (self.lista_temp[2]-self.lista_temp[0])
            if cambio > VEL_AUMENT_TEMP_MAX:
                estado.temperatura(True)
            elif self.lista_temp[2] > TEMP_MAX:
                estado.temperatura(True)
            else:
                estado.temperatura(False)


class Estado:
    """
    alamcena dos lista: la primera almacena el estado dado por los ssensores
    de temperatura, flama y humo.
    la segunda lista almacena el estado de la bateria. 
    """
    def __init__(self):
        self.list_estado = [False, False, False]
        self.estado_bateria = True
        self.suma = 0

    def temperatura(self, x):
        self.list_estado[0] = x

    def flama(self, x):
        self.list_estado[1] = x

    def humo(self, x):
        self.list_estado[2] = x

    def bateria(self, x):
        self.estado_bateria = x
    
    def verificar(self):
        self.suma = sum(self.list_estado)
        if self.suma >= 2:
            incendio()
        if not self.estado_bateria:
            bateria_baja()


#============== definicion de funciones ========================================

def medir_flama():
    pass
    #tamaño = s_flama.read()


def medir_humo():
    #humo = s_humo.read()
    pass

def medir_bateria():
    """
    mide la carga de la bateria, si la carga baja de cierto valor cambia el valor de la lista 
    de estado de bateria.
    """
    carga = s_bateria.read()
    tension_bateria = carga * 3.3 / 4096
    if tension_bateria <= TENSION_BATERIA_MIN:
        estado.estado_bateria(False)
    else:
        estado.estado_bateria(True)





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
wf.active(True)
wf.connect(WIFI_NAME, PASSWORD)
count = 0
while not wf.isconnected():
    time.sleep(0.5)
    count += 1
    if count > 12:
        led.value(count%2)
"""
#creo el socket cliente, si la conexion es exitosa enciende el led por 3 seg
s = socket.socket()
while True:
    try:
        s.connect(ADDRS)
    except ConnectionRefusedError:
        time.sleep(0.5)
        continue
    break
"""
led.on()

#creacion de los objetos para los sensores
s_flama = m.ADC(m.Pin(PIN_SFLAMA))
s_flama.atten(m.ADC.ATTN_11DB)
s_humo = m.ADC(m.Pin(PIN_SHUMO))
s_humo.atten(m.ADC.ATTN_11DB)
s_temperatura = m.ADC(m.Pin(PIN_STEMPERATURA))
s_temperatura.atten(m.ADC.ATTN_2_5DB)
s_bateria = m.ADC(m.Pin(PIN_BATERIA))
s_bateria.atten(m.ADC.ATTN_11DB)

time.sleep(3)
led.off()

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
    estado.verificar()
