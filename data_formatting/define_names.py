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
