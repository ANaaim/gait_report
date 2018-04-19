# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 13:25:48 2018

@author: Alexandre Naaim
"""

import numpy as np
import btk
import matplotlib.pyplot as plt
for i in [1]:
    filename = 'test.c3d'
#def plot_emg(filename):
    reader = btk.btkAcquisitionFileReader()
    reader.SetFilename(filename)
    reader.Update()
    acq = reader.GetOutput()
    side = 'left'
    side_cl = 'right'
    name_emg = ["VL","Gastroc","RF","IJ","TA"]
    
    emg_R = {}
    emg_L = {}
    
    for muscle_name in name_emg:
        emg_R[muscle_name] = acq.GetAnalog("R"+muscle_name).GetValues()
        emg_L[muscle_name] = acq.GetAnalog("L"+muscle_name).GetValues()

 # Initialisation des lists contenant les evenements
    FO = []
    FO_CL = []
    FS = []
    FS_CL = []
    for it in btk.Iterate(acq.GetEvents()): 
        if it.GetContext().lower() == side:
            if it.GetLabel() == 'Foot Strike':
                FS.append(it.GetFrame())
            elif it.GetLabel() == 'Foot Off':
                FO.append(it.GetFrame())
        elif it.GetContext().lower() == side_cl:
            if it.GetLabel() == 'Foot Strike':
                FS_CL.append(it.GetFrame())
            elif it.GetLabel() == 'Foot Off':
                FO_CL.append(it.GetFrame())
                
    numbre_emg = len(name_emg)
    
    fig,axis = plt.subplots(numbre_emg*2,1,figsize=(8.27,11.69),dpi=100)
    
    
    for ind_muscle, muscle_name in enumerate(name_emg):
        ax_temp_R = axis[ind_muscle*2]
        ax_temp_L =  axis[ind_muscle*2+1]
        
        ax_temp_R.plot(emg_R[muscle_name])
        ax_temp_L.plot(emg_L[muscle_name])
    plt.show()