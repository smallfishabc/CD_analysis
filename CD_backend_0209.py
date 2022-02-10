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
import matplotlib.pyplot as plt
# Load the xlsx for the dataset. The xlsx is created/edited by CD_rename script
def load_datafile(datafile_name):
    dataframe=pd.read_excel(datafile_name)
    return dataframe
# Read concentration, CD filename and other parameters from xlsx file based on
# the tube_number(we may need to set the tube_number to index later)
def obtain_parameters(dataframe,tube_number):
    data_selected=dataframe.loc[dataframe['Tube_number']==tube_number]
    #print(data_selected)
    # Here we may need to add protein name in further analysis
    concentration=data_selected['protein_final_molality'].values[0]
    concentration=round(concentration, 2)
    solute_concentration=data_selected['Final_concentration_trehalose'].values[0]
    solute_concentration=round(solute_concentration, 2)
    solute_type=data_selected['Solute_type'].values[0]
    path_length=data_selected['Cuvette'].values[0]
    tag="_".join((str(concentration),str('CASHD'),str(solute_concentration),str(solute_type)))
    experiment_file_name=data_selected['File_name'].values[0]+'-1.txt'
    background_file_name=data_selected['Buffer_file'].values[0]+'-1.txt'
    return concentration,tag,path_length,experiment_file_name,background_file_name
# Load JASCO CD txt file into dataframe
def load_CD(fname):
    # Here the skiprows are manually calculated based on the txt file
    # For the same CD setup normally these number will not change.
    # nrows=700 is the setting with scanning internval 0.1nm and scanning limit 190-260nm
    spectrum=pd.read_csv(fname,sep='\t',skiprows=20,nrows=700,header=None,names=['wavelength','degree','voltage'])
    return(spectrum)
def background_subtraction(experiment_file_name,background_file_name):
    # Read data based on the protein file name
    experiment=load_CD(experiment_file_name)
    standard=load_CD(background_file_name)
    # Background sbstraction
    subtracted=(experiment['degree']-standard['degree'])
    #ratio=subtracted[subtracted['wavelength']]/degree[600]
    return experiment['wavelength'],subtracted
# MRE is the average CD signal change normalized by sequence length and the 
# concentration.
def MRE_calculation(sequence_length,concentration,path_length,wavelength,subtracted_CD):
    # Concentration unit is micromolar
    #degree=subtracted_CD
    degree=subtracted_CD.divide(float(concentration)*0.000001*1000*sequence_length*path_length)
    return(wavelength,degree)
def single_CD_plot(datafile,tube_number,sequence_length):
    dataframe=load_datafile(datafile)
    concentration,tag,path_length,experiment_file,background_file=obtain_parameters(dataframe,tube_number)
    wavelength,subtracted=background_subtraction(experiment_file,background_file)
    x,y=MRE_calculation(sequence_length,concentration,path_length,wavelength,subtracted)
    plt.figure(figsize=[20,20])
    plt.plot(x,y)
    plt.xticks(ticks=[200,220,240,260],fontsize=40)
    plt.subplots_adjust(hspace =0.4,wspace=0.4)
    plt.yticks(fontsize=40)
    plt.ylim([-15,15])
    plt.title(tag,fontsize=40)
    plt.ylabel('Molality $MRE({10^3*deg*kg*cm^{-1}*dmol^{-1}})$',fontsize=30)
    plt.xlabel('Wavelength (nm)',fontsize=40)
    #if figure_object!=0:
    # Here I will write a function to 
        #pass
def multi_CD_plot(dataframe,tube_number,sequence_length,axis_object=0):
    concentration,tag,path_length,experiment_file,background_file=obtain_parameters(dataframe,tube_number)
    wavelength,subtracted=background_subtraction(experiment_file,background_file)
    x,y=MRE_calculation(sequence_length,concentration,path_length,wavelength,subtracted)
    return(x,y,tag)
def plot_modification():
    plt.xticks(ticks=[200,220,240,260],fontsize=40)
    plt.subplots_adjust(hspace =0.4,wspace=0.4)
    plt.yticks(fontsize=40)
    plt.ylim([-15,15])
    plt.ylabel('Molality $MRE({10^3*deg*kg*cm^{-1}*dmol^{-1}})$',fontsize=30)
    plt.xlabel('Wavelength (nm)',fontsize=40)
    plt.legend(fontsize=20)
def main():
    sequence_length=227
    single_CD_plot('evaporation_0206_CASHD_written.xlsx',21,sequence_length)
if __name__=="__main__":
    main()