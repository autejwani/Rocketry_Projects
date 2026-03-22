# Flight Computer

The first iteration flight computer built for development and testing of the telemetry protocol and ground station application. Built around the Teensy 4.1 development board and tested with STM32F411RE Nucleo development board.

---

## Development Checkpoints

| Checkpoint | Status |
|---|---|
| I2C driver | Complete |
| Barometer driver — LPS22HB | Complete |
| IMU driver — LSM6DSO | Complete |
| Telemetry packet transmission | Complete |
| Ground station validation | Complete |
| Flight ready packaging | Not Started |

---

## Purpose

This board was used to develop and validate the telemetry protocol, sensor libraries, and ground station application before designing the TALON-1 custom PCB. All firmware written for this board laid the foundation for the TALON-1 firmware.

---

## Hardware

| Item | Detail |
|---|---|
| Microcontroller | STM32F411RE Nucleo |
| IMU | LSM6DSO — accelerometer and gyroscope |
| Barometer | LPS22HB — pressure and temperature |
| Interface | I2C |
| SDA Pin | PB9 (Arduino pin 18) |
| SCL Pin | PB8 (Arduino pin 19) |
| Baud Rate | 115200 |

---

## Firmware Structure
```
Code/
├── platformio.ini
└── src/
    ├── config.h                  pin and timing definitions
    ├── main.cpp                  setup and loop
    ├── sensors/
    │   ├── baro.h / baro.cpp     LPS22HB barometer driver
    │   └── imu.h  / imu.cpp      LSM6DSO IMU driver
    ├── utilities/
    │   └── i2c.h  / i2c.cpp      I2C bus driver
    └── telemetry/
        ├── telemetry.h           packet struct and state enum
        └── telemetry.cpp         packet assembly and transmission
```

---

## Sensor I2C Addresses

| Sensor | Address |
|---|---|
| LSM6DSO IMU | 0x6A |
| LPS22HB Barometer | 0x5C |

---

## Building and Flashing

Install PlatformIO then run from inside the `Code/` folder:
```bash
pio run --target upload
pio device monitor --baud 115200
```

