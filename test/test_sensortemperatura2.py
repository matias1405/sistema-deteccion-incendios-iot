# Universidad Tecnológica Nacional - Facultad Regional Tucumán
# Proyecto Final de grado
# Sistema de Alarma contra Incendios basado en Tecnologías de IoT
# Dessarolladores:
#    + Matías Alfaro - matiasalfaro1405@gmail.com
#    + Romina Farías - romii12mf@gmail.com

import machine as m
import network
import socket
import math
import utime

#=============== definicion de constantes ======================================

ID_DISPOSITIVO = 1

#Pines analogicos
PIN_STEMPERATURA = 39 #gpio 39 y pin nro 4 #cambiado
PIN_SHUMO = 32 #gpio 32 y pin nro 7 
PIN_SFLAMA = 35 #gpio 8 y pin nro 22 #cambiar por embedded flash a gpio 35 pin 6

#Pines digitales
PIN_LED_VERDE = 2 #led integrado en la placa del esp32
PIN_LED_ROJO = 10 #led indicador #cambiar por embedded flash a gpio 10 pin 17
PIN_BUZZER = 14 #gpio 14 y pin nro 12

SSID = "FBWAY-473372_2.4"
PASSWORD = "qlWjQcTi"
SERVER_IP = '192.168.100.10'
PORT = 2020
TEMP_MAX = 57
VEL_AUMENT_TEMP_MAX = 8.3

STOP_FLAG = False

TIMEOUT = 4

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
        #self.pin_s_temperatura.atten(m.ADC.ATTN_6DB) #6db /4095*2.44*100
        self.pin_s_temperatura.atten(m.ADC.ATTN_2_5DB) #2_5db /4095*1.53*100
        #self.pin_s_temperatura.atten(m.ADC.ATTN_0DB) #0db /4095*1.15*100
        temp_inicial = self.pin_s_temperatura.read_uv()/10000*0.9
        #temp_inicial = self.pin_s_temperatura.read()/4095*1.53*100
        self.lista_temp = [temp_inicial, temp_inicial, temp_inicial]

    def medir(self):
        self.temp = self.pin_s_temperatura.read_uv()/10000*0.9
        #self.temp = self.pin_s_temperatura.read()/4095*1.53*100
        utime.sleep(1)
        self.temp += self.pin_s_temperatura.read_uv()/10000*0.9
        #self.temp += self.pin_s_temperatura.read()/4095*1.53*100
        utime.sleep(1)
        self.temp += self.pin_s_temperatura.read_uv()/10000*0.9
        #self.temp += self.pin_s_temperatura.read()/4095*1.53*100
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

def notificar_temp():
    print("te0: ", lm35.lista_temp[0])
    cadena = f'te0: {lm35.lista_temp[0]:.2f}'
    s.send(cadena.encode())
    salir()
    utime.sleep(4)
    print("te1: ", lm35.lista_temp[1])
    cadena = f'te1: {lm35.lista_temp[1]:.2f}'
    s.send(cadena.encode())
    salir()
    utime.sleep(4)
    print("te2: ", lm35.lista_temp[2])
    cadena = f'te2: {lm35.lista_temp[2]:.2f}'
    s.send(cadena.encode())
    salir()
    utime.sleep(4)


def notificar_humo():
    print("ppm: ", mq2.ppm)
    cadena = f'ppm: {mq2.ppm:.2f}'
    s.send(cadena.encode())
    salir()
    utime.sleep(6)
    

def notificar_flama():
    print("pdf: ", ky026.presencia_flama)
    cadena = f'pdf: {ky026.presencia_flama}'
    s.send(cadena.encode())
    utime.sleep(6)
    salir()

def notificar():
    if (lm35.lista_temp[2] > 30 and mq2.ppm > 500):
        pdf = 1
    else:
        pdf = 0
    cadena = f'humo={mq2.ppm:.2f}&temperatura={lm35.lista_temp[2]:.2f}&pdf={pdf}'
    print(cadena)
    s.send(cadena.encode())
    utime.sleep(6)
    salir()

def salir():
    cadena = s.recv(512).decode().strip()
    print(cadena)
    if cadena == 'OK':
        pass
    elif cadena == 'STOP':
        global STOP_FLAG
        STOP_FLAG = True
        print("parando programa...")
    else:
        print("dato no recibido")
    


#============== inicio del programa ============================================

led = m.Pin(PIN_LED_ROJO, m.Pin.OUT)
led.off()
buzzer = m.Pin(PIN_BUZZER, m.Pin.OUT)
buzzer.off()
lm35 = SensorTemperatura(PIN_STEMPERATURA)
print("sensor temp creado")
estado = Estado()

while(True):
    utime.sleep(2)
    lm35.medir()
    print(lm35.lista_temp)