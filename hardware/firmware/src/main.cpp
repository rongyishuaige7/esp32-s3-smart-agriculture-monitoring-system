/**
 * ESP32-S3 智能农业环境监测教学原型（公开默认受限观测构建）。
 *
 * 默认只初始化传感器与 OLED 的观测路径；它不连接 Wi-Fi/TCP，且不把
 * GPIO5/GPIO6/GPIO38 配置为输出。启用本地实验配置也不等于设备身份、
 * 加密、命令确认、真实负载动作或电气安全已经得到验证。
 */
#include <Arduino.h>
#include <cstring>
#include <math.h>
#include <Wire.h>
#include <DHT.h>
#include <BH1750.h>
#include <ACD10.h>
#include <Adafruit_BMP280.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "config.h"

#if EXPERIMENTAL_WIFI_TCP_ENABLED
#include <WiFi.h>
#include <WiFiClient.h>
#endif

#if EXPERIMENTAL_ACTUATORS_ENABLED
#include <FastLED.h>
#endif

namespace {
constexpr unsigned long LOOP_INTERVAL_MS = 5000UL;
constexpr uint8_t DHT_PIN = 4;
constexpr uint8_t I2C_SDA = 8;
constexpr uint8_t I2C_SCL = 9;
constexpr uint8_t BMP280_ADDR = 0x76;
constexpr uint8_t WS2812B_PIN = 38;
constexpr uint8_t FAN_PIN_A = 5;
constexpr uint8_t FAN_PIN_B = 6;
constexpr uint8_t NUM_LEDS = 16;
constexpr int SCREEN_WIDTH = 128;
constexpr int SCREEN_HEIGHT = 64;

DHT dht(DHT_PIN, DHT11);
BH1750 bh(0x23);
ACD10 acd10(&Wire);
Adafruit_BMP280 bmp(&Wire);
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

float temperature = 0;
float humidity = 0;
float pressure = 0;
int lightLux = 0;
uint32_t co2Ppm = 0;
bool co2Ready = false;
unsigned long lastLoop = 0;

#if EXPERIMENTAL_WIFI_TCP_ENABLED
WiFiClient telemetryClient;
#endif
#if EXPERIMENTAL_ACTUATORS_ENABLED
CRGB leds[NUM_LEDS];
bool requestedFan = false;
bool requestedLight = false;
#endif

bool usableLocalNetworkConfig() {
#if EXPERIMENTAL_WIFI_TCP_ENABLED
  return strlen(WIFI_SSID) > 0 && strlen(WIFI_PASS) > 0
      && strlen(SERVER_HOST) > 0 && SERVER_PORT > 0;
#else
  return false;
#endif
}

void renderDisplay(bool co2Initializing) {
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(1);
  display.setCursor(0, 0);
  display.print(F("T:")); display.print(temperature, 1); display.print(F("C H:")); display.print(humidity, 0); display.println(F("%"));
  display.print(F("Lux:")); display.print(lightLux); display.print(F(" CO2:"));
  if (co2Initializing) display.println(F("--")); else display.println(co2Ppm);
  display.print(F("P:")); display.print(pressure, 1); display.println(F("hPa"));
#if EXPERIMENTAL_ACTUATORS_ENABLED
  display.println(F("Local bench output"));
#else
  display.println(F("Public default: observe only"));
#endif
  display.display();
}

#if EXPERIMENTAL_WIFI_TCP_ENABLED
void connectAndReportOnce() {
  // This opt-in teaching path sends telemetry only. It intentionally accepts no
  // no downlink commands, provides no listener, device identity, TLS, ACK, retry
  // guarantee, authorization, or remote actuator control.
  if (!usableLocalNetworkConfig() || WiFi.status() != WL_CONNECTED) return;
  if (!telemetryClient.connected() && !telemetryClient.connect(SERVER_HOST, SERVER_PORT, 1500)) return;
  char payload[180];
  snprintf(payload, sizeof(payload),
      "{\"temperature\":%.1f,\"humidity\":%.1f,\"light\":%d,\"co2\":%lu,\"pressure\":%.1f}\n",
      temperature, humidity, lightLux, static_cast<unsigned long>(co2Ppm), pressure);
  telemetryClient.print(payload);
}
#endif

void readSensors() {
  temperature = dht.readTemperature();
  humidity = dht.readHumidity();
  if (isnan(temperature)) temperature = 0;
  if (isnan(humidity)) humidity = 0;

  const float light = bh.readLightLevel();
  lightLux = light < 0 || isnan(light) ? 0 : static_cast<int>(light);

  pressure = bmp.readPressure() / 100.0F;
  if (isnan(pressure)) pressure = 0;

  co2Ready = false;
  if (acd10.preHeatDone()) {
    if (acd10.requestSensor() == 0) {
      delay(100);
      if (acd10.readSensor() == ACD10_OK) {
        co2Ppm = acd10.getCO2Concentration();
        co2Ready = true;
      }
    }
  }
}
}  // namespace

void setup() {
  Serial.begin(115200);

#if EXPERIMENTAL_ACTUATORS_ENABLED
  // Only an explicit local compile-time opt-in reaches these output paths. It
  // remains a supervised low-voltage bench experiment, not an electrical or
  // operational safety claim.
  pinMode(FAN_PIN_A, OUTPUT);
  pinMode(FAN_PIN_B, OUTPUT);
  digitalWrite(FAN_PIN_A, LOW);
  digitalWrite(FAN_PIN_B, LOW);
  FastLED.addLeds<WS2812B, WS2812B_PIN, GRB>(leds, NUM_LEDS);
  fill_solid(leds, NUM_LEDS, CRGB::Black);
  FastLED.show();
#else
  // Do not configure actuator pins as output in the public default build.
  pinMode(FAN_PIN_A, INPUT);
  pinMode(FAN_PIN_B, INPUT);
  pinMode(WS2812B_PIN, INPUT);
#endif

  Wire.begin(I2C_SDA, I2C_SCL);
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  dht.begin();
  bh.begin(BH1750::CONTINUOUS_HIGH_RES_MODE);
  bmp.begin(BMP280_ADDR);
  acd10.begin();

#if EXPERIMENTAL_WIFI_TCP_ENABLED
  if (usableLocalNetworkConfig()) {
    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASS);
  }
#endif
  renderDisplay(!acd10.preHeatDone());
}

void loop() {
  const unsigned long now = millis();
  if (now - lastLoop < LOOP_INTERVAL_MS) return;
  lastLoop = now;

  readSensors();
#if EXPERIMENTAL_ACTUATORS_ENABLED
  // The public source intentionally keeps outputs de-energized even in the
  // compile-only actuator branch. There is no automatic threshold control and
  // no remote command parser. External circuitry can still behave unexpectedly.
  digitalWrite(FAN_PIN_A, LOW);
  digitalWrite(FAN_PIN_B, LOW);
  fill_solid(leds, NUM_LEDS, CRGB::Black);
  FastLED.show();
#endif
#if EXPERIMENTAL_WIFI_TCP_ENABLED
  connectAndReportOnce();
#endif
  renderDisplay(!co2Ready);
}
