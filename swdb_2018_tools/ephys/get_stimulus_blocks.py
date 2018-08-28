#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Created on Mon Aug 27

@author: shawno
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def get_stimulus_blocks(data_set, block_threshold=100):
    '''Return dataframe with start and end times for each stimulus block '''
    stim_blocks = []
    for i,k in enumerate(data_set.stim_tables.keys()):
        stim_table = data_set.stim_tables[k]
        s = stim_table.start.values
        s_end = stim_table.end.values

        idx = np.where(np.diff(s)>block_threshold)[0] + 1
        full_idx = np.sort(np.unique(np.concatenate([idx, [0, len(s)]])))

        for low, high in zip(full_idx[:-1], full_idx[1:]):
            stim_blocks.append((k, s[low], s_end[high-1]))
            
    stim_blocks = pd.DataFrame(stim_blocks,columns=['stimulus_type','start','end'])
    return stim_blocks

def plot_stimulus_blocks(data_set,ax=[]):
    
    if not ax:
        fig,ax = plt.subplots(1,1)
    
    colors = {'drifting_gratings': '#06738D',
          'static_gratings': '#3DB1AA',
          'locally_sparse_noise': '#263C87',
          'natural_scenes': '#F89D51',
          'natural_movie_one': '#E35887',
          'natural_movie_three': '#E35887',
          'spontaneous': '#676767',
          'gabor_20_deg_250ms': '#bdc7d8',
          'flash_250ms': '#fff138',        
          }
    
    stim_blocks = get_stimulus_blocks(data_set)
    for _,block in stim_blocks.iterrows():
        try:
            ax.axvspan(block.start,block.end,color=colors[block['stimulus_type']],alpha=0.7)
        except:
            pass
            
    


