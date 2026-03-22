# gui/state_panel.py
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGroupBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


# colour for each flight state
STATE_COLORS = {
    'IDLE':    '#888888',
    'ARMED':   '#ffaa00',
    'ASCENT':  '#00ff99',
    'COAST':   '#00aaff',
    'APOGEE':  '#ff6600',
    'DESCENT': '#ffff00',
    'MAIN':    '#ff00ff',
    'LANDED':  '#ffffff',
    'UNKNOWN': '#ff4444',
}

# all states in flight order — used to draw the progress indicators
STATES_IN_ORDER = ['IDLE', 'ARMED', 'ASCENT', 'COAST', 'APOGEE', 'DESCENT', 'MAIN', 'LANDED']


class StatePanel(QWidget):

    def __init__(self):
        super().__init__()
        self.current_state = 'IDLE'
        self._build_ui()

    def _build_ui(self):
        layout = QHBoxLayout(self)
        layout.setSpacing(10)

        # current state group — large label showing the active state
        self.state_group = QGroupBox('Flight State')
        self.state_group.setStyleSheet('QGroupBox { color: white; }')
        state_layout = QVBoxLayout(self.state_group)

        self.label_state = QLabel('IDLE')
        self.label_state.setFont(QFont('Arial', 28, QFont.Weight.Bold))
        self.label_state.setStyleSheet(f'color: {STATE_COLORS["IDLE"]};')
        self.label_state.setAlignment(Qt.AlignmentFlag.AlignCenter)
        state_layout.addWidget(self.label_state)

        self.label_timestamp = QLabel('T+ 0.000 s')
        self.label_timestamp.setStyleSheet('color: #888888; font-size: 11px;')
        self.label_timestamp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        state_layout.addWidget(self.label_timestamp)

        layout.addWidget(self.state_group)

        # state progress group — shows all states with current one highlighted
        self.progress_group = QGroupBox('Flight Progress')
        self.progress_group.setStyleSheet('QGroupBox { color: white; }')
        progress_layout = QHBoxLayout(self.progress_group)

        # create one label per state — stored in a dict for easy access
        self.state_labels = {}
        for state in STATES_IN_ORDER:
            lbl = QLabel(state)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setFixedWidth(80)
            lbl.setStyleSheet('color: #444444; font-size: 10px; padding: 4px; border: 1px solid #444444; border-radius: 3px;')
            progress_layout.addWidget(lbl)
            self.state_labels[state] = lbl

        layout.addWidget(self.progress_group)

    def update(self, packet):
        state     = packet['state']
        timestamp = packet['timestamp_ms'] / 1000.0
        color     = STATE_COLORS.get(state, '#ff4444')

        # update the large state label
        self.label_state.setText(state)
        self.label_state.setStyleSheet(f'color: {color}; font-size: 28px; font-weight: bold;')
        self.label_timestamp.setText(f'T+ {timestamp:.3f} s')

        # update the progress bar — highlight current state, dim all others
        for s, lbl in self.state_labels.items():
            if s == state:
                lbl.setStyleSheet(f'color: {color}; font-size: 10px; font-weight: bold; padding: 4px; border: 1px solid {color}; border-radius: 3px;')
            elif STATES_IN_ORDER.index(s) < STATES_IN_ORDER.index(state):
                # past states shown in dim green to indicate they were completed
                lbl.setStyleSheet('color: #225522; font-size: 10px; padding: 4px; border: 1px solid #225522; border-radius: 3px;')
            else:
                # future states shown dimmed
                lbl.setStyleSheet('color: #444444; font-size: 10px; padding: 4px; border: 1px solid #444444; border-radius: 3px;')