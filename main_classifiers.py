#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 14:49:00 2019

@author: florianpgn
"""
import numpy as np

from importlib import reload
import params
reload(params)

import data_formatting.data_post_processing as post_pro
import tools_classifier as ctools
import tools_file as ftools

if __name__ == "__main__":      

    data = ftools.readData(params.ANNOTATION_FILE)
    data = post_pro.addDurationFeature(data) # Just putting the data into a 'good' shape
    
    """
    We try the classifiers in a hierarchical scheme (in the same manner as the 
    proposed method) as well as in straight-forward non-hierarchical scheme. 
    
    Note that in case we use the hierarchical approach, we need to adjust the 
    dataset (i.e. labels)
                                        
    """
    if not params.HIERARCHICAL:
        if params.STAGE == 1:
            """
            At stage-1, anything that is not Document or Test, needs to be renamed 
            as Others
            """
            for p in [params.HAND_TASK_STR, params.EST_1_STR, \
                      params.EST_2_STR, params.EST_3_STR]:
                
                data[p] = np.array(data[p])
                
                data[p][np.invert(np.logical_or(data[p] == params.TEST, \
                     data[p] == params.DOCUMENT))] = params.OTHER
        else:
            """
            At stage-2, we filter out the rows that are labeled Document or Test
            and consider only the others
            """
            boolean_matrix = (data[params.HAND_TASK_STR] == np.array(params.TASKS)[:,None])
            query_array = boolean_matrix.any(axis=0) # Logical or between rows
            for k in data.keys():
                data[k] = np.array(data[k])[query_array]
    
    
    titles = ftools.load(params.PATH_TITLE+params.DAT_FILE_PREFIX+params.TITLE_MAT)
    data[params.WINDOW_STR] = [ftools.joinTitles(t) for t in titles]
    
    ctools.kNN(data, multi=False)
    ctools.randomForest(data, multi=False)
    ctools.svm(data, multi=False)
