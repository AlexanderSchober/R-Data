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




class Key:

    '''
    ######################################################
    This class makes sure that the mouse buttons are also
    considered as keys.... They will be called 
    
    B1, B2, B3
    ######################################################
    '''

    def __init__(self, Canvas, Handler):

        #make the local reference
        self.Canvas  = Canvas
        self.Handler = Handler
        self.Verbose = False
        self.Present = False
    
        #link the listener
        self.KeyPressListener()
        self.KeyReleaseListener()
    

    def KeyPressListener(self):

        '''
        ######################################################
        Handle the events
        ######################################################
        '''
        
        self.Canvas.bind('<KeyPress>', self.KeyPressHandler,'+')
    
        self.BoundMethod_2 = self.Canvas.bind('<Enter>', self.Enter, "+"    )
        self.BoundMethod_3 = self.Canvas.bind('<Leave>', self.Exit , "+"    )


    def KeyPressHandler(self,event):

        if self.Verbose:
            print 'Pressed Key: ',event.char

        self.Handler.KeyHandler('KeyPress',value = event.char)

    

    def KeyReleaseListener(self):
        '''
        ######################################################
        Handle the events
        ######################################################
        '''
    
        self.Canvas.bind('<KeyRelease>', self.keyReleaseHandler,'+')

    def keyReleaseHandler(self,event):
        
        if self.Verbose:
            print 'Released Key: ',event.char

        if self.Present:
            self.Handler.KeyHandler('KeyRelease',value = event.char)

    def Enter(self,event):
        '''
        ######################################################
        Enter the canvas
        ######################################################
        '''
        if self.Verbose:
            print 'Entered the canvas'

        #notify the systeme
        self.Present = True
    
    def Exit(self,event):
        '''
        ######################################################
        Exit the canvas
        ######################################################
        '''
        if self.Verbose:
            print 'Left the canvas'

        #notify the systeme
        self.Present = True

