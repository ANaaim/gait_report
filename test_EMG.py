# -*- coding: utf-8 -*-
"""
Created on Thu May 03 10:36:25 2018

@author: VICON
"""

colorleft_case1 = 'tab:red'
colorright_case1 = 'tab:green'
colorleft_case2 = 'tab:orange'
colorright_case2 = 'tab:blue'

from plot_emg import plot_emg as plot_emg

plot_emg('test.c3d',colorleft_case2,colorright_case2,title = "EMG")