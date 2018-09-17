import numpy as np
import pandas as pd
from datetime import datetime

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


def includeDateTime(manifest,dateStringKey = 'experiment_date',datetimeKey = 'experiment_datetime',dateConversionStr = '%m/%d/%Y %H:%S'):
    experiment_date = manifest[dateStringKey].values
    experiment_datetime = []
    for date in experiment_date:
        experiment_datetime.append(datetime.strptime(date,dateConversionStr))
    manifest[datetimeKey] = pd.Series(experiment_datetime)
    return manifest

def includeNovelSession(manifest):
    '''
    Appends a Series to manifest dataframe to indicate if this session is the first time that this mouse did each behavioral task.
    Inputs: Allen style manifest 
    '''
    if not ('experiment_datetime' in manifest.columns):
        includeDateTime(manifest);
    
    unique_donors = np.unique(manifest['donor_id'])
    manifest.sort_values('experiment_datetime',ascending = True)
    manifest['first_session'] = pd.Series(np.zeros(manifest['session_type'].shape,dtype = bool))
    behavior_types = np.unique(manifest.session_type)
    for ii,donor in enumerate(unique_donors):
        thismouse = manifest[manifest.donor_id==donor].sort_values('experiment_datetime',ascending = True)
        for beh in behavior_types:
            if beh in thismouse.session_type.values:
                experiment_id = thismouse[thismouse.session_type==beh]['experiment_id'].values[0]
                Rindex = manifest[manifest['experiment_id']==experiment_id].index[0]
                manifest.at[Rindex,'first_session'] = 1
    return manifest

def includeAddRepeats_dataset(flash_data_frame,trial_data_frame):
    '''
    Computes the number of repeats in a flash data frame
    Inputs:
    flash_data_frame = ResponseAnalysis().flash_response_df
    trial_data_frame = VisualBehaviorOphysDataset().all_trials
    
    
    '''
    flash_data_join = flash_data_frame.merge(trial_data_frame,left_on ='start_time',right_on = 'change_time',how = 'left')
    addthis = np.zeros((len(flash_data_frame['image_name'].values,)))
    addblock = np.zeros((len(flash_data_frame['image_name'].values,)))
    addblocktype = []
    addthis[0] = 1
    addblock[0] = 1
    addblocktype = [None]
    for nn in np.arange(1,len(addthis),1):
        if flash_data_frame['image_name'][nn]==flash_data_frame['image_name'][nn-1]:
            addthis[nn] = addthis[nn-1]+1
            addblock[nn] = addblock[nn-1]
            addblocktype.append(addblocktype[nn-1])
        else:
            addthis[nn] = 1
            addblock[nn] = addblock[nn-1]+1
            addblocktype.append(flash_data_join['response_type'][nn])
            
    flash_data_frame['repeats'] = addthis
    flash_data_frame['block'] = addblock
    flash_data_frame['response_type'] = addblocktype
    return flash_data_frame

def moving_response_average(dataset,window = 5, tme = None):
    '''
    Computes a moving average behavior hit rate and correct reject rate.
    Returns hit rate and correct r
    Inputs:
    dataset: behavior dataset from allen tools
    window: moving trial average window (optional, default is 5)
    tme: time steps for upsampling. If None (default) uses dataset.timestamps_ophys
    Returns:
    cont_go_ave: moving average hit rate
    cont_catch_ave: moving average of correct response rate
    '''
    trldata = dataset.trials
    catch_tmes = trldata[trldata.trial_type == 'catch']['change_time']
    go_tmes = trldata[trldata.trial_type=='go']['change_time']
    catch_correct = trldata[trldata.trial_type=='catch']['response_type']=='CR'
    go_correct = trldata[trldata.trial_type=='go']['response_type']=='HIT'

    go_ave = np.convolve(go_correct, np.ones((window,))/window, mode='same')
    catch_ave = np.convolve(catch_correct,np.ones((window,))/window, mode='same')
    
    if tme is None:
        cont_go_ave = np.interp(dataset.timestamps_ophys,go_tmes,go_ave)
        cont_catch_ave = np.interp(dataset.timestamps_ophys,catch_tmes,catch_ave)
    else:
        cont_go_ave = np.interp(tme,go_tmes,go_ave)
        cont_catch_ave = np.interp(tme,catch_tmes,catch_ave)

    return cont_go_ave,cont_catch_ave