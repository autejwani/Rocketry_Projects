// utilities/i2c.cpp
#include "i2c.h"
#include "../config.h"
#include <Wire.h>

bool i2c_init()
{
	Wire.setSDA(I2C_SDA_PIN);
	Wire.setSCL(I2C_SCL_PIN);
	Wire.begin();
	Wire.setClock(I2C_CLOCK_HZ);
	Serial.begin(SERIAL_BAUD);
	while (!Serial) {}
	return true;
}

uint8_t i2c_read(uint8_t addr, uint8_t reg)
{
	Wire.beginTransmission(addr);
	Wire.write(reg);
	if (Wire.endTransmission(false) != 0) return 0xFF;
	Wire.requestFrom(addr, (uint8_t)1);
	if (Wire.available()) return Wire.read();
	return 0xFF;
}

bool i2c_write(uint8_t addr, uint8_t reg, uint8_t val)
{
	Wire.beginTransmission(addr);
	Wire.write(reg);
	Wire.write(val);
	return (Wire.endTransmission() == 0);
}

bool i2c_read_multi(uint8_t addr, uint8_t reg, uint8_t* buf, uint8_t len)
{
	Wire.beginTransmission(addr);
	Wire.write(reg);
	if (Wire.endTransmission(false) != 0) return false;
	Wire.requestFrom(addr, len);
	if (Wire.available() < len) return false;
	for (uint8_t i = 0; i < len; i++) buf[i] = Wire.read();
	return true;
}

void i2c_identify_devices()
{
	const uint8_t WHO_AM_I_REG = 0x0F;
	const uint8_t IMU_WHOAMI   = 0x6C;
	const uint8_t BARO_WHOAMI  = 0xB1;

	bool imu_found  = false;
	bool baro_found = false;

	for (uint8_t addr = 1; addr < 127; addr++)
	{
		Wire.beginTransmission(addr);
		if (Wire.endTransmission() != 0) continue;
		uint8_t whoami = i2c_read(addr, WHO_AM_I_REG);
		if (whoami == IMU_WHOAMI)  imu_found  = true;
		if (whoami == BARO_WHOAMI) baro_found = true;
	}

	Serial.print("IMU (LSM6DSO) ... ");
	Serial.println(imu_found  ? "FOUND" : "NOT FOUND");
	Serial.print("Barometer (LPS22HB) ... ");
	Serial.println(baro_found ? "FOUND" : "NOT FOUND");
}
