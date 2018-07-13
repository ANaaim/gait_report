# -*- coding: utf-8 -*-
"""
Created on Thu May 17 15:20:51 2018

@author: VICON
"""
from extraction_name_enf import extraction_name_enf as extraction_name_enf


def extraction_enf(filename):
    # extraction du fichier contenant les pas
    FP1 = 'invalid'
    FP2 = 'invalid'
    name_enf = extraction_name_enf(filename)

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
