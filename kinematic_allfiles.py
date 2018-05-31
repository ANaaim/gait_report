# -*- coding: utf-8 -*-
"""
Created on Thu Apr 05 17:19:30 2018

@author: AdminXPS
"""

import numpy as np
from kinematic import kinematic as kinematic


def kinematic_allfiles(filenames):

    for ind_file, filename in enumerate(filenames):
        filename_str = str(filename)
        print filename
        if ind_file == 0:
            left = kinematic(filename_str, "left")
            right = kinematic(filename_str, "right")
        else:
            left_temp = kinematic(filename_str, "left")
            right_temp = kinematic(filename_str, "right")
            for key in left:
                left[key] = np.concatenate((left[key], left_temp[key]), axis=1)
                right[key] = np.concatenate((right[key], right_temp[key]), axis=1)

    left_mean = {}
    right_mean = {}
    left_std = {}
    right_std = {}
    for key in left:
        left_mean[key] = np.mean(left[key], axis=1)
        left_std[key] = np.std(left[key], axis=1)
        right_mean[key] = np.mean(right[key], axis=1)
        right_std[key] = np.std(right[key], axis=1)

    left = {"mean": left_mean,
            "std": left_std}
    right = {"mean": right_mean,
             "std": right_std}
    subject_kin = {"left": left,
                   "right": right}

    return subject_kin
