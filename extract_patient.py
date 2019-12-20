# -*- coding: utf- -*-
from tkFileDialog import askdirectory
from fnmatch import fnmatch
import os
from extraction_info_enf import extraction_info_enf as extraction_info_enf
from extraction_name_c3d import extraction_name_c3d as extraction_name_c3d
from collections import defaultdict
import Tkinter as tk
from unidecode import unidecode


def extract_patient():
    root = str(askdirectory(initialdir=r'D:\DonneesViconInstallBMF'))
    #root = 'D:/DonneesViconInstallBMF/Pediatrie/BARTON Ethan'
    print(root)
    # root = '/some/directory'

    # ------------------------------------------------------------------------------
    # Extraction information from all enf file in the directory
    # ------------------------------------------------------------------------------
    pattern = "*trial*.enf"
    list_analysis = []
    dict_file = defaultdict()
    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch(name, pattern):
                final_path = os.path.join(path, name)
                [notes, notes_exist, description,
                    description_exist] = extraction_info_enf(final_path)
                if notes_exist and description_exist:
                    if 'Session' in os.path.split(path)[-1]:
                        type_analysis = description[12:-1]
                        # print(type_analysis)
                        # print(type(type_analysis))

                        # type_analysis_uni = unicode(type_analysis)
                        # print(type_analysis_uni)
                        Session_name = os.path.split(path)[-1]
                        Session_name = Session_name[:9]
                        # Session_name_uni = unidecode(Session_name)
                        # print(type(Session_name))
                        # print(Session_name+type_analysis)
                        list_analysis.append(Session_name + ' ' + type_analysis)
                        dict_file.setdefault(Session_name + ' ' +
                                             type_analysis, defaultdict())

                        if 'stati' in notes:
                            dict_file[str(Session_name) + ' ' +
                                      type_analysis].setdefault("static", []).append(final_path)
                        elif 'L' in notes or 'R' in notes:
                            dict_file[str(Session_name) + ' ' +
                                      type_analysis].setdefault("dynamic", []).append(final_path)
                        if 'emg' in notes or 'EMG' in notes:
                            dict_file[str(Session_name) + ' ' +
                                      type_analysis].setdefault("emg", []).append(final_path)

    final_list_case = list(set(list_analysis))
    final_list_case.sort()
    # ------------------------------------------------------------------------------
    # Choice by the user of the case he want to analyse
    # ------------------------------------------------------------------------------

    # Definition of all the option available
    # no comparison is added in the case we want to only do a case

    final_list_case_2 = list(final_list_case)
    final_list_case_2.append('no comparison')

    # case not found is added to
    OPTIONS = final_list_case
    OPTIONS.append('case not found')
    OPTION_2 = final_list_case_2

    master = tk.Tk()

    variable = tk.StringVar(master)
    variable_2 = tk.StringVar(master)

    variable.set(OPTIONS[0])  # default value
    variable_2.set(OPTION_2[-1])

    menu_1 = tk.OptionMenu(master, variable, *OPTIONS)
    menu_2 = tk.OptionMenu(master, variable_2, *OPTION_2)
    menu_1.place(relx=0.5, y=0, anchor='ne')
    menu_2.place(relx=0.5, y=0, anchor='nw')

    menu_1.pack()
    menu_2.pack()

    def close_window():
        master.destroy()

    button = tk.Button(master, text="Valeurs choisies", command=close_window)
    button.pack()

    tk.mainloop()

    # ------------------------------------------------------------------------------
    # Extraction information from all enf file in the directory
    # ------------------------------------------------------------------------------
    case_1_exist = False
    case_2_exist = False

    emg_case_1_exist = False
    emg_case_2_exist = False

    dynamic_list_c3d_case_1 = []
    dynamic_list_c3d_case_2 = []

    static_c3d_case_1 = []
    static_c3d_case_2 = []

    emg_c3d_case_1 = []
    emg_c3d_case_2 = []

    case_1 = variable.get()
    case_2 = variable_2.get()

    name_case_1 = case_1
    name_case_2 = case_2
    # Verification si tout est en ordre

    if case_1 == case_2:
        case_2 = 'no comparison'

    if case_2 != 'no comparison':
        dynamic_list_enf_case_2 = dict_file[case_2]['dynamic']
        static_list_enf_case_2 = dict_file[case_2]['static']

        for filename in dynamic_list_enf_case_2:
            dynamic_list_c3d_case_2.append(extraction_name_c3d(filename))

        # Tester qu'il y a bien qu'un seul fichier statique
        if len(static_list_enf_case_2) == 0:
            print(0)
        elif len(static_list_enf_case_2) > 1:
            print('Plus de 1')
        else:
            static_c3d_case_2 = extraction_name_c3d(static_list_enf_case_2[0])
            case_1_exist = True
        if 'emg' in dict_file[case_2]:
            emg_list_enf_case_2 = dict_file[case_2]['emg']
            if len(emg_list_enf_case_2) > 0:
                emg_case_2_exist = True
                emg_c3d_case_2 = extraction_name_c3d(emg_list_enf_case_2[0])
        else:
            emg_c3d_case_2 = []

    if case_1 != 'case not found':
        dynamic_list_enf_case_1 = dict_file[case_1]['dynamic']
        static_list_enf_case_1 = dict_file[case_1]['static']

        dynamic_list_c3d_case_1 = []

        for filename in dynamic_list_enf_case_1:
            dynamic_list_c3d_case_1.append(extraction_name_c3d(filename))

        # Tester qu'il y a bien qu'un seul fichier statique
        if len(static_list_enf_case_1) == 0:
            print(0)
        elif len(static_list_enf_case_1) > 1:
            print('Plus de 1')
        else:
            static_c3d_case_1 = extraction_name_c3d(static_list_enf_case_1[0])
            case_2_exist = True

        if 'emg' in dict_file[case_1]:
            emg_list_enf_case_1 = dict_file[case_1]['emg']
            if len(emg_list_enf_case_1) > 0:
                emg_case_1_exist = True
                emg_c3d_case_1 = extraction_name_c3d(emg_list_enf_case_1[0])
        else:
            emg_c3d_case_1 = []
    else:
        case_1_exist = False
        case_2_exist = False

    return [case_1_exist, name_case_1, dynamic_list_c3d_case_1, static_c3d_case_1, emg_case_1_exist, emg_c3d_case_1,
            case_2_exist, name_case_2, dynamic_list_c3d_case_2, static_c3d_case_2, emg_case_2_exist, emg_c3d_case_2]


if __name__ == "__main__":
    [case_1_exist, name_case_1, dynamic_list_c3d_case_1, static_c3d_case_1, emg_case_1_exist, emg_c3d_case_1,
     case_2_exist, name_case_2, dynamic_list_c3d_case_2, static_c3d_case_2, emg_case_2_exist, emg_c3d_case_2] = extract_patient()
