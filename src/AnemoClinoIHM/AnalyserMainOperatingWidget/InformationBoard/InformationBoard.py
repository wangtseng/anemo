"""
Last updated on 07/01/2015

@author: Cheng WANG,
"""

from TitleListWidget import *


class InformationBoard(QWidget):
    """InformationBoard

        - This class represent the parameter and file information of the analyser

    Attributes:
        -

            *************************
            *                       *
            *                       *
            *  fileListTreeWidget   *
            *                       *
            *                       *
            *************************
            *  filterCmdLine        *
            *************************
            *                       *
            *                       *
            *  parameterListWidget  *
            *                       *
            *                       *
            *************************
    """

    def __init__(self, parent=None):
        super(InformationBoard, self).__init__(parent)

        # ------------------------------------------------------
        # initialize some useful attributes
        # ------------------------------------------------------
        tree_widget_style = "QTreeWidget{show-decoration-selected:2}" \
                            "QTreeWidget::item {border: 1px solid #d9d9d9;border-top-color: transparent;border-bottom-color: transparent;}" \
                            "QTreeWidget::item:hover {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e7effd, stop: 1 #cbdaf1),border: 1px solid #bfcde4;}" \
                            "QTreeWidget::item:selected {border: 1px solid #567dbc;}" \
                            "QTreeWidget::item:selected:active{background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6ea1f1, stop: 1 #567dbc)}" \
                            "QTreeWidget::item:selected:!active {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6b9be8, stop: 1 #577fbf)}"

        self.analyseurMediator = None
        self.defaultFolderIcon = QIcon(":/folder.png")
        self.fileUnloadedIcon = QIcon(":/fileunloaded.png")
        self.fileLoadedIcon = QIcon(":/fileloaded.png")
        self.defaultTitleIcon = QIcon(":/title.png")
        self.font = QFont("Helvetica", 8, QFont.AnyStyle, True)
        self.setFixedWidth(300)

        # -----------------------------------------------------------
        # private attributes initialization for file list tree widget
        # -----------------------------------------------------------
        self.pos = None
        self.index = -1
        self.fileTypeHandling = 'csv'
        self.csvFolderExisted = False
        self.lomFolderExisted = False
        self.newIndexOfLoadedCSVFile = 0
        self.newIndexOfLoadedLOMFile = 0
        self.folder_list = []
        self.loadedCSVFiles = []
        self.loadedLOMFiles = []
        self.titlesLoadedCSVFiles = []
        self.titlesLoadedLOMFiles = []
        self.loadedCSVFilesValidity = []
        self.loadedLOMFilesValidity = []
        self.fileItemToBeHandled = None  # the filename item on the file tree widget which has been right clicked
        self.csv_folder = None
        self.lom_folder = None

        information_board_layout = QVBoxLayout(self)
        file_list_group_box = QGroupBox()
        file_list_group_box.setStyleSheet("background-color:transparent;")
        file_list_group_box.setTitle("Files")
        file_list_group_box.setFont(self.font)
        file_list_group_box.setFixedHeight(200)
        file_list_group_box_layout = QVBoxLayout(file_list_group_box)
        self.fileListTreeWidget = QTreeWidget()
        self.fileListTreeWidget.setFont(self.font)
        self.fileListTreeWidget.setColumnCount(1)
        self.fileListTreeWidget.setHeaderHidden(1)
        self.fileListTreeWidget.setStyleSheet(tree_widget_style)
        self.fileListTreeWidget.verticalScrollBar().setStyleSheet("background-color: transparent")
        self.fileListTreeWidget.setFrameStyle(QFrame.NoFrame)
        self.fileListTreeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        file_list_group_box_layout.addWidget(self.fileListTreeWidget)
        file_list_group_box.setLayout(file_list_group_box_layout)

        # -----------------------------------------------------------
        # private attributes initialization for parameter filter area
        # -----------------------------------------------------------
        self.cmdline_string = ""
        self.filterCmdLine = QLineEdit()
        self.filterCmdLine.setStyleSheet("QLineEdit {border: 1px solid aliceBlue;border-radius: 0px;padding: 2 2px;background: transparent;selection-background-color: skyblue;}")
        font = QFont("Times", 9, QFont.AnyStyle, True)
        self.filterCmdLine.setFont(font)

        # -----------------------------------------------------------
        # private attributes initialization for parameter list widget
        # -----------------------------------------------------------
        self.title_list_in_loaded_csv_files = []
        self.title_list_in_loaded_lom_files = []
        file_group_box = QGroupBox()
        file_group_box.setStyleSheet("background-color: transparent")
        file_group_box_layout = QVBoxLayout(file_group_box)
        self.parameterListWidget = TitleListWidget()
        self.parameterListWidget.verticalScrollBar().setStyleSheet("background-color: transparent")
        self.parameterListWidget.setFrameStyle(QFrame.NoFrame)
        file_group_box_layout.addWidget(self.parameterListWidget)
        file_group_box.setLayout(file_group_box_layout)

        # -------------------------------------
        # add tree component to the main layout
        # -------------------------------------
        information_board_layout.addWidget(file_list_group_box)
        information_board_layout.addWidget(self.filterCmdLine)
        information_board_layout.addWidget(file_group_box)
        information_board_layout.setContentsMargins(4, 0, 0, 1)
        information_board_layout.setSpacing(2)
        information_board_layout.setAlignment(Qt.AlignBottom)

        # self.connect(self.fileListTreeWidget, SIGNAL("itemDoubleClicked(QTreeWidgetItem*,int)"),self.item_double_clicked_handle)
        self.connect(self.fileListTreeWidget, SIGNAL("customContextMenuRequested(QPoint)"), self.file_item_been_right_clicked)
        self.connect(self.fileListTreeWidget, SIGNAL("itemChanged(QTreeWidgetItem*,int)"), self.handle_item_checked)
        self.filterCmdLine.textChanged.connect(self.parameter_filter)

    def add_file_to_file_list_tree_widget(self, filename, file_type):
        """
            -- add a file into the file list tree widget according to its name and its type
        :param filename: something like: F1V3031_takeoff_R7ADC
        :param file_type: csv or gen
        """
        if file_type == "csv":
            if not self.csvFolderExisted:
                self.csv_folder = QTreeWidgetItem(self.fileListTreeWidget)
                self.csv_folder.setText(0, "csv folder")
                self.csv_folder.setIcon(0, self.defaultFolderIcon)
                self.csv_folder.setFlags(self.csv_folder.flags() | Qt.ItemIsUserCheckable)
                self.csv_folder.setCheckState(0, Qt.Unchecked)
                self.csvFolderExisted = True
                self.folder_list.append("csv folder")

            if not self.analyseurMediator.check_if_csv_file_created(filename):
                csv_file_item = QTreeWidgetItem(self.csv_folder)
                csv_file_item.setText(0, filename)
                csv_file_item.setIcon(0, self.fileUnloadedIcon)
                csv_file_item.setFlags(csv_file_item.flags() | Qt.ItemIsUserCheckable)
                csv_file_item.setCheckState(0, Qt.Unchecked)

        elif file_type == "gen":
            if not self.lomFolderExisted:
                self.lom_folder = QTreeWidgetItem(self.fileListTreeWidget)
                self.lom_folder.setText(0, "lom folder")
                self.lom_folder.setIcon(0, self.defaultFolderIcon)
                self.lom_folder.setFlags(self.lom_folder.flags() | Qt.ItemIsUserCheckable)
                self.lom_folder.setCheckState(0, Qt.Unchecked)
                self.lomFolderExisted = True
                self.folder_list.append("lom folder")

            if not self.analyseurMediator.check_if_lom_file_created(filename):
                lom_file_Item = QTreeWidgetItem(self.lom_folder)
                lom_file_Item.setText(0, filename)
                lom_file_Item.setIcon(0, self.fileUnloadedIcon)
                lom_file_Item.setFlags(lom_file_Item.flags() | Qt.ItemIsUserCheckable)
                lom_file_Item.setCheckState(0, Qt.Unchecked)

    def load_file_into_context(self):
        """Load the file into model(package AnemoClinoContext) to declare the files which need to be considered when plotting

        Firstly get the file name from the qtreewidgetitem which has been right clicked.
        Then, identify the type of the file.
        Finally, append the file name to the file list related
        """
        file_temp = str(self.fileItemToBeHandled.text(0))

        if file_temp.__contains__("csv"):
            if file_temp not in self.loadedCSVFiles:
                self.loadedCSVFiles.insert(self.newIndexOfLoadedCSVFile, file_temp)
                self.loadedCSVFilesValidity.insert(self.newIndexOfLoadedCSVFile, 0)
                self.analyseurMediator.set_loaded_csvfile_into_context(file_temp, self.newIndexOfLoadedCSVFile)
                self.analyseurMediator.set_loaded_csvfile_validity_into_context(0, self.newIndexOfLoadedCSVFile)
                self.newIndexOfLoadedCSVFile += 1
        if file_temp.__contains__("gen"):
            if file_temp not in self.loadedLOMFiles:
                self.loadedLOMFiles.insert(self.newIndexOfLoadedLOMFile, file_temp)
                self.loadedLOMFilesValidity.insert(self.newIndexOfLoadedLOMFile, 0)
                self.analyseurMediator.set_loaded_lomfile_into_context(file_temp, self.newIndexOfLoadedLOMFile)
                self.analyseurMediator.set_loaded_lom_files_validity_into_context(0, self.newIndexOfLoadedLOMFile)
                self.newIndexOfLoadedLOMFile += 1
        self.analyseurMediator.generate_an_action_into_global_context('load the file ' + file_temp + ' which has a parent at: ' + str(self.index))
        self.fileItemToBeHandled.setIcon(0, self.fileLoadedIcon)
        self.fileItemToBeHandled = None

    def load_file_into_context_while_import(self, index, filename):
        self.index = index
        top_level_item = self.fileListTreeWidget.topLevelItem(index)

        for i in range(top_level_item.childCount()):
            if top_level_item.child(i).text(0) == filename:
                self.fileItemToBeHandled = top_level_item.child(i)

        file_temp = str(self.fileItemToBeHandled.text(0))

        if file_temp.__contains__("csv"):
            if file_temp not in self.loadedCSVFiles:
                self.loadedCSVFiles.insert(self.newIndexOfLoadedCSVFile, file_temp)
                self.loadedCSVFilesValidity.insert(self.newIndexOfLoadedCSVFile, 0)
                self.analyseurMediator.set_loaded_csvfile_into_context(file_temp, self.newIndexOfLoadedCSVFile)
                self.analyseurMediator.set_loaded_csvfile_validity_into_context(0, self.newIndexOfLoadedCSVFile)
                self.newIndexOfLoadedCSVFile += 1
        if file_temp.__contains__("gen"):
            if file_temp not in self.loadedLOMFiles:
                self.loadedLOMFiles.insert(self.newIndexOfLoadedLOMFile, file_temp)
                self.loadedLOMFilesValidity.insert(self.newIndexOfLoadedLOMFile, 0)
                self.analyseurMediator.set_loaded_lomfile_into_context(file_temp, self.newIndexOfLoadedLOMFile)
                self.analyseurMediator.set_loaded_lom_files_validity_into_context(0, self.newIndexOfLoadedLOMFile)
                self.newIndexOfLoadedLOMFile += 1
        self.analyseurMediator.generate_an_action_into_global_context('load the file ' + file_temp + ' which has a parent at: ' + str(self.index))
        self.fileItemToBeHandled.setIcon(0, self.fileLoadedIcon)
        self.fileItemToBeHandled = None

    def unload_file_from_context(self):
        """Unload the file into model(package AnemoClinoContext) to declare the files which need to be considered when plotting

        Firstly get the file name from the qtreewidgetitem which has been right clicked.
        Then, identify the type of the file.
        Finally, delete the file name from the file list related
        """
        file_temp = str(self.fileItemToBeHandled.text(0))
        if file_temp.__contains__("csv"):
            if file_temp in self.loadedCSVFiles:
                pos = self.loadedCSVFiles.index(file_temp)
                del self.loadedCSVFiles[pos]
                del self.loadedCSVFilesValidity[pos]
                self.analyseurMediator.delete_loaded_csvfile_from_context(file_temp, pos)

        elif file_temp.__contains__("gen"):
            if file_temp in self.loadedLOMFiles:
                pos = self.loadedLOMFiles.index(file_temp)
                del self.loadedLOMFiles[pos]
                del self.loadedLOMFilesValidity[pos]
                self.analyseurMediator.delete_loaded_lomfile_from_context(file_temp, pos)
        self.analyseurMediator.generate_an_action_into_global_context('unload the file ' + file_temp + ' which has a parent at: ' + str(self.index))
        self.fileItemToBeHandled.setIcon(0, self.fileUnloadedIcon)
        self.fileItemToBeHandled = None

    def unload_file_from_context_while_import(self, index, filename):
        self.index = index
        top_level_item = self.fileListTreeWidget.topLevelItem(index)

        for i in range(top_level_item.childCount()):
            print top_level_item.child(i).text(0), filename

            if top_level_item.child(i).text(0) == filename:
                self.fileItemToBeHandled = top_level_item.child(i)
                print self.fileItemToBeHandled.text(0)

        file_temp = str(self.fileItemToBeHandled.text(0))
        if file_temp.__contains__("csv"):
            if file_temp in self.loadedCSVFiles:
                pos = self.loadedCSVFiles.index(file_temp)
                del self.loadedCSVFiles[pos]
                del self.loadedCSVFilesValidity[pos]
                self.analyseurMediator.delete_loaded_csvfile_from_context(file_temp, pos)

        elif file_temp.__contains__("gen"):
            if file_temp in self.loadedLOMFiles:
                pos = self.loadedLOMFiles.index(file_temp)
                del self.loadedLOMFiles[pos]
                del self.loadedLOMFilesValidity[pos]
                self.analyseurMediator.delete_loaded_lomfile_from_context(file_temp, pos)
        self.analyseurMediator.generate_an_action_into_global_context('unload the file ' + file_temp + ' which has a parent at: ' + str(self.index))
        self.fileItemToBeHandled.setIcon(0, self.fileUnloadedIcon)
        self.fileItemToBeHandled = None

    def delete_file_from_context(self):
        """Delete the file from model(package AnemoClinoContext) to declare the new file list which need to be considered when plotting

        Firstly get the file name from the qtreewidgetitem which has been right clicked.
        Then, identify the type of the file.
        Finally, delete the file name from the file list related and also the qtreewidgetitem right clicked
        """
        parent = self.fileItemToBeHandled.parent()
        filename = str(self.fileItemToBeHandled.text(0))
        parent.removeChild(self.fileItemToBeHandled)
        if filename.__contains__("csv"):
            if filename in self.loadedCSVFiles:
                pos = self.loadedCSVFiles.index(filename)
                del self.loadedCSVFiles[pos]
                del self.loadedCSVFilesValidity[pos]
                self.analyseurMediator.delete_loaded_csvfile_from_context(filename, pos)

        elif filename.__contains__("gen"):
            if filename in self.loadedLOMFiles:
                pos = self.loadedLOMFiles.index(filename)
                del self.loadedLOMFiles[pos]
                del self.loadedLOMFilesValidity[pos]
                self.analyseurMediator.delete_loaded_lomfile_from_context(filename, pos)
        self.analyseurMediator.generate_an_action_into_global_context('delete the file ' + filename + ' which has a parent at: ' + str(self.index))
        self.parent().parent().get_toolbar_reference().delete_the_file_path(filename)
        self.fileItemToBeHandled = None

    def delete_file_from_context_while_import(self, index, filename):
        self.index = index
        top_level_item = self.fileListTreeWidget.topLevelItem(index)

        for i in range(top_level_item.childCount()):
            print top_level_item.child(i).text(0), filename

            if top_level_item.child(i).text(0) == filename:
                self.fileItemToBeHandled = top_level_item.child(i)
                print self.fileItemToBeHandled.text(0)

        filename = str(self.fileItemToBeHandled.text(0))
        parent = self.fileItemToBeHandled.parent()

        parent.removeChild(self.fileItemToBeHandled)
        if filename.__contains__("csv"):
            if filename in self.loadedCSVFiles:
                pos = self.loadedCSVFiles.index(filename)
                del self.loadedCSVFiles[pos]
                del self.loadedCSVFilesValidity[pos]
                self.analyseurMediator.delete_loaded_csvfile_from_context(filename, pos)

        elif filename.__contains__("gen"):
            if filename in self.loadedLOMFiles:
                pos = self.loadedLOMFiles.index(filename)
                del self.loadedLOMFiles[pos]
                del self.loadedLOMFilesValidity[pos]
                self.analyseurMediator.delete_loaded_lomfile_from_context(filename, pos)
        self.analyseurMediator.generate_an_action_into_global_context('delete the file ' + filename + ' which has a parent at: ' + str(self.index))
        self.parent().parent().get_toolbar_reference().delete_the_file_path(filename)
        self.fileItemToBeHandled = None

    def file_item_been_right_clicked(self, pos):
        """
            -- once an item in the qtreewidgetitem been right clicked, an action window(include load,unload,delete) will display to let the user manipulate the item
        :param pos: the current mouse position to position the actions window
        """
        if self.fileListTreeWidget.itemAt(pos) is None:
            return

        self.index = self.fileListTreeWidget.indexOfTopLevelItem(self.fileListTreeWidget.itemAt(pos).parent())

        title = str(self.fileListTreeWidget.itemAt(pos).text(0))
        if not title.__contains__("folder"):
            self.fileItemToBeHandled = self.fileListTreeWidget.itemAt(pos)
            menu = QMenu(self.fileListTreeWidget)
            menu.setStyleSheet('QMenu {background-color: #ABABAB; border: 1px solid black;}'
                               'QMenu::item {background-color: transparent;}'
                               'QMenu::item:selected {background-color: #654321;}')
            load_file_into_context_button = menu.addAction("load")
            unload_file_from_context_button = menu.addAction("unload")
            delete_file_from_context_button = menu.addAction("delete")
            self.connect(load_file_into_context_button, SIGNAL("triggered()"), self.load_file_into_context)
            self.connect(unload_file_from_context_button, SIGNAL("triggered()"), self.unload_file_from_context)
            self.connect(delete_file_from_context_button, SIGNAL("triggered()"), self.delete_file_from_context)
            menu.exec_(QCursor.pos())

    def parameter_filter(self, cmdline_string):
        """
            -- parameter name filter area which react a search action each time user input a letter in the filterCmdLine
                -firstly, analyse the string in the edit line
                -then if the string start with the character '*', it mean search and generate a new list of parameter, in which, each parameter's name include the rest of the string in edit line
                 else: just generate a new list of parameter's name, in which, each parameter's name include the string in the edit line
                -finally, update the parameterListWidget with the new list of parameter generated

        :param cmdline_string:
        """
        list_temp = []
        self.cmdline_string = str(cmdline_string)

        if self.cmdline_string.startswith('*'):
            self.cmdline_string = self.cmdline_string.translate(None, '*')
            for title in self.title_list_in_loaded_csv_files:
                if self.cmdline_string in title:
                    list_temp.append(title)

            for title in self.title_list_in_loaded_lom_files:
                if self.cmdline_string in title:
                    list_temp.append(title)
        else:
            for title in self.title_list_in_loaded_csv_files:
                if title.startswith(self.cmdline_string):
                    list_temp.append(title)

            for title in self.title_list_in_loaded_lom_files:
                if title.startswith(self.cmdline_string):
                    list_temp.append(title)

        self.parameterListWidget.clear()

        for i in list_temp:
            title_item = QListWidgetItem(i)
            title_item.setIcon(self.defaultTitleIcon)
            title_item.setFont(self.font)
            self.parameterListWidget.addItem(title_item)

    def update_title_list_widget(self):
        self.parameterListWidget.clear()
        if self.fileTypeHandling == 'csv':
            for i in range(len(self.title_list_in_loaded_csv_files)):
                title_item = QListWidgetItem(self.title_list_in_loaded_csv_files[i])
                title_item.setIcon(self.defaultTitleIcon)
                title_item.setFont(self.font)
                self.parameterListWidget.addItem(title_item)
        elif self.fileTypeHandling == 'lom':
            for i in range(len(self.title_list_in_loaded_lom_files)):
                title_item = QListWidgetItem(self.title_list_in_loaded_lom_files[i])
                title_item.setIcon(self.defaultTitleIcon)
                title_item.setFont(self.font)
                self.parameterListWidget.addItem(title_item)

    def load_titles_of_the_file_into_widget(self, filename):
        self.parameterListWidget.clear()
        if str(filename).__contains__("csv"):
            csv_file = self.analyseurMediator.get_csv_file_in_context_by_name(filename)
            if None != csv_file:
                title_list = csv_file.get_title_list()
                for i in title_list:
                    if i not in self.title_list_in_loaded_csv_files:
                        self.title_list_in_loaded_csv_files.append(i)

                if filename not in self.titlesLoadedCSVFiles:
                    self.titlesLoadedCSVFiles.append(filename)

                for i in range(len(self.title_list_in_loaded_csv_files)):
                    title_item = QListWidgetItem(self.title_list_in_loaded_csv_files[i])
                    title_item.setIcon(self.defaultTitleIcon)
                    title_item.setFont(self.font)
                    self.parameterListWidget.addItem(title_item)
                self.fileTypeHandling = 'csv'
                self.analyseurMediator.set_file_type_handling_into_context(self.fileTypeHandling)
                self.analyseurMediator.generate_an_action_into_global_context('file type handling: ' + self.fileTypeHandling)
                return True

        elif str(filename).__contains__("gen"):
            lom_file = self.analyseurMediator.get_lom_file_in_context_by_name(filename)
            if None != lom_file:
                title_list = lom_file.get_label_list()
                for i in title_list:
                    if i not in self.title_list_in_loaded_lom_files:
                        self.title_list_in_loaded_lom_files.append(i)

                if filename not in self.titlesLoadedLOMFiles:
                    self.titlesLoadedLOMFiles.append(filename)

                for i in range(len(self.title_list_in_loaded_lom_files)):
                    title_item = QListWidgetItem(self.title_list_in_loaded_lom_files[i])
                    title_item.setIcon(self.defaultTitleIcon)
                    title_item.setFont(self.font)
                    self.parameterListWidget.addItem(title_item)
                self.fileTypeHandling = 'lom'
                self.analyseurMediator.set_file_type_handling_into_context(self.fileTypeHandling)
                self.analyseurMediator.generate_an_action_into_global_context('file type handling: ' + self.fileTypeHandling)

                return True

        return False

    def handle_item_checked(self, item, i):
        """ handle all the click event on check boxes of the fileListTreeWidget
        case:

        :param item:
        :param i:
        """

        # if the item("csv folder") has been chosen, we need to set all its children as checked. else, unchecked
        if item.text(0) == "csv folder":

            # set all the lom item to unchecked
            if self.lom_folder is not None:
                for j in range(self.lom_folder.childCount()):
                    self.lom_folder.child(j).setCheckState(0, Qt.Unchecked)

            # if we set item("csv folder") as unchecked, then set all its children items unchecked
            if item.checkState(i) == 0:
                for j in range(item.childCount()):
                    item.child(j).setCheckState(0, Qt.Unchecked)
                self.parameterListWidget.clear()  # clean the titles on the titleListWidget
                del self.titlesLoadedCSVFiles[:]  # reset the list of the parameter names to zero

            # if we set item("csv folder") as checked, then set all its children items checked
            elif item.checkState(i) == 2:
                self.parameterListWidget.clear()
                for j in range(item.childCount()):
                    item.child(j).setCheckState(0, Qt.Checked)
                    self.load_titles_of_the_file_into_widget(item.child(j).text(0))

            self.filterCmdLine.clear()

        # if the item("lom folder") has been chosen, we need to set all its children as checked. else, unchecked
        elif item.text(0) == "lom folder":

            # set all the csv item to unchecked
            if self.csv_folder is not None:
                for j in range(self.csv_folder.childCount()):
                    self.csv_folder.child(j).setCheckState(0, Qt.Unchecked)

            if item.checkState(i) == 0:
                for j in range(item.childCount()):
                    item.child(j).setCheckState(0, Qt.Unchecked)
                self.parameterListWidget.clear()
                del self.titlesLoadedLOMFiles[:]

            elif item.checkState(i) == 2:
                self.parameterListWidget.clear()
                for j in range(item.childCount()):
                    item.child(j).setCheckState(0, Qt.Checked)
                    self.load_titles_of_the_file_into_widget(item.child(j).text(0))
            self.filterCmdLine.clear()

        # if an csv file item has been checked
        elif item.parent().text(0) == "csv folder":

            # set all the lom item to unchecked
            if self.lom_folder is not None:
                for j in range(self.lom_folder.childCount()):
                    self.lom_folder.child(j).setCheckState(0, Qt.Unchecked)

            if item.checkState(i) == 2:
                if item.text(0) not in self.titlesLoadedCSVFiles:
                    if self.load_titles_of_the_file_into_widget(item.text(0)):
                        if len(self.titlesLoadedCSVFiles) == item.parent().childCount():
                            item.parent().setCheckState(0, Qt.Checked)

                if item.text(0) in self.loadedCSVFiles:
                    x = self.loadedCSVFiles.index(item.text(0))

            elif item.checkState(i) == 0:
                if item.text(0) in self.titlesLoadedCSVFiles:
                    self.parameterListWidget.clear()
                    self.titlesLoadedCSVFiles.remove(item.text(0))
                    del self.title_list_in_loaded_csv_files[:]

                    for filename in self.titlesLoadedCSVFiles:
                        self.load_titles_of_the_file_into_widget(filename)

                    if len(self.titlesLoadedCSVFiles) == 0:
                        item.parent().setCheckState(0, Qt.Unchecked)

                    if item.text(0) in self.loadedCSVFiles:
                        x = self.loadedCSVFiles.index(item.text(0))

            self.filterCmdLine.clear()

        elif item.parent().text(0) == "lom folder":
            if self.csv_folder is not None:
                for j in range(self.csv_folder.childCount()):
                    self.csv_folder.child(j).setCheckState(0, Qt.Unchecked)

            if item.checkState(i) == 2:
                if item.text(0) not in self.titlesLoadedLOMFiles:
                    if self.load_titles_of_the_file_into_widget(item.text(0)):
                        if len(self.titlesLoadedLOMFiles) == item.parent().childCount():
                            item.parent().setCheckState(0, Qt.Checked)

            elif item.checkState(i) == 0:
                if item.text(0) in self.titlesLoadedLOMFiles:
                    self.parameterListWidget.clear()
                    self.titlesLoadedLOMFiles.remove(item.text(0))
                    del self.title_list_in_loaded_lom_files[:]

                    for filename in self.titlesLoadedLOMFiles:
                        self.load_titles_of_the_file_into_widget(filename)

                    if len(self.titlesLoadedLOMFiles) == 0:
                        item.parent().setCheckState(0, Qt.Unchecked)

            self.filterCmdLine.clear()

    def get_file_list(self):
        return self.fileListTreeWidget

    def set_analyseur_mediator(self, analyseur_mediator):
        self.analyseurMediator = analyseur_mediator