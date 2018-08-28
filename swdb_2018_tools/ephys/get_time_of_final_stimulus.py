#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Created on Mon Aug 27

@author: shawno
"""

import numpy as np

def get_time_of_final_stimulus(data_set):
    
    '''Get time of the final stimulus is the session. This is a proxy for the session duration.'''

    all_stim_end_times = []
    for v in data_set.stim_tables.itervalues():
        all_stim_end_times.append(np.max(v.end.values))
    
    return np.max(all_stim_end_times)



