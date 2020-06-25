#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 10:57:16 2019

@author: florianpgn

This file contains the functions to compute relative entropy distance so as to 
judge in/dependence. 

computing mutual information and joint entropy are the essential steps and there
are also some other trivial functions to for computing the 1D/2D histograms etc. 
"""
import numpy as np

def getDataHistParams(data):
    return np.min(data), np.max(data)+1, 1

def compute_joint_histogram(data1, data2):
    """
    Returns the 2D histogram
    """
    (min_bound, max_bound, bin_size) = getDataHistParams(data1)
    n_bins = int(round((max_bound - min_bound) / bin_size) + 1)
    edges1 = np.linspace(min_bound, max_bound, n_bins)

    (min_bound, max_bound, bin_size) = getDataHistParams(data2)
    n_bins = int(round((max_bound - min_bound) / bin_size) + 1)
    edges2 = np.linspace(min_bound, max_bound, n_bins)
     
    histogram2D, edges1, edges2 = np.histogram2d(data1, data2, 
                                                  bins=(edges1, edges2))

    return histogram2D

def compute_histogram(data):
    """
    Returns 1d histogram
    """
    (min_bound, max_bound, bin_size) = getDataHistParams(data)
    n_bins = int(round((max_bound - min_bound) / bin_size) + 1)
    edges = np.linspace(min_bound, max_bound, n_bins)

    histogram, edges = np.histogram(data, bins=edges)

    return histogram

def compute_joint_pdf(histogram2D):
     """
     Here I do not scale with bin size, but with the sum of entries of the array.
     
     In that sense, it is not a real pdf. Because the pdf has to have the area 
     under the curve equal to 1. 
     """
    
     pdf_joint = histogram2D / np.sum(histogram2D)
     return pdf_joint

def get_mutual_inf(jointProb, q1, q2):
     """
     jointProb is the joint probability distribution. By definition, it is a pdf 
     but I need to scale it to 1, otherwise bin size is not accounted.
          
     q1 and q2 are the individual distributions of the two variables. Similarly, 
     they are scaled to 1.
     """
     q1 = q1 / np.sum(q1)
     q2 = q2 / np.sum(q2)
     mutual_inf = 0
     for i in range(0, len(q1)):
         for j in range(0, len(q2)):
             # only when all values are nonzero
             if 0 not in np.array([ jointProb[i,j], q1[i], q2[j] ]):
                 mutual_inf += jointProb[i,j]*np.log(jointProb[i,j] / q1[i] / q2[j])
     return mutual_inf


def get_joint_ent(jointProb, q1, q2):
     """
     Takes only joint pdf. Scaled to 1 as above.
     """
     q1 = q1 / np.sum(q1)
     q2 = q2 / np.sum(q2)

     joint_ent = 0
     for p in range(0, len(jointProb)):
         for q in range(0, len(jointProb[p])):
             #if not math.isnan(jointProb[p,q] * np.log(jointProb[p, q])):
             if 0 not in np.array([ jointProb[p,q], q1[p], q2[q] ]):
                 joint_ent -= jointProb[p,q] * np.log(jointProb[p, q])
     return joint_ent
