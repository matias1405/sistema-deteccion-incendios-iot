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
import utime

#=============== definicion de constantes ======================================

ID_DISPOSITIVO = 1

#Pines analogicos
PIN_STEMPERATURA = 13 #gpio 13 y pin nro 15 #cambiar por wifi
PIN_SHUMO = 32 #gpio 32 y pin nro 7 
PIN_SFLAMA = 8 #gpio 8 y pin nro 22

#Pines digitales
PIN_LED_VERDE = 2 #led integrado en la placa del esp32
PIN_LED_ROJO = 6 #led indicador
PIN_BUZZER = 14 #gpio 14 y pin nro 12

SSID = "FBWAY-473372_2.4"
PASSWORD = "qlWjQcTi"
ADDRS = ('192.168.56.1', 2020)
TEMP_MAX = 57
VEL_AUMENT_TEMP_MAX = 8.3

STOP_FLAG = False

TIMEOUT = 30

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
        print("R0: ", self.R0)
        print("x1: ", self.x1)
        print("y1: ", self.y1)
        print("curva: ", self.curva)

    def calculos(self):
        voltaje_i = self.pin_s_humo.read_uv()/1000000*1.588028
        #voltaje_i = voltaje_i * 3.3 / 4096
        self.R0 = 1000 * (5 - voltaje_i) / voltaje_i
        self.R0 = self.R0 / 9.7
        self.x1 = math.log(200)/math.log(10)
        self.y1 = math.log(3.43)/math.log(10)
        x2 = math.log(10000)/math.log(10)
        y2 = math.log(0.61)/math.log(10)
        self.curva = (y2 - self.y1)/(x2 - self.x1)
    
    def medir_humo(self):
        voltaje_i = self.pin_s_humo.read_uv()/1000000*1.588028
        print(voltaje_i)
        if voltaje_i > 3.3:
            voltaje_i = 3.3
        print(voltaje_i)
        RS = 1000 * (5 - voltaje_i) / voltaje_i
        ratio = RS/self.R0
        exponente = ((math.log(ratio)/math.log(10))-self.y1)/self.curva
        exponente = exponente + self.x1
        self.ppm = int(10**exponente)


class SensorFlama:
    """
    Detecta la presencia de flama
    """
    def __init__(self, n_pin):
        self.pin_s_flama = m.Pin(n_pin, m.Pin.IN) 
        self.presencia_flama = False

    def medir_flama(self):
        valor = self.pin_s_flama.value()
        if(valor == 1):
            self.presencia_flama = False
            estado.flama(False)
        else:
            self.presencia_flama = True
            estado.flama(True)


class Estado:
    """
    almacena dos lista: la primera almacena el estado dado por los ssensores
    de temperatura, flama y humo.
    """
    def __init__(self):
        self.lista_estado = [False, False, False]

    def temperatura(self, x):
        self.lista_estado[0] = x

    def flama(self, x):
        self.lista_estado[1] = x

    def humo(self, x):
        self.lista_estado[2] = x
    
    def evaluar(self):
        return sum(self.lista_estado)
        

#============== palabra clave salir ============================================

def verificacion_salir():
    if uart.any():
        command = uart.readline().strip()
        if command == b"STOP":
            uart.write(b'saliendo...')
            STOP_FLAG = True


def modo_incendio():
    TIEMPO_PUB = 30
    while True:
        buzzer.on()
        time.sleep(TIEMPO_PUB/2) 
        lm35.medir()
        mq2.medir_humo()
        ky026.medir_flama()
        buzzer.off()
        time.sleep(TIEMPO_PUB/2)
        lm35.medir()
        s.connect(ADDRS)
        notificar_temp()
        notificar_humo()
        notificar_flama()
        cadena = "OK"
        s.sendall(cadena.encode())
        tiempo_inicial = utime.time()
        while not s.recv(1024).decode().strip() == 'OK' and utime.time() - tiempo_inicial < TIMEOUT:
            time.sleep_ms(100)
            pass
        s.close
        #verificacion de aviso de fin de incendio
        if uart.any():
            command = uart.readline().strip()
            if command == b"FININCENDIO":
                uart.write(b'incendio terminado...')
                return
        verificacion_salir()
        if STOP_FLAG:
            return


def notificar_temp(self):
    cadena = f'te0: {lm35.lista_temp[0]:.2f}'
    s.send(cadena.encode())
    time.sleep(1)
    cadena = f'te1: {lm35.lista_temp[1]:.2f}'
    s.send(cadena.encode())
    time.sleep(1)
    cadena = f'te2: {lm35.lista_temp[2]:.2f}'
    s.send(cadena.encode())
    time.sleep(1)


def notificar_humo(self):
    cadena = f'ppm: {mq2.ppm:.2f}'
    s.send(cadena.encode())
    time.sleep(1)


def notificar_flama(self):
    cadena = f'pdf: {ky026.presencia_flama}'
    s.send(cadena.encode())
    time.sleep(1)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#====================================================================
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

buzzer = m.Pin(PIN_BUZZER, m.Pin.OUT)
buzzer.off()
estado = Estado()
#creacion de los objetos para los sensores
mq2 = SensorHumo(PIN_SHUMO)
print("sensor humo creado")
"""
sta_if = network.WLAN(network.STA_IF)
time.sleep(2)
sta_if.active(False)
time.sleep(2)
sta_if.active(True)
time.sleep(2)
sta_if.connect(SSID, PASSWORD)

# Espera a que se establezca la conexión WiFi
tiempo_inicial = utime.time()
while not sta_if.isconnected() and utime.time() - tiempo_inicial < 10:
    print(".")
    time.sleep_ms(100)
    pass

# Si no se logra conectar, se desactiva el modo WiFi
if not sta_if.isconnected():
    print('No se pudo conectar al WiFi')
    sta_if.active(False)

print('network config:', sta_if.ifconfig())
"""

while True:
    time.sleep(1)
    mq2.medir_humo()
    print("ppm: ", mq2.ppm)
    print("=============================")