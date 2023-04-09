from machine import Pin
import time

class Lcd:
    def __init__(self, rs, en, d4, d5, d6, d7):
        self.rs_pin = Pin(rs, Pin.OUT)
        self.en_pin = Pin(en, Pin.OUT)
        self.d4_pin = Pin(d4, Pin.OUT)
        self.d5_pin = Pin(d5, Pin.OUT)
        self.d6_pin = Pin(d6, Pin.OUT)
        self.d7_pin = Pin(d7, Pin.OUT)
        self.initialize()

    def initialize(self):
        # Esperar por lo menos 15ms después de encender el LCD
        time.sleep_ms(50)

        # Enviar los comandos de inicialización según la hoja de datos
        self.send(0x30, False)
        time.sleep_us(4500)
        self.send(0x30, False)
        time.sleep_us(4500)
        self.send(0x30, False)
        time.sleep_us(150)

        # Configurar el LCD para trabajar en modo de 4 bits
        self.send(0x20, False)  # Modo de 8 bits
        self.send(0x28, False)  # Modo de 4 bits
        self.send(0x08, False)  # Apagar el display
        self.send(0x01, False)  # Limpiar la pantalla
        self.send(0x06, False)  # Configurar el cursor para avanzar
        self.send(0x0C, False)  # Encender el display sin cursor ni parpadeo

    def send(self, value, mode):
        self.rs_pin.value(mode)
        self.d7_pin.value((value >> 3) & 1)
        self.d6_pin.value((value >> 2) & 1)
        self.d5_pin.value((value >> 1) & 1)
        self.d4_pin.value(value & 1)
        self.pulse_enable()

        self.d7_pin.value((value >> 7) & 1)
        self.d6_pin.value((value >> 6) & 1)
        self.d5_pin.value((value >> 5) & 1)
        self.d4_pin.value((value >> 4) & 1)
        self.pulse_enable()

    def pulse_enable(self):
        self.en_pin.value(0)
        time.sleep_us(1)
        self.en_pin.value(1)
        time.sleep_us(1)
        self.en_pin.value(0)
        time.sleep_us(100)

    def clear(self):
        self.send(0x01, False)
        time.sleep_ms(200)

    def move_cursor(self, row, col):
        pos = col
        if row == 1:
            pos += 0x40
        self.send(0x80 + pos, False)

    def write(self, text):
        for char in text:
            self.send(int(ord(char)), True)
            print(char)
            print(ord(char))
            print(hex(ord(char)))
            print("-------------")
            #time.sleep_us(50)
