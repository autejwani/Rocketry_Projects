// baro.cpp
#include "baro.h"
#include <Wire.h>
#include <math.h>

static float ground_pressure_pa = 101325.0f; // Default sea level, updated by calibration

bool baro_init()
{
    Wire.setSDA(18);//PB9, 18
    Wire.setSCL(19);//PB8, 19
    Wire.begin();

    uint8_t whoami = i2c_read(BARO_ADDR, BARO_WHO_REG);
    if (whoami != BARO_WHO_AM_I)
    {
       Serial.print("Barometer WHO_AM_I mismatch: 0x");
       Serial.println(whoami, HEX);
       return false;
    }

    // CTRL_REG1: active, 1 Hz ODR
    i2c_write(BARO_ADDR, CTRL_REG1, 0x10);

    Serial.println("Barometer initialized successfully");
    return true;
}

void baro_set_ground_level()
{
    // Take multiple readings and average for better accuracy
    float pressure_sum = 0;
    int valid_readings = 0;

    Serial.println("Calibrating ground level...");

    for (int i = 0; i < 10; i++)
    {
        uint8_t buf[5];
        if (i2c_read_multi(BARO_ADDR, PRESS_OUT_XL, buf, 5))
        {
            int32_t press_raw = (int32_t)buf[2] << 16 | (int32_t)buf[1] << 8 | buf[0];
            float pressure_hpa = press_raw / PRESS_SCALE;
            pressure_sum += pressure_hpa * 100.0f; // Convert to Pa
            valid_readings++;
        }
        delay(100); // Wait between readings
    }

    if (valid_readings > 0)
    {
        ground_pressure_pa = pressure_sum / valid_readings;
        Serial.print("Ground pressure set to: ");
        Serial.print(ground_pressure_pa, 1);
        Serial.println(" Pa");
    }
    else
    {
        Serial.println("Warning: Failed to calibrate ground level!");
    }
}

bool baro_read(float &pressure_pa, float &temperature_k, float &altitude_m)
{
    uint8_t buf[5];
    if (!i2c_read_multi(BARO_ADDR, PRESS_OUT_XL, buf, 5))
       return false;

    // Pressure: 24-bit raw value
    int32_t press_raw = (int32_t)buf[2] << 16 | (int32_t)buf[1] << 8 | buf[0];
    float pressure_hpa = press_raw / PRESS_SCALE;
    pressure_pa = pressure_hpa * 100.0f;  // Convert hPa to Pa

    // Temperature: 16-bit raw value
    int16_t temp_raw = (int16_t)(buf[4] << 8 | buf[3]);
    float temperature_c = temp_raw / TEMP_SCALE;
    temperature_k = temperature_c + 273.15f;  // Convert °C to Kelvin

    // Altitude relative to ground level using barometric formula
    altitude_m = 44330.0f * (1.0f - powf(pressure_pa / ground_pressure_pa, 0.1903f));

    return true;
}