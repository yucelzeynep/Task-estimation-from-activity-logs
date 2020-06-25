#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 13:44:02 2019

@author: florianpgn

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


from prettytable import PrettyTable

from importlib import reload
import params
reload(params)

#Display a confusion matrix
def printTable(uniques_tasks, conf_mat):
    conf_table = PrettyTable()
    fields = uniques_tasks.copy()
    fields = np.insert(fields, 0, 'Task')
    conf_table.field_names = fields
    for i, task in enumerate(uniques_tasks):
        row = [round(conf_mat[i,j],3) for j in range(len(conf_mat))]
        row.insert(0, task)
        conf_table.add_row(row)
    print(conf_table)

def getLikelihood(conditionals):
    # likelihood is sometimes 0, if the exe occurs only once 
    # or window title is unknown
    # so I initilize likelihood to 1 and multiply with the conditional if it is not 0.
    # so I avoid making lielihood 0 and the posterior NaN 
    likelihood = 1
    for c in conditionals:
        likelihood *= c
    likelihood = round(likelihood, 4) # TO BE DELETED (here for readability in console)
    return likelihood
      
def selectConditionals(descriptors, conditionals, sample_index, task, exes, windows):
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
    
    
    ########################################
    #
    # load activity data and do definitions
    #
    exes = ftools.load(params.PATH_EXE+params.DAT_FILE_PREFIX+params.EXE_MAT)
    windows = ftools.load(params.PATH_TITLE+params.DAT_FILE_PREFIX+params.TITLE_MAT)
    tasks = ftools.load(params.PATH_TASK+params.DAT_FILE_PREFIX+params.TASK_MAT)
    keystrokes_quan = ftools.load(params.PATH_KSTROKES+params.DAT_FILE_PREFIX+params.KSTROKE_MAT)
    lunch = ftools.load(params.PATH_LUNCH+params.DAT_FILE_PREFIX+params.LUNCH_MAT)
    l_clicks = ftools.load(params.PATH_CLICKS+params.NEW_DAT+params.LCLICK_MAT)
    r_clicks = ftools.load(params.PATH_CLICKS+params.NEW_DAT+params.RCLICK_MAT)
    duration = ftools.load(params.PATH_DURATION+params.NEW_DAT+params.DURATION_MAT)
    
    (exe_names, window_names, time_names, level_of_assoc) = define_names()
    
    title_combinations = np.unique([ftools.joinTitles(t) for t in windows])
    title_codes = np.array([ftools.joinTitles(t) for t in windows])
    
    #Copies for stages
    tasks_s1 = tasks.copy()
    tasks_s2 = tasks.copy()
    # In stage 1 we label everything but TEST and DOCUMENT with OTHER
    tasks_s1[np.invert(np.logical_or(tasks == params.TEST, tasks == params.DOCUMENT))] = params.OTHER
    # In stage 2 we select all the samples where the associated task is PROG, ADMIN or LEISURE
    boolean_matrix = (tasks == np.array(params.TASKS_S2)[:,None])
    others_query = boolean_matrix.any(axis=0) # Logical or between rows
    tasks_s2 = tasks[others_query]
    
        
    
    ########################################
    # get priors and conditional probabilities
    #
    prior_task_single_label_s1 = btools.get_prior_task(tasks_s1)
    prior_task_single_label_s2 = btools.get_prior_task(tasks_s2)
    
    
    #Conditionals stage 1
    conditionals_s1 = btools.get_conditional_s1(tasks_s1, exes, title_codes, 
                       keystrokes_quan, lunch, duration, l_clicks, r_clicks, exe_names, title_combinations)
    #Conditionals stage 2
    conditionals_s2 = btools.get_conditional_s2(tasks_s2,
                                      exes[others_query], 
                                      title_codes[others_query], 
                                      keystrokes_quan[others_query],
                                      lunch[others_query], 
                                      duration[others_query],
                                      l_clicks[others_query],
                                      r_clicks[others_query],
                                      exe_names, 
                                      title_combinations)
    ########################################
    #
    # get posterior
    #
    n_actions = len(exes) #  or any other matrix
    likelihood = dtools.init_matrix(n_actions, params.TASKS_S1) #TASKS_S1 is not needed, but it makes debug easier when looking at the data
    posterior = dtools.init_matrix(n_actions)
    
    # 1 col for line number, rest for estimations,
    # 4 columsn for being safe
    # actually number of maximum estimations is 3
    est_by_rules_direct = []
    est_by_bayes_direct = []
    est_by_post_prob = []
    
    for i in range(n_actions):
        ######################################
        # bayesian estimation for this action
        #
        for task in params.TASKS_S1:
            ####################################
            # get prior
            #
            # decide how you want to update !!
            if params.USE_DISTRIB_PROB:
                prior_task_single_label_s1 = dtools.init_dic(1/len(np.unique(params.TASKS_S1)), params.TASKS_S1)
            if i>1:
                prior_updated = dtools.add(dtools.mul(posterior[i-1], 1-params.ALPHA), dtools.mul(prior_task_single_label_s1, params.ALPHA))
            else:
                prior_updated = prior_task_single_label_s1
            
            ####################################
            # get likelihood
            #
            selected_conditionals_s1 = selectConditionals(params.STAGE_1_DESCRIPTORS, conditionals_s1, i, task, exes, title_codes)
            likelihood[i][task] = getLikelihood(selected_conditionals_s1)
            
            ####################################
            # get posterior
            #
            posterior[i][task] = likelihood[i][task] * prior_updated[task]
    
        
        #Stage 2
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
                likelihood[i][task] = getLikelihood(selected_conditionals_s2)
                
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
    
        #Pad with unknows
        pad = est_task.tolist().copy()
        pad += [params.UNKNOWN] * (params.N_MAX_EST-len(est_task))
        est_by_rules_direct.append(pad)
    
        ######################################
        #
        # refine the estimation by bayesian approach
        #
        if len(est_task) == 1: # single estimation
            est_by_post_prob.append(est_task[0])   # app the only estimation 
    
        elif len(est_task) == 0:#no estimation
            # no estimation -> get the best decision out of posterior
            est_by_post_prob.append(tsk)
    
        elif len(est_task) > 1: #  multiple estimation
            # reduce the possibilites and get the highest from remaining
            temp = [posterior_wo_other[t] for t in est_task] # get only those probabilities to compare (initially estimated by the rules)
     
            ind = np.argmax(temp)
            est_by_post_prob.append(est_task[ind])
        else:
            print('Probably a bug!')
        
    
    ########################################
    #
    # analyze estimation
    #
    # by direct application of rules
    print('==========================================')
    print('Applying the rules directly')
    nest_count = rtools.analyze_rule_based_estimations(tasks, est_by_rules_direct)
    
    
    # by direct application of belief propagation
    print('\n==========================================')
    print('Applying the belief propagation directly')
    nest_count = rtools.analyze_rule_based_estimations(tasks, est_by_bayes_direct)
    
    
    # by refining with bayesian approach
    print('\n==========================================')
    print('After refining the initial estimation')
    nest_count = rtools.analyze_rule_based_estimations(tasks, est_by_post_prob)
    
        
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
    printTable(unique_tasks, conf_mat)
    printTable(unique_tasks, conf_mat_s)
    
    precision = np.sum([conf_mat_s[i,i] for i in range(len(conf_mat_s))])/np.sum(conf_mat_s)
    print('Precision : {:.4f}'.format(precision))
    ########################################
    #
    #x = time.time() - start_time
    #print('Time elapsed {} sec'.format(x))
