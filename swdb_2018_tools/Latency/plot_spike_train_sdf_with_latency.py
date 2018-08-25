# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 21:41:41 2018

@author: Stav
"""

import numpy as np
import matplotlib.pyplot as plt
from get_hist_sdf import get_hist_sdf
from print_info import print_info

def plot_spike_train_sdf_with_latency(spike_train, fig_path):

    number_of_std = 3
    window_in_ms = float(10) # 5
    first_possible_response = 50
    start_window_in_ms = float(-100)
    end_window_in_ms = float(250)
    window_in_secs = window_in_ms/float(1000)
    min_range = int(float(-100)/window_in_ms)
    max_range = int(float(250)/window_in_ms + 1)

    x_axis_values = [float(x)/float(1000) for x in range(min_range*int(window_in_ms), (max_range-1)*int(window_in_ms))]

    fig,ax = plt.subplots(1,1,figsize=(6,3))
    spike_times = []
    for row in spike_train:
        spike_times.extend(list(row))
# vals, bins, patches = plt.hist(spike_times, bins=[x * window_in_secs for x in range(min_range, max_range)])

# stimulus_ind = np.argmax(np.array(bins) >= 0)
# pre_stimulus_vals = vals[:stimulus_ind]
# start_gap = int(first_possible_response/window_in_ms)
# post_stimulus_val = vals[stimulus_ind+start_gap:]
# std_val = np.std(pre_stimulus_vals)
# mean_val = np.mean(pre_stimulus_vals)
# positive_threshold = mean_val + number_of_std*std_val
# negative_threshold = mean_val + -1*number_of_std*std_val
# post_np_arr = np.array(post_stimulus_val)

# first_occur = -1
# pos_first_occur = -1
# neg_first_occur = -1

# if post_np_arr.max() > positive_threshold:
#     pos_first_occur = np.argmax(post_np_arr > positive_threshold)

# if post_np_arr.min() < negative_threshold:
#     neg_first_occur = np.argmax(post_np_arr < negative_threshold)

# if pos_first_occur > -1 and neg_first_occur > -1:
#     if pos_first_occur < neg_first_occur:
#         first_occur = pos_first_occur
#         plt.axvline(x=bins[first_occur+stimulus_ind+start_gap], color='green',alpha=0.5)    		
#     else:
#         first_occur = neg_first_occur
#         plt.axvline(x=bins[first_occur+stimulus_ind+start_gap], color='red',alpha=0.5)    		
# else:
#     if pos_first_occur > -1:
#         first_occur = pos_first_occur
#         plt.axvline(x=bins[first_occur+stimulus_ind+start_gap], color='green',alpha=0.5)    		    		
#     elif neg_first_occur > -1:
#         first_occur = neg_first_occur
#         plt.axvline(x=bins[first_occur+stimulus_ind+start_gap], color='red',alpha=0.5)
    sdfs = np.zeros((len(spike_train), int(end_window_in_ms-start_window_in_ms)))
    for row_ind, row in enumerate(spike_train):
        sdf = get_hist_sdf(row)
        sdfs[row_ind, :] = sdf[:350]
    mean_sdf = sdfs.mean(axis=0)
    plt.plot(x_axis_values, mean_sdf, color='yellow')

    ax.axvspan(start_window_in_ms/float(1000),0,color='gray',alpha=0.2)
    ax.set_xlim([start_window_in_ms/float(1000), end_window_in_ms/float(1000)])
    ax.set_ylim([0, 0.2])
    fig.savefig(fig_path)

    # print(pos_first_occur)
    # print(neg_first_occur)
    # print(first_occur)
    # print(stimulus_ind)
    # print(start_gap)
    # print(first_occur+stimulus_ind+start_gap)
    # print(bins[first_occur+stimulus_ind+start_gap])
    # print('--')

    response_time = float('nan')
# if first_occur > -1:
#     response_time = x_axis_values[int((first_occur+stimulus_ind+start_gap)*window_in_ms)]*1000

    return response_time