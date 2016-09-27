import threading
import time
import mmap
import numpy as np


class CSVFile:
    # this class represent all the titleNames and values in the file
    def __init__(self):
        self.fileName = ""
        self.fileType = ""
        self.filePath = ""
        self.rowCount = 0
        self.columnCount = 0
        self.titles = []
        self.values = []
        self.csv_file_parse_thread = threading.Thread(None, self.do_parse_csv_file)

    def parse_csv_file(self, filepath):
        self.filePath = filepath
        self.csv_file_parse_thread.start()
        self.csv_file_parse_thread.join()

    def get_filename(self):
        return self.fileName

    def set_filename(self, filename):
        self.fileName = filename

    def get_file_type(self):
        return self.fileType

    def set_file_type(self, file_type):
        self.fileType = file_type

    def get_values(self):
        return self.values

    def set_values(self, s):
        self.values = s

    def get_title_list(self):
        return self.titles

    def set_title_list(self, title_list):
        self.titles = title_list

    def get_row_count(self):
        return self.rowCount

    def set_row_count(self, row_count):
        self.rowCount = row_count

    def get_column_count(self):
        return self.columnCount

    def do_parse_csv_file(self):
        start = time.time()
        values = list()
        with open(self.filePath, "r+b") as f:
            # memory-mapInput the file, size 0 means whole file
            mapInput = mmap.mmap(f.fileno(), 0)
            # read content via standard file methods
            cpt = 0
            for s in iter(mapInput.readline, ""):
                s = s.translate(None, "\r\n")
                if cpt == 0:
                    title_list = s.split(";")
                    self.set_title_list(title_list)
                    print title_list
                else:
                    a_line_of_values = s.split(";")
                    values.append(a_line_of_values)
                cpt += 1

            self.set_values(values)
            self.set_row_count(len(values))
            mapInput.close()
            end = time.time()
            print "Time for completion",end-start