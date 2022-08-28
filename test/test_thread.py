from threading import Thread
from time import sleep
from datetime import datetime

def funcion():
    print('llamada a otra funcion')


def temporizador():
    hora_pub = datetime.strptime(hora, '%H:%M:%S')
    while(True):
        if datetime.now().minute == hora_pub.minute:
            print("hilo ejecutado ", datetime.now().time())
            funcion()
            sleep(60)
        sleep(5)


hora = "12:21:00"
hilo = Thread(name='hilo', target=temporizador, daemon=True)
hilo.start()
while(True):
    print("programa principal")
    sleep(4)
