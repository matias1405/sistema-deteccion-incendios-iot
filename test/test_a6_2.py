import machine as m
import time

pwr = m.Pin(15, m.Pin.OUT)
pwr.on()
print("hola")
enable = m.Pin(0, m.Pin.OUT)
enable.on()
print ("iniciando")
a6 = m.UART(1, baudrate=9600, tx=10 , rx=9)
time.sleep(1)
print("a6 declarado")
a6.init()
time.sleep(5)
print("a6 iniciado")
a6.write("ATI\r\n")
time.sleep(1)
print(a6.read())
