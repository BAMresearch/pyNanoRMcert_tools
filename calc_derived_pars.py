import numpy as np
import pandas as pd
# for testing only
import unittest
from io import StringIO

def f_calc_derived_pars(df, SASfit=False, distribution='lognormal', intensity_unit='1/cm',
                        concentration_unit='1/cm^3'):
    """
    Calculation of derived particle characteristics:
    *rho*: bulk density of material
    *concentration_unit*: '1/cm^3' or 'mol/l'
    *N1*: number concentration, [N1] = *concentration_unit*
    *c1*: mass concentration, [c1] = micrograms per gram for *concentration_unit* = 1/cm^3
          or [c1] = g/l for *concentration_unit* = mol/l
    *Rm*: radius, [Rm] = nm
    *Dm*: diameter, [Dm] = nm
    *sigma*: width of size distribution, [sigma] = nm
    *v*: volume of particles, [v] = nm^3

    Note: Gaussian size distribution is assumed,
    *SASfit*: False -> eta is used for number concentration here, but not for curve fit
              True -> eta is already used for curve fit
    """
    # particle diameter
    df['D'] = 2*df['Rm']
    df['uD'] = 2*df['uRm']

    # size distribution width
    df['sigma'] = df['D'] * np.sqrt(np.exp(2*df['si']**2)-np.exp(df['si']**2))
    df['usigma']= df['uD']* np.sqrt(np.exp(2*df['si']**2)-np.exp(df['si']**2))
    #+ df['D']*(2*np.exp(2*df['si']**2)*df['si'] + 2*np.exp(df['si']**2)*(-1 + np.exp(df['si']**2)*df['si']))/ (2.*np.sqrt(np.exp(df['si'])**2*(np.exp(df['si'])**2-1. )))

    #df['usigma'] = (df['uD'] * np.sqrt(np.exp(2*df['si']**2)-np.exp(df['si']**2))
    #               + df['D']*(2*np.exp(2*df['si']**2)*df['si'] + 2*np.exp(df['si']**2)*(-1 + np.exp(df['si']**2)*df['si']))
    #                        /(2.*np.sqrt(np.exp(df['si'])**2*(np.exp(df['si'])**2-1.))))

    # particle number concentration
    k = 1
    if intensity_unit == '1/cm':
        k = 1e42 # scaling factor to calculate particle number concentration in units of 1/cm^3
    elif intensity_unit == '1/m':
        k = 1e40
    else:
        raise NotImplementedError
    df['N1'] = k*df['N']
    df['uN1'] = k*df['uN']
    # conversion factor for number concentration in mol/cm^3
    fac_avo = 1
    if concentration_unit == 'mol/l':
        fac_avo = 1e-6 * 6.02214076e23 # combined factors with Avogadro constant
        df['N1']  /= fac_avo * 1e-3 # same as '/N_A*1e9' in previous versions
        df['uN1'] /= fac_avo * 1e-3
    # typically the scattering contrast is already part of the SASfit curve fit
    if not SASfit:
        df['N1']  /= df['eta']**2
        df['uN1'] /= df['eta']**2

    # Volume of a particle
    # correction factor that takes size distribution widths of Gaussian or lognormal into account
    k_distribution = 1
    if distribution.lower() == 'gaussian':
        k_Gauss = (1+3*(df['si']/df['Rm'])**3) # for Gaussian size distribution
        df['k_Gauss'] = k_Gauss
        k_distribution = k_Gauss
    elif distribution.lower() == 'lognormal':
        # for lognormal distribution
        k_lognormal = np.exp(9 * df['si']**2/2)
        df['k_lognormal'] = k_lognormal 
        k_distribution = k_lognormal
    else:
        raise NotImplementedError
    
    df['v'] = k_distribution*4./3.*np.pi*df['Rm']**3
    try:
        variance21 = (4*np.pi*df['Rm']**2*k_distribution)**df['uRm']**2
        variance22 = (12*np.pi*df['si']*df['Rm']**3*k_distribution)**2 * df['usi']**2
        df['uv'] = np.sqrt(variance21+variance22)
    except KeyError:
        df['uv'] = 0.
    
    # Mass concentration of particles
    k_c = 1e-21 # factor 1e-21 to convert nm^3 to cm^3
    df['c1'] = k_c*df['N1']*df['rho']*df['v'] * fac_avo
    try:
        # uncertainty contribution due to number density
        df['uc1N1'] = k_c*df['rho'] * df['v'] * df['uN1'] * fac_avo
        # uncertainty contribution due to particle volume
        df['uc1v'] =  k_c*df['rho'] * df['N1']* df['uv'] * fac_avo
        # combinded uncertainty
        df['uc1'] = np.sqrt(df['uc1N1']**2+df['uc1v']**2)
    except KeyError:
        df['uc1'] = 0.

    return df

class CalcDerivedParsTestCase(unittest.TestCase):
    def setUp(self):
        # Capture test data with
        #   from io import StringIO
        #   csv_buffer = StringIO()
        #   df.to_csv(csv_buffer)
        #   print(csv_buffer.getvalue())
        self.indf = pd.read_csv(StringIO(
             """N,uN,Rm,uRm,si,usi,bkg,ubkg,redchi,eta,rho
             0.1085012144495496,0.0001814495399165621,2.879640435129163,0.002810255749320768,0.2252910498976491,0.0006600846953580116,0.05503957,0,4.164235514420764,679340000000.0,10.49"""),index_col=False)
        self.outdf = pd.read_csv(StringIO(
            """N,uN,Rm,uRm,si,usi,bkg,ubkg,redchi,eta,rho,D,uD,sigma,usigma,N1,uN1,k_lognormal,v,uv,c1,uc1N1,uc1v,uc1
            0.1085012144495496,0.0001814495399165621,2.879640435129163,0.002810255749320768,0.2252910498976491,0.0006600846953580116,0.05503957,0,4.164235514420764,679340000000.0,10.49,5.759280870258326,0.005620511498641536,1.3479314694130662,0.0013154531779029392,3.9039956319021285,0.006528758363108348,1.2565906964837272,125.68899070363065,1.0140696294586864,3.099794850504684,0.005183871464603114,0.025009412501857484,0.02554101088542879"""),index_col=False)

    def test_calc_derived_pars(self):
        df = f_calc_derived_pars(self.indf, SASfit=False, distribution='lognormal',
                                 intensity_unit='1/m', concentration_unit='mol/l')
        pd.testing.assert_frame_equal(df, self.outdf, rtol=1e-12, atol=1e-12)

if __name__ == "__main__":
    unittest.main()
