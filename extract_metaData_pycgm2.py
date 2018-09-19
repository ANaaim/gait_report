# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 14:22:09 2018

@author: VICON
"""
import btk
# Extraction des paramètres pour la création du sujet


def extract_metaData_pycgm2(filename):
    reader = btk.btkAcquisitionFileReader()
    reader.SetFilename(str(filename))
    reader.Update()
    acq = reader.GetOutput()

    md = acq.GetMetaData()

    nameParameters = ["Bodymass",
                      "Height",
                      "LLegLength",
                      "RLegLength",
                      "LKneeWidth",
                      "RKneeWidth",
                      "LAnkleWidth",
                      "RAnkleWidth",
                      "LSoleDelta",
                      "RSoleDelta",
                      "InterAsisDistance",
                      "LAsisTrocanterDistance",
                      "LTibialTorsion",
                      "LThighRotation",
                      "LShankRotation",
                      "RAsisTrocanterDistance",
                      "RTibialTorsion",
                      "RThighRotation",
                      "RShankRotation"]

    extracted_param = {}
    for nameParameter in nameParameters:
        extracted_param[nameParameter] = md.FindChild("PROCESSING").\
            value().FindChild(nameParameter).\
            value().GetInfo().ToDouble()[0]

    required_mp = {
        "Bodymass": extracted_param['Bodymass'],
        "Height": extracted_param['Height'],
        "LeftLegLength": extracted_param['LLegLength'],
        "RightLegLength": extracted_param['RLegLength'],
        "LeftKneeWidth": extracted_param['LKneeWidth'],
        "RightKneeWidth": extracted_param['RKneeWidth'],
        "LeftAnkleWidth": extracted_param['LAnkleWidth'],
        "RightAnkleWidth": extracted_param['RAnkleWidth'],
        "LeftSoleDelta": extracted_param['LSoleDelta'],
        "RightSoleDelta": extracted_param['RSoleDelta']
    }
    optional_mp = {
        "InterAsisDistance": extracted_param['InterAsisDistance'],
        "LeftAsisTrocanterDistance": extracted_param['LAsisTrocanterDistance'],
        "LeftTibialTorsion": extracted_param['LTibialTorsion'],
        "LeftThighRotation": extracted_param['LThighRotation'],
        "LeftShankRotation": extracted_param['LShankRotation'],
        "RightAsisTrocanterDistance": extracted_param['RAsisTrocanterDistance'],
        "RightTibialTorsion": extracted_param['RTibialTorsion'],
        "RightThighRotation": extracted_param['RThighRotation'],
        "RightShankRotation": extracted_param['RShankRotation']
    }
    return required_mp, optional_mp


if __name__ == '__main__':
    filenametest = 'C:\Users\VICON\Desktop\Faux Patient\Patient 1\CORLIN Alexis Cal 04.c3d'
    extract_metaData_pycgm2(filenametest)
