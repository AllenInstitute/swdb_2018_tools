# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 21:52:27 2018

@author: Stav
"""

def get_all_regions(multi_probe_expt_info):    
#    all_regions = []
#    
#    for multi_probe_example in range(len(multi_probe_expt_info)):
#    
#        multi_probe_filename  = multi_probe_expt_info.iloc[multi_probe_example]['nwb_filename']
#    
#        # Specify full path to the .nwb file
#        nwb_file = os.path.join(drive_path,multi_probe_filename)
#    
#        data_set = NWB_adapter(nwb_file)
#        unique_regions = np.unique(data_set.unit_df['structure'])
#        unique_list = list(unique_regions)
#        all_regions.extend(unique_list)
#    
#    all_regions = list(set(all_regions))
    
    all_regions = ['VISp', 'VISrl', 'DG', 'CA', 'VISal', 'VISam', 'SCs', 'TH', 'VISpm', 'VISl']

    return all_regions