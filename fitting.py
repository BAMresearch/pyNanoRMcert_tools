# -*- coding: utf-8 -*-
# fitting.py

import glob
import os
import sys
import re
import io
import time
from contextlib import redirect_stdout
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from PIL import Image # for buffering plots in f_fit_data(), used with multiprocessing
from .utils import loggg
# scattering functions
from .scattering_models import f_lognormal_sphere, f_gaussian_sphere
# data reading/parsing functions
from jupyter_analysis_tools import readdata
# read SAXS data binning helpers
from .SAXS_data_binning import f_SAXS_data_binning_df
# optimization functions
from lmfit import minimize, Parameters

def f_resid(params, q, data=None, eps=None, distrib='lognormal'):
    """SAXS of Gaussian or lognormal size distribution of spheres 
    Residuals to be minimized in a curve fit
    https://lmfit.github.io/lmfit-py/examples/example_reduce_fcn.html#sphx-glr-examples-example-reduce-fcn-py
    Fit Specifying Different Reduce Functions
    """
    N = params['N'].value    # scaling factor
    Rm = params['Rm'].value   # median radius
    si = params['si'].value   # size distribution width in nm for Gaussian, no unit for lognormal
    try:
        bkg = params['bkg'].value # constant scattering background
    except KeyError:
        bkg = 0.
    
    # --- scattering contribution of spheres with size distribution ----
    assert distrib in ('lognormal', 'gaussian')
    if distrib == 'lognormal':
        intensity = f_lognormal_sphere(q, N, Rm, si)
    if distrib == 'gaussian':
        intensity = f_gaussian_sphere(q, N, Rm, si)
    
    # --- scattering model ---
    model = intensity + bkg
    
    if data is None: # for plotting of the scattering cuve
        return model        
    if eps is None:  # for curve fit of data without uncertainty values
        #return model - data # for least square optimization of a "normal fit" 
        data2=data.copy()
        data2[data2<0.]=0. # set negative intensites to zero
        # otherwise minimization of log( model-data) may produce errors
        # or if model-data is negative the np.log(np.abs(model - data2)) values 
        # may influence the model in a physically meaningless way
        return np.log(np.abs(model - data2)) # minimize logarithmic differences
    
    if data is not None and eps is not None:
        data2=data.copy()
        data2[data2<0.]=0. # set negative intensites to zero
        #return (model-data2)/eps # "normal" fit
        return np.log(np.abs((model-data2)/eps)) # minimize logarithmic differences
    
    #return (model-data)/eps # for curve fit of data with uncertainy values
    return print('check input')#np.log(np.abs((model-data)/eps)) # for curve fit of data with uncertainy values


def datafileBasename(filename):
    return os.path.splitext(os.path.basename(filename))[0].split('[')[0]

