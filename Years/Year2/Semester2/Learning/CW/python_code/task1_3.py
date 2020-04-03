#
# Version 0.9.1  (HS 23/03/2020)
#
import numpy as np
import scipy.io

def task1_3(Cov):
    # Input:
    #  Cov : D-by-D covariance matrix (np.float64)
    # Variales to save:
    #  EVecs : D-by-D matrix of column vectors of eigen vectors (np.float64)  
    #  EVals : D-by-1 vector of eigen values (np.float64)  
    #  Cumvar : D-by-1 vector of cumulative variance (np.float64)  
    #  MinDims : 4-by-1 vector (np.int32)  

    # find D
    D,D = Cov.shape

    # find the eigen values and eigen vectors in ascending order
    EVals,EVecs = np.linalg.eigh(Cov)

    # find indexes of those eigenvectors whose first element is negative and negate those columns
    for i in np.argwhere(EVecs[0] < 0):
        EVecs[0,i] = EVecs[0,i] * -1
    
    # reverse the order of EVals and EVecs
    EVals = EVals[::-1][np.newaxis,:].T
    EVecs = np.flip(EVecs,1)

    # calculate the cummulative variance which is the sum of eigen values at each addition
    Cumvar = np.cumsum(EVals,axis=0)

    # calculate MinDims using Cumvar
    minBounds = np.array([70,80,90,95])/100 * Cumvar[-1]  # the minimum variance bounds
    
    currDims = 1 
    i = 0 # current bound

    MinDims = np.zeros((4,1))
    while i < 4:
        if Cumvar[currDims] >= minBounds[i]:
            MinDims[i] = currDims 
            i += 1
        currDims += 1

    scipy.io.savemat('t1_EVecs.mat', mdict={'EVecs': EVecs})
    scipy.io.savemat('t1_EVals.mat', mdict={'EVals': EVals})
    scipy.io.savemat('t1_Cumvar.mat', mdict={'Cumvar': Cumvar})
    scipy.io.savemat('t1_MinDims.mat', mdict={'MinDims': MinDims})

