# AWS
basic_path = 'F:\\'
drive_path = basic_path + 'visual_coding_neuropixels'

# We need to import these modules to get started
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

# Import NWB_adapter
import os
import sys
sys.path.append(basic_path + 'resources/swdb_2018_neuropixels')
from swdb_2018_neuropixels.ephys_nwb_adapter import NWB_adapter

from filter_spikes_by_region_stimulus import filter_spikes_by_region_stimulus
from plot_spike_train import plot_spike_train
from plot_spike_train_psth import plot_spike_train_psth
from plot_spike_train_psth_with_latency import plot_spike_train_psth_with_latency
from get_all_regions import get_all_regions
from print_info import print_info
import pickle

current_stimulus = ['natural_images']

# Provide path to manifest file
manifest_file = os.path.join(drive_path,'ephys_manifest.csv')

# Create a dataframe 
expt_info_df = pd.read_csv(manifest_file)

#make new dataframe by selecting only multi-probe experiments
multi_probe_expt_info = expt_info_df[expt_info_df.experiment_type == 'multi_probe']

all_regions = get_all_regions(multi_probe_expt_info)
print('All regions: ' + str(all_regions))

output_path = 'Latency_results/'
input_path = '../../../Resources/'
if not os.path.exists(output_path):
    os.makedirs(output_path)

region_latency = {}

for region in all_regions:
    region_latency[region] = []
    # region_spikes = filter_spikes_by_region_stimulus(multi_probe_expt_info, region, current_stimulus)


    # with open('region_spikes.pkl', 'w') as f:
    #     pickle.dump([region_spikes], f)

    with open(input_path + 'Small_' + region + '_spikes.pkl') as f:
        region_spikes = pickle.load(f)

    region_spikes = region_spikes[0]

    print('Loaded spikes file from region: ' + region)

    c_output_path = output_path + region + '/'
    if not os.path.exists(c_output_path):
        os.makedirs(c_output_path)

    temp_ind = 0
    for key, val in region_spikes.iteritems():
        file_name = c_output_path + key
        plot_spike_train(val, file_name + '.png')
        c_latency = plot_spike_train_psth_with_latency(val, file_name + '_psth.png')
        region_latency[region].append(c_latency)
        if temp_ind > 50:
            break
        temp_ind += 2

    print(region_latency)

with open(input_path + 'region_latency.pkl', 'w') as f:
    pickle.dump([region_latency], f)
