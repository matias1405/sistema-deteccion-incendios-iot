#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiServer.h>

const char* ssid = "TeleCentro-7f93";
const char* password = "MWYKRJYWKTMK";

String url_base = "http://ec2-15-229-8-95.sa-east-1.compute.amazonaws.com:1880/nodered?";
WiFiServer serverSocket(2020);
int COUNTER = 0;

HTTPClient http;

void setup() {
  Serial.begin(115200);
  delay(1000);

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
  Serial.println("Dirección IP obtenida: ");
  Serial.println(WiFi.localIP());
  serverSocket.begin();
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
        http.begin(url);
        int httpCode = http.GET();

        // Si la solicitud fue exitosa, leer la respuesta del servidor
        if (httpCode == HTTP_CODE_OK) {
          String payload = http.getString();
          Serial.println(payload);
        } else {
          Serial.println("Error en la solicitud HTTP");
        }
      }
    }
    
    delay(10);
    client.stop();
    Serial.println("Cliente desconectado");    
  }
}

