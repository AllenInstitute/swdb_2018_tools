basic_path = 'F:\\'
drive_path = basic_path + 'visual_coding_neuropixels'

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

# Import NWB_adapter
import os
import sys
sys.path.append(basic_path + 'resources/swdb_2018_neuropixels')
from swdb_2018_neuropixels.ephys_nwb_adapter import NWB_adapter

def filter_spikes_by_region_stimulus(multi_probe_expt_info, region, stimulus):
    spike_trains = {}
    pre_stimulus_time = 0.1
    for multi_probe_example in range(len(multi_probe_expt_info)):
        multi_probe_filename = multi_probe_expt_info.iloc[multi_probe_example]['nwb_filename']

        # Specify full path to the .nwb file
        nwb_file = os.path.join(drive_path,multi_probe_filename)

        data_set = NWB_adapter(nwb_file)

        for c_probe in np.unique(data_set.unit_df['probe']):
            region_units = data_set.unit_df[(data_set.unit_df['structure'] == region) & (data_set.unit_df['probe'] == c_probe)]
            all_units = data_set.spike_times[c_probe]
            for index, region_unit in region_units.iterrows():
                spike_train = all_units[region_unit['unit_id']]
                for ind, stim_row in data_set.stim_tables['natural_scenes'].iterrows():
                    current_train = spike_train[(spike_train > stim_row['start'] - pre_stimulus_time) & (spike_train < stim_row['end'])] - stim_row['start']
                    train_id = multi_probe_filename + '_' + c_probe + '_' + region_unit['unit_id'] + '_' + str(int(stim_row['frame'])) + '_' + str(region_unit['depth'])
                    if not spike_trains.has_key(train_id):
                        spike_trains[train_id] = []
                    spike_trains[train_id].append(current_train)
    return spike_trains
        
