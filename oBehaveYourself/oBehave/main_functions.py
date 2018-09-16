#Load the relevant packages
import numpy as np 
import pandas as pd 
import os 
import sys 
import h5py 
import matplotlib.pyplot as plt 
drive_path = '/data/allen-brain-observatory/visual-coding-2p'
from allensdk.core.brain_observatory_cache import BrainObservatoryCache

'''
These are some wrappers to save time loading visual behavior datset components.
Created by Sam Sied, August 2018. 
'''

from visual_behavior.ophys.dataset.visual_behavior_ophys_dataset import VisualBehaviorOphysDataset
def observatory_variables(data_path=drive_path):
    #creates boc object and returns it
    #input your own filepath for the data if you are not using AWS
    manifest_file = os.path.join(drive_path, 'manifest.json')
    boc = BrainObservatoryCache(manifest_file=manifest_file)
    print('yes')
    return(boc)

def dataset_object(session_id):
    #input session id and output dataset object
    #useful for quickly changing observatory datasets
    data_set = boc.get_ophys_experiment_data(ophys_experiment_id=session_id)
    return(data_set)

def load_analysis(session_id):
    #input session id and output analysis file
    drive_path = '/data/allen-brain-observatory/visual-coding-2p'
    analysis_path = os.path.join(drive_path,'ophys_experiment_analysis')
    analysis_file = os.path.join(analysis_path, str(session_id)+'_three_session_B_analysis.h5')
    return(analysis_file)

def stim_table():
    #pull the stimulus information and mean sweep response
    stim_table_sg = pd.read_hdf(analysis_file, key='analysis/stim_table_sg')
    mean_sweep_response_sg = pd.read_hdf(analysis_file, key='analysis/mean_sweep_response_sg')
    return(stim_table_sg, mean_sweep_response_sg)

def behavior_variables():
    #load the behavior manifest for analysis, as well as a list of all the experiments
    drive_path = '/data/dynamic-brain-workshop/visual_behavior'
    manifest_file = 'visual_behavior_data_manifest.csv'
    manifest = pd.read_csv(os.path.join(drive_path,manifest_file))
    experiment_list = manifest['experiment_id']
    experiment_list = experiment_list.tolist()
    return(manifest, experiment_list)
