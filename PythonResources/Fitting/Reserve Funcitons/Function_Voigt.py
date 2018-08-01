#--FUNCTION--#

# -*- coding: utf-8 -*-
"""
Created on Mon May 11 10:30:43 2015

@author: Schober 
"""
import numpy

class VoigtInfo:
    '''
    ###############################################################################
    This class will contain information about the function, parameters and names
    ###############################################################################
    '''
    
    def __init__(self):
        
        #--------------------------------------------------------#
        #--------------------------------------------------------#
        #---------------------   EDIT   -------------------------#
        #--------------------------------------------------------#
        #--------------------------------------------------------#
        
        #######################
        #name of the function
        self.Name = 'Voigt'
        
        #how to order the functions( do not touch lorenz and linear)
        self.Order = 4
        
        #number of parameters
        self.ParameterNumber        = 3
        
        #######################
        #parameter names
        self.ParameterNames         = ['Position',
                                       'Amplitude',
                                       'Tau']
                                        
        #Parameter units
        self.ParameterUnit          = ['cm-1',
                                       'Intensity',
                                       'cm-1']
                                       
        #######################
        #Parameter Boundaries
        self.ParameterBoundaries    = [['-1.0','1.0'],        # <- Relative shift min, max
                                       ['xmin','xmax'],     # <- Absolute shift min, max
                                       
                                       ['-2.0','2.0'],          # <- Relative shift min, max
                                       ['0.0','Inf'],      # <- Absolute shift min, max
                                       
                                       ['-0.1','0.1'],    # <- Relative shift min, max
                                       ['0.01','200'],         # <- Absolute shift min, max
                                       
                                       ]

        #######################
        #Parameter Boundaries
        self.ParameterProcessing    = ['1',         # <- Number of iteration
                                       '0,1,2']   # <- Order of Processing
        #--------------------------------------------------------#
        #--------------------------------------------------------#
        #---------------------  NO EDIT -------------------------#
        #--------------------------------------------------------#
        #--------------------------------------------------------#

class Voigt:
    '''
    ###############################################################################
    In this class we will store the croped data used for the calculation
    this data can be modified once the class is loaded to fit the needs
    ###############################################################################
    '''
    
    def __init__(self,FitData, Info):
        
        #Link this class to the lorrentzian computation
        self.FitData = FitData
        self.Info = Info

        #--------------------------------------------------------#
        #--------------------------------------------------------#
        #---------------------   EDIT   -------------------------#
        #--------------------------------------------------------#
        #--------------------------------------------------------#
        
        #define the types
        self.Type = 'Voigt'
    
        #--------------------------------------------------------#
        #--------------------------------------------------------#
        #---------------------  NO EDIT -------------------------#
        #--------------------------------------------------------#
        #--------------------------------------------------------#
        
        #Initialise basic lorrentzian parameters to b changed later
        self.Parameters     = [0,0,0,0,0]
        self.ParametersIni  = [0,0,0,0,0]
        self.ParametersFix  = [0,0,0,0,0]
        
        #Set boolean variables
        self.isCalculated   = False
        self.x              = []
    
        #set the visuals
        self.SetVisuals()

    def Function(self,Parameters):
        '''
        ###############################################################################
        This will be the main function name and shoud thereofre be called Function
        
        The first parameter will be x and should therefore be loaded. We recommend
        unfolding the actual elements and giving them proper names to allows for a more
        simple understanding of the function.
        ###############################################################################
        '''
        #unfold x
        x           = numpy.asarray(Parameters[0])
        
        #--------------------------------------------------------#
        #--------------------------------------------------------#
        #---------------------   EDIT   -------------------------#
        #--------------------------------------------------------#
        #--------------------------------------------------------#
        
        #function parameters
        Position    = Parameters[1]
        Amplitude   = Parameters[2]
        Tau         = Parameters[3]
    
        #process the function
        
        y           = (Amplitude
                       * numpy.exp(-(
                                     (x - Position)**2.)
                                   /(2. * Tau **2.)))
        
        #--------------------------------------------------------#
        #--------------------------------------------------------#
        #---------------------  NO EDIT -------------------------#
        #--------------------------------------------------------#
        #--------------------------------------------------------#
        
        #return the function
        return y
    
    def Compute(self,X):
        '''
        ###############################################################################
        This classes serves to compute and access single lorrentzians for given input
        
        In the new version we introduced the assymetric funcitons and therefore we need
        to check for the assymtry and if the assymetry is present compute it...
        ###############################################################################
        '''
        
        #Function
        self.yBis       = self.ReturnData(X)
        
        #set x
        self.x          = X
        
        #immidiately take the informations
        self.yRangeBis  = [numpy.min(self.yBis),numpy.max(self.yBis)]
        self.xRange     = [numpy.min(self.x),numpy.max(self.x)]

    def ReturnData(self,X):
        '''
        ###############################################################################
        This classes serves to compute and access single lorrentzians for given input
        
        In the new version we introduced the assymetric funcitons and therefore we need
        to check for the assymtry and if the assymetry is present compute it...
        ###############################################################################
        '''
        
        #set the parameters
        Parameters = [X]
        
        #pack the parameters
        for i in range(0, self.Info.ParameterNumber):
            
            Parameters.append(self.Parameters[i+1])
        
        #compute y and send it back to whoever called it
        y = self.Function(Parameters)
        
        #return
        return y
    
    def SetVisuals(self):
        '''
        ###############################################################################
        It was found that this place is the most appropriate to set visuals for the 
        plot. Note that this will be used to initialize and reset the color and 
        the thickness as well as the Group
        
        the group can be used to toggle on and off info
        ###############################################################################
        '''

        #set initial group
        self.Group = 0

        #set the initial color
        self.Color = '#000000'

        #st the initial thickess
        self.Thickness = int(3)

        #set the initial thickess
        self.Trace = True

        #allow for a name
        self.Name = 'None given'
