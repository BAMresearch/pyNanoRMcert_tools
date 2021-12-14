# collection of my definitions

def configMatplotlib(plt):
    plt.rcParams.update({'axes.titlesize': 16})
    plt.rcParams.update({'axes.labelsize': 16})
    plt.rcParams.update({'lines.linewidth': 3})
    plt.rcParams.update({'lines.markersize':10})
    plt.rcParams.update({'xtick.labelsize': 12})
    plt.rcParams.update({'ytick.labelsize': 12})
    plt.rcParams["legend.frameon"] = False
    plt.rcParams["legend.fontsize"] = 16
    plt.rcParams['figure.figsize'] = [1*6.4,4.8]


class BAMColors:
    """Definition of BAM colors according to the corporate design of BAM"""

    # --- color accents of black ---
    black    = '#070d0d' # primary color 
    black_80 = '#273d3d' 
    black_60 = '#506e6e' 
    black_45 = '#749191'
    black_30 = '#9eb8b8'
    black_15 = '#ccdbdb'
    # --- The four color accents of red ---
    red      = '#E60000' # primary color
    red_2    = '#b80000'
    red_3    = '#7c0000'
    red_4    = '#330000'
    # --- The four color accents of blue ---
    blue     = '#00ffff' # primary color
    blue_2   = '#13bfbf'
    blue_3   = '#1c8c8c'
    blue_4   = '#174d4d'
    #--- The four color accents of green ---
    green    = '#73e600'
    green_2  = '#66cc14'
    green_3  = '#47b312'
    green_4  = '#2e990f'
    #--- The four color accents of yellow ---
    yellow   = '#ffe600'
    yellow_2 = '#ffb300'
    yellow_3 = '#fe68a0'
    yellow_4 = '#cc6600' 

class BAMMarkerStyles:
    """Style of markers in plots with BAM colors"""
    # --- style of plot ---
    black = dict(color=BAMColors.black, linestyle='', marker='o', fillstyle='none',
                    markersize=5, markeredgewidth=1, markeredgecolor=BAMColors.black)
    red = dict(color=BAMColors.red, linestyle='', marker='s', fillstyle='none',
                    markersize=5, markeredgewidth=1, markeredgecolor=BAMColors.red)
    green = dict(color=BAMColors.green, linestyle='', marker='x', fillstyle='none',
                    markersize=5, markeredgewidth=1, markeredgecolor=BAMColors.green)
    
    blue = dict(color=BAMColors.blue, linestyle='', marker='^', fillstyle='none',
                    markersize=5, markeredgewidth=1, markeredgecolor=BAMColors.blue)
    yellow = dict(color=BAMColors.yellow, linestyle='', marker='^', fillstyle='none',
                    markersize=5, markeredgewidth=1, markeredgecolor=BAMColors.yellow)