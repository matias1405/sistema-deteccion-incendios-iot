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
PIN_STEMPERATURA = 13 #gpio 13 y pin nro 15 #cambiar por wifi
PIN_SHUMO = 32 #gpio 32 y pin nro 7 
PIN_SFLAMA = 8 #gpio 8 y pin nro 22

#Pines digitales
PIN_LED_VERDE = 2 #led integrado en la placa del esp32
PIN_LED_ROJO = 6 #led indicador
PIN_BUZZER = 14 #gpio 14 y pin nro 12

SSID = "ALFARO"
PASSWORD = "MATIAS64P13"
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
        utime.sleep(1)
        self.temp += self.pin_s_temperatura.read_uv()/10000
        utime.sleep(1)
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
        utime.sleep(TIEMPO_PUB/2) 
        lm35.medir()
        mq2.medir_humo()
        ky026.medir_flama()
        buzzer.off()
        utime.sleep(TIEMPO_PUB/2)
        lm35.medir()
        s.connect(ADDRS)
        notificar_temp()
        notificar_humo()
        notificar_flama()
        cadena = "OK"
        s.sendall(cadena.encode())
        tiempo_inicial = utime.time()
        while not s.recv(1024).decode().strip() == 'OK' and utime.time() - tiempo_inicial < TIMEOUT:
            utime.sleep_ms(100)
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
    utime.sleep(1)
    cadena = f'te1: {lm35.lista_temp[1]:.2f}'
    s.send(cadena.encode())
    utime.sleep(1)
    cadena = f'te2: {lm35.lista_temp[2]:.2f}'
    s.send(cadena.encode())
    utime.sleep(1)


def notificar_humo(self):
    cadena = f'ppm: {mq2.ppm:.2f}'
    s.send(cadena.encode())
    utime.sleep(1)


def notificar_flama(self):
    cadena = f'pdf: {ky026.presencia_flama}'
    s.send(cadena.encode())
    utime.sleep(1)

#============== inicio del programa ============================================

led = m.Pin(PIN_LED_ROJO, m.Pin.OUT)
led.off()
buzzer = m.Pin(PIN_BUZZER, m.Pin.OUT)
buzzer.off()
estado = Estado()
#creacion de los objetos para los sensores
lm35 = SensorTemperatura(PIN_STEMPERATURA)
print("sensor temp creado")
mq2 = SensorHumo(PIN_SHUMO)
ky026 = SensorFlama(PIN_SFLAMA)
print("sensores creados")
led.on()
buzzer.on()

sta_if = network.WLAN(network.STA_IF)
utime.sleep(2)
sta_if.active(False)
utime.sleep(2)
sta_if.active(True)
utime.sleep(2)
sta_if.connect(SSID, PASSWORD)

# Espera a que se establezca la conexión WiFi
tiempo_inicial = utime.time()
while not sta_if.isconnected() and utime.time() - tiempo_inicial < 10:
    print(".")
    utime.sleep_ms(100)
    pass

# Si no se logra conectar, se desactiva el modo WiFi
if not sta_if.isconnected():
    print('No se pudo conectar al WiFi')
    sta_if.active(False)

print('network config:', sta_if.ifconfig())
led.off()
buzzer.off()

#uart = m.UART(0, 9600) #encender si ampy esta apagado

# Conexión con el servidor
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    TIEMPO_PUB = 8
    try:
        utime.sleep(TIEMPO_PUB/2) 
        lm35.medir()
        mq2.medir_humo()
        ky026.medir_flama()
        utime.sleep(TIEMPO_PUB/2)
        lm35.medir()
        print("te0: ", lm35.lista_temp[0])
        print("te1: ", lm35.lista_temp[1])
        print("te2: ", lm35.lista_temp[2])
        print("ppm: ", mq2.ppm)
        print("pdf: ", ky026.presencia_flama)
        print("=============================")
        if estado.evaluar() >= 2:
            #notificar incendio y entrar al modo incendio
            s.connect(ADDRS)
            cadena = "INCENDIO"
            s.sendall(cadena.encode())
            tiempo_inicial = utime.time()
            while not s.recv(1024).decode().strip() == 'OK' and utime.time() - tiempo_inicial < TIMEOUT:
                utime.sleep_ms(100)
                pass
            s.close()
            modo_incendio()
        elif estado.evaluar() == 1:
            #notificar advertencia
            s.connect(ADDRS)
            cadena = "ADVERTENCIA"
            s.sendall(cadena.encode())
            while not s.recv(1024).decode().strip() == 'OK' and utime.time() - tiempo_inicial < TIMEOUT:
                utime.sleep_ms(100)
                pass
            for i in range(3):
                if estado.lista_estado[i] == True and i == 0:
                    notificar_temp()
                elif estado.lista_estado[i] == True and i == 1:
                    notificar_humo()
                else:
                    notificar_flama()
            s.close()
        #verificacion_salir() #encender si ampy esta apagado
        if STOP_FLAG:
            break

    except Exception as e:
        print(e)
