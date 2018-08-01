# -*- coding: utf-8 -*-
"""
Created on Mon May 11 10:30:43 2015

@author: Schober 
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

#numpyy mathematical import
import numpy

#scipy import
import scipy

#######################################
#advanced imports

#Thread the fiting process to avoid ssytem lockup
from threading import Thread, Event
from Queue import Queue

#######################################
#advanced imports

#fitting routines
from scipy.optimize import least_squares

from scipy.optimize import leastsq

from scipy.sparse.linalg import spsolve

######################################
#import matplotlib for colors
import matplotlib



"""
##################################################
These Interface imports. The whole application is 
based on the Tkinter framework which interfaces 
Tk/Tcl cross platform elements with Python
##################################################
"""

#########################
#import Tk/Tcl interface to Python
if sys.version_info[0] < 3:
    
    import Tkinter as tk

else:
    
    import tkinter as tk

#Tk variable objects
import Tkconstants

#dialog for import saving
import tkFileDialog

#enhanced tkinter layout
import ttk

#import the font mofifer
import tkFont

#Special textbox arrangement
import ScrolledText

#########################
#import image management routines
from PIL import Image, ImageTk


"""
##################################################
These are the custome imports
##################################################
"""

#import Utility for requests
from .. import Utility_Main         as Utility
from .. import Utility_File         as File

#load the drawer class
from Raman_Fit_Visual import DrawClass

class FitDispatcher:
    
    '''
    ##################################################
    This class will have refresh function for the
    current graphical object.
    
    ##################################################
    '''
    def __init__(self,DataClass):
    
    
        #Take over class adresses
        self.DataClass = DataClass
        self.RawData   = DataClass.RawData
        self.CompData  = DataClass.CompData

        #Define graph parameters
        self.BoundingBox = [0,0,0,0]

        #Define fit window parameters
        self.FigHeight = 10
        self.FigWidth  = 16
        
        #Define info window parameters
        self.FigHeightText = 5
        self.FigWidthText  = 10
    
        self.ResetViewVar = True

        #finnally initiatethe drawclass
        self.DrawClass = DrawClass(self.DataClass)

    def Reset(self):
        '''
        ##################################################
        Reinitialise the Drawer class
        ##################################################
        '''
        try:
            del self.DrawClass
            self.DrawClass = DrawClass(self.DataClass)
        except:
            print 'could not reset'
    
    def ReadPosition(self):
        '''
        ##################################################
        This function will be the
        ##################################################
        '''
        
        #Set the folder Windows specific handling done within
        inTxt  = FileManagement.GetRuntimeTextFile(['Default_Ini','WINDOW_FIT1.txt'])
        outTxt = FileManagement.GetRuntimeTextFile(['Default_Ini','WINDOW_FIT2.txt'])

        #Read the text file
        Read = open(inTxt,'r')
    
        #Read lines
        Lines = Read.readlines()
        
        #Read the first line
        self.FitValues = Lines[0].split(' ')
        
        #convert
        self.FitValues = [float(i) for i in self.FitValues]
        
        #close the file and write it
        Read.close
        
        #Read the text file        
        Read = open(outTxt,'r')

        #Read lines
        Lines = Read.readlines()
        
        #Read the first line
        self.InfoValues = Lines[0].split(' ')
        
        #convert
        self.InfoValues = [float(i) for i in self.InfoValues]
    
        #close the file and write it
        Read.close

    def WritePosition(self,ID,x,y,dx,dy):
        '''
        ##################################################
        This function will be the
        ##################################################
        '''
        
        #Set the folder Windows specific handling done within
        inTxt  = FileManagement.GetRuntimeTextFile(['Default_Ini','WINDOW_FIT1.txt'])
        outTxt = FileManagement.GetRuntimeTextFile(['Default_Ini','WINDOW_FIT2.txt'])

        #write the text file
        if ID == 0:
            Write = open(inTxt,'wb')
            self.FitValues = [x,y,dx,dy]
        elif ID == 1:
            Write = open(outTxt,'wb')
            self.InfoValues = [x,y,dx,dy]
    
        #Insert the created text line
        Write.writelines(str(x)+' '+str(y)+' '+str(dx)+' '+str(dy))
    
        #close the file and write it
        Write.close


    def BuildScatter(self,SubPlot,Type = [10,0,'',False]):
    
        '''
        ######################################################################
        This function will launcht the scatter plot interfacer onto the target
        
        Note taht passing through the fititng class has historical reasons
        as it may seem unnecessarily complicated
        ######################################################################
        '''
        
        #send it out
        self.DrawClass.Place(SubPlot,Type, Update = False)
    
    def BuildLowerGraph(self,SubPlot, Update = False):
        '''
        ######################################################################
        This function will build the current grpah subplot and resize elements
        accordingly
        ######################################################################
        '''
        
        #send it out
        self.DrawClass.Place(SubPlot,Type = [0,0,'',False], Update = Update)

    def BuildLowerGraph2(self,SubPlot, Update = False):
        '''
        ######################################################################
        This function will build the current grpah subplot and resize elements
        accordingly
        ######################################################################
        '''

        #spwn
        self.DrawClass.Place(SubPlot,Type = [1,0,'',False], Update = Update)
    
    def BuildRestGraph(self,SubPlot, Update = False):
        '''
        ######################################################################
        This function will build the current grpah subplot and resize elements
        accordingly
        ######################################################################
        '''

        #spwn
        self.DrawClass.Place(SubPlot,Type = [3,0,'',False], Update = Update)
    
    def BuildBaseGraph(self,SubPlot,Container):
        '''
        ######################################################################
        This function will build the current grpah subplot and resize elements
        accordingly
        ######################################################################
        '''
        
        #Caomputation plot migth be seeded with hole so need to buil it first (same as for fiting)
        #Prepare DataX and DataY
        
        SubPlot.cla()
        SubPlot.plot(Container[0],Container[1],color="blue",linewidth=1.5)
        SubPlot.plot(Container[2],Container[3],color="red",linewidth=1.5)
        SubPlot.plot(Container[4],Container[5],color="black",linewidth=2.5)
        
        #build min max rrays
        XMin = numpy.min([numpy.min(Container[0]),numpy.min(Container[2]),numpy.min(Container[4])])
        XMax = numpy.max([numpy.max(Container[0]),numpy.max(Container[2]),numpy.max(Container[4])])
        YMin = numpy.min([numpy.min(Container[1]),numpy.min(Container[3]),numpy.min(Container[5])])
        YMax = numpy.max([numpy.max(Container[1]),numpy.max(Container[3]),numpy.max(Container[5])])
        
        #if a minimum setting has been set
        if self.ResetViewVar:
            SubPlot.set_xlim(XMin,XMax)
            SubPlot.set_ylim(YMin,YMax)
        
        return SubPlot

    def BuildUpperGraph(self,SubPlot,Class,InitialRun = False, Update = False):
        '''
        ######################################################################
        This function will build the current main subplot and resize elements
        accordingly
        ######################################################################
        '''
        
        #send it out
        self.DrawClass.Place(SubPlot,Type = [2,0,'',False], Update = Update)
