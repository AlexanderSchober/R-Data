# -*- coding: utf-8 -*-
'''
######################################################
################Simple Plot Method####################
######################################################

After seeing the complexity of Matplotlib regarding 
memory management I (Alexander Schober) have decided 
to work on my own plotting framework based on the
simple TKinter intherface. It allows object oriented
plotting and enough maniability to be used. 
Further more it allows for cross platform maniability.

A plot consists of different layers which have to be
taylored. This includes an axes layer and a draw layer. 
All plots and there information will saved into the 
Drawer. He is the main draw manager of the instance.
To him everything is linked that needs to be.
Note that he manages following instances:

- Axes (BUILT)
    All axes are defined by the axes class and drawn by here:
        - Grid Lines    (BUILT)
        - Tick Lines    (BUILT)
        - Tick Labels   (BUILT)
        - Axes lines    (BUILT)
        - inside padding    (BUILT)
        - outside padding   (BUILT)
        
- Zoomer (BUILT)
    He will manage the zoom box activated upon clicking
    
        - Zoom routines
        - Zoom bindings
        - Zoom box draw and refresh on move
        - unzoom on rightclick 
        - focused zoom on doubleclick
        
- Pointer (BUILT)
    The pointer method will decide what to do with 
    the mouse. While the mouse in matplotlib is
    very sluggish to code it was found that the 
    tkinter canvas manages it very smoothly. This
    is how we shall proceed. In the future we will 
    propose a variaty of crosshairs. Note that
    the canvas coordinates have to be fetched from 
    the root canvas method
    
- Mouse (BUILT)

- Key (BUILT)

- Keyboard (BUILT)

- Drawer (BUILT)

- MultiplotCanvas Accounts for multiple subplots.... (BUILT)
'''

#-INFO-
#-Name-SimplePlot-
#-Version-0.1.0-
#-Date-15_January_2016-
#-Author-Alexander_Schober-
#-email-alex.schober@mac.com-
#-INFO-

#import Tkinter related libraries
from Tkinter import *
import tkFont
import ttk
import Tkinter
import tkFileDialog
from tkColorChooser import askcolor
import profile

#import basic libraris
import numpy
import math
import os
import time

#import imaging libraries
import PIL
from PIL import Image,ImageDraw
from PIL import ImageTk
from PIL import ImageFilter
from PIL import ImageColor as ColorLib

#the last 'fast visual'
import pygame as pyg
import pygame.gfxdraw

#multiprocessing routine
import multiprocessing


