//sendATCommand("AT"); // Comprobar la conexión con el módulo A6
  //sendATCommand("AT+CGATT=1"); // Habilitar el acceso GPRS
  //sendATCommand("AT+CSTT=\"internet.movistar.com.ar\""); // Configurar el APN de nuestro proveedor
  //sendATCommand("AT+CIICR"); // Establecer la conexión GPRS
  //sendATCommand("AT+CIFSR"); // Obtener la dirección IP asignada por el proveedor
  //String getRequest = "GET / HTTP/1.1\r\nHost: www.google.com\r\nConnection: close\r\n\r\n";
  //String sendRequest = "AT+CIPSEND=" + String(getRequest.length()) + "\r\n";
  //sendATCommand(sendRequest); // Enviar el comando "AT+CIPSEND" con el tamaño del mensaje a enviar
  //sendATCommand(getRequest); // Enviar la solicitud HTTP GET
  //sendATCommand("AT+CIPCLOSE"); // Cerrar la conexión TCP


void setup() {
  Serial.begin(115200);
  Serial2.begin(115200, SERIAL_8N1, 16, 17); // Configurar el puerto serial 2 para comunicarse con el módulo A6
  delay(1000);

  Serial.println("Configurando el módulo A6...");
  
  //String getRequest = "GET / HTTP/1.1\r\nHost: www.google.com\r\nConnection: close\r\n\r\n";
  //String sendRequest = "AT+CIPSEND=" + String(getRequest.length()) + "\r\n";
  //Serial.println(sendRequest);
  delay(1000);
  
}

void loop() {
  String cadena = "";
  if (Serial.available()) {
    cadena = Serial.readString();
    //Serial.println(cadena);
    Serial2.println(cadena);
    delay(500);
    readResponse();
  } 
  delay(1000);
}

void sendATCommand(String command) {
  delay(1000);
}

void readResponse() {
  while (Serial2.available()) {
    Serial.write(Serial2.read());
  }
}
