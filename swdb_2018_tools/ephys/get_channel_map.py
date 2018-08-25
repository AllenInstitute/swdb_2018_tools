#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Created on Fri Aug 24

@author: shawno
"""

import os
import pandas as pd

def get_channel_map(drive_path):
    
    # Provide path to channel positions file
    channel_positions_file = os.path.join(drive_path,'channel_positions.csv')

    # Create a dataframe
    ch_map = pd.read_csv(channel_positions_file)

    # Return channel map dataframe
    return ch_map