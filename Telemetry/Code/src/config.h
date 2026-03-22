// config.h
#pragma once

// I2C pins
#define I2C_SDA_PIN PB9
#define I2C_SCL_PIN PB8
#define I2C_CLOCK_HZ 100000

// Serial
#define SERIAL_BAUD	115200

// Telemetry
#define TELEMETRY_HZ 20
#define TELEMETRY_DELAY_MS (1000 / TELEMETRY_HZ)
