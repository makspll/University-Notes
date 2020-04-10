#
# Version 0.9.1  (HS 23/03/2020)
#
import numpy as np
import scipy.io

def task2_sNeuron(W, X):
    # Input:
    #  X : N-by-D matrix of input vectors (in row-wise) (np.float64)
    #  W : (D+1)-by-1 vector of weights (np.float64)
    # Output:
    #  Y : N-by-1 vector of output (np.float64)

    # the output is defined as y(x_i) = step(w.T*X[0]) where
    # X needs to be augmented with a one at the top

    # find out sizes
    (N,D) = X.shape

    # augment X
    X = np.concatenate((np.ones((N,1)),X),axis=1)
    
    # apply activation function and change type
    return 1/(1+np.exp(-(X@W)))
