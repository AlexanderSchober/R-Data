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

class TitleClass:

    '''
    ######################################################
    This class is built in the subplot routine but injects
    its dependencies and methods into the associates
    PlotCanavas though the self.Title variavle pointing
    back to this class. 
    
    This is done to facilitae the space management. Note
    the the tile will be built in a frame with a centered
    label widget....
    
    
    The subplot manager will manage the placement through 
    root as the input
    ######################################################
    '''
    
    def __init__(self, Canvas, Root):

        #make the pointer permanent
        self.Canvas = Canvas

        #inject dependencies
        self.Canvas.Title = self

        #default variables
        self.Align      = CENTER
        self.TitleStr   = StringVar()
        self.TitleStr.set('No Tilte Set')

        #create frame and label and associated adjustements
        self.TitleFrame = Frame(Root)
        self.TitleLabel = Label(self.TitleFrame,
                                textvariable    = self.TitleStr,
                                justify = self.Align)

        #set the label
        self.TitleLabel.grid(row = 0, column = 0, sticky = E+W)
        self.TitleFrame.grid_columnconfigure(0, weight = 1)

    def SetTitle(self,text = ''):
        
        '''
        ######################################################
        This is a method to set the title with the given text
        
        
        
        ######################################################
        '''

        self.TitleStr.set(text)


