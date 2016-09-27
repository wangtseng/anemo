"""
Last updated on 22/12/2014

@author: Cheng WANG
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import mmap


class MenuBarOfAnalyseur(QMenuBar):
    def __init__(self, parent=None):
        super(MenuBarOfAnalyseur, self).__init__(parent)
        self.parent = parent
        self.analyserMediator = None
        self.actions = list()

        self.setStyleSheet('QMenuBar {background-color: transparent;}'
                           'QMenuBar::item {spacing: 3px; padding: 4px 4px;background: transparent;border-radius: 4px;color:aliceBlue}'
                           'QMenuBar::item:selected {background: #a8a8a8;}'
                           'QMenuBar::item:pressed {background: #888888;}')

        self.defaultFolderIcon = QIcon("images/folder.png")
        self.defaultFileIcon = QIcon("images/csvfile.png")

        file_open_action = self.create_action("&Open...", self.add_file, QKeySequence.Open, "fileopen", "Open an existing file")
        environment_save_action = self.create_action("&Save...", self.environment_save, QKeySequence.Save, "environmentsave", "Save the environment")
        import_environment_action = self.create_action("&Import...", self.import_environment, QKeySequence("Ctrl+l"), "upload_files", "load the environment")
        pages_print_action = self.create_action("&Print...", self.pages_print, QKeySequence.Print, "pagesprint", "Print the pages")
        pages_capture_action = self.create_action("&Capture...", self.capture, QKeySequence.Cut, "close", "cut the pages")
        help_menu_action = self.create_action("&Help...", self.help_doc_display, QKeySequence.HelpContents, "addPageButton", "Open an existing file")
        help_topic_find_action = self.create_action("&Find...", self.help_doc_topic_find, QKeySequence.Find, "find_topic", "Open an existing file")

        self.fileMenu = self.addMenu("&File")
        self.fileMenuActions = (file_open_action, environment_save_action, import_environment_action)
        self.addActions(self.fileMenu, self.fileMenuActions)

        self.imagingMenu = self.addMenu("&Imaging")
        self.imagingMenuActions = (pages_print_action, pages_capture_action)
        self.addActions(self.imagingMenu, self.imagingMenuActions)

        self.viewMenu = self.addMenu("&View")

        self.helpMenu = self.addMenu("&Help")
        self.helpMenuActions = (help_menu_action, help_topic_find_action)
        self.addActions(self.helpMenu, self.helpMenuActions)

    def set_analyseur_mediator(self, analyseur_mediator):
        self.analyserMediator = analyseur_mediator

    def capture(self):
        print 'lalal'

    def help_doc_topic_find(self):
        print 'help_doc_topic_find'

    def help_doc_display(self):
        print 'help_doc'

    def import_environment(self):
        filepath = QFileDialog.getOpenFileName(self, "Import global context dialog", "/")
        self.import_environment_from_path(filepath)
        self.parse_actions_existed()

    def parse_actions_existed(self):
        for action in self.actions:
            self.action_analyse(action)

    def action_analyse(self, action_string):

        if action_string.__contains__('add a page'):
            self.parent.get_parent_widget().get_toolbar_reference().add_page_button_clicked()

        elif action_string.__contains__('delete the page'):
            temp = action_string.split('page')
            index = int(temp[1].translate(None, ' '))
            self.parent.get_parent_widget().get_main_operating_widget_reference().get_plotting_workspace().delete_page(index)

        elif action_string.__contains__('add a plotting board'):
            temp = action_string.split('page')
            index = int(temp[1].translate(None, ' '))
            page = self.parent.get_parent_widget().get_main_operating_widget_reference().get_plotting_workspace().get_the_page_at(index)
            page.add_a_plotting_board()

        elif action_string.__contains__('import file'):
            temp = action_string.split('from')
            path = temp[1].translate(None, ' ')
            self.parent.get_parent_widget().get_toolbar_reference().add_file_from_path(path)

        elif action_string.__contains__('file type handling'):
            temp = action_string.split(':')
            filetype = temp[1].translate(None, ' ')
            self.analyserMediator.set_file_type_handling_into_context(filetype)
            self.analyserMediator.generate_an_action_into_global_context('file type handling: ' + filetype)

        elif action_string.__contains__('load the file'):
            temp = action_string.split('at:')

            index_string = temp[1].translate(None, ' ')
            index = int(index_string)

            temp_1 = temp[0].split('file')
            temp_2 = temp_1[1].split('which has a parent')
            filename = temp_2[0].translate(None, ' ')
            self.parent.get_parent_widget().get_main_operating_widget_reference().get_information_board().load_file_into_context_while_import(index, filename)

        elif action_string.__contains__('unload the file'):
            temp = action_string.split('at:')

            index_string = temp[1].translate(None, ' ')
            index = int(index_string)

            temp_1 = temp[0].split('file')
            temp_2 = temp_1[1].split('which has a parent')
            filename = temp_2[0].translate(None, ' ')
            self.parent.get_parent_widget().get_main_operating_widget_reference().get_information_board().unload_file_into_context_while_import(index, filename)

        elif action_string.__contains__('delete the file'):
            temp = action_string.split('at:')

            index_string = temp[1].translate(None, ' ')
            index = int(index_string)

            temp_1 = temp[0].split('file')
            temp_2 = temp_1[1].split('which has a parent')
            filename = temp_2[0].translate(None, ' ')
            self.parent.get_parent_widget().get_main_operating_widget_reference().get_information_board().delete_file_into_context_while_import(index, filename)

        elif action_string.__contains__('drop parameter'):
            temp_1 = action_string.split('drop parameter:')
            temp_2 = temp_1[1].split('as')

            parameter_name = temp_2[0].translate(None, ' ')

            temp_3 = temp_2[1].split('for')
            axis = temp_3[0].translate(None, ' ')

            temp_4 = temp_3[1].split('in page:')
            page_index = int(temp_4[1].translate(None, ' '))
            temp_5 = temp_4[0].translate(None, ' ')
            plotting_board_index = int(temp_5[-1])

            page = self.parent.get_parent_widget().get_main_operating_widget_reference().get_plotting_workspace().get_the_page_at(page_index)
            plotting_board = page.get_plotting_board_at(plotting_board_index)
            plotting = plotting_board.get_plot_object()
            plotting.drop_event_while_import(parameter_name, axis, None)

        elif action_string.__contains__('as iso'):
            temp_1 = action_string.split('as iso for')

            temp_2 = temp_1[1].split('in page:')
            page_index = int(temp_2[1].translate(None, ' '))
            temp_3 = temp_2[0].translate(None, ' ')
            plotting_board_index = int(temp_3[-1])

            temp_4 = temp_1[0].split('set')
            parameter_name = temp_4[1].translate(None, ' ')

            page = self.parent.get_parent_widget().get_main_operating_widget_reference().get_plotting_workspace().get_the_page_at(page_index)
            plotting_board = page.get_plotting_board_at(plotting_board_index)
            plot_parameter_manipulation = plotting_board.get_plot_parameter_manipulation_object()
            iso_label = plot_parameter_manipulation.get_iso_label()
            iso_label.drop_event_while_import(parameter_name)

        elif action_string.__contains__('as siso'):
            temp_1 = action_string.split('as siso for')

            temp_2 = temp_1[1].split('in page:')
            page_index = int(temp_2[1].translate(None, ' '))
            temp_3 = temp_2[0].translate(None, ' ')
            plotting_board_index = int(temp_3[-1])

            temp_4 = temp_1[0].split('set')
            parameter_name = temp_4[1].translate(None, ' ')

            page = self.parent.get_parent_widget().get_main_operating_widget_reference().get_plotting_workspace().get_the_page_at(page_index)
            plotting_board = page.get_plotting_board_at(plotting_board_index)
            plot_parameter_manipulation = plotting_board.get_plot_parameter_manipulation_object()
            siso_label = plot_parameter_manipulation.get_siso_label()
            siso_label.drop_event_while_import(parameter_name)

        elif action_string.__contains__('set iso cut information:'):
            temp_1 = action_string.split(') for')

            temp_2 = temp_1[1].split('in page:')

            page_index = int(temp_2[1].translate(None, ' '))
            temp_3 = temp_2[0].translate(None, ' ')
            plotting_board_index = int(temp_3[-1])

            temp_4 = temp_1[0].split('(')
            iso_cut_information = temp_4[1].translate(None, ' ')

            page = self.parent.get_parent_widget().get_main_operating_widget_reference().get_plotting_workspace().get_the_page_at(page_index)
            plotting_board = page.get_plotting_board_at(plotting_board_index)
            plot_parameter_manipulation = plotting_board.get_plot_parameter_manipulation_object()
            plot_parameter_manipulation.iso_commandline_return_pressed_while_import(iso_cut_information)

        elif action_string.__contains__('set siso cut information:'):
            temp_1 = action_string.split(') for')

            temp_2 = temp_1[1].split('in page:')

            page_index = int(temp_2[1].translate(None, ' '))
            temp_3 = temp_2[0].translate(None, ' ')
            plotting_board_index = int(temp_3[-1])

            temp_4 = temp_1[0].split('(')
            siso_cut_information = temp_4[1].translate(None, ' ')

            page = self.parent.get_parent_widget().get_main_operating_widget_reference().get_plotting_workspace().get_the_page_at(page_index)
            plotting_board = page.get_plotting_board_at(plotting_board_index)
            plot_parameter_manipulation = plotting_board.get_plot_parameter_manipulation_object()
            plot_parameter_manipulation.siso_commandline_return_pressed_while_import(siso_cut_information)

        elif action_string.__contains__('set siso') and action_string.__contains__('represent by'):
            temp_1 = action_string.split('siso')
            temp_2 = temp_1[1].split('represent by')
            represent_mode = temp_2[1].translate(None, ' ')

            temp_3 = temp_2[0].split('in page:')
            page_index = int(temp_3[1].translate(None, ' '))
            temp_4 = temp_3[0].translate(None, ' ')
            plotting_board_index = int(temp_4[-1])

            page = self.parent.get_parent_widget().get_main_operating_widget_reference().get_plotting_workspace().get_the_page_at(page_index)
            plotting_board = page.get_plotting_board_at(plotting_board_index)
            plot_parameter_manipulation = plotting_board.get_plot_parameter_manipulation_object()
            siso_label = plot_parameter_manipulation.get_siso_label()
            siso_label.set_siso_represent_by(represent_mode)

        elif action_string.__contains__('set iso check information:'):

            temp_1 = action_string.split(') for')

            temp_2 = temp_1[1].split('in page:')

            page_index = int(temp_2[1].translate(None, ' '))
            temp_3 = temp_2[0].translate(None, ' ')
            plotting_board_index = int(temp_3[-1])

            temp_4 = temp_1[0].split('(')
            temp_5 = temp_4[1]
            temp_5 = temp_5.translate(None, ' ')

            check_states = temp_5.split(',')
            page = self.parent.get_parent_widget().get_main_operating_widget_reference().get_plotting_workspace().get_the_page_at(page_index)
            plotting_board = page.get_plotting_board_at(plotting_board_index)
            plot_parameter_manipulation = plotting_board.get_plot_parameter_manipulation_object()
            plot_parameter_manipulation.iso_check_setting(check_states)

        elif action_string.__contains__('set siso check information:'):
            temp_1 = action_string.split(') for')

            temp_2 = temp_1[1].split('in page:')
            page_index = int(temp_2[1].translate(None, ' '))
            temp_3 = temp_2[0].translate(None, ' ')
            plotting_board_index = int(temp_3[-1])

            temp_4 = temp_1[0].split('(')
            temp_5 = temp_4[1]
            temp_5 = temp_5.translate(None, ' ')

            check_states = temp_5.split(',')
            page = self.parent.get_parent_widget().get_main_operating_widget_reference().get_plotting_workspace().get_the_page_at(page_index)
            plotting_board = page.get_plotting_board_at(plotting_board_index)
            plot_parameter_manipulation = plotting_board.get_plot_parameter_manipulation_object()
            plot_parameter_manipulation.siso_check_setting(check_states)

        elif action_string.__contains__('drop label'):
            temp_1 = action_string.split('for')

            temp_2 = temp_1[1].split('in page:')
            page_index = int(temp_2[1].translate(None, ' '))
            temp_3 = temp_2[0].translate(None, ' ')
            plotting_board_index = int(temp_3[-1])

            if str(temp_1[0]).__contains__('first'):
                temp_4 = temp_1[0].split('the')
                temp_5 = temp_4[0].split('label:')
                label_name = temp_5[1].translate(None, ' ')

                page = self.parent.get_parent_widget().get_main_operating_widget_reference().get_plotting_workspace().get_the_page_at(page_index)
                plotting_board = page.get_plotting_board_at(plotting_board_index)
                plotting = plotting_board.get_plot_object()
                plotting.drop_event_while_import(label_name, None, 'first')

            elif str(temp_1[0]).__contains__('superpose'):
                temp_4 = temp_1[0].split('to')
                temp_5 = temp_4[0].split(':')
                label_name = temp_5[1].translate(None, ' ')

                page = self.parent.get_parent_widget().get_main_operating_widget_reference().get_plotting_workspace().get_the_page_at(page_index)
                plotting_board = page.get_plotting_board_at(plotting_board_index)
                plotting = plotting_board.get_plot_object()
                plotting.drop_event_while_import(label_name, None, 'superpose')

            elif str(temp_1[0]).__contains__('replace'):
                temp_4 = temp_1[0].split('to')
                temp_5 = temp_4[0].split(':')
                label_name = temp_5[1].translate(None, ' ')

                page = self.parent.get_parent_widget().get_main_operating_widget_reference().get_plotting_workspace().get_the_page_at(page_index)
                plotting_board = page.get_plotting_board_at(plotting_board_index)
                plotting = plotting_board.get_plot_object()
                plotting.drop_event_while_import(label_name, None, 'replace')

        elif action_string.__contains__('remove the label'):
            temp_1 = action_string.split('for')

            temp_2 = temp_1[1].split('in page:')
            page_index = int(temp_2[1].translate(None, ' '))
            temp_3 = temp_2[0].translate(None, ' ')
            plotting_board_index = int(temp_3[-1])

            temp_4 = temp_1[0].split('at position')
            item_index = int(temp_4[1].translate(None, ' '))
            temp_5 = temp_4[0].split('in file:')
            filename = temp_5[1].translate(None, ' ')
            temp_6 = temp_5[0].split('label:')
            label_name = temp_6[1].translate(None, ' ')

            page = self.parent.get_parent_widget().get_main_operating_widget_reference().get_plotting_workspace().get_the_page_at(page_index)
            plotting_board = page.get_plotting_board_at(plotting_board_index)
            plot_parameter_manipulation = plotting_board.get_plot_parameter_manipulation_object()
            plot_parameter_manipulation.delete_the_label_while_import(filename, label_name, item_index)

        elif action_string.__contains__('remove the ordinate'):
            temp_1 = action_string.split('for')

            temp_2 = temp_1[1].split('in page:')
            page_index = int(temp_2[1].translate(None, ' '))
            temp_3 = temp_2[0].translate(None, ' ')
            plotting_board_index = int(temp_3[-1])

            temp_4 = temp_1[0].split(' at position')
            item_index = int(temp_4[1].translate(None, ' '))
            temp_5 = temp_4[0].split('in file:')
            filename = temp_5[1].translate(None, ' ')
            temp_6 = temp_5[0].split('ordinate:')
            label_name = temp_6[1].translate(None, ' ')

            page = self.parent.get_parent_widget().get_main_operating_widget_reference().get_plotting_workspace().get_the_page_at(page_index)
            plotting_board = page.get_plotting_board_at(plotting_board_index)
            plot_parameter_manipulation = plotting_board.get_plot_parameter_manipulation_object()
            plot_parameter_manipulation.delete_ordinate_while_import(filename, label_name, item_index)

        #  set an extra parameter: OUT_ALPHA_B0_PR1) for plotting board :0 in page: 0
        elif action_string.__contains__('set an extra parameter'):
            temp_1 = action_string.split('for')

            temp_2 = temp_1[1].split('in page:')
            page_index = int(temp_2[1].translate(None, ' '))
            temp_3 = temp_2[0].translate(None, ' ')
            plotting_board_index = int(temp_3[-1])

            temp_4 = temp_1[0].split('parameter:')
            parameter_name = temp_4[1].translate(None, ' ')

            page = self.parent.get_parent_widget().get_main_operating_widget_reference().get_plotting_workspace().get_the_page_at(page_index)
            plotting_board = page.get_plotting_board_at(plotting_board_index)
            extra_parameter_widget = plotting_board.get_plotting_option_reference().get_extra_parameter_widget_reference()
            extra_parameter_widget.drop_event_while_import(parameter_name)

        elif action_string.__contains__('confirm the configuration'):
            temp_1 = action_string.split('for')

            temp_2 = temp_1[1].split('in page:')
            page_index = int(temp_2[1].translate(None, ' '))
            temp_3 = temp_2[0].translate(None, ' ')
            plotting_board_index = int(temp_3[-1])

            page = self.parent.get_parent_widget().get_main_operating_widget_reference().get_plotting_workspace().get_the_page_at(page_index)
            plotting_board = page.get_plotting_board_at(plotting_board_index)
            plotting_option_widget = plotting_board.get_plotting_option_reference()
            plotting_option_widget.confirmed()

        elif action_string.__contains__('cancel the configuration'):
            temp_1 = action_string.split('for')

            temp_2 = temp_1[1].split('in page:')
            page_index = int(temp_2[1].translate(None, ' '))
            temp_3 = temp_2[0].translate(None, ' ')
            plotting_board_index = int(temp_3[-1])

            page = self.parent.get_parent_widget().get_main_operating_widget_reference().get_plotting_workspace().get_the_page_at(page_index)
            plotting_board = page.get_plotting_board_at(plotting_board_index)
            plotting_option_widget = plotting_board.get_plotting_option_reference()
            plotting_option_widget.cancelled()

    def import_environment_from_path(self, filepath):
        with open(filepath, "r+b") as f:
            map_input = mmap.mmap(f.fileno(), 0)
            # read content via standard file methods
            cpt = 0
            for s in iter(map_input.readline, ""):
                s = s.translate(None, "\r\n")
                self.actions.append(str(s))
                cpt += 1
            map_input.close()

    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def create_action(self, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action

    def environment_save(self):
        self.analyserMediator.save_actions_in_global_context()

    def pages_print(self):
        self.parent.grab_fullscreen()

    def add_file(self):
        self.parent.get_parent_widget().get_toolbar_reference().file_open_button_clicked()
