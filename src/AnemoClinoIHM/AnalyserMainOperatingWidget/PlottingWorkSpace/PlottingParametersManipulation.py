# coding=utf-8
"""
Last updated on 08/01/2015

@author: Cheng WANG,
"""

from ISOLabel import *
from CuttingPropertySetting import CuttingPropertySetting


class PlottingParametersManipulation(QToolBox):
    def __init__(self, plotting_board_reference=None):
        super(PlottingParametersManipulation, self).__init__()

        self.setAcceptDrops(True)
        self.plottingBoardReference = plotting_board_reference
        self.setFont(QFont("Helvetica", 8.5, QFont.AnyStyle, True))
        self.setStyleSheet(
            "QToolBox::tab {background: lavender ;border-radius: 0px; color: darkSeaGreen;}"
            "QToolBox::tab:selected {color: lightSeaGreen;}")

        """
        initialize attribute
        """
        self.labelItemToBeHandled = None
        self.analyserMediator = None
        self.rowCount = 0
        self.isoCutPoints = []
        self.isoScaleList = []
        self.sisoCutPoints = []
        self.sisoScaleList = []
        self.isoConfigTableRowCount = 2
        self.sisoConfigTableRowCount = 2
        self.isoRangeCheckList = []
        self.sisoRangeCheckList = []
        self.subListISO = []
        self.subListISOIndex = []
        self.subListSISO = []
        self.subListSISOIndex = []
        self.new_Color_List = []
        self.new_Marker_List = []
        self.curves_on_canvas = {}
        self.fileTreeItemList = []
        self.iso_max = 0.0
        self.iso_min = 0.0
        self.siso_max = 0.0
        self.siso_min = 0.0
        self.plot = self.plottingBoardReference.get_plot_object()
        self.font = QFont("Helvetica", 8, QFont.AnyStyle, True)
        self.buttonSize = QSize(19, 19)
        self.siso_existed = False
        self.curve_gradient_using = False
        self.lom_existed = False
        self.isoDisplayMode = "represent_by_marker"
        self.sisoDisplayMode = "represent_by_color"
        self.isoCutInformation = ""
        self.sisoCutInformation = ""
        self.ISOParameter = ""
        self.SISOParameter = ""
        self.cuttingPropertySetting = CuttingPropertySetting()
        self.cuttingPropertySetting.set_my_parent(self)

        self.iso_check_list = list()
        self.siso_check_list = list()
        self.index = -1

        """
        colors, markers
        """
        self.defaultFileIcon = QIcon(":/csvfile.png")
        self.colorList = list()
        self.colorNumber = 0
        self.markerList = list()
        style_of_table = "QHeaderView::section{spacing: 10px; background-color:transparent; color: blue; border: 1px solid white;margin: 1px;text-align: right;font-family: arial;font-size:12px;}"

        self.setMinimumWidth(150)
        self.setMaximumWidth(200)

        # ----------------------------------------------------------
        # component necessary to manipulate the parameter chosen for Y
        # ----------------------------------------------------------
        self.Ordinate_groupBox = QGroupBox()
        self.Ordinate_Layout = QVBoxLayout(self.Ordinate_groupBox)
        self.Ordinate_Layout.setMargin(0)
        self.Ordinate_Layout.setAlignment(Qt.AlignCenter)
        self.ordinateManipulationTree = QTreeWidget()
        self.ordinateManipulationTree.setFont(self.font)
        self.ordinateManipulationTree.setColumnCount(1)
        self.ordinateManipulationTree.setHeaderHidden(1)
        self.ordinateManipulationTree.verticalScrollBar().setStyleSheet("background-color: transparent")
        self.ordinateManipulationTree.setFrameStyle(QFrame.NoFrame)
        self.ordinateManipulationTree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Ordinate_Layout.addWidget(self.ordinateManipulationTree)
        # self.Ordinate_Layout.addStretch()

        self.mySplitter = QSplitter(Qt.Vertical, self)
        self.mySplitter.setOpaqueResize(True)
        self.mySplitter.setHandleWidth(1)
        """
        self.minimizeButton.setFixedSize(self.buttonSize)
        self.minimizeButton.setFlat(True)
        """
        self.iso_siso_control_label = QLabel(self.mySplitter)
        self.iso_siso_control_label.setFixedHeight(20)
        self.iso_siso_display_config_button = QPushButton(self.iso_siso_control_label)
        self.iso_siso_display_config_button.setFixedSize(self.buttonSize)
        self.iso_siso_display_config_button.setFlat(True)
        self.iso_siso_display_config_button.setStyleSheet("QPushButton{border-image: url(:/iso_siso_display_config.png);}")
        self.iso_siso_display_config_button.move(0, 0)

        self.iso_siso_information_export_button = QPushButton(self.iso_siso_control_label)
        self.iso_siso_information_export_button.setFixedSize(self.buttonSize)
        self.iso_siso_information_export_button.setFlat(True)
        self.iso_siso_information_export_button.setStyleSheet("QPushButton{border-image: url(:/import_cutting_information.png);}")
        self.iso_siso_information_export_button.move(20, 0)

        self.iso_siso_clear_button = QPushButton(self.iso_siso_control_label)
        self.iso_siso_clear_button.setFixedSize(self.buttonSize)
        self.iso_siso_clear_button.setFlat(True)
        self.iso_siso_clear_button.setStyleSheet("QPushButton{border-image: url(:/clear.png);}")
        self.iso_siso_clear_button.move(40, 0)  # import_cutting_information

        # ---------------------------------------------------------------
        # component necessary to manipulate the parameter chosen for ISO
        # ---------------------------------------------------------------
        self.ISO_groupBox = QGroupBox(self.mySplitter)
        self.ISO_Layout = QVBoxLayout(self.ISO_groupBox)
        self.ISO_Layout.setMargin(0)
        self.ISO_Layout.setAlignment(Qt.AlignCenter)
        self.isoConfigTable = QTableWidget()
        self.isoConfigTable.setStyleSheet(style_of_table)
        self.isoConfigTable.verticalScrollBar().setStyleSheet("background-color: transparent")
        self.isoConfigTable.setFrameStyle(QFrame.NoFrame)
        self.isoConfigTable.setColumnCount(1)
        self.isoConfigTable.setColumnWidth(0, 200)
        self.isoConfigTable.setRowCount(2)
        self.isoConfigTable.horizontalHeader().setHidden(True)
        self.isoConfigTable.verticalHeader().setHidden(True)
        self.isoConfigTable.verticalScrollBar().setStyleSheet("background-color: transparent")
        self.isoConfigTable.setRowHeight(0, 20)
        self.isoConfigTable.setRowHeight(1, 20)
        self.isoLabel = ISOLabel(self)
        self.ISO_cmdline = QLineEdit("x;x;x;x")
        self.ISO_cmdline.setMinimumWidth(120)
        self.ISO_cmdline.setStyleSheet("QLineEdit{border-width:0;border-style:outset}")
        self.isoConfigTable.setCellWidget(0, 0, self.isoLabel)
        self.isoConfigTable.setCellWidget(1, 0, self.ISO_cmdline)
        self.ISO_Layout.addWidget(self.isoConfigTable)

        # --------------------------------------------------------------------
        # component necessary to manipulate the parameter chosen for Super ISO
        # ---------------------------------------------------------------------
        self.SISO_groupBox = QGroupBox(self.mySplitter)
        self.SISO_Layout = QVBoxLayout(self.SISO_groupBox)
        self.SISO_Layout.setMargin(0)
        self.SISO_Layout.setAlignment(Qt.AlignCenter)
        self.sisoConfigTable = QTableWidget()
        self.sisoConfigTable.setStyleSheet(style_of_table)
        self.sisoConfigTable.verticalScrollBar().setStyleSheet("background-color: transparent")
        self.sisoConfigTable.setFrameStyle(QFrame.NoFrame)
        self.sisoConfigTable.setColumnCount(1)
        self.sisoConfigTable.setColumnWidth(0, 200)
        self.sisoConfigTable.setRowCount(2)
        self.sisoConfigTable.horizontalHeader().setHidden(True)
        self.sisoConfigTable.verticalHeader().setHidden(True)
        self.sisoConfigTable.verticalScrollBar().setStyleSheet("background-color: transparent")
        self.sisoLabel = SISOLabel(self)
        self.SISO_cmdline = QLineEdit("x;x;x;x")
        self.SISO_cmdline.setMinimumWidth(120)
        self.SISO_cmdline.setStyleSheet("QLineEdit{border-width:0;border-style:outset}")
        self.sisoConfigTable.setCellWidget(0, 0, self.sisoLabel)
        self.sisoConfigTable.setCellWidget(1, 0, self.SISO_cmdline)
        self.sisoConfigTable.setRowHeight(0, 20)
        self.sisoConfigTable.setRowHeight(1, 20)
        self.SISO_Layout.addWidget(self.sisoConfigTable)

        self.addItem(self.Ordinate_groupBox, self.tr("Ordinate"))
        self.addItem(self.mySplitter, self.tr("ISO && SISO"))

        self.connect(self.ISO_cmdline, SIGNAL("returnPressed()"), self.iso_commandline_return_pressed)
        self.connect(self.SISO_cmdline, SIGNAL("returnPressed()"), self.siso_commandline_return_pressed)
        # self.connect(self.ordinateConfigTree, SIGNAL("itemChanged(QTreeWidgetItem*,int)"), self.handleItemChecked)
        self.connect(self.iso_siso_display_config_button, SIGNAL("clicked()"), self.iso_siso_display_configuration)
        self.connect(self.iso_siso_information_export_button, SIGNAL("clicked()"), self.iso_siso_information_export_to)
        self.connect(self.ordinateManipulationTree, SIGNAL("itemChanged(QTreeWidgetItem*,int)"), self.handle_item_checked)
        self.connect(self.ordinateManipulationTree, SIGNAL("customContextMenuRequested(QPoint)"), self.ordinate_manipulation_tree_widget_custom_context_menu_requested)

    def set_color_list(self, l):
        self.colorList = l
        self.colorNumber = len(self.colorList)

    def set_marker_list(self, l):
        self.markerList = l

    def get_plotting_board_reference(self):
        return self.plottingBoardReference

    def clean_all_component(self, flag):
        self.clear_the_table_items('iso')
        self.clear_the_table_items('siso')

        if flag:
            self.ordinateManipulationTree.clear()
            self.curves_on_canvas.clear()
            del self.fileTreeItemList[:]

        self.rowCount = 0
        self.ISOParameter = ""
        self.SISOParameter = ""
        self.isoConfigTableRowCount = 2
        self.sisoConfigTableRowCount = 2
        del self.isoCutPoints[:]
        del self.sisoCutPoints[:]
        del self.isoScaleList[:]
        del self.sisoScaleList[:]
        del self.isoRangeCheckList[:]
        del self.sisoRangeCheckList[:]
        del self.subListISO[:]
        del self.subListISOIndex[:]
        del self.subListSISO[:]
        del self.subListSISOIndex[:]
        del self.new_Color_List[:]
        del self.new_Marker_List[:]
        self.siso_existed = False
        self.curve_gradient_using = False
        self.lom_existed = False
        self.isoDisplayMode = "represent_by_marker"
        self.sisoDisplayMode = "represent_by_color"
        self.sisoCutInformation = ""
        self.isoCutInformation = ""
        self.isoLabel.clear()
        self.ISO_cmdline.clear()
        self.sisoLabel.clear()
        self.SISO_cmdline.clear()

    def get_iso_label(self):
        return self.isoLabel

    def get_siso_label(self):
        return self.sisoLabel

    def set_analyser_mediator(self, analyser_mediator):
        self.analyserMediator = analyser_mediator
        self.isoLabel.set_analyser_mediator(analyser_mediator)
        self.sisoLabel.set_analyser_mediator(analyser_mediator)
        self.cuttingPropertySetting.set_analyser_mediator(analyser_mediator)

    def get_curves_validity_information(self):
        return self.curves_on_canvas

    def ordinate_manipulation_tree_widget_custom_context_menu_requested(self, pos):
        """
            -- once an item in the qtreewidgetitem been right clicked, an action window(include: ...) will display
        :param pos: the current mouse position to position the actions window
        """
        if self.plottingBoardReference.get_canvas_operation_mode() != 2:
            return

        if self.ordinateManipulationTree.itemAt(pos) is None:
            return

        if self.ordinateManipulationTree.itemAt(pos).parent() is None:
            return

        self.index = self.ordinateManipulationTree.indexOfTopLevelItem(self.ordinateManipulationTree.itemAt(pos).parent())

        title = str(self.ordinateManipulationTree.itemAt(pos).parent().text(0))

        if title.__contains__(".gen"):
            self.labelItemToBeHandled = self.ordinateManipulationTree.itemAt(pos)
            menu = QMenu(self.ordinateManipulationTree)
            menu.setStyleSheet('QMenu {background-color: #ABABAB; border: 1px solid black;}'
                               'QMenu::item {background-color: transparent;}'
                               'QMenu::item:selected {background-color: #654321;}')
            label_modify_button = menu.addAction("modify")
            delete_label_button = menu.addAction("delete")
            self.connect(label_modify_button, SIGNAL("triggered()"), self.modify_the_label)
            self.connect(delete_label_button, SIGNAL("triggered()"), self.delete_the_label)
            menu.exec_(QCursor.pos())

        elif title.__contains__(".csv"):
            self.labelItemToBeHandled = self.ordinateManipulationTree.itemAt(pos)
            menu = QMenu(self.ordinateManipulationTree)
            menu.setStyleSheet('QMenu {background-color: #ABABAB; border: 1px solid black;}'
                               'QMenu::item {background-color: transparent;}'
                               'QMenu::item:selected {background-color: #654321;}')
            delete_ordinate_button = menu.addAction("delete")
            self.connect(delete_ordinate_button, SIGNAL("triggered()"), self.delete_ordinate)
            menu.exec_(QCursor.pos())

    def modify_the_label(self):
        label_to_be_modified = str(self.labelItemToBeHandled.text(0))
        filename = str(self.labelItemToBeHandled.parent().text(0))
        self.plottingBoardReference.set_label_to_be_modified(label_to_be_modified, filename)

    def delete_ordinate(self):
        ordinate_name = str(self.labelItemToBeHandled.text(0))
        filename = str(self.labelItemToBeHandled.parent().text(0))

        if self.plottingBoardReference.delete_the_ordinate_on_the_canvas(ordinate_name, filename):
            parent = self.labelItemToBeHandled.parent()
            parent.removeChild(self.labelItemToBeHandled)

            if parent.childCount() == 0:
                self.ordinateManipulationTree.takeTopLevelItem(self.ordinateManipulationTree.indexOfTopLevelItem(parent))

            if self.ordinateManipulationTree.topLevelItemCount() == 0:
                self.plottingBoardReference.self_cleaning()

            self.plottingBoardReference.get_plot_object().refresh_curves_on_canvas()

        self.analyserMediator.generate_an_action_into_global_context('remove the ordinate: ' + ordinate_name + ' in file: ' + filename + ' at position ' + str(self.index)
                                                                     + ' for plotting board :'
                                                                     + str(self.plottingBoardReference.get_plotting_index()) + ' in page: '
                                                                     + str(self.plottingBoardReference.get_page_index()))

    def delete_ordinate_while_import(self, filename, ordinate_name, item_index):

        if self.plottingBoardReference.delete_the_ordinate_on_the_canvas(ordinate_name, filename):
            self.index = item_index
            parent = self.ordinateManipulationTree.topLevelItem(item_index)

            for i in range(parent.childCount()):
                if parent.child(i).text(0) == ordinate_name:
                    self.labelItemToBeHandled = parent.child(i)

            parent.removeChild(self.labelItemToBeHandled)

            if parent.childCount() == 0:
                self.ordinateManipulationTree.takeTopLevelItem(self.ordinateManipulationTree.indexOfTopLevelItem(parent))

            if self.ordinateManipulationTree.topLevelItemCount() == 0:
                self.plottingBoardReference.self_cleaning()

            self.plottingBoardReference.get_plot_object().refresh_curves_on_canvas()

        self.analyserMediator.generate_an_action_into_global_context('remove the ordinate: ' + ordinate_name + ' in file: ' + filename + ' at position ' + str(self.index)
                                                                     + ' for plotting board :'
                                                                     + str(self.plottingBoardReference.get_plotting_index()) + ' in page: '
                                                                     + str(self.plottingBoardReference.get_page_index()))

    def delete_the_label(self):
        label_to_be_deleted = str(self.labelItemToBeHandled.text(0))
        filename = str(self.labelItemToBeHandled.parent().text(0))

        if self.plottingBoardReference.delete_the_label_on_the_canvas(label_to_be_deleted, filename):
            parent = self.labelItemToBeHandled.parent()
            parent.removeChild(self.labelItemToBeHandled)

            if parent.childCount() == 0:
                self.ordinateManipulationTree.takeTopLevelItem(self.ordinateManipulationTree.indexOfTopLevelItem(parent))
                self.lom_existed = False

            if self.ordinateManipulationTree.topLevelItemCount() == 0:
                self.plottingBoardReference.self_cleaning()
                return

            self.plottingBoardReference.get_plot_object().refresh_curves_on_canvas()

        self.analyserMediator.generate_an_action_into_global_context('remove the label: ' + label_to_be_deleted + ' in file: ' + filename + ' at ' + str(self.index)
                                                                     + ' for plotting board :'
                                                                     + str(self.plottingBoardReference.get_plotting_index()) + ' in page: '
                                                                     + str(self.plottingBoardReference.get_page_index()))

    def delete_the_label_while_import(self, filename, label_to_be_deleted, item_index):

        if self.plottingBoardReference.delete_the_label_on_the_canvas(label_to_be_deleted, filename):

            self.index = item_index
            parent = self.ordinateManipulationTree.topLevelItem(item_index)

            for i in range(parent.childCount()):
                if parent.child(i).text(0) == label_to_be_deleted:
                    self.labelItemToBeHandled = parent.child(i)

            parent.removeChild(self.labelItemToBeHandled)

            if parent.childCount() == 0:
                self.ordinateManipulationTree.takeTopLevelItem(self.ordinateManipulationTree.indexOfTopLevelItem(parent))
                self.lom_existed = False

            if self.ordinateManipulationTree.topLevelItemCount() == 0:
                self.plottingBoardReference.self_cleaning()
                return

            self.plottingBoardReference.get_plot_object().refresh_curves_on_canvas()

        self.analyserMediator.generate_an_action_into_global_context('remove the label: ' + label_to_be_deleted + ' in file: ' + filename + ' at ' + str(self.index)
                                                                     + 'for plotting board :'
                                                                     + str(self.plottingBoardReference.get_plotting_index()) + ' in page: '
                                                                     + str(self.plottingBoardReference.get_page_index()))

    @staticmethod
    def iso_siso_information_export_to():
        flag = False
        if flag:
            print 'export information'

    def set_lom_existed(self):
        self.lom_existed = True

    def get_siso_display_mode(self):
        return self.sisoDisplayMode

    def get_iso_display_mode(self):
        return self.isoDisplayMode

    def iso_siso_display_configuration(self):
        self.cuttingPropertySetting.display(QCursor.pos())

    def set_siso_config(self, siso_config):
        self.sisoDisplayMode = siso_config

    def tool_choose_choosing(self, index):
        flag = False
        if flag:
            print index, self.currentWidget()

    def handle_item_checked(self, item, i):
        if not self.flag:
            return

        if item in self.fileTreeItemList:
            if item.checkState(0) == 0:
                for j in range(item.childCount()):
                    item.child(j).setCheckState(0, Qt.Unchecked)

            elif item.checkState(0) == 2:
                for j in range(item.childCount()):
                    item.child(j).setCheckState(0, Qt.Checked)

        else:
            if item.parent() is None:
                return

            if item.checkState(0) == 0:
                for ordinate in self.curves_on_canvas[str(item.parent().text(0))].keys():
                    if ordinate == str(item.text(0)):
                        self.curves_on_canvas[str(item.parent().text(0))][ordinate] = 0

                flag = True
                for j in range(item.parent().childCount()):
                    if item.parent().child(j).checkState(0) == 2:
                        flag = False
                        break
                if flag:
                    if item.parent().checkState(0) == 2:
                        item.parent().setCheckState(0, Qt.Unchecked)

            elif item.checkState(0) == 2:
                for ordinate in self.curves_on_canvas[str(item.parent().text(0))].keys():
                    if ordinate == str(item.text(0)):
                        self.curves_on_canvas[str(item.parent().text(0))][ordinate] = 1

                flag = True
                for j in range(item.parent().childCount()):
                    if item.parent().child(j).checkState(0) == 0:
                        flag = False
                        break
                if flag:
                    if item.parent().checkState(0) == 0:
                        item.parent().setCheckState(0, Qt.Checked)

        self.plottingBoardReference.get_plot_object().refresh_curves_on_canvas()

    def set_ordinate_config_table(self, filename, ordinate_parameter):
        self.flag = False

        if filename not in self.curves_on_canvas.keys():
            file_in_using = QTreeWidgetItem(self.ordinateManipulationTree)
            file_in_using.setText(0, filename)
            file_in_using.setIcon(0, self.defaultFileIcon)
            file_in_using.setFlags(file_in_using.flags() | Qt.ItemIsUserCheckable)
            file_in_using.setCheckState(0, Qt.Checked)
            self.curves_on_canvas[filename] = {}
            self.curves_on_canvas[filename][ordinate_parameter] = 1
            ordinate = QTreeWidgetItem(file_in_using)
            ordinate.setText(0, ordinate_parameter)
            ordinate.setIcon(0, QIcon(":/title.png"))
            ordinate.setFlags(ordinate.flags() | Qt.ItemIsUserCheckable)
            ordinate.setCheckState(0, Qt.Checked)
            # to be verified if it need to be used or not
            self.fileTreeItemList.append(file_in_using)
        else:
            # if ordinate_parameter not in self.ordinate_information[filename]:
            self.curves_on_canvas[filename][ordinate_parameter] = 1
            for file_item in self.fileTreeItemList:
                if file_item.text(0) == filename:
                    ordinate = QTreeWidgetItem(file_item)
                    ordinate.setText(0, ordinate_parameter)
                    ordinate.setIcon(0, QIcon(":/title.png"))
                    ordinate.setFlags(ordinate.flags() | Qt.ItemIsUserCheckable)
                    ordinate.setCheckState(0, Qt.Checked)
        self.flag = True

    def get_my_plotting_context(self):
        page_index = self.plottingBoardReference.get_page_index()
        plotting_index = self.plottingBoardReference.get_plotting_index()
        return self.analyserMediator.get_a_plotting_context(page_index, plotting_index)

    def iso_unchecked_all(self):
        for i in self.isoRangeCheckList:
            i.setCheckState(Qt.Unchecked)
        self.iso_range_check_list_changed()

    def iso_checked_all(self):
        for i in self.isoRangeCheckList:
            i.setCheckState(Qt.Checked)
        self.iso_range_check_list_changed()

    def iso_check_setting(self, check_states):
        cpt = 0
        if len(check_states) != len(self.isoRangeCheckList):
            return
        for i in self.isoRangeCheckList:
            if check_states[cpt] == '1':
                i.setCheckState(Qt.Checked)
            elif check_states[cpt] == '0':
                i.setCheckState(Qt.Unchecked)
            cpt += 1
        self.iso_range_check_list_changed()

    def siso_unchecked_all(self):
        for i in self.sisoRangeCheckList:
            i.setCheckState(Qt.Unchecked)
        self.siso_range_check_list_changed()

    def siso_checked_all(self):
        for i in self.sisoRangeCheckList:
            i.setCheckState(Qt.Checked)
        self.siso_range_check_list_changed()

    def siso_check_setting(self, check_states):
        cpt = 0
        if len(check_states) != len(self.sisoRangeCheckList):
            return
        for i in self.sisoRangeCheckList:
            if check_states[cpt] == '1':
                i.setCheckState(Qt.Checked)
            elif check_states[cpt] == '0':
                i.setCheckState(Qt.Unchecked)
            cpt += 1
        self.siso_range_check_list_changed()

    def generate_scale_list(self, flag):
        scale_list = []
        if flag == 'iso':
            for i in range(0, len(self.isoCutPoints) - 1):
                scale_list.append((self.isoCutPoints[i] + self.isoCutPoints[i + 1]) / 2)
        elif flag == 'siso':
            for i in range(0, len(self.sisoCutPoints) - 1):
                scale_list.append((self.sisoCutPoints[i] + self.sisoCutPoints[i + 1]) / 2)
        return scale_list

    def verify_iso_cutting_information(self, string_in_cut_cmdline):
        unit = 0
        iso_cut_information = string_in_cut_cmdline.translate(None, " ")
        if iso_cut_information.__contains__(";"):
            del self.subListISO[:]
            del self.subListISOIndex[:]
            del self.isoRangeCheckList[:]
            del self.isoScaleList[:]
            del self.isoCutPoints[:]
            cut_points = iso_cut_information.split(";")
            self.isoCutPoints = map(float, cut_points)

        elif iso_cut_information.__contains__("[") and iso_cut_information.__contains__("]") and iso_cut_information.__contains__("/"):
            del self.subListISO[:]
            del self.subListISOIndex[:]
            del self.isoRangeCheckList[:]
            del self.isoScaleList[:]
            del self.isoCutPoints[:]
            """
            [2, 10]/4
            2, 10, 4

            unit = 2

            [2,4],[4,6],[6,8],[8,10],
            1, 3, 5, 7, 9, 11

            2 + 2*0 - 2/2
            2 + 2*1 - 2/2
            2 + 2*2 -2/2
            2 + 2*3 - 2/2
            2 + 2*4 - 2/2
            2 + 2*5 - 2/2
            """
            t1 = iso_cut_information.index("[")
            t2 = iso_cut_information.index("]")
            str1 = string_in_cut_cmdline[t1 + 1:t2]
            m = str1.split(",")

            v1 = float(m[0])
            v2 = float(m[1])
            v3 = int(string_in_cut_cmdline.split("/")[1])
            unit = abs(v1 - v2) / v3

            for i in range(0, v3 + 2):
                self.isoCutPoints.append(v1 + unit * i - unit / 2)

        elif iso_cut_information.__contains__("->"):
            color_elements = string_in_cut_cmdline.split("->")
            if self.siso_existed:
                if self.sisoDisplayMode == 'represent_by_marker':
                    self.iso_gradient(color_elements[0], color_elements[1])
                else:
                    del self.sisoRangeCheckList[:]
                    self.set_siso_config("represent_by_marker")
                    self.sisoScaleList = self.generate_scale_list("siso")

                    if self.sisoDisplayMode == "represent_by_color":
                        self.update_text_or_color_for_table('iso', 'represent_by_marker')
                        self.generate_scale_list_for_table('siso', 'represent_by_color')
                    elif self.sisoDisplayMode == "represent_by_marker":
                        self.update_text_or_color_for_table('iso', 'represent_by_color')
                        self.generate_scale_list_for_table('siso', 'represent_by_marker')

                    self.clear_the_table_items('siso')
                    self.apply_scale_list_on_table('siso')

            self.iso_gradient(color_elements[0], color_elements[1])
            return False

        elif iso_cut_information.__contains__("to"):
            color_elements = string_in_cut_cmdline.split("to")
            self.iso_gradient(color_elements[0], color_elements[1])
            return False

        elif iso_cut_information.__contains__("gradient") and iso_cut_information.__contains__("no"):
            self.curve_gradient_using = False

            for i in range(len(self.isoScaleList) + 1):
                if i == 0:
                    range_temp = "<" + str(self.isoScaleList[i]) + "," + self.markerList[i % self.colorNumber][0]
                elif i < len(self.isoScaleList):
                    range_temp = "[" + str(self.isoScaleList[i - 1]) + "," + str(self.isoScaleList[i]) + "[ : " + \
                                 self.markerList[i % self.colorNumber][0]
                else:
                    range_temp = ">=" + str(self.isoScaleList[i - 1]) + "," + self.markerList[i % self.colorNumber][0]

                self.isoRangeCheckList[i].setText(QString.fromUtf8(range_temp))
                self.isoRangeCheckList[i].setStyleSheet("background-color:" + self.colorList[i % self.colorNumber] + "; margin-left:6px; color: white")
            self.plot.set_current_iso_curves_no_linear_gradient()
            return False

        else:
            QMessageBox.question(self, 'Message', "Please represent values by semicolon(;) now do it again", QMessageBox.Yes)
            return False

        """
        if (max(self.isoCutPoints) > (self.iso_max + unit)) or (min(self.isoCutPoints) < (self.iso_min - unit)):
                QMessageBox.question(self, 'Message', "Please respect the range of the value, now do it again",
                                     QMessageBox.Yes)
                self.set_iso_parameter_range_information()
                return False
        """

        return True

    def verify_siso_cutting_information(self, string_in_cut_cmdline):
        unit = 0
        siso_cut_information = string_in_cut_cmdline.translate(None, " ")
        if siso_cut_information.__contains__(";"):
            del self.subListSISO[:]
            del self.subListSISOIndex[:]
            del self.sisoRangeCheckList[:]
            del self.sisoCutPoints[:]
            del self.sisoScaleList[:]
            cut_points = siso_cut_information.split(";")
            self.sisoCutPoints = map(float, cut_points)

        elif siso_cut_information.__contains__("[") and siso_cut_information.__contains__("]") and siso_cut_information.__contains__("/"):
            del self.subListSISO[:]
            del self.subListSISOIndex[:]
            del self.sisoRangeCheckList[:]
            del self.sisoCutPoints[:]
            del self.sisoScaleList[:]
            t1 = siso_cut_information.index("[")
            t2 = siso_cut_information.index("]")
            str1 = string_in_cut_cmdline[t1 + 1:t2]
            m = str1.split(",")

            v1 = float(m[0])
            v2 = float(m[1])

            v3 = int(siso_cut_information.split("/")[1])

            unit = abs(v1 - v2) / v3

            for i in range(0, v3 + 2):
                self.sisoCutPoints.append(v1 + unit * i - unit / 2)

        elif siso_cut_information.__contains__("->"):
            color_elements = string_in_cut_cmdline.split("->")
            if self.sisoDisplayMode == 'represent_by_color':
                self.siso_gradient(color_elements[0], color_elements[1])
                return False
            else:
                del self.sisoRangeCheckList[:]
                self.set_siso_config("represent_by_color")
                self.sisoScaleList = self.generate_scale_list("siso")

                if self.sisoDisplayMode == "represent_by_color":
                    self.update_text_or_color_for_table('iso', 'represent_by_marker')
                    self.generate_scale_list_for_table('siso', 'represent_by_color')
                elif self.sisoDisplayMode == "represent_by_marker":
                    self.update_text_or_color_for_table('iso', 'represent_by_color')
                    self.generate_scale_list_for_table('siso', 'represent_by_marker')

                self.clear_the_table_items('siso')
                self.apply_scale_list_on_table('siso')
                self.siso_gradient(color_elements[0], color_elements[1])
                return False

        elif siso_cut_information.__contains__("color"):
            del self.sisoRangeCheckList[:]
            self.set_siso_config("represent_by_color")
            # self.siso_gradient(color_elements[0], color_elements[1])
            return True

        elif siso_cut_information.__contains__("marker"):
            del self.sisoRangeCheckList[:]
            self.set_siso_config("represent_by_marker")
            # self.siso_gradient(color_elements[0], color_elements[1])
            return True

        elif siso_cut_information.__contains__("gradient") and siso_cut_information.__contains__("no"):
            self.curve_gradient_using = False
            self.update_text_or_color_for_table('siso', 'represent_by_color')
            self.plot.cut_current_curves_by_siso(self.sisoDisplayMode)

            return False
        else:
            QMessageBox.question(self, 'Message', "Please represent values by semicolon(;) now do it again",
                                 QMessageBox.Yes)
            return False
        """
        if (max(self.sisoCutPoints) > (self.siso_max + unit)) or (min(self.sisoCutPoints) < (self.siso_min - unit)):
                QMessageBox.question(self, 'Message', "Please respect the range of the value, now do it again",
                                     QMessageBox.Yes)
                self.set_siso_parameter_range_information()
                return False
        """

        return True

    def generate_scale_list_for_table(self, parameter_type, display_mode):
        page_index = self.plottingBoardReference.get_page_index()
        plotting_index = self.plottingBoardReference.get_plotting_index()
        plotting_context = self.analyserMediator.get_a_plotting_context(page_index, plotting_index)
        if parameter_type == 'iso':
            if display_mode == 'represent_by_marker':
                if plotting_context.get_iso_display_mode() == 0:
                    for i in range(len(self.isoScaleList) + 1):
                        if i == 0:
                            range_temp = "<" + str(self.isoScaleList[i]) + "," + self.markerList[i % self.colorNumber][0]
                        elif i < len(self.isoScaleList):
                            range_temp = "[" + str(self.isoScaleList[i - 1]) + "," + str(self.isoScaleList[i]) + "[ : " + \
                                         self.markerList[i % self.colorNumber][0]
                        else:
                            range_temp = ">=" + str(self.isoScaleList[i - 1]) + "," + self.markerList[i % self.colorNumber][0]

                        checkbox = QCheckBox(QString.fromUtf8(range_temp))
                        sub_cutting_value_list = []
                        sub_cutting_index_list = []
                        self.subListISO.append(sub_cutting_value_list)
                        self.subListISOIndex.append(sub_cutting_index_list)
                        checkbox.setStyleSheet("background-color: transparent; margin-left:0px;")
                        self.isoRangeCheckList.append(checkbox)

                elif plotting_context.get_iso_display_mode() == 1:
                    for i in range(len(self.isoScaleList) + 1):
                        range_temp = str(self.isoCutPoints[i]) + "," + self.markerList[i % self.colorNumber][0]
                        checkbox = QCheckBox(QString.fromUtf8(range_temp))
                        sub_cutting_value_list = []
                        sub_cutting_index_list = []
                        self.subListISO.append(sub_cutting_value_list)
                        self.subListISOIndex.append(sub_cutting_index_list)
                        checkbox.setStyleSheet("background-color: transparent; margin-left:0px;")
                        self.isoRangeCheckList.append(checkbox)

            elif display_mode == 'represent_by_color':
                if plotting_context.get_iso_display_mode() == 0:
                    for i in range(len(self.isoScaleList) + 1):
                        if i == 0:
                            range_temp = "<" + str(self.isoScaleList[i])
                        elif i < len(self.isoScaleList):
                            range_temp = "[" + str(self.isoScaleList[i - 1]) + "," + str(self.isoScaleList[i]) + "["
                        else:
                            range_temp = ">=" + str(self.isoScaleList[i - 1])

                        checkbox = QCheckBox(QString.fromUtf8(range_temp), self)
                        sub_cutting_value_list = []
                        sub_cutting_index_list = []
                        self.subListISO.append(sub_cutting_value_list)
                        self.subListISOIndex.append(sub_cutting_index_list)
                        checkbox.setStyleSheet(
                            "background-color:" + self.colorList[i % self.colorNumber] + "; margin-left:6px; color: white")
                        self.isoRangeCheckList.append(checkbox)
                elif plotting_context.get_iso_display_mode() == 1:
                    for i in range(len(self.isoScaleList) + 1):
                        range_temp = str(self.isoCutPoints[i])
                        checkbox = QCheckBox(QString.fromUtf8(range_temp), self)
                        sub_cutting_value_list = []
                        sub_cutting_index_list = []
                        self.subListISO.append(sub_cutting_value_list)
                        self.subListISOIndex.append(sub_cutting_index_list)
                        checkbox.setStyleSheet(
                            "background-color:" + self.colorList[i % self.colorNumber] + "; margin-left:6px; color: white")
                        self.isoRangeCheckList.append(checkbox)
            else:
                if plotting_context.get_iso_display_mode() == 0:
                    for i in range(len(self.isoScaleList) + 1):
                        if i == 0:
                            range_temp = "<" + str(self.isoScaleList[i]) + "," + self.markerList[i % self.colorNumber][0]
                        elif i < len(self.isoScaleList):
                            range_temp = "[" + str(self.isoScaleList[i - 1]) + "," + str(self.isoScaleList[i]) + "[ : " + \
                                         self.markerList[i % self.colorNumber][0]
                        else:
                            range_temp = ">=" + str(self.isoScaleList[i - 1]) + "," + self.markerList[i % self.colorNumber][0]

                        checkbox = QCheckBox(QString.fromUtf8(range_temp), self)
                        sub_cutting_value_list = []
                        sub_cutting_index_list = []
                        self.subListISO.append(sub_cutting_value_list)
                        self.subListISOIndex.append(sub_cutting_index_list)
                        checkbox.setStyleSheet(
                            "background-color:" + self.colorList[i % self.colorNumber] + "; margin-left:6px; color: white")
                        self.isoRangeCheckList.append(checkbox)
                elif plotting_context.get_iso_display_mode() == 1:
                    for i in range(len(self.isoScaleList) + 1):
                        range_temp = str(self.isoCutPoints[i]) + "," + self.markerList[i % self.colorNumber][0]
                        checkbox = QCheckBox(QString.fromUtf8(range_temp), self)
                        sub_cutting_value_list = []
                        sub_cutting_index_list = []
                        self.subListISO.append(sub_cutting_value_list)
                        self.subListISOIndex.append(sub_cutting_index_list)
                        checkbox.setStyleSheet(
                            "background-color:" + self.colorList[i % self.colorNumber] + "; margin-left:6px; color: white")
                        self.isoRangeCheckList.append(checkbox)
            self.isoDisplayMode = display_mode

        elif parameter_type == 'siso':
            if display_mode == 'represent_by_color':
                if plotting_context.get_siso_display_mode() == 0:
                    for i in range(len(self.sisoScaleList) + 1):
                        if i == 0:
                            range_temp = "<" + str(self.sisoScaleList[i])
                        elif i < len(self.sisoScaleList):
                            range_temp = "[" + str(self.sisoScaleList[i - 1]) + "," + str(self.sisoScaleList[i]) + "["
                        else:
                            range_temp = ">=" + str(self.sisoScaleList[i - 1]) + ","

                        checkbox = QCheckBox(QString.fromUtf8(range_temp), self)
                        sub_cutting_value_list = []
                        sub_cutting_index_list = []
                        self.subListSISO.append(sub_cutting_value_list)
                        self.subListSISOIndex.append(sub_cutting_index_list)
                        checkbox.setStyleSheet(
                            "background-color:" + self.colorList[i % self.colorNumber] + "; margin-left:6px; color: white")
                        self.sisoRangeCheckList.append(checkbox)
                elif plotting_context.get_siso_display_mode() == 1:
                    for i in range(len(self.sisoScaleList) + 1):
                        range_temp = str(self.sisoCutPoints[i])
                        checkbox = QCheckBox(QString.fromUtf8(range_temp), self)
                        sub_cutting_value_list = []
                        sub_cutting_index_list = []
                        self.subListSISO.append(sub_cutting_value_list)
                        self.subListSISOIndex.append(sub_cutting_index_list)
                        checkbox.setStyleSheet(
                            "background-color:" + self.colorList[i % self.colorNumber] + "; margin-left:6px; color: white")
                        self.sisoRangeCheckList.append(checkbox)

            elif display_mode == 'represent_by_marker':
                if plotting_context.get_siso_display_mode() == 0:
                    for i in range(len(self.sisoScaleList) + 1):
                        if i == 0:
                            range_temp = "<" + str(self.sisoScaleList[i]) + "," + self.markerList[i % self.colorNumber][0]
                        elif i < len(self.sisoScaleList):
                            range_temp = "[" + str(self.sisoScaleList[i - 1]) + "," + str(self.sisoScaleList[i]) + "[ : " + \
                                         self.markerList[i % self.colorNumber][0]
                        else:
                            range_temp = ">=" + str(self.sisoScaleList[i - 1]) + "," + self.markerList[i % self.colorNumber][0]

                        checkbox = QCheckBox(QString.fromUtf8(range_temp), self)
                        sub_cutting_value_list = []
                        sub_cutting_index_list = []
                        self.subListSISO.append(sub_cutting_value_list)
                        self.subListSISOIndex.append(sub_cutting_index_list)
                        self.sisoRangeCheckList.append(checkbox)
                elif plotting_context.get_siso_display_mode() == 1:
                    for i in range(len(self.sisoScaleList) + 1):
                        range_temp = str(self.sisoCutPoints[i]) + "," + self.markerList[i % self.colorNumber][0]
                        checkbox = QCheckBox(QString.fromUtf8(range_temp), self)
                        sub_cutting_value_list = []
                        sub_cutting_index_list = []
                        self.subListSISO.append(sub_cutting_value_list)
                        self.subListSISOIndex.append(sub_cutting_index_list)
                        self.sisoRangeCheckList.append(checkbox)
            self.sisoDisplayMode = display_mode

    def update_text_or_color_for_table(self, parameter_type, display_mode):

        page_index = self.plottingBoardReference.get_page_index()
        plotting_index = self.plottingBoardReference.get_plotting_index()
        plotting_context = self.analyserMediator.get_a_plotting_context(page_index, plotting_index)

        if parameter_type == 'iso':
            if display_mode == 'represent_by_marker':
                if plotting_context.get_iso_display_mode() == 0:
                    for i in range(len(self.isoScaleList) + 1):
                        if i == 0:
                            range_temp = "<" + str(self.isoScaleList[i]) + "," + self.markerList[i % self.colorNumber][0]
                        elif i < len(self.isoScaleList):
                            range_temp = "[" + str(self.isoScaleList[i - 1]) + "," + str(self.isoScaleList[i]) + "[ : " + \
                                         self.markerList[i % self.colorNumber][0]
                        else:
                            range_temp = ">=" + str(self.isoScaleList[i - 1]) + "," + self.markerList[i % self.colorNumber][0]

                        self.isoRangeCheckList[i].setText(QString.fromUtf8(range_temp))
                        self.isoRangeCheckList[i].setStyleSheet("background-color: white; margin-left:6px; color: black")
                elif plotting_context.get_iso_display_mode() == 1:
                    for i in range(len(self.isoScaleList) + 1):
                        range_temp = str(self.isoCutPoints[i]) + "," + self.markerList[i % self.colorNumber][0]
                        self.isoRangeCheckList[i].setText(QString.fromUtf8(range_temp))
                        self.isoRangeCheckList[i].setStyleSheet("background-color: white; margin-left:6px; color: black")

            elif display_mode == 'represent_by_color':
                if plotting_context.get_iso_display_mode() == 0:
                    for i in range(len(self.isoScaleList) + 1):
                        if i == 0:
                            range_temp = "<" + str(self.isoScaleList[i])
                        elif i < len(self.isoScaleList):
                            range_temp = "[" + str(self.isoScaleList[i - 1]) + "," + str(self.isoScaleList[i]) + "["
                        else:
                            range_temp = ">=" + str(self.isoScaleList[i - 1])

                        self.isoRangeCheckList[i].setText(QString.fromUtf8(range_temp))
                        self.isoRangeCheckList[i].setStyleSheet(
                            "background-color:" + self.colorList[i % self.colorNumber] + "; margin-left:6px; color: white")

                elif plotting_context.get_iso_display_mode() == 1:
                    for i in range(len(self.isoScaleList) + 1):
                        range_temp = str(self.isoCutPoints[i])
                        self.isoRangeCheckList[i].setText(QString.fromUtf8(range_temp))
                        self.isoRangeCheckList[i].setStyleSheet(
                            "background-color:" + self.colorList[i % self.colorNumber] + "; margin-left:6px; color: white")
            else:
                if plotting_context.get_iso_display_mode() == 0:
                    for i in range(len(self.isoScaleList) + 1):
                        if i == 0:
                            range_temp = "<" + str(self.isoScaleList[i]) + "," + self.markerList[i % self.colorNumber][0]
                        elif i < len(self.isoScaleList):
                            range_temp = "[" + str(self.isoScaleList[i - 1]) + "," + str(self.isoScaleList[i]) + "[ : " + \
                                         self.markerList[i % self.colorNumber][0]
                        else:
                            range_temp = ">=" + str(self.isoScaleList[i - 1]) + "," + self.markerList[i % self.colorNumber][0]

                        self.isoRangeCheckList[i].setText(QString.fromUtf8(range_temp))
                        self.isoRangeCheckList[i].setStyleSheet(
                            "background-color:" + self.colorList[i % self.colorNumber] + "; margin-left:6px; color: white")

                elif plotting_context.get_iso_display_mode() == 1:
                    for i in range(len(self.isoScaleList) + 1):
                        range_temp = str(self.isoCutPoints[i]) + "," + self.markerList[i % self.colorNumber][0]
                        self.isoRangeCheckList[i].setText(QString.fromUtf8(range_temp))
                        self.isoRangeCheckList[i].setStyleSheet("background-color:" + self.colorList[i % self.colorNumber] + "; margin-left:6px; color: white")
            self.isoDisplayMode = display_mode
        elif parameter_type == 'siso':
            if self.siso_existed:
                if display_mode == 'represent_by_marker':
                    if plotting_context.get_siso_display_mode() == 0:
                        for i in range(len(self.sisoScaleList) + 1):
                            if i == 0:
                                range_temp = "<" + str(self.sisoScaleList[i]) + "," + self.markerList[i % self.colorNumber][0]
                            elif i < len(self.sisoScaleList):
                                range_temp = "[" + str(self.sisoScaleList[i - 1]) + "," + str(self.sisoScaleList[i]) + "[ : " + \
                                             self.markerList[i % self.colorNumber][0]
                            else:
                                range_temp = ">=" + str(self.sisoScaleList[i - 1]) + "," + self.markerList[i % self.colorNumber][0]

                            self.sisoRangeCheckList[i].setText(QString.fromUtf8(range_temp))
                            self.sisoRangeCheckList[i].setStyleSheet("background-color: white; margin-left:6px; color: black")
                    elif plotting_context.get_siso_display_mode() == 1:
                        for i in range(len(self.sisoScaleList) + 1):
                            range_temp = str(self.sisoCutPoints[i]) + "," + self.markerList[i % self.colorNumber][0]
                            self.sisoRangeCheckList[i].setText(QString.fromUtf8(range_temp))
                            self.sisoRangeCheckList[i].setStyleSheet("background-color: white; margin-left:6px; color: black")

                elif display_mode == 'represent_by_color':
                    if plotting_context.get_siso_display_mode() == 0:
                        for i in range(len(self.sisoScaleList) + 1):
                            if i == 0:
                                range_temp = "<" + str(self.sisoScaleList[i])
                            elif i < len(self.sisoScaleList):
                                range_temp = "[" + str(self.sisoScaleList[i - 1]) + "," + str(self.sisoScaleList[i]) + "["
                            else:
                                range_temp = ">=" + str(self.sisoScaleList[i - 1])

                            self.sisoRangeCheckList[i].setText(QString.fromUtf8(range_temp))
                            self.sisoRangeCheckList[i].setStyleSheet(
                                "background-color:" + self.colorList[i % self.colorNumber] + "; margin-left:6px; color: white")

                    elif plotting_context.get_siso_display_mode() == 1:
                        for i in range(len(self.sisoScaleList) + 1):
                            range_temp = str(self.sisoCutPoints[i])
                            self.sisoRangeCheckList[i].setText(QString.fromUtf8(range_temp))
                            self.sisoRangeCheckList[i].setStyleSheet(
                                "background-color:" + self.colorList[i % self.colorNumber] + "; margin-left:6px; color: white")
                else:
                    if plotting_context.get_siso_display_mode() == 0:
                        for i in range(len(self.sisoScaleList) + 1):
                            if i == 0:
                                range_temp = "<" + str(self.sisoScaleList[i]) + "," + self.markerList[i % self.colorNumber][0]
                            elif i < len(self.isoScaleList):
                                range_temp = "[" + str(self.sisoScaleList[i - 1]) + "," + str(self.sisoScaleList[i]) + "[ : " + \
                                             self.markerList[i % self.colorNumber][0]
                            else:
                                range_temp = ">=" + str(self.sisoScaleList[i - 1]) + "," + self.markerList[i % self.colorNumber][0]

                            self.sisoRangeCheckList[i].setText(QString.fromUtf8(range_temp))
                            self.sisoRangeCheckList[i].setStyleSheet(
                                "background-color:" + self.colorList[i % self.colorNumber] + "; margin-left:6px; color: white")

                    elif plotting_context.get_siso_display_mode() == 1:
                        for i in range(len(self.sisoScaleList) + 1):
                            range_temp = str(self.sisoCutPoints[i]) + "," + self.markerList[i % self.colorNumber][0]
                            self.sisoRangeCheckList[i].setText(QString.fromUtf8(range_temp))
                            self.sisoRangeCheckList[i].setStyleSheet("background-color:" + self.colorList[i % self.colorNumber] + "; margin-left:6px; color: white")
                self.sisoDisplayMode = display_mode

    def clear_the_table_items(self, table_flag):
        if table_flag == 'iso':
            row_count_temp = self.isoConfigTable.rowCount()
            if row_count_temp > 2:
                for i in range(2, row_count_temp)[::-1]:
                    self.isoConfigTable.removeRow(i)
                    self.isoConfigTableRowCount -= 1
        elif table_flag == 'siso':
            row_count_temp = self.sisoConfigTable.rowCount()
            if row_count_temp > 2:
                for i in range(2, row_count_temp)[::-1]:
                    self.sisoConfigTable.removeRow(i)
                    self.sisoConfigTableRowCount -= 1

    def apply_scale_list_on_table(self, parameter_type):
        if parameter_type == 'iso':
            for i in range(0, len(self.isoRangeCheckList)):
                self.connect(self.isoRangeCheckList[i], SIGNAL("clicked()"), self.iso_range_check_list_changed)
                self.isoConfigTableRowCount += 1
                self.isoConfigTable.insertRow(self.isoConfigTableRowCount - 1)
                self.isoConfigTable.setCellWidget(i + 2, 0, self.isoRangeCheckList[i])
                self.isoConfigTable.setRowHeight(i + 2, 20)
        elif parameter_type == 'siso':
            for i in range(0, len(self.sisoRangeCheckList)):
                self.connect(self.sisoRangeCheckList[i], SIGNAL("clicked()"), self.siso_range_check_list_changed)
                self.sisoConfigTableRowCount += 1
                self.sisoConfigTable.insertRow(self.sisoConfigTableRowCount - 1)
                self.sisoConfigTable.setCellWidget(i + 2, 0, self.sisoRangeCheckList[i])
                self.sisoConfigTable.setRowHeight(i + 2, 20)

    def set_iso_cutting_information_by_lom_file(self, new_iso_cutting_command, iso_name):
        self.isoLabel.setText(iso_name)
        self.ISO_cmdline.setText(new_iso_cutting_command)
        self.iso_commandline_return_pressed()
        for i in self.isoRangeCheckList:
            i.setChecked(True)

    def set_siso_cutting_information_by_lom_file(self, new_siso_cutting_command, siso_name):
        self.siso_existed = True
        self.sisoLabel.setText(siso_name)
        self.SISO_cmdline.setText(new_siso_cutting_command)
        self.siso_commandline_return_pressed()
        for i in self.sisoRangeCheckList:
            i.setChecked(True)

    def replace_iso_cutting_information_by_lom_file(self, new_iso_cutting_command):
        self.ISO_cmdline.setText(new_iso_cutting_command)
        self.iso_commandline_return_pressed()
        for i in self.isoRangeCheckList:
            i.setChecked(True)
        self.iso_range_check_list_changed()

    def replace_siso_cutting_information_by_lom_file(self, new_siso_cutting_command):
        self.SISO_cmdline.setText(new_siso_cutting_command)
        self.siso_commandline_return_pressed()
        for i in self.sisoRangeCheckList:
            i.setChecked(True)
        self.siso_range_check_list_changed()

    def iso_commandline_return_pressed(self):
        # Do not need to analyse second time with the same command
        if self.isoCutInformation == str(self.ISO_cmdline.text()):
            # QMessageBox.question(self, 'Message', "Do not return the same command", QMessageBox.Yes)
            return

        # Assign the string entered from the text line to the self.isoCutInformation
        self.isoCutInformation = str(self.ISO_cmdline.text())
        if self.analyserMediator.get_filetype_handling_from_context() != "lom" and self.plot.ask_if_curve_from_csv_existed():
            self.analyserMediator.generate_an_action_into_global_context('set iso cut information: (' + self.isoCutInformation + ') for plotting board :'
                                                                         + str(self.plottingBoardReference.get_plotting_index()) + ' in page: '
                                                                         + str(self.plottingBoardReference.get_page_index()))

        # Check the command to identifier what user want to do for iso
        if not self.verify_iso_cutting_information(self.isoCutInformation):
            return

        # Generate the scale list which will be used for the cutting actions
        self.isoScaleList = self.generate_scale_list("iso")

        # if siso existed already, we have to make a little modification on the iso table according to the siso's display mode
        # else, we cut & display the iso's information use the default mode
        if self.siso_existed:
            if self.sisoDisplayMode == "represent_by_color":
                self.generate_scale_list_for_table('iso', 'represent_by_marker')
            elif self.sisoDisplayMode == "represent_by_marker":
                self.generate_scale_list_for_table('iso', 'represent_by_color')
        else:
            self.generate_scale_list_for_table('iso', None)
        self.clear_the_table_items('iso')
        self.apply_scale_list_on_table('iso')

    def iso_commandline_return_pressed_while_import(self, iso_cut_information):

        self.ISO_cmdline.setText(iso_cut_information)

        # Do not need to analyse second time with the same command
        if self.isoCutInformation == str(self.ISO_cmdline.text()):
            # QMessageBox.question(self, 'Message', "Do not return the same command", QMessageBox.Yes)
            return

        # Assign the string entered from the text line to the self.isoCutInformation
        self.isoCutInformation = str(self.ISO_cmdline.text())
        if self.analyserMediator.get_filetype_handling_from_context() != "lom" and self.plot.ask_if_curve_from_csv_existed():
            self.analyserMediator.generate_an_action_into_global_context('set iso cut information: (' + self.isoCutInformation + ') for plotting board :'
                                                                         + str(self.plottingBoardReference.get_plotting_index()) + ' in page: '
                                                                         + str(self.plottingBoardReference.get_page_index()))

        # Check the command to identifier what user want to do for iso
        if not self.verify_iso_cutting_information(self.isoCutInformation):
            return

        # Generate the scale list which will be used for the cutting actions
        self.isoScaleList = self.generate_scale_list("iso")

        # if siso existed already, we have to make a little modification on the iso table according to the siso's display mode
        # else, we cut & display the iso's information use the default mode
        if self.siso_existed:
            if self.sisoDisplayMode == "represent_by_color":
                self.generate_scale_list_for_table('iso', 'represent_by_marker')
            elif self.sisoDisplayMode == "represent_by_marker":
                self.generate_scale_list_for_table('iso', 'represent_by_color')
        else:
            self.generate_scale_list_for_table('iso', None)
        self.clear_the_table_items('iso')
        self.apply_scale_list_on_table('iso')

    def siso_commandline_return_pressed(self):
        if not self.verify_siso_cutting_information(str(self.SISO_cmdline.text())):
            return

        self.sisoCutInformation = str(self.SISO_cmdline.text())
        if self.analyserMediator.get_filetype_handling_from_context() != "lom":
            self.analyserMediator.generate_an_action_into_global_context('set siso cut information: (' + self.sisoCutInformation + ') for plotting board :'
                                                                         + str(self.plottingBoardReference.get_plotting_index()) + ' in page: '
                                                                         + str(self.plottingBoardReference.get_page_index()))
        self.sisoScaleList = self.generate_scale_list("siso")

        if self.sisoDisplayMode == "represent_by_color":
            self.update_text_or_color_for_table('iso', 'represent_by_marker')
            self.generate_scale_list_for_table('siso', 'represent_by_color')
        elif self.sisoDisplayMode == "represent_by_marker":
            self.update_text_or_color_for_table('iso', 'represent_by_color')
            self.generate_scale_list_for_table('siso', 'represent_by_marker')

        self.clear_the_table_items('siso')
        self.apply_scale_list_on_table('siso')

    def siso_commandline_return_pressed_while_import(self, siso_cut_information):
        self.SISO_cmdline.setText(siso_cut_information)

        if not self.verify_siso_cutting_information(str(self.SISO_cmdline.text())):
            return

        self.sisoCutInformation = str(self.SISO_cmdline.text())
        if self.analyserMediator.get_filetype_handling_from_context() != "lom":
            self.analyserMediator.generate_an_action_into_global_context('set siso cut information: (' + self.sisoCutInformation + ') for plotting board :'
                                                                         + str(self.plottingBoardReference.get_plotting_index()) + ' in page: '
                                                                         + str(self.plottingBoardReference.get_page_index()))
        self.sisoScaleList = self.generate_scale_list("siso")

        if self.sisoDisplayMode == "represent_by_color":
            self.update_text_or_color_for_table('iso', 'represent_by_marker')
            self.generate_scale_list_for_table('siso', 'represent_by_color')
        elif self.sisoDisplayMode == "represent_by_marker":
            self.update_text_or_color_for_table('iso', 'represent_by_color')
            self.generate_scale_list_for_table('siso', 'represent_by_marker')

        self.clear_the_table_items('siso')
        self.apply_scale_list_on_table('siso')

    def set_sub_lists_of_iso_information(self):
        """Calculate a new list of iso for each csv file loaded
        an example:
            iso [1,2,3,4,5,6]
            isoCutCommand = 2;4
            sub_list_iso_value: '>=3': [3,4,5,6], '<3': [1,2]
            sub_list_iso_index: '>=3': [2,3,4,5], '<3': [0,1]
                ==> assign two list into the plotting context according to csv file's name
        """

        page_index = self.plottingBoardReference.get_page_index()
        plotting_index = self.plottingBoardReference.get_plotting_index()
        plotting_context = self.analyserMediator.get_a_plotting_context(page_index, plotting_index)
        loaded_csv_files = self.analyserMediator.get_loaded_csv_files_from_context(page_index, plotting_index)
        loaded_csvfiles_validity = self.analyserMediator.get_loaded_csv_files_validity_from_context(page_index, plotting_index)

        # Generate a list with the dimension [number_of_csv_file X iso's_range_number]
        sub_list_iso_values = [[[] for y in range(len(self.isoRangeCheckList))] for y in range(len(loaded_csv_files))]
        sub_list_iso_indexs = [[[] for y in range(len(self.isoRangeCheckList))] for y in range(len(loaded_csv_files))]

        # Calculate the sub list of iso after the cutting action and assign them into the tree structure in the plotting context
        cpt = 0
        for csv_file_name in loaded_csv_files:
            if not loaded_csvfiles_validity[loaded_csv_files.index(csv_file_name)]:
                continue
            csvfile = self.analyserMediator.get_csv_file_in_context_by_name(csv_file_name)
            iso_values = plotting_context.get_iso_parameter_values(csv_file_name)
            row_count = csvfile.get_row_count()
            del self.iso_check_list[:]
            for i in range(len(self.isoRangeCheckList)):

                if self.isoRangeCheckList[i].isChecked():
                    self.iso_check_list.append(1)
                    if i == 0:
                        for j in range(row_count):
                            if iso_values[j] < self.isoScaleList[i]:
                                sub_list_iso_values[cpt][i].append(iso_values[j])
                                sub_list_iso_indexs[cpt][i].append(j)
                    elif 0 < i < len(self.isoRangeCheckList) - 1:
                        for j in range(row_count):
                            if self.isoScaleList[i - 1] <= iso_values[j] < self.isoScaleList[i]:
                                sub_list_iso_values[cpt][i].append(iso_values[j])
                                sub_list_iso_indexs[cpt][i].append(j)
                    else:
                        for j in range(row_count):
                            if self.isoScaleList[i - 1] <= iso_values[j]:
                                sub_list_iso_values[cpt][i].append(iso_values[j])
                                sub_list_iso_indexs[cpt][i].append(j)
                else:
                    self.iso_check_list.append(0)

            plotting_context.set_sub_lists_of_iso_index(sub_list_iso_indexs[cpt], csv_file_name)
            plotting_context.set_sub_lists_of_iso(sub_list_iso_values[cpt], csv_file_name)
            cpt += 1

        del sub_list_iso_values[:]
        del sub_list_iso_indexs[:]

    def set_iso_validity_for_lom(self):
        page_index = self.plottingBoardReference.get_page_index()
        plotting_index = self.plottingBoardReference.get_plotting_index()
        loaded_lomfiles = self.analyserMediator.get_loaded_lom_files_from_context(page_index, plotting_index)
        loaded_lomfiles_validity = self.analyserMediator.get_loaded_lom_files_validity_from_context(page_index, plotting_index)
        plotting_context = self.analyserMediator.get_a_plotting_context(page_index, plotting_index)

        if self.lom_existed:
            for lom_file_name in loaded_lomfiles:
                if not loaded_lomfiles_validity[loaded_lomfiles.index(lom_file_name)]:
                    continue
                for label_name in plotting_context.get_label_list_from_lom_file(lom_file_name):
                    iso_validity = plotting_context.get_iso_parameter_validity_from_lom_file(label_name, lom_file_name)
                    del self.iso_check_list[:]
                    for i in range(len(self.isoRangeCheckList)):

                        if self.isoRangeCheckList[i].isChecked():
                            self.iso_check_list.append(1)
                            iso_validity[i] = 1
                        else:
                            self.iso_check_list.append(0)
                            iso_validity[i] = 0

    def iso_range_check_list_changed(self):
        # if siso not existed currently
        if not self.siso_existed:
            self.set_sub_lists_of_iso_information()
            self.plot.cut_current_curves_by_iso()
            self.set_iso_validity_for_lom()
            self.plot.replot_current_lom_curves()
        else:
            self.set_sub_lists_of_iso_information()  # for csv files
            self.set_iso_validity_for_lom()
            self.siso_range_check_list_changed()

        iso_check_list_string = ''
        for x in self.iso_check_list:
            iso_check_list_string += str(x) + ','
        iso_check_list_string = iso_check_list_string[:-1]

        self.analyserMediator.generate_an_action_into_global_context('set iso check information: (' + iso_check_list_string + ') for plotting board :'
                                                                         + str(self.plottingBoardReference.get_plotting_index()) + ' in page: '
                                                                         + str(self.plottingBoardReference.get_page_index()))

    def update_canvas(self):
        self.set_iso_validity_for_lom()
        self.plot.refresh_curves_on_canvas()
        self.plot.replot_current_lom_curves()

    def iso_gradient(self, start_color, finish_color):

        self.isoScaleList = self.generate_scale_list("iso")
        length = len(self.isoRangeCheckList)

        if self.siso_existed:
            if self.sisoDisplayMode == "represent_by_color":
                if (start_color == "red") and (finish_color == "yellow"):
                    for i in range(length):
                        self.isoRangeCheckList[i].setCheckState(Qt.Checked)
                        color_string = "rgb(255, " + str(int(float(i) * 255 / length)) + ", 0)"
                        self.isoRangeCheckList[i].setStyleSheet(
                            "background-color:" + color_string + "; margin-left:6px; color: white")
                elif (start_color == "green") and (finish_color == "yellow"):
                    for i in range(length):
                        self.isoRangeCheckList[i].setCheckState(Qt.Checked)
                        color_string = "rgb(" + str(int(float(i) * 255 / length)) + ",255 , 0)"
                        self.isoRangeCheckList[i].setStyleSheet(
                            "background-color:" + color_string + "; margin-left:6px; color: white")
                elif (start_color == "blue") and (finish_color == "cyan"):
                    for i in range(length):
                        self.isoRangeCheckList[i].setCheckState(Qt.Checked)
                        color_string = "rgb(0, " + str(int(float(i) * 255 / length)) + ",255)"
                        self.isoRangeCheckList[i].setStyleSheet(
                            "background-color:" + color_string + "; margin-left:6px; color: white")

                self.update_text_or_color_for_table('siso', 'represent_by_marker')

            elif self.sisoDisplayMode == "represent_by_marker":
                if (start_color == "red") and (finish_color == "yellow"):
                    for i in range(length):
                        self.isoRangeCheckList[i].setCheckState(Qt.Checked)
                        color_string = "rgb(255, " + str(int(float(i) * 255 / length)) + ", 0)"
                        self.isoRangeCheckList[i].setStyleSheet(
                            "background-color:" + color_string + "; margin-left:6px; color: white")
                elif (start_color == "green") and (finish_color == "yellow"):
                    for i in range(length):
                        self.isoRangeCheckList[i].setCheckState(Qt.Checked)
                        color_string = "rgb(" + str(int(float(i) * 255 / length)) + ",255 , 0)"
                        self.isoRangeCheckList[i].setStyleSheet(
                            "background-color:" + color_string + "; margin-left:6px; color: white")
                elif (start_color == "blue") and (finish_color == "cyan"):
                    for i in range(length):
                        self.isoRangeCheckList[i].setCheckState(Qt.Checked)
                        color_string = "rgb(0, " + str(int(float(i) * 255 / length)) + ",255)"
                        self.isoRangeCheckList[i].setStyleSheet(
                            "background-color:" + color_string + "; margin-left:6px; color: white")
        else:
            if (start_color == "red") and (finish_color == "yellow"):
                for i in range(length):
                    self.isoRangeCheckList[i].setCheckState(Qt.Checked)
                    color_string = "rgb(255, " + str(int(float(i) * 255 / length)) + ", 0)"
                    self.isoRangeCheckList[i].setStyleSheet(
                        "background-color:" + color_string + "; margin-left:6px; color: white")
            elif (start_color == "green") and (finish_color == "yellow"):
                for i in range(length):
                    self.isoRangeCheckList[i].setCheckState(Qt.Checked)
                    color_string = "rgb(" + str(int(float(i) * 255 / length)) + ",255 , 0)"
                    self.isoRangeCheckList[i].setStyleSheet(
                        "background-color:" + color_string + "; margin-left:6px; color: white")
            elif (start_color == "blue") and (finish_color == "cyan"):
                for i in range(length):
                    self.isoRangeCheckList[i].setCheckState(Qt.Checked)
                    color_string = "rgb(0, " + str(int(float(i) * 255 / length)) + ",255)"
                    self.isoRangeCheckList[i].setStyleSheet(
                        "background-color:" + color_string + "; margin-left:6px; color: white")

            page_index = self.plottingBoardReference.get_page_index()
            plotting_index = self.plottingBoardReference.get_plotting_index()
            loaded_csvfiles = self.analyserMediator.get_loaded_csv_files_from_context(page_index, plotting_index)
            loaded_csvfiles_validity = self.analyserMediator.get_loaded_csv_files_validity_from_context(page_index, plotting_index)
            plotting_context = self.analyserMediator.get_a_plotting_context(page_index, plotting_index)

            sub_list_iso_values = [[[] for y in range(len(self.isoRangeCheckList))] for y in range(len(loaded_csvfiles))]
            sub_list_iso_indexs = [[[] for y in range(len(self.isoRangeCheckList))] for y in range(len(loaded_csvfiles))]
            cpt = 0
            for filename in loaded_csvfiles:
                if not loaded_csvfiles_validity[loaded_csvfiles.index(filename)]:
                    continue
                csvfile = self.analyserMediator.get_csv_file_in_context_by_name(filename)
                iso_values = plotting_context.get_iso_parameter_values(filename)
                row_count = csvfile.get_row_count()
                for i in range(len(self.isoRangeCheckList)):
                    if self.isoRangeCheckList[i].isChecked():
                        if i == 0:
                            for j in range(row_count):
                                if iso_values[j] < self.isoScaleList[i]:
                                    sub_list_iso_values[cpt][i].append(iso_values[j])
                                    sub_list_iso_indexs[cpt][i].append(j)

                        elif 0 < i < len(self.isoRangeCheckList) - 1:  # TODO A Verifier
                            for j in range(row_count):
                                if self.isoScaleList[i - 1] <= iso_values[j] < self.isoScaleList[i]:
                                    sub_list_iso_values[cpt][i].append(iso_values[j])
                                    sub_list_iso_indexs[cpt][i].append(j)
                        else:
                            for j in range(row_count):
                                if self.isoScaleList[i - 1] <= iso_values[j]:
                                    sub_list_iso_values[cpt][i].append(iso_values[j])
                                    sub_list_iso_indexs[cpt][i].append(j)
                plotting_context.set_sub_lists_of_iso_index(sub_list_iso_indexs[cpt], filename)
                plotting_context.set_sub_lists_of_iso(sub_list_iso_values[cpt], filename)
                cpt += 1

            # self.myCurveChartInformation.print_data_center()
            del sub_list_iso_values[:]
            del sub_list_iso_indexs[:]

        self.plot.set_current_iso_curves_linear_gradient(start_color, finish_color)
        self.curve_gradient_using = True

    def siso_gradient(self, start_color, finish_color):
        self.update_text_or_color_for_table('iso', 'represent_by_marker')

        length = len(self.sisoRangeCheckList)
        if (start_color == "red") and (finish_color == "yellow"):
            for i in range(length):
                self.sisoRangeCheckList[i].setCheckState(Qt.Checked)
                color_string = "rgb(255, " + str(int(float(i) * 255 / length)) + ", 0)"
                self.sisoRangeCheckList[i].setStyleSheet(
                    "background-color:" + color_string + "; margin-left:6px; color: white")
        elif (start_color == "green") and (finish_color == "yellow"):
            for i in range(length):
                self.sisoRangeCheckList[i].setCheckState(Qt.Checked)
                color_string = "rgb(" + str(int(float(i) * 255 / length)) + ",255 , 0)"
                self.sisoRangeCheckList[i].setStyleSheet(
                    "background-color:" + color_string + "; margin-left:6px; color: white")
        elif (start_color == "blue") and (finish_color == "cyan"):
            for i in range(length):
                self.sisoRangeCheckList[i].setCheckState(Qt.Checked)
                color_string = "rgb(0, " + str(int(float(i) * 255 / length)) + ",255)"
                self.sisoRangeCheckList[i].setStyleSheet(
                    "background-color:" + color_string + "; margin-left:6px; color: white")

        page_index = self.plottingBoardReference.get_page_index()
        plotting_index = self.plottingBoardReference.get_plotting_index()
        loaded_csvfiles = self.analyserMediator.get_loaded_csv_files_from_context(page_index, plotting_index)
        loaded_csvfiles_validity = self.analyserMediator.get_loaded_csv_files_validity_from_context(page_index, plotting_index)
        plotting_context = self.analyserMediator.get_a_plotting_context(page_index, plotting_index)

        sub_list_siso_values = [[[] for y in range(len(self.sisoRangeCheckList))] for y in range(len(loaded_csvfiles))]
        sub_list_siso_indexs = [[[] for y in range(len(self.sisoRangeCheckList))] for y in range(len(loaded_csvfiles))]
        cpt = 0
        for filename in loaded_csvfiles:
            if not loaded_csvfiles_validity[loaded_csvfiles.index(filename)]:
                continue
            csvfile = self.analyserMediator.get_csv_file_in_context_by_name(filename)
            siso_values = plotting_context.get_siso_parameter_values(filename)
            row_count = csvfile.get_row_count()
            for i in range(len(self.sisoRangeCheckList)):
                if self.sisoRangeCheckList[i].isChecked():
                    if i == 0:
                        for j in range(row_count):
                            if siso_values[j] < self.sisoScaleList[i]:
                                sub_list_siso_values[cpt][i].append(siso_values[j])
                                sub_list_siso_indexs[cpt][i].append(j)

                    elif 0 < i < len(self.sisoRangeCheckList) - 1:  # TODO A Verifier
                        for j in range(row_count):
                            if self.sisoScaleList[i - 1] <= siso_values[j] < self.sisoScaleList[i]:
                                sub_list_siso_values[cpt][i].append(siso_values[j])
                                sub_list_siso_indexs[cpt][i].append(j)
                    else:
                        for j in range(row_count):
                            if self.sisoScaleList[i - 1] <= siso_values[j]:
                                sub_list_siso_values[cpt][i].append(siso_values[j])
                                sub_list_siso_indexs[cpt][i].append(j)
            plotting_context.set_sub_lists_of_siso_index(sub_list_siso_indexs[cpt], filename)
            plotting_context.set_sub_lists_of_siso(sub_list_siso_values[cpt], filename)
            cpt += 1

        del sub_list_siso_values[:]
        del sub_list_siso_indexs[:]

        self.plot.set_current_siso_curves_linear_gradient(start_color, finish_color)
        self.curve_gradient_using = True

    def siso_range_check_list_changed(self):

        page_index = self.plottingBoardReference.get_page_index()
        plotting_index = self.plottingBoardReference.get_plotting_index()
        loaded_csvfiles = self.analyserMediator.get_loaded_csv_files_from_context(page_index, plotting_index)
        loaded_csvfiles_validity = self.analyserMediator.get_loaded_csv_files_validity_from_context(page_index, plotting_index)
        plotting_context = self.analyserMediator.get_a_plotting_context(page_index, plotting_index)

        sub_list_siso_values = [[[] for y in range(len(self.sisoRangeCheckList))] for y in range(len(loaded_csvfiles))]
        sub_list_siso_indexs = [[[] for y in range(len(self.sisoRangeCheckList))] for y in range(len(loaded_csvfiles))]
        cpt = 0
        for filename in loaded_csvfiles:
            if not loaded_csvfiles_validity[loaded_csvfiles.index(filename)]:
                continue

            csvfile = self.analyserMediator.get_csv_file_in_context_by_name(filename)
            siso_values = plotting_context.get_siso_parameter_values(filename)
            row_count = csvfile.get_row_count()
            # print siso_values
            del self.siso_check_list[:]
            for i in range(len(self.sisoRangeCheckList)):
                if self.sisoRangeCheckList[i].isChecked():
                    self.siso_check_list.append(1)
                    if i == 0:
                        for j in range(row_count):
                            if siso_values[j] < self.sisoScaleList[i]:
                                sub_list_siso_values[cpt][i].append(siso_values[j])
                                sub_list_siso_indexs[cpt][i].append(j)

                    elif 0 < i < len(self.sisoRangeCheckList) - 1:
                        for j in range(row_count):
                            if self.sisoScaleList[i - 1] <= siso_values[j] < self.sisoScaleList[i]:
                                sub_list_siso_values[cpt][i].append(siso_values[j])
                                sub_list_siso_indexs[cpt][i].append(j)
                    else:
                        for j in range(row_count):
                            if self.sisoScaleList[i - 1] <= siso_values[j]:
                                sub_list_siso_values[cpt][i].append(siso_values[j])
                                sub_list_siso_indexs[cpt][i].append(j)
                else:
                    self.siso_check_list.append(0)
            plotting_context.set_sub_lists_of_siso_index(sub_list_siso_indexs[cpt], filename)
            plotting_context.set_sub_lists_of_siso(sub_list_siso_values[cpt], filename)
            cpt += 1

        # self.myCurveChartInformation.print_data_center()
        del sub_list_siso_values[:]
        del sub_list_siso_indexs[:]

        self.plot.cut_current_curves_by_siso(self.sisoDisplayMode)

        if self.lom_existed:

            loaded_lomfiles = self.analyserMediator.get_loaded_lom_files_from_context(page_index, plotting_index)
            loaded_lomfiles_validity = self.analyserMediator.get_loaded_lom_files_validity_from_context(page_index, plotting_index)

            # loaded_lomfiles = plotting_context.get_loaded_lomfiles()
            # loaded_lomfiles_validity = plotting_context.get_loaded_lomfiles_validity()

            for lom_file_name in loaded_lomfiles:
                if not loaded_lomfiles_validity[loaded_lomfiles.index(lom_file_name)]:
                    continue
                for label_name in plotting_context.get_label_list_from_lom_file(lom_file_name):
                    siso_validity = plotting_context.get_siso_parameter_validity_from_lom_file(label_name, lom_file_name)
                    del self.siso_check_list[:]
                    for i in range(len(self.sisoRangeCheckList)):
                        if self.sisoRangeCheckList[i].isChecked():
                            self.siso_check_list.append(1)
                            siso_validity[i] = 1
                        else:
                            self.siso_check_list.append(0)
                            siso_validity[i] = 0
            self.plot.replot_current_lom_curves()

        siso_check_list_string = ''
        for x in self.siso_check_list:
            siso_check_list_string += str(x) + ','
        siso_check_list_string = siso_check_list_string[:-1]

        self.analyserMediator.generate_an_action_into_global_context('set siso check information: (' + siso_check_list_string + ') for plotting board :'
                                                                         + str(self.plottingBoardReference.get_plotting_index()) + ' in page: '
                                                                         + str(self.plottingBoardReference.get_page_index()))

    def set_siso_parameter_name(self, siso_parameter):
        siso_values = []
        self.SISOParameter = siso_parameter

        page_index = self.plottingBoardReference.get_page_index()
        plotting_index = self.plottingBoardReference.get_plotting_index()
        loaded_csvfiles = self.analyserMediator.get_loaded_csv_files_from_context(page_index, plotting_index)
        loaded_csvfiles_validity = self.analyserMediator.get_loaded_csv_files_validity_from_context(page_index, plotting_index)
        plotting_context = self.analyserMediator.get_a_plotting_context(page_index, plotting_index)

        siso_values_list = [[] for y in range(len(loaded_csvfiles))]
        cut_tips = ""

        cpt = 0
        for filename in loaded_csvfiles:
            if not loaded_csvfiles_validity[loaded_csvfiles.index(filename)]:
                continue
            csvfile = self.analyserMediator.get_csv_file_in_context_by_name(filename)
            if siso_parameter in csvfile.get_title_list():
                siso_value_pointer = csvfile.get_title_list().index(self.SISOParameter)
                row_count = csvfile.get_row_count()
                values = csvfile.get_values()
                for i in range(row_count):
                    siso_values_list[cpt].append(float(values[i][siso_value_pointer]))

                siso_max = max(siso_values_list[cpt])
                siso_min = min(siso_values_list[cpt])
                temp = "[" + str(siso_min) + "," + str(siso_max) + "],"

                plotting_context.set_siso_parameter_name(siso_parameter, filename)
                plotting_context.set_siso_parameter_values(siso_values_list[cpt], filename)
                cut_tips += temp
            else:
                print 'the chosen parameter does not existed in the file', filename

            cpt += 1

            if self.siso_max < siso_max:
                self.siso_max = siso_max

            if self.siso_min > siso_min:
                self.siso_min = siso_min

        self.SISO_cmdline.setText(cut_tips)
        self.plottingBoardReference.set_function_title(None, "", "", self.SISOParameter)
        self.siso_existed = True

    def set_siso_parameter_range_information(self):
        siso_values = []

        page_index = self.plottingBoardReference.get_page_index()
        plotting_index = self.plottingBoardReference.get_plotting_index()
        loaded_csvfiles = self.analyserMediator.get_loaded_csv_files_from_context(page_index, plotting_index)
        loaded_csvfiles_validity = self.analyserMediator.get_loaded_csv_files_validity_from_context(page_index, plotting_index)

        siso_values_list = [[] for y in range(len(loaded_csvfiles))]
        cut_tips = ""

        cpt = 0
        for filename in loaded_csvfiles:
            if not loaded_csvfiles_validity[loaded_csvfiles.index(filename)]:
                continue
            csvfile = self.analyserMediator.get_csv_file_in_context_by_name(filename)

            siso_value_pointer = csvfile.get_title_list().index(self.SISOParameter)
            row_count = csvfile.get_row_count()
            values = csvfile.get_values()
            for i in range(row_count):
                siso_values_list[cpt].append(float(values[i][siso_value_pointer]))

            siso_max = max(siso_values_list[cpt])
            siso_min = min(siso_values_list[cpt])
            temp = "[" + str(siso_min) + "," + str(siso_max) + "],"

            cut_tips += temp

            cpt += 1

            if self.siso_max < siso_max:
                self.siso_max = siso_max

            if self.siso_min > siso_min:
                self.siso_min = siso_min

        self.SISO_cmdline.setText(cut_tips)

    def set_iso_parameter_name(self, iso_parameter):
        iso_values = []
        self.ISOParameter = iso_parameter

        page_index = self.plottingBoardReference.get_page_index()
        plotting_index = self.plottingBoardReference.get_plotting_index()
        loaded_csvfiles = self.analyserMediator.get_loaded_csv_files_from_context(page_index, plotting_index)
        loaded_csvfiles_validity = self.analyserMediator.get_loaded_csv_files_validity_from_context(page_index, plotting_index)
        plotting_context = self.analyserMediator.get_a_plotting_context(page_index, plotting_index)

        iso_values_list = [[] for y in range(len(loaded_csvfiles))]
        cut_tips = ""

        cpt = 0
        for filename in loaded_csvfiles:
            if not loaded_csvfiles_validity[loaded_csvfiles.index(filename)]:
                continue
            csvfile = self.analyserMediator.get_csv_file_in_context_by_name(filename)
            if iso_parameter in csvfile.get_title_list():
                iso_value_pointer = csvfile.get_title_list().index(self.ISOParameter)
                row_count = csvfile.get_row_count()
                values = csvfile.get_values()
                for i in range(row_count):
                    iso_values_list[cpt].append(float(values[i][iso_value_pointer]))

                iso_max = max(iso_values_list[cpt])
                iso_min = min(iso_values_list[cpt])
                temp = "[" + str(iso_min) + "," + str(iso_max) + "],"

                plotting_context.set_iso_parameter_name(iso_parameter, filename)
                plotting_context.set_iso_parameter_values(iso_values_list[cpt], filename)
                cut_tips += temp
            else:
                print 'the chosen parameter does not existed in the file', filename

            cpt += 1

            if self.iso_max < iso_max:
                self.iso_max = iso_max

            if self.iso_min > iso_min:
                self.iso_min = iso_min

        self.ISO_cmdline.setText(cut_tips)
        self.plottingBoardReference.set_function_title(None, "", self.ISOParameter, "")

    def set_iso_parameter_range_information(self):
        iso_values = []

        page_index = self.plottingBoardReference.get_page_index()
        plotting_index = self.plottingBoardReference.get_plotting_index()
        loaded_csvfiles = self.analyserMediator.get_loaded_csv_files_from_context(page_index, plotting_index)
        loaded_csvfiles_validity = self.analyserMediator.get_loaded_csv_files_validity_from_context(page_index, plotting_index)
        plotting_context = self.analyserMediator.get_a_plotting_context(page_index, plotting_index)

        iso_values_list = [[] for y in range(len(loaded_csvfiles))]
        cut_tips = ""

        cpt = 0
        for filename in loaded_csvfiles:
            if not loaded_csvfiles_validity[loaded_csvfiles.index(filename)]:
                continue

            csvfile = self.analyserMediator.get_csv_file_in_context_by_name(filename)
            iso_value_pointer = csvfile.get_title_list().index(self.ISOParameter)
            row_count = csvfile.get_row_count()
            values = csvfile.get_values()
            for i in range(row_count):
                iso_values_list[cpt].append(float(values[i][iso_value_pointer]))

            iso_max = max(iso_values_list[cpt])
            iso_min = min(iso_values_list[cpt])
            temp = "[" + str(iso_min) + "," + str(iso_max) + "],"

            cut_tips += temp

            cpt += 1

            if self.iso_max < iso_max:
                self.iso_max = iso_max

            if self.iso_min > iso_min:
                self.iso_min = iso_min

        self.ISO_cmdline.setText(cut_tips)
