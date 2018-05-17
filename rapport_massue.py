# -*- coding: utf-8 -*-
"""
Created on Thu Apr 05 12:55:11 2018

@author: AdminXPS
"""

# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
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
from plot_spt import plot_spt as plot_spt
from extract_Schwartz_norm import extract_Schwartz_norm as extract_Schwartz_norm
from plot_emg import plot_emg as plot_emg

comparaison_bool = tkMessageBox.askyesno("Title","Voulez vous comparer à d'autres résultats?")
emg_bool = tkMessageBox.askyesno("Title","Voulez vous tracer les emg ?")

# On choisit les premiers fichiers
data_directory = 'D:\DonneesViconInstallBMF';
filenames_case1 = askopenfilenames(title="Choisir les fichiers de la première condition:",filetypes=[("Fichiers C3D","*.c3d")],
                                    initialdir = data_directory)
one_filename = filenames_case1[0]
subject_directory_ind_1 = [i for i in range(len(one_filename)) if one_filename.startswith('/', i)]
subjectory_directory_1 = one_filename[0:subject_directory_ind_1[-1]]

case1_name = askstring("Input", "Quelle est la première condition?")

# Calcul des paramètres spatio temporels
subject_spt_case1 = param_spt_allfiles(filenames_case1)
subject_kin_case1 = kinematic_allfiles(filenames_case1)

# si l'utilisateurs veut comparer à autre chose on choisit d'autre fichier
if comparaison_bool:
    filenames_case2 = askopenfilenames(title="Choisir les fichiers de la deuxième condition:",filetypes=[("Fichiers C3D","*.c3d")],
                                       initialdir = subjectory_directory_1)
    one_filename = filenames_case2[0]
    subject_directory_ind_2 = [i for i in range(len(one_filename)) if one_filename.startswith('/', i)]
    subjectory_directory_2 = one_filename[0:subject_directory_ind_1[-1]]
    # Calcul des paramètres spatio temporels
    subject_spt_case2 = param_spt_allfiles(filenames_case2)
    subject_kin_case2 = kinematic_allfiles(filenames_case2)
    case2_name = askstring("Input", "Quelle est la deuxième condition?")

subject_kin_left_case1 = subject_kin_case1["left"]
subject_kin_right_case1 = subject_kin_case1["right"]
subject_spt_left_case1 = subject_spt_case1["left"]
subject_spt_right_case1 = subject_spt_case1["right"]
# Chaque cote contiendra paramètres spatio temporel, kinematic, kinetics
# extraction des event en list
colorleft_case1 = 'tab:red'
colorright_case1 = 'tab:green'
colorleft_case2 = 'tab:orange'
colorright_case2 = 'tab:blue'

# Extraction des normes 
[norm_spt,norm_kin,nomr_kinetic] = extract_Schwartz_norm(Speed="Free")


plot_kinematic(subject_kin_left_case1, subject_spt_left_case1, colorleft_case1,
               subject_kin_right_case1, subject_spt_right_case1, colorright_case1,
               norm_spt,norm_kin,
               legend_1="Gauche "+case1_name,legend_2="Droite "+case1_name, title="Kinematic_"+case1_name)

plot_spt(subject_spt_left_case1, colorleft_case1,
         subject_spt_right_case1, colorright_case1,
         legend_1="Gauche\n"+case1_name, legend_2="Droite\n"+case1_name, title="SPT_"+case1_name)

if emg_bool:
    emg_filename_case1 = askopenfilenames(title="Choisir le fichies de tracer EMG condition "+case1_name+" :",filetypes=[("Fichiers C3D","*.c3d")],
                                    initialdir = subjectory_directory_1)
    plot_emg(emg_filename_case1[0],colorleft_case1,colorright_case1,title = "EMG "+case1_name)


if comparaison_bool:
    subject_kin_left_case2 = subject_kin_case2["left"]
    subject_kin_right_case2 = subject_kin_case2["right"]
    subject_spt_left_case2 = subject_spt_case2["left"]
    subject_spt_right_case2 = subject_spt_case2["right"]
    
    plot_kinematic(subject_kin_left_case2, subject_spt_left_case2, colorleft_case2,
                   subject_kin_right_case2, subject_spt_right_case2, colorright_case2,
                   norm_spt,norm_kin,
                   legend_1="Gauche "+case2_name,legend_2="Droite "+case2_name, title="Kinematic_"+case2_name)
    plot_spt(subject_spt_left_case2, colorleft_case2,
             subject_spt_right_case2, colorright_case2,
             legend_1="Gauche\n"+case2_name,legend_2="Droite\n"+case2_name, title="SPT_"+case2_name)
    
    
    plot_kinematic(subject_kin_left_case1, subject_spt_left_case1, colorleft_case1,
                   subject_kin_left_case2, subject_spt_left_case2, colorleft_case2,
                   norm_spt,norm_kin,
                   legend_1="Gauche "+case1_name,legend_2="Gauche "+case2_name, title="Kin_Comparaison_Left")
    plot_spt(subject_spt_left_case1, colorleft_case1,
             subject_spt_left_case2, colorleft_case2,
             legend_1="Gauche\n"+case1_name,legend_2="Gauche\n"+case2_name, title="SPT_Comparaison_Left")
    
    plot_kinematic(subject_kin_right_case1, subject_spt_right_case1, colorright_case1,
                   subject_kin_right_case2, subject_spt_right_case2, colorright_case2,
                   norm_spt,norm_kin,
                   legend_1="Droite "+case1_name, legend_2="Droite "+case2_name, title="Kin_Comparaison_Right")
    plot_spt(subject_spt_right_case1, colorright_case1,
             subject_spt_right_case2, colorright_case2,
             legend_1="Droite\n"+case1_name,legend_2="Droite\n"+case2_name, title="SPT_Comparaison_Right")
    if emg_bool:
        emg_filename_case2 = askopenfilenames(title="Choisir le fichies de tracer EMG condition "+case2_name+" :",filetypes=[("Fichiers C3D","*.c3d")],
                                    initialdir = subjectory_directory_2)
        plot_emg(emg_filename_case2[0],colorleft_case2,colorright_case2,title = "EMG "+case2_name)
