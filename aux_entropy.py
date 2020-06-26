#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 21 08:50:23 2019

@author: zeynep

This function computes the normalized entropy distance between each pair of 
descriptors. The decision on being whether depedent or not is made in an 
empirical manner.

Since this decision can be carried out prior to the estimation and the relating 
settings in the parameters file can be adjusted accordingly, we realize it in
an offline manner.
"""
import numpy as np

import params
from importlib import reload
reload(params)

from matplotlib import pyplot as plt

import tools_file as ftools
import tools_entropy as etools
import tools_dic as dtools

if __name__ == "__main__":
    
    """
    Load all data
    """
    exes =  ftools.load( params.PATH_EXE + params.DAT_FILE_PREFIX + params.EXE_MAT)
    titles =  ftools.load( params.PATH_TITLE + params.DAT_FILE_PREFIX + params.TITLE_MAT)
    tasks =  ftools.load( params.PATH_TASK + params.DAT_FILE_PREFIX + params.TASK_MAT)
    keystrokes_quan =  ftools.load( params.PATH_KSTROKES + params.DAT_FILE_PREFIX + params.KSTROKE_MAT)
    lunchs =  ftools.load( params.PATH_LUNCH + params.DAT_FILE_PREFIX + params.LUNCH_MAT)
    l_clicks =  ftools.load( params.PATH_CLICKS + params.NEW_DAT + params.LCLICK_MAT)
    r_clicks =  ftools.load( params.PATH_CLICKS + params.NEW_DAT + params.RCLICK_MAT)
    duration =  ftools.load( params.PATH_DURATION + params.NEW_DAT + params.DURATION_MAT)
    
    exe_names, window_titles = dtools.define_names()[:2]
    window_titles.insert(0,'') # for alien titles, i.e. not a known title
    
    
    """
    One hot encoding for exes and window titles
    """
    exe_codes = [exe_names.index(e) + 1 for e in exes] # + 1 because I don't want exes with ID code 0
    
    title_combination = np.unique([ftools.joinTitles(t) for t in titles]).tolist()
    title_codes = [title_combination.index(ftools.joinTitles(t)) for t in titles]
    descriptors = [exe_codes, title_codes, keystrokes_quan, \
                   l_clicks, r_clicks, duration] # eventually we omit lunch time info
    
    descriptors_names = ['exes', 'titles', 'keystrokes', 'Left clicks', \
                         'Right clicks', 'Duration'] # Only for printing purposes
    jointProbs = []
    for i in range(len(descriptors)-1):
        for j in range(i + 1, len(descriptors)):
            desc1 = descriptors [i]
            desc2 = descriptors [j]
            q1 = etools.compute_histogram(desc1)
            q2 = etools.compute_histogram(desc2)
            jointProb = etools.compute_joint_pdf(etools.compute_joint_histogram(desc1, desc2))
            jointProbs.append(jointProb)
            mutInf = etools.get_mutual_inf(jointProb, q1, q2)
            jointEnt = etools.get_joint_ent(jointProb, q1, q2)
            
            print(descriptors_names[i], '&', descriptors_names[j])
            print('Mutual information {:.3f}'.format(etools.get_mutual_inf(jointProb, q1, q2)))
            print('Joint entropy {:.3f}'.format(etools.get_joint_ent(jointProb, q1, q2)))
            print('Relative entropy distance {:.3f}'.format(1-mutInf/jointEnt))
            print()
            
    plt.imshow(jointProbs[0])