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
from Function_Lorenzian     import Lorenzian
from Function_Linear        import Linear
from Function_Polynomial    import Polynome
from Function_Gaussian      import Gaussian

from Function_Lorenzian     import LorenzianInfo
from Function_Linear        import LinearInfo
from Function_Polynomial    import PolynomeInfo
from Function_Gaussian      import GaussianInfo


class RamanSignalGenerator:
    '''
    ###############################################################################
    This class will generate the different signall. Ths input array will give the 
    different parameters in DataArray:
    
    [   [Min, Max , Steps],
    
        [   [Type, Parameter[0], Parameter[1], ...] , 
            .
            .
            .
        ]
        
    ]
    ###############################################################################
    '''

    def __init__(self,DataArray):

        #save structure locally
        self.DataArray = DataArray
    
    def Generate(self):
    
        ########################
        #Set up X and Y
        self.X = [ float(i) * (self.DataArray[0][1]
                               - self.DataArray[0][0])
                  / self.DataArray[0][2]
                  + self.DataArray[0][0] for i in range(0, self.DataArray[0][2])]
                  
        self.Y = [0 for i in range(0, self.DataArray[0][2])]

        ########################
        #Set up initial arrays
        self.Lorrentz   = []
        self.Linear     = []
        self.Poly       = []
        self.Gauss      = []
        
        
        ########################
        #Set up initial arrays
        self.LorenzianInfo = LorenzianInfo()
        self.GaussianInfo = GaussianInfo()
        self.LinearInfo = LinearInfo()
        self.GaussianInfo = GaussianInfo()
        
        
        ########################
        #set up individual arrays
        for Element in self.DataArray[1]:

            #is it a lorrentzian
            if Element[0] == 'Lorr':

                #if lorrentzian append the class
                self.Lorrentz.append(Lorenzian(None, self.LorenzianInfo))

                #set the values
                self.Lorrentz[-1].Parameters = Element[1:]

            #is it a lorrentzian
            elif Element[0] == 'Linear':

                #if lorrentzian append the class
                self.Linear.append(Linear(None, self.LinearInfo))

                #set the values
                self.Linear[-1].Parameters = Element[1:]

            #is it a lorrentzian
            elif Element[0] == 'Poly':

                #if lorrentzian append the class
                self.Poly.append(Polynome(None, self.PolynomeInfo))

                #set the values
                self.Poly[-1].Parameters = Element[1:]

            #is it a lorrentzian
            elif Element[0] == 'Gauss':

                #if lorrentzian append the class
                self.Gauss.append(Gaussian(None, self.GaussianInfo))

                #set the values
                self.Gauss[-1].Parameters = Element[1:]


        ########################
        #Build the result
        for SubElement in [self.Lorrentz,self.Linear,self.Poly,self.Gauss]:

            for Element in SubElement:
                
                Proc = Element.ReturnData(self.X)
                
                self.Y = [self.Y[i] + Proc[i] for i in range(0, len(self.Y))]


    def Write(self):

        ########################
        #Initiate variable
        lines = []


        ########################
        #populate the line
        for i in range(0, len(self.X)):

            lines.append(str(self.X[i])+' '+str(self.Y[i])+'\n')


        ########################
        #write the line
        f = open(self.DataArray[0][3], 'w')

        f.writelines(lines)

        f.close()

if __name__ == "__main__":




    B = [   [250,550, 300, 'Film_Signal.txt'],
         
            [
                ['Lorr', 300, 10, 1500000, 0],
                ['Linear', 0, 0,  170000]
         
            ]
         
         
         ]

    A = RamanSignalGenerator(B)
    
    A.Generate()

    A.Write()







