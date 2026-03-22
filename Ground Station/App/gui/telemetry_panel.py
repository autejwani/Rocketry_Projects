# gui/telemetry_panel.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class TelemetryPanel(QWidget):

    def __init__(self):
        super().__init__()
        self._build_ui()

    def _build_ui(self):
        layout = QHBoxLayout(self)
        layout.setSpacing(10)

        # barometer group
        self.baro_group  = QGroupBox('Barometer')
        self.baro_group.setStyleSheet('QGroupBox { color: white; }')
        baro_layout = QVBoxLayout(self.baro_group)

        self.unit_pressure = QLabel('Pressure (Pa)')
        self.unit_pressure.setStyleSheet('color: #888888; font-size: 11px;')
        self.unit_pressure.setAlignment(Qt.AlignmentFlag.AlignCenter)
        baro_layout.addWidget(self.unit_pressure)
        self.label_pressure = QLabel('---')
        self.label_pressure.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        self.label_pressure.setStyleSheet('color: #00aaff;')
        self.label_pressure.setAlignment(Qt.AlignmentFlag.AlignCenter)
        baro_layout.addWidget(self.label_pressure)

        self.unit_temperature = QLabel('Temperature (°C)')
        self.unit_temperature.setStyleSheet('color: #888888; font-size: 11px;')
        self.unit_temperature.setAlignment(Qt.AlignmentFlag.AlignCenter)
        baro_layout.addWidget(self.unit_temperature)
        self.label_temperature = QLabel('---')
        self.label_temperature.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        self.label_temperature.setStyleSheet('color: #00aaff;')
        self.label_temperature.setAlignment(Qt.AlignmentFlag.AlignCenter)
        baro_layout.addWidget(self.label_temperature)

        self.unit_altitude = QLabel('Altitude (m)')
        self.unit_altitude.setStyleSheet('color: #888888; font-size: 11px;')
        self.unit_altitude.setAlignment(Qt.AlignmentFlag.AlignCenter)
        baro_layout.addWidget(self.unit_altitude)
        self.label_altitude = QLabel('---')
        self.label_altitude.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        self.label_altitude.setStyleSheet('color: #00aaff;')
        self.label_altitude.setAlignment(Qt.AlignmentFlag.AlignCenter)
        baro_layout.addWidget(self.label_altitude)

        layout.addWidget(self.baro_group)

        # accelerometer group
        self.accel_group  = QGroupBox('Accelerometer')
        self.accel_group.setStyleSheet('QGroupBox { color: white; }')
        accel_layout = QVBoxLayout(self.accel_group)

        self.unit_ax = QLabel('X (g)')
        self.unit_ax.setStyleSheet('color: #888888; font-size: 11px;')
        self.unit_ax.setAlignment(Qt.AlignmentFlag.AlignCenter)
        accel_layout.addWidget(self.unit_ax)
        self.label_ax = QLabel('---')
        self.label_ax.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        self.label_ax.setStyleSheet('color: #00aaff;')
        self.label_ax.setAlignment(Qt.AlignmentFlag.AlignCenter)
        accel_layout.addWidget(self.label_ax)

        self.unit_ay = QLabel('Y (g)')
        self.unit_ay.setStyleSheet('color: #888888; font-size: 11px;')
        self.unit_ay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        accel_layout.addWidget(self.unit_ay)
        self.label_ay = QLabel('---')
        self.label_ay.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        self.label_ay.setStyleSheet('color: #00aaff;')
        self.label_ay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        accel_layout.addWidget(self.label_ay)

        self.unit_az = QLabel('Z (g)')
        self.unit_az.setStyleSheet('color: #888888; font-size: 11px;')
        self.unit_az.setAlignment(Qt.AlignmentFlag.AlignCenter)
        accel_layout.addWidget(self.unit_az)
        self.label_az = QLabel('---')
        self.label_az.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        self.label_az.setStyleSheet('color: #00aaff;')
        self.label_az.setAlignment(Qt.AlignmentFlag.AlignCenter)
        accel_layout.addWidget(self.label_az)

        layout.addWidget(self.accel_group)

        # gyroscope group
        self.gyro_group  = QGroupBox('Gyroscope')
        self.gyro_group.setStyleSheet('QGroupBox { color: white; }')
        gyro_layout = QVBoxLayout(self.gyro_group)

        self.unit_gx = QLabel('X (dps)')
        self.unit_gx.setStyleSheet('color: #888888; font-size: 11px;')
        self.unit_gx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        gyro_layout.addWidget(self.unit_gx)
        self.label_gx = QLabel('---')
        self.label_gx.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        self.label_gx.setStyleSheet('color: #00aaff;')
        self.label_gx.setAlignment(Qt.AlignmentFlag.AlignCenter)
        gyro_layout.addWidget(self.label_gx)

        self.unit_gy = QLabel('Y (dps)')
        self.unit_gy.setStyleSheet('color: #888888; font-size: 11px;')
        self.unit_gy.setAlignment(Qt.AlignmentFlag.AlignCenter)
        gyro_layout.addWidget(self.unit_gy)
        self.label_gy = QLabel('---')
        self.label_gy.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        self.label_gy.setStyleSheet('color: #00aaff;')
        self.label_gy.setAlignment(Qt.AlignmentFlag.AlignCenter)
        gyro_layout.addWidget(self.label_gy)

        self.unit_gz = QLabel('Z (dps)')
        self.unit_gz.setStyleSheet('color: #888888; font-size: 11px;')
        self.unit_gz.setAlignment(Qt.AlignmentFlag.AlignCenter)
        gyro_layout.addWidget(self.unit_gz)
        self.label_gz = QLabel('---')
        self.label_gz.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        self.label_gz.setStyleSheet('color: #00aaff;')
        self.label_gz.setAlignment(Qt.AlignmentFlag.AlignCenter)
        gyro_layout.addWidget(self.label_gz)

        layout.addWidget(self.gyro_group)

    def update(self, packet):
        self.label_pressure.setText(f"{packet['pressure_pa']:.1f}")
        self.label_temperature.setText(f"{packet['temperature_k'] - 273.15:.2f}")
        self.label_altitude.setText(f"{packet['altitude_m']:.2f}")
        self.label_ax.setText(f"{packet['ax_g']:.4f}")
        self.label_ay.setText(f"{packet['ay_g']:.4f}")
        self.label_az.setText(f"{packet['az_g']:.4f}")
        self.label_gx.setText(f"{packet['gx_dps']:.4f}")
        self.label_gy.setText(f"{packet['gy_dps']:.4f}")
        self.label_gz.setText(f"{packet['gz_dps']:.4f}")