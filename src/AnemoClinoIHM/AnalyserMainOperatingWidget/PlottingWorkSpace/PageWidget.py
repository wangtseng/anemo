"""
Last updated on 18/12/2014

@author: Cheng WANG,
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from numpy import *
from PlottingBoard import PlottingBoard


class PageWidget(QWidget):
    """ PageWidget

        -- in the page widget, user can add 0 ~ 6 plotting board to achieve the plot operations

    """
    def __init__(self, plotting_workspace_reference=None, page_index=0):
        super(QWidget, self).__init__()
        self.plottingWorkspaceReference = plotting_workspace_reference
        self.pageIndex = page_index
        self.analyserMediator = None

        self.listOfTitles = []

        self.plottingBoardNumber = 0
        self.plottingBoardList = []
        self.plottingBoardListIndex = []
        self.plottingBoardButtonList = []

        # ------------------------------------------------------------------
        # the control bar at the bottom of the page
        # ------------------------------------------------------------------
        self.addPlottingBoardButton = QPushButton()
        self.addPlottingBoardButton.setStyleSheet("QPushButton{border-image: url(:/scissors.png);}")
        self.addPlottingBoardButton.setFixedSize(QSize(23, 23))

        self.pickAllPlottingBoardButton = QPushButton()
        self.pickAllPlottingBoardButton.setStyleSheet("QPushButton{border-image: url(:/pickall.png);}")
        self.pickAllPlottingBoardButton.setFixedSize(QSize(23, 23))

        self.cmdLineEdit = QLineEdit()
        self.cmdLineEdit.setStyleSheet("QLineEdit {border: 2px solid lightGray;border-radius: 10px;padding: 0 8px;background: transparent;selection-background-color: lightBlue;}")

        self.controlFrame = QFrame()
        self.controlFrame.setFixedHeight(40)
        self.control_frame_layout = QHBoxLayout(self.controlFrame)
        self.control_frame_layout.addWidget(self.addPlottingBoardButton)
        self.control_frame_layout.addWidget(self.pickAllPlottingBoardButton)
        self.control_frame_layout.addWidget(self.cmdLineEdit)
        self.control_frame_layout.setSpacing(0)
        self.control_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.control_frame_layout.setMargin(0)
        self.controlFrame.setLayout(self.control_frame_layout)

        # ------------------------------------------------------------------
        # the widget for contain the plotting board
        # ------------------------------------------------------------------
        self.plottingBoardWidget = QWidget()
        self.plottingBoardWidgetLayout = QGridLayout(self.plottingBoardWidget)
        self.plottingBoardWidgetLayout.setSpacing(0)
        self.plottingBoardWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.plottingBoardWidgetLayout.setMargin(0)

        # ----------------------------------
        # the main layout of the widget
        # ----------------------------------
        layout = QVBoxLayout(self)
        layout.addWidget(self.plottingBoardWidget)
        layout.addWidget(self.controlFrame)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setMargin(0)
  
        # self.cmdLineEdit.setText("draw {IN_PT_PROBE_CPT = f(IN_ALPHA_PROBE_FO), V0001V0192_takeoff_GISEH_IN.csv} on graph 1")
        self.cmdLineEdit.setDragEnabled(True)
        self.connect(self.addPlottingBoardButton, SIGNAL("clicked()"), self.add_a_plotting_board)
        self.connect(self.cmdLineEdit, SIGNAL("returnPressed()"), self.command_parsing)

    def get_parent(self):
        """
            --get the reference plotting workspace
        """
        return self.plottingWorkspaceReference

    def set_my_page_index(self, index):
        """
            -- set the index of the page on the plotting workspace
        :param index:
        """
        self.pageIndex = index

    def get_my_page_index(self):
        return self.pageIndex

    def set_analyser_mediator(self, analyser_mediator):
        """
            -- set the analyser_mediator reference to the page for access of the global context
        :param analyser_mediator:
        """
        self.analyserMediator = analyser_mediator

    def minimize_curve_operation_board_at(self, index):
        """
            --minimize the plotting board with the index passed, then generate a button on control bar
              there are two list which is import for the close&display action
              self.plottingBoardList      =  [button1, button2, button3, ...]
              self.plottingBoardListIndex =  [index_for_button1, index_for_button2, index_for_button3, ...]

              each time the user minimize a plotting board, we'll generate a button with the plotting board index, and then we store the button to the plottingBoardButtonList
              and at the same position of the list plottingBoardListIndex, we will save the index of the plotting board in this page. so that it will be easy to redisplay the
              plotting board at the right position on the grid layout

        :param index:
        """
        button = QPushButton(str(index))
        button.setFixedSize(25, 25)
        button.setFlat(1)
        button.setStyleSheet("border-image:url(:/curvechart.png); color: white")
        self.control_frame_layout.addWidget(button)
        self.plottingBoardButtonList.append(button)
        self.plottingBoardListIndex.append(index)
        self.connect(button, SIGNAL("clicked()"), self.display_the_board)

    def display_the_board(self):
        """
            --if user click the button at the right side of the control bar, the function is to find the plotting board related to the index represent by the button,
            then redisplay it.
        """
        for i in range(len(self.plottingBoardButtonList)):
            if QObject.sender(self) == self.plottingBoardButtonList[i]:
                self.plottingBoardList[self.plottingBoardListIndex[i]].display_the_curve()
                self.plottingBoardButtonList[i].deleteLater()   # remove the button displayed on the control bar
                del self.plottingBoardButtonList[i]
                del self.plottingBoardListIndex[i]
                break

    def get_plotting_board_at(self, index):
        for p in self.plottingBoardList:
            if p.get_plotting_index() == index:
                return p

    def add_a_plotting_board(self):
        """
            --add_a_plotting_board
            1, generate a new plotting board
            2, add the widget to the plottingBoardWidgetLayout with the current plottingBoardNumber and the page index
            3, add a page context in global context with the same plottingBoardNumber and the page index
            4, plottingBoardNumber + 1 for the next plotting board
        """
        plotting_board = PlottingBoard(self)
        plotting_board.set_analyser_mediator(self.analyserMediator)

        if self.plottingBoardNumber == 0:
            self.plottingBoardWidgetLayout.addWidget(plotting_board, 0, 0)
            self.plottingBoardList.append(plotting_board)

        elif self.plottingBoardNumber == 1:
            self.plottingBoardWidgetLayout.addWidget(plotting_board, 1, 0)
            self.plottingBoardList.append(plotting_board)

        elif self.plottingBoardNumber == 2:
            self.plottingBoardWidgetLayout.addWidget(plotting_board, 2, 0)
            self.plottingBoardList.append(plotting_board)

        elif self.plottingBoardNumber == 3:
            self.plottingBoardWidgetLayout.removeWidget(self.plottingBoardList[1])
            self.plottingBoardWidgetLayout.removeItem(self.plottingBoardWidgetLayout.itemAtPosition(1, 0))
            self.plottingBoardWidgetLayout.removeWidget(self.plottingBoardList[2])
            self.plottingBoardWidgetLayout.removeItem(self.plottingBoardWidgetLayout.itemAtPosition(2, 0))

            self.plottingBoardWidgetLayout.addWidget(self.plottingBoardList[1], 0, 1)
            self.plottingBoardWidgetLayout.addWidget(self.plottingBoardList[2], 1, 0)
            self.plottingBoardWidgetLayout.addWidget(plotting_board, 1, 1)
            self.plottingBoardList.append(plotting_board)

        elif self.plottingBoardNumber == 4:
            self.plottingBoardWidgetLayout.addWidget(plotting_board, 2, 0)
            self.plottingBoardList.append(plotting_board)

        elif self.plottingBoardNumber == 5:
            self.plottingBoardWidgetLayout.addWidget(plotting_board, 2, 1)
            self.plottingBoardList.append(plotting_board)

        else:
            print "too many curve in one page"
            return

        self.analyserMediator.add_a_plotting_context_in_a_page(self.pageIndex, self.plottingBoardNumber)
        plotting_board.set_plotting_index(self.plottingBoardNumber)
        plotting_board.set_page_index(self.pageIndex)
        self.analyserMediator.generate_an_action_into_global_context('add a plotting board in page ' + str(self.pageIndex))

        self.plottingBoardNumber += 1

    # TODO to be developed after new year
    def command_parsing(self):
        cmd = str(self.cmdLineEdit.text())
        cmdlist = cmd.split("{")

        if (cmdlist[0] == "draw") or (cmdlist[0] == "draw "):
                plotting_action_list = cmdlist[1].split("}")

                howToDraw = plotting_action_list[0]
                whereToDraw = plotting_action_list[1]

                plottingConditions = howToDraw.split(",")
                function = plottingConditions[0]
                fileName = plottingConditions[1]

                temp1 = function.rstrip()
                function = temp1.lstrip()
                temp2 = fileName.rstrip()
                fileName = temp2.lstrip()

                csvfile = self.analyserMediator.get_csv_file_in_context_by_name(csv_file_name)
                self.values = self.csvFile.get_values()
                self.listOfTitles = self.csvFile.get_title_list()
                rowCount     = self.csvFile.get_row_count()

                functionp = function.translate(None," ")

                coordinates = functionp.split("=f(")
                Y_coordinate = coordinates[0]
                X_coordinate = coordinates[1].translate(None, ")")

                Y_valuePointer = self.listOfTitles.index(Y_coordinate)
                X_valuePointer = self.listOfTitles.index(X_coordinate)

                Y_values = []
                X_values = []

                for i in range(0, rowCount - 1):
                    Y_values.append(self.values[i][Y_valuePointer])
                    X_values.append(self.values[i][X_valuePointer])

                whereInfo = whereToDraw.translate(None, " ")
                graphNum = whereInfo.translate(None, "ongraph")

                if int(graphNum) <= (self.plottingBoardNumber + 1):
                        self.plottingBoardList[int(graphNum) - 1].setPropertyOfCurve(X_coordinate, Y_coordinate, X_values, Y_values)
                else:
                    print "no widget available"