import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

from .my_definitions_matplotlib import BAMColors

def f_trapzSim(xvec, yvec, yvecErr):
    """Function to integrate data including an estimate of the uncertainty"""
    #startTime = time.time()
    areavec = np.zeros(10000)
    for i in range(len(areavec)):
        tempy = np.random.normal(loc = yvec, scale = yvecErr)
        #plt.plot(xvec, tempy, 'rx')
        areavec[i] = np.trapz(tempy, xvec)
    assert(all(areavec != 0.))
    area, areaStd = areavec.mean(), areavec.std()
    print("area mean: {:f} ± {:f} (based on {} randomly varied curves)"
          .format(area, areaStd, len(areavec)))
    #print("trapzSim duration: {:f} seconds".format(time.time() - startTime))
    return area, areaStd
    
def f_Invariant(df, bkg=2.5e-1,**kwargs):
    """Determination of the scattering invariant"""
    bkg=bkg # background
    df['q2I']   = df['q']**2*df['I']
    df['q2Ie']  = df['q']**2*df['e']
    df['q2Ibkg']= df['q']**2*(df['I']-bkg)
    
    fig, ax = plt.subplots()
    ax.errorbar('q', 'q2I',    'q2Ie', data=df , color=BAMColors.yellow, ls='-', label="$q^2 I$")
    ax.errorbar('q', 'q2Ibkg', 'q2Ie', data=df , color=BAMColors.red,    ls=':', label="$q^2 (i-bkg)$")
    ax.axhline(y=0., color=BAMColors.blue, linestyle='--', lw = 1)
    ax.set(
        xscale = 'linear',
        yscale = 'linear',
        #title = 'sample: {}'.format(sample_name),
        xlabel = r'$q$ (nm$^{-1}$)',
        ylabel = r'$q^2$ Intensity',)
    #ax.legend()
    #plt.savefig('Figures/sample.png', dpi = 300)
    
    #area, areaStd = trapzSim(x_test, y_test, dy_test)
    print('Invariant without background subtraction')
    area, areaStd = f_trapzSim(df['q'], df['q2I'], df['q2Ie'])
    print(' ')
    print('Invariant after background subtraction')
    area, areaStd = f_trapzSim(df['q'], df['q2Ibkg'], df['q2Ie'])
    return area, areaStd

