"""
Last updated on 15/12/2014

@author: Cheng WANG
"""
import threading
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from LittleAirbusLabel import LittleAirbusLabel
from AnemoClinoIHM.AnalyserUsefulClasses.ObjectEventService import ObjectEventService
#import pygame
import cv2.cv as cv
import time

class ToolBarOfAnalyseur(QWidget):
    """ToolBarOfAnalyseur

    This class represent the tool bar of the main window of the anemo clino analyser, which include a number of push button below

    Attributes:
        - principal component of the title bar
            -------------------------------------------------------------------------------------------------------------------------------------------------------------
            | pickInformationBoardButton | importFileButton |                     | addPageButton | ...                                             | organizationLabel |
            -------------------------------------------------------------------------------------------------------------------------------------------------------------
    """

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.setFixedHeight(40)

        # -------------------------------------------------------------------------------
        # Attributes initialization
        # -------------------------------------------------------------------------------
        self.filepathList = []
        self.analyserMediator = None
        self.pickInformationBoardButtonClicked = False
        self.organizationLabel = LittleAirbusLabel(self)
        self.myButtonList = []
        self.myButtonString = ["fileList", "fileopen", "addPageButton", "analyser_configuration", "analyser_save", "screen_grab"]
        self.buttonSize = QSize(40, 40)
        self.screenGrabActivated = False
        self.Coordinate = [1, 1, 1, 1]

        self.videoDisplayWidget = QWidget()
        self.videoDisplayWidget.setFixedSize(400,300)

        # -------------------------------------------------------------------------------
        # Push buttons on the tool bar
        # -------------------------------------------------------------------------------
        self.pickInformationBoardButton = QPushButton(self)
        self.pickInformationBoardButton.move(0, 0)
        self.importFileButton = QPushButton(self)
        self.importFileButton.move(40, 0)
        self.addPageButton = QPushButton(self)
        self.addPageButton.move(300, 0)
        self.analyserConfigurationButton = QPushButton(self)
        self.analyserConfigurationButton.move(340, 0)
        self.analyserSaveButton = QPushButton(self)
        self.analyserSaveButton.move(380, 0)
        self.startVideoCaptureButton = QPushButton(self)
        self.startVideoCaptureButton.move(420, 0)

        self.myButtonList.append(self.pickInformationBoardButton)
        self.myButtonList.append(self.importFileButton)
        self.myButtonList.append(self.addPageButton)
        self.myButtonList.append(self.analyserConfigurationButton)
        self.myButtonList.append(self.analyserSaveButton)
        self.myButtonList.append(self.startVideoCaptureButton)
        self.create_widget()

        self.connect(self.pickInformationBoardButton, SIGNAL("clicked()"), self.pick_information_board_button_clicked)
        self.connect(self.importFileButton, SIGNAL("clicked()"), self.file_open_button_clicked)
        self.connect(self.addPageButton, SIGNAL("clicked()"), self.add_page_button_clicked)
        self.connect(self.startVideoCaptureButton, SIGNAL("clicked()"), self.active_video_capture_task)

        # ------------------------------------------------------------------------------------------
        # Display message on the status bar while the mouse's pointer is hovering a pushbutton
        # ------------------------------------------------------------------------------------------
        self.connect(ObjectEventService(self.pickInformationBoardButton), SIGNAL("MouseHovered"), self.pick_information_board_button_hovered)
        self.connect(ObjectEventService(self.importFileButton), SIGNAL("MouseHovered"), self.open_file_button_hovered)
        self.connect(ObjectEventService(self.addPageButton), SIGNAL("MouseHovered"), self.add_page_button_hovered)
        self.connect(ObjectEventService(self.organizationLabel), SIGNAL("MouseHovered"), self.organization_label_hovered)
        self.connect(ObjectEventService(self.pickInformationBoardButton), SIGNAL("MouseLeaved"), self.button_leaved)
        self.connect(ObjectEventService(self.importFileButton), SIGNAL("MouseLeaved"), self.button_leaved)
        self.connect(ObjectEventService(self.addPageButton), SIGNAL("MouseLeaved"), self.button_leaved)
        self.connect(ObjectEventService(self.organizationLabel), SIGNAL("MouseLeaved"), self.button_leaved)

    def create_widget(self):
        """
            -- set the property of the pushbutton
        """
        for i in range(0, len(self.myButtonList)):
            self.myButtonList[i].setIcon(QIcon(":/%s.png" % self.myButtonString[i]))
            self.myButtonList[i].setMouseTracking(True)
            self.myButtonList[i].setFixedSize(self.buttonSize)
            self.myButtonList[i].setFlat(True)

    def button_leaved(self):
        """
            -- while the mouse's pointer has been just leaved the area of a pushbutton
        """
        self.parent().get_status_bar_reference().clear_message()

    def pick_information_board_button_hovered(self):
        """
            -- while the mouse's pointer hovering the pickInformationBoardButton's area
        """
        if not self.pickInformationBoardButtonClicked:
            self.parent().get_status_bar_reference().display_message("click the button to collapse the widget at the left side")
        else:
            self.parent().get_status_bar_reference().display_message("click the button to display the widget at the left side")

    def open_file_button_hovered(self):
        self.parent().get_status_bar_reference().display_message("click the button to import a file")

    def add_page_button_hovered(self):
        self.parent().get_status_bar_reference().display_message("click the button to add a page in the plotting workspace")

    def organization_label_hovered(self):
        self.parent().get_status_bar_reference().display_message("you could also drag a file here to achieve the import action")

    def file_open_button_clicked(self):
        # Open a window for use to choose the file which use want to import, then get the file path
        filepath = QFileDialog.getOpenFileName(self.parent(), "Open file dialog", "/")

        # complete all the procedure of the add file action
        self.add_file_from_path(filepath)

    def add_file_from_path(self, filepath):
        """
            Analyse the filepath passed and get the enough information for reading and displaying
            1.check if the file from the path passed in has already been imported, if not, import th path firstly to the file path list
            2.identify the type of the document

            :param filepath:
            :return:
            """
        if filepath in self.filepathList:
            print 'do not import the same file another time'
            return

        self.filepathList.append(filepath)

        self.analyserMediator.set_path_list_to_global_context(self.filepathList)

        temp = filepath.split("/")
        filename = temp[len(temp) - 1]
        temp = filename.split(".")

        if len(temp) == 2:
            file_type = temp[1]
        else:
            return

        if file_type == "csv":
            csv_file = self.analyserMediator.add_a_csvfile_request(filepath, filename)  # ask the controller to create a csv file object in the global context
            self.parent().get_main_operating_widget_reference().get_information_board().add_file_to_file_list_tree_widget(filename, file_type)
            self.analyserMediator.add_the_csv_file_into_context(csv_file)
            self.analyserMediator.generate_an_action_into_global_context('import file from ' + filepath)
            return True
        elif file_type == "gen":
            lom_file = self.analyserMediator.add_a_lomfile_request(filepath, filename)
            self.parent().get_main_operating_widget_reference().get_information_board().add_file_to_file_list_tree_widget(filename, file_type)
            self.analyserMediator.add_the_lom_file_into_context(lom_file)
            self.analyserMediator.generate_an_action_into_global_context('import file from ' + filepath)
            return True
        return False


    def delete_the_file_path(self, filename):
        for path in self.filepathList:
            if path.__contains__(filename):
                self.filepathList.remove(path)
                self.analyserMediator.delete_file_by_name_from_context(filename)

    def resizeEvent(self, event):
        self.organizationLabel.move(self.parent().width() - 105, 0)

    def set_analyseur_mediator(self, analyseur_mediator):
        self.analyserMediator = analyseur_mediator

    def pick_information_board_button_clicked(self):
        if not self.pickInformationBoardButtonClicked:
            self.parent().get_main_operating_widget_reference().get_information_board().close()
            self.addPageButton.move(80, 0)
            self.analyserConfigurationButton.move(120, 0)
            self.analyserSaveButton.move(160, 0)
            self.startVideoCaptureButton.move(200, 0)
            self.pickInformationBoardButton.setIcon(QIcon(":/fileList-pressed.png"))
        else:
            self.parent().get_main_operating_widget_reference().get_information_board().show()
            self.addPageButton.move(300, 0)
            self.analyserConfigurationButton.move(340, 0)
            self.analyserSaveButton.move(380, 0)
            self.startVideoCaptureButton.move(420, 0)
            self.pickInformationBoardButton.setIcon(QIcon(":/fileList.png"))

        self.pickInformationBoardButtonClicked = not self.pickInformationBoardButtonClicked

    def add_page_button_clicked(self):
        page_index = self.parent().get_main_operating_widget_reference().get_plotting_workspace().add_a_page_in_workspace()
        info = 'page ' + str(page_index) + ' created...'
        self.parent().get_status_bar_reference().display_message(info)
        self.analyserMediator.generate_an_action_into_global_context('add a page in workspace')

    # TODO capture a 30s video
    def active_video_capture_task(self):
        self.startVideoCaptureButton.setIcon(QIcon(":/screen_grab_clicked.png"))
        self.screenGrabActivated = True
        print "active_video_capture_task"
        #threading.Thread(None, self.do_grab_screen).start()


        #self.openVideoScreen()

        self.do_video_acquisition()

    #generate a qwidget to display video captured in reeal time
    def openVideoScreen(self):
        self.videoDisplayWidget.show()

    def do_video_acquisition(self):
        print "capture work"

        capture = cv.CaptureFromCAM(0)
        num = 0;
        while True:
            img = cv.QueryFrame(capture)
            cv.ShowImage("camera",img)

            key = cv.WaitKey(10)
            if key == 27:
                break
            if key == ord(' '):
                num = num+1
                filename = "frmaes_%s.jpg" % num
                cv.SaveImage(filename,img)

        del(capture)
        cv.DestroyWindow("camera")

        """
        grab_begin = False
        flag2 = True
        while flag2:
            if not grab_begin and self.parent().get_mouse_stat():
                print 'beginning'
                self.Coordinate[0] = QCursor.pos().x()
                self.Coordinate[1] = QCursor.pos().y()
                grab_begin = True

            if grab_begin and not self.parent().get_mouse_stat():
                print 'finish'
                self.Coordinate[2] = abs(QCursor.pos().x() - self.Coordinate[0])
                self.Coordinate[3] = abs(QCursor.pos().y() - self.Coordinate[1])
                print self.Coordinate

                pic = ImageGrab.grab(self.Coordinate)
                pic.save("321.jpg")

                flag2 = False
                self.screenGrabActivated = False
        """

    def get_screen_grab_stat(self):
        return self.screenGrabActivated



