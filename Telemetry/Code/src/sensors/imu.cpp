// sensors/imu.cpp
#include "imu.h"
#include "../utilities/i2c.h"
#include "../config.h"

bool imu_init()
{
	uint8_t whoami = i2c_read(IMU_ADDR, IMU_WHO_REG);
	if (whoami != IMU_WHO_AM_I)
	{
		Serial.print("IMU WHO_AM_I mismatch: 0x");
		Serial.println(whoami, HEX);
		return false;
	}
	i2c_write(IMU_ADDR, IMU_CTRL1_XL, 0x48);   // accel 104Hz, 4g range
	i2c_write(IMU_ADDR, IMU_CTRL2_G,  0x4C);   // gyro 104Hz, 2000dps range
	Serial.println("IMU initialized");
	return true;
}

bool imu_read_accel(float &ax_g, float &ay_g, float &az_g)
{
	uint8_t buf[6];
	if (!i2c_read_multi(IMU_ADDR, IMU_OUTX_L_XL, buf, 6)) return false;
	ax_g = (int16_t)((buf[1] << 8) | buf[0]) * IMU_ACCEL_SCALE / 1000.0f;
	ay_g = (int16_t)((buf[3] << 8) | buf[2]) * IMU_ACCEL_SCALE / 1000.0f;
	az_g = (int16_t)((buf[5] << 8) | buf[4]) * IMU_ACCEL_SCALE / 1000.0f;
	return true;
}

bool imu_read_gyro(float &gx_dps, float &gy_dps, float &gz_dps)
{
	uint8_t buf[6];
	if (!i2c_read_multi(IMU_ADDR, IMU_OUTX_L_G, buf, 6)) return false;
	gx_dps = (int16_t)((buf[1] << 8) | buf[0]) * IMU_GYRO_SCALE / 1000.0f;
	gy_dps = (int16_t)((buf[3] << 8) | buf[2]) * IMU_GYRO_SCALE / 1000.0f;
	gz_dps = (int16_t)((buf[5] << 8) | buf[4]) * IMU_GYRO_SCALE / 1000.0f;
	return true;
}