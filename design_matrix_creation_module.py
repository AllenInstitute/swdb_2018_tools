import numpy as np
import pandas as pd


def get_frame_at_time(time, stim_table):
    starts = stim_table.start.values
    idx = np.searchsorted(starts, time)-1
    return(stim_table.iloc[idx].values[2])


def get_sampled_stimulus_time_array(stim_table, sampling_time, flattened_image_list):
    ns_time_start = stim_table.iloc[0].values[0]
    ns_time_end = stim_table.iloc[stim_table.last_valid_index()][1]
    time_array = np.linspace(ns_time_start,ns_time_end,int((ns_time_end-ns_time_start)/sampling_time))
    stim_array = []
    for idx, time_point in enumerate(time_array):
        stim_index = get_frame_at_time(time_point, stim_table)
        stim_array.append(flattened_image_list[int(stim_index)])
    return(stim_array)