class Zoomer:
    
    '''
    ######################################################
    This class is here to zoom and dezoom the canvas. This
    will take over methods present in version 0.0.5 where
    the zoom class was definied individually.
    
    In a future version we will include a double click
    method able to handle the focus on a single plot
    object. This will be done in junction with the Pointer
    class.
    

    ######################################################
    '''
    
    def __init__(self, Canvas):
        
        #Bind to the canvas.
        self.Canvas = Canvas
        
        #verbose
        self.Verbose = False
    
        #launch defaults
        self.SetInitial()
    
    def SetInitial(self):
        '''
        ######################################################
        This class allows to dicretly manage the initialisation
        and for further manipulations if the user wnats a reset
        ######################################################
        '''
        #cursor parameters
        self.Color      = 'black'
        self.Thickness  = 2
        self.Roundness  = 5


    def Listen(self):

        '''
        ######################################################
        This method is there to start listening for different
        events. This includes the click and release.
        ######################################################
        '''
        #bind method to the mouse click
        self.BoundMethod_0 = self.Canvas.bind('<Button-1>', self.StartZoomBox,'+')
        
        #start the motion lister as well as the kill listener
        self.BoundMethod_1 = self.Canvas.bind('<ButtonRelease-1>'   , self.KillZoomBox      ,'+')
        
        #link the method
        self.Canvas.Drawer.Mouse.Bind('<B1-Motion>',self.UpdateZoomBox,'Pointer')
        
        #verbose
        if self.Verbose:
            
            print 'The zoomer got bound'

    def Quiet(self):

        '''
        ######################################################
        This method is there to start listening for different
        events. This includes the click and release.
        ######################################################
        '''
        #bind method to the mouse click
        self.Canvas.unbind('<Button-1>', self.BoundMethod_0)
        
        #start the motion lister as well as the kill listener
        self.Canvas.unbind('<ButtonRelease-1>'   , self.BoundMethod_1)
        
        #link the method
        self.Canvas.Drawer.Mouse.Unbind('<B1-Motion>','Pointer')
        
        #verbose
        if self.Verbose:
            
            print 'The zoomer got unbound'

    def StartZoomBox(self,event):

        '''
        ######################################################
        This method initialises the zoom box and grabs the
        initial coordinates. Note that it also starts the 
        end and move listeners
        ######################################################
        '''
        
        #verbose
        if self.Verbose:
            
            print 'I am entering zoom mode'
            
        #grab the actual cursor position from the Pointer class
        X, Y = self.Canvas.Drawer.Mouse.Cursor_x,self.Canvas.Drawer.Mouse.Cursor_y
        
        self.StartPositions     = [X,Y]
        self.EndPositions       = [X,Y]
        
        #calculate the adapted canvas position
        self.StartPositionsScale = [((X-self.Canvas.Drawer.BoundingBoxOffset[0])*self.Canvas.Drawer.BoundingBoxFactor[0]
                                +self.Canvas.Drawer.Axes.PaddingIn[0]+self.Canvas.Drawer.Axes.PaddingOut[0])*self.Canvas.Drawer.wScaleFactor,
                                    
                               (1-(Y-self.Canvas.Drawer.BoundingBoxOffset[1])*self.Canvas.Drawer.BoundingBoxFactor[1]
                                 -self.Canvas.Drawer.Axes.PaddingIn[1]-self.Canvas.Drawer.Axes.PaddingOut[1])*self.Canvas.Drawer.hScaleFactor]
        
        #create the zoom box with associated ID
        self.ZoomBox = self.Canvas.create_rectangle(self.StartPositionsScale[0],
                                                    self.StartPositionsScale[1],
                                                    self.StartPositionsScale[0],
                                                    self.StartPositionsScale[1],
                                                    width = self.Thickness,
                                                    outline = self.Color,
                                                    tag = 'Top')




    def UpdateZoomBox(self,X,Y):

        '''
        ######################################################
        This method initialises the zoom box and grabs the
        initial coordinates. Note that it also starts the 
        end and move listeners
        ######################################################
        '''
        
        #grab the actual cursor position from the Pointer class
        self.EndPositions = [X,Y]
        
        #calculate the adapted canvas position
        self.EndPositionsScale = [((X-self.Canvas.Drawer.BoundingBoxOffset[0])*self.Canvas.Drawer.BoundingBoxFactor[0]
                                +self.Canvas.Drawer.Axes.PaddingIn[0]+self.Canvas.Drawer.Axes.PaddingOut[0])*self.Canvas.Drawer.wScaleFactor,
                               (1-(Y-self.Canvas.Drawer.BoundingBoxOffset[1])*self.Canvas.Drawer.BoundingBoxFactor[1]
                                 -self.Canvas.Drawer.Axes.PaddingIn[1]-self.Canvas.Drawer.Axes.PaddingOut[1])*self.Canvas.Drawer.hScaleFactor]
        

        #update the rectangle
        self.Canvas.coords(self.ZoomBox,
                           self.StartPositionsScale[0],
                           self.StartPositionsScale[1],
                           self.EndPositionsScale[0],
                           self.EndPositionsScale[1])
    
        #try to project the information onto the first two free
        #fields of the main canvas
        try:
            self.Canvas.Multi.ManagerLabels[0].configure(text = ' X: '+str(round(numpy.min([self.EndPositions[0], self.StartPositions[0]]),self.Roundness)))
            self.Canvas.Multi.ManagerLabels[1].configure(text = 'to: '+str(round(numpy.max([self.EndPositions[0], self.StartPositions[0]]),self.Roundness)))
            self.Canvas.Multi.ManagerLabels[2].configure(text = ' Y: '+str(round(numpy.min([self.EndPositions[1], self.StartPositions[1]]),self.Roundness)))
            self.Canvas.Multi.ManagerLabels[3].configure(text = 'to: '+str(round(numpy.max([self.EndPositions[1], self.StartPositions[1]]),self.Roundness)))
            
        except:
            pass
        
        #verbose
        if self.Verbose:
            print 'X, and Y are: ',X,Y
            print 'I am updating the zoombox to:'
            print 'Start :',self.StartPositions
            print 'End : ',self.EndPositions



    def KillZoomBox(self,event):

        '''
        ######################################################
        This method initialises the zoom box and grabs the
        initial coordinates. Note that it also starts the 
        end and move listeners
        ######################################################
        '''
        
        #visual purpose we need to destroy the zoom box
        self.Canvas.delete(self.ZoomBox)
        
        #verbose
        if self.Verbose:
            
            print 'I killed the zoom box'
        
        #kill the lsiteners
        #self.Canvas.unbind('<B1-Motion>'        , self.BoundMethod_0 )
        #self.Canvas.unbind('<ButtonRelease-1>'  , self.BoundMethod_1 )
        
        #verbose
        if self.Verbose:
            
            print 'I unlinked the listeners'
        
        if self.StartPositions[0] == self.EndPositions[0] or self.StartPositions[1] == self.EndPositions[1]:
        
            #unzoom
            self.Canvas.Drawer.ZoomBox = [None,None,None,None]
        
        else:
            
            #send out the zoom info and formati it
            self.Canvas.Drawer.ZoomBox = [numpy.min([self.StartPositionsScale[0],self.EndPositionsScale[0]]),
                                          numpy.min([self.StartPositionsScale[1],self.EndPositionsScale[1]]),
                                          numpy.max([self.StartPositionsScale[0],self.EndPositionsScale[0]]),
                                          numpy.max([self.StartPositionsScale[1],self.EndPositionsScale[1]])]
        
            self.Canvas.Drawer.ZoomBox = [self.EvaluateMousePos(*self.Canvas.Drawer.ZoomBox)[i] for i in range(0,4)]
        
        
        #try to project the information onto the first two free
        #fields of the main canvas
        try:
            self.Canvas.Multi.ManagerLabels[0].configure(text = '')
            self.Canvas.Multi.ManagerLabels[1].configure(text = '')
            self.Canvas.Multi.ManagerLabels[2].configure(text = '')
            self.Canvas.Multi.ManagerLabels[3].configure(text = '')
            
        except:
            pass
        
        
        if self.Verbose:
        
            print self.StartPositionsScale
            print self.EndPositionsScale
            print 'The zoom Box is : ',self.Canvas.Drawer.ZoomBox
        

        #zoom
        self.Canvas.delete(self.ZoomBox)
        self.Canvas.Drawer.Zoom()

    def EvaluateMousePos(self,X_0,Y_0,X_1,Y_1):
        
        '''
        ######################################################
        This method pushes out the actual coordinates after 
        grabing all the padding criterias and so on
        
        This method can be called externally and returns
        self.Cursor_x and self.Cursor_y
        ######################################################
        '''
        
        ########################################################
        #try to fetch new positions
        self.DeltaX = (self.Canvas.Drawer.Axes.PaddingIn[0]
                       +self.Canvas.Drawer.Axes.PaddingIn[2]
                       +self.Canvas.Drawer.Axes.PaddingOut[0]
                       +self.Canvas.Drawer.Axes.PaddingOut[2])*self.Canvas.width
                       
        self.DeltaY = (self.Canvas.Drawer.Axes.PaddingIn[1]
                       +self.Canvas.Drawer.Axes.PaddingIn[3]
                       +self.Canvas.Drawer.Axes.PaddingOut[1]
                       +self.Canvas.Drawer.Axes.PaddingOut[3])*self.Canvas.height
        
        #grab the actual top left part of the draw zone
        self.DrawTopX = (self.Canvas.Drawer.Axes.PaddingIn[0]
                       +self.Canvas.Drawer.Axes.PaddingOut[0])*self.Canvas.width
                       
        self.DrawTopY = (self.Canvas.Drawer.Axes.PaddingIn[3]
                       +self.Canvas.Drawer.Axes.PaddingOut[3])*self.Canvas.height
        
        self.DrawWidth  = self.Canvas.width  - int(self.DeltaX)
        self.DrawHeight = self.Canvas.height - int(self.DeltaY)
        
        
        #calculate the actual coordinates
        Cursor_x_0 = (self.Canvas.Drawer.BoundingBoxOffset[2]-self.Canvas.Drawer.BoundingBoxOffset[0])*((float(X_0)-float(self.DrawTopX))/float(self.DrawWidth))+self.Canvas.Drawer.BoundingBoxOffset[0]

        Cursor_y_0 = (self.Canvas.Drawer.BoundingBoxOffset[1]-self.Canvas.Drawer.BoundingBoxOffset[3])*((float(Y_0)-float(self.DrawTopY))/float(self.DrawHeight))+self.Canvas.Drawer.BoundingBoxOffset[3]
        
        Cursor_x_1 = (self.Canvas.Drawer.BoundingBoxOffset[2]-self.Canvas.Drawer.BoundingBoxOffset[0])*((float(X_1)-float(self.DrawTopX))/float(self.DrawWidth))+self.Canvas.Drawer.BoundingBoxOffset[0]

        Cursor_y_1 = (self.Canvas.Drawer.BoundingBoxOffset[1]-self.Canvas.Drawer.BoundingBoxOffset[3])*((float(Y_1)-float(self.DrawTopY))/float(self.DrawHeight))+self.Canvas.Drawer.BoundingBoxOffset[3]
        
        #for debugging puproses
        if self.Verbose:
            
            #print the coordinates
            print 'These are the actual zoom coordinates: ',Cursor_x_0 , Cursor_y_0 , Cursor_x_1 , Cursor_y_1

        return Cursor_x_0 , Cursor_y_0 , Cursor_x_1 , Cursor_y_1




