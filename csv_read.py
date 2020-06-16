# -*- coding: utf-8 -*-
"""
Created on Tue May 21 08:50:23 2019

@author: zeynep
"""
import numpy as np

from importlib import reload
from params import COL_NAMES

def readData(fname): 
    
    # Open file and read column names and data block 
    f = open(fname) 
    head = f.readline() # skip one line at the top
    data_block = f.readlines()  # read all following lines
    f.close() 
    
    # Create a data dictionary, containing 
    # a list of values for each variable 
    # Add an entry to the data dictionary for each column 
    datalog = {} 
    for col_name in COL_NAMES: 
        datalog[col_name] = []
    datalog['window_title'] = []
   
    # Loop through each value: append to each column 
    line_count = 0
    seperator = ';'
    for line in data_block: 
        
        items = line.split( seperator ) 

        if len( items ) is not len(COL_NAMES):
            print('Size mismatch: size is  {} instead of {} '.format(len( items ), len(COL_NAMES)))
            
        for n, item in enumerate(items):        
            # We need to split the 'exe_name" column in two different columns 
            if n == COL_NAMES.index('exe_name') :
                datalog['exe_name'].append( item.split(':', 1)[0])
                datalog['window_title'].append( item.split(':', 1)[1])
                
            else:
                datalog[ COL_NAMES[n] ].append( item.rstrip('\n') )
                

        line_count += 1
            
    return datalog 
