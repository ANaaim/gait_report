# -*- coding: utf-8 -*-
"""
Created on Thu Apr 05 15:50:02 2018

@author: AdminXPS
"""

import numpy as np
from param_spt import param_spt as param_spt

def param_spt_allfiles(filenames):
    
    for ind_file, filename in enumerate(filenames):
        filename_str = str(filename)
        print filename
        if ind_file == 0:
            left = param_spt(filename_str,"left")
            right =  param_spt(filename_str,"right")
        else:
            left_temp = param_spt(filename_str,"left")
            right_temp = param_spt(filename_str,"right")
            for key in left:
                left[key].extend(left_temp[key])
                right[key].extend(right_temp[key])
    
    left_mean ={}
    right_mean = {}
    left_std ={}
    right_std = {}
    for key in left:
        left_mean[key] = np.mean(left[key])
        left_std[key] = np.std(left[key])
        right_mean[key] = np.mean(right[key])
        right_std[key] = np.std(right[key])
    left = {"mean": left_mean,
            "std": left_std}
    right = {"mean": right_mean,
            "std": right_std} 
    subject_spt = {"left": left,
               "right": right}
    return subject_spt