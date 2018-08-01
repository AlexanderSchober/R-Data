# -*- coding: utf-8 -*-

#-INFO-
#-Name-NMF_R-
#-Version-0.1.0-
#-Date-22_April_2016-
#-Author-Alexander_Schober-
#-email-alex.schober@mac.com-
#-INFO-

print 'Loading NMF dependencies...'
"""
###########################################################################
###########################################################################

     o---------------------------------------------------------o
     |    ##       ###              ..O,.  . .=OZ              |
     |    ##       ###            ?=?...   ?   ..Z~            |
     |    ##       ###         .?.O.       . .,. .Z.  .        |
     |    ##       ###        . .?. . ?Z    ...O7.ZZ. =        |
     |    ##       ###       . ,?:.:        . .  . Z. .?       |
     |    ##       ###       ..?Z         .ZZZZZ+ :Z:ZZZ.      |
     |    ##       ###      ~ .??     .ZZZ. .... ..Z+  ZI?     |
     |    ##       ###      ?$.?? ..OO????+,. .~???8?: .ZZ     |
     |    ######   ###      :..??OO+..           .ZZ?.?7 Z     |
     |    ######   ###     Z? 8O                 ZZ. ??O=      |
     |                     .Z?8??                ZZ..7O. ?I    |
     |    ###### #######   .ZO.?7:              =Z7?ZO.  ?Z    |
     |    ##  ##   ###     .O.. 77??~. .     ..$OOO?.?. .Z.    |
     |    ##       ###      Z7  .?????????????OOO... ?.?,Z     |
     |    ##       ###       ZO. ??   ..~?OZ.ZZ7  . .7.,Z.     |
     |    ######   ###       .Z7.?OOI:..  .$ZZ...+? .:ZZ.      |
     |        ##   ###       . ZZ$.??..~?OOZ.....   OZZ        |
     |    ##  ##   ###           ZZZOOOZZ.    . .ZZZZ          |
     |    ##  ##   ###            .ZZZOOZZZZZZZZZZZ..          |
     |    ######   ###                .?OOOZZZ+ :?             |
     o---------------------------------------------------------o

###########################################################################
###########################################################################
"""


"""
##################################################
Default python lbrary imports
##################################################
"""

#######################################
#basic imports

#system import
import sys

#jettison out system
import json

#time
import time

#######################################
#numpy imports

#numpy mathematical import
import numpy as np
import math

#import linear algorithmic
import numpy.linalg as nla

#import direct randome treatment
from numpy import random

#######################################
#scipy imports
import scipy.sparse as sps
import scipy.optimize as opt

#######################################
#multiprocessing
import multiprocessing

'''
###########################################################################
These are the custome imports
###########################################################################
'''

#File and system management routines
import Utility_File     as File

#import the processing methods
from Utility_NNLS       import nnlsm_activeset
from Utility_NNLS       import nnlsm_blockpivot

#import matric utilities
import Utility_Math     as mu

#The terminal viual manager
import Utility_Out      as VisOut

#General Utility
import Utility_Main     as Utility

