from PyQt4.QtCore import *
from PyQt4.QtGui import *
from InformationBoard.InformationBoard import InformationBoard
from PlottingWorkSpace.PlottingWorkSpace import PlottingWorkSpace


class MainOperatingWidget(QWidget):

    """MainOperatingWidget

        - This class represent the main operating area of the analyser

    Attributes:
        - four principal component

            *******************************************
            *                   *                     *
            *                   *                     *
            *   Information     *  Plotting           *
            *   Board           *  workspace          *
            *                   *                     *
            *******************************************

    """
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.analyseurMediator = None
        self.informationBoard = InformationBoard(self)
        self.plottingWorkSpace = PlottingWorkSpace(self)

        my_layout = QHBoxLayout(self)
        my_layout.addWidget(self.informationBoard)
        my_layout.addWidget(self.plottingWorkSpace)
        my_layout.setSpacing(4)
        my_layout.setContentsMargins(0, 0, 0, 0)
        my_layout.setMargin(0)
        my_layout.setAlignment(Qt.AlignLeft)

    def set_analyseur_mediator(self, analyseur_mediator):
        self.analyseurMediator = analyseur_mediator
        self.plottingWorkSpace.set_analyseur_mediator(self.analyseurMediator)
        self.informationBoard.set_analyseur_mediator(self.analyseurMediator)

    def get_information_board(self):
        return self.informationBoard

    def get_plotting_workspace(self):
        return self.plottingWorkSpace

