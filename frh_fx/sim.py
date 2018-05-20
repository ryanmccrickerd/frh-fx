import numpy as np
from scipy.special import hyp2f1, k1
from scipy.optimize import brentq
from scipy.stats import norm

# def prices(x,k,t,n=252):
#     """
#     t.shape = (1,n) : time grid
#     Wα.shape = (2,) : indep. volterra processes
#     Wα[i].shape = (N,n)
#     ξ.shape = (1,n) : forward variance
#     η.shape = (2,) : vol vols
#     α.shape = (2,) : roughness indices
#     """
#     I = (n*t).astype(int)
#     X = x[:,I][:,:,np.newaxis]
#     K = np.exp(k)[np.newaxis,:,:]
#     c = np.mean(np.maximum(X - K,0) + X - K - np.minimum(X - K,0),axis=0)/2
#     return c

def prices(x,k,t,n=252,N=1):
    """
    t.shape = (1,n) : time grid
    Wα.shape = (2,) : indep. volterra processes
    Wα[i].shape = (N,n)
    ξ.shape = (1,n) : forward variance
    η.shape = (2,) : vol vols
    α.shape = (2,) : roughness indices
    """
    I = (n*t).astype(int)
    X = x[:,I][:,:,np.newaxis]
    if type(N) != int:
        N = N[:,I][:,:,np.newaxis]
    K = np.exp(k)[np.newaxis,:,:]
    c = np.mean(N*(np.maximum(X - K,0) + X - K - np.minimum(X - K,0)),axis=0)/2
    return c
