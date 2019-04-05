# -*- coding: utf-8 -*-
"""
Created on 05/04/2019

@author: Alexandre Naaim
"""

import pandas as pd


def Age_to_Age_min(Age):
    print(Age)
    if Age < 5:
        Agemin = 5
    elif Age == 13:
        Agemin = 12
    elif Age > 13 and Age < 18:
        Agemin = 14
    elif Age >= 18 and Age < 30:
        Agemin = 18
    elif Age >= 30 and Age < 40:
        Agemin = 30
    elif Age >= 40 and Age < 50:
        Agemin = 40
    elif Age >= 50 and Age < 60:
        Agemin = 50
    elif Age >= 60 and Age < 70:
        Agemin = 60
    elif Age >= 70 and Age < 75:
        Agemin = 70
    elif Age >= 75 and Age < 80:
        Agemin = 75
    elif Age >= 80 and Age < 85:
        Agemin = 80
    elif Age >= 85:
        Agemin = 85
    else:
        Agemin = Age
    return Agemin


def Optimize_Pace(walking_speed, Age, Gender):
    Agemin = 40
    Gender = 'Male'
    walking_speed = 1.6
    walking_speed_cm = walking_speed * 100

    xls = pd.ExcelFile("Normals_SPT_Kid.xlsx")
    SPT = xls.parse("SPT_age")
    extracted_value = SPT[(SPT['Age (min)'] == Agemin) & (SPT['Gender'] == Gender)]
    Fast_speed_limit = extracted_value[extracted_value['Pace'] == "Fast"]
    Fast_speed_limit = Fast_speed_limit["Velocity (cm./sec.)min"].values[0]
    Normal_speed_limit = extracted_value[(extracted_value['Pace'] == 'Normal')]
    Normal_speed_limit = Normal_speed_limit["Velocity (cm./sec.)min"].values[0]
    print(Normal_speed_limit)

    if walking_speed_cm < Normal_speed_limit:
        Pace = 'Slow'
    elif walking_speed_cm >= Normal_speed_limit and walking_speed_cm < Fast_speed_limit:
        Pace = 'Normal'
    else:
        Pace = 'Fast'
    return Pace


