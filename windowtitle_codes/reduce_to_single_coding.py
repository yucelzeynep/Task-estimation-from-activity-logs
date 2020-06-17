#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 31 11:27:06 2019

@author: florianpgn
////////////////////////////////////////////////////////////////////////////////
// I used to code a title like AIRS_PSAM with two codes such that
// 11  AIRS_PSAM 
// 27  AIRS
// This function reduces such multiple-codings to a single coding
//
// Note thatit does not eliminate all multiple-codings
// There still other lines which have multiple codes.
//
// Zeynep Yucel
// 2017 12 26
//
////////////////////////////////////////////////////////////////////////////////
"""
    
import h5py_file_tool as hft
from params import DAT_FILE_PREFIX, TITLE_MAT

title_code_mat = hft.load(DAT_FILE_PREFIX+TITLE_MAT)

counter0 = 0
counter1 = 0
counter2 = 0
counter3 = 0

out = title_code_mat.copy()

for i in range(len(title_code_mat)):
    if (title_code_mat[i,0:2] == ['AIRS_PSAM', 'AIRS']).all():
        out[i,0:2] = ['AIRS_PSAM', ''];
        counter1 += 1
    elif (title_code_mat[i,0:2] == ['百度搜索', '搜索']).all():
        out[i,0:2] = ['百度搜索', ''];
        counter2 = counter2 + 1
    elif (title_code_mat[i,0:2] == ['調査報告書', '報告書']).all():
        out[i,0:2] = ['調査報告書', ''];
        counter3 = counter3 + 1
    else:
        counter0 = counter0 + 1

title_code_mat = [[t.encode('utf-8') for t in line] for line in out]
hft.save(DAT_FILE_PREFIX+TITLE_MAT, [title_code_mat], [TITLE_MAT])    