#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Created on Mon Aug 27

@author: shawno
"""

import h5py

def get_running_speed(data_set):
    f = h5py.File(data_set.nwb_path, 'r') 
    
    try:
        running_speed = f['acquisition']['timeseries']['RunningSpeed']['data'].value
        running_timestamps = f['acquisition']['timeseries']['RunningSpeed']['timestamps'].value
    except:
        running_speed = []
        running_timestamps = []
        
    f.close()
    
    return running_speed, running_timestamps



