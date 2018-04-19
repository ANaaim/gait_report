# -*- coding: utf-8 -*-
"""
Created on Thu Apr 05 15:11:03 2018

@author: AdminXPS
"""

import btk 
import numpy as np

def param_spt(filename, side):
    reader = btk.btkAcquisitionFileReader()
    reader.SetFilename(filename)
    reader.Update()
    acq = reader.GetOutput()


    if side.lower() == "left":
        foot_marker = acq.GetPoint('LHEE').GetValues()
        foot_marker_ct = acq.GetPoint('RHEE').GetValues()
        side_cl = "right"
    elif side.lower() == "right":
        foot_marker = acq.GetPoint('RHEE').GetValues()
        foot_marker_ct = acq.GetPoint('LHEE').GetValues()
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
    # Les evenements ne sont pas forcement organisé dans le bon ordre
    FO.sort()
    FO_CL.sort()
    FS.sort()
    FS_CL.sort()
    
    frq_point = float(acq.GetPointFrequency())
    # On enleve tout les evenements qui sont avant le premier foot strike du coté étudié
    first_event = FS[0]
    first_frame = acq.GetFirstFrame()
    last_frame = acq.GetLastFrame()
    FS =    [x-first_frame for x in FS if x >= first_event]
    FS_CL = [x-first_frame for x in FS_CL if x >= first_event]
    FO =    [x-first_frame for x in FO if x >= first_event]
    FO_CL = [x-first_frame for x in FO_CL if x >= first_event]
    
    # définition de la direction de marche
    point =  acq.GetPoint('LPSI').GetValues()
    direction_walk = point[last_frame-first_frame,:] - point[0,:]
    direction_walk = np.argmax(np.abs(direction_walk))
    point = acq.GetPoint('LPSI').GetValues() -acq.GetPoint('RPSI').GetValues()
    direction_width = np.argmax(np.abs(point[0,:]))
    
    param_spt = {"cycle_time": [],
                 "cadence": [],
                 "length_cycle": [],
                 "walking_speed": [],
                 "step_length": [],
                 "step_sec": [],
                 "step_width": [],
                 "stance_phase_sec": [],
                 "stance_phase_perc": [],
                 "swing_phase_sec": [],
                 "swing_phase_perc": [],
                 "double_stance_sec": [],
                 "double_stance_perc": [],
                 "simple_stance_sec": [],
                 "simple_stance_perc": [],
                 "percentage_CTFO":[],
                 "percentage_CTFS":[]}
    
    for ind_cycle in range(len(FS)-1):   
        nb_frame_cycle = float(FS[ind_cycle+1] - FS[ind_cycle])
        
        # Temps du cycle (s)
        cycle_time = (FS[ind_cycle+1] - FS[ind_cycle])/frq_point
        param_spt["cycle_time"].append(cycle_time)
        # Cadence (step/mn)
        cadence = 120.0 / cycle_time
        param_spt["cadence"].append(cadence)
        # Longueur du cycle (m)
        length_cycle = np.abs(foot_marker[FS[ind_cycle+1],direction_walk] 
                              - foot_marker[FS[ind_cycle],direction_walk]) / 1000.0
        param_spt["length_cycle"].append(length_cycle)
        # Vitesse de marche (m/s)
        walking_speed = cadence * length_cycle / 120.0
        param_spt["walking_speed"].append(walking_speed)
        # Longueur du pas (m)
        step_length = np.abs(foot_marker_ct[FO[ind_cycle] ,direction_walk] 
                              - foot_marker[FS[ind_cycle] ,direction_walk]) / 1000.0
        param_spt["step_length"].append(step_length)
        # Temps Pas (frame, sec)
        step_frame = FS_CL[ind_cycle] - FS[ind_cycle]
        step_sec = step_frame / frq_point
        param_spt["step_sec"].append(step_sec)
        # Largeur pas (m)
        step_width = np.abs(foot_marker_ct[FO[ind_cycle] ,direction_width] 
                              - foot_marker[FS[ind_cycle] ,direction_width]) / 1000.0
        param_spt["step_width"].append(step_width)
    
        # Phase d'appui (frame, sec, pourcentage)
        stance_phase_frame = FO[ind_cycle] - FS[ind_cycle]
        stance_phase_sec = stance_phase_frame/frq_point
        stance_phase_perc = stance_phase_frame/nb_frame_cycle * 100
        param_spt["stance_phase_sec"].append(stance_phase_sec)
        param_spt["stance_phase_perc"].append(stance_phase_perc)
        
        # Phase oscillante (frame, sec, pourcentage)
        swing_phase_frame = FS[ind_cycle+1] - FO[ind_cycle]
        swing_phase_sec = swing_phase_frame/frq_point
        swing_phase_perc = swing_phase_frame/nb_frame_cycle * 100
        param_spt["swing_phase_sec"].append(swing_phase_sec)
        param_spt["swing_phase_perc"].append(swing_phase_perc)
        
        # Double appui (frame, sec, pourcentage)
        double_stance_frame = (FO_CL[ind_cycle] - FS[ind_cycle]
                              + FO[ind_cycle] - FS_CL[ind_cycle])
        double_stance_sec = double_stance_frame/frq_point
        double_stance_perc = double_stance_frame/nb_frame_cycle *100
        param_spt["double_stance_sec"].append(double_stance_sec)
        param_spt["double_stance_perc"].append(double_stance_perc)
        
        # Simple appui (frame, sec, pourcentage)
        simple_stance_frame =  FS_CL[ind_cycle] - FO_CL[ind_cycle]
        simple_stance_sec = simple_stance_frame / frq_point
        simple_stance_perc = simple_stance_frame / nb_frame_cycle * 100
        param_spt["simple_stance_sec"].append(simple_stance_sec)
        param_spt["simple_stance_perc"].append(simple_stance_perc)
        
        # Calcul des evenements controlateral pour affichage cinématique
        CTFS_frame = FS_CL[ind_cycle]-FS[ind_cycle]
        CTFO_frame = FO_CL[ind_cycle]-FS[ind_cycle]
        CTFS_perc = CTFS_frame/nb_frame_cycle * 100
        CTFO_perc = CTFO_frame/nb_frame_cycle * 100
        param_spt["percentage_CTFS"].append(CTFS_perc)
        param_spt["percentage_CTFO"].append(CTFO_perc)
        
    return param_spt
