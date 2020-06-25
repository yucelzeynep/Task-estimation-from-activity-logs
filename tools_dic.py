#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 16:42:50 2019

@author: florianpgn

This file involves functions which (i) initialize instances of varying sorts of 
dictionary variables and (ii) which carry out trivial operations on those
"""
import numpy as np

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


def define_names():
    ###########################################################################
    exe_names = ['excel', 'explorer', 'sakura', 'devenv', 'iexplore', 'notepad',
             'bcompare', 'airsovly', 'firefox', 'editplus', 'tortoiseproc', 'symphony', 
             'sofficebin','msimn', 'ipmsg', 'aliim', 'rundll32', 'airspsam', 
             'taskpit', 'dwwin']

    ###########################################################################
    
    """
    Window titles are once copied from the association rules
    """
    title_names = ['Debug','Test','出退勤','OGA','OGT','OGU','OGV','OLT',\
               'OLV','VOL','AIRS_PSAM','PSAM_変換仕様書','出力系調査報告書',\
               '帳票定義体','画面定義体','娘','童','淘宝','常来返','taobao',\
               '百度搜索','百度百科','百度知道','服装','SQL','搜房网','AIRS',\
               'THICK変換ﾃｰﾌﾞﾙ','POINT変換ﾃｰﾌﾞﾙ','SIZE変換ﾃｰﾌﾞﾙ',\
               '漢字コード変換表','ＢＭＳ','ＩＢＭ漢字コード変換対応表',\
               '調査報告書','ATTRパターン','ＦＩＥＬＤ文','Q&A管理台帳','搜索',\
               '不具合対応','天猫','支付宝','ReverseServer','Error',\
               'ＤＡＴＡ文（項目定義）の変換','ﾛｸﾞﾌｧｲﾙ','解析Log','解析ｿｰｽ',\
               '報告書','査読シート','ファイル内の検索']

    ###########################################################################

    time_names = ['Lunch+', 'Lunch-']
    
    ###########################################################################


    """
    Here is the benchmark for level of association
     0.00                 	No Relationship    	Knowing the independent variable does not help in predicting the dependent variable.
    .00 to .15            	Very Weak          	Not generally acceptable
    .15 to .20            	Weak              	Minimally acceptable
    .20 to .25            	Moderate           	Acceptable
    .25 to .30            	Moderately Strong  	Desirable
    .30 to .35            	Strong             	Very Desirable
    .35 to .40            	Very Strong        	Extremely Desirable
    .40 to .50            	Worrisomely Strong 	Either an extremely good relationship or the two variables are measuring the same concept
    .50 to .99            	Redundant          	The two variables are probably measuring the same concept.
    1.00                  	Perfect Relationship.  	If we the know the independent variable, we can perfectly predict the dependent variable.  
    
    Refer to U. Toronto Pol242 Lab manual
    http://homes.chass.utoronto.ca/~josephf/pol242/Labs/LM-3A/LM-3A_frameset.htm
    """
    level_of_assoc = ['Weak', #15 to .20  
                  'Moderate',#20 to .25 
                  'Moderately Strong ',#25 to .30
                  'Strong',#30 to .35
                  'Very Strong ',#35 to .40 
                  'Worrisomely Strong ']#40 to .50
    
    return (exe_names, title_names, time_names, level_of_assoc)
