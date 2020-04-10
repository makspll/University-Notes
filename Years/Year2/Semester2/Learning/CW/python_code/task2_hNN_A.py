#
# Version 0.9.2  (HS 27/03/2020)
#
import numpy as np
import scipy.io
import task2_hNeuron as t2 

def task2_hNN_A(X):
    # Input:
    #  X : N-by-D matrix (np.ndarray) of input vectors (in row-wise) (np.float64), where D=2.
    # Output:
    #  Y : N-by-1 vector (np.ndarray) of output (np.float64)

    N,D = X.shape 
    
    weightsLayer1 = np.array([[1.0,-0.34994868685872166,-0.18980256091259212],
                            [0.22933150896320767,0.7699130167301808,-1.0],
                            [-1.0,0.3219838025165198,0.08814889248320788],
                            [-1.0,-0.7294263777054958,0.9924893972926816]])
              
    Nrns1,D1 = weightsLayer1.shape
    weightsLayer1 = weightsLayer1.T

    weightsLayer2 = np.array([[1,-1,-1,-1,-1]])
    Nrns2,D2 = weightsLayer2.shape
    weightsLayer2 = weightsLayer2.T

    # N-by-Nrns1
    layer1Output = np.zeros((N,Nrns1))
    for neuron in range(Nrns1):
        layer1Output[:,neuron] = t2.task2_hNeuron(weightsLayer1[:,neuron,None],X)[:,0]
    
    # N-by-Nrns2 
    layer2Output = np.zeros((N,Nrns2))
    for neuron in range(Nrns2):
        layer2Output[:,neuron] = t2.task2_hNeuron(weightsLayer2[:,neuron,None],layer1Output)[:,0]

    return layer2Output[:,0]
