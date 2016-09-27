# ************************************************ -*- coding: utf-8 -*-
"""
Last updated on 06/01/2015

@author: Cheng WANG
"""

import os
import time
from AnalyserAction import AnalyserAction


class AnalyserActions():

    def __init__(self):
        self.actions = list()

    def add_an_action(self, action_string):
        self.actions.append(str(action_string))

    def get_actions(self):
        return self.actions

    def pop_last_action(self):
        self.actions.pop()

    def write(self, path):
        username = os.environ['USERNAME']
        current_time = time.strftime("__%H.%M.%S")
        current_date = time.strftime("__%d.%m.%Y")
        path_to_save = path + username + current_time + current_date + '.txt'

        file = open(path_to_save, "w")
        for act in self.actions:
            file.write(act + '\n')
        file.close()