"""
Last updated on 07/01/2015

@author: Cheng WANG,
"""

from PyQt4.QtCore import *


class ObjectEventService(QObject):
    def __init__(self, parent):
        QObject.__init__(self, parent)
        parent.setMouseTracking(True)
        parent.installEventFilter(self)

    def eventFilter(self, _, event):
        if event.type() == QEvent.MouseMove:
            self.emit(SIGNAL("MouseMove"), event.pos())
        elif event.type() == QEvent.MouseButtonPress:
            self.emit(SIGNAL("MouseClicked"), event.pos())
        elif event.type() == QEvent.MouseButtonRelease:
            self.emit(SIGNAL("MouseReleased"), event.pos())
        elif event.type() == QEvent.MouseButtonDblClick:
            self.emit(SIGNAL("MouseDoubleClick"), event.pos())
        elif event.type() == QEvent.HoverEnter:
            self.emit(SIGNAL("MouseHovered"), event.pos())
        elif event.type() == QEvent.Leave:
            self.emit(SIGNAL("MouseLeaved"))
        return False

        # eventFilter()