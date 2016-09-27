"""
Last updated on 07/01/2015

@author: Cheng WANG,
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class LittleAirbusLabel(QPushButton):
    def __init__(self, parent=None):
        super(LittleAirbusLabel, self).__init__(parent)
        self.setStyleSheet('QPushButton{border-image: url(:/logo.png);}; border:0px;')
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setFixedSize(QSize(90, 35))
        self.setAcceptDrops(True)
        self.setFlat(True)

    def dragEnterEvent(self, e):
        self.setStyleSheet('QPushButton{border-image: url(:/upload_files.png);}; border:0px;')
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, event):
        self.setStyleSheet('QPushButton{border-image: url(:/logo.png);}; border:0px;')
        for url in event.mimeData().urls():
            filepath = url.toLocalFile()
            self.parent().add_file_from_path(filepath)