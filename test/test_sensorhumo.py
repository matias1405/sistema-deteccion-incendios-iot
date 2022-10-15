import machine as m
import time

humo_input = m.Pin(34,m.Pin.IN)
adc_humo = m.ADC(humo_input)
adc_humo.atten(m.ADC.ATTN_6DB)

while True:
    humo = adc_humo.read_uv()
    humo =
    print(humo)
    time.sleep_ms(1000)