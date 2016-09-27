"""
Last updated on 07/01/2015

@author: Cheng WANG,
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class SISOLabel(QLabel):
    def __init__(self, parent=None):
        super(SISOLabel, self).__init__(parent)
        self.parent = parent
        self.analyserMediator = None
        self.setAcceptDrops(True)
        self.doubleClicked = False

    def set_analyser_mediator(self, analyser_mediator_reference):
        self.analyserMediator = analyser_mediator_reference

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked = not self.doubleClicked

        if self.doubleClicked:
            self.parent.siso_checked_all()
        else:
            self.parent.siso_unchecked_all()

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            data = event.mimeData().data("application/x-icon-and-text")
            stream = QDataStream(data, QIODevice.ReadOnly)
            text = QString()
            stream >> text

        cutting_choice = QMessageBox()
        represent_by_color = cutting_choice.addButton(str("represent by color"), QMessageBox.ActionRole)
        represent_by_color.setFlat(1)
        represent_by_marker = cutting_choice.addButton(str("represent by marker"), QMessageBox.ActionRole)
        represent_by_marker.setFlat(1)
        cutting_choice.setFont(QFont("Helvetica", 8, QFont.AnyStyle, True))
        cutting_choice.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        cutting_choice.setText("Choose the point represent mode:")
        cutting_choice.setStyleSheet("background-color: skyBlue; color: AliceBlue")
        cutting_choice.exec_()

        if cutting_choice.clickedButton() == represent_by_color:
            self.parent.set_siso_config("represent_by_color")
            self.analyserMediator.generate_an_action_into_global_context(' set siso in plotting board :'
                                                                         + str(self.parent.get_plotting_board_reference().get_plotting_index()) + ' in page: '
                                                                         + str(self.parent.get_plotting_board_reference().get_page_index()) + ' represent by color')
        if cutting_choice.clickedButton() == represent_by_marker:
            self.parent.set_siso_config("represent_by_marker")
            self.analyserMediator.generate_an_action_into_global_context(' set siso in plotting board :'
                                                                         + str(self.parent.get_plotting_board_reference().get_plotting_index()) + ' in page: '
                                                                         + str(self.parent.get_plotting_board_reference().get_page_index()) + ' represent by marker')

        self.setText("siso: " + text)
        self.parent.set_siso_parameter_name(text)
        self.analyserMediator.generate_an_action_into_global_context('set ' + text + ' as siso for plotting board :'
                                                                     + str(self.parent.get_plotting_board_reference().get_plotting_index()) + ' in page: '
                                                                     + str(self.parent.get_plotting_board_reference().get_page_index()))

    def set_siso_represent_by(self, mode):
        if mode == 'color':
            self.parent.set_siso_config("represent_by_color")
            self.analyserMediator.generate_an_action_into_global_context('set siso in plotting board :'
                                                                         + str(self.parent.get_plotting_board_reference().get_plotting_index()) + ' in page: '
                                                                         + str(self.parent.get_plotting_board_reference().get_page_index()) + ' represent by color')
        elif mode == 'marker':
            self.parent.set_siso_config("represent_by_marker")
            self.analyserMediator.generate_an_action_into_global_context('set siso in plotting board :'
                                                                         + str(self.parent.get_plotting_board_reference().get_plotting_index()) + ' in page: '
                                                                         + str(self.parent.get_plotting_board_reference().get_page_index()) + ' represent by marker')

    def drop_event_while_import(self, text):
        self.setText("siso: " + text)
        self.parent.set_siso_parameter_name(text)
        self.analyserMediator.generate_an_action_into_global_context('set ' + text + ' as siso for plotting board :'
                                                                     + str(self.parent.get_plotting_board_reference().get_plotting_index()) + ' in page: '
                                                                     + str(self.parent.get_plotting_board_reference().get_page_index()))


class ISOLabel(QLabel):
    def __init__(self, parent=None):
        super(ISOLabel, self).__init__(parent)
        self.parent = parent
        self.analyserMediator = None
        self.setAcceptDrops(True)
        self.doubleClicked = False

    def set_analyser_mediator(self, analyser_mediator_reference):
        self.analyserMediator = analyser_mediator_reference

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked = not self.doubleClicked

        if self.doubleClicked:
            self.parent.iso_checked_all()
        else:
            self.parent.iso_unchecked_all()

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):

        if event.mimeData().hasFormat("application/x-icon-and-text"):
            data = event.mimeData().data("application/x-icon-and-text")
            stream = QDataStream(data, QIODevice.ReadOnly)
            text = QString()
            stream >> text
        self.setText("iso: " + text)

        self.parent.set_iso_parameter_name(text)
        self.analyserMediator.generate_an_action_into_global_context('set ' + text + ' as iso for plotting board :'
                                                                     + str(self.parent.get_plotting_board_reference().get_plotting_index()) + ' in page: '
                                                                     + str(self.parent.get_plotting_board_reference().get_page_index()))

    def drop_event_while_import(self, text):
        self.setText("iso: " + text)

        self.parent.set_iso_parameter_name(text)
        self.analyserMediator.generate_an_action_into_global_context('set ' + text + ' as iso for plotting board :'
                                                                     + str(self.parent.get_plotting_board_reference().get_plotting_index()) + ' in page: '
                                                                     + str(self.parent.get_plotting_board_reference().get_page_index()))
