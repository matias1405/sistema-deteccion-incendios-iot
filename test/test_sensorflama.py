import machine as m
import time

sensor = m.ADC(Pin(32))

sensor.atten(m.ADC.ATTN_11DB)


while True :
	print(sensor.read())
	time.sleep_ms(200)
