import machine as m
import time


led = m.Pin(2, m.Pin.OUT, value=0)
s_flama = m.Pin(32, m.Pin.IN)     # create input pin on GPIO2
while(true):
    #leer sensor
    s_flama = m.Pin(32, m.Pin.IN)     # create input pin on GPIO2
    print(s_flama.value())       # get value, 0 or 1
    #prender un led
    if(s_flama.value() == 1):
        #encender el led
        led.on()
    else:
        #apagar el led
        led.off()
    time.sleep_ms(200)