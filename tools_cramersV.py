#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 13:47:19 2019

@author: florianpgn

 LEVEL OF ASSOCIATION 	Verbal Description 	COMMENTS
 0.00                 	No Relationship    	Knowing the indepent variable does not help in predicting the depent variable.
.00 to .15            	Very Weak          	Not generally acceptable
.15 to .20            	 Weak              	Minimally acceptable
.20 to .25            	Moderate           	Acceptable
.25 to .30            	Moderately Strong  	Desirable
.30 to .35            	Strong             	Very Desirable
.35 to .40            	Very Strong        	Extremely Desirable
.40 to .50            	Worrisomely Strong 	Either an extremely good relationship or the two variables are measuring the same concept
.50 to .99            	Redundant          	The two variables are probably measuring the same concept.
1.00                  	Perfect Relationship.  	If we the know the indepent variable, we can perfectly predict the depent variable.  

from http:#groups.chass.utoronto.ca/pol242/Labs/LM-3A/LM-3A_content.htm

Zeynep Yucel
2017 12 18


"""

import math
import numpy as np

import tools_dic as dtools


def getIntArray(data):
    return np.array(list(map(int, data)))

def cramersV(crosstab):
    if isinstance(crosstab, dict):
        crosstab = np.array([[val for val in row.values()] for row in crosstab.values()])
    ni = len(crosstab)
    nj = len(crosstab[0])

    x_sq = 0

    for i in range(ni):
        for j in range(nj):
            temp1 = np.sum(crosstab[i]) * np.sum(crosstab, axis=0)[j] / np.sum(crosstab)
            num = (crosstab[i][j] - temp1)**2
            den = temp1

            if den !=0:
                x_sq = x_sq + num/den
            
    v = math.sqrt(x_sq / np.sum(crosstab) / min(ni-1, nj-1))

    return (x_sq, v)


def cramersV_bias_corrected(crosstab):
    if isinstance(crosstab, dict):
        crosstab = np.array([[val for val in row.values()] for row in crosstab.values()])
    ni = len(crosstab)
    nj = len(crosstab[0])

    x_sq = 0

    for i in range(ni):
        for j in range(nj):
            temp1 = sum(crosstab[i]) * crosstab.sum(axis=0)[j] / sum(sum(crosstab))
            num = (crosstab[i][j] - temp1)**2
            den = temp1

            if den !=0:
                x_sq = x_sq + num/den
            
    k_tilde = ni - (ni-1)*(ni-1)/sum(sum(crosstab))
    r_tilde = nj - (nj-1)*(nj-1)/sum(sum(crosstab))

    v = math.sqrt(x_sq / sum(sum(crosstab)) / min(k_tilde-1, r_tilde-1))
    return (x_sq, v)


def cramersV_test():
    """
    Some dummy test function
    """
    cont_table = np.array([[12,4,2,2],
                       [12,4,2,2],
                       [8,20,8,4],
                       [8,6,30,16],
                       [0,6,18,36]])

    (x,s) = cramersV_bias_corrected(cont_table)
    print(x, s)
    

def computeCramers(data1, dataName1, data2, dataName2):  
    """
    Correlation between data1 and data2 (in our case a task and a descriptor)
    
    cramersV is symmetric so, it does not matter which is first variable 
    (dimension) and which is second
    """
    d1 = np.unique(data1)
    d2 = np.unique(data2)
    crosstab = dtools.init_dic_matrix(d1, d2)
    for val1 in d1:
        for val2 in d2:
            crosstab[val1][val2] = np.sum(np.multiply(data1 == val1, data2 == val2))
    
    
    (x_sq, v) =  cramersV(crosstab)
    (x_sq_cor, v_cor) =  cramersV_bias_corrected(crosstab)
    
    print('******************************')
    print('Correlation between {} and {}\n'.format(dataName1, dataName2))
    print('Cramers V: {:.3f}'.format(v))
    print('Cramers V: {:.3f} (bias corrected)\n'.format(v_cor))


    