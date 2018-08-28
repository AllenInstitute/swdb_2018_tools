import numpy as np
import pandas as pd


def get_trial_len(dataset):
    '''this function gets the starts, ends and the length of each image repetition sequence from the given dataset'''
    
    stim_table = dataset.get_stimulus_table()
    im_name = stim_table['image_name'].unique()
    
    # get trial length for each image
    trial_start = []
    trial_end = []
    trial_len = []
    # start_time = []
    # end_time = []

    for i, im in enumerate(im_name):
        t = stim_table['image_name']==im
        trial_diff = t[:-1].values*1 - t[1:].values*1
        if t[0]==1:
            trial_diff = np.insert(trial_diff,0,-1)
        if t[len(t)-1]==1:
            trial_diff = np.insert(trial_diff,len(trial_diff),1)
        trial_start.append(np.where(trial_diff==-1)[0])
        trial_end.append(np.where(trial_diff==1)[0])
        trial_len.append(trial_end[i]-trial_start[i]+1)
        # start_time.append(stim_table['start_time'].values[np.where(trial_diff==1)])
        # end_time.append(stim_table['end_time'].values[np.where(trial_diff==1)])
    
        result_dict = {'image':[im_name[0]]*len(trial_start[0]), 'trial_start':list(trial_start[0]), 'trial_end':list(trial_end[0]), 'trial_length':list(trial_len[0])} #, 'start_time':list(start_time[0]), 'end_time':list(end_time[0])}
    for i in range(len(im_name)-1):
        result_dict['image'] += [im_name[i+1]]*len(trial_start[i+1])
        result_dict['trial_start'] += list(trial_start[i+1])
        result_dict['trial_end'] += list(trial_end[i+1])
        result_dict['trial_length'] += list(trial_len[i+1])
        # result_dict['start_time'] += list(start_time[i+1])
        # result_dict['end_time'] += list(end_time[i+1])
    
    result = pd.DataFrame(result_dict)
    result = result[['image','trial_start','trial_end','trial_length']]
    
    return result