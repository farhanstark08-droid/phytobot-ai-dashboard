/*
  ESP32 MAIN CONTROLLER: DHT11 + capacitive soil moisture + NEO-6M + 3 IR sensors
  Sends telemetry JSON to the Flask dashboard over Wi-Fi.
  Install libraries: TinyGPSPlus, DHT sensor library by Adafruit.
  Update Wi-Fi and SERVER_IP before uploading.
*/
#include <WiFi.h>
#include <HTTPClient.h>
#include <TinyGPSPlus.h>
#include <DHT.h>

const char* WIFI_SSID = "YOUR_WIFI_NAME";
const char* WIFI_PASS = "YOUR_WIFI_PASSWORD";
const char* SERVER_URL = "http://192.168.1.10:5000/api/telemetry"; // laptop IP

#define DHTPIN 4
#define DHTTYPE DHT11
#define SOIL_PIN 34
#define IR_LEFT 25
#define IR_CENTER 26
#define IR_RIGHT 27
#define OBSTACLE_PIN 33 // optional digital obstacle output; adapt to your module
#define GPS_RX 16        // ESP32 RX2 <- NEO-6M TX
#define GPS_TX 17        // ESP32 TX2 -> NEO-6M RX (optional)
#define IR_ACTIVE_LEVEL LOW // change to HIGH if your IR module is active-HIGH

DHT dht(DHTPIN, DHTTYPE);
TinyGPSPlus gps;
HardwareSerial GPSSerial(2);

void setup() {
  Serial.begin(115200);
  dht.begin();
  GPSSerial.begin(9600, SERIAL_8N1, GPS_RX, GPS_TX);
  pinMode(IR_LEFT, INPUT);
  pinMode(IR_CENTER, INPUT);
  pinMode(IR_RIGHT, INPUT);
  pinMode(OBSTACLE_PIN, INPUT);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.println("\nWi-Fi connected. ESP32 IP: " + WiFi.localIP().toString());
}

void loop() {
  while (GPSSerial.available()) gps.encode(GPSSerial.read());

  if (WiFi.status() == WL_CONNECTED) {
    float temp = dht.readTemperature();
    float hum = dht.readHumidity();
    int raw = analogRead(SOIL_PIN);
    // Calibrate these two values in your own soil; dryRaw should be larger on many capacitive sensors.
    const int dryRaw = 3200, wetRaw = 1400;
    float soil = constrain(map(raw, dryRaw, wetRaw, 0, 100), 0, 100);

    int l = (digitalRead(IR_LEFT) == IR_ACTIVE_LEVEL) ? 1 : 0;
    int c = (digitalRead(IR_CENTER) == IR_ACTIVE_LEVEL) ? 1 : 0;
    int r = (digitalRead(IR_RIGHT) == IR_ACTIVE_LEVEL) ? 1 : 0;
    int obstacle = digitalRead(OBSTACLE_PIN) == LOW ? 1 : 0; // adapt to your sensor polarity

    String lat = gps.location.isValid() ? String(gps.location.lat(), 6) : "null";
    String lon = gps.location.isValid() ? String(gps.location.lng(), 6) : "null";
    String json = "{";
    json += "\"temperature\":" + String(isnan(temp) ? 0 : temp, 1) + ",";
    json += "\"humidity\":" + String(isnan(hum) ? 0 : hum, 1) + ",";
    json += "\"soil_moisture\":" + String(soil, 1) + ",";
    json += "\"latitude\":" + lat + ",\"longitude\":" + lon + ",";
    json += "\"satellites\":" + String(gps.satellites.isValid() ? gps.satellites.value() : 0) + ",";
    json += "\"ir_left\":" + String(l) + ",\"ir_center\":" + String(c) + ",\"ir_right\":" + String(r) + ",";
    json += "\"obstacle\":" + String(obstacle);
    json += "}";

    HTTPClient http;
    http.begin(SERVER_URL);
    http.addHeader("Content-Type", "application/json");
    http.POST(json);
    http.end();
  }
  delay(2000);
}
