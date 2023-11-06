#include <SoftwareSerial.h>

SoftwareSerial SerialAT(16, 17); // RX, TX

void setup() {
  Serial.begin(115200);
  SerialAT.begin(9600);
  
  // Iniciar comunicación GPRS (pueden variar los comandos según el módulo A6)
  SerialAT.println("AT");
  delay(1500);
  SerialAT.println("AT+CGATT=1"); // Activar el contexto GPRS
  delay(3000);

  sendATCommand("AT+CSTT=\"wap.gprs.unifon.com.ar\",\"wap\",\"wap\""); // Configurar el APN de nuestro proveedor
  delay(3000);

  sendATCommand("AT+CIICR"); // Establecer la conexión GPRS
  delay(3000);

  sendATCommand("AT+CIFSR"); // Obtener la dirección IP asignada por el proveedor
  delay(3000);
}

void loop() {
  // Realizar la petición GET
  SerialAT.println("AT+CIPSTART=\"TCP\",\"ec2-15-229-8-95.sa-east-1.compute.amazonaws.com\",1880");
  delay(2000);
  
  SerialAT.print("AT+CIPSEND=");
  SerialAT.println(100); // Tamaño de la solicitud GET
  
  delay(1500);
  SerialAT.println("GET /nodered?tem=10 HTTP/1.0");
  SerialAT.println("Host: ec2-15-229-8-95.sa-east-1.compute.amazonaws.com");
  SerialAT.println();
  
  delay(1000);
  
  // Leer y mostrar la respuesta
  while (SerialAT.available()) {
    char c = SerialAT.read();
    Serial.write(c);
  }
  
  SerialAT.println("AT+CIPCLOSE"); // Cerrar la conexión
  delay(5000); // Esperar antes de la siguiente solicitud
}


void sendATCommand(String command) {
  SerialAT.println(command); // Enviar el comando AT al módulo A6
  delay(1500);
  readResponse();
  delay(1000);
}

void readResponse() {
  while (SerialAT.available()) {
    Serial.write(SerialAT.read());
  }
}