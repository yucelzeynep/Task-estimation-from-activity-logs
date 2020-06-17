#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 09:19:14 2019

@author: florianpgn

This function returns the prior of all combinations of exes names and window 
titles in a array.

"""

import numpy as np

import sys
sys.path.insert(0, '../') 

import dic_tools as dt
from params import TASKS

def get_p_exe_window_given_task(tasks, exes, exe_names, windows, window_names):
    
    p_exe_window_given_task = dict()
    for task in TASKS:
        p_exe_window_given_task[task] = dict()
        for exe in exe_names:
            p_exe_window_given_task[task][exe] = dict()
            for title in window_names:
                    p_exe_window_given_task[task][exe][title] = np.sum(
                        np.logical_and.reduce((
                                exes == exe, 
                                windows == title, 
                                tasks == task)))
        p_exe_window_given_task[task] = dt.normalize2D(p_exe_window_given_task[task])
            
    return p_exe_window_given_task 