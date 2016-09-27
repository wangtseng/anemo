"""
Last updated on 07/01/2015

@author: Cheng WANG,
"""

import os
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class TitleListWidget(QListWidget):

    def __init__(self, parent=None):
        super(QListWidget, self).__init__(parent)
        self.parent = parent
        self.setStyleSheet("QListWidget {show-decoration-selected: 2;}"
                           "QListWidget::item:alternate { background: transparent;}"
                           "QListWidget::item:selected {border: 0px;}"
                           "QListWidget::item:selected:!active {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 lightGreen, stop: 1 DarkSeaGreen);}"
                           "QListWidget::item:selected:active {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 DarkSeaGreen, stop: 1 lightGreen);}"
                           "QListWidget::item:hover {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #FAFBFE, stop: 1 #DCDEF1);}")

        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDefaultDropAction(Qt.MoveAction)

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.viewport().setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()
    '''
    def dragLeaveEvent(self, event):
        self.parent.update_title_list_widget()
    '''

    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            data = event.mimeData().data("application/x-icon-and-text")
            stream = QDataStream(data, QIODevice.ReadOnly)
            text = QString()
            icon = QIcon()
            stream >> text >> icon
            item = QListWidgetItem(text, self)
            item.setIcon(icon)
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def startDrag(self, event):
        item = self.currentItem()
        icon = item.icon()
        data = QByteArray()
        stream = QDataStream(data, QIODevice.WriteOnly)
        stream << item.text() << icon

        mimeData = QMimeData()
        mimeData.setData("application/x-icon-and-text", data)
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        pixmap = icon.pixmap(24, 24)
        drag.setHotSpot(QPoint(12, 12))
        drag.setPixmap(pixmap)

        if drag.start(Qt.MoveAction) == Qt.MoveAction:
            print 'dragged'
            #self.takeItem(self.row(item))
