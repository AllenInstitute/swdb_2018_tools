import numpy as np
import os

AWS_EVENTS_PATH = '/data/dynamic-brain-workshop/visual_coding_2p_events'

os.listdir('/paththatdoesntexit')

def get_events(eid, path=AWS_EVENTS_PATH):
    """
        params:
            eid:  The experiment id (integer) for the experimental session
            path:  Path to the visual_coding_2p_events folder, default is the AWS path
        returns:
            events:  array of shape (number of neurons, acquisition frames) containing L0 extracted event magnitudes
    """

    try:
        files = os.listdir(path)
    except OSError as ose:
        print("Path not found.  Please input a path to the 'visual_coding_2p_events' folder using the 'path' optional variable")
        raise ose

    filename = [f for f in files if f[:9] == str(eid)][0]

    events = np.load(filename)

    return events['ev']