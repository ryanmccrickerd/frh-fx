# Helper functions for obtain model prices
# Not to include further analytic funcs
import numpy as np
# from rypy import vlt
from scipy.special import hyp2f1, k1
from scipy.optimize import brentq
from scipy.stats import norm
# Time grid
def time_grid(T,n):
    t = np.linspace(0,T,n+1)[np.newaxis,:]
    return t
# Draw Brownian increments
def brownian_increments(N,n,d,dt):
    dB = np.random.normal(size=(N,n,d))*np.sqrt(dt)
    return dB
def antithetic(dB):
    """
    dB.shape = (N,n,d=2) : brownian increments
    """
    N,n,d = dB.shape
    dW = [np.array([i,j]).reshape(1,1,2)*dB for i in (-1,1) for j in (-1,1)]
    dZ = np.array(dW).reshape(4*N,n,d)
    return dZ
def variance_process(t,Wα,ξ,η,α):
    """
    t.shape = (1,n) : time grid
    Wα.shape = (2,) : indep. volterra processes
    Wα[i].shape = (N,n)
    ξ.shape = (1,n) : forward variance
    η.shape = (2,) : vol vols
    α.shape = (2,) : roughness indices
    """
    v0 = np.exp(η[0]*Wα[0] - 0.5*η[0]**2*t**(2*α[0] + 1))
    v1 = np.exp(η[1]*Wα[1] - 0.5*η[1]**2*t**(2*α[1] + 1))
    v = ξ*v0*v1
    return v
# Non-anticipative Itô / Riemann integral
def ito_integral(h,dW):
    ihdW = np.cumsum(h[:,:-1]*dW,axis=1)
    return ihdW
# Generic price process
def price_process(iσdW,ivdt):
    N,n = iσdW.shape
    x = np.exp(np.hstack((np.zeros((N,1)),iσdW - 0.5*ivdt)))
    return x
def states(Φ,N=2**10,n=252,d=2,T=1.0,s=0,a=True):
    """
    t.shape = (1,n) : time grid
    Wα.shape = (2,) : indep. volterra processes
    Wα[i].shape = (N,n)
    ξ.shape = (1,n) : forward variance
    η.shape = (2,) : vol vols
    α.shape = (2,) : roughness indices
    """
    ξ,η,α = Φ
    dt = T/n
    t = time_grid(T,n)
    np.random.seed(s)
    if a == True:
        dB = brownian_increments(int(N/4),n,d,dt)
        dB = antithetic(dB)
    else:
        dB = brownian_increments(N,n,d,dt)
    dW0 = dB[:,:,0]
    dW1 = dB[:,:,1]
    W0α = vlt.process(t,α[0],dW0)
    W1α = vlt.process(t,α[1],dW1)
    Wα = (W0α,W1α)
    v = variance_process(t,Wα,ξ,η,α)
    σ = np.sqrt(v)
    iσdW = ito_integral(σ,dW1)
    ivdt = ito_integral(v,dt)
    x = price_process(iσdW,ivdt)
    return t,v,x
def prices(x,k,t,n=252):
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
    K = np.exp(k)[np.newaxis,:,:]
    c = np.mean(np.maximum(X - K,0) + X - K - np.minimum(X - K,0),axis=0)/2
    return c
def prices2(x,k,t,n=252,N=1):
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
