/*
  ESP32-CAM AUTOMATIC FRAME SENDER
  Sends a JPEG frame to Flask every 5 seconds. No manual upload button is needed.
  Select AI Thinker ESP32-CAM board and configure camera pins for your exact board.
  Update Wi-Fi and laptop SERVER_IP.
*/
#include "esp_camera.h"
#include <WiFi.h>
#include <HTTPClient.h>

const char* WIFI_SSID = "YOUR_WIFI_NAME";
const char* WIFI_PASS = "YOUR_WIFI_PASSWORD";
const char* FRAME_URL = "http://192.168.1.10:5000/api/frame";

#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

void setup() {
  Serial.begin(115200);
  camera_config_t c;
  c.ledc_channel=LEDC_CHANNEL_0; c.ledc_timer=LEDC_TIMER_0;
  c.pin_d0=Y2_GPIO_NUM; c.pin_d1=Y3_GPIO_NUM; c.pin_d2=Y4_GPIO_NUM; c.pin_d3=Y5_GPIO_NUM;
  c.pin_d4=Y6_GPIO_NUM; c.pin_d5=Y7_GPIO_NUM; c.pin_d6=Y8_GPIO_NUM; c.pin_d7=Y9_GPIO_NUM;
  c.pin_xclk=XCLK_GPIO_NUM; c.pin_pclk=PCLK_GPIO_NUM; c.pin_vsync=VSYNC_GPIO_NUM;
  c.pin_href=HREF_GPIO_NUM; c.pin_sccb_sda=SIOD_GPIO_NUM; c.pin_sccb_scl=SIOC_GPIO_NUM;
  c.pin_pwdn=PWDN_GPIO_NUM; c.pin_reset=RESET_GPIO_NUM;
  c.xclk_freq_hz=20000000; c.pixel_format=PIXFORMAT_JPEG;
  c.frame_size=FRAMESIZE_VGA; c.jpeg_quality=12; c.fb_count=1;
  if (esp_camera_init(&c) != ESP_OK) { Serial.println("Camera init failed"); while(true) delay(1000); }
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status()!=WL_CONNECTED) delay(500);
  Serial.println("Camera online");
}

void loop() {
  if (WiFi.status()==WL_CONNECTED) {
    camera_fb_t *fb=esp_camera_fb_get();
    if (fb) {
      HTTPClient http;
      http.begin(FRAME_URL);
      http.addHeader("Content-Type","image/jpeg");
      int code=http.POST(fb->buf, fb->len);
      Serial.printf("Frame sent, HTTP %d\n", code);
      http.end();
      esp_camera_fb_return(fb);
    }
  }
  delay(5000); // adjust capture interval for your rover speed and camera power
}
