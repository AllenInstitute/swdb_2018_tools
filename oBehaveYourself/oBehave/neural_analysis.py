import numpy as np
import scipy as sp
from sklearn.decomposition import PCA
from oBehave.plotting_stuff import dffBlockPlot


def singlecellpca(dff,tme,starttime,nPCs = 1,window=(0,.75)):
    '''
    Do PCA to an all of a cells image responses within a specified window.
    Inputs:
    dff: dff trace for a given cell
    tme: timestamps for dff trace
    starttime: list of timestamps to do PCA over. Usually image flash or change times
    nPCs: number of pcs to charecterize response with (default is 1, and I can't 
        garentee behavior of this function with more than that...)
    window: window to look around starttimes, in seconds. default = (0,.75)
    Returns: resonses for each starttime (trial/Flash/etc.) projected onto first PC. 
        This maximizes variance of neuron, which might help see changes in e.g. image selectivity
        
    NOTE: in practice, this really didn't seem to behave differently from the mean responses in
    the analysis dataframe. Since the PCs take a min to compute and are a little tedious to work with,
    we didn't follow through with this line of analyiss
    
    Created by Yoni Browning, August 2018
    '''
    
    X = dffBlockPlot(dff,tme,starttime,window = window,plotme = False);
    pca = PCA()
    a = pca.fit_transform(X)
    a = a[:,:nPCs].T
    a = a[0]
    return a,pca

def sparsity(image_responses):
    '''
    # image responses should be an array of the trial averaged responses to each image
    # sparseness = 1-(sum of trial averaged responses to images / N)squared / (sum of (squared mean responses / n)) / (1-(1/N))
    # N = number of images
    # Borrowed shamelessly from visual behavior tutorial code. 
    
    NOTE: There should probably be an absolute value around the image responses 
        in the numerator of this expression. It doesn't when working with the mean responses,
        but in its current form this assumes that responses are always positive. If you want
        to do something fancy with e.g. singlecellpca (in which responses can be negative)
        this will give you wonky sparsity values (like all sparsity = 1.14...)
    '''
    N = float(len(image_responses))
    ls = ((1-(1/N) * ((np.power(image_responses.sum(axis=0),2)) / (np.power(image_responses,2).sum(axis=0)))) / (1-(1/N)))
    return ls