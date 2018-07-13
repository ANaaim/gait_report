
# -*- coding: utf-8 -*-
import os


def extraction_name_enf(filename):
    f = []

    for (dirpath, dirnames, filenames) in os.walk(os.path.split(filename)[0]):
        f.extend(filenames)
        break
    validation = 0
    for ind, name_file in enumerate(f):
        if os.path.split(filename)[1][:-4] + '.Trial' in name_file:
            validation += 1
            ind_file = ind

    if validation == 1:
        name_enf = os.path.split(filename)[0] + '\\' + f[ind_file]

    return name_enf
