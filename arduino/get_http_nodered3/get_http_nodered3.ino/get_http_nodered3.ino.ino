#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiServer.h>
#include <LiquidCrystal.h>

const int rs = 14;
const int en = 13;
const int d4 = 32;
const int d5 = 25;
const int d6 = 27;
const int d7 = 26;//12

LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

const char* ssid = "ALFARO";
const char* password = "MATIAS64P13";
IPAddress local_IP(192, 168, 100, 10);  // Cambia la dirección IP según tus preferencias
IPAddress gateway(192, 168, 100, 1);
IPAddress subnet(255, 255, 255, 0);
IPAddress primaryDNS(8, 8, 8, 8);   //optional
IPAddress secondaryDNS(8, 8, 4, 4); //optional

String url_base = "http://ec2-15-229-8-95.sa-east-1.compute.amazonaws.com:1880/nodered?";
WiFiServer serverSocket(2020);
int COUNTER = 0;

HTTPClient http;

void imprimir(String cadena, int x=0, int y=0){
  lcd.clear();
  lcd.setCursor(x, y);
  lcd.print(cadena);
  delay(1000);
}

void setup() {
  lcd.begin(16, 2);
  // Print a message to the LCD.
  imprimir("Iniciando...");
  delay(2000);
  if (!WiFi.config(local_IP, gateway, subnet, primaryDNS, secondaryDNS)) {
    imprimir("STA Failed to configure");
  }
  // Conectar a la red Wi-Fi
  
  imprimir("Conectando a la red Wi-Fi ");
  imprimir(ssid, 0, 1);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    imprimir(".");
  }

  
  imprimir("Conexión Wi-Fi establecida");
  delay(500);
  //WiFi.config(localIP, gateway, subnet);
  delay(500);
  imprimir("Dirección IP estatica configurada: ");
  imprimir(WiFi.localIP().toString(), 0, 1);
  delay(500);
  serverSocket.begin();
  delay(500);
}

void loop() {
  WiFiClient client = serverSocket.available();
  
  if (client) {
    imprimir("Cliente conectado");
    
    while (client.connected()) {
      if (client.available()) {
        String request = client.readStringUntil('\r');
        imprimir("Mensaje recibido: ");
        imprimir(request);
        // Procesar el mensaje recibido y preparar una respuesta
        if (COUNTER > 15){
          String response = "STOP";
          client.println(response);
        }
        else{
          String response = "OK";
          client.println(response);
        }
        String url = url_base + request;
        //String url = url_base;
        
        http.begin(url);

        int httpCode = http.GET();
        if (httpCode > 0) {
          //imprimir("Código de respuesta HTTP: %d\n", httpCode);
          String payload = http.getString();
          imprimir("Respuesta del servidor:");
          imprimir(payload), 0, 1;
        } else {
          imprimir("Error en la solicitud HTTP");
        }

        http.end();
      }
    }
    
    delay(10);
    client.stop();
    imprimir("Cliente desconectado");
  }
}

