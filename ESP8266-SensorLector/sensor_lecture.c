#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

const char* ssid = "ARRIS-A802";
const char* password = "D782A84123D8143A";

// Cambia esta IP por la de tu PC (ver ipconfig)
//const char* server_ip = "192.168.0.1";  // ← Cambia esto
const char* server_ip = "54.167.101.155";
const char* serverAddress = "http://192.168.0.10:5000/data/append";
const int IR_Sensor = A0;
float SIR;
float dist;

void setup() {
  Serial.begin(9600);
  delay(1000);

  WiFi.begin(ssid, password);
  Serial.print("Conectando a WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConectado a WiFi");
  Serial.print("Dirección IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  SIR = analogRead(IR_Sensor);
  dist = pow(3027.4 / SIR, 1.2134);

  Serial.print("Distancia medida = ");
  Serial.println(dist);

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    WiFiClient client;

    // URL correcta
    String url = "http://" + String(server_ip) + ":5000/data/append?dist=" + String(dist, 2);

    http.begin(client, url);
    //http.addHeader("?dist=", String(dist, 2));
    int httpCode = http.GET();

    if (httpCode > 0) {
      Serial.print("Código de respuesta HTTP: ");
      Serial.println(httpCode);
    } else {
      Serial.print("Error en la solicitud: ");
      Serial.println(http.errorToString(httpCode).c_str());
    }

    http.end();
  } else {
    Serial.println("WiFi no conectado");
  }

  delay(2000);
}
