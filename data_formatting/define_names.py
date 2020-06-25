#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 10:28:26 2019

@author: florianpgn
"""
import numpy as np


def sort_by_frequency(table):	
    """
    Returns the number of occurences of each exe	
    """
    arr, counts = np.unique(table, return_counts=True)	
    
    #Minus because we want to order in decreasing order (most occurences to less)	
    #Argsort so that it gives us the index of the exe which corresponds to the counter 	
    sorted_counts = np.argsort(-counts)	
    sorted_table = arr[sorted_counts]	
    return sorted_table

