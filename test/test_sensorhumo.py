import machine as m
import time
import math


PIN_SHUMO = 34 #gpio 34 y pin nro 5

class SensorHumo:
    """
    Mide la concentracion de humo en ppm
    """
    def __init__(self, n_pin):
        self.pin_s_humo = m.ADC(m.Pin(n_pin, m.Pin.IN))
        self.pin_s_humo.atten(m.ADC.ATTN_11DB)
        #self.calculos()
        self.medir_humo()

    def calculos(self):
        voltaje_i = self.pin_s_humo.read()
        voltaje_i = voltaje_i * 3.3 / 4096
        self.R0 = 1000 * (5 - voltaje_i) / voltaje_i
        self.R0 = self.R0 / 9.7
        self.x1 = math.log10(200)
        self.y1 = math.log10(3.43)
    
    def medir_humo(self):
        self.ppm = self.pin_s_humo.read_uv()*1000
        return self.ppm


s_humo = SensorHumo(PIN_SHUMO)

while True:
    print("tension en mV detectado: ", s_humo.medir_humo())
    time.sleep(5)