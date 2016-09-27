# coding=utf-8
"""
Last updated on 18/12/2014

@author: Cheng WANG,
"""

import PyQt4.Qwt5 as Qwt
import numpy as np
from PyQt4.Qt import *
from PyQt4.Qwt5 import *
#from PyQt4.Qwt5.anynumpy import *
from scipy import zeros

from PlottingParametersManipulation import PlottingParametersManipulation
from PlottingPointTracking import PlottingPointTracking
from PlottingOption import PlottingOption
from Plotting import Plotting
# noinspection PyUnresolvedReferences
from AnemoClinoIHM.AnalyserUsefulClasses.ObjectEventService import ObjectEventService


class PlottingBoard(QWidget):
    """PlottingBoard

        -- This class represent a plotting unit in a page

    Attributes:
        -- four principal component
            *******************************************
            *           menuBar                       *
            *******************************************
            *                               *         *
            *                               *         *
            *     plotting    area          *  manip  *
            *                               *         *
            *                               *         *
            *******************************************
    """

    def __init__(self, parent=None):
        super(PlottingBoard, self).__init__(parent)

        # ------------------------------------------------------
        # statement of the parameter useful
        # ------------------------------------------------------
        self.page_widget_reference = parent

        self.colorList = ["blue",
                          "CadetBlue",
                          "DarkSlateGray",
                          "aquamarine",
                          "magenta",
                          "brown",
                          "gold",
                          "BlueViolet",
                          "SteelBlue",
                          "thistle",
                          "chartreuse",
                          "DeepPink",
                          "IndianRed",
                          "SpringGreen"]

        self.markerList = [('O', QwtSymbol.Ellipse),
                           ('口', QwtSymbol.Rect),
                           ('◇', QwtSymbol.Diamond),
                           ('▽', QwtSymbol.DTriangle),
                           ('△', QwtSymbol.UTriangle),
                           ('◁', QwtSymbol.LTriangle),
                           ('▷', QwtSymbol.RTriangle),
                           ('+', QwtSymbol.Cross),
                           ('✳', QwtSymbol.Star1),
                           ('☆', QwtSymbol.Star2),
                           ('hexagon', QwtSymbol.Hexagon),
                           ('X', QwtSymbol.XCross),
                           ('--', QwtSymbol.HLine),
                           ('|', QwtSymbol.VLine)]

        self.numberOfDigitToKeep = 8

        self.my_plotting_index = 0
        self.my_page_index = 0

        self.labelToBeModified = ()
        self.pointToBeModified = ()

        self.abscissa_point = 12345
        self.ordinate_point = 54321

        self.radius_x = 1
        self.radius_y = 1

        self.analyserMediator = None

        self.ordinate_list = []
        self.function = ""
        self.abscissa = ""
        self.iso = ""
        self.siso = ""

        self.zoomingState = 0
        self.canvasOperationMode = 0

        self.calibrateFile = ""
        self.mouseButtonOnCanvasClicked = False

        self.extraParameterTobeDisplayed = []
        self.extraValues = {}

        self.plottingOption = PlottingOption()
        self.plottingOption.set_plotting_board_reference(self)

        self.plottingPointDisplay = PlottingPointTracking()  # in point tracking mode, this widget is to display the point found
        self.setContextMenuPolicy(Qt.NoContextMenu)

        # ----------------------------------------------------------
        # the main unit to achieve the curve manipulate actions
        # ----------------------------------------------------------
        self.plottingBoardOperatingUnit = QSplitter(Qt.Horizontal, self)
        self.plottingBoardOperatingUnit.setOpaqueResize(True)
        self.plottingBoardOperatingUnit.setHandleWidth(1)

        # plotting area
        self.plotting = Plotting(self)
        self.plotting.set_color_list(self.colorList)
        self.plotting.set_marker_list(self.markerList)

        self.plotParametersManipulation = PlottingParametersManipulation(self)
        self.plotParametersManipulation.set_color_list(self.colorList)
        self.plotParametersManipulation.set_marker_list(self.markerList)
        # curves manipulation area
        self.plottingBoardOperatingUnit.addWidget(self.plotting)
        self.plottingBoardOperatingUnit.addWidget(self.plotParametersManipulation)

        self.picker = QwtPlotPicker(
            QwtPlot.xBottom,
            QwtPlot.yLeft,
            QwtPicker.PointSelection | QwtPicker.DragSelection,
            QwtPlotPicker.CrossRubberBand,
            QwtPicker.ActiveOnly,
            self.plotting.canvas())
        self.picker.setRubberBandPen(QPen(QColor('gainsboro')))
        self.picker.setTrackerPen(QPen(QColor('darkSeaGreen')))

        """
        zoomer = QwtPlotZoomer(self.plotting.canvas())
        zoomer.setTrackerMode(QwtPicker.AlwaysOff)
        zoomer.setMousePattern(QwtEventPattern.MouseSelect1, Qt.RightButton, Qt.ControlModifier)
        zoomer.setMousePattern(QwtEventPattern.MouseSelect2, Qt.RightButton, Qt.ControlModifier)
        zoomer.setMousePattern(QwtEventPattern.MouseSelect3, Qt.RightButton)
        zoomer.setEnabled(True)
        """

        self.qwtPlotPanner = QwtPlotPanner(self.plotting.canvas())
        self.qwtPlotPanner.setAxisEnabled(QwtPlot.yLeft, True)
        self.qwtPlotPanner.setAxisEnabled(QwtPlot.yRight, False)
        self.qwtPlotPanner.setAxisEnabled(QwtPlot.xBottom, True)
        self.qwtPlotPanner.setAxisEnabled(QwtPlot.xTop, False)
        self.qwtPlotPanner.setMouseButton(Qt.RightButton)
        self.qwtPlotPanner.setEnabled(True)

        self.qwtPlotMagnifier = QwtPlotMagnifier(self.plotting.canvas())
        self.qwtPlotMagnifier.setAxisEnabled(QwtPlot.xBottom, False)
        self.qwtPlotMagnifier.setAxisEnabled(QwtPlot.yLeft, False)

        # ---------------------------------------------------------------------------------------------------------
        # the menu bar of the plotting board which include a number of buttons and a label to display the function
        # ---------------------------------------------------------------------------------------------------------
        self.plottingBoardMenuBar = QWidget()
        self.plottingBoardMenuBar.setFixedHeight(30)

        self.minimizeButton = QPushButton()
        self.minimizeButton.setFixedSize(QSize(19, 19))
        self.minimizeButton.setFlat(True)
        self.minimizeButton.setStyleSheet("border-image: url(:/minimize_canvas.png)")

        self.maximizeButton = QPushButton()
        self.maximizeButton.setFixedSize(QSize(19, 19))
        self.maximizeButton.setFlat(True)
        self.maximizeButton.setStyleSheet("border-image: url(:/maximize_canvas.png)")

        self.plottingBoardClose = QPushButton()
        self.plottingBoardClose.setFixedSize(QSize(19, 19))
        self.plottingBoardClose.setFlat(True)
        self.plottingBoardClose.setStyleSheet("border-image: url(:/plotting_board_close.png)")

        self.plotZoomingConfigurationButton = QPushButton("N")
        self.plotZoomingConfigurationButton.setFixedSize(QSize(19, 19))
        self.plotZoomingConfigurationButton.setFlat(True)
        self.plotZoomingConfigurationButton.setFont(QFont("Helvetica", 8, QFont.Bold, True))
        self.plotZoomingConfigurationButton.setStyleSheet("border-image:url(:/button_background.png); color: darkCyan")

        self.changeCanvasOperationModeButton = QPushButton("N")
        self.changeCanvasOperationModeButton.setFixedSize(QSize(19, 19))
        self.changeCanvasOperationModeButton.setFlat(True)
        self.changeCanvasOperationModeButton.setFont(QFont("Helvetica", 8, QFont.Bold, True))
        self.changeCanvasOperationModeButton.setStyleSheet("border-image:url(:/button_background.png); color: darkCyan")

        self.plottingConfigurationButton = QPushButton()
        self.plottingConfigurationButton.setFixedSize(QSize(19, 19))
        self.plottingConfigurationButton.setFlat(True)
        self.plottingConfigurationButton.setStyleSheet("border-image:url(:/plotting_config.png)")

        self.plottingCleanerButton = QPushButton()
        self.plottingCleanerButton.setFixedSize(QSize(19, 19))
        self.plottingCleanerButton.setFlat(True)
        self.plottingCleanerButton.setStyleSheet("border-image: url(:/clean_plotting_board.png)")

        self.saveButton = QPushButton()
        self.saveButton.setFixedSize(QSize(19, 19))
        self.saveButton.setFlat(True)
        self.saveButton.setStyleSheet("border-image: url(:/download.png)")

        self.functionLabel = QLabel()
        self.functionLabel.setFont(QFont("Helvetica", 8, QFont.AnyStyle, True))

        menu_bar_layout = QHBoxLayout(self.plottingBoardMenuBar)
        menu_bar_layout.addWidget(self.functionLabel)
        menu_bar_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding))
        menu_bar_layout.addWidget(self.saveButton)
        menu_bar_layout.addWidget(self.plottingCleanerButton)
        menu_bar_layout.addWidget(self.plottingConfigurationButton)
        menu_bar_layout.addWidget(self.changeCanvasOperationModeButton)
        menu_bar_layout.addWidget(self.plotZoomingConfigurationButton)
        menu_bar_layout.addWidget(self.plottingBoardClose)
        menu_bar_layout.addWidget(self.maximizeButton)
        menu_bar_layout.addWidget(self.minimizeButton)
        menu_bar_layout.setSpacing(0)
        menu_bar_layout.setMargin(0)

        # ---------------------------------------------------------------------------------------------------------
        # add all components in le plotting board Layout
        # ---------------------------------------------------------------------------------------------------------
        plotting_board_layout = QVBoxLayout(self)
        plotting_board_layout.addWidget(self.plottingBoardMenuBar)
        plotting_board_layout.addWidget(self.plottingBoardOperatingUnit)
        plotting_board_layout.setSpacing(0)
        plotting_board_layout.setMargin(0)

        # ---------------------------------------------------------------------------------------
        # signals and slots
        # ---------------------------------------------------------------------------------------
        self.canvas = ObjectEventService(self.plotting.canvas())
        self.connect(self.canvas, SIGNAL("MouseMove"), self.point_tracking_procedure)
        self.connect(self.canvas, SIGNAL("MouseClicked"), self.set_mouse_button_on_canvas_clicked)
        self.connect(self.canvas, SIGNAL("MouseReleased"), self.set_mouse_button_on_canvas_released)
        self.connect(self.canvas, SIGNAL("MouseLeaved"), self.close_point_tracking_window)
        self.connect(self.saveButton, SIGNAL('clicked()'), self.save_change_to_file)
        self.connect(self.minimizeButton, SIGNAL("clicked()"), self.minimize_the_curve)
        self.connect(self.plotZoomingConfigurationButton, SIGNAL("clicked()"), self.plot_zooming_configuration)
        self.connect(self.plottingCleanerButton, SIGNAL("clicked()"), self.clean_plotting_board_button_clicked)
        self.connect(self.changeCanvasOperationModeButton, SIGNAL("clicked()"), self.change_canvas_operation_mode)
        self.connect(self.plottingConfigurationButton, SIGNAL("clicked()"), self.plotting_configuration_button_clicked)

    def get_color_list(self):
        return self.colorList

    def get_marker_list(self):
        return self.markerList

    def set_digit_to_keep(self, digit):
        self.numberOfDigitToKeep = digit

    def get_parent(self):
        return self.page_widget_reference

    def get_plotting_index(self):
        return self.my_plotting_index

    def set_plotting_index(self, index):
        self.my_plotting_index = index

    def get_page_index(self):
        return self.my_page_index

    def set_page_index(self, index):
        self.my_page_index = index

    def get_plot_object(self):
        return self.plotting

    def get_plot_parameter_manipulation_object(self):
        return self.plotParametersManipulation

    def get_menu_bar_object(self):
        return self.plottingBoardMenuBar

    def set_analyser_mediator(self, analyser_controller):
        self.analyserMediator = analyser_controller
        self.plotting.set_analyser_mediator(self.analyserMediator)
        self.plotParametersManipulation.set_analyser_mediator(self.analyserMediator)
        self.plottingOption.set_analyser_mediator(self.analyserMediator)

    def get_canvas_operation_mode(self):
        return self.canvasOperationMode

    def change_canvas_operation_mode(self):
        """
            -- each time the manipulationModeButton clicked, the counter canvasOperationMode + 1,
               the value of the canvasOperationMode represent the three operation mode when mouse's pointer do something on the canvas

            0: nothing
            1: point tracking
            2: lom_edit
        """
        self.canvasOperationMode += 1

        if self.canvasOperationMode == 0:
            self.plotting.canvas().setCursor(Qt.ArrowCursor)
            self.changeCanvasOperationModeButton.setText("N")
        elif self.canvasOperationMode == 1:
            self.plotting.canvas().setCursor(Qt.CrossCursor)
            self.changeCanvasOperationModeButton.setText("T")
        elif self.canvasOperationMode == 2:
            self.plotting.canvas().setCursor(Qt.PointingHandCursor)
            self.changeCanvasOperationModeButton.setText("E")
        elif self.canvasOperationMode == 3:
            self.plotting.canvas().setCursor(Qt.ArrowCursor)
            self.changeCanvasOperationModeButton.setText("N")
            self.canvasOperationMode = 0

    def delete_the_ordinate_on_the_canvas(self, ordinate_name, filename):
        plotting_context = self.analyserMediator.get_a_plotting_context(self.my_plotting_index, self.my_page_index)
        plotting_context.delete_the_ordinate_in_plotting_context(ordinate_name, filename)
        curves_on_canvas = self.plotParametersManipulation.get_curves_validity_information()
        self.plotting.delete_a_curve_from_curve_center(ordinate_name, filename)

        if not self.plotting.ask_if_curve_from_lom_existed():
            if len(self.ordinate_list) != 0:
                if ordinate_name in self.ordinate_list:
                    self.ordinate_list.remove(ordinate_name)
                    del curves_on_canvas[filename][ordinate_name]
                    if len(curves_on_canvas[filename]) == 0:
                        del curves_on_canvas[filename]
            else:
                self.self_cleaning()
                return False
        else:
            if ordinate_name in self.ordinate_list:
                self.ordinate_list.remove(ordinate_name)
                del curves_on_canvas[filename][ordinate_name]
                if len(curves_on_canvas[filename]) == 0:
                    del curves_on_canvas[filename]

        # TODO
        ord = str(self.function).split('=')
        print ord[0], ordinate_name
        if ord[0].__contains__(ordinate_name):
            t = ord[0].translate(None, ' ')
            ords = t.split(',')
            new_ord = ''
            for i in ords:
                if i == ordinate_name:
                    continue
                else:
                    new_ord += i + ','
            new_ord = new_ord[:-1]

            if len(new_ord) != 0:
                self.function = new_ord + '=' + ord[1]
                self.functionLabel.clear()
                self.functionLabel.setText(self.function)
            else:
                self.functionLabel.clear()

        return True

    def delete_the_label_on_the_canvas(self, label_to_be_deleted, filename):
        plotting_context = self.analyserMediator.get_a_plotting_context(self.my_plotting_index, self.my_page_index)
        plotting_context.delete_the_label_in_plotting_context(label_to_be_deleted, filename)
        curves_on_canvas = self.plotParametersManipulation.get_curves_validity_information()

        self.plotting.delete_a_curve_from_curve_center(label_to_be_deleted, filename)

        if not self.plotting.ask_if_curve_from_csv_existed():
            if len(self.plotting.get_labels_drawn()) == 0:
                self.self_cleaning()
                return False
            else:
                del curves_on_canvas[filename][label_to_be_deleted]
                if len(curves_on_canvas[filename]) == 0:
                    del curves_on_canvas[filename]
        else:
            del curves_on_canvas[filename][label_to_be_deleted]
            if len(curves_on_canvas[filename]) == 0:
                del curves_on_canvas[filename]

        return True


    def set_label_to_be_modified(self, label_name, filename):
        """
            -- when canvas operation mode is in 2 : lom edit mode,
               user can set the label which he want to make some changes via right click the label from the tree list widget at the right side of the plotting board

        :param label_name:
        :param filename:
        """
        self.labelToBeModified = (label_name, filename)

    def set_mouse_button_on_canvas_clicked(self):
        """
            -- when the mouse's left button has been clicked and at the same time, the canvas operation mode is in lom_edit mode
               firstly set the mouse's left click state to true
               then, call the point search method to try to find a point existing from a curve on the canvas
        """
        if self.canvasOperationMode == 2:
            self.mouseButtonOnCanvasClicked = True
            self.point_search()

    def point_search(self):
        """
            -- the pointToBeModified will be assigned only if the mouse's current position find just one point from a curve on the canvas
        """
        results = self.target_point_search(self.abscissa_point, self.ordinate_point)

        if results is not None:
            if len(results) == 1:
                self.pointToBeModified = results[0]

    def target_point_search(self, abscissa_point, ordinate_point):
        """
            -- if the label to be modified has been configured, trying to search for a point which is nearest to the mouse's pointer
        :param abscissa_point:
        :param ordinate_point:
        """
        results = []

        if len(self.labelToBeModified) != 2:
            return

        plotting_context = self.analyserMediator.get_a_plotting_context(self.my_page_index, self.my_plotting_index)
        data_center = plotting_context.get_data_center()
        label = data_center[self.labelToBeModified[1]][self.labelToBeModified[0]]
        dim = label['dimension']

        if dim == 1:
            abscissa_values = label['abscissa'][1]
            ordinate_values = label['ordinate'][1]
            radius_x = self.calculate_radius_reference(abscissa_values)
            if (radius_x < self.radius_x) and (radius_x != 0):
                self.radius_x = radius_x
            radius_y = self.calculate_radius_reference(ordinate_values)
            if (radius_y < self.radius_y) and (radius_y != 0):
                self.radius_y = radius_y

            while True:
                v = self.locked_into_target_point(ordinate_values, abscissa_values, abscissa_point, ordinate_point)
                if v[0] == 1:
                    result = (v[1], abscissa_values[v[1]], ordinate_values[v[1]])
                    results.append(result)
                    break
                elif v[0] > 1:
                    self.radius_x /= 2
                    self.radius_y /= 2
                else:
                    break

        elif dim == 2:
            abscissa_values = label['abscissa'][1]
            list_of_ordinate_values = label['ordinate'][1]
            iso_validity = label['iso'][2]

            radius_x = self.calculate_radius_reference(abscissa_values)
            if (radius_x < self.radius_x) and (radius_x != 0):
                self.radius_x = radius_x
            radius_y = self.calculate_radius_reference(list_of_ordinate_values[0])
            if (radius_y < self.radius_y) and (radius_y != 0):
                self.radius_y = radius_y

            cpt_iso = 0
            for i in range(len(list_of_ordinate_values)):
                point = ''
                ordinate_values = list_of_ordinate_values[i]
                while True:
                    v = self.locked_into_target_point(ordinate_values, abscissa_values, abscissa_point, ordinate_point)
                    if v[0] == 1:
                        if iso_validity[cpt_iso]:
                            result = (v[1], abscissa_values[v[1]], ordinate_values[v[1]], i)
                            results.append(result)
                        break
                    elif v[0] > 1:
                        self.radius_x /= 2
                        self.radius_y /= 2
                    else:
                        break
                cpt_iso += 1

        elif dim == 3:
            abscissa_values = label['abscissa'][1]
            list_of_ordinate_values = label['ordinate'][1]
            iso_values = label['iso'][1]
            iso_validity = label['iso'][2]
            siso_values = label['siso'][1]
            siso_validity = label['siso'][2]

            radius_x = self.calculate_radius_reference(abscissa_values)
            if (radius_x < self.radius_x) and (radius_x != 0):
                self.radius_x = radius_x
            radius_y = self.calculate_radius_reference(list_of_ordinate_values[0][0])
            if (radius_y < self.radius_y) and (radius_y != 0):
                self.radius_y = radius_y

            for i in range(len(siso_values)):
                for j in range(len(iso_values)):
                    point = ''
                    ordinate_values = list_of_ordinate_values[i][j]
                    while True:
                        v = self.locked_into_target_point(ordinate_values, abscissa_values, abscissa_point, ordinate_point)

                        if v[0] == 1:
                            if siso_validity[i]:
                                if iso_validity[j]:
                                    result = (v[1], abscissa_values[v[1]], ordinate_values[v[1]], j, i)
                                    results.append(result)
                            break
                        elif v[0] > 1:
                            self.radius_x /= 2
                            self.radius_y /= 2
                        else:
                            break
        return results

    @staticmethod
    def calculate_radius_reference(values):
        radius_reference = 0

        for i in range(len(values) - 1):
            r = (float(values[i + 1]) - float(values[i])) / 8
            if i == 0:
                radius_reference = r
            elif r < radius_reference:
                radius_reference = r

        return abs(radius_reference)

    def locked_into_target_point(self, ordinate_values, abscissa_values, abscissa_point, ordinate_point):
        cpt = 0
        index = -1
        for j in range(len(ordinate_values)):
            ordinate_v = float(ordinate_values[j])
            abscissa_v = float(abscissa_values[j])
            if (abscissa_point - self.radius_x < abscissa_v < abscissa_point + self.radius_x) and (ordinate_point - self.radius_y < ordinate_v < ordinate_point + self.radius_y):
                cpt += 1
                index = j
        return [cpt, index]

    def set_mouse_button_on_canvas_released(self):
        if self.canvasOperationMode == 2:
            self.mouseButtonOnCanvasClicked = False

    def minimize_the_curve(self):
        self.hide()
        self.page_widget_reference.minimize_curve_operation_board_at(self.my_plotting_index)

    def display_the_curve(self):
        self.show()

    def remove_an_element_in_ordinate_list(self, ordinate):
        if ordinate in self.ordinate_list:
            self.ordinate_list.remove(ordinate)

    def set_function_title(self, ordinates, abscissa, iso, siso):
        y_string = ""
        if (ordinates is not None) and (len(abscissa) != 0):
            self.abscissa = abscissa
            for ordinate in ordinates:
                if ordinate not in self.ordinate_list:
                    self.ordinate_list.append(ordinate)

        for i in self.ordinate_list:
            y_string += i + ", "
        y_string = y_string[:-1]
        y_string = y_string[:-1]

        if len(iso) != 0:
            self.iso = iso

        if len(siso) != 0:
            self.siso = siso

        if (len(self.iso) != 0) and (len(self.siso) != 0):
            self.function = y_string + "= f(" + self.abscissa + ", " + self.iso + ", " + self.siso + ")"
        elif (len(self.iso) != 0) and (len(self.siso) == 0):
            self.function = y_string + "= f(" + self.abscissa + ", " + self.iso + ")"
        else:
            self.function = y_string + "= f(" + self.abscissa + ")"

        self.functionLabel.setText(self.function)

    def get_function_title(self):
        return self.functionLabel.text()

    def save_change_to_file(self):
        # save current lom file in the memory as a file in the workspace
        if len(self.labelToBeModified) == 0:
            return

        reply = QMessageBox()
        reply.setText('Do you confirm the modification of the label:' + self.labelToBeModified[0] + ' in the file:' + self.labelToBeModified[1])
        yes = reply.addButton(str("yes"), QMessageBox.ActionRole)
        yes.setFlat(True)
        cancel = reply.addButton(str("abandon"), QMessageBox.ActionRole)
        cancel.setFlat(True)
        reply.setFont(QFont("Helvetica", 9, QFont.AnyStyle, True))
        reply.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        reply.setStyleSheet("background-color: skyBlue; color: AliceBlue")
        reply.exec_()

        if reply.clickedButton() == cancel:
            return
        elif reply.clickedButton() == yes:
            current_file = self.analyserMediator.get_lom_file_in_context_by_name(self.labelToBeModified[1])
            labels = current_file.get_labels()
            # path = str(self.analyserMediator.get_calibrated_files_path_from_context() + 'Calibrated_' + self.labelToBeModified[1])
            # labels.write('*', path, fmt='generic',  valuetype='double')

            resource_filepath_list = self.analyserMediator.get_path_list_to_global_context()
            for p in resource_filepath_list:
                if str(p).__contains__(str(self.labelToBeModified[1])):
                    labels.write('*', p, fmt='generic', valuetype='double')

    def plot_zooming_configuration(self):
        self.zoomingState += 1

        if self.zoomingState == 0:
            self.qwtPlotMagnifier.setAxisEnabled(QwtPlot.xBottom, False)
            self.qwtPlotMagnifier.setAxisEnabled(QwtPlot.yLeft, False)
            self.plotZoomingConfigurationButton.setText("N")
        elif self.zoomingState == 1:
            self.qwtPlotMagnifier.setAxisEnabled(QwtPlot.xBottom, True)
            self.qwtPlotMagnifier.setAxisEnabled(QwtPlot.yLeft, False)
            self.plotZoomingConfigurationButton.setText("H")
        elif self.zoomingState == 2:
            self.qwtPlotMagnifier.setAxisEnabled(QwtPlot.xBottom, False)
            self.qwtPlotMagnifier.setAxisEnabled(QwtPlot.yLeft, True)
            self.plotZoomingConfigurationButton.setText("V")
        elif self.zoomingState == 3:
            self.qwtPlotMagnifier.setAxisEnabled(QwtPlot.xBottom, True)
            self.qwtPlotMagnifier.setAxisEnabled(QwtPlot.yLeft, True)
            self.plotZoomingConfigurationButton.setText("HV")
            self.zoomingState = -1

    def clean_plotting_board_button_clicked(self):
        """the method is to remove all the curves information in the front plotting board and in the background"""

        # a choice box to ask the user to confirm or cancel the clean action
        confirm_to_clean_box = QMessageBox()
        confirm_to_clean_box.setFont(QFont("Helvetica", 8, QFont.AnyStyle, True))
        confirm_to_clean_box.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        confirm_to_clean_box.setText("Do you really want to remove all the information in the plotting board")
        confirm_choice = confirm_to_clean_box.addButton(str("confirm"), QMessageBox.ActionRole)
        confirm_choice.setFixedSize(60, 25)
        confirm_choice.setFlat(1)
        cancel_choice = confirm_to_clean_box.addButton("cancel", QMessageBox.RejectRole)
        cancel_choice.setFixedSize(50, 25)
        cancel_choice.setFlat(1)
        confirm_to_clean_box.setStyleSheet("background-color: skyBlue; color: AliceBlue")
        confirm_to_clean_box.exec_()

        # If the choice is to apply the parameter's information to the abscissa axis
        if confirm_to_clean_box.clickedButton() == confirm_choice:
            self.self_cleaning()
        if confirm_to_clean_box.clickedButton() == cancel_choice:
            return

    def self_cleaning(self):
        self.plotting.clean_all_information()
        plotting_context = self.analyserMediator.get_a_plotting_context(self.my_page_index, self.my_plotting_index)
        plotting_context.reinitialize()
        self.plotParametersManipulation.clean_all_component(True)
        self.functionLabel.clear()
        self.function = ''
        del self.ordinate_list[:]

    def plotting_configuration_button_clicked(self):
        self.plottingOption.display(QCursor.pos())

    def get_plotting_option_reference(self):
        return self.plottingOption

    def clear_extra_parameter_list_to_be_displayed(self):
        del self.extraParameterTobeDisplayed[:]
        self.extraValues.clear()

    def set_extra_parameter_list_to_be_displayed(self, extra_parameter_list):
        self.extraParameterTobeDisplayed = extra_parameter_list

        # Fetch the list of the loaded csv file's names
        loaded_csvfiles = self.analyserMediator.get_loaded_csv_files_from_context(self.my_page_index, self.my_plotting_index)

        for csvfile in loaded_csvfiles:
            if csvfile not in self.extraValues.keys():
                self.extraValues[csvfile] = {}

            current_file = self.analyserMediator.get_csv_file_in_context_by_name(csvfile)
            values = current_file.get_values()
            list_of_titles = current_file.get_title_list()
            rowcount = current_file.get_row_count()
            for parameter_name in self.extraParameterTobeDisplayed:
                if (parameter_name in list_of_titles) or (parameter_name == ""):
                    if parameter_name not in self.extraValues[csvfile].keys():
                        self.extraValues[csvfile][parameter_name] = []
                    else:
                        continue
                    try:
                        value_pointer = list_of_titles.index(parameter_name)

                        if parameter_name == 'GMT':
                            for k in range(rowcount):
                                self.extraValues[csvfile][parameter_name].append(k)
                        else:
                            for k in range(rowcount):
                                self.extraValues[csvfile][parameter_name].append(values[k][value_pointer])
                    except ValueError:
                        print "not existed"

    def verify_parameter(self, parameter_name):
        plotting_context = self.analyserMediator.get_a_plotting_context(self.my_page_index, self.my_plotting_index)
        data_center = plotting_context.get_data_center()

        for filename in data_center.keys():
            if filename.__contains__('csv'):
                csvfile = data_center[filename]

                abscissa_name = csvfile['abscissa'][0]
                if parameter_name == abscissa_name:
                    return False

                list_of_ordinate_names = csvfile['ordinate'][0]
                if parameter_name in list_of_ordinate_names:
                    return False

                iso_name = csvfile['iso'][0]
                if parameter_name == iso_name:
                    return False

                siso_name = csvfile['siso'][0]
                if siso_name == parameter_name:
                    return False

        return True

    def close_point_tracking_window(self):
        self.plottingPointDisplay.close()

    def point_tracking_procedure(self, position):
        """Three mode of operation when the mouse pointer is just upon the area of the canvas
        0: when the mouse pointer is on the canvas, nothing to do
        1: when the mouse pointer is on the canvas and is also very close to a point, displaying all the information related to the the point
        2: when the mouse pointer is on the canvas and is also very close to a point, lom_edit .........(to be enriched here)
        :param position: the position to positioning the point display widget
        """
        if self.canvasOperationMode == 0:
            return
        else:
            # get the current mouse pointer's coordinate information -- (x, y)
            abscissa_point = self.plotting.invTransform(Qwt.QwtPlot.xBottom, position.x())
            ordinate_point = self.plotting.invTransform(Qwt.QwtPlot.yLeft, position.y())

            # tracking and displaying mode
            if self.canvasOperationMode == 1:
                # get all the data from the context of this plotting board
                plotting_context = self.analyserMediator.get_a_plotting_context(self.my_page_index, self.my_plotting_index)
                data_center = plotting_context.get_data_center()

                curves_on_canvas = self.plotParametersManipulation.get_curves_validity_information()

                # a string to store all the points which is within the tracking area
                information_parameter = ''
                information_value = ''

                # parse all the files loaded in the data center
                for filename in data_center.keys():
                    point_parameter_information = ''
                    if filename.__contains__('csv'):

                        csvfile_values = data_center[filename]

                        abscissa_name = csvfile_values['abscissa'][0]
                        abscissa_values = csvfile_values['abscissa'][1]

                        list_of_ordinate_names = csvfile_values['ordinate'][0]
                        list_of_ordinate_values = csvfile_values['ordinate'][1]

                        iso_name = csvfile_values['iso'][0]
                        iso_values = csvfile_values['iso'][1]

                        sub_lists_of_iso_index = csvfile_values['iso_cut'][0]
                        sub_lists_of_siso_index = csvfile_values['siso_cut'][0]

                        siso_name = csvfile_values['siso'][0]
                        siso_values = csvfile_values['siso'][1]

                        radius_x = self.calculate_radius_reference(abscissa_values)
                        if (radius_x < self.radius_x) and (radius_x != 0):
                            self.radius_x = radius_x

                        if len(list_of_ordinate_values) > 0:
                            radius_y = self.calculate_radius_reference(list_of_ordinate_values[0])
                            if (radius_y < self.radius_y) and (radius_y != 0):
                                self.radius_y = radius_y
                        else:
                            return

                        """
                        if self.radius_x > self.radius_y:
                            self.radius_x = self.radius_y
                        else:
                            self.radius_y = self.radius_x
                        """

                        # parse all ordinate value lists
                        for i in range(len(list_of_ordinate_values)):
                            if curves_on_canvas[filename][list_of_ordinate_names[i]] == 0:
                                continue
                            ordinate_values = list_of_ordinate_values[i]
                            while True:
                                v = self.locked_into_target_point(ordinate_values, abscissa_values, abscissa_point, ordinate_point)
                                if v[0] == 1:
                                    if siso_name != "":
                                        if iso_name != "":
                                            flag = False
                                            for l in sub_lists_of_siso_index:
                                                if v[1] in l:
                                                    flag = True
                                                    break

                                            if flag:

                                                point_parameter_information = abscissa_name + ':\n' \
                                                                              + str(list_of_ordinate_names[i]) + ':\n' \
                                                                              + iso_name + ':\n' \
                                                                              + siso_name + ':'

                                                point_value_information = str(abscissa_values[v[1]]) + '\n' \
                                                                          + str(ordinate_values[v[1]]) + '\n' \
                                                                          + str(iso_values[v[1]]) + '\n' \
                                                                          + str(siso_values[v[1]])

                                                for param in self.extraParameterTobeDisplayed:
                                                    point_parameter_information += '\n' + param + ':'
                                                    point_value_information += '\n' + self.extraValues[filename][param][v[1]]

                                    else:
                                        if iso_name != "":
                                            flag = False
                                            for l in sub_lists_of_iso_index:
                                                if v[1] in l:
                                                    flag = True
                                                    break
                                            if flag:

                                                point_parameter_information = abscissa_name + ':\n' \
                                                                              + str(list_of_ordinate_names[i]) + ':\n' \
                                                                              + iso_name

                                                point_value_information = str(abscissa_values[v[1]]) + '\n' \
                                                                          + str(ordinate_values[v[1]]) + '\n' \
                                                                          + str(iso_values[v[1]])

                                                for param in self.extraParameterTobeDisplayed:
                                                    point_parameter_information += '\n' + param + ':'
                                                    point_value_information += '\n' + self.extraValues[filename][param][v[1]]

                                        else:
                                            point_parameter_information = abscissa_name + ':\n' + str(list_of_ordinate_names[i])

                                            point_value_information = str(abscissa_values[v[1]]) + '\n' + str(ordinate_values[v[1]])

                                            for param in self.extraParameterTobeDisplayed:
                                                point_parameter_information += '\n' + param + ':'
                                                point_value_information += '\n' + self.extraValues[filename][param][v[1]]

                                    break
                                elif v[0] > 1:
                                    self.radius_x /= 2
                                    self.radius_y /= 2
                                else:
                                    break

                    elif filename.__contains__('gen'):
                        lomfile = data_center[filename]

                        for label_name in lomfile.keys():
                            if curves_on_canvas[filename][label_name] == 0:
                                continue
                            label = data_center[filename][label_name]
                            dim = label['dimension']

                            if dim == 1:
                                abscissa_name = label['abscissa'][0]
                                abscissa_values = label['abscissa'][1]
                                ordinate_name = label['ordinate'][0]
                                ordinate_values = label['ordinate'][1]
                                radius_x = self.calculate_radius_reference(abscissa_values)
                                if (radius_x < self.radius_x) and (radius_x != 0):
                                    self.radius_x = radius_x
                                radius_y = self.calculate_radius_reference(ordinate_values)
                                if (radius_y < self.radius_y) and (radius_y != 0):
                                    self.radius_y = radius_y

                                """
                                if self.radius_x > self.radius_y:
                                    self.radius_x = self.radius_y
                                else:
                                    self.radius_y = self.radius_x
                                """

                                while True:
                                    v = self.locked_into_target_point(ordinate_values, abscissa_values, abscissa_point, ordinate_point)
                                    if v[0] == 1:
                                        point_parameter_information = abscissa_name + ':\n' \
                                                                      + str(ordinate_name)

                                        point_value_information = str(abscissa_values[v[1]]) + '\n' \
                                                                  + str(ordinate_values[v[1]])
                                        break
                                    elif v[0] > 1:
                                        self.radius_x /= 2
                                        self.radius_y /= 2
                                    else:
                                        break

                            elif dim == 2:
                                abscissa_name = label['abscissa'][0]
                                abscissa_values = label['abscissa'][1]
                                list_of_ordinate_values = label['ordinate'][1]
                                iso_name = label['iso'][0]
                                iso_values = label['iso'][1]
                                iso_validity = label['iso'][2]

                                radius_x = self.calculate_radius_reference(abscissa_values)
                                if (radius_x < self.radius_x) and (radius_x != 0):
                                    self.radius_x = radius_x
                                radius_y = self.calculate_radius_reference(list_of_ordinate_values[0])
                                if (radius_y < self.radius_y) and (radius_y != 0):
                                    self.radius_y = radius_y

                                """
                                if self.radius_x > self.radius_y:
                                    self.radius_x = self.radius_y
                                else:
                                    self.radius_y = self.radius_x
                                """

                                for i in range(len(list_of_ordinate_values)):
                                    point = ''
                                    ordinate_values = list_of_ordinate_values[i]
                                    while True:
                                        v = self.locked_into_target_point(ordinate_values, abscissa_values, abscissa_point, ordinate_point)
                                        if v[0] == 1:
                                            if iso_validity[i]:
                                                point_parameter_information = abscissa_name + ':\n' \
                                                                              + label_name + ':\n' \
                                                                              + iso_name

                                                point_value_information = str(abscissa_values[v[1]]) + '\n' \
                                                                          + str(ordinate_values[v[1]]) + '\n' \
                                                                          + str(iso_values[i])

                                            break
                                        elif v[0] > 1:
                                            self.radius_x /= 2
                                            self.radius_y /= 2
                                        else:
                                            break

                                    if point == '':
                                        continue
                                    else:
                                        point_parameter_information = point
                                        break

                            elif dim == 3:
                                abscissa_name = label['abscissa'][0]
                                abscissa_values = label['abscissa'][1]
                                list_of_ordinate_values = label['ordinate'][1]
                                iso_name = label['iso'][0]
                                iso_values = label['iso'][1]
                                iso_validity = label['iso'][2]
                                siso_name = label['siso'][0]
                                siso_values = label['siso'][1]
                                siso_validity = label['siso'][2]

                                radius_x = self.calculate_radius_reference(abscissa_values)
                                if (radius_x < self.radius_x) and (radius_x != 0):
                                    self.radius_x = radius_x
                                radius_y = self.calculate_radius_reference(list_of_ordinate_values[0][0])
                                if (radius_y < self.radius_y) and (radius_y != 0):
                                    self.radius_y = radius_y
                                """
                                if self.radius_x > self.radius_y:
                                    self.radius_x = self.radius_y
                                else:
                                    self.radius_y = self.radius_x
                                """
                                for i in range(len(siso_values)):
                                    for j in range(len(iso_values)):
                                        point = ''
                                        ordinate_values = list_of_ordinate_values[i][j]
                                        while True:
                                            v = self.locked_into_target_point(ordinate_values, abscissa_values, abscissa_point, ordinate_point)
                                            if v[0] == 1:
                                                if siso_validity[i]:
                                                    if iso_validity[j]:
                                                        point_parameter_information = abscissa_name + ':\n' \
                                                                                      + label_name + ':\n' \
                                                                                      + iso_name + ':\n' \
                                                                                      + siso_name + ':'

                                                        point_value_information = str(abscissa_values[v[1]]) + '\n' \
                                                                                  + str(ordinate_values[v[1]]) + '\n' \
                                                                                  + str(iso_values[j]) + '\n' \
                                                                                  + str(siso_values[i])
                                                break
                                            elif v[0] > 1:
                                                self.radius_x /= 2
                                                self.radius_y /= 2
                                            else:
                                                break
                                        if point == '':
                                            continue
                                        else:
                                            point_parameter_information = point
                                            break

                    if point_parameter_information == '':
                        continue
                    else:
                        information_parameter += point_parameter_information
                        information_value += point_value_information
                        break

                self.plottingPointDisplay.set_point_information(information_parameter, information_value)

                if information_parameter != '':
                    self.plottingPointDisplay.display(QCursor.pos())
                else:
                    self.plottingPointDisplay.close()

            # mode : modify the label in lom file
            elif self.canvasOperationMode == 2:

                # determine if the label to be modified has been assigned. '2' means (filename, label_name)
                if len(self.labelToBeModified) != 2:
                    return

                self.abscissa_point = abscissa_point
                self.ordinate_point = ordinate_point

                # determine if the point on the canvas has been found after the mouse's left button clicked event
                if len(self.pointToBeModified) == 0:
                    return

                # get the ordinate values from the the label to be modified in the plotting context
                plotting_context = self.analyserMediator.get_a_plotting_context(self.my_page_index, self.my_plotting_index)
                data_center = plotting_context.get_data_center()
                label = data_center[self.labelToBeModified[1]][self.labelToBeModified[0]]
                dim = label['dimension']
                list_of_ordinate_values = label['ordinate'][1]

                # if the mouse's left button has been clicked
                if self.mouseButtonOnCanvasClicked:
                    # self.ordinate_point to be used

                    # modify the point's ordinate values in the right index
                    if dim == 3:
                        list_of_ordinate_values[self.pointToBeModified[4]][self.pointToBeModified[3]][self.pointToBeModified[0]] = ordinate_point
                    elif dim == 2:
                        list_of_ordinate_values[self.pointToBeModified[3]][self.pointToBeModified[0]] = ordinate_point
                    elif dim == 1:
                        list_of_ordinate_values[self.pointToBeModified[0]] = ordinate_point
                    else:
                        return

                    self.plotting.refresh_curves_on_canvas()
                    """

                    if self.plotting.ask_if_curve_from_csv_existed():
                        if dim == 3:
                            self.plotParametersManipulation.siso_range_check_list_changed()
                        elif dim == 2:
                            self.plotParametersManipulation.iso_range_check_list_changed()
                        elif dim == 1:
                            self.plotParametersManipulation.update_canvas()

                    else:
                        # update curves on the canvas
                        self.plotting.clean_before_replot()
                        self.plotting.replot_current_lom_curves()
                    """
                else:

                    new_ordinate_values = np.array(label['ordinate'][1])
                    ordinate_point = round(ordinate_point, self.numberOfDigitToKeep)
                    current_file = self.analyserMediator.get_lom_file_in_context_by_name(self.labelToBeModified[1])
                    labels = current_file.get_labels()

                    if dim == 3:
                        iso_values = label['iso'][1]
                        siso_values = label['siso'][1]
                        labels.setval3(self.labelToBeModified[0], label['abscissa'][1][self.pointToBeModified[0]], iso_values[self.pointToBeModified[3]], siso_values[self.pointToBeModified[4]],
                                       ordinate_point)

                    elif dim == 2:
                        iso_values = label['iso'][1]
                        labels.setval2(self.labelToBeModified[0], label['abscissa'][1][self.pointToBeModified[0]], iso_values[self.pointToBeModified[3]], ordinate_point)

                    elif dim == 1:
                        labels.setval1(self.labelToBeModified[0], label['abscissa'][1][self.pointToBeModified[0]], ordinate_point)

                    else:
                        return

                    # reinitialize the global variable 'pointToBeModified'
                    self.pointToBeModified = ()

