#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 09:50:46 2019

@author: florianpgn

This function computes the Q-quartiles from the cdf. In what follows, 
Q is nb_bins. Note that if number of data points is not enough, than 
the cdf may not be binned into that particular nb_bins. 
"""

import numpy as np
import sys
import random
import matplotlib.pyplot as plt

# This was originally in params but I moved it out, after structirng the folders
# Set it locally
# In computing quartiles, you may choose to remove or not the offset
# Does not have much significance
REMOVE_OFFSET = False

def get_quartiles(data, nb_bins, dispay_graph = True):
    data = np.array(data)
    data_quan  = np.zeros(len(data))
    
    """
    Filter out values of 0, since they will have a devoted a bin
    """
    data_without_0 = data[data!=0]
    
    hist, bin_edges = np.histogram(data_without_0, 
                                   bins=np.arange(np.max(data_without_0), 
                                                  step=1)+1)
    
    cdf = np.cumsum(hist)
    
    """
    You may remove offset because it may make things simpler for getting the 
    intercepts
    """
    offset_value = 0
    if REMOVE_OFFSET:
        offset_value = cdf[0]
        cdf = cdf - cdf[0]
    
    if dispay_graph:
        plt.bar(bin_edges[:-1], hist, width=1)
        plt.step(bin_edges[1:], cdf)
    
    """
    Here, we bin the cdf into nb_bins and retrieve the cut-offs
    
    Careful that the cdf does not necessarily have a data point at every bin 
    edge. In that case, we return the index of the data point with the smallest
    distance to bin edge. 
    """
    step_size = np.max(cdf) / nb_bins
    th = [0]
    for i in range(1, nb_bins):
        ind = np.argmin( abs(np.subtract(cdf, i*step_size) ) ) 
        th.append( ind + 1 ) 
        print('{}th bin starts at {}'.format(i, ind))
    th.append( np.Infinity )    
    
    """
    Redundant but add back the offset just in case.
    """
    cdf += offset_value
    
    """
    If number of data points is not enough, than the cdf may not be binned 
    into that particular nb_bins
    """
    if len(np.unique(th)) < len(th):
        print('Cannot compute Q quartiles into {}'.format(nb_bins))        
        sys.exit()

    """
    Some random colors just to make things pretty
    """
    color_options = ['r', 'm', 'c', 'y', 'b', 'g']
    color = random.choice(color_options)
    for i in range(1, len(th)):
        lower_bound = th[i-1]
        upper_bound = th[i]
        
        if dispay_graph:
            plt.axvline(x=upper_bound,linewidth=1, color=color)
        
        print('Interval n°{}: [{}, {}['.format(i, lower_bound, upper_bound))
        data_quan[ np.logical_and(lower_bound < data, data <= upper_bound) ] = i 
     
    if not 0 in data_quan:
        data_quan-= 1
    
    print('Thresholds :', th)
    classes, counts = np.unique(data_quan, return_counts=True)
    print('Bin numbers :', classes, 'Counts :', counts)
    print()
    
    return data_quan
