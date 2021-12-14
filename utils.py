# -*- coding: utf-8 -*-
# utils.py

import os
import matplotlib.pyplot as plt

def f_makedir_figures(dir_figures):
    """Create a directory for storage of figures and fit curves"""
    try:
        # Create target Directory
        os.mkdir(dir_figures)
        print("Directory " , dir_figures ,  " created ") 
    except FileExistsError:
        print("Directory " , dir_figures ,  " already exists")

def store_results(outdir, filename_prefix, dataframes=None, names=None, saveplot=True):
    """Stores the given tuple or list of pandas.DataFrames to excel files (.xlsx)
    and stores the current plot to PNG via `plt.savefig`.
    A names for each DataFrame has to be provided to be used as file name suffix
    and for informative output."""
    
    if not os.path.isdir(outdir):
        os.mkdir(outdir)
    if dataframes:
        assert len(dataframes) == len(names)
        for df, name in zip(dataframes, names):
            fn = os.path.join(outdir, f"{filename_prefix}_{name.lower()}.xlsx")
            df.to_excel(fn)
            print(f"{name} saved in '{fn}'.")
    if saveplot:
        fn = os.path.join(outdir, f"{filename_prefix}.png")
        print(f"Plot saved in '{fn}'.")
        plt.savefig(fn, dpi=600,  bbox_inches='tight')

    plt.show()
    return

def loggg(f):
    """Decorator for timimg
    Vincent D. Warmerdam: Untitled12.ipynb | PyData Eindhoven 2019
    https://www.youtube.com/watch?v=yXGCKqo5cEY
    """
    import datetime as dt
    def wrapper(dataf, *args, **kwargs):
        tic = dt.datetime.now()
        result = f(dataf, *args, **kwargs)
        toc = dt.datetime.now()
        print(f"{f.__name__} took={toc-tic}") # f-string
        return result
    return wrapper

# vim: set ts=4 sts=4 sw=4 tw=0:
