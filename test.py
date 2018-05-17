# -*- coding: utf-8 -*-
"""
Created on Thu May 17 21:03:01 2018

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
from plot_spt import plot_spt as plot_spt
from extract_Schwartz_norm import extract_Schwartz_norm as extract_Schwartz_norm
from plot_emg import plot_emg as plot_emg
from plot_kinetic import plot_kinetic as plot_kinetic
from kinetic_allfiles import kinetic_allfiles as kinetic_allfiles

data_directory = 'C:\Users\AdminXPS\SynchronisationXPS\Professionel\GitHub\Data\Gait_report'


filenames_case1 = askopenfilenames(title="Choisir les fichiers de la première condition:",filetypes=[("Fichiers C3D","*.c3d")],
                                    initialdir = data_directory)

subject_spt_case1 = param_spt_allfiles(filenames_case1)
subject_kinematic_case1,subject_kinetic_case1  = kinetic_allfiles(filenames_case1)

subject_kin_left_case1 = subject_kinetic_case1["left"]
subject_kin_right_case1 = subject_kinetic_case1["right"]
subject_spt_left_case1 = subject_spt_case1["left"]
subject_spt_right_case1 = subject_spt_case1["right"]
# Chaque cote contiendra paramètres spatio temporel, kinematic, kinetics
# extraction des event en list
colorleft_case1 = 'tab:red'
colorright_case1 = 'tab:green'
colorleft_case2 = 'tab:orange'
colorright_case2 = 'tab:blue'

# Extraction des normes 
[norm_spt,norm_kin,norm_kinetic] = extract_Schwartz_norm(Speed="Free")

plot_kinetic(subject_kin_left_case1, subject_spt_left_case1, colorleft_case1,
               subject_kin_right_case1, subject_spt_right_case1, colorright_case1,
               norm_spt,norm_kinetic,
               legend_1="Gauche "+'test',legend_2="Droite "+'Test', title="Kinematic_"+'test')



