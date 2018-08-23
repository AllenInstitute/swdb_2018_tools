#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 14:38:40 2018

@author: saskiad
"""
import pandas as pd
from swdb_2018_neuropixels.ephys_nwb_adapter import NWB_adapter

def get_all_spike_times(data_set):
    '''Adds unit spike times to the unit_df dataframe

Parameters
----------
ephys data_set


Returns
-------
unit_df (pandas DataFrame)

    '''
    unit_df = data_set.unit_df
    unit_df['spike_times'] = np.NaN
    for probe in data_set.probe_list:
        subset = unit_df[unit_df.probe==probe]
        probe_spikes = data_set.spike_times[probe]
        for index,row in subset.iterrows():
            unit_df.spike_times.loc[index] = probe_spikes[row.unit_id].astype(object)
    return unit_df