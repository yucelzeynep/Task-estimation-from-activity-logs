#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 12:40:38 2019

@author: zeynep

This function returns the prior of all the exes in a array. It simply counts 
how many times the exe is called and computes an expected value based on this. 
This is done based on the labelled lines only.

All priors are based on the same principle.

Zeynep Yucel

"""

import numpy as np

import sys
sys.path.insert(0, '../') 

import dic_tools as dt
from params import TASKS

def get_p_exe_given_task(tasks, exes, exe_names, n_tot_task):

    p_exe_given_task = dt.init_dic_matrix(exe_names+[''])

    for e in exe_names:
        for task in TASKS:
            p_exe_given_task[e][task] = np.sum(
                    np.logical_and(
                            exes == e, 
                            tasks == task))
        p_exe_given_task[e] = dt.normalize(p_exe_given_task[e])
    
    return p_exe_given_task 
