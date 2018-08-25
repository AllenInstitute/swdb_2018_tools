def load_dff_events_file(expt_id):
    #load visual behavior event files by supplying experiment id 
    event_drive_path = '/data/dynamic-brain-workshop/visual_behavior_events' #AWS
    tmp = os.path.join(event_drive_path, str(expt_id)+'_events.npz')
    tmp_data = np.load(tmp)
    event_array = tmp_data['ev']
    return event_array