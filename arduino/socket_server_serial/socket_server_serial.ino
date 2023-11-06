#include <WiFi.h>
#include <WiFiClient.h>
#include <WiFiAP.h>
#include <WiFiServer.h>

const char* ssid = "NombreDeLaRed";
const char* password = "ContraseñaDeLaRed";

WiFiServer serverSocket(2020);  // Cambiar el puerto a 8080
int COUNTER = 0;

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  // Conectarse a la red WiFi
  WiFi.softAP(ssid, password);
  
  IPAddress IP = WiFi.softAPIP();
  Serial.print("Dirección IP de la red: ");
  Serial.println(IP);
  
  server.begin();
  delay(3000);
}

void loop() {
  WiFiClient client = server.available();
  
  if (client) {
    Serial.println("Cliente conectado");
    
    while (client.connected()) {
      if (client.available()) {
        String request = client.readStringUntil('\r');
        Serial.print("Mensaje recibido: ");
        Serial.println(request);
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
    Serial.println("Cliente desconectado");
  }
}
