import numpy as np

def kernel_fn(x,h):
    return (1./h)*(np.exp(1)**(-(x**2)/h**2))

def get_sdf_from_spike_train(spike_train,h=None):
    n=len(spike_train)
    sdf=np.zeros(n);
    out=np.abs(np.mgrid[0:n,0:n][0]-np.matrix.transpose(np.mgrid[0:n,0:n][0]))
    sdf=1000*np.mean(kernel_fn(out,h)*spike_train,axis=1)
    return sdf