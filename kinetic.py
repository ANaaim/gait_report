# -*- coding: utf-8 -*-
"""
Created on Thu May 17 14:24:16 2018

@author: VICON
"""

import btk 
import numpy as np
from extraction_enf import extraction_enf as extraction_enf

filename  = 'D:\DonneesViconInstallBMF\Pediatrie\FAURE Aymeric\Session 3\FAUR Aym marchePN S3 10.c3d'


[FP1,FP2] = extraction_enf(filename)

reader = btk.btkAcquisitionFileReader()
reader.SetFilename(filename)
reader.Update()
acq = reader.GetOutput()
side = "left"
plateform_valid = [side==FP1,side==FP2]
   

if side.lower() == "left":
    side_letter = 'L'
    side_cl = "right"
elif side.lower() == "right":
    side_letter = 'R'
    side_cl = "left"
        
# Initialisation des lists contenant les evenements
FO = []
FO_CL = []
FS = []
FS_CL = []
for it in btk.Iterate(acq.GetEvents()): 
    if it.GetContext().lower() == side:
        if it.GetLabel() == 'Foot Strike':
            FS.append(it.GetFrame())
        elif it.GetLabel() == 'Foot Off':
            FO.append(it.GetFrame())
    elif it.GetContext().lower() == side_cl:
        if it.GetLabel() == 'Foot Strike':
            FS_CL.append(it.GetFrame())
        elif it.GetLabel() == 'Foot Off':
            FO_CL.append(it.GetFrame())
FO.sort()
FO_CL.sort()
FS.sort()
FS_CL.sort()
frq_point = float(acq.GetPointFrequency())
frq_analog = float(acq.GetAnalogFrequency())
factor_point_analog = frq_analog/frq_point
# On enleve tout les evenements qui sont avant le premier foot strike du coté étudié
first_event = FS[0]
first_frame = acq.GetFirstFrame()
last_frame = acq.GetLastFrame()
FS =    [x-first_frame for x in FS if x >= first_event]
FS_CL = [x-first_frame for x in FS_CL if x >= first_event]
FO =    [x-first_frame for x in FO if x >= first_event]
FO_CL = [x-first_frame for x in FO_CL if x >= first_event]

# Initialisation 
nb_cycle = len(FS)-1

fz1 = acq.GetAnalog("Fz1").GetValues()
fz2 = acq.GetAnalog("Fz2").GetValues()

nb_cycle = sum(plateform_valid)

kinematic = {"Pelvis_Fle": np.zeros((101,nb_cycle)),
             "Pelvis_Abd": np.zeros((101,nb_cycle)),
             "Pelvis_Ier": np.zeros((101,nb_cycle)),
             "Hip_Fle": np.zeros((101,nb_cycle)),
             "Hip_Abd": np.zeros((101,nb_cycle)),
             "Hip_Ier": np.zeros((101,nb_cycle)),
             "Knee_Fle": np.zeros((101,nb_cycle)),
             "Knee_Abd": np.zeros((101,nb_cycle)),
             "Knee_Ier": np.zeros((101,nb_cycle)),
             "Ankle_Fle": np.zeros((101,nb_cycle)),
             "Foot_Progression": np.zeros((101,nb_cycle)),
             "Foot_tilt": np.zeros((101,nb_cycle))}

kinetic = {"Hip_Power": np.zeros((101,nb_cycle)),
           "Knee_Power": np.zeros((101,nb_cycle)),
           "Ankle_Power": np.zeros((101,nb_cycle)),
           "Normalised_Ground_Reaction_X": np.zeros((101,nb_cycle)),
           "Normalised_Ground_Reaction_Y": np.zeros((101,nb_cycle)),
           "Normalised_Ground_Reaction_Z": np.zeros((101,nb_cycle)),
           "Hip_Moment": np.zeros((101,nb_cycle)),
           "Knee_Moment": np.zeros((101,nb_cycle)),
           "Ankle_Moment": np.zeros((101,nb_cycle))}

nb_cycle_total = len(FS)-1
cycle_valid = 0

