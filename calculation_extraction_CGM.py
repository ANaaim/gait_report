# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 12:29:11 2018

@author: Alexandre Naaim
"""
from calculation_kindyn import calculation_kindyn as calculation_kindyn
import os


def calculation_extraction_CGM(filenames_stat, filenames):
    # calculs de la cinématique avec la tool box et changement du repertoire
    # contenant les fichiers ==> Les fichiers sont généré dans un dossier Post_CGM2_1
    # contenu dans le même dossier que les données initiales
    calculation_kindyn(filenames_stat, filenames)
    # On change le noms des fichier qui seront utilisé pour l'extraction des données
    # Pour cela on va rajouté le dossier Post_CGM2_1 entre le dossier ou était contenu
    # le fichier initial et le nouveau fichier
    filenames_postCGM = ()
    for name_file in filenames:
        temp = os.path.join(os.path.split(filenames[0])[
                            0], 'Post_CGM2_1', os.path.split(name_file)[1])
        filenames_postCGM = filenames_postCGM + (temp,)
    # filenames_case1 = filenames_case1_postCGM
    subject_directory_postCGM = os.path.split(filenames_postCGM[0])[0]
    # Definition de l'extension pgm en fonction du repertoire dans lequel il est
    last_repertory = os.path.split(subject_directory_postCGM)[1]
    if 'CGM' in last_repertory:
        posCGM = last_repertory.find('CGM')
        extension_pycgm2 = str('_cgm' + last_repertory[posCGM + 3:])
    else:
        extension_pycgm2 = ''

    return filenames_postCGM, subject_directory_postCGM, extension_pycgm2
