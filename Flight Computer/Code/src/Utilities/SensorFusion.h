#pragma once
#include <Arduino.h>

struct SensorData
{
	unsigned long timestamp_ms;

	float pressure;
	float temperature;
	float altitude;

	float ax;
	float ay;
	float az;

	float gx;
	float gy;
	float gz;

	bool baro_valid;
	bool imu_valid;
};

void sensor_init(SensorData &data);
bool sensor_readall(SensorData &data);