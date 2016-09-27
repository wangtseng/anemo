"""
Last updated on 07/01/2015

@author: Cheng WANG,
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class StatusBar(QWidget):
        def __init__(self, parent=None):
            super(StatusBar, self).__init__(parent)
            self.setAttribute(Qt.WA_TranslucentBackground, True)
            self.font = QFont("Times New Romans", 9, QFont.AnyStyle, True)
            self.errorFont = QFont("Times New Romans", 9, QFont.AnyStyle, True)
            self.setMinimumHeight(15)
            self.messagingLabel = QLabel()
            self.messagingLabel.setAlignment(Qt.AlignLeft)

            my_layout = QHBoxLayout(self)
            my_layout.addWidget(self.messagingLabel)
            my_layout.setSpacing(0)
            my_layout.setContentsMargins(0, 0, 0, 0)
            my_layout.setMargin(0)

        def display_message(self, text):
            self.messagingLabel.setFont(self.font)
            self.messagingLabel.setStyleSheet("color: AliceBlue")
            self.messagingLabel.clear()
            self.messagingLabel.setText(text)

        def display_error_message(self, text):
            self.messagingLabel.setFont(self.errorFont)
            self.messagingLabel.setStyleSheet("color: DarkBlue")
            self.messagingLabel.clear()
            self.messagingLabel.setText(text)

        def clear_message(self):
            self.messagingLabel.clear()
