import machine as m
import time

PIN_LED = 2

led = m.Pin(PIN_LED, m.Pin.OUT)
led.off()
time.sleep(1)

for i in range (10):
    led.on(1)
    time.sleep(1)
    led.off(1)
    time.sleep(1)