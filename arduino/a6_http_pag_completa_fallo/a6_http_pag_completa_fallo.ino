void setup() {
  Serial.begin(115200);
  Serial2.begin(115200, SERIAL_8N1, 16, 17); // Configurar el puerto serial 2 para comunicarse con el módulo A6
  delay(1000);

  Serial.println("Configurando el módulo A6...");
  sendATCommand("AT"); // Comprobar la conexión con el módulo A6
  sendATCommand("AT+CGATT=1"); // Habilitar el acceso GPRS
  delay(1000);

  sendATCommand("AT+CSTT=\"internet.movistar.com.ar\""); // Configurar el APN de nuestro proveedor
  delay(1000);

  sendATCommand("AT+CIICR"); // Establecer la conexión GPRS
  delay(3000);

  sendATCommand("AT+CIFSR"); // Obtener la dirección IP asignada por el proveedor
  delay(1000);
}

void loop() {
  Serial.println("Realizando la solicitud HTTP GET...");
  sendATCommand("AT+CIPSTART=\"TCP\",\"www.google.com\",80"); // Establecer la conexión TCP con el servidor de Google
  delay(1000);

  sendATCommand("AT+CIPRXGET=1"); // Recibir la respuesta completa en una sola transmisión
  delay(1000);

  String getRequest = "GET / HTTP/1.1\r\nHost: www.google.com\r\nConnection: close\r\n\r\n";
  String sendRequest = "AT+CIPSEND=" + String(getRequest.length()) + "\r\n";
  sendATCommand(sendRequest); // Enviar el comando "AT+CIPSEND" con el tamaño del mensaje a enviar
  delay(1000);

  sendATCommand(getRequest); // Enviar la solicitud HTTP GET

  Serial.println("Esperando respuesta del servidor...");
  while (!Serial2.available()) {
    delay(100);
  }

  Serial.println("Respuesta del servidor:");
  while (Serial2.available()) {
    Serial.write(Serial2.read());
  }
  Serial.println();

  sendATCommand("AT+CIPCLOSE"); // Cerrar la conexión TCP
  delay(1000);
}

void sendATCommand(String command) {
  Serial2.println(command); // Enviar el comando AT al módulo A6
  delay(1000);
}