for ind_cycle in range(nb_cycle_total):
    init_cycle =  FS[ind_cycle]
    end_cycle = FS[ind_cycle+1] 
    nb_frame = end_cycle - init_cycle

    nbr_frame_fz1 = sum(np.abs(fz1[int(init_cycle*factor_point_analog):
                                   int(end_cycle*factor_point_analog)])>5)/ factor_point_analog
    nbr_frame_fz2 = sum(np.abs(fz2[int(init_cycle*factor_point_analog):
                                   int(end_cycle*factor_point_analog)])>5)/ factor_point_analog
    condition_Plat1 = (nbr_frame_fz1/float(nb_frame))>0.15
    condition_Plat2 = (nbr_frame_fz1/float(nb_frame))>0.15
    
    if condition_Plat1 or condition_Plat2:
        # paramètre pour l'interpolation sur 100 point
        x = np.linspace(0, nb_frame, 101)
        xp = np.linspace(0,nb_frame,nb_frame)
        # Pelvis
        f_flexion =  acq.GetPoint(side_letter+'PelvisAngles').GetValues()[FS[ind_cycle]:FS[ind_cycle+1],0]
        f_abduction = acq.GetPoint(side_letter+'PelvisAngles').GetValues()[FS[ind_cycle]:FS[ind_cycle+1],1]
        f_rotation = acq.GetPoint(side_letter+'PelvisAngles').GetValues()[FS[ind_cycle]:FS[ind_cycle+1],2]
        kinematic["Pelvis_Fle"][:,cycle_valid] = np.interp(x, xp, f_flexion)
        kinematic["Pelvis_Abd"][:,cycle_valid] = np.interp(x, xp, f_abduction)
        kinematic["Pelvis_Ier"][:,cycle_valid] = np.interp(x, xp, f_rotation)
        # Hip
        f_flexion =  acq.GetPoint(side_letter+'HipAngles').GetValues()[FS[ind_cycle]:FS[ind_cycle+1],0]
        f_abduction = acq.GetPoint(side_letter+'HipAngles').GetValues()[FS[ind_cycle]:FS[ind_cycle+1],1]
        f_rotation = acq.GetPoint(side_letter+'HipAngles').GetValues()[FS[ind_cycle]:FS[ind_cycle+1],2]
        kinematic["Hip_Fle"][:,cycle_valid] = np.interp(x, xp, f_flexion)
        kinematic["Hip_Abd"][:,cycle_valid] = np.interp(x, xp, f_abduction)
        kinematic["Hip_Ier"][:,cycle_valid] = np.interp(x, xp, f_rotation)
    
        # Knee
        f_flexion =  acq.GetPoint(side_letter+'KneeAngles').GetValues()[FS[ind_cycle]:FS[ind_cycle+1],0]
        f_abduction = acq.GetPoint(side_letter+'KneeAngles').GetValues()[FS[ind_cycle]:FS[ind_cycle+1],1]
        f_rotation = acq.GetPoint(side_letter+'KneeAngles').GetValues()[FS[ind_cycle]:FS[ind_cycle+1],2]
        kinematic["Knee_Fle"][:,cycle_valid] = np.interp(x, xp, f_flexion)
        kinematic["Knee_Abd"][:,cycle_valid] = np.interp(x, xp, f_abduction)
        kinematic["Knee_Ier"][:,cycle_valid] = np.interp(x, xp, f_rotation)
        
        # Ankle
        f_flexion =  acq.GetPoint(side_letter+'AnkleAngles').GetValues()[FS[ind_cycle]:FS[ind_cycle+1],0]
        f_progression = acq.GetPoint(side_letter+'FootProgressAngles').GetValues()[FS[ind_cycle]:FS[ind_cycle+1],2]
        f_tilt = acq.GetPoint(side_letter+'FootProgressAngles').GetValues()[FS[ind_cycle]:FS[ind_cycle+1],0]
        f_tilt = -f_tilt - 90
        kinematic["Ankle_Fle"][:,cycle_valid] = np.interp(x, xp, f_flexion)
        kinematic["Foot_Progression"][:,cycle_valid] = np.interp(x, xp, f_progression)
        kinematic["Foot_tilt"][:,cycle_valid] = np.interp(x, xp, f_tilt)
        
        # kinetic
        power_hip = acq.GetPoint(side_letter+'HipPower').GetValues()[FS[ind_cycle]:FS[ind_cycle+1],2]
        power_knee = acq.GetPoint(side_letter+'KneePower').GetValues()[FS[ind_cycle]:FS[ind_cycle+1],2]
        power_ankle = acq.GetPoint(side_letter+'AnklePower').GetValues()[FS[ind_cycle]:FS[ind_cycle+1],2]
        kinetic["Hip_Power"][:,cycle_valid] = np.interp(x, xp, power_hip)
        kinetic["Knee_Power"][:,cycle_valid] = np.interp(x, xp, power_knee)
        kinetic["Ankle_Power"][:,cycle_valid] = np.interp(x, xp, power_ankle)
        
        normal_GRF_X = acq.GetPoint(side_letter+'GroundReactionForce').GetValues()[FS[ind_cycle]:FS[ind_cycle+1],0]
        normal_GRF_Y = acq.GetPoint(side_letter+'GroundReactionForce').GetValues()[FS[ind_cycle]:FS[ind_cycle+1],1]
        normal_GRF_Z = acq.GetPoint(side_letter+'GroundReactionForce').GetValues()[FS[ind_cycle]:FS[ind_cycle+1],2] 
        kinetic["Normalised_Ground_Reaction_X"][:,cycle_valid] = np.interp(x, xp, normal_GRF_X)
        kinetic["Normalised_Ground_Reaction_Y"][:,cycle_valid] = np.interp(x, xp, normal_GRF_Y)
        kinetic["Normalised_Ground_Reaction_Z"][:,cycle_valid] = np.interp(x, xp, normal_GRF_Z)
        
        moment_hip = acq.GetPoint(side_letter+'HipMoment').GetValues()[FS[ind_cycle]:FS[ind_cycle+1],2]
        moment_knee = acq.GetPoint(side_letter+'KneeMoment').GetValues()[FS[ind_cycle]:FS[ind_cycle+1],2]
        moment_ankle = acq.GetPoint(side_letter+'AnkleMoment').GetValues()[FS[ind_cycle]:FS[ind_cycle+1],2]
        kinetic["Hip_Moment"][:,cycle_valid] = np.interp(x, xp, moment_hip)
        kinetic["Knee_Moment"][:,cycle_valid] = np.interp(x, xp, moment_knee)
        kinetic["Ankle_Moment"][:,cycle_valid] = np.interp(x, xp, moment_ankle)
        
        cycle_valid +=1
    
    