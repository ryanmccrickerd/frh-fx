import os
import numpy as np
import pandas as pd
from scipy.stats import norm
from datetime import datetime as dt

def get_deltas(σ,k,t,ρ=0):
    ς = σ*np.sqrt(t[:,np.newaxis])
    Δ = norm.cdf(k/ς + 0.5*ρ**2*ς)
    return Δ

def get_logstrikes(t,Δ=0.05,n=9,σ=0.1):
    δ = np.linspace(Δ,1 - Δ,2*n + 1)[np.newaxis,:]
    k = norm.ppf(δ)*σ*np.sqrt(t[:,np.newaxis])
    return k

def export_surface(k,t,σ):
    cwd = os.getcwd()
    if not os.path.exists('data'):
        os.mkdir('data')
    now = dt.now().strftime('%Y%m%d-%H%M%S')
    os.mkdir(os.path.join('data',now))
    os.chdir(os.path.join('data',now))
    pd.DataFrame(k).to_csv('log-strikes.csv',header=False,index=False)
    pd.DataFrame(t).to_csv('maturities.csv',header=False,index=False)
    pd.DataFrame(σ).to_csv('surface.csv',header=False,index=False)
    print('Exported to:',os.path.join(os.getcwd()))
    os.chdir(cwd)
# try exporting data and plots
def get_drift(Θ):
    α,β,δ = Θ
    γ = np.sqrt(α**2 - β**2)
    μ = - δ*(γ - np.sqrt(α**2 - (β + 1)**2))
    return μ
