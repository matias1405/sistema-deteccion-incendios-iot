import random
import time
from paho.mqtt import client as mqtt_client

temperatura_original = []

class Nodo:
    def __init__(self, name, t_mod_dist, t_mod_tiempo, h_mod_dist, h_mod_tiempo, t_lim, h_lim):
        self.name = name
        self.t_mod_dist = t_mod_dist
        self.t_mod_tiempo = t_mod_tiempo
        self.h_mod_dist = h_mod_dist
        self.h_mod_tiempo = h_mod_tiempo
        self.t_lim = t_lim
        self.h_lim = h_lim
        self.t_inicial = c_temperatura.lista[0]
        self.h_inicial = c_humo.lista[0]
        self.t_topic = self.name + "/temperatura"
        self.h_topic = self.name + "/humo"
        self.pdf_topic = self.name + "/flama"

    def t_promedio(self):
        suma = 0
        for n in range(-1, -self.t_mod_tiempo-1, -1):
            suma = suma + c_temperatura.lista[n]
        return suma/self.t_mod_tiempo
    
    def obtener_temp(self):
        t = (self.t_promedio()-self.t_inicial)*(1-self.t_mod_dist)+self.t_inicial
        if self.t_mod_dist > 0 :
            self.t_mod_dist = self.t_mod_dist - DISM_MOD_TIEMPO
        return round(random.uniform(0.99*t, 1.01*t), 2)
    
    def h_promedio(self):
        suma = 0
        for n in range(-1, -self.h_mod_tiempo-1, -1):
            suma = suma + c_humo.lista[n]
        return suma/self.h_mod_tiempo
    
    def obtener_humo(self):
        h = (self.h_promedio()-self.h_inicial)*(1-self.h_mod_dist)+self.h_inicial
        if self.h_mod_dist > 0 :
            self.h_mod_dist = self.h_mod_dist - DISM_MOD_TIEMPO
        return round(random.uniform(0.99*h, 1.01*h), 2)
    
    def publicar(self, client):
        temp = self.obtener_temp()
        print(f'la temperatura en {self.name} es de {temp} *C')
        client.publish(self.t_topic, temp)
        humo = self.obtener_humo()
        print(f'la cantidad de humo en {self.name} es de {humo} ppm')
        client.publish(self.h_topic, humo)
        if (self.t_lim < temp and self.h_lim < humo):
            client.publish(self.pdf_topic, "true")
        else:
            client.publish(self.pdf_topic, "false")


class Colas:
    def __init__(self, valor_inicial, size_list):
        self.valor_inicial = valor_inicial
        self.lista = [valor_inicial for _ in range(size_list)]
        
    def add(self, temp):
        self.lista.append(temp)
        self.remove()

    def remove(self):
        self.lista.pop(0)



 #esto debe ir en la clase nodo donde la cantidad de elementos es el modificador de tiempo y el 30 es el modificador de distancia
    
def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.connect(BROKER, PORT)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        mensaje = msg.payload.decode()
        print(f"Received '{mensaje}' from '{msg.topic}' topic")

    client.subscribe("nodo1")
    client.on_message = on_message

TEMP_LIMITE = 100
TEMP_AUMENTO = 1
HUMO_AUMENTO = 10000
DISM_MOD_TIEMPO = 0.01
inicio = True

BROKER = 'localhost'
PORT = 1883

temp = float(input("temp_promedio_inicial: "))
humo = float(input("ppm_humo_inicial: "))

c_temperatura = Colas(temp, 60)
c_humo = Colas(humo, 60)

nodo2 = Nodo(name="nodo2", t_mod_dist=0.2, t_mod_tiempo=20, h_mod_dist=0.2, h_mod_tiempo=20, t_lim=40, h_lim=400000)
nodo3 = Nodo(name="nodo3", t_mod_dist=0.3, t_mod_tiempo=30, h_mod_dist=0.3, h_mod_tiempo=30, t_lim=50, h_lim=500000)
nodo4 = Nodo(name="nodo4", t_mod_dist=0.4, t_mod_tiempo=40, h_mod_dist=0.4, h_mod_tiempo=40, t_lim=60, h_lim=400000)
nodo5 = Nodo(name="nodo5", t_mod_dist=0.5, t_mod_tiempo=50, h_mod_dist=0.5, h_mod_tiempo=50, t_lim=40, h_lim=600000)
nodo6 = Nodo(name="nodo6", t_mod_dist=0.6, t_mod_tiempo=60, h_mod_dist=0.6, h_mod_tiempo=60, t_lim=50, h_lim=400000)

if inicio == True:
    inicio = False

client = connect_mqtt()
#subscribe(client)
client.loop_start()
try:
    while(True):
        c_temperatura.add(temp)
        print("temperatura:", temp)
        c_humo.add(humo)
        print("humo:", humo)
        nodo2.publicar(client)
        time.sleep(1)
        nodo3.publicar(client)
        time.sleep(1)
        nodo4.publicar(client)
        time.sleep(1)
        nodo5.publicar(client)
        time.sleep(1)
        nodo6.publicar(client)
        if(temp < 100):
            temp = temp + TEMP_AUMENTO
        if(humo < 600000):
            humo = humo + HUMO_AUMENTO
        time.sleep(5)
finally:
    client.loop_stop()