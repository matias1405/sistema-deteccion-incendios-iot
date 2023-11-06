#include <WiFi.h>
#include <WiFiClient.h>
#include <WiFiAP.h>
#include <WiFiServer.h>
#include <LiquidCrystal.h>

const char* ssid = "NombreDeLaRed";
const char* password = "ContraseñaDeLaRed";
//LiquidCrystal lcd(19, 23, 18, 17, 16, 15);
LiquidCrystal lcd(14, 13, 32, 25, 27, 12);

WiFiServer serverSocket(2020);  // Cambiar el puerto a 8080
int COUNTER = 0;

void setup() {
  delay(1000);

  lcd.begin(16, 2);
  // Conectarse a la red WiFi
  WiFi.softAP(ssid, password);
  
  IPAddress IP = WiFi.softAPIP();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Direccion IP:");
  lcd.setCursor(0, 1);
  lcd.print(IP);
  
  serverSocket.begin();
  delay(7000);
}

void loop() {
  WiFiClient client = serverSocket.available();
  
  if (client) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Cliente conectado");
    delay(1000);
    while (client.connected()) {
      if (client.available()) {
        String request = client.readStringUntil('\r');
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Mensaje recibido:");
        lcd.setCursor(0, 1);
        lcd.print(request);
        COUNTER += 1;
        // Procesar el mensaje recibido y preparar una respuesta
        if (COUNTER > 15){
          String response = "STOP";
          client.println(response);
        }
        else{
          String response = "OK";
          client.println(response);
        }        
      }
    }
    
    delay(10);
    client.stop();
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Cliente desconectado");
  }
}

