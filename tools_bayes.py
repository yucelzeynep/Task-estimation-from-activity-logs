#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 15:37:26 2019

@author: florianpgn
"""


import numpy as np

import tools_dic as dtools
from params import TASKS

import params
from importlib import reload
reload(params)

def get_prior_task(tasks):
    """
    This function returns the prior of all the tasks in an array. It simply counts 
    how many times the task is labeled and computes an expected value based on this. 
    Obviously, this is done using only the labeled lines.
    
    All priors are based on the same principle.
    """

    prior_task_single_label = dtools.init_dic(keys = tasks)

    for task in np.unique(tasks):
        prior_task_single_label[task] = np.sum(tasks == task)
    
    prior_task_single_label = dtools.normalize(prior_task_single_label)

    return prior_task_single_label


def get_p_keyst_given_task(tasks, keystrokes_quan, n_tot_keyst, unique_tasks=TASKS):
    """
    This function returns the conditional probability of observing keystrokes_quan 
    quantiles of keystrokes, given the task.
    
    Since we are trying to estimate the task, at this point it is still unkonwn 
    and therefore we compute the conditional probability for each possible value
    of task.
    """

    p_keyst_given_task = dtools.init_dic_matrix(unique_tasks, np.arange(n_tot_keyst))
    for task in unique_tasks:
        for i in range(n_tot_keyst):
            p_keyst_given_task[task][i] = np.sum(
                    np.logical_and(
                            keystrokes_quan == i, 
                            tasks == task)) 
            
        p_keyst_given_task[task] = dtools.normalize(p_keyst_given_task[task])
    

    return p_keyst_given_task

def get_p_lclicks_given_task(tasks, lclicks, n_clicks, unique_tasks=TASKS):
    """
    Get the conditional probability of observing lclicks many left clicks,
    given the task.
    
    For the same reason as above, we compute the conditional probability for 
    each possible value of task.
    """    

    p_lclicks_given_task = dtools.init_dic_matrix(unique_tasks, np.arange(n_clicks))
    for task in unique_tasks:
        for i in range(n_clicks):
            p_lclicks_given_task [task][i] = np.sum(
                    np.logical_and(
                            lclicks == i, 
                            tasks == task)) 
        p_lclicks_given_task [task] = dtools.normalize(p_lclicks_given_task [task])
    

    return p_lclicks_given_task 

def get_p_rclicks_given_task(tasks, rclicks, n_clicks, unique_tasks=TASKS):
    """
    Get the conditional probability of observing rclicks many right clicks,
    given the task.
    
    For the same reason as above, we compute the conditional probability for 
    each possible value of task.
    """        

    p_rclicks_given_task = dtools.init_dic_matrix(unique_tasks, np.arange(n_clicks))
    for task in unique_tasks:
        for i in range(n_clicks):
            p_rclicks_given_task [task][i] = np.sum(
                    np.logical_and(
                            rclicks == i, 
                            tasks == task)) 
        p_rclicks_given_task [task] = dtools.normalize(p_rclicks_given_task[task])
    

    return p_rclicks_given_task 





def get_p_exe_given_task(tasks, exes, exe_names, unique_tasks=TASKS):
    """
    This is 1D case relating application (i.e. exe) names. Namely, in case exe 
    name and window title are judged to be independent, we treat each of them 
    individualy (i.e. as 1D).
        
    Here, we get the conditional probability of observing the exe name, given 
    the task.
    
    For the same reason as above, we compute the conditional probability for 
    each possible value of task.
    """ 
    p_exe_given_task = dtools.init_dic_matrix(unique_tasks, exe_names)

    for e in exe_names:
        for task in unique_tasks:
            p_exe_given_task[task][e] = np.sum(
                    np.logical_and(
                            exes == e, 
                            tasks == task))

        p_exe_given_task[task] = dtools.normalize(p_exe_given_task[task])
    
    return p_exe_given_task 

def get_p_window_given_task(tasks, windows, window_names, unique_tasks=TASKS):
    """
    Similar to the above, 1D case relating window titles. This function is called 
    when exe name and window title are judged to be independent.
    
    Here, we get the conditional probability of observing the window title, given 
    the task.
    
    For the same reason as above, we compute the conditional probability for 
    each possible value of task.
    """ 

    p_window_given_task = dtools.init_dic_matrix(unique_tasks, window_names) # + class for unknown titles
    # first unknown titles and known tasks
    for task in unique_tasks:
        p_window_given_task[task][''] = np.sum(np.logical_and(
                windows == '',
                tasks == task))
    p_window_given_task[task] = dtools.normalize(p_window_given_task[task])

    # then known titles and known tasks
    for w in window_names:
        for task in unique_tasks:
            temp_window = windows == w

            temp_task = tasks == task
            
            p_window_given_task[task][w] = np.sum(np.logical_and(temp_window, temp_task)) 
        p_window_given_task[task] = dtools.normalize(p_window_given_task[task])

    return p_window_given_task

def get_p_exe_window_given_task(tasks, exes, exe_names, windows, window_names, unique_tasks=TASKS):
    """
    This replaces the twoabove functions, when exe name and window title are 
    judged to be dependent (i.e. the 2D case).
    
    Namely, if we are working on the joint probability of application name and 
    window title, we retrieve the conditional probability from the 2D matrix.
    
    Here, we compute the conditional probability of observing the combination 
    of exe name and window title, given the task.
    
    For the same reason as above, we compute the conditional probability for 
    each possible value of task.
    """ 
    
    p_exe_window_given_task = dict()
    for task in unique_tasks:
        p_exe_window_given_task[task] = dict()
        for exe in exe_names:
            p_exe_window_given_task[task][exe] = dict()
            for title in window_names:
                    p_exe_window_given_task[task][exe][title] = np.sum(
                        np.logical_and.reduce((
                                exes == exe, 
                                windows == title, 
                                tasks == task)))
        p_exe_window_given_task[task] = dtools.normalize2D(p_exe_window_given_task[task])
            
    return p_exe_window_given_task 

def get_p_duration_given_task(tasks, duration, unique_tasks=TASKS):
    """
    This function is very similar the 1D case relating exe name or window title. 
    
    Here, we get the conditional probability of observing the duration value, given 
    the task.
    
    For the same reason as above, we compute the conditional probability for 
    each possible value of task.
    """
    n_bins = len(np.unique(duration))
    p_duration_given_task = dtools.init_dic_matrix(unique_tasks, np.arange(n_bins))

    for task in unique_tasks:
        for i in range(n_bins+1):
            p_duration_given_task[task][i] = np.sum(
                    np.logical_and(
                            duration == i, 
                            tasks == task)) 
        p_duration_given_task[task] = dtools.normalize(p_duration_given_task[task])
    

    return p_duration_given_task

"""
Note that the three functions below essentially carry out the same operations:
    get_conditional_s1: is called at stage1
    get_conditional_s1: is called at stage-2
    get_conditional: is called when no hierrachical framework is considered or 
    at s1/s2 with adjusted arguments
    
