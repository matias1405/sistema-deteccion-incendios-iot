import network
import urequests

# SSID y contraseña de la red Wi-Fi
ssid = "moto g9 play"
password = "1234matias"

# Inicializar objeto WLAN
wlan = network.WLAN(network.STA_IF)

# Activar WLAN
wlan.active(True)

# Conectarse a la red Wi-Fi
wlan.connect(ssid, password)

# Esperar a que la conexión se establezca
while not wlan.isconnected():
    pass

# Imprimir dirección IP asignada por la red Wi-Fi
print("Conectado a la red Wi-Fi. Dirección IP: ", wlan.ifconfig()[0])

# URL de la API pública
url = "https://jsonplaceholder.typicode.com/todos/1"

# Realizar solicitud GET
response = urequests.get(url)

# Imprimir contenido de la respuesta
print(response.text)
