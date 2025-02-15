#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "your_wifi_ssid";
const char* password = "your_wifi_password";
const char* mqtt_server = "your_mqtt_broker_ip";

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  client.setServer(mqtt_server, 1883);
  while (!client.connected()) {
    if (client.connect("ESP32_Client")) {
      Serial.println("Connected to MQTT Broker");
    } else {
      delay(500);
    }
  }
}

void loop() {
  float acceleration = random(1, 10);
  float temperature = random(20, 40);

  char acc_str[8], temp_str[8];
  dtostrf(acceleration, 4, 2, acc_str);
  dtostrf(temperature, 4, 2, temp_str);

  client.publish("ev/acceleration", acc_str);
  client.publish("ev/temperature", temp_str);

  delay(5000);  // Send data every 5 seconds
}