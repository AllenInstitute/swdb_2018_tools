def data_explorer(expt_id, begin, end):

    # AWS1
    drive_path = '/data/dynamic-brain-workshop/visual_behavior'

    manifest_file = 'visual_behavior_data_manifest.csv'

    manifest = pd.read_csv(os.path.join(drive_path,manifest_file))

    #
    experiment_id = expt_id

    # import visual behavior dataset class from the visual_behavior package
    from visual_behavior.ophys.dataset.visual_behavior_ophys_dataset import VisualBehaviorOphysDataset

    dataset= VisualBehaviorOphysDataset(experiment_id, cache_dir=drive_path)

    # attribute method of accesing data
    dff_traces = dataset.dff_traces
    timestamps_ophys = dataset.timestamps_ophys

    from visual_behavior.ophys.response_analysis.response_analysis import ResponseAnalysis 
    analysis = ResponseAnalysis(dataset)
    
    event_drive_path = '/data/dynamic-brain-workshop/visual_behavior_events' #AWS
    tmp = os.path.join(event_drive_path, str(expt_id)+'_events.npz')
    tmp_data = np.load(tmp)
    event_array = tmp_data['ev']

    # Figure setup
    fig,ax = plt.subplots(1,1,figsize=(16,14))

    # Make raster plot
    for i,tr_spikes in enumerate(event_array):
         ax.plot(dataset.timestamps_ophys,dataset.dff_traces[i]+i)
         ax.plot(dataset.timestamps_ophys, event_array[i]+i,'.',color='k')

    plt.plot(dataset.timestamps_stimulus,(dataset.running_speed.running_speed.values*0.05)-8)

    plt.xlim(begin,end)
    #plt.xlim(0,max(dataset.timestamps_ophys))

    # plot rewards
    reward_y_vals = np.repeat(-1,repeats=len(dataset.rewards.time.values))
    plt.plot(dataset.rewards.time.values,reward_y_vals,marker='*',linestyle='None',label='rewards',)

    # # plot licks
    lick_y_vals = np.repeat(-10,repeats=len(dataset.licks.time.values))
    plt.vlines(dataset.licks.values, -2, -5, label='licks', color = 'r')

    for index in dataset.stimulus_table.index:
        row_data = dataset.stimulus_table.iloc[index]
        plt.axvspan(xmin=row_data.start_time,xmax=row_data.end_time,facecolor='gray',alpha=0.3)

    ax.set_ylabel('Cells')
    ax.set_xlabel('time')
    #set ticks
    ax.set_yticklabels( [] , visible=False )

    plt.show()
