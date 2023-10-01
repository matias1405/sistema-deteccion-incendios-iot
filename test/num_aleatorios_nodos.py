import random
import time
from paho.mqtt import client as mqtt_client

temperatura_original = []

class Nodo:
    def __init__(self, name, mod_dist, mod_tiempo, temp_inicial):
        self.name = name
        self.mod_dist = mod_dist
        self.mod_tiempo = mod_tiempo
        self.temp_inicial = temp_inicial

    def promedio(self):
        suma = 0
        for n in range(-1, -self.mod_tiempo-1, -1):
            suma = suma + temperaturas.lista_temp[n]
        return suma/self.mod_tiempo
    
    def obtener_temp(self):
        t = (self.promedio()-self.temp_inicial)*(1-self.mod_dist)+self.temp_inicial
        if self.mod_dist > 0 :
            self.mod_dist = self.mod_dist - 0.01
        return round(random.uniform(0.99*t, 1.01*t), 2)
    
    def publicar(self):
        msg = f'la temperatura en {self.name} es de {self.obtener_temp()} *C'
        print(msg)
        client.publish(self.name, msg)

class Temperaturas:
    def __init__(self, temp_inicial, size_list):
        self.temp_inicial = temp_inicial
        self.lista_temp = [temp_inicial for _ in range(size_list)]
        
    def add(self, temp):
        self.lista_temp.append(temp)
        self.remove()

    def remove(self):
        self.lista_temp.pop(0)



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

    client.subscribe(TOPIC_SUB)
    client.on_message = on_message

def publish(client, msg):
    result = client.publish(TOPIC_PUB, msg)
    status = result[0]
    #if status == 0:
    #    print(f"Send `{msg}` to topic `{TOPIC_PUB}`")
    #else:
    #    print(f"Failed to send message to topic {TOPIC_PUB}")

TEMP_LIMITE = 100
TEMP_AUMENTO = 1
inicio = True

BROKER = 'localhost'
PORT = 1883
TOPIC_SUB = "test"
TOPIC_PUB = "test"

temp = float(input("temp_promedio_inicial: "))
temperaturas = Temperaturas(temp, 60)

nodo2 = Nodo("nodo2", 0.2, 20, temp)
nodo3 = Nodo("nodo3", 0.3, 30, temp)
nodo4 = Nodo("nodo4", 0.4, 40, temp)
nodo5 = Nodo("nodo5", 0.5, 50, temp)
nodo6 = Nodo("nodo6", 0.6, 60, temp)

if inicio == True:
    inicio = False

client = connect_mqtt()
#subscribe(client)
client.loop_forever()

while(True):
    temperaturas.add(temp)
    print("temperatura:", temp)
    nodo2.publicar(client)
    nodo3.publicar(client)
    nodo4.publicar(client)
    nodo5.publicar(client)
    nodo6.publicar(client)
    if(temp < 100):
        temp = temp + TEMP_AUMENTO
    time.sleep(5)