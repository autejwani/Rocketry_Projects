# gui/main_window.py
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                              QHBoxLayout, QComboBox, QPushButton, QLabel, QGroupBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from comms.serial_worker import SerialWorker, list_ports
from gui.telemetry_panel import TelemetryPanel
from gui.state_panel import StatePanel
from gui.rocket_view import RocketView


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('FC Ground Station')
        self.setMinimumSize(1200, 700)
        self.worker = None
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        top_layout = QHBoxLayout(central)
        top_layout.setSpacing(10)
        top_layout.setContentsMargins(10, 10, 10, 10)

        # left panel
        self.left_panel = QWidget()
        self.left_panel.setFixedWidth(220)
        left_layout = QVBoxLayout(self.left_panel)
        left_layout.setSpacing(8)

        self.title = QLabel('FC Ground Station')
        self.title.setFont(QFont('Arial', 13, QFont.Weight.Bold))
        self.title.setStyleSheet('color: #00aaff;')
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(self.title)

        self.conn_group = QGroupBox('Connection')
        self.conn_group.setStyleSheet('QGroupBox { color: white; }')
        conn_layout = QVBoxLayout(self.conn_group)

        self.port_label = QLabel('Port:')
        conn_layout.addWidget(self.port_label)
        self.combo_port = QComboBox()
        self.combo_port.addItems(list_ports())
        conn_layout.addWidget(self.combo_port)

        self.baud_label = QLabel('Baud Rate:')
        conn_layout.addWidget(self.baud_label)
        self.combo_baud = QComboBox()
        self.combo_baud.addItems(['9600', '57600', '115200', '230400'])
        self.combo_baud.setCurrentText('115200')
        conn_layout.addWidget(self.combo_baud)

        self.btn_refresh = QPushButton('Refresh Ports')
        self.btn_refresh.clicked.connect(self._refresh_ports)
        conn_layout.addWidget(self.btn_refresh)

        self.btn_connect = QPushButton('Connect')
        self.btn_connect.setFixedHeight(40)
        self.btn_connect.setStyleSheet('''
            QPushButton { background-color: #00aaff; color: black; font-weight: bold; border-radius: 5px; }
            QPushButton:hover { background-color: #33bbff; }
        ''')
        self.btn_connect.clicked.connect(self._on_connect_clicked)
        conn_layout.addWidget(self.btn_connect)

        self.label_status = QLabel('Disconnected')
        self.label_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_status.setStyleSheet('color: #ff4444;')
        conn_layout.addWidget(self.label_status)

        left_layout.addWidget(self.conn_group)
        left_layout.addStretch()

        # right panel — created once, telemetry panel lives here
        self.right_panel = QWidget()
        self.right_layout = QVBoxLayout(self.right_panel)
        self.telemetry_panel = TelemetryPanel()
        self.state_panel = StatePanel()
        self.rocket_view = RocketView()
        self.right_layout.addWidget(self.telemetry_panel)
        self.right_layout.addWidget(self.state_panel)
        self.right_layout.addWidget(self.rocket_view)

        top_layout.addWidget(self.left_panel)
        top_layout.addWidget(self.right_panel)

    def _refresh_ports(self):
        self.combo_port.clear()
        self.combo_port.addItems(list_ports())

    def _on_connect_clicked(self):
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker = None
            self.btn_connect.setText('Connect')
            self.btn_connect.setStyleSheet('''
                QPushButton { background-color: #00aaff; color: black; font-weight: bold; border-radius: 5px; }
                QPushButton:hover { background-color: #33bbff; }
            ''')
            self.label_status.setText('Disconnected')
            self.label_status.setStyleSheet('color: #ff4444;')
        else:
            port      = self.combo_port.currentText()
            baud_rate = int(self.combo_baud.currentText())
            self.worker = SerialWorker(port, baud_rate)
            self.worker.packet_received.connect(self._on_packet)
            self.worker.connection_error.connect(self._on_error)
            self.worker.start()
            self.btn_connect.setText('Disconnect')
            self.btn_connect.setStyleSheet('''
                QPushButton { background-color: #ff4444; color: white; font-weight: bold; border-radius: 5px; }
                QPushButton:hover { background-color: #ff6666; }
            ''')
            self.label_status.setText(f'Connected\n{port}')
            self.label_status.setStyleSheet('color: #00ff99;')

    def _on_packet(self, packet):
        self.telemetry_panel.update(packet)
        self.state_panel.update(packet)
        self.rocket_view.update(packet)

    def _on_error(self, error):
        self.label_status.setText(f'Error:\n{error}')
        self.label_status.setStyleSheet('color: #ff4444;')


def run():
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget { background-color: #1e1e1e; color: white; }
        QGroupBox { border: 1px solid #444444; border-radius: 4px; margin-top: 8px; padding-top: 8px; }
        QGroupBox::title { subcontrol-origin: margin; left: 8px; }
        QComboBox, QSpinBox { background-color: #2a2a2a; color: white; border: 1px solid #444444; padding: 3px; border-radius: 3px; }
        QPushButton { background-color: #2a2a2a; color: white; border: 1px solid #444444; padding: 4px; border-radius: 3px; }
        QLabel { color: #cccccc; }
    ''')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    run()