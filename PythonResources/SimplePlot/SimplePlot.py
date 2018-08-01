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
from functools import *

#import imaging libraries
import PIL

import PIL.Image

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

#import visual element classes
from Visual_Contour         import *
from Visual_Cascade         import *
from Visual_Plot            import *
from Visual_Int_Plot        import *
from Visual_Line            import *
from Visual_Range           import *

#import UI element classes
from UI_Axes                import *
from UI_Interaction         import *
from UI_Keyboard            import *
from UI_Title               import *
from UI_Settings            import *
from UI_Drawer              import *
from UI_Zoomer              import *
from UI_Legend              import *

import UI_Drawer as DrawerClass

#import Pointer definition classes
from Pointer_Pointer        import *
from Pointer_Modification   import *
from Pointer_Measurement    import *
from Pointer_Move_Object    import *


def main():
    
#create some data for the contour loop
#    Y = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
#         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
#         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
#         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
#         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
#         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
#         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
#         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
#         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
#         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
#    
#    X = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#         [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
#         [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
#         [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
#         [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
#         [6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
#         [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
#         [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
#         [9, 9, 9, 9, 9, 9, 9, 9, 9, 9]]
#         
#    Z = [[1,   1,   1,   1,   1,   1,   1,   1,   1,   1],
#         [1,   0,   0,   0,   0,   0,   1,   0,   0,   1],
#         [1,   0,   0,   1,   1,   1,   1, 0.5,   0,   1],
#         [1,   0,   0,   1,   0, 0.5,   0, 0.5,   0,   1],
#         [1,   0,   1,   1,   0, 0.5,   0,   1,   0,   1],
#         [1,   0, 0.5,   0, 0.5,   0,   0,   1,   0,   1],
#         [1,   0,   1,   0,   0,   0,   0,   1,   0,   1],
#         [1,   0,   1,   0,   1, 0.5, 0.5, 0.5,   0,   1],
#         [1,   0,   0,   0,   0,   0,   0,   0,   0,   1],
#         [0,   0,   1,   1,   1,   1,   1,   1,   1,   1]]
#
#    Z = numpy.random.rand(10,10)

    
    delta = 1
    x = numpy.arange(0, 100, delta)
    y = numpy.arange(0, 100, delta)
    X, Y = numpy.meshgrid(x, y)
    Z = numpy.random.rand(100,100)
    #print Z
    ######################################################
    root = Tk()
    myframe = Frame(root,width=400, height=300)
    myframe.pack(fill=BOTH, expand=YES)
    mycanvas = MultiPlotCanvas(myframe,
                               grid     = [[True,True],[True,True]],
                               ratioX   = [4,1],
                               ratioY   = [1,4],
                               width    = 100,
                               height   = 100,
                               bg       = "white",
                               highlightthickness = 0)
    
        
    #grab the subplot definitions
    
    ax = mycanvas.GetSubPlot(0,0)
    
    bx = mycanvas.GetSubPlot(1,0)
    
    cx = mycanvas.GetSubPlot(1,1)
    #cx.MakeGhost()
    dx = mycanvas.GetSubPlot(0,1)
    
