# -*- coding: utf-8 -*-

"""
Last updated on 16/12/2014

@author: Cheng WANG
"""

from AnemoClinoEnvironment.PageInformation import PageInformation
from AnemoClinoActions.AnalyserActions import AnalyserActions


class GlobalContext:

    """
        -- this class is just like a data base which include:
                -- all the files loaded
                --
                -- ...
    """
    def __init__(self):

        # ---------------------------------
        # files information
        # ---------------------------------
        self.csvFiles = []
        self.lomFiles = []
        self.filePathList = []

        # ---------------------------------
        #  context of workspace
        # ---------------------------------
        self.username = ''
        self.workspacePath = ''
        self.calibratedFilesPath = ''
        self.globalContextPath = ''
        self.pageInformationList = []
        self.loadedCSVFiles = []
        self.loadedLOMFiles = []
        self.loadedCSVFilesValidity = []
        self.loadedLOMFilesValidity = []
        self.fileTypeHandling = ""

        # ---------------------------------------------------------
        # command list which store user's each action sequentially
        # ---------------------------------------------------------
        self.actions = AnalyserActions()

    def save_actions(self):
        self.actions.write(self.globalContextPath)

    def add_action(self, action_string):
        self.actions.add_an_action(action_string)

    def get_actions(self):
        return self.actions.get_actions()

    def get_file_path_list(self):
        return self.filePathList

    def set_file_path_list(self, file_path_list):
        self.filePathList = file_path_list

    def set_workspace_path(self, path):
        self.workspacePath = path

    def get_workspace_path(self):
        return self.workspacePath

    def set_calibrated_files_path(self, path):
        self.calibratedFilesPath = path

    def get_calibrated_files_path(self):
        return self.calibratedFilesPath

    def set_global_context_path(self, path):
        self.globalContextPath = path

    def set_user_name(self, username):
        self.username = username

    def get_user_name(self):
        return self.username

    def get_global_context_path(self):
        return self.globalContextPath

    def get_command_list(self):
        return self.commandList

    def set_filetype_handling(self, filetype):
        """
            -- set the filetype working with currently to the context
        :param filetype:
        """
        self.fileTypeHandling = filetype

    def get_filetype_handling(self):
        return self.fileTypeHandling

    # ---------------------------------------------------------
    # methods for lom files
    # ---------------------------------------------------------
    def get_loaded_lom_files(self, page_index, plotting_index):
        if len(self.pageInformationList) > 0:
            for pageInfo in self.pageInformationList:
                if pageInfo.get_page_index() == page_index:
                    plotting_context_list = pageInfo.get_plotting_context_list()
                    for plotting_context in plotting_context_list:
                        if plotting_context.get_index() == plotting_index:
                            return plotting_context.get_loaded_lomfiles()
        else:
            return self.loadedLOMFiles

    def get_loaded_lom_files_validity(self, page_index, plotting_index):
        if len(self.pageInformationList) > 0:
            for pageInfo in self.pageInformationList:
                if pageInfo.get_page_index() == page_index:
                    plotting_context_list = pageInfo.get_plotting_context_list()
                    for plotting_context in plotting_context_list:
                        if plotting_context.get_index() == plotting_index:
                            return plotting_context.get_loaded_lomfiles_validity()
        else:
            return self.loadedLOMFiles

    def add_lom_file(self, lom_file):
        self.lomFiles.append(lom_file)

    def set_loaded_lom_files(self, loaded_lomfile, pos):
        self.loadedLOMFiles.insert(pos, loaded_lomfile)
        for pageInfo in self.pageInformationList:
            pageInfo.set_loaded_lomfile_into_page(loaded_lomfile, pos)

    def set_loaded_lom_files_validity(self, loaded_lomfile_validity, pos):
        self.loadedLOMFilesValidity.insert(pos, loaded_lomfile_validity)
        for pageInfo in self.pageInformationList:
            pageInfo.set_loaded_lomfile_validity_into_page(loaded_lomfile_validity, pos)

    def get_lom_file_by_name(self, filename):
        for i in range(len(self.lomFiles)):
            if self.lomFiles[i].get_filename() == filename:
                return self.lomFiles[i]
        return None

    def lom_file_existed(self, filename):
        for i in range(len(self.lomFiles)):
            if self.lomFiles[i].get_filename() == filename:
                return True
        return False

    def delete_loaded_lomfiles(self, loaded_lomfile, pos):
        del self.loadedLOMFiles[pos]
        del self.loadedLOMFilesValidity[pos]
        for pageInfo in self.pageInformationList:
            pageInfo.delete_loaded_lomfile_into_page(loaded_lomfile, pos)

    # ---------------------------------------------------------
    # methods for csv files
    # ---------------------------------------------------------
    def get_loaded_csv_files(self, page_index, plotting_index):
        for pageInfo in self.pageInformationList:
            if pageInfo.get_page_index() == page_index:
                plotting_context_list = pageInfo.get_plotting_context_list()
                for plotting_context in plotting_context_list:
                    if plotting_context.get_index() == plotting_index:
                        return plotting_context.get_loaded_csvfiles()

    def get_loaded_csv_files_validity(self, page_index, plotting_index):
        for pageInfo in self.pageInformationList:
            if pageInfo.get_page_index() == page_index:
                plotting_context_list = pageInfo.get_plotting_context_list()
                for plotting_context in plotting_context_list:
                    if plotting_context.get_index() == plotting_index:
                        return plotting_context.get_loaded_csvfiles_validity()

    def set_loaded_csvfile(self, loaded_csvfile, pos):
        self.loadedCSVFiles.insert(pos, loaded_csvfile)
        for pageInfo in self.pageInformationList:
            pageInfo.set_loaded_csvfile_into_page(loaded_csvfile, pos)

    def set_loaded_csvfiles(self, loaded_csvfiles):
        self.loadedCSVFiles = loaded_csvfiles
        for pageInfo in self.pageInformationList:
            pageInfo.set_loaded_csvfiles_into_page(loaded_csvfiles)

    def delete_loaded_csvfiles(self, loaded_csvfile, pos):
        del self.loadedCSVFiles[pos]
        del self.loadedCSVFilesValidity[pos]
        for pageInfo in self.pageInformationList:
            pageInfo.delete_loaded_csvfile_into_page(loaded_csvfile, pos)

    def set_loaded_csvfile_validity(self, loaded_csvfile_validity, pos):
        self.loadedCSVFilesValidity.insert(pos, loaded_csvfile_validity)
        for pageInfo in self.pageInformationList:
            pageInfo.set_loaded_csvfile_validity_into_page(loaded_csvfile_validity, pos)

    def set_loaded_csvfiles_validity(self, loaded_csv_files_validity):
        self.loadedCSVFilesValidity = loaded_csv_files_validity
        for pageInfo in self.pageInformationList:
            pageInfo.set_loaded_csvfiles_validity_into_page(loaded_csv_files_validity)

    def add_csv_file(self, csv_file):
        self.csvFiles.append(csv_file)

    def delete_file_by_name(self, filename):
        temp = filename.split(".")
        if temp[1] == 'csv':
            csvfile = self.get_csv_file_by_name(filename)
            self.csvFiles.remove(csvfile)
        elif temp[1] == 'gen':
            lomfile = self.get_lom_file_by_name(filename)
            self.lomFiles.remove(lomfile)

    def get_csv_file_list(self):
        return self.csvFiles

    def get_csv_file_by_name(self, filename):
        for i in range(len(self.csvFiles)):
            if self.csvFiles[i].get_filename() == filename:
                return self.csvFiles[i]
        return None

    def csv_file_existed(self, filename):
        for i in range(len(self.csvFiles)):
            if self.csvFiles[i].get_filename() == filename:
                return True
        return False

    def add_a_page(self, page_index):
        page_information = PageInformation(page_index)

        for i in range(len(self.loadedCSVFiles)):
            page_information.set_loaded_csvfile_into_page(self.loadedCSVFiles[i], i)
            page_information.set_loaded_csvfile_validity_into_page(0, i)

        for j in range(len(self.loadedLOMFiles)):
            page_information.set_loaded_lomfile_into_page(self.loadedLOMFiles[j], j)
            page_information.set_loaded_lomfile_validity_into_page(0, j)

        page_information.set_file_type_work_with(self.fileTypeHandling)
        self.pageInformationList.append(page_information)

    def remove_the_page(self, index):
        del self.pageInformationList[index]

    def get_a_page_information(self, index):
        for page in self.pageInformationList:
            if page.get_page_index() == index:
                return page