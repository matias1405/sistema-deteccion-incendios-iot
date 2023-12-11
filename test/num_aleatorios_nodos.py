import random
from paho.mqtt import client as mqtt_client

class Nodo:
    def __init__(self, name, t_mod_dist, t_mod_tiempo, h_mod_dist, h_mod_tiempo, t_lim, h_lim):
        self.name = name
        self.t_mod_dist = t_mod_dist
        self.t_mod_tiempo = t_mod_tiempo
        self.h_mod_dist = h_mod_dist
        self.h_mod_tiempo = h_mod_tiempo
        self.t_lim = t_lim
        self.h_lim = h_lim
        self.t_topic = self.name + "/temperatura"
        self.h_topic = self.name + "/humo"
        self.pdf_topic = self.name + "/flama"
        self.pdf = False
        self.t = 0
        self.h = 0

    def t_promedio(self):
        suma = 0
        for n in range(-1, -self.t_mod_tiempo-1, -1):
            suma = suma + c_temperatura.lista[n]
        return suma/self.t_mod_tiempo
    
    def obtener_temp(self):
        self.t = (self.t_promedio()-c_temperatura.lista[0])*(1-self.t_mod_dist)+c_temperatura.lista[0]
        if self.t_mod_dist > 0 :
            self.t_mod_dist = self.t_mod_dist - DISM_MOD_TIEMPO
        return round(random.uniform(0.99*self.t, 1.01*self.t), 2)
    
    def h_promedio(self):
        suma = 0
        for n in range(-1, -self.h_mod_tiempo-1, -1):
            suma = suma + c_humo.lista[n]
        return suma/self.h_mod_tiempo
    
    def obtener_humo(self):
        self.h = (self.h_promedio()-c_humo.lista[0])*(1-self.h_mod_dist)+c_humo.lista[0]
        if self.h_mod_dist > 0 :
            self.h_mod_dist = self.h_mod_dist - DISM_MOD_TIEMPO
        return round(random.uniform(0.99*self.h, 1.01*self.h), 2)
    
    def publicar_t(self, client):
        temp = self.obtener_temp()
        client.publish(self.t_topic, temp)
        if (self.t_lim < temp and self.h_lim < self.h):
            client.publish(self.pdf_topic, "1")
        else:
            client.publish(self.pdf_topic, "0")

    def publicar_h(self, client):
        humo = self.obtener_humo()
        client.publish(self.h_topic, humo)
        if (self.t_lim < self.t and self.h_lim < humo):
            client.publish(self.pdf_topic, "1")
        else:
            client.publish(self.pdf_topic, "0")


class Colas:
    def __init__(self, size_list):
        self.size_list = size_list
        self.inicio = True
        
    def add(self, temp):
        if self.inicio == True:
            self.lista = [temp for _ in range(self.size_list)]
            self.inicio = False
        else:
            self.lista.append(temp)
            self.remove()

    def remove(self):
        self.lista.pop(0)
    

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
        #print(f"Received '{mensaje}' from '{msg.topic}' topic")
        if msg.topic == "nodo-sensores/temperatura":
            c_temperatura.add(float(mensaje))
            nodo2.publicar_t(client)
            #time.sleep(1)
            nodo3.publicar_t(client)
            #time.sleep(1)
            nodo4.publicar_t(client)
            #time.sleep(1)
            nodo5.publicar_t(client)
            #time.sleep(1)
            nodo6.publicar_t(client)
            #time.sleep(1)
            nodo7.publicar_t(client)
        else:
            c_humo.add(float(mensaje))
            nodo2.publicar_h(client)
            #time.sleep(1)
            nodo3.publicar_h(client)
            #time.sleep(1)
            nodo4.publicar_h(client)
            #time.sleep(1)
            nodo5.publicar_h(client)
            #time.sleep(1)
            nodo6.publicar_h(client)
            #time.sleep(1)
            nodo7.publicar_h(client)        

    client.subscribe([("nodo-sensores/temperatura", 0), ("nodo-sensores/humo", 0)])
    client.on_message = on_message

DISM_MOD_TIEMPO = 0.01
BROKER = 'localhost'
PORT = 1883

#temp = float(input("temp_promedio_inicial: "))
#humo = float(input("ppm_humo_inicial: "))
c_temperatura = Colas(60)
c_humo = Colas(60)

nodo2 = Nodo(name="nodo2", t_mod_dist=0.2, t_mod_tiempo=20, h_mod_dist=0.2, h_mod_tiempo=20, t_lim=40, h_lim=400000) #bano
nodo3 = Nodo(name="nodo3", t_mod_dist=0.3, t_mod_tiempo=30, h_mod_dist=0.3, h_mod_tiempo=30, t_lim=50, h_lim=500000) #habitacionA
nodo4 = Nodo(name="nodo4", t_mod_dist=0.4, t_mod_tiempo=40, h_mod_dist=0.4, h_mod_tiempo=40, t_lim=60, h_lim=400000) #habitacionB
nodo5 = Nodo(name="nodo5", t_mod_dist=0.5, t_mod_tiempo=50, h_mod_dist=0.5, h_mod_tiempo=50, t_lim=40, h_lim=600000) #habitacionC
nodo6 = Nodo(name="nodo6", t_mod_dist=0.6, t_mod_tiempo=60, h_mod_dist=0.6, h_mod_tiempo=60, t_lim=50, h_lim=400000) #livingA
nodo7 = Nodo(name="nodo7", t_mod_dist=0.6, t_mod_tiempo=60, h_mod_dist=0.6, h_mod_tiempo=60, t_lim=50, h_lim=400000) #livingB

client = connect_mqtt()
subscribe(client)
#client.loop_start()
client.loop_forever()