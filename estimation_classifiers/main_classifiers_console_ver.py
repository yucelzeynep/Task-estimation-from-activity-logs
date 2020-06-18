#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 10:36:05 2019

@author: florianpgn

This file is more handy (as compared to main_classifiers), if you prefer testing 
and contrasting different choices of hyper-parameters on the console.

You may at once modify the param.py file and test it (instead of switching between 
files, i.e. first changing the variable values in param.py and then rerunnig 
main_classifiers.py)

When calling this script on console, you need 2 arguments, (i) the stage number 
(either 1 or 2) and (ii) the file name for the data.
"""

import re
import sys
import params

def setup_params(stage, file):
    """
    Update param values
    """
    f = open('params.py','r')
    new_lines = []
    for line in f.readlines():
        line = re.sub('ANNOTATION_FILE = \w+', 'ANNOTATION_FILE = {}'.format(file), line)
        line = re.sub('STAGE = \d', 'STAGE = {}'.format(stage), line)
        new_lines.append(line)        
    f.close()

    #Overwrite with the new content
    f = open('params.py','w')
    for line in new_lines:
        f.write(line)        
    f.close()


if __name__ == "__main__":      
    if len(sys.argv) > 1:

        setup_params(sys.argv[1], sys.argv[2])
        
        f = open("classifiers_results.txt", "a+")
        person = 'DEV' if params.ANNOTATION_FILE == params.FILE_DEV else 'LEADER'
        
        f.write('{} - Stage {}\n'.format(person, params.STAGE))
        f.write('Non hierarchical, Relevant desc({}), Train size({})\n'.format(params.USE_REL_DESC, params.TRAINSET_SIZE))
        f.close()