#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 14:49:00 2019

@author: florianpgn
"""
import numpy as np

import sys
sys.path.insert(0, '../') 
sys.path.insert(0, '../tools/') 
sys.path.insert(0, '../data_formatting/') 

from importlib import reload
import params
reload(params)

from file_tools import readData
import data_post_processing as post_pro
import classifier_tools
import file_tools as hft


def joinTitles(titles):
    return '/'.join(titles[:len(titles)-np.sum(titles=='')])


data = readData(params.ANNOTATION_FILE)
data = post_pro.addDurationFeature(data) # Just putting the data into a 'good' shape

"""
We try the classifiers in a hierrachical scheme (in the same manner as the 
proposed method) as well as in straight-forward non-hierrachical scheme. 

Note that in case we use the hiearchical approach, we need to adjust the 
dataset (i.e. labels)
                                    
"""
if not params.HIERARCHICAL:
    if params.STAGE == 1:
        """
        In stage-1 everything that is not Document or Test need to be renamed 
        as Others
        """
        for p in [params.HAND_TASK_STR, params.EST_1_STR, params.EST_2_STR, params.EST_3_STR]:
            data[p] = np.array(data[p])
            data[p][np.invert(np.logical_or(data[p] == params.TEST, data[p] == params.DOCUMENT))] = params.OTHER
    else:
        """
        In stage-2, we filter out the rows that are labelled DOCUMENT or TEST
        """
        boolean_matrix = (data[params.HAND_TASK_STR] == np.array(params.TASKS)[:,None])
        query_array = boolean_matrix.any(axis=0) # Logical or between rows
        for k in data.keys():
            data[k] = np.array(data[k])[query_array]


titles = hft.load(params.PATH_TITLE[6:]+params.DAT_FILE_PREFIX+params.TITLE_MAT)
data[params.WINDOW_STR] = [joinTitles(t) for t in titles]

classifier_tools.kNN(data, multi=False)
classifier_tools.randomForest(data, multi=False)
classifier_tools.svm(data, multi=False)
