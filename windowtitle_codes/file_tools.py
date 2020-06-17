#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 31 13:00:40 2019

@author: florianpgn
"""
import numpy as np

def scanfMat(filename):
    f = open(filename, 'r')
    mat = []
    for line in f.readlines():
        mat.append(line.split())
    f.close()
    return np.asarray(mat, dtype=int)
        