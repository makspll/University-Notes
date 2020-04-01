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
    
    scipy.io.savemat('t1_EVecs.mat', mdict={'EVecs': EVecs})
    scipy.io.savemat('t1_EVals.mat', mdict={'EVals': EVals})
    scipy.io.savemat('t1_Cumvar.mat', mdict={'Cumvar': Cumvar})
    scipy.io.savemat('t1_MinDims.mat', mdict={'MinDims': MinDims})


