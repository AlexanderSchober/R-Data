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

class RangeClass:
    
    '''
    ######################################################
    This class allows for range creations
    ######################################################
    '''
    
    def __init__(self,Coordinates, Indentifier):
        
        
        #set the variables
        self.Coordinates = Coordinates
        self.Color       = 'grey'#u'#E0E0E0'
        self.Identifier  = Indentifier
        self.CanvasObject   = False
        self.Active         = True
        self.Name           = 'ROI'
        self.Verbose        = False

    def DrawPIL(self, Target, Parameters):

        '''
        ######################################################
        all plot elements will have an implicit draw method
        that will prepare the method and arguments to be drawn
        This instance will output the content into PIL
        ######################################################
        '''
        if self.Verbose:
            
            print Parameters
                      
        #grab coordinates
        Coordinates = [((self.Coordinates[0]-Parameters[0][0])*Parameters[1][0]
                        +Parameters[2][0]+Parameters[3][0])*Parameters[4]*Parameters[6],
                       
                       (Parameters[3][3])*Parameters[5]*Parameters[6],
                       
                       ((self.Coordinates[1]-Parameters[0][0])*Parameters[1][0]
                        +Parameters[2][0]+Parameters[3][0])*Parameters[4]*Parameters[6],
                       
                       (1-Parameters[3][1])*Parameters[5]*Parameters[6]]
     
        #fetch the region and draw it:
        Target.rectangle(Coordinates,
                         fill = ColorLib.getrgb(self.Color))

        #set the state
        self.CanvasObject   = False

    def DrawPyG(self, Target, Parameters):

        '''
        ######################################################
        all plot elements will have an implicit draw method
        that will prepare the method and arguments to be drawn
        This instance will output the content into PIL
        ######################################################
        '''
        if self.Verbose:
            
            print Parameters
                      
        #grab coordinates
        Coordinates = [(((self.Coordinates[0]-Parameters[0][0])*Parameters[1][0]
                        +Parameters[2][0]+Parameters[3][0])*Parameters[4],
                       
                       (Parameters[3][1])*Parameters[5]),
                       
                       (((self.Coordinates[0]-Parameters[0][0])*Parameters[1][0]
                        +Parameters[2][0]+Parameters[3][0])*Parameters[4],
                       
                       (1-Parameters[3][3])*Parameters[5]),
                       
                       (((self.Coordinates[1]-Parameters[0][0])*Parameters[1][0]
                        +Parameters[2][0]+Parameters[3][0])*Parameters[4],
                       
                       (1-Parameters[3][3])*Parameters[5]),
                       
                       (((self.Coordinates[1]-Parameters[0][0])*Parameters[1][0]
                        +Parameters[2][0]+Parameters[3][0])*Parameters[4],
                       
                       (Parameters[3][1])*Parameters[5])]
     
        #fetch the region and draw it:
        self.AntiAlliasPolygone(Target, Coordinates)

        #set the state
        self.CanvasObject   = False

    def AntiAlliasPolygone(self, Target, DrawList):
        '''
        ######################################################
        This converts the default method into a anti aliassed
        one. This particular case is for lines. Note that
        this allows the contour lines to be rather slooth
        ######################################################
        '''
        
    
        #draw
        pygame.gfxdraw.aapolygon(Target, DrawList, ColorLib.getrgb(self.Color))
        pygame.gfxdraw.filled_polygon(Target, DrawList, ColorLib.getrgb(self.Color))
    
    def DrawCanvas(self, Target, Parameters):

        '''
        ######################################################
        all plot elements will have an implicit draw method
        that will prepare the method and arguments to be drawn
        This Method will use the canvas draw method
        ######################################################
        '''

        #grab coordinates
        Coordinates = (((self.Coordinates[0]-Parameters[0][0])*Parameters[1][0]
                        +Parameters[2][0]+Parameters[3][0])*Parameters[4],
                       
                       (Parameters[3][3])*Parameters[5],
                       
                       ((self.Coordinates[1]-Parameters[0][0])*Parameters[1][0]
                        +Parameters[2][0]+Parameters[3][0])*Parameters[4],
                       
                       (+1-Parameters[3][1])*Parameters[5])
                       
    
        #fetch the region and draw it:
        self.Identifier  = Target.create_rectangle(Coordinates,
                                                   fill = self.Color,
                                                   tag = 'Top')

        #set the state
        self.CanvasObject   = True
