# -*- coding: utf-8 -*-
"""
Created on Thu May 17 20:27:34 2018

@author: AdminXPS
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Apr 06 11:41:00 2018

@author: AdminXPS
"""
import os

import matplotlib.pyplot as plt
import numpy as np


# Chaque cote contiendra paramètres spatio temporel, kinematic, kinetics
# extraction des event en list


def plot_kinetic(subject_kinetic_case1, subject_spt_case1, color1,
                 subject_kinetic_case2, subject_spt_case2, color2,
                 norm_spt, norm_kinetic, report_repertory,
                 legend_1="test1", legend_2="test2", title="Kinetic"):
    for trace in ['mean','control']:
        x = np.linspace(0, 101, 101)
    
        list_kin = ["Hip_Fle", "Knee_Fle", "Ankle_Fle",
                    "Hip_Moment", "Knee_Moment", "Ankle_Moment",
                    "Hip_Power", "Knee_Power", "Ankle_Power",
                    "Normalised_Ground_Reaction_Z", "Normalised_Ground_Reaction_X", "Normalised_Ground_Reaction_Y"]
        list_name = ["Hip flexion", "Knee flexion", "Ankle dorsiflexion",
                     "Hip flexion moment", "Knee flexion moment", "Ankle flexion moment",
                     "Total hip power", "Total Knee power", "Total Ankle power",
                     "Vertical Ground Reaction Force", "Ant/Post Ground Reaction Force", "Lateral Ground Reaction Force"]
        list_name = ["Hip flexion", "Knee flexion", "Ankle dorsiflexion",
                     "Hip flexion moment", "Knee flexion moment", "Ankle flexion moment",
                     "Total hip power", "Total Knee power", "Total Ankle power",
                     "Vertical GRF", "Ant/Post GRF", "Lateral GRF"]
    
        list_ylim = [(-30, 60), (-10, 70), (-30, 30),
                     (-1.2, 1.2), (-0.8, 0.8), (-0.4, 1.6),
                     (-0.8, 1.6), (-2.0, 2.0), (-2, 4),
                     (0, 150), (-30, 30), (-20, 20)]
    
        list_ytick = [[-30, -5, 20, 45, 60], [-10, 10, 30, 50, 70], [-30, -15, 0, 15, 30],
                      [-1.2, -0.6, 0, 0.6, 1.2], [-0.8, -0.4, 0, 0.4, 0.8], [-0.4, 0, 0.6, 1.2, 1.6],
                      [-0.8, -0.2, 0.6, 1.2, 1.6], [-2.0, 1.0, 0, 1.0, 2.0], [-2, 0, 1.5, 3.0, 4.0],
                      [0, 50, 90, 120, 150], [-30, -15, 0, 15, 30], [-20, -10, 0, 10, 20]]
    
        list_ybarinterval = [10, 10, 10,
                             0.1, 0.1, 0.1,
                             0.2, 0.2, 0.2,
                             10, 10, 10]
    
        list_yticklabel = [["-30", "Ext", "deg", "Flex", "60"],
                           ["-10", "Ext", "deg", "Flex", "70"],
                           ["-30", "Plant", "deg", "Dorsi", "30"],
                           ["-1.2", "Ext", "adim", "Flex", "1.2"],
                           ["-0.8", "Abd", "adim", "Add", "0.8"],
                           ["-0.4", "Ext", "adim", "Int", "1.6"],
                           ["-0.8", "Ext", "deg", "Flex", "1.6"],
                           ["-2.0", "Val", "deg", "Var", "2.0"],
                           ["-2", "Ext", "deg", "Int", "4"],
                           ["0", "50", "BW %", "120", "150"],
                           ["-30", "-15", "BW %", "15", "30"],
                           ["-20", "-10", "BW %", "10", "20"]]
    
        fig, axis = plt.subplots(4, 3, figsize=(8.27, 11.69), dpi=100)
    
        for ind_kin, name_kin in enumerate(list_kin):
    
            i_row = ind_kin / 3
            i_collumn = ind_kin % 3
            # Definition du subplot à utiliser
            ax_temp = axis[i_row, i_collumn]
            ylim_inf = list_ylim[ind_kin][0]
            ylim_sup = list_ylim[ind_kin][1]
            ylim_huitieme = ylim_sup - (ylim_sup - ylim_inf) / 8.0
    
            # tracer des lignes
            ax_temp.plot([0, 100], [0, 0], 'k')
            y_interval_temp = list_ybarinterval[ind_kin]
            for value in np.arange(list_ylim[ind_kin][0] - y_interval_temp, list_ylim[ind_kin][1] + y_interval_temp,
                                   step=y_interval_temp):
                ax_temp.plot([0, 100], [value, value], color=(0.5, 0.5, 0.5), linewidth=1.0)
    
            # tracer des évenements spatio temporel
            # foot off
            fo_mean_case1 = subject_spt_case1["mean"]["stance_phase_perc"]
            fo_mean_case2 = subject_spt_case2["mean"]["stance_phase_perc"]
            fo_mean_norm = norm_spt["mean"]["stance_phase_perc"]
            fo_std_case1 = subject_spt_case1["std"]["stance_phase_perc"]
            fo_std_case2 = subject_spt_case2["std"]["stance_phase_perc"]
            fo_std_norm = norm_spt["std"]["stance_phase_perc"]
    
            ax_temp.fill_between([fo_mean_norm - fo_std_norm,
                                  fo_mean_norm + fo_std_norm],
                                 [ylim_inf, ylim_inf], [ylim_sup, ylim_sup],
                                 facecolor='0.5', alpha=0.5)
            ax_temp.fill_between([fo_mean_case1 - fo_std_case1,
                                  fo_mean_case1 + fo_std_case1],
                                 [ylim_inf, ylim_inf], [ylim_sup, ylim_sup],
                                 facecolor=color1, alpha=0.5)
            ax_temp.fill_between([fo_mean_case2 - fo_std_case2,
                                  fo_mean_case2 + fo_std_case2],
                                 [ylim_inf, ylim_inf], [ylim_sup, ylim_sup],
                                 facecolor=color2, alpha=0.5)
    
            # controlateral foot strike
            ctfs_mean_case1 = subject_spt_case1["mean"]["percentage_CTFS"]
            ctfs_mean_case2 = subject_spt_case2["mean"]["percentage_CTFS"]
            ctfs_mean_norm = norm_spt["mean"]["percentage_CTFS"]
            ctfs_std_case1 = subject_spt_case1["std"]["percentage_CTFS"]
            ctfs_std_case2 = subject_spt_case2["std"]["percentage_CTFS"]
            ctfs_std_norm = norm_spt["std"]["percentage_CTFS"]
    
            ax_temp.fill_between([ctfs_mean_norm - ctfs_std_norm,
                                  ctfs_mean_norm + ctfs_std_norm],
                                 [ylim_huitieme, ylim_huitieme], [ylim_sup, ylim_sup],
                                 facecolor='0.5', alpha=0.5)
            ax_temp.fill_between([ctfs_mean_case1 - ctfs_std_case1,
                                  ctfs_mean_case1 + ctfs_std_case1],
                                 [ylim_huitieme, ylim_huitieme], [ylim_sup, ylim_sup],
                                 facecolor=color1, alpha=0.5)
            ax_temp.fill_between([ctfs_mean_case2 - ctfs_std_case2,
                                  ctfs_mean_case2 + ctfs_std_case2],
                                 [ylim_huitieme, ylim_huitieme], [ylim_sup, ylim_sup],
                                 facecolor=color2, alpha=0.5)
            # controlateral foot off
            ctfo_mean_case1 = subject_spt_case1["mean"]["percentage_CTFO"]
            ctfo_mean_case2 = subject_spt_case2["mean"]["percentage_CTFO"]
            ctfo_mean_norm = norm_spt["mean"]["percentage_CTFO"]
            ctfo_std_case1 = subject_spt_case1["std"]["percentage_CTFO"]
            ctfo_std_case2 = subject_spt_case2["std"]["percentage_CTFO"]
            ctfo_std_norm = norm_spt["std"]["percentage_CTFO"]
    
            ax_temp.fill_between([ctfo_mean_norm - ctfo_std_norm,
                                  ctfo_mean_norm + ctfo_std_norm],
                                 [ylim_huitieme, ylim_huitieme], [ylim_sup, ylim_sup],
                                 facecolor='0.5', alpha=0.5)
            ax_temp.fill_between([ctfo_mean_case1 - ctfo_std_case1,
                                  ctfo_mean_case1 + ctfo_std_case1],
                                 [ylim_huitieme, ylim_huitieme], [ylim_sup, ylim_sup],
                                 facecolor=color1, alpha=0.5)
            ax_temp.fill_between([ctfo_mean_case2 - ctfo_std_case2,
                                  ctfo_mean_case2 + ctfo_std_case2],
                                 [ylim_huitieme, ylim_huitieme], [ylim_sup, ylim_sup],
                                 facecolor=color2, alpha=0.5)
    
            # controlateral foot off
            # tracer des courbes
            mean_1 = subject_kinetic_case1["mean"][list_kin[ind_kin]]
            all_1 = subject_kinetic_case1["all"][list_kin[ind_kin]]
            mean_2 = subject_kinetic_case2["mean"][list_kin[ind_kin]]
            all_2 = subject_kinetic_case2["all"][list_kin[ind_kin]]
            std_1 = subject_kinetic_case1["std"][list_kin[ind_kin]]
            std_2 = subject_kinetic_case2["std"][list_kin[ind_kin]]
            if not (i_row == 3 and i_collumn == 2):
                norm_mean = norm_kinetic["mean"][list_kin[ind_kin]]
                norm_std = norm_kinetic["std"][list_kin[ind_kin]]
                norm_X = norm_kinetic["mean"]['X_value']
                ax_temp.fill_between(norm_X, norm_mean - norm_std, norm_mean + norm_std, facecolor='0.5', alpha=0.5)
            # Tracer des courbes
            if trace == 'mean':
                ax_temp.fill_between(x, mean_1 - std_1, mean_1 + std_1, facecolor=color1, alpha=0.5)
                ax_temp.fill_between(x, mean_2 - std_2, mean_2 + std_2, facecolor=color2, alpha=0.5)
                ax_temp.plot(x, mean_1, color1, label=legend_1)
                ax_temp.plot(x, mean_2, color2, label=legend_2)
                title_final = title
            elif trace == 'control':
                #ontrace séparemment le premier pour n'avoir qu'une légende
                ax_temp.plot(x, all_1[:,0], color1, label=legend_1)
                ax_temp.plot(x, all_2[:,0], color2, label=legend_2)
                ax_temp.plot(x, all_1[:,1:], color1)
                ax_temp.plot(x, all_2[:,1:], color2)
                title_final = title + '_control'
    
            # Reglages des élement du graphique
            ax_temp.set_title(list_name[ind_kin], fontsize=15)
            ax_temp.set_ylim(list_ylim[ind_kin])
            ax_temp.set_xlim((0, 100))
            ax_temp.set_xticks([0, 20, 40, 60, 80, 100])
            ax_temp.set_xticklabels(["0", "20", "40", "60", "80", "100"])
            ax_temp.set_yticks(list_ytick[ind_kin])
            ax_temp.set_yticklabels(list_yticklabel[ind_kin])
            ax_temp.spines['right'].set_visible(False)
            ax_temp.spines['top'].set_visible(False)
            if i_row == 3:
                ax_temp.set_xlabel("% Gait cycle")
            if (i_row == 0 and i_collumn == 1):
                # ax_temp.legend()
                lgd = ax_temp.legend(loc='upper center', bbox_to_anchor=(0.5, 1.35), ncol=2, prop={'size': 13})
    
        # fig.suptitle(title, fontsize=16)
        # plt.tight_layout(pad=7.0, w_pad=0.3, h_pad=1.0)
        plt.tight_layout()
        #    gs1.tight_layout(fig, rect=[0, 0.03, 1, 0.95])
        #plt.show(block=False)
        file_name = os.path.join(report_repertory, title_final + '.png')
        print('Sauvegarde du fichier '+ title_final)
        fig.savefig(file_name, bbox_extra_artists=(lgd,), bbox_inches='tight')
        plt.close(fig)
        # fig.savefig('samplefigure.png')
