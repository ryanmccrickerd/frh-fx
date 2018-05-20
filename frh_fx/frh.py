import numpy as np
from scipy.integrate import quad

def nig_params(σ,ρ,γ):
    α = np.sqrt(4 - 4*ρ*γ*σ + γ**2*σ**2)/2/γ/σ/(1 - ρ**2)
    β = - (γ*σ - 2*ρ)/2/γ/σ/(1 - ρ**2)
    δ = σ/γ*np.sqrt(1 - ρ**2)
    μ = - σ/γ*ρ
    return α,β,δ,μ

# def generator(p,σ,ρ,γ):
#     """
#     p.shape = () : value in nig support (-∞,∞)
#     σ.shape = () : level
#     ρ.shape = () : skewness
#     γ.shape = () : kurtosis
#     https://papers.ssrn.com/abstract=2418631
#     """
#     Λ = (1 - 1j*σ*ρ*γ*p -
#          np.sqrt((1 - 1j*σ*ρ*γ*p)**2 + (σ*γ)**2*(p**2 + 1j*p)))/γ**2
#     return Λ

def generator(u,p,θ):
    σ,ρ,γ = θ
    i = 1j
    Λ = (1 - i*σ(u)*ρ(u)*γ(u)*p -
         np.sqrt((1 - i*σ(u)*ρ(u)*γ(u)*p)**2 + (σ(u)*γ(u))**2*(p**2 + i*p)))/γ(u)**2
    return Λ

def gen_real(u,p,θ):
    return generator(u,p,θ).real
def gen_imag(u,p,θ):
    return generator(u,p,θ).imag

def char_func(t,p,θ):
    Φ = np.exp(quad(gen_real,0,t,args=(p,θ))[0] +
            1j*quad(gen_imag,0,t,args=(p,θ))[0])
    return Φ

# piecewise const
# def char_func(p,t,Θ):
#     """
#     p.shape = () : value in nig support (-∞,∞)
#     t.shape = () : maturity
#     Θ.shape = (4,) : frh params
#     """
#     u,σ,ρ,γ = Θ
#     # Unpack np array
#     # u,σ,ρ,γ = np.squeeze(np.hsplit(Θ,4))
#     u = np.hstack(([0],u))
#     du = np.diff(u)
#     Λ = 0
#     for i in range(len(u)):
#         if t < u[i+1]:
#             Λ += generator(p,σ[i],ρ[i],γ[i])*(t - u[i])
#             break
#         else:
#             Λ += generator(p,σ[i],ρ[i],γ[i])*du[i]
#             if t == u[i+1]:
#                 break
#     Φ = np.exp(Λ)
#     return Φ

def ft_integrand(p,k,t,θ):
    """
    p.shape = () : value in nig support (-∞,∞)
    k.shape = () : log-strike
    Θ.shape = (4,) : nig params
    https://papers.ssrn.com/abstract=2418631
    """
    ρ = (np.exp(-1j*k*p)*char_func(t,p - .5j,θ)/(p**2 + .25)).real
    return ρ

# def ft_integrand(p,k,t,Θ):
#     """
#     p.shape = () : value in nig support (-∞,∞)
#     k.shape = () : log-strike
#     t.shape = () : maturity
#     Θ.shape = (4,) : frh params
#     """
#     ρ = (np.exp(-1j*k*p)*char_func(p - .5j,t,Θ)/(p**2 + .25)).real
#     return ρ

def ft_price(k,t,θ,u=np.inf):
    """
    k.shape = () : log-strike
    Θ.shape = (4,) : nig params
    u : integral limits
    """
    p = 1 - 1/2/np.pi*np.exp(k/2)*quad(ft_integrand,-u,u,args=(k,t,θ))[0]
    return p

# def ft_price(k,t,Θ,u=np.inf):
#     """
#     k.shape = () : log-strike
#     t.shape = () : maturity
#     Θ.shape = (4,) : frh params
#     u : integral limits
#     """
#     p = 1 - 1/2/np.pi*np.exp(k/2)*quad(ft_integrand,-u,u,args=(k,t,Θ))[0]
#     return p

def price(k,t,θ):
    """
    k.shape = (n,m) : log-strike
    Θ.shape = (n,4) : nig params
    u : integral limits
    """
    m,n = k.shape
    p = [[ft_price(k[i,j],t[i],θ) for j in range(n)] for i in range(m)]
    return np.array(p)

# def price(k,t,Θ):
#     """
#     k.shape = (n,m) : log-strikes
#     t.shape = (n,) : maturities
#     Θ.shape = (4,) : frh params
#     """
#     n,m = k.shape
#     p = [[ft_price(k[i,j],t[i],Θ) for j in range(m)] for i in range(n)]
#     return np.array(p)

# def pc_crv(t,α):
#     n = len(t)
#     x = np.zeros(2*n)
#     y = np.zeros(2*n)
#     x[ 1] = t[ 0]
#     y[ 0] = α[ 0]
#     y[ 1] = α[ 0]
#     x[-2] = t[-2]
#     x[-1] = t[-1]
#     y[-2] = α[-1]
#     y[-1] = α[-1]
#     for i in np.arange(1,n-1):
#         x[2*i  ] = t[i-1]
#         x[2*i+1] = t[i  ]
#         y[2*i  ] = α[i  ]
#         y[2*i+1] = α[i  ]
#     return (x,y)