class NMF_Base(object):

    """ 
    ###########################################################################
    Base class for NMF algorithms
    Specific algorithms need to be implemented by deriving from this class.
    ###########################################################################
    """
    default_max_iter = 100
    default_max_time = np.inf

    def __init__(self):
        
        raise NotImplementedError('NMF_Base is a base class that cannot be instantiated')

    def set_default(self, default_max_iter, default_max_time):
        
        self.default_max_iter = default_max_iter
        
        self.default_max_time = default_max_time


    '''
    ###########################################################################
    Run an NMF algorithm several times with random initial values 
    and return the best result in terms of the Frobenius norm of
    the approximation error matrix
    Parameters
    ----------
    A : numpy.array or scipy.sparse matrix, shape (m,n)
    k : int - target lower rank
    num_trial : int number of trials
    Optional Parameters
    -------------------
    max_iter : int - maximum number of iterations for each trial.
                If not provided, default maximum for each algorithm is used.
    max_time : int - maximum amount of time in seconds for each trial.
                If not provided, default maximum for each algorithm is used.
    verbose : int - 0 (default) - No debugging information is collected, but
                                input and output information is printed on screen.
                    -1 - No debugging information is collected, and
                                nothing is printed on screen.
                    1 (debugging/experimental purpose) - History of computation is
                                    returned. See 'rec' variable.
                    2 (debugging/experimental purpose) - History of computation is
                                    additionally printed on screen.
    Returns
    -------
    (W, H, rec)
    W : Obtained factor matrix, shape (m,k)
    H : Obtained coefficient matrix, shape (n,k)
    rec : dict - (debugging/experimental purpose) Auxiliary information about the execution
    ###########################################################################
    '''

    
    def run_repeat(self, NMF, A):
        
        """ 
        What we have learned using multiprocessing. 
        Everything needs to be static to limit errors. So I think self. is not callable
        as such. Therefore we need to put everything into a stationarry array and unfold it after
        """
        trialBest     = 0
        elapsedBest   = 0
        rel_errorBest = 1
        
        this = [None]*NMF.Repeat
        
        #Pass into NMF the algo values
        NMF.Initializer = self.Initializer
        NMF.IterSolver = self.IterSolver
        
        '''
        For the next section of the code to ork under windows we had to change the forking.py
        file at line 478 as follows:
        
        if main_name != 'ipython':
            import imp
        
        to:
        
        if main_name == '__main__':
            # For directory and zipfile execution, we assume an implicit
            # "if __name__ == '__main__':" around the module, and don't
            # rerun the main module code in spawned processes
        
            main_module = sys.modules['__main__']
            main_module.__file__ = main_path
            
        elif main_name != 'ipython':
            # Main modules not actually called __main__.py may
            # contain additional code that should still be executed
            
            import imp
        
        '''
        
        #############################################
        #############################################
        #set queu output method
        output = multiprocessing.Manager().Queue()
        
        #set process grid
        u = 0
        processors = NMF.CPUs
        ResultOut = []
        
        #send out the log
        VisOut.TextBox(Title = 'NMF Processing',state = 0,close = False)
        
        #############################################
        #############################################
        #if we are going to run only onee.
        if NMF.Repeat == 0:
        
            #only run one instance:
            self.run(NMF,A,x,trialBest,elapsedBest,rel_errorBest,0, output)
        
        
        #############################################
        #############################################
        #If the User asked for a multiprocessor call
        else:
            
            #initialise a while loop to move to new processes
            while u<NMF.Repeat:

                ################################
                #if we reached the limit of iterations
                if u+processors > NMF.Repeat:
                    o = u
                    
                    #Set the other processes
                    processes = [multiprocessing.Process(target=self.runNMF, args=(NMF,A,x,trialBest,elapsedBest,rel_errorBest,0, output)) for x in range(u,NMF.Repeat-1)]
                    
                    #Set the process that will output the visual progress
                    processes.append(multiprocessing.Process(target=self.runNMF, args=(NMF,A,NMF.Repeat,trialBest,elapsedBest,rel_errorBest,-1, output)))
                    
                    #set exit u 
                    u = NMF.Repeat
                
                ################################
                #if we didn't
                else:
                    o = u
                    #Set the other processes
                    processes = [multiprocessing.Process(target=self.runNMF, args=(NMF,A,x,trialBest,elapsedBest,rel_errorBest,0, output)) for x in range(u,u+processors-1)]
                    
                    #Set the process that will output the visual progress
                    processes.append(multiprocessing.Process(target=self.runNMF, args=(NMF,A,u+processors-1,trialBest,elapsedBest,rel_errorBest,-1, output)))
                
                
                ################################
                #Start the cretaed processes
                #start process
                for p in processes:
                    p.start()
                    
                    #Do we want verbose
                    VisOut.TextBox(Text ='[NMF] Running: '+str(o)+'the trial linked to single process.',state = 0 ,Top = False,close = False)
                    
                    o += 1
                    time.sleep(0.1)
                
                ################################
                #Wait for process completion
                
                #wait for process to end
                for p in processes:
                    p.join()
        
                #check if all processes where done
                time.sleep(0.1)
                
                #log it out
                VisOut.TextBox(Text = 'Finished processes will now wait for the results...',state = 0, Top = False, close = False)
                
                #fetch the results of the last process
                results = [output.get() for p in processes]    
            
                for t in range(0,len(results)): 
                    ResultOut.append(results[t])
                    
                #move forward
                u = o
                
            ################################
            #check the results
            for t in range(0,len(ResultOut)):
                
                #grab it
                this = ResultOut[t]
                
                #if it is the first iteration
                if t == 0:
                    
                    #set he best
                    best = this
                
                #else compare
                else:
                    if this[2]['final']['rel_error'] < best[2]['final']['rel_error']:
                        best          = this
        
            ################################
            #Send it to the dictionaries
            trialBest     = best[2]['final']['trial']
            elapsedBest   = best[2]['final']['elapsed'] 
            rel_errorBest = best[2]['final']['rel_error']
            
            #print it
            VisOut.TextBox(Text = '[NMF] Best result is as follows.', state = 0,close = False)
            
            print json.dumps(best[2]['final'], indent=4, sort_keys=True)
            
            
            #exit
            return best
            
    

    '''
    ###########################################################################
    Run a NMF algorithm

    Parameters
    ----------
    A : numpy.array or scipy.sparse matrix, shape (m,n)
    k : int - target lower rank
    Optional Parameters

    Returns
    -------
    (W, H, rec)
    W : Obtained factor matrix, shape (m,k)
    H : Obtained coefficient matrix, shape (n,k)
    rec : dict - (debugging/experimental purpose) Auxiliary information about the execution
    ###########################################################################
    '''

    def runNMF(self,NMF,A, trial, trialBest, elapsedBest, rel_errorBest,verbose,output):

        max_time = None
        k        = NMF.k
        max_iter = NMF.Iter
        
        
        #Set the info array
        info = {'k'             : k,
                'alg'           : str(NMF.__class__),
                'A_dim_1'       : A.shape[0],
                'A_dim_2'       : A.shape[1],
                'A_type'        : str(A.__class__),
                'max_iter'      : max_iter if max_iter is not None else max_iter,
                'verbose'       : verbose,
                'max_time'      : max_time if max_time is not None else 'none given'}



        #if the user added initial starting vecors
        #this could eventually be used with the PCA data (absolute PCA)
        if NMF.Init:
            
            #Set compoennts right
            H = np.asarray(NMF.CompInitVal).transpose()
            W = np.asarray(NMF.ScoreInitVal).transpose()
            
            
            #We have to check that they are all possitive if not set value to 0.1

            for i in range(0,k):
            
                if NMF.CompInit[i]:
                    
                    #True called means we keep yhis value
                    pass
                    
                else:
                    
                    #else randome in da place
                    H = np.concatenate((H,random.rand(H.shape[0],1)),axis=1)

            W = random.rand(A.shape[0], k)
            
            #inform the info set
            info['init'] = 'user_provided'
            
            
            
            
        #if the user didn't provide a starting set
        else:
            
            #Set random starting sets
            W = random.rand(A.shape[0], k)
            H = random.rand(A.shape[1], k)
            info['init'] = 'uniform_random'

        

        #normalize data
        norm_A = norm_fro(A)
        total_time = 0
        
        start = time.time()   
        
        # algorithm-specific initilization
        (W, H) = NMF.Initializer(W, H)

        for i in range(1, info['max_iter'] + 1):
            
            #timer for iteration start
            start_iter = time.time()
            
            # algorithm-specific iteration solver
            (W, H) = NMF.IterSolver(A, W, H, k, i)
            
            #calculated elapsed time after solving           
            elapsed = time.time() - start_iter

            #Do we want verbose further
            if verbose >= 1:
                try:
                    rel_error = norm_fro_err(A, W, H, norm_A) / norm_A
                except:
                    print 'could not initiate'
                
                if verbose >= 2:
                    #print Utility.Wiper() 
                    print 'Trial: ' + str(trialBest)  + ', Relative Error:' + str(rel_errorBest)+ ', Elapsed:' + str(round(elapsedBest,12)) + 'Iteration:' + str(0) 
                    print 'Trial: ' + str(trial)  + ', Relative Error:' + str(rel_error) + ', Elapsed:' + str(round(elapsed,12)) + 'Iteration:' + str(i) 
                
            if verbose == -1 :
                
                #send out progress
                print ' '*5+'|'+'-> Progress in percent:'+str(float(i*100)/(info['max_iter'] + 1))+'\r',
                
                #flush it to the system
                sys.stdout.flush()

            total_time += elapsed

            
        #Normalise data    
        W, H, weights = normalize_column_pair(W, H)
        
        #prepare verbose data for the dump
        final               = {}
        final['norm_A']     = norm_A
        final['rel_error']  = norm_fro_err(A, W, H, norm_A) / norm_A
        final['iterations'] = i
        final['elapsed']    = time.time() - start
        final['trial']      = trial

            
        #save it to the return value of the function
        rec = {'info': info, 'final': final}
        
        
        #depending on the verbose level add info
        if verbose > 0:
            print '[NMF] Completed: '
            print json.dumps(final, indent=4, sort_keys=True)
            
        #send return of fucntion
        output.put([np.asarray(W), np.asarray(H), rec]) 
        time.sleep(0.1)
        

    def IterSolver(self, A, W, H, k, it):
        
        raise NotImplementedError

    def Initializer(self, W, H):
        
        return (W, H)

