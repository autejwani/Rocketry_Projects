// main.cpp
#include <Arduino.h>
#include "config.h"
#include "utilities/i2c.h"
#include "sensors/baro.h"
#include "sensors/imu.h"
#include "telemetry/telemetry.h"

static uint32_t last_send_ms = 0;

void setup()
{
    i2c_init();
    Serial.print("Packet size: ");
    Serial.println(sizeof(TelemetryPacket));

    Serial.println("=== FC Telemetry ===");

    // scan and identify sensors
    i2c_identify_devices();

    // init sensors and report result
    if (!baro_init())   Serial.println("ERROR: Barometer failed to init");
    if (!imu_init())    Serial.println("ERROR: IMU failed to init");

    // calibrate ground pressure before flight
    baro_set_ground_level();

    Serial.println("Setup complete — sending telemetry");
    Serial.println("-----------------------------------");
}

void loop()
{
    if (millis() - last_send_ms >= TELEMETRY_DELAY_MS)
    {
        last_send_ms = millis();

        // read all sensors
        float pressure_pa, temperature_k, altitude_m;
        float ax_g, ay_g, az_g;
        float gx_dps, gy_dps, gz_dps;

        bool baro_ok = baro_read(pressure_pa, temperature_k, altitude_m);
        bool accel_ok = imu_read_accel(ax_g, ay_g, az_g);
        bool gyro_ok  = imu_read_gyro(gx_dps, gy_dps, gz_dps);

        // print human readable data to serial monitor for verification
        Serial.println("--- Telemetry Packet ---");

        if (baro_ok)
        {
            Serial.print("Pressure    : "); Serial.print(pressure_pa, 1);    Serial.println(" Pa");
            Serial.print("Temperature : "); Serial.print(temperature_k - 273.15f, 2); Serial.println(" C");
            Serial.print("Altitude    : "); Serial.print(altitude_m, 2);     Serial.println(" m");
        }
        else Serial.println("Barometer   : READ FAILED");

        if (accel_ok)
        {
            Serial.print("Accel X     : "); Serial.print(ax_g, 4); Serial.println(" g");
            Serial.print("Accel Y     : "); Serial.print(ay_g, 4); Serial.println(" g");
            Serial.print("Accel Z     : "); Serial.print(az_g, 4); Serial.println(" g");
        }
        else Serial.println("Accelerometer : READ FAILED");

        if (gyro_ok)
        {
            Serial.print("Gyro X      : "); Serial.print(gx_dps, 4); Serial.println(" dps");
            Serial.print("Gyro Y      : "); Serial.print(gy_dps, 4); Serial.println(" dps");
            Serial.print("Gyro Z      : "); Serial.print(gz_dps, 4); Serial.println(" dps");
        }
        else Serial.println("Gyroscope   : READ FAILED");

        Serial.println("------------------------");

        // send binary telemetry packet
        telemetry_send();
    }
}