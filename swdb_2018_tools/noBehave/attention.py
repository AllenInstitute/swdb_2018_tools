def l0_event_pull(session):
    #input a session id, and output the array L0 events for each cell
    l0 = '/data/dynamic-brain-workshop/visual_behavior_events/%s_events.npz' % session
    l0_events = np.load(l0)['ev']
    return(l0_events)

def graph_compare(mouse1, mouse2, xlim1, xlim2, xlim3=None, xlim4=None): 
    #This function inputs two mice and xlimits, and will output 
    #two graphs with overlayed dff trace and L0 events, with stim events included
    if xlim3 == None:
        xlim3 = xlim1
        xlim4 = xlim2
    slc = mouse1
    vip = mouse2
    
    l0_events_vip = l0_event_pull(vip)
    l0_events_slc = l0_event_pull(slc)
    
    dataset_vip = VisualBehaviorOphysDataset(vip, cache_dir = drive_path)
    dataset_slc = VisualBehaviorOphysDataset(slc, cache_dir = drive_path)
    
    times_vip, traces_vip = dataset_vip.dff_traces
    times_slc, traces_slc = dataset_slc.dff_traces
    
    figsize = (10,10)
    fig, (ax1, ax2) = plt.subplots(2,1,figsize = figsize)

    ax1.plot(times_vip, traces_vip[1], label = 'dF/F Trace')
    ax1.plot(times_vip, l0_events_vip[1], label = 'L0 Events')


    for index in dataset_vip.stimulus_table.index:
        row_data = dataset_vip.stimulus_table.iloc[index]
        if ((row_data.start_time >= xlim1)&(row_data.end_time <= xlim2)):
            ax1.axvspan(xmin=row_data.start_time,xmax=row_data.end_time,facecolor='gray',alpha=0.3)

    ax2.plot(times_slc, traces_slc[4], label = 'dF/F Trace')
    ax2.plot(times_slc,l0_events_slc[4], label = 'L0 Events')

    for index in dataset.stimulus_table.index:
        row_data = dataset_slc.stimulus_table.iloc[index]
        if ((row_data.start_time >= xlim3)&(row_data.end_time <= xlim4)):
            ax2.axvspan(xmin=row_data.start_time,xmax=row_data.end_time,facecolor='gray',alpha=0.3)

    ax1.set_xlim(xlim1,xlim2)
    ax2.set_xlim(xlim3,xlim4)


    ax1.set_title('Vip dF/F vs L0 Events')
    ax2.set_title('Slc dF/F vs L0 Events')
    ax1.set_xlabel('Time(s)')
    ax1.set_ylabel('Event Size')
    
    ax1.legend()
    ax2.legend()
    
    ax2.set_xlabel('Time(s)')
    ax2.set_ylabel('Event Size')
    fig.tight_layout()
    ax.legend()

def experiments_for_donor_id (donor_id):
   # returns experiment_id in an array #
   holder_value = manifest[manifest.donor_id == donor_id]['experiment_id'].values
   return holder_value