#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 13:44:02 2019

@author: florianpgn

This function implements the proposed Bayesian approach. It also runs in 
parallel the benchmark method such that a comparison between the two is provided.

Please see below for detailed explanation concerning each step.

Zeynep Yucel
2018 01 08
"""
 
import numpy as np

import time

from data_formatting import define_names
import tools_dic as dtools

import tools_file as ftools
import tools_bayes as btools
import tools_rule as rtools
import tools_presentation as ptools

from prettytable import PrettyTable

from importlib import reload
import params
reload(params)
      
def selectConditionals(descriptors, conditionals, sample_index, task, exes, windows):
    """
    Simply for running at once a bunch of functions relating the chosen 
    descriptors
    """
    selected_conditionals = []    
    
    if params.EXES in descriptors:
        selected_conditionals.append(
                conditionals[params.EXES][task][exes[sample_index]])
        
    if params.WINDOWS in descriptors:
        selected_conditionals.append(
                conditionals[params.WINDOWS][task][windows[sample_index]])
        
    if params.EXES_WINDOWS in descriptors:
        selected_conditionals.append(
                conditionals[params.EXES_WINDOWS][task][exes[sample_index]][windows[sample_index]])
        
    if params.KEYSTROKES in descriptors:
        selected_conditionals.append(
                conditionals[params.KEYSTROKES][task][keystrokes_quan[sample_index]])
        
    if params.DURATIONS in descriptors:
        selected_conditionals.append(
                conditionals[params.DURATIONS][task][duration[sample_index]])
        
    if params.LCLICKS in descriptors:
        selected_conditionals.append(
                conditionals[params.LCLICKS][task][l_clicks[sample_index]])
        
    return selected_conditionals

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
    
    """
    Initializations for the variables used in Bayesian estimation. Here, I basically
    create empty instances of some dictionary variables, arrays etc
    """
    #Copies for the two stages
    tasks_s1 = tasks.copy()
    tasks_s2 = tasks.copy()
    
    # In stage 1, we label everything but TEST and DOCUMENT with OTHER
    tasks_s1[np.invert(np.logical_or(tasks == params.TEST, tasks == params.DOCUMENT))] = params.OTHER
    
    # In stage 2, we select all the samples where the associated task is PROG, ADMIN or LEISURE
    boolean_matrix = (tasks == np.array(params.TASKS_S2)[:,None])
    others_query = boolean_matrix.any(axis=0) # Logical or between rows
    tasks_s2 = tasks[others_query]
    
        
    
    """
    We go on initializations but the below is not simply empty instances. I 
    compute the priors and the conditionals which will be used for estimating 
    the first action (and probably get updated from the second on).
    
    I first compute the priors and then conditional probabilities at stage-1 and 2.
    """
    prior_task_single_label_s1 = btools.get_prior_task(tasks_s1)
    prior_task_single_label_s2 = btools.get_prior_task(tasks_s2)
    
    
    conditionals_s1 = btools.get_conditional_s1(tasks_s1, exes, title_codes, \
                       keystrokes_quan, lunch, duration, l_clicks, \
                       r_clicks, exe_names, title_combinations)

    conditionals_s2 = btools.get_conditional_s2(tasks_s2, exes[others_query], \
                                      title_codes[others_query], \
                                      keystrokes_quan[others_query], \
                                      lunch[others_query], \
                                      duration[others_query], \
                                      l_clicks[others_query], \
                                      r_clicks[others_query], \
                                      exe_names, \
                                      title_combinations)
    """
    Initialization for the posteriors
    """
    n_actions = len(exes) #  or any other matrix
    likelihood = dtools.init_matrix(n_actions, params.TASKS_S1) # Actually, TASKS_S1 is not needed here, but it makes debug easier when looking at the data
    posterior = dtools.init_matrix(n_actions)
    
    
    """
    Initialize the estimation arrays.
    
    In est_by_rules_direct, I use use 1 column for line number,  4 columns for 
    estimations. But actually number of maximum estimations is no more than 3.
    This part is common with main_benchmark
    """
    est_by_rules_direct = []
    est_by_bayes_direct = []
    
    for i in range(n_actions):
        """
        We first go through the two stages of Bayesian estimation. The below is stage-1
        """
        for task in params.TASKS_S1:
            """
            Get prior and decide how you want to update 
            """
            if params.USE_DISTRIB_PROB:
                prior_task_single_label_s1 = dtools.init_dic(1/len(np.unique(params.TASKS_S1)), \
                                                             params.TASKS_S1)
            if i>1:
                prior_updated = dtools.add(dtools.mul(posterior[i-1], 1-params.ALPHA), \
                                                      dtools.mul(prior_task_single_label_s1, params.ALPHA))
            else:
                prior_updated = prior_task_single_label_s1
            
            """
            Get likelihood
            """
            selected_conditionals_s1 = selectConditionals(params.STAGE_1_DESCRIPTORS, \
                                                          conditionals_s1, i, task, \
                                                          exes, title_codes)
            likelihood[i][task] = btools.get_likelihood(selected_conditionals_s1)
            
            """
            Get posterior
            """
            posterior[i][task] = likelihood[i][task] * prior_updated[task]
    
        
        """
        Stage-2
        """
        if dtools.arg_max(posterior[i]) == params.OTHER:
            #posterior[i][params.TEST] = posterior[i][params.DOCUMENT] = 0
            for task in params.TASKS_S2:
                if params.USE_DISTRIB_PROB:
                    prior_task_single_label_s2 = dtools.init_dic(1/len(np.unique(params.TASKS_S2)), params.TASKS_S2)
                if i>1:
                    prior_updated = dtools.add(dtools.mul(posterior[i-1], 1-params.ALPHA), dtools.mul(prior_task_single_label_s2, params.ALPHA))
                else:
                    prior_updated = prior_task_single_label_s2
                    
                selected_conditionals_s2 = selectConditionals(params.STAGE_2_DESCRIPTORS, conditionals_s2, i, task, exes, title_codes)
                likelihood[i][task] = btools.get_likelihood(selected_conditionals_s2)
                
                posterior[i][task] = likelihood[i][task] * prior_updated[task]
        #print(posterior)
        posterior[i] = dtools.normalize(posterior[i])  # scale the posterior to achieve a cumulative of 1
        #p
        #
        #  of bayesian
        #
        ####################################
    
        ######################################
        #
        # estimation by bayes directly
        #s
        posterior_wo_other = {k:v for k,v in posterior[i].items() if k != params.OTHER}
        tsk = dtools.arg_max(posterior_wo_other)
        est_by_bayes_direct.append(tsk)
        
        ######################################
        #
        # estimation by applying the rules directly
        # 
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
    Analyze and compare the estimations obtained by the benchmark method and
    proposed method
    """
    # by direct application of rules
    print('==========================================')
    print('Applying the rules directly')
    nest_count = rtools.analyze_rule_based_estimations(tasks, est_by_rules_direct)
        
    # by direct application of belief propagation
    print('\n==========================================')
    print('Applying the belief propagation directly')
    nest_count = rtools.analyze_rule_based_estimations(tasks, est_by_bayes_direct)
    
        
    """
    Present the results in a nice and readable way
    """
    #Compute confusion matrix
    predicted_task = np.array(est_by_bayes_direct)
    unique_tasks = np.unique(tasks)
    n_tasks = len(unique_tasks)
    conf_mat = np.zeros((n_tasks, n_tasks))
    for i, task1 in enumerate(unique_tasks):
        for j, task2 in enumerate(unique_tasks):
            conf_mat[j,i] = np.nansum(np.logical_and(predicted_task == task1, tasks == task2))
    
    conf_mat_s = conf_mat #Save unscaled matrix
    conf_mat = conf_mat / np.nansum(conf_mat, axis=1)[:,None]
    
          
    #Display confusion matrix
    print('\n\t\t\tLabeled task ')
    ptools.printTable(unique_tasks, conf_mat)
    ptools.printTable(unique_tasks, conf_mat_s)
    
    precision = np.sum([conf_mat_s[i,i] for i in range(len(conf_mat_s))])/np.sum(conf_mat_s)
    print('Precision : {:.4f}'.format(precision))
    ########################################
    
    x = time.time() - start_time
    print('Time elapsed {} sec'.format(x))
