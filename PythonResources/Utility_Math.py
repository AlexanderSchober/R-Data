# -*- coding: utf-8 -*-

#-INFO-
#-Name-Matrix_utils-
#-Version-0.1.0-
#-Date-22_April_2015-
#-Author-Alexander_Schober-
#-email-alex.schober@mac.com-
#-INFO-

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

import numpy as np
import scipy.sparse as sps
import numpy.linalg as nla
import math




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
        return math.sqrt(X.multiply(X).sum())
    else:                   # numpy array
        return nla.norm(X)

'''
###############################################################################
Compute the approximation error in Frobeinus norm
    norm(X - W.dot(H.T)) is efficiently computed based on trace() expansion 
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

    try:
        sum_squared = norm_X * norm_X - 2 * np.trace(H.T.dot(X.T.dot(W))) + np.trace((W.T.dot(W)).dot(H.T.dot(H)))
    except:
        print 'failed at calculating sum_squared'
    
    try:
        Return = math.sqrt(np.maximum(sum_squared, 0))
    except: 
        print 'failed at calculating return'
    
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
            norm_vec = np.sqrt(X.multiply(X).sum(axis=0))
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
    the product W.dot(H.T) remains the same.  The normalizing coefficients are 
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
        Y = X.dot(mat)
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