class Mouse:
    
    '''
    ######################################################
    The Mouse class is a way of unifying the mouse
    poisition management. It will contain the references
    to the axes class as the padding variables are needed
    It will also contain the reference to the canvas
    for the canvas size parameters
    ######################################################
    '''
    
    def __init__(self, Canvas):

        #make the local reference
        self.Canvas = Canvas
        self.Verbose = False
        self.Present = False
        
        #Bound mouse method list
        self.BoundMethods_0 = []
        self.BoundMethods_1 = []
        
        #the lsit of mouses to comunicate to
        self.LinkList = []
    
        #bindMouse
        self.BindMouse()
    
        #initalise
        self.Cursor_x = 0
        self.Cursor_y = 0

    def BindMouse(self):
        '''
        ######################################################
        Simple binding method
        ######################################################
        '''
        
        #check if the pointer is live
        try:
            self.UnbindMouse()
        except:
            pass
    
        
        #bind the methods
        self.BoundMethod_0 = self.Canvas.bind('<Motion>',       self.Move_0, "+"    )
        self.BoundMethod_1 = self.Canvas.bind('<B1-Motion>',    self.Move_1, "+"    )

        self.BoundMethod_2 = self.Canvas.bind('<Enter>', self.Enter, "+"    )
        self.BoundMethod_3 = self.Canvas.bind('<Leave>', self.Exit , "+"    )

    def Enter(self,event):
        '''
        ######################################################
        Enter the canvas
        ######################################################
        '''
        if self.Verbose:
            print 'Entered the canvas'
        
        #this allows the canvas to be focus on mouse enter
        self.Canvas.focus_set()
        
        #notify the systeme
        self.Present = True
    
    def Exit(self,event):
        '''
        ######################################################
        Exit the canvas
        ######################################################
        '''
        if self.Verbose:
            print 'Left the canvas'

        #notify the systeme
        self.Present = True
    
    def UnbindMouse(self):
        '''
        ######################################################
        Simple unbinding method
        
        could be to lock the cursor in a certain position
        ######################################################
        '''
    
        #kill all the listeners
        self.Canvas.unbind('<Motion>',      self.BoundMethod_0  )
        self.Canvas.unbind('<B1-Motion>',   self.BoundMethod_1  )
    
    def Bind(self,Type, Method, IdStr):
        '''
        ######################################################
        Binding methods
        
        The IDStr variable can then be used to find the 
        method to remove from the list
        ######################################################
        '''
        #normal mouse move
        if Type == '<Motion>':
            self.BoundMethods_0.append([Method, IdStr])

        #B1 mouse move
        if Type == '<B1-Motion>':
            self.BoundMethods_1.append([Method, IdStr])

    def Unbind(self,Type,IdStr):
        '''
        ######################################################
        Unbiniding the method with the IdSr associated
        ######################################################
        '''
    
        #normal mouse move
        if Type == '<Motion>':
            
            #find the string
            for i in range(0,len(self.BoundMethods_0)):
                
                if self.BoundMethods_0[i][1] == IdStr:
                
                    del self.BoundMethods_0[i]
                    break
        

        #B1 mouse move
        if Type == '<B1-Motion>':

            #find the string
            for i in range(0,len(self.BoundMethods_1)):
                
                if self.BoundMethods_1[i][1] == IdStr:
                
                    del self.BoundMethods_1[i]
                    break
    
    def Move_0(self,event):
        '''
        ######################################################
        This will keep the local cursor method fresh
        ######################################################
        '''
        
        #grab
        self.x = event.x
        self.y = event.y
        
        #run the transmit to othersubplots
        self.Transmit()
        
        #evaluate
        self.Evaluate(0)
    
    def Move_1(self,event):
        '''
        ######################################################
        This will keep the local cursor method fresh
        ######################################################
        '''
        
        #grab
        self.x = event.x
        self.y = event.y
        
        #evaluate
        self.Evaluate(1)
        
    def Evaluate(self,Type):
    
        if self.Present:
            #run it
            try:
                self.MousePosition()
            except:
                pass
            
            if Type == 0:
            
                #run the bound methods
                for i in range(0,len(self.BoundMethods_0)):
        
                    self.BoundMethods_0[i][0](self.Cursor_x,self.Cursor_y)

            if Type == 1:
            
                #run the bound methods
                for i in range(0,len(self.BoundMethods_1)):
        
                    self.BoundMethods_1[i][0](self.Cursor_x,self.Cursor_y)
    
    def MousePosition(self):
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
        self.Cursor_x = (self.Canvas.Drawer.BoundingBoxOffset[2]-self.Canvas.Drawer.BoundingBoxOffset[0])*((float(self.x)-float(self.DrawTopX))/float(self.DrawWidth))+self.Canvas.Drawer.BoundingBoxOffset[0]

        self.Cursor_y = (self.Canvas.Drawer.BoundingBoxOffset[1]-self.Canvas.Drawer.BoundingBoxOffset[3])*((float(self.y)-float(self.DrawTopY))/float(self.DrawHeight))+self.Canvas.Drawer.BoundingBoxOffset[3]
        
        #for debugging puproses
        if self.Verbose:
            
            #print the coordinates
            print 'These are the actual coordinates: ',self.Cursor_x,self.Cursor_y


    def PixelPosition(self):

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
        self.x = ((self.Cursor_x-self.Canvas.Drawer.BoundingBoxOffset[0])/(self.Canvas.Drawer.BoundingBoxOffset[2]-self.Canvas.Drawer.BoundingBoxOffset[0]))*float(self.DrawWidth)+float(self.DrawTopX)

        self.y = ((self.Cursor_y-self.Canvas.Drawer.BoundingBoxOffset[3])/(self.Canvas.Drawer.BoundingBoxOffset[1]-self.Canvas.Drawer.BoundingBoxOffset[3]))*float(self.DrawHeight)+float(self.DrawTopY)
        
        #for debugging puproses
        if self.Verbose:
            
            #print the coordinates
            print 'These are the actual coordinates: ',self.Cursor_x,self.Cursor_y

    def Transmit(self):
        
        '''
        ######################################################
        This Method is to comunicate to different mouse
        instances to allow for linkage
        ######################################################
        '''
        
        #pass it onto the elements of the list
        #[ID, Source , variable Type, Target, Method]
        for i in range(0,len(self.LinkList)):
        
            if self.LinkList[i][2] == 'x':
        
                if self.LinkList[i][3] == 'x':
                
                    self.LinkList[i][4].Cursor_x = numpy.copy(self.Cursor_x)
                    
                if self.LinkList[i][3] == 'y':
                
                    self.LinkList[i][4].Cursor_y = numpy.copy(self.Cursor_x)
        
            if self.LinkList[i][2] == 'y':
        
                if self.LinkList[i][3] == 'x':
                
                    self.LinkList[i][4].Cursor_x = numpy.copy(self.Cursor_y)
                    
                if self.LinkList[i][3] == 'y':
                
                    self.LinkList[i][4].Cursor_y = numpy.copy(self.Cursor_y)
    
            #reverse engeneer
            self.LinkList[i][5].PixelPosition()
            
            #process the method
            self.LinkList[i][5].Evaluate(0)
    
        #if verbose
        if self.Verbose:
            print 'These are the raw pixel positions', self.x, self.y
