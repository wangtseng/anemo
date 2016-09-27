# coding=utf-8
"""
Last updated on 15/12/2014

@author: Cheng WANG
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from AnemoClinoIHM.AnalyserUsefulClasses.ObjectEventService import ObjectEventService
from AnemoClinoIHM.AnalyserUsefulClasses.RECT import *
import win32gui
import ctypes
from PIL import ImageGrab
import win32api, win32con
import pythoncom

# noinspection PyArgumentList
from MenuBarOfAnalyseur import MenuBarOfAnalyseur


class TitleBarOfAnalyseur(QWidget):
    """TitleBarOfAnalyseur

    This class represent the title bar of the main window of the anemo clino analyser, which include the Name of the application at the right side
    and four push button to control the main window. the click & move of the mouse's left button trigger the moving of the main window

    Attributes:
        - principal components of the title bar
            ---------------------------------------------------------------------------------------------------------------------------------
            | analyserTitle |                         | picktoolbarButton | minimizeWindowButton | maximizeWindowButton | closeWindowButton |
            ---------------------------------------------------------------------------------------------------------------------------------
    """

    def __init__(self, parent=None):
        super(TitleBarOfAnalyseur, self).__init__(parent)
        self.parent = parent
        # ----------------------------------------------------------
        # Attributes initialization
        # ----------------------------------------------------------
        self.analyserMediator = None
        self.mousePointerMove = None
        self.mousePosition = None
        self.mouseLeftButtonPressed = False
        self.m_bMaxWin = False
        self.toolbarPickedUp = False
        self.m_rectRestoreWindow = self.parent.geometry()
        button_size = QSize(20, 20)
        font = QFont("Times", 10, QFont.StyleItalic, True)
        self.rect = RECT()

        # ----------------------------------------------------------
        # configure the appearance and the setting of the title bar
        # ----------------------------------------------------------
        self.setFixedHeight(30)
        self.setMouseTracking(True)

        # -----------------------------------------------------------
        # components of the title bar
        # -----------------------------------------------------------
        # --the name of the app
        self.analyserTitle = QLabel(self)
        self.analyserTitle.setFixedHeight(30)
        self.analyserTitle.setText("AnemoClinoAnalyseur")
        self.analyserTitle.setStyleSheet("margin-left:6px; color: AliceBlue")
        self.analyserTitle.setCursor(Qt.PointingHandCursor)
        self.analyserTitle.setFont(QFont("Helvetica", 8, QFont.AnyStyle, True))
        self.analyserTitle.move(0, 0)

        # -- the embedded menu bar
        self.menuBar = QWidget(self)
        self.menuBar.move(300, 0)
        self.menuBar.setFixedHeight(30)
        self.analyserMenuBar = MenuBarOfAnalyseur(self)
        self.analyserMenuBar.setFont(QFont("Helvetica", 8, QFont.AnyStyle, True))
        self.ll = QVBoxLayout(self.menuBar)
        self.ll.addWidget(self.analyserMenuBar)
        self.ll.setMargin(0)
        self.ll.setSpacing(0)

        # --button to close the main window
        self.closeWindowButton = QPushButton()
        self.closeWindowButton.setFixedSize(button_size)
        self.closeWindowButton.setText('x')
        self.closeWindowButton.setStyleSheet('color:AliceBlue')
        self.closeWindowButton.setFlat(True)

        # --button to maximize the main window
        self.maximizeWindowButton = QPushButton()
        self.maximizeWindowButton.setFixedSize(button_size)
        self.maximizeWindowButton.setText('+')
        self.maximizeWindowButton.setStyleSheet('color:AliceBlue')
        self.maximizeWindowButton.setFlat(True)

        # --button to minimize the main window
        self.minimizeWindowButton = QPushButton()
        self.minimizeWindowButton.setFixedSize(button_size)
        self.minimizeWindowButton.setText(QString.fromUtf8('—'))
        self.minimizeWindowButton.setStyleSheet('color:AliceBlue')
        self.minimizeWindowButton.setFlat(True)

        # --button to pick up and pull down the tool bar
        self.pickToolbarButton = QPushButton()
        self.pickToolbarButton.setFixedSize(button_size)
        self.pickToolbarButton.setText(QString.fromUtf8('↑'))
        self.pickToolbarButton.setStyleSheet('color:AliceBlue')
        self.pickToolbarButton.setFlat(True)

        self.buttonsNecessaryLabel = QPushButton(self)
        self.buttonsNecessaryLabel.setStyleSheet("background-color:transparent")
        self.buttonsNecessaryLabel.setFlat(True)
        self.buttonsNecessaryLabel.setFixedSize(80, 30)
        self.buttonsNecessaryLabel.setCursor(Qt.CustomCursor)
        buttons_necessary_label_layout = QHBoxLayout(self.buttonsNecessaryLabel)
        buttons_necessary_label_layout.addWidget(self.pickToolbarButton)
        buttons_necessary_label_layout.addWidget(self.minimizeWindowButton)
        buttons_necessary_label_layout.addWidget(self.maximizeWindowButton)
        buttons_necessary_label_layout.addWidget(self.closeWindowButton)
        buttons_necessary_label_layout.setMargin(0)
        buttons_necessary_label_layout.setSpacing(0)

        self.connect(self.minimizeWindowButton, SIGNAL("clicked()"), self.minimize_window)
        self.connect(self.maximizeWindowButton, SIGNAL("clicked()"), self.maximize_window)
        self.connect(self.closeWindowButton, SIGNAL("clicked()"), self.close_window)
        self.connect(self.pickToolbarButton, SIGNAL("clicked()"), self.on_pick_toolbar_button_clicked)

        # display message on the status bar while the mouse's pointer is hovering a pushbutton
        self.connect(ObjectEventService(self.minimizeWindowButton), SIGNAL("MouseHovered"), self.minimize_window_button_hovered)
        self.connect(ObjectEventService(self.maximizeWindowButton), SIGNAL("MouseHovered"), self.maximize_window_button_hovered)
        self.connect(ObjectEventService(self.closeWindowButton), SIGNAL("MouseHovered"), self.close_window_button_hovered)
        self.connect(ObjectEventService(self.pickToolbarButton), SIGNAL("MouseHovered"), self.pick_toolbar_button_hovered)
        self.connect(ObjectEventService(self.buttonsNecessaryLabel), SIGNAL("MouseHovered"), self.buttons_hovered)

        self.connect(ObjectEventService(self.minimizeWindowButton), SIGNAL("MouseLeaved"), self.button_leaved)
        self.connect(ObjectEventService(self.maximizeWindowButton), SIGNAL("MouseLeaved"), self.button_leaved)
        self.connect(ObjectEventService(self.closeWindowButton), SIGNAL("MouseLeaved"), self.button_leaved)
        self.connect(ObjectEventService(self.pickToolbarButton), SIGNAL("MouseLeaved"), self.button_leaved)
        self.connect(ObjectEventService(self.buttonsNecessaryLabel), SIGNAL("MouseLeaved"), self.buttons_leaved)

    def get_parent_widget(self):
        return self.parent

    def set_analyseur_mediator(self, analyseur_mediator):
        self.analyserMediator = analyseur_mediator
        self.analyserMenuBar.set_analyseur_mediator(analyseur_mediator)

    def grab_fullscreen(self):
        hwnd = win32gui.GetForegroundWindow()
        ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(self.rect))
        coordinate = (self.rect.left + 2, self.rect.top + 2, self.rect.right - 2, self.rect.bottom - 2)
        pic = ImageGrab.grab(coordinate)

        dialog = QFileDialog()
        path_to_save = dialog.getSaveFileName(self.parent, "Open file dialog", "/")

        if str(path_to_save).__contains__('.'):
            pic.save(str(path_to_save))

    def buttons_leaved(self):
        self.pickToolbarButton.setStyleSheet('color:AliceBlue')
        self.minimizeWindowButton.setStyleSheet('color:AliceBlue')
        self.maximizeWindowButton.setStyleSheet('color:AliceBlue')
        self.closeWindowButton.setStyleSheet('color:AliceBlue')

    def buttons_hovered(self):
        self.pickToolbarButton.setStyleSheet('QPushButton{color:black} QPushButton:pressed {background-color: white;}')
        self.minimizeWindowButton.setStyleSheet('QPushButton{color:black} QPushButton:pressed {background-color: white;}')
        self.maximizeWindowButton.setStyleSheet('QPushButton{color:black} QPushButton:pressed {background-color: white;}')
        self.closeWindowButton.setStyleSheet('QPushButton{color:black} QPushButton:pressed {background-color: white;}')

    def pick_toolbar_button_hovered(self):
        """
            -- while the mouse's pointer hovering the pickToolbarButton's area
        """
        if not self.toolbarPickedUp:
            self.parent.get_status_bar_reference().display_message("click the button to pick up the tool bar")
        else:
            self.parent.get_status_bar_reference().display_message("click the button to display the tool bar")

    def minimize_window_button_hovered(self):
        """
            -- while the mouse's pointer hovering the minimizeWindowButton's area
        """
        self.parent.get_status_bar_reference().display_message("click the button to minimize the main window")

    def maximize_window_button_hovered(self):
        """
            -- while the mouse's pointer hovering the maximizeWindowButton's area
        """
        self.parent.get_status_bar_reference().display_message("click the button to maximize the main window")

    def close_window_button_hovered(self):
        """
            -- while the mouse's pointer hovering the closeWindowButton's area
        """
        self.parent.get_status_bar_reference().display_message("click the button to close the main window")

    def button_leaved(self):
        """
            -- while the mouse's pointer has been just leaved the area of a pushbutton
        """
        self.parent.get_status_bar_reference().clear_message()

    def on_pick_toolbar_button_clicked(self):
        """
            -- the method to achieve pick up or pull down the tool bar
        """
        if self.toolbarPickedUp:
            self.parent.get_toolbar_reference().show()
            self.toolbarPickedUp = False
            self.pickToolbarButton.setText(QString.fromUtf8('↑'))
        else:
            self.parent.get_toolbar_reference().close()
            self.pickToolbarButton.setText(QString.fromUtf8('↓'))
            self.toolbarPickedUp = True

    def minimize_window(self):
        """
            -- minimize the main window
        """
        self.parent.showMinimized()

    def maximize_window(self):
        """
            -- maximize the main window
        """
        self.parent.setGeometry(QApplication.desktop().availableGeometry())
        self.m_bMaxWin = True
        self.parent.set_window_maximize_size()
        self.parent.draw_background()

    def close_window(self):
        """
            -- close the main window
        """
        reply = QMessageBox.question(None,
                                     "AnemoClinoAnalyseur",
                                     "Save unsaved changes?",
                                     QMessageBox.Yes | QMessageBox.No |
                                     QMessageBox.Cancel)
        if reply == QMessageBox.Cancel:
            return
        elif reply == QMessageBox.No:
            self.parent.close()
        elif reply == QMessageBox.Yes:
            self.analyserMediator.save_actions_in_global_context()
            self.parent.close()


    def resizeEvent(self, event):
        """
            -- positioning of the four button
        :param event:
        """
        self.buttonsNecessaryLabel.move(self.parent.width() - 80, 0)
        """
        self.closeWindowButton.move(self.parent().width() - 20, 0)
        self.maximizeWindowButton.move(self.parent().width() - 40, 0)
        self.minimizeWindowButton.move(self.parent().width() - 60, 0)
        self.pickToolbarButton.move(self.parent().width() - 80, 0)
        """

    def mousePressEvent(self, event):
        """
            -- get the mouse's left button clicked event
        :param event:
        """
        if event.button() == Qt.LeftButton:
            if (event.y() < 5) or (event.x() < 5):
                event.ignore()
                return
            self.mousePosition = event.globalPos()
            self.mouseLeftButtonPressed = True

    def mouseMoveEvent(self, event):
        """
            -- if the mouse is moving while it's left button has always been maintain clicked, then move the main window with the mouse's pointer
        :param event:
        """
        if self.mouseLeftButtonPressed:
            self.mousePointerMove = event.globalPos()
            self.parent.move(self.parent.pos() + self.mousePointerMove - self.mousePosition)
            self.mousePosition = self.mousePointerMove
        event.ignore()

    def mouseReleaseEvent(self, event):
        """
            -- get the mouse's left button release event
        :param event:
        """
        if event.button() == Qt.LeftButton:
            self.mouseLeftButtonPressed = False
        event.ignore()

    def mouseDoubleClickEvent(self, event):
        """
            -- double click the mouse's left button to maximize/restore the size of the screen
        :param event:
        """
        if event.button() == Qt.LeftButton:
            if not self.m_bMaxWin:
                self.m_rectRestoreWindow = self.parent.geometry()
                self.parent.setGeometry(QApplication.desktop().availableGeometry())
            else:
                self.parent.setGeometry(self.m_rectRestoreWindow)

            self.m_bMaxWin = not self.m_bMaxWin
            self.parent.set_window_maximize_size()
            self.parent.draw_background()