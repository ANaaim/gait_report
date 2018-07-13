# -*- coding: utf-8 -*-
"""
Created on Thu Apr 05 16:02:17 2018

@author: AdminXPS
"""

import btk
import numpy as np


def kinematic(filename, side, extension):
    reader = btk.btkAcquisitionFileReader()
    reader.SetFilename(filename)
    reader.Update()
    acq = reader.GetOutput()

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

    # frq_point = float(acq.GetPointFrequency())
    # On enleve tout les evenements qui sont avant le premier foot strike du coté étudié
    first_event = FS[0]
    first_frame = acq.GetFirstFrame()
    # last_frame = acq.GetLastFrame()
    FS = [x - first_frame for x in FS if x >= first_event]
    FS_CL = [x - first_frame for x in FS_CL if x >= first_event]
    FO = [x - first_frame for x in FO if x >= first_event]
    FO_CL = [x - first_frame for x in FO_CL if x >= first_event]

    # Initialisation
    nb_cycle = len(FS) - 1
    kinematic = {"Pelvis_Fle": np.zeros((101, nb_cycle)),
                 "Pelvis_Abd": np.zeros((101, nb_cycle)),
                 "Pelvis_Ier": np.zeros((101, nb_cycle)),
                 "Hip_Fle": np.zeros((101, nb_cycle)),
                 "Hip_Abd": np.zeros((101, nb_cycle)),
                 "Hip_Ier": np.zeros((101, nb_cycle)),
                 "Knee_Fle": np.zeros((101, nb_cycle)),
                 "Knee_Abd": np.zeros((101, nb_cycle)),
                 "Knee_Ier": np.zeros((101, nb_cycle)),
                 "Ankle_Fle": np.zeros((101, nb_cycle)),
                 "Foot_Progression": np.zeros((101, nb_cycle)),
                 "Foot_tilt": np.zeros((101, nb_cycle))}

    for ind_cycle in range(nb_cycle):
        nb_frame = FS[ind_cycle + 1] - FS[ind_cycle]
        # paramètre pour l'interpolation sur 100 point
        x = np.linspace(0, nb_frame, 101)
        xp = np.linspace(0, nb_frame, nb_frame)
        # Pelvis
        f_flexion = acq.GetPoint(
            side_letter + 'PelvisAngles' + extension).GetValues()[FS[ind_cycle]:FS[ind_cycle + 1], 0]
        f_abduction = acq.GetPoint(
            side_letter + 'PelvisAngles' + extension).GetValues()[FS[ind_cycle]:FS[ind_cycle + 1], 1]
        f_rotation = acq.GetPoint(
            side_letter + 'PelvisAngles' + extension).GetValues()[FS[ind_cycle]:FS[ind_cycle + 1], 2]
        #        if side == "left":
        #            f_abduction = -f_abduction
        #            f_rotation = -f_rotation
        kinematic["Pelvis_Fle"][:, ind_cycle] = np.interp(x, xp, f_flexion)
        kinematic["Pelvis_Abd"][:, ind_cycle] = np.interp(x, xp, f_abduction)
        kinematic["Pelvis_Ier"][:, ind_cycle] = np.interp(x, xp, f_rotation)
        # Hip
        f_flexion = acq.GetPoint(
            side_letter + 'HipAngles' + extension).GetValues()[FS[ind_cycle]:FS[ind_cycle + 1], 0]
        f_abduction = acq.GetPoint(
            side_letter + 'HipAngles' + extension).GetValues()[FS[ind_cycle]:FS[ind_cycle + 1], 1]
        f_rotation = acq.GetPoint(
            side_letter + 'HipAngles' + extension).GetValues()[FS[ind_cycle]:FS[ind_cycle + 1], 2]
        kinematic["Hip_Fle"][:, ind_cycle] = np.interp(x, xp, f_flexion)
        kinematic["Hip_Abd"][:, ind_cycle] = np.interp(x, xp, f_abduction)
        kinematic["Hip_Ier"][:, ind_cycle] = np.interp(x, xp, f_rotation)

        # Knee
        f_flexion = acq.GetPoint(
            side_letter + 'KneeAngles' + extension).GetValues()[FS[ind_cycle]:FS[ind_cycle + 1], 0]
        f_abduction = acq.GetPoint(
            side_letter + 'KneeAngles' + extension).GetValues()[FS[ind_cycle]:FS[ind_cycle + 1], 1]
        f_rotation = acq.GetPoint(
            side_letter + 'KneeAngles' + extension).GetValues()[FS[ind_cycle]:FS[ind_cycle + 1], 2]
        kinematic["Knee_Fle"][:, ind_cycle] = np.interp(x, xp, f_flexion)
        kinematic["Knee_Abd"][:, ind_cycle] = np.interp(x, xp, f_abduction)
        kinematic["Knee_Ier"][:, ind_cycle] = np.interp(x, xp, f_rotation)

        # Ankle
        f_flexion = acq.GetPoint(
            side_letter + 'AnkleAngles' + extension).GetValues()[FS[ind_cycle]:FS[ind_cycle + 1], 0]
        f_progression = acq.GetPoint(
            side_letter + 'FootProgressAngles' + extension).GetValues()[FS[ind_cycle]:FS[ind_cycle + 1], 2]
        f_tilt = acq.GetPoint(
            side_letter + 'FootProgressAngles' + extension).GetValues()[FS[ind_cycle]:FS[ind_cycle + 1], 0]
        f_tilt = -f_tilt - 90
        kinematic["Ankle_Fle"][:, ind_cycle] = np.interp(x, xp, f_flexion)
        kinematic["Foot_Progression"][:, ind_cycle] = np.interp(x, xp, f_progression)
        kinematic["Foot_tilt"][:, ind_cycle] = np.interp(x, xp, f_tilt)

    return kinematic
