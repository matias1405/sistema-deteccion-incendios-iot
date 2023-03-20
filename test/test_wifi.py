# -*- coding: utf-8 -*-

import machine as m
import network
import time
import socket

PIN_LED_VERDE = 2 #led integrado en la placa del esp32


WIFI_NAME = "MOVISTAR WIFI2276"
PASSWORD = "romi1234"
ADDRS = ('192.168.145.14', 2020)

led = m.Pin(PIN_LED_VERDE, m.Pin.OUT)
led.off()

wf = network.WLAN(network.STA_IF)
wf.active(False)
time.sleep(3)
wf.active(True)
if not wf.isconnected():
    print('connecting to network...')
    wf.connect(WIFI_NAME, PASSWORD)
    count = 0
    while not wf.isconnected():
        time.sleep(0.5)
        count += 1
        if count > 12:
            led.value(count%2)


#print('network config:', wf.ifconfig())

#s = socket.socket()
#s.connect(ADDRS)
print("me conecte")

while True:
    #s.send("hola".encode())
    print("hola")
    time.sleep(2)


