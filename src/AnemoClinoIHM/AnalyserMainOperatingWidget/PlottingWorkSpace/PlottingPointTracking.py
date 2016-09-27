"""
Last updated on 07/01/2015

@author: Cheng WANG,
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class PlottingPointTracking(QWidget):
    def __init__(self, parent=None):
        super(PlottingPointTracking, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet('background-color: skyblue')
        self.font = QFont("Helvetica", 8, QFont.AnyStyle, True)
        layout = QHBoxLayout(self)
        self.coordinate_display = QLabel()
        self.coordinate_display.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.coordinate_display.setStyleSheet('background-color: transparent; color:AliceBlue')
        self.coordinate_display.setAlignment(Qt.AlignRight)
        self.coordinate_display.setFont(self.font)
        self.coordinate_display.setEnabled(False)

        self.coordinate_value_display = QLabel()
        self.coordinate_value_display.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.coordinate_value_display.setStyleSheet('background-color: transparent; color:AliceBlue')
        self.coordinate_value_display.setFont(self.font)
        self.coordinate_value_display.setEnabled(False)

        layout.addWidget(self.coordinate_display)
        layout.addWidget(self.coordinate_value_display)
        layout.setSpacing(0)
        layout.setMargin(1)

    def set_point_information(self, information_parameter, information_value):
        self.coordinate_display.clear()
        self.coordinate_display.setText(information_parameter)
        self.coordinate_value_display.setText(information_value)

    def close_window(self):
        self.close()

    def display(self, pos):
        self.show()
        self.move(pos.x() + 20, pos.y() - 80)