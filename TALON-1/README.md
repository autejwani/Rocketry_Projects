# TALON-1 Modular Flight Computer System

TALON-1 is a modular three-board avionics stack designed for high-powered rocketry applications across all certification levels under Tripoli Rocketry Association and National Association of Rocketry guidelines. The system operates in the 915 MHz ISM band for long range telemetry.

---

## Development Checkpoints

| Checkpoint | TALON-1A | TALON-1B | TALON-1C |
|---|---|---|---|
| Component Selection | Complete | Complete | Complete |
| Schematic Design | Complete | Complete | Complete |
| PCB Layout | Complete | Complete | Complete |
| PCB Fabrication | Not Started | Not Started | Not Started |
| Assembly | Not Started | Not Started | Not Started |
| Bring-up Testing | Not Started | Not Started | Not Started |
| Sensor Validation | Not Started | Not Started | Not Started |
| System Integration | Not Started | Not Started | Not Started |
| Flight Testing | Not Started | Not Started | Not Started |

---

## System Overview

The TALON-1 is a three-board modular avionics stack built on a circular PCB form factor. The three modules are designated TALON-1A (Core Processing), TALON-1B (Sensing), and TALON-1C (RF and Navigation), stacked bottom to top and connected via 2.54mm pitch pin headers.

---

## Assembled Stack

*Photo of fully assembled TALON-1 stack (all three boards) to be added here.*

*CAD render of assembled stack to be added here.*

---

## Board Overview

### TALON-1A — Core Processing Module
*PCB image to be added here.*

The base board of the stack. Hosts the STM32H503KBU6 microcontroller running at up to 250 MHz on an ARM Cortex-M33 core, the AP63203WU-7 3.3V 2A buck converter, and the TB6612FNG dual H-bridge motor driver for airbrake control. All inter-board signals originate from this board via male 2.54mm pin headers.

| Item | Detail |
|---|---|
| Microcontroller | STM32H503KBU6 |
| Core | ARM Cortex-M33 @ 250 MHz |
| Flash | 128 KB |
| SRAM | 32 KB |
| Package | UFQFPN-32 |
| Power Regulator | AP63203WU-7 — 3.3V 2A |
| Motor Driver | TB6612FNG — Dual H-Bridge |
| Input Voltage | 3S LiPo (11.1V nominal, 12.6V max) |

---

### TALON-1B — Sensing Module
*PCB image to be added here.*

The middle board of the stack. Carries three ST MEMS sensors on a shared I2C bus. Receives signals from TALON-1A below and passes all signals through to TALON-1C above.

| Sensor | Part | Function | Interface | Address |
|---|---|---|---|---|
| IMU | LSM6DSVTR | 3-axis Accel + 3-axis Gyro | I2C | 0x6A or 0x6B |
| Barometer | LPS27HHWTR | Pressure + Temperature | I2C | 0x5C or 0x5D |
| Magnetometer | IIS2MDCTR | 3-axis Magnetic Field | I2C | 0x1E (fixed) |

I2C pull-up resistors (4.7kΩ) are placed on this board only. No additional pull-ups on TALON-1A or TALON-1C to avoid bus loading.

---

### TALON-1C — RF and Navigation Module
*PCB image to be added here.*

The topmost board of the stack. Hosts the RA-01H 915 MHz LoRa transceiver and the u-blox MAX-M10M GNSS receiver. Being at the top of the stack positions this board closest to any externally mounted antenna, minimising RF feedline losses.

| Device | Part | Function | Interface | Address / Notes |
|---|---|---|---|---|
| LoRa Radio | RA-01H | 915 MHz Telemetry | SPI | CS, DIO1, RESET |
| GNSS | MAX-M10M-00B | GPS, GLONASS, Galileo, BeiDou | I2C | 0x42 (fixed) |

The RA-01H uses a quarter-wave whip antenna at 915 MHz with a wire length of approximately 81.9 mm. The MAX-M10M connects to a separate GNSS antenna via SMA connector.

---

## Inter-Board Bus Pinout

| Signal | Type | Destination |
|---|---|---|
| 3V3 | Power | All boards |
| GND | Power | All boards |
| SDA | I2C Data | TALON-1B sensors, TALON-1C GPS |
| SCL | I2C Clock | TALON-1B sensors, TALON-1C GPS |
| MOSI | SPI Data | TALON-1C RA-01H |
| MISO | SPI Data | TALON-1C RA-01H |
| SCK | SPI Clock | TALON-1C RA-01H |
| CS | SPI Chip Select | TALON-1C RA-01H |
| DIO1 | Digital Input | TALON-1C RA-01H interrupt |
| RESET | Digital Output | TALON-1C RA-01H reset |

---

## Power Architecture

The entire stack is powered by a single 3S LiPo battery (11.1V nominal, 12.6V fully charged). The AP63203WU-7 buck converter on TALON-1A regulates this down to 3.3V for all digital logic and sensors across the stack. Raw battery voltage is fed directly to the TB6612FNG motor driver for airbrake motor control.

---

## Firmware

Firmware targets the STM32H503KBU6 using the STM32 HAL library via PlatformIO. Development is ongoing and will cover sensor acquisition, flight state machine logic, telemetry transmission over LoRa, and GNSS data parsing. See the `Code/` folder for current firmware.

---

## Repository Structure
```
TALON-1/
│
├── PCB Design/
│   ├── Base Layer/        TALON-1A KiCad files
│   ├── Sensor Layer/      TALON-1B KiCad files
│   └── Comms Layer/       TALON-1C KiCad files
│
├── CAD/                   mechanical CAD files
├── Code/                  PlatformIO firmware project
│
└── Docs/
    ├── architecture.md
    ├── packet_protocol.md
    └── board_pinout.md
```

---

## Design Philosophy

TALON-1 was designed with an emphasis on modularity, repairability, and iterative development. Separating processing, sensing, and RF functions into discrete modules means a change to one layer does not require a redesign of the others. Each board can be developed, tested, and replaced independently.
