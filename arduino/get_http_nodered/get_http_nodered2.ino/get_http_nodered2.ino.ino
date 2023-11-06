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

const char* ssid = "FBWAY-473372_2.4";
const char* password = "qlWjQcTi";
IPAddress local_IP(192, 168, 100, 10);  // Cambia la dirección IP según tus preferencias
IPAddress gateway(192, 168, 100, 1);
IPAddress subnet(255, 255, 255, 0);
IPAddress primaryDNS(8, 8, 8, 8);   //optional
IPAddress secondaryDNS(8, 8, 4, 4); //optional

String url_base = "http://ec2-15-229-8-95.sa-east-1.compute.amazonaws.com:1880/nodered?temperatura=3";
WiFiServer serverSocket(2020);
int COUNTER = 0;

HTTPClient http;

void setup() {
  Serial.begin(115200);
  delay(1000);
  if (!WiFi.config(local_IP, gateway, subnet, primaryDNS, secondaryDNS)) {
    Serial.println("STA Failed to configure");
  }
  // Conectar a la red Wi-Fi
  Serial.println();
  Serial.println();
  Serial.print("Conectando a la red Wi-Fi ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("Conexión Wi-Fi establecida");
  delay(500);
  //WiFi.config(localIP, gateway, subnet);
  delay(500);
  Serial.println("Dirección IP estatica configurada: ");
  Serial.println(WiFi.localIP());
  delay(500);
  serverSocket.begin();
  delay(500);
}

void loop() {
  WiFiClient client = serverSocket.available();
  
  if (client) {
    Serial.println("Cliente conectado");
    
    while (client.connected()) {
      if (client.available()) {
        String request = client.readStringUntil('\r');
        Serial.print("Mensaje recibido: ");
        Serial.println(request);
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
          Serial.printf("Código de respuesta HTTP: %d\n", httpCode);
          String payload = http.getString();
          Serial.println("Respuesta del servidor:");
          Serial.println(payload);
        } else {
          Serial.println("Error en la solicitud HTTP");
        }

        http.end();
      }
    }
    
    delay(10);
    client.stop();
    Serial.println("Cliente desconectado");
  }
}

