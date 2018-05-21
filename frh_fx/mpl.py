from matplotlib import pyplot as plt
from cycler import cycler
def config(scale=1.5,print_keys='False'):

    plt.rcParams['figure.figsize'] = [3,3*9/16]
    plt.rcParams['figure.dpi'] = scale*100

    plt.rcParams['lines.linewidth'] = 0.75

    plt.rcParams['axes.titlesize'] = 10
    plt.rcParams['axes.labelsize'] = 9.2
    plt.rcParams['legend.fontsize'] = 7.2
    plt.rcParams['xtick.labelsize'] = 6.2
    plt.rcParams['ytick.labelsize'] = 6.2
    plt.rcParams['axes.grid'] = True
    plt.rcParams['axes.facecolor'] = 'ghostwhite'

    plt.rcParams['grid.alpha'] = 0.1
    plt.rcParams['grid.linestyle'] = '-'
    plt.rcParams['grid.linewidth'] = 0.25

    plt.rcParams['legend.numpoints'] = 1
    plt.rcParams['legend.loc'] = 'best'
    # plt.rcParams['legend.loc'] = 'center left'
    plt.rcParams['legend.fancybox'] = True
    plt.rcParams['legend.framealpha'] = 0.1

    plt.rcParams['savefig.bbox'] = 'tight'
    plt.rcParams['savefig.format'] = 'pdf'
    plt.rcParams['savefig.dpi'] = scale*100

    plt.rcParams['markers.fillstyle'] = 'none'
    plt.rcParams['lines.markersize'] = 3

    plt.rcParams['xtick.major.size'] = 0
    plt.rcParams['ytick.major.size'] = 0

    plt.rcParams['axes.prop_cycle'] = cycler(color=['r','coral','gold',
                                          'g','b','indigo','violet'])

    if print_keys:
        print(plt.rcParams.keys())
