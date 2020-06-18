#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 16:42:50 2019

@author: florianpgn

This file involves functions which (i) initialize instances of varying sorts of 
dictionary variables and (ii) which carry out trivial operations on those
"""
import numpy as np

import sys
sys.path.insert(0, '../') 

import params
from importlib import reload
reload(params)

from prettytable import PrettyTable

"""
Initializations
"""
def init_dic(value = 0, keys = params.TASKS):
    return {key: value for key in keys}

def init_matrix(nbSamples, keys = params.TASKS):
    return [init_dic(keys = keys) for i in range(nbSamples)]

def init_dic_matrix(keys1, keys2 = params.TASKS):
    return {k: init_dic(keys = keys2) for k in keys1}

"""
The below functions carry put some trivial arithmetic operations (+, *, /) over
dictionary variables 
"""
def add(dic1, dic2):
    return {key: dic1[key] + dic2[key] for key in dic1.keys() & dic2.keys()}

def mul(dic, factor):
    return {key: value * factor for (key,value) in dic.items()}

def div(dic, factor):
    return {key: value / factor for (key,value) in dic.items()}



"""
Other trivial functions for getting argmax and normalization in 1D and 2D
for dictionary variables
"""
def arg_max(dic):
    if type(dic) == list:
        return np.array([arg_max(d) for d in dic])
    return max(dic, key=dic.get)
    
def normalize(dic):
    den = sum(dic.values())
    if den == 0: return mul(dic, 0)
    factor = 1 / den
    return mul(dic, factor)

def normalize2D(dic):
    den = np.sum(np.array([value for sub_dic in dic.values() for value in sub_dic.values()] ).flatten())
    print(den)
    if den == 0: return {key: mul(sub_dic, 0) for (key, sub_dic) in dic.items()}
    factor = 1 / den
    return {key: mul(sub_dic, factor) for (key, sub_dic) in dic.items()}



def getOrderedKeys(dic):
    """
    Return a list of keys ordered by their value
    """
    return [kv[0] for kv in sorted(dic.items(), key=lambda kv: kv[1], reverse=True)]

def taskToID(task):
    """
    Maps the task string to task code
    """
    if task == params.UNKNOWN:
        return 0
    if task == params.PROG:
        return 1
    if task == params.TEST:
        return 2
    if task == params.ADMIN:
        return 3
    if task == params.LEISURE:
        return 4
    if task == params.DOCUMENT:
        return 5
    
def iDToTask(task):
    """
    Maps the task code to task string
    """
    if task == 0:
        return params.UNKNOWN
    if task == 1:
        return params.PROG
    if task == 2:
        return params.TEST
    if task == 3:
        return params.ADMIN
    if task == 4:
        return params.LEISURE
    if task == 5:
        return params.DOCUMENT
    
def getTaskTable(title, dic):
    """
    Builds the confusion table
    """
    conf_table = PrettyTable()
    fields = params.TASKS.copy()
    fields.insert(0,title)
    conf_table.field_names = fields
    for key in dic.keys():
        row = [round(dic[key][task],3) for task in params.TASKS]
        row.insert(0, key)
        conf_table.add_row(row)
    return conf_table
