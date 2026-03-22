# Telemetry Protocol

This folder contains the C++ firmware implementing the TALON-1 telemetry protocol. The protocol defines a fixed binary packet format transmitted over UART that is shared across all Kestrel Avionics flight computers. Any flight computer that implements this protocol is immediately compatible with the ground station application without modification.

---

## Development Checkpoints

| Checkpoint | Status |
|---|---|
| Define packet structure | Complete |
| Implement sensor reads | Complete |
| Implement checksum | Complete |
| Validate packet size matches Python parser | Complete |
| Test on STM32F411RE | Complete |
| Port to STM32H503KBU6 (TALON-1) | Not Started |

---

## Packet Format

Every packet is 44 bytes transmitted little endian over UART at 115200 baud at 20 Hz.

| Byte(s) | Field | Type | Units |
|---|---|---|---|
| 0–1 | Header | uint8[2] | Always 0x07 0x32 |
| 2–5 | Timestamp | uint32 | Milliseconds since boot |
| 6–9 | Pressure | float32 | Pascals |
| 10–13 | Temperature | float32 | Kelvin |
| 14–17 | Altitude | float32 | Metres above ground |
| 18–21 | Accel X | float32 | g |
| 22–25 | Accel Y | float32 | g |
| 26–29 | Accel Z | float32 | g |
| 30–33 | Gyro X | float32 | Degrees per second |
| 34–37 | Gyro Y | float32 | Degrees per second |
| 38–41 | Gyro Z | float32 | Degrees per second |
| 42 | Flight State | uint8 | See state table below |
| 43 | Checksum | uint8 | XOR of bytes 2 through 42 |

Total packet size: **44 bytes**

---

## Header Bytes

Every packet begins with `0x07 0x32`. The receiver scans the incoming byte stream for this sequence to find the start of each packet. If the header is not found or the checksum fails the packet is discarded.

---

## Checksum

The checksum is computed by XORing every byte between the header and the checksum field:
```cpp
uint8_t chk = 0;
for (size_t i = 0; i < PACKET_SIZE - 3; i++) chk ^= bytes[i];
```

The Python parser verifies this on every received packet and discards any packet where the checksum does not match.

---

## Flight States

| Value | State | Description |
|---|---|---|
| 0 | IDLE | Waiting on pad |
| 1 | ARMED | Pyros armed, ready for launch |
| 2 | ASCENT | Motor burning |
| 3 | COAST | Motor burnout, still climbing |
| 4 | APOGEE | Peak altitude, drogue fires here |
| 5 | DESCENT | Falling under drogue |
| 6 | MAIN | Main chute deployed |
| 7 | LANDED | On the ground |

---

## Firmware Structure
```
Code/
├── platformio.ini
└── src/
    ├── config.h                  central pin and timing definitions
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

## Hardware Used for Development

| Item | Detail |
|---|---|
| Microcontroller | STM32F411RE Nucleo |
| IMU | LSM6DSO |
| Barometer | LPS22HB |
| Baud rate | 115200 |
| Interface | USB Serial (UART) |


---

## Compatibility

The protocol is transport independent. The same packet format works over USB serial today and will work over LoRa radio in future revisions. The ground station parser does not need to change when the transport changes — only the physical connection differs.

| Transport | Status |
|---|---|
| USB Serial (UART) | Complete |
| LoRa (RA-01H, 915 MHz) | Planned |

---
