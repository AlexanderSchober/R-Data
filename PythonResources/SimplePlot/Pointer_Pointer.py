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

class Pointer:

    '''
    ######################################################
    This class will manage the pointer behaviour. Note 
    that it will only bin and unbind on request. This 
    method should be exited to reach the desired
    bhaviour
    
    - if sticky is 0 the cursor is free
    - if sticky is 1 the cursor follows the closest line
    - if sticky is 2 the cursor sticks to points
    ######################################################
    '''

    def __init__(self, Canvas):

        ##################################################
        #Bind to the canvas.
        self.Canvas = Canvas
        
        ##################################################
        #for debugging
        self.Verbose = False
        self.Initialise = False
        self.SetInitial()
        
    def SetInitial(self):
        '''
        ######################################################
        This class allows to dicretly manage the initialisation
        and for further manipulations if the user wnats a reset
        ######################################################
        '''
        self.Live    = False
        self.Locked  = False
        self.Projections = [None, None]
        self.Method = None
    
        ##################################################
        #cursor parameters
        self.Color       = 'black'
        self.Thickness   = 2
        self.Rounding    = 1
        
        ##################################################
        #sticky parameter
        # 0 no stickyness
        # 1 stickyness along Y
        # 2 stickyness along X and Y
        #should be changed by the user as desired
        
        #Type 0 the crosshair goes thorugh
        #Type 1 the Crosshair consists of a small cross and edges
        #Type 2 the crosshair consists of a small cross and circle
        # can be toggled with 'c'
        
        self.Sticky     = 0
        self.Type       = 1
        self.Size       = [20,20]
        
        ##################################################
        #defaults:
        self.x = 0
        self.y = 0
        
        #initialise
        self.Cursor_x = 0.0
        self.Cursor_y = 0.0
        
        
        ##################################################
        #Do we want labels? Types:
        # 0 the Labels will be in on the out padding
        # 1 The lables will be in on the inside
        # 2 The labels will be around the crosshair
        #can be toggled with 'l'
        
        self.Labels                 = True
        self.LabelType              = 1
        self.LabelPositions         = [False,False,True,True]
        self.LabelTicks             = [False,False,True,True]
        self.LabelTicksThickness    = 5
        self.LabelTicksColor        = 'blue'
        self.LabelTicksOffset       = 5
        self.LabelColor             = 'black'
        
        
        #Windows fonts have to be rescaled smaller
        if os.name == 'nt':
        
            self.FontSize               = ('Helvetica', '9')
        
        else:
        
            self.FontSize               = ('Helvetica', '11')
        
        self.isXSci                 = False
        self.isYSci                 = False
        self.XSciPrecision          = '%.1e'
        self.YSciPrecision          = '%.1e'
    
        ##################################################
        #Tgis serves cursor linking to allow the program
        #to send information to another canvas
        #each element will be
        # - Method
        # - Type, x, y , z
        self.LinkList               = []
    
    def BindCursor(self, Init = True):
        '''
        ######################################################
        Simple binding method
        ######################################################
        '''
        #link the Recalculate methode to the mouse
        self.Canvas.Drawer.Mouse.Bind('<Motion>',self.Recalculate,'Pointer')
        self.Canvas.Drawer.Keyboard.Bind('KeyPress','c',self.CycleCursor)
        self.Canvas.Drawer.Keyboard.Bind('KeyPress','t',self.CycleLabel)
        self.Canvas.Drawer.Keyboard.Bind('KeyPress','l',self.LockCursor)
        self.Canvas.Drawer.Keyboard.Bind('KeyPress','r',self.ToggleCursor)
        
        #initialise the local drawing method
        self.DrawCursor(live = False)
        
        #call thelocal drawing method once
        self.DrawCursor(live = True)
    
    def BindMethod(self,Method):
        '''
        ######################################################
        This allows to link and external function to the
        pointer that will call the method with the function...
        ######################################################
        '''
        #link the Recalculate methode to the mouse
        self.Method = Method
    
    def UnbindCursor(self):
        '''
        ######################################################
        Simple unbinding method
        
        could be to lock the cursor in a certain position
        ######################################################
        '''
    
        self.Canvas.Drawer.Mouse.Unbind('<Motion>','Pointer')
        self.Canvas.Drawer.Keyboard.Unbind('KeyPress','c')
        self.Canvas.Drawer.Keyboard.Unbind('KeyPress','t')
        self.Canvas.Drawer.Keyboard.Unbind('KeyPress','l')
        self.Canvas.Drawer.Keyboard.Unbind('KeyPress','r')
    
    def LockCursor(self):
        '''
        ######################################################
        Changes the locked parameter and inverts it accordin
        gly. NOte that this just keeps the cutrsor from moving
        ######################################################
        '''
        
        if self.Locked:
            self.Locked = False

        else:
            self.Locked = True

    def ToggleCursor(self):
        '''
        ######################################################
        Toggles cursor on or off
        ######################################################
        '''
    
        if self.Live:
    
            self.DeleteCursor()

        else:
    
            #initialise the local drawing method
            self.DrawCursor(live = False)
        
            #call thelocal drawing method once
            self.DrawCursor(live = True)

            self.Live = True
            
    def DeleteCursor(self):
        '''
        ######################################################
        Simple method to delete the elements the cursor. 
        
        ######################################################
        '''
        
        try:
        
            self.Initialise = False
            
            for i in range(0,len(self.ElementList)):
        
                try:
                    self.Canvas.delete(self.ElementList[i])
                    self.Live = False
                
                except:
                    
                    if self.Verbose:
                        
                        print 'Could not delete cursor element',self.ElementList[i]

        except:
                    
            if self.Verbose:
                        
                    print 'Could not delete cursor at all, is it Drawn?'
        
    def CycleCursor(self):
        '''
        ######################################################
        Cursor type cycling mthod
        
        
        ######################################################
        '''
        
        self.Type += 1
        
        if self.Type > 3:
            self.Type = 0
    
        self.BindCursor()

    def CycleLabel(self):
        '''
        ######################################################
        Label type cycling method
        
        
        ######################################################
        '''
    
        self.LabelType += 1
        
        if self.LabelType > 2:
            self.LabelType = 0
        
    def Recalculate(self,X,Y):
        '''
        ######################################################
        Combines two methods to be ued with variable transfer
        through subplots
        ######################################################
        '''
        
        #grab the position
        if not self.Locked:
            self.Cursor_x = numpy.copy(X)
            self.Cursor_y = numpy.copy(Y)
        
        if self.Live:
            #call the local drawing method
            self.DrawCursor(live = True)

    def find_nearestY(self, X, Y):
        
        '''
        ##########################################################################################
        This method aims at searching sucessively for the nearest value in all plots by first
        scanning the nearest X. Then e find the second nearest to zero after X-Nearest. This 
        will give us back two point ids which whome we can calculate the nearest Y
        ##########################################################################################
        '''
        
        List = []
        
        #combine the two lists
        ElementList = list(self.Canvas.Drawer.Plots)
        ElementList.extend(self.Canvas.Drawer.iPlots)
        
        #first grab closest Id to the researched value
        for i in range(0,len(ElementList)):
        
        
            #search the first closest
            idx_0 = (numpy.abs(numpy.asarray(ElementList[i].X) - X)).argmin()
        
            #search the second closest (obviously our value will be in between)
            
            try:
                if ElementList[i].X[idx_0] <= X:
                    
                    #check for the array direction
                    if ElementList[i].X[idx_0]<ElementList[i].X[idx_0+1]:
                        
                        idx_1 = idx_0+1
            
                    else:
                        
                        idx_1 = idx_0-1
                else:
                    
                    #check for the array direction
                    if ElementList[i].X[idx_0]<ElementList[i].X[idx_0+1]:

                        idx_0 -= 1
                    
                        idx_1  = idx_0+1

                    else:
                        
                        idx_0 += 1
                    
                        idx_1  = idx_0-1

        
                #calclate the Y from these positions
                List.append(float(ElementList[i].Y[idx_0])+float((X-ElementList[i].X[idx_0]))*
                            (float(ElementList[i].Y[idx_1])-float(ElementList[i].Y[idx_0]))/
                            (float(ElementList[i].X[idx_1])-float(ElementList[i].X[idx_0])))
            except:
                List.append(numpy.inf)
    
        if self.Verbose:
            
            print List
        
        if not len(List) == 0:
            
            #grab the second one
            idx_2 = (numpy.abs(numpy.asarray(List)-Y)).argmin()
        
            if not self.Method == None:
            
                self.Method(idx_2, [X,Y])
        
            Out = List[idx_2]
        
        else:
            Out = 0
            idx_2 = 0
        
        return X,Out,idx_2

    def find_nearestX(self, X, Y):
        
        '''
        ##########################################################################################
        This method aims at searching sucessively for the nearest value in all plots by first
        scanning the nearest X. Then e find the second nearest to zero after X-Nearest. This 
        will give us back two point ids which whome we can calculate the nearest Y
        
        Offset has to be integers
        ##########################################################################################
        '''
        
        List = []
        
        #combine the two lists
        ElementList = list(self.Canvas.Drawer.Plots)
        ElementList.extend(self.Canvas.Drawer.iPlots)
        
        #first grab closest Id to the researched value
        for i in range(0,len(ElementList)):
        
        
            #search the first closest
            idx_0 = (numpy.abs(numpy.asarray(ElementList[i].Y) - Y)).argmin()
        
            #search the second closest (obviously our value will be in between)
            try:
                if ElementList[i].Y[idx_0] <= Y:
                    idx_1 = idx_0+1
                else:
                    idx_1 = idx_0-1
        
                #calclate the Y from these positions
                List.append(float(ElementList[i].X[idx_0])+float((Y-ElementList[i].Y[idx_0]))*
                            (float(ElementList[i].X[idx_1])-float(ElementList[i].X[idx_0]))/
                            (float(ElementList[i].Y[idx_1])-float(ElementList[i].Y[idx_0])))
            except:
                List.append(numpy.inf)
    
        if self.Verbose:
            print List
        
        idx_2 = (numpy.abs(numpy.asarray(List)-X)).argmin()
        
        if not self.Method == None:
        
            self.Method(idx_2, [X,Y])
    
        return List[idx_2],Y,idx_2

    def find_nearestXY(self, X, Y, OffsetX = 0, OffsetY = 0):
        
        '''
        ##########################################################################################
        This method aims at searching sucessively for the nearest value in all plots by first
        scanning the nearest X. Then e find the second nearest to zero after X-Nearest. This 
        will give us back two point ids which whome we can calculate the nearest Y
        
        This version will pin it to the closest point also. This is particulary helpful when
        dealing with scatter plots
        
        Note that this version also sends out the function so the point editor can do it's work...
        ##########################################################################################
        '''
        ########################
        #initialise
        List = []
        idx_0 = []
        
        ########################
        #combine the two lists
        ElementList = list(self.Canvas.Drawer.Plots)
        ElementList.extend(self.Canvas.Drawer.iPlots)
        
        ########################
        #first grab closest Id to the researched value
        for i in range(0,len(ElementList)):
        
        
            #search the first closest
            idx_0.append((numpy.abs(numpy.asarray(ElementList[i].X) - X)).argmin())
        
            #calclate the Y from these positions
            try:
                
                if idx_0[-1] + OffsetX > len(ElementList[i].X)-1 or idx_0[-1] + OffsetX < 0:
                
                    List.append(float(ElementList[i].Y[idx_0[-1]]))
                
                else:
                
                    List.append(float(ElementList[i].Y[idx_0[-1] + OffsetX]))
            except:
                
                List.append(numpy.inf)
        
        idx_2 = (numpy.abs(numpy.asarray(List)-Y)).argmin()
        
        if not self.Method == None:
        
            self.Method(idx_2, [X,Y])
    
        ########################
        #prepare the send out method
        if idx_2 > len(self.Canvas.Drawer.Plots)-1:
            
            if self.Verbose:
            
                print 'This is the length: ',len(self.Canvas.Drawer.Plots)
                print 'This is the length: ',len(self.Canvas.Drawer.iPlots)
                print 'this is the indice: ', idx_0 - len(self.Canvas.Drawer.Plots)
        
            #set the curve
            Curve = self.Canvas.Drawer.iPlots[idx_2 - len(self.Canvas.Drawer.Plots)]
        
        else:
        
            Curve = None
    
        ########################
        #expulsion conditions

        if self.Verbose:
            print 'This is idx_2: ',idx_2,idx_0[idx_2]
            print List
            print ElementList[idx_2 + OffsetY].X[idx_0[idx_2]]
            print List[idx_2+ OffsetY]
        
        if idx_0[idx_2] + OffsetX > len(ElementList[idx_2 + OffsetY].X)-1 or idx_0[idx_2] + OffsetX <0:
        
            return ElementList[idx_2 + OffsetY].X[idx_0[idx_2]],List[idx_2+ OffsetY],idx_0[idx_2],Curve

        else:
            return ElementList[idx_2 + OffsetY].X[idx_0[idx_2] + OffsetX],List[idx_2+ OffsetY],idx_0[idx_2],Curve

    def find_nearestXYContour(self, X, Y):
        
        '''
        ##########################################################################################
        This tries to find the closest X and Y of the a the first contour plots...
        Multiple contours are not supporte yet abd frankly don't make to much sense therefore we
        will simply grab contour [0]
        ##########################################################################################
        '''

        if not self.Initialise:
            
            try:
            
                #set variable
                self.Target = self.Canvas.Drawer.Contours[0]
                
                #set variable
                self.Target_X = numpy.asarray([self.Target.X[i][0] for i in range(0, len(self.Target.X))])
                self.Target_Y = numpy.asarray(self.Target.Y[0])
            
                #set variable
                self.Initialise = True
                
            except:
                print 'Could not intialise'
                return 0,0
                    
        #grab the X closest value index
        idx_0 = (numpy.abs(self.Target_X - X)).argmin()

        #grab the Y closest value index
        idx_1 = (numpy.abs(self.Target_Y - Y)).argmin()
        
        #fetch the new datat for the projection if necessary
        if not self.Projections[0] == None:
        
            #fetch
            self.Projections[0][0].FetchNewData(idx_1)
            
            #redraw
            self.Projections[0][1].Zoom_Projection()
        
        #fetch the new datat for the projection if necessary
        if not self.Projections[1] == None:
            
            self.Projections[1][0].FetchNewData(idx_0)
            
            #redraw
            self.Projections[1][1].Zoom_Projection()
        
        return self.Target_X[idx_0],self.Target_Y[idx_1]

    def find_nearestXCascade(self, X, Y):
        
        '''
        ##########################################################################################
        This tries to find the closest X and Y of the a the first contour plots...
        Multiple contours are not supporte yet abd frankly don't make to much sense therefore we
        will simply grab contour [0]
        ##########################################################################################
        '''

        if not self.Initialise:
            
            try:
            
                #set variable
                self.Target = self.Canvas.Drawer.Cascades[0]
                
                #set variable
                self.Target_X = numpy.asarray(self.Target.X[0])
                self.Target_Z = numpy.asarray(self.Target.Z)
            
                #set variable
                self.Initialise = True
                
            except:
                print 'Could not intialise'
                return 0,0
                    
        List = []
    
        #search the first closest
        idx_0 = (numpy.abs(self.Target_X- X)).argmin()
    
        #search the second closest (obviously our value will be in between)
        for i in range(0,len(self.Target.Z)):
            
            try:
                if self.Canvas.Drawer.Plots[i].X[idx_0] <= X:
                    
                    #check for the array direction
                    if self.Canvas.Drawer.Plots[i].X[idx_0]<self.Canvas.Drawer.Plots[i].X[idx_0+1]:
                        
                        idx_1 = idx_0+1
            
                    else:
                        
                        idx_1 = idx_0-1
                else:
                    
                    #check for the array direction
                    if self.Canvas.Drawer.Plots[i].X[idx_0]<self.Canvas.Drawer.Plots[i].X[idx_0+1]:

                        idx_0 -= 1
                    
                        idx_1  = idx_0+1

                    else:
                        
                        idx_0 += 1
                    
                        idx_1  = idx_0-1

        
                #calclate the Y from these positions
                List.append(float(self.Canvas.Drawer.Plots[i].Y[idx_0])+float((X-self.Canvas.Drawer.Plots[i].X[idx_0]))*
                            (float(self.Canvas.Drawer.Plots[i].Y[idx_1])-float(self.Canvas.Drawer.Plots[i].Y[idx_0]))/
                            (float(self.Canvas.Drawer.Plots[i].X[idx_1])-float(self.Canvas.Drawer.Plots[i].X[idx_0])))
            except:
                List.append(numpy.inf)
    
        if self.Verbose:
            print List
        
        idx_2 = (numpy.abs(List-Y)).argmin()
    
        if not self.Method == None:
        
            self.Method(idx_2, [X,Y])
        
        return X,List[idx_2],idx_2
        
    def Fetch(self,OffsetX, OffsetY):
        
        '''
        ######################################################
        This fucntion was writen for the interaction routines
        It should give back the position of a point with
        offset...
        ######################################################
        '''
     
        return self.find_nearestXY(self.Cursor_x,
                                       self.Cursor_y,
                                       OffsetX,
                                       OffsetY )
    
    


    def DrawCursor(self,live = False):
        
        '''
        ######################################################
        Draw or update the cursor
        
        
        - if the cursor is not live he will draw and center
            it. This will result in a cursor initialization
        - if the cursor is live it will redraw it and change
            the coordinatrs.
        ######################################################
        '''
        #initialise X and Y
        X = [None]*8
        Y = [None]*8
        
        if not live:
            
            
            
            #create a list of elements
            self.ElementList = []

            ########################################################
            #Normal cursor lines that go through
            
            if self.Type == 0:

                #the horizontal cursor lines
                self.CursorX =  self.Canvas.create_line(self.Canvas.Drawer.Axes.PaddingOut[0]*self.Canvas.Drawer.wScaleFactor,
                                                       0.5*self.Canvas.Drawer.hScaleFactor,
                                                       (1-self.Canvas.Drawer.Axes.PaddingOut[0])*self.Canvas.Drawer.wScaleFactor,
                                                       0.5*self.Canvas.Drawer.hScaleFactor,
                                                       fill  = self.Color,
                                                       width = self.Thickness,
                                                       tag = 'TopTop')
                                
                #append
                self.ElementList.append(self.CursorX)
                
                #the vertical cursor lines
                self.CursorY = self.Canvas.create_line(0.5*self.Canvas.Drawer.wScaleFactor,
                                                       (self.Canvas.Drawer.Axes.PaddingOut[1])*self.Canvas.Drawer.hScaleFactor,
                                                       0.5*self.Canvas.Drawer.wScaleFactor,
                                                       (1.0-self.Canvas.Drawer.Axes.PaddingOut[1])*self.Canvas.Drawer.hScaleFactor,
                                                       fill  = self.Color,
                                                       width = self.Thickness,
                                                       tag = 'TopTop')
            
                #append
                self.ElementList.append(self.CursorY)
            
            
            ########################################################
            #Normal cursor cross only
            
            elif self.Type == 1:
                
                #the horizontal cursor lines
                self.CursorX =  self.Canvas.create_line((0.5-self.Size[0])*self.Canvas.Drawer.wScaleFactor,
                                                        0.5*self.Canvas.Drawer.hScaleFactor,
                                                        (0.5+self.Size[0])*self.Canvas.Drawer.wScaleFactor,
                                                        0.5*self.Canvas.Drawer.hScaleFactor,
                                                        fill  = self.Color,
                                                        width = self.Thickness,
                                                        tag = 'TopTop')
                                                        
                #append
                self.ElementList.append(self.CursorX)
                
                #the vertical cursor lines
                self.CursorY = self.Canvas.create_line(0.5*self.Canvas.Drawer.wScaleFactor,
                                                       (0.5-self.Size[1])*self.Canvas.Drawer.wScaleFactor,
                                                       0.5*self.Canvas.Drawer.wScaleFactor,
                                                       (0.5-self.Size[1])*self.Canvas.Drawer.wScaleFactor,
                                                       fill  = self.Color,
                                                       width = self.Thickness,
                                                       tag = 'TopTop')
            
                #append
                self.ElementList.append(self.CursorY)
        
            ########################################################
            #X shaped cursor cross only
            elif self.Type == 2:
                
                #the horizontal cursor lines
                self.CursorX =  self.Canvas.create_line(self.Canvas.Drawer.Axes.PaddingOut[0]*self.Canvas.Drawer.wScaleFactor,
                                                       0.5*self.Canvas.Drawer.hScaleFactor,
                                                       (1-self.Canvas.Drawer.Axes.PaddingOut[0])*self.Canvas.Drawer.wScaleFactor,
                                                       0.5*self.Canvas.Drawer.hScaleFactor,
                                                       fill  = self.Color,
                                                       width = self.Thickness,
                                                       tag = 'TopTop')
                                                       
                #append
                self.ElementList.append(self.CursorX)
                
                #the vertical cursor lines
                self.CursorY = self.Canvas.create_line(0.5*self.Canvas.Drawer.wScaleFactor,
                                                       (self.Canvas.Drawer.Axes.PaddingOut[1])*self.Canvas.Drawer.hScaleFactor,
                                                       0.5*self.Canvas.Drawer.wScaleFactor,
                                                       (1.0-self.Canvas.Drawer.Axes.PaddingOut[1])*self.Canvas.Drawer.hScaleFactor,
                                                       fill  = self.Color,
                                                       width = self.Thickness,
                                                       tag = 'TopTop')
            
                #append
                self.ElementList.append(self.CursorY)
            
            ########################################################
            #X shaped cursor cross only
            elif self.Type == 3:
                
                #the horizontal cursor lines
                self.CursorXY_0 = self.Canvas.create_line(self.Canvas.Drawer.Axes.PaddingOut[0]*self.Canvas.Drawer.wScaleFactor,
                                                          self.Canvas.Drawer.Axes.PaddingOut[1]*self.Canvas.Drawer.hScaleFactor,
                                                          0.5*self.Canvas.Drawer.wScaleFactor,
                                                          0.5*self.Canvas.Drawer.hScaleFactor,
                                                          fill  = self.Color,
                                                          width = self.Thickness,
                                                          tag = 'TopTop')
                                                       
                #append
                self.ElementList.append(self.CursorXY_0)
                
                #the vertical cursor lines
                self.CursorXY_1 = self.Canvas.create_line(self.Canvas.Drawer.Axes.PaddingOut[0]*self.Canvas.Drawer.wScaleFactor,
                                                          (1-self.Canvas.Drawer.Axes.PaddingOut[1])*self.Canvas.Drawer.hScaleFactor,
                                                          0.5*self.Canvas.Drawer.wScaleFactor,
                                                          0.5*self.Canvas.Drawer.hScaleFactor,
                                                          fill  = self.Color,
                                                          width = self.Thickness,
                                                          tag = 'TopTop')
            
                #append
                self.ElementList.append(self.CursorXY_1)
                    
                #the horizontal cursor lines
                self.CursorXY_2 = self.Canvas.create_line((1-self.Canvas.Drawer.Axes.PaddingOut[0])*self.Canvas.Drawer.wScaleFactor,
                                                          (1-self.Canvas.Drawer.Axes.PaddingOut[1])*self.Canvas.Drawer.hScaleFactor,
                                                          0.5*self.Canvas.Drawer.wScaleFactor,
                                                          0.5*self.Canvas.Drawer.hScaleFactor,
                                                          fill  = self.Color,
                                                          width = self.Thickness,
                                                          tag = 'TopTop')
                                                       
                #append
                self.ElementList.append(self.CursorXY_2)
                
                #the vertical cursor lines
                self.CursorXY_3 = self.Canvas.create_line((1-self.Canvas.Drawer.Axes.PaddingOut[0])*self.Canvas.Drawer.wScaleFactor,
                                                          self.Canvas.Drawer.Axes.PaddingOut[1]*self.Canvas.Drawer.hScaleFactor,
                                                          0.5*self.Canvas.Drawer.wScaleFactor,
                                                          0.5*self.Canvas.Drawer.hScaleFactor,
                                                          fill  = self.Color,
                                                          width = self.Thickness,
                                                          tag = 'TopTop')
            
                #append
                self.ElementList.append(self.CursorXY_3)
            
                #add the rectangle...
                self.CursorBox = self.Canvas.create_rectangle(0.5*self.Canvas.Drawer.wScaleFactor-self.Size[0],
                                                              0.5*self.Canvas.Drawer.hScaleFactor-self.Size[1],
                                                              0.5*self.Canvas.Drawer.wScaleFactor+self.Size[0],
                                                              0.5*self.Canvas.Drawer.hScaleFactor+self.Size[1],
                                                              width     = self.Thickness,
                                                              outline   = self.Color,
                                                              tag       = 'Top')
            
                #append
                self.ElementList.append(self.CursorBox)
                
            
            ########################################################
            #the cursor labels
            
            ############################
            #left
            if self.LabelPositions[0]:
                self.LeftPointerLabel = self.Canvas.create_text(#X
                                                                (self.Canvas.Drawer.Axes.PaddingOut[0]
                                                                 -self.Canvas.Drawer.Axes.YLabelOffset[0])
                                                                *self.Canvas.Drawer.wScaleFactor,
                                                                
                                                                #Y
                                                                0.5*self.Canvas.Drawer.wScaleFactor,
                                                                
                                                                #Options
                                                                fill  = self.LabelColor,
                                                                font  = self.FontSize,
                                                                text  = str(round(0.5,self.Rounding)),
                                                                tag   = 'TopTop')
            
                #append
                self.ElementList.append(self.LeftPointerLabel)
            
            #Do we add a Tick
            if self.LabelTicks[0]:
            
                self.LeftPointerTick = self.Canvas.create_line(#X_0
                                                               0,
                                                               
                                                               #Y_0
                                                               0,
                                                               
                                                               #X_1
                                                               1*self.Canvas.Drawer.wScaleFactor,
                                                               
                                                               #Y_1
                                                               1*self.Canvas.Drawer.hScaleFactor,
                                                               
                                                               #Options
                                                               fill  = self.LabelTicksColor,
                                                               width = self.LabelTicksThickness,
                                                               tag = 'TopTop')
            
                #append
                self.ElementList.append(self.LeftPointerTick)
            
            ############################
            #bot
            if self.LabelPositions[1]:
                self.BotPointerLabel = self.Canvas.create_text(#X
                                                               (0.5*self.Canvas.Drawer.wScaleFactor),
                                                               
                                                               #Y
                                                               (1-(self.Canvas.Drawer.Axes.PaddingOut[1]
                                                                    -self.Canvas.Drawer.Axes.XLabelOffset[0]))
                                                               *self.Canvas.Drawer.hScaleFactor,
                                                               
                                                               #Options
                                                               fill  = self.LabelColor,
                                                               font  = self.FontSize,
                                                               text  = str(round(0.5,self.Rounding)),
                                                               tag   = 'TopTop')
            
                #append
                self.ElementList.append(self.BotPointerLabel)
                    
            #Do we add a Tick
            if self.LabelTicks[1]:
            
                self.BotPointerTick = self.Canvas.create_line(#X_0
                                                               0,
                                                               
                                                               #Y_0
                                                               0,
                                                               
                                                               #X_1
                                                               1*self.Canvas.Drawer.wScaleFactor,
                                                               
                                                               #Y_1
                                                               1*self.Canvas.Drawer.hScaleFactor,
                                                               
                                                               #Options
                                                              fill  = self.LabelTicksColor,
                                                              width = self.LabelTicksThickness,
                                                              tag = 'TopTop')
            
                #append
                self.ElementList.append(self.BotPointerTick)
            
            ############################
            #Right
            if self.LabelPositions[2]:
                self.RightPointerLabel = self.Canvas.create_text(#X
                                                                 (1-(self.Canvas.Drawer.Axes.PaddingOut[0]
                                                                     -self.Canvas.Drawer.Axes.YLabelOffset[1]))
                                                                 *self.Canvas.Drawer.wScaleFactor,
                                                                 
                                                                 #Y
                                                                 0.5*self.Canvas.Drawer.wScaleFactor,
                                                                 
                                                                 #Options
                                                                 fill  = self.LabelColor,
                                                                 font  = self.FontSize,
                                                                 text  = str(round(0.5,self.Rounding)),
                                                                 tag   = 'TopTop')
            
                #append
                self.ElementList.append(self.RightPointerLabel)
            
            #Do we add a Tick
            if self.LabelTicks[2]:
            
                self.RightPointerTick = self.Canvas.create_line(#X_0
                                                               0,
                                                               
                                                               #Y_0
                                                               0,
                                                               
                                                               #X_1
                                                               1*self.Canvas.Drawer.wScaleFactor,
                                                               
                                                               #Y_1
                                                               1*self.Canvas.Drawer.hScaleFactor,
                                                               
                                                               #Options
                                                                fill  = self.LabelTicksColor,
                                                                width = self.LabelTicksThickness,
                                                                tag = 'TopTop')
            
                #append
                self.ElementList.append(self.RightPointerTick)
            
            ############################
            #Top
            if self.LabelPositions[3]:
                self.TopPointerLabel = self.Canvas.create_text(
                                                               #X
                                                               (0.5*self.Canvas.Drawer.wScaleFactor),
                                                                (self.Canvas.Drawer.Axes.PaddingOut[1]
                                                                 -self.Canvas.Drawer.Axes.XLabelOffset[1])
                                                               
                                                               #Y
                                                               *self.Canvas.Drawer.hScaleFactor,
                                                               
                                                               #Options
                                                               fill  = self.LabelColor,
                                                               font  = self.FontSize,
                                                               text  = str(round(0.5,self.Rounding)),
                                                               tag   = 'TopTop')
            
                #append
                self.ElementList.append(self.TopPointerLabel)
                    
            #Do we add a Tick
            if self.LabelTicks[3]:
            
                self.TopPointerTick = self.Canvas.create_line(#X_0
                                                               0,
                                                               
                                                               #Y_0
                                                               0,
                                                               
                                                               #X_1
                                                               1*self.Canvas.Drawer.wScaleFactor,
                                                               
                                                               #Y_1
                                                               1*self.Canvas.Drawer.hScaleFactor,
                                                               
                                                               #Options
                                                              fill  = self.LabelTicksColor,
                                                              width = self.LabelTicksThickness,
                                                              tag = 'TopTop')
                    
                #append
                self.ElementList.append(self.TopPointerTick)
                    
                    
            #Notify user that the cursor has been dranw
            self.Live = True
                                                           

        else:

            #check cursor bounding
            self.CorrectCursor()
            
            if self.Sticky == 0:
                
                #simple case we keep the current coordinates
                pass
            
            if self.Sticky == 1:
                
                #stick to the closest line including calculating position
                try:
                    self.Cursor_x, self.Cursor_y, ClosestID =  self.find_nearestY(self.Cursor_x,self.Cursor_y)
                except:
                    pass
        
            if self.Sticky == 2:
            
                #stick to the closest line including calculating position
                try:
                    self.Cursor_x, self.Cursor_y, ClosestID, Curve =  self.find_nearestXY(self.Cursor_x,self.Cursor_y)
                except:
                    pass
            
            if self.Sticky == 3:
            
                #stick to the closest line including calculating position
                try:
                    self.Cursor_x, self.Cursor_y, ClosestID =  self.find_nearestX(self.Cursor_x,self.Cursor_y)
                except:
                    pass
        
            if self.Sticky == 4:
                try:
                    #stick to the closest line including calculating position
                    self.Cursor_x, self.Cursor_y = self.find_nearestXYContour(self.Cursor_x,self.Cursor_y)
                except:
                     pass
            #check cursor bounding
            self.CorrectCursor()
            
            
            ########################################################
            #Normal cursor lines that go through
            
            if self.Type == 0:
                
                #change the coordinates of the lines
                X[0] = self.Canvas.Drawer.Axes.PaddingOut[0]*self.Canvas.Drawer.wScaleFactor         #fixed
                
                X[1] = (1-self.Canvas.Drawer.Axes.PaddingOut[2])*self.Canvas.Drawer.wScaleFactor     #fixed
                
                X[2] = (((self.Cursor_x-self.Canvas.Drawer.BoundingBoxOffset[0])*self.Canvas.Drawer.BoundingBoxFactor[0]
                        +self.Canvas.Drawer.Axes.PaddingIn[0]+self.Canvas.Drawer.Axes.PaddingOut[0])
                       *self.Canvas.Drawer.wScaleFactor)#changes
                       
                X[3] = X[2]
                
                
                Y[0] = ((1-(self.Cursor_y-self.Canvas.Drawer.BoundingBoxOffset[1])*self.Canvas.Drawer.BoundingBoxFactor[1]
                        -self.Canvas.Drawer.Axes.PaddingIn[1]-self.Canvas.Drawer.Axes.PaddingOut[1])
                       *self.Canvas.Drawer.hScaleFactor)#changes
                       
                Y[1] = Y[0]
                
                Y[2] = (self.Canvas.Drawer.Axes.PaddingOut[3])*self.Canvas.Drawer.hScaleFactor           #fixed
                
                Y[3] = (1.0-self.Canvas.Drawer.Axes.PaddingOut[1])*self.Canvas.Drawer.hScaleFactor       #fixed
            
            ########################################################
            #Normal cursor cross only
            elif self.Type == 1:
                
                ###### FOR X ########
                X[0] = (((self.Cursor_x-self.Canvas.Drawer.BoundingBoxOffset[0])
                        *self.Canvas.Drawer.BoundingBoxFactor[0]
                        +self.Canvas.Drawer.Axes.PaddingIn[0]+self.Canvas.Drawer.Axes.PaddingOut[0])
                        *self.Canvas.Drawer.wScaleFactor
                        -self.Size[0])#changes
                       
                       
                X[1] = (((self.Cursor_x-self.Canvas.Drawer.BoundingBoxOffset[0])
                        *self.Canvas.Drawer.BoundingBoxFactor[0]
                        +self.Canvas.Drawer.Axes.PaddingIn[0]+self.Canvas.Drawer.Axes.PaddingOut[0])
                        *self.Canvas.Drawer.wScaleFactor
                        +self.Size[0])#changes

                X[2] = (((self.Cursor_x-self.Canvas.Drawer.BoundingBoxOffset[0])
                       *self.Canvas.Drawer.BoundingBoxFactor[0]
                       +self.Canvas.Drawer.Axes.PaddingIn[0]+self.Canvas.Drawer.Axes.PaddingOut[0])
                       *self.Canvas.Drawer.wScaleFactor)#changes

                X[3] = numpy.copy(X[2])
                
                ###### FOR Y ########
                Y[0] = ((1-(self.Cursor_y-self.Canvas.Drawer.BoundingBoxOffset[1])
                        *self.Canvas.Drawer.BoundingBoxFactor[1]
                        -self.Canvas.Drawer.Axes.PaddingIn[1]-self.Canvas.Drawer.Axes.PaddingOut[1])
                        *self.Canvas.Drawer.hScaleFactor)#changes

                Y[1] = numpy.copy(Y[0])

                Y[2] = ((1-(self.Cursor_y-self.Canvas.Drawer.BoundingBoxOffset[1])
                        *self.Canvas.Drawer.BoundingBoxFactor[1]
                        -self.Canvas.Drawer.Axes.PaddingIn[1]-self.Canvas.Drawer.Axes.PaddingOut[1])
                       *self.Canvas.Drawer.hScaleFactor
                       -self.Size[1])#changes

                Y[3] = ((1-(self.Cursor_y-self.Canvas.Drawer.BoundingBoxOffset[1])
                        *self.Canvas.Drawer.BoundingBoxFactor[1]
                        -self.Canvas.Drawer.Axes.PaddingIn[1]-self.Canvas.Drawer.Axes.PaddingOut[1])
                       *self.Canvas.Drawer.hScaleFactor
                       +self.Size[1])#changes
                            

            ########################################################
            #X shaped cursor cross only
            elif self.Type == 2:
                
                ###### FOR X ########
                X[0] = (((self.Cursor_x-self.Canvas.Drawer.BoundingBoxOffset[0])
                        *self.Canvas.Drawer.BoundingBoxFactor[0]
                        +self.Canvas.Drawer.Axes.PaddingIn[0]+self.Canvas.Drawer.Axes.PaddingOut[0])
                       *self.Canvas.Drawer.wScaleFactor
                       -self.Size[0])#changes
                       
                       
                X[1] = (((self.Cursor_x-self.Canvas.Drawer.BoundingBoxOffset[0])
                        *self.Canvas.Drawer.BoundingBoxFactor[0]
                        +self.Canvas.Drawer.Axes.PaddingIn[0]+self.Canvas.Drawer.Axes.PaddingOut[0])
                       *self.Canvas.Drawer.wScaleFactor
                       +self.Size[0])#changes

                X[2] = (((self.Cursor_x-self.Canvas.Drawer.BoundingBoxOffset[0])
                        *self.Canvas.Drawer.BoundingBoxFactor[0]
                        +self.Canvas.Drawer.Axes.PaddingIn[0]+self.Canvas.Drawer.Axes.PaddingOut[0])
                       *self.Canvas.Drawer.wScaleFactor
                       -self.Size[0])#changes

                X[3] = (((self.Cursor_x-self.Canvas.Drawer.BoundingBoxOffset[0])
                        *self.Canvas.Drawer.BoundingBoxFactor[0]
                        +self.Canvas.Drawer.Axes.PaddingIn[0]+self.Canvas.Drawer.Axes.PaddingOut[0])
                       *self.Canvas.Drawer.wScaleFactor
                       +self.Size[0])#changes
                
                ###### FOR Y ########
                Y[0] = ((1-(self.Cursor_y-self.Canvas.Drawer.BoundingBoxOffset[1])
                        *self.Canvas.Drawer.BoundingBoxFactor[1]
                        -self.Canvas.Drawer.Axes.PaddingIn[1]-self.Canvas.Drawer.Axes.PaddingOut[1])
                       *self.Canvas.Drawer.hScaleFactor
                       +self.Size[1])#changes

                Y[1] = ((1-(self.Cursor_y-self.Canvas.Drawer.BoundingBoxOffset[1])
                        *self.Canvas.Drawer.BoundingBoxFactor[1]
                        -self.Canvas.Drawer.Axes.PaddingIn[1]-self.Canvas.Drawer.Axes.PaddingOut[1])
                       *self.Canvas.Drawer.hScaleFactor
                       -self.Size[1])#changes

                Y[2] = ((1-(self.Cursor_y-self.Canvas.Drawer.BoundingBoxOffset[1])
                        *self.Canvas.Drawer.BoundingBoxFactor[1]
                        -self.Canvas.Drawer.Axes.PaddingIn[1]-self.Canvas.Drawer.Axes.PaddingOut[1])
                       *self.Canvas.Drawer.hScaleFactor
                       -self.Size[1])#changes

                Y[3] = ((1-(self.Cursor_y-self.Canvas.Drawer.BoundingBoxOffset[1])
                        *self.Canvas.Drawer.BoundingBoxFactor[1]
                        -self.Canvas.Drawer.Axes.PaddingIn[1]-self.Canvas.Drawer.Axes.PaddingOut[1])
                       *self.Canvas.Drawer.hScaleFactor
                       +self.Size[1])#changes
            
            ########################################################
            #X shaped cursor cross only
            elif self.Type == 3:
                
                ###### FOR X ########
                X[0] = self.Canvas.Drawer.Axes.PaddingOut[0]*self.Canvas.Drawer.wScaleFactor#changes
                       
                       
                X[1] = (((self.Cursor_x-self.Canvas.Drawer.BoundingBoxOffset[0])
                        *self.Canvas.Drawer.BoundingBoxFactor[0]
                        +self.Canvas.Drawer.Axes.PaddingIn[0]+self.Canvas.Drawer.Axes.PaddingOut[0])
                        *self.Canvas.Drawer.wScaleFactor
                        -self.Size[0])#changes

                X[2] = self.Canvas.Drawer.Axes.PaddingOut[0]*self.Canvas.Drawer.wScaleFactor#changes

                X[3] = (((self.Cursor_x-self.Canvas.Drawer.BoundingBoxOffset[0])
                        *self.Canvas.Drawer.BoundingBoxFactor[0]
                        +self.Canvas.Drawer.Axes.PaddingIn[0]+self.Canvas.Drawer.Axes.PaddingOut[0])
                        *self.Canvas.Drawer.wScaleFactor
                        -self.Size[0])#changes
                        
                X[4] = (1-self.Canvas.Drawer.Axes.PaddingOut[2])*self.Canvas.Drawer.wScaleFactor#changes

                X[5] = (((self.Cursor_x-self.Canvas.Drawer.BoundingBoxOffset[0])
                        *self.Canvas.Drawer.BoundingBoxFactor[0]
                        +self.Canvas.Drawer.Axes.PaddingIn[0]+self.Canvas.Drawer.Axes.PaddingOut[0])
                        *self.Canvas.Drawer.wScaleFactor
                        +self.Size[0])#changes
                        
                X[6] = (1-self.Canvas.Drawer.Axes.PaddingOut[2])*self.Canvas.Drawer.wScaleFactor#changes

                X[7] = (((self.Cursor_x-self.Canvas.Drawer.BoundingBoxOffset[0])
                        *self.Canvas.Drawer.BoundingBoxFactor[0]
                        +self.Canvas.Drawer.Axes.PaddingIn[0]+self.Canvas.Drawer.Axes.PaddingOut[0])
                        *self.Canvas.Drawer.wScaleFactor
                        +self.Size[0])#changes
                
                ###### FOR Y ########
                Y[0] = self.Canvas.Drawer.Axes.PaddingOut[3]*self.Canvas.Drawer.hScaleFactor#changes

                Y[1] = ((1-(self.Cursor_y-self.Canvas.Drawer.BoundingBoxOffset[1])
                        *self.Canvas.Drawer.BoundingBoxFactor[1]
                        -self.Canvas.Drawer.Axes.PaddingIn[1]-self.Canvas.Drawer.Axes.PaddingOut[1])
                        *self.Canvas.Drawer.hScaleFactor
                        -self.Size[1])#changes

                Y[2] = (1-self.Canvas.Drawer.Axes.PaddingOut[1])*self.Canvas.Drawer.hScaleFactor#changes

                Y[3] = ((1-(self.Cursor_y-self.Canvas.Drawer.BoundingBoxOffset[1])
                        *self.Canvas.Drawer.BoundingBoxFactor[1]
                        -self.Canvas.Drawer.Axes.PaddingIn[1]-self.Canvas.Drawer.Axes.PaddingOut[1])
                        *self.Canvas.Drawer.hScaleFactor
                        +self.Size[1])#changes
            
                Y[4] = (1-self.Canvas.Drawer.Axes.PaddingOut[1])*self.Canvas.Drawer.hScaleFactor#changes

                Y[5] = ((1-(self.Cursor_y-self.Canvas.Drawer.BoundingBoxOffset[1])
                        *self.Canvas.Drawer.BoundingBoxFactor[1]
                        -self.Canvas.Drawer.Axes.PaddingIn[1]-self.Canvas.Drawer.Axes.PaddingOut[1])
                        *self.Canvas.Drawer.hScaleFactor
                        +self.Size[1])#changes
            
                Y[6] = self.Canvas.Drawer.Axes.PaddingOut[3]*self.Canvas.Drawer.hScaleFactor#changes

                Y[7] = ((1-(self.Cursor_y-self.Canvas.Drawer.BoundingBoxOffset[1])
                        *self.Canvas.Drawer.BoundingBoxFactor[1]
                        -self.Canvas.Drawer.Axes.PaddingIn[1]-self.Canvas.Drawer.Axes.PaddingOut[1])
                        *self.Canvas.Drawer.hScaleFactor
                        -self.Size[1])#changes
            
            
            ########################################################
            #Apply the crosshari move
            
            if self.Type == 0 or self.Type == 1 or self.Type == 2:
                
                #move X cursor part
                self.Canvas.coords(self.CursorX,
                                   X[0],
                                   Y[0],
                                   X[1],
                                   Y[1])

                #move Y cursor part
                self.Canvas.coords(self.CursorY,
                                   X[2],
                                   Y[2],
                                   X[3],
                                   Y[3])
            
                #evaluate label positions
                LabelX = (X[3]+X[2])/2
                LabelY = (Y[0]+Y[1])/2
            
                    
            elif self.Type == 3:
            
                #move X cursor part
                self.Canvas.coords(self.CursorXY_0,
                                   X[0],
                                   Y[0],
                                   X[1],
                                   Y[1])

                #move Y cursor part
                self.Canvas.coords(self.CursorXY_1,
                                   X[2],
                                   Y[2],
                                   X[3],
                                   Y[3])
            
                #move X cursor part
                self.Canvas.coords(self.CursorXY_2,
                                   X[4],
                                   Y[4],
                                   X[5],
                                   Y[5])

                #move Y cursor part
                self.Canvas.coords(self.CursorXY_3,
                                   X[6],
                                   Y[6],
                                   X[7],
                                   Y[7])
            
                #move the box
                self.Canvas.coords(self.CursorBox,
                                   X[1],
                                   Y[1],
                                   X[5],
                                   Y[5])

                #evaluate label positions
                LabelX = (X[1]+X[7])/2
                LabelY = (Y[1]+Y[3])/2
            
            ########################################################
            #change the position and text of the labels


            if self.LabelType == 0:
    
                if self.LabelPositions[0]:
                    self.Canvas.coords(self.LeftPointerLabel,
                                       (self.Canvas.Drawer.Axes.PaddingOut[0]-self.Canvas.Drawer.Axes.YLabelOffset)*self.Canvas.Drawer.wScaleFactor,
                                       LabelY)
                                       
                                       
                    if self.isYSci:
                        self.Canvas.itemconfig(self.LeftPointerLabel,
                                               text = self.YSciPrecision % self.Cursor_y)
                        
                    else:
                        self.Canvas.itemconfig(self.LeftPointerLabel,
                                               text = str(round(self.Cursor_y,self.Rounding)))

                if self.LabelPositions[1]:
                    self.Canvas.coords(self.BotPointerLabel,
                                       LabelX,
                                       (1-(self.Canvas.Drawer.Axes.PaddingOut[1]-self.Canvas.Drawer.Axes.XLabelOffset))*self.Canvas.Drawer.hScaleFactor)
                
                    if self.isXSci:
                        self.Canvas.itemconfig(self.BotPointerLabel,
                                               text = self.XSciPrecision % self.Cursor_x)
                        
                    else:
                        self.Canvas.itemconfig(self.BotPointerLabel,
                                               text = str(round(self.Cursor_x,self.Rounding)))
                
                if self.LabelPositions[2]:
                    self.Canvas.coords(self.RightPointerLabel,
                                       (1-(self.Canvas.Drawer.Axes.PaddingOut[2]-self.Canvas.Drawer.Axes.YLabelOffset))*self.Canvas.Drawer.wScaleFactor,
                                       LabelY)
                
                    if self.isYSci:
                        self.Canvas.itemconfig(self.RightPointerLabel,
                                               text = self.YSciPrecision % self.Cursor_y)
                        
                    else:
                        self.Canvas.itemconfig(self.RightPointerLabel,
                                               text = str(round(self.Cursor_y,self.Rounding)))
                                   
                if self.LabelPositions[3]:
                    self.Canvas.coords(self.TopPointerLabel,
                                       LabelX,
                                       (self.Canvas.Drawer.Axes.PaddingOut[3]-self.Canvas.Drawer.Axes.XLabelOffset)*self.Canvas.Drawer.hScaleFactor)

                    if self.isXSci:
                        self.Canvas.itemconfig(self.TopPointerLabel,
                                               text = self.XSciPrecision % self.Cursor_x)
                        
                    else:
                        self.Canvas.itemconfig(self.TopPointerLabel,
                                               text = str(round(self.Cursor_x,self.Rounding)))
        
            if self.LabelType == 1:
                
                if self.Verbose:
                
                    print 'This is X of the pointer: ',LabelX
                    print 'This is Y of the pointer: ',LabelY
                
                    print 'This is the wScaleFactor',self.Canvas.Drawer.wScaleFactor/2
                    print 'This is the hScaleFactor',self.Canvas.Drawer.hScaleFactor/2
                
                #find the side the text will be on...
                if LabelX > self.Canvas.Drawer.wScaleFactor/2:
                
                    wSign = -1
                
                else:
                
                    wSign = 1
                
                if LabelY > self.Canvas.Drawer.hScaleFactor/2:
                
                    hSign = 1
                        
                else:
                
                    hSign = -1
                
                if self.Type == 0:
                    
                    Modifier = 1
                
                else:
                
                    Modifier = 0
                
                if self.LabelPositions[0]:
                    
                    #grab the size of the bounding box
                    bounds = self.Canvas.bbox(self.LeftPointerLabel)
                    
                    #calculate the parameters
                    width  = bounds[2] - bounds[0]
                    height = bounds[3] - bounds[1]
                    
                    #place th enew object
                    self.Canvas.coords(self.LeftPointerLabel,
                                       (self.Canvas.Drawer.Axes.PaddingOut[0])*self.Canvas.Drawer.wScaleFactor+width,
                                       LabelY-2*hSign*Modifier*height)
                
                    if self.isYSci:
                        self.Canvas.itemconfig(self.LeftPointerLabel,
                                               text = self.YSciPrecision % self.Cursor_y)
                        
                    else:
                        self.Canvas.itemconfig(self.LeftPointerLabel,
                                               text = str(round(self.Cursor_y,self.Rounding)))

                if self.LabelPositions[1]:
                    
                    #grab the size of the bounding box
                    bounds = self.Canvas.bbox(self.BotPointerLabel)
                    
                    #calculate the parameters
                    width  = bounds[2] - bounds[0]
                    height = bounds[3] - bounds[1]
                    
                    #place th enew object
                    self.Canvas.coords(self.BotPointerLabel,
                                       LabelX+wSign*Modifier*width,
                                       (1-self.Canvas.Drawer.Axes.PaddingOut[1])*self.Canvas.Drawer.hScaleFactor-height)
                
                    if self.isXSci:
                        self.Canvas.itemconfig(self.BotPointerLabel,
                                               text = self.XSciPrecision % self.Cursor_x)
                        
                    else:
                        self.Canvas.itemconfig(self.BotPointerLabel,
                                               text = str(round(self.Cursor_x,self.Rounding)))
                
                if self.LabelPositions[2]:
                    
                    #grab the size of the bounding box
                    bounds = self.Canvas.bbox(self.RightPointerLabel)
                    
                    #calculate the parameters
                    width  = bounds[2] - bounds[0]
                    height = bounds[3] - bounds[1]
                    
                    #place th enew object
                    self.Canvas.coords(self.RightPointerLabel,
                                       (1-self.Canvas.Drawer.Axes.PaddingOut[2])*self.Canvas.Drawer.wScaleFactor-width,
                                       LabelY-2*hSign*Modifier*height)
                
                    if self.isYSci:
                        self.Canvas.itemconfig(self.RightPointerLabel,
                                               text = self.YSciPrecision % self.Cursor_y)
                        
                    else:
                        self.Canvas.itemconfig(self.RightPointerLabel,
                                               text = str(round(self.Cursor_y,self.Rounding)))
                                   
                if self.LabelPositions[3]:
                    
                    #grab the size of the bounding box
                    bounds = self.Canvas.bbox(self.TopPointerLabel)
                    
                    #calculate the parameters
                    width  = bounds[2] - bounds[0]
                    height = bounds[3] - bounds[1]
                    
                    #place th enew object
                    self.Canvas.coords(self.TopPointerLabel,
                                       LabelX+wSign*Modifier*width,
                                       (self.Canvas.Drawer.Axes.PaddingOut[3])*self.Canvas.Drawer.hScaleFactor+height)

                    if self.isXSci:
                        self.Canvas.itemconfig(self.TopPointerLabel,
                                               text = self.XSciPrecision % self.Cursor_x)
                        
                    else:
                        self.Canvas.itemconfig(self.TopPointerLabel,
                                               text = str(round(self.Cursor_x,self.Rounding)))

            if self.LabelType == 2:
                
                if self.Verbose:
                
                    print 'This is X of the pointer: ',LabelX
                    print 'This is Y of the pointer: ',LabelY
                
                    print 'This is the wScaleFactor',self.Canvas.Drawer.wScaleFactor/2
                    print 'This is the hScaleFactor',self.Canvas.Drawer.hScaleFactor/2
                
                #find the side the text will be on...
                if LabelX > self.Canvas.Drawer.wScaleFactor/2:
                
                    wSign = -1
                
                else:
                
                    wSign = 1
                
                if LabelY > self.Canvas.Drawer.hScaleFactor/2:
                
                    hSign = 1
                        
                else:
                
                    hSign = -1
                
                if self.LabelPositions[0]:
                    
                    #grab the size of the bounding box
                    bounds = self.Canvas.bbox(self.LeftPointerLabel)
                    
                    #calculate the parameters
                    width  = bounds[2] - bounds[0]
                    height = bounds[3] - bounds[1]
                    
                    #place th enew object
                    self.Canvas.coords(self.LeftPointerLabel,
                                       LabelX+wSign*width,
                                       LabelY-2*hSign*height)
                
                    if self.isYSci:
                        self.Canvas.itemconfig(self.LeftPointerLabel, text = self.YSciPrecision % self.Cursor_y)
                        
                    else:
                        self.Canvas.itemconfig(self.LeftPointerLabel, text = 'Y = '+str(round(self.Cursor_y,self.Rounding)))

                if self.LabelPositions[1]:
                    
                    #grab the size of the bounding box
                    bounds = self.Canvas.bbox(self.BotPointerLabel)
                    
                    #calculate the parameters
                    width  = bounds[2] - bounds[0]
                    height = bounds[3] - bounds[1]
                    
                    #place th enew object
                    self.Canvas.coords(self.BotPointerLabel,
                                       LabelX+wSign*width,
                                       LabelY-hSign*height)
                
                    if self.isXSci:
                        self.Canvas.itemconfig(self.BotPointerLabel, text = self.XSciPrecision % self.Cursor_x)
                        
                    else:
                        self.Canvas.itemconfig(self.BotPointerLabel, text = 'X = '+str(round(self.Cursor_x,self.Rounding)))
                
                if self.LabelPositions[2]:
                    
                    #grab the size of the bounding box
                    bounds = self.Canvas.bbox(self.RightPointerLabel)
                    
                    #calculate the parameters
                    width  = bounds[2] - bounds[0]
                    height = bounds[3] - bounds[1]
                    
                    #place th enew object
                    self.Canvas.coords(self.RightPointerLabel,
                                       LabelX+wSign*width,
                                       LabelY-2*hSign*height)
                
                    if self.isYSci:
                        self.Canvas.itemconfig(self.RightPointerLabel, text = self.YSciPrecision % self.Cursor_y)
                        
                    else:
                        self.Canvas.itemconfig(self.RightPointerLabel, text = 'Y = '+str(round(self.Cursor_y,self.Rounding)))
                                   
                if self.LabelPositions[3]:
                    
                    #grab the size of the bounding box
                    bounds = self.Canvas.bbox(self.TopPointerLabel)
                    
                    #calculate the parameters
                    width  = bounds[2] - bounds[0]
                    height = bounds[3] - bounds[1]
                    
                    #place th enew object
                    self.Canvas.coords(self.TopPointerLabel,
                                       LabelX+wSign*width,
                                       LabelY-hSign*height)

                    if self.isXSci:
                        self.Canvas.itemconfig(self.TopPointerLabel, text = self.XSciPrecision % self.Cursor_x)
                        
                    else:
                        self.Canvas.itemconfig(self.TopPointerLabel, text = 'X = '+str(round(self.Cursor_x,self.Rounding)))
            
            ########################################################
            #change the position of the Ticks

            if self.Verbose:
                print self.LabelTicks


            if self.LabelTicks[0]:
                
                if self.Verbose:
                    print 'Trying to move the Left Tick'


                self.Canvas.coords(self.LeftPointerTick,
                                   
                                   (self.Canvas.Drawer.Axes.PaddingOut[0])
                                   *self.Canvas.Drawer.wScaleFactor-self.LabelTicksOffset,
                                   
                                   LabelY,
                                   
                                   (self.Canvas.Drawer.Axes.PaddingOut[0])
                                   *self.Canvas.Drawer.wScaleFactor+self.LabelTicksOffset,
                                   
                                   LabelY)
            

            if self.LabelTicks[1]:
                
                if self.Verbose:
                    print 'Trying to move the Bot Tick'
                
                self.Canvas.coords(self.BotPointerTick,
                                   
                                   LabelX,
                                   
                                   (1-self.Canvas.Drawer.Axes.PaddingOut[1])
                                   *self.Canvas.Drawer.hScaleFactor-self.LabelTicksOffset,
                                   
                                   LabelX,
                                   
                                   (1-self.Canvas.Drawer.Axes.PaddingOut[1])
                                   *self.Canvas.Drawer.hScaleFactor+self.LabelTicksOffset)
            
            
            if self.LabelTicks[2]:
                
                if self.Verbose:
                    print 'Trying to move the Right Tick'
                
                self.Canvas.coords(self.RightPointerTick,
                                   
                                   (1-self.Canvas.Drawer.Axes.PaddingOut[2])
                                   *self.Canvas.Drawer.wScaleFactor-self.LabelTicksOffset,
                                   
                                   LabelY,
                                   
                                   (1-self.Canvas.Drawer.Axes.PaddingOut[2])
                                   *self.Canvas.Drawer.wScaleFactor+self.LabelTicksOffset,
                                   
                                   LabelY)

            if self.LabelTicks[3]:
                
                if self.Verbose:
                    print 'Trying to move the Top Tick'
                
                self.Canvas.coords(self.TopPointerTick,
                                   
                                   LabelX,
                                   
                                   (self.Canvas.Drawer.Axes.PaddingOut[3])
                                   *self.Canvas.Drawer.hScaleFactor-self.LabelTicksOffset,
                                   
                                   LabelX,
                                   
                                   (self.Canvas.Drawer.Axes.PaddingOut[3])
                                   *self.Canvas.Drawer.hScaleFactor+self.LabelTicksOffset)

        #tkinter function
        self.Canvas.tag_raise('TopTop', 'Top')
        

        X = []
        Y = []

    def CorrectCursor(self):
        
        #Do a check if we are located within the area...
        if self.Cursor_x <= self.Canvas.Drawer.BoundingBoxOffset[0]:
        
            self.Cursor_x = self.Canvas.Drawer.BoundingBoxOffset[0]

        if self.Cursor_x >= self.Canvas.Drawer.BoundingBoxOffset[2]:
        
            self.Cursor_x = self.Canvas.Drawer.BoundingBoxOffset[2]

        if self.Cursor_y <= self.Canvas.Drawer.BoundingBoxOffset[1]:
        
            self.Cursor_y = self.Canvas.Drawer.BoundingBoxOffset[1]

        if self.Cursor_y >= self.Canvas.Drawer.BoundingBoxOffset[3]:
        
            self.Cursor_y = self.Canvas.Drawer.BoundingBoxOffset[3]




