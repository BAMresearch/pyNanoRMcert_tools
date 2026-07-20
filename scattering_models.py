import numpy as np
from numpy import sin, cos
import scipy.integrate as integrate 
from scipy.integrate import quad_vec
from .distributions import f_lognormal, f_gaussian

def f_gaussian_sphere(q, N, Rm, si, method=1):
    """Scattering of spheres with Gaussian size distribution
    *N*:  scaling factor
    *Rm*: median radius
    *si*: width of size distribution, [si] = nm,
    Note: upper limit of integration here is set to 5 Rm, which was found sufficient for typical values of si
    """

    def f_P_sphere(q,R):
        """form factor of a sphere"""
        a_sphere   = 3.*(sin(q*R)-q*R*cos(q*R))/(q*R)**3
        return a_sphere**2

    if method == 1:
        def integrand(R,N,Rm,si,q):
            v=4./3.*np.pi*R**3
            f = f_gaussian(R,N,Rm,si)*v**2*f_P_sphere(q,R)
            return f

        def curve(q,N,Rm,si):
            x0=5*Rm # integration up to 5 times the mean radius Rm
            res = integrate.quad(integrand, 0, x0, args=(N,Rm,si,q)) #x0 is the independent variable here
            return res[0]

        vcurve = np.vectorize(curve)#, excluded=set([1])) # vectorizing the output of the function which includes the integration step
        return vcurve(q,N,Rm,si)

    if method == 2:
        #def integrand(R):
        #    f = f_Gaussian(R,N,Rm,si)*f_P_sphere(q,R)
        #    return f
        #vcurve = integrate.quad_vec(integrand, 0, 5*Rm)[0]
        #return vcurve
    
        f = lambda R: N/(np.sqrt(2*np.pi)*si)*np.exp(- 0.5*((R-Rm)/si)**2)*(4./3.*np.pi*R**3)**2*(3.*(sin(q*R)-q*R*cos(q*R))/(q*R)**3)**2
        f_int=quad_vec(f, 0, 5*Rm)
        return f_int[0]

def f_lognormal_sphere(q, N, Rm, si, method=1):
    """Scattering of spheres with LogNormal size distribution
    *method*: 1 uses vectorize of quad for integration
    *method*: 2 uses quad_vec for integration
    *N*:  scaling factor
    *Rm*: median radius
    *si*: width parameter of size distribution
    Note: upper limit of integration here is set to 5 Rm, which was found sufficient for typical values of si
    """

    def f_P_sphere(q,R):
        """form factor of a sphere"""
        a_sphere   = 3.*(sin(q*R)-q*R*cos(q*R))/(q*R)**3
        return a_sphere**2

    if method ==1:
        def integrand(R,N,Rm,si,q):
            v=4./3.*np.pi*R**3
            f = f_lognormal(R,N,Rm,si)*v**2*f_P_sphere(q,R)
            return f

        def curve(q,N,Rm,si):
            x0=5*Rm # integration up to 5 times the mean radius Rm
            res = integrate.quad(integrand, 0, x0, args=(N,Rm,si,q)) #x0 is the independent variable here
            return res[0]

        vcurve = np.vectorize(curve)#, excluded=set([1])) # vectorizing the output of the function which includes the integration step
        return vcurve(q,N,Rm,si)

    if method ==2:
        f = lambda R: N/(np.sqrt(2*np.pi)*si*R)*np.exp(- ((np.log(R/Rm))**2)/(2*si*si))*(4./3.*np.pi*R**3)**2*(3.*(sin(q*R)-q*R*cos(q*R))/(q*R)**3)**2
        f_int=quad_vec(f, 0, 5*Rm)
        return f_int[0]