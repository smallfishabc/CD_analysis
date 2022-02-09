# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 16:12:32 2022

@author: ShaharGroup-fyu

This is the standard CD analysis library developed from old scripts.

This script can realize 1. background subtraction
                        2. Calculate MRE
                        3. Single CD spectra plot (with limited customization)
                        4. Overlay CD curve from same/different protein
I recommand to source this script and use juypter notebook to customize the plot.                        
Future improvment: Automatically determine the roww number
"""
import pandas as pd
import matplotplib.pyplot as plt
# Load JASCO CD txt file into dataframe
def obtain_parameters(experiment_file_name):
    # Remove the txt from the file name
    raw_information=experiment_file_name.split('.')[0]
    splited=raw_information.split('_')
    concentration=splited[0]
    tag=splited[0]+splited[1]
    return splited,concentration,tag
def load_CD(fname):
    # Here the skiprows are manually calculated based on the txt file
    # For the same CD setup normally these number will not change.
    # nrows=700 is the setting with scanning internval 0.1nm and scanning limit 190-260nm
    spectrum=pd.read_csv(fname,sep='\t',skiprows=20,nrows=700,header=None,names=['wavelength','degree','voltage'])
    return(spectrum)
def background_subtraction(experiment_file_name,background_file_name):
    # Read data based on the protein file name
    a=load_CD(experiment_file_name)
    standard=load_CD(background_file_name)
    # Background sbstraction
    subtracted=(a.drop(['voltage'])-standard.drop(['voltage']))
    ratio=subtracted[subtracted['wavelength']]/degree[600]
    return subtracted
# MRE is the average CD signal change normalized by sequence length and the 
# concentration.
def MRE_calculation(sequence_length,concentration,subtracted_CD):
    degree=subtracted_CD['degree'].divide(float(concentration)*0.000001*1000*sequence_length)
    return(subtracted_CD['wavelength'],degree)
def single_CD_plot(experiment_file,background_file,sequence_length,figure_object=0):
    _,concentration,tag=obtain_parameters(experiment_file)
    subtracted=background_subtraction(experiment_file,background_file)
    x,y=MRE_calculation(sequence_length,concentration,subtracted)
    plt.plot(x,y)
    plt.xticks(ticks=[200,220,240,260],fontsize=40)
    plt.subplots_adjust(hspace =0.4,wspace=0.4)
    plt.yticks(fontsize=40)
    plt.ylim([-5,5])
    plt.title(tag,fontsize=40)
    plt.ylabel('Normalized degree milideg*L/mol',fontsize=30)
    plt.xlabel('Wavelength (nm)',fontsize=40)
    #if figure_object!=0:
    # Here I will write a function to 
        #pass
    