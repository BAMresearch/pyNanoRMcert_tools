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
    black    = '#002832' # primary color
    black_80 = '#325463'
    black_60 = '#5F7B89'
    black_45 = '#7D95A3'
    black_30 = '#7D95A3'
    black_15 = '#CCD8DF'
    # --- The four color accents of red ---
    red      = '#D2001E' # primary color
    red_2    = '#B40F1E'
    red_3    = '#8C1419'
    red_4    = '#501919'
    # --- The four color accents of blue ---
    blue     = '#00AFF0' # primary color
    blue_2   = '#0089BA'
    blue_3   = '#007599'
    blue_4   = '#00556E'
    #--- The four color accents of green ---
    green    = '#73E600'
    green_2  = '#66CC14'
    green_3  = '#47B312'
    green_4  = '#2E990F'
    #--- The four color accents of yellow ---
    yellow   = '#FFDC00'
    yellow_2 = '#FAB900'
    yellow_3 = '#E69B00'
    yellow_4 = '#CD7D00'

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
