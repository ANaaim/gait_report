# -*- coding: utf-8 -*-
import logging
from argparse import Namespace
import os
from tkFileDialog import askopenfilenames, askopenfilename
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

# test decorator
cgm2_1_DynaKad = modelDecorator.KneeCalibrationDecorator(cgm2_1).calibrate2dof('Left')

cgm2_1_DynaKad.calibrate2dof('Left')
cgm2_1_DynaKad.calibrate2dof('Right')
