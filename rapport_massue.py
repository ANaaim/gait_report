# -*- coding: utf-8 -*-
"""
Created on Thu Apr 05 12:55:11 2018

@author: Alexandre Naaim
"""

import datetime
from param_spt_allfiles import param_spt_allfiles as param_spt_allfiles
from kinematic_allfiles import kinematic_allfiles as kinematic_allfiles
from kinetic_allfiles import kinetic_allfiles as kinetic_allfiles
# pour demander à l'utilisateur de sélectionner des fichiers
from tkFileDialog import askopenfilenames
from tkSimpleDialog import askstring
import tkMessageBox
from plot_kinematic import plot_kinematic as plot_kinematic
from plot_kinetic import plot_kinetic as plot_kinetic
from plot_spt import plot_spt as plot_spt
from extract_Schwartz_norm import extract_Schwartz_norm as extract_Schwartz_norm
from plot_emg import plot_emg as plot_emg
import os
import btk

comparaison_bool = tkMessageBox.askyesno("Title",
                                         "Voulez vous comparer à d'autres résultats?")
kinetic_bool = tkMessageBox.askyesno("Title",
                                     "Voulez vous tracer la cinétique?")
emg_bool = tkMessageBox.askyesno("Title",
                                 "Voulez vous tracer les emg ?")

# On choisit les premiers fichiers
data_directory = r'D:\DonneesViconInstallBMF'
report_directory = r'C:\Users\VICON\Desktop\Rapport_Python'

filenames_case1 = askopenfilenames(title="Choisir les fichiers de la première condition:", filetypes=[("Fichiers C3D", "*.c3d")],
                                   initialdir=data_directory)

one_filename = filenames_case1[0]
subject_directory_ind_1 = [i for i in range(len(one_filename)) if one_filename.startswith('/', i)]
subject_directory_1 = one_filename[0:subject_directory_ind_1[-1]]
subject_name = str(one_filename[subject_directory_ind_1[-3] + 1:subject_directory_ind_1[-2]])

reader = btk.btkAcquisitionFileReader()
reader.SetFilename(str(one_filename))
reader.Update()
acq = reader.GetOutput()

md = acq.GetMetaData()
subject_name = md.FindChild("SUBJECTS").\
    value().FindChild('NAMES').\
    value().GetInfo().ToString()[0]
# Creation of the file containing the data of the patient for today
now = datetime.datetime.now()
date_today = now.strftime("%Y_%m_%d_%Hh%M")
report_directory = os.path.join(report_directory, subject_name.strip(), date_today)

if not os.path.isdir(report_directory):
    os.makedirs(report_directory)


case1_name = askstring("Input", "Quelle est la première condition?")

# Calcul des paramètres spatio temporels
subject_spt_case1 = param_spt_allfiles(filenames_case1)
if kinetic_bool:
    subject_kinematic_case1, subject_kinetic_case1 = kinetic_allfiles(filenames_case1)
else:
    subject_kinematic_case1 = kinematic_allfiles(filenames_case1)

# si l'utilisateurs veut comparer à autre chose on choisit d'autre fichier
if comparaison_bool:
    filenames_case2 = askopenfilenames(title="Choisir les fichiers de la deuxième condition:", filetypes=[("Fichiers C3D", "*.c3d")],
                                       initialdir=subject_directory_1)
    one_filename = filenames_case2[0]
    subject_directory_ind_2 = [i for i in range(
        len(one_filename)) if one_filename.startswith('/', i)]
    subjectory_directory_2 = one_filename[0:subject_directory_ind_1[-1]]
    # Calcul des paramètres spatio temporels
    subject_spt_case2 = param_spt_allfiles(filenames_case2)
    if kinetic_bool:
        subject_kinematic_case2, subject_kinetic_case2 = kinetic_allfiles(filenames_case2)
    else:
        subject_kinematic_case2 = kinematic_allfiles(filenames_case2)
    case2_name = askstring("Input", "Quelle est la deuxième condition?")

