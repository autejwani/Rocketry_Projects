// sensors/baro.cpp
#include "baro.h"
#include "../utilities/i2c.h"
#include "../config.h"
#include <math.h>

static float ground_pressure_pa = 101325.0f;

bool baro_init()
{
	uint8_t whoami = i2c_read(BARO_ADDR, BARO_WHO_REG);
	if (whoami != BARO_WHO_AM_I)
	{
		Serial.print("Barometer WHO_AM_I mismatch: 0x");
		Serial.println(whoami, HEX);
		return false;
	}
	i2c_write(BARO_ADDR, CTRL_REG1, 0x10);
	Serial.println("Barometer initialized");
	return true;
}

void baro_set_ground_level()
{
	delay(2000);
	float sum = 0;
	int   valid = 0;

	Serial.println("Calibrating ground pressure...");

	for (int i = 0; i < 10; i++)
	{
		uint8_t buf[5];
		if (i2c_read_multi(BARO_ADDR, PRESS_OUT_XL, buf, 5))
		{
			int32_t raw = (int32_t)buf[2] << 16 | (int32_t)buf[1] << 8 | buf[0];
			sum += (raw / PRESS_SCALE) * 100.0f;
			valid++;
		}
		delay(100);
	}

	if (valid > 0)
	{
		ground_pressure_pa = sum / valid;
		Serial.print("Ground pressure: ");
		Serial.print(ground_pressure_pa, 1);
		Serial.println(" Pa");
	}
	else
	{
		Serial.println("Warning: ground calibration failed");
	}
}

bool baro_read(float &pressure_pa, float &temperature_k, float &altitude_m)
{
	uint8_t buf[5];
	if (!i2c_read_multi(BARO_ADDR, PRESS_OUT_XL, buf, 5)) return false;

	int32_t press_raw = (int32_t)buf[2] << 16 | (int32_t)buf[1] << 8 | buf[0];
	pressure_pa = (press_raw / PRESS_SCALE) * 100.0f;

	int16_t temp_raw = (int16_t)(buf[4] << 8 | buf[3]);
	temperature_k = (temp_raw / TEMP_SCALE) + 273.15f;

	altitude_m = 44330.0f * (1.0f - powf(pressure_pa / ground_pressure_pa, 0.1903f));

	return true;
}