# ************************************************ -*- coding: utf-8 -*-
"""
Last updated on 06/01/2015

@author: Cheng WANG
"""


class PlottingContext():

    """PlottingContext

    This class represent all information to support the plotting actions on the plotting board

    Attributes:
        -index: the index of the plotting board in a page widget
        -loadedCSVFiles: the list of csv files which has been loaded into the global context
        -loadedLOMFiles: the list of lom which has been loaded into the global context
        -loadedCSVFilesValidity: the list of csv files validity, each file's validity is initial to 0. then, according to the drop event, the class's method will confirm the dropped parameter's existence, if exist in the file, 1, else, 0
        -loadedLOMFilesValidity: the list of lom files validity, each file's validity is initial to 0. then, according to the drop event, the class's method will confirm the dropped label's existence, if exist in the file, 1, else, 0
        *-data_center: the tree architecture to store all the values and parameters from csv or lom file, which will be used while plotting actions
        -fileTypeHandling: the descriptor to inform the plotting board which type of file currently working with
        *-iso_display_mode: the
        *-siso_display_mode:
    """

    def __init__(self, index):
        """Init PlottingContext with the attributes explained above"""
        self.name_of_file_related = ""  # maybe not useful
        self.index = index
        self.loadedCSVFiles = []
        self.loadedLOMFiles = []
        self.loadedCSVFilesValidity = []
        self.loadedLOMFilesValidity = []
        self.data_center = {}
        self.fileTypeHandling = ""
        self.filesHandling = list()  # maybe not useful

        # 0: range,  1: value pointer
        self.iso_display_mode = 0
        self.siso_display_mode = 0

    def reinitialize(self):
        # remove the values and parameter information in the background
        for file_name in self.data_center.keys():
            if str(file_name).__contains__('csv'):
                del self.data_center[file_name]
                self.set_loaded_csvfile_into_plotting_context(file_name, -1)
            elif str(file_name).__contains__('gen'):
                del self.data_center[file_name]
                self.set_loaded_lomfile_into_plotting_context(file_name, -1)

        for i in range(len(self.loadedCSVFilesValidity)):
            self.loadedCSVFilesValidity[i] = 0

        for i in range(len(self.loadedLOMFilesValidity)):
            self.loadedLOMFilesValidity[i] = 0

    def set_iso_display_mode(self, mode):
        self.iso_display_mode = mode

    def set_siso_display_mode(self, mode):
        self.siso_display_mode = mode

    def get_iso_display_mode(self):
        return self.iso_display_mode

    def get_siso_display_mode(self):
        return self.siso_display_mode

    def get_loaded_csvfiles(self):
        return self.loadedCSVFiles

    def get_loaded_csvfiles_validity(self):
        return self.loadedCSVFilesValidity

    def get_loaded_lomfiles(self):
        return self.loadedLOMFiles

    def get_loaded_lomfiles_validity(self):
        return self.loadedLOMFilesValidity

    def set_file_type_work_with(self, filetype):
        self.fileTypeHandling = filetype

    def get_file_type_work_with(self):
        return self.fileTypeHandling

    def set_files_work_with(self, files):
        self.filesHandling = files

    def get_files_work_with(self):
        return self.filesHandling

    def get_label_list_from_lom_file(self, lom_file_name):
        return self.data_center[lom_file_name].keys()

    def set_label_to_lom_files(self, label_name, lom_file_name):
        if label_name not in self.data_center[lom_file_name].keys():
            abscissa_parameter_name = ""
            abscissa_parameter_values = []

            list_of_ordinate_parameter_name = []
            list_of_ordinate_parameter_values = []

            iso_parameter_validity = []
            iso_parameter_values = []
            iso_parameter_name = ""

            siso_parameter_validity = []
            siso_parameter_values = []
            siso_parameter_name = ""

            x = 0

            data_center_for_the_file = {'abscissa': [abscissa_parameter_name, abscissa_parameter_values],
                                        'ordinate': [list_of_ordinate_parameter_name, list_of_ordinate_parameter_values],
                                        'iso': [iso_parameter_name, iso_parameter_values, iso_parameter_validity],
                                        'siso': [siso_parameter_name, siso_parameter_values, siso_parameter_validity],
                                        'dimension': x}

            self.data_center[lom_file_name][label_name] = data_center_for_the_file
            return True

        return False

    def delete_the_label_in_plotting_context(self, label_to_be_deleted, filename):
        del self.data_center[filename][label_to_be_deleted]

    def delete_the_ordinate_in_plotting_context(self, ordinate_name, filename):
        i = self.data_center[filename]['ordinate'][0].index(ordinate_name)
        self.data_center[filename]['ordinate'][0].remove(ordinate_name)
        del self.data_center[filename]['ordinate'][1][i]

    def get_label_list_from_lom_file(self, lom_file_name):
        return self.data_center[lom_file_name].keys()

    def set_loaded_lomfiles_validity_into_plotting_context(self, loaded_lomfiles_validity):
        del self.loadedLOMFilesValidity[:]
        for _ in loaded_lomfiles_validity:
            self.loadedLOMFilesValidity.append(0)

    def set_loaded_lomfile_into_plotting_context(self, name_of_the_loaded_lomfile, pos):
        if pos != -1:
            # if name_of_the_loaded_lomfile not in self.loadedLOMFiles:
            self.loadedLOMFiles.insert(pos, name_of_the_loaded_lomfile)
        data_center_for_the_file = {}
        self.data_center[name_of_the_loaded_lomfile] = data_center_for_the_file

    def set_loaded_lomfile_validity_into_plotting_context(self, loaded_lomfile_validity, pos):
        self.loadedLOMFilesValidity.insert(pos, loaded_lomfile_validity)

    def set_loaded_lomfiles_into_plotting_context(self, name_of_the_loaded_lomfiles):
        del self.loadedLOMFiles[:]
        for i in name_of_the_loaded_lomfiles:
            self.loadedLOMFiles.append(i)

        for lomfile in self.loadedLOMFiles:
            self.set_loaded_lomfile_into_plotting_context(lomfile, -1)

    def set_loaded_csvfiles_into_plotting_context(self, loaded_csv_files):
        del self.loadedCSVFiles[:]
        for i in loaded_csv_files:
            self.loadedCSVFiles.append(i)

        for csvfile in self.loadedCSVFiles:
            self.set_loaded_csvfile_into_plotting_context(csvfile, -1)

    def set_loaded_csvfiles_validity_into_plotting_context(self, loaded_csvfiles_validity):
        del self.loadedCSVFilesValidity[:]
        for _ in loaded_csvfiles_validity:
            self.loadedCSVFilesValidity.append(0)

    def set_loaded_csvfile_validity_into_plotting_context(self, loaded_csvfile_validity, pos):
        self.loadedCSVFilesValidity.insert(pos, loaded_csvfile_validity)

    def set_loaded_lom_files_validity_into_plotting_context(self, loaded_lom_files_validity):
        del self.loadedLOMFilesValidity[:]
        for _ in loaded_lom_files_validity:
            self.loadedLOMFilesValidity.append(0)

    def delete_loaded_csvfile_from_plotting_context(self, loaded_csvfile, pos):
        del self.loadedCSVFiles[pos]
        del self.loadedCSVFilesValidity[pos]
        del self.data_center[loaded_csvfile]

    def delete_loaded_lomfile_from_plotting_context(self, loaded_lomfile, pos):
        del self.loadedLOMFiles[pos]
        del self.loadedLOMFilesValidity[pos]
        del self.data_center[loaded_lomfile]

    def set_loaded_csvfile_into_plotting_context(self, name_of_the_loaded_csv_file, pos):
        if pos != -1:
            self.loadedCSVFiles.insert(pos, name_of_the_loaded_csv_file)

        abscissa_parameter_name = ""
        abscissa_parameter_values = []

        list_of_ordinate_parameter_name = []
        list_of_ordinate_parameter_values = []

        iso_parameter_values = []
        iso_parameter_name = ""

        sub_lists_of_iso = []
        sub_lists_of_iso_index = []

        siso_parameter_values = []
        siso_parameter_name = ""

        sub_lists_of_siso = []
        sub_lists_of_siso_index = []

        data_center_for_the_file = {'abscissa': [abscissa_parameter_name, abscissa_parameter_values],
                                    'ordinate': [list_of_ordinate_parameter_name, list_of_ordinate_parameter_values],
                                    'iso': [iso_parameter_name, iso_parameter_values],
                                    'iso_cut': [sub_lists_of_iso_index, sub_lists_of_iso],
                                    'siso': [siso_parameter_name, siso_parameter_values],
                                    'siso_cut': [sub_lists_of_siso_index, sub_lists_of_siso]}

        self.data_center[name_of_the_loaded_csv_file] = data_center_for_the_file

    def print_data_center(self):
        print "_________________________________"
        print self.data_center
        print "_________________________________"

    def get_data_center(self):
        return self.data_center

    def get_index(self):
        return self.index

    def set_index(self, index):
        self.index = index

    def set_name_of_file_related(self, filename):
        self.name_of_file_related = filename

    def get_name_of_file_related(self):
        return self.name_of_file_related

    """
    The methods to control the iso in the data center
    """

    def set_siso_parameter_name(self, name, filename):
        self.data_center[filename]['siso'][0] = name

    def set_siso_parameter_name_from_lom_file(self, name, label_name, filename):
        self.data_center[filename][label_name]['siso'][0] = name

    def get_siso_parameter_name(self, filename):
        return self.data_center[filename]['siso'][0]

    def get_siso_parameter_name_from_lom_file(self, label_name, filename):
        return self.data_center[filename][label_name]['siso'][0]

    def set_siso_parameter_values(self, siso_values, filename):
        self.data_center[filename]['siso'][1] = siso_values

    def set_siso_parameter_values_from_lom_file(self, siso_values, label_name, filename):
        self.data_center[filename][label_name]['siso'][1] = siso_values

    def set_siso_parameter_validity_from_lom_file(self, siso_validity, label_name, filename):
        self.data_center[filename][label_name]['siso'][2] = siso_validity

    def get_siso_parameter_values(self, filename):
        return self.data_center[filename]['siso'][1]

    def get_siso_parameter_values_from_lom_file(self, label_name, filename):
        return self.data_center[filename][label_name]['siso'][1]

    def get_siso_parameter_validity_from_lom_file(self, label_name, filename):
        return self.data_center[filename][label_name]['siso'][2]

    def set_sub_lists_of_siso_index(self, sub_lists_of_siso_index, filename):
        del self.data_center[filename]['siso_cut'][0][:]
        self.data_center[filename]['siso_cut'][0] = sub_lists_of_siso_index

    def get_sub_lists_of_siso_index(self, filename):
        return self.data_center[filename]['siso_cut'][0]

    def set_sub_lists_of_siso(self, sub_lists_of_siso, filename):
        del self.data_center[filename]['siso_cut'][1][:]
        self.data_center[filename]['siso_cut'][1] = sub_lists_of_siso

    def get_sub_lists_of_siso(self, filename):
        return self.data_center[filename]['siso_cut'][1]

    """
    The methods to control the iso in the data center
    """

    def set_iso_parameter_name(self, name, filename):
        self.data_center[filename]['iso'][0] = name

    def set_iso_parameter_name_from_lom_file(self, name, label_name, filename):
        self.data_center[filename][label_name]['iso'][0] = name

    def get_iso_parameter_name(self, filename):
        return self.data_center[filename]['iso'][0]

    def get_iso_parameter_name_from_lom_file(self, label_name, filename):
        return self.data_center[filename][label_name]['iso'][0]

    def set_iso_parameter_values(self, iso_values, filename):
        self.data_center[filename]['iso'][1] = iso_values

    def set_iso_parameter_values_from_lom_file(self, iso_values, label_name, filename):
        self.data_center[filename][label_name]['iso'][1] = iso_values

    def set_iso_parameter_validity_from_lom_file(self, iso_validity, label_name, filename):
        self.data_center[filename][label_name]['iso'][2] = iso_validity

    def get_iso_parameter_values(self, filename):
        return self.data_center[filename]['iso'][1]

    def get_iso_parameter_values_from_lom_file(self, label_name, filename):
        return self.data_center[filename][label_name]['iso'][1]

    def get_iso_parameter_validity_from_lom_file(self, label_name, filename):
        return self.data_center[filename][label_name]['iso'][2]

    def set_sub_lists_of_iso_index(self, sub_lists_of_iso_index, filename):
        del self.data_center[filename]['iso_cut'][0][:]
        self.data_center[filename]['iso_cut'][0] = sub_lists_of_iso_index

    def get_sub_lists_of_iso_index(self, filename):
        return self.data_center[filename]['iso_cut'][0]

    def set_sub_lists_of_iso(self, sub_lists_of_iso, filename):
        del self.data_center[filename]['iso_cut'][1][:]
        self.data_center[filename]['iso_cut'][1] = sub_lists_of_iso

    def get_sub_lists_of_iso(self, filename):
        return self.data_center[filename]['iso_cut'][1]

    """
    The methods to control the abscissa axe in the data center
    """

    def set_abscissa_parameter_name(self, name, filename):
        self.data_center[filename]['abscissa'][0] = name

    def set_abscissa_parameter_name_from_lom_file(self, name, label_name, filename):
        self.data_center[filename][label_name]['abscissa'][0] = name

    def get_abscissa_parameter_name(self, filename):
        return self.data_center[filename]['abscissa'][0]

    def get_abscissa_parameter_name_from_lom_file(self, label_name, filename):
        return self.data_center[filename][label_name]['abscissa'][0]

    def set_abscissa_parameter_values(self, x_values, filename):
        if self.data_center[filename]['abscissa'][0] == 'GMT':
            for i in range(0, len(x_values)):
                self.data_center[filename]['abscissa'][1].append(i)
        else:
            self.data_center[filename]['abscissa'][1] = x_values

    def set_abscissa_parameter_values_from_lom_file(self, x_values, label_name, filename):
        if self.data_center[filename][label_name]['abscissa'][0] == 'GMT':
            for i in range(0, len(x_values)):
                self.data_center[filename][label_name]['abscissa'][1].append(i)
        else:
            self.data_center[filename][label_name]['abscissa'][1] = x_values

    def get_abscissa_parameter_values(self, filename):
        return self.data_center[filename]['abscissa'][1]

    def get_abscissa_parameter_values_from_lom_file(self, label_name, filename):
        return self.data_center[filename][label_name]['abscissa'][1]

    """
    The methods to control the ordinate axe in the data center
    """

    def set_list_of_ordinate_parameter_name(self, name, filename):
        self.data_center[filename]['ordinate'][0].append(name)

    def set_list_of_ordinate_parameter_name_from_lom_file(self, name, label_name, filename):
        self.data_center[filename][label_name]['ordinate'][0].append(name)

    def get_list_of_ordinate_parameter_name_at(self, index, filename):
        return self.data_center[filename]['ordinate'][0][index]

    def get_list_of_ordinate_parameter_name_at_from_lom_file(self, index, label_name, filename):
        return self.data_center[filename][label_name]['ordinate'][0][index]

    def get_list_of_ordinate_parameter_name(self, filename):
        return self.data_center[filename]['ordinate'][0]

    def get_list_of_ordinate_parameter_name_from_lom_file(self, label_name, filename):
        return self.data_center[filename][label_name]['ordinate'][0]

    def get_ordinate_parameter_values_by_name(self, filename):
        return self.data_center[filename]['ordinate'][1]

    def get_ordinate_parameter_values_by_name_from_lom_file(self, label_name, filename):
        return self.data_center[filename][label_name]['ordinate'][1]

    def set_list_of_ordinate_parameter_values(self, y_values, filename):
        self.data_center[filename]['ordinate'][1].append(y_values)

    def set_list_of_ordinate_parameter_values_from_lom_file(self, y_values, label_name, filename):
        self.data_center[filename][label_name]['ordinate'][1] = y_values

    def get_list_of_ordinate_parameter_values_at(self, index, filename):
        return self.data_center[filename]['ordinate'][1][index]

    def get_list_of_ordinate_parameter_values_at_from_lom_file(self, index, label_name, filename):
        return self.data_center[filename][label_name]['ordinate'][1][index]

    def get_list_of_ordinate_parameter_values(self, filename):
        return self.data_center[filename]['ordinate'][1]

    def get_list_of_ordinate_parameter_values_from_lom_file(self, label_name, filename):
        return self.data_center[filename][label_name]['ordinate'][1]

    def set_label_dimension_from_lom_file(self, dimension, label_name, filename):
        self.data_center[filename][label_name]['dimension'] = dimension

    def get_label_dimension_from_lom_file(self, label_name, filename):
        return self.data_center[filename][label_name]['dimension']