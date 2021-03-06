# -*- coding: utf-8 -*-
"""
Created on Thu May 17 14:24:16 2018

@author: VICON
"""

import btk
import numpy as np

from extraction_enf import extraction_enf as extraction_enf


def kinetic(filename, side, extension):
    [FP1, FP2] = extraction_enf(filename)

    reader = btk.btkAcquisitionFileReader()
    reader.SetFilename(filename)
    reader.Update()
    acq = reader.GetOutput()
    plateform_valid = [side == FP1, side == FP2]

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
    factor_point_analog = frq_analog / frq_point
    # On enleve tout les evenements qui sont avant le premier foot strike du coté étudié
    first_event = FS[0]
    first_frame = acq.GetFirstFrame()
    # last_frame = acq.GetLastFrame()
    FS = [x - first_frame for x in FS if x >= first_event]
    FS_CL = [x - first_frame for x in FS_CL if x >= first_event]
    FO = [x - first_frame for x in FO if x >= first_event]
    FO_CL = [x - first_frame for x in FO_CL if x >= first_event]

    # Coefficient d'adimension pour les moments
    md = acq.GetMetaData()
    leg_lenght = md.FindChild("PROCESSING").\
        value().FindChild(side_letter + 'LegLength').\
        value().GetInfo().ToDouble()[0] / 1000.0

    body_mass = md.FindChild("PROCESSING").\
        value().FindChild('Bodymass').\
        value().GetInfo().ToDouble()[0]

    gravity = 9.81
    # In nexus the unit of the moment is Nmm / kg and in the Schwartz norm the data are
    # in N m/kg (just divided by the mass of the subject)
    # coeff_moment = leg_lenght * body_mass * gravity
    coeff_moment = 1000
    # Initialisation
    # nb_cycle = len(FS) - 1

    fz1 = acq.GetAnalog("Fz1").GetValues()
    fz2 = acq.GetAnalog("Fz2").GetValues()

    # nb_cycle = sum(plateform_valid)

    nb_cycle = len(FS) - 1
    cycle_valid = 0
    for ind_cycle in range(nb_cycle):
        init_cycle = FS[ind_cycle]
        end_cycle = FS[ind_cycle + 1]
        nb_frame = end_cycle - init_cycle

        nbr_frame_fz1 = sum(np.abs(fz1[int(init_cycle * factor_point_analog):
                                       int(end_cycle * factor_point_analog)]) > 5) / factor_point_analog
        nbr_frame_fz2 = sum(np.abs(fz2[int(init_cycle * factor_point_analog):
                                       int(end_cycle * factor_point_analog)]) > 5) / factor_point_analog
        condition_Plat1 = (nbr_frame_fz1 / float(nb_frame)) > 0.15 and plateform_valid[0]
        condition_Plat2 = (nbr_frame_fz2 / float(nb_frame)) > 0.15 and plateform_valid[1]
        if condition_Plat1 or condition_Plat2:
            cycle_valid += 1

    kinematic = {"Pelvis_Fle": np.zeros((101, cycle_valid)),
                 "Pelvis_Abd": np.zeros((101, cycle_valid)),
                 "Pelvis_Ier": np.zeros((101, cycle_valid)),
                 "Hip_Fle": np.zeros((101, cycle_valid)),
                 "Hip_Abd": np.zeros((101, cycle_valid)),
                 "Hip_Ier": np.zeros((101, cycle_valid)),
                 "Knee_Fle": np.zeros((101, cycle_valid)),
                 "Knee_Abd": np.zeros((101, cycle_valid)),
                 "Knee_Ier": np.zeros((101, cycle_valid)),
                 "Ankle_Fle": np.zeros((101, cycle_valid)),
                 "Foot_Progression": np.zeros((101, cycle_valid)),
                 "Foot_tilt": np.zeros((101, cycle_valid))}

    kinetic = {"Pelvis_Abd": np.zeros((101, cycle_valid)),
               "Hip_Abd": np.zeros((101, cycle_valid)),
               "Knee_Abd": np.zeros((101, cycle_valid)),
               "Hip_Fle": np.zeros((101, cycle_valid)),
               "Knee_Fle": np.zeros((101, cycle_valid)),
               "Ankle_Fle": np.zeros((101, cycle_valid)),
               "Hip_Power": np.zeros((101, cycle_valid)),
               "Knee_Power": np.zeros((101, cycle_valid)),
               "Ankle_Power": np.zeros((101, cycle_valid)),
               "Normalised_Ground_Reaction_X": np.zeros((101, cycle_valid)),
               "Normalised_Ground_Reaction_Y": np.zeros((101, cycle_valid)),
               "Normalised_Ground_Reaction_Z": np.zeros((101, cycle_valid)),
               "Hip_Moment": np.zeros((101, cycle_valid)),
               "Knee_Moment": np.zeros((101, cycle_valid)),
               "Ankle_Moment": np.zeros((101, cycle_valid)),
               "Hip_Moment_abd": np.zeros((101, cycle_valid)),
               "Knee_Moment_abd": np.zeros((101, cycle_valid)),
               "Ankle_Moment_abd": np.zeros((101, cycle_valid))}

    cycle_valid = 0
    for ind_cycle in range(nb_cycle):
        init_cycle = FS[ind_cycle]
        end_cycle = FS[ind_cycle + 1]
        nb_frame = end_cycle - init_cycle

        nbr_frame_fz1 = sum(np.abs(fz1[int(init_cycle * factor_point_analog):
                                       int(end_cycle * factor_point_analog)]) > 5) / factor_point_analog
        nbr_frame_fz2 = sum(np.abs(fz2[int(init_cycle * factor_point_analog):
                                       int(end_cycle * factor_point_analog)]) > 5) / factor_point_analog
        condition_Plat1 = (nbr_frame_fz1 / float(nb_frame)) > 0.15 and plateform_valid[0]
        condition_Plat2 = (nbr_frame_fz2 / float(nb_frame)) > 0.15 and plateform_valid[1]

        if condition_Plat1 or condition_Plat2:
            # paramètre pour l'interpolation sur 100 point
            x = np.linspace(0, nb_frame, 101)
            xp = np.linspace(0, nb_frame, nb_frame)
            # Pelvis
            print side_letter + 'PelvisAngles' + extension
            f_flexion = acq.GetPoint(
                side_letter + 'PelvisAngles' + extension).GetValues()[FS[ind_cycle]:FS[ind_cycle + 1], 0]
            f_abduction = acq.GetPoint(
                side_letter + 'PelvisAngles' + extension).GetValues()[FS[ind_cycle]:FS[ind_cycle + 1], 1]
            f_rotation = acq.GetPoint(
                side_letter + 'PelvisAngles' + extension).GetValues()[FS[ind_cycle]:FS[ind_cycle + 1], 2]
            kinematic["Pelvis_Fle"][:, cycle_valid] = np.interp(x, xp, f_flexion)
            kinematic["Pelvis_Abd"][:, cycle_valid] = np.interp(x, xp, f_abduction)
            kinematic["Pelvis_Ier"][:, cycle_valid] = np.interp(x, xp, f_rotation)

            kinetic["Pelvis_Abd"][:, cycle_valid] = np.interp(x, xp, f_abduction)

            # Hip
            f_flexion = acq.GetPoint(
                side_letter + 'HipAngles' + extension).GetValues()[FS[ind_cycle]:FS[ind_cycle + 1], 0]
            f_abduction = acq.GetPoint(
                side_letter + 'HipAngles' + extension).GetValues()[FS[ind_cycle]:FS[ind_cycle + 1], 1]
            f_rotation = acq.GetPoint(
                side_letter + 'HipAngles' + extension).GetValues()[FS[ind_cycle]:FS[ind_cycle + 1], 2]
            kinematic["Hip_Fle"][:, cycle_valid] = np.interp(x, xp, f_flexion)
            kinematic["Hip_Abd"][:, cycle_valid] = np.interp(x, xp, f_abduction)
            kinematic["Hip_Ier"][:, cycle_valid] = np.interp(x, xp, f_rotation)

            kinetic["Hip_Fle"][:, cycle_valid] = np.interp(x, xp, f_flexion)
            kinetic["Hip_Abd"][:, cycle_valid] = np.interp(x, xp, f_abduction)

            # Knee
            f_flexion = acq.GetPoint(
                side_letter + 'KneeAngles' + extension).GetValues()[FS[ind_cycle]:FS[ind_cycle + 1], 0]
            f_abduction = acq.GetPoint(
                side_letter + 'KneeAngles' + extension).GetValues()[FS[ind_cycle]:FS[ind_cycle + 1], 1]
            f_rotation = acq.GetPoint(
                side_letter + 'KneeAngles' + extension).GetValues()[FS[ind_cycle]:FS[ind_cycle + 1], 2]

            kinematic["Knee_Fle"][:, cycle_valid] = np.interp(x, xp, f_flexion)
            kinematic["Knee_Abd"][:, cycle_valid] = np.interp(x, xp, f_abduction)
            kinematic["Knee_Ier"][:, cycle_valid] = np.interp(x, xp, f_rotation)

            kinetic["Knee_Fle"][:, cycle_valid] = np.interp(x, xp, f_flexion)
            kinetic["Knee_Abd"][:, cycle_valid] = np.interp(x, xp, f_abduction)

            # Ankle
            f_flexion = acq.GetPoint(
                side_letter + 'AnkleAngles' + extension).GetValues()[FS[ind_cycle]:FS[ind_cycle + 1], 0]
            f_progression = acq.GetPoint(side_letter + 'FootProgressAngles' + extension).GetValues()[
                FS[ind_cycle]:FS[ind_cycle + 1], 2]
            f_tilt = acq.GetPoint(
                side_letter + 'FootProgressAngles' + extension).GetValues()[FS[ind_cycle]:FS[ind_cycle + 1], 0]
            f_tilt = -f_tilt - 90
            kinematic["Ankle_Fle"][:, cycle_valid] = np.interp(x, xp, f_flexion)
            kinematic["Foot_Progression"][:, cycle_valid] = np.interp(x, xp, f_progression)
            kinematic["Foot_tilt"][:, cycle_valid] = np.interp(x, xp, f_tilt)

            kinetic["Ankle_Fle"][:, cycle_valid] = np.interp(x, xp, f_flexion)

            # kinetic
            power_hip = acq.GetPoint(
                side_letter + 'HipPower' + extension).GetValues()[FS[ind_cycle]:FS[ind_cycle + 1], 2]
            power_knee = acq.GetPoint(
                side_letter + 'KneePower' + extension).GetValues()[FS[ind_cycle]:FS[ind_cycle + 1], 2]
            power_ankle = acq.GetPoint(
                side_letter + 'AnklePower' + extension).GetValues()[FS[ind_cycle]:FS[ind_cycle + 1], 2]
            kinetic["Hip_Power"][:, cycle_valid] = np.interp(x, xp, power_hip)
            kinetic["Knee_Power"][:, cycle_valid] = np.interp(x, xp, power_knee)
            kinetic["Ankle_Power"][:, cycle_valid] = np.interp(x, xp, power_ankle)

            normal_GRF_X = acq.GetPoint(
                side_letter + 'NormalisedGRF').GetValues()[FS[ind_cycle]:FO[ind_cycle], 0]
            normal_GRF_X = np.append(normal_GRF_X, np.zeros((FS[ind_cycle + 1] - FO[ind_cycle], 1)))

            normal_GRF_Y = acq.GetPoint(
                side_letter + 'NormalisedGRF').GetValues()[FS[ind_cycle]:FO[ind_cycle], 1]
            normal_GRF_Y = np.append(normal_GRF_Y, np.zeros((FS[ind_cycle + 1] - FO[ind_cycle], 1)))

            normal_GRF_Z = acq.GetPoint(
                side_letter + 'NormalisedGRF').GetValues()[FS[ind_cycle]:FO[ind_cycle], 2]
            normal_GRF_Z = np.append(normal_GRF_Z, np.zeros((FS[ind_cycle + 1] - FO[ind_cycle], 1)))

            kinetic["Normalised_Ground_Reaction_X"][:,
                                                    cycle_valid] = -np.interp(x, xp, normal_GRF_X)
            kinetic["Normalised_Ground_Reaction_Y"][:, cycle_valid] = np.interp(x, xp, normal_GRF_Y)
            kinetic["Normalised_Ground_Reaction_Z"][:, cycle_valid] = np.interp(x, xp, normal_GRF_Z)

            moment_hip = acq.GetPoint(
                side_letter + 'HipMoment' + extension).GetValues()[FS[ind_cycle]:FS[ind_cycle + 1], 0]
            moment_knee = acq.GetPoint(
                side_letter + 'KneeMoment' + extension).GetValues()[FS[ind_cycle]:FS[ind_cycle + 1], 0]
            moment_ankle = acq.GetPoint(
                side_letter + 'AnkleMoment' + extension).GetValues()[FS[ind_cycle]:FS[ind_cycle + 1], 0]
            kinetic["Hip_Moment"][:, cycle_valid] = np.interp(x, xp, moment_hip) / coeff_moment
            kinetic["Knee_Moment"][:, cycle_valid] = np.interp(x, xp, moment_knee) / coeff_moment
            kinetic["Ankle_Moment"][:, cycle_valid] = np.interp(x, xp, moment_ankle) / coeff_moment

            moment_hip_abd = acq.GetPoint(
                side_letter + 'HipMoment' + extension).GetValues()[FS[ind_cycle]:FS[ind_cycle + 1], 1]
            moment_knee_abd = acq.GetPoint(
                side_letter + 'KneeMoment' + extension).GetValues()[FS[ind_cycle]:FS[ind_cycle + 1], 1]
            moment_ankle_abd = acq.GetPoint(
                side_letter + 'AnkleMoment' + extension).GetValues()[FS[ind_cycle]:FS[ind_cycle + 1], 1]

            kinetic["Hip_Moment_abd"][:, cycle_valid] = np.interp(
                x, xp, moment_hip_abd) / coeff_moment
            kinetic["Knee_Moment_abd"][:, cycle_valid] = np.interp(
                x, xp, moment_knee_abd) / coeff_moment
            kinetic["Ankle_Moment_abd"][:, cycle_valid] = np.interp(
                x, xp, moment_ankle_abd) / coeff_moment

            cycle_valid += 1
    return [kinematic, kinetic]


if __name__ == '__main__':
    filename = 'C:\Users\AdminXPS\SynchronisationXPS\
    Professionel\GitHub\Data\
    Gait_report\FAUR Aym marchePN S3 10.c3d'

    [kinematic, kinetic] = kinetic(filename, 'left', '')
