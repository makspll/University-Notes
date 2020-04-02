#
# Version 0.9.1  (HS 23/03/2020)
#
import numpy as np
import scipy.io
import math

# assumes none of the variables have 0 variance, i.e. no constant variables
def task1_1(X, Y):
    # Input:
    #  X : N-by-D data matrix (np.float64)
    #  Y : N-by-1 label vector (np.int32)
    # Variables to save
    #  S : D-by-D covariance matrix (np.float64) to save as 't1_S.mat'
    #  R : D-by-D correlation matrix (np.float64) to save as 't1_R.mat'

    # get sizes
    (N,D) = X.shape
    
    # mu hat - 1-by-D vector
    mu = np.mean(X,axis = 0)

    # N-by-D matrix
    centeredX = (X - mu)

    # sigma hat - D-by-D matrix
    S = (centeredX.T@centeredX)/N

    # correlation matrix - D-by-D matrix
    diag = S.diagonal().reshape(1,D)
    R = S / (np.sqrt(diag.T@diag))
    
    scipy.io.savemat('t1_S.mat', mdict={'S': S})
    scipy.io.savemat('t1_R.mat', mdict={'R': R})

def test():
    print("task1_1")
    data = scipy.io.loadmat("../data/dset.mat")
    task1_1(data["X"],data["Y_species"])

    outR = scipy.io.loadmat("t1_R.mat")["R"]    
    outS = scipy.io.loadmat("t1_S.mat")["S"]
    print("Output:")
    print("R:\n",outR)
    print("S:\n",outS)