'''
###############################################################################
NMF algorithm: ANLS with block principal pivoting
J. Kim and H. Park, Fast nonnegative matrix factorization: 
An active-set-like method and comparisons,
SIAM Journal on Scientific Computing, 
vol. 33, no. 6, pp. 3261-3281, 2011.
###############################################################################
'''
class NMF_ANLS_BLOCKPIVOT(NMF_Base):

    #Class initialising method
    def __init__(self, default_max_iter=50, default_max_time=np.inf):
        self.set_default(default_max_iter, default_max_time)

    #class iteration solver
    def IterSolver(self, A, W, H, k, it):
        Sol, info = nnlsm_blockpivot(W, A, init=H.T)
        H = Sol.T
        Sol, info = nnlsm_blockpivot(H, A.T, init=W.T)
        W = Sol.T
        return (W, H)

'''
###############################################################################
NMF algorithm: ANLS with scipy.optimize.nnls solver
###############################################################################
'''
class NMF_ANLS_AS_NUMPY(NMF_Base):

    #Class initialising method
    def __init__(self, default_max_iter=50, default_max_time=np.inf):
        self.set_default(default_max_iter, default_max_time)

    #class iteration solver
    def IterSolver(self, A, W, H, k, it):
        
        if not sps.issparse(A):
            
            for j in xrange(0, H.shape[0]):
                
                res = opt.nnls(W, A[:, j])
                H[j, :] = res[0]
        else:
            
            for j in xrange(0, H.shape[0]):
                
                res = opt.nnls(W, A[:, j].toarray()[:, 0])
                H[j, :] = res[0]

        if not sps.issparse(A):
            
            for j in xrange(0, W.shape[0]):
                
                res = opt.nnls(H, A[j, :])
                W[j, :] = res[0]
        else:
            
            for j in xrange(0, W.shape[0]):
                
                res = opt.nnls(H, A[j, :].toarray()[0,:])
                W[j, :] = res[0]
        return (W, H)


