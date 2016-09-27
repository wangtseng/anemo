__author__ = 'TO113762'

import threading
import time
from SIREMI_LIB.srm_labels import *


class LOMFile:
    # this class represent all the titleNames and values in the file
    def __init__(self):
            self.fileName = ""
            self.fileType = ""
            self.filePath = ""
            self.labelNameList = list()
            self.labels = labels_()
            self.lom_file_parse_thread = threading.Thread(None, self.do_parse_lom_file)

    def parse_lom_file(self, filepath):
            self.filePath = filepath
            self.lom_file_parse_thread.start()
            self.lom_file_parse_thread.join()

    def get_filename(self):
            return self.fileName

    def set_filename(self, filename):
            self.fileName = filename

    def get_file_type(self):
            return self.fileType

    def set_file_type(self, file_type):
            self.fileType = file_type

    def get_labels(self):
            return self.labels

    def get_label_list(self):
            return self.labelNameList

    def set_label_list(self, label_list):
            self.labelNameList = label_list

    def write_label_into_the_file(self, label,label_name):
            self.labels.addlab(label, label_name)

    def do_parse_lom_file(self):
            start = time.time()
            self.labels.read(str(self.filePath),fmt='generic')
            self.set_label_list(self.labels.getnames())
            end = time.time()
            print "Time for completion",end-start