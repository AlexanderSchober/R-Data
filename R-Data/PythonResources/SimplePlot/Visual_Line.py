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

class LineClass:
    
    '''
    ######################################################
    This class aims to draw lines to assist the user in
    displaying key elements. The Type option will tell
    if the line is either vertical or horizontal on the 
    plot interface. Note that like the plot we will allow
    the system to draw both in PIL and TKinter Canvas
    
    this instance was obvioulsy created to draw the lines
    always from one edge to the other ....
    ######################################################
    '''
    
    def __init__(self,Value,
                 Type = 'vertical',
                 Dash = '',
                 Thickness = 1,
                 Color = 'black',
                 Active = True,
                 Name = '',
                 style = ['',0,0],
                 Indentifier = None):


        #set the variables
        self.Value = Value
        self.Name  = 'Line'
        self.Type  = Type
        self.Dash  = Dash
        
        #set the parameters
        self.Thickness  = Thickness
        self.Color      = Color
        self.Active     = Active

        #set the style
        self.Style = style
    
        #identifier
        self.Identifier     = Indentifier
        self.CanvasObject   = False
        self.Verbose        = False


    def DrawPIL(self, Target, Parameters):

        '''
        ######################################################
        all plot elements will have an implicit draw method
        that will prepare the method and arguments to be drawn
        This instance will output the content into PIL
        ######################################################
        '''
                      
        #make the plot list
        if self.Type == 'vertical':
        
            DrawList = [((self.Value-Parameters[0][0])*Parameters[1][0]
                         +Parameters[2][0]+Parameters[3][0])*Parameters[4]*Parameters[6],
                        
                         (1-Parameters[2][1]-Parameters[3][1])*Parameters[5]*Parameters[6],
                        
                        ((self.Value-Parameters[0][0])*Parameters[1][0]
                         +Parameters[2][0]+Parameters[3][0])*Parameters[4]*Parameters[6],
                        
                         (Parameters[2][3]+Parameters[3][3])*Parameters[5]*Parameters[6]
                        ]
        else:
        
            DrawList = [(Parameters[2][0]+Parameters[3][0])*Parameters[4]*Parameters[6],
                        
                        (-(self.Value-Parameters[0][1])*Parameters[1][1]
                         +1-Parameters[2][1]-Parameters[3][1])*Parameters[5]*Parameters[6],
                        
                        (1-Parameters[2][2]+Parameters[3][2])*Parameters[4]*Parameters[6],
                        
                        (-(self.Value-Parameters[0][1])*Parameters[1][1]
                         +1-Parameters[2][1]-Parameters[3][1])*Parameters[5]*Parameters[6]
                        
                        ]
        
        #draw the object
        Target.line(DrawList,
                    fill    =   ColorLib.getrgb(self.Color),
                    width   =   self.Thickness*Parameters[6])
    

        #set the state
        self.CanvasObject   = False
    
    
    def DrawPyG(self, Target, Parameters):
        '''
        ######################################################
        PyGame imaging echnique. Note that this explicitly 
        calls an antialliassing method that is the line ...
        ######################################################
        '''
        
            
        #make the plot list
        if self.Type == 'vertical':
        
            DrawList = [(((self.Value-Parameters[0][0])*Parameters[1][0]
                         +Parameters[2][0]+Parameters[3][0])*Parameters[4],
                        
                         (1-Parameters[2][3]-Parameters[3][3])*Parameters[5]),
                        
                        (((self.Value-Parameters[0][0])*Parameters[1][0]
                         +Parameters[2][0]+Parameters[3][0])*Parameters[4],
                        
                         (Parameters[2][1]+Parameters[3][1])*Parameters[5])
                        ]
        else:
        
            DrawList = [((Parameters[2][0]+Parameters[3][0])*Parameters[4],
                        
                         ((self.Value-Parameters[0][1])*Parameters[1][1]
                          +Parameters[2][1]+Parameters[3][1])*Parameters[5]),
                        
                        ((1-Parameters[2][2]+Parameters[3][2])*Parameters[4],
                        
                         ((self.Value-Parameters[0][1])*Parameters[1][1]
                          +Parameters[2][1]+Parameters[3][1])*Parameters[5])
                        
                        ]
        
        
        ###########################
        #send out antialliassing
        self.AntiAlliasLine(Target, Parameters, DrawList[0],DrawList[1])
        
        if len(DrawList) > 2:
            self.AntiAlliasLine(Target, Parameters, DrawList[2],DrawList[3])

        #set the state
        self.CanvasObject   = False

    def AntiAlliasLine(self, Target, Parameters, X0,X1):
        '''
        ######################################################
        This converts the default method into a anti aliassed
        one. This particular case is for lines. Note that
        this allows the contour lines to be rather slooth
        ######################################################
        '''
        
        #define the center of my line
        center_L1       = [None]*2
        center_L1[0]    = (X0[0] + X1[0]) / 2.
        center_L1[1]    = (X0[1] + X1[1]) / 2.
    
        #grab the parameters
        length = math.sqrt((X0[0] - X1[0])**2+(X0[1] - X1[1])**2) # Line size
        angle = math.atan2(X0[1] - X1[1], X0[0] - X1[0])
    
        #define the edges
        UL = (center_L1[0] + (length / 2.) * math.cos(angle) - (self.Thickness / 2.) * math.sin(angle),
              center_L1[1] + (self.Thickness / 2.) * math.cos(angle) + (length / 2.) * math.sin(angle))
        UR = (center_L1[0] - (length / 2.) * math.cos(angle) - (self.Thickness / 2.) * math.sin(angle),
              center_L1[1] + (self.Thickness / 2.) * math.cos(angle) - (length / 2.) * math.sin(angle))
        BL = (center_L1[0] + (length / 2.) * math.cos(angle) + (self.Thickness / 2.) * math.sin(angle),
              center_L1[1] - (self.Thickness / 2.) * math.cos(angle) + (length / 2.) * math.sin(angle))
        BR = (center_L1[0] - (length / 2.) * math.cos(angle) + (self.Thickness / 2.) * math.sin(angle),
              center_L1[1] - (self.Thickness / 2.) * math.cos(angle) - (length / 2.) * math.sin(angle))
    
        #draw
        pygame.gfxdraw.aapolygon(Target, (UL, UR, BR, BL), ColorLib.getrgb(self.Color))
        pygame.gfxdraw.filled_polygon(Target, (UL, UR, BR, BL), ColorLib.getrgb(self.Color))
        
        #draw the cicrle at first end
        pygame.gfxdraw.aacircle(Target, int(X0[0]), int(X0[1]), int((self.Thickness / 2)),  ColorLib.getrgb(self.Color))
        pygame.gfxdraw.filled_circle(Target, int(X0[0]), int(X0[1]), int((self.Thickness / 2)),   ColorLib.getrgb(self.Color))
        
        #draw the circle at the last end
        pygame.gfxdraw.aacircle(Target, int(X1[0]), int(X1[1]), int((self.Thickness / 2)),   ColorLib.getrgb(self.Color))
        pygame.gfxdraw.filled_circle(Target, int(X1[0]), int(X1[1]), int((self.Thickness / 2)),   ColorLib.getrgb(self.Color))
    
    
    def DrawCanvas(self, Target, Parameters):

        '''
        ######################################################
        all plot elements will have an implicit draw method
        that will prepare the method and arguments to be drawn
        This Method will use the canvas draw method
        ######################################################
        '''
        
        
        #make the plot list
        if self.Type == 'vertical':
            
            DrawList = [((self.Value-Parameters[0][0])*Parameters[1][0]
                         +Parameters[2][0]+Parameters[3][0])*Parameters[4],
                        
                        (1-Parameters[2][1]-Parameters[3][1])*Parameters[5],
                        
                        ((self.Value-Parameters[0][0])*Parameters[1][0]
                         +Parameters[2][0]+Parameters[3][0])*Parameters[4],
                        
                        (Parameters[2][3]+Parameters[3][3])*Parameters[5]
                        ]
        else:
            
            DrawList = [(Parameters[2][0]+Parameters[3][0])*Parameters[4],
                        
                        (-(self.Value-Parameters[0][1])*Parameters[1][1]
                         +1-Parameters[2][1]-Parameters[3][1])*Parameters[5],
                        
                        (1-Parameters[2][2]-Parameters[3][2])*Parameters[4],
                        
                        (-(self.Value-Parameters[0][1])*Parameters[1][1]
                         +1-Parameters[2][1]-Parameters[3][1])*Parameters[5]
                        
                        ]

        #draw the object
        self.Identifier = Target.create_line(DrawList,
                                            fill     =   self.Color,
                                            width    =   self.Thickness,
                                            tag = 'Top')

        #set the state
        self.CanvasObject   = True
