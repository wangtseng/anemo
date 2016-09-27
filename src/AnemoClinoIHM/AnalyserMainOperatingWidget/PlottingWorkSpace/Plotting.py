"""
Last updated on 07/01/2015

@author: Cheng WANG,
"""
import threading

import numpy as np  # Numpy functions for image creation
import PyQt4.Qwt5 as Qwt
from PyQt4.Qwt5.qplt import *


# noinspection PyTypeChecker,PyCallByClass,PyArgumentList
class Plotting(Qwt.QwtPlot):
    """
    This class represent a plot area who wil react the actions just like: plotting action, cutting action, tracking action and dropping action.
    """

    def __init__(self, plotting_board_reference=None):
        super(Plotting, self).__init__()

        # -----------------------------------------------------------------------------------------------
        # embellishing the canvas
        # -----------------------------------------------------------------------------------------------
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.setAcceptDrops(True)
        self.setMargin(4)
        self.plotLayout().setAlignCanvasToScales(True)
        self.plotLayout().setCanvasMargin(0)
        self.canvas().setFrameStyle(QFrame.StyledPanel)
        self.canvas().setLineWidth(1)
        self.canvas().setCursor(Qt.ArrowCursor)

        for i in range(0, QwtPlot.axisCnt):
            scale_widget = self.axisWidget(i)
            if scale_widget:
                scale_widget.setMargin(0)
            scale_draw = self.axisScaleDraw(i)
            if scale_draw:
                scale_draw.enableComponent(Qwt.QwtAbstractScaleDraw.Backbone, False)
                self.setAutoFillBackground(True)

        self.grid = QwtPlotGrid()
        self.grid.enableY(False)
        self.grid.enableX(False)
        self.grid.enableXMin(False)
        self.grid.enableYMin(False)
        self.grid.setMajPen(QPen(QColor('lightGray'), 0, Qt.SolidLine))
        self.grid.setMinPen(QPen(QColor('lightGray'), 0, Qt.SolidLine))
        self.grid.attach(self)

        # -----------------------------------------------------------------------------------------------
        # initialize attributes
        # -----------------------------------------------------------------------------------------------
        self.abscissa_name = ""
        self.sisoConfig = "represent_by_color"
        self.dimensionAdoptable = 0
        self.font = QFont("Helvetica", 8, QFont.AnyStyle, True)

        self.analyseurMediator = None
        self.plottingBoardReference = plotting_board_reference

        self.isoExisted = False
        self.sisoExisted = False
        self.curve_gradient_using = False
        self.curve_from_csv_existed = False
        self.curve_from_lom_existed = False
        self.labelSuperposeActionActivated = False

        # the dictionary to save all the curves on the canvas
        self.curves_center = {'csv': {}, 'lom': {}}

        # list to store the label which has been drawn on the plotting board
        self.labelsDrawn = []

        # linear_gradient_color_list
        self.linear_gradient_color_list = list()

        # main curve color
        self.mainCurveColorList = [QPen(QColor("red")),
                                   QPen(QColor("blue")),
                                   QPen(QColor("black")),
                                   QPen(QColor("orange")),
                                   QPen(QColor("magenta")),
                                   QPen(QColor("brown")),
                                   QPen(QColor("DeepPink")),
                                   QPen(QColor("green")),
                                   QPen(QColor("OrangeRed")),
                                   QPen(QColor("VioletRed"))]

        self.mainCurveColorNumber = len(self.mainCurveColorList)

        self.markerList = list()
        self.colorList = list()

        self.markerNumberForCutting = 0

        # separate the size of symbol og the curves from lom et csv
        self.markerSize = QSize(8, 8)

    def set_color_list(self, l):
        self.colorList = l

    def set_marker_list(self, l):
        self.markerList = l
        self.markerNumberForCutting = len(self.colorList)

    def set_curve_property(self, curve, i):
        curve.setPen(self.mainCurveColorList[i % self.mainCurveColorNumber])
        curve.setStyle(QwtPlotCurve.Lines)
        curve.setCurveAttribute(QwtPlotCurve.Fitted)
        curve.setRenderHint(QwtPlotItem.RenderAntialiased)

    def set_curve_gradient(self, curve, marker, length, start_color, finish_color):
        del self.linear_gradient_color_list[:]
        if (start_color == "red") and (finish_color == "yellow"):
            curve.setSymbol(QwtSymbol(self.markerList[marker % self.markerNumberForCutting][1],
                                      QBrush(QColor(255, int(float(marker) * 255 / length), 0, 255)),
                                      QPen(QColor(255, int(float(marker) * 255 / length), 0, 255)),
                                      self.markerSize))
            self.linear_gradient_color_list.append(QColor(255, int(float(marker) * 255 / length), 0, 255))
        if (start_color == "green") and (finish_color == "yellow"):
            curve.setSymbol(QwtSymbol(self.markerList[marker % self.markerNumberForCutting][1],
                                      QBrush(QColor(int(float(marker) * 255 / length), 255, 0, 255)),
                                      QPen(QColor(int(float(marker) * 255 / length), 255, 0, 255)),
                                      self.markerSize))
            self.linear_gradient_color_list.append(QColor(int(float(marker) * 255 / length), 255, 0, 255))
        if (start_color == "blue") and (finish_color == "cyan"):
            curve.setSymbol(QwtSymbol(self.markerList[marker % self.markerNumberForCutting][1],
                                      QBrush(QColor(0, int(float(marker) * 255 / length), 255, 255)),
                                      QPen(QColor(0, int(float(marker) * 255 / length), 255, 255)),
                                      self.markerSize))
            self.linear_gradient_color_list.append(QColor(0, int(float(marker) * 255 / length), 255, 255))

        curve.setStyle(QwtPlotCurve.NoCurve)

    def set_lom_curve_property_by_color_marker(self, curve, marker):
        curve.setPen(QPen(QColor(self.colorList[marker % self.markerNumberForCutting])))
        curve.setRenderHint(QwtPlotItem.RenderAntialiased)

        curve.setSymbol(QwtSymbol(self.markerList[marker % self.markerNumberForCutting][1],
                                  QBrush(QColor(self.colorList[marker % self.markerNumberForCutting])),
                                  QPen(QColor(self.colorList[marker % self.markerNumberForCutting])),
                                  self.markerSize))

        curve.setStyle(QwtPlotCurve.Lines)

    def set_curve_property_by_color_marker(self, curve, marker):
        curve.setSymbol(QwtSymbol(self.markerList[marker % self.markerNumberForCutting][1],
                                  QBrush(QColor(self.colorList[marker % self.markerNumberForCutting])),
                                  QPen(QColor(self.colorList[marker % self.markerNumberForCutting])),
                                  self.markerSize))

        curve.setStyle(QwtPlotCurve.NoCurve)

    def set_curve_property_by_color(self, curve, marker, color):
        curve.setSymbol(QwtSymbol(self.markerList[marker % self.markerNumberForCutting][1],
                                  QBrush(QColor(self.colorList[color % self.markerNumberForCutting])),
                                  QPen(QColor(self.colorList[color % self.markerNumberForCutting])),
                                  self.markerSize))

        curve.setStyle(QwtPlotCurve.NoCurve)

    def set_curve_property_by_marker(self, curve, color, marker):
        curve.setSymbol(QwtSymbol(self.markerList[marker % self.markerNumberForCutting][1],
                                  QBrush(QColor(self.colorList[color % self.markerNumberForCutting])),
                                  QPen(QColor(self.colorList[color % self.markerNumberForCutting])),
                                  self.markerSize))

        curve.setStyle(QwtPlotCurve.NoCurve)

    def set_lom_curve_property_by_marker(self, curve, color, marker):
        curve.setPen(QPen(QColor(self.colorList[marker % self.markerNumberForCutting])))
        curve.setRenderHint(QwtPlotItem.RenderAntialiased)
        curve.setSymbol(QwtSymbol(self.markerList[color % self.markerNumberForCutting][1],
                                  QBrush(QColor(self.colorList[marker % self.markerNumberForCutting])),
                                  QPen(QColor(self.colorList[marker % self.markerNumberForCutting])),
                                  self.markerSize))

        curve.setStyle(QwtPlotCurve.Lines)

    def set_lom_curve_property_by_color(self, curve, color, marker):
        curve.setPen(QPen(QColor(self.colorList[color % self.markerNumberForCutting])))
        curve.setRenderHint(QwtPlotItem.RenderAntialiased)
        curve.setSymbol(QwtSymbol(self.markerList[marker % self.markerNumberForCutting][1],
                                  QBrush(QColor(self.colorList[color % self.markerNumberForCutting])),
                                  QPen(QColor(self.colorList[color % self.markerNumberForCutting])),
                                  self.markerSize))

        curve.setStyle(QwtPlotCurve.Lines)

    def delete_a_curve_from_curve_center(self, label_to_be_deleted, filename):
        if str(filename).__contains__('gen'):
            del self.curves_center['lom'][filename][label_to_be_deleted]
            i = self.labelsDrawn.index((label_to_be_deleted, filename))
            del self.labelsDrawn[i]

            if len(self.labelsDrawn) == 0:
                self.dimensionAdoptable = 0
                if not self.curve_from_csv_existed:
                    self.clean_all_information()

        elif str(filename).__contains__('csv'):
            del self.curves_center['csv'][filename][label_to_be_deleted]
            if len(self.curves_center['csv'][filename].keys()) == 0:
                self.clean_all_information()

    def get_labels_drawn(self):
        return self.labelsDrawn

    def change_canvas_color(self, color):
        self.setCanvasBackground(color)
        self.replot()

    def change_canvas_layout(self, layout_mode):

        if layout_mode == 'grid':
            self.grid.enableY(True)
            self.grid.enableX(True)
            self.grid.enableXMin(True)
            self.grid.enableYMin(True)
        elif layout_mode == 'verticalBox':
            self.grid.enableY(False)
            self.grid.enableX(True)
            self.grid.enableYMin(False)
            self.grid.enableXMin(True)
        elif layout_mode == 'horizontalBox':
            self.grid.enableY(True)
            self.grid.enableX(False)
            self.grid.enableYMin(True)
            self.grid.enableXMin(False)
        elif layout_mode == 'NoGrid':
            self.grid.enableY(False)
            self.grid.enableX(False)
            self.grid.enableXMin(False)
            self.grid.enableYMin(False)

        self.replot()

    def get_siso_config(self):
        return self.sisoConfig

    def print_curve_center(self):
        print self.curves_center

    def ask_if_curve_from_csv_existed(self):
        return self.curve_from_csv_existed

    def ask_if_curve_from_lom_existed(self):
        return self.curve_from_csv_existed

    def set_analyser_mediator(self, analyser_mediator):
        self.analyseurMediator = analyser_mediator

    """
    def curves_property_setting(self):
        curve = QwtPlotCurve()
        curve.setSymbol(QwtSymbol(QwtSymbol.Diamond, QBrush(Qt.black), QPen(Qt.white), QSize(7, 7)))
        curve.setStyle(QwtPlotCurve.NoCurve)
        curve.setCurveAttribute(QwtPlotCurve.Fitted)
        curve.setRenderHint(QwtPlotItem.RenderAntialiased)
        curve.setPen(QPen(Qt.green))
        curve.attach(self)
        self.csvCurveList.append(curve)
    """

    def set_current_siso_curves_linear_gradient(self, start_color, finish_color):
        self.clean_before_replot()

        sub_x = []
        sub_y = []

        page_index = self.plottingBoardReference.get_page_index()
        plotting_index = self.plottingBoardReference.get_plotting_index()
        loaded_csv_files = self.analyseurMediator.get_loaded_csv_files_from_context(page_index, plotting_index)
        loaded_csvfiles_validity = self.analyseurMediator.get_loaded_csv_files_validity_from_context(page_index, plotting_index)
        curves_on_canvas = self.plottingBoardReference.get_plot_parameter_manipulation_object().get_curves_validity_information()
        plotting_context = self.analyseurMediator.get_a_plotting_context(page_index, plotting_index)

        for csv_file_name in loaded_csv_files:
            if not loaded_csvfiles_validity[loaded_csv_files.index(csv_file_name)]:
                continue
            # get the list of super siso which has been cut
            sub_list_siso_indexs = plotting_context.get_sub_lists_of_siso_index(csv_file_name)
            sub_list_iso_indexs = plotting_context.get_sub_lists_of_iso_index(csv_file_name)
            abscissa_values = plotting_context.get_abscissa_parameter_values(csv_file_name)
            list_of_ordinate_name = plotting_context.get_list_of_ordinate_parameter_name(csv_file_name)
            list_of_ordinate_values = plotting_context.get_list_of_ordinate_parameter_values(csv_file_name)

            for h in range(len(list_of_ordinate_values)):  # parse the nbr of the curve
                if curves_on_canvas[csv_file_name][list_of_ordinate_name[h]] == 0:
                    continue

                for i in range(len(sub_list_iso_indexs)):  # parse the latest sub list of iso
                    index_temp = list()
                    for j in range(len(sub_list_siso_indexs)):
                        for iso_value_index in sub_list_iso_indexs[i]:
                            if iso_value_index in sub_list_siso_indexs[j]:
                                index_temp.append(iso_value_index)

                        curve = QwtPlotCurve()
                        self.set_curve_gradient(curve, j, len(sub_list_siso_indexs), start_color, finish_color)

                        for k in index_temp:
                            sub_x.append(float(abscissa_values[k]))
                            sub_y.append(float(list_of_ordinate_values[h][k]))
                        curve.setData(sub_x, sub_y)

                        self.curves_center['csv'][csv_file_name][list_of_ordinate_name[h]].append(curve)
                        del sub_x[:]
                        del sub_y[:]
                        del index_temp[:]

                for i in self.curves_center['csv'][csv_file_name][list_of_ordinate_name[h]]:
                    i.attach(self)

        self.replot()
        self.curve_gradient_using = True

    def set_current_iso_curves_linear_gradient(self, start_color, finish_color):
        page_index = self.plottingBoardReference.get_page_index()
        plotting_index = self.plottingBoardReference.get_plotting_index()
        loaded_csv_files = self.analyseurMediator.get_loaded_csv_files_from_context(page_index, plotting_index)
        loaded_csvfiles_validity = self.analyseurMediator.get_loaded_csv_files_validity_from_context(page_index, plotting_index)
        curves_on_canvas = self.plottingBoardReference.get_plot_parameter_manipulation_object().get_curves_validity_information()

        for csv_file_name in loaded_csv_files:
            if not loaded_csvfiles_validity[loaded_csv_files.index(csv_file_name)]:
                continue
            for h in self.curves_center['csv'][csv_file_name].keys():
                if curves_on_canvas[csv_file_name][h] == 0:
                    continue
                cpt = 0
                for curve in self.curves_center['csv'][csv_file_name][h]:
                    self.set_curve_gradient(curve, cpt, len(self.curves_center['csv'][csv_file_name][h]), start_color, finish_color)
                    cpt += 1
        self.replot()
        self.curve_gradient_using = True

    def set_current_iso_curves_no_linear_gradient(self):
        page_index = self.plottingBoardReference.get_page_index()
        plotting_index = self.plottingBoardReference.get_plotting_index()
        loaded_csv_files = self.analyseurMediator.get_loaded_csv_files_from_context(page_index, plotting_index)
        loaded_csvfiles_validity = self.analyseurMediator.get_loaded_csv_files_validity_from_context(page_index, plotting_index)
        curves_on_canvas = self.plottingBoardReference.get_plot_parameter_manipulation_object().get_curves_validity_information()

        for csv_file_name in loaded_csv_files:
            if not loaded_csvfiles_validity[loaded_csv_files.index(csv_file_name)]:
                continue

            for h in self.curves_center['csv'][csv_file_name].keys():
                if curves_on_canvas[csv_file_name][h] == 0:
                    continue

                cpt = 0
                for curve in self.curves_center['csv'][csv_file_name][h]:
                    self.set_curve_property_by_color_marker(curve, cpt)
                    cpt += 1
        self.replot()
        self.curve_gradient_using = False

    def update_current_curve(self):
        self.clean_before_replot()

        page_index = self.plottingBoardReference.get_page_index()
        plotting_index = self.plottingBoardReference.get_plotting_index()
        loaded_csv_files = self.analyseurMediator.get_loaded_csv_files_from_context(page_index, plotting_index)
        loaded_csvfiles_validity = self.analyseurMediator.get_loaded_csv_files_validity_from_context(page_index, plotting_index)
        curves_on_canvas = self.plottingBoardReference.get_plot_parameter_manipulation_object().get_curves_validity_information()
        plotting_context = self.analyseurMediator.get_a_plotting_context(page_index, plotting_index)

        for csv_file_name in loaded_csv_files:
            if not loaded_csvfiles_validity[loaded_csv_files.index(csv_file_name)]:
                continue
            abscissa_values = plotting_context.get_abscissa_parameter_values(csv_file_name)
            list_of_ordinate_name = plotting_context.get_list_of_ordinate_parameter_name(csv_file_name)
            list_of_ordinate_values = plotting_context.get_list_of_ordinate_parameter_values(csv_file_name)

            for h in range(len(list_of_ordinate_values)):  # parse the nbr of the curve
                if curves_on_canvas[csv_file_name][list_of_ordinate_name[h]] == 0:
                    continue

                curve = QwtPlotCurve()
                self.set_curve_property(curve, h)

                curve.setData(np.array(abscissa_values, dtype='float64'), np.array(list_of_ordinate_values[h], dtype='float64'))

                self.curves_center['csv'][csv_file_name][list_of_ordinate_name[h]].append(curve)

                for i in self.curves_center['csv'][csv_file_name][list_of_ordinate_name[h]]:
                    i.attach(self)

        self.replot()
        self.curve_gradient_using = False

    def cut_current_curves_by_iso(self):
        self.isoExisted = True
        self.clean_before_replot()

        sub_x = []
        sub_y = []

        page_index = self.plottingBoardReference.get_page_index()
        plotting_index = self.plottingBoardReference.get_plotting_index()
        loaded_csv_files = self.analyseurMediator.get_loaded_csv_files_from_context(page_index, plotting_index)
        loaded_csvfiles_validity = self.analyseurMediator.get_loaded_csv_files_validity_from_context(page_index, plotting_index)
        curves_on_canvas = self.plottingBoardReference.get_plot_parameter_manipulation_object().get_curves_validity_information()
        plotting_context = self.analyseurMediator.get_a_plotting_context(page_index, plotting_index)

        for csv_file_name in loaded_csv_files:
            if not loaded_csvfiles_validity[loaded_csv_files.index(csv_file_name)]:
                continue
            sub_list_iso_values = plotting_context.get_sub_lists_of_iso(csv_file_name)
            sub_list_iso_indexs = plotting_context.get_sub_lists_of_iso_index(csv_file_name)
            abscissa_values = plotting_context.get_abscissa_parameter_values(csv_file_name)
            list_of_ordinate_name = plotting_context.get_list_of_ordinate_parameter_name(csv_file_name)
            list_of_ordinate_values = plotting_context.get_list_of_ordinate_parameter_values(csv_file_name)

            for h in range(len(list_of_ordinate_values)):  # parse the nbr of the curve
                if curves_on_canvas[csv_file_name][list_of_ordinate_name[h]] == 0:
                    continue

                for i in range(len(sub_list_iso_values)):  # parse the latest sub list of iso
                    if len(sub_list_iso_indexs[i]) != 0:
                        curve = QwtPlotCurve()
                        self.set_curve_property_by_color_marker(curve, i)

                        for j in sub_list_iso_indexs[i]:
                            sub_x.append(float(abscissa_values[j]))
                            sub_y.append(float(list_of_ordinate_values[h][j]))
                        curve.setData(sub_x, sub_y)

                        self.curves_center['csv'][csv_file_name][list_of_ordinate_name[h]].append(curve)
                        del sub_x[:]
                        del sub_y[:]

                for i in self.curves_center['csv'][csv_file_name][list_of_ordinate_name[h]]:
                    i.attach(self)

        self.replot()
        self.curve_gradient_using = False

    def cut_current_curves_by_siso(self, siso_config):
        self.sisoConfig = siso_config
        self.sisoExisted = True
        self.clean_before_replot()

        sub_x = []
        sub_y = []

        page_index = self.plottingBoardReference.get_page_index()
        plotting_index = self.plottingBoardReference.get_plotting_index()
        loaded_csv_files = self.analyseurMediator.get_loaded_csv_files_from_context(page_index, plotting_index)
        loaded_csvfiles_validity = self.analyseurMediator.get_loaded_csv_files_validity_from_context(page_index, plotting_index)
        curves_on_canvas = self.plottingBoardReference.get_plot_parameter_manipulation_object().get_curves_validity_information()
        plotting_context = self.analyseurMediator.get_a_plotting_context(page_index, plotting_index)

        # parse the loaded files to find the list to be drawn
        for csv_file_name in loaded_csv_files:
            if not loaded_csvfiles_validity[loaded_csv_files.index(csv_file_name)]:
                continue
            # get the list of super siso which has been cut
            sub_list_siso_indexs = plotting_context.get_sub_lists_of_siso_index(csv_file_name)
            sub_list_iso_indexs = plotting_context.get_sub_lists_of_iso_index(csv_file_name)
            abscissa_values = plotting_context.get_abscissa_parameter_values(csv_file_name)
            list_of_ordinate_name = plotting_context.get_list_of_ordinate_parameter_name(csv_file_name)
            list_of_ordinate_values = plotting_context.get_list_of_ordinate_parameter_values(csv_file_name)

            for h in range(len(list_of_ordinate_values)):  # parse the nbr of the curve
                if curves_on_canvas[csv_file_name][list_of_ordinate_name[h]] == 0:
                    continue

                for i in range(len(sub_list_iso_indexs)):  # parse the latest sub list of iso
                    index_temp = list()
                    for j in range(len(sub_list_siso_indexs)):
                        for iso_value_index in sub_list_iso_indexs[i]:
                            if iso_value_index in sub_list_siso_indexs[j]:
                                index_temp.append(iso_value_index)

                        curve = QwtPlotCurve()
                        if siso_config == "represent_by_color":
                            self.set_curve_property_by_color(curve, i, j)
                        elif siso_config == "represent_by_marker":
                            self.set_curve_property_by_marker(curve, i, j)

                        for k in index_temp:
                            sub_x.append(float(abscissa_values[k]))
                            sub_y.append(float(list_of_ordinate_values[h][k]))
                        curve.setData(sub_x, sub_y)

                        self.curves_center['csv'][csv_file_name][list_of_ordinate_name[h]].append(curve)
                        del sub_x[:]
                        del sub_y[:]
                        del index_temp[:]

                for i in self.curves_center['csv'][csv_file_name][list_of_ordinate_name[h]]:
                    i.attach(self)

        self.replot()
        self.curve_gradient_using = False

    def replot_current_lom_curves(self):

        if not self.curve_from_lom_existed:
            return

        page_index = self.plottingBoardReference.get_page_index()
        plotting_index = self.plottingBoardReference.get_plotting_index()
        loaded_lomfiles = self.analyseurMediator.get_loaded_lom_files_from_context(page_index, plotting_index)
        loaded_lomfiles_validity = self.analyseurMediator.get_loaded_lom_files_validity_from_context(page_index, plotting_index)
        curves_on_canvas = self.plottingBoardReference.get_plot_parameter_manipulation_object().get_curves_validity_information()
        plotting_context = self.analyseurMediator.get_a_plotting_context(page_index, plotting_index)

        for lom_file_name in loaded_lomfiles:
            if not loaded_lomfiles_validity[loaded_lomfiles.index(lom_file_name)]:
                continue
            for label_name in plotting_context.get_label_list_from_lom_file(lom_file_name):
                if curves_on_canvas[lom_file_name][label_name] == 0:
                    continue

                if plotting_context.get_label_dimension_from_lom_file(label_name, lom_file_name) == 1:
                    abscissa_values = plotting_context.get_abscissa_parameter_values_from_lom_file(label_name, lom_file_name)
                    ordinate_values = plotting_context.get_list_of_ordinate_parameter_values_from_lom_file(label_name, lom_file_name)

                    curve = QwtPlotCurve()
                    self.set_lom_curve_property_by_color_marker(curve, 0)
                    curve.setData(abscissa_values, ordinate_values)
                    self.curves_center['lom'][lom_file_name][label_name] = curve
                    self.curves_center['lom'][lom_file_name][label_name].attach(self)

                elif plotting_context.get_label_dimension_from_lom_file(label_name, lom_file_name) == 2:
                    abscissa_values = plotting_context.get_abscissa_parameter_values_from_lom_file(label_name, lom_file_name)
                    list_of_ordinate_values = plotting_context.get_list_of_ordinate_parameter_values_from_lom_file(label_name, lom_file_name)
                    iso_values = plotting_context.get_iso_parameter_values_from_lom_file(label_name, lom_file_name)
                    iso_validity = plotting_context.get_iso_parameter_validity_from_lom_file(label_name, lom_file_name)

                    for i in range(len(list_of_ordinate_values)):
                        curve = QwtPlotCurve()
                        self.set_lom_curve_property_by_color_marker(curve, i)
                        ordinate_values = list_of_ordinate_values[i]
                        curve.setData(abscissa_values, ordinate_values)
                        self.curves_center['lom'][lom_file_name][label_name][iso_values[i]] = curve

                    cpt_iso = 0
                    for c in iso_values:
                        if iso_validity[cpt_iso] == 1:
                            self.curves_center['lom'][lom_file_name][label_name][c].attach(self)
                        cpt_iso += 1

                elif plotting_context.get_label_dimension_from_lom_file(label_name, lom_file_name) == 3:
                    abscissa_values = plotting_context.get_abscissa_parameter_values_from_lom_file(label_name, lom_file_name)
                    list_of_ordinate_values = plotting_context.get_list_of_ordinate_parameter_values_from_lom_file(label_name, lom_file_name)
                    iso_values = plotting_context.get_iso_parameter_values_from_lom_file(label_name, lom_file_name)
                    iso_validity = plotting_context.get_iso_parameter_validity_from_lom_file(label_name, lom_file_name)
                    siso_values = plotting_context.get_siso_parameter_values_from_lom_file(label_name, lom_file_name)
                    siso_validity = plotting_context.get_siso_parameter_validity_from_lom_file(label_name, lom_file_name)

                    for i in range(len(siso_values)):
                        for j in range(len(iso_values)):
                            curve = QwtPlotCurve()
                            if self.sisoConfig == "represent_by_color":
                                self.set_lom_curve_property_by_color(curve, i, j)
                            elif self.sisoConfig == "represent_by_marker":
                                self.set_lom_curve_property_by_marker(curve, i, j)

                            ordinate_values = list_of_ordinate_values[i][j]

                            curve.setData(abscissa_values, ordinate_values)
                            self.curves_center['lom'][lom_file_name][label_name][siso_values[i]][iso_values[j]] = curve

                    cpt_siso = 0
                    for j in siso_values:
                        if siso_validity[cpt_siso] == 1:
                            cpt_iso = 0
                            for c in iso_values:
                                if iso_validity[cpt_iso] == 1:
                                    self.curves_center['lom'][lom_file_name][label_name][j][c].attach(self)
                                cpt_iso += 1
                        cpt_siso += 1
        self.replot()

    def draw_on_canvas_using_csv_files(self, csv_file_name, ordinate_name, abscissa_name):
        """plot a curve according to the parameter passed

            -- Fetch the values of two parameter of the file chosen from the plottingContext to generate a curve object
            Then Save the curve into in curves_center according to its ordinate name and the file came from
            Finally, create a tree widget item in the parameter manipulation board at the right side which connect to the curve

        :param csv_file_name:
        :param ordinate_name:
        :param abscissa_name:
        :return:
        """
        page_index = self.plottingBoardReference.get_page_index()
        plotting_index = self.plottingBoardReference.get_plotting_index()
        plotting_context = self.analyseurMediator.get_a_plotting_context(page_index, plotting_index)

        if csv_file_name not in self.curves_center['csv'].keys():
            self.curves_center['csv'][csv_file_name] = {}

        ordinate_names = plotting_context.get_list_of_ordinate_parameter_name(csv_file_name)
        ordinate_index = ordinate_names.index(ordinate_name)

        abscissa_values = np.array(plotting_context.get_abscissa_parameter_values(csv_file_name), dtype='float64')

        list_of_y = plotting_context.get_list_of_ordinate_parameter_values(csv_file_name)
        ordinate_values = np.array(list_of_y[ordinate_index], dtype='float64')

        curve = QwtPlotCurve()
        curve.setData(abscissa_values, ordinate_values)
        self.set_curve_property(curve, len(self.curves_center['csv'][csv_file_name].keys()))
        curve.attach(self)

        self.replot()
        self.curve_from_csv_existed = True

        # verify if the ordinate parameter key existed already in the curves center
        if ordinate_name not in self.curves_center['csv'][csv_file_name].keys():
            self.curves_center['csv'][csv_file_name][ordinate_name] = []
            self.curves_center['csv'][csv_file_name][ordinate_name].append(curve)

        # for k in ordinate_names:
        self.plottingBoardReference.get_plot_parameter_manipulation_object().set_ordinate_config_table(csv_file_name, ordinate_name)

        self.plottingBoardReference.set_function_title(ordinate_names, abscissa_name, "", "")

    def draw_on_canvas_using_lom_files(self, lom_file_name, label_name, dimension):

        page_index = self.plottingBoardReference.get_page_index()
        plotting_index = self.plottingBoardReference.get_plotting_index()
        plotting_context = self.analyseurMediator.get_a_plotting_context(page_index, plotting_index)

        if dimension == 1:
            if lom_file_name not in self.curves_center['lom'].keys():
                self.curves_center['lom'][lom_file_name] = {}
                self.curves_center['lom'][lom_file_name][label_name] = []
            else:
                self.curves_center['lom'][lom_file_name][label_name] = []

            abscissa_values = plotting_context.get_abscissa_parameter_values_from_lom_file(label_name, lom_file_name)
            ordinate_values = plotting_context.get_list_of_ordinate_parameter_values_from_lom_file(label_name, lom_file_name)
            curve = QwtPlotCurve()
            self.set_lom_curve_property_by_color_marker(curve, 0)
            curve.setData(abscissa_values, ordinate_values)
            self.curves_center['lom'][lom_file_name][label_name].append(curve)

            for j in self.curves_center['lom'][lom_file_name][label_name]:
                j.attach(self)

        elif dimension == 2:
            if lom_file_name not in self.curves_center['lom'].keys():
                self.curves_center['lom'][lom_file_name] = {}
                self.curves_center['lom'][lom_file_name][label_name] = {}
            else:
                self.curves_center['lom'][lom_file_name][label_name] = {}

            abscissa_values = plotting_context.get_abscissa_parameter_values_from_lom_file(label_name, lom_file_name)
            list_of_ordinate_values = plotting_context.get_list_of_ordinate_parameter_values_from_lom_file(label_name, lom_file_name)
            iso_values = plotting_context.get_iso_parameter_values_from_lom_file(label_name, lom_file_name)
            iso_validity = plotting_context.get_iso_parameter_validity_from_lom_file(label_name, lom_file_name)

            for i in range(len(list_of_ordinate_values)):
                if len(list_of_ordinate_values[i]) != 0:
                    curve = QwtPlotCurve()
                    self.set_lom_curve_property_by_color_marker(curve, i)
                    curve.setData(abscissa_values, list_of_ordinate_values[i])
                    self.curves_center['lom'][lom_file_name][label_name][iso_values[i]] = curve
                else:
                    curve = QwtPlotCurve()
                    self.set_lom_curve_property_by_color_marker(curve, i)
                    curve.setData([], [])
                    self.curves_center['lom'][lom_file_name][label_name][iso_values[i]] = curve

            cpt_iso = 0
            for j in iso_values:
                if iso_validity[cpt_iso] == 1:
                    self.curves_center['lom'][lom_file_name][label_name][j].attach(self)
                    cpt_iso += 1

        elif dimension == 3:
            if lom_file_name not in self.curves_center['lom'].keys():
                self.curves_center['lom'][lom_file_name] = {}
                self.curves_center['lom'][lom_file_name][label_name] = {}
            else:
                self.curves_center['lom'][lom_file_name][label_name] = {}

            abscissa_values = plotting_context.get_abscissa_parameter_values_from_lom_file(label_name, lom_file_name)
            list_of_ordinate_values = plotting_context.get_list_of_ordinate_parameter_values_from_lom_file(label_name, lom_file_name)
            iso_values = plotting_context.get_iso_parameter_values_from_lom_file(label_name, lom_file_name)
            iso_validity = plotting_context.get_iso_parameter_validity_from_lom_file(label_name, lom_file_name)
            siso_values = plotting_context.get_siso_parameter_values_from_lom_file(label_name, lom_file_name)
            siso_validity = plotting_context.get_siso_parameter_validity_from_lom_file(label_name, lom_file_name)

            for i in range(len(siso_values)):
                self.curves_center['lom'][lom_file_name][label_name][siso_values[i]] = {}
                for j in range(len(iso_values)):
                    curve = QwtPlotCurve()
                    if self.sisoConfig == "represent_by_color":
                        self.set_lom_curve_property_by_color(curve, i, j)
                    elif self.sisoConfig == "represent_by_marker":
                        self.set_lom_curve_property_by_marker(curve, i, j)

                    ordinate_values = list_of_ordinate_values[i][j]

                    curve.setData(abscissa_values, ordinate_values)
                    self.curves_center['lom'][lom_file_name][label_name][siso_values[i]][iso_values[j]] = curve

            cpt_siso = 0
            for j in siso_values:
                if siso_validity[cpt_siso] == 1:
                    cpt_iso = 0
                    for c in iso_values:
                        if iso_validity[cpt_iso] == 1:
                            self.curves_center['lom'][lom_file_name][label_name][j][c].attach(self)
                        cpt_iso += 1
                cpt_siso += 1

        self.replot()
        self.curve_from_lom_existed = True

    def dragEnterEvent(self, event):
        """
            Accept a drop event if the item entered is the type "application/x-icon-and-text"
        :param event:
        :return:
        """
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """Set the values of an parameter/label into the plotting context

        After the drop action of the parameter/label chosen from the csv/lom file,  Fetch parameter/label's values from the files context
        and set the values into the tree structure of the plotting context

        :param event.mimeData().hasFormat("application/x-icon-and-text"):  the name of the parameter/label
        """

        page_index = self.plottingBoardReference.get_page_index()
        plotting_index = self.plottingBoardReference.get_plotting_index()
        plotting_context = self.analyseurMediator.get_a_plotting_context(page_index, plotting_index)

        y_value_pointer = -1
        ordinate_name = ''
        # If we work with the csv file currently
        if self.analyseurMediator.get_filetype_handling_from_context() == "csv":

            # Need_to_draw is a parameter who decide if it is ready to plotting, which means the curve can be drawn at least if the abscissa and ordinate's ready
            need_to_replot = False

            # Fetch the parameter's name from a drop event
            if event.mimeData().hasFormat("application/x-icon-and-text"):
                data = event.mimeData().data("application/x-icon-and-text")
                stream = QDataStream(data, QIODevice.ReadOnly)
                parameter_name = QString()
                stream >> parameter_name

                # With the help of the message box widget, user can decide the axis to apply the parameter dropped
                axis_choose_box = QMessageBox()
                axis_choose_box.setFont(QFont("Helvetica", 8, QFont.AnyStyle, True))
                icon_img = QIcon(":/fileconfiguration.png")
                axis_choose_box.setWindowIcon(icon_img)
                axis_choose_box.setWindowTitle("configuration")
                axis_choose_box.setText("Set the parameter " + parameter_name + " as: ")
                abscissa_choice = axis_choose_box.addButton(str("abscissa"), QMessageBox.ActionRole)
                abscissa_choice.setFixedSize(60, 25)
                abscissa_choice.setFlat(1)
                ordinate_choice = axis_choose_box.addButton(str("ordinate"), QMessageBox.ActionRole)
                ordinate_choice.setFixedSize(60, 25)
                ordinate_choice.setFlat(1)
                cancel_choice = axis_choose_box.addButton("cancel", QMessageBox.RejectRole)
                cancel_choice.setFixedSize(50, 25)
                cancel_choice.setFlat(1)
                axis_choose_box.setStyleSheet("background-color: skyBlue; color: AliceBlue")
                axis_choose_box.exec_()

                # Abandon the drag&drop operation
                if axis_choose_box.clickedButton() == cancel_choice:
                    return
                # If the choice is to apply the parameter's information to the abscissa axis
                elif axis_choose_box.clickedButton() == abscissa_choice:
                    self.analyseurMediator.generate_an_action_into_global_context('drop parameter: ' + parameter_name + ' as abscissa'
                                                                                  + ' for plotting board :'
                                                                                  + str(self.plottingBoardReference.get_plotting_index()) + ' in page: '
                                                                                  + str(self.plottingBoardReference.get_page_index()))
                    # Fetch the list of the loaded csv file's names
                    page_index = self.plottingBoardReference.get_page_index()
                    plotting_index = self.plottingBoardReference.get_plotting_index()
                    loaded_csvfiles = self.analyseurMediator.get_loaded_csv_files_from_context(page_index, plotting_index)
                    loaded_csvfiles_validity = self.analyseurMediator.get_loaded_csv_files_validity_from_context(page_index, plotting_index)

                    # For each csv file's name, firstly to check if the parameter has been already set as the abscissa in the csv file tree,
                    # if not, set the value list into this csv tree structure
                    if len(loaded_csvfiles) > 0:

                        for csvfile in loaded_csvfiles:
                            # if not loaded_csvfiles_validity[loaded_csvfiles.index(csvfile)]:
                            # continue
                            current_file = self.analyseurMediator.get_csv_file_in_context_by_name(csvfile)
                            values = current_file.get_values()
                            list_of_titles = current_file.get_title_list()
                            rowcount = current_file.get_row_count()

                            # check if the current file contains the parameter with the name dropped
                            if parameter_name not in list_of_titles:
                                loaded_csvfiles_validity[loaded_csvfiles.index(csvfile)] = 0
                                continue

                            loaded_csvfiles_validity[loaded_csvfiles.index(csvfile)] = 1

                            # check if the plotting context related has the abscissa value with the same name in order to avoid do the same thing a second time
                            if parameter_name == plotting_context.get_abscissa_parameter_name(csvfile):
                                print 'this parameter existed already in the abscissa in file', csvfile
                                return
                            else:
                                if plotting_context.get_abscissa_parameter_name(csvfile) == "":
                                    self.abscissa_name = str(parameter_name)
                                    plotting_context.set_abscissa_parameter_name(self.abscissa_name, csvfile)

                                    try:
                                        abscissa_value_pointer = list_of_titles.index(plotting_context.get_abscissa_parameter_name(csvfile))
                                        abscissa_value_list = plotting_context.get_abscissa_parameter_values(csvfile)
                                        del abscissa_value_list[:]
                                        if self.abscissa_name == 'GMT':
                                            for k in range(rowcount):
                                                abscissa_value_list.append(k)
                                        else:
                                            for i in range(rowcount):
                                                abscissa_value_list.append(values[i][abscissa_value_pointer])
                                    except ValueError:
                                        continue
                                else:
                                    # TODO Need to update all the curve with the new abscissa list
                                    print "let us do it"
                    else:
                        QMessageBox.question(self, 'Message', "No csv file loaded right now")

                # If the choice is to apply the parameter's information to the ordinate axis
                elif axis_choose_box.clickedButton() == ordinate_choice:
                    self.analyseurMediator.generate_an_action_into_global_context('drop parameter: ' + parameter_name + ' as ordinate'
                                                                                  + ' for plotting board :'
                                                                                  + str(self.plottingBoardReference.get_plotting_index()) + ' in page: '
                                                                                  + str(self.plottingBoardReference.get_page_index()))

                    ordinate_name = str(parameter_name)

                    # Fetch the list of the csv file's names
                    page_index = self.plottingBoardReference.get_page_index()
                    plotting_index = self.plottingBoardReference.get_plotting_index()
                    loaded_csvfiles = self.analyseurMediator.get_loaded_csv_files_from_context(page_index, plotting_index)
                    loaded_csvfiles_validity = self.analyseurMediator.get_loaded_csv_files_validity_from_context(page_index, plotting_index)

                    y_values_list = [[] for _ in range(len(loaded_csvfiles))]
                    cpt = 0

                    # For each csv file's name, firstly to check if the parameter has been already set as the ordinate in the csv file tree,
                    # if not, set the value list into this vsv tree structure
                    if len(loaded_csvfiles) > 0:

                        for csvfile in loaded_csvfiles:
                            # if not loaded_csvfiles_validity[loaded_csvfiles.index(csvfile)]:
                            # continue
                            current_file = self.analyseurMediator.get_csv_file_in_context_by_name(csvfile)
                            values = current_file.get_values()
                            list_of_titles = current_file.get_title_list()
                            rowcount = current_file.get_row_count()

                            # check if the current file contains the parameter with the name dropped
                            if ordinate_name not in list_of_titles:
                                loaded_csvfiles_validity[loaded_csvfiles.index(csvfile)] = 0
                                continue

                            loaded_csvfiles_validity[loaded_csvfiles.index(csvfile)] = 1

                            if ordinate_name in plotting_context.get_list_of_ordinate_parameter_name(csvfile):
                                print 'this parameter existed already in the list of ordinate in file', csvfile
                                return
                            else:
                                need_to_replot = True

                                # firstly, we have to check if the abscissa name applied existed in the current file's parameter list
                                # so that, we can decide whether need to fetch the ordinate's value list or not
                                if (self.abscissa_name in list_of_titles) or (self.abscissa_name == ""):
                                    try:
                                        y_value_pointer = list_of_titles.index(ordinate_name)

                                        if ordinate_name == 'GMT':
                                            for k in range(rowcount):
                                                y_values_list[cpt].append(k)
                                        else:
                                            for k in range(rowcount):
                                                y_values_list[cpt].append(values[k][y_value_pointer])
                                    except ValueError:
                                        print "not existed"
                                        continue
                                else:
                                    QMessageBox.question(self, 'Message', "The file:" + csvfile + " doesn't existed the abscissa" + self.abscissa_name)

                            if y_value_pointer >= 0:
                                plotting_context.set_list_of_ordinate_parameter_name(ordinate_name, csvfile)
                                plotting_context.set_list_of_ordinate_parameter_values(y_values_list[cpt], csvfile)
                            cpt += 1
                            y_value_pointer = -1
                    else:
                        QMessageBox.question(self, 'Message', "No csv file loaded right now")

                # If we need to update the curves on the canvas, just do it
                if need_to_replot:
                    for csv_file_name in loaded_csvfiles:
                        if not loaded_csvfiles_validity[loaded_csvfiles.index(csv_file_name)]:
                            continue
                        if (plotting_context.get_abscissa_parameter_name(csv_file_name) != "") and (len(plotting_context.get_list_of_ordinate_parameter_name(csv_file_name)) > 0):
                            self.draw_on_canvas_using_csv_files(csv_file_name, ordinate_name, self.abscissa_name)
                            # break

        # If we work with the lom file currently
        elif self.analyseurMediator.get_filetype_handling_from_context() == "lom":
            """
            if self.curve_from_csv_existed:
                loaded_csv_files = self.analyseurController.get_loaded_csv_files_from_context(self.plotting_board_reference.get_page_index(), self.plotting_board_reference.get_plotting_index())
                loaded_csvfiles_validity = self.analyseurController.get_loaded_csv_files_validity_from_context(self.plotting_board_reference.get_page_index(), self.plotting_board_reference.get_plotting_index())

                for csvfile in self.curves_center['csv'].keys():
                    if csvfile in loaded_csv_files:
                        loaded_csvfiles_validity[loaded_csv_files.index(csvfile)] = 1
            """

            # fetch the label's name from a drop event
            if event.mimeData().hasFormat("application/x-icon-and-text"):
                data = event.mimeData().data("application/x-icon-and-text")
                stream = QDataStream(data, QIODevice.ReadOnly)
                parameter_name = QString()
                stream >> parameter_name
                ordinate_name = str(parameter_name)

                # Fetch the list of the loaded lom file's names and its validity in the global context through the page index and the canvas index number
                page_index = self.plottingBoardReference.get_page_index()
                plotting_index = self.plottingBoardReference.get_plotting_index()
                loaded_lomfiles = self.analyseurMediator.get_loaded_lom_files_from_context(page_index, plotting_index)
                loaded_lomfiles_validity = self.analyseurMediator.get_loaded_lom_files_validity_from_context(page_index, plotting_index)

                if len(loaded_lomfiles) > 0:
                    for lomfile in loaded_lomfiles:
                        # Get the current lom file object
                        current_file = self.analyseurMediator.get_lom_file_in_context_by_name(lomfile)

                        # get a reference of all the labels in the lom file objects
                        labels = current_file.get_labels()

                        # get a reference of the label object
                        label = labels.getlab(ordinate_name)

                        # check if the current file contains the parameter with the name dropped, if not, pass this turn of loop
                        if label == -1:
                            loaded_lomfiles_validity[loaded_lomfiles.index(lomfile)] = 0
                            continue

                        # check the dimension of the label which has been plotted before, if existed.
                        # if it is different, let user decide to update the label or cancel the drop action
                        if (self.dimensionAdoptable != 0) and (self.dimensionAdoptable != label.get_dimension()):
                            self.plottingBoardReference.get_parent().get_parent().parent().parent().get_status_bar_reference().display_error_message(
                                "the dimension of the label is not adoptable")
                            reply = QMessageBox()
                            reply.setText("Update canvas with the label dropped?")
                            yes = reply.addButton(str("yes"), QMessageBox.ActionRole)
                            yes.setFlat(True)
                            cancel = reply.addButton(str("abandon"), QMessageBox.ActionRole)
                            cancel.setFlat(True)
                            reply.setFont(QFont("Helvetica", 8, QFont.AnyStyle, True))
                            reply.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
                            reply.setStyleSheet("background-color: skyBlue; color: AliceBlue")
                            reply.exec_()

                            if reply.clickedButton() == cancel:
                                event.ignore()
                                return
                            elif reply.clickedButton() == yes:
                                self.plottingBoardReference.self_cleaning()
                                self.analyseurMediator.generate_an_action_into_global_context('drop label: ' + ordinate_name + ' to replace'
                                                                                              + ' for plotting board :'
                                                                                              + str(self.plottingBoardReference.get_plotting_index()) + ' in page: '
                                                                                              + str(self.plottingBoardReference.get_page_index()))

                        elif (self.dimensionAdoptable != 0) and (self.dimensionAdoptable == label.get_dimension()):
                            reply = QMessageBox()
                            reply.setText("Are you sure to achieve superpose action?")
                            yes = reply.addButton(str("yes"), QMessageBox.ActionRole)
                            yes.setFlat(True)
                            cancel = reply.addButton(str("abandon"), QMessageBox.ActionRole)
                            cancel.setFlat(True)
                            reply.setFont(QFont("Helvetica", 8, QFont.AnyStyle, True))
                            reply.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
                            reply.setStyleSheet("background-color: skyBlue; color: AliceBlue")
                            reply.exec_()

                            if reply.clickedButton() == cancel:
                                event.ignore()
                                return
                            elif reply.clickedButton() == yes:
                                # Activate the superpose action. after the action achieved, reset to false
                                self.labelSuperposeActionActivated = True
                                self.analyseurMediator.generate_an_action_into_global_context('drop label: ' + ordinate_name + ' to superpose'
                                                                                              + ' for plotting board :'
                                                                                              + str(self.plottingBoardReference.get_plotting_index()) + ' in page: '
                                                                                              + str(self.plottingBoardReference.get_page_index()))
                        else:
                            self.analyseurMediator.generate_an_action_into_global_context('drop label: ' + ordinate_name + ' the first time'
                                                                                          + ' for plotting board :'
                                                                                          + str(self.plottingBoardReference.get_plotting_index()) + ' in page: '
                                                                                          + str(self.plottingBoardReference.get_page_index()))

                        loaded_lomfiles_validity[loaded_lomfiles.index(lomfile)] = 1

                        lom_function = ""

                        # Set the label into the plotting context to produce a new tree structure of label. if existed already, reject.
                        if plotting_context.set_label_to_lom_files(ordinate_name, lomfile):

                            # check the dimension of the label dropped
                            # if y = f(x)
                            if label.get_dimension() == 1:

                                # set the dimension adoptable for the plotting
                                self.dimensionAdoptable = 1

                                # fetch the values associated
                                abscissa_name = labels.getabsname(ordinate_name)
                                abscissa_value = labels.getabs(ordinate_name)
                                ordinate_values = labels.getord(ordinate_name)

                                self.labelsDrawn.append((ordinate_name, lomfile))

                                # write the values above into the plotting context associated to the plotting
                                plotting_context.set_abscissa_parameter_name_from_lom_file(abscissa_name, ordinate_name, lomfile)
                                plotting_context.set_abscissa_parameter_values_from_lom_file(abscissa_value, ordinate_name, lomfile)
                                plotting_context.set_list_of_ordinate_parameter_name_from_lom_file(ordinate_name, ordinate_name, lomfile)
                                plotting_context.set_list_of_ordinate_parameter_values_from_lom_file(ordinate_values, ordinate_name, lomfile)
                                plotting_context.set_label_dimension_from_lom_file(label.get_dimension(), ordinate_name, lomfile)

                                # draw...
                                self.draw_on_canvas_using_lom_files(lomfile, ordinate_name, 1)
                                self.plottingBoardReference.get_plot_parameter_manipulation_object().set_ordinate_config_table(lomfile, ordinate_name)

                                # lom function to be displayed
                                lom_function += " ||: " + ordinate_name + " [" + abscissa_name + "]"

                            # if y = f(x, z)
                            elif label.get_dimension() == 2:

                                # fetch the values associated
                                # abscissa
                                abscissa_name = labels.getabsname(ordinate_name)
                                abscissa_value = list(labels.getabs(ordinate_name))

                                print type(labels.getord(ordinate_name))
                                print labels.getord(ordinate_name)
                                # ordinate
                                ordinate_values = []
                                for l in (labels.getord(ordinate_name)):
                                    ordinate_values.append(list(l))

                                # iso
                                iso_name = labels.getisoname(ordinate_name)
                                iso_values = list(labels.getiso(ordinate_name))
                                iso_validity = list()
                                for _ in iso_values:
                                    iso_validity.append(1)

                                # check if it is the normal lom plotting action, or its a superpose action
                                if not self.labelSuperposeActionActivated:
                                    self.labelsDrawn.append((ordinate_name, lomfile))
                                    self.dimensionAdoptable = 2

                                    plotting_context.set_abscissa_parameter_name_from_lom_file(abscissa_name, ordinate_name, lomfile)
                                    plotting_context.set_abscissa_parameter_values_from_lom_file(abscissa_value, ordinate_name, lomfile)
                                    plotting_context.set_list_of_ordinate_parameter_name_from_lom_file(ordinate_name, ordinate_name, lomfile)
                                    plotting_context.set_list_of_ordinate_parameter_values_from_lom_file(ordinate_values, ordinate_name, lomfile)
                                    plotting_context.set_iso_parameter_name_from_lom_file(iso_name, ordinate_name, lomfile)
                                    plotting_context.set_iso_parameter_values_from_lom_file(iso_values, ordinate_name, lomfile)
                                    plotting_context.set_iso_parameter_validity_from_lom_file(iso_validity, ordinate_name, lomfile)
                                    plotting_context.set_label_dimension_from_lom_file(self.dimensionAdoptable, ordinate_name, lomfile)

                                    # Generate a cutting command for iso to be applied on the plotting configuration board
                                    new_iso_cutting_command = ""

                                    for i in range(len(iso_values)):
                                        if i == len(iso_values) - 1:
                                            new_iso_cutting_command += str(iso_values[i])
                                        else:
                                            new_iso_cutting_command += str(iso_values[i]) + ";"

                                    if self.isoExisted:
                                        self.plottingBoardReference.get_plot_parameter_manipulation_object().replace_iso_cutting_information_by_lom_file(new_iso_cutting_command)
                                    else:
                                        self.isoExisted = True
                                        self.plottingBoardReference.get_plot_parameter_manipulation_object().set_iso_cutting_information_by_lom_file(new_iso_cutting_command, iso_name)

                                    self.draw_on_canvas_using_lom_files(lomfile, ordinate_name, 2)
                                    self.plottingBoardReference.get_plot_parameter_manipulation_object().set_ordinate_config_table(lomfile, ordinate_name)
                                    lom_function += "LOM: " + ordinate_name + " [" + abscissa_name + ", " + iso_name + "]"
                                else:
                                    # firstly
                                    for pair in self.labelsDrawn:
                                        old_ordinate_name = pair[0]
                                        old_lomfile = pair[1]
                                        old_ordinate_values = plotting_context.get_list_of_ordinate_parameter_values_from_lom_file(old_ordinate_name, old_lomfile)
                                        old_iso_values = list(plotting_context.get_iso_parameter_values_from_lom_file(old_ordinate_name, old_lomfile))
                                        old_iso_validity = plotting_context.get_iso_parameter_validity_from_lom_file(old_ordinate_name, old_lomfile)

                                        # then, find if iso values of the label existed has to be enriched or not
                                        for iso in iso_values:
                                            if iso not in old_iso_values:
                                                old_iso_values.append(iso)
                                                old_iso_values.sort()
                                                pos = old_iso_values.index(iso)
                                                old_iso_validity.insert(pos, 1)
                                                old_ordinate_values.insert(pos, [])

                                        plotting_context.set_list_of_ordinate_parameter_values_from_lom_file(old_ordinate_values, old_ordinate_name, old_lomfile)
                                        plotting_context.set_iso_parameter_values_from_lom_file(old_iso_values, old_ordinate_name, old_lomfile)
                                        plotting_context.set_iso_parameter_validity_from_lom_file(old_iso_validity, old_ordinate_name, old_lomfile)

                                        # renew the curves on the plotting board which represent this label
                                        self.clean_before_replot()
                                        self.plottingBoardReference.get_plot_parameter_manipulation_object().clean_all_component(False)
                                        self.isoExisted = False
                                        del self.curves_center['lom'][old_lomfile][old_ordinate_name]

                                        # Generate a cutting command for iso to be applied on the plotting configuration board
                                        new_iso_cutting_command = ""

                                        for i in range(len(old_iso_values)):
                                            if i == len(old_iso_values) - 1:
                                                new_iso_cutting_command += str(old_iso_values[i])
                                            else:
                                                new_iso_cutting_command += str(old_iso_values[i]) + ";"

                                        # if self.isoExisted:
                                        #    self.plotting_board_reference.get_plot_parameter_manipulation_object().replace_iso_cutting_information_by_lom_file(new_iso_cutting_command)
                                        #else:
                                        #    self.isoExisted = True
                                        if not self.isoExisted:
                                            self.plottingBoardReference.get_plot_parameter_manipulation_object() \
                                                .set_iso_cutting_information_by_lom_file \
                                                (new_iso_cutting_command, plotting_context.get_iso_parameter_name_from_lom_file(old_ordinate_name, old_lomfile))
                                            self.isoExisted = True

                                        self.draw_on_canvas_using_lom_files(old_lomfile, old_ordinate_name, 2)
                                        self.setAxisTitle(QwtPlot.xBottom, "x")
                                        lom_function += "|| " + old_ordinate_name + " [" + plotting_context.get_abscissa_parameter_name_from_lom_file(old_ordinate_name, old_lomfile) + \
                                                        ", " + plotting_context.get_iso_parameter_name_from_lom_file(old_ordinate_name, old_lomfile) + "]"

                                    # Secondly, find if iso values of the label just has been dropped has to be enriched or not
                                    for iso in old_iso_values:
                                        if iso not in iso_values:
                                            iso_values.append(iso)
                                            iso_values.sort()
                                            pos = iso_values.index(iso)
                                            ordinate_values.insert(pos, [])
                                            iso_validity.insert(pos, 1)

                                    plotting_context.set_abscissa_parameter_name_from_lom_file(abscissa_name, ordinate_name, lomfile)
                                    plotting_context.set_abscissa_parameter_values_from_lom_file(abscissa_value, ordinate_name, lomfile)
                                    plotting_context.set_list_of_ordinate_parameter_name_from_lom_file(ordinate_name, ordinate_name, lomfile)
                                    plotting_context.set_list_of_ordinate_parameter_values_from_lom_file(ordinate_values, ordinate_name, lomfile)
                                    plotting_context.set_iso_parameter_name_from_lom_file(iso_name, ordinate_name, lomfile)
                                    plotting_context.set_iso_parameter_values_from_lom_file(iso_values, ordinate_name, lomfile)
                                    plotting_context.set_iso_parameter_validity_from_lom_file(iso_validity, ordinate_name, lomfile)
                                    plotting_context.set_label_dimension_from_lom_file(self.dimensionAdoptable, ordinate_name, lomfile)

                                    # self.isoExisted = False

                                    #if self.isoExisted:
                                    #self.plotting_board_reference.get_plot_parameter_manipulation_object().iso_range_check_list_changed()
                                    #else:
                                    #   self.isoExisted = True

                                    self.draw_on_canvas_using_lom_files(lomfile, ordinate_name, 2)
                                    self.plottingBoardReference.get_plot_parameter_manipulation_object().set_ordinate_config_table(lomfile, ordinate_name)
                                    self.plottingBoardReference.get_plot_parameter_manipulation_object().iso_range_check_list_changed()
                                    self.labelsDrawn.append((ordinate_name, lomfile))
                                    lom_function += "|| " + ordinate_name + " [" + abscissa_name + ", " + iso_name + "]"
                                    self.replot()

                                lom_functions = QwtText(lom_function)
                                lom_functions.setFont(self.font)
                                self.setAxisTitle(QwtPlot.xBottom, lom_functions)
                                self.labelSuperposeActionActivated = False

                            elif label.get_dimension() == 3:
                                abscissa_name = labels.getabsname(ordinate_name)
                                iso_name = labels.getisoname(ordinate_name)
                                siso_name = labels.getsisname(ordinate_name)
                                abscissa_value = list(labels.getabs(ordinate_name))
                                ordinate_values = []
                                for l in (labels.getord(ordinate_name)):
                                    ordinate_values.append(list(l))
                                iso_values = list(labels.getiso(ordinate_name))
                                siso_values = list(labels.getsis(ordinate_name))
                                iso_validity = list()
                                for _ in iso_values:
                                    iso_validity.append(1)
                                siso_validity = list()
                                for _ in siso_values:
                                    siso_validity.append(1)

                                if not self.labelSuperposeActionActivated:
                                    self.dimensionAdoptable = 3
                                    self.labelsDrawn.append((ordinate_name, lomfile))
                                    plotting_context.set_abscissa_parameter_name_from_lom_file(abscissa_name, ordinate_name, lomfile)
                                    plotting_context.set_abscissa_parameter_values_from_lom_file(abscissa_value, ordinate_name, lomfile)
                                    plotting_context.set_list_of_ordinate_parameter_name_from_lom_file(ordinate_name, ordinate_name, lomfile)
                                    plotting_context.set_list_of_ordinate_parameter_values_from_lom_file(ordinate_values, ordinate_name, lomfile)
                                    plotting_context.set_iso_parameter_name_from_lom_file(iso_name, ordinate_name, lomfile)
                                    plotting_context.set_iso_parameter_values_from_lom_file(iso_values, ordinate_name, lomfile)
                                    plotting_context.set_iso_parameter_validity_from_lom_file(iso_validity, ordinate_name, lomfile)
                                    plotting_context.set_siso_parameter_name_from_lom_file(siso_name, ordinate_name, lomfile)
                                    plotting_context.set_siso_parameter_values_from_lom_file(siso_values, ordinate_name, lomfile)
                                    plotting_context.set_siso_parameter_validity_from_lom_file(siso_validity, ordinate_name, lomfile)
                                    plotting_context.set_label_dimension_from_lom_file(label.get_dimension(), ordinate_name, lomfile)

                                    # Generate a cutting command for iso to be applied on the plotting configuration board
                                    new_iso_cutting_command = ""
                                    for i in range(len(iso_values)):
                                        if i == len(iso_values) - 1:
                                            new_iso_cutting_command += str(iso_values[i])
                                        else:
                                            new_iso_cutting_command += str(iso_values[i]) + ";"

                                    # Generate a cutting command for siso to be applied on the plotting configuration board
                                    new_siso_cutting_command = ""
                                    for i in range(len(siso_values)):
                                        if i == len(siso_values) - 1:
                                            new_siso_cutting_command += str(siso_values[i])
                                        else:
                                            new_siso_cutting_command += str(siso_values[i]) + ";"

                                    # if siso parameter existed already in the plotting context. we just update the cutting information
                                    # if not, we need to create a new one
                                    if self.sisoExisted:
                                        self.plottingBoardReference.get_plot_parameter_manipulation_object().replace_iso_cutting_information_by_lom_file(new_iso_cutting_command)
                                        self.plottingBoardReference.get_plot_parameter_manipulation_object().replace_siso_cutting_information_by_lom_file(new_siso_cutting_command)
                                    else:
                                        self.isoExisted = True
                                        self.sisoExisted = True
                                        self.plottingBoardReference.get_plot_parameter_manipulation_object().set_iso_cutting_information_by_lom_file(new_iso_cutting_command, iso_name)
                                        self.plottingBoardReference.get_plot_parameter_manipulation_object().set_siso_cutting_information_by_lom_file(new_siso_cutting_command, siso_name)

                                    # draw a new list of curves for lom
                                    lom_function += "LOM: " + ordinate_name + " [" + abscissa_name + ", " + iso_name + ", " + siso_name + "]"
                                    plotting_context.print_data_center()
                                    self.draw_on_canvas_using_lom_files(lomfile, ordinate_name, 3)
                                    self.plottingBoardReference.get_plot_parameter_manipulation_object().set_ordinate_config_table(lomfile, ordinate_name)
                                else:
                                    # firstly
                                    for pair in self.labelsDrawn:
                                        old_ordinate_name = pair[0]
                                        old_lomfile = pair[1]
                                        old_ordinate_values = plotting_context.get_list_of_ordinate_parameter_values_from_lom_file(old_ordinate_name, old_lomfile)
                                        old_iso_values = list(plotting_context.get_iso_parameter_values_from_lom_file(old_ordinate_name, old_lomfile))
                                        old_iso_validity = plotting_context.get_iso_parameter_validity_from_lom_file(old_ordinate_name, old_lomfile)
                                        old_siso_values = list(plotting_context.get_siso_parameter_values_from_lom_file(old_ordinate_name, old_lomfile))
                                        old_siso_validity = plotting_context.get_siso_parameter_validity_from_lom_file(old_ordinate_name, old_lomfile)

                                        # then, find if iso values of the label existed has to be enriched or not
                                        for iso in iso_values:
                                            if iso not in old_iso_values:
                                                old_iso_values.append(iso)
                                                old_iso_values.sort()
                                                pos = old_iso_values.index(iso)
                                                old_iso_validity.insert(pos, 1)

                                        for siso_index in range(len(siso_values)):
                                            if siso_values[siso_index] not in old_siso_values:
                                                old_siso_values.append(siso_values[siso_index])
                                                old_siso_values.sort()
                                                pos = old_siso_values.index(siso_values[siso_index])
                                                old_siso_validity.insert(pos, 1)
                                                old_ordinate_values.insert(pos, [])
                                                for _ in old_iso_values:
                                                    old_ordinate_values[pos].append([])
                                            else:
                                                for iso in iso_values:
                                                    if iso not in old_iso_values:
                                                        pos = old_iso_values.index(iso)
                                                        old_ordinate_values[siso_index].insert(pos, [])

                                        plotting_context.set_list_of_ordinate_parameter_values_from_lom_file(old_ordinate_values, old_ordinate_name, old_lomfile)
                                        plotting_context.set_iso_parameter_values_from_lom_file(old_iso_values, old_ordinate_name, old_lomfile)
                                        plotting_context.set_iso_parameter_validity_from_lom_file(old_iso_validity, old_ordinate_name, old_lomfile)
                                        plotting_context.set_siso_parameter_values_from_lom_file(old_siso_values, old_ordinate_name, old_lomfile)
                                        plotting_context.set_siso_parameter_validity_from_lom_file(old_siso_validity, old_ordinate_name, old_lomfile)

                                        # renew the curves on the plotting board which represent this label
                                        self.clean_before_replot()
                                        self.plottingBoardReference.get_plot_parameter_manipulation_object().clean_all_component(False)
                                        self.sisoExisted = False
                                        del self.curves_center['lom'][old_lomfile][old_ordinate_name]

                                        # Generate a cutting command for iso to be applied on the plotting configuration board
                                        new_iso_cutting_command = ""
                                        for i in range(len(old_iso_values)):
                                            if i == len(old_iso_values) - 1:
                                                new_iso_cutting_command += str(old_iso_values[i])
                                            else:
                                                new_iso_cutting_command += str(old_iso_values[i]) + ";"

                                        # Generate a cutting command for siso to be applied on the plotting configuration board
                                        new_siso_cutting_command = ""
                                        for i in range(len(old_siso_values)):
                                            if i == len(old_siso_values) - 1:
                                                new_siso_cutting_command += str(old_siso_values[i])
                                            else:
                                                new_siso_cutting_command += str(old_siso_values[i]) + ";"

                                        # if siso parameter existed already in the plotting context. we just update the cutting information
                                        # if not, we need to create a new one
                                        if self.sisoExisted:
                                            self.plottingBoardReference.get_plot_parameter_manipulation_object().replace_iso_cutting_information_by_lom_file(new_iso_cutting_command)
                                            self.plottingBoardReference.get_plot_parameter_manipulation_object().replace_siso_cutting_information_by_lom_file(new_siso_cutting_command)
                                        else:
                                            self.isoExisted = True
                                            self.sisoExisted = True
                                            self.plottingBoardReference.get_plot_parameter_manipulation_object(). \
                                                set_iso_cutting_information_by_lom_file(new_iso_cutting_command,
                                                                                        plotting_context.get_iso_parameter_name_from_lom_file(old_ordinate_name, old_lomfile))
                                            self.plottingBoardReference.get_plot_parameter_manipulation_object(). \
                                                set_siso_cutting_information_by_lom_file(new_siso_cutting_command,
                                                                                         plotting_context.get_siso_parameter_name_from_lom_file(old_ordinate_name, old_lomfile))

                                        # draw a new list of curves for lom
                                        self.draw_on_canvas_using_lom_files(old_lomfile, old_ordinate_name, 3)
                                        lom_function += " || " + old_ordinate_name + " [" + plotting_context.get_abscissa_parameter_name_from_lom_file(old_ordinate_name, old_lomfile) + \
                                                        ", " + plotting_context.get_iso_parameter_name_from_lom_file(old_ordinate_name, old_lomfile) + \
                                                        ", " + plotting_context.get_siso_parameter_name_from_lom_file(old_ordinate_name, old_lomfile) + "]"

                                    # Secondly, find if iso values of the label just has been dropped has to be enriched or not
                                    for iso in old_iso_values:
                                        if iso not in iso_values:
                                            iso_values.append(iso)
                                            iso_values.sort()
                                            pos = iso_values.index(iso)
                                            iso_validity.insert(pos, 1)

                                    for siso_index in range(len(old_siso_values)):
                                        if old_siso_values[siso_index] not in siso_values:
                                            siso_values.append(old_siso_values[siso_index])
                                            siso_values.sort()
                                            pos = siso_values.index(old_siso_values[siso_index])
                                            siso_validity.insert(pos, 1)
                                            ordinate_values.insert(pos, [])
                                            for _ in iso_values:
                                                ordinate_values[pos].append([])
                                        else:
                                            for iso in old_iso_values:
                                                if iso not in iso_values:
                                                    pos = iso_values.index(iso)
                                                    ordinate_values[siso_index].insert(pos, [])

                                    plotting_context.set_abscissa_parameter_name_from_lom_file(abscissa_name, ordinate_name, lomfile)
                                    plotting_context.set_abscissa_parameter_values_from_lom_file(abscissa_value, ordinate_name, lomfile)
                                    plotting_context.set_list_of_ordinate_parameter_name_from_lom_file(ordinate_name, ordinate_name, lomfile)
                                    plotting_context.set_list_of_ordinate_parameter_values_from_lom_file(ordinate_values, ordinate_name, lomfile)
                                    plotting_context.set_iso_parameter_name_from_lom_file(iso_name, ordinate_name, lomfile)
                                    plotting_context.set_iso_parameter_values_from_lom_file(iso_values, ordinate_name, lomfile)
                                    plotting_context.set_iso_parameter_validity_from_lom_file(iso_validity, ordinate_name, lomfile)
                                    plotting_context.set_siso_parameter_name_from_lom_file(siso_name, ordinate_name, lomfile)
                                    plotting_context.set_siso_parameter_values_from_lom_file(siso_values, ordinate_name, lomfile)
                                    plotting_context.set_siso_parameter_validity_from_lom_file(siso_validity, ordinate_name, lomfile)
                                    plotting_context.set_label_dimension_from_lom_file(label.get_dimension(), ordinate_name, lomfile)

                                    self.sisoExisted = False
                                    # if siso parameter existed already in the plotting context. we just update the cutting information
                                    # if not, we need to create a new one
                                    if self.sisoExisted:
                                        self.plottingBoardReference.get_plot_parameter_manipulation_object().siso_range_check_list_changed()
                                    else:
                                        self.isoExisted = True
                                        self.sisoExisted = True

                                    # draw a new list of curves for lom
                                    lom_function += " || " + ordinate_name + " [" + abscissa_name + ", " + iso_name + ", " + siso_name + "]"
                                    self.draw_on_canvas_using_lom_files(lomfile, ordinate_name, 3)
                                    self.plottingBoardReference.get_plot_parameter_manipulation_object().set_ordinate_config_table(lomfile, ordinate_name)
                                    self.labelsDrawn.append((ordinate_name, lomfile))

                                lom_functions = QwtText(lom_function)
                                lom_functions.setFont(self.font)
                                self.setAxisTitle(QwtPlot.xBottom, lom_functions)
                                self.labelSuperposeActionActivated = False
                            self.plottingBoardReference.get_plot_parameter_manipulation_object().set_lom_existed()
                            self.plottingBoardReference.get_parent().get_parent().parent().parent().get_status_bar_reference().display_message(lom_function)

                        else:
                            # QMessageBox.question(self, 'Message', "this label has been imported already")
                            self.plottingBoardReference.get_parent().get_parent().parent().parent().get_status_bar_reference(). \
                                display_error_message("this label has been imported already")
                else:
                    QMessageBox.question(self, 'Message', "No lom file loaded right now")

    def drop_event_while_import(self, parameter_name, axis, label_flag):
        page_index = self.plottingBoardReference.get_page_index()
        plotting_index = self.plottingBoardReference.get_plotting_index()
        plotting_context = self.analyseurMediator.get_a_plotting_context(page_index, plotting_index)

        y_value_pointer = -1
        ordinate_name = ''
        # If we work with the csv file currently
        if self.analyseurMediator.get_filetype_handling_from_context() == "csv":

            # Need_to_draw is a parameter who decide if it is ready to plotting, which means the curve can be drawn at least if the abscissa and ordinate's ready
            need_to_replot = False

            if axis == 'abscissa':
                self.analyseurMediator.generate_an_action_into_global_context('drop parameter: ' + parameter_name + ' as abscissa'
                                                                              + ' for plotting board :'
                                                                              + str(self.plottingBoardReference.get_plotting_index()) + ' in page: '
                                                                              + str(self.plottingBoardReference.get_page_index()))
                # Fetch the list of the loaded csv file's names
                page_index = self.plottingBoardReference.get_page_index()
                plotting_index = self.plottingBoardReference.get_plotting_index()
                loaded_csvfiles = self.analyseurMediator.get_loaded_csv_files_from_context(page_index, plotting_index)
                loaded_csvfiles_validity = self.analyseurMediator.get_loaded_csv_files_validity_from_context(page_index, plotting_index)

                # For each csv file's name, firstly to check if the parameter has been already set as the abscissa in the csv file tree,
                # if not, set the value list into this csv tree structure
                if len(loaded_csvfiles) > 0:

                    for csvfile in loaded_csvfiles:
                        # if not loaded_csvfiles_validity[loaded_csvfiles.index(csvfile)]:
                        # continue
                        current_file = self.analyseurMediator.get_csv_file_in_context_by_name(csvfile)
                        values = current_file.get_values()
                        list_of_titles = current_file.get_title_list()
                        rowcount = current_file.get_row_count()

                        # check if the current file contains the parameter with the name dropped
                        if parameter_name not in list_of_titles:
                            loaded_csvfiles_validity[loaded_csvfiles.index(csvfile)] = 0
                            continue

                        loaded_csvfiles_validity[loaded_csvfiles.index(csvfile)] = 1

                        # check if the plotting context related has the abscissa value with the same name in order to avoid do the same thing a second time
                        if parameter_name == plotting_context.get_abscissa_parameter_name(csvfile):
                            print 'this parameter existed already in the abscissa in file', csvfile
                            return
                        else:
                            if plotting_context.get_abscissa_parameter_name(csvfile) == "":
                                self.abscissa_name = str(parameter_name)
                                plotting_context.set_abscissa_parameter_name(self.abscissa_name, csvfile)

                                try:
                                    abscissa_value_pointer = list_of_titles.index(plotting_context.get_abscissa_parameter_name(csvfile))
                                    abscissa_value_list = plotting_context.get_abscissa_parameter_values(csvfile)
                                    del abscissa_value_list[:]
                                    if self.abscissa_name == 'GMT':
                                        for k in range(rowcount):
                                            abscissa_value_list.append(k)
                                    else:
                                        for i in range(rowcount):
                                            abscissa_value_list.append(values[i][abscissa_value_pointer])
                                except ValueError:
                                    continue
                            else:
                                # TODO Need to update all the curve with the new abscissa list
                                print "let us do it"
                else:
                    QMessageBox.question(self, 'Message', "No csv file loaded right now")

            # If the choice is to apply the parameter's information to the ordinate axis
            elif axis == 'ordinate':
                self.analyseurMediator.generate_an_action_into_global_context('drop parameter: ' + parameter_name + ' as ordinate'
                                                                              + ' for plotting board :'
                                                                              + str(self.plottingBoardReference.get_plotting_index()) + ' in page: '
                                                                              + str(self.plottingBoardReference.get_page_index()))

                ordinate_name = str(parameter_name)

                # Fetch the list of the csv file's names
                page_index = self.plottingBoardReference.get_page_index()
                plotting_index = self.plottingBoardReference.get_plotting_index()
                loaded_csvfiles = self.analyseurMediator.get_loaded_csv_files_from_context(page_index, plotting_index)
                loaded_csvfiles_validity = self.analyseurMediator.get_loaded_csv_files_validity_from_context(page_index, plotting_index)

                y_values_list = [[] for _ in range(len(loaded_csvfiles))]
                cpt = 0

                # For each csv file's name, firstly to check if the parameter has been already set as the ordinate in the csv file tree,
                # if not, set the value list into this vsv tree structure
                if len(loaded_csvfiles) > 0:

                    for csvfile in loaded_csvfiles:
                        # if not loaded_csvfiles_validity[loaded_csvfiles.index(csvfile)]:
                        # continue
                        current_file = self.analyseurMediator.get_csv_file_in_context_by_name(csvfile)
                        values = current_file.get_values()
                        list_of_titles = current_file.get_title_list()
                        rowcount = current_file.get_row_count()

                        # check if the current file contains the parameter with the name dropped
                        if ordinate_name not in list_of_titles:
                            loaded_csvfiles_validity[loaded_csvfiles.index(csvfile)] = 0
                            continue

                        loaded_csvfiles_validity[loaded_csvfiles.index(csvfile)] = 1

                        if ordinate_name in plotting_context.get_list_of_ordinate_parameter_name(csvfile):
                            print 'this parameter existed already in the list of ordinate in file', csvfile
                            return
                        else:
                            need_to_replot = True

                            # firstly, we have to check if the abscissa name applied existed in the current file's parameter list
                            # so that, we can decide whether need to fetch the ordinate's value list or not
                            if (self.abscissa_name in list_of_titles) or (self.abscissa_name == ""):
                                try:
                                    y_value_pointer = list_of_titles.index(ordinate_name)

                                    if ordinate_name == 'GMT':
                                        for k in range(rowcount):
                                            y_values_list[cpt].append(k)
                                    else:
                                        for k in range(rowcount):
                                            y_values_list[cpt].append(values[k][y_value_pointer])
                                except ValueError:
                                    print "not existed"
                                    continue
                            else:
                                QMessageBox.question(self, 'Message', "The file:" + csvfile + " doesn't existed the abscissa" + self.abscissa_name)

                        if y_value_pointer >= 0:
                            plotting_context.set_list_of_ordinate_parameter_name(ordinate_name, csvfile)
                            plotting_context.set_list_of_ordinate_parameter_values(y_values_list[cpt], csvfile)
                        cpt += 1
                        y_value_pointer = -1
                else:
                    QMessageBox.question(self, 'Message', "No csv file loaded right now")

            # If we need to update the curves on the canvas, just do it
            if need_to_replot:
                for csv_file_name in loaded_csvfiles:
                    if not loaded_csvfiles_validity[loaded_csvfiles.index(csv_file_name)]:
                        continue
                    if (plotting_context.get_abscissa_parameter_name(csv_file_name) != "") and (len(plotting_context.get_list_of_ordinate_parameter_name(csv_file_name)) > 0):
                        self.draw_on_canvas_using_csv_files(csv_file_name, ordinate_name, self.abscissa_name)
                        # break

        # If we work with the lom file currently
        elif self.analyseurMediator.get_filetype_handling_from_context() == "lom":

            ordinate_name = str(parameter_name)

            # Fetch the list of the loaded lom file's names and its validity in the global context through the page index and the canvas index number
            page_index = self.plottingBoardReference.get_page_index()
            plotting_index = self.plottingBoardReference.get_plotting_index()
            loaded_lomfiles = self.analyseurMediator.get_loaded_lom_files_from_context(page_index, plotting_index)
            loaded_lomfiles_validity = self.analyseurMediator.get_loaded_lom_files_validity_from_context(page_index, plotting_index)

            if len(loaded_lomfiles) > 0:
                for lomfile in loaded_lomfiles:
                    # Get the current lom file object
                    print lomfile
                    current_file = self.analyseurMediator.get_lom_file_in_context_by_name(lomfile)

                    # get a reference of all the labels in the lom file objects
                    labels = current_file.get_labels()

                    # get a reference of the label object
                    label = labels.getlab(parameter_name)

                    if label == -1:
                        print label
                        continue

                    # check if the current file contains the parameter with the name dropped, if not, pass this turn of loop
                    if label == -1:
                        loaded_lomfiles_validity[loaded_lomfiles.index(lomfile)] = 0
                        continue

                    # check the dimension of the label which has been plotted before, if existed.
                    # if it is different, let user decide to update the label or cancel the drop action
                    if (self.dimensionAdoptable != 0) and (self.dimensionAdoptable != label.get_dimension()):
                        self.plottingBoardReference.self_cleaning()
                        self.analyseurMediator.generate_an_action_into_global_context('drop label: ' + ordinate_name + ' to replace'
                                                                                      + ' for plotting board :'
                                                                                      + str(self.plottingBoardReference.get_plotting_index()) + ' in page: '
                                                                                      + str(self.plottingBoardReference.get_page_index()))

                    elif (self.dimensionAdoptable != 0) and (self.dimensionAdoptable == label.get_dimension()):
                        self.labelSuperposeActionActivated = True
                        self.analyseurMediator.generate_an_action_into_global_context('drop label: ' + ordinate_name + ' to superpose'
                                                                                      + ' for plotting board :'
                                                                                      + str(self.plottingBoardReference.get_plotting_index()) + ' in page: '
                                                                                      + str(self.plottingBoardReference.get_page_index()))
                    else:
                        print label_flag
                        self.analyseurMediator.generate_an_action_into_global_context('drop label: ' + ordinate_name + ' the first time'
                                                                                      + ' for plotting board :'
                                                                                      + str(self.plottingBoardReference.get_plotting_index()) + ' in page: '
                                                                                      + str(self.plottingBoardReference.get_page_index()))

                    loaded_lomfiles_validity[loaded_lomfiles.index(lomfile)] = 1

                    lom_function = ""

                    # Set the label into the plotting context to produce a new tree structure of label. if existed already, reject.
                    if plotting_context.set_label_to_lom_files(ordinate_name, lomfile):

                        # check the dimension of the label dropped
                        # if y = f(x)
                        if label.get_dimension() == 1:

                            # set the dimension adoptable for the plotting
                            self.dimensionAdoptable = 1

                            # fetch the values associated
                            abscissa_name = labels.getabsname(ordinate_name)
                            abscissa_value = labels.getabs(ordinate_name)
                            ordinate_values = labels.getord(ordinate_name)

                            self.labelsDrawn.append((ordinate_name, lomfile))

                            # write the values above into the plotting context associated to the plotting
                            plotting_context.set_abscissa_parameter_name_from_lom_file(abscissa_name, ordinate_name, lomfile)
                            plotting_context.set_abscissa_parameter_values_from_lom_file(abscissa_value, ordinate_name, lomfile)
                            plotting_context.set_list_of_ordinate_parameter_name_from_lom_file(ordinate_name, ordinate_name, lomfile)
                            plotting_context.set_list_of_ordinate_parameter_values_from_lom_file(ordinate_values, ordinate_name, lomfile)
                            plotting_context.set_label_dimension_from_lom_file(label.get_dimension(), ordinate_name, lomfile)

                            # draw...
                            self.draw_on_canvas_using_lom_files(lomfile, ordinate_name, 1)
                            self.plottingBoardReference.get_plot_parameter_manipulation_object().set_ordinate_config_table(lomfile, ordinate_name)

                            # lom function to be displayed
                            lom_function += " ||: " + ordinate_name + " [" + abscissa_name + "]"

                        # if y = f(x, z)
                        elif label.get_dimension() == 2:

                            # fetch the values associated
                            # abscissa
                            abscissa_name = labels.getabsname(ordinate_name)
                            abscissa_value = list(labels.getabs(ordinate_name))

                            print type(labels.getord(ordinate_name))
                            print labels.getord(ordinate_name)
                            # ordinate
                            ordinate_values = []
                            for l in (labels.getord(ordinate_name)):
                                ordinate_values.append(list(l))

                            # iso
                            iso_name = labels.getisoname(ordinate_name)
                            iso_values = list(labels.getiso(ordinate_name))
                            iso_validity = list()
                            for _ in iso_values:
                                iso_validity.append(1)

                            # check if it is the normal lom plotting action, or its a superpose action
                            if not self.labelSuperposeActionActivated:
                                self.labelsDrawn.append((ordinate_name, lomfile))
                                self.dimensionAdoptable = 2

                                plotting_context.set_abscissa_parameter_name_from_lom_file(abscissa_name, ordinate_name, lomfile)
                                plotting_context.set_abscissa_parameter_values_from_lom_file(abscissa_value, ordinate_name, lomfile)
                                plotting_context.set_list_of_ordinate_parameter_name_from_lom_file(ordinate_name, ordinate_name, lomfile)
                                plotting_context.set_list_of_ordinate_parameter_values_from_lom_file(ordinate_values, ordinate_name, lomfile)
                                plotting_context.set_iso_parameter_name_from_lom_file(iso_name, ordinate_name, lomfile)
                                plotting_context.set_iso_parameter_values_from_lom_file(iso_values, ordinate_name, lomfile)
                                plotting_context.set_iso_parameter_validity_from_lom_file(iso_validity, ordinate_name, lomfile)
                                plotting_context.set_label_dimension_from_lom_file(self.dimensionAdoptable, ordinate_name, lomfile)

                                # Generate a cutting command for iso to be applied on the plotting configuration board
                                new_iso_cutting_command = ""

                                for i in range(len(iso_values)):
                                    if i == len(iso_values) - 1:
                                        new_iso_cutting_command += str(iso_values[i])
                                    else:
                                        new_iso_cutting_command += str(iso_values[i]) + ";"

                                if self.isoExisted:
                                    self.plottingBoardReference.get_plot_parameter_manipulation_object().replace_iso_cutting_information_by_lom_file(new_iso_cutting_command)
                                else:
                                    self.isoExisted = True
                                    self.plottingBoardReference.get_plot_parameter_manipulation_object().set_iso_cutting_information_by_lom_file(new_iso_cutting_command, iso_name)

                                self.draw_on_canvas_using_lom_files(lomfile, ordinate_name, 2)
                                self.plottingBoardReference.get_plot_parameter_manipulation_object().set_ordinate_config_table(lomfile, ordinate_name)
                                lom_function += "LOM: " + ordinate_name + " [" + abscissa_name + ", " + iso_name + "]"
                            else:
                                # firstly
                                for pair in self.labelsDrawn:
                                    old_ordinate_name = pair[0]
                                    old_lomfile = pair[1]
                                    old_ordinate_values = plotting_context.get_list_of_ordinate_parameter_values_from_lom_file(old_ordinate_name, old_lomfile)
                                    old_iso_values = list(plotting_context.get_iso_parameter_values_from_lom_file(old_ordinate_name, old_lomfile))
                                    old_iso_validity = plotting_context.get_iso_parameter_validity_from_lom_file(old_ordinate_name, old_lomfile)

                                    # then, find if iso values of the label existed has to be enriched or not
                                    for iso in iso_values:
                                        if iso not in old_iso_values:
                                            old_iso_values.append(iso)
                                            old_iso_values.sort()
                                            pos = old_iso_values.index(iso)
                                            old_iso_validity.insert(pos, 1)
                                            old_ordinate_values.insert(pos, [])

                                    plotting_context.set_list_of_ordinate_parameter_values_from_lom_file(old_ordinate_values, old_ordinate_name, old_lomfile)
                                    plotting_context.set_iso_parameter_values_from_lom_file(old_iso_values, old_ordinate_name, old_lomfile)
                                    plotting_context.set_iso_parameter_validity_from_lom_file(old_iso_validity, old_ordinate_name, old_lomfile)

                                    # renew the curves on the plotting board which represent this label
                                    self.clean_before_replot()
                                    self.plottingBoardReference.get_plot_parameter_manipulation_object().clean_all_component(False)
                                    self.isoExisted = False
                                    del self.curves_center['lom'][old_lomfile][old_ordinate_name]

                                    # Generate a cutting command for iso to be applied on the plotting configuration board
                                    new_iso_cutting_command = ""

                                    for i in range(len(old_iso_values)):
                                        if i == len(old_iso_values) - 1:
                                            new_iso_cutting_command += str(old_iso_values[i])
                                        else:
                                            new_iso_cutting_command += str(old_iso_values[i]) + ";"

                                    # if self.isoExisted:
                                    #    self.plotting_board_reference.get_plot_parameter_manipulation_object().replace_iso_cutting_information_by_lom_file(new_iso_cutting_command)
                                    #else:
                                    #    self.isoExisted = True
                                    if not self.isoExisted:
                                        self.plottingBoardReference.get_plot_parameter_manipulation_object() \
                                            .set_iso_cutting_information_by_lom_file \
                                            (new_iso_cutting_command, plotting_context.get_iso_parameter_name_from_lom_file(old_ordinate_name, old_lomfile))
                                        self.isoExisted = True

                                    self.draw_on_canvas_using_lom_files(old_lomfile, old_ordinate_name, 2)
                                    self.setAxisTitle(QwtPlot.xBottom, "x")
                                    lom_function += "|| " + old_ordinate_name + " [" + plotting_context.get_abscissa_parameter_name_from_lom_file(old_ordinate_name, old_lomfile) + \
                                                    ", " + plotting_context.get_iso_parameter_name_from_lom_file(old_ordinate_name, old_lomfile) + "]"

                                # Secondly, find if iso values of the label just has been dropped has to be enriched or not
                                for iso in old_iso_values:
                                    if iso not in iso_values:
                                        iso_values.append(iso)
                                        iso_values.sort()
                                        pos = iso_values.index(iso)
                                        ordinate_values.insert(pos, [])
                                        iso_validity.insert(pos, 1)

                                plotting_context.set_abscissa_parameter_name_from_lom_file(abscissa_name, ordinate_name, lomfile)
                                plotting_context.set_abscissa_parameter_values_from_lom_file(abscissa_value, ordinate_name, lomfile)
                                plotting_context.set_list_of_ordinate_parameter_name_from_lom_file(ordinate_name, ordinate_name, lomfile)
                                plotting_context.set_list_of_ordinate_parameter_values_from_lom_file(ordinate_values, ordinate_name, lomfile)
                                plotting_context.set_iso_parameter_name_from_lom_file(iso_name, ordinate_name, lomfile)
                                plotting_context.set_iso_parameter_values_from_lom_file(iso_values, ordinate_name, lomfile)
                                plotting_context.set_iso_parameter_validity_from_lom_file(iso_validity, ordinate_name, lomfile)
                                plotting_context.set_label_dimension_from_lom_file(self.dimensionAdoptable, ordinate_name, lomfile)

                                # self.isoExisted = False

                                #if self.isoExisted:
                                #self.plotting_board_reference.get_plot_parameter_manipulation_object().iso_range_check_list_changed()
                                #else:
                                #   self.isoExisted = True

                                self.draw_on_canvas_using_lom_files(lomfile, ordinate_name, 2)
                                self.plottingBoardReference.get_plot_parameter_manipulation_object().set_ordinate_config_table(lomfile, ordinate_name)
                                self.plottingBoardReference.get_plot_parameter_manipulation_object().iso_range_check_list_changed()
                                self.labelsDrawn.append((ordinate_name, lomfile))
                                lom_function += "|| " + ordinate_name + " [" + abscissa_name + ", " + iso_name + "]"
                                self.replot()

                            lom_functions = QwtText(lom_function)
                            lom_functions.setFont(self.font)
                            self.setAxisTitle(QwtPlot.xBottom, lom_functions)
                            self.labelSuperposeActionActivated = False

                        elif label.get_dimension() == 3:
                            abscissa_name = labels.getabsname(ordinate_name)
                            iso_name = labels.getisoname(ordinate_name)
                            siso_name = labels.getsisname(ordinate_name)
                            abscissa_value = list(labels.getabs(ordinate_name))
                            ordinate_values = []
                            for l in (labels.getord(ordinate_name)):
                                ordinate_values.append(list(l))
                            iso_values = list(labels.getiso(ordinate_name))
                            siso_values = list(labels.getsis(ordinate_name))
                            iso_validity = list()
                            for _ in iso_values:
                                iso_validity.append(1)
                            siso_validity = list()
                            for _ in siso_values:
                                siso_validity.append(1)

                            if not self.labelSuperposeActionActivated:
                                self.dimensionAdoptable = 3
                                self.labelsDrawn.append((ordinate_name, lomfile))
                                plotting_context.set_abscissa_parameter_name_from_lom_file(abscissa_name, ordinate_name, lomfile)
                                plotting_context.set_abscissa_parameter_values_from_lom_file(abscissa_value, ordinate_name, lomfile)
                                plotting_context.set_list_of_ordinate_parameter_name_from_lom_file(ordinate_name, ordinate_name, lomfile)
                                plotting_context.set_list_of_ordinate_parameter_values_from_lom_file(ordinate_values, ordinate_name, lomfile)
                                plotting_context.set_iso_parameter_name_from_lom_file(iso_name, ordinate_name, lomfile)
                                plotting_context.set_iso_parameter_values_from_lom_file(iso_values, ordinate_name, lomfile)
                                plotting_context.set_iso_parameter_validity_from_lom_file(iso_validity, ordinate_name, lomfile)
                                plotting_context.set_siso_parameter_name_from_lom_file(siso_name, ordinate_name, lomfile)
                                plotting_context.set_siso_parameter_values_from_lom_file(siso_values, ordinate_name, lomfile)
                                plotting_context.set_siso_parameter_validity_from_lom_file(siso_validity, ordinate_name, lomfile)
                                plotting_context.set_label_dimension_from_lom_file(label.get_dimension(), ordinate_name, lomfile)

                                # Generate a cutting command for iso to be applied on the plotting configuration board
                                new_iso_cutting_command = ""
                                for i in range(len(iso_values)):
                                    if i == len(iso_values) - 1:
                                        new_iso_cutting_command += str(iso_values[i])
                                    else:
                                        new_iso_cutting_command += str(iso_values[i]) + ";"

                                # Generate a cutting command for siso to be applied on the plotting configuration board
                                new_siso_cutting_command = ""
                                for i in range(len(siso_values)):
                                    if i == len(siso_values) - 1:
                                        new_siso_cutting_command += str(siso_values[i])
                                    else:
                                        new_siso_cutting_command += str(siso_values[i]) + ";"

                                # if siso parameter existed already in the plotting context. we just update the cutting information
                                # if not, we need to create a new one
                                if self.sisoExisted:
                                    self.plottingBoardReference.get_plot_parameter_manipulation_object().replace_iso_cutting_information_by_lom_file(new_iso_cutting_command)
                                    self.plottingBoardReference.get_plot_parameter_manipulation_object().replace_siso_cutting_information_by_lom_file(new_siso_cutting_command)
                                else:
                                    self.isoExisted = True
                                    self.sisoExisted = True
                                    self.plottingBoardReference.get_plot_parameter_manipulation_object().set_iso_cutting_information_by_lom_file(new_iso_cutting_command, iso_name)
                                    self.plottingBoardReference.get_plot_parameter_manipulation_object().set_siso_cutting_information_by_lom_file(new_siso_cutting_command, siso_name)

                                # draw a new list of curves for lom
                                lom_function += "LOM: " + ordinate_name + " [" + abscissa_name + ", " + iso_name + ", " + siso_name + "]"
                                self.draw_on_canvas_using_lom_files(lomfile, ordinate_name, 3)
                                self.plottingBoardReference.get_plot_parameter_manipulation_object().set_ordinate_config_table(lomfile, ordinate_name)
                            else:
                                # firstly
                                for pair in self.labelsDrawn:
                                    old_ordinate_name = pair[0]
                                    old_lomfile = pair[1]
                                    old_ordinate_values = plotting_context.get_list_of_ordinate_parameter_values_from_lom_file(old_ordinate_name, old_lomfile)
                                    old_iso_values = list(plotting_context.get_iso_parameter_values_from_lom_file(old_ordinate_name, old_lomfile))
                                    old_iso_validity = plotting_context.get_iso_parameter_validity_from_lom_file(old_ordinate_name, old_lomfile)
                                    old_siso_values = list(plotting_context.get_siso_parameter_values_from_lom_file(old_ordinate_name, old_lomfile))
                                    old_siso_validity = plotting_context.get_siso_parameter_validity_from_lom_file(old_ordinate_name, old_lomfile)

                                    # then, find if iso values of the label existed has to be enriched or not
                                    for iso in iso_values:
                                        if iso not in old_iso_values:
                                            old_iso_values.append(iso)
                                            old_iso_values.sort()
                                            pos = old_iso_values.index(iso)
                                            old_iso_validity.insert(pos, 1)

                                    for siso_index in range(len(siso_values)):
                                        if siso_values[siso_index] not in old_siso_values:
                                            old_siso_values.append(siso_values[siso_index])
                                            old_siso_values.sort()
                                            pos = old_siso_values.index(siso_values[siso_index])
                                            old_siso_validity.insert(pos, 1)
                                            old_ordinate_values.insert(pos, [])
                                            for _ in old_iso_values:
                                                old_ordinate_values[pos].append([])
                                        else:
                                            for iso in iso_values:
                                                if iso not in old_iso_values:
                                                    pos = old_iso_values.index(iso)
                                                    old_ordinate_values[siso_index].insert(pos, [])

                                    plotting_context.set_list_of_ordinate_parameter_values_from_lom_file(old_ordinate_values, old_ordinate_name, old_lomfile)
                                    plotting_context.set_iso_parameter_values_from_lom_file(old_iso_values, old_ordinate_name, old_lomfile)
                                    plotting_context.set_iso_parameter_validity_from_lom_file(old_iso_validity, old_ordinate_name, old_lomfile)
                                    plotting_context.set_siso_parameter_values_from_lom_file(old_siso_values, old_ordinate_name, old_lomfile)
                                    plotting_context.set_siso_parameter_validity_from_lom_file(old_siso_validity, old_ordinate_name, old_lomfile)

                                    # renew the curves on the plotting board which represent this label
                                    self.clean_before_replot()
                                    self.plottingBoardReference.get_plot_parameter_manipulation_object().clean_all_component(False)
                                    self.sisoExisted = False
                                    del self.curves_center['lom'][old_lomfile][old_ordinate_name]

                                    # Generate a cutting command for iso to be applied on the plotting configuration board
                                    new_iso_cutting_command = ""
                                    for i in range(len(old_iso_values)):
                                        if i == len(old_iso_values) - 1:
                                            new_iso_cutting_command += str(old_iso_values[i])
                                        else:
                                            new_iso_cutting_command += str(old_iso_values[i]) + ";"

                                    # Generate a cutting command for siso to be applied on the plotting configuration board
                                    new_siso_cutting_command = ""
                                    for i in range(len(old_siso_values)):
                                        if i == len(old_siso_values) - 1:
                                            new_siso_cutting_command += str(old_siso_values[i])
                                        else:
                                            new_siso_cutting_command += str(old_siso_values[i]) + ";"

                                    # if siso parameter existed already in the plotting context. we just update the cutting information
                                    # if not, we need to create a new one
                                    if self.sisoExisted:
                                        self.plottingBoardReference.get_plot_parameter_manipulation_object().replace_iso_cutting_information_by_lom_file(new_iso_cutting_command)
                                        self.plottingBoardReference.get_plot_parameter_manipulation_object().replace_siso_cutting_information_by_lom_file(new_siso_cutting_command)
                                    else:
                                        self.isoExisted = True
                                        self.sisoExisted = True
                                        self.plottingBoardReference.get_plot_parameter_manipulation_object(). \
                                            set_iso_cutting_information_by_lom_file(new_iso_cutting_command,
                                                                                    plotting_context.get_iso_parameter_name_from_lom_file(old_ordinate_name, old_lomfile))
                                        self.plottingBoardReference.get_plot_parameter_manipulation_object(). \
                                            set_siso_cutting_information_by_lom_file(new_siso_cutting_command,
                                                                                     plotting_context.get_siso_parameter_name_from_lom_file(old_ordinate_name, old_lomfile))

                                    # draw a new list of curves for lom
                                    self.draw_on_canvas_using_lom_files(old_lomfile, old_ordinate_name, 3)
                                    lom_function += " || " + old_ordinate_name + " [" + plotting_context.get_abscissa_parameter_name_from_lom_file(old_ordinate_name, old_lomfile) + \
                                                    ", " + plotting_context.get_iso_parameter_name_from_lom_file(old_ordinate_name, old_lomfile) + \
                                                    ", " + plotting_context.get_siso_parameter_name_from_lom_file(old_ordinate_name, old_lomfile) + "]"

                                # Secondly, find if iso values of the label just has been dropped has to be enriched or not
                                for iso in old_iso_values:
                                    if iso not in iso_values:
                                        iso_values.append(iso)
                                        iso_values.sort()
                                        pos = iso_values.index(iso)
                                        iso_validity.insert(pos, 1)

                                for siso_index in range(len(old_siso_values)):
                                    if old_siso_values[siso_index] not in siso_values:
                                        siso_values.append(old_siso_values[siso_index])
                                        siso_values.sort()
                                        pos = siso_values.index(old_siso_values[siso_index])
                                        siso_validity.insert(pos, 1)
                                        ordinate_values.insert(pos, [])
                                        for _ in iso_values:
                                            ordinate_values[pos].append([])
                                    else:
                                        for iso in old_iso_values:
                                            if iso not in iso_values:
                                                pos = iso_values.index(iso)
                                                ordinate_values[siso_index].insert(pos, [])

                                plotting_context.set_abscissa_parameter_name_from_lom_file(abscissa_name, ordinate_name, lomfile)
                                plotting_context.set_abscissa_parameter_values_from_lom_file(abscissa_value, ordinate_name, lomfile)
                                plotting_context.set_list_of_ordinate_parameter_name_from_lom_file(ordinate_name, ordinate_name, lomfile)
                                plotting_context.set_list_of_ordinate_parameter_values_from_lom_file(ordinate_values, ordinate_name, lomfile)
                                plotting_context.set_iso_parameter_name_from_lom_file(iso_name, ordinate_name, lomfile)
                                plotting_context.set_iso_parameter_values_from_lom_file(iso_values, ordinate_name, lomfile)
                                plotting_context.set_iso_parameter_validity_from_lom_file(iso_validity, ordinate_name, lomfile)
                                plotting_context.set_siso_parameter_name_from_lom_file(siso_name, ordinate_name, lomfile)
                                plotting_context.set_siso_parameter_values_from_lom_file(siso_values, ordinate_name, lomfile)
                                plotting_context.set_siso_parameter_validity_from_lom_file(siso_validity, ordinate_name, lomfile)
                                plotting_context.set_label_dimension_from_lom_file(label.get_dimension(), ordinate_name, lomfile)

                                self.sisoExisted = False
                                # if siso parameter existed already in the plotting context. we just update the cutting information
                                # if not, we need to create a new one
                                if self.sisoExisted:
                                    self.plottingBoardReference.get_plot_parameter_manipulation_object().siso_range_check_list_changed()
                                else:
                                    self.isoExisted = True
                                    self.sisoExisted = True

                                # draw a new list of curves for lom
                                lom_function += " || " + ordinate_name + " [" + abscissa_name + ", " + iso_name + ", " + siso_name + "]"
                                self.draw_on_canvas_using_lom_files(lomfile, ordinate_name, 3)
                                self.plottingBoardReference.get_plot_parameter_manipulation_object().set_ordinate_config_table(lomfile, ordinate_name)
                                self.labelsDrawn.append((ordinate_name, lomfile))

                            lom_functions = QwtText(lom_function)
                            lom_functions.setFont(self.font)
                            self.setAxisTitle(QwtPlot.xBottom, lom_functions)
                            self.labelSuperposeActionActivated = False
                        self.plottingBoardReference.get_plot_parameter_manipulation_object().set_lom_existed()
                        self.plottingBoardReference.get_parent().get_parent().parent().parent().get_status_bar_reference().display_message(lom_function)


                    else:
                        # QMessageBox.question(self, 'Message', "this label has been imported already")
                        self.plottingBoardReference.get_parent().get_parent().parent().parent().get_status_bar_reference(). \
                            display_error_message("this label has been imported already")

            else:
                QMessageBox.question(self, 'Message', "No lom file loaded right now")

    def clean_all_information(self):
        self.curves_center['csv'].clear()
        self.curves_center['lom'].clear()

        self.detachItems(QwtPlotItem.Rtti_PlotCurve)
        self.detachItems(QwtPlotItem.Rtti_PlotMarker)
        self.replot()

        self.curve_from_csv_existed = False
        self.curve_from_lom_existed = False
        self.dimensionAdoptable = 0
        self.abscissa_name = ""
        self.isoExisted = False
        self.sisoExisted = False
        self.sisoConfig = "represent_by_color"
        self.labelSuperposeActionActivated = False
        del self.labelsDrawn[:]

        self.curve_gradient_using = False
        self.setAxisTitle(QwtPlot.xBottom, QwtText(''))

    def clean_before_replot(self):
        page_index = self.plottingBoardReference.get_page_index()
        plotting_index = self.plottingBoardReference.get_plotting_index()
        loaded_csvfiles = self.analyseurMediator.get_loaded_csv_files_from_context(page_index, plotting_index)
        loaded_csvfiles_validity = self.analyseurMediator.get_loaded_csv_files_validity_from_context(page_index, plotting_index)
        loaded_lomfiles = self.analyseurMediator.get_loaded_lom_files_from_context(page_index, plotting_index)
        loaded_lomfiles_validity = self.analyseurMediator.get_loaded_lom_files_validity_from_context(page_index, plotting_index)

        if self.curve_from_csv_existed:
            for csv_file_name in loaded_csvfiles:
                if not loaded_csvfiles_validity[loaded_csvfiles.index(csv_file_name)]:
                    continue
                if len(self.curves_center['csv'][csv_file_name]) > 0:
                    for key in self.curves_center['csv'][csv_file_name].keys():
                        del self.curves_center['csv'][csv_file_name][key][:]
        """
        if self.curve_from_lom_existed:
            for lom_file_name in loaded_lomfiles:
                if not loaded_lomfiles_validity[loaded_lomfiles.index(lom_file_name)]:
                    continue
                if len(self.curves_center['lom'][lom_file_name]) > 0:
                    for key in self.curves_center['lom'][lom_file_name].keys():
                        del self.curves_center['lom'][lom_file_name][key][:]
        """

        self.detachItems(QwtPlotItem.Rtti_PlotCurve)
        self.detachItems(QwtPlotItem.Rtti_PlotMarker)
        self.replot()

    def refresh_curves_on_canvas(self):
        # curves_on_canvas = self.plottingBoardReference.get_plot_parameter_manipulation_object().get_curves_validity_information()
        if self.curve_from_csv_existed and not self.curve_from_lom_existed:
            if self.sisoExisted:
                self.cut_current_curves_by_siso(self.sisoConfig)
            else:
                if self.isoExisted:
                    self.cut_current_curves_by_iso()
                else:
                    self.update_current_curve()

        if self.curve_from_lom_existed and not self.curve_from_csv_existed:
            self.clean_before_replot()
            self.replot_current_lom_curves()

        if self.curve_from_lom_existed and self.curve_from_csv_existed:

            if self.sisoExisted:
                self.cut_current_curves_by_siso(self.sisoConfig)
                self.replot_current_lom_curves()
            else:
                if self.isoExisted:
                    self.cut_current_curves_by_iso()
                    self.replot_current_lom_curves()
                else:
                    self.update_current_curve()
                    self.replot_current_lom_curves()