"""
Last updated on 07/01/2015

@author: Cheng WANG,
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class ExtraParameterWidget(QListWidget):

    def __init__(self, parent=None):
        super(ExtraParameterWidget, self).__init__(parent)
        self.parent = parent
        self.analyserMediator = None
        self.plottingBoardReference = None
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.parameterList = []

    def set_plotting_board_reference(self, plotting_board_reference):
        self.plottingBoardReference = plotting_board_reference

    def set_analyser_mediator(self, analyser_controller):
        self.analyserMediator = analyser_controller

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

    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            data = event.mimeData().data("application/x-icon-and-text")
            stream = QDataStream(data, QIODevice.ReadOnly)
            text = QString()
            icon = QIcon()
            stream >> text >> icon
            item = QListWidgetItem(text, self)
            item.setIcon(icon)
            parameter_name = text
            if self.parent.check_parameter_dragged(parameter_name):
                self.parameterList.append(parameter_name)
                self.analyserMediator.generate_an_action_into_global_context('set an extra parameter: ' + parameter_name + ' for plotting board :'
                                                                             + str(self.plottingBoardReference.get_plotting_index()) + ' in page: '
                                                                             + str(self.plottingBoardReference.get_page_index()))
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def drop_event_while_import(self, text):
        icon = QIcon(':/title.png')
        item = QListWidgetItem(text, self)
        parameter_name = text
        if self.parent.check_parameter_dragged(parameter_name):
            self.parameterList.append(parameter_name)
            self.analyserMediator.generate_an_action_into_global_context('set an extra parameter: ' + parameter_name + ' for plotting board :'
                                                                         + str(self.plottingBoardReference.get_plotting_index()) + ' in page: '
                                                                         + str(self.plottingBoardReference.get_page_index()))

    def startDrag(self, dropActions):
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
            self.takeItem(self.row(item))

    def get_extra_parameter_list(self):
        return self.parameterList