import numpy as np
import matplotlib.mlab as mlab
from get_sdf_from_spike_train import get_sdf_from_spike_train

def spike_times_to_arr(spike_times, start_point, end_point):
    arr_size = int((end_point-start_point)*1000)
    spike_arr = np.zeros(arr_size)
    for spike_time in spike_times:
        spike_index = int((spike_time-start_point)*1000)
        if spike_index < arr_size:
            spike_arr[spike_index] = 1

    return spike_arr

def get_hist_sdf(spike_times):
    spike_times_arr = spike_times_to_arr(spike_times, -0.1, 0.25)
    if True:
        sdf = get_sdf_from_spike_train(spike_times_arr, 10)

        # print(spike_times_arr)
        # print(sdf)

        return sdf
    # sigma = 0.045
    sigma = 0.01
    dx = 0.001
    # start = -3*sigma
    # stop = 3*sigma
    # step = 0.001
    # edges = np.arange(start, stop+step, step)
    # kernel = mlab.normpdf(edges, 0, sigma)
    # kernel *= 0.001
    gx = np.arange(-3*sigma, 3*sigma+dx, dx)
    gaussian = np.exp(-(gx/sigma)**2/2)
    conv_data = np.convolve(spike_times_arr, gaussian, mode='full')

    return conv_data
# center = np.ceil(float(len(edes))/float(2))
# conv_data