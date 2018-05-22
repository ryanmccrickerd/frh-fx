# Functions for NIG related computations
import os
import numpy as np
import pandas as pd
from scipy.stats import norm
from scipy.special import k1
from scipy.integrate import quad
from datetime import datetime as dt
# def integrand(x,k,Θ):
#     """
#     x.shape = () : value in nig support (-∞,∞)
#     k.shape = () : log-strike
#     Θ.shape = (4,) : nig params
#     """
#     ρ = (np.exp(x) - np.exp(k))*nig_pdf(x,Θ)
#     return ρ
# def call(k,Θ,u=100):
#     """
#     k.shape = () : log-strike
#     Θ.shape = (4,) : nig params
#     u : upper integral limit
#     """
#     p = quad(nig_integrand,k,u,args=(k,Θ))[0]
#     return p

def inverse_gaussian(δ,γ,size=(1,1)):
    return np.random.wald(δ/γ,δ**2,size=size)

def cross_params(θ1,θ2,ρ):
    α1,β1,δ1 = θ1
    α2,β2,δ2 = θ2
    ω = np.sqrt(np.sqrt((α2**2 - β2**2)/(α1**2 - β1**2))*δ1/δ2)
    β3 = (ω**2*β1 + ω*ρ - β2 - 1)/(ω**2 - 2*ω*ρ + 1)
    δ3 = np.sqrt(ω**2 - 2*ω*ρ + 1)*δ2
    γ3 = np.sqrt(α2**2 - (β2 + 1)**2)/np.sqrt(ω**2 - 2*ω*ρ + 1)
    α3 = np.sqrt(β3**2 + γ3**2)
    μ3 = - δ3*(γ3 - np.sqrt(α3**2 - (β3 + 1)**2))
    return α3,β3,δ3,μ3

def inverse_params(θ1):
    α1,β1,δ1 = θ1
    α0,δ0 = α1,δ1
    β0 = - (β1 + 1)
    γ0 = np.sqrt(α0**2 - β0**2)
    μ0 = - δ0*(γ0 - np.sqrt(α0**2 - (β0 + 1)**2))
    return α0,β0,δ0,μ0

def char_func(p,Θ,t):
    """
    p.shape = () : cmplx value
    Θ.shape = (3,) : nig params
    """
    α,β,δ = Θ
    γ = np.sqrt(α**2 - β**2)
    μ = - δ*(γ - np.sqrt(α**2 - (β + 1)**2))
    ϕ = np.exp(1j*μ*p*t + δ*(γ - np.sqrt(α**2 - (β + 1j*p)**2))*t)
    return ϕ
def ft_integrand(p,k,Θ,t):
    """
    p.shape = () : value in nig support (-∞,∞)
    k.shape = () : log-strike
    Θ.shape = (3,) : nig params
	https://papers.ssrn.com/abstract=2418631
    """
    ρ = (np.exp(-1j*k*p)*char_func(p - .5j,Θ,t)/(p**2 + .25)).real
    return ρ
def ft_price(k,Θ,t,u=np.inf):
    """
    k.shape = () : log-strike
    Θ.shape = (3,) : nig params
    u : integral limits
    """
    p = 1 - 1/2/np.pi*np.exp(k/2)*quad(ft_integrand,-u,u,args=(k,Θ,t))[0]
    return p
def price(k,T,Θ):
    """
    k.shape = (n,m) : log-strike
    Θ.shape = (n,3) : nig params
    u : integral limits
    """
    m,n = k.shape
    p = [[ft_price(k[i,j],Θ,T[i]) for j in range(n)] for i in range(m)]
    return np.array(p)
def pdf(x,Θ):
    """
    x.shape = () : value in nig support (-∞,∞)
    Θ.shape = (4,) : nig params
    """
    μ,δ,β,γ = Θ
    α = np.sqrt(β**2 + γ**2)
    ϕ = np.sqrt(δ**2 + (x - μ)**2)
    ρ = α*δ*k1(α*ϕ)/np.pi/ϕ*np.exp(δ*γ + β*(x - μ))
    return ρ
def log_likelihood(x,Θ):
    """
    x.shape = (n,) : sampled rv
    Θ.shape = (4,) : nig params
	http://www.diva-portal.org/smash/get/diva2:240092/FULLTEXT01.pdf
    """
    μ,δ,β,γ = Θ
    α = np.sqrt(β**2 + γ**2)
    n = len(x)
    ϕ = 1 + ((x - μ)/δ)**2
    a = np.log(α)
    b = δ*np.sqrt(α**2 - β**2) - β*μ
    c = -0.5/n*np.sum(np.log(ϕ))
    d = β/n*np.sum(x)
    e = 1/n*np.sum(np.log(k1(δ*α*np.sqrt(ϕ))))
    f = a + b + c + d + e
    return -f
