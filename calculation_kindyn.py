# -*- coding: utf-8 -*-
import logging
from argparse import Namespace
import os
# from tkFileDialog import askopenfilenames, askopenfilename
from extraction_enf import extraction_enf as extraction_enf
from extract_metaData_pycgm2 import extract_metaData_pycgm2 as extract_metaData_pycgm2
from extraction_name_enf import extraction_name_enf as extraction_name_enf
# pyCGM2 libraries
import pyCGM2
# from pyCGM2 import enums
from pyCGM2.Model.CGM2.coreApps import cgm2_1, cgmUtils
from pyCGM2.Model import modelDecorator
from pyCGM2.Tools import btkTools
from pyCGM2.Utils import files
# from pyCGM2.Eclipse import vskTools

from shutil import copy2


# Choix des fichiers à traiter
# report_directory = r'C:\Users\VICON\Desktop\Faux Patient'

# filenames_stat = askopenfilename(title="Choisir le fichiers de statique :",
#                                  filetypes=[("Fichiers C3D", "*Cal*.c3d")],
#                                  initialdir=report_directory)

# filenames_dyn = askopenfilenames(title="Choisir les fichiers de la première condition:",
#                                  filetypes=[("Fichiers C3D", "*.c3d")],
#                                  initialdir=os.path.split(filenames_stat)[0])


def calculation_kindyn(filenames_stat, filenames_dyn):

    # Definition des différents répertoires
    DATA_PATH = os.path.split(filenames_stat)[0] + '\\'
    DATA_PATH_OUT = os.path.join(DATA_PATH, 'Post_CGM2_1')
    if not os.path.isdir(DATA_PATH_OUT):
        os.mkdir(DATA_PATH_OUT)
    DATA_PATH_OUT = os.path.join(DATA_PATH, 'Post_CGM2_1') + '\\'
    calibrateFilenameLabelled = str(os.path.split(filenames_stat)[1])

    # Setting pour la toolbox pycgm2
    args = Namespace()
    args.leftFlatFoot = None
    args.rightFlatFoot = None
    args.markerDiameter = None
    args.pointSuffix = None
    args.fileSuffix = None
    args.mfpa = None
    args.proj = None
    args.check = True

    # --------------------------GLOBAL SETTINGS ------------------------------------
    # global setting ( in user/AppData)
    settings = files.openJson(pyCGM2.CONFIG.PYCGM2_APPDATA_PATH, "CGM2_1-pyCGM2.settings")

    fileSuffix = None
    # settings overloading
    argsManager = cgmUtils.argsManager_cgm(settings, args)
    leftFlatFoot = argsManager.getLeftFlatFoot()
    rightFlatFoot = argsManager.getRightFlatFoot()
    markerDiameter = argsManager.getMarkerDiameter()
    pointSuffix = argsManager.getPointSuffix("cgm2_1")
    momentProjection = argsManager.getMomentProjection()
    mfpa = argsManager.getManualForcePlateAssign()

    # Translator
    translators = files.getTranslators(DATA_PATH, "CGM2_1.translators")
    if not translators:
        translators = settings["Translators"]

    # Choix de la methode de Hanche
    hjcMethod = settings["Calibration"]["HJC"]

    # Extraction des meta data
    required_mp, optional_mp = extract_metaData_pycgm2(filenames_stat)

    # Statique
    model, acqStatic = cgm2_1.calibrate(DATA_PATH, calibrateFilenameLabelled,
                                        translators, required_mp, optional_mp,
                                        leftFlatFoot, rightFlatFoot,
                                        markerDiameter, hjcMethod,
                                        pointSuffix)

    for ind_file, filename in enumerate(filenames_dyn):
        plateforme_mpa = ''
        name_enf = extraction_name_enf(filename)
        # on fait une copy du fichier ENF pour pouvoir utiliser la génération de rapport
        copy2(name_enf, DATA_PATH_OUT)
        [FP1, FP2] = extraction_enf(filename)

        if FP1 == 'right':
            plateforme_mpa += 'R'
        elif FP1 == 'left':
            plateforme_mpa += 'L'
        else:
            plateforme_mpa += 'X'

        if FP2 == 'right':
            plateforme_mpa += 'R'
        elif FP2 == 'left':
            plateforme_mpa += 'L'
        else:
            plateforme_mpa += 'X'

        reconstructFilenameLabelled = os.path.split(filename)[1]
        # Fitting
        # Pour le premier fichier on 'décore' le modèle pour pouvoir faire
        # la méthode de dynakad (il faut que le modele ait été utilisé en dynamique)
        if ind_file == 0:
            print(filename)
            acqGait = cgm2_1.fitting(model, DATA_PATH, reconstructFilenameLabelled,
                                     translators,
                                     markerDiameter,
                                     pointSuffix,
                                     plateforme_mpa, momentProjection)
            modelDecorator.KneeCalibrationDecorator(model).calibrate2dof('Left')
            modelDecorator.KneeCalibrationDecorator(model).calibrate2dof('Right')

        acqGait = cgm2_1.fitting(model, DATA_PATH, reconstructFilenameLabelled,
                                 translators,
                                 markerDiameter,
                                 pointSuffix,
                                 plateforme_mpa, momentProjection)
        # writer
        if fileSuffix is not None:
            c3dFilename = str(reconstructFilenameLabelled[:-4] +
                              "-modelled-" + fileSuffix + ".c3d")
        else:
            c3dFilename = str(reconstructFilenameLabelled)

        btkTools.smartWriter(acqGait, str(DATA_PATH_OUT + c3dFilename))
        logging.info("c3d file (%s) generated" % (c3dFilename))
    return DATA_PATH_OUT
