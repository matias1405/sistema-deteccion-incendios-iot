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
import random

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

SSID = ["ESP 32", "Galaxy S23 FE 3B0E", "ALFARO"]
PASSWORD = ["romi1234", "1234matias", "MATIAS64P13"]
SERVER_IP = ['192.168.135.10', '192.168.102.10', '192.168.100.10']
PORT = 2020
TEMP_MAX = 57
VEL_AUMENT_TEMP_MAX = 8.3

STOP_FLAG = False
INCENDIO = False

TIME_PUB = 4

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
        temp_inicial = self.pin_s_temperatura.read_uv()/10000*0.9
        self.temp = temp_inicial
        #self.lista_temp = [temp_inicial, temp_inicial, temp_inicial]

    def medir(self):
        self.temp = self.pin_s_temperatura.read_uv()/10000*0.9
        utime.sleep(1)
        self.temp += self.pin_s_temperatura.read_uv()/10000*0.9
        utime.sleep(1)
        self.temp += self.pin_s_temperatura.read_uv()/10000*0.9
        self.temp = round(self.temp/3, 1)
        #self.medir_cambio(self.temp)  #temperatura en °C
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
        self.ppm = int(10**exponente)
        #self.ppm = round(self.ppm, 2)


class SensorFlama:
    """
    Detecta la presencia de flama
    """
    def __init__(self, n_pin):
        self.pin_s_flama = m.Pin(n_pin, m.Pin.IN) 
        self.presencia_flama = 0

    def medir_flama(self):
        if(self.pin_s_flama.value() == 1):
            self.presencia_flama = 0
        else:
            self.presencia_flama = 1
        

def notificar():
    cadena = f'{mq2.ppm}&{lm35.temp}&{ky026.presencia_flama}'
    print(cadena)
    s.send(cadena.encode())
    utime.sleep(1)
    cadena = s.recv(512).decode().strip()
    print(cadena)
    global INCENDIO
    if cadena == 'OK':
        if INCENDIO:
            INCENDIO = False
    elif cadena == 'INCENDIO':
        if not INCENDIO:
            INCENDIO = True

def terminar():
    buzzer.on()
    led.on()
    utime.sleep(0.5)
    buzzer.off()
    led.off()
    utime.sleep(0.5)
    buzzer.on()
    led.on()
    utime.sleep(0.5)
    buzzer.off()
    led.off()
    raise("Error: programa finalizado")

def avisar_incendio():
    buzzer.on()
    led.on()
    utime.sleep(0.5)
    buzzer.off()
    led.off()
    utime.sleep(0.5)
    global TIME_PUB
    utime.sleep(TIME_PUB)


#============== inicio del programa ============================================

led = m.Pin(PIN_LED_ROJO, m.Pin.OUT)
led.off()
buzzer = m.Pin(PIN_BUZZER, m.Pin.OUT)
buzzer.off()
print("Iniciando...")
#creacion de los objetos para los sensores
lm35 = SensorTemperatura(PIN_STEMPERATURA)
mq2 = SensorHumo(PIN_SHUMO)
ky026 = SensorFlama(PIN_SFLAMA)
print("Sensores creados")
led.on()
buzzer.off()

sta_if = network.WLAN(network.STA_IF)
utime.sleep(1)
sta_if.active(False)
utime.sleep(1)
sta_if.active(True)
utime.sleep(1)

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
        

_SERVER_IP = SERVER_IP[red]
print("red: ", SSID[red])
# Si no se logra conectar, se desactiva el modo WiFi
if not sta_if.isconnected():
    print('No se pudo conectar al WiFi')
    sta_if.active(False)
    terminar()

print('network config:', sta_if.ifconfig())
led.off()
buzzer.off()
#INCENDIO = True
# Conexión con el servidor
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((_SERVER_IP, PORT))
    print("conectando..")
    while True:
    #for i in range(10):
        try:
            if INCENDIO:
                avisar_incendio()
            print(".")
            lm35.medir()
            if INCENDIO:
                avisar_incendio()
            print(".")
            mq2.medir_humo()
            if INCENDIO:
                avisar_incendio()
            print(".")
            ky026.medir_flama()
            notificar()
            if INCENDIO:
                avisar_incendio()
            print(".")

        except Exception as e:
            print(e)
            
        #if STOP_FLAG:
        #    print("if para salir")
        #    break
finally:
    s.close()
    terminar()

