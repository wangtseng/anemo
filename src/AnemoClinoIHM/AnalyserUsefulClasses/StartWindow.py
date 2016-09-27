"""
Last updated on 06/01/2015

@author: Cheng WANG,
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class StartWindow(QDialog):
    def __init__(self, parent=None):
        super(StartWindow, self).__init__(parent)
        self.workspacePath = ''
        self.quitRequested = False
        self.Configured = False
        self.setWindowTitle("Let us begin by configure something ...")
        self.setWindowOpacity(0.92)
        self.resize(500, 200)
        gird_layout = QGridLayout()

        self.workspacePathChooseButton = QPushButton('choose')
        gird_layout.addWidget(self.workspacePathChooseButton, 0, 0)

        self.lineEdit = QLineEdit('choose the place where you want to set as workspace ')
        self.lineEdit.setEnabled(False)
        gird_layout.addWidget(self.lineEdit, 0, 1)

        self.nameOfSession = QLineEdit('set the name of your work ')
        gird_layout.addWidget(self.nameOfSession, 1, 1)

        textArea = QTextEdit()
        gird_layout.addWidget(textArea, 2, 1)

        self.ok_button = QPushButton('ok')
        gird_layout.addWidget(self.ok_button, 5, 0)

        self.connect(self.ok_button, SIGNAL('clicked()'), self.OnButton)
        self.connect(self.workspacePathChooseButton, SIGNAL('clicked()'), self.choose_workspace)
        self.setLayout(gird_layout)

    def get_app_state(self):
        return self.quitRequested

    def OnButton(self):
        if self.workspacePath != '':
            self.Configured = True
            self.close()

    def get_configuration_state(self):
        return self.Configured

    def get_workspace_path(self):
        return self.workspacePath

    def choose_workspace(self):
        dialog = QFileDialog()
        self.workspacePath = dialog.getExistingDirectory(self, "set the place of your workspace", "/")
        self.workspacePath += '\\'
        self.lineEdit.setText(self.workspacePath)
