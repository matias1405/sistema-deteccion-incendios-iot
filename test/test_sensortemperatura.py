import machine as m
import time

temp_input = m.Pin(35, m.Pin.IN)
adc_temp = m.ADC(temp_input)
adc_temp.atten(m.ADC.ATTN_2_5DB)

while True:
    temp = adc_temp.read_uv()
    #max = 9.7563*(temp**(-0.251))
    #temp_1 = temp/4095*max
    temp_1 = temp/4095*3.3
    print("temperatura con funcion expo: ", temp_1*100)
    #temp_2 = temp/4095*1.619
    #print("temperatura con funcion 1.619: ", temp_2*100)
    #temp_3 = temp/4095*1.485
    #print("temperatura con funcion 1.485: ", temp_3*100)
    time.sleep_ms(3000)
