# -*- coding: utf-8 -*-
"""
Created on Tue May 21 08:50:23 2019

@author: zeynep

This file contains some functions necessary for carrying out file operations. 
Mainly, for reading dta in correct format, decoding, and saving.
"""
import numpy as np

from importlib import reload
from params import COL_NAMES

import h5py

def scanfMat(filename):
    """
    Build a np.array variable from a file
    """
    f = open(filename, 'r')
    mat = []
    for line in f.readlines():
        mat.append(line.split())
    f.close()
    return np.asarray(mat, dtype=int)

def joinTitles(titles):
    """
    Join title strings
    """
    return '/'.join(titles[:len(titles)-np.sum(titles=='')])

def readData(fname): 
    """
    This function reads the raw log of the TaskPit, which is a csv file, and 
    builds a variable that can be processed.
    """
    
    # Open file and read column names and data block 
    f = open(fname) 
    head = f.readline() # skip one line at the top
    data_block = f.readlines()  # read all following lines
    f.close() 
    
    """
    Create a data dictionary, containing a list of values for each variable.
    Add an entry to the data dictionary for each column 
    """
    datalog = {} 
    for col_name in COL_NAMES: 
        datalog[col_name] = []
    datalog['window_title'] = []
   
    """
    Loop through each value and append to each respective column 
    """
    line_count = 0
    seperator = ';'
    for line in data_block: 
        
        items = line.split( seperator ) 

        if len( items ) is not len(COL_NAMES):
            print('Size mismatch: size is  {} instead of {} '.format(len( items ), len(COL_NAMES)))
            
        for n, item in enumerate(items):        
            """
            We need to split the 'exe_name" column into two different columns. 
            Because TaskPit registers the exe name and the window title into the
            same column
            """
            if n == COL_NAMES.index('exe_name') :
                datalog['exe_name'].append( item.split(':', 1)[0])
                datalog['window_title'].append( item.split(':', 1)[1])
                
            else:
                datalog[ COL_NAMES[n] ].append( item.rstrip('\n') )
                
        line_count += 1
            
    return datalog 

def decode(value):
    if isinstance(value, np.ndarray):
        return [decode(x) for x in value]
    return value.decode('utf-8') if isinstance(value, bytes) else value

def load(filename):
    """
    This function deals with different file formats, encodings. 
    """
    f = h5py.File(filename+'.dat', 'r')

    """
    If there is only one matrix we directly return it
    """
    if len(f.keys()) == 1 :
        array_name = list(f.keys())[0]
        arr = list(f[array_name])[0]
        f.close()
        decoded_list = decode(arr)
        return np.array(decoded_list)
    else:
        data = []
        # List all groups
        for array_name in  f.keys():
            # Get the data
            decoded_list = [x.decode('utf-16') if isinstance(x, bytes) else x for x in list(f[array_name])[0]]
            
            #map(lambda x: x.decode('UTF-8'), list(f[array_name])[0])
            data.append(decoded_list)
        f.close()
        return tuple(data)
    
def save(filename, dataset, datasetNames):
    """
    Finally create the data set (ready to be processed) and save it
    """
    with h5py.File(filename+'.dat', 'w') as f:
        for index, name in enumerate(datasetNames):
            f.create_dataset(name, data=[dataset[index]])
