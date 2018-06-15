# -*- coding: utf-8 -*-
"""
Created on Thu May 17 16:51:58 2018

@author: VICON
"""
import numpy as np

from extraction_enf import extraction_enf as extraction_enf
from kinetic import kinetic as kinetic


def kinetic_allfiles(filenames):
    valid_file = []
    for ind_file, filename in enumerate(filenames):
        if extraction_enf(filename) != ['invalid', 'invalid']:
            valid_file.append(filename)

    # initialisation
    for ind_file, filename in enumerate(valid_file):
        filename_str = str(filename)
        print filename
        if ind_file == 0:
            left_kinematic, left_kinetic = kinetic(filename_str, "left")
            right_kinematic, right_kinetic = kinetic(filename_str, "right")

        else:
            left_kinematic_temp, left_kinetic_temp = kinetic(filename_str, "left")
            right_kinematic_temp, right_kinetic_temp = kinetic(filename_str, "right")

            for key in left_kinematic:
                left_kinematic[key] = np.concatenate(
                    (left_kinematic[key], left_kinematic_temp[key]), axis=1)
                right_kinematic[key] = np.concatenate(
                    (right_kinematic[key], right_kinematic_temp[key]), axis=1)
            for key in left_kinetic:
                left_kinetic[key] = np.concatenate(
                    (left_kinetic[key], left_kinetic_temp[key]), axis=1)
                right_kinetic[key] = np.concatenate(
                    (right_kinetic[key], right_kinetic_temp[key]), axis=1)

    left_mean_kinematic = {}
    right_mean_kinematic = {}
    left_std_kinematic = {}
    right_std_kinematic = {}
    for key in left_kinematic:
        left_mean_kinematic[key] = np.mean(left_kinematic[key], axis=1)
        left_std_kinematic[key] = np.std(left_kinematic[key], axis=1)
        right_mean_kinematic[key] = np.mean(right_kinematic[key], axis=1)
        right_std_kinematic[key] = np.std(right_kinematic[key], axis=1)

    left_kinematic = {"mean": left_mean_kinematic,
                      "std": left_std_kinematic,
                      "all": left_kinematic}
    right_kinematic = {"mean": right_mean_kinematic,
                       "std": right_std_kinematic,
                       "all": right_kinematic}
    subject_kinematic = {"left": left_kinematic,
                         "right": right_kinematic}

    left_mean_kinetic = {}
    right_mean_kinetic = {}
    left_std_kinetic = {}
    right_std_kinetic = {}
    for key in left_kinetic:
        left_mean_kinetic[key] = np.mean(left_kinetic[key], axis=1)
        left_std_kinetic[key] = np.std(left_kinetic[key], axis=1)
        right_mean_kinetic[key] = np.mean(right_kinetic[key], axis=1)
        right_std_kinetic[key] = np.std(right_kinetic[key], axis=1)

    left_kinetic = {"mean": left_mean_kinetic,
                    "std": left_std_kinetic,
                    "all": left_kinetic}
    right_kinetic = {"mean": right_mean_kinetic,
                     "std": right_std_kinetic,
                     "all": right_kinetic}
    subject_kinetic = {"left": left_kinetic,
                       "right": right_kinetic}

    return [subject_kinematic, subject_kinetic]