There are only some minor differences between them, namely possible task outcomes
(see the last arguments)

"""

def get_conditional_s1(tasks, exes, windows, keystrokes_quan, lunch, duration, \
                       l_clicks, r_clicks, exe_names, window_names):
    
        return get_conditional(tasks, exes, windows, keystrokes_quan, lunch, duration, \
                        l_clicks, r_clicks, exe_names, window_names, 
                        unique_tasks=params.TASKS_S1)
        
def get_conditional_s2(tasks, exes, windows, keystrokes_quan, lunch, duration, \
                       l_clicks, r_clicks, exe_names, window_names):
    
        return get_conditional(tasks, exes, windows, keystrokes_quan, lunch, duration, \
                        l_clicks, r_clicks, exe_names, window_names, 
                        unique_tasks=params.TASKS_S2)

def get_conditional(tasks, exes, windows, keystrokes_quan, lunch, duration, \
                    l_clicks, r_clicks, exe_names, window_names, unique_tasks=params.TASKS):

    n_tot_keyst = len(np.unique(keystrokes_quan)) # 6 classes: 0~5
    n_clicks = len(np.unique(l_clicks))
    n_rclicks = len(np.unique(r_clicks))
    
    """
    For each desciptor get the conditional probability and enter it into the 
    dictionary variable
    """
    p_keyst_given_task = get_p_keyst_given_task(tasks, keystrokes_quan, n_tot_keyst, unique_tasks)
    p_duration_given_task = get_p_duration_given_task(tasks, duration, unique_tasks)
    p_lclicks_given_task = get_p_lclicks_given_task(tasks, l_clicks, n_clicks, \
                                                    unique_tasks)
    p_rclicks_given_task = get_p_rclicks_given_task(tasks, r_clicks, n_rclicks, \
                                                    unique_tasks)
    p_exe_window_given_task = get_p_exe_window_given_task(tasks,exes, exe_names, \
                                                          windows, window_names, unique_tasks)
    p_exe_given_task = get_p_exe_given_task(tasks, exes, exe_names, unique_tasks)
    p_window_given_task = get_p_window_given_task(tasks, windows, window_names, unique_tasks)
    """
    In the past I used to use the information whether hh:mm:ss is during lunch 
    break or not. but currently I do not use time of the day, but I only use the 
    duration of the action. Therefore, the below is skipped.
    """
    p_lunch_given_task = [] 
    #p_lunch_given_task = get_p_lunch_given_task(tasks, lunch, unique_tasks)

    conditionals = dict()
    conditionals[params.EXES] = p_exe_given_task
    conditionals[params.WINDOWS] = p_window_given_task
    conditionals[params.EXES_WINDOWS] = p_exe_window_given_task
    conditionals[params.KEYSTROKES] = p_keyst_given_task
    conditionals[params.LUNCHS] = p_lunch_given_task
    conditionals[params.DURATIONS] = p_duration_given_task
    conditionals[params.LCLICKS] = p_lclicks_given_task
    conditionals[params.RCLICKS] = p_rclicks_given_task
    
    return conditionals
