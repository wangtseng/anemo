# -*- coding: utf-8 -*-

"""
Last updated on 15/12/2014

@author: Cheng WANG
"""

from AnemoClinoContext.AnemoClinoFile.CSVFile.CSVFile import *
from AnemoClinoContext.AnemoClinoFile.LOMFile.LOMFile import *


class AnalyserMediator:
    """
     this class represent all the titleNames and values in the file
    """
    def __init__(self):
        self.global_context = None
        self.filePath = ""

    def save_actions_in_global_context(self):
        self.global_context.save_actions()

    def get_actions_from_global_context(self):
        return self.global_context.get_actions()

    def generate_an_action_into_global_context(self, action_string):
        self.global_context.add_action(action_string)

    def set_path_list_to_global_context(self, file_path_list):
        self.global_context.set_file_path_list(file_path_list)

    def get_path_list_to_global_context(self):
        return self.global_context.get_file_path_list()

    def get_workspace_path_from_context(self):
        return self.global_context.get_workspace_path()

    def get_calibrated_files_path_from_context(self):
        return self.global_context.get_calibrated_files_path()

    def get_global_context_path_from_context(self):
        return self.global_context.get_global_context_path()

    def set_global_context(self, global_context):
        self.global_context = global_context

    # -------------------------------------------------------------
    #  methods for files data base
    # -------------------------------------------------------------
    @staticmethod
    def add_a_csvfile_request(filepath, filename):
        csv_file = CSVFile()
        csv_file.set_filename(filename)
        csv_file.parse_csv_file(filepath)
        return csv_file

    @staticmethod
    def add_a_lomfile_request(filepath, filename):
        lom_file = LOMFile()
        lom_file.set_filename(filename)
        lom_file.parse_lom_file(filepath)
        return lom_file

    def add_the_csv_file_into_context(self, csv_file):
        self.global_context.add_csv_file(csv_file)

    def add_the_lom_file_into_context(self, lom_file):
        self.global_context.add_lom_file(lom_file)

    def delete_file_by_name_from_context(self, filename):
        self.global_context.delete_file_by_name(filename)

    def get_lom_file_in_context_by_name(self, filename):
        return self.global_context.get_lom_file_by_name(filename)

    def get_csv_file_in_context_by_name(self, filename):
        return self.global_context.get_csv_file_by_name(filename)

    def check_if_csv_file_created(self, filename):
        return self.global_context.csv_file_existed(filename)

    def check_if_lom_file_created(self, filename):
        return self.global_context.lom_file_existed(filename)

    # -------------------------------------------------------------
    #  methods for plotting context center
    # -------------------------------------------------------------
    def change_the_plotting_context_index_in_a_page(self, page_index, old_plotting_context_index, new_plotting_context_index):
        page_reference = self.global_context.get_a_page_information(page_index)
        plotting_context_reference = page_reference.get_plotting_context_at(old_plotting_context_index)
        plotting_context_reference.set_index(new_plotting_context_index)

    def add_a_plotting_context_in_a_page(self, page_index, plotting_context_index):
        page_reference = self.global_context.get_a_page_information(page_index)
        page_reference.add_a_plotting_context(plotting_context_index)

    def get_a_plotting_context(self, page_index, plotting_context_index):
        page_reference = self.global_context.get_a_page_information(page_index)
        return page_reference.get_plotting_context_at(plotting_context_index)

    def add_a_plotting_page(self, page_index):
        self.global_context.add_a_page(page_index)

    def remove_the_plotting_page(self, page_index):
        self.global_context.remove_the_page(page_index)

    def set_file_type_handling_into_context(self, filetype):
        self.global_context.set_filetype_handling(filetype)

    def get_filetype_handling_from_context(self):
        return self.global_context.get_filetype_handling()

    def get_loaded_lom_files_from_context(self, page_index, plotting_index):
        return self.global_context.get_loaded_lom_files(page_index, plotting_index)

    def get_loaded_lom_files_validity_from_context(self , page_index, plotting_index):
        return self.global_context.get_loaded_lom_files_validity(page_index, plotting_index)

    def get_loaded_csv_files_from_context(self, page_index, plotting_index):
        return self.global_context.get_loaded_csv_files(page_index, plotting_index)

    def get_loaded_csv_files_validity_from_context(self, page_index, plotting_index):
        return self.global_context.get_loaded_csv_files_validity(page_index, plotting_index)

    def set_loaded_csvfiles_into_context(self, loaded_csv_files):
        self.global_context.set_loaded_csvfiles(loaded_csv_files)

    def delete_loaded_csvfile_from_context(self, loaded_csvfile, pos):
        self.global_context.delete_loaded_csvfiles(loaded_csvfile, pos)

    def set_loaded_csvfile_into_context(self, loaded_csv_file, pos):
        self.global_context.set_loaded_csvfile(loaded_csv_file, pos)

    def set_loaded_csvfile_validity_into_context(self, loaded_csv_file_validity, pos):
        self.global_context.set_loaded_csvfile_validity(loaded_csv_file_validity, pos)

    def set_loaded_csvfiles_validity_into_context(self, loaded_csv_files_validity):
        self.global_context.set_loaded_csvfiles_validity(loaded_csv_files_validity)

    def set_loaded_lomfile_into_context(self, loaded_lomfile, pos):
        self.global_context.set_loaded_lom_files(loaded_lomfile, pos)

    def delete_loaded_lomfile_from_context(self, loaded_lomfile, pos):
        self.global_context.delete_loaded_lomfiles(loaded_lomfile, pos)

    def set_loaded_lom_files_validity_into_context(self, loaded_lomfile_validity, pos):
        self.global_context.set_loaded_lom_files_validity(loaded_lomfile_validity, pos)