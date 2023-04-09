from machine import Pin
import time



class Lcd:

    # commands
    LCD_CLEARDISPLAY = 0x01
    LCD_RETURNHOME = 0x02
    LCD_ENTRYMODESET = 0x04
    LCD_DISPLAYCONTROL = 0x08
    LCD_CURSORSHIFT = 0x10
    LCD_FUNCTIONSET = 0x20
    LCD_SETCGRAMADDR = 0x40
    LCD_SETDDRAMADDR = 0x80

    # flags for display entry mode
    LCD_ENTRYRIGHT = 0x00
    LCD_ENTRYLEFT = 0x02
    LCD_ENTRYSHIFTINCREMENT = 0x01
    LCD_ENTRYSHIFTDECREMENT = 0x00

    #flags for display on/off control
    LCD_DISPLAYON = 0x04
    LCD_DISPLAYOFF = 0x00
    LCD_CURSORON = 0x02
    LCD_CURSOROFF = 0x00
    LCD_BLINKON = 0x01
    LCD_BLINKOFF = 0x00

    # flags for display/cursor shift
    LCD_DISPLAYMOVE = 0x08
    LCD_CURSORMOVE = 0x00
    LCD_MOVERIGHT = 0x04
    LCD_MOVELEFT = 0x00

    # flags for function set
    LCD_8BITMODE = 0x10
    LCD_4BITMODE = 0x00
    LCD_2LINE = 0x08
    LCD_1LINE = 0x00
    LCD_5x10DOTS = 0x04
    LCD_5x8DOTS = 0x00

    displayfunction = 0x00
    displaycontrol = 0x00
    displaymode = 0x00

    def __init__(self, rs, en, d4, d5, d6, d7):
        self.rs_pin = Pin(rs, Pin.OUT)
        self.en_pin = Pin(en, Pin.OUT)
        self.d4_pin = Pin(d4, Pin.OUT)
        self.d5_pin = Pin(d5, Pin.OUT)
        self.d6_pin = Pin(d6, Pin.OUT)
        self.d7_pin = Pin(d7, Pin.OUT)
        self.displayfunction = self.LCD_4BITMODE | self.LCD_2LINE | self.LCD_5x8DOTS

        self.initialize(16, 2)

    def initialize(self, cols, lines):

        self.numlines = lines

        self.setRowOffsets(0x00, 0x40, 0x00 + cols, 0x40 + cols)

        self.rs_pin.value(0)
        self.en_pin.value(0)

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
        self.send(self.LCD_FUNCTIONSET | self.displayfunction, False)  # Modo de 4 bits
        self.displaycontrol = self.LCD_DISPLAYON | self.LCD_CURSOROFF | self.LCD_BLINKOFF
        self.display()
        self.displaymode = self.LCD_ENTRYLEFT | self.LCD_ENTRYSHIFTDECREMENT
        self.send(self.LCD_ENTRYMODESET | self.displaymode, False) 

    def setRowOffsets(self, row0, row1, row2, row3):
        self._row_offsets = [0, 0, 0, 0]
        self._row_offsets[0] = row0
        self._row_offsets[1] = row1
        self._row_offsets[2] = row2
        self._row_offsets[3] = row3

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

    def display(self):
        self.displaycontrol |= self.LCD_DISPLAYON
        self.send(self.LCD_DISPLAYCONTROL | self.displaycontrol, False)

    def clear(self):
        self.send(0x01, False)
        time.sleep_ms(200)

    def home(self):
        self.send(self.LCD_RETURNHOME, False)
        time.sleep_ms(200)

    def setCursor(self, col, row):
        max_lines = len(self._row_offsets)
        if row >= max_lines:
            row = max_lines - 1
        if row >= self.numlines:
            row = self.numlines - 1
    
        self.send(self.LCD_SETDDRAMADDR | (col + self._row_offsets[row]), False)


    def write(self, text):
        for char in text:
            self.send(int(ord(char)), True)
            print(char)
            print(ord(char))
            print(hex(ord(char)))
            print("-------------")
            #time.sleep_us(50)
