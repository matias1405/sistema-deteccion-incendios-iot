# -*- coding: utf-8 -*-

import machine as m
import network
import time

PIN_LED_VERDE = 2 #led integrado en la placa del esp32


WIFI_NAME = "WiFi-Arnet-6jbs"
PASSWORD = "j3ygefpf"
ADDRS = ('192.168.1.19', 2020)

led = m.Pin(PIN_LED_VERDE, m.Pin.OUT)
led.off()

wf = network.WLAN(network.STA_IF)
wf.active(True)
if not wf.isconnected():
    print('connecting to network...')
    wf.connect(WIFI_NAME, PASSWORD)
    count = 0
    print('llegue aqui')
    while not wf.isconnected():
        time.sleep(0.5)
        count += 1
        if count > 12:
            led.value(count%2)
            print('tambien llegue aqui')

print('network config:', wf.ifconfig())