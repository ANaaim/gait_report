# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 13:25:48 2018

@author: Alexandre Naaim
"""

import numpy as np
import btk
import matplotlib.pyplot as plt

def plot_emg(filename,color1,color2,title="EMG"):
    
    reader = btk.btkAcquisitionFileReader()
    reader.SetFilename(filename)
    reader.Update()
    acq = reader.GetOutput()
    name_emg = ["VL","Gastroc","RF","IJ","TA"]
    
    emg_R = {}
    emg_L = {}
    
    for muscle_name in name_emg:
        emg_R[muscle_name] = acq.GetAnalog("R"+muscle_name).GetValues()
        emg_L[muscle_name] = acq.GetAnalog("L"+muscle_name).GetValues()

 # Initialisation des lists contenant les evenements
    L_FO = []
    R_FO = []
    L_FS = []
    R_FS = []
    
    for it in btk.Iterate(acq.GetEvents()): 
        if it.GetContext().lower() == "left":
            if it.GetLabel() == 'Foot Strike':
                L_FS.append(it.GetFrame())
            elif it.GetLabel() == 'Foot Off':
                L_FO.append(it.GetFrame())
        elif it.GetContext().lower() == 'right':
            if it.GetLabel() == 'Foot Strike':
                R_FS.append(it.GetFrame())
            elif it.GetLabel() == 'Foot Off':
                R_FO.append(it.GetFrame())
                
    L_FO.sort()
    R_FO.sort()
    L_FS.sort()
    R_FS.sort()
    point2analog = acq.GetAnalogFrequency()/float(acq.GetPointFrequency())
    
    # On enleve tout les evenements qui sont avant le premier foot strike du coté étudié
    first_frame = acq.GetFirstFrame()
    
    L_FS = [(x-first_frame)*point2analog for x in L_FS ]
    R_FS = [(x-first_frame)*point2analog for x in R_FS]
    L_FO = [(x-first_frame)*point2analog for x in L_FO]
    R_FO = [(x-first_frame)*point2analog for x in R_FO]
                
    numbre_emg = len(name_emg)
    nbr_frame = np.size(acq.GetAnalog("R"+name_emg[0]).GetValues(),0)
    
    fig,axis = plt.subplots(numbre_emg*2,1,figsize=(8.27,11.69),dpi=100)
    
    
    for ind_muscle, muscle_name in enumerate(name_emg):
        ax_temp_R = axis[ind_muscle*2]
        ax_temp_L =  axis[ind_muscle*2+1]
        
         
        
        ax_temp_R.plot(emg_R[muscle_name],color = color2, linewidth = 1.0)
        ax_temp_R.set_title("R "+muscle_name, fontsize=8)
        ax_temp_R.set_xlim((0,nbr_frame))
        ax_temp_R.set_xticklabels([])
        
        ax_temp_L.plot(emg_L[muscle_name],color = color1)
        ax_temp_L.set_title("L "+muscle_name, fontsize=8)
        ax_temp_L.set_xlim((0,nbr_frame))
        if not ind_muscle == numbre_emg:
            ax_temp_L.set_xticklabels([])
        
        for axis_temp in [ax_temp_R,ax_temp_L]:
            for x_event in L_FS:
                y_lim = axis_temp.get_ylim()
                axis_temp.plot([x_event, x_event],y_lim,color = color1)
                axis_temp.set_ylim(y_lim)
            for x_event in L_FO:
                y_lim = axis_temp.get_ylim()
                axis_temp.plot([x_event, x_event],y_lim,color = color1,linestyle='--')
                axis_temp.set_ylim(y_lim)
            for x_event in R_FS:
                y_lim = axis_temp.get_ylim()
                axis_temp.plot([x_event, x_event],y_lim,color = color2)
                axis_temp.set_ylim(y_lim)
            for x_event in R_FO:
                y_lim = axis_temp.get_ylim()
                axis_temp.plot([x_event, x_event],y_lim,color = color2,linestyle='--')
                axis_temp.set_ylim(y_lim)
    
    plt.tight_layout()
    plt.show()
    fig.savefig(title+'.png', bbox_inches='tight')