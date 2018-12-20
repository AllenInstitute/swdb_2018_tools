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
from print_info import print_info

# Provide path to manifest file
manifest_file = os.path.join(drive_path,'ephys_manifest.csv')

# Create a dataframe 
expt_info_df = pd.read_csv(manifest_file)

#make new dataframe by selecting only multi-probe experiments
multi_probe_expt_info = expt_info_df[expt_info_df.experiment_type == 'multi_probe']

multi_probe_example = 0

multi_probe_filename  = multi_probe_expt_info.iloc[multi_probe_example]['nwb_filename']

# Specify full path to the .nwb file
nwb_file = os.path.join(drive_path,multi_probe_filename)

data_set = NWB_adapter(nwb_file)

print_info(data_set.unit_df)