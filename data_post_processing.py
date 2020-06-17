# !/usr/bin/env python3
#  -*- coding: utf-8 -*-
"""
Created on Wed May 22 13:19:42 2019

@author: florianpgn

This file is called post-processing but it may a little confusing. 

Here, the post-processing refers to putting the data, which is loaded from the 
raw file, into some shape that we like, e.g. setting 'duration' to the time 
difference between t_start and t_stop.

Actually, the pre-processing explained in the article comes after this so-called
post-processing.
"""
from datetime import datetime # There is a datetime module in datetime...

import params
from importlib import reload
reload(params)


DATE_FORMAT = "%Y %m %d %H:%M:%S"

def formatDate(date):
    """
    Format the date and apply the format declared at the top of this file
    """
    
    formated_date = datetime.strptime(date, '%Y/%m/%d %H:%M:%S').strftime(DATE_FORMAT)
    return formated_date


def mapFuncOnDictArray(dic, key, func):
    """
    Apply the function 'func' to an array reference by the key 'key' in dict 
    'dic'
    """
    dic[key] = list(map(func, dic[key]))


def clearDates(datalog):
    """
    Format the dates in the datalog so that there is no more kanji
    """
    mapFuncOnDictArray(datalog, params.TIME_START_STR, formatDate)
    mapFuncOnDictArray(datalog, params.TIME_STOP_STR, formatDate)
    return datalog



def addDurationFeature(datalog):
    """
    Duration feature section
    """
    # Add the new feature
    datalog[ params.DURATION_STR ] = []
    
    # Format the date
    datalog = clearDates(datalog)
    
    # Iterate through both the starting time and ending time
    for date_start, date_stop in zip(datalog[ params.TIME_START_STR ] ,\
                                     datalog[ params.TIME_STOP_STR ] ):
        
        start_time = datetime.strptime(date_start, DATE_FORMAT)
        stop_time = datetime.strptime(date_stop, DATE_FORMAT)
        
        # Calculate the difference bewteen the stoping and starting time
        duration = (stop_time - start_time).total_seconds();
        datalog[ params.DURATION_STR ].append(duration)
        
    return datalog


def addIdleFeature(datalog):
    """
    Idle  feature section

    """
    # Add the new feature
    datalog['idle_after_task'] = []
    
    # Loop over the tasks and calculate the difference between the end time of
    # the task and start time of the next task
    for index in range(len(datalog[ params.TIME_START_STR ])-1):
        
        t_stop = datalog[ params.TIME_STOP_STR ][index]
        t_next_start = datalog[ params.TIME_START_STR ][index+1]
        
        stop_time = datetime.strptime(t_stop, DATE_FORMAT)
        next_start_time = datetime.strptime(t_next_start, DATE_FORMAT)
        
        # Idle must be 0 the working day change
        if stop_time.day != next_start_time.day:
            idle_duration = 0
        else:
            # Calculate the difference bewteen the stoping and starting time
            idle_duration = (next_start_time - stop_time).total_seconds();
        
        datalog['idle_after_task'].append(idle_duration)
        
    return datalog



def addAPMFeature(datalog):
    """
    Action per minute (APM) feature section
    
    """
    if params.DURATION_STR not in datalog:
        print("Duration feature must me added before. Abort.")
        return
    
    # Add the new feature
    datalog['apm'] = []
    
    # Iterate through both the keystrokes number and duration
    for nb_key_strokes, duration in zip(datalog[ params.NB_KSTROKES_STR ] , datalog[ params.DURATION_STR ] ):
        if duration == 0:
            apm = 0
        else:
            apm = int(nb_key_strokes) / (duration/60) # Keystrokes per minute
        datalog['apm'].append(apm)
        
    return datalog






