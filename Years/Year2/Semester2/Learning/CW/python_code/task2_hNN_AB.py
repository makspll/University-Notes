#
# Version 0.9.2  (HS 27/03/2020)
#
import numpy as np
import scipy.io
import task2_hNeuron as t2

def task2_hNN_AB(X):
    # Input:
    #  X : N-by-D matrix of input vectors (in row-wise) (np.float64), where D=2
    # Output:
    #  Y : N-by-1 vector of output (np.float64)

    # weights B
    #     [[-1.         -0.08723287  0.30008223]
    #  [-0.76903546  1.         -0.98133664]
    #  [-1.          0.29507611  0.03808055]
    #  [ 1.         -0.50965075 -0.38684878]
    
    N,D = X.shape 
                            
    # Layer 1
    weightsLayer1 = np.array([  #PolyA - 1 if outwith in each direction
                            [1.0,-0.34994868685872166,-0.18980256091259212],
                            [0.22933150896320767,0.7699130167301808,-1.0],
                            [-1.0,0.3219838025165198,0.08814889248320788],
                            [-1.0,-0.7294263777054958,0.9924893972926816],
                                #PolyB-1 triangle - 1 if outwith in each direction
                            [-1.         ,-0.08723287  ,0.30008223],
                            [-0.76903546  ,1.         ,-0.98133664],
                            [ 1.         ,-0.0764559  ,-0.323877  ],
                                #PolyB-2 triangle - 1 if outwith in each direction
                            [-1.          ,0.29507611  ,0.03808055],
                            [ 1.         ,-0.50965075 ,-0.38684878],
                            [-1.          ,0.0764559   ,0.323877  ]
                            ])
              
    Nrns1,D1 = weightsLayer1.shape
    weightsLayer1 = weightsLayer1.T

    # Layer2
    weightsLayer2 = np.array([  #PolyA - OR
                            [0, 1,1,1,1, 0,0,0, 0,0,0],
                                #PolyB-1 triangle - NOR
                            [1, 0,0,0,0, -1,-1,-1, 0,0,0],
                                #PolyB-2 triangle - NOR
                            [1, 0,0,0,0, 0,0,0, -1,-1,-1,],
                            ])
    Nrns2,D2 = weightsLayer2.shape
    weightsLayer2 = weightsLayer2.T

    # Layer3
    weightsLayer3 = np.array([  # Carry forward w1 
                            [0, 1,0,0],
                                # PolyB OR
                            [0, 0,1,1 ]]) 
    Nrns3,D3 = weightsLayer3.shape
    weightsLayer3 = weightsLayer3.T

    
    # Layer4
    weightsLayer4 = np.array([  # AND 
                            [-1, 0.6,0.6]]) 
    Nrns4,D4 = weightsLayer4.shape
    weightsLayer4 = weightsLayer4.T

    # N-by-Nrns1
    layer1Output = np.zeros((N,Nrns1))
    for neuron in range(Nrns1):
        layer1Output[:,neuron] = t2.task2_hNeuron(weightsLayer1[:,neuron,None],X)[:,0]
    # N-by-Nrns2 
    layer2Output = np.zeros((N,Nrns2))
    for neuron in range(Nrns2):
        layer2Output[:,neuron] = t2.task2_hNeuron(weightsLayer2[:,neuron,None],layer1Output)[:,0]

    # N-by-Nrns3
    layer3Output = np.zeros((N,Nrns3))
    for neuron in range(Nrns3):
        layer3Output[:,neuron] = t2.task2_hNeuron(weightsLayer3[:,neuron,None],layer2Output)[:,0]
    # N-by-Nrns4
    layer4Output = np.zeros((N,Nrns4))
    for neuron in range(Nrns4):
        layer4Output[:,neuron] = t2.task2_hNeuron(weightsLayer4[:,neuron,None],layer3Output)[:,0]
    
    return layer4Output[:,0]
