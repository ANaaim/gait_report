# -*- coding: utf-8 -*-
"""
Created on Fri Apr 06 14:57:56 2018

@author: AdminXPS
"""

import numpy as np 
from param_spt_allfiles import param_spt_allfiles as param_spt_allfiles
from kinematic_allfiles import kinematic_allfiles as kinematic_allfiles
# pour demander à l'utilisateur de sélectionner des fichiers
from Tkinter import Tk
from tkFileDialog import askopenfilenames
from tkSimpleDialog import askstring 
import tkMessageBox
import matplotlib.pyplot as plt
from plot_kinematic import plot_kinematic as plot_kinematic

#
#filenames_case1 = askopenfilenames(title="Choisir les fichiers de la première condition:",filetypes=[("Fichiers C3D","*.c3d")])
#
## Calcul des paramètres spatio temporels
#subject_spt_case1 = param_spt_allfiles(filenames_case1)
#
#name_case_1 = "left"
#name_case_2 = "right"
#color_case_1 = 'tab:orange'
#color_case_2 = 'tab:blue'
#
#subject_spt_case1 = subject_spt_case1["left"]
#subject_spt_case1 = subject_spt_case1["right"]

def plot_spt(subject_spt_case1,color_case_1,
             subject_spt_case2,color_case_2,
             legend_1="",legend_2 ="",title="SPT"):

    list_spt = ["cycle_time",
                "cadence",
                "length_cycle",
                "walking_speed",
                "step_length",
                "step_sec",
                "step_width",
                "stance_phase_sec",
                "swing_phase_sec",
                "stance_phase_perc",
                "swing_phase_perc",
                "simple_stance_perc",
                "double_stance_perc"]
    name_spt = ["Temps du cycle (s)",
                "Cadence (Pas/min)",
                "Longueur du cycle (m)",
                "Vitesse de marche (m/s)",
                "Longueur du pas (m)",
                "Temps du pas (s)",
                "Largeur du pas (m)",
                "Phase d\'appui (s)",
                "Phase oscillante (s)",
                "Phase d\'appui (%)",
                "Phase oscillante (%)",
                "Simple appui (%)",
                "Double appui (%)"]
    
    list_temp = []
    # ["",name_case_1, name_case_2,"Norme"]
    for key, name in zip(list_spt,name_spt):
        value_1 = '%.2f'%subject_spt_case1["mean"][key] + u"\u00B1" + '%.2f'%subject_spt_case1["std"][key] 
        value_2 = '%.2f'%subject_spt_case2["mean"][key] + u"\u00B1" + '%.2f'%subject_spt_case2["std"][key]
        list_temp.append([name, value_1, value_2,value_2])
    
    
    
    fig, axis =plt.subplots(1,1,dpi=100)
    #fig,axis = plt.subplots(1,1,figsize=(8.27,11.69),dpi=100)
    
    collabel=("", legend_1, legend_2, "norme")
    
    the_table = axis.table(cellText=list_temp,colLabels=collabel,loc='center',edges='open')
    
    
    
    table_props = the_table.properties()
    table_cells = table_props['child_artists']
    for cell in table_cells: 
            cell._text.set_fontsize(15)
    the_table._cells[(0,1)]._text.set_color(color_case_1)
    #the_table._cells[(0,1)].set_fontsize(40)
    the_table._cells[(0,2)]._text.set_color(color_case_2)
    axis.axis('tight')
    axis.axis('off')
    for ind_row in range(len(list_spt)+1):
        the_table._cells[(ind_row,3)]._text.set_color('grey')
    the_table.auto_set_column_width([-1,0,1,2,3])
    the_table.scale(1.0, 2.0)
    plt.tight_layout()
    plt.show(block=False)
    fig.savefig(title+'.png', bbox_inches='tight')