#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 13:44:02 2019

@author: florianpgn

This function applies the association rules on the actions and estimates tasks. For
a detailed analysis and comparison with the proposed method, check main_bayes, 
which implements not only the Bayesian approach but also the benchmark method 
and provides comparison. 
"""
 
import numpy as np

import time

from data_formatting import define_names
import tools_dic as dtools

import tools_file as ftools
import tools_rule as rtools
import tools_presentation as ptools

from prettytable import PrettyTable

from importlib import reload
import params
reload(params)


if __name__ == "__main__":      
    
    start_time = time.time()
    
    """
    Load activity data and set the definitions
    """
    exes = ftools.load(params.PATH_EXE+params.DAT_FILE_PREFIX+params.EXE_MAT)
    windows = ftools.load(params.PATH_TITLE+params.DAT_FILE_PREFIX+params.TITLE_MAT)
    tasks = ftools.load(params.PATH_TASK+params.DAT_FILE_PREFIX+params.TASK_MAT)
    keystrokes_quan = ftools.load(params.PATH_KSTROKES+params.DAT_FILE_PREFIX+params.KSTROKE_MAT)
    lunch = ftools.load(params.PATH_LUNCH+params.DAT_FILE_PREFIX+params.LUNCH_MAT)
    l_clicks = ftools.load(params.PATH_CLICKS+params.NEW_DAT+params.LCLICK_MAT)
    r_clicks = ftools.load(params.PATH_CLICKS+params.NEW_DAT+params.RCLICK_MAT)
    duration = ftools.load(params.PATH_DURATION+params.NEW_DAT+params.DURATION_MAT)
    
    (exe_names, window_names, time_names, level_of_assoc) = dtools.define_names()
    
    title_combinations = np.unique([ftools.joinTitles(t) for t in windows])
    title_codes = np.array([ftools.joinTitles(t) for t in windows])
    
 
    n_actions = len(exes) #  or any other matrix

    
    """
    In est_by_rules_direct, I use use 1 column for line number,  4 columns for 
    estimations. But actually number of maximum estimations is no more than 3.
    """
    est_by_rules_direct = []
    
    for i in range(n_actions):

        """
        Estimation by applying the rules directly
        """ 
        (exe_only_rules, title_only_rules, exe_and_title_rules, exe_and_keyst_rules, exe_and_lunch_rules) = rtools.define_rules()
        est_task = np.array(rtools.apply_rules_to_action( exes[i], 
                                                  windows[i], 
                                                  keystrokes_quan[i], 
                                                  lunch[i],
                                                  exe_only_rules, 
                                                  title_only_rules, 
                                                  exe_and_title_rules, 
                                                  exe_and_keyst_rules, 
                                                  exe_and_lunch_rules), dtype='<U14')
    
        # Pad with unknowns
        pad = est_task.tolist().copy()
        pad += [params.UNKNOWN] * (params.N_MAX_EST-len(est_task))
        est_by_rules_direct.append(pad)
    
    
    """
    Analyze results obtained by the benchmark method
    """
    print('==========================================')
    print('Applying the rules directly')
    nest_count = rtools.analyze_rule_based_estimations(tasks, est_by_rules_direct)
    
    
    x = time.time() - start_time
    print('Time elapsed {} sec'.format(x))
