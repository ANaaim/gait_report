# -*- coding: utf-8 -*-
"""
Created on Thu May 17 21:03:01 2018

@author: AdminXPS
"""
# pour demander à l'utilisateur de sélectionner des fichiers
from tkFileDialog import askopenfilenames

from extract_Schwartz_norm import extract_Schwartz_norm as extract_Schwartz_norm
from kinetic_allfiles import kinetic_allfiles as kinetic_allfiles
from param_spt_allfiles import param_spt_allfiles as param_spt_allfiles
from plot_kinetic import plot_kinetic as plot_kinetic

data_directory = 'C:\Users\AdminXPS\SynchronisationXPS\Professionel\GitHub\Data\Gait_report'

filenames_case1 = askopenfilenames(title="Choisir les fichiers de la première condition:",
                                   filetypes=[("Fichiers C3D", "*.c3d")],
                                   initialdir=data_directory)

subject_spt_case1 = param_spt_allfiles(filenames_case1)
subject_kinematic_case1, subject_kinetic_case1 = \
    kinetic_allfiles(filenames_case1)

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
[norm_spt, norm_kin, norm_kinetic] = extract_Schwartz_norm(Speed="Free")

plot_kinetic(subject_kin_left_case1, subject_spt_left_case1, colorleft_case1,
             subject_kin_right_case1, subject_spt_right_case1, colorright_case1,
             norm_spt, norm_kinetic,
             legend_1="Gauche " + 'test', legend_2="Droite " + 'Test',
             title="Kinematic_" + 'test')

for i in ['test', 'blabla']:
    print (i)