#    dx.AddContour(X,Y,Z,
#                  MeshStepping = 50,
#                  Stepping  = 30,
#                  Type      = 'Surface',
#                  MeshThickness = 0.1)

    dx.AddCascade(X,Y,Z)
    
    dx.Live = 2
    dx.Pointer.Sticky = 0
    
    ######################################################
    # add some Plot to the Drawer
    ax.AddiPlot([1,3,4,5,6,7,8],[1,2,3,2.5,1,0.5,0], Thickness = 5,Name = 'I am first', color = 'red'  , style = ['o',4,4])
    ax.AddiPlot([1,3,4,4.5,6,7,8],[1,2,3,2,1,0.5,0], Thickness = 8, color = 'black', style = ['o',4,4])
    ax.AddiPlot([i*0.01 for i in range(0,4*315)],numpy.sin([i*0.01 for i in range(0,4*315)]), color = 'blue', Thickness = 3 )
    bx.AddPlot([i*0.01 for i in range(0,4*315)],numpy.sin([i*0.01+1 for i in range(0,4*315)]), color = 'yellow', Thickness = 3 )
    cx.AddPlot(numpy.sin([i*0.01+1 for i in range(0,4*315)]),[i*0.01 for i in range(0,4*315)], color = 'green', Thickness = 3 )
    
    ax.AddRange([2,3])
    ax.AddLine(0, Type = 'horizontal',Thickness = 5,Name = 'I am first', color = 'red'  )
    ax.AddLine(4, Type = 'vertical',Thickness = 3,Name = 'I am first', color = 'black'  )
    
    ax.Pointer.Sticky = 1
    #dx.AddContour(X,Y,Z,35)
    #dx.ZoomBox = [0,0,10,10]
    
    ######################################################
    #Set some padding parameters for ax
    ax.Axes.PaddingIn       = [0.05,0.05,0.05,0.05]
    ax.Axes.PaddingOut      = [0.15,0.1,0.1,0.1]
    ax.Axes.Thickness       = [2,2,2,2]
    ax.Axes.XTickSpacing    = 1
    ax.Axes.XTickType       = 1
    ax.SmartResize          = True
    ax.Axes.isYSci          = [True,True,True,True]
    ax.Pointer.isYSci       = [True,True,True,True]
    
    ax.Pointer.YSciPrecision = '%.1e'
    
    ax.Title.SetTitle(text = 'Hello')
    
    ######################################################
    #Set some padding parameters for ax
    bx.Axes.PaddingIn       = [0.05,0.05,0.05,0.05]
    bx.Axes.PaddingOut      = [0.05,0.05,0.05,0.05]
    bx.Axes.Thickness       = [2,2,2,2]
    bx.Axes.XTickSpacing    = 1
    bx.Axes.XTickType       = 1
    
    cx.Axes.PaddingIn       = [0.05,0.05,0.05,0.05]
    cx.Axes.PaddingOut      = [0.05,0.05,0.05,0.05]
    cx.Axes.Thickness       = [2,2,2,2]
    cx.Axes.XTickSpacing    = 1
    cx.Pointer.Sticky       = 3
    cx.SmartResize          = True
    
    
    
    #######################################################
    #draw the plots
    ax.DrawAllPlot()
    bx.DrawAllPlot()
    cx.DrawAllPlot()
    dx.DrawAllPlot()
    
    #place the axes
    ax.Axes.DrawAxes()
    bx.Axes.DrawAxes()
    cx.Axes.DrawAxes()
    dx.Axes.DrawAxes()
    
    #place the ticks
    ax.Axes.PlaceAllTicks()
    bx.Axes.PlaceAllTicks()
    cx.Axes.PlaceAllTicks()
    dx.Axes.PlaceAllTicks()
    
    #Place tick labels
    ax.Axes.PlaceAllLabels()
    bx.Axes.PlaceAllLabels()
    cx.Axes.PlaceAllLabels()
    dx.Axes.PlaceAllLabels()
    
    #activate the cursor
    ax.BindCursor()
    bx.BindCursor()
    cx.BindCursor()
    dx.BindCursor()
    
    #place the ticks
    ax.Axes.PlaceGrids()
    bx.Axes.PlaceGrids()
    cx.Axes.PlaceGrids()
    dx.Axes.PlaceGrids()
    
    #actiavte the zomer
    ax.BindZoomer()
    bx.BindZoomer()
    cx.BindZoomer()
    dx.BindZoomer()
    
    #link the axes
    mycanvas.Link(ax,bx,variableIn = 'x',variableOut = 'x')
    mycanvas.Link(bx,ax,variableIn = 'x',variableOut = 'x')
    mycanvas.Link(bx,cx,variableIn = 'x',variableOut = 'y')

    
    def Print(indx):
    
        print indx
    
    #bind cursor
    ax.Pointer.BindMethod(Print)
    ax.Pointer.Sticky = 1
    
    ax.UnbindZoomer()
    #ax.BindInteractor()
    
    #start the tkinter test loop
    root.mainloop()

