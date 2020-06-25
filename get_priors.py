#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 17:36:02 2020

@author: zeynep
"""

import numpy as np

import sys
sys.path.insert(0, '../') 
sys.path.insert(0, '../tools/') 

import dic_tools as dt

from importlib import reload
import params
reload(params)

def get_prior_task(tasks):

    prior_task_single_label = dt.init_dic(keys = tasks)

    for task in np.unique(tasks):
        prior_task_single_label[task] = np.sum(tasks == task)
    
    prior_task_single_label = dt.normalize(prior_task_single_label)

    return prior_task_single_label
