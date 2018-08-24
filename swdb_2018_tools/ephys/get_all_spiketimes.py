#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 14:38:40 2018

@author: saskiad
"""
import numpy as np
import pandas as pd

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


def one_spike_dataframe_to_rule_them_all(data_set):
    ''' loads all spike times into a single dataframe

    Parameters
    ----------
    data_set : ephys dataset

    Returns
    -------
    spikes : pandas DataFrame
    '''

    spikes = []

    for probe_name, probe_spikes in data_set.spike_times.items():
        for unit_id, unit_times in probe_spikes.items():
            df = pd.DataFrame({'time': unit_times})
            df['unit_id'] = unit_id
            df['probe'] = probe_name
            spikes.append(df)

    spikes = (
        pd.concat(spikes)
        .set_index('time')
        .sort_index()
    )

    return spikes
