"""
Last updated on 15/12/2014

@author: Cheng WANG,
"""

from AnalyserMainOperatingWidget.MainOperatingWidget import MainOperatingWidget
from AnalyserStatusBar.StatusBar import StatusBar
from AnalyserTitleBar.TitleBarOfAnalyseur import TitleBarOfAnalyseur
from AnalyserToolBar.ToolBarOfAnalyseur import ToolBarOfAnalyseur
from PyQt4.QtCore import *
from PyQt4.QtGui import *


# noinspection PyArgumentList
class AnalyserMainWindow(QFrame):
    """AnalyserMainWindow

        - This class represent the main window of the anemo clino analyser

    Attributes:
        - four principal component
            *******************************************
            *           analyserTitleBar              *
            *******************************************
            *           analyserToolBar               *
            *******************************************
            *                                         *
            *                                         *
            *      analyserMainOperatingWidget        *
            *                                         *
            *                                         *
            *******************************************
            *           analyserStatusBar             *
            *******************************************

    """

    def __init__(self, parent=None):
        super(AnalyserMainWindow, self).__init__(parent)

        # ----------------------------------------------------------
        # positioning the Graphical tool in the middle of the screen
        # ----------------------------------------------------------
        self.desktop = QApplication.desktop()
        width = self.desktop.width()
        height = self.desktop.height()
        self.appWidth = 0.95 * width
        self.appHeight = 0.85 * height
        self.setMinimumWidth(self.appWidth)
        self.setMinimumHeight(self.appHeight)
        self.setGeometry((width - self.appWidth) / 3, (height - self.appHeight) / 3, self.appWidth, self.appHeight)
        self.normalSize = True
        self.mouseStat = True

        # ----------------------------------------------------------
        # configure the appearance of the graphic tool
        # ----------------------------------------------------------
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.setWindowOpacity(0.97)
        self.setMouseTracking(True)
        self.setAutoFillBackground(True)
        self.draw_background()

        # ----------------------------------------------------------
        # initialise the principal components of the graphic tool
        # ----------------------------------------------------------
        self.analyserTitleBar = TitleBarOfAnalyseur(self)
        self.analyserToolBar = ToolBarOfAnalyseur(self)
        self.analyserMainOperatingWidget = MainOperatingWidget(self)
        self.analyserStatusBar = StatusBar(self)
        self.analyserMediator = None

        # ----------------------------------------------------------
        # generate a vertical layout to contains all the component upon
        # ----------------------------------------------------------
        self.analyserMainLayout = QVBoxLayout(self)
        self.analyserMainLayout.addWidget(self.analyserTitleBar)
        self.analyserMainLayout.addWidget(self.analyserToolBar)
        self.analyserMainLayout.addWidget(self.analyserMainOperatingWidget)
        self.analyserMainLayout.addWidget(self.analyserStatusBar)
        self.analyserMainLayout.setSpacing(0)
        self.analyserMainLayout.setContentsMargins(0, 0, 0, 0)
        self.analyserMainLayout.setMargin(0)
        self.analyserMainLayout.setAlignment(Qt.AlignCenter)

    def set_analyseur_mediator(self, analyseur_mediator):
        """
            - broadcast the analyseur_mediator reference to all the view component of the graphical tool
        :param analyseur_mediator:
        """
        self.analyserMediator = analyseur_mediator
        self.analyserToolBar.set_analyseur_mediator(self.analyserMediator)
        self.analyserTitleBar.set_analyseur_mediator(self.analyserMediator)
        self.analyserMainOperatingWidget.set_analyseur_mediator(self.analyserMediator)

    def draw_background(self):
        """
            - configure the background and the size of the graphical tool
        """
        pixmap = QPixmap(":/background.png")
        palette = self.palette()
        if self.normalSize:
            palette.setBrush(QPalette.Background, QBrush(pixmap.scaled(QSize(self.appWidth, self.appHeight), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
        else:
            palette.setBrush(QPalette.Background, QBrush(pixmap.scaled(QSize(self.desktop.width(), self.desktop.height()), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))

        self.setPalette(palette)
        self.setMask(pixmap.mask())
        self.setAutoFillBackground(True)

    def get_app_width(self):
        return self.appWidth

    def get_app_height(self):
        return self.appHeight

    def get_toolbar_reference(self):
        return self.analyserToolBar

    def get_main_operating_widget_reference(self):
        return self.analyserMainOperatingWidget

    def get_title_bar_reference(self):
        return self.analyserTitleBar

    def get_analyser_controller_reference(self):
        return self.analyserMediator

    def get_status_bar_reference(self):
        return self.analyserStatusBar

    def set_window_normal_size(self):
        self.normalSize = True

    def set_window_maximize_size(self):
        self.normalSize = False

    def mousePressEvent(self, *args, **kwargs):
        if self.analyserToolBar.get_screen_grab_stat():
            self.mouseStat = True

    def mouseReleaseEvent(self, *args, **kwargs):
        if self.analyserToolBar.get_screen_grab_stat():
            self.mouseStat = False

    def get_mouse_stat(self):
        return self.mouseStat

    def reset(self):
        self.mousePressed = False
        self.mouseReleased = False