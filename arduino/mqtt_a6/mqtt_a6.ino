#include <GSM.h>
#include <SoftwareSerial.h>
#include <AsyncMqttClient.h>

const char* apn = "wap.gprs.unifon.com.ar";
const char* user = "wap";
const char* password = "wap";
const char* mqtt_server = "ec2-18-228-225-6.sa-east-1.compute.amazonaws.com";
const char* mqtt_user = "";
const char* mqtt_password = "";

SoftwareSerial gsmSerial(17, 16);
GSM gsmAccess(gsmSerial);
GSM_SMS sms;
GPRS gprs;
GSMClient gsmClient;
AsyncMqttClient mqttClient;

void setup() {
  Serial.begin(115200);
  gsmSerial.begin(115200);

  Serial.println("Conectando al servicio GSM...");
  while (gsmAccess.begin() != GSM_READY) {
    delay(1000);
  }
  Serial.println("Servicio GSM conectado");

  Serial.println("Conectando a la red GPRS...");
  while (!gprs.attachGPRS(apn, user, password)) {
    delay(1000);
  }
  Serial.println("Red GPRS conectada");

  mqttClient.onConnect(onMqttConnect);
  mqttClient.setServer(mqtt_server, 1883);
}

void loop() {
  if (!mqttClient.connected()) {
    Serial.println("Conectando al servidor MQTT...");
    mqttClient.connect();
  }

  // Publicar un mensaje en el tema "mi_tema"
  mqttClient.publish("temperatura", "23");

  // Esperar 1 minuto antes de publicar otro mensaje
  delay(60000);
}

void onMqttConnect(bool sessionPresent) {
  Serial.println("Conectado al servidor MQTT");
  Serial.print("Session present: ");
  Serial.println(sessionPresent);

  // Suscribirse al tema "mi_tema"
  mqttClient.subscribe("temperatura", 0);
}
