#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 15:57:37 2020

@author: zeynep


This function does cross-tabulation for each exe and each window title
and evaluates the correlation between the exe/window title with the assigned task.

It takes one exe (or one title) and all the tasks. It labels exe as positive 
or negative for each labeled  line.

Therefore the table is 2 x N_task. Using this table, it computes Cramers V to
measure the level of association between this exe (or window title) and the tasks.

The exe/window title which are found to be descriptive will be used computing 
the post probability. 

If the line is not coded by annotator with a task, it omits that line. 

For the explanation of exe names and window titles, 
see codes_exe.txt, codes_title.txt.

For refence, level of association is judged as follows

 LEVEL OF ASSOCIATION 	Verbal Description 	COMMENTS
 0.00                 	No Relationship    	Knowing the indepent variable does not help in predicting the depent variable.
.00 to .15            	Very Weak          	Not generally acceptable
.15 to .20            	Weak              	Minimally acceptable
.20 to .25            	Moderate           	Acceptable
.25 to .30            	Moderately Strong  	Desirable
.30 to .35            	Strong             	Very Desirable
.35 to .40            	Very Strong        	Extremely Desirable
.40 to .50            	Worrisomely Strong 	Either an extremely good relationship or the two variables are measuring the same concept
.50 to .99            	Redundant          	The two variables are probably measuring the same concept.
1.00                  	Perfect Relationship.  	If we the know the indepent variable, we can perfectly predict the depent variable.  

from http:#groups.chass.utoronto.ca/pol242/Labs/LM-3A/LM-3A_content.htm


Zeynep Yucel
2017 12 19