# a subclass of Canvas for dealing with resizing of windows
class MultiPlotCanvas():
    
    '''
    ########################################################################
    In the hope to make things easier a Subplot interface was created.
    It functions on the same basis as matplotlib...
    
    grid of boolean values is given to the element, the ratios in X and in
    Y are given as scale multiplication factors. 
    
    All other arguments are ported onto the different Subplots
    
    ########################################################################
    '''
    
    def __init__(self,
                 parent,
                 grid           = [[True]],
                 ratioX         = [1],
                 ratioY         = [1],
                 NoTitle        = False,
                 ManagerFrame   = True,
                 **kwargs):
        
        ####################################
        #Default parameetrs
        self.Verbose        = False
        self.Parent         = parent
        self.ratiosX        = ratioX
        self.ratiosY        = ratioY
        self.NoTitle        = NoTitle
        self.ManagerFrame   = ManagerFrame
        self.ManagerIconDimension = 20
        

        ####################################
        #Prepare the object adress array
        self.Objects            = []
        self.ObjectCoordinates  = []
        self.Titles             = []
        self.Frames             = []
        self.Settings           = []
        self.LinkList           = []
        self.GrabObjects        = []
        
        #prepare an index
        Index = 0
        
        #make a internal reference matrix
        for i in range(0,len(grid)):
            
            #append empty array
            self.Objects.append([])
        
            for j in range(0,len(grid[i])):
        
                #check condition
                if grid[i][j]:
                    
                    #create the fame
                    self.Frames.append([Frame(parent),i,j])
                    
                    #save it
                    self.Objects[i].append([PlotCanvas(self.Frames[-1][0],
                                                       Multi = self,
                                                       ID = Index,
                                                       **kwargs)
                                            ,i,j])
                    
                    #make a pointer list
                    self.GrabObjects.append(self.Objects[i][-1])
                    
                    if not self.NoTitle:
                    
                        #create Tilte frame
                        self.Titles.append(TitleClass.TitleClass(self.Objects[i][-1][0].Drawer,self.Frames[-1][0]))
                    
                    #add corrdinates into the list keep linear access
                    self.ObjectCoordinates.append([i,j])
                
                    #move the index forward
                    Index += 1
                
                else:
    
                    self.Objects[i].append([])
    
        #are we verbose
        if self.Verbose:
        
            print 'This is the object array: ',self.Objects
            print 'This is the Frame array: ',self.Frames

        ####################################
        #Try to place the elements
        self.PlaceSubPlots()
        self.ConfigureGrid(self.ratiosX,self.ratiosY)
        self.PlaceManager()

        ####################################
        #Configure settings window
        self.SettingsClass = SettingsClass(parent,self)
    
    def PlaceSubPlots(self):
    
        '''
        ########################################################################
        Simple Tkinter placement manager...
        
        Note that it will use grid as this is the mode that makes sense in a
        Subplot interface and that was also used by matplotlib
        ########################################################################
        '''
                
        #cycle through all elements
        for k in range(0,len(self.Frames)):
            
            #grid the canvas to the frame
            self.Objects[self.Frames[k][1]][self.Frames[k][2]][0].grid(row      = 1,
                                                                       column   = 0,
                                                                       sticky   = N+S+E+W)

            if not self.NoTitle:
                self.Titles[k].TitleFrame.grid(row      = 0,
                                               column   = 0,
                                               sticky   = E+W)
                                                                       
            #configure
            self.Frames[k][0].grid_rowconfigure(1,weight =1)
            self.Frames[k][0].grid_columnconfigure(0,weight =1)
            
            #palce all ements grid style
            self.Frames[k][0].grid(row      = self.Frames[k][1],
                                   column   = self.Frames[k][2],
                                   sticky   = N+S+E+W)



    def PlaceManager(self):
        '''
        ########################################################################
        Here we are trying to build the selector that will allow us to manage
        all plots between selected tool and save tool ultimately. This means 
        also that the save tool will be revised.
        
        
        This also configures 4 labels that can be used by the user to bind method
        input such as coordinates and so on. For example the measuroing tool can
        display it's output here if requested.
        Or the zoom box can siplay the zoom area... etc...
        ########################################################################
        '''
        
        #create the Manager
        if self.ManagerFrame:
    
            #create the manager frame
            self.Manager = ttk.Frame(self.Parent, padding = '2p')

            #######################
            #Modes and variables
            self.MODES = [
                          ("Zoom"       , 0),
                          ("Measure"    , 1),
                          ("Edit"       , 2),
                          ("Settings"   , 3),
                          ]
        
            #######################
            #Grab the Path
            Path = os.path.join(os.path.dirname(DrawerClass.__file__),'Images')
            
            #######################
            #Load images
            ZoomImage    = PIL.Image.open(os.path.join(Path,'Zoom.jpg'))
            ZoomImage    = ZoomImage.resize((self.ManagerIconDimension,
                                             self.ManagerIconDimension),PIL.Image.ANTIALIAS)
            ZoomImage    = ImageTk.PhotoImage(ZoomImage)
            
            MeasImage    = PIL.Image.open(os.path.join(Path,'Measure.jpg'))
            MeasImage    = MeasImage.resize((self.ManagerIconDimension,
                                             self.ManagerIconDimension),PIL.Image.ANTIALIAS)
            MeasImage    = ImageTk.PhotoImage(MeasImage)
            
            EditImage    = PIL.Image.open(os.path.join(Path,'Edit.jpg'))
            EditImage    = EditImage.resize((self.ManagerIconDimension,
                                             self.ManagerIconDimension),PIL.Image.ANTIALIAS)
            EditImage    = ImageTk.PhotoImage(EditImage)
            
            SettImage    = PIL.Image.open(os.path.join(Path,'Setting.jpg'))
            SettImage    = SettImage.resize((self.ManagerIconDimension,
                                             self.ManagerIconDimension),PIL.Image.ANTIALIAS)
            SettImage    = ImageTk.PhotoImage(SettImage)
            
            #######################
            #######################
            #Set the array
            self.PATHS = [ZoomImage,
                          MeasImage,
                          EditImage,
                          SettImage]
            
            self.VARIABLE = [IntVar(),
                             IntVar(),
                             IntVar(),
                             IntVar()]
            
            
            #######################
            #######################
            #Populate the frame:
            self.Selector = [None]*len(self.PATHS)
            
            for i in range(0,len(self.MODES)):
                
                self.Selector[i] = ttk.Checkbutton(self.Manager,
                                                   #text         = self.MODES[i][0],
                                                   image        = self.PATHS[i],
                                                   variable     = self.VARIABLE[i],
                                                   command      = partial(self.TogglerMethod,i))
                                                   #value        = self.MODES[i][1])
                                                   #indicatoron  =   0)
                     
                self.Selector[i].config(style    = 'Toolbutton'  )
                self.Selector[i].grid(row = 0,
                                      column = i)


            #######################
            #######################
            #initialise the labels
            self.ManagerLabels = [None]*4
            
            for i in range(0, len(self.ManagerLabels)):
            
                self.ManagerLabels[i] = ttk.Label(self.Manager,
                                                  text = '')
            
                self.ManagerLabels[i].grid(row = 0,
                                           column = len(self.MODES)+i )
            
            #######################
            #######################
            #place the manager frame
            self.Manager.grid(row = len(self.ratiosX),
                              column = 0,
                              columnspan = len(self.ratiosY),
                              sticky = E+W)


    def TogglerMethod(self, ID):
        '''
        ########################################################################
        This will allow the system to process the togling of the tool selector
        
        ########################################################################
        '''

        #cycle
        for i in range(0,len(self.Selector)):
        
            if ID == i:
            
                #grid the object into place.
                self.VARIABLE[i].set(1)
        
            else:
            
                #grid the object into place.
                self.VARIABLE[i].set(0)

        #set out the processing
        self.ProcessMethod(ID)
                
    def ProcessMethod(self, ID):
        '''
        ########################################################################
        This will allow the system to process the togling of the tool selector
        
        ########################################################################
        '''
        
        ##########################
        #Bid right method
        if ID < 3:
        
            ##########################
            #set the methods
            BindMethods = [[self.GrabObjects[i][0].Drawer.BindZoomer   for i in range(0, len(self.GrabObjects))],
                           [self.GrabObjects[i][0].Drawer.BindMeasurer for i in range(0, len(self.GrabObjects))],
                           [self.GrabObjects[i][0].Drawer.BindModifier for i in range(0, len(self.GrabObjects))]]

            UnbindMethods = [[self.GrabObjects[i][0].Drawer.UnbindZoomer   for i in range(0, len(self.GrabObjects))],
                             [self.GrabObjects[i][0].Drawer.UnbindMeasurer for i in range(0, len(self.GrabObjects))],
                             [self.GrabObjects[i][0].Drawer.UnbindModifier for i in range(0, len(self.GrabObjects))]]

            ##########################
            #unbind all methods
            for i in range(0,len(self.GrabObjects)):
            
                try:
                    UnbindMethods[0][i]()
                except:
                    pass
                
                try:
                    UnbindMethods[1][i]()
                except:
                    pass
                
                try:
                    UnbindMethods[2][i]()
                except:
                    pass
                      
            
        
            ##########################
            #bind the corresponding method
            for i in range(0,len(self.GrabObjects)):
    
                BindMethods[ID][i]()

        elif ID == 3:
                
            self.SettingsClass.Creator()
    
    def ConfigureGrid(self, ratiosX, ratiosY):
        '''
        ########################################################################
        The ratio definition is important for tkinter to handle the stickyness
        
        Otherwise elements will nto expand
        ########################################################################
        '''
        
        for i in range(0,len(ratiosX)):
        
            try:
                #configure the frame
                self.Parent.grid_rowconfigure(i,weight = ratiosX[i])
    
            except:
    
                if self.Verbose:
                    print 'Could not set the row weight for: ',i
        
        for j in range(0,len(ratiosY)):
        
            try:
                #configure the frame
                self.Parent.grid_columnconfigure(j,weight = ratiosY[j])
    
            except:
    
                if self.Verbose:
                    print 'Could not set the row weight for: ',j

    def GetSubPlot(self,i,j):

        '''
        ########################################################################
        Very simple funciton that will retrieve the suplot pointer 
        
        can be used ax = GetSubPlot(0,0)
        ########################################################################
        '''

        return self.Objects[i][j][0].Drawer


    def Link(self, ax , bx , variableIn = 'x', variableOut = 'x'):

        '''
        ########################################################################
        This class is here to allow for corss listening between variables
        between different subplots...
        
        
        This will call the pointer of ax and bx and tell thel to pass on the
        coordinates to the pointer handlers each time there is a refresh. 
        
        So basically we parasite the pointer to speak to another element
        
        This will also return a link in the link list and an associated ID
        The ID will be returned and can be fed to the Unlink
        ########################################################################
        '''
        
        #chose the target
        Target = bx.Mouse
        
        #create the array of th emethod
        Link = ['',ax.Mouse.LinkList,variableIn,variableOut, Target, bx.Mouse]
        
        #add the element at the end of the list
        self.LinkList.append(Link)

        #append the ID
        ID = self.LinkList[-1][0] = len(self.LinkList)

        #finally send it out to the linker
        Link[1].append(self.LinkList[-1])
        
        #debug
        if self.Verbose:
        
            print 'This is the Link: ', Link
        
        return ID

    def Unlink(self, ID = 'all'):
        '''
        ########################################################################
        This serves to unlink two elements
        ########################################################################
        '''
        pass

