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
import dht

#=============== definicion de constantes ======================================

ID_DISPOSITIVO = 1002

#Pines analogicos
PIN_SDHT = 14 #gpio 39 y pin nro 4 #cambiado
PIN_SHUMO = 0 #gpio 32 y pin nro 7 
PIN_SFLAMA = 5 #gpio 8 y pin nro 22 #cambiar por embedded flash a gpio 35 pin 6

#Pines digitales
PIN_LED_VERDE = 2 #led integrado en la placa del esp32
PIN_LED_ROJO = 13 #led indicador #cambiar por embedded flash a gpio 10 pin 17
PIN_BUZZER = 4 #gpio 14 y pin nro 12

SSID = ["ESP 32", "Galaxy S23 FE 3B0E", "ALFARO"]
PASSWORD = ["romi1234", "1234matias", "MATIAS64P13"]
SERVER_IP = ['192.168.135.10', '192.168.31.10', '192.168.100.10']
PORT = 2020
TEMP_MAX = 57
VEL_AUMENT_TEMP_MAX = 8.3

STOP_FLAG = False
INCENDIO = False

TIME_PUB = 5
dutycicle = 300

#============== definicion de clases ========================================

class SensorDHT:
    """
    Mide temperaturas en grados centigrados y los almacena en listas.
    lista_temp[0] es temperatura hace un minuto
    lista_temp[1] es temperatiura hace 30 segundos
    lista_temp[2] es la temperatura actual
    Tambien mide el cambio de temperatura en un minuto y la temperatura actual
    """
    def __init__(self, n_pin):
        self.s_dht = dht.DHT11(m.Pin(n_pin))
        #self.medir()
        #self.lista_temp = [temp_inicial, temp_inicial, temp_inicial]

    def medir(self):
        try:
            self.s_dht.measure()
            self.temp = self.s_dht.temperature()
        except Exception:
            self.temp = 25
        utime.sleep(1)
        

class SensorHumo:
    """
    Mide la concentracion de humo en ppm
    """
    def __init__(self, n_pin):
        self.pin_s_humo = m.ADC(n_pin)
        self.calculos()
        self.medir_humo()
        print("R0: ", self.R0)
        print("x1: ", self.x1)
        print("y1: ", self.y1)
        print("curva: ", self.curva)

    def calculos(self):
        voltaje_i = self.pin_s_humo.read()
        voltaje_i = voltaje_i * 3.3 / 1024
        self.R0 = 1000 * (5 - voltaje_i) / voltaje_i
        self.R0 = self.R0 / 9.7
        self.x1 = math.log(200)/math.log(10)
        self.y1 = math.log(3.43)/math.log(10)
        x2 = math.log(10000)/math.log(10)
        y2 = math.log(0.61)/math.log(10)
        self.curva = (y2 - self.y1)/(x2 - self.x1)
    
    def medir_humo(self):
        voltaje_i = self.pin_s_humo.read()
        voltaje_i = voltaje_i * 3.3 / 1024
        print(voltaje_i)
        RS = 1000 * (5 - voltaje_i) / voltaje_i
        ratio = RS/self.R0
        exponente = ((math.log(ratio)/math.log(10))-self.y1)/self.curva
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
        try:
            if(self.pin_s_flama.value() == 1):
                self.presencia_flama = 0
            else:
                self.presencia_flama = 1
        except Exception:
            self.presencia_flama = 0

def notificar():
    cadena = f'{mq2.ppm}&{dht11.temp}&{ky026.presencia_flama}&{ID_DISPOSITIVO}'
    print(cadena)
    s.send(cadena.encode())
    utime.sleep(1)
    cadena = s.recv(128).decode().strip()
    print(cadena)
    global TIME_PUB
    global INCENDIO
    if cadena == 'OK':
        if INCENDIO:
            INCENDIO = False
            TIME_PUB = 5
    elif cadena == 'INCENDIO':
        if not INCENDIO:
            INCENDIO = True
            TIME_PUB = 2

def terminar():
    buzzer.duty(dutycicle)
    led.on()
    utime.sleep(0.5)
    buzzer.duty(0)
    led.off()
    utime.sleep(0.5)
    buzzer.duty(dutycicle)
    led.on()
    utime.sleep(0.5)
    buzzer.duty(0)
    led.off()
    raise("Error: programa finalizado")

def avisar_incendio():
    buzzer.duty(dutycicle)
    led.on()
    utime.sleep(0.5)
    buzzer.duty(0)
    led.off()
    utime.sleep(0.5)

#============== inicio del programa ============================================

led = m.Pin(PIN_LED_ROJO, m.Pin.OUT)
led.off()
frequency = 5000
buzzer = m.PWM(m.Pin(PIN_BUZZER), frequency)
buzzer.duty(0)
print("Iniciando...")
#creacion de los objetos para los sensores
led.on()
buzzer.duty(dutycicle)
utime.sleep(1)
buzzer.duty(0)



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

dht11 = SensorDHT(PIN_SDHT)
mq2 = SensorHumo(PIN_SHUMO)
ky026 = SensorFlama(PIN_SFLAMA)
print("Sensores creados")

_SERVER_IP = SERVER_IP[red]
print("red: ", SSID[red])
# Si no se logra conectar, se desactiva el modo WiFi
if not sta_if.isconnected():
    print('No se pudo conectar al WiFi')
    sta_if.active(False)
    terminar()

print('network config:', sta_if.ifconfig())
led.off()
# Conexión con el servidor
try:
    while True:
        try:
            print(".")
            dht11.medir()
            if INCENDIO:
                avisar_incendio()
            print(".")
            mq2.medir_humo()
            if INCENDIO:
                avisar_incendio()
            print(".")
            ky026.medir_flama()
            if INCENDIO:
                avisar_incendio()
            print("conectando..")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((_SERVER_IP, PORT))
            utime.sleep(1)
            notificar()

        #except Exception as e:
        #    print(e)
        finally:
            s.close()
            utime.sleep(TIME_PUB)
finally:
    terminar()