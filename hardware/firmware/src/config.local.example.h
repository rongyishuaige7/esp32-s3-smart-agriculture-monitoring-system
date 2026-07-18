#pragma once

// Copy this file to config.local.h only for a supervised, isolated low-voltage
// teaching bench. Never commit it, publish it, paste it in issues, or include it
// in screenshots/logs. The public build keeps both switches at 0.
#define ENABLE_EXPERIMENTAL_WIFI_TCP 0
#define ENABLE_EXPERIMENTAL_ACTUATORS 0

// Fill only after you understand the network and electrical boundaries.
#define WIFI_SSID "YOUR_WIFI_SSID"
#define WIFI_PASS "YOUR_WIFI_PASSWORD"
#define SERVER_HOST "YOUR_TRUSTED_LOCAL_SERVER"
#define SERVER_PORT 0
