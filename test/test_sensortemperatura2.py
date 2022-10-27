import machine as m
import time

TEMP_MAX = 57
VEL_AUMENT_TEMP_MAX = 8.3

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
        temp_inicial = self.pin_s_temperatura.read()#* 3.3 / 4096
        #temp_inicial = temp_inicial*100
        self.lista_temp = [temp_inicial, temp_inicial, temp_inicial]

    def medir(self):
        self.temp = self.pin_s_temperatura.read()#* 3.3 / 4096 #valor en voltios
        self.medir_cambio(self.temp)  #temperatura en °C

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

time.sleep(5)
s_temperatura = SensorTemperatura(35)
estado = Estado()
while True:
    time.sleep(2)
    s_temperatura.medir()
    print(s_temperatura.lista_temp)