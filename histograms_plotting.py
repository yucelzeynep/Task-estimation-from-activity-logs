#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 14:23:21 2019

@author: florianpgn
"""
import numpy as np

from prettytable import PrettyTable

from csv_read import readData
import data_post_processing as post_pro
import task_classification
import h5py_file_tool as hft
import distribution_visualizer

from importlib import reload
import params
reload(params)   

def joinTitles(titles):
    return '/'.join(titles[:len(titles)-np.sum(titles=='')])


def printTable(uniques_tasks, conf_mat):
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




"""
Actually, the below is not part of the analysis. It rather serves to display an 
example of computing the Q-quartiles. 

Specifically, it is for reproducing the graph given in Appendix-I (Pre-processing
of quantitaive variables). The below saves the data points into a file, which is
later used in a gnu-plot script.
"""

data = readData( params.ANNOTATION_FILE )
data = post_pro.addDurationFeature( data ) # Just putting the data into a 'good' shape
titles = hft.load(params.PATH_TITLE[6:]+params.NEW_DAT+params.TITLE_MAT)
data[params.WINDOW_STR] = [joinTitles(t) for t in titles]
array = list(map(int, data[params.DURATION_STR]))

y, x = np.histogram(array, bins=np.arange(np.max(array), step=1)+1) 
x = x[:-1]
y = np.cumsum(y)
f = open('cdf_duration_dev.txt','w')
for i in range(len(x)):
    f.write(str(x[i])+'\t'+str(y[i])+'\n')
f.close()

"""
This part compares the estimated tasks through assoc rules (and relating post 
proc) to the manual annotations and displays the confusion matrix.

auto refers to automatic annoattion (with the assoc rules and relating post-proc)
hand refers to manual annotation
"""
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
task_classification.kNN(data)
task_classification.randomForest(data)
task_classification.svm(data)
"""

distribution_visualizer.displayDurationDensities(data)
