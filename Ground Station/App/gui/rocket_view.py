# gui/rocket_view.py
# Draws a 3D rocket and rotates it based on gyroscope data

import numpy as np
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox
from PyQt6.QtCore import QTimer
import pyqtgraph.opengl as gl


class RocketView(QWidget):

    def __init__(self):
        super().__init__()
        # euler angles in degrees — integrated from gyro data
        self.roll  = 0.0
        self.pitch = 0.0
        self.yaw   = 0.0
        self.last_timestamp_ms = None
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        self.group = QGroupBox('Rocket Orientation')
        self.group.setStyleSheet('QGroupBox { color: white; }')
        group_layout = QVBoxLayout(self.group)

        # 3D OpenGL viewport
        self.view = gl.GLViewWidget()
        self.view.setBackgroundColor('#1e1e1e')
        self.view.setCameraPosition(distance=6, elevation=20, azimuth=45)
        self.view.setMinimumHeight(300)
        group_layout.addWidget(self.view)

        # add a grid on the ground plane for reference
        self.grid = gl.GLGridItem()
        self.grid.setSize(10, 10)
        self.grid.setSpacing(1, 1)
        self.view.addItem(self.grid)

        # build the rocket mesh and add to view
        self.rocket_body  = self._make_rocket_body()
        self.rocket_nose  = self._make_nose_cone()
        self.rocket_fins  = self._make_fins()

        self.view.addItem(self.rocket_body)
        self.view.addItem(self.rocket_nose)
        for fin in self.rocket_fins:
            self.view.addItem(fin)

        layout.addWidget(self.group)

    def _make_rocket_body(self):
        # cylinder along the Z axis representing the main body
        radius    = 0.15
        height    = 2.0
        segments  = 24
        verts     = []
        faces     = []

        # generate vertices around the cylinder
        for i in range(segments):
            angle = 2 * np.pi * i / segments
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            verts.append([x, y, 0])         # bottom ring
            verts.append([x, y, height])    # top ring

        verts = np.array(verts)

        # connect vertices into triangular faces
        for i in range(segments):
            b0 = i * 2
            b1 = ((i + 1) % segments) * 2
            t0 = b0 + 1
            t1 = b1 + 1
            faces.append([b0, b1, t0])
            faces.append([b1, t1, t0])

        faces    = np.array(faces)
        colors   = np.ones((len(faces), 4))
        colors[:, 0] = 0.8   # R
        colors[:, 1] = 0.2   # G
        colors[:, 2] = 0.2   # B

        mesh = gl.GLMeshItem(vertexes=verts, faces=faces, faceColors=colors, smooth=False)
        return mesh

    def _make_nose_cone(self):
        # cone on top of the body
        radius   = 0.15
        height   = 0.6
        segments = 24
        tip_z    = 2.0 + height
        base_z   = 2.0
        verts    = [[0, 0, tip_z]]   # tip of the cone

        for i in range(segments):
            angle = 2 * np.pi * i / segments
            verts.append([radius * np.cos(angle), radius * np.sin(angle), base_z])

        verts = np.array(verts)
        faces = []
        for i in range(segments):
            faces.append([0, i + 1, (i % segments) + 2 if i < segments - 1 else 1])

        faces  = np.array(faces)
        colors = np.ones((len(faces), 4))
        colors[:, 0] = 0.9
        colors[:, 1] = 0.6
        colors[:, 2] = 0.1

        return gl.GLMeshItem(vertexes=verts, faces=faces, faceColors=colors, smooth=False)

    def _make_fins(self):
        # four flat fins at the base of the rocket
        fins = []
        for i in range(4):
            angle  = np.pi / 2 * i
            cos_a  = np.cos(angle)
            sin_a  = np.sin(angle)
            r      = 0.15

            verts = np.array([
                [r * cos_a,       r * sin_a,       0.0],
                [(r + 0.4) * cos_a, (r + 0.4) * sin_a, 0.0],
                [r * cos_a,       r * sin_a,       0.5],
            ])
            faces  = np.array([[0, 1, 2]])
            colors = np.ones((1, 4))
            colors[0] = [0.2, 0.4, 0.9, 1.0]

            fins.append(gl.GLMeshItem(vertexes=verts, faces=faces, faceColors=colors, smooth=False))

        return fins

    def _apply_rotation(self):
        # apply current roll, pitch, yaw to all rocket parts
        transform = gl.GLMeshItem

        # reset and reapply rotation to each part
        for item in [self.rocket_body, self.rocket_nose] + self.rocket_fins:
            item.resetTransform()
            item.rotate(self.yaw,   0, 0, 1)   # yaw   around Z
            item.rotate(self.pitch, 1, 0, 0)   # pitch around X
            item.rotate(self.roll,  0, 1, 0)   # roll  around Y

    def update(self, packet):
        # integrate gyro rates over time to get angles
        ts = packet['timestamp_ms']

        if self.last_timestamp_ms is not None:
            dt = (ts - self.last_timestamp_ms) / 1000.0   # convert ms to seconds
            if 0 < dt < 0.5:   # ignore large gaps
                self.roll  += packet['gx_dps'] * dt
                self.pitch += packet['gy_dps'] * dt
                self.yaw   += packet['gz_dps'] * dt

        self.last_timestamp_ms = ts
        self._apply_rotation()