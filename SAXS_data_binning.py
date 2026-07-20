from jupyter_analysis_tools.binning import reBin
import pandas as pd
import matplotlib.pyplot as plt

def f_SAXS_data_binning_df(df,
                           k_error=1.0,
                           qMin=0.02,
                           qMax=7.,
                           scaling="logarithmic",
                           numBins=100,
                           plot_data=True,
                           plot_title="SAXS data binning",
                           binning=True):
    """Function for binning SAXS data provided as Pandas data frame.
    *k_error*: allows for compensation of over or underestimated uncertainties.
    *scaling*: chose "logarithmic" or "linear" (equidistantly distributed points)."""
    q1, I1, IError1 = df.q.values, df.I.values, k_error*df.e.values

    #print('length of q1-vector is ', len(q)) # sometimes this needs to be checked
    # ---------- Rebinning of the data ---------------
    eMin = 0.01 # minium error of the intensity values is 1%
    binArgs = {"qMin": qMin,   # Input: lower limit of q-values
               "qMax": qMax,   # Input: upper limit of q-values
               "numBins": numBins, # Input: number of suitable bins
               "verbose": False,
               "scaling": scaling,
               "cleanEmpty" : True, 
               "minE": 1e-10}

    # binning:
    reBinning = reBin(**binArgs)
    reBinning.Q = q1
    reBinning.I = I1
    reBinning.E = IError1
    reBinning.validate()
    reBinning.defineBinEdges()
    reBinning.binning1D()
    reBinning.cleanup()
    df0 = pd.DataFrame({'q': q1, 'I': I1, 'e': IError1})
    df1 = pd.DataFrame({'q': reBinning.QBin, 'I': reBinning.IBin, 'e': reBinning.EBin})
    if binning == False:
        df1 = df0
    
    def config_axis(ax, sample_name):
        """appearance of an axis of a plot"""
        ax.set(
            xscale = 'log',
            yscale = 'log',
            title = sample_name,
            xlabel = r'$q$ (nm$^{-1}$)',
            ylabel = 'Intensity',)
        ax.legend()
    BAM_blue     = '#00ffff' # primary color
    BAM_black_15 = '#ccdbdb'
    marker_style_blue = dict(color=BAM_blue, linestyle='', marker='o', fillstyle='none',
                             markersize=5, markeredgewidth=1, markeredgecolor=BAM_blue)
    if plot_data == True:
        plt.rcParams['figure.figsize'] = [1*6.4,4.8]
        fig, ax = plt.subplots()
        ax.errorbar('q', 'I', 'e', data=df0 , color=BAM_black_15, ls=':', label="data")
        ax.errorbar('q', 'I', 'e', data=df1,  **marker_style_blue, label="data_bin")
        config_axis(ax, plot_title)
    return df1
