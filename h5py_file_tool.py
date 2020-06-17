#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 10:57:20 2019

@author: florianpgn
"""
import h5py
import numpy as np

def decode(value):
    if isinstance(value, np.ndarray):
        return [decode(x) for x in value]
    return value.decode('utf-8') if isinstance(value, bytes) else value

def load(filename):
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
    with h5py.File(filename+'.dat', 'w') as f:
        for index, name in enumerate(datasetNames):
            f.create_dataset(name, data=[dataset[index]])
