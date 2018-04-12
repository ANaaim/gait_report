# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 17:51:54 2018

@author: Alexandre Naaim 
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Extraction des informations contenu dans le fichier xls de Schwartz
def extract_Schwartz_norm(Speed="Free"):
    speed_mean_name = Speed +"Mean"
    speed_std_name = Speed+"SD"
    xls = pd.ExcelFile("Formatted- Schwartz2008.xlsx")
    jointRotations = xls.parse("Joint Rotations")
#    jointMoments = xls.parse("Joint Moments")
#    jointPower = xls.parse("Joint Power")
    
    cycleEvents = xls.parse("Cycle Events")
    
    
    param_spt_mean= {"percentage_CTFO":[],
                   "percentage_CTFS":[],
                   "stance_phase_perc" : []}
    
    param_spt_std = {"percentage_CTFO" : [],
                     "percentage_CTFS" : [],
                     "stance_phase_perc" : []}
    
    
    kinematic_mean = {"Pelvis_Fle": [],
                     "Pelvis_Abd": [],
                     "Pelvis_Ier": [],
                     "Hip_Fle": [],
                     "Hip_Abd": [],
                     "Hip_Ier": [],
                     "Knee_Fle": [],
                     "Knee_Abd": [],
                     "Knee_Ier": [],
                     "Ankle_Fle": [],
                     "Foot_Progression": [],
                     "Foot_tilt": [],
                     "X_value":[]}  
    
    kinematic_std = {"Pelvis_Fle": [],
                     "Pelvis_Abd": [],
                     "Pelvis_Ier": [],
                     "Hip_Fle": [],
                     "Hip_Abd": [],
                     "Hip_Ier": [],
                     "Knee_Fle": [],
                     "Knee_Abd": [],
                     "Knee_Ier": [],
                     "Ankle_Fle": [],
                     "Foot_Progression": [],
                     "Foot_tilt": []} 
    
    # free events
    param_spt_mean["percentage_CTFO"] = cycleEvents[ cycleEvents["Parameter"] == "Opposite Foot Off  [% cycle]"][speed_mean_name].values[0] * 100
    param_spt_mean["percentage_CTFS"] = cycleEvents[ cycleEvents["Parameter"] == "Opposite Foot Contact  [% cycle]"][speed_mean_name].values[0] * 100
    param_spt_mean["stance_phase_perc"] = cycleEvents[ cycleEvents["Parameter"] == "Ipsilateral Foot Off  [% cycle]"][speed_mean_name].values[0] * 100
    
    param_spt_std["percentage_CTFO"] = cycleEvents[ cycleEvents["Parameter"] == "Opposite Foot Off  [% cycle]"][speed_std_name].values[0]*100
    param_spt_std["percentage_CTFS"] = cycleEvents[ cycleEvents["Parameter"] == "Opposite Foot Contact  [% cycle]"][speed_std_name].values[0]*100
    param_spt_std["stance_phase_perc"] = cycleEvents[ cycleEvents["Parameter"] == "Ipsilateral Foot Off  [% cycle]"][speed_std_name].values[0]*100
    
    
    norm_spt = {"mean": param_spt_mean,"std": param_spt_std}
    
    
     # ----- Kinematic -----
     # Pelvis
    data0 = jointRotations [ jointRotations["Angle"] == "Pelvic Ant/Posterior Tilt"]
    kinematic_mean["X_value"] = data0['PercentageGaitCycle']*100
    kinematic_mean["Pelvis_Fle"] = data0[speed_mean_name]
    kinematic_std["Pelvis_Fle"] = data0[speed_mean_std]
    
    data1 = jointRotations [ jointRotations["Angle"] == "Pelvic Up/Down Obliquity"]
    kinematic_mean["Pelvis_Abd"] = data1[speed_mean_name]
    kinematic_std["Pelvis_Abd"] = data1[speed_mean_std]
    data2 = jointRotations [ jointRotations["Angle"] == "Pelvic Int/External Rotation"]
    kinematic_mean["Pelvis_Ier"] = data2[speed_mean_name]
    kinematic_std["Pelvis_Ier"] = data2[speed_mean_std]
    #hip
    data3 = jointRotations [ jointRotations["Angle"] == "Hip Flex/Extension"]
    kinematic_mean["Hip_Fle"] = data3[speed_mean_name]
    kinematic_std["Hip_Fle"] = data3[speed_mean_std]
    data4 = jointRotations [ jointRotations["Angle"] == "Hip Ad/Abduction"]
    kinematic_mean["Hip_Abd"] = data4[speed_mean_name]
    kinematic_std["Hip_Abd"] = data4[speed_mean_std]
    data5 = jointRotations [ jointRotations["Angle"] == "Hip Int/External Rotation"]
    kinematic_mean["Hip_Ier"] = data5[speed_mean_name]
    kinematic_std["Hip_Ier"] = data5[speed_mean_std]
    #knee
    data6 = jointRotations [ jointRotations["Angle"] == "Knee Flex/Extension"]
    kinematic_mean["Knee_Fle"] = data6[speed_mean_name]
    kinematic_std["Knee_Fle"] = data6[speed_mean_std]
    data7 = jointRotations [ jointRotations["Angle"] == "Knee Ad/Abduction"]
    kinematic_mean["Knee_Abd"] = data7[speed_mean_name]
    kinematic_std["Knee_Abd"] = data7[speed_mean_std]
    data8 = jointRotations [ jointRotations["Angle"] == "Knee Int/External Rotation"]
    kinematic_mean["Knee_Ier"] = data8[speed_mean_name]
    kinematic_std["Knee_Ier"] = data8[speed_mean_std]
    
    
    data9 = jointRotations [ jointRotations["Angle"] == "Ankle Dorsi/Plantarflexion"]
    kinematic_mean["Ankle_Fle"] = data9[speed_mean_name]
    kinematic_std["Ankle_Fle"] = data9[speed_mean_std]
    
    
    data10 = jointRotations [ jointRotations["Angle"] == "Foot Int/External Progression"]
    kinematic_mean["Foot_Progression"] = data10[speed_mean_name]
    kinematic_std["Foot_Progression"] = data10[speed_mean_std]
    norm_kin = {"mean": kinematic_mean,"std": kinematic_std}

return [norm_spt,norm_kin]

