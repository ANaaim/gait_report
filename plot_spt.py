# -*- coding: utf-8 -*-
"""
Created on Fri Apr 06 14:57:56 2018

@author: AdminXPS
"""

import os

import matplotlib.patches as patches
# pour demander à l'utilisateur de sélectionner des fichiers
import matplotlib.pyplot as plt
import numpy as np


#
# filenames_case1 = askopenfilenames(title="Choisir les fichiers de la première condition:",filetypes=[("Fichiers C3D","*.c3d")])
#
# Calcul des paramètres spatio temporels
# subject_spt_case1 = param_spt_allfiles(filenames_case1)
#
# name_case_1 = "left"
# name_case_2 = "right"
# color_case_1 = 'tab:orange'
# color_case_2 = 'tab:blue'
#
# subject_spt_case1 = subject_spt_case1["left"]
# subject_spt_case1 = subject_spt_case1["right"]


def plot_spt(subject_spt_case1, color_case_1,
             subject_spt_case2, color_case_2, 
             norm_spt, report_directory,
             legend_1="", legend_2="", title="SPT"):
    for spt_type in ["normal", "adm"]:
        if spt_type == "normal":
            list_spt = ["cadence",
                        "length_cycle",
                        "walking_speed",
                        "step_length",
                        "step_width",
                        "stance_phase_perc",
                        "swing_phase_perc",
                        "simple_stance_perc",
                        "double_stance_perc"]
            name_spt = ["Cadence (Pas/min)",
                        "Longueur du cycle (m)",
                        "Vitesse de marche (m/s)",
                        "Longueur du pas (m)",
                        "Largeur du pas (m)",
                        "Phase d\'appui (%)",
                        "Phase oscillante (%)",
                        "Simple appui (%)",
                        "Double appui (%)"]
            list_echelle = [[0, 150],
                            [0, 1.5],
                            [0, 1.5],
                            [0, 1],
                            [0, 0.3],
                            [0, 80],
                            [0, 80],
                            [0, 80],
                            [0, 40]]
        elif spt_type == "adm":
            list_spt = ["cadence_adm",
                        "length_cycle_adm",
                        "walking_speed_adm",
                        "step_length_adm",
                        "step_width_adm",
                        "stance_phase_perc",
                        "swing_phase_perc",
                        "simple_stance_perc",
                        "double_stance_perc"]
            name_spt = ["Cadence (adm)",
                        "Longueur du cycle (adm)",
                        "Vitesse de marche (adm)",
                        "Longueur du pas (adm)",
                        "Largeur du pas (adm)",
                        "Phase d\'appui (%)",
                        "Phase oscillante (%)",
                        "Simple appui (%)",
                        "Double appui (%)"]
            list_echelle = [[0, 50],
                            [0, 2],
                            [0, 0.8],
                            [0, 1.5],
                            [0, 0.5],
                            [0, 80],
                            [0, 80],
                            [0, 80],
                            [0, 40]]
            title = title + "_adm"
            
        size_first_graph = 3
        indice_list = np.array(range(10)) + size_first_graph
    
        # fig_new,axis_new = plt.subplots(len(list_spt)*2+1,1,figsize=(8.27,11.69),dpi=200)
        fig = plt.figure(figsize=(8.27, 11.69), dpi=100)
        grid = plt.GridSpec(size_first_graph + len(list_spt), 1, wspace=0.4, hspace=1.5)
    
        ax_temp = fig.add_subplot(grid[0:size_first_graph, 0])  # axis_new[0]
        ax_temp.set_ylim([0, 3])
        ax_temp.set_xlim([0, 100])
        plt.title("% Gait cycle")
        Case1_FO = subject_spt_case1["mean"]["stance_phase_perc"]
        Case2_FO = subject_spt_case2["mean"]["stance_phase_perc"]
        Casenorm_FO = norm_spt["mean"]["stance_phase_perc"]
        
        ax_temp.add_patch(patches.Rectangle((0, 0), 100, 1, facecolor=color_case_1, zorder=-10))
        ax_temp.add_patch(patches.Rectangle((0, 1), 100, 1, facecolor=color_case_2, zorder=-10))
        ax_temp.add_patch(patches.Rectangle((0, 2), 100, 1, facecolor=(0.5, 0.5, 0.5), zorder=-10))
        
        ax_temp.add_patch(
            patches.Rectangle((Case1_FO, 0), 100 - Case1_FO, 1, alpha=0.5, facecolor=[0.8, 0.8, 0.8], zorder=0))
        ax_temp.add_patch(
            patches.Rectangle((Case2_FO, 1), 100 - Case2_FO, 1, alpha=0.5, facecolor=[0.8, 0.8, 0.8], zorder=0))
        ax_temp.add_patch(
            patches.Rectangle((Casenorm_FO, 2), 100 - Casenorm_FO, 1, alpha=0.5, facecolor=[0.8, 0.8, 0.8], zorder=0))
        
        # Left
        # C_FO
        Case1_CFO_up = subject_spt_case1["mean"]["percentage_CTFO"] - \
            subject_spt_case1["std"]["percentage_CTFO"]
        Case1_CFO_down = subject_spt_case1["mean"]["percentage_CTFO"] + \
            subject_spt_case1["std"]["percentage_CTFO"]
        ax_temp.plot([Case1_CFO_up, Case1_CFO_up], [0, 1], color='k')
        ax_temp.plot([Case1_CFO_down, Case1_CFO_down], [0, 1], color='k')
    
        # C_FS
        Case1_CFS_up = subject_spt_case1["mean"]["percentage_CTFS"] - \
            subject_spt_case1["std"]["percentage_CTFS"]
        Case1_CFS_down = subject_spt_case1["mean"]["percentage_CTFS"] + \
            subject_spt_case1["std"]["percentage_CTFS"]
        ax_temp.plot([Case1_CFS_up, Case1_CFS_up], [0, 1], color='k')
        ax_temp.plot([Case1_CFS_down, Case1_CFS_down], [0, 1], color='k')
    
        # FO
        Case1_FO_up = subject_spt_case1["mean"]["stance_phase_perc"] - \
            subject_spt_case1["std"]["stance_phase_perc"]
        Case1_FO_down = subject_spt_case1["mean"]["stance_phase_perc"] + \
            subject_spt_case1["std"]["stance_phase_perc"]
        ax_temp.plot([Case1_FO_up, Case1_FO_up], [0, 1], color='k')
        ax_temp.plot([Case1_FO_down, Case1_FO_down], [0, 1], color='k')
    
        # Right
        # C_FO
        Case2_CFO_up = subject_spt_case2["mean"]["percentage_CTFO"] - \
            subject_spt_case2["std"]["percentage_CTFO"]
        Case2_CFO_down = subject_spt_case2["mean"]["percentage_CTFO"] + \
            subject_spt_case2["std"]["percentage_CTFO"]
        ax_temp.plot([Case2_CFO_up, Case2_CFO_up], [1, 2], color='k')
        ax_temp.plot([Case2_CFO_down, Case2_CFO_down], [1, 2], color='k')
    
        # C_FS
        Case2_CFS_up = subject_spt_case2["mean"]["percentage_CTFS"] - \
            subject_spt_case2["std"]["percentage_CTFS"]
        Case2_CFS_down = subject_spt_case2["mean"]["percentage_CTFS"] + \
            subject_spt_case2["std"]["percentage_CTFS"]
        ax_temp.plot([Case2_CFS_up, Case2_CFS_up], [1, 2], color='k')
        ax_temp.plot([Case2_CFS_down, Case2_CFS_down], [1, 2], color='k')
    
        # FO
        Case2_FO_up = subject_spt_case2["mean"]["stance_phase_perc"] - \
            subject_spt_case2["std"]["stance_phase_perc"]
        Case2_FO_down = subject_spt_case2["mean"]["stance_phase_perc"] + \
            subject_spt_case2["std"]["stance_phase_perc"]
        ax_temp.plot([Case2_FO_up, Case2_FO_up], [1, 2], color='k')
        ax_temp.plot([Case2_FO_down, Case2_FO_down], [1, 2], color='k')
        
        # Norm
        # C_FO
        Casenorm_CFO_up = norm_spt["mean"]["percentage_CTFO"] - \
            norm_spt["std"]["percentage_CTFO"]
        Casenorm_CFO_down = norm_spt["mean"]["percentage_CTFO"] + \
            norm_spt["std"]["percentage_CTFO"]
        ax_temp.plot([Casenorm_CFO_up, Casenorm_CFO_up], [2, 3], color='k')
        ax_temp.plot([Casenorm_CFO_down, Casenorm_CFO_down], [2, 3], color='k')
    
        # C_FS
        Casenorm_CFS_up = norm_spt["mean"]["percentage_CTFS"] - \
            norm_spt["std"]["percentage_CTFS"]
        Casenorm_CFS_down = norm_spt["mean"]["percentage_CTFS"] + \
            norm_spt["std"]["percentage_CTFS"]
        ax_temp.plot([Casenorm_CFS_up, Casenorm_CFS_up], [2, 3], color='k')
        ax_temp.plot([Casenorm_CFS_down, Casenorm_CFS_down], [2, 3], color='k')
    
        # FO
        Casenorm_FO_up = norm_spt["mean"]["stance_phase_perc"] - \
            norm_spt["std"]["stance_phase_perc"]
        Casenorm_FO_down = norm_spt["mean"]["stance_phase_perc"] + \
            norm_spt["std"]["stance_phase_perc"]
        ax_temp.plot([Casenorm_FO_up, Casenorm_FO_up], [2, 3], color='k')
        ax_temp.plot([Casenorm_FO_down, Casenorm_FO_down], [2, 3], color='k')
    
        
        ax_temp.spines['top'].set_visible(False)
        ax_temp.spines['right'].set_visible(False)
        ax_temp.spines['left'].set_visible(False)
        ax_temp.get_yaxis().set_ticks([])
    
        ax_temp.plot([101, 101], [3, 4], color=color_case_1, label=legend_1.replace('\n', ' '))
        ax_temp.plot([101, 101], [3, 4], color=color_case_2, label=legend_2.replace('\n', ' '))
    
        lgd = ax_temp.legend(loc='upper center', bbox_to_anchor=(0.5, 1.35), ncol=2, prop={'size': 13})
        # Tracer des paramètres
        # cadence
        for key, name, echelle, indice in zip(list_spt, name_spt, list_echelle, indice_list):
            ax_temp = fig.add_subplot(grid[indice:indice + 1, 0])
            ax_temp.set_ylim([0, 3])
            ax_temp.set_xlim(echelle)
    
            Case1_down = subject_spt_case1["mean"][key] - subject_spt_case1["std"][key]
            ax_temp.add_patch(patches.Rectangle(
                (Case1_down, 0.25), subject_spt_case1["std"][key] * 2, 0.5,
                facecolor=color_case_1, zorder=0))
            Case2_down = subject_spt_case2["mean"][key] + subject_spt_case2["std"][key]
            ax_temp.add_patch(patches.Rectangle(
                (Case2_down, 2.25), subject_spt_case2["std"][key] * 2, 0.5,
                facecolor=color_case_2, zorder=0))
            
            if key in norm_spt["mean"].keys():
                Casenorm_down = norm_spt["mean"][key] - norm_spt["std"][key]
                ax_temp.add_patch(patches.Rectangle(
                        (Casenorm_down, 1.25), norm_spt["std"][key] * 2, 0.5,
                        facecolor=(0.5,0.5,0.5), zorder=0))
            
            ax_temp.spines['top'].set_visible(False)
            ax_temp.spines['right'].set_visible(False)
            ax_temp.spines['left'].set_visible(False)
            ax_temp.get_yaxis().set_ticks([])
            plt.title(name)
    
        plt.tight_layout()
    
        report_directory_final = os.path.join(report_directory, 'SPT')
        if not os.path.isdir(report_directory_final):
            os.makedirs(report_directory_final)
    
        file_name_visuel = os.path.join(report_directory_final, title + '_Visuel.png')
        print('Sauvegarde du fichier ' + title + '_Visuel.png')
        fig.savefig(file_name_visuel, bbox_extra_artists=(lgd,), bbox_inches='tight')
        plt.close(fig)
    
        list_temp = []
        # ["",name_case_1, name_case_2,"Norme"]
        for key, name in zip(list_spt, name_spt):
            value_1 = '%.2f' % subject_spt_case1["mean"][key] + \
                u"\u00B1" + '%.2f' % subject_spt_case1["std"][key]
            value_2 = '%.2f' % subject_spt_case2["mean"][key] + \
                u"\u00B1" + '%.2f' % subject_spt_case2["std"][key]
            list_temp.append([name, value_1, value_2, value_2])
    
        fig, axis = plt.subplots(1, 1, dpi=100)
        # fig,axis = plt.subplots(1,1,figsize=(8.27,11.69),dpi=100)
    
        collabel = ("", legend_1, legend_2, "norme")
    
        the_table = axis.table(cellText=list_temp, colLabels=collabel, loc='center', edges='open')
    
        table_props = the_table.properties()
        table_cells = table_props['child_artists']
        for cell in table_cells:
            cell._text.set_fontsize(15)
        the_table._cells[(0, 1)]._text.set_color(color_case_1)
        # the_table._cells[(0,1)].set_fontsize(40)
        the_table._cells[(0, 2)]._text.set_color(color_case_2)
        axis.axis('tight')
        axis.axis('off')
        for ind_row in range(len(list_spt) + 1):
            the_table._cells[(ind_row, 3)]._text.set_color('grey')
        the_table.auto_set_column_width([-1, 0, 1, 2, 3])
        the_table.scale(1.0, 2.0)
        plt.tight_layout()
    
        file_name = os.path.join(report_directory_final, title + '.png')
        print('Sauvegarde du fichier ' + title)
        fig.savefig(file_name, bbox_inches='tight')
        plt.close(fig)
