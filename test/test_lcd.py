"""
import lcd_display2
import time


#Pins 34-39 are input only, and also do not have internal pull-up resistors

PIN_rs = 19
PIN_en = 23
PIN_d4 = 18
PIN_d5 = 17
PIN_d6 = 16
PIN_d7 = 15


lcd = lcd_display2.Lcd(rs=PIN_rs, en=PIN_en, d4=PIN_d4, d5=PIN_d5, d6=PIN_d6, d7=PIN_d7)

lcd.clear()
print("llegue")
lcd.home()
lcd.write("hola mundo")
lcd.display()
time.sleep(6)
lcd.clear()
lcd.display()
"""

from machine import Pin
from gpio_lcd import GpioLcd
import time
 
# Create the LCD object
lcd = GpioLcd(rs_pin=Pin(14),
              enable_pin=Pin(13),
              d4_pin=Pin(32),
              d5_pin=Pin(25),
              d6_pin=Pin(27),
              d7_pin=Pin(26),
              num_lines=2, num_columns=16)
 
# #The following line of codes should be tested one by one according to your needs
lcd.clear()
time.sleep(1)
lcd.move_to(0,0)
# #1. To print a string to the LCD, you can use
lcd.putstr('UTN FRT')
# #2. Now, to clear the display.
#lcd.clear()
time.sleep(1)
# #3. and to exactly position the cursor location
lcd.move_to(0,1)
lcd.putstr('2023')
time.sleep(1)