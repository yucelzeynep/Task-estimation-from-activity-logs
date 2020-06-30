#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 14:23:21 2019

@author: florianpgn

This file includes some functions to display part of the results in a nice and
easy to understand manner. It also saves data points that we import into gnuplot 
for better quality figures.

In addition, it helps to produce some of the examples in the appendices.

"""
import numpy as np

import matplotlib.pyplot as plt
import matplotlib
import math
from prettytable import PrettyTable

from data_formatting import data_post_processing as post_pro
#import classifier_tools # load if necessary
import tools_file as ftools

from importlib import reload
import params
reload(params)   


def displayDurationDensities(datalog):
    plotFeatureDensities(datalog, 'duration')
        
def displayIdleDensities(datalog):
    plotFeatureDensities(datalog, 'idle_after_task', 0, 4000)
    
def displayKeystrokeDensities(datalog):
    plotFeatureDensities(datalog, 'n_keystrokes', 0, 4000)
    
def displayClickDensities(datalog):
    plotFeatureDensities(datalog, 'idle_after_task', 0, 4000)

def printTable(unique_tasks, conf_mat):
    """
    Display a confusion matrix
    """
    conf_table = PrettyTable()
    fields = unique_tasks.copy()
    fields = np.insert(fields, 0, 'Task')
    conf_table.field_names = fields
    for i, task in enumerate(unique_tasks):
        row = [round(conf_mat[i,j],3) for j in range(len(conf_mat))]
        row.insert(0, task)
        conf_table.add_row(row)
    print(conf_table)


def plotFeatureDensities(datalog, featureName, minValue = -math.inf, maxValue = math.inf):
    #Allow the use of Japanese character
    matplotlib.rc('font', family='TakaoPGothic')
    
    tasks_values = {}
    #Build a dictionary that contains each possible task and the associate feature values
    for task_name, feature in zip(datalog['hand_annotation'], datalog[featureName]):
        #Initialize a new array if we match a new task
        if task_name not in tasks_values:
            tasks_values[task_name] = []
        tasks_values[task_name].append(feature)
        
    nb_tasks = len(tasks_values.keys())
    nb_rows_max = math.ceil(nb_tasks/2)
    fig, subplots = plt.subplots(nb_rows_max, 2)
    
    #Plot a histogram distribution of the feature for each task
    for ax, (task_name, features) in zip(subplots.flatten(), tasks_values.items()):
        #We filter values that are inferior or equal to the min value.
        filtered_list = list(filter(lambda a: int(a)>minValue and int(a)<maxValue, features))
        if len(filtered_list) == 0:
            continue
                
        ax.set_title(task_name)
        ax.set_xlabel(featureName)
        ax.set_ylabel('Occurrences')
        #ax.set_yscale('log')
        #ax.set_xticks(np.arange(0, 60*len(filtered_list)+1, 60))
        ax.autoscale(enable=True, axis='both', tight=None)
        #kde.kde(np.reshape(filtered_list, (-1,1)), 100, ax)
        ax.hist(filtered_list, color = 'blue', edgecolor = 'black', bins = 15)
        hist, bins = np.histogram(filtered_list, bins=np.arange(1,np.max(filtered_list)))
        hist= hist / np.sum(hist)
        print(hist, bins)
        f = open(task_name+'_duration_pdf_both.txt', 'w')
        
        for i in range(len(bins)-1):
            f.write(str(bins[i])+'\t'+str(hist[i])+'\n')
        f.close()
        
    plt.show()


def example_q_quartiles():
    """
    This function serves to display an example of computing Q-quartiles. 
    
    Specifically, it is for reproducing the graph given in Appendix-I (Pre-processing
    of quantitaive variables). The below saves the data points into a file, which is
    later used in a gnu-plot script.
    """
    
    data = ftools.readData( params.ANNOTATION_FILE )
    data = post_pro.addDurationFeature( data ) # Just putting the data into a 'good' shape
    titles = ftools.load(params.PATH_TITLE[6:]+params.NEW_DAT+params.TITLE_MAT)
    data[params.WINDOW_STR] = [ftools.joinTitles(t) for t in titles]
    array = list(map(int, data[params.DURATION_STR]))
    
    y, x = np.histogram(array, bins=np.arange(np.max(array), step=1)+1) 
    x = x[:-1]
    y = np.cumsum(y)
    f = open('cdf_duration_dev.txt','w')
    for i in range(len(x)):
        f.write(str(x[i])+'\t'+str(y[i])+'\n')
    f.close()

def display_confmat_compare():
    """
    This function compares the estimated tasks through assoc rules (and relating post 
    proc) to the manual annotations and displays that nicely as a confusion
    matrix.
    
    In what follows, 
    auto refers to automatic annoattion (with the assoc rules and relating post-proc)
    hand refers to manual annotation
    """
    data = ftools.readData( params.ANNOTATION_FILE )
    data = post_pro.addDurationFeature( data ) # Just putting the data into a 'good' shape
    titles = ftools.load(params.PATH_TITLE[6:]+params.NEW_DAT+params.TITLE_MAT)
    data[params.WINDOW_STR] = [ftools.joinTitles(t) for t in titles]
    
    
    auto = np.array(data[params.AUTO_TASK_STR]) 
    hand = np.array(data[params.HAND_TASK_STR]) 
    unique_tasks = np.unique(hand)
    n_tasks = len(unique_tasks)
    conf_mat = np.zeros((n_tasks, n_tasks))
    for i, task1 in enumerate(unique_tasks):
        for j, task2 in enumerate(unique_tasks):    
            conf_mat[j,i] = np.nansum(np.logical_and(auto == task1, hand == task2))
    
    conf_mat_s = conf_mat #Save unscaled matrix
    conf_mat = conf_mat / np.nansum(conf_mat, axis=1)[:,None]
    
    corrects = np.sum([conf_mat_s[i,i] for i in range(len(conf_mat_s))])
    print('Correct ', corrects, corrects/np.sum(conf_mat_s))
    
    printTable(unique_tasks, conf_mat)
    printTable(unique_tasks, conf_mat_s)
    
    """
    classifier_tools.kNN(data)
    classifier_tools.randomForest(data)
    classifier_tools.svm(data)
    """

    displayDurationDensities(data)
