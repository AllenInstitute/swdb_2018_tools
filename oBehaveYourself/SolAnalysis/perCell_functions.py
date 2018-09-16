#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 09:46:26 2018
Below are functions necessary to recapitulate the single-cell analysis presented by 
o'Behave Yourself at the SWDB_2018
@author: mariasolbernardezsarria (in collaboration with teammates and TAs)
"""


# add Flash Repeats and Block Number to a panda dataframe. 
#Checks have been included to confirm accuracy in the off-chance that the first 
#and last image presented within a session are the same.
    
class RepeatsCounter(object):
    def __init__(self, first_repeat=1, first_block=1, stimulus_key='image_name', cell_key='cell'):
        
        self.stimulus_key = stimulus_key
        self.cell_key = cell_key
        
        self.first_repeat = first_repeat
        self.first_block = first_block
        
        self.repeat = first_repeat
        self.block = first_block
        
        self.image = None
        self.cell = None
        
    def __call__(self, row):
        if self.cell != row[self.cell_key]:
            self.repeat = self.first_repeat
            self.block = self.first_block
        elif self.image != row[self.stimulus_key]:
            self.block += 1
            self.repeat = self.first_repeat
        else:
            self.repeat += 1
            
        self.image = row[self.stimulus_key]
        self.cell = row[self.cell_key]
            
        return (self.block, self.repeat)


def include_add_repeats(flash_response, all_trials, stimulus_key='image_name'):
    merged = flash_response.merge(all_trials,left_on ='start_time',right_on = 'change_time',how = 'left')
    
    rc = RepeatsCounter(stimulus_key=stimulus_key)
    merged['foo'] = merged.apply(rc, axis=1)
    merged['block'] = merged.apply(lambda row: row['foo'][0], axis=1)
    merged['repeats'] = merged.apply(lambda row: row['foo'][1], axis=1)
    merged = merged.drop(columns=['foo'])
    
    return merged
    
def validate_resets(df):
    def check_flash(row):
        if row['flash_number'] == 0:
            return row['block'] == 1
        else:
            return True
    
    results = df.apply(lambda row: check_flash, axis=1).values
    assert all(results)
    
def validate_block_transitions(df):
    def check(row):
        if row['block'] == 1:
            return row['repeats'] == 1
    
    results = df.apply(lambda row: check, axis=1).values
    assert all(results)
    
    
#function to average the mean_response of the first 3 Flashes/Repeats of every Block 
#can be modified to include relevant repeats
def get_block_mean_response(df, repeats=(1, 2, 3), output_name='three_repeats_mr'):
    data = df.copy()
    data['in_repeats'] = data['repeats'].isin(repeats)
    data = data[data['in_repeats']]
    
    grouped = data.groupby(by=['cell', 'block'])
    
    result = grouped['mean_response'].mean().to_dict()
    output = df.copy()
    output[output_name] = df.apply(lambda row: result[(row['cell'],  row['block'])], axis=1)
    
    return output