@loggg
def f_fit_data(df_data, outdir, params=None, distrib=None, Sample_ID=None, SAXS_ID=None,
               filename=None, date_SAXS=None, plot_start=True, fit=True,
               eps=False, save_fit=True):
    """function for curve fitting"""
    #print('filename:', filename)
    print('distribution_selected:', distrib)

    q = df_data['q'].values
    I = df_data['I'].values
    e = df_data['e'].values
    
    if plot_start: # plot the initial estimate for curve fit
        fig, ax = plt.subplots(1,1)
        ax.plot(q, I, ls=':', label='I')
        I_start=f_resid(params, q, data=None)
        ax.plot(q, I_start, ls='-', label='I_start')
        ax.set(xscale= 'log', yscale='log', 
                xlabel= r'$q$ (nm$^{-1}$)',ylabel= r'Intensity', title='{}'.format(filename),)
        ax.legend()
        plt.show()
        
    if not fit:
        return
    # performing the fit
    if eps:
        # e-values (uncertainties of I values) are used for curve fit
        out = minimize(f_resid, params, args=(q,), kws={'data':I, 'eps': e})
    else:
        # no uncertainties used for curve fit
        out = minimize(f_resid, params, args=(q,), kws={'data':I})

    df_data['Ifit']=f_resid(out.params, q, data=None)

    fig, ax = plt.subplots(1,1)
    ax.plot('q', 'I',    data=df_data, ls=':', label='I')
    ax.plot('q', 'Ifit', data=df_data, ls='-', color='r',label='Ifit')
    ax.set(xscale= 'log', yscale='log',
           xlabel= r'$q$ (nm$^{-1}$)', ylabel= r'Intensity', title='{}'.format(filename),)
    ax.legend()
    # a buffer for plotting outside
    plotbuf = io.BytesIO()
    plt.savefig(plotbuf)

    if save_fit:
        # Directory for storage of figures and results
        outdir = os.path.abspath(outdir)
        # basename of the files to be stored
        base_name = datafileBasename(filename)
        fnplot = os.path.join(outdir, base_name + '.png')
        print("Storing results:")
        print("    plot:  ", fnplot)
        plt.savefig(fnplot)
        fnfit = os.path.join(outdir, base_name + 'fit.xlsx')
        print("    fit:   ", fnfit)
        df_data.to_excel(fnfit, index=False)
        try: # save the fit parameteres
            d_res={'Sample_ID': Sample_ID,
                   'SAXS_ID': SAXS_ID,
                   'file': filename,
                   'date': date_SAXS,
                   'distribution': distrib}

            for key in out.params.keys():
                d_res[key]=[out.params[key].value]
                d_res['u'+key]=[out.params[key].stderr]
                if out.params[key].stderr is None:
                    d_res['u'+key] = 0.

            # reduced chi^2
            d_res['redchi']=out.redchi
            df_res=pd.DataFrame(d_res)

            fnpars = os.path.join(outdir, base_name + 'fitpar.xlsx')
            print("    params:", fnpars)
            df_res.to_excel(fnpars, index=False)

        except ValueError:
            print('something went wrong with the out.params')

    plt.close()
    # return plot buffer as image array, allows to run this in parallel without loosing plots
    plotbuf.seek(0)
    plotimg = np.array(Image.open(plotbuf))
    plotbuf.close()
    return df_data, out, plotimg

def showBufferedPlots(plots):
    """Show plots provided as numpy array raster images (from background threads)"""
    # creating a figure where to plot to
    figwidth, figheight = mpl.rcParams["figure.figsize"]
    _, axes = plt.subplots(nrows=1, ncols=len(plots),
                           figsize=(figwidth*2.5, figheight*1.5), tight_layout=True)
    for ax, plotimg in zip(axes, plots):
        # hide axis decorations for showing a pixel grid with an embedded axis
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        # plot the raster image into this axis
        ax.imshow(plotimg)
    plt.show() # show all axes

def numFilesCompleted(filelist, outdir):
    return sum([bool(len(glob.glob(os.path.join(outdir, datafileBasename(fn)+"*"))))
                for fn in filelist])

@loggg
def fit_files(filelist, outdir, qrange, distrib='lognormal', initParams=None, nthreads=None,
              Sample_IDs=None, SAXS_IDs=None,
              date_SAXS=None, read_csv_args=None):
    """Processes *filelist* sequentially in a single thread (*nthreads*=1)
    or in parallel (*nthread*=None)."""
    # Directory for storage of figures and results
    outdir = os.path.abspath(outdir)
    # explicitly add all arguments to maintain the ordering
    allargs = [(fn, i, len(filelist), outdir, qrange, distrib, initParams,
                Sample_IDs[i] if Sample_IDs else None,
                SAXS_IDs[i] if SAXS_IDs else None,
                date_SAXS, read_csv_args)
                for i, fn in enumerate(filelist)]
    if nthreads == 1:
        # set buffer_stdout to print text immediately but all text will be shown before plots
        results = [fit_file(*args, buffer_stdout=False) for args in allargs]
    else: # Using multiple CPU cores if available
        import multiprocess # pip install multiprocess
        if not nthreads:
            nthreads = multiprocess.cpu_count()
        pool = multiprocess.Pool(processes = nthreads)
        results = pool.starmap_async(fit_file, allargs)
        while not results.ready():
            # Misleading if previous results files still exist
            print(f"\rCompleted {numFilesCompleted(filelist, outdir)} of {len(filelist)} files...", end="")
            time.sleep(2)
        pool.close()
        pool.join()
        print(f"\rCompleted {numFilesCompleted(filelist, outdir)} of {len(filelist)} files:")
        results = results.get()
    # when done, show accumulated output generated by each 'eval_file()' call
    for outbuf, out, plots in results:
        if hasattr(outbuf, "getvalue"):
            print(outbuf.getvalue()) # print all text output produced by 'print()'
        # show plots generated by each 'eval_file()' call
        showBufferedPlots(plots)
        # show parameter table from 'eval_file()'
        if out:
            print(out.params)