def extract_GaitRite_norm(walking_speed, Age, Gender):

    Agemin = Age_to_Age_min(Age)
    if Agemin > 69:
        Pace = 'Normal'
    elif Agemin == 14:
        Pace = 'Normal'
    else:
        Pace = Optimize_Pace(walking_speed, Age, Gender)
    print(Pace)
    xls = pd.ExcelFile("Normals_SPT_Kid.xlsx")
    SPT = xls.parse("SPT_age")

    extracted_value = SPT[(SPT['Pace'] == Pace) & (
        SPT['Age (min)'] == Agemin) & (SPT['Gender'] == Gender)]

    param_spt_mean = {"cycle_time": [],
                      "cadence": [],
                      "length_cycle": [],
                      "walking_speed": [],
                      "step_length": [],
                      "step_width": [],
                      "stance_phase_perc": [],
                      "swing_phase_perc": [],
                      "double_stance_perc": [],
                      "simple_stance_perc": [],
                      "percentage_CTFO": [],
                      "percentage_CTFS": []}
    param_spt_std = {"cycle_time": [],
                     "cadence": [],
                     "length_cycle": [],
                     "walking_speed": [],
                     "step_length": [],
                     "step_width": [],
                     "stance_phase_perc": [],
                     "swing_phase_perc": [],
                     "double_stance_perc": [],
                     "simple_stance_perc": [],
                     "percentage_CTFO": [],
                     "percentage_CTFS": []}

    param_spt_mean["cadence"] = (extracted_value["Cadence (steps/min.)max"].values[0] +
                                 extracted_value["Cadence (steps/min.)min"].values[0]) / 2
    param_spt_std["cadence"] = (extracted_value["Cadence (steps/min.)max"].values[0] -
                                extracted_value["Cadence (steps/min.)min"].values[0]) / 2

    param_spt_mean["walking_speed"] = (extracted_value["Velocity (cm./sec.)max"].values[0] +
                                       extracted_value["Velocity (cm./sec.)min"].values[0]) / 2 * 100
    param_spt_std["walking_speed"] = (extracted_value["Velocity (cm./sec.)max"].values[0] -
                                      extracted_value["Velocity (cm./sec.)min"].values[0]) / 2 * 100

    param_spt_mean["cycle_time"] = (extracted_value["Stride Time (sec.)max"].values[0] +
                                    extracted_value["Stride Time (sec.)min"].values[0]) / 2
    param_spt_std["cycle_time"] = (extracted_value["Stride Time (sec.)max"].values[0] -
                                   extracted_value["Stride Time (sec.)min"].values[0]) / 2

    param_spt_mean["length_cycle"] = (extracted_value["Stride Length (cm.)max"].values[0] +
                                      extracted_value["Stride Length (cm.)min"].values[0]) / 2 * 100
    param_spt_std["length_cycle"] = (extracted_value["Stride Length (cm.)max"].values[0] -
                                     extracted_value["Stride Length (cm.)min"].values[0]) / 2 * 100

    param_spt_mean["step_sec"] = (extracted_value["Step Time (sec.)max"].values[0] +
                                  extracted_value["Step Time (sec.)min"].values[0]) / 2
    param_spt_std["step_sec"] = (extracted_value["Step Time (sec.)max"].values[0] -
                                 extracted_value["Step Time (sec.)min"].values[0]) / 2

    param_spt_mean["step_length"] = (extracted_value["Step Length (cm.)max"].values[0] +
                                     extracted_value["Step Length (cm.)min"].values[0]) / 2 * 100
    param_spt_std["step_length"] = (extracted_value["Step Length (cm.)max"].values[0] -
                                    extracted_value["Step Length (cm.)min"].values[0]) / 2 * 100

    param_spt_mean["step_width"] = (extracted_value["Stride Width (cm.)max"].values[0] +
                                    extracted_value["Stride Width (cm.)min"].values[0]) / 2 * 100
    param_spt_std["step_width"] = (extracted_value["Stride Width (cm.)max"].values[0] -
                                   extracted_value["Stride Width (cm.)min"].values[0]) / 2 * 100

    param_spt_mean["stance_phase_perc"] = (extracted_value["Stance %max"].values[0] +
                                           extracted_value["Stance %min"].values[0]) / 2
    param_spt_std["stance_phase_perc"] = (extracted_value["Stance %max"].values[0] -
                                          extracted_value["Stance %min"].values[0]) / 2

    param_spt_mean["simple_stance_perc"] = (extracted_value["Single Support %max"].values[0] +
                                            extracted_value["Single Support %min"].values[0]) / 2
    param_spt_std["simple_stance_perc"] = (extracted_value["Single Support %max"].values[0] -
                                           extracted_value["Single Support %min"].values[0]) / 2

    param_spt_mean["double_stance_perc"] = (extracted_value["Total D. Support %max"].values[0] +
                                            extracted_value["Total D. Support %min"].values[0]) / 2
    param_spt_std["double_stance_perc"] = (extracted_value["Total D. Support %max"].values[0] -
                                           extracted_value["Total D. Support %min"].values[0]) / 2

    param_spt_mean["swing_phase_perc"] = (extracted_value["Swing %max"].values[0] +
                                          extracted_value["Swing %min"].values[0]) / 2
    param_spt_std["swing_phase_perc"] = (extracted_value["Swing %max"].values[0] -
                                         extracted_value["Swing %min"].values[0]) / 2

    # It is half the double support
    param_spt_mean["percentage_CTFO"] = (extracted_value["Total D. Support %max"].values[0] +
                                         extracted_value["Total D. Support %min"].values[0]) / 4
    param_spt_std["percentage_CTFO"] = (extracted_value["Total D. Support %max"].values[0] -
                                        extracted_value["Total D. Support %min"].values[0]) / 4

    # It is half the double support
    param_spt_mean["percentage_CTFS"] = param_spt_mean["percentage_CTFO"] + \
        param_spt_mean["simple_stance_perc"]

    param_spt_std["percentage_CTFS"] = param_spt_std["percentage_CTFO"]

    norm_spt = {"mean": param_spt_mean, "std": param_spt_std}

    return norm_spt
