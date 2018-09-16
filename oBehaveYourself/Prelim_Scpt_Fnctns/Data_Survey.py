#!/usr/bin/env python2
# -*- coding: utf-8 -*-

''' 
2018.May.23, 23:30, SB & SS
#This is just a general code to do a quick survey of your all of relevant mouse:
# 1) Narrow down conditions based on cortical area and cre-line = creates a list
# 2) Use this list to identify unique mouse_ids = creates a list
# 3) Use mouse_ids to identify their relevant experiment ids (input for 'VisualBehaviorOphysDataset') 
# and extract the data.objects that have all the juicy info!
# 4) Plot some of that data (does not save in a new variable or object at this time)
'''

#Must first run load_manifest from the file helper_functions
# matplotlib is a standard python visualization package
import matplotlib.pyplot as plt
%matplotlib inline

manifest = load_manifest()
# import visual behavior dataset class from the visual_behavior package
from visual_behavior.ophys.dataset.visual_behavior_ophys_dataset import VisualBehaviorOphysDataset

# extracting the information (experiment_id for L2/3 V1)
data_inv = manifest[(manifest.targeted_structure=='VISp')&(manifest.cre_line=='Slc17a7-IRES2-Cre')] 

temp_idx = data_inv.donor_id.unique()
# temp_idx
exp_idx = data_inv.experiment_id.unique()
# exp_idx

all_experiment_ids = manifest[(manifest.targeted_structure=='VISp')&(manifest.cre_line=='Slc17a7-IRES2-Cre')].experiment_id.values
len(all_experiment_ids)

# if the conditions will remain constant, you can create a mask for them
# if so, remove comment below
# mask = (manifest.targeted_structure=='VISp')&(manifest.cre_line=='Slc17a7-IRES2-Cre')


# Create a dictionary with all of the data you want to use (based on the conditions above)
all_data = {}
for n, data in enumerate(all_experiment_ids):
    all_data['%s' % data] = VisualBehaviorOphysDataset(all_experiment_ids[n], cache_dir=drive_path)
len(all_data) # to confirm  length of all_data is equal to that of all_experiment_ids


# use this general framework to extract relevant info you would like to plot to survey the data for all relevant mice
# remember to employ the all_data[key].TAB to access the ".get_whateverColumnYouCareAbout"
# examples of additional information you may need are:
#      timeseries, dff_trace = temp0.get_dff_traces
#      running_data = temp0.running_speed
#      lick_data = temp0.licks
#      stimulus = temp0.stimulus_table

for key in all_data:
    temp0 = all_data[key]
    temp1 = temp0.get_running_speed() #change this for different information
    plt.plot(temp1['time'], temp1['running_speed']) #format your figure in a way that makes sense!
    plt.title(str(key)+ "running speed")
    plt.show()

