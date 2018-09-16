from __future__ import print_function
import os
import numpy as np
import pandas as pd

'''
I got tired of typing some stuff, so these are just cute wrappers to save time
Created by Yoni Browning, August 2018
'''

# Local of the event drive path
event_drive_path_AWS = '/data/dynamic-brain-workshop/visual_behavior_events' #AWS Location
drive_path =  '/data/dynamic-brain-workshop/visual_behavior'

def load_manifest(drive_path = drive_path,manifest_file = 'visual_behavior_data_manifest.csv'):
    '''
    This is just a rapper to load behavior dataset manifest. 
    Inputs 
    drive_path (optional): Location of data on drive. Default is AWS location
    '''
    manifest = pd.read_csv(os.path.join(drive_path,manifest_file))
    return manifest


def load_dff_events_file(experiment_id,event_drive_path = event_drive_path_AWS):
    '''
    Loads a given behavior event file from a supplied experiment id
    Can be used in conjunction with the manifest file, in a format
    similar to the way dataset objs are called
    Input
    experiment_id: manifest ID
    event_drive_path: Optional. Script has built in drive path to AWS location.
    '''
    event_drive_path = '/data/dynamic-brain-workshop/visual_behavior_events'
    tmp = os.path.join(event_drive_path, str(experiment_id)+'_events.npz')
    tmp_data = np.load(tmp)
    event_array = tmp_data['ev']
    return event_array
