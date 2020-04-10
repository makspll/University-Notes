import numpy as np 
import scipy.io
import matplotlib.pyplot as plt
import matplotlib


import task1_1
import task1_3
import task1_mgc_cv

# for easier colorbar layout
def colorbar(mappable):
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    import matplotlib.pyplot as plt
    last_axes = plt.gca()
    ax = mappable.axes
    fig = ax.figure
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    cbar = fig.colorbar(mappable, cax=cax)
    plt.sca(last_axes)
    return cbar

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
    width = 505 #252.5
    
    # TASK1_1
    matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
    })

    print("task1_1")
    data = scipy.io.loadmat("../data/dset.mat")
    task1_1.task1_1(data["X"],data)

    outR = scipy.io.loadmat("t1_R.mat")["R"]
    outS = scipy.io.loadmat("t1_S.mat")["S"]

    fig,axes = plt.subplots(nrows=1,ncols=2,figsize=set_size(width,subplots=(1,2)))
    plt.rcParams.update({'font.size': 7})

    im = axes[0].imshow(outS, interpolation="none", cmap='RdBu_r',origin='lower',vmin=-0.04,vmax=0.04)
    axes[0].set_title("Covariance Matrix")
    axes[0].set_xticks(np.arange(outS.shape[0]))
    axes[0].set_yticks(np.arange(outS.shape[0]))
    axes[0].tick_params(axis='both', which='major', labelsize=4)

    colorbar(im)

    im = axes[1].imshow(outR, interpolation="none", cmap='RdBu_r',origin='lower',vmin=-1,vmax=1)
    axes[1].set_title("Correlation Matrix")
    axes[1].set_xticks(np.arange(outR.shape[0]))
    axes[1].set_yticks(np.arange(outR.shape[0]))
    axes[1].tick_params(axis='both', which='major', labelsize=4)

    colorbar(im)

    fig.tight_layout()

    #plt.savefig('correlation.png')
    plt.show()

    # TASK1_3
    plt.rcdefaults()
    matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
    })

    print("task1_3")
    task1_3.task1_3(outS)

    outEVe = scipy.io.loadmat("t1_EVecs.mat")["EVecs"]
    outEVa = scipy.io.loadmat("t1_EVals.mat")["EVals"]
    outCV = scipy.io.loadmat("t1_Cumvar.mat")["Cumvar"]
    outMD = scipy.io.loadmat("t1_MinDims.mat")["MinDims"]
  
    fig,ax = plt.subplots(1,figsize=set_size(width))

    X = np.arange(len(outCV))
    ax.set_xticks(X)
    ax.set_title("Cummulative Variance")
    ax.set_xlabel("Dimensions")
    ax.set_ylabel("Total Variance")

    ax.bar(X,outCV.flatten())

    #plt.savefig('cumvar.png')
    plt.show()
    
    # draw the data after PCA using the first 2 eigenvalues as new basis
    fig,ax = plt.subplots(1,figsize=set_size(width))
    
    # get matrix to transform data
    W = outEVe[:,[0,1]]

    # the dot product of each feature vector with each unit eigenvector: 1-by-D dot D-by-1 gives
    # the scalar projection or the distance of the vector projection along that eigenvector
    # D is then a N-by-2 matrix of the feature vectors expressed as a linear combination of the first 2 principal components
      
    D = data["X"]@W
    
    # plot each class in a different color
    for i in range(10):
        idxs = np.argwhere(data["Y_species"] == i)
        D = D
        X = D[idxs,0]
        Y = D[idxs,1]
        ax.scatter(X,Y,label = data["list_species"][i,0][0],s=3)
    ax.legend(loc="upper right",fontsize="x-small")
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    ax.set_title("Data transformed onto first two principle components")
    fig.tight_layout()
    # plt.savefig('pca.png')
    plt.show()

    #TASK 1.4
    plt.rcdefaults()
    matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
    })

    fig,ax = plt.subplots(1,figsize=set_size(width))

    X = [1,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.01,0.001,0.0001,0.00001,0.000001,0.0000001,0.0000001,0.000000001,0]
    Y = []
    for e in X:
        try:
            task1_mgc_cv.task1_mgc_cv(data["X"],data["Y_species"],1,e,5)
            outCM = scipy.io.loadmat('t1_mgc_5cv6_ck1_CM.mat')["CM"]
            print(e,outCM)
            Y.append(np.sum(outCM.diagonal()))
        except: 
            Y.append(np.nan)

    ax.plot(X,Y)
    ax.set_xlabel("Epsilon")
    ax.set_ylabel("accuracy")
    ax.set_title("Classification with 5-fold cv, full covariance matrices and varying epsilon")

    plt.savefig('epsilon.png')
    plt.show()

def task4(e):
    data = scipy.io.loadmat("../data/dset.mat")
    task1_mgc_cv.task1_mgc_cv(data["X"],data["Y_species"],1,e,5)

          