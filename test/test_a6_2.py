import machine as m
import time

PIN_TX_A6 = 17 #pin 28
PIN_RX_A6 = 16 #pin 27
PIN_LED_INTERNO = 2
pwr = m.Pin(2, m.Pin.OUT)
pwr.on()
enable = m.Pin(15, m.Pin.OUT)
enable.on()
time.sleep(1)
print("inciando...")
#uart=m.UART(1, baudrate=115200)
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
    time.sleep(1)
    response = u6.read()
    response_str = response#.decode()
    print(response_str)
    return response_str

send_at_command("AT+CGATT=1")
time.sleep(6)
send_at_command("AT+CSTT=\"wap.gprs.unifon.com.ar\", \"wap\", \"wap\"")
time.sleep(6)
send_at_command("AT+CIICR")
time.sleep(6)
send_at_command("AT+CIFSR")
time.sleep(6)


send_at_command("AT+CIPSTART=\"TCP\",\"www.ec2-18-228-225-6.sa-east-1.compute.amazonaws.com\",1880")
time.sleep(3)
str_len=len("GET /temperatura?temp=26 HTTP/1.1\r\nHost: www.ec2-18-228-225-6.sa-east-1.compute.amazonaws.com\r\nConnection: close\r\n\r\n")
cadena = "AT+CIPSEND=" + str(str_len) + "\r\n"
send_at_command2("AT+CIPSEND\r\n")
time.sleep(3)
send_at_command2("GET / HTTP/1.1\r\nHost: www.google.com\r\nConnection: close\r\n\r\n")
time.sleep(3)

send_at_command("AT+CIPCLOSE")
time.sleep(3)
send_at_command("AT+CIPSHUT")
time.sleep(3)

#asyncmqqtclient libreria
#pushingbox
#node red