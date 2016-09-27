"""
Last updated on 07/01/2015

@author: Cheng WANG,
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class LomEditWidget(QWidget):
    def __init__(self, parent=None):
        super(LomEditWidget, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.font = QFont("Helvetica", 8, QFont.AnyStyle, True)
        self.lomfileLabel = QLabel()
        self.label_1 = QLabel(':')

        self.abscissaNameLabel = QLabel()
        self.ordinateNameLabel = QLabel()
        self.isoNameLabel = QLabel()
        self.sisoNameLabel = QLabel()

        self.abscissaLabel = QLabel('abscissa')
        self.ordinateLabel = QLabel('ordinate')
        self.isoLabel = QLabel('iso')
        self.sisoLabel = QLabel('siso')

        self.abscissaValueLabel = QLabel('abscissa')
        self.ordinateValueLabel = QLabel('ordinate')
        self.isoLabel = QLabel('iso')
        self.sisoLabel = QLabel('siso')

        layout = QGridLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setMargin(0)
        layout.setMargin(0)