#pragma once

// Local configuration is optional and ignored by Git. Load it before applying
// public defaults so a supervised local teaching bench can explicitly opt in
// without macro-redefinition warnings.
#if __has_include("config.local.h")
#include "config.local.h"
#endif

// Public defaults keep network and actuator paths disabled.
#ifndef ENABLE_EXPERIMENTAL_WIFI_TCP
#define ENABLE_EXPERIMENTAL_WIFI_TCP 0
#endif

#ifndef ENABLE_EXPERIMENTAL_ACTUATORS
#define ENABLE_EXPERIMENTAL_ACTUATORS 0
#endif

// Exact value 1 is required. Other nonzero values stay disabled.
#if ENABLE_EXPERIMENTAL_WIFI_TCP == 1
#define EXPERIMENTAL_WIFI_TCP_ENABLED 1
#else
#define EXPERIMENTAL_WIFI_TCP_ENABLED 0
#endif

#if ENABLE_EXPERIMENTAL_ACTUATORS == 1
#define EXPERIMENTAL_ACTUATORS_ENABLED 1
#else
#define EXPERIMENTAL_ACTUATORS_ENABLED 0
#endif

#ifndef WIFI_SSID
#define WIFI_SSID ""
#endif
#ifndef WIFI_PASS
#define WIFI_PASS ""
#endif
#ifndef SERVER_HOST
#define SERVER_HOST ""
#endif
#ifndef SERVER_PORT
#define SERVER_PORT 0
#endif
