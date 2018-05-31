# -*- coding: utf-8 -*-
"""
Created on Thu May 17 15:20:51 2018

@author: VICON
"""
import os


def extraction_enf(filename):
    # extraction du fichier contenant les pas
    f = []
    FP1 = 'invalid'
    FP2 = 'invalid'
    for (dirpath, dirnames, filenames) in os.walk(os.path.split(filename)[0]):
        f.extend(filenames)
        break
    validation = 0
    for ind, name_file in enumerate(f):
        if os.path.split(filename)[1][:-4] + '.Trial' in name_file:
            validation += 1
            ind_file = ind

    if validation == 1:
        name_enf = os.path.split(filename)[0] + '\\' + f[ind_file]

        fd = open(name_enf, 'r')
        text = fd.readlines()
        for lign in text:
            if 'FP1' in lign:
                if 'eft' in lign:
                    FP1 = 'left'
                elif 'ight' in lign:
                    FP1 = 'right'
            elif 'FP2' in lign:
                if 'eft' in lign:
                    FP2 = 'left'
                elif 'ight' in lign:
                    FP2 = 'right'
    return [FP1, FP2]
