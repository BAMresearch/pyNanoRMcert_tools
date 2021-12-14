import numpy as np
from scipy.special import erf
import matplotlib.pyplot as plt 

def f_lognormal(R, N, Rm, si):
    """Log normal distribution
    *N*: scaling factor
    *Rm*: median value of the radius
    *si*: width parameter, [si] = 1"""
    return N/(np.sqrt(2*np.pi)*si*R)*np.exp(- ((np.log(R/Rm))**2)/(2*si*si))
    
def f_lognormal_cdf(R, N, Rm, si):
    """cdf of lognormal distribution numerically calculated
    *N*: scaling factor
    *Rm*: median value of the radius
    *si*: width parameter"""
    cdf = N*(0.5 + 0.5*erf(np.log(R/Rm)/(np.sqrt(2)*si)))
    return cdf

def f_gaussian(R, N, Rm, si):
    """Gaussian normal distribution
    N: scaling factor
    Rm: mean value of the radius
    si: width parameter"""
    pdf = N/(np.sqrt(2*np.pi)*si)*np.exp(- 0.5*((R-Rm)/si)**2)
    return pdf

def f_gaussian_cdf(R, N, Rm, si):
    """cdf of Gaussian normal distribution
    N: scaling factor
    Rm: mean value of the radius
    si: width parameter"""
    cdf = N*0.5*(1+erf((R-Rm)/(si*np.sqrt(2))))
    return cdf
    
def f_plot_lognormal(R, N, Rm, si, xrange=None):
    """Plot log normal size distribution"""
    pdf = f_lognormal(R, N, Rm, si)
    cdf = f_lognormal_cdf(R, N, Rm, si)
    fig, ax = plt.subplots(1,1)
    ax.plot(R, pdf, ls=':', label='pdf')
    ax.set(xscale='linear')
    ax2 = ax.twinx()
    ax2.plot(R, cdf, label='cdf')
    ax.set(
        xscale='linear', xlabel=r'$R$ (nm)',
        yscale='linear', ylabel='pdf', title='lognormal distribution')
    ax.legend()
    ax2.legend()
    if xrange:
        ax.set_xlim(xrange)

def f_plot_gaussian(R, N, Rm, si, xrange=None):
    """Plot log normal size distribution"""
    pdf = f_gaussian(R, N, Rm, si)
    cdf = f_gaussian_cdf(R, N, Rm, si)
    fig, ax = plt.subplots(1,1)
    ax.plot(R, pdf, ls=':', label='pdf')
    ax.set(xscale='linear')
    ax2 = ax.twinx()
    ax2.plot(R, cdf, label='cdf')
    ax.set(
        xscale='linear', xlabel=r'$R$ (nm)',
        yscale='linear', ylabel='pdf', title='Gaussian distribution')
    ax.legend()
    ax2.legend()
    if xrange:
        ax.set_xlim(xrange)