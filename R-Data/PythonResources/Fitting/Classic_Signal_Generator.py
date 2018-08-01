# -*- coding: utf-8 -*-
"""
Created on Mon May 11 10:30:43 2015

@author: Schober 
"""


########################################
###########GENERAL IMPORTS##############
########################################

#systeme library
import sys

#import numpy datastructure management
import numpy
import scipy

########################################
##########SPEC.  Breakdowns#############
########################################

class ClassicalSignalGenerator:
    '''
    ###############################################################################
    This class will generate the different signall. Ths input array will give the 
    different parameters in DataArray:
    
    [[X, Y] ,
            .
            .
            .
     ]
    ###############################################################################
    '''

    def __init__(self,DataArray, Path):

        #save structure locally
        self.DataArray = DataArray
    
        #set the path
        self.Path = Path
    
    def Write(self):

        ########################
        #Initiate variable
        lines = []
        
        ########################
        #populate the line
        for i in range(0, len(self.DataArray)):

            lines.append(str(self.DataArray[i][0])+' '+str(self.DataArray[i][1])+'\n')

        ########################
        #write the line
        f = open(self.Path, 'w')

        f.writelines(lines)

        f.close()









