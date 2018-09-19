# -*- coding: utf-8 -*-
"""
Created on Thu Apr 05 12:55:11 2018

@author: AdminXPS
"""
import datetime
from param_spt_allfiles import param_spt_allfiles as param_spt_allfiles
from kinematic_allfiles import kinematic_allfiles as kinematic_allfiles
from kinetic_allfiles import kinetic_allfiles as kinetic_allfiles
from tkFileDialog import askopenfilenames, askopenfilename
from tkSimpleDialog import askstring
import tkMessageBox
from plot_kinematic import plot_kinematic as plot_kinematic
from plot_kinetic import plot_kinetic as plot_kinetic
from plot_spt import plot_spt as plot_spt
from extract_Schwartz_norm import extract_Schwartz_norm as extract_Schwartz_norm
from plot_emg import plot_emg as plot_emg
import os
import btk
from calculation_extraction_CGM import calculation_extraction_CGM as calculation_extraction_CGM

# ------------------------------------------------------------------------------
# Définition des répertoires de travail
# ------------------------------------------------------------------------------
# Repertoire contenant les sujets
data_directory = r'D:\DonneesViconInstallBMF'
# Repertoire ou seront généré les images pour le rapport
report_directory = r'C:\Users\VICON\Desktop\Rapport_Python'

# ------------------------------------------------------------------------------
# Définition de ce que l'utilisateur des choses qu'ils souhaitent faire
# comparaison, cinétique et emg
# ------------------------------------------------------------------------------
comparaison_bool = tkMessageBox.askyesno("Title",
                                         "Voulez vous comparer à d'autres résultats?")
kinetic_bool = tkMessageBox.askyesno("Title",
                                     "Voulez vous tracer la cinétique?")
emg_bool = tkMessageBox.askyesno("Title",
                                 "Voulez vous tracer les emg ?")

# Choix des fichiers du premiers repertoire
filenames_case1 = askopenfilenames(title="Choisir les fichiers de la première condition:",
                                   filetypes=[("Fichiers C3D", "*.c3d")],
                                   initialdir=data_directory)

# Remise en forme du nom du repertoire pour l'utiliser dans askopenfilename
one_filename = filenames_case1[0]
subject_directory_ind_1 = [i for i in range(len(one_filename)) if one_filename.startswith('/', i)]
subject_directory_1 = one_filename[0:subject_directory_ind_1[-1]]
subject_directory_initial = one_filename[0:subject_directory_ind_1[-1]]

# choix du fichier statique pour le cas 1
filenames_stat_case1 = askopenfilename(title="Choisir le fichiers de statique cas 1:",
                                       filetypes=[("Fichiers C3D", "*Cal*.c3d")],
                                       initialdir=subject_directory_1)

case1_name = askstring("Input", "Quelle est la première condition?")

[filenames_case1_postCGM, subject_directory_1_postCGM,
 extension_pycgm2_case1] = calculation_extraction_CGM(filenames_stat_case1, filenames_case1)

if comparaison_bool:
    filenames_case2 = askopenfilenames(title="Choisir les fichiers de la deuxième condition:", filetypes=[("Fichiers C3D", "*.c3d")],
                                       initialdir=subject_directory_initial)
    one_filename = filenames_case2[0]

    subject_directory_ind_2 = [i for i in range(
        len(one_filename)) if one_filename.startswith('/', i)]
    subject_directory_2 = one_filename[0:subject_directory_ind_1[-1]]
    # choix du fichier statique pour le cas 1
    filenames_stat_case2 = askopenfilename(title="Choisir le fichiers de statique cas 2:",
                                           filetypes=[("Fichiers C3D", "*Cal*.c3d")],
                                           initialdir=subject_directory_initial)
    case2_name = askstring("Input", "Quelle est la deuxième condition?")
    [filenames_case2_postCGM, subject_directory_2_postCGM,
     extension_pycgm2_case2] = calculation_extraction_CGM(filenames_stat_case2, filenames_case2)

# ------------------------------------------------------------------------------
# Création d'un répertoire ou seront stocké les donnés par sujet
# ------------------------------------------------------------------------------
# Extraction du nom du sujet pour créer un repertoire spécifique ou seront sauvegardé les images
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

# ------------------------------------------------------------------------------
# Calcul des paramètres spatio temporels et extraction de la cinétique et cinématique
# ------------------------------------------------------------------------------
subject_spt_case1 = param_spt_allfiles(filenames_case1_postCGM)

