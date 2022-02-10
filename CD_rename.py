# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 11:57:14 2022

@author: ShaharGroup-fyu

Rename CD measurement base on 

"""

import os
import pandas as pd
import numpy as np
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
def excel_name_edit(old_name):
    front=old_name.replace('.xlsx','')
    new_name=front+'_written'+'.xlsx'
    return new_name
def write_file_name_csv(dataframe,new_excel_name):
    for i in range(len(dataframe)):
        print(dataframe.loc[i,'Tube_number'],type(dataframe.loc[i,'Tube_number']),not dataframe.loc[i,'Tube_number'])
        if np.isnan(dataframe.loc[i,'Tube_number']):
            break
            # Input the component of the file name from xlsx file
            # For different experiments, the column name maybe different
            # But the structure will stay the same
        Solute_concentration=dataframe.loc[i,'Solute_Concentration_Experiment']
        Solute_type=dataframe.loc[i,'Solute_type']
        tag=dataframe.loc[i,'tag']
        time=dataframe.loc[i,'Time_experiment']
        file_name='_'.join((str(Solute_concentration),str(Solute_type),str(tag),str(time)))
        dataframe.loc[i,'File_name']=file_name
        dataframe.loc[i,'Buffer_file']=file_name+'_buffer'
    dataframe.to_excel(new_excel_name,index=False)
#def get_CD_file_list():
excel_name='evaporation_0206_CASHD.xlsx'
test=pd.read_excel(excel_name)
a=list_txt_file()
new_excel_name=excel_name_edit(excel_name)
write_file_name_csv(test,new_excel_name)
