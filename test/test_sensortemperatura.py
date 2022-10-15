import machine as m
import time

temp_input = m.Pin(35,m.Pin.IN)
adc_temp = m.ADC(temp_input)
adc_temp.atten(m.ADC.ATTN_6DB)

while True:
    temp = adc_temp.read_uv()
    temp = temp/10000
    print(temp)
    time.sleep_ms(1000)