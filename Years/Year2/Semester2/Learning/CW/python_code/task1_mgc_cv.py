#
# Version 0.9  (HS 09/03/2020)
#
import numpy as np
import scipy.io

def task1_mgc_cv(X, Y, CovKind, epsilon, Kfolds):
    # Input:
    #  X : trainingN-by-D matrix of feature vectors (np.float64)
    #  Y : trainingN-by-1 label vector (np.int32)
    #  CovKind : scalar (np.int32)
    #  epsilon : scalar (np.float64)
    #  Kfolds  : scalar (np.int32)
    #
    # Variables to save
    #  PMap   : trainingN-by-1 vector (np.ndarray) of partition numbers (np.int32)
    #  Ms     : C-by-D matrix (np.ndarray) of mean vectors (np.float64)
    #  Covs   : C-by-D-by-D array (np.ndarray) of covariance matrices (np.float64)
    #  CM     : C-by-C confusion matrix (np.ndarray) (np.float64)

    ## split the test data by classes

    # the number of classes
    C = 10
    D = X.shape[1]
    # the total number of samples
    Xcount = len(X)

    # idxs of elements in each class, C-by-len(C_i indices)
    ClassIdxs = np.zeros((C),dtype=object)
    for c in range(C):
        ClassIdxs[c] = np.nonzero(Y == c+1)[0] # Y ranges between 1 and 10

    # numbers of elements in each class
    vecLen = np.vectorize(len)
    Ncs = vecLen(ClassIdxs)
    # the initial partition lenghts for each class, C-by-1
    Mcs = Ncs//Kfolds

    PMap = np.zeros((Xcount,1))
    CM = np.zeros((C,C))

    # partition the elements except for the last partition
    for p in range(Kfolds):
        a = p * Mcs
        b = (p+1) * Mcs

        # clamp the elements in the last partition
        if p == Kfolds - 1:
            np.minimum(b,Ncs-1,out=b) # Ncs contains lengths, b contains indices, equalize the difference and take min
            b+=1 # we slice exclusively later so we need to keep the values as lenghts rather than indices
        # flattened elements taken from a portion of each class

        idxs = [ item for c,sublist in enumerate(ClassIdxs) for item in sublist[a[c]:b[c]]]
        PMap[idxs] = p

    # perform classification with each partition as a test set 
    for p in range(Kfolds):

        ## estimate the parameters
        Covs = np.zeros((C,D,D)) 
        Ms = np.zeros((C,D))

        testingMask = (PMap == p)
        trainingMask = (PMap != p)

        for c in range(C):
            # training is Msc[c]-by-D in size
            # labels range 1-10, so in referring to Y be careful with off-by-one errors
            testing = X[(testingMask & (Y == c+1)).ravel(),:]
            training = X[(trainingMask & (Y == c+1)).ravel(),:]
            # get size
            trainingN = len(training)

            # mu hat - 1-by-D vector
            mu = np.mean(training,axis = 0)

            Ms[c] = mu
            # trainingN-by-D matrix
            centeredX = (training - mu)

            # we estimate and regularize the matrices
            if CovKind == 1:
                # full covariance matrix calculation 
                Covs[c] = (centeredX.T@centeredX)/trainingN
                np.fill_diagonal(Covs[c], Covs[c].diagonal() + (epsilon * 1))

            elif CovKind == 2:
                # diagonal covariance matrix, just valculate auto variance
                np.fill_diagonal(Covs[c],np.sum(centeredX**2,axis=0)/trainingN)
                np.fill_diagonal(Covs[c], Covs[c].diagonal() + (epsilon * 1))

            else:
                # for shared covariance accumulate the result in 0, and later 'tile' the shared matrix
                S = ((centeredX.T@centeredX)/trainingN)
                np.fill_diagonal(S, S.diagonal() + (epsilon * 1))
                Covs[0] = S + Covs[0]

        if CovKind == 3:
            Covs[0] = Covs[0]/C
            Covs = np.tile(Covs[0],(C,1,1))

        ## perform classification and calculate confusion matrix as you go

        CM_p = np.zeros((C,C))

        # classify each sample according to posterior likelihoods
        
        # PLL = np.zeros((trainingN,1))
        for i in np.nonzero(testingMask)[0]:
            x = X[i]
            (pll,c) = max([(log_posterior(x,Ms[i],Covs[i]),i) for i in range(C)])

            # PLL[i] = c
            CM_p[Y[i]-1,c] += 1

        # accumulate the total confusion matrix
        CM += CM_p/len(np.nonzero(testingMask)[0]) 
        ## save results
        scipy.io.savemat('t1_mgc_'+str(Kfolds)+'cv'+str(p)+'_Ms.mat', mdict={'Ms':Ms})
        scipy.io.savemat('t1_mgc_'+str(Kfolds)+'cv'+str(p)+'_ck'+str(CovKind)+'_Covs.mat', mdict={'Covs': Covs})
    
        scipy.io.savemat('t1_mgc_'+str(Kfolds)+'cv'+str(p)+'_ck'+str(CovKind)+'_CM.mat', mdict={'CM':CM_p})
    
    CM /= Kfolds
    np.set_printoptions(precision=1)
    scipy.io.savemat('t1_mgc_'+str(Kfolds)+'cv'+str(Kfolds+1)+'_ck'+str(CovKind)+'_CM.mat', mdict={'CM':CM})
    scipy.io.savemat('t1_mgc_'+str(Kfolds)+'cv_PMap.mat', mdict={'PMap':PMap})

def log_posterior(x,mu,si):
    si_det = np.linalg.det(si)
    si_inv = np.linalg.inv(si)
    xCentered = (x - mu)[:,None]
    return ((-(1/2)* ((xCentered.T@si_inv@xCentered))) - ((1/2)*np.log(si_det)))[0,0]  # + np.log(prior) - assumed equal priors
