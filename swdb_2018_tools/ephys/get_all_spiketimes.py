#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 14:38:40 2018

@author: saskiad
"""
import numpy as np
import pandas as pd
import scipy.ndimage as ndi

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

def get_fr(spike_times, num_timestep_second=20, filter_width=0.5):
    '''Filters spike times to create instantaneous firing rate

    Parameters
    ----------
    spike times: for one unit (np array)
    num_timestep_second : number of "bins" per second (int)
    filter width : st. dev of the gaussian filter in seconds (float)


    Returns
    -------
    firing rate (array)
    timestamps (array)

    '''
    timesteps = 1./num_timestep_second
    spikes = spike_times.astype(float)
    spike_train = np.zeros((int((spikes[-1]+0.2)*num_timestep_second)))
    spike_train[(spikes*num_timestep_second).astype(int)]=1
    filter_width = int(filter_width*num_timestep_second)
    fr = ndi.gaussian_filter(spike_train, filter_width)
    timestamps = np.linspace(0,len(fr)/num_timestep_second, num=len(fr))
    return fr, timestamps