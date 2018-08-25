import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from visual_behavior.ophys.response_analysis.utilities import get_trace_around_timepoint,get_nearest_frame

# Local of the event drive path
event_drive_path_AWS = '/data/dynamic-brain-workshop/visual_behavior_events' #AWS Location
drive_path_AWS = 'data/dynamic-brain-workshop/visual_behavior'#AWS Location

def load_dff_events_file(experiment_id,event_drive_path = event_drive_path_AWS):
	'''
	Loads a given behavior event file from a supplied experiment id
	Can be used in conjunction with the manifest file, in a format
	similar to the way dataset objs are called
	Input
	experiment_id: manifest ID
	event_drive_path: Optional. Script has built in drive path to AWS location.
	'''
    event_drive_path = '/data/dynamic-brain-workshop/visual_behavior_events'
    tmp = os.path.join(event_drive_path, str(experiment_id)+'_events.npz')
    tmp_data = np.load(tmp)
    event_array = tmp_data['ev']
    return event_array

def dffBlockPlot(dff,tme,starttme,framerate = 31,window = (-.5,.75),startstop = (0,.25),
                 ax = None,cmap = 'plasma', returnMatrix = False,aspect = 'auto',
                 plotme = True,xlabel = 'Time',ylabel = 'Flash #'):
    '''
    Plots a block dff block plot. 
    Each plotted row represents a single time series (usually a dff trace)
    locked to the starttime and plotted w.in the specified window.
    Inputs
    dff: 1 D time series
    tme: 1 D time series (same size as dff)
    starttme: "trial" start markers
    framerate: 31 (optional), should be frame rate of time series
    window: (-.5,.75) (optional), 
    ax: None (optional), axis to plot on. If not passed, will use gca
    cmap: 'plasma'(optional), colormap
    returnMatrix: False (optional), Default is to return ax. If True, returns ax AND analyis matrix
    plotme: True (optional), option to skip plotting. If true, output will be ONLY analysis matrix
    aspect: 'auto' (optional), input to imshow to specify axis filling 
    xlabel: 'Time' (optional)
    ylabel = 'Flash #' (optional)
    '''
    # Confirm that the window variable is suitable
    window = np.array(window)
    assert window.ndim==1 
    assert len(window) == 2
    
    # if user did not specify an axis, get one.
    if ax is None:
        ax = plt.gca();
        
    # Construct matrix
    window_size = int(np.abs(window[0])*framerate)+int(np.abs(window[1])*framerate)+1
    X = np.zeros([len(starttme),window_size])

    for ii,ts in enumerate(starttme):
        if ((ts+window[0]>tme[0])&(ts+window[1]<tme[-1])):
            ts_idx = get_nearest_frame(ts,tme)
            X[ii,:] = get_trace_around_timepoint(tme[ts_idx],dff,tme,window,framerate)[0]
        
    # plot and return
    if plotme:
        ax.imshow(X,cmap = cmap,aspect = aspect,extent=[window[0],window[1],0,len(X[:,0])-1])  
        #ax.invert_yaxis()
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        if startstop:
            ax.axvline(startstop[0],color = 'cyan')
            ax.axvline(startstop[1],color = 'magenta')

    else:
        return X
    if returnMatrix:
        return ax
    else:
        return X,ax
    
def dffBlockPlot_flashes_allImages(dff,tme,FlashDataFrame,framerate = 31,window = (-.5,.75),
                 fig = None,cmap = 'plasma',aspect = 'auto',
                 xlabel = 'Time',ylabel = 'Flash #'):
    '''
    Wrapper on dffBlockPlot to plot block plots for each image.
    See dffBlockPlot for unspecified documentation
    Inputs
    dff: 1 D time series
    tme: 1 D time series (same size as dff)
    FlashDataFrame: DataFrame in format of DataFrame 
        from visual_behavior.ophys.dataset.visual_behavior_ophys_dataset.VisualBehaviorOphysDataset
    '''
    # Confirm that the window variable is suitable
    window = np.array(window)
    assert window.ndim==1 
    assert len(window) == 2
    
    # if user did not specify an axis, get one.
    if fig is None:
        fig = plt.figure();
    unique_images = np.unique(FlashDataFrame.image_name)
    # make subplots
    ax = fig.subplots(2,len(unique_images)/2)
    ax = ax.flatten()
    
    # plot responce to each image
    for ii, axis in enumerate(ax):
        starttme = FlashDataFrame[FlashDataFrame.image_name==unique_images[ii]].start_time.values
        dffBlockPlot(dff,tme,starttme,ax = axis,framerate = framerate,
                     window = window,cmap = cmap,aspect = aspect,
                     xlabel = xlabel,ylabel = ylabel);
        axis.set_title(unique_images[ii])
    fig.tight_layout()
    
    return fig

def plotMeanFlashResponseOverTime(flash_response_df,cellnumber,ax = None):
	'''
    Plot Allen-provided mean responce for a given cell
    FlashDataFrame: DataFrame in format of DataFrame 
        from from visual_behavior.ophys.response_analysis.response_analysis.ResponseAnalysis
    '''
    # handle axes, in case user didn't define them
    if ax is None:
        ax = plt.gca()
    
    unique_images = np.unique(flash_response_df['image_name'])
    for ii,image in enumerate(unique_images):
        this_responce= flash_response_df[(flash_response_df['image_name']==image)&(flash_response_df['cell']==cellnumber)]['mean_response'].values
        this_frm_idx = flash_response_df[(flash_response_df['image_name']==image)&(flash_response_df['cell']==cellnumber)]['flash_number'].values
        ax.plot(this_frm_idx,this_responce,'.')
    ax.legend(unique_images)
    ax.xlabel('Flash#')
    ax.ylabel('Mean Response')
    return ax