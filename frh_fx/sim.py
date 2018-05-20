import numpy as np
from frh_fx import uts, nig
from scipy.special import hyp2f1, k1
from scipy.optimize import brentq
from scipy.stats import norm

# would suit a class structure but haven't got around to it

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

def subordinator(T,γ,size=(1,1)):
    m,n = size
    Δ = T/n
    v = nig.inverse_gaussian(Δ/γ,1/γ,size=(m,n))
    return v

def scaled_sub(v,σ,ρ):
    V = σ**2*(1 - ρ**2)*v
    return V

def correlated_noise(ρ,size=(1,1)):
    m,n = size
    ɛ1 = np.random.normal(size=(m,n))
    ɛ2 = ρ*ɛ1 + np.sqrt(1 - ρ**2)*np.random.normal(size=(m,n))
    return ɛ1,ɛ2

def nig_process(v,ɛ,Δ,Θ,drift_correct=True):
    m,n = v.shape
    μ = uts.get_drift(Θ)
    α,β,δ = Θ
    dx = β*v + np.sqrt(v)*ɛ + μ*Δ
    x = np.hstack((np.zeros((m,1)),np.cumsum(dx,axis=1)))
    if drift_correct:
        X = np.exp(x)/np.mean(np.exp(x),axis=0)
    else:
        X = np.exp(x)
    return X
