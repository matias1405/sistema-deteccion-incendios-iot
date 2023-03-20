import machine as m
import time
import json

PIN_TX_A6 = 17 #pin 28
PIN_RX_A6 = 16 #pin 27
pwr = m.Pin(15, m.Pin.OUT)
pwr.on()
print("hola")
enable = m.Pin(0, m.Pin.OUT)
enable.on()
direccion = "GET /prueba-http/ HTTP/1.1\r\nHost: www.prometec.net\r\nConnection:"
comando = "AT+CIPSEND="+str(len(direccion))
led = m.Pin(2, m.Pin.OUT)
led.off()
time.sleep(1)
led.on()
time.sleep(1)
print("ok")
u6 = m.UART(1, baudrate=9600, rx=16, tx=17)
time.sleep(1)
print("hola")
def send_at_command(command):
    print("enviando..." , command)
    command = command + "\r\n"
    u6.write(command)
    response = u6.read()
    print(response)
    if type(response) == list: 
        for l in response:
            print(l)
    return response

while True:
    result = send_at_command("ATI")
    if result == None:
        time.sleep(1)
        continue
    if len(result) > 0 and "OK\r\n" in result:
        break
    time.sleep(1)

time.sleep(6)
#send_at_command("AT+IPR=9600")
#time.sleep(3)
#u6 = m.UART(1, baudrate=9600)
#time.sleep(1)
send_at_command("AT+CPIN=\"1234\"")
time.sleep(6)
send_at_command("AT+CREG?")
time.sleep(6)
send_at_command("AT+CREG?")
time.sleep(6)
send_at_command("AT+CGATT=1")
time.sleep(6)
send_at_command("AT+CSTT=\"wap.gprs.unifon.com.ar\",\"internet\",\"internet\"")
time.sleep(6)
send_at_command("AT+CIICR")
time.sleep(6)
send_at_command("AT+CIFSR")
time.sleep(6)
send_at_command("AT+CIPSTART=\"TCP\",\"www.prometec.net\",\"80\"")
time.sleep(6)
send_at_command(comando)
time.sleep(6)
send_at_command(direccion)
time.sleep(6)
send_at_command("AT+CIPCLOSE")
time.sleep(6)
send_at_command("AT+CIPSHUT")
time.sleep(6)