import os
import numpy as np
import pandas as pd
from scipy.stats import norm
from datetime import datetime as dt
from matplotlib import pyplot as plt
# from frh_fx.sobol import i4_sobol_generate

def get_deltas(σ,k,t,ρ=0):
    ς = σ*np.sqrt(t[:,np.newaxis])
    Δ = norm.cdf(k/ς + 0.5*ρ**2*ς)
    return Δ

def get_logstrikes(t,Δ=0.05,n=9,σ=0.1):
    δ = np.linspace(Δ,1 - Δ,2*n + 1)[np.newaxis,:]
    k = norm.ppf(δ)*σ*np.sqrt(t[:,np.newaxis])
    return k

def save_data(k,t,σ):
    cwd = os.getcwd()
    if not os.path.exists('data'):
        os.mkdir('data')
    now = dt.now().strftime('%Y%m%d-%H%M%S')
    os.mkdir(os.path.join('data',now))
    os.chdir(os.path.join('data',now))
    pd.DataFrame(k).to_csv('log-strikes.csv',header=False,index=False)
    pd.DataFrame(t).to_csv('maturities.csv',header=False,index=False)
    pd.DataFrame(σ).to_csv('surface.csv',header=False,index=False)
    print('Saved at:',os.path.join(os.getcwd()))
    os.chdir(cwd)
# try exporting data and plots

def save_plot():
    cwd = os.getcwd()
    if not os.path.exists('plots'):
        os.mkdir('plots')
    now = dt.now().strftime('%Y%m%d-%H%M%S')
    # os.mkdir(os.path.join('plots',now))
    # os.chdir(os.path.join('plots'))
    plt.savefig(os.path.join('plots',now))
    print('Saved at:',os.path.join(cwd,'plots'))
    os.chdir(cwd)

def get_drift(Θ):
    α,β,δ = Θ
    γ = np.sqrt(α**2 - β**2)
    μ = - δ*(γ - np.sqrt(α**2 - (β + 1)**2))
    return μ

# def sobol(size=(1,1),seed=0):
#     m,n = size
#     if n > 40:
#         print('Max dimension is n=40!')
#     else:
#         x = i4_sobol_generate(n,m,seed+2).T
#         return x

def convert_deltas(T,Δ,σ):
    T = T[:,np.newaxis]
    Δ = Δ[np.newaxis,:]
    d1 = - norm.ppf(Δ)
    k = 0.5*σ**2*T - d1*σ*np.sqrt(T)
    return k

def import_data(currency,date):
    """
    Function for importing Bloomberg FX volatility data from a csv file for
    a given date. Currency should be passed as 'GBPUSD' and date as '2017-01-31'.
    """
    df = pd.read_csv('data/'+date+'-'+currency+'.csv',header=None)
    T = np.array(df.loc[1:,0]).astype(float)
    Δ = np.array(df.loc[0,1:]).astype(float)/100
    σ = np.array(df.loc[1:,1:]).astype(float)/100
    return T,Δ,σ

def draw_rands(T,γ,ρ,size=(1,1)):
    m,n = size
    v = 1
    ɛ = 1
    return v,ɛ
