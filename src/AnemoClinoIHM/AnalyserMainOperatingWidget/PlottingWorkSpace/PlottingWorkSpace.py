"""
Last updated on 18/12/2014

@author: Cheng WANG,
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PageWidget import PageWidget


class PlottingWorkSpace(QWidget):
    """ PlottingWorkSpace
        -- on this workspace, users can create the pages
    """
    def __init__(self, parent=None):
        super(PlottingWorkSpace, self).__init__(parent)

        the_table_style = "QTabWidget::pane {border-top: 0px solid gainsboro; border-bottom: 0px solid gainsboro;} " \
                          "QTabWidget::tab-bar {alignment: left;}  " \
                          "QTabBar::tab {border: 0px solid #C4C4C3;border-bottom-color: transparent; border-top-left-radius: 0px;border-top-right-radius: 0px; min-width: 8ex; font:500 9pt Times; color: darkGray; padding: 0px 5px 0px 5px} " \
                          "QTabBar::tab:selected, QTabBar::tab:hover {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 LightSteelBlue, stop: 0.4 #f4f4f4,stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);}" \
                          "QTabBar::close-button{border-image: url(:/no.png)}" \
                          "QTabBar::close-button:hover {border-image: url(:/close-hover.png)}"
        self.analyseurMediator = None
        self.setGeometry(300, 0, self.parent().parent().get_app_width() - 300, self.parent().height())

        # ------------------------------------------
        # attributes initialization
        # ------------------------------------------
        self.pageCount = 0
        self.pageList = []

        self.plottingPages = QTabWidget()
        self.plottingPages.setStyleSheet(the_table_style)
        self.plottingPages.setTabsClosable(True)
        self.plottingPages.setContextMenuPolicy(Qt.ActionsContextMenu)

        my_layout = QVBoxLayout(self)
        my_layout.setSpacing(0)
        my_layout.setContentsMargins(1, 6, 1, 1)
        my_layout.addWidget(self.plottingPages)

        self.connect(self.plottingPages, SIGNAL("tabCloseRequested(int)"), self.delete_page)

    def set_analyseur_mediator(self, analyseur_mediator):
        """
            -- set the reference of the controller to workspace, which can be used to access to the global context
        :param analyseur_mediator:
        :return:
        """
        self.analyseurMediator = analyseur_mediator

    def get_the_page_at(self, index):
        print 'nbr of page: ', len(self.pageList)
        for page in self.pageList:
            if page.get_my_page_index() == index:
                return page

    def add_a_page_in_workspace(self):
        """
            --add a page in the plotting workspace, at the same time, add a page in the global context with the same index of page
        """
        if self.pageCount == 0:
            self.setStyleSheet("background-color:AliceBlue")

        if self.pageCount >= 0:
            page = PageWidget(self, self.pageCount)
            page.set_analyser_mediator(self.analyseurMediator)
            self.pageList.append(page)
            self.plottingPages.insertTab(self.pageCount, page, "Page" + str(self.pageCount))
            self.analyseurMediator.add_a_plotting_page(self.pageCount)
            self.pageCount += 1

        return self.pageCount - 1

    def delete_page(self, index):
        """
            --delete a page from the plotting workspace, at the same time, delete the page information related from the context according to the page number
        """
        print index
        self.analyseurMediator.remove_the_plotting_page(index)
        self.analyseurMediator.generate_an_action_into_global_context('delete the page ' + str(index))
        del self.pageList[index]
        for i in range(index, self.pageCount):
            self.plottingPages.removeTab(index)

        self.pageCount -= 1
        for i in range(index, self.pageCount):
            self.plottingPages.insertTab(i, self.pageList[i], "Page" + str(i))
        for j in range(0, len(self.pageList)):
            self.pageList[j].set_my_page_index(j)

        if self.pageCount == 0:
            self.setStyleSheet("background-color:transparent")

    def update_file_list(self):
        for i in self.pageList:
            i.update_file_list()

