# Universidad Tecnológica Nacional - Facultad Regional Tucumán
# Proyecto Final de grado
# Sistema de Alarma contra Incendios basado en Tecnologías de IoT
# Dessarolladores:
#    + Matías Alfaro - matiasalfaro1405@gmail.com
#    + Romina Farías - romii12mf@gmail.com

from cgi import print_environ_usage
import machine as m
import network
import socket
import time
import math

#=============== definicion de constantes ======================================

ID_DISPOSITIVO = 1

#Pines analogicos
PIN_STEMPERATURA = 35
PIN_SHUMO = 34
PIN_SFLAMA = 22
PIN_SBATERIA = 33
#Pines digitales
PIN_LED_VERDE = 2

WIFI_NAME = "WiFi-Arnet-6jbs"
PASSWORD = "j3ygefpf"
ADDRS = ('192.168.1.15', 2020)

TIEMPO_PUB = 60
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
        self.pin_s_temperatura = m.ADC(m.Pin(n_pin))
        self.pin_s_temperatura.atten(m.ADC.ATTN_6DB)
        temp_inicial = self.pin_s_temperatura.read_uv()/10000
        self.lista_temp = [temp_inicial, temp_inicial, temp_inicial]

    def medir(self):
        self.temp = self.pin_s_temperatura.read_uv() #valor en uvoltios
        self.medir_cambio(self.temp/10000)  #temperatura en °C

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


class SensorHumo:
    """
    Mide la concentracion de humo en ppm
    """
    def __init__(self, n_pin):
        self.pin_s_humo = m.ADC(m.Pin(n_pin))
        self.pin_s_humo.atten(m.ADC.ATTN_11DB)
        self.calculos()
        self.medir_humo()

    def calculos(self):
        voltaje_i = self.pin_s_humo.read()
        voltaje_i = voltaje_i * 3.3 / 4096
        self.R0 = 1000 * (5 - voltaje_i) / voltaje_i
        self.R0 = self.R0 / 9.7
        self.x1 = math.log10(200)
        self.y1 = math.log10(3.43)
    
    def medir_humo(self):
        self.ppm = 250


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
        self.pin_s_bateria = m.ADC(m.Pin(n_pin))
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
        string_temperatura_0 = f'temperatura_0: {s_temperatura.lista_temp[0]}'
        s.send(string_temperatura_0.encode())
        time.sleep(1)
        string_temperatura_1 = f'temperatura_1: {s_temperatura.lista_temp[1]}'
        s.send(string_temperatura_1.encode())
        time.sleep(1)
        string_temperatura_2 = f'temperatura_2: {s_temperatura.lista_temp[2]}'
        s.send(string_temperatura_2.encode())
        time.sleep(1)
        string_humo = f'humo: {s_humo.ppm}'
        s.send(string_humo.encode())
        time.sleep(1)
        string_flama = f'presencia de flama: {s_flama.presencia_flama}'
        s.send(string_flama.encode())
        time.sleep(1)
        string_bateria = f'bateria: {s_bateria.tension_bateria}'
        s.send(string_bateria.encode())
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
#creo el socket cliente, si la conexion es exitosa enciende el led por 3 seg
s = socket.socket()


while True:
    try:
        s.connect(ADDRS)
    except ConnectionRefusedError:
        time.sleep(0.5)
        continue
    break


time.sleep(3)
led.off()

estado = Estado()

#creacion de los objetos para los sensores
s_temperatura = SensorTemperatura(PIN_STEMPERATURA)
time.sleep(2)
s_humo = SensorHumo(PIN_SHUMO)
time.sleep(2)
s_flama = SensorFlama(PIN_SFLAMA)
time.sleep(2)
s_bateria = Bateria(PIN_SBATERIA)
time.sleep(2)

while True:
    time.sleep(30) 
    s_temperatura.medir()
    s_humo.medir_humo()
    s_flama.medir_flama()
    s_bateria.medir_bateria()
    time.sleep(30)
    s_temperatura.medir()
    estado.verificar()