if kinetic_bool:
    subject_kinematic_case1, subject_kinetic_case1 = kinetic_allfiles(
        filenames_case1_postCGM, extension_pycgm2_case1)
else:
    subject_kinematic_case1 = kinematic_allfiles(filenames_case1_postCGM, extension_pycgm2_case1)

# si l'utilisateurs veut comparer à autre chose on choisit d'autre fichier
if comparaison_bool:
    if extension_pycgm2_case2 != extension_pycgm2_case1:
        tkMessageBox.showerror(
            'Error message', 'Les deux conditions n\'ont pas été traité avec le même modèle. Veuillez retraité les données ou utilisé le bon repertoire!')
        raise ValueError('Les deux conditions n\'ont pas été traité avec le même modèlé')

    # Calcul des paramètres spatio temporels
    subject_spt_case2 = param_spt_allfiles(filenames_case2_postCGM)
    if kinetic_bool:
        subject_kinematic_case2, subject_kinetic_case2 = kinetic_allfiles(
            filenames_case2_postCGM, extension_pycgm2_case2)
    else:
        subject_kinematic_case2 = kinematic_allfiles(
            filenames_case2_postCGM, extension_pycgm2_case2)


subject_kinematic_left_case1 = subject_kinematic_case1["left"]
subject_kinematic_right_case1 = subject_kinematic_case1["right"]

if kinetic_bool:
    subject_kinetic_left_case1 = subject_kinetic_case1["left"]
    subject_kinetic_right_case1 = subject_kinetic_case1["right"]

subject_spt_left_case1 = subject_spt_case1["left"]
subject_spt_right_case1 = subject_spt_case1["right"]

# ------------------------------------------------------------------------------
# Extraction des normes en fonction de la vitesse
# ------------------------------------------------------------------------------
# Calcul de la vitesse pour la norme de Schwartz 2008
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

[norm_spt, norm_kinematic, norm_kinetic] = extract_Schwartz_norm(Speed=Speed_norm)

# ------------------------------------------------------------------------------
# Tracer des graphiques
# ------------------------------------------------------------------------------
# Chaque cote contiendra paramètres spatio temporel, kinematic, kinetics
# extraction des event en list
colorleft_case1 = 'tab:red'
colorright_case1 = 'tab:green'
colorleft_case2 = 'tab:orange'
colorright_case2 = 'tab:blue'

plot_kinematic(subject_kinematic_left_case1, subject_spt_left_case1,
               colorleft_case1,
               subject_kinematic_right_case1, subject_spt_right_case1,
               colorright_case1,
               norm_spt, norm_kinematic, report_directory,
               legend_1="Gauche " + case1_name,
               legend_2="Droite " + case1_name,
               title="Kinematic_" + case1_name)

plot_spt(subject_spt_left_case1, colorleft_case1,
         subject_spt_right_case1, colorright_case1,
         norm_spt, report_directory,
         legend_1="Gauche\n" + case1_name,
         legend_2="Droite\n" + case1_name,
         title="SPT_" + case1_name)

if kinetic_bool:
    plot_kinetic(subject_kinetic_left_case1, subject_spt_left_case1,
                 colorleft_case1,
                 subject_kinetic_right_case1, subject_spt_right_case1,
                 colorright_case1,
                 norm_spt, norm_kinetic, report_directory,
                 legend_1="Gauche " + case1_name,
                 legend_2="Droite " + case1_name,
                 title="Kinetic_" + case1_name)

if emg_bool:
    windows_emg_name = "Choisir le fichies de tracer EMG condition " + \
        case1_name + " :"
    emg_filename_case1 = askopenfilenames(title=windows_emg_name,
                                          filetypes=[("Fichiers C3D", "*.c3d")],
                                          initialdir=subject_directory_1_postCGM)
    plot_emg(emg_filename_case1[0], colorleft_case1, colorright_case1,
             report_directory, title="EMG " + case1_name)


if comparaison_bool:
    if emg_bool:
        windows_emg_name = "Choisir le fichies de tracer EMG condition " + \
            case2_name + " :"
        emg_filename_case2 = askopenfilenames(title=windows_emg_name,
                                              filetypes=[("Fichiers C3D", "*.c3d")],
                                              initialdir=subject_directory_2_postCGM)
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
print(report_directory)
