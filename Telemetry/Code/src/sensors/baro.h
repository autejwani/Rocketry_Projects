// sensors/baro.h
#pragma once
#include <Arduino.h>

// LPS22HB register addresses
#define BARO_ADDR       0x5C
#define BARO_WHO_REG    0x0F
#define BARO_WHO_AM_I   0xB1
#define CTRL_REG1       0x10
#define PRESS_OUT_XL    0x28

// Conversion constants
#define PRESS_SCALE     4096.0f
#define TEMP_SCALE      100.0f

bool baro_init();
void baro_set_ground_level();
bool baro_read(float &pressure_pa, float &temperature_k, float &altitude_m);