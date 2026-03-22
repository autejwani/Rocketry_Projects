//
// Created by aditya on 1/30/26.
//
#include "SensorFusion.h"

#include "Sensing/baro.h"
#include "Sensing/imu.h"
#include <math.h>
#define G_TO_MS2 9.8f

void sensor_init(SensorData &data)
{
	data.timestamp_ms = 0;
	data.pressure = 0.0f;
	data.temperature = 0.0f;
	data.altitude = 0.0f;

	data.ax = 0.0f;
	data.ay = 0.0f;
	data.az = 0.0f;

	data.baro_valid = false;
	data.imu_valid = false;
}

bool sensor_readall(SensorData &data)
{
	data.timestamp_ms = millis();

	data.baro_valid = baro_read(data.pressure, data.temperature, data.altitude);
	float ax, ay, az; //In gs
	bool accel_ok = imu_read_accel(ax, ay, az);

	if (accel_ok)
	{
		data.ax = ax * G_TO_MS2;
		data.ay = ay * G_TO_MS2;
		data.az = az * G_TO_MS2;
	}

	float gx, gy, gz; //degrees per sec
	bool gyro_ok = imu_read_gyro(gx, gy, gz);

	if (gyro_ok)
	{
		data.gx = gx;
		data.gy = gy;
		data.gz = gz;
	}

	data.imu_valid = accel_ok && gyro_ok;
	return data.baro_valid && data.imu_valid;

}