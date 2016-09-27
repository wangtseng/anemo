"""
Last updated on 07/01/2015

@author: Cheng WANG,
"""

import ctypes


class RECT(ctypes.Structure):
    _fields_ = [('left', ctypes.c_int),
                ('top', ctypes.c_int),
                ('right', ctypes.c_int),
                ('bottom', ctypes.c_int)]