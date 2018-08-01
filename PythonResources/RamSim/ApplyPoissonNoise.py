# -*- coding: utf-8 -*-
"""
###########################################################################
This routine will tke all files in a folder that are supposed to be raman
measurements and apply a poisson type noise ditribution to them and then
save the files again in a folder with the appendix - PNoise
###########################################################################
"""

#essential python updates for math

import numpy
from numpy.random import poisson as poisson
import Utility_File as File
import os
import sys


#set the folder path
PathIn = 'Dropbox/Data/G - Reports/2018 - Projects/2018_02_20 - Depth Simulation Output/Real Spectra/NNO_NGO_Simulation/Out - 1mum Sub_1/'

PathOut = 'Dropbox/Data/G - Reports/2018 - Projects/2018_02_20 - Depth Simulation Output/Real Spectra/NNO_NGO_Simulation/Out - 1mum Sub_1 Noise/'

Factor = 1e15
#grab the list of files in this folder
PathList = File.GetFileNames(PathIn,'.txt')

#make the out directory if it doesnt exist
try:
    os.stat(PathOut)
except:
    os.mkdir(PathOut)


#open each file
for Element in PathList:

    #########################
    #handle the input
    
    #open the file
    f = open(Element , 'r')
    
    #read all line
    Lines = f.readlines()
    
    #close the file
    f.close()

    #########################
    #handle the values
    
    #set the initial values
    X = []
    Y = []
    
    #loop over the lines
    for Line in Lines:

        X.append(float(Line.strip('\n').split(' ')[0]))
        Y.append(float(Line.strip('\n').split(' ')[1]))

    #########################
    #process the data
    for i in range(0,len(Y)):

        #handle poisson
        
        Y[i] *= Factor
        
        #Y[i] = poisson(Y[i],1)[0]

    #########################
    #handle the output

    #create the file
    f = open(PathOut + Element.split(PathIn)[1], 'w')

    #populate it
    Out = []

    #loop over
    for i in range(0, len(Y)):
        
        Out.append(str(X[i]) + ' ' + str(Y[i]) + '\n')

    #write the file
    f.writelines(Out)

    #close this file
    f.close()




