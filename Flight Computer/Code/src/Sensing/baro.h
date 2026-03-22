// baro.h
#pragma once
#include <Arduino.h>
#include "Utilities/i2c.h"

// LPS22HB I2C address and identification
#define BARO_ADDR       0x5C
#define BARO_WHO_AM_I   0xB1
#define BARO_WHO_REG    0x0F

// Register addresses
#define PRESS_OUT_XL    0x28
#define CTRL_REG1       0x10

// Sensor scale factors
#define PRESS_SCALE            4096.0f    // LSB per hPa
#define TEMP_SCALE             100.0f     // LSB per °C

// Initialize barometer
bool baro_init();

// Set ground reference pressure (call this at launch/startup)
void baro_set_ground_level();

// Read barometer data for EKF
// Returns:
//   pressure_pa: Absolute pressure in Pascals
//   temperature_k: Temperature in Kelvin
//   altitude_m: Altitude in meters relative to ground level
bool baro_read(float &pressure_pa, float &temperature_k, float &altitude_m);
