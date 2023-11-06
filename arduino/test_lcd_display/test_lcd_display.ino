// include the library code:
#include <LiquidCrystal.h>

const int rs = 14;
const int en = 13;
const int d4 = 32;
const int d5 = 25;
const int d6 = 27;
const int d7 = 26;//12

LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
 
// initialize the library with the numbers of the interface pins
//LiquidCrystal lcd(14, 13, 32, 25, 27, 12);
 
void setup() {
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  // Print a message to the LCD.
  lcd.print("circuitschools.");
  delay(5000);
}
 
void loop() {
  // set the cursor to column 0, line 1
  // (note: line 1 is the second row, since counting begins with 0):
  lcd.setCursor(0, 1);
  // print the number of seconds since reset:
  lcd.print(millis() / 1000);
}