subject_kinematic_left_case1 = subject_kinematic_case1["left"]
subject_kinematic_right_case1 = subject_kinematic_case1["right"]
if kinetic_bool:
    subject_kinetic_left_case1 = subject_kinetic_case1["left"]
    subject_kinetic_right_case1 = subject_kinetic_case1["right"]

subject_spt_left_case1 = subject_spt_case1["left"]
subject_spt_right_case1 = subject_spt_case1["right"]
# Chaque cote contiendra paramètres spatio temporel, kinematic, kinetics
# extraction des event en list
colorleft_case1 = 'tab:red'
colorright_case1 = 'tab:green'
colorleft_case2 = 'tab:orange'
colorright_case2 = 'tab:blue'

# Définition de la norme de Schwartz utilisé
bool_vitesse = tkMessageBox.askyesno("Title",
                                     "Voulez vous utiliser une norme adaptée à la vitesse ?")
if bool_vitesse:
    vitesse_norm = subject_spt_right_case1["mean"]["walking_speed_adm"]
    if vitesse_norm < 0.227:
        Speed_norm = "VerySlow"
    elif vitesse_norm >= 0.227 and vitesse_norm < 0.363:
        Speed_norm = "Slow"
    elif vitesse_norm >= 0.363 and vitesse_norm < 0.500:
        Speed_norm = "Free"
    elif vitesse_norm >= 0.500 and vitesse_norm < 0.636:
        Speed_norm = "Fast"
    else:
        Speed_norm = "VeryFast"
    bool_vitesse_2 = tkMessageBox.askyesno("Title",
                                           "La norme choisi est :" + Speed_norm +
                                           " .Souhaitez vous la conserver ?")
    if not bool_vitesse_2:
        Speed_norm = "Free"
else:
    Speed_norm = "Free"
# Extraction des normes
[norm_spt, norm_kinematic, norm_kinetic] = extract_Schwartz_norm(Speed=Speed_norm)


plot_kinematic(subject_kinematic_left_case1, subject_spt_left_case1,
               colorleft_case1,
               subject_kinematic_right_case1, subject_spt_right_case1,
               colorright_case1,
               norm_spt, norm_kinematic, report_directory,
               legend_1="Gauche " + case1_name,
               legend_2="Droite " + case1_name,
               title="Kinematic_" + case1_name)

if kinetic_bool:
    plot_kinetic(subject_kinetic_left_case1, subject_spt_left_case1,
                 colorleft_case1,
                 subject_kinetic_right_case1, subject_spt_right_case1,
                 colorright_case1,
                 norm_spt, norm_kinetic, report_directory,
                 legend_1="Gauche " + case1_name,
                 legend_2="Droite " + case1_name,
                 title="Kinetic_" + case1_name)

plot_spt(subject_spt_left_case1, colorleft_case1,
         subject_spt_right_case1, colorright_case1,
         norm_spt, report_directory,
         legend_1="Gauche\n" + case1_name,
         legend_2="Droite\n" + case1_name,
         title="SPT_" + case1_name)

if emg_bool:
    windows_emg_name = "Choisir le fichies de tracer EMG condition " + \
        case1_name + " :"
    emg_filename_case1 = askopenfilenames(title=windows_emg_name,
                                          filetypes=[("Fichiers C3D", "*.c3d")],
                                          initialdir=subject_directory_1)
    plot_emg(emg_filename_case1[0], colorleft_case1, colorright_case1,
             report_directory, title="EMG " + case1_name)


