# comms/serial_worker.py
# Reads serial data from the flight computer in a background thread

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import serial
import serial.tools.list_ports
from PyQt6.QtCore import QThread, pyqtSignal
from data_parser import find_packet


def list_ports():
    # returns a list of all available serial ports on the computer
    return [port.device for port in serial.tools.list_ports.comports()]


class SerialWorker(QThread):
    packet_received  = pyqtSignal(dict)
    connection_error = pyqtSignal(str)

    def __init__(self, port, baud_rate):
        super().__init__()
        self.port      = port
        self.baud_rate = baud_rate
        self.running   = False

    def run(self):
        self.running = True
        buffer = b''

        try:
            ser = serial.Serial(self.port, self.baud_rate, timeout=1)
        except serial.SerialException as e:
            self.connection_error.emit(str(e))
            return

        while self.running:
            try:
                if ser.in_waiting > 0:
                    buffer += ser.read(ser.in_waiting)
                    packet, buffer = find_packet(buffer)
                    while packet:
                        self.packet_received.emit(packet)
                        packet, buffer = find_packet(buffer)
            except serial.SerialException as e:
                self.connection_error.emit(str(e))
                break

        ser.close()

    def stop(self):
        self.running = False
        self.wait()


if __name__ == '__main__':
    ports = list_ports()
    print(f"Available ports: {ports}")

    if not ports:
        print("No ports found — connect the flight computer and try again")
        sys.exit(1)

    # use ttyACM0 directly — this is always the STM32 on Linux
    port = '/dev/ttyACM0'
    print(f"Connecting to {port} at 115200 baud...")

    buffer = b''
    try:
        ser = serial.Serial(port, 115200, timeout=1)
        print("Connected — receiving packets (Ctrl+C to stop)\n")

        while True:
            if ser.in_waiting > 0:
                buffer += ser.read(ser.in_waiting)
                packet, buffer = find_packet(buffer)
                while packet:
                    print(f"  [{packet['timestamp_ms']:>8} ms]"
                          f"  Alt: {packet['altitude_m']:>7.2f} m"
                          f"  Az:  {packet['az_g']:>6.3f} g"
                          f"  State: {packet['state']}")
                    packet, buffer = find_packet(buffer)

    except KeyboardInterrupt:
        print("\nStopped")
    except serial.SerialException as e:
        print(f"Serial error: {e}")