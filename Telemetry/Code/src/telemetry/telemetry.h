// telemetry/telemetry.h
#pragma once
#include <Arduino.h>

#define PACKET_HEADER_0  0x07
#define PACKET_HEADER_1  0x32

typedef enum {
	STATE_IDLE       = 0,    // waiting on pad
	STATE_ARMED      = 1,    // pyros armed, ready for launch
	STATE_ASCENT     = 2,    // motor burning
	STATE_COAST      = 3,    // motor burnout, still climbing
	STATE_APOGEE     = 4,    // peak altitude, drogue fires here
	STATE_DESCENT    = 5,    // falling under drogue
	STATE_MAIN       = 6,    // main chute deployed
	STATE_LANDED     = 7     // on the ground
} FlightState;

typedef struct __attribute__((packed)) {
	uint8_t     header[2];
	uint32_t    timestamp_ms;
	float       pressure_pa;
	float       temperature_k;
	float       altitude_m;
	float       ax_g;
	float       ay_g;
	float       az_g;
	float       gx_dps;
	float       gy_dps;
	float       gz_dps;
	FlightState state;
	uint8_t     checksum;
} TelemetryPacket;

#define PACKET_SIZE sizeof(TelemetryPacket)

void telemetry_set_state(FlightState state);
void telemetry_send();