#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 10:48:22 2019

@author: florianpgn
"""
"""
Manual annotation files
"""
FILE_DEV = 'shimizu_annotation_dev.csv'
FILE_LEADER = 'shimizu_annotation_lead.csv'
FILE_BOTH = 'shimizu_annotation_combined.csv'

"""
Descriptors
"""
EXES = 'Exes'
WINDOWS = 'Windows'
EXES_WINDOWS = 'Exes&Windows'
KEYSTROKES = 'Keystrokes'
LUNCHS = 'Lunchs'
DURATIONS = 'Durations'
LCLICKS = 'Left clicks'
RCLICKS = 'Right clicks'

"""
Task strings
"""
PROG = 'プログラミング'
TEST = 'テスト'
ADMIN = '事務'
LEISURE = '余暇'
DOCUMENT = '文書作成・確認'
UNKNOWN = 'UNKNOWN'
OTHER = 'Other'

"""
Params
"""
ANNOTATION_FILE = FILE_LEADER
NB_TITLES_PER_SAMPLE = 4
N_MAX_EST = 3
N_EXE_RELEVANT = 20
N_TITLE_RELEVANT = 30
ALPHA = .5
USE_DISTRIB_PROB = True
HIERARCHICAL = True
STAGE = 2

"""
Preferences related to classifiers
"""
TRAINSET_SIZE = 0.7
USE_REL_DESC = True

"""
Preferences relating the hierrachical framework
As descriptos, by default, we have 2D desciptor at stage-1 and 2 1D descriptors 
at stage-2.
"""

STAGE_1_DESCRIPTORS = [EXES_WINDOWS]
STAGE_2_DESCRIPTORS = [EXES, WINDOWS]

"""
You may as well try with all descriptors
Such results are provided in the supplemental material
"""
# STAGE_1_DESCRIPTORS = [EXES_WINDOWS, KEYSTROKES, LUNCHS, DURATIONS, LCLICKS, RCLICKS]
# STAGE_2_DESCRIPTORS = [EXES, WINDOWS, KEYSTROKES, LUNCHS, DURATIONS, LCLICKS, RCLICKS]

"""
The possible tasks at stage-1 and stage-2 and all possible tasks (for non-hier)
"""

TASKS_S1 = [TEST, OTHER, DOCUMENT]
TASKS_S2 = [PROG, ADMIN, LEISURE]
TASKS = [PROG, TEST, ADMIN, LEISURE, DOCUMENT]

if not HIERARCHICAL:
    if STAGE == 1:
        TASKS = TASKS_S1
    else:
        TASKS = TASKS_S2

N_TASKS = len(TASKS)

# In computing quartiles, you may choose to remove or not the offset
# Does not have much significance
REMOVE_OFFSET = False
"""
Define the Q for computng the Q-quartiles. We solved for the below variables as 
explained in Appendix J (Details of Assessment of descriptors' relevance)
"""
#Keystrokes quartiles
N_BINS_KSTROKES = 2
#Left clicks quartiles
N_BINS_LCLICKS = 2
#Duration quartiles
N_BINS_DURATION = 6


#Correlation bagging
BAG_SIZE_EXE = 7
BAG_SIZE_TITLE = 5

# Code mat names
TASK_MAT = 'task_code_mat'
TITLE_MAT = 'title_code_mat'
EXE_MAT = 'exe_code_mat'
LUNCH_MAT = 'lunch_code_mat'
KSTROKE_MAT = 'keystrokes_code_mat'
LCLICK_MAT = 'lclicks_code_mat'
RCLICK_MAT = 'rclicks_code_mat'
DURATION_MAT = 'duration_code_mat'

# .dat file names
PREV_DAT = 'person1_'
NEW_DAT = 'new_'
DAT_FILE_PREFIX = NEW_DAT

# Path for dat files
PATH_TASK = '../../task_codes/'
PATH_TITLE = '../../windowtitle_codes/'
PATH_EXE = '../../exe_codes/'
PATH_KSTROKES = '../../keystrokes/'
PATH_LUNCH = '../../lunch_codes/'
PATH_CLICKS = '../../clicks/'
PATH_DURATION = '../../duration/'

# CSV feature names
TASK_STR = 'task_name'
TIME_START_STR = 'time_start'
TIME_STOP_STR = 'time_stop'
DURATION_STR = 'duration'

NB_LCLICK_STR = 'n_left_click'
NB_RCLICK_STR = 'n_right_click'
NB_KSTROKES_STR = 'n_keystrokes'

EXE_STR = 'exe_name'
WINDOW_STR = 'window_title'
HAND_TASK_STR = 'hand_annotation'
AUTO_TASK_STR = 'auto_annotation'
EST_1_STR = 'candidate_1'
EST_2_STR = 'candidate_2'
EST_3_STR = 'candidate_3'

COL_NAMES = [TASK_STR, TIME_START_STR, TIME_STOP_STR, \
             NB_LCLICK_STR, NB_RCLICK_STR, NB_KSTROKES_STR,\
             EXE_STR, HAND_TASK_STR, EST_1_STR,\
             EST_2_STR, EST_3_STR, AUTO_TASK_STR]


