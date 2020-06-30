#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 14:18:49 2019

@author: florianpgn

This file contains the necessary functions for implementing the benchmark method. 
Basically, they define the association rules and then apply them on the actions. 
It also contains a function for evaluating the performance of the benchmark 
method. 
"""
import numpy as np

import tools_file as ftools
from prettytable import PrettyTable

import sys
sys.path.insert(0,'../') 
import params 

def define_rules():
    exe_only_rules = np.array([
    ['tortoiseproc', params.TEST, params.PROG, params.UNKNOWN],
    ['airsovly', params.TEST, params.UNKNOWN, params.UNKNOWN],
    ['airspsam', params.TEST, params.UNKNOWN, params.UNKNOWN],
    ['aliim', params.LEISURE, params.UNKNOWN, params.UNKNOWN],
    ['bcompare', params.TEST, params.DOCUMENT, params.UNKNOWN],
    ['devenv', params.PROG, params.TEST, params.UNKNOWN],
    ['firefox', params.PROG, params.LEISURE, params.TEST],
    ['ipmsg', params.ADMIN, params.UNKNOWN, params.UNKNOWN],
    ['msimn', params.ADMIN, params.UNKNOWN, params.UNKNOWN],
    ['sakura',params.PROG, params.TEST, params.DOCUMENT],
    ['editplus',params.DOCUMENT, params.UNKNOWN, params.UNKNOWN],
    ['taskpit', params.ADMIN, params.UNKNOWN, params.UNKNOWN]])
    
    title_only_rules = np.array([
    ['Test', params.TEST, params.DOCUMENT, params.UNKNOWN],
    ['淘宝', params.LEISURE, params.UNKNOWN, params.UNKNOWN],
    ['taobao', params.LEISURE, params.UNKNOWN, params.UNKNOWN],
    ['服装', params.LEISURE, params.UNKNOWN, params.UNKNOWN],
    ['天猫', params.LEISURE, params.UNKNOWN, params.UNKNOWN],
    ['支付宝', params.LEISURE, params.UNKNOWN, params.UNKNOWN]])
    
    exe_and_title_rules = np.array([
    ['devenv', 'ファイル内の検索', params.PROG, params.UNKNOWN, params.UNKNOWN],
    ['sofficebin', '査読シート', params.LEISURE, params.DOCUMENT, params.UNKNOWN]])
    

    # First column is exe code, second is keystroke code, last is the estimated task
    exe_and_keyst_rules = np.array([['excel', 5, params.TEST], ['notepad', 5, params.TEST]])

    # First column is exe code, second is lunch break, last is the estimated task
    exe_and_lunch_rules = np.array(['firefox', params.PROG, params.LEISURE])
    
    #ftools.save('rules.dat',
    #     [exe_only_rules, title_only_rules, exe_and_title_rules, exe_and_lunch_rules],
    #     ['exe_only_rules', 'title_only_rules', 'exe_and_title_rules']);
    
    return (exe_only_rules, title_only_rules, exe_and_title_rules, exe_and_keyst_rules, exe_and_lunch_rules)
    


def apply_rules_to_action(exe, window, keyst, lunch, exe_only_rules, \
                          title_only_rules, exe_and_title_rules, \
                          exe_and_keyst_rules, exe_and_lunch_rules):
    """
    This function takes a single action: 
    an exe name, a window title, keystrokes and lunch time. 
    
    Then it applies the rules to this action and produces a set estimations.
    
    The rules are divided according to the terms they have in the antecedant. For
    instance,  exe-only-rules involve only exe name in antecedent, whereas 
    exe-and-title-rules have conditions on both exe and window title in the 
    antecedant.
    """

    """
    apply exe only rules
    """
    est_exe_only = exe_only_rules[exe_only_rules[:,0] == exe, 1:].flatten()

    """
    apply title-only-rules
    """
    title1 = window[0]
    title2 = window[1]
    est_window_only_for_title1 = title_only_rules[title_only_rules[:,0] == title1, 1:].flatten()
    est_window_only_for_title2 = title_only_rules[title_only_rules[:,0] == title2, 1:].flatten()
    
    """
    apply exe-and-title-rules
    """
    est_exe_and_title = exe_and_title_rules[
            np.logical_and(exe_and_title_rules[:,0] == exe, 
                    np.logical_or(
                            exe_and_title_rules[:,1] == title1, 
                            exe_and_title_rules[:,1] == title2)), 2:].flatten()

    """
    apply exe-and-keyst rules
    """
    est_exe_and_keyst = exe_and_keyst_rules[np.logical_and(
                    exe_and_keyst_rules[:,0] == exe,
                    np.array(list(map(int, exe_and_keyst_rules[:,1]))) == keyst), 2]
            
    """
    apply exe-and-lunch rules
    """
    est_exe_and_lunch = exe_and_lunch_rules[np.logical_and(
                    exe_and_lunch_rules[0] == exe,
                    exe_and_lunch_rules[1] == lunch), 2]

    
    """
    All estimations go into one variable
    """
    est_task = np.concatenate((est_exe_only,
                               est_window_only_for_title1,
                               est_window_only_for_title2,
                               est_exe_and_title,
                               est_exe_and_keyst,
                               est_exe_and_lunch))
    
    est_task = np.unique(est_task)[np.unique(est_task) != params.UNKNOWN]
    return list(est_task)


def analyze_rule_based_estimations(tasks, est):
    """
    This function gets a set of estimations and returns some stats like
    how many estimations are made, number of cases with no-estimation, 
    1-estimation, 2-estimation, 3-estimation ...  for each action (ie line)
    
    Also it returns the numbre of miss and fail of the estimations 
    
    Zeynep Yucel
    2018 01 08
    """
    est = np.array(est)
    if len(est.shape) == 1:
        est = est.reshape(len(est),1)

    n_max_est = len(est[0]) if len(est.shape) == 2 else 1  #nb columns
    nest_count = [] # starts by 0 est and goes to n_max_est

    # first actions with  no estimation 
    nest_count.append(np.sum(est[:,0] == params.UNKNOWN))
    
    n_exact_hit = 0 # one task assingned, one task estimated. exact hit
    n_possible_hit_single_label_two_est = 0 
    n_possible_hit_single_label_three_est = 0 

    n_miss = 0 # any of the estimated task does not match any of the assigned tasks

    # then estimations with 1 or more estimation
    for i in range(n_max_est):

        # first i columns are nonzero
        temp1 = np.ones(len(est))
        for j in range(i+1):
            temp1 *= (est[:,j] != params.UNKNOWN)
        
        # remaining columns are zero
        temp2 = np.ones(len(est))
        for j in range(i+1, n_max_est):
            temp2 *= (est[:,j] == params.UNKNOWN)
        
        # lines with i estimations
        temp = temp1 * temp2
        nest_count.append(np.sum(temp))

        if temp.size != 0:
            """
            Compute number of hit and miss
            
            There are two possible tasks assigned to this action. If I get one 
            of them correctly, I call it a possible hit
            
            I have finer counters to classify possible hit like 
            single_label_multi_est etc...
            """
            #tasks_true = np.array(tasks)[:2,temp == 1] #  there are at most 2 tasks assigned to asingle line
            tasks_true = tasks[temp == 1]
            tasks_estim = est[temp == 1, :i+1] # since there are i estimations

            for j in range(len(tasks_true)):

                if i == 0: # one assigned task and one estimation
                    #print(tasks_true[j], tasks_estim[j,0])
                    n_exact_hit = n_exact_hit + np.sum(tasks_true[j] == tasks_estim[j,0])
                    n_miss += np.sum(tasks_true[j] != tasks_estim[j,0])

                elif i == 1: # one assigned task but two estimations
                    hit = 0
                    for p in range(i+1):
                        hit += np.sum(tasks_true[j] != tasks_estim[j,p])  
                    
                    if hit > 0:
                        n_possible_hit_single_label_two_est += 1
                    else:
                        n_miss += 1
                    
                elif i == 2: # one assigned task but three estimations
                    hit = 0
                    for p in range(i+1):
                        hit += np.sum(tasks_true[j] == tasks_estim[j,p])
                    
                    if hit > 0:
                        n_possible_hit_single_label_three_est += 1
                    else:
                        n_miss += 1
                    
                    
             
    
    """
    Report on console
    """
    n_est_table = PrettyTable()
    n_est_table.field_names = ['Nb Est', 'Nb Inst', 'Nb Max Est']
    for i in range(n_max_est+1):
        n_est_table.add_row([i, nest_count[i], n_max_est])
    print(n_est_table)

    hit_table = PrettyTable()
    hit_table.field_names = ['Hit', 'Count']
    hit_table.add_row(['Exact hits', n_exact_hit])
    hit_table.add_row(['Possible hit: single label + two est', n_possible_hit_single_label_two_est])
    hit_table.add_row(['Possible hit: single label + three est', n_possible_hit_single_label_three_est])
    hit_table.add_row(['Miss', n_miss])
    print(hit_table)
    return nest_count 