def f_get_date_measurement(file_selected):
    """Read the date at which the measurement was performed from a pdh-file of the SAXSess data"""
    #print('filename is', file_selected)
    with open(file_selected) as fd:
        content = fd.read()
        start=content.index('"DateTime" type="DateTime" db="P">')
        end = content.index("</value>",start)
        date_SAXS = (content[start:end])
        date_SAXS = date_SAXS.split(">")[1].split("T")[0]
    return date_SAXS

def fit_file(fn, i, count, outdir, qrange, distrib=None, initParams=None,
             Sample_ID=None, SAXS_ID=None, date_SAXS=None,
             read_csv_args=None, buffer_stdout=True):
    """*date_SAXS*: Allows to override the measurement date if not readable from file.
    *buffer_stdout*: Store text output in a buffer to print it later along with the plots.
    """
    out, outbuf = None, sys.stdout
    if buffer_stdout:
        outbuf = io.StringIO()
    with redirect_stdout(outbuf):
        print(f"Evaluation number i = {i+1} (of {count})")
        # 1. select  file and q-range for curve fit
        #print("fn:", fn) # for debugging
        if not Sample_ID:
            Sample_ID = re.search(r"ID[0-9]+", fn).group()
        if not SAXS_ID:
            SAXS_ID =   re.search(r"S[0-9]+", fn)
            if SAXS_ID: # found the pattern
                SAXS_ID = SAXS_ID.group()
            else:
                SAXS_ID = os.path.splitext(os.path.basename(fn))[0]
        print('Sample_ID:', Sample_ID)
        print('SAXS_ID:  ', SAXS_ID)

        if not date_SAXS:
            # get the measurement date from file if not given
            date_SAXS = f_get_date_measurement(fn)
        print('Date of measurement:', date_SAXS)

        # 2. read file as pandas dataframe and the file name
        df_data, file_name = readdata(fn, q_range=qrange,
                                      read_csv_args=read_csv_args)

        # 3. produce a binned file for a first fast curve fit
        df_binned = f_SAXS_data_binning_df(df_data, k_error=1.0, numBins=50, binning=True,
                                           qMin=min(qrange), qMax=max(qrange),
                                           scaling='logarithmic', plot_data=False)

        #if i >=0: # start always with the same start fit parameteres
            # if i ==0 means that for i>0 the fitted value for i+1 are used as start values
            # this makes the fit procedure faster but seem to produce a bias in the fits
            #print(i)
            #initialize parameters
            # defining the parameters and providing the initial values
        assert isinstance(initParams, Parameters), \
            "Please provide a lmfit Parameters object containing the parameters N, Rm, si and bkg!"
        #initParams.pretty_print() # Show actual fit params, for debugging
        if 'bkg' not in initParams:
            initParams.add('bkg', value=df_data.I.min(), vary=False)

        ## 4 fit the binned data
        print("Fitting binned data to the model for parameter estimates ...")
        df_binned, out, plot_binned = f_fit_data(df_binned, outdir, params=initParams, distrib=distrib,
                    Sample_ID=Sample_ID, SAXS_ID=SAXS_ID, filename=fn,
                    plot_start=False, fit=True, eps=None, save_fit=False)
        #out.params.pretty_print() # Show actual fit params, for debugging

        # 5. Fit the data
        print("Fitting full data to the model with estimates as initial parameters ...")
        df_data, out, plot_data = f_fit_data(df_data, outdir, params=out.params, distrib=distrib,
                    Sample_ID=Sample_ID, SAXS_ID=SAXS_ID, filename=fn,
                    date_SAXS=date_SAXS,
                    plot_start=False, fit=True, eps=None, save_fit=True)
        #out.params.pretty_print() # Show resulting fit params, for debugging
    # finally, print all output at once to prevent interweaved messages
    return outbuf, out, (plot_binned, plot_data)

# vim: set ts=4 sts=4 sw=4 tw=0:
