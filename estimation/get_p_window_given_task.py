#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 12:35:16 2019

@author: zeynep

This function returns the conditional probability of observing a window title. 
The value comes from the empirical distribution. 

It simply counts how many times a window title is observed with a given (i.e. 
labeled) task and computes an expected value based on this.

The window title has 4 columns (just in case) because sometimes a window title 
has a few matches (never up to 4)
 
And the tasks has 2 columns. 

Both window title and task may be unknown. So it is hard to debug by only 
counting. I do it the long way not to make mistakes. 

Be careful tha the window title code and the prior array index are not the same. 
The first entry is for unknown title so it shifts by 1. 

"""

import numpy as np

import sys
sys.path.insert(0, '../') 

import dic_tools as dt
from params import TASKS

def get_p_window_given_task(tasks, windows, window_names, n_tot_task):

    p_window_given_task = dt.init_dic_matrix(window_names+['']) # + class for unknown
    print(windows)
    # first unknown titles and known tasks
    for task in TASKS:
        p_window_given_task[''][task] = np.sum(np.logical_and(
                windows == '',
                tasks == task))
    p_window_given_task[''] = dt.normalize(p_window_given_task[''])

    # then known titles and known tasks
    for w in window_names:
        for task in TASKS:
            temp_window = windows == w

            temp_task = tasks == task
            
            p_window_given_task[w][task] = np.sum(np.logical_and(temp_window, temp_task)) 
        p_window_given_task[w] = dt.normalize(p_window_given_task[w])

    return p_window_given_task