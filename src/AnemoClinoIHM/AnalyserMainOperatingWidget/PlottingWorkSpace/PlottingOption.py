"""
Last updated on 07/01/2015

@author: Cheng WANG,
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ExtraParameterWidget import ExtraParameterWidget


class PlottingOption(QDialog):
    def __init__(self, parent=None):
        super(PlottingOption, self).__init__(parent)
        self.plottingBoardReference = None
        self.analyserMediator = None
        self.layoutOption = 'NoGrid'
        self.canvasColor = QColor('AliceBlue')
        self.setFont(QFont("Helvetica", 8, QFont.AnyStyle, True))

        combo_box_style = 'QComboBox {border: 0px solid gray;border-radius: 3px;padding: 1px 18px 1px 3px;min-width: 6em;} ' \
                          'QComboBox::drop-down { subcontrol-origin: padding;subcontrol-position: top right;width: 15px;border-left-width: 1px; border-left-color: lightGray; border-left-style: solid;border-top-right-radius: 3px; border-bottom-right-radius: 3px;}' \
                          'QComboBox::down-arrow {border-image: url(:/down_arrow.png); } ' \
                          'QComboBox::down-arrow:on {top: 1px; left: 1px;}'

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background-color:darkGray; color: White")
        grid_layout_label = QLabel("GridStyle:")
        self.gridLayoutOptions = QComboBox()
        self.gridLayoutOptions.addItems(["NoGrid", "grid", "verticalBox", "horizontalBox"])
        self.gridLayoutOptions.setStyleSheet(combo_box_style)

        canvas_label = QLabel("background:")
        self.canvasOptions = QComboBox()
        self.fill_color_list(self.canvasOptions)
        self.canvasOptions.setStyleSheet(combo_box_style)

        digit_to_keep_label = QLabel('digit to keep:')
        self.digitToKeepEditLine = QLineEdit('8')
        self.digitToKeepEditLine.setStyleSheet("QLineEdit {border: 2px solid lightGray;border-radius: 10px;padding: 0 8px;background: transparent;selection-background-color: lightBlue;}")

        my_grid_layout = QGridLayout()
        my_grid_layout.addWidget(grid_layout_label, 0, 0)
        my_grid_layout.addWidget(self.gridLayoutOptions, 0, 1)
        my_grid_layout.addWidget(canvas_label, 0, 2)
        my_grid_layout.addWidget(self.canvasOptions, 0, 3)
        my_grid_layout.addWidget(digit_to_keep_label, 1, 0)
        my_grid_layout.addWidget(self.digitToKeepEditLine, 1, 1)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.setFixedHeight(25)

        self.buttonBox.setStyleSheet('font: bold italic large "Times New Roman"')
        self.buttonBox.button(QDialogButtonBox.Ok).setFlat(True)
        self.buttonBox.button(QDialogButtonBox.Ok).setIcon(QIcon(":/plotting_configuration_confirmation.png"))
        self.buttonBox.button(QDialogButtonBox.Cancel).setFlat(True)
        self.buttonBox.button(QDialogButtonBox.Cancel).setIcon(QIcon(":/plotting_configuration_cancel.png"))

        config_tab_widget = QTabWidget()
        config_tab_widget.setStyleSheet("QTabWidget::pane { border-top: 2px solid #C2C7CB;position: absolute; top: -0.5em;} QTabWidget::tab-bar {alignment: center;}"
                                        "QTabBar::tab {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);border: 2px solid #C4C4C3;border-bottom-color: #C2C7CB; border-top-left-radius: 4px;border-top-right-radius: 4px;min-width: 8ex;padding: 2px;}"
                                        "QTabBar::tab:selected, QTabBar::tab:hover {background-color: darkGray;} "
                                        "QTabBar::tab:selected {border-color: #9B9B9B;border-bottom-color: #C2C7CB; }")
        point_tracking_option_widget = QWidget()
        point_tracking_option_layout = QVBoxLayout()
        point_tracking_option_label = QLabel('Drag the extra parameter to be displayed here:')
        self.point_tracking_option_clear_button = QPushButton()
        self.point_tracking_option_clear_button.setFixedWidth(30)
        self.point_tracking_option_clear_button.setFixedHeight(30)
        self.point_tracking_option_clear_button.setFlat(True)
        self.point_tracking_option_clear_button.setStyleSheet("QPushButton{border-image: url(:/clear.png);}")
        layout_1 = QHBoxLayout()
        layout_1.addWidget(point_tracking_option_label)
        layout_1.addWidget(self.point_tracking_option_clear_button)

        self.extra_parameter_widget = ExtraParameterWidget(self)
        point_tracking_option_layout.addLayout(layout_1)
        point_tracking_option_layout.addWidget(self.extra_parameter_widget)
        point_tracking_option_widget.setLayout(point_tracking_option_layout)

        restriction_config_widget = QWidget()
        restriction_config_layout = QGridLayout()
        restriction_config_widget.setLayout(restriction_config_layout)

        config_tab_widget.addTab(point_tracking_option_widget, "Tracking")
        config_tab_widget.addTab(restriction_config_widget, "Restriction")

        layout = QVBoxLayout()
        layout.addLayout(my_grid_layout)
        layout.addWidget(config_tab_widget)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

        self.connect(self.buttonBox.button(QDialogButtonBox.Ok), SIGNAL('clicked()'), self.confirmed)
        self.connect(self.buttonBox.button(QDialogButtonBox.Cancel), SIGNAL('clicked()'), self.cancelled)
        self.connect(self.gridLayoutOptions, SIGNAL('currentIndexChanged(QString)'), self.layout_option_changed)
        self.connect(self.canvasOptions, SIGNAL("currentIndexChanged(int)"), self.canvas_option_changed)
        self.connect(self.point_tracking_option_clear_button, SIGNAL('clicked()'), self.clear_extra_parameters)
        self.digitToKeepEditLine.textChanged.connect(self.verify_digit)

    def set_analyser_mediator(self, analyser_controller):
        self.analyserMediator = analyser_controller
        self.extra_parameter_widget.set_analyser_mediator(self.analyserMediator)

    def set_plotting_board_reference(self, plotting_board_reference):
        self.plottingBoardReference = plotting_board_reference
        self.extra_parameter_widget.set_plotting_board_reference(self.plottingBoardReference)

    def verify_digit(self, number):
        number = str(number)
        if number != '':
            if number.isdigit():
                t = int(number)
                if t > 10:
                    self.digitToKeepEditLine.setText('8')
            elif number.__contains__('-'):
                number_temp = number.translate(None, '-')
                if number_temp.isdigit():
                    t = -int(number_temp)
                    if t < 0:
                        self.digitToKeepEditLine.setText('8')

    def layout_option_changed(self, layout_option):
        self.layoutOption = layout_option

    def canvas_option_changed(self):
        color_list = QColor.colorNames()
        self.canvasColor = QColor(color_list[self.canvasOptions.currentIndex()])

    @staticmethod
    def fill_color_list(combo_box):
        color_list = QColor.colorNames()
        for color in color_list:
            pix = QPixmap(QSize(40, 15))
            pix.fill(QColor(color))
            combo_box.addItem(QIcon(pix),color)
            combo_box.setIconSize(QSize(40,15))
            combo_box.setSizeAdjustPolicy(QComboBox.AdjustToContents)

    def cancelled(self):
        self.close()

    def confirmed(self):
        """
            --
        :return:
        """
        extra_parameter_list = self.extra_parameter_widget.get_extra_parameter_list()
        if len(extra_parameter_list) != 0:
            self.plottingBoardReference.set_extra_parameter_list_to_be_displayed(extra_parameter_list)

        self.plottingBoardReference.get_plot_object().change_canvas_layout(self.layoutOption)
        self.plottingBoardReference.get_plot_object().change_canvas_color(self.canvasColor)
        self.plottingBoardReference.set_digit_to_keep(int(self.digitToKeepEditLine.text()))

        self.close()
        self.analyserMediator.generate_an_action_into_global_context('confirm the configuration for plotting board :'
                                                                     + str(self.plottingBoardReference.get_plotting_index()) + ' in page: '
                                                                     + str(self.plottingBoardReference.get_page_index()))

    def clear_extra_parameters(self):
        self.extra_parameter_widget.clear()
        self.plottingBoardReference.clear_extra_parameter_list_to_be_displayed()
        self.analyserMediator.generate_an_action_into_global_context('clear extra parameter for plotting board :'
                                                                     + str(self.plottingBoardReference.get_plotting_index()) + ' in page: '
                                                                     + str(self.plottingBoardReference.get_page_index()))

    def get_extra_parameter_widget_reference(self):
        return self.extra_parameter_widget

    def display(self, pos):
        self.show()
        self.move(pos.x() - self.width(), pos.y() + 5)

    def check_parameter_dragged(self, parameter_name):
        return self.plottingBoardReference.verify_parameter(parameter_name)