# data_parser.py
# Parses binary telemetry packets from the flight computer

import struct

PACKET_FORMAT = '<2BI9f2B'
PACKET_SIZE   = struct.calcsize(PACKET_FORMAT)
HEADER        = bytes([0x07, 0x32])

FLIGHT_STATES = {0: 'IDLE', 1: 'ARMED', 2: 'ASCENT', 3: 'COAST', 4: 'APOGEE', 5: 'DESCENT', 6: 'MAIN', 7: 'LANDED'}

def compute_checksum(raw_bytes):
    chk = 0
    for b in raw_bytes[2:-1]: chk ^= b
    return chk

def parse_packet(raw_bytes):
    if len(raw_bytes) != PACKET_SIZE:
        return None
    if raw_bytes[0:2] != HEADER:
        return None
    if compute_checksum(raw_bytes) != raw_bytes[-1]:
        return None
    fields = struct.unpack(PACKET_FORMAT, raw_bytes)
    return {
        'timestamp_ms':  fields[2],
        'pressure_pa':   fields[3],
        'temperature_k': fields[4],
        'altitude_m':    fields[5],
        'ax_g':          fields[6],
        'ay_g':          fields[7],
        'az_g':          fields[8],
        'gx_dps':        fields[9],
        'gy_dps':        fields[10],
        'gz_dps':        fields[11],
        'state':         FLIGHT_STATES.get(fields[12], 'UNKNOWN'),
    }

def find_packet(buffer):
    while len(buffer) >= PACKET_SIZE:
        idx = buffer.find(HEADER)
        if idx == -1:                    return None, b''
        if idx > 0:                      buffer = buffer[idx:]
        if len(buffer) < PACKET_SIZE:   break
        packet = parse_packet(buffer[:PACKET_SIZE])
        if packet:                       return packet, buffer[PACKET_SIZE:]
        buffer = buffer[1:]
    return None, buffer


if __name__ == '__main__':

    def make_test_packet():
        header = bytes([0x07, 0x32])
        body   = struct.pack('<I9fB', 1000, 101325.0, 298.15, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0)
        chk    = 0
        for b in body: chk ^= b
        return header + body + bytes([chk])

    test_packet = make_test_packet()

    print(f"Packet size      : {len(test_packet)} bytes")
    print(f"Expected size    : {PACKET_SIZE} bytes")
    print(f"Header correct   : {test_packet[0:2] == HEADER}")

    result = parse_packet(test_packet)
    if result:
        print("\nParsed packet:")
        for key, value in result.items(): print(f"  {key:<16} : {value}")
    else:
        print("Parse failed - check struct format")

    packet, remaining = find_packet(bytes([0xFF, 0xAA, 0x00, 0x11]) + test_packet)
    print(f"\nfind_packet test : {'PASSED' if packet else 'FAILED'}")
    print(f"Remaining buffer : {len(remaining)} bytes (should be 0)")