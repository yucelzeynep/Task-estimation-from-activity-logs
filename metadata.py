#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 10:44:06 2019

@author: zeynep

This function builds up the metadata reported in the section on 'Empirical 
distribution of descriptors' and also some part of the appendices. 
 
Specifically, we study the ground truth task distribution, and distribution of 
nominal descriptors in  the annotated subset and the entire data set. 
"""

import numpy as np

from importlib import reload
import params
reload(params)

from prettytable import PrettyTable

import tools_file as ftools
import tools_dic as dtools

if __name__ == "__main__":      

    (exe_names, window_names, time_names, level_of_assoc) = dtools.define_names()
    
    exe_code_mat = ftools.load(params.PATH_EXE + params.DAT_FILE_PREFIX + params.EXE_MAT)
    title_code_mat = ftools.load(params.PATH_TITLE + params.DAT_FILE_PREFIX + params.TITLE_MAT)
    task_code_mat = ftools.load(params.PATH_TASK + params.DAT_FILE_PREFIX + params.TASK_MAT)
    
    n_notask = np.sum(task_code_mat == 0)
    n_singletask = np.sum(task_code_mat != 0)
    
    n_total_lines = len(task_code_mat)
    r_notask = n_notask / n_total_lines
    r_singletask = n_singletask / n_total_lines
    
    
    """
    Distribution of principal tasks
    """
    count_task_principal = dtools.init_dic()
    
    for task in params.TASKS:
        count_task_principal[task] = np.sum(task_code_mat == task)# / sum(task_known_code_mat(:,1) != 0)
    
    
    prior_task_principal = dtools.normalize(count_task_principal)
    
    task_table = PrettyTable()
    task_table.field_names = ['Code', 'Name', 'Count', 'Ratio']
    print('******************************')
    print('Distibution of principal tasks')
    for i, task in enumerate(params.TASKS, 1):
        task_table.add_row([i, task, count_task_principal[task], round(prior_task_principal[task],3)])
    print(task_table)
    
    """
    exe with codes with 24 and above occur very seldom
    """
    unique_exes = np.unique(exe_code_mat)
    count_exe = dict()
    for e in unique_exes:
        count_exe[e] = np.sum(exe_code_mat == e)
    
    ordered = dtools.getOrderedKeys(count_exe)
    prior_exe = dtools.normalize(count_exe)
    
    print('\n******************************')
    print('Distibution of exe (only top-5)')
    exe_table = PrettyTable()
    exe_table.field_names = ['Name', 'Count', 'Ratio']
    for e in ordered[:5]: #size(exe_names,1)
        exe_table.add_row([e, count_exe[e], round(prior_exe[e],3)])
    print(exe_table)
    top5_ratio = np.sum([prior_exe[key] for key in ordered[:5]])
    print('Top-5 exe consitute {0:.03f} of the entire applications'.format(top5_ratio))
    
    """
    Distribution of title codes
    
    Note that I take all columns (1~4)
    Only cols 1 and 2 are nonzero, col 3 and 4 are all zeros (they are there just 
    in case)
    """
    unique_titles = np.unique(title_code_mat)
    unique_titles = unique_titles[unique_titles!='']
    count_title = dict()
    for t in unique_titles:
        count_title[t] = np.sum(title_code_mat == t)
    
    ordered = dtools.getOrderedKeys(count_title)
    prior_title = dtools.normalize(count_title)
    
    print('\n******************************')
    print('Distibution of window title (principal)')
    title_table = PrettyTable()
    title_table.field_names = ['Name', 'Count', 'Ratio']
    for t in ordered[:10]: #size(title_names,1)
            title_table.add_row([t, count_title[t], round(prior_title[t],3)])
    print(title_table)
    
    top10 = np.sum([prior_title[key] for key in ordered[:10]])
    print('Top-10 window titles consitute {0:.3f} of the entire applications'.format(top10))
    

    """
    The below file will be used in computng Cramer's V
    """
    ftools.save('count_exe_title_task',
             [list(count_task_principal.values()), list(count_exe.values()), list(count_title.values())],
             ['count_task_principal', 'count_exe', 'count_title'])
