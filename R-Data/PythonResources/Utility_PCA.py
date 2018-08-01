# -*- coding: utf-8 -*-

#-INFO-
#-Name-PCAEdit-
#-Version-0.1.0-
#-Date-22_April_2016-
#-Author-Alexander_Schober-
#-email-alex.schober@mac.com-
#-INFO-

print 'Loading PCA computing dependencies...'

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

#common imports
import numpy
import sys


#scientifi imports
from math import log, sqrt
from scipy import linalg
from scipy.special import gammaln


#proceed with sklearn imports
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils import as_float_array


class PCA(BaseEstimator, TransformerMixin):
    """
    ###########################################################################

    ###########################################################################
    """
    
    def __init__(self, copy = True, whiten=False):
        
        self.copy        = copy
        self.CompMean    = True
        self.TakeBase    = False


    def fit(self, X):
        
        """
        #######################################################################
        
        #######################################################################    
        """
        
        #Convert array into numpy 2d array just to be sure
        X = numpy.asarray(X)
        
        #Get dimentions of the array
        SampleNumber, NumberOfFeatures = X.shape
        
        #catch component number
        self.ComponentsNum = NumberOfFeatures
        
        #Convert the array to float
        X = as_float_array(X,
                           copy = self.copy)
        
        #do we remove the mean ?
        if self.CompMean:
            
            # Center data This means substracting mean value along the x axis       
            self.Mean = numpy.mean(X, axis=0)            
            X -= self.Mean
        
        #Compute the PCA wich is matrix numpy linearisations
        UnitaryMatrice_In, DiagonalMatrix, UnitaryMatrice_Out = linalg.svd(X,
                                                                           full_matrices = False)

        #Compute Vriance
        ExplainedVariance = (DiagonalMatrix ** 2) / SampleNumber
        
        #Compute variance ratio
        ExplainedVarianceRatio = (ExplainedVariance / ExplainedVariance.sum())
        
        #Extract components
        Components = UnitaryMatrice_Out

        #Fetch number of components desired
        ComponentsNum = self.ComponentsNum

        # Compute noise covariance using Probabilistic PCA model
        self.NoiseVariance = 0.

        # store SampleNumber to revert whitening when getting covariance
        self.SampleNumber               = SampleNumber
        self.Components                 = Components[:ComponentsNum]
        self.ExplainedVariance          = ExplainedVariance[0:ComponentsNum-2]
        self.ExplainedVarianceRatio_1   = ExplainedVarianceRatio[:ComponentsNum]
        self.ExplainedVarianceRatio     = ExplainedVarianceRatio
        self.ComponentsNum              = ComponentsNum
        
        #finally compute components and send them out
        self.CalcComponents(X)
        
        return (UnitaryMatrice_In, DiagonalMatrix, UnitaryMatrice_Out)

    def CalcComponents(self, X):
        
        #Compute score by projecting on each element
        Scores = numpy.dot(X,self.Components.transpose())
        
        #transpose the score
        self.Scores = Scores.transpose()










