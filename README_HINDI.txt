AGRIBOT AI – FULLY AUTOMATIC DASHBOARD (NO WATER PUMP)

FEATURES
- Live dashboard refresh every 2 seconds.
- ESP32 sends temperature, humidity, soil moisture, IR left/center/right and obstacle state.
- NEO-6M GPS latitude/longitude and satellite count update automatically.
- ESP32-CAM sends JPEG images automatically; no manual image upload.
- On every received image, Flask automatically runs the configured CNN model and records the result.
- Latest image, diagnosis, confidence and timestamp appear on dashboard.
- Water pump and irrigation controls are removed.

IMPORTANT: "Fully automatic" camera-to-dashboard workflow is provided. Real disease diagnosis needs your own trained CNN model.
If no model is installed, dashboard explicitly displays "AI model not configured"; it does not fake a result.

RUN ON LAPTOP
1. Extract this ZIP.
2. Open the extracted folder in Terminal / Command Prompt.
3. Install Python 3.10 or 3.11 recommended.
4. Run:
   python -m venv venv
   Windows: venv\Scripts\activate
   Mac/Linux: source venv/bin/activate
   pip install -r requirements.txt
   python app.py
5. On laptop, open: http://127.0.0.1:5000
6. Find laptop IPv4 address (Windows: ipconfig; Mac/Linux: ifconfig/ip addr).
7. Put that laptop IP in both ESP32 firmware files, e.g. http://192.168.1.10:5000
8. Put same Wi-Fi name/password in both firmware files. Laptop and ESP32 devices must be on the same Wi-Fi network.
9. Upload firmware to main ESP32 and ESP32-CAM. Open Serial Monitor to check messages.

HARDWARE NOTES
- NEO-6M: GPS TX -> ESP32 GPIO16 (RX2); GPS RX -> ESP32 GPIO17 (TX2, optional); common GND; use correct voltage levels for your module.
- IR sensors: sample pins GPIO25, GPIO26, GPIO27. Adjust pins and active HIGH/LOW logic to your modules.
- Soil sensor: GPIO34 is ADC input. Calibrate dryRaw/wetRaw in firmware for your sensor and soil.
- DHT11: sample data pin GPIO4.
- Obstacle input: sample GPIO33 is optional and must be adapted to your actual obstacle sensor.
- Keep motor supply separate from regulated ESP32 logic supply; connect grounds together. Do not connect motors to ESP32 pins.
- GPS may not get a fix indoors. Test outdoors with open sky; dashboard shows NO FIX until coordinates are valid.
- For the ESP32-CAM, camera pin mapping above is for AI Thinker ESP32-CAM. Confirm your board variant.

IR LINE FOLLOWING
The dashboard visualizes sensor states; it does not itself steer the robot. Your motor-control firmware must use the same IR readings to drive the L298N. A basic path-following truth table depends on whether your IR modules output LOW or HIGH on the dark line. Calibrate on your actual track before running.

AI MODEL
See models/README.txt. Use a tomato leaf model if the demonstration crop is tomato. The labels and preprocessing must match your trained model.