'''
###############################################################################
NMF algorithm: ANLS with active-set method and column grouping
H. Kim and H. Park, Nonnegative matrix factorization based on alternating
nonnegativity constrained least squares and active set method, SIAM Journal on 
Matrix Analysis and Applications, vol. 30, no. 2, pp. 713-730, 2008.
###############################################################################
'''
class NMF_ANLS_AS_GROUP(NMF_Base):

    #Class initialising method
    def __init__(self, default_max_iter=50, default_max_time=np.inf):
        
        self.set_default(default_max_iter, default_max_time)

    #class iteration solver
    def IterSolver(self, A, W, H, k, it):
        
        if it == 1:
            
            Sol, info = nnlsm_activeset(W, A)
            
            H = Sol.T
            
            Sol, info = nnlsm_activeset(H, A.T)
            
            W = Sol.T
        
        else:
            
            Sol, info = nnlsm_activeset(W, A, init=H.T)
            
            H = Sol.T
            Sol, info = nnlsm_activeset(H, A.T, init=W.T)
            W = Sol.T
        return (W, H)


'''
###############################################################################
NMF algorithm: Hierarchical alternating least squares
A. Cichocki and A.-H. Phan, Fast local algorithms for large scale nonnegative 
matrix and tensor factorizations,IEICE Transactions on Fundamentals of 
Electronics, Communications and Computer Sciences,
vol. E92-A, no. 3, pp. 708-721, 2009.
###############################################################################
'''

class NMF_HALS(NMF_Base):

    #Class initialising method
    def __init__(self, default_max_iter=100, default_max_time=np.inf):
        
        self.eps = 1e-16
        
        self.set_default(default_max_iter, default_max_time)
        
    #Class initialising NORMALISING METHOD
    def Initializer(self, W, H):
        
        W, H, weights = mu.normalize_column_pair(W, H)
        
        return W, H

    #class iteration solver
    def IterSolver(self, A, W, H, k, it):
        
        AtW = MatMult(A.T,W)
        
        WtW = MatMult(W.T,W)
        
        for kk in xrange(0, k):
            
            temp_vec = H[:, kk] + AtW[:, kk] - MatMult(H,WtW[:, kk])
            
            H[:, kk] = np.maximum(temp_vec, self.eps)
        

        AH = MatMult(A,H)
        
        HtH = MatMult(H.T,H)
        
        for kk in xrange(0, k):
            
            temp_vec = W[:, kk] * HtH[kk, kk] + AH[:, kk] - MatMult(W,HtH[:, kk])
            
            W[:, kk] = np.maximum(temp_vec, self.eps)
            
            ss = nla.norm(W[:, kk])
            
            if ss > 0:
                
                W[:, kk] = W[:, kk] / ss

        return (W, H)

