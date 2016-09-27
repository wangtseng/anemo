# ************************************************ -*- coding: utf-8 -*-
"""
Last updated on 06/01/2015

@author: Cheng WANG
"""


class AnalyserAction():

    def __init__(self, action_string):
        self.action_string = action_string

    def get_action_string(self):
        return self.action_string

    def action_string_parsing(self):
        print 'command_parsing'