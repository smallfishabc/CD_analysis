# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 11:57:14 2022

@author: ShaharGroup-fyu

Rename CD measurement base on 

"""

import os
import pandas as pd
def list_txt_file():   
    list_name=[]
    # List all the files in the current working directory (Similar to DIR command in DOS)
    namestemp = os.listdir()
    # Remove all unneccessary files (Actually I think we can just select the txt file rather than remove the redundant files)
    for n in namestemp:
        if n.split('.')[-1]=='txt':
        # Attach txt file name into the list name
            list_name.append(n.replace('.txt',''))
    return list_name
#def get_CD_file_list():
    
test=pd.read_csv('evaporation_experiment_D_0127.csv')
a=list_txt_file()
