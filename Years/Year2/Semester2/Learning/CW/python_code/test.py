import numpy as np 
import scipy.io
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

import task1_1

# for determining the size of figures to port to latex

def set_size(width, fraction=1, subplots=(1, 1)):
    """ Set figure dimensions to avoid scaling in LaTeX.

    Parameters
    ----------
    width: float or string
            Document width in points, or string of predined document type
    fraction: float, optional
            Fraction of the width which you wish the figure to occupy
    subplots: array-like, optional
            The number of rows and columns of subplots.
    Returns
    -------
    fig_dim: tuple
            Dimensions of figure in inches
    """
    if width == 'thesis':
        width_pt = 426.79135
    elif width == 'beamer':
        width_pt = 307.28987
    elif width == 'pnas':
        width_pt = 246.09686
    else:
        width_pt = width

    # Width of figure (in pts)
    fig_width_pt = width_pt * fraction
    # Convert from pt to inches
    inches_per_pt = 1 / 72.27

    # Golden ratio to set aesthetic figure height
    golden_ratio = (5**.5 - 1) / 2

    # Figure width in inches
    fig_width_in = fig_width_pt * inches_per_pt
    # Figure height in inches
    fig_height_in = fig_width_in * golden_ratio * (subplots[0] / subplots[1])

    return (fig_width_in, fig_height_in)

if __name__ == "__main__":
    width = 345
    
    print("task1_1,b)")
    data = scipy.io.loadmat("../data/dset.mat")
    task1_1.task1_1(data["X"],data)

    outR = scipy.io.loadmat("t1_R.mat")["R"]
    outS = scipy.io.loadmat("t1_S.mat")["S"]

    fig,axes = plt.subplots(2,1,figsize=set_size(width,subplots=(2,1)))

    im = axes[0].imshow(outS, interpolation="none", cmap='RdBu_r',origin='lower',vmin=-0.04,vmax=0.04)
    axes[0].set_title("Covariance matrix of X's")
    axes[0].set_xticks(np.arange(outS.shape[0]))
    axes[0].set_yticks(np.arange(outS.shape[0]))
    axes[0].tick_params(axis='both', which='major', labelsize=5)
    axes[0].set_xlabel("variable")
    axes[0].set_ylabel("variable")
    plt.colorbar(im,ax=axes[0])

    im = axes[1].imshow(outR, interpolation="none", cmap='RdBu_r',origin='lower',vmin=-1,vmax=1)
    axes[1].set_title("Correlation matrix of X's")
    axes[1].set_xticks(np.arange(outR.shape[0]))
    axes[1].set_yticks(np.arange(outR.shape[0]))
    axes[1].tick_params(axis='both', which='major', labelsize=5)
    axes[1].set_xlabel("variable")
    axes[1].set_ylabel("variable")
    plt.colorbar(im,ax=axes[1])
    
    fig.tight_layout()
    plt.savefig('correlation.png')
    plt.show()
