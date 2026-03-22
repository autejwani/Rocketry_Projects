#include <Arduino.h>
#include "Utilities/i2c.h"
#include "Sensing/baro.h"
#include "Sensing/imu.h"
#include "Utilities/SensorFusion.h"
#include "Utilities/Song.h"
#include <Wire.h>

#define BUZZER_PIN 30

BuzzerNotes buzzer(BUZZER_PIN);
SensorData sensors;

void setup()
{
    Serial.begin(115200);
    while (!Serial) { delay(10); }

    i2c_init();
    i2c_identify_devices();

    if (!baro_init())
    {
        Serial.println("Failed to initialize barometer!");
        while (1);
    }

    if (!imu_init())
    {
        Serial.println("Failed to initialize IMU!");
        while (1);
    }

    baro_set_ground_level();
    sensor_init(sensors);

    Serial.println("Setup complete. Playing startup tune...");
    buzzer.playTune();
}

void loop()
{
    static unsigned long last_print = 0;
    unsigned long current_time = millis();

    if (current_time - last_print >= 1000)
    {
        bool success = sensor_readall(sensors);

        if (success)
        {
            Serial.println("========== SENSOR DATA ==========");
            Serial.print("Timestamp: "); Serial.print(sensors.timestamp_ms); Serial.println(" ms");

            Serial.print("Pressure: "); Serial.print(sensors.pressure, 1); Serial.println(" Pa");
            Serial.print("Temperature: "); Serial.print(sensors.temperature - 273.15, 1); Serial.println(" C");
            Serial.print("Altitude: "); Serial.print(sensors.altitude, 2); Serial.println(" m");

            Serial.print("ax: "); Serial.print(sensors.ax, 2); Serial.print("  ");
            Serial.print("ay: "); Serial.print(sensors.ay, 2); Serial.print("  ");
            Serial.print("az: "); Serial.println(sensors.az, 2);

            Serial.print("gx: "); Serial.print(sensors.gx, 3); Serial.print("  ");
            Serial.print("gy: "); Serial.print(sensors.gy, 3); Serial.print("  ");
            Serial.print("gz: "); Serial.println(sensors.gz, 3);

            Serial.print("Baro: "); Serial.print(sensors.baro_valid);
            Serial.print("  IMU: "); Serial.println(sensors.imu_valid);
            Serial.println("=================================");
        }
        else
        {
            Serial.println("ERROR: Failed to read sensors");
        }

        last_print = current_time;
    }
}