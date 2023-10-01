import machine as m
import utime
import math
import network
import urequests


PIN_SHUMO = 32 #gpio 34 y pin nro 5
SSID = "moto g9 play"
PASSWORD = "1234matias"

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

def notificar_humo():
    print("ppm: ", mq2.ppm)
    url = f'http://ec2-15-229-8-95.sa-east-1.compute.amazonaws.com:1880/nodered?humo={mq2.ppm}'

    try:
        response = urequests.get(url)

        response.close()

    except Exception as e:
        print("Excepción durante la solicitud HTTP:", e)
    utime.sleep(3)

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

PIN_BUZZER = 14 #gpio 14 y pin nro 12
buzzer = m.Pin(PIN_BUZZER, m.Pin.OUT)
buzzer.off()
mq2 = SensorHumo(PIN_SHUMO)


while True:
    mq2.medir_humo()
    notificar_humo()