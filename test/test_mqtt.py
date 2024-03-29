import random

from paho.mqtt import client as mqtt_client


broker = 'localhost'
port = 1883
topic = "python/mqtt"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'

"""PEP 484
def saludo(nombre: str) -> str:
    devuelve 'Hola' + nombre

despues de los dos puntos dentro del argumento se especifica el tipo o clase del
argumento esperado y analogamente luego de -> se especifica el tipo de o clase
del retorno de la funcion"""

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    print(client)
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