if comparaison_bool:
    if emg_bool:
        windows_emg_name = "Choisir le fichies de tracer EMG condition " + \
            case2_name + " :"
        emg_filename_case2 = askopenfilenames(title=windows_emg_name,
                                              filetypes=[("Fichiers C3D", "*.c3d")],
                                              initialdir=subjectory_directory_2)
        plot_emg(emg_filename_case2[0], colorleft_case2, colorright_case2,
                 report_directory, title="EMG " + case2_name)

    subject_kinematic_left_case2 = subject_kinematic_case2["left"]
    subject_kinematic_right_case2 = subject_kinematic_case2["right"]
    if kinetic_bool:
        subject_kinetic_left_case2 = subject_kinetic_case2["left"]
        subject_kinetic_right_case2 = subject_kinetic_case2["right"]

    subject_spt_left_case2 = subject_spt_case2["left"]
    subject_spt_right_case2 = subject_spt_case2["right"]

    plot_kinematic(subject_kinematic_left_case2, subject_spt_left_case2,
                   colorleft_case2,
                   subject_kinematic_right_case2, subject_spt_right_case2,
                   colorright_case2,
                   norm_spt, norm_kinematic, report_directory,
                   legend_1="Gauche " + case2_name,
                   legend_2="Droite " + case2_name,
                   title="Kinematic_" + case2_name)

    plot_spt(subject_spt_left_case2, colorleft_case2,
             subject_spt_right_case2, colorright_case2,
             norm_spt, report_directory,
             legend_1="Gauche\n" + case2_name,
             legend_2="Droite\n" + case2_name,
             title="SPT_" + case2_name)

    plot_kinematic(subject_kinematic_left_case1, subject_spt_left_case1,
                   colorleft_case1,
                   subject_kinematic_left_case2, subject_spt_left_case2,
                   colorleft_case2,
                   norm_spt, norm_kinematic, report_directory,
                   legend_1="Gauche " + case1_name,
                   legend_2="Gauche " + case2_name,
                   title="Kinematic_Comparaison_Left")

    plot_spt(subject_spt_left_case1, colorleft_case1,
             subject_spt_left_case2, colorleft_case2,
             norm_spt, report_directory,
             legend_1="Gauche\n" + case1_name,
             legend_2="Gauche\n" + case2_name,
             title="SPT_Comparaison_Left")

    plot_kinematic(subject_kinematic_right_case1, subject_spt_right_case1,
                   colorright_case1,
                   subject_kinematic_right_case2, subject_spt_right_case2,
                   colorright_case2,
                   norm_spt, norm_kinematic, report_directory,
                   legend_1="Droite " + case1_name,
                   legend_2="Droite " + case2_name,
                   title="Kinematic_Comparaison_Right")

    plot_spt(subject_spt_right_case1, colorright_case1,
             subject_spt_right_case2, colorright_case2,
             norm_spt, report_directory,
             legend_1="Droite\n" + case1_name,
             legend_2="Droite\n" + case2_name,
             title="SPT_Comparaison_Right")

    if kinetic_bool:
        plot_kinetic(subject_kinetic_left_case2, subject_spt_left_case2,
                     colorleft_case2,
                     subject_kinetic_right_case2, subject_spt_right_case2,
                     colorright_case2,
                     norm_spt, norm_kinetic, report_directory,
                     legend_1="Gauche " + case2_name,
                     legend_2="Droite " + case2_name,
                     title="Kinetic_" + case2_name)

        plot_kinetic(subject_kinetic_left_case1, subject_spt_left_case1,
                     colorleft_case1,
                     subject_kinetic_left_case2, subject_spt_left_case2,
                     colorleft_case2,
                     norm_spt, norm_kinetic, report_directory,
                     legend_1="Gauche " + case1_name,
                     legend_2="Gauche " + case2_name,
                     title="Kinetic_Comparaison_Left")

        plot_kinetic(subject_kinetic_right_case1, subject_spt_right_case1,
                     colorright_case1,
                     subject_kinetic_right_case2, subject_spt_right_case2,
                     colorright_case2,
                     norm_spt, norm_kinetic, report_directory,
                     legend_1="Droite " + case1_name,
                     legend_2="Droite " + case2_name,
                     title="Kinetic_Comparaison_Right")
