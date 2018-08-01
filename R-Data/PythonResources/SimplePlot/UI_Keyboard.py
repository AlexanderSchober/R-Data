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

########################################
########################################
#import the modules


from UI_Interaction import Key as Key

class Keyboard:
    '''
    ######################################################
    We try to merge general listeners and to this purpose
    there will be only one keyboard lsistener in the 
    entire PLotcanavas class. Note that this listener
    will the call a list depending on the key and the
    ID
    
    types are:
    
    KeyPress
    KeyRelease
    ButtonPress
    ButtonRelease
    ######################################################
    '''
    def __init__(self, Canvas, Multi = None):

        #make the local reference
        self.Canvas     = Canvas
        self.Multi      = Multi
        self.Verbose    = False
        self.Present    = False
        
        #grab the Key class
        self.Key        = Key(self.Canvas, self)
    
        #Create Button List a list
        self.ButtonPressList     = []
        self.ButtonReleaseList   = []
        
        #create key list
        self.KeyPressList   = []
        self.KeyReleasList  = []
    
    def Bind(self, Type, key, Method):
    
        '''
        ######################################################
        This will manage the lists and add elments
        
        
        ######################################################
        '''
    
        if Type == 'KeyPress':
    
            self.KeyPressList.append([key,Method])

        if Type == 'KeyRelease':
    
            self.KeyReleasList.append([key,Method])

        if Type == 'ButtonPress':
    
            self.ButtonPressList.append([key,Method])

        if Type == 'ButtonRelease':
    
            self.ButtonReleaseList.append([key,Method])

    def Unbind(self,Type,value = ''):
    
        '''
        ######################################################
        This class makes sure that the mouse buttons are also
        considered as keys.... They will be called
        ######################################################
        '''
        if Type == 'KeyPress':
    
            for i in range(0,len(self.KeyPressList)):
        
                if self.KeyPressList[i][0] == value:
    
                    del self.KeyPressList[i]
                    break
        

        if Type == 'KeyRelease':
    
            for i in range(0,len(self.KeyReleasList)):
        
                if self.KeyReleasList[i][0] == value:
    
                    del self.KeyReleasList[i]
                    break

        if Type == 'ButtonPress':
    
            for i in range(0,len(self.ButtonPressList)):
        
                if self.ButtonPressList[i][0] == value:
    
                    del self.ButtonPressList[i]
                    break

        if Type == 'ButtonRelease':
    
            for i in range(0,len(self.ButtonReleaseList)):
        
                if self.ButtonReleaseList[i][0] == value:
    
                    del self.ButtonReleaseList[i]
                    break

    def KeyHandler(self,Type,value = ''):
    
        '''
        ######################################################
        This class makes sure that the mouse buttons are also
        considered as keys.... They will be called
        ######################################################
        '''
        if Type == 'KeyPress':
    
            for i in range(0,len(self.KeyPressList)):
        
                if self.KeyPressList[i][0] == value:
    
                    self.KeyPressList[i][1]()
        
            #This is special and should not be changed
            #it is the way to prompt the setting window
            if not self.Multi == None:
    
                if value == 'p':
        
                    self.Multi.SettingsClass.Creator()
        
        if Type == 'KeyRelease':
    
            for i in range(0,len(self.KeyReleasList)):
        
                if self.KeyReleasList[i][0] == value:
    
                    self.KeyReleasList[i][1]()

        if Type == 'ButtonPress':
    
            for i in range(0,len(self.ButtonPressList)):
        
                if self.ButtonPressList[i][0] == value:
    
                    self.ButtonPressList[i][1]()

        if Type == 'ButtonRelease':
    
            for i in range(0,len(self.ButtonReleaseList)):
        
                if self.ButtonReleaseList[i][0] == value:
    
                    self.ButtonReleaseList[i][1]()