# a subclass of Canvas for dealing with resizing of windows
class PlotCanvas(Canvas):
    
    def __init__(self,parent,Multi = None, ID = 0 ,width = 100, height = 100, **kwargs):
        
        '''
        ######################################################
        Add a description here
        ######################################################
        '''
        
        #hirarchy
        self.Multi          = Multi
        self.ManagerStarted = False
        self.ID             = ID
        
        #initialise the canvas
        Canvas.__init__(self, parent,width = width, height = height,**kwargs)
        
        #bind the resize routine
        self.bind('<Configure>', self.on_resize)
        
        #grab initial parameters
        self.height = self.winfo_reqheight()
        self.width  = self.winfo_reqwidth()
        
        #link the drawer
        self.LinkDrawer()
        
        #initialise drawer scale parameetrs
        self.Drawer.SetScale(width,height)
    
    def LinkDrawer(self):
    
        '''
        ######################################################
        Links the drawer to this class
        ######################################################
        '''
        self.Drawer = Drawer(self,
                             Multi = self.Multi,
                             ID = self.ID)
    
    def on_resize(self,event):
        
        '''
        ######################################################
        Makes sure than an event handler resizes the canvas
        plane to ensure the fill attribute
        ######################################################
        '''
            
        ########################################################
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        
        ########################################################
        #fetch the corners
        self.width  = event.width
        self.height = event.height
    
        ########################################################
        #start the resize manager
        if not self.ManagerStarted:
    
            self.Manager(initialise = True)
            self.ManagerStarted = True

    def Manager(self, initialise = False):
        
        '''
        ######################################################
        This is a simple manager utilising the .after() method
        of tkinter in order to check f we stoped moving.
        ######################################################
        '''
        
        if initialise:
            
            #grab the buffer
            self.BufferWidth    = numpy.copy(self.width)
            self.BufferHeight   = numpy.copy(self.height)
        
            #start the listener loop
            self.after(50, self.Manager)

        else:
            
            #do a check
            if self.width == self.BufferWidth and self.height == self.BufferHeight:

                #we stoped moving perfor the resize
                self.PerformResize()
                    
                #reset the manager variable
                self.ManagerStarted = False

            else:
                
                #grab the buffer
                self.BufferWidth    = numpy.copy(self.width)
                self.BufferHeight   = numpy.copy(self.height)

                #start the listener loop
                self.after(50, self.Manager)

    def PerformResize(self):
        '''
        ######################################################
        It was found that reseizing the entire time was to 
        resource expensive. As such the handler will wait for
        0.5 seconds before comparing and then trying to
        performe a resize if the variables didn't change
        ######################################################
        '''
        
        #resize
        self.config(width=self.width, height=self.height)
        
        #send the scale to the drawer
        self.Drawer.SetScale(self.width,self.height)
        
        #reprocess all
        if not self.Drawer.Ghost:
        
            self.Drawer.Zoom()

    def CanvasCoordinates(self,event):
        
        '''
        ######################################################
        Fetches and returns the proper set of coordinates
        inside the canvas. This will be usefull for the 
        zoomer classes later on
        
        ######################################################
        '''
        
        ########################################################
        #try to fetch new positions
        self.DeltaX = (self.Drawer.Axes.PaddingIn[0]+self.Drawer.Axes.PaddingOut[0])*self.width
        self.DeltaY = (self.Drawer.Axes.PaddingIn[1]+self.Drawer.Axes.PaddingOut[1])*self.height
        
        #grab the actual top left part of the draw zone
        self.DrawTopX = int(self.DeltaX)
        self.DrawTopY = int(self.DeltaY)
        
        self.DrawWidth  = self.width  - 2 * int(self.DeltaX)
        self.DrawHeight = self.height - 2 * int(self.DeltaY)
        
        #calculate the actual coordinates
        x = (self.Drawer.BoundingBoxOffset[2]-self.Drawer.BoundingBoxOffset[0])*((float(event.x)-float(self.DrawTopX))/float(self.DrawWidth))+self.Drawer.BoundingBoxOffset[0]

        y = (self.Drawer.BoundingBoxOffset[1]-self.Drawer.BoundingBoxOffset[3])*((float(event.y)-float(self.DrawTopY))/float(self.DrawHeight))+self.Drawer.BoundingBoxOffset[3]
        
        #if self.Verbose:
        
        print 'These are the pixel coordinates: ',event.x, event.y
        
        print 'These are the actual coordinates: ',x,y

        return x,y






'''
I want a settings window to adjust padding and ticks and 
things like this dynamically...

class Settings:

'''

if __name__ == "__main__":
    #profile.run('main(); print')
    main()
