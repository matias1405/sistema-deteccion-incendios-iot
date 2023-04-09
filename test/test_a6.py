import machine as m
import time
import json

PIN_TX_A6 = 17 #pin 28
PIN_RX_A6 = 16 #pin 27
PIN_LED_INTERNO = 2
pwr = m.Pin(2, m.Pin.OUT)
pwr.on()
enable = m.Pin(15, m.Pin.OUT)
enable.on()
direccion = "GET /prueba-http/ HTTP/1.1\r\nHost: www.prometec.net\r\nConnection:"
#comando = "AT+CIPSEND="+str(len(direccion))
#led = m.Pin(PIN_LED_INTERNO, m.Pin.OUT)
#led.off()
time.sleep(1)
#led.on()
time.sleep(1)
print("inciando...")
u6 = m.UART(1, baudrate=115200, rx=PIN_RX_A6, tx=PIN_TX_A6)
time.sleep(1)
print("...")
def send_at_command(command):
    print("enviando..." , command)
    command = command + "\r\n"
    u6.write(command)
    time.sleep(1)
    response = u6.read()
    response_str = response#.decode()
    print(response_str)
    return response_str

def send_at_command2(command):
    print("enviando..." , command)
    u6.write(command)
    time.sleep(0.2)
    response = u6.read()
    response_str = response#.decode()
    print(response_str)

while True:
    command = "ATI\r\n"
    u6.write(command)
    time.sleep(0.5)
    result = u6.read()
    print(result)
    if result == None:
        time.sleep(1)
        continue
    if len(result) > 0 and "OK" in result:
        print("modulo detectado")
        break
    time.sleep(1)

time.sleep(3)
print("enviando comando para saber estado de pin")
send_at_command("AT+IPR?")
time.sleep(3)
send_at_command("AT+CPIN=?")
time.sleep(3)
send_at_command("AT+CPIN?")
time.sleep(2)
send_at_command("AT+CPIN=1234")
time.sleep(3)
send_at_command("AT+CPIN?")
time.sleep(2)
send_at_command("AT+CREG=1")
time.sleep(3)
send_at_command("AT+CREG?")
time.sleep(3)
send_at_command("AT+CGATT?")
time.sleep(3)
send_at_command("AT+CGATT=1")
time.sleep(3)
#send_at_command("AT+CGDCONT=1,\"IP\",\"wap.gprs.unifon.com.ar\"")
send_at_command("AT+CGDCONT?")
#send_at_command("AT+CGDCONT=1,\"IP\",\"igprs.claro.com.ar\"")
time.sleep(3)
send_at_command("AT+CGACT=1, 1")
time.sleep(3)
send_at_command("AT+CGACT?")
time.sleep(3)
send_at_command("AT+CGPADDR=1")
time.sleep(3)
send_at_command("AT+CIPSTATUS")
time.sleep(3)
send_at_command("AT+CGREG=1")
time.sleep(3)
send_at_command("AT+CGREG?")
time.sleep(3)
send_at_command("AT+CIPSTATUS")
time.sleep(3)
send_at_command("AT+CSTT?")
time.sleep(3)
#send_at_command("AT+CSTT=\"wap.gprs.unifon.com.ar\", \"wap\", \"wap\"")
#send_at_command("AT+CSTT=\"igprs.claro.com.ar\", \"\", \"\"")
time.sleep(3)
send_at_command("AT+CIICR")
time.sleep(3)
"""
while True:
    command = "AT+CIICR\r\n"
    u6.write(command)
    time.sleep(0.5)
    result = u6.read()
    print(result)
    if result == None:
        time.sleep(1)
        continue
    if len(result) > 0 and "OK" in result:
        print("CIICR conectado")
        break
    time.sleep(1)
"""
send_at_command("AT+CIFSR")
time.sleep(3)
send_at_command("AT+CIPSTATUS")
time.sleep(3)
send_at_command("AT+CIPSTART=\"TCP\",\"www.prometec.net\",80")
time.sleep(3)
send_at_command("AT+CIPSTATUS")
time.sleep(3)
str_len=len("GET / HTTP/1.1\r\nHost: www.prometec.net\r\nConnection: close\r\n\r\n")
cadena = "AT+CIPSEND=" + str(str_len)
send_at_command2(cadena)
time.sleep(3)
send_at_command2("GET / HTTP/1.1\r\nHost: www.prometec.net\r\nConnection: close\r\n\r\n")
time.sleep(0.2)
result = u6.read()
print(result)
time.sleep(0.2)


"""
while True:
    command = "AT+CIPSTART=\"TCP\",\"www.google.com\",80\r\n"
    u6.write(command)
    time.sleep(0.5)
    result = u6.read()
    print(result)
    if result == None:
        time.sleep(1)
        continue
    if len(result) > 0 and "OK" in result:
        print("modulo detectado")
        break
    time.sleep(1)
"""
send_at_command("AT+CIPCLOSE")
time.sleep(3)
send_at_command("AT+CIPSHUT")
time.sleep(3)

"""
send_at_command("AT+CSTT=\"wap.gprs.unifon.com.ar\",\"wap\",\"wap\"")
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
"""