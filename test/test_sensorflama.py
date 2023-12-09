import machine as m
import time

PIN_SFLAMA = 35

class SensorFlama:
    """
    Detecta la presencia de flama
    """
    def __init__(self, n_pin):
        self.pin_s_flama = m.Pin(n_pin, m.Pin.IN) 
        self.presencia_flama = False

    def medir_flama(self):
        valor = self.pin_s_flama.value()
        print(valor)
        if(valor == 1):
            self.presencia_flama = False
            #estado.flama(False)
        else:
            self.presencia_flama = True
            #estado.flama(True)

ky026 = SensorFlama(PIN_SFLAMA)


while True :
	ky026.medir_flama()
	time.sleep_ms(800)
