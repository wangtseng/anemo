# -*- coding: utf-8 -*-
"""
Last updated on 07/01/2015

@author: Cheng WANG,
"""

from PlottingContext import PlottingContext


class PageInformation():
    def __init__(self, index):
        print 'generate the page :', index
        self.pageIndex = index
        self.plottingBoardCount = 0
        self.plottingContextList = []                # curve chart list information
        self.loadedCSVFiles = []
        self.loadedLOMFiles = []
        self.loadedCSVFilesValidity = []
        self.loadedLOMFilesValidity = []
        self.fileTypeHandling = ""

    def get_page_index(self):
        return self.pageIndex

    def get_number_of_plotting_context(self):
        return len(self.plottingContextList)

    def set_file_type_work_with(self, type):
        self.fileTypeHandling = type
        for curve in self.plottingContextList:
            curve.set_filetype_handling(type)
    '''
    def set_loaded_csvfiles_into_page(self, loaded_csvfile):
        self.loadedCSVFiles.append(loaded_csvfile)
        for curve in self.plottingContextList:
            curve.set_loaded_csvfiles_into_plotting_context(loaded_csvfiles)
    '''

    def set_loaded_csvfile_into_page(self, loaded_csvfile, pos):
        self.loadedCSVFiles.insert(pos, loaded_csvfile)
        for curve in self.plottingContextList:
            curve.set_loaded_csvfile_into_plotting_context(loaded_csvfile, pos)

    def delete_loaded_csvfile_into_page(self, loaded_csvfile, pos):
        del self.loadedCSVFiles[pos]
        del self.loadedCSVFilesValidity[pos]
        for curve in self.plottingContextList:
            curve.delete_loaded_csvfile_from_plotting_context(loaded_csvfile, pos)

    def delete_loaded_lomfile_into_page(self, loaded_lomfile, pos):
        del self.loadedLOMFiles[pos]
        del self.loadedLOMFilesValidity[pos]

        for curve in self.plottingContextList:
            curve.delete_loaded_lomfile_from_plotting_context(loaded_lomfile, pos)

    def set_loaded_csvfile_validity_into_page(self, loaded_csvfile_validity, pos):
        self.loadedCSVFilesValidity.insert(pos, loaded_csvfile_validity)
        for curve in self.plottingContextList:
            curve.set_loaded_csvfile_validity_into_plotting_context(loaded_csvfile_validity, pos)

    def set_loaded_csvfiles_validity_into_page(self, loaded_csv_files_validity):
        self.loadedCSVFilesValidity = loaded_csv_files_validity
        for curve in self.plottingContextList:
            curve.set_loaded_csvfiles_validity_into_plotting_context(loaded_csv_files_validity)

    def set_loaded_lomfile_validity_into_page(self, loaded_lomfile_validity, pos):
        self.loadedLOMFilesValidity.insert(pos, loaded_lomfile_validity)
        for curve in self.plottingContextList:
            curve.set_loaded_lomfile_validity_into_plotting_context(loaded_lomfile_validity, pos)

    def set_loaded_lomfiles_validity_into_page(self, loaded_lomfile_validity):
        self.loadedLOMFilesValidity = loaded_lomfile_validity
        for curve in self.plottingContextList:
            curve.set_loaded_lomfiles_validity_into_plotting_context(loaded_lomfile_validity)

    def set_loaded_lomfiles_into_page(self, loaded_lomfiles):
        self.loadedLOMFiles = loaded_lomfiles
        for curve in self.plottingContextList:
            curve.set_loaded_lomfiles_into_plotting_context(loaded_lomfiles)

    def set_loaded_lomfile_into_page(self, loaded_lomfile, pos):
        self.loadedLOMFiles.insert(pos, loaded_lomfile)
        for curve in self.plottingContextList:
            curve.set_loaded_lomfile_into_plotting_context(loaded_lomfile, pos)

    def add_a_plotting_context(self, plotting_board_index):
        plotting_context = PlottingContext(plotting_board_index)
        if len(self.loadedCSVFiles) > 0:
            plotting_context.set_loaded_csvfiles_into_plotting_context(self.loadedCSVFiles)
            plotting_context.set_loaded_csvfiles_validity_into_plotting_context(self.loadedCSVFilesValidity)

        if len(self.loadedLOMFiles) > 0:
            plotting_context.set_loaded_lomfiles_into_plotting_context(self.loadedLOMFiles)
            plotting_context.set_loaded_lomfiles_validity_into_plotting_context(self.loadedLOMFilesValidity)

        self.plottingContextList.append(plotting_context)

    def remove_the_plotting_context_at(self, index):
        for i in self.plottingContextList:
            index_temp = i.get_index()
            if index_temp == index:
                del self.plottingContextList[self.plottingContextList.index(i)]

    def get_plotting_context_at(self, index):
        for i in self.plottingContextList:
            index_temp = i.get_index()
            if index_temp == index:
                return i

    def get_plotting_context_list(self):
        return self.plottingContextList