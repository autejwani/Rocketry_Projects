// telemetry/telemetry.cpp
#include "telemetry.h"
#include "../sensors/baro.h"
#include "../sensors/imu.h"
#include "../config.h"

static FlightState current_state = STATE_IDLE;

static uint8_t compute_checksum(TelemetryPacket* pkt)
{
	uint8_t* bytes = (uint8_t*)pkt + 2;
	uint8_t  chk   = 0;
	for (size_t i = 0; i < PACKET_SIZE - 3; i++) chk ^= bytes[i];
	return chk;
}

void telemetry_set_state(FlightState state)
{
	current_state = state;
}

void telemetry_send()
{
	TelemetryPacket pkt;

	pkt.header[0]    = PACKET_HEADER_0;
	pkt.header[1]    = PACKET_HEADER_1;
	pkt.timestamp_ms = millis();
	pkt.state        = current_state;

	// read into local variables first to avoid packed field reference error
	float pressure_pa, temperature_k, altitude_m;
	float ax_g, ay_g, az_g;
	float gx_dps, gy_dps, gz_dps;

	if (baro_read(pressure_pa, temperature_k, altitude_m))
	{
		pkt.pressure_pa   = pressure_pa;
		pkt.temperature_k = temperature_k;
		pkt.altitude_m    = altitude_m;
	}
	else
	{
		pkt.pressure_pa   = 0.0f;
		pkt.temperature_k = 0.0f;
		pkt.altitude_m    = 0.0f;
	}

	if (imu_read_accel(ax_g, ay_g, az_g))
	{
		pkt.ax_g = ax_g;
		pkt.ay_g = ay_g;
		pkt.az_g = az_g;
	}
	else
	{
		pkt.ax_g = 0.0f;
		pkt.ay_g = 0.0f;
		pkt.az_g = 0.0f;
	}

	if (imu_read_gyro(gx_dps, gy_dps, gz_dps))
	{
		pkt.gx_dps = gx_dps;
		pkt.gy_dps = gy_dps;
		pkt.gz_dps = gz_dps;
	}
	else
	{
		pkt.gx_dps = 0.0f;
		pkt.gy_dps = 0.0f;
		pkt.gz_dps = 0.0f;
	}

	pkt.checksum = compute_checksum(&pkt);
	Serial.write((uint8_t*)&pkt, PACKET_SIZE);
}