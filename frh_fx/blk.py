# Functions for Black-Scholes related computations
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq
def price(k,v):
    """
    k.shape = () : log-strike
    v.shape = () : total variance
    """
    σ = np.sqrt(v)
    d1 = -k/σ + 0.5*σ
    d2 = d1 - σ
    p = norm.cdf(d1) - np.exp(k)*norm.cdf(d2)
    return p
def obj_func(σ,k,t,p):
    """
    σ.shape = () : bs volatility
    k.shape = () : log-strike
    t.shape = () : years to maturity
    p.shape = () : option price
    """
    e = price(k,σ**2*t) - p
    return e
def vol(k,t,p):
    """
    k.shape = () : log-strike
    t.shape = () : years to maturity
    p.shape = () : option price
    """
    p = np.maximum(p, np.maximum(1. - np.exp(k),0))
    σ = brentq(obj_func,1e-9,1e+9,args=(k,t,p))
    return σ
# def bs_vol(k,t,p):
#     """
#     k.shape = () : log-strike
#     t.shape = () : years to maturity
#     p.shape = () : option price
#     """
#     p = np.maximum(p, np.maximum(1. - np.exp(k),0))
#     σ = brentq(bs_obj_func,1e-9,1e+9,args=(k,t,p))
#     return σ
# def bs_vols(k,t,p):
#     """
#     k.shape = (n,) : log-strikes
#     t.shape = () : years to maturity
#     p.shape = (n,) : option prices
#     """
#     n = len(k)
#     σ = [bs_vol(k[i],t,p[i]) for i in range(n)]
#     return np.array(σ)
# def bs_surface(k,t,p):
#     """
#     k.shape = (n,*) : log-strikes
#     t.shape = (n,) : years to maturity
#     p.shape = (n,*) : option prices
#     """
#     n = len(t)
#     σ = [bs_vols(k[i,:],t[i],p[i,:]) for i in range(n)]
#     return np.array(σ)
def surface(k,t,p):
    """
    k.shape = (m,n) : log-strikes
    t.shape = (m,) : years to maturity
    p.shape = (m,n) : option prices
    """
    m,n = k.shape
    σ = [[vol(k[i,j],t[i],p[i,j]) for j in range(n)] for i in range(m)]
    return np.array(σ)