'''
###############################################################################
NMF algorithm: Multiplicative updating 
Lee and Seung, Algorithms for non-negative matrix factorization, 
Advances in Neural Information Processing Systems, 2001, pp. 556-562.
###############################################################################
'''

class NMF_MU(NMF_Base):
    
    
    #Class initialising method
    def __init__(self, default_max_iter=500, default_max_time=np.inf):
        self.eps = 1e-16
        self.set_default(default_max_iter, default_max_time)

    #class iteration solver
    def IterSolver(self, A, W, H, k, it):

        #if we are windows or linux we can do Mu quick
        #print 'I was here 0'
        if File.IsWindows() :
            
            AtW = A.T.dot(W)
            
            HWtW = H.dot(W.T.dot(W)) + self.eps
            
            H = H * AtW
            
            H = H / HWtW
    
            AH = A.dot(H)
            
            WHtH = W.dot(H.T.dot(H)) + self.eps
            
            W = W * AH
            
            W = W / WHtH
        
        
        #If we are mac we have a multiprocessing issue
        else:
            
            AtW = MatMult(A.T,W)
            
            HWtW = MatMult(H,MatMult(W.T,W)) + self.eps
            
            H = H * AtW
            
            H = H / HWtW
            
            AH = MatMult(A,H)
            
            WHtH = MatMult(W,MatMult(H.T,H)) + self.eps
            
            W = W * AH
            
            W = W / WHtH

        return (W, H)


'''
###############################################################################
Default NMF algorithm: NMF_ANLS_BLOCKPIVOT
###############################################################################
'''
class NMF(NMF_ANLS_BLOCKPIVOT):

    #Class initialising method
    def __init__(self, default_max_iter=50, default_max_time=np.inf):
        
        self.set_default(default_max_iter, default_max_time)

'''
###############################################################################
.dot() is broken in parallel on macintosh so we rewrote the thing for
standart matrix multiplications.

takes a and b as matrix input where the multiplication dimension should be the
same.
###############################################################################
'''
def MatMult(a,b):
    import numpy
    
    #Dimension of a
    i = len(a)
    j = len(a[0])
    
    #dimension of b
    k = len(b)
    try:
        
        l = len(b[0])
    
    except:
        
        b = [b]
        
        l = len(b[0])

    k = len(b)

    #check 
    if not j == k :
        
        return 0
        
    #new array 
    Result = numpy.zeros((i,l))
    
    for i1 in range(0,i):
        
        for l1 in range(0,l):
            
            Val = a[i1,0]*b[0,l1]
            
            for k1 in range(1,k):
                
                #calc values
                Val += a[i1,k1]*b[k1,l1]
            
            Result[i1,l1] = Val
    
    return Result    
'''
###############################################################################
Compute the Frobenius norm of a matrix
    Parameters
    ----------
    X : numpy.array or scipy.sparse matrix
    Returns
    -------
    float
###############################################################################
'''
def norm_fro(X):
    
    
    
        
    if sps.issparse(X):     # scipy.sparse array
        return math.sqrt(MatMult(X,X).sum())
    else:                   # numpy array
        return nla.norm(X)

'''
###############################################################################
Compute the approximation error in Frobeinus norm
    norm(X - W.matmul(H.T)) is efficiently computed based on trace() expansion 
    when W and H are thin.
    Parameters
    ----------
    X : numpy.array or scipy.sparse matrix, shape (m,n)
    W : numpy.array, shape (m,k)
    H : numpy.array, shape (n,k)
    norm_X : precomputed norm of X
    Returns
    -------
    float
###############################################################################
'''
def norm_fro_err(X, W, H, norm_X):
        
    X = np.asarray(np.ndarray.tolist(X))
    
    W = np.asarray(np.ndarray.tolist(W))
    
    H = np.asarray(np.ndarray.tolist(H))
    
    sum_squared = (norm_X * norm_X
                   - 2 * np.trace(MatMult(np.transpose(H),MatMult(np.transpose(X),W)))
                   + np.trace(MatMult(MatMult(np.transpose(W),W),
                                      (MatMult(np.transpose(H),H)))))
    
    Return = math.sqrt(np.maximum(sum_squared, 0))
    
    
    return Return