"""
 
import numpy as np

import tools_file as ftools
import tools_dic as dtools
import tools_cramersV as Vtools

import params
from importlib import reload
reload(params)

if __name__ == "__main__":


    (exe_names, title_names, time_names, level_of_assoc) = dtools.define_names()
    
    """
    Load all data
    """
    
    exe_code_mat = ftools.load(params.PATH_EXE + params.DAT_FILE_PREFIX + params.EXE_MAT)
    title_code_mat = ftools.load(params.PATH_TITLE + params.DAT_FILE_PREFIX + params.TITLE_MAT)
    task_code_mat = ftools.load(params.PATH_TASK + params.DAT_FILE_PREFIX + params.TASK_MAT)
    time_code_mat = ftools.load(params.PATH_LUNCH + params.DAT_FILE_PREFIX + params.LUNCH_MAT)
    
    
    (count_exe, count_task_principal, count_title) = ftools.load('count_exe_title_task')
    ###########################################################################
    
    n_task = params.N_TASKS  # I include '0' for unknown task (not labeled by Shimizu)
    all_exe = (np.unique(exe_code_mat)) # number of all exe 
    all_title = (np.unique(title_code_mat)) # all window titles used in the Shimizu's rules and +1 for the titles which do  not include keyword from his rules
    n_all_time = 2 # for lunch break and not-lunch break
    
    """    
    Correlation between exe and task
    CramersV is symmetric (so it does not matter which one comes first)
    """
    cV = []
    for exe in all_exe:
    
        """
        Two rows in cross tabulation:  one for exeE positive, other for exeE negative
        """
        crosstab_exeE_vs_task = dtools.init_dic_matrix(['Positive','Negative'])
        tempE = (exe_code_mat == exe)
        for task in params.TASKS:
            # exeE negative
            crosstab_exeE_vs_task['Negative'][task] = np.sum( np.logical_and(tempE == False, \
                                 task_code_mat == task))
            # exeE positive
            crosstab_exeE_vs_task['Positive'][task] = np.sum( np.logical_and(tempE == True, \
                                 task_code_mat == task))
        
    
        (x_sq_task_vs_exe, v_task_vs_exe) =  Vtools.cramersV(crosstab_exeE_vs_task)
        (x_sq_task_vs_exe_cor, v_task_vs_exe_cor) =  Vtools.cramersV_bias_corrected(crosstab_exeE_vs_task)

        cV.append(v_task_vs_exe)
    
    ## If desired, uncomment the below
#    cV_exe = cV
#    ftools.save('cV_exe_1by1', [cV_exe], ['cV_exe'])
    
    print('\n**********************************************')
    print('List of exe which present statistically significant correlation with task:\n')
    print('Code \t Exe \t\t No \t cV \t Level of association')
    print('---------------------------------------------------------------')
    for i in range(len(cV)):
        if 0.15< cV[i] and cV[i] < 0.20 :
            print('{0} \t {1} \t {2:.3f}\t {3:s}'.format( i+1,count_exe[i],cV[i],level_of_assoc[0] ))
        elif 0.2< cV[i] and cV[i] < 0.25 :
            print('{0} \t {1} \t {2:.3f}\t {3:s}'.format( i+1,count_exe[i],cV[i],level_of_assoc[1] ))
        elif 0.25< cV[i] and cV[i] < 0.30 :
            print('{0} \t {1} \t {2:.3f}\t {3:s}'.format( i+1,count_exe[i],cV[i],level_of_assoc[2] ))
        elif 0.30< cV[i] and cV[i] < 0.35 :
            print('{0} \t {1} \t {2:.3f}\t {3:s}'.format( i+1,count_exe[i],cV[i],level_of_assoc[3] ))
        elif 0.35< cV[i] and cV[i] < 0.40 :
            print('{0} \t {1} \t {2:.3f}\t {3:s}'.format( i+1,count_exe[i],cV[i],level_of_assoc[4] ))
        elif 0.40< cV[i] and cV[i] < 0.50 :
            print('{0} \t {1} \t {2:.3f}\t {3:s}'.format( i+1,count_exe[i],cV[i],level_of_assoc[5] ))
        
    
    
    
    """
    Correlation between title and task
    CramersV is symmetric (so it does not matter which one comes first)
    """
    cV = []
    for t in all_title:
    
        """
        Two rows in cross tabulation: one for titleE positive, other for titleE 
        negative
        """
        crosstab_titleT_vs_task = dtools.init_dic_matrix(['Positive','Negative'])
        
        #Perfom a logical OR between columns
        tempE = (title_code_mat == t).any(axis=1)
        for task in params.TASKS:
            crosstab_titleT_vs_task['Negative'][task] = np.sum( np.logical_and(tempE == False, task_code_mat == task))
            crosstab_titleT_vs_task['Positive'][task] = np.sum( np.logical_and(tempE == True, task_code_mat == task))
        
    
        (x_sq_task_vs_title, v_task_vs_title) =  Vtools.cramersV(crosstab_titleT_vs_task)
        (x_sq_task_vs_title_cor, v_task_vs_title_cor) =  Vtools.cramersV_bias_corrected(crosstab_titleT_vs_task)   
    
        cV.append(v_task_vs_title)
    
        ## If desired, uncomment the below
#    cV_title = cV
#    ftools.save('cV_title_1by1', [cV_title], ['cV_title'])
    
    print('\n**********************************************')
    print('List of titles which present statistically significant correlation with task:\n')
    print('Code \t Title \t\t No \t cV \t Level of association')
    print('--------------------------------------------')
    for i in range(len(cV)):
        if 0.15< cV[i] and cV[i] < 0.20 :
            print('{0} \t {1} \t {2:.3f}\t {3:s}'.format( i+1,count_title[i],cV[i],level_of_assoc[0] ))
        elif 0.2< cV[i] and cV[i] < 0.25 :
            print('{0} \t {1} \t {2:.3f}\t {3:s}'.format( i+1,count_title[i],cV[i],level_of_assoc[1] ))
        elif 0.25< cV[i] and cV[i] < 0.30 :
            print('{0} \t {1} \t {2:.3f}\t {3:s}'.format( i+1,count_title[i],cV[i],level_of_assoc[2] ))
        elif 0.30< cV[i] and cV[i] < 0.35 :
            print('{0} \t {1} \t {2:.3f}\t {3:s}'.format( i+1,count_title[i],cV[i],level_of_assoc[3] ))
        elif 0.35< cV[i] and cV[i] < 0.40 :
            print('{0} \t {1} \t {2:.3f}\t {3:s}'.format( i+1,count_title[i],cV[i],level_of_assoc[4] ))
        elif 0.40< cV[i] and cV[i] < 0.50 :
            print('{0} \t {1} \t {2:.3f}\t {3:s}'.format( i+1,count_exe[i],cV[i],level_of_assoc[5] ))


    