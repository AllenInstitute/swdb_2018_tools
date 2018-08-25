#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 25 08:46:09 2018

@author: mariasolbernardezsarria
"""

#import all necessary packages and data

import matplotlib
%matplotlib notebook

import os
import numpy as np
import pandas as pd


# Plotting
import matplotlib.pyplot as plt
%matplotlib inline
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection, LineCollection
from matplotlib import colors as mcolors
# %matplotlib notebook

from __future__ import print_function

#Behavior
from visual_behavior.ophys.dataset.visual_behavior_ophys_dataset import VisualBehaviorOphysDataset
from visual_behavior.ophys.response_analysis.response_analysis import ResponseAnalysis 

drive_path = '/data/dynamic-brain-workshop/visual_behavior'


#The function below loads manifest file, it's also located helper_functions.py
def load_manifest(drive_path = '/data/dynamic-brain-workshop/visual_behavior',
                  manifest_file = 'visual_behavior_data_manifest.csv'):
    '''
    This is just a rapper to load behavior dataset manifest. 
    Inputs 
    drive_path (optional): Location of data on drive. Default is AWS location
    '''
    manifest = pd.read_csv(os.path.join(drive_path,manifest_file))
    return manifest

#Beginning of script
manifest = load_manifest()

#Define the scpecifics you are interested in, such as
#cre-line
#cortical area
mask = (manifest.targeted_structure=='VISp')&(manifest.cre_line=='Slc17a7-IRES2-Cre')

# extracting the information (experiment_id for L2/3 V1) 
data_inv = manifest[mask] 

#temp_idx = data_inv.donor_id.unique()  #use this if you want to see the unique mice
#exp_idx = data_inv.experiment_id.unique() ##use this if you want to see the unique experiment ids, mice < experiment_ids

all_experiment_ids = manifest[mask].experiment_id.values
len(all_experiment_ids)

# Create a dictionary with all of the data you want to use (based on the conditions above)
all_data = {}
for n, data in enumerate(all_experiment_ids):
    all_data['%s' % data] = VisualBehaviorOphysDataset(all_experiment_ids[n], cache_dir=drive_path)
len(all_data) # to confirm  length of all_data is equal to that of all_experiment_ids


#Select for a specific cell and image
# temp0 = all_data[experiment_id]
expID = 639438856 #your experiment of choice
cellID = 19       #your cell of choice
temp0 = all_data['639438856'] #create a temporary file with data for your experiment_id

analysis = ResponseAnalysis(temp0) #fetching data, refer to beginning
data = analysis.get_flash_response_df() #data for all cells

#select cell
data_cell = data[(data.cell==cellID)]
data_cell.reset_index(drop=True, inplace=True)
data_cell


#add information about image repeats
len(data_cell)
addCol = np.zeros(len(data_cell))
addCol[0]=1

counter = 1

for n in np.arange(1,len(data_cell),1):
    if data_cell['image_name'][n] == data_cell['image_name'][n-1]:
        addCol[n] = counter + 1
        counter = counter + 1

    else:
        addCol[n] = 1
        counter = 1

data_cell['Repeats'] = addCol

#add information about block number
addBlock = np.zeros(len(data_cell))
addBlock[0]=1

counter = 1
for n in np.arange(1,len(data_cell),1):
    if data_cell['Repeats'][n-1] - data_cell['Repeats'][n] < 1:
        addBlock[n] = counter
    else:
        addBlock[n] = counter + 1
        counter = counter +1

data_cell['Block'] = addBlock


#choose data for a single image, i.e. img012
print(data_cell['image_name'].unique())
IIW = 'im012'

data_cell_image = data_cell[(data_cell.image_name == IIW)] 
data_cell_image.reset_index(drop=True, inplace=True)

unqBlocks = data_cell_image['Block'].unique()  #find number of blocks
no_blocks = len(unqBlocks)
len(no_blocks)

#Extract the mean response 
tdata2plot = []

for n in np.arange(0,no_blocks,1):
    ptemp = data_cell_image[data_cell_image.Block == unqBlocks[n]]
    meanR = ptemp['mean_response']
    tdata2plot.append(meanR)


#plot all traces one on top of the other
for n in np.arange(0,len(tdata2plot),1):
    plt.plot(tdata2plot[n].values)
    plt.xlabel('repetitions within block')
    plt.ylabel('mean response')
    
#outcome is messy, may want to use a waterfall plot
# DFeng created a function you can import, the info is below (and slightly changed)
    

def waterfall(arrs, colors=None):
    fig = plt.figure(figsize=plt.figaspect(0.4))
    ax = fig.gca(projection='3d')

    def cc(arg):
        return mcolors.to_rgba(arg, alpha=0.5)

    verts = [ zip(np.arange(len(a)), a) for a in arrs ]
    zs = np.arange(len(verts))


    poly = LineCollection(verts, colors=colors)
    poly.set_alpha(0.5)
    ax.add_collection3d(poly, zs=zs, zdir='y')

    #ax.set_xlabel('X')
    ax.set_xlim3d(0, max([len(a) for a in arrs])-1)
    #ax.set_ylabel('Y')
    ax.set_ylim3d(0, len(arrs))
    #ax.set_zlabel('Z')
    ax.set_zlim3d(0, max([max(a) for a in arrs]))

    plt.show()

waterfall(tdata2plot,colors = None)

