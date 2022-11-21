import machine as m
import time
import json

PIN_TX_A6 = 1
PIN_RX_A6 = 3

u6 = m.UART(id=1, baudrate=9600, tx=PIN_TX_A6 , rx=PIN_RX_A6)
time.sleep(1)

def send_at_command(command):
    command = command + "\r\n"
    u6.write(command.encode())
    response = list(map(lambda elem: elem.decode(), u6.readlines()))
    for l in response:
        print(l)
    return response

while True:
    result = send_at_command("ATI")
    if len(result) > 0 and result[-1] == "OK\r\n":
        break
    time.sleep(1)

send_at_command("AT+CREG?")
time.sleep(5)