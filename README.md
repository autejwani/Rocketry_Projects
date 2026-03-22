# Rocketry Projects

A collection of my model rocketry projects including flight computer hardware, firmware, ground station software, and certification flight documentation.

---

## Projects

| Project | Status | Current Checkpoint | Description |
|---|---|---|---|
| TALON-1 | In Progress | TBD | Modular 3-board flight computer system |
| Ground Station | In Progress | TBD | Python telemetry ground station application |
| Flight Computer | Complete | TBD | First iteration flight computer |
| Telemetry | Complete | TBD | C++ telemetry protocol for STM32 |
| LoRa Test | Planned | TBD | LoRa radio range and reliability testing |
| L1 | Complete | Certified | H100 motor, certified March 8th |
| L2 | Planned | TBD | Level 2 certification flight |
| L3 | Planned | TBD | Level 3 certification flight |

---

## TALON-1 System Overview

TALON-1 is a modular flight computer built around a 3-board stacking architecture connected via GPIO headers. Each board serves a dedicated purpose and can be developed and tested independently.

**Base Layer**
- STM32H503KBU6 microcontroller
- Power regulation for entire stack
- Distributes power and signals to upper boards via stacking headers

**Sensor Layer**
- IMU: LSM6DSVTR — accelerometer and gyroscope
- Barometer: LPS27HHWTR — pressure and temperature
- Magnetometer: IIS2MDCTR

**Communications Layer**
- GPS: MAX-M10M-00B
- LoRa: RA-01H — long range telemetry

---

## Flight Computer (First Iteration)

The original flight computer used for development and testing. Built around the Teensy4.1 development board and tested with STM32F411RE Nucleo development board.

**Sensors**
- IMU: LSM6DSO — accelerometer and gyroscope
- Barometer: LPS22HB — pressure and temperature

This board was used to develop and validate the telemetry protocol, sensor libraries, and ground station application before designing the TALON-1 custom PCB.

---

## Ground Station

A desktop application written in Python that receives and displays live telemetry from any flight computer that implements the TALON-1 packet protocol.

**Features**
- Serial port and baud rate selection
- Live barometer readout — pressure, temperature, altitude
- Live accelerometer and gyroscope readouts
- Flight state display with progress indicator across all flight phases
- 3D rocket orientation visualization driven by live gyroscope data
- Compatible with any future flight computer that implements the telemetry protocol

---

## Telemetry Protocol

All flight computers in this repository share a common binary packet format transmitted over UART at 115200 baud. The protocol is transport independent — the same packet format works over USB serial today and will work over LoRa radio in future revisions.

**Key specifications**
- Header bytes: 0x07 0x32
- Packet size: 44 bytes
- Byte order: little endian
- Checksum: XOR of all bytes between header and checksum field
- Data rate: 20 Hz

Any flight computer that implements this protocol is immediately compatible with the ground station without any changes to the application. See `Telemetry/README.md` for the full packet specification.

---

## Flight Certifications

| Level | Date | Motor | Status |
|---|---|---|---|
| L1 | March 8, 2025 | H100 | Complete |
| L2 | TBD | J, K, or L class | Planned |
| L3 | TBD | M class or higher | Planned |

---

## Repository Structure
```
Rocketry_Projects/
│
├── TALON-1/              modular flight computer hardware and firmware
├── Ground Station/       Python telemetry ground station application
├── Flight Computer/      first iteration flight computer
├── Telemetry/            shared C++ telemetry protocol
├── LoRa_Test/            LoRa radio testing
├── L1/                   level 1 certification flight
├── L2/                   level 2 certification flight
└── L3/                   level 3 certification flight
```
