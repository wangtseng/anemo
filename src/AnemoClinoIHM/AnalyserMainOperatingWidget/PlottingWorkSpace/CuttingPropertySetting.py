"""
Last updated on 07/01/2015

@author: Cheng WANG,
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class CuttingPropertySetting(QWidget):
    def __init__(self, parent=None):
        super(CuttingPropertySetting, self).__init__(parent)
        self.parent = None
        self.analyserMediator = None
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background-color: DarkSeaGreen; color:white")
        self.myPlottingContext = None
        self.font = QFont("Helvetica", 8, QFont.AnyStyle, True)
        self.setFont(self.font)

        my_layout = QGridLayout(self)
        iso_display_label = QLabel("Display iso's cutting information by:")
        siso_display_label = QLabel("Display siso's cutting information by:")

        self.value_pointer_display_mode_iso = QCheckBox("value")
        self.value_pointer_display_mode_iso.setChecked(False)
        self.value_range_display_mode_iso = QCheckBox("range")
        self.value_range_display_mode_iso.setChecked(True)
        self.value_pointer_display_mode_siso = QCheckBox("value")
        self.value_pointer_display_mode_siso.setChecked(False)
        self.value_range_display_mode_siso = QCheckBox("range")
        self.value_range_display_mode_siso.setChecked(True)

        self.confirm_button = QPushButton("confirm")
        self.confirm_button.setFlat(1)
        self.cancel_button = QPushButton("cancel")
        self.cancel_button.setFlat(1)

        my_layout.addWidget(iso_display_label, 0, 0)
        my_layout.addWidget(self.value_pointer_display_mode_iso, 0, 1)
        my_layout.addWidget(self.value_range_display_mode_iso, 0, 2)
        my_layout.addWidget(siso_display_label, 1, 0)
        my_layout.addWidget(self.value_pointer_display_mode_siso, 1, 1)
        my_layout.addWidget(self.value_range_display_mode_siso, 1, 2)
        my_layout.addWidget(self.confirm_button, 2, 1)
        my_layout.addWidget(self.cancel_button, 2, 2)

        self.connect(self.value_pointer_display_mode_iso, SIGNAL("stateChanged(int)"), self.value_pointer_display_mode_for_iso_chosen)
        self.connect(self.value_pointer_display_mode_siso, SIGNAL("stateChanged(int)"), self.value_pointer_display_mode_for_siso_chosen)
        self.connect(self.value_range_display_mode_iso, SIGNAL("stateChanged(int)"), self.range_pointer_display_mode_for_iso_chosen)
        self.connect(self.value_range_display_mode_siso, SIGNAL("stateChanged(int)"), self.range_pointer_display_mode_for_siso_chosen)
        self.connect(self.confirm_button, SIGNAL("clicked()"), self.configuration_confirmed)
        self.connect(self.cancel_button, SIGNAL("clicked()"), self.configuration_canceled)

    def set_analyser_mediator(self, analyser_mediator_reference):
        self.analyserMediator = analyser_mediator_reference

    def set_my_parent(self, parent):
        self.parent = parent

    def display(self, pos):
        self.show()
        self.move(pos.x() - self.width(), pos.y() + 5)

    def configuration_confirmed(self):
        plotting_context = self.parent.get_my_plotting_context()
        if self.value_pointer_display_mode_iso.isChecked():
            plotting_context.set_iso_display_mode(1)
        else:
            plotting_context.set_iso_display_mode(0)

        if self.value_pointer_display_mode_siso.isChecked():
            plotting_context.set_siso_display_mode(1)
        else:
            plotting_context.set_siso_display_mode(0)

        self.parent.update_text_or_color_for_table('iso', self.parent.get_iso_display_mode())
        self.parent.update_text_or_color_for_table('siso', self.parent.get_siso_display_mode())

        self.close()

    def configuration_canceled(self):
        self.close()

    def set_plotting_context(self, plotting_context):
        self.myPlottingContext = plotting_context

    def value_pointer_display_mode_for_iso_chosen(self, check_stat):
        if check_stat == 2:
            self.value_range_display_mode_iso.setChecked(False)
        else:
            self.value_range_display_mode_iso.setChecked(True)

    def value_pointer_display_mode_for_siso_chosen(self, check_stat):
        if check_stat == 2:
            self.value_range_display_mode_siso.setChecked(False)
        else:
            self.value_range_display_mode_siso.setChecked(True)

    def range_pointer_display_mode_for_iso_chosen(self, check_stat):
        if check_stat == 2:
            self.value_pointer_display_mode_iso.setChecked(False)
        else:
            self.value_pointer_display_mode_iso.setChecked(True)

    def range_pointer_display_mode_for_siso_chosen(self, check_stat):
        if check_stat == 2:
            self.value_pointer_display_mode_siso.setChecked(False)
        else:
            self.value_pointer_display_mode_siso.setChecked(True)