'''
###############################################################################
Compute the norms of each column of a given matrix
    Parameters
    ----------
    X : numpy.array or scipy.sparse matrix
    Optional Parameters
    -------------------
    by_norm : '2' for l2-norm, '1' for l1-norm.
              Default is '2'.
    Returns
    -------
    numpy.array
###############################################################################
'''
def column_norm(X, by_norm='2'):
    
    if sps.issparse(X):
        
        if by_norm == '2':
            
            norm_vec = np.sqrt(MatMult(X,X).sum(axis=0))
        
        elif by_norm == '1':
            
            norm_vec = X.sum(axis=0)
        
        return np.asarray(norm_vec)[0]

    else:
        
        if by_norm == '2':
            
            norm_vec = np.sqrt(np.sum(X * X, axis=0))
        
        elif by_norm == '1':
            
            norm_vec = np.sum(X, axis=0)
        
        return norm_vec

'''
###############################################################################
Column normalization for a matrix pair 
    Scale the columns of W and H so that the columns of W have unit norms and 
    the product W.matmul(H.T) remains the same.  The normalizing coefficients are 
    also returned.
    Side Effect
    -----------
    W and H given as input are changed and returned.
    Parameters
    ----------
    W : numpy.array, shape (m,k)
    H : numpy.array, shape (n,k)
    Optional Parameters
    -------------------
    by_norm : '1' for normalizing by l1-norm, '2' for normalizing by l2-norm.
              Default is '2'.
    Returns
    -------
    ( W, H, weights )
    W, H : normalized matrix pair
    weights : numpy.array, shape k 
###############################################################################
'''
def normalize_column_pair(W, H, by_norm='2'):
    
    import numpy as np
    
    norms = column_norm(W, by_norm=by_norm)

    toNormalize = norms > 0
    W[:, toNormalize] = W[:, toNormalize] / norms[toNormalize]
    H[:, toNormalize] = H[:, toNormalize] * norms[toNormalize]

    weights = np.ones(norms.shape)
    weights[toNormalize] = norms[toNormalize]
    return (W, H, weights)

'''
###############################################################################
Column normalization
    Scale the columns of X so that they have unit l2-norms.
    The normalizing coefficients are also returned.
    Side Effect
    -----------
    X given as input are changed and returned
    Parameters
    ----------
    X : numpy.array or scipy.sparse matrix
    Returns
    -------
    ( X, weights )
    X : normalized matrix
    weights : numpy.array, shape k 
###############################################################################
'''
def normalize_column(X, by_norm='2'):

    if sps.issparse(X):
        weights = column_norm(X, by_norm)
        
        # construct a diagonal matrix
        dia = [1.0 / w if w > 0 else 1.0 for w in weights]
        
        N = X.shape[1]
        
        r = np.arange(N)
        
        c = np.arange(N)
        
        mat = sps.coo_matrix((dia, (r, c)), shape=(N, N))
        
        Y = X.matmul(mat)
        
        return (Y, weights)
    
    else:
        norms = column_norm(X, by_norm)
        
        toNormalize = norms > 0
        
        X[:, toNormalize] = X[:, toNormalize] / norms[toNormalize]
        
        weights = np.ones(norms.shape)
        
        weights[toNormalize] = norms[toNormalize]
        
        return (X, weights)

'''
###############################################################################
Delete rows from a sparse matrix
    Parameters
    ----------
    X : scipy.sparse matrix
    to_remove : a list of row indices to be removed.
    Returns
    -------
    Y : scipy.sparse matrix
###############################################################################
'''
def sparse_remove_row(X, to_remove):

    if not sps.isspmatrix_lil(X):
        
        X = X.tolil()

    to_keep = [i for i in xrange(0, X.shape[0]) if i not in to_remove]

    Y = sps.vstack([X.getrowview(i) for i in to_keep])
    
    return Y

'''
###############################################################################
Delete columns from a sparse matrix
    Parameters
    ----------
    X : scipy.sparse matrix
    to_remove : a list of column indices to be removed.
    Returns
    -------
    Y : scipy.sparse matrix
###############################################################################
'''
def sparse_remove_column(X, to_remove):
    
    B = sparse_remove_row(X.transpose().tolil(), to_remove).tocoo().transpose()
    return B
