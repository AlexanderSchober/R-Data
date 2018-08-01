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

#c implementation
import cContourCalculations as CCalc


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
    myframe = Frame(root,width=200, height=100)
    myframe.pack(fill=BOTH, expand=YES)
    mycanvas = MultiPlotCanvas(myframe,
                               grid     = [[True,True],[True,True]],
                               ratioX   = [1,1],
                               ratioY   = [1,1],
                               width    = 100,
                               height   = 100,
                               bg       = "white",
                               highlightthickness = 0)
    
        
    #grab the subplot definitions
    
    ax = mycanvas.GetSubPlot(0,0)
    
    bx = mycanvas.GetSubPlot(1,0)
    
    cx = mycanvas.GetSubPlot(1,1)
    
    dx = mycanvas.GetSubPlot(0,1)
    
    dx.AddContour(X,Y,Z,
                  MeshStepping = 50,
                  Stepping  = 30,
                  Type      = 'Surface',
                  MeshThickness = 0.1)
    
    
    dx.Live = 2
    dx.Pointer.Sticky = 4
    
    ######################################################
    # add some Plot to the Drawer
    ax.AddPlot([1,3,4,5,6,7,8],[1,2,3,2.5,1,0.5,0], Thickness = 5,Name = 'I am first', color = 'red'  , style = ['o',4,4])
    ax.AddPlot([1,3,4,4.5,6,7,8],[1,2,3,2,1,0.5,0], Thickness = 8, color = 'black', style = ['o',4,4])
    ax.AddPlot([i*0.01 for i in range(0,4*315)],numpy.sin([i*0.01 for i in range(0,4*315)]), color = 'blue', Thickness = 3 )
    bx.AddPlot([i*0.01 for i in range(0,4*315)],numpy.sin([i*0.01+1 for i in range(0,4*315)]), color = 'yellow', Thickness = 3 )
    cx.AddPlot(numpy.sin([i*0.01+1 for i in range(0,4*315)]),[i*0.01 for i in range(0,4*315)], color = 'green', Thickness = 3 )
    
    ax.AddRange([2,3])
    ax.AddLine(0, Type = 'horizontal',Thickness = 5,Name = 'I am first', color = 'red'  )
    ax.AddLine(4, Type = 'vertical',Thickness = 3,Name = 'I am first', color = 'black'  )
    
    #dx.AddContour(X,Y,Z,35)
    #dx.ZoomBox = [0,0,10,10]
    
    ######################################################
    #Set some padding parameters for ax
    #ax.Axes.PaddingIn  = [0.05,0.05]
    #ax.Axes.PaddingOut = [0.15,0.1]
    ax.Axes.Thickness       = 2
    ax.Axes.XTickSpacing    = 1
    ax.Axes.XTickType       = 1
    ax.SmartResize          = True
    ax.Axes.isYSci          = True
    ax.Pointer.isYSci       = True
    
    ax.Pointer.YSciPrecision = '%.1e'
    
    ax.Title.SetTitle(text = 'Hello')
    
    ######################################################
    #Set some padding parameters for ax
    #bx.Axes.PaddingIn  = [0.05,0.05]
    #bx.Axes.PaddingOut = [0.05,0.05]
    bx.Axes.Thickness       = 2
    bx.Axes.XTickSpacing    = 1
    bx.Axes.XTickType       = 1
    
    #cx.Axes.PaddingIn  = [0.05,0.05]
    #cx.Axes.PaddingOut = [0.05,0.05]
    cx.Axes.Thickness       = 2
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
                 grid = [[True]],
                 ratioX = [1],
                 ratioY = [1],
                 NoTitle = False,
                 **kwargs):
        
        ####################################
        #Default parameetrs
        self.Verbose    = True
        self.Parent     = parent
        self.ratiosX    = ratioX
        self.ratiosY    = ratioY
        self.NoTitle    = NoTitle
        
        ####################################
        #Prepare the object adress array
        self.Objects    = []
        self.ObjectCoordinates = []
        self.Titles     = []
        self.Frames     = []
        self.Settings   = []
        self.LinkList   = []
        
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
                    self.Objects[i].append([PlotCanvas(self.Frames[-1][0],Multi = self, ID = Index,**kwargs),i,j])
                    
                    if not self.NoTitle:
                    
                        #create Tilte frame
                        self.Titles.append(TitleClass(self.Objects[i][-1][0].Drawer,self.Frames[-1][0]))
                    
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
        self.Multi = Multi
        self.ManagerStarted = False
        self.ID = ID
        
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
        self.Drawer = Drawer(self,Multi = self.Multi, ID = self.ID)
    
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

class SettingsClass:
    
    '''
    ########################################################################
    This settings class is a window creator on standbye. it will launch when
    the call is made
    ########################################################################
    '''
    
    def __init__(self,parent,MultiPlotCanvas):

        #store local
        self.Parent = parent
        self.MultiPlotCanvas = MultiPlotCanvas
    
        #variabmes
        self.Verbose = True
        self.WindowUp = False

    def Creator(self):

        '''
        ########################################################################
        Create the window
        ########################################################################
        '''
        
        if self.WindowUp:
            
            #bring it to the front
            self.Window.lift()
            
            #focus it now
            self.Window.focus()
            #exit the function
            return
        
        
        if self.Verbose:
            print 'I was here'
        
        #create the window
        self.Window = Toplevel(self.Parent)
        
        #set the frame
        self.frame = ttk.Frame(self.Window, padding = '10p')
        
        #create the class
        self.WindowFrame = SettingWindow(self.Parent,self.MultiPlotCanvas,self.frame)
        
        #populate it
        self.WindowFrame.PopulateMainFrame()
        
        #call the notebook
        self.frame.grid(row = 0, column = 0, sticky= E+W+N+S)
        
        #give weight
        self.frame.grid_columnconfigure(0,weight = 1)
        self.frame.grid_rowconfigure(1,weight = 1)
    
        #give weight...
        self.Window.grid_columnconfigure(0, weight = 1)
        self.Window.grid_rowconfigure(   0, weight = 1)
        
        #set some basic properties
        self.Window.title('Settings')

        #link the destruciton method
        self.Window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        #set the boolean
        self.WindowUp = True

    def on_closing(self):
        '''
        ########################################################################
        This method is only called when the user closes thewindow
        ########################################################################
        '''
        
        if self.Verbose:
            print 'Destroy...'
        
        #set the creation boolean to 0
        self.WindowUp = False

        del self.WindowFrame
    
        self.Window.destroy()


class SettingWindow:
    
    def __init__(self,parent,MultiPlotCanvas,frame):

        #store local
        self.Parent = parent
        self.MultiPlotCanvas = MultiPlotCanvas
    
        #variabmes
        self.Verbose    = True
        self.frame      = frame
        self.All        = False
    
        #Link the classes
        self.AxesSettingClass       = SettingWindowAxes()
        self.TicksSettingClass      = SettingWindowTicks()
        self.PointerSettingClass    = SettingWindowPointer()
        self.DataSettingClass       = SettingWindowData()
        self.SaveSettingClass       = SettingWindowSave()

    def PopulateMainFrame(self):
        '''
        ########################################################################
        This will create the container frame with a subplot selector method
        ########################################################################
        '''
        ####################
        #Selector frame
        self.SelectorTopFrame = ttk.Frame(self.frame)
        
        #initialise the lsit
        self.List = []
        
        #Initialise
        self.Current = 0
        
        #create the selector list
        for i in range(0,len(self.MultiPlotCanvas.Frames)):
        
            self.List.append('Subplot '+str(i))
        
        self.List.append('All Subplots')
        
        #create the associated list variable
        self.SelectorVar = StringVar()
        
        if self.Verbose:
        
            print 'This is the Selector list ',self.List
        
        #create the drop down
        self.SelectorDrop = ttk.OptionMenu(self.SelectorTopFrame,
                                           self.SelectorVar,
                                           self.List[0],
                                           *self.List,
                                           command = self.SelectSubPlot)
        
        #create the label
        self.SelectorLabel_0 = ttk.Label(self.SelectorTopFrame,
                                         text = 'Specify the Subplot :',
                                         justify = RIGHT)
            
        #Place the items
        self.SelectorDrop.grid(row = 0, column = 1,sticky= E+W)
        self.SelectorLabel_0.grid(row = 0, column = 0,sticky= E+W)
            
        #give weight
        self.SelectorTopFrame.grid_columnconfigure(0,weight = 1)
        self.SelectorTopFrame.grid_columnconfigure(1,weight = 1)
            
        #place the selector frame
        self.SelectorTopFrame.grid(row = 0, column = 0)
            
        ####################
        #content frame
        self.SelectorBotFrame = ttk.Frame(self.frame)
        
        #make notebook array at the same time
        self.NoteBooks = []
        
        #create the selector list
        self.BuildNoteBooks(self.SelectorBotFrame,SubPlot = self.Current)

        #place the selector frame
        self.SelectorBotFrame.grid(row = 1, column = 0, sticky= E+W+N+S)
        
        #give weight
        self.SelectorBotFrame.grid_columnconfigure(0,weight = 1)
        self.SelectorBotFrame.grid_rowconfigure(0,weight = 1)

        ####################
        #Apply frames
        self.ButtonBotFrame = ttk.Frame(self.frame)
            
        self.CloseButton = ttk.Button(self.ButtonBotFrame,
                                      command = self.Close,
                                      text = 'Close')
                                      
        self.ResetButton = ttk.Button(self.ButtonBotFrame,
                                      command = self.Reset,
                                      text = 'Reset')
                                      
        self.ApplyButton = ttk.Button(self.ButtonBotFrame,
                                      command = self.Apply,
                                      text = 'Apply')
                                      
        
        self.CloseButton.grid(row = 0, column = 1, sticky= E+W+N+S)
        self.ResetButton.grid(row = 0, column = 2, sticky= E+W+N+S)
        self.ApplyButton.grid(row = 0, column = 3, sticky= E+W+N+S)
        
        #place the selector frame
        self.ButtonBotFrame.grid(row = 2, column = 0, sticky= E+W+N+S)
        
        #give weight
        self.ButtonBotFrame.grid_columnconfigure(0,weight = 1)

    def SelectSubPlot(self,val):
        '''
        ####################################################################################
        This method sends out self.current and changes its value. Note that the Selector
        found thourgh an interation though the list
        ####################################################################################    
        '''
        
        #for debuging
        if self.Verbose:
        
            print 'This is the selector: ',val
        
        #the user wants all or specific subplot
        if val == 'All Subplots':
            
            self.Current = 0
            self.All     = True
        
        else:
        
            for i in range(0,len(self.List)):
        
                if self.List[i] == val:

                    self.Current = i
                    break
            self.All = False
    
        self.Update()
    
    def Close(self):
    
        '''
        ####################################################################################
        Window closing method
        ####################################################################################    
        '''
        
        if self.Verbose:
        
            print 'Entered the closing method'

    def Reset(self):
    
        '''
        ####################################################################################
        Window closing method
        ####################################################################################    
        '''
        
        if self.Verbose:
        
            print 'Entered the Reset method'

        if not self.All:
            
            #the axes
            self.MultiPlotCanvas.Objects[self.MultiPlotCanvas.ObjectCoordinates[self.Current][0]][self.MultiPlotCanvas.ObjectCoordinates[self.Current][1]][0].Drawer.Axes.SetInitial()
            
            #the axes
            self.MultiPlotCanvas.Objects[self.MultiPlotCanvas.ObjectCoordinates[self.Current][0]][self.MultiPlotCanvas.ObjectCoordinates[self.Current][1]][0].Drawer.Pointer.SetInitial()
            
        
            #redraw
            self.MultiPlotCanvas.Objects[self.MultiPlotCanvas.ObjectCoordinates[self.Current][0]][self.MultiPlotCanvas.ObjectCoordinates[self.Current][1]][0].Drawer.Zoom()
                
            #regrab the info
            self.Update()
        
        else:
        
            for i in range(0,len(self.List)-1):
        
                #the axes
                self.MultiPlotCanvas.Objects[self.MultiPlotCanvas.ObjectCoordinates[i][0]][self.MultiPlotCanvas.ObjectCoordinates[i][1]][0].Drawer.Axes.SetInitial()
            
                #the axes
                self.MultiPlotCanvas.Objects[self.MultiPlotCanvas.ObjectCoordinates[i][0]][self.MultiPlotCanvas.ObjectCoordinates[i][1]][0].Drawer.Pointer.SetInitial()
        
                #redraw
                self.MultiPlotCanvas.Objects[self.MultiPlotCanvas.ObjectCoordinates[i][0]][self.MultiPlotCanvas.ObjectCoordinates[i][1]][0].Drawer.Zoom()

    
    def Apply(self):
    
        '''
        ####################################################################################
        Window closing method
        ####################################################################################    
        '''
        
        if self.Verbose:
        
            print 'Entered the Appy method'
        
        if not self.All:
            
            #the axes
            self.AxesSettingClass.SubmitAxesSetting(self.MultiPlotCanvas.Objects[self.MultiPlotCanvas.ObjectCoordinates[self.Current][0]][self.MultiPlotCanvas.ObjectCoordinates[self.Current][1]][0].Drawer)
            
            #the axes
            self.TicksSettingClass.SubmitTicksSetting(self.MultiPlotCanvas.Objects[self.MultiPlotCanvas.ObjectCoordinates[self.Current][0]][self.MultiPlotCanvas.ObjectCoordinates[self.Current][1]][0].Drawer)
            
            #the Pointer
            self.PointerSettingClass.SubmitPointerSetting(self.MultiPlotCanvas.Objects[self.MultiPlotCanvas.ObjectCoordinates[self.Current][0]][self.MultiPlotCanvas.ObjectCoordinates[self.Current][1]][0].Drawer)
            
            #the Pointer
            self.DataSettingClass.SubmitDataSetting(self.MultiPlotCanvas.Objects[self.MultiPlotCanvas.ObjectCoordinates[self.Current][0]][self.MultiPlotCanvas.ObjectCoordinates[self.Current][1]][0].Drawer)
        
            #redraw
            self.MultiPlotCanvas.Objects[self.MultiPlotCanvas.ObjectCoordinates[self.Current][0]][self.MultiPlotCanvas.ObjectCoordinates[self.Current][1]][0].Drawer.Zoom()
        
        else:
        
            for i in range(0,len(self.List)-1):
        
                #the axes
                self.AxesSettingClass.SubmitAxesSetting(self.MultiPlotCanvas.Objects[self.MultiPlotCanvas.ObjectCoordinates[i][0]][self.MultiPlotCanvas.ObjectCoordinates[i][1]][0].Drawer)
            
                #the axes
                self.TicksSettingClass.SubmitTicksSetting(self.MultiPlotCanvas.Objects[self.MultiPlotCanvas.ObjectCoordinates[i][0]][self.MultiPlotCanvas.ObjectCoordinates[i][1]][0].Drawer)
                
                #the Pointer
                self.PointerSettingClass.SubmitPointerSetting(self.MultiPlotCanvas.Objects[self.MultiPlotCanvas.ObjectCoordinates[i][0]][self.MultiPlotCanvas.ObjectCoordinates[i][1]][0].Drawer)
        
                #redraw
                self.MultiPlotCanvas.Objects[self.MultiPlotCanvas.ObjectCoordinates[i][0]][self.MultiPlotCanvas.ObjectCoordinates[i][1]][0].Drawer.Zoom()

    def BuildNoteBooks(self, TargetFrame, SubPlot = 0):
        '''
        ####################################################################################
        This builds the notebook
        
        The filling of the pages will be done by BuildSettingFrame that will chose the 
        content depending on the target
        ####################################################################################    
        '''
        #add notebook capabilities into this frame
        self.NoteBookFrame = ttk.Frame(TargetFrame)
        
        self.NoteBook = ttk.Notebook(self.NoteBookFrame)
        
        #build all small frames...
        self.NoteBookPage  = []
        self.NoteBookTitle = ['Axes','Ticks','Pointer','Data','Save']
        
        #grab the frames
        for j in range(0,len(self.NoteBookTitle)):
            
            self.NoteBookPage.append(self.BuildSettingFrame(self.NoteBookFrame,Title = self.NoteBookTitle[j]))

        #Build the notebooks
        for i in range(0,len(self.NoteBookTitle)):
            self.NoteBook.add(self.NoteBookPage[i],text = self.NoteBookTitle[i] )
        
        #We call the population routine putting all butons and entry fields
        self.NoteBook.grid(row = 0, column = 0, sticky = E+W+N+S)
        
        #give weight...
        self.NoteBookFrame.grid_columnconfigure(0, weight = 1)
        self.NoteBookFrame.grid_rowconfigure(0, weight = 1)
        
        #Place the frame into the main frame...
        self.NoteBookFrame.grid(row = 0 ,column = 0 , sticky = E+W+N+S)

    def BuildSettingFrame(self,Target, Title = ''):
        '''
        ####################################################################################
        This dispatcher send the proper builder out...
        ####################################################################################    
        '''
        #create the frame
        ReturnFrame = ttk.Frame(Target, padding = '10p')
        
        #the system asks for axes
        if Title == 'Axes':
        
            ReturnFrame = self.AxesSettingClass.BuildAxesSetting(ReturnFrame)
        
            self.AxesSettingClass.CatchAxesSetting(self.MultiPlotCanvas.Objects[self.MultiPlotCanvas.ObjectCoordinates[self.Current][0]][self.MultiPlotCanvas.ObjectCoordinates[self.Current][1]][0].Drawer)
        
        #the system asks for axes
        if Title == 'Ticks':
        
            ReturnFrame = self.TicksSettingClass.BuildTicksSetting(ReturnFrame)
        
            self.TicksSettingClass.CatchTickSetting(self.MultiPlotCanvas.Objects[self.MultiPlotCanvas.ObjectCoordinates[self.Current][0]][self.MultiPlotCanvas.ObjectCoordinates[self.Current][1]][0].Drawer)
        
        #the system asks for axes
        if Title == 'Pointer':
        
            ReturnFrame = self.PointerSettingClass.BuildPointerSetting(ReturnFrame)
        
            self.PointerSettingClass.CatchPointerSetting(self.MultiPlotCanvas.Objects[self.MultiPlotCanvas.ObjectCoordinates[self.Current][0]][self.MultiPlotCanvas.ObjectCoordinates[self.Current][1]][0].Drawer)
        
        #the system asks for axes
        if Title == 'Data':
        
            ReturnFrame = self.DataSettingClass.BuildDataSetting(ReturnFrame)
        
            self.DataSettingClass.CatchDataSetting(self.MultiPlotCanvas.Objects[self.MultiPlotCanvas.ObjectCoordinates[self.Current][0]][self.MultiPlotCanvas.ObjectCoordinates[self.Current][1]][0].Drawer,ReturnFrame)
        
        #the system asks for axes
        if Title == 'Save':
        
            ReturnFrame = self.SaveSettingClass.BuildSaveSetting(ReturnFrame)
        
            self.SaveSettingClass.CatchSaveSetting(self.MultiPlotCanvas.Objects[self.MultiPlotCanvas.ObjectCoordinates[self.Current][0]][self.MultiPlotCanvas.ObjectCoordinates[self.Current][1]][0].Drawer)
        
        return ReturnFrame

    def Update(self):
        '''
        ####################################################################################
        This dispatcher send the proper builder out...
        ####################################################################################    
        '''
        
        self.AxesSettingClass.CatchAxesSetting(self.MultiPlotCanvas.Objects[self.MultiPlotCanvas.ObjectCoordinates[self.Current][0]][self.MultiPlotCanvas.ObjectCoordinates[self.Current][1]][0].Drawer)
        
        self.TicksSettingClass.CatchTickSetting(self.MultiPlotCanvas.Objects[self.MultiPlotCanvas.ObjectCoordinates[self.Current][0]][self.MultiPlotCanvas.ObjectCoordinates[self.Current][1]][0].Drawer)

        self.PointerSettingClass.CatchPointerSetting(self.MultiPlotCanvas.Objects[self.MultiPlotCanvas.ObjectCoordinates[self.Current][0]][self.MultiPlotCanvas.ObjectCoordinates[self.Current][1]][0].Drawer)

        self.DataSettingClass.CatchDataSetting(self.MultiPlotCanvas.Objects[self.MultiPlotCanvas.ObjectCoordinates[self.Current][0]][self.MultiPlotCanvas.ObjectCoordinates[self.Current][1]][0].Drawer,self.NoteBookPage[3])

        self.SaveSettingClass.CatchSaveSetting(self.MultiPlotCanvas.Objects[self.MultiPlotCanvas.ObjectCoordinates[self.Current][0]][self.MultiPlotCanvas.ObjectCoordinates[self.Current][1]][0].Drawer)

class SettingWindowSave:
    
    def __init__(self):
        
        #set initial path
        self.Path = ''
        
        #set the directory method
        self.dir_opt = options = {}
        options['initialdir'] = os.path.dirname(os.path.realpath(__file__))
        options['mustexist'] = False
        #options['parent'] = Window
        options['title'] = 'This is a title'

        #variabmes
        self.Verbose    = True

    def BuildSaveSetting(self,Target):
        '''
        ####################################################################################
        This will populatethe frame with the widgets for the Awes class
        ####################################################################################    
        '''
        ####################################################################################
        #create arrays
        self.RowOffset          = 1
        self.ColumnOffset       = 1
        
        self.ColumnWeight       = [1,0,0,0,0,0,1]
        
        self.AxesLabelList      = [None]*20
        self.PaddingInEntries   = [None]*4
        self.PaddingOutEntries  = [None]*4
        
        #to allow for simple for loop proceeding
        # [Element, row, column, sticky]
        self.PoisitionMatrix = []
        
        ##############################
        #Build Padding Header
        self.PoisitionMatrix.append([ttk.Button(Target,
                                                text = 'Select Path',
                                                command = self.SelectDir),
                                     0+self.RowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
                                     
        self.DirLabel = ttk.Label(Target,
                                  text='No Path selected yet',
                                  justify=LEFT,
                                  wraplength = 200
                                  )
                                  
        self.PoisitionMatrix.append([self.DirLabel,
                                     0+self.RowOffset,
                                     1+self.ColumnOffset,
                                     N+S+E+W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Name:',
                                               anchor = E,
                                               font = tkFont.Font(weight = 'bold',
                                                                  underline = 0)),
                                     1+self.RowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
                                     
        self.NameEntry = ttk.Entry(Target)
        
        self.PoisitionMatrix.append([self.NameEntry,
                                     1+self.RowOffset,
                                     1+self.ColumnOffset,
                                     E+W,1,1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Format:',
                                               anchor = E,
                                               font = tkFont.Font(weight = 'bold',
                                                                  underline = 0)),
                                     2+self.RowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = '.eps',
                                               anchor = W,
                                               font = tkFont.Font(weight = 'bold',
                                                                  underline = 0)),
                                     2+self.RowOffset,
                                     1+self.ColumnOffset,
                                     E+W,1,1])
                                     
        self.PoisitionMatrix.append([ttk.Button(Target,
                                               text = 'Save',
                                                command = self.SaveImage),
                                     3+self.RowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,2])
        
        #place everything
        for i in range(0,len(self.PoisitionMatrix)):
        
            self.PoisitionMatrix[i][0].grid(row         =  self.PoisitionMatrix[i][1],
                                            column      =  self.PoisitionMatrix[i][2],
                                            sticky      =  self.PoisitionMatrix[i][3],
                                            rowspan     =  self.PoisitionMatrix[i][4],
                                            columnspan  =  self.PoisitionMatrix[i][5])
        
        #cofigure all
        for i in range(0,len(self.ColumnWeight)):
        
            Target.grid_columnconfigure(i,weight =self.ColumnWeight[i])
        
        return Target

    def CatchSaveSetting(self,Object):
        '''
        ######################################################
        Catches the settings from the subplot variable and
        sends it back to the Entry fields and the checkbuttons
        
        The object hsould be given by the multiplot and is the
        associated object element
        ######################################################
        '''
        #make the object locally available
        self.Object = Object
        
        #delete entry content
        self.NameEntry.delete(0,END)

        #fill entry content
        self.NameEntry.insert(0,'SubPlot_'+str(Object.ID))

    def SaveImage(self):
        '''
        ######################################################
        Catches the settings from the subplot variable and
        sends it back to the Entry fields and the checkbuttons
        
        The object hsould be given by the multiplot and is the
        associated object element
        ######################################################
        '''
    
        #send it out to the appropriate method
        self.Object.Save(FileName = os.path.join(self.Path,self.NameEntry.get()+'.eps'))
    
    def SelectDir(self):
        '''
        ######################################################
        This selects the directoy string
        ######################################################
        '''
        #ask
        DirName =  tkFileDialog.askdirectory(**self.dir_opt)
    
        #set
        self.DirLabel.configure(text = DirName)
    
    def SubmitSaveSetting(self,Object):
        '''
        ######################################################
        Catches the settings from the subplot variable and
        sends it back to the Entry fields and the checkbuttons
        
        The object hsould be given by the multiplot and is the
        associated object element
        ######################################################
        '''
        pass



class SettingWindowAxes:
    
    def __init__(self):

        #variabmes
        self.Verbose    = True

    def BuildAxesSetting(self,Target):
        '''
        ####################################################################################
        This will populatethe frame with the widgets for the Awes class
        ####################################################################################    
        '''
        ####################################################################################
        #create arrays
        self.RowOffset          = 1
        self.ColumnOffset       = 1
        
        self.ColumnWeight       = [1,0,0,0,0,0,1]
        
        self.AxesLabelList      = [None]*20
        self.PaddingInEntries   = [None]*4
        self.PaddingOutEntries  = [None]*4
        
        #to allow for simple for loop proceeding
        # [Element, row, column, sticky]
        self.PoisitionMatrix = []
        
        ##############################
        #Build Padding Header
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Padding:',
                                               anchor = W,
                                               font = tkFont.Font(weight = 'bold',
                                                                  underline = 0)),
                                     0+self.RowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Left',
                                               anchor = CENTER),
                                     1+self.RowOffset,
                                     1+self.ColumnOffset,
                                     E+W,1,1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Bottom',
                                               anchor = CENTER),
                                     1+self.RowOffset,
                                     2+self.ColumnOffset,
                                     E+W,1,1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Right',
                                               anchor = CENTER),
                                     1+self.RowOffset,
                                     3+self.ColumnOffset,
                                     E+W,1,1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Top',
                                               anchor = CENTER),
                                     1+self.RowOffset,
                                     4+self.ColumnOffset,
                                     E+W,1,1])
                                     
        ##############################
        #Build Padding out
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Outside: ',
                                               anchor = E),
                                     2+self.RowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
        
        for i in range(0,4):
        
            #create the entry
            self.PaddingOutEntries[i] = ttk.Entry(Target,
                                                  width = 5,
                                                  font=("Helvetica",12))
                                                  
            self.PoisitionMatrix.append([self.PaddingOutEntries[i],
                                         2+self.RowOffset,
                                         i+1+self.ColumnOffset,
                                         E+W,1,1])
        
        ##############################
        #Build Padding in
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Inside: ',
                                               anchor = E),
                                     3+self.RowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
        
        for i in range(0,4):
        
            #create the entry
            self.PaddingInEntries[i] = ttk.Entry(Target,
                                                 width = 5,
                                                 font=("Helvetica",12))
                                                 
            self.PoisitionMatrix.append([self.PaddingInEntries[i],
                                         3+self.RowOffset,
                                         i+1+self.ColumnOffset,
                                         E+W,1,1])
        
        ##############################
        #Toggle header
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = '',
                                               anchor = CENTER),
                                     4+self.RowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Axis:',
                                               anchor = W,
                                               font = tkFont.Font(weight = 'bold',
                                                                  underline = 0)),
                                     5+self.RowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
        
        ################################
        #Build the element entry fields
        self.AxisOnOff   = [None]*4
        self.AxisOnOffVal = [IntVar(),IntVar(),IntVar(),IntVar()]
        
        for i in range(0,len(self.AxisOnOff)):
        
        
            #create the entry
            self.AxisOnOff[i] = ttk.Checkbutton(Target,
                                                variable = self.AxisOnOffVal[i])
                                                 
            self.PoisitionMatrix.append([self.AxisOnOff[i],
                                        5+self.RowOffset,
                                        1+i+self.ColumnOffset,
                                        E+W,1,1])
        

        ##############################
        #Toggle header
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = '',
                                               anchor = CENTER),
                                     6+self.RowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Imaging mode:',
                                               anchor = W,
                                               font = tkFont.Font(weight = 'bold',
                                                                  underline = 0)),
                                     7+self.RowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
                                     
        #initialise the variable
        self.ImagingType        = StringVar()
        
        #create the two lists
        self.ImagingTypeList        = ['PIL assisted',
                                       'Tk Canvas imaging',
                                       'PyGame assisted']
                                       
        #Create the two elements
        self.ImagingTypeDrop = ttk.OptionMenu(Target,
                                              self.ImagingType,
                                              self.ImagingTypeList[0],
                                              *self.ImagingTypeList)
                                              
        self.PoisitionMatrix.append([self.ImagingTypeDrop,
                                     7+self.RowOffset,
                                     1+self.ColumnOffset,
                                     E+W,1,4])
                                     
        
        
        ####################################################################################
        
        #place everything
        for i in range(0,len(self.PoisitionMatrix)):
        
            self.PoisitionMatrix[i][0].grid(row         =  self.PoisitionMatrix[i][1],
                                            column      =  self.PoisitionMatrix[i][2],
                                            sticky      =  self.PoisitionMatrix[i][3],
                                            rowspan     =  self.PoisitionMatrix[i][4],
                                            columnspan  =  self.PoisitionMatrix[i][5])
        
        #cofigure all
        for i in range(0,len(self.ColumnWeight)):
        
            Target.grid_columnconfigure(i,weight =self.ColumnWeight[i])
        
        return Target

    def CatchAxesSetting(self,Object):
        '''
        ######################################################
        Catches the settings from the subplot variable and
        sends it back to the Entry fields and the checkbuttons
        
        The object hsould be given by the multiplot and is the
        associated object element
        ######################################################
        '''

        #if the subplot is empty pass
        if Object == '':

            return
        
        #logging purpose
        if self.Verbose:
        
            print 'Tried to catch'



        ##############################
        #Build Padding out
        
        for i in range(0,4):
        
            #delete entry content
            self.PaddingOutEntries[i].delete(0,END)

            #fill entry content
            self.PaddingOutEntries[i].insert(0,str(Object.Axes.PaddingOut[i]))

        ##############################
        #Build Padding in
        
        for i in range(0,4):
        
            #delete entry content
            self.PaddingInEntries[i].delete(0,END)

            #fill entry content
            self.PaddingInEntries[i].insert(0,str(Object.Axes.PaddingIn[i]))

        ##############################
        #Set the logical variables for the ticks
        if Object.Axes.Type[0]:
            
            #set var
            self.AxisOnOffVal[0].set(1)
            
            #set button state
            self.AxisOnOff[0].state(['selected'])

        else:
            
            #set var
            self.AxisOnOffVal[0].set(0)
            
            #set button state
            self.AxisOnOff[0].state(['!selected'])

        if Object.Axes.Type[1]:
            
            #set var
            self.AxisOnOffVal[1].set(1)
            
            #set button state
            self.AxisOnOff[1].state(['selected'])

        else:
            
            #set var
            self.AxisOnOffVal[1].set(0)
            
            #set button state
            self.AxisOnOff[1].state(['!selected'])

        if Object.Axes.Type[2]:
            
            #set var
            self.AxisOnOffVal[2].set(1)
            
            #set button state
            self.AxisOnOff[2].state(['selected'])

        else:
            
            #set var
            self.AxisOnOffVal[2].set(0)
            
            #set button state
            self.AxisOnOff[2].state(['!selected'])

        if Object.Axes.Type[3]:
            
            #set var
            self.AxisOnOffVal[3].set(1)
            
            #set button state
            self.AxisOnOff[3].state(['selected'])

        else:
            
            #set var
            self.AxisOnOffVal[3].set(0)
            
            #set button state
            self.AxisOnOff[3].state(['!selected'])

        self.ImagingType.set(self.ImagingTypeList[Object.Live])
#
#        #delete entry content
#        self.TickPointer[0][0].delete(0,END)
#
#        #fill entry content
#        self.TickPointer[0][0].insert(0,str(Object.Axes.XTickHeight))
#
#        #delete entry content
#        self.TickPointer[0][1].delete(0,END)
#
#        #fill entry content
#        self.TickPointer[0][1].insert(0,str(Object.Axes.XTickThickness))
#
#        #delete entry content
#        self.TickPointer[0][2].delete(0,END)
#
#        #fill entry content
#        self.TickPointer[0][2].insert(0,str(Object.Axes.XTickColor))
#
#        #delete entry content
#        self.TickPointer[1][0].delete(0,END)
#
#        #fill entry content
#        self.TickPointer[1][0].insert(0,str(Object.Axes.YTickHeight))
#
#        #delete entry content
#        self.TickPointer[1][1].delete(0,END)
#
#        #fill entry content
#        self.TickPointer[1][1].insert(0,str(Object.Axes.YTickThickness))
#
#        #delete entry content
#        self.TickPointer[1][2].delete(0,END)
#
#        #fill entry content
#        self.TickPointer[1][2].insert(0,str(Object.Axes.YTickColor))


    def SubmitAxesSetting(self,Object):
        '''
        ######################################################
        Catches the settings from the subplot variable and
        sends it back to the Entry fields and the checkbuttons
        
        The object hsould be given by the multiplot and is the
        associated object element
        ######################################################
        '''

        #if the subplot is empty pass
        if Object == '':

            return
        
        #logging purpose
        if self.Verbose:
        
            print 'Tried to catch'



        ##############################
        #Build Padding out
        
        for i in range(0,4):

            #fill entry content
            Object.Axes.PaddingOut[i] = float(self.PaddingOutEntries[i].get())

        ##############################
        #Build Padding in
        
        for i in range(0,4):

            #fill entry content
            Object.Axes.PaddingIn[i] = float(self.PaddingInEntries[i].get())

        ##############################
        #Set the logical variables for the ticks
        if self.AxisOnOffVal[0].get() == 1:
            
            #set var
            Object.Axes.Type[0] = True

        else:
            
            #set var
            Object.Axes.Type[0] = False

        if self.AxisOnOffVal[1].get() == 1:
            
            #set var
            Object.Axes.Type[1] = True

        else:
            
            #set var
            Object.Axes.Type[1] = False

        if self.AxisOnOffVal[2].get() == 1:
            
            #set var
            Object.Axes.Type[2] = True

        else:
            
            #set var
            Object.Axes.Type[2] = False

        if self.AxisOnOffVal[3].get() == 1:
            
            #set var
            Object.Axes.Type[3] = True

        else:
            
            #set var
            Object.Axes.Type[3] = False

        for i in range(0, len(self.ImagingTypeList)):
        
            if self.ImagingTypeList[i] == self.ImagingType.get():
        
                Object.Live = i
                break



#        #fill entry content
#        Object.Axes.XTickHeight = float(self.TickPointer[0][0].get())
#
#        #fill entry content
#        Object.Axes.XTickThickness = float(self.TickPointer[0][1].get())
#
#        #fill entry content
#        Object.Axes.XTickColor = self.TickPointer[0][2].get()
#
#        #fill entry content
#        Object.Axes.YTickHeight = float(self.TickPointer[1][0].get())
#
#        #fill entry content
#        Object.Axes.YTickThickness = float(self.TickPointer[1][1].get())
#
#        #fill entry content
#        Object.Axes.YTickColor = self.TickPointer[1][2].get()


class SettingWindowTicks:
    
    def __init__(self):

        #variabmes
        self.Verbose    = True

    def BuildTicksSetting(self,Target):
        '''
        ####################################################################################
        This will populatethe frame with the widgets for the Awes class
        ####################################################################################    
        '''
        ####################################################################################
        #create arrays
        self.RowOffset          = 1
        self.ColumnOffset       = 1
        
        self.ColumnWeight       = [1,0,0,0,0,0,1]
        
        #to allow for simple for loop proceeding
        # [Element, row, column, sticky]
        self.PoisitionMatrix = []
        
        ####################################################################################
        self.TicksRowOffset = 1
        
        ##############################
        #Tick header
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Tick Style',
                                               anchor = W,
                                               font = tkFont.Font(weight = 'bold',
                                                                  underline = 0)),
                                     2+self.RowOffset+self.TicksRowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
                                    
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'On/Off',
                                               anchor = CENTER),
                                     3+self.RowOffset+self.TicksRowOffset,
                                     1+self.ColumnOffset,
                                     E+W,1,2])
                                    
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Length',
                                               anchor = CENTER),
                                     3+self.RowOffset+self.TicksRowOffset,
                                     3+self.ColumnOffset,
                                     E+W,1,1])
                                    
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Width',
                                               anchor = CENTER),
                                     3+self.RowOffset+self.TicksRowOffset,
                                     4+self.ColumnOffset,
                                     E+W,1,1])
                                    
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Left Y',
                                               anchor = CENTER),
                                     4+self.RowOffset+self.TicksRowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
                                    
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Right Y',
                                               anchor = CENTER),
                                     5+self.RowOffset+self.TicksRowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
                                    
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Top X',
                                               anchor = CENTER),
                                     6+self.RowOffset+self.TicksRowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
                                    
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Bot X',
                                               anchor = CENTER),
                                     7+self.RowOffset+self.TicksRowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
 
                                     
        ################################
        #Build the element entry fields
        self.TickOnOff   = [None]*4
        self.TickOnOffVal = [IntVar(),IntVar(),IntVar(),IntVar()]
        
        for i in range(0,len(self.TickOnOff)):
        
        
            #create the entry
            self.TickOnOff[i] = ttk.Checkbutton(Target,
                                                variable = self.TickOnOffVal[i])
                                                 
            self.PoisitionMatrix.append([self.TickOnOff[i],
                                        4+i+self.RowOffset+self.TicksRowOffset,
                                        1+self.ColumnOffset,
                                        E+W,1,1])


        ################################
        #Build the color selector fields
        self.TickColor = [None]*4
        
        self.TickColor[0] = ColorCanvas(Target)
        
        self.TickColor[1] = ColorCanvas(Target)
        
        self.TickColor[2] = ColorCanvas(Target)
        
        self.TickColor[3] = ColorCanvas(Target)
        
        for i in range(0,len(self.TickColor)):
            
            self.PoisitionMatrix.append([self.TickColor[i],
                                         4+i+self.RowOffset+self.TicksRowOffset,
                                         2+self.ColumnOffset,
                                         E+W,1,1])
        
        self.TickPointer = [None]*2
        
        self.TickPointer[0] = self.TicksX = [None]*2
        self.TickPointer[1] = self.TicksY = [None]*2
        
        ####################################################################################
        for i in range(0,len(self.TickPointer)):
        
            for j in range(0,len(self.TickPointer[i])):
                
                #create the entry
                self.TickPointer[i][j] = ttk.Entry(Target,
                                                    width = 5,
                                                    font=("Helvetica",12))
                                                 
                self.PoisitionMatrix.append([self.TickPointer[i][j],
                                             4+2*i+self.RowOffset++self.TicksRowOffset,
                                             j+3+self.ColumnOffset,
                                             E+W,
                                             2,
                                             1])
    
        ##############################
        #Toggle header
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = '',
                                               anchor = CENTER),
                                     10+self.RowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Label',
                                               anchor = W,
                                               font = tkFont.Font(weight = 'bold',
                                                                  underline = 0)),
                                     11+self.RowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'On/Off',
                                               anchor = CENTER),
                                     11+self.RowOffset,
                                     1+self.ColumnOffset,
                                     E+W,1,2])
                                    
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Size',
                                               anchor = CENTER),
                                     11+self.RowOffset,
                                     3+self.ColumnOffset,
                                     E+W,1,1])
                                    
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Font',
                                               anchor = CENTER),
                                     11+self.RowOffset,
                                     4+self.ColumnOffset,
                                     E+W,1,1])

        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Left Y',
                                               anchor = CENTER),
                                     12+self.RowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
                                    
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Right Y',
                                               anchor = CENTER),
                                     13+self.RowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
                                    
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Top X',
                                               anchor = CENTER),
                                     14+self.RowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
                                    
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Bot X',
                                               anchor = CENTER),
                                     15+self.RowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
        
        ################################
        #Build the element entry fields
        self.LabelOnOff   = [None]*4
        self.LabelOnOffVal = [IntVar(),IntVar(),IntVar(),IntVar()]
        
        for i in range(0,len(self.LabelOnOff)):
        
        
            #create the entry
            self.LabelOnOff[i] = ttk.Checkbutton(Target,
                                                variable = self.LabelOnOffVal[i])
                                                 
            self.PoisitionMatrix.append([self.LabelOnOff[i],
                                        12+i+self.RowOffset,
                                        1+self.ColumnOffset,
                                        E+W,1,1])
        
        ################################
        #Build the color selector fields
        self.LabelColor = [None]*4
        
        self.LabelColor[0] = ColorCanvas(Target)
        
        self.LabelColor[1] = ColorCanvas(Target)
        
        self.LabelColor[2] = ColorCanvas(Target)
        
        self.LabelColor[3] = ColorCanvas(Target)
        
        for i in range(0,len(self.LabelColor)):
            
            self.PoisitionMatrix.append([self.LabelColor[i],
                                         12+i+self.RowOffset,
                                         2+self.ColumnOffset,
                                         E+W,1,1])

        ################################
        #Put font and size entry fields
        self.SizeEntry   = [None]*4
        
        for i in range(0,len(self.SizeEntry)):
        
        
            #create the entry
            self.SizeEntry[i] = ttk.Entry(Target,
                                          width = 5,
                                          font=("Helvetica",12))
                                          
            self.PoisitionMatrix.append([self.SizeEntry[i],
                                         12+i+self.RowOffset,
                                         3+self.ColumnOffset,
                                         E+W,1,1])

        ################################
        #Put font and size entry fields
        self.FontEntry   = [None]*4
        
        for i in range(0,len(self.FontEntry)):
        
        
            #create the entry
            self.FontEntry[i] = ttk.Entry(Target,
                                          width = 8,
                                          font=("Helvetica",12))
                                          
            self.PoisitionMatrix.append([self.FontEntry[i],
                                         12+i+self.RowOffset,
                                         4+self.ColumnOffset,
                                         E+W,1,1])

        ####################################################################################
        
        #place everything
        for i in range(0,len(self.PoisitionMatrix)):
        
            self.PoisitionMatrix[i][0].grid(row         =  self.PoisitionMatrix[i][1],
                                            column      =  self.PoisitionMatrix[i][2],
                                            sticky      =  self.PoisitionMatrix[i][3],
                                            rowspan     =  self.PoisitionMatrix[i][4],
                                            columnspan  =  self.PoisitionMatrix[i][5])

        #cofigure all
        for i in range(0,len(self.ColumnWeight)):
        
            Target.grid_columnconfigure(i,weight =self.ColumnWeight[i])
        
        return Target

    def CatchTickSetting(self,Object):
        '''
        ######################################################
        Catches the settings from the subplot variable and
        sends it back to the Entry fields and the checkbuttons
        
        The object hsould be given by the multiplot and is the
        associated object element
        ######################################################
        '''

        #if the subplot is empty pass
        if Object == '':

            return
        
        #logging purpose
        if self.Verbose:
        
            print 'Tried to catch'

        ##############################
        #Set the logical variables for the ticks
        if Object.Axes.TicksActiveGrid[0]:
            
            #set var
            self.TickOnOffVal[0].set(1)
            
            #set button state
            self.TickOnOff[0].state(['selected'])

        else:
            
            #set var
            self.TickOnOffVal[0].set(0)
            
            #set button state
            self.TickOnOff[0].state(['!selected'])

        if Object.Axes.TicksActiveGrid[2]:
            
            #set var
            self.TickOnOffVal[1].set(1)
            
            #set button state
            self.TickOnOff[1].state(['selected'])

        else:
            
            #set var
            self.TickOnOffVal[1].set(0)
            
            #set button state
            self.TickOnOff[1].state(['!selected'])

        if Object.Axes.TicksActiveGrid[3]:
            
            #set var
            self.TickOnOffVal[2].set(1)
            
            #set button state
            self.TickOnOff[2].state(['selected'])

        else:
            
            #set var
            self.TickOnOffVal[2].set(0)
            
            #set button state
            self.TickOnOff[2].state(['!selected'])

        if Object.Axes.TicksActiveGrid[1]:
            
            #set var
            self.TickOnOffVal[3].set(1)
            
            #set button state
            self.TickOnOff[3].state(['selected'])

        else:
            
            #set var
            self.TickOnOffVal[3].set(0)
            
            #set button state
            self.TickOnOff[3].state(['!selected'])
        
         ##############################
        #Set the logical variables for the ticks
        if Object.Axes.LabelsActiveGrid[0]:
            
            #set var
            self.LabelOnOffVal[0].set(1)
            
            #set button state
            self.LabelOnOff[0].state(['selected'])

        else:
            
            #set var
            self.LabelOnOffVal[0].set(0)
            
            #set button state
            self.LabelOnOff[0].state(['!selected'])

        if Object.Axes.LabelsActiveGrid[2]:
            
            #set var
            self.LabelOnOffVal[1].set(1)
            
            #set button state
            self.LabelOnOff[1].state(['selected'])

        else:
            
            #set var
            self.LabelOnOffVal[1].set(0)
            
            #set button state
            self.LabelOnOff[1].state(['!selected'])

        if Object.Axes.LabelsActiveGrid[3]:
            
            #set var
            self.LabelOnOffVal[2].set(1)
            
            #set button state
            self.LabelOnOff[2].state(['selected'])

        else:
            
            #set var
            self.LabelOnOffVal[2].set(0)
            
            #set button state
            self.LabelOnOff[2].state(['!selected'])

        if Object.Axes.LabelsActiveGrid[1]:
            
            #set var
            self.LabelOnOffVal[3].set(1)
            
            #set button state
            self.LabelOnOff[3].state(['selected'])

        else:
            
            #set var
            self.LabelOnOffVal[3].set(0)
            
            #set button state
            self.LabelOnOff[3].state(['!selected'])
        
        #delete entry content
        self.TickPointer[0][0].delete(0,END)

        #fill entry content
        self.TickPointer[0][0].insert(0,str(Object.Axes.XTickHeight))

        #delete entry content
        self.TickPointer[0][1].delete(0,END)

        #fill entry content
        self.TickPointer[0][1].insert(0,str(Object.Axes.XTickThickness))

        #delete entry content
        self.TickPointer[1][0].delete(0,END)

        #fill entry content
        self.TickPointer[1][0].insert(0,str(Object.Axes.YTickHeight))

        #delete entry content
        self.TickPointer[1][1].delete(0,END)

        #fill entry content
        self.TickPointer[1][1].insert(0,str(Object.Axes.YTickThickness))

        ############################
        #et the color framework
        
        self.TickColor[0].LoadColor(Object.Axes.YTickColor[0])
        self.TickColor[1].LoadColor(Object.Axes.YTickColor[1])
        self.TickColor[2].LoadColor(Object.Axes.YTickColor[1])
        self.TickColor[3].LoadColor(Object.Axes.YTickColor[0])
         
        self.LabelColor[0].LoadColor(Object.Axes.YLabelColor[0])
        self.LabelColor[1].LoadColor(Object.Axes.YLabelColor[1])
        self.LabelColor[2].LoadColor(Object.Axes.XLabelColor[0])
        self.LabelColor[3].LoadColor(Object.Axes.XLabelColor[1])

        #delete entry content
        self.SizeEntry[0].delete(0,END)

        #fill entry content
        self.SizeEntry[0].insert(0,str(Object.Axes.YLabelSize[0][1]))

        #delete entry content
        self.SizeEntry[1].delete(0,END)

        #fill entry content
        self.SizeEntry[1].insert(0,str(Object.Axes.YLabelSize[1][1]))
          
        #delete entry content
        self.SizeEntry[2].delete(0,END)

        #fill entry content
        self.SizeEntry[2].insert(0,str(Object.Axes.XLabelSize[0][1]))

        #delete entry content
        self.SizeEntry[3].delete(0,END)

        #fill entry content
        self.SizeEntry[3].insert(0,str(Object.Axes.XLabelSize[1][1]))
          
        #delete entry content
        self.FontEntry[0].delete(0,END)

        #fill entry content
        self.FontEntry[0].insert(0,str(Object.Axes.YLabelSize[0][0]))

        #delete entry content
        self.FontEntry[1].delete(0,END)

        #fill entry content
        self.FontEntry[1].insert(0,str(Object.Axes.YLabelSize[1][0]))
          
        #delete entry content
        self.FontEntry[2].delete(0,END)

        #fill entry content
        self.FontEntry[2].insert(0,str(Object.Axes.XLabelSize[0][0]))

        #delete entry content
        self.FontEntry[3].delete(0,END)

        #fill entry content
        self.FontEntry[3].insert(0,str(Object.Axes.XLabelSize[1][0]))
          
    def SubmitTicksSetting(self,Object):
        '''
        ######################################################
        Catches the settings from the subplot variable and
        sends it back to the Entry fields and the checkbuttons
        
        The object hsould be given by the multiplot and is the
        associated object element
        ######################################################
        '''

        #if the subplot is empty pass
        if Object == '':

            return
        
        #logging purpose
        if self.Verbose:
        
            print 'Tried to catch'

        ##############################
        #Set the logical variables for the ticks
        if self.TickOnOffVal[0].get() == 1:
            
            #set var
            Object.Axes.TicksActiveGrid[0] = True

        else:
            
            #set var
            Object.Axes.TicksActiveGrid[0] = False

        if self.TickOnOffVal[1].get() == 1:
            
            #set var
            Object.Axes.TicksActiveGrid[2] = True

        else:
            
            #set var
            Object.Axes.TicksActiveGrid[2] = False

        if self.TickOnOffVal[2].get() == 1:
            
            #set var
            Object.Axes.TicksActiveGrid[3] = True

        else:
            
            #set var
            Object.Axes.TicksActiveGrid[3] = False

        if self.TickOnOffVal[3].get() == 1:
            
            #set var
            Object.Axes.TicksActiveGrid[1] = True

        else:
            
            #set var
            Object.Axes.TicksActiveGrid[1] = False


        #fill entry content
        Object.Axes.XTickHeight = float(self.TickPointer[0][0].get())

        #fill entry content
        Object.Axes.XTickThickness = float(self.TickPointer[0][1].get())

        #fill entry content
        Object.Axes.XTickColor[1] = self.TickColor[3].GetColor()
        Object.Axes.XTickColor[0] = self.TickColor[2].GetColor()
        
        #fill entry content
        Object.Axes.YTickHeight = float(self.TickPointer[1][0].get())

        #fill entry content
        Object.Axes.YTickThickness = float(self.TickPointer[1][1].get())

        #fill entry content
        Object.Axes.YTickColor[0] = self.TickColor[0].GetColor()
        Object.Axes.YTickColor[1] = self.TickColor[1].GetColor()
        
        
        ##############################
        #Set the logical variables for the ticks
        if self.LabelOnOffVal[0].get() == 1:
            
            #set var
            Object.Axes.LabelsActiveGrid[0] = True

        else:
            
            #set var
            Object.Axes.LabelsActiveGrid[0] = False

        if self.LabelOnOffVal[1].get() == 1:
            
            #set var
            Object.Axes.LabelsActiveGrid[2] = True

        else:
            
            #set var
            Object.Axes.LabelsActiveGrid[2] = False

        if self.LabelOnOffVal[2].get() == 1:
            
            #set var
            Object.Axes.LabelsActiveGrid[3] = True

        else:
            
            #set var
            Object.Axes.LabelsActiveGrid[3] = False

        if self.LabelOnOffVal[3].get() == 1:
            
            #set var
            Object.Axes.LabelsActiveGrid[1] = True

        else:
            
            #set var
            Object.Axes.LabelsActiveGrid[1] = False

        #fill entry content
        Object.Axes.YLabelSize[0] = (self.FontEntry[0].get(),self.SizeEntry[0].get())

        #fill entry content
        Object.Axes.YLabelSize[1] = (self.FontEntry[1].get(),self.SizeEntry[1].get())

        #fill entry content
        Object.Axes.XLabelSize[0] = (self.FontEntry[2].get(),self.SizeEntry[2].get())

        #fill entry content
        Object.Axes.XLabelSize[1] = (self.FontEntry[3].get(),self.SizeEntry[3].get())

        Object.Axes.YLabelColor[1] = self.LabelColor[0].GetColor()
        Object.Axes.YLabelColor[0] = self.LabelColor[1].GetColor()
        Object.Axes.XLabelColor[1] = self.LabelColor[2].GetColor()
        Object.Axes.XLabelColor[0] = self.LabelColor[3].GetColor()

class SettingWindowPointer:
    
    def __init__(self):

        #variabmes
        self.Verbose    = True

    def BuildPointerSetting(self,Target):
        '''
        ####################################################################################
        This will populatethe frame with the widgets for the Awes class
        ####################################################################################    
        '''
        ####################################################################################
        #create arrays
        self.RowOffset          = 1
        self.ColumnOffset       = 1
        
        self.ColumnWeight       = [1,0,0,0,0,0,0,1]

        
        #to allow for simple for loop proceeding
        # [Element, row, column, sticky]
        self.PoisitionMatrix = []
        
        ####################################################################################
        ##############################
        #variables
        self.PointerType        = StringVar()
        self.PointerLabelType   = StringVar()
        
        #create the two lists
        self.PointerTypeList        = ['+ Crosshair Global',
                                       '+ Crosshair Local',
                                       'x Crosshair Local',
                                       'Square Frame']
                                       
        self.PointerLabelTypeList   = ['Border Outside',
                                       'Border Inside',
                                       'On Cursor']
                                       
        #Create the two elements
        self.PointerTypeDrop = ttk.OptionMenu(Target,
                                              self.PointerType,
                                              self.PointerTypeList[0],
                                              *self.PointerTypeList)
                                                      
        self.PointerLabelTypeDrop = ttk.OptionMenu(Target,
                                                   self.PointerLabelType,
                                                   self.PointerLabelTypeList[0],
                                                   *self.PointerLabelTypeList)
                                                   
        #Add the two items to the positionins matrix
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Pointer Type',
                                               anchor = W,
                                               font = tkFont.Font(weight = 'bold',
                                                                  underline = 0)),
                                     0+self.RowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Pointer Type: ',
                                               anchor = E),
                                     1+self.RowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,2])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Pointer Label Type: ',
                                               anchor = E),
                                     2+self.RowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,2])
                                     
        self.PoisitionMatrix.append([self.PointerTypeDrop,
                                     1+self.RowOffset,
                                     2+self.ColumnOffset,
                                     E+W,1,4])
                                     
        self.PoisitionMatrix.append([self.PointerLabelTypeDrop,
                                     2+self.RowOffset,
                                     2+self.ColumnOffset,
                                     E+W,1,4])
                                     
        ##############################
        #Toggle header
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = '',
                                               anchor = CENTER),
                                     3+self.RowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Ticks',
                                               anchor = W,
                                               font = tkFont.Font(weight = 'bold',
                                                                  underline = 0)),
                                     4+self.RowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Ticks: ',
                                               anchor = E),
                                     5+self.RowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Labels: ',
                                               anchor = E),
                                     6+self.RowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
                                     
#        self.PoisitionMatrix.append([ttk.Label(Target,
#                                               text = 'L',
#                                               anchor = W),
#                                     4+self.RowOffset,
#                                     1+self.ColumnOffset,
#                                     E+W,1,1])
#        
#        self.PoisitionMatrix.append([ttk.Label(Target,
#                                               text = 'B',
#                                               anchor = W),
#                                     4+self.RowOffset,
#                                     2+self.ColumnOffset,
#                                     E+W,1,1])
#                                     
#        self.PoisitionMatrix.append([ttk.Label(Target,
#                                               text = 'R',
#                                               anchor = W),
#                                     4+self.RowOffset,
#                                     3+self.ColumnOffset,
#                                     E+W,1,1])
#                                     
#        self.PoisitionMatrix.append([ttk.Label(Target,
#                                               text = 'T',
#                                               anchor = W),
#                                     4+self.RowOffset,
#                                     4+self.ColumnOffset,
#                                     E+W,1,1])


        ################################
        #Build the elemen   t entry fields
        
        #name list
        self.NameList = ['Left','Bottom','Right','Top']
        
        self.TickOnOff   = [None]*4
        self.TickOnOffVal = [IntVar(),IntVar(),IntVar(),IntVar()]
        
        for i in range(0,len(self.TickOnOff)):
        
        
            #create the entry
            self.TickOnOff[i] = ttk.Checkbutton(Target,
                                                variable = self.TickOnOffVal[i],
                                                text = self.NameList[i])
                                                 
            self.PoisitionMatrix.append([self.TickOnOff[i],
                                         5+self.RowOffset,
                                         1+i+self.ColumnOffset,
                                         E+W,1,1])


        ################################
        #Build the element entry fields
        self.LabelOnOff     = [None]*4
        self.LabelOnOffVal  = [IntVar(),IntVar(),IntVar(),IntVar()]
        
        for i in range(0,len(self.LabelOnOff)):
        
        
            #create the entry
            self.LabelOnOff[i] = ttk.Checkbutton(Target,
                                                 variable = self.LabelOnOffVal[i],
                                                 text = self.NameList[i])
                                                 
            self.PoisitionMatrix.append([self.LabelOnOff[i],
                                        6+self.RowOffset,
                                        1+i+self.ColumnOffset,
                                        E+W,1,1])
                                     
        ####################################################################################
        #scientigic request
        
        #put th elabel
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Scientific X: ',
                                               anchor = E),
                                     7+self.RowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
                                     
                                    
        #Put the boolena :)
        self.ScientificX = IntVar()
        
        #create the entry
        self.ScientificOnOffX = ttk.Checkbutton(Target,
                                               variable = self.ScientificX,
                                               text = 'On/Off')
                                                 
        self.PoisitionMatrix.append([self.ScientificOnOffX,
                                     7+self.RowOffset,
                                     1+self.ColumnOffset,
                                     E+W,1,1])
        
        
        #put th elabel
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Precision',
                                               anchor = E),
                                     7+self.RowOffset,
                                     2+self.ColumnOffset,
                                     E+W,1,2])
                                     
                                     
        #create the entry
        self.ScientificPrecisionX = ttk.Entry(Target,
                                             width = 2,
                                             font=("Helvetica",12))
                                                 
        self.PoisitionMatrix.append([self.ScientificPrecisionX,
                                     7+self.RowOffset,
                                     4+self.ColumnOffset,
                                     E+W,1,1])
        
        ####################################################################################
        #scientigic request
        
        #put th elabel
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Scientific Y: ',
                                               anchor = E),
                                     8+self.RowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
                                     
                                    
        #Put the boolena :)
        self.ScientificY = IntVar()
        
        #create the entry
        self.ScientificOnOffY = ttk.Checkbutton(Target,
                                               variable = self.ScientificY,
                                               text = 'On/Off')
                                                 
        self.PoisitionMatrix.append([self.ScientificOnOffY,
                                     8+self.RowOffset,
                                     1+self.ColumnOffset,
                                     E+W,1,1])
        
        
        #put th elabel
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Precision',
                                               anchor = E),
                                     8+self.RowOffset,
                                     2+self.ColumnOffset,
                                     E+W,1,2])
                                     
                                     
        #create the entry
        self.ScientificPrecisionY = ttk.Entry(Target,
                                             width = 2,
                                             font=("Helvetica",12))
                                                 
        self.PoisitionMatrix.append([self.ScientificPrecisionY,
                                     8+self.RowOffset,
                                     4+self.ColumnOffset,
                                     E+W,1,1])
                                     
        ####################################################################################
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Length: ',
                                               anchor = E),
                                     9+self.RowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
                     
        #create the entry
        self.Length = ttk.Entry(Target,
                                width = 2,
                                font=("Helvetica",12))
                                                 
        self.PoisitionMatrix.append([self.Length,
                                     9+self.RowOffset,
                                     1+self.ColumnOffset,
                                     E+W,1,1])
                     
        ####################################################################################
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Width: ',
                                               anchor = E),
                                     9+self.RowOffset,
                                     2+self.ColumnOffset,
                                     E+W,1,2])
                                     
        #create the entry
        self.Width = ttk.Entry(Target,
                                width = 2,
                                font=("Helvetica",12))
                                                 
        self.PoisitionMatrix.append([self.Width,
                                     9+self.RowOffset,
                                     4+self.ColumnOffset,
                                     E+W,1,1])
                                     
        ####################################################################################
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Color: ',
                                               anchor = E),
                                     10+self.RowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
                                     
        #create the entry
        self.Color = ttk.Entry(Target,
                                width = 2,
                                font=("Helvetica",12))
                                                 
        self.PoisitionMatrix.append([self.Color,
                                     10+self.RowOffset,
                                     1+self.ColumnOffset,
                                     E+W,1,1])
                                     

        ####################################################################################
        
        #place everything
        for i in range(0,len(self.PoisitionMatrix)):
        
            self.PoisitionMatrix[i][0].grid(row         =  self.PoisitionMatrix[i][1],
                                            column      =  self.PoisitionMatrix[i][2],
                                            sticky      =  self.PoisitionMatrix[i][3],
                                            rowspan     =  self.PoisitionMatrix[i][4],
                                            columnspan  =  self.PoisitionMatrix[i][5])

        #cofigure all
        for i in range(0,len(self.ColumnWeight)):
        
            Target.grid_columnconfigure(i,weight =self.ColumnWeight[i])
        
        return Target

    def CatchPointerSetting(self,Object):
        '''
        ######################################################
        Catches the settings from the subplot variable and
        sends it back to the Entry fields and the checkbuttons
        
        The object hsould be given by the multiplot and is the
        associated object element
        ######################################################
        '''
        
        #if the subplot is empty pass
        if Object == '':

            return
        
        #logging purpose
        if self.Verbose:
        
            print 'Tried to catch'
        
        
        ##############################
        #Set the drop down menues
        self.PointerType.set(self.PointerTypeList[Object.Pointer.Type])
        self.PointerLabelType.set(self.PointerLabelTypeList[Object.Pointer.LabelType])

        ##############################
        #Set the logical variables for the ticks
        if Object.Pointer.LabelTicks[0]:
            
            #set var
            self.TickOnOffVal[0].set(1)
            
            #set button state
            self.TickOnOff[0].state(['selected'])

        else:
            
            #set var
            self.TickOnOffVal[0].set(0)
            
            #set button state
            self.TickOnOff[0].state(['!selected'])

        if Object.Pointer.LabelTicks[1]:
            
            #set var
            self.TickOnOffVal[1].set(1)
            
            #set button state
            self.TickOnOff[1].state(['selected'])

        else:
            
            #set var
            self.TickOnOffVal[1].set(0)
            
            #set button state
            self.TickOnOff[1].state(['!selected'])

        if Object.Pointer.LabelTicks[2]:
            
            #set var
            self.TickOnOffVal[2].set(1)
            
            #set button state
            self.TickOnOff[2].state(['selected'])

        else:
            
            #set var
            self.TickOnOffVal[2].set(0)
            
            #set button state
            self.TickOnOff[2].state(['!selected'])

        if Object.Pointer.LabelTicks[3]:
            
            #set var
            self.TickOnOffVal[3].set(1)
            
            #set button state
            self.TickOnOff[3].state(['selected'])

        else:
            
            #set var
            self.TickOnOffVal[3].set(0)
            
            #set button state
            self.TickOnOff[3].state(['!selected'])
        
        ##############################
        #Set the logical variables for the ticks
        if Object.Pointer.LabelPositions[0]:
            
            #set var
            self.LabelOnOffVal[0].set(1)
            
            #set button state
            self.LabelOnOff[0].state(['selected'])

        else:
            
            #set var
            self.LabelOnOffVal[0].set(0)
            
            #set button state
            self.LabelOnOff[0].state(['!selected'])

        if Object.Pointer.LabelPositions[1]:
            
            #set var
            self.LabelOnOffVal[1].set(1)
            
            #set button state
            self.LabelOnOff[1].state(['selected'])

        else:
            
            #set var
            self.LabelOnOffVal[1].set(0)
            
            #set button state
            self.LabelOnOff[1].state(['!selected'])

        if Object.Pointer.LabelPositions[2]:
            
            #set var
            self.LabelOnOffVal[2].set(1)
            
            #set button state
            self.LabelOnOff[2].state(['selected'])

        else:
            
            #set var
            self.LabelOnOffVal[2].set(0)
            
            #set button state
            self.LabelOnOff[2].state(['!selected'])

        if Object.Pointer.LabelPositions[3]:
            
            #set var
            self.LabelOnOffVal[3].set(1)
            
            #set button state
            self.LabelOnOff[3].state(['selected'])

        else:
            
            #set var
            self.LabelOnOffVal[3].set(0)
            
            #set button state
            self.LabelOnOff[3].state(['!selected'])
                
        ##############################
        #Set scientific on off
        if Object.Pointer.isXSci:
            
            #set var
            self.ScientificX.set(1)
            
            #set button state
            self.ScientificOnOffX.state(['selected'])

        else:
            
            #set var
            self.ScientificX.set(0)
            
            #set button state
            self.ScientificOnOffX.state(['!selected'])
        
        if Object.Pointer.isYSci:
            
            #set var
            self.ScientificY.set(1)
            
            #set button state
            self.ScientificOnOffY.state(['selected'])

        else:
            
            #set var
            self.ScientificY.set(0)
            
            #set button state
            self.ScientificOnOffY.state(['!selected'])
                
        ##############################
        #Grab scientific precision
        
        #delete entry content
        self.ScientificPrecisionX.delete(0,END)

        #fill entry content
        self.ScientificPrecisionX.insert(0,str(Object.Pointer.XSciPrecision.split('%.')[1].split('e')[0]))

        #delete entry content
        self.ScientificPrecisionY.delete(0,END)

        #fill entry content
        self.ScientificPrecisionY.insert(0,str(Object.Pointer.YSciPrecision.split('%.')[1].split('e')[0]))

        #delete entry content
        self.Length.delete(0,END)

        #fill entry content
        self.Length.insert(0,str(Object.Pointer.LabelTicksOffset))

        #delete entry content
        self.Width.delete(0,END)

        #fill entry content
        self.Width.insert(0,str(Object.Pointer.LabelTicksThickness))

        #delete entry content
        self.Color.delete(0,END)

        #fill entry content
        self.Color.insert(0,str(Object.Pointer.LabelTicksColor))
#
#        #delete entry content
#        self.TickPointer[1][2].delete(0,END)
#
#        #fill entry content
#        self.TickPointer[1][2].insert(0,str(Object.Axes.YTickColor))


    def SubmitPointerSetting(self,Object):
        '''
        ######################################################
        Catches the settings from the subplot variable and
        sends it back to the Entry fields and the checkbuttons
        
        The object hsould be given by the multiplot and is the
        associated object element
        ######################################################
        '''

        #if the subplot is empty pass
        if Object == '':

            return
        
        #logging purpose
        if self.Verbose:
        
            print 'Tried to catch'
        
        ##############################
        #Set the drop down menues
        for i in range(0, len(self.PointerTypeList)):
        
            if self.PointerTypeList[i] == self.PointerType.get():
        
                Object.Pointer.Type = i
                break
        
        #Set the drop down menues
        for i in range(0, len(self.PointerLabelTypeList)):
        
            if self.PointerLabelTypeList[i] == self.PointerLabelType.get():
        
                Object.Pointer.LabelType = i
                break

        ##############################
        #Set the logical variables for the ticks
        if self.TickOnOffVal[0].get() == 1:
            
            #set var
            Object.Pointer.LabelTicks[0] = True

        else:
            
            #set var
            Object.Pointer.LabelTicks[0] = False

        if self.TickOnOffVal[1].get() == 1:
            
            #set var
            Object.Pointer.LabelTicks[1] = True

        else:
            
            #set var
            Object.Pointer.LabelTicks[1] = False

        if self.TickOnOffVal[2].get() == 1:
            
            #set var
            Object.Pointer.LabelTicks[2] = True

        else:
            
            #set var
            Object.Pointer.LabelTicks[2] = False

        if self.TickOnOffVal[3].get() == 1:
            
            #set var
            Object.Pointer.LabelTicks[3] = True

        else:
            
            #set var
            Object.Pointer.LabelTicks[3] = False

        ##############################
        #Set the logical variables for the ticks
        if self.LabelOnOffVal[0].get() == 1:
            
            #set var
            Object.Pointer.LabelPositions[0] = True

        else:
            
            #set var
            Object.Pointer.LabelPositions[0] = False

        if self.LabelOnOffVal[1].get() == 1:
            
            #set var
            Object.Pointer.LabelPositions[1] = True

        else:
            
            #set var
            Object.Pointer.LabelPositions[1] = False

        if self.LabelOnOffVal[2].get() == 1:
            
            #set var
            Object.Pointer.LabelPositions[2] = True

        else:
            
            #set var
            Object.Pointer.LabelPositions[2] = False

        if self.LabelOnOffVal[3].get() == 1:
            
            #set var
            Object.Pointer.LabelPositions[3] = True

        else:
            
            #set var
            Object.Pointer.LabelPositions[3] = False

        ##############################
        #Scientific logical
        if self.ScientificX.get() == 1:
            
            #set var
            Object.Pointer.isXSci = True

        else:
            
            #set var
            Object.Pointer.isXSci = False

        if self.ScientificY.get() == 1:
            
            #set var
            Object.Pointer.isYSci = True

        else:
            
            #set var
            Object.Pointer.isYSci = False

        ##############################
        #Set the text variables

        Object.Pointer.LabelTicksColor      = self.Color.get()
        Object.Pointer.LabelTicksOffset     = float(self.Length.get())
        Object.Pointer.LabelTicksThickness  = float(self.Width.get())
        Object.Pointer.XSciPrecision        = '%.'+self.ScientificPrecisionX.get()+'e'
        Object.Pointer.YSciPrecision        = '%.'+self.ScientificPrecisionY.get()+'e'


class SettingWindowData:
    
    def __init__(self):

        #variabmes
        self.Verbose    = True

    def BuildDataSetting(self,Target):
        '''
        ######################################################
        Loads and displays the data of the current plotting
        instanc. Note that the editability might be overriden
        by another instance upon refresh. 
        
        It is possible to write the setting to file in that 
        case or to buffer to keep it alive for one session.
        ######################################################
        '''
        
        #set the offset parameters
        self.RowOffset      = 1
        self.ColumnOffset   = 1
        self.PoisitionMatrix = []
        
        #populate the static labels
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Active',
                                               anchor = W,
                                               font = tkFont.Font(weight = 'bold',
                                                                  underline = 0)),
                                     0+self.RowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Type',
                                               anchor = W,
                                               font = tkFont.Font(weight = 'bold',
                                                                  underline = 0)),
                                     0+self.RowOffset,
                                     1+self.ColumnOffset,
                                     E+W,1,1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Name',
                                               anchor = W,
                                               font = tkFont.Font(weight = 'bold',
                                                                  underline = 0)),
                                     0+self.RowOffset,
                                     2+self.ColumnOffset,
                                     E+W,1,1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Color',
                                               anchor = W,
                                               font = tkFont.Font(weight = 'bold',
                                                                  underline = 0)),
                                     0+self.RowOffset,
                                     3+self.ColumnOffset,
                                     E+W,1,1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Options',
                                               anchor = W,
                                               font = tkFont.Font(weight = 'bold',
                                                                  underline = 0)),
                                     0+self.RowOffset,
                                     4+self.ColumnOffset,
                                     E+W,1,3])
        
        ####################################################################################
        
        #place everything
        for i in range(0,len(self.PoisitionMatrix)):
        
            self.PoisitionMatrix[i][0].grid(row         =  self.PoisitionMatrix[i][1],
                                            column      =  self.PoisitionMatrix[i][2],
                                            sticky      =  self.PoisitionMatrix[i][3],
                                            rowspan     =  self.PoisitionMatrix[i][4],
                                            columnspan  =  self.PoisitionMatrix[i][5])
        
        return Target

    def CatchDataSetting(self,Object,Target):
        '''
        ######################################################
        
        ######################################################
        '''
        
        #if the subplot is empty pass
        if Object == '':

            return
        
        #logging purpose
        if self.Verbose:
        
            print 'Tried to catch'
    
        #try to destroy all emements previously loaded
        try:
        
            for i in range(0, len(self.ElementList)):
        
                for j in range(0, len(self.ElementList[i])):
        
                    self.ElementList[i][j].destroy()
            
        except:
            
            pass
        
        #initialise the matrix
        self.PoisitionMatrix_2 = []
        self.ElementList = []
        self.TypeList = []
        
        #set theindex
        Index =0
        
        ######################################################################
        ######################################################################
        ######################################################################
        #build the information
        for i in range(0, len(Object.Plots)):
            
            #temporary variable list
            LocalList = []
            
            ###################################
            #active state
            tempVar = IntVar()
            tempVar.set(1)
            LocalList.append(ttk.Checkbutton(Target, variable = tempVar))
                                
            if Object.Plots[i].Active:
                
                tempVar.set(1)
                LocalList[-1].state(['selected'])
                 
            else:
            
                tempVar.set(0)
                LocalList[-1].state(['!selected'])
            
            
            self.PoisitionMatrix_2.append([LocalList[-1],
                                           Index+1+self.RowOffset,
                                           0+self.ColumnOffset,
                                           E+W,1,1])
                                           
            ###################################
            #place the type
            LocalList.append(ttk.Label(Target,text = '2D Plot'))
            
            #send to type list
            self.TypeList.append(['2D Plot',i])
            
            self.PoisitionMatrix_2.append([LocalList[-1],
                                           Index+1+self.RowOffset,
                                           1+self.ColumnOffset,
                                           E+W,1,1])
           
            ###################################
            #Place the name
            if Object.Plots[i].Name == '':
                
                text = ' - '
            
            else:
            
                text = Object.Plots[i].Name
            
            LocalList.append(ttk.Label(Target,text = text))
            
            self.PoisitionMatrix_2.append([LocalList[-1],
                                            Index+1+self.RowOffset,
                                            2+self.ColumnOffset,
                                            E+W,1,1])
            
            ###################################
            #Place the color though color canvas
            LocalList.append(ColorCanvas(Target, color = Object.Plots[i].Color))
            
            self.PoisitionMatrix_2.append([LocalList[-1],
                                            Index+1+self.RowOffset,
                                            3+self.ColumnOffset,
                                            E+W,1,1])
            
            ###################################
            #Place the thickness through ntry field
            LocalList.append(ttk.Entry(Target,
                                       width = 3))
            
            #delete entry content
            LocalList[-1].delete(0,END)

            #fill entry content
            LocalList[-1].insert(0,str(Object.Plots[i].Thickness))
            
            self.PoisitionMatrix_2.append([LocalList[-1],
                                            Index+1+self.RowOffset,
                                            4+self.ColumnOffset,
                                            E+W,1,1])
                                
            self.ElementList.append(LocalList)
            
            #Move the index forward
            Index += 1
            
        ######################################################################
        ######################################################################
        ######################################################################
        #build the information
        for i in range(0, len(Object.Ranges)):
            
            #temporary variable list
            LocalList = []
            
            ###################################
            #active state
            tempVar = IntVar()
            tempVar.set(1)
            LocalList.append(ttk.Checkbutton(Target, variable = tempVar))
                                
            if Object.Ranges[i].Active:
                
                tempVar.set(1)
                LocalList[-1].state(['selected'])
                 
            else:
            
                tempVar.set(0)
                LocalList[-1].state(['!selected'])
            
            
            self.PoisitionMatrix_2.append([LocalList[-1],
                                           Index+1+self.RowOffset,
                                           0+self.ColumnOffset,
                                           E+W,1,1])
                                           
            ###################################
            #place the type
            LocalList.append(ttk.Label(Target,text = 'Range'))
            
            #send to type list
            self.TypeList.append(['Range',i])
            
            self.PoisitionMatrix_2.append([LocalList[-1],
                                           Index+1+self.RowOffset,
                                           1+self.ColumnOffset,
                                           E+W,1,1])
           
            ###################################
            #Place the name
            if Object.Ranges[i].Name == '':
                
                text = ' - '
            
            else:
            
                text = Object.Ranges[i].Name
            
            LocalList.append(ttk.Label(Target,text = text))
            
            self.PoisitionMatrix_2.append([LocalList[-1],
                                            Index+1+self.RowOffset,
                                            2+self.ColumnOffset,
                                            E+W,1,1])
            
            ###################################
            #Place the color though color canvas
            LocalList.append(ColorCanvas(Target, color = Object.Ranges[i].Color))
            
            self.PoisitionMatrix_2.append([LocalList[-1],
                                            Index+1+self.RowOffset,
                                            3+self.ColumnOffset,
                                            E+W,1,1])
            
            #set the list
            self.ElementList.append(LocalList)
            
            #Move the index forward
            Index += 1
                
        ######################################################################
        ######################################################################
        ######################################################################
        #build the information
        for i in range(0, len(Object.Lines)):
            
            #temporary variable list
            LocalList = []
            
            ###################################
            #active state
            tempVar = IntVar()
            tempVar.set(1)
            LocalList.append(ttk.Checkbutton(Target, variable = tempVar))
                                
            if Object.Lines[i].Active:
                
                tempVar.set(1)
                LocalList[-1].state(['selected'])
                 
            else:
            
                tempVar.set(0)
                LocalList[-1].state(['!selected'])
            
            
            self.PoisitionMatrix_2.append([LocalList[-1],
                                           Index+1+self.RowOffset,
                                           0+self.ColumnOffset,
                                           E+W,1,1])
                                           
            ###################################
            #place the type
            LocalList.append(ttk.Label(Target,text = 'Line'))
            
            #send to type list
            self.TypeList.append(['Line',i])
            
            self.PoisitionMatrix_2.append([LocalList[-1],
                                           Index+1+self.RowOffset,
                                           1+self.ColumnOffset,
                                           E+W,1,1])
           
            ###################################
            #Place the name
            if Object.Lines[i].Name == '':
                
                text = ' - '
            
            else:
            
                text = Object.Lines[i].Name
            
            LocalList.append(ttk.Label(Target,text = text))
            
            self.PoisitionMatrix_2.append([LocalList[-1],
                                            Index+1+self.RowOffset,
                                            2+self.ColumnOffset,
                                            E+W,1,1])
            
            ###################################
            #Place the color though color canvas
            LocalList.append(ColorCanvas(Target, color = Object.Lines[i].Color))
            
            self.PoisitionMatrix_2.append([LocalList[-1],
                                            Index+1+self.RowOffset,
                                            3+self.ColumnOffset,
                                            E+W,1,1])

            ###################################
            #Place the thickness through ntry field
            LocalList.append(ttk.Entry(Target,
                                       width = 3))
            
            #delete entry content
            LocalList[-1].delete(0,END)

            #fill entry content
            LocalList[-1].insert(0,str(Object.Lines[i].Thickness))
            
            self.PoisitionMatrix_2.append([LocalList[-1],
                                            Index+1+self.RowOffset,
                                            4+self.ColumnOffset,
                                            E+W,1,1])
            #Move the index forward
            Index += 1

            self.ElementList.append(LocalList)

        if self.Verbose:
            
            print self.ElementList
            
        ####################################################################################
        #place everything
        for i in range(0,len(self.PoisitionMatrix_2)):
        
            self.PoisitionMatrix_2[i][0].grid(row         =  self.PoisitionMatrix_2[i][1],
                                              column      =  self.PoisitionMatrix_2[i][2],
                                              sticky      =  self.PoisitionMatrix_2[i][3],
                                              rowspan     =  self.PoisitionMatrix_2[i][4],
                                              columnspan  =  self.PoisitionMatrix_2[i][5])

    def SubmitDataSetting(self,Object):
        '''
        ######################################################
        This function will submit the changes done to the
        ploting environement and then submit them to the 
        plot instance. 
        
        The plot instance is linked by the Target keyword
        ######################################################
        '''
        
        if self.Verbose:
        
            print 'List'
            print self.TypeList
            print 'Length:'
            print len(self.TypeList)
            print 'List'
            print self.ElementList
            print 'Length:'
            print len(self.ElementList)

        for i in range(0, len(self.TypeList)):
        
            ###################################
            #Plots
            if self.TypeList[i][0] == '2D Plot':
            
                try:
                    if self.ElementList[i][0].state()[0] == 'selected':
                    
                        Object.Plots[self.TypeList[i][1]].Active = True
                
                    else:
                    
                        Object.Plots[self.TypeList[i][1]].Active = False
        
                except:
                
                    Object.Plots[self.TypeList[i][1]].Active = False
                
                #the color
                Object.Plots[self.TypeList[i][1]].color = self.ElementList[i][3].GetColor()

                #the thikeness
                Object.Plots[self.TypeList[i][1]].Thickness = int(self.ElementList[i][4].get())

            ###################################
            #Ranges

            if self.TypeList[i][0] == 'Range':
            
                try:
                    if self.ElementList[i][0].state()[0] == 'selected':
                    
                        Object.Ranges[self.TypeList[i][1]].Active = True
                
                    else:
                    
                        Object.Ranges[self.TypeList[i][1]].Active = False
        
                except:
                
                    Object.Ranges[self.TypeList[i][1]].Active = False
                
                #the color
                Object.Ranges[self.TypeList[i][1]].color = self.ElementList[i][3].GetColor()

                #the thikeness
                #Object.Ranges[i].Thickness = int(self.ElementList[i][4].get())

            ###################################
            #Lines
            if self.TypeList[i][0] == 'Line':
            
                try:
                    if self.ElementList[i][0].state()[0] == 'selected':
                    
                        Object.Lines[self.TypeList[i][1]].Active = True
                
                    else:
                    
                        Object.Lines[self.TypeList[i][1]].Active = False
        
                except:
                
                    Object.Lines[self.TypeList[i][1]].Active = False
                
                #the color
                Object.Lines[self.TypeList[i][1]].color = self.ElementList[i][3].GetColor()

                #the thikeness
                Object.Lines[self.TypeList[i][1]].Thickness = int(self.ElementList[i][4].get())

class ColorCanvas(Canvas):


    '''
    ######################################################
    This is a small square cnavas that is suppsoed to act
    as a olor selector. Note that the canvas is otherwie
    completly empty. the clikc is bound on self.
    
    it can be tested by 
    
    def main():

        root = Tk()
        myframe = Frame(root,width=200, height=100)
        myframe.pack(fill=BOTH, expand=YES)
    
        canvas = ColorCanvas(myframe,width = 10, height = 10)
    
        canvas.pack()
        mainloop()


    if __name__ == "__main__":
        main()
        
        
    The actual value of the color can then be trieved
    by using the canvas inherent function GetColor()
    ######################################################
    '''
    
    def __init__(self, parent,width = 10,height = 10, color = None,**kwargs):

        Canvas.__init__(self,
                        parent,
                        width = 10,
                        height = 10,
                        background = 'black',
                        **kwargs)

        #set parameters
        self.Verbose    = True
        
        #set the click binding
        self.bind('<Button-1>', self.SetColor, '+')
    
        #if the variable is not set to None set the color
        if not color == None:
            
            self.color = (None,color)
            self.configure(background = self.color[1])
        
        else:
    
            self.color = (None,'black')
            self.configure(background = self.color[1])

    def SetColor(self,event):
        
        '''
        ######################################################
        opens the tikinter color selection palette which is 
        dependant on the operating systeme. Note that this 
        makes it very easy...
        
        from tkColorChooser import askcolor
        
        should be imported nevertheless
        ######################################################
        '''
        
        #some verbose output
        if self.Verbose:
            print event.char
        
        #start the tkinter color selector
        self.color = askcolor()
        
        #some mor verbose
        if self.Verbose:
            print self.color
        
        #finnally configure the buttons
        self.configure(background = self.color[1])

    def LoadColor(self,color):
        '''
        ######################################################
        Manually load the color
        ######################################################
        '''
        #load color into class
        self.color = (None,color)
    
        #finnally configure the buttons
        self.configure(background = self.color[1])
    
    def GetColor(self):
        '''
        ######################################################
        Sends out the acutal color
        ######################################################
        '''
        return self.color[1]

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
        self.Color = 'black'
        self.Thickness = 2


    def Listen(self):

        '''
        ######################################################
        This method is there to start listening for different
        events. This includes the click and release.
        ######################################################
        '''
        #bind method to the mouse click
        self.Canvas.bind('<Button-1>', self.StartZoomBox,'+')
        
        #start the motion lister as well as the kill listener
        self.BoundMethod_1 = self.Canvas.bind('<ButtonRelease-1>'   , self.KillZoomBox      ,'+')
        
        #link the method
        self.Canvas.Drawer.Mouse.Bind('<B1-Motion>',self.UpdateZoomBox,'Pointer')
        
        #verbose
        if self.Verbose:
            
            print 'The zoomer got bound'


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
        
        #first grab closest Id to the researched value
        for i in range(0,len(self.Canvas.Drawer.Plots)):
        
        
            #search the first closest
            idx_0 = (numpy.abs(self.Canvas.Drawer.Plots[i].X - X)).argmin()
        
            #search the second closest (obviously our value will be in between)
            
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
        
            self.Method(idx_2)
        
        return X,List[idx_2],idx_2

    def find_nearestX(self, X, Y):
        
        '''
        ##########################################################################################
        This method aims at searching sucessively for the nearest value in all plots by first
        scanning the nearest X. Then e find the second nearest to zero after X-Nearest. This 
        will give us back two point ids which whome we can calculate the nearest Y
        ##########################################################################################
        '''
        
        List = []
        
        #first grab closest Id to the researched value
        for i in range(0,len(self.Canvas.Drawer.Plots)):
        
        
            #search the first closest
            idx_0 = (numpy.abs(self.Canvas.Drawer.Plots[i].Y - Y)).argmin()
        
            #search the second closest (obviously our value will be in between)
            try:
                if self.Canvas.Drawer.Plots[i].Y[idx_0] <= Y:
                    idx_1 = idx_0+1
                else:
                    idx_1 = idx_0-1
        
                #calclate the Y from these positions
                List.append(float(self.Canvas.Drawer.Plots[i].X[idx_0])+float((Y-self.Canvas.Drawer.Plots[i].Y[idx_0]))*
                            (float(self.Canvas.Drawer.Plots[i].X[idx_1])-float(self.Canvas.Drawer.Plots[i].X[idx_0]))/
                            (float(self.Canvas.Drawer.Plots[i].Y[idx_1])-float(self.Canvas.Drawer.Plots[i].Y[idx_0])))
            except:
                List.append(numpy.inf)
    
        if self.Verbose:
            print List
        
        idx_2 = (numpy.abs(List-X)).argmin()
        
        if not self.Method == None:
        
            self.Method(idx_2)
    
        return List[idx_2],Y,idx_2

    def find_nearestXY(self, X, Y):
        
        '''
        ##########################################################################################
        This method aims at searching sucessively for the nearest value in all plots by first
        scanning the nearest X. Then e find the second nearest to zero after X-Nearest. This 
        will give us back two point ids which whome we can calculate the nearest Y
        
        This version will pin i tto the closest point also. This is particulary helpful when 
        dealing with sctter plots
        ##########################################################################################
        '''
        
        List = []
        
        #first grab closest Id to the researched value
        for i in range(0,len(self.Canvas.Drawer.Plots)):
        
        
            #search the first closest
            idx_0 = (numpy.abs(self.Canvas.Drawer.Plots[i].X - X)).argmin()
        
            #calclate the Y from these positions
            List.append(float(self.Canvas.Drawer.Plots[i].Y[idx_0]))
        
        idx_2 = (numpy.abs(List-Y)).argmin()
        
        if not self.Method == None:
        
            self.Method(idx_2)
    
        return self.Canvas.Drawer.Plots[idx_2].X[idx_0],List[idx_2],idx_0

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
        
        #print self.Target.X
        #print self.Target_X,self.Target_Y
        #print X,Y
        #print idx_0, idx_1
        #print self.Target_X[idx_0],self.Target_Y[idx_1]
        
        return self.Target_X[idx_0],self.Target_Y[idx_1]
    
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
                                                                 -self.Canvas.Drawer.Axes.YLabelOffset)
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
                                                                    -self.Canvas.Drawer.Axes.XLabelOffset))
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
                                                                     -self.Canvas.Drawer.Axes.YLabelOffset))
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
                                                                 -self.Canvas.Drawer.Axes.XLabelOffset)
                                                               
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
                    self.Cursor_x, self.Cursor_y, ClosestID =  self.find_nearestXY(self.Cursor_x,self.Cursor_y)
                except:
                    pass
            
            if self.Sticky == 3:
            
                #stick to the closest line including calculating position
                try:
                    self.Cursor_x, self.Cursor_y, ClosestID =  self.find_nearestX(self.Cursor_x,self.Cursor_y)
                except:
                    pass
        
            if self.Sticky == 4:
                #try:
                    #stick to the closest line including calculating position
                self.Cursor_x, self.Cursor_y = self.find_nearestXYContour(self.Cursor_x,self.Cursor_y)
                #except:
                #     pass
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
        self.Canvas.focus_set()

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
            self.MousePosition()
            
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

class Axes:
    
    '''
    ######################################################
    The axes class will generally handle the box with the
    Ticks and the writings on the ticks.
    ######################################################
    '''

    def __init__(self, Canvas):
        
        #save canvas pointer
        self.Canvas  = Canvas
        self.Verbose = False
        
        #Set Default
        self.SetInitial()
        
    def SetInitial(self):
        
        '''
        ##########################################
        This method will Set all parameters to the
        default. Note that these settings can then 
        be used and changed by the user or the 
        Setting window
        
        The Setting array used by the Settings
        Interface is then creathed
        ##########################################
        '''
        
        ##########################################
        #Set the variables
        self.Thickness  = 5
        self.Color      = 'black'
        self.PaddingIn  = [0.0, 0.0, 0.0, 0.0]
        self.PaddingOut = [0.1, 0.2, 0.05, 0.05]
        self.Type       = [True,True,True,True]

        ##########################################
        #Prepare Axes information
        self.AxesAdresses = []
        self.isAxesDrawn = False
    
        ##########################################
        #Prepare Tick variables
        
        #XTicks variables
        self.XTickType          = 0
        self.XTickSpacing       = None
        self.XTickNumber        = 10
        self.XTickOrigin        = None
        self.XTickThickness     = 4
        self.XTickColor         = ['black','black']
        self.XTickHeight        = 5
        self.isXTicksDrawn      = [False,False]
        self.XTickAdresses      = []
    
        #YTicks variables
        self.YTickType          = 0
        self.YTickSpacing       = None
        self.YTickNumber        = 10
        self.YTickOrigin        = None
        self.YTickThickness     = 4
        self.YTickColor         = ['black','black']
        self.YTickHeight        = 5
        self.isYTicksDrawn      = [False,False]
        self.YTickAdresses      = []
        
        #grid variables
        self.XGrid              = True
        self.XGridThickness     = 1
        self.XGridDash          = (10,5,3,5,10,5)
        self.XGridColor         = u'#E0E0E0'
        self.XGridAdresses      = []
        
        self.YGrid              = True
        self.YGridThickness     = 1
        self.YGridDash          = (10,5,3,5,10,5)
        self.YGridColor         = u'#E0E0E0'
        self.YGridAdresses      = []
    
        #XLabel variables
        self.XLabelSize         = [('Helvetica', '11'),('Helvetica', '11')]
        self.XLabelColor        = ['black','black']
        self.XLabelOffset       = 0.025
        self.XLabelAdresses     = []
        self.XLabelRounding     = 1
    
        #XLabel variables
        self.YLabelSize         = [('Helvetica', '11'),('Helvetica', '11')]
        self.YLabelColor        = ['black','black']
        self.YLabelOffset       = 0.05
        self.YLabelAdresses     = []
        self.YLabelRounding     = 1
        
        #label formating
        self.isXSci             = False
        self.isYSci             = False
        self.XSciPrecision      = '%.1e'
        self.YSciPrecision      = '%.1e'
    
    
        #Label and Tick Grids (Left - Botton - Right - Top)
        self.TicksActiveGrid = [True, True, False, False]
        self.LabelsActiveGrid = [True, True, False, False]
    
        #cover the padding edges accordingly.
        self.CoverBox = True
    
        #bind the key dispatcher
        self.BoundMethod_0 = self.Canvas.bind('<Key>', self.keyDispatcher, "+")
    
    def keyDispatcher(self,event):
        '''
        ######################################################
        Rotate through the cursor type when the user presses
        the c modifier key
        ######################################################
        '''
        
        #grab the key
        Key = event.char
        
        #th user wants to switch pointer type
        if Key == 'z':
        
            self.PaddingOut[1] += 0.02
        
        if Key == 's':
        
            self.PaddingOut[1] -= 0.02
        
        if Key == 'q':
        
            self.PaddingOut[0] -= 0.02
        
        if Key == 'd':
        
            self.PaddingOut[0] += 0.02

        #reset the axes
        self.ResetAxes()
            
        #redraw the canvass
        self.Canvas.Drawer.Zoom()

    def DrawCoverBoxes(self):
    
        '''
        ######################################################
        The cover boxes avoids that items outside the scope
        are visible. Basically it will draw a box on the
        padding area to mask the potential elements.
        ######################################################
        '''
    
        #try to delete cover boxes
        try:
            for i in range(0,len(self.CoverBoxes)):
        
                self.Canvas.delete(self.CoverBoxes[i])
        except:
    
            pass

        #reset box variable
        self.CoverBoxes = []
    
        #draw the left one
        self.CoverBoxes.append(self.Canvas.create_rectangle(0*self.Canvas.Drawer.wScaleFactor,
                                                            0*self.Canvas.Drawer.hScaleFactor,
                                                            (self.PaddingOut[0]+self.PaddingIn[0])*self.Canvas.Drawer.wScaleFactor,
                                                            1*self.Canvas.Drawer.hScaleFactor,
                                                            width = 0,
                                                            outline = 'white',
                                                            fill = 'white',
                                                            tag = 'Top'))
        
        
        #draw the bot one
        self.CoverBoxes.append(self.Canvas.create_rectangle(0*self.Canvas.Drawer.wScaleFactor,
                                                            1*self.Canvas.Drawer.hScaleFactor,
                                                            1*self.Canvas.Drawer.wScaleFactor,
                                                            (1.0-self.PaddingOut[1]-self.PaddingIn[1])*self.Canvas.Drawer.hScaleFactor,
                                                            width = 0,
                                                            outline = 'white',
                                                            fill = 'white',
                                                            tag = 'Top'))
        
        
        #draw the right one
        self.CoverBoxes.append(self.Canvas.create_rectangle(1*self.Canvas.Drawer.wScaleFactor,
                                                            0*self.Canvas.Drawer.hScaleFactor,
                                                            (1-self.PaddingOut[2]-self.PaddingIn[2])*self.Canvas.Drawer.wScaleFactor,
                                                            1*self.Canvas.Drawer.hScaleFactor,
                                                            width = 0,
                                                            outline = 'white',
                                                            fill = 'white',
                                                            tag = 'Top'))
        
        
        #draw the top one
        self.CoverBoxes.append(self.Canvas.create_rectangle(0*self.Canvas.Drawer.wScaleFactor,
                                                            0*self.Canvas.Drawer.hScaleFactor,
                                                            1*self.Canvas.Drawer.wScaleFactor,
                                                            (self.PaddingOut[3]+self.PaddingIn[3])*self.Canvas.Drawer.hScaleFactor,
                                                            width = 0,
                                                            outline = 'white',
                                                            fill = 'white',
                                                            tag = 'Top'))


    def DrawAxes(self):

        '''
        ######################################################
        Draws the axes related to the given bounding ratios. 
        Note that if the Axes are already drawn it will first
        launch the clearing method to remove them
        ######################################################
        '''
        
        if self.isAxesDrawn:
            
            #remove all Axes element from the current canvas
            self.RemoveAxes()
        
        #draw the padding boxes
        self.DrawCoverBoxes()
        
        #Do we draw the left part
        if self.Type[0]:
            self.AxesAdresses.append(self.Canvas.create_line((self.PaddingOut[0])*self.Canvas.Drawer.wScaleFactor,
                                                             
                                                             (self.PaddingOut[3])*self.Canvas.Drawer.hScaleFactor,
                                                             
                                                             (self.PaddingOut[0])*self.Canvas.Drawer.wScaleFactor,
                                                             
                                                             (1.0-self.PaddingOut[1])*self.Canvas.Drawer.hScaleFactor,
                                                             
                                                             fill  = self.Color,
                                                             width = self.Thickness,
                                                             tag = 'TopTop'))
        #Draw the bottom part
        if self.Type[1]:
            self.AxesAdresses.append(self.Canvas.create_line((self.PaddingOut[0])*self.Canvas.Drawer.wScaleFactor,
                                                             
                                                             (1.0-self.PaddingOut[1])*self.Canvas.Drawer.hScaleFactor,
                                                             
                                                             (1.0-self.PaddingOut[2])*self.Canvas.Drawer.wScaleFactor,
                                                             
                                                             (1.0-self.PaddingOut[1])*self.Canvas.Drawer.hScaleFactor,
                                                             
                                                             fill  = self.Color,
                                                             width = self.Thickness,
                                                             tag = 'TopTop'))
        #Draw the right part
        if self.Type[2]:
            self.AxesAdresses.append(self.Canvas.create_line((1.0-self.PaddingOut[2])*self.Canvas.Drawer.wScaleFactor,
                                                             
                                                             (1.0-self.PaddingOut[1])*self.Canvas.Drawer.hScaleFactor,
                                                             
                                                             (1.0-self.PaddingOut[2])*self.Canvas.Drawer.wScaleFactor,
                                                             
                                                             (self.PaddingOut[3])*self.Canvas.Drawer.hScaleFactor,
                                                             
                                                             fill  = self.Color,
                                                             width = self.Thickness,
                                                             tag = 'TopTop'))
        #Draw the top part
        if self.Type[3]:
            self.AxesAdresses.append(self.Canvas.create_line((1.0-self.PaddingOut[2])*self.Canvas.Drawer.wScaleFactor,
                                                             
                                                             (self.PaddingOut[3])*self.Canvas.Drawer.hScaleFactor,
                                                             
                                                             (self.PaddingOut[0])*self.Canvas.Drawer.wScaleFactor,
                                                             
                                                             (self.PaddingOut[3])*self.Canvas.Drawer.hScaleFactor,
                                                             
                                                             fill  = self.Color,
                                                             width = self.Thickness,
                                                             tag = 'TopTop'))

        #Set the variable
        self.isAxesDrawn = True
                                                             
    def ResetAxes(self):

        '''
        ######################################################
        Does a reset of the axes for internal use after
        iupdates only...
        
        ######################################################
        '''
    
        self.RemoveAll()
    
        self.DrawAxes()
    
        self.PlaceAllTicks()
        
        self.PlaceAllLabels()


    def RemoveAll(self):

        '''
        ######################################################
        Clears all elements of the axes and redraws them
        
        - axes
        - Ticks
        - Labels
        ######################################################
        '''

        #the axes
        self.RemoveAxes()

        #remove the ticks
        self.RemoveTicks()

        #remove the Labels
        self.RemoveLabels()
    
    def RemoveAxes(self):
        
        '''
        ######################################################
        Clears the axes objects depending on the provided
        adresses
        ######################################################
        '''
        
        #check if it has been drawn before removing it
        if self.isAxesDrawn:
                                     
            #cycle through adresses to remove the elements
            for i in range(0,len(self.AxesAdresses)):
                               
                #delete the canvas element associated to the adress
                self.Canvas.delete(self.AxesAdresses[i])
            
            #empty the adress list for a redraw
            self.AxesAdresses = []
            self.isAxesDrawn  = False

    def SmartTickSpacer(self, Min, Max, Num, Type = 0 , Spacing = None):
        '''
        ######################################################
        Independant from X or Y ticks it is found that simple
        ticks recquire actually a lot of thinking. As a result
        we develop this simple routine...
        
        ######################################################
        '''
        #Initialise
        TickCoords = []
        
        #grab the range in all calculations
        Range = Max - Min
    
        #############################################
        #simple ticks regardless of beauty
        if Type == 0:

            #build tick positions
            for i in range(0,Num+1):
        
                #Create array
                TickCoords.append(Min+float(i)*(Range)/Num)

            return TickCoords
        
        #############################################
        #Ticks with spacing
        
        elif Type == 1:
            
            #set boolean
            NotSatisfied = True
            
            #start a loop
            while NotSatisfied:
            
                ########################
                ########################
                #logical variable
                bellow  = True
                i       = 0
                Sign_0  = 1
                
                #check the sign of advance
                if Min < 0:
                
                    Sign_0 = -1
                
                ########################
                #find min index
                while bellow:
                
                    #advance
                    if i*abs(Spacing) < Sign_0*Min :
                
                        i += 1
                    
                    #retrieve and break
                    else:
                        
                        Low_index = i
                        bellow = False
                        
                            
                ########################
                ########################
                #logical variable
                bellow  = True
                i       = 0
                Sign_1  = 1
                
                #check the sign of advance
                if Max < 0:
                
                    Sign_1 = -1
                
                ########################
                #find max index
                while bellow:
                
                    #advance
                    if i*abs(Spacing) <= Sign_1*Max:
                
                        i += 1

                    #retrieve and break
                    else:
                        
                        High_index = i
                        bellow = False
                        
                            
                if self.Verbose:
                
                    print 'Lower index is: ',Low_index
                    print 'High index is: ',High_index

                if Sign_0 < 0 and Sign_1 > 0:
                    
                    #build tick positions
                    for i in range(0,High_index+Low_index):
                
                        #Create array
                        TickCoords.append(i*abs(Spacing)+Low_index*Sign_0*Spacing)
                            
                elif Sign_0 > 0 and Sign_1 > 0:
                
                    #build tick positions
                    for i in range(Low_index,High_index):
                
                        #Create array
                        TickCoords.append(i*abs(Spacing))
                
                elif Sign_0 < 0 and Sign_1 < 0:
                
                    #build tick positions
                    for i in range(High_index,Low_index,):
                
                        #Create array
                        TickCoords.append(-i*abs(Spacing))

                #Do a logical chech if the Ticks are neough (minimum 5 Ticks)
                if len(TickCoords) < 5 :
                    TickCoords = []
                    Spacing = float(Spacing) / 2
                
                elif len(TickCoords) > 12:
                    
                    TickCoords = []
                    Spacing = float(Spacing) * 2
                        
                else:
                    
                    NotSatisfied = False
                    break
                
            #return the output
            
            if self.Verbose:
                print TickCoords

            return TickCoords
        
        
        

    def CalculateXTicks(self):
        
        '''
        ######################################################
        Ticks need to be calculated before being drawn
        ######################################################
        '''
        
        #grab the minima and maxima of the bounding
        if self.Canvas.Drawer.isZoomX():
        
            Min = self.Canvas.Drawer.ZoomBox[0]
            Max = self.Canvas.Drawer.ZoomBox[2]
        
        else:
        
            Min = self.Canvas.Drawer.BoundingBoxOffset[0]
            Max = self.Canvas.Drawer.BoundingBoxOffset[2]

        #Smart tick spacer
        self.XTicksCoord = self.SmartTickSpacer(Min,
                                                Max,
                                                self.XTickNumber,
                                                self.XTickType,
                                                Spacing = self.XTickSpacing)
                                                
        if self.Verbose:
            print 'The X min is: ',Min
            print 'The X Max is: ',Max
            print 'The Spacing is: ',self.XTickSpacing
            print 'The Type is: ',self.XTickType
            print 'The Ticks are:',self.XTicksCoord

    def CalculateYTicks(self):
        
        '''
        ######################################################
        Ticks need to be calculated before being drawn
        ######################################################
        '''


        #grab the minima and maxima of the bounding
        #grab the minima and maxima of the bounding
        if self.Canvas.Drawer.isZoomY():
        
            Min = self.Canvas.Drawer.ZoomBox[1]
            Max = self.Canvas.Drawer.ZoomBox[3]
        
        else:
        
            Min = self.Canvas.Drawer.BoundingBoxOffset[1]
            Max = self.Canvas.Drawer.BoundingBoxOffset[3]
        
        #Smart tick spacer
        self.YTicksCoord = self.SmartTickSpacer(Min,
                                                Max,
                                                self.YTickNumber,
                                                self.YTickType,
                                                Spacing = self.YTickSpacing)

        if self.Verbose:
            print 'The Y min is: ',Min
            print 'The Y Max is: ',Max
            print 'The Spacing is: ',self.YTickSpacing
            print 'The Type is: ',self.YTickType
            print 'The Ticks are:',self.YTicksCoord

    def PlaceAllTicks(self):
    
        '''
        ######################################################
        Places the ticks defined by self.XTicksCoord
        ######################################################
        '''
    
        #Will calculate all Ticks and place them
        self.CalculateXTicks()
        self.CalculateYTicks()
    
        #pace them
        if self.TicksActiveGrid[1]:
            
            self.PlaceXTicksBot()
        
        if self.TicksActiveGrid[3]:
            
            self.PlaceXTicksTop()
        
        if self.TicksActiveGrid[0]:
            
            self.PlaceYTicksLeft()
        
        if self.TicksActiveGrid[2]:
            
            self.PlaceYTicksRight()

    def PlaceAllLabels(self):
    
        '''
        ######################################################
        Places the Labels defined by self.XTicksCoord
        ######################################################
        '''
    
        #Will calculate all Ticks and place them
        self.CalculateXTicks()
        self.CalculateYTicks()
    
        #pace them
        if self.LabelsActiveGrid[1]:
            
            self.PlaceXLabelsBot()
        
        if self.LabelsActiveGrid[3]:
            
            self.PlaceXLabelsTop()
        
        if self.LabelsActiveGrid[0]:
            
            self.PlaceYLabelsLeft()
        
        if self.LabelsActiveGrid[2]:
            
            self.PlaceYLabelsRight()

    def PlaceGrids(self):
    
        '''
        ######################################################
        Places the Labels defined by self.XTicksCoord
        ######################################################
        '''
    
        #Will calculate all Ticks and place them
        self.CalculateXTicks()
        self.CalculateYTicks()
    
        #pace them
        if self.XGrid:
            
            self.PlaceXGrid()
        
        if self.YGrid:
            
            self.PlaceYGrid()

    def PlaceXGrid(self):

        '''
        ######################################################
        Places the ticks defined by self.XTicksCoord
        ######################################################
        '''
        
        #cycle through drawn and save ID
        for i in range(0, len(self.XTicksCoord)):
            
            self.XGridAdresses.append(self.Canvas.create_line(((self.XTicksCoord[i]-self.Canvas.Drawer.BoundingBoxOffset[0])*self.Canvas.Drawer.BoundingBoxFactor[0]
                                                              +self.PaddingIn[0]+self.PaddingOut[0])*self.Canvas.Drawer.wScaleFactor,    #X0 point of the Tick
                                                              
                                                              (1.0-self.PaddingOut[1])*self.Canvas.Drawer.hScaleFactor, #Y0 point of the Tick
                                                              
                                                              ((self.XTicksCoord[i]-self.Canvas.Drawer.BoundingBoxOffset[0])*self.Canvas.Drawer.BoundingBoxFactor[0]
                                                              +self.PaddingIn[0]+self.PaddingOut[0])*self.Canvas.Drawer.wScaleFactor,    #X1 point of the Tick
                                                              
                                                              (self.PaddingOut[3])*self.Canvas.Drawer.hScaleFactor, #Y1 point of the Tick
                                                              
                                                              fill  = self.XGridColor,
                                                              width = self.XGridThickness,
                                                              dash  = self.XGridDash,
                                                              tag = 'Grid'))
        #lower it
        self.Canvas.tag_lower('Grid')

    def PlaceYGrid(self):

        '''
        ######################################################
        Places the ticks defined by self.XTicksCoord
        ######################################################
        '''
        
        #cycle through drawn and save ID
        for i in range(0, len(self.YTicksCoord)):
            
            self.YGridAdresses.append(self.Canvas.create_line((self.PaddingOut[0])*self.Canvas.Drawer.wScaleFactor,     #X0 point of the Tick
                                                              
                                                              ((self.YTicksCoord[i]-self.Canvas.Drawer.BoundingBoxOffset[1])*self.Canvas.Drawer.BoundingBoxFactor[1]
                                                              +self.PaddingIn[3]+self.PaddingOut[3])*self.Canvas.Drawer.hScaleFactor,    #Y0 point of the Tick
                                                              
                                                              (1-self.PaddingOut[2])*self.Canvas.Drawer.wScaleFactor,     #X1 point of the Tick
                                                              
                                                              ((self.YTicksCoord[i]-self.Canvas.Drawer.BoundingBoxOffset[1])*self.Canvas.Drawer.BoundingBoxFactor[1]
                                                              +self.PaddingIn[3]+self.PaddingOut[3])*self.Canvas.Drawer.hScaleFactor,   #Y1 point of the Tick
                                                              
                                                              fill  = self.YGridColor,
                                                              width = self.YGridThickness,
                                                              dash  = self.YGridDash,
                                                              tag = 'Grid'))
        #lower it
        self.Canvas.tag_lower('Grid')
    
    def PlaceXTicksBot(self):

        '''
        ######################################################
        Places the ticks defined by self.XTicksCoord
        ######################################################
        '''
        
        #if the ticks are already drawn clear them
        if self.isXTicksDrawn[0]:

            self.RemoveTicks()

        #cycle through drawn and save ID
        for i in range(0, len(self.XTicksCoord)):
            
            self.XTickAdresses.append(self.Canvas.create_line(((self.XTicksCoord[i]-self.Canvas.Drawer.BoundingBoxOffset[0])*self.Canvas.Drawer.BoundingBoxFactor[0]
                                                              +self.PaddingIn[0]+self.PaddingOut[0])*self.Canvas.Drawer.wScaleFactor,    #X0 point of the Tick
                                                              
                                                              (1.0-self.PaddingOut[1])*self.Canvas.Drawer.hScaleFactor-self.XTickHeight, #Y0 point of the Tick
                                                              
                                                              ((self.XTicksCoord[i]-self.Canvas.Drawer.BoundingBoxOffset[0])*self.Canvas.Drawer.BoundingBoxFactor[0]
                                                              +self.PaddingIn[0]+self.PaddingOut[0])*self.Canvas.Drawer.wScaleFactor,    #X1 point of the Tick
                                                              
                                                              (1.0-self.PaddingOut[1])*self.Canvas.Drawer.hScaleFactor+self.XTickHeight, #Y1 point of the Tick
                                                              
                                                              fill  = self.XTickColor[1],
                                                              width = self.XTickThickness,
                                                              tag = 'Top'))


    def PlaceXTicksTop(self):

        '''
        ######################################################
        Places the ticks defined by self.XTicksCoord
        ######################################################
        '''
        
        #if the ticks are already drawn clear them
        if self.isXTicksDrawn[1]:

            self.RemoveTicks()

        #cycle through drawn and save ID
        for i in range(0, len(self.XTicksCoord)):
            
            self.XTickAdresses.append(self.Canvas.create_line(((self.XTicksCoord[i]-self.Canvas.Drawer.BoundingBoxOffset[0])*self.Canvas.Drawer.BoundingBoxFactor[0]
                                                              +self.PaddingIn[0]+self.PaddingOut[0])*self.Canvas.Drawer.wScaleFactor,    #X0 point of the Tick
                                                              
                                                              (self.PaddingOut[3])*self.Canvas.Drawer.hScaleFactor-self.XTickHeight,     #Y0 point of the Tick
                                                              
                                                              ((self.XTicksCoord[i]-self.Canvas.Drawer.BoundingBoxOffset[0])*self.Canvas.Drawer.BoundingBoxFactor[0]
                                                              +self.PaddingIn[0]+self.PaddingOut[0])*self.Canvas.Drawer.wScaleFactor,    #X1 point of the Tick
                                                              
                                                              (self.PaddingOut[3])*self.Canvas.Drawer.hScaleFactor+self.XTickHeight,     #Y1 point of the Tick
                                                              
                                                              fill  = self.XTickColor[0],
                                                              width = self.XTickThickness,
                                                              tag = 'Top'))
            
    def PlaceYTicksLeft(self):

        '''
        ######################################################
        Places the ticks defined by self.XTicksCoord
        ######################################################
        '''
        
        #if the ticks are already drawn clear them
        if self.isYTicksDrawn[0]:

            self.RemoveTicks()

        #cycle through drawn and save ID
        for i in range(0, len(self.YTicksCoord)):
            
            self.YTickAdresses.append(self.Canvas.create_line((self.PaddingOut[0])*self.Canvas.Drawer.wScaleFactor-self.YTickHeight,     #X0 point of the Tick
                                                              
                                                              ((self.YTicksCoord[i]-self.Canvas.Drawer.BoundingBoxOffset[1])*self.Canvas.Drawer.BoundingBoxFactor[1]
                                                              +self.PaddingIn[3]+self.PaddingOut[3])*self.Canvas.Drawer.hScaleFactor,    #Y0 point of the Tick
                                                              
                                                              (self.PaddingOut[0])*self.Canvas.Drawer.wScaleFactor+self.YTickHeight,     #X1 point of the Tick
                                                              
                                                              ((self.YTicksCoord[i]-self.Canvas.Drawer.BoundingBoxOffset[1])*self.Canvas.Drawer.BoundingBoxFactor[1]
                                                              +self.PaddingIn[3]+self.PaddingOut[3])*self.Canvas.Drawer.hScaleFactor,   #Y1 point of the Tick
                                                              
                                                              
                                                              fill  = self.YTickColor[0],
                                                              width = self.YTickThickness,
                                                              tag = 'Top'))


    def PlaceYTicksRight(self):

        '''
        ######################################################
        Places the ticks defined by self.XTicksCoord
        ######################################################
        '''
        
        #if the ticks are already drawn clear them
        if self.isYTicksDrawn[1]:

            self.RemoveTicks()

        #cycle through drawn and save ID
        for i in range(0, len(self.YTicksCoord)):
            
            self.YTickAdresses.append(self.Canvas.create_line((1-self.PaddingOut[2])*self.Canvas.Drawer.wScaleFactor-self.YTickHeight,     #X0 point of the Tick
                                                              
                                                              ((self.YTicksCoord[i]-self.Canvas.Drawer.BoundingBoxOffset[1])*self.Canvas.Drawer.BoundingBoxFactor[1]
                                                               +self.PaddingIn[3]+self.PaddingOut[3])*self.Canvas.Drawer.hScaleFactor,    #Y0 point of the Tick
                                                              
                                                              (1-self.PaddingOut[2])*self.Canvas.Drawer.wScaleFactor+self.YTickHeight,     #X1 point of the Tick
                                                              
                                                              ((self.YTicksCoord[i]-self.Canvas.Drawer.BoundingBoxOffset[1])*self.Canvas.Drawer.BoundingBoxFactor[1]
                                                               +self.PaddingIn[3]+self.PaddingOut[3])*self.Canvas.Drawer.hScaleFactor,   #Y1 point of the Tick
                                                              
                                                              fill  = self.YTickColor[1],
                                                              width = self.YTickThickness,
                                                              tag = 'Top'))
    def PlaceXLabelsBot(self):

        '''
        ######################################################
        Places the ticks defined by self.XTicksCoord
        ######################################################
        '''
        
        #if the ticks are already drawn clear them
        if self.isXTicksDrawn[0]:

            self.RemoveTicks()

        #cycle through drawn and save ID
        for i in range(0, len(self.XTicksCoord)):
            
            if self.isXSci:
            
                Text = self.XSciPrecision % self.XTicksCoord[i]
            
            else:
            
                Text = str(round(self.XTicksCoord[i],self.XLabelRounding))
            
            self.XLabelAdresses.append(self.Canvas.create_text(((self.XTicksCoord[i]-self.Canvas.Drawer.BoundingBoxOffset[0])*self.Canvas.Drawer.BoundingBoxFactor[0]
                                                               +self.PaddingIn[0]+self.PaddingOut[0])*self.Canvas.Drawer.wScaleFactor,    #X0 point of the Tick
                                                               (1.0-self.PaddingOut[1]+self.XLabelOffset)*self.Canvas.Drawer.hScaleFactor, #Y0 point of the Tick
                                                               fill  = self.XLabelColor[0],
                                                               font = self.XLabelSize[0],
                                                               text = Text,
                                                               tag = 'Top'))


    def PlaceXLabelsTop(self):

        '''
        ######################################################
        Places the ticks defined by self.XTicksCoord
        ######################################################
        '''
        
        #if the ticks are already drawn clear them
        if self.isXTicksDrawn[1]:

            self.RemoveTicks()

        #cycle through drawn and save ID
        for i in range(0, len(self.XTicksCoord)):
            
            if self.isXSci:
            
                Text = self.XSciPrecision % self.XTicksCoord[i]
            
            else:
            
                Text = str(round(self.XTicksCoord[i],self.XLabelRounding))
            
            self.XLabelAdresses.append(self.Canvas.create_text(((self.XTicksCoord[i]-self.Canvas.Drawer.BoundingBoxOffset[0])*self.Canvas.Drawer.BoundingBoxFactor[0]
                                                               +self.PaddingIn[0]+self.PaddingOut[0])*self.Canvas.Drawer.wScaleFactor,    #X0 point of the Tick
                                                               
                                                               (self.PaddingOut[3]-self.XLabelOffset)*self.Canvas.Drawer.hScaleFactor,    #Y0 point of the Tick
                                                               
                                                               fill  = self.XLabelColor[1],
                                                               font = self.XLabelSize[1],
                                                               text = Text,
                                                               tag = 'Top'))
            #check item height
            coords = self.Canvas.bbox(self.XLabelAdresses[-1])
            
            #move it
            self.Canvas.move(self.XLabelAdresses[-1], 0,-(coords[3]-coords[1]))
            
    def PlaceYLabelsLeft(self):

        '''
        ######################################################
        Places the ticks defined by self.XTicksCoord
        ######################################################
        '''
        
        #if the ticks are already drawn clear them
        if self.isYTicksDrawn[0]:

            self.RemoveTicks()

        #cycle through drawn and save ID
        for i in range(0, len(self.YTicksCoord)):
            
            if self.isYSci:
            
                Text = self.YSciPrecision % self.YTicksCoord[-1-i]
            
            else:
            
                Text = str(round(self.YTicksCoord[-1-i],self.YLabelRounding))
            
            self.YLabelAdresses.append(self.Canvas.create_text((self.PaddingOut[0]-self.YLabelOffset)*self.Canvas.Drawer.wScaleFactor,     #X0 point of the Tick
                                                               
                                                               ((self.YTicksCoord[i]-self.Canvas.Drawer.BoundingBoxOffset[1])*self.Canvas.Drawer.BoundingBoxFactor[1]
                                                               +self.PaddingIn[3]+self.PaddingOut[3])*self.Canvas.Drawer.hScaleFactor,    #Y0 point of the Tick
                                                               
                                                               fill  = self.YLabelColor[0],
                                                               font = self.YLabelSize[0],
                                                               text = Text,
                                                               tag = 'Top'))


    def PlaceYLabelsRight(self):

        '''
        ######################################################
        Places the ticks defined by self.XTicksCoord
        ######################################################
        '''
        
        #if the ticks are already drawn clear them
        if self.isYTicksDrawn[1]:

            self.RemoveTicks()

        #cycle through drawn and save ID
        for i in range(0, len(self.YTicksCoord)):
            
            if self.isYSci:
            
                Text = self.YSciPrecision % self.YTicksCoord[-1-i]
            
            else:
            
                Text = str(round(self.YTicksCoord[i],self.YLabelRounding))
            
            self.YLabelAdresses.append(self.Canvas.create_text((1-self.PaddingOut[2]+self.YLabelOffset)*self.Canvas.Drawer.wScaleFactor,     #X0 point of the Tick
                                                               
                                                               ((self.YTicksCoord[i]-self.Canvas.Drawer.BoundingBoxOffset[1])*self.Canvas.Drawer.BoundingBoxFactor[1]
                                                                +self.PaddingIn[3]+self.PaddingOut[3])*self.Canvas.Drawer.hScaleFactor,    #Y0 point of the Tick
                                                               
                                                               fill  = self.YLabelColor[1],
                                                               font = self.YLabelSize[1],
                                                               text = Text,
                                                               tag = 'Top'))
            #check item height
            coords = self.Canvas.bbox(self.YLabelAdresses[-1])
            
            #move it
            self.Canvas.move(self.YLabelAdresses[-1], (coords[2]-coords[0]),0)
                                                               
    def RemoveTicks(self):

        '''
        ######################################################
        Supposed to remove all the ticks of the current
        figure. It doesnt matter whaere they are as we are
        workign on an adresse basis. 
        
        Thi means thta we remove all adreses we can find
        ######################################################
        '''


        #for the X Ticks
        for i in range(0, len(self.XTickAdresses)):

            #remove the associated item
            self.Canvas.delete(self.XTickAdresses[i])
                
        #for the X Ticks
        for i in range(0, len(self.YTickAdresses)):

            #remove the associated item
            self.Canvas.delete(self.YTickAdresses[i])

    def RemoveLabels(self):

        '''
        ######################################################
        Supposed to remove all the ticks of the current
        figure. It doesnt matter whaere they are as we are
        workign on an adresse basis. 
        
        Thi means thta we remove all adreses we can find
        ######################################################
        '''


        #for the X Ticks
        for i in range(0, len(self.XLabelAdresses)):

            #remove the associated item
            self.Canvas.delete(self.XLabelAdresses[i])

        #for the X Ticks
        for i in range(0, len(self.YLabelAdresses)):

            #remove the associated item
            self.Canvas.delete(self.YLabelAdresses[i])


    def RemoveGrids(self):

        '''
        ######################################################
        Supposed to remove all the ticks of the current
        figure. It doesnt matter whaere they are as we are
        workign on an adresse basis. 
        
        Thi means thta we remove all adreses we can find
        ######################################################
        '''


        #for the X Ticks
        for i in range(0, len(self.XGridAdresses)):

            #remove the associated item
            self.Canvas.delete(self.XGridAdresses[i])

        #for the X Ticks
        for i in range(0, len(self.YGridAdresses)):

            #remove the associated item
            self.Canvas.delete(self.YGridAdresses[i])

class Legend:
    
    '''
    ######################################################
    in an effort to be more modulable it tought more
    advantageouse to creta a class for each plot. This way
    the parameters and adresses are more obvious.
    
    it will also allow easier fetching in the settings
    to allow data manipulation and statistics
    ######################################################
    '''
    
    def __init__(self,X,Y,
                 Thickness = 1,
                 Color = 'black',
                 Active = True,
                 Name = '',
                 style = ['',0,0]):


        #set the variables
        self.X          = X
        self.Y          = Y
        self.Name       = Name
        
        #set the parameters
        self.Thickness  = Thickness
        self.Color      = Color
        self.Active     = Active

        #set the style
        self.Style = style
        self.Verbose        = False

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

class PlotClass:
    
    '''
    ######################################################
    in an effort to be more modulable it tought more
    advantageouse to creta a class for each plot. This way
    the parameters and adresses are more obvious.
    
    it will also allow easier fetching in the settings
    to allow data manipulation and statistics
    ######################################################
    '''
    
    def __init__(self,X,Y,
                 Thickness = 1,
                 Color = 'black',
                 Active = True,
                 Name = '',
                 style = ['',0,0],
                 Indentifier = None):


        #set the variables
        self.X          = X
        self.Y          = Y
        self.Name       = Name
        self.DataPool   = None
        
        #set the parameters
        self.Thickness  = Thickness
        self.Color      = Color
        self.Active     = Active

        #set the style
        self.Style = style
    
        #identifier
        self.Identifier     = Indentifier
        self.IdentifierList = []
        self.CanvasObject   = False
        self.Verbose = False

    def FetchNewData(self):
        '''
        ######################################################
        This method is here to fetch the new data from
        a dataset
        ######################################################
        '''
        print self.DataPool
    
    def DrawPIL(self, Target, Parameters):

        '''
        ######################################################
        all plot elements will have an implicit draw method
        that will prepare the method and arguments to be drawn
        This instance will output the content into PIL
        ######################################################
        '''
                      
        #make the plot list
        DrawList = [(((self.X[j]-Parameters[0][0])*Parameters[1][0]
                      +Parameters[2][0]+Parameters[3][0])*Parameters[4]*Parameters[6],
                     (-(self.Y[j]-Parameters[0][1])*Parameters[1][1]
                      +1-Parameters[2][1]-Parameters[3][1])*Parameters[5]*Parameters[6])
                    for j in range(0,len(self.X))]
                
        #draw the object
        Target.line(DrawList,
                    fill    =   ColorLib.getrgb(self.Color),
                    width   =   self.Thickness*Parameters[6])
    
    
        #Do we need scater circles
        if self.Style[0] == 'o':
            
            for j in range(0,len(DrawList)):
            
                #draw the circle
                Target.ellipse((DrawList[j][0]-self.Style[1]*Parameters[6],
                                DrawList[j][1]-self.Style[2]*Parameters[6],
                                DrawList[j][0]+self.Style[1]*Parameters[6],
                                DrawList[j][1]+self.Style[2]*Parameters[6]),
                                fill = ColorLib.getrgb(self.Color))

        #set the state
        self.CanvasObject   = False
    
    
    def DrawPyG(self, Target, Parameters):
        '''
        ######################################################
        PyGame imaging echnique. Note that this explicitly 
        calls an antialliassing method that is the line ...
        ######################################################
        '''
        if self.Active:
            
            ########################
            #make the plot list
            DrawList = [(((self.X[j]-Parameters[0][0])*Parameters[1][0]
                          +Parameters[2][0]+Parameters[3][0])*Parameters[4],
                         
                         ((self.Y[j]-Parameters[0][1])*Parameters[1][1]
                          +Parameters[2][1]+Parameters[3][1])*Parameters[5])
                        for j in range(0,len(self.X))]

            ########################
            #Draw the anti alliased elements
            for l in range(0,len(DrawList)-1):
            
                self.AntiAlliasLine(Target, DrawList[l],DrawList[l+1])
            
            
            ########################
            #Do we need scater circles
            if self.Style[0] == 'o':
                
                for j in range(0,len(DrawList)-1):
                
                    self.AntiAlliasEllipse(Target, DrawList[l],[self.Style[1],self.Style[2]])
    
            
            if self.Verbose:
                
                print 'Trying to draw:\n',DrawList
                print Parameters
        
            #set the state
            self.CanvasObject   = False

    def AntiAlliasLine(self, Target, X0,X1):
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
        pygame.gfxdraw.filled_polygon(Target, (UL, UR, BR, BL),  ColorLib.getrgb(self.Color))
        
        #draw the cicrle at first end
        pygame.gfxdraw.aacircle(Target, int(X0[0]), int(X0[1]), int((self.Thickness / 2)),   ColorLib.getrgb(self.Color))
        pygame.gfxdraw.filled_circle(Target, int(X0[0]), int(X0[1]), int((self.Thickness / 2)),   ColorLib.getrgb(self.Color))
        
        #draw the circle at the last end
        pygame.gfxdraw.aacircle(Target, int(X1[0]), int(X1[1]), int((self.Thickness / 2)),   ColorLib.getrgb(self.Color))
        pygame.gfxdraw.filled_circle(Target, int(X1[0]), int(X1[1]), int((self.Thickness / 2)),   ColorLib.getrgb(self.Color))
    
    def AntiAlliasEllipse(self, Target, X, R):
        '''
        ######################################################
        This draws an anti alliased elipse according to the 
        gfx antia alliased method
        ######################################################
        '''
        
        #draw the circle at the last end
        pygame.gfxdraw.aaellipse(Target, int(X[0]), int(X[1]), R[0] / 2, R[1] / 2,   ColorLib.getrgb(self.Color))
        pygame.gfxdraw.filled_ellipse(Target, int(X[0]), int(X[1]), R[0] / 2, R[1] / 2,   ColorLib.getrgb(self.Color))
    
    def DrawCanvas(self, Target, Parameters):

        '''
        ######################################################
        all plot elements will have an implicit draw method
        that will prepare the method and arguments to be drawn
        This Method will use the canvas draw method
        ######################################################
        '''
        
        self.IdentifierList = []
        
        #make the plot list
        DrawList = [(((self.X[j]-Parameters[0][0])*Parameters[1][0]
                      +Parameters[2][0]+Parameters[3][0])*Parameters[4],
                     (-(self.Y[j]-Parameters[0][1])*Parameters[1][1]
                      +1-Parameters[2][1]-Parameters[3][1])*Parameters[5])
                    for j in range(0,len(self.X))]

        #draw the object
        self.IdentifierList.append(Target.create_line(DrawList,
                                                      fill     =   self.Color,
                                                      width    =   self.Thickness,
                                                      tag = 'Top'))

        #Do we need scater circles
        if self.Style[0] == 'o':
            
            for j in range(0,len(DrawList)):
            
                #draw the circle
                self.IdentifierList.append(Target.create_oval((DrawList[j][0]-self.Style[1],
                                                              DrawList[j][1]-self.Style[2],
                                                              DrawList[j][0]+self.Style[1],
                                                              DrawList[j][1]+self.Style[2]),
                                                              fill = self.Color,
                                                              tag = 'Top'))

        #set the state
        self.CanvasObject   = True

class OneDProjectionClass:
    
    '''
    ######################################################
    This function aims at grabing the line from a contour
    plot data when requested and redraws it on request
    ######################################################
    '''
    
    def __init__(self,
                 Contour,
                 Thickness = 1,
                 Color = 'black',
                 Active = True,
                 Type = 'x',
                 Name = '',
                 style = ['',0,0],
                 Indentifier = None):


        #set the variables
        self.LinkContour(Contour)
        
        self.Type       = Type
        
        #grabe the name if necessary
        self.Name       = Name
        
        #set the parameters
        self.Thickness  = Thickness
        self.Color      = Color
        self.Active     = Active

        #set the style
        self.Style = style
    
        #identifier
        self.Identifier     = Indentifier
        self.IdentifierList = []
        self.CanvasObject   = False
    
        #grab the new data
        self.FetchNewData(0)
    
    def LinkContour(self,Contour):
        '''
        ######################################################
        This method is here to fetch the new data from
        a dataset
        ######################################################
        '''
        
        self.XDataPool  = [Contour.X[i][1] for i in range(0, len(Contour.X))]
        self.YDataPool  = numpy.asarray(Contour.Y[1]).tolist()
        self.ZDataPool  = numpy.asarray(Contour.Z)

    def FetchNewData(self,Index):
        '''
        ######################################################
        This method is here to fetch the new data from
        a dataset
        ######################################################
        '''
        
        if self.Type == 'y':
        
            self.Y = self.YDataPool
            self.X = self.ZDataPool[Index,:]

        if self.Type == 'x':
        
            self.X = self.XDataPool
            self.Y = self.ZDataPool[:,Index]
    
    def DrawPIL(self, Target, Parameters):

        '''
        ######################################################
        all plot elements will have an implicit draw method
        that will prepare the method and arguments to be drawn
        This instance will output the content into PIL
        ######################################################
        '''
                      
        #make the plot list
        DrawList = [(((self.X[j]-Parameters[0][0])*Parameters[1][0]
                      +Parameters[2][0]+Parameters[3][0])*Parameters[4]*Parameters[6],
                     (-(self.Y[j]-Parameters[0][1])*Parameters[1][1]
                      +1-Parameters[2][1]-Parameters[3][1])*Parameters[5]*Parameters[6])
                    for j in range(0,len(self.X))]
                
        #draw the object
        Target.line(DrawList,
                    fill    =   Color.getrgb(self.Color),
                    width   =   self.Thickness*Parameters[6])
    
    
        #Do we need scater circles
        if self.Style[0] == 'o':
            
            for j in range(0,len(DrawList)):
            
                #draw the circle
                Target.ellipse((DrawList[j][0]-self.Style[1]*Parameters[6],
                                DrawList[j][1]-self.Style[2]*Parameters[6],
                                DrawList[j][0]+self.Style[1]*Parameters[6],
                                DrawList[j][1]+self.Style[2]*Parameters[6]),
                                fill = ColorLib.getrgb(self.Color))

        #set the state
        self.CanvasObject   = False
                                
    def DrawCanvas(self, Target, Parameters):

        '''
        ######################################################
        all plot elements will have an implicit draw method
        that will prepare the method and arguments to be drawn
        This Method will use the canvas draw method
        ######################################################
        '''
        
        self.IdentifierList = []
        
        #make the plot list
        DrawList = [(((self.X[j]-Parameters[0][0])*Parameters[1][0]
                      +Parameters[2][0]+Parameters[3][0])*Parameters[4],
                     (-(self.Y[j]-Parameters[0][1])*Parameters[1][1]
                      +1-Parameters[2][1]-Parameters[3][1])*Parameters[5])
                    for j in range(0,len(self.X))]

        #draw the object
        self.IdentifierList.append(Target.create_line(DrawList,
                                                      fill     =   self.Color,
                                                      width    =   self.Thickness,
                                                      tag = 'Top'))

        #Do we need scater circles
        if self.Style[0] == 'o':
            
            for j in range(0,len(DrawList)):
            
                #draw the circle
                self.IdentifierList.append(Target.create_oval((DrawList[j][0]-self.Style[1],
                                                              DrawList[j][1]-self.Style[2],
                                                              DrawList[j][0]+self.Style[1],
                                                              DrawList[j][1]+self.Style[2]),
                                                              fill = self.Color,
                                                              tag = 'Top'))

        #set the state
        self.CanvasObject   = True

class ContourClass:
    
    '''
    ######################################################
    in an effort to be more modulable it tought more
    advantageouse to creta a class for each plot. This way
    the parameters and adresses are more obvious.
    
    it will also allow easier fetching in the settings
    to allow data manipulation and statistics
    ######################################################
    '''
    
    def __init__(self,
                 #Data variables
                 X,Y,Z,
                 
                 #General variables
                 Type = 'Surface',
                 Range = None,
                 Active = True,
                 Name = '',
                 style = [0,0,0],
                 Indentifier = None,
                 
                 #Surface variables
                 ColorList = None,
                 Stepping  = 10,
                 
                 #Mesh variables
                 MeshColorList = None,
                 MeshStepping  = 10,
                 MeshThickness = 5):

        ########################
        #set the Common variables
        self.XIni       = X
        self.YIni       = Y
        self.ZIni       = Z
        
        self.Name       = Name
        self.Verbose    = False
        self.Verbose_2  = False
        self.PyGDrawn   = False
        self.Type       = Type
        self.Range      = Range
        self.Processors = 1
        
        ############################################################
        #set the parameters
        self.Active     = Active

        #set the style
        self.Style = style
    
        #identifier
        self.Identifier     = Indentifier
        self.IdentifierList = []
        self.CanvasObject   = False
        
        ########################
        #set the Surface variables
        self.ColorList  = ColorList
        self.Stepping   = Stepping
        self.MeshStepping = MeshStepping
        
        ########################
        #set the Mesh variables
        self.MeshColorList  = MeshColorList
        self.MeshThickness  = MeshThickness
        
        
        if self.Verbose:
            
            print X,Y,Z
            print Stepping
            print Type
            print Range
            print Thickness
            print color
            print Active
            print Name
            print style
            print Indentifier
                
        #define the projections X and Y
        self.Projections = [None,None]
        
        #compute boundaries once
        if Range == None:
        
            self.ZMax = max([max(self.ZIni[j]) for j in range(0,len(self.ZIni))])
            self.ZMin = min([min(self.ZIni[j]) for j in range(0,len(self.ZIni))])
        
        else:
        
            self.ZMax = Range[1]
            self.ZMin = Range[0]
        
        #set X boundaries
        self.XMax = max([max(self.XIni[j]) for j in range(0,len(self.XIni))])
        self.XMin = min([min(self.XIni[j]) for j in range(0,len(self.XIni))])
        
        #Set X Scale
        self.XScale = self.XMax - self.XMin
        
        #Set Y boundaries
        self.YMax = max([max(self.YIni[j]) for j in range(0,len(self.YIni))])
        self.YMin = min([min(self.YIni[j]) for j in range(0,len(self.YIni))])
        
        #set Y Scale
        self.YScale = self.YMax - self.YMin
        
        #Prepaer the new arrays
        self.X = numpy.asarray(self.XIni)
        self.Y = numpy.asarray(self.YIni)
        self.Z = numpy.asarray(self.ZIni)

        ##############
        #visual
        if self.Verbose:
        
            print self.Z
            print self.X
            print self.Y
        
        ##############
        #conver the basterd to lis
        self.X = self.X.tolist()
        self.Y = self.Y.tolist()
        self.Z = self.Z.tolist()
        
        
    
        #build a color map
        if self.ColorList == None:
            self.ColorList = ['blue','green','yellow','red']
        
        if self.MeshColorList == None:
            self.MeshColorList = ['black','black']
        
        #initialise the variabes
        self.RGB = []
        self.MeshRGB = []
        
        for i in range(0,len(self.ColorList)-1):
            
            First   =  ColorLib.getrgb(self.ColorList[i])
            Last    =  ColorLib.getrgb(self.ColorList[i+1])
        
            for k in range(0,int(Stepping/(len(self.ColorList)-1))+1):
        
        
                self.RGB.append((k*(Last[0]-First[0])/int(Stepping/(len(self.ColorList)-1))+First[0],
                                 k*(Last[1]-First[1])/int(Stepping/(len(self.ColorList)-1))+First[1],
                                 k*(Last[2]-First[2])/int(Stepping/(len(self.ColorList)-1))+First[2]))
    
        for i in range(0,len(self.MeshColorList)-1):
            
            First   =  ColorLib.getrgb(self.MeshColorList[i])
            Last    =  ColorLib.getrgb(self.MeshColorList[i+1])
        
            for k in range(0,int(MeshStepping/(len(self.MeshColorList)-1))+1):
        
        
                self.MeshRGB.append((k*(Last[0]-First[0])/int(Stepping/(len(self.MeshColorList)-1))+First[0],
                                     k*(Last[1]-First[1])/int(Stepping/(len(self.MeshColorList)-1))+First[1],
                                     k*(Last[2]-First[2])/int(Stepping/(len(self.MeshColorList)-1))+First[2]))
        
        #run once
        self.Run()


    def Run(self):

        '''
        ######################################################
        Because the XYZ matrix elements are raw some islanding
        needs to be dones. This is givzn by the separation 
        matrix given by the steping matrix
        
        This will effectively scan the matrix and create
        ContourPolygane classes which will have the
        coordinates, the colors and if they are inside or
        outside shaped...
        ######################################################
        '''
        #######################################
        #first check if the dimentionality is right
        if not len(self.X) == len(self.Y) or not len(self.Y) == len(self.Z):
            
            #break right here
            if self.Verbose:
            
                print 'Dimentionality test failed'
                print len(self.X) ,len(self.Y) ,len(self.Z)
            
            return 0

        if not len(self.X[0]) == len(self.Y[0]) or not len(self.Y[0]) == len(self.Z[0]):
            
            #break right here
            if self.Verbose:
                
                print 'Dimentionality test failed'
                print len(self.X[0]) , len(self.Y[0]) , len(self.Z[0])
            
            #break right here
            return 0
        
        #######################################
        #compute boundaries
        Max = self.ZMax
        Min = self.ZMin
        
        #break right here
        if self.Verbose:
                
            print 'This is the found Max: ',Max
            print 'This is the found Min: ',Min
        
        #######################################
        #compute boundaries
        self.Range = [Min + float(i) * (Max - Min)/float(self.Stepping) for i in range(0,self.Stepping)]
        self.MeshRange = [Min + float(i) * (Max - Min)/float(self.MeshStepping) for i in range(0,self.MeshStepping)]
        
        if self.Verbose:
                
            print 'This is the Range:\n ',self.Range
        
        #######################################
        #create scanner clases
            
        #create scanner class
        self.Scanner = ContourScannerClass(self)

        #run him
        self.Surfaces,self.Meshes = self.Scanner.Scan('Normal')
        
        #Set the color
        for l in range(len(self.Surfaces)):
            
            for k in range(len(self.Surfaces[l])):
                
                #set the parameters
                self.Surfaces[l][k].Color = self.RGB[l]
                
        for l in range(len(self.Meshes)):
            
            for k in range(len(self.Meshes[l])):

                #set the parameters
                self.Meshes[l][k].Thickness = self.MeshThickness
                self.Meshes[l][k].Color     = self.MeshRGB[l]


    def DrawPyG(self, Target, Parameters,xi,xf,yi,yf):
        '''
        ######################################################
        Send in the draw command for polygons
        ######################################################
        '''
        #write time doyn
        start = time.time()
        
        #draw the high resolution if not yet available
        if not self.PyGDrawn:
            
            if self.Verbose_2:
                print 'Initialising the drawer'
            
            #launch drawer
            self.IniPyGDrawer()
    
            self.PyGDrawn = True
                
        if not xi == None and not xf == None and not yi == None and not yf == None:
            
            
            #crop a part of the initial image
            crop_rect = ((xi-self.XMin)*self.DrawFactorX,
                         (yi-self.YMin)*self.DrawFactorY,
                         (xf-xi)*self.DrawFactorX,
                         (yf-yi)*self.DrawFactorY)
                         
            cropped = self.DrawSurface.subsurface(crop_rect)
            
            if self.Verbose_2:

                print 'This is the croping rectangle', crop_rect

            pyg.image.save(Target,'Croped.png')
            
            #now resize it to match the scale
            ResizeSurface = pyg.transform.scale(cropped,
                                                (int(crop_rect[2]/self.DrawFactorX*Parameters[1][0]*Parameters[4]),
                                                 int(crop_rect[3]/self.DrawFactorY*Parameters[1][1]*Parameters[5])))
        
        else:
        
            #grab the entire image
            cropped = self.DrawSurface.copy()
            
            if self.Verbose_2:
                print 'This is the Croped size: ', cropped.get_rect()
            
            #resize it
            ResizeSurface = pyg.transform.scale(cropped,
                                                (int(self.XScale*Parameters[1][0]*Parameters[4]),
                                                 int(self.YScale*Parameters[1][1]*Parameters[5])))
        
        if self.Verbose_2:
            print 'This is the Resized size: ', ResizeSurface.get_rect()

        if self.Verbose_2:
            print 'This is the Target size: ', Target.get_rect()
            print Parameters
            print 'This is the rescaling: ',(int(Parameters[1][0]*Parameters[4]),int(Parameters[1][1]*Parameters[5]))
            print 'This is the offset: ',((Parameters[2][0]+Parameters[3][0])*Parameters[4],(1-Parameters[2][1]-Parameters[3][1])*Parameters[5])
        
        #now we have to position this properly
        Target.blit(ResizeSurface,
                    ((Parameters[2][0]+Parameters[3][0])*Parameters[4],
                     (Parameters[2][1]+Parameters[3][1])*Parameters[5]))
         
        if self.Verbose_2:
            pyg.image.save(Target,'Target.png')
                     
        #set logic
        self.CanvasObject = False
    
        #print the time out
        end = time.time()
        
        print 'time spent Bliting in PyGame: ', end-start

    

    def IniPyGDrawer(self):
        '''
        ######################################################
        This will draw the initial Pyg fram and will be
        expensive and then set the PYG, Drawn to true
        
        Parameters = [self.BoundingBoxOffset,
                      self.BoundingBoxFactor,
                      self.Axes.PaddingIn,
                      self.Axes.PaddingOut,
                      self.wScaleFactor,
                      self.hScaleFactor,
                      SamplingFactor]
                      
                      
        DrawList[j] = (int(((self.Coordinates[j][0]-Parameters[0][0])*Parameters[1][0]
                              +Parameters[2][0]+Parameters[3][0])*Parameters[4]),
                               
                               int((-(self.Coordinates[j][1]-Parameters[0][1])*Parameters[1][1]
                                +1-Parameters[2][1]-Parameters[3][1])*Parameters[5]))
        ######################################################
        '''
        
        #make sure the image has a high enough resolution for drwing
        self.XPixels      = len(self.X)*10#int(numpy.max([len(self.X),len(self.X[0])]))
        self.YPixels      = len(self.X[0])*10
        
        if self.Verbose_2:
            print 'This is XPixels: ',self.XPixels
            print 'This is YPixels: ',self.YPixels
        
        self.DrawFactorX = self.XPixels/self.XScale
        self.DrawFactorY = self.YPixels/self.YScale
        
        #create artificial parameters
        Parameters = [[self.XMin,self.YMin,0,0],
                      [1,1,0,0],
                      [0,0,0,0],
                      [0,0,0,0],
                      self.DrawFactorX,
                      self.DrawFactorY,
                      1]
        
        if self.Verbose_2:
            print 'The dimention of the picture', (self.XPixels,self.YPixels)
        
        #create an optimal surface (no pixels lost yet)
        self.DrawSurface   = pyg.Surface((self.XPixels,
                                          self.YPixels))
                                          
        #make the background white
        self.DrawSurface.fill((255,255,255)) # fill background white
        
        if self.Verbose_2:
            print 'This is the DrawSurface size: ', self.DrawSurface.get_rect()
        
        #write time doyn
        start = time.time()
        
        #####################
        #draw up the surfaces
        Index = 0
        
        for i in range(len(self.Surfaces)):

            for j in range(len(self.Surfaces[i])):
                
                self.Surfaces[i][j].DrawPyG(self.DrawSurface, Parameters)
                
                Index += 1
        
        ##################
        #draw up the meshes
        Index = 0
        
        for i in range(len(self.Meshes)):

            for j in range(len(self.Meshes[i])):
                
                self.Meshes[i][j].DrawPyG(self.DrawSurface, Parameters)
                
                Index += 1
        
        #set logic
        self.CanvasObject = False
    
        #print the time out
        end = time.time()
        
        print 'time spent drawing in PyGame: ', end-start
        print 'Drew this amout of polygones: ',Index

        if self.Verbose:
            pyg.image.save(self.DrawSurface,'Hello.png')

    def DrawPIL(self, Target, Parameters,xi,xf,yi,yf):
        '''
        ######################################################
        Send in the draw command for polygons
        ######################################################
        '''
        #write time doyn
        start = time.time()
        
        #draw up
        for i in range(len(self.Surfaces)):

            for j in range(len(self.Surfaces[i])):
                
                if xi == None and self.Surfaces[i][j].Active:
                    
                    self.Surfaces[i][j].DrawPIL(Target, Parameters)
                
                elif self.Surfaces[i][j].Check(xi,xf,yi,yf):
                    
                    self.Surfaces[i][j].DrawPIL(Target, Parameters)
    
        #draw up
        for i in range(len(self.Meshes)):

            for j in range(len(self.Meshes[i])):
                
                if xi == None and self.Meshes[i][j].Active:
                    
                    self.Meshes[i][j].DrawPIL(Target, Parameters)
                
                elif self.Meshes[i][j].Check(xi,xf,yi,yf):
                    
                    self.Meshes[i][j].DrawPIL(Target, Parameters)

        #set logic
        self.CanvasObject = False

        #print the time out
        end = time.time()
        print 'time spent drawing in PIL: ', end-start



    def DrawCanvas(self, Target, Parameters,xi,xf,yi,yf):
        '''
        ######################################################
        Send in the draw command for polygons
        ######################################################
        '''
        
        #reset the list
        self.IdentifierList = []
        
        #draw up
        for i in range(0, len(self.Surfaces)):

            for j in range(0, len(self.Surfaces[i])):
                
                if xi == None and self.Surfaces[i][j].Active:
                    
                    self.IdentifierList.append(self.Surfaces[i][j].DrawCanvas(Target, Parameters))
                
                elif self.Surfaces[i][j].Check(xi,xf,yi,yf):
                    
                    self.IdentifierList.append(self.Surfaces[i][j].DrawCanvas(Target, Parameters))
    
        #draw up
        for i in range(0, len(self.Meshes)):

            for j in range(0, len(self.Meshes[i])):
                
                if xi == None and self.Meshes[i][j].Active:
                    
                    self.IdentifierList.append(self.Meshes[i][j].DrawCanvas(Target, Parameters))
                
                elif self.Meshes[i][j].Check(xi,xf,yi,yf):
                    
                    self.IdentifierList.append(self.Meshes[i][j].DrawCanvas(Target, Parameters))
                    
        #Set Logic
        self.CanvasObject = True


class PolygoneClass:
    
    '''
    ######################################################
    These will be the polygones which only call a draw
    method inside
    ######################################################
    '''
    
    def __init__(self,Data,x,y):

        #grab the parameters
        self.Verbose        = False
        self.Active         = True
        self.Color          = 'black'
        self.CanvasObject   = False
        
        #set the position of the polygone
        self.x = x
        self.y = y
        self.Type = 'Surface'
        
        #run formating immediately
        self.PrepareData(Data)
    
    def PrepareData(self,Data):

        '''
        ######################################################
        Prepares the Data
        ######################################################
        '''
        
        #initialise the coordinate var
        self.Coordinates = []
        
        if Data == None:
        
            Active = False
        
        else:
            
            #run the formatting loop
            for i in range(0, len(Data)):

                self.Coordinates.append((Data[i][0],Data[i][1]))


            #log
            if self.Verbose:

                print 'The formated coordinates look like this:'
                print self.Coordinates


    def Check(self,xi,xf,yi,yf):

        '''
        ######################################################
        check if the point is withing the limits
        ######################################################
        '''
        Include = False
    
    
        if self.Active:
    
            if xi < self.x and xf >= self.x  and yi < self.y and yf >= self.y:

                Include = True
        
        
        return Include
        
    def DrawPyG(self, Target, Parameters):
        '''
        ######################################################
        PIL imaging technique
        ######################################################
        '''
        if self.Active and len(self.Coordinates)>0:
            
            #make the plot list
            DrawList = [None]*len(self.Coordinates)
            
            for j in range(len(self.Coordinates)):
            
                DrawList[j] = ((self.Coordinates[j][0]-Parameters[0][0])*Parameters[4],
                               (self.Coordinates[j][1]-Parameters[0][1])*Parameters[5])
            
           
            if self.Verbose:
                print 'Trying to draw:\n',DrawList
                print Parameters
            
            self.AntiAlliasPolygone(Target, Parameters, DrawList)
            
            
#            try:
#                pyg.draw.polygon(Target,
#                                 self.Color,
#                                 DrawList)
#                            
#            except:
#                pass

            #set the state
            self.CanvasObject   = False


    def AntiAlliasPolygone(self, Target, Parameters, DrawList):
        '''
        ######################################################
        This converts the default method into a anti aliassed
        one. This particular case is for lines. Note that
        this allows the contour lines to be rather slooth
        ######################################################
        '''
        
    
        #draw
        pygame.gfxdraw.aapolygon(Target, DrawList, self.Color)
        pygame.gfxdraw.filled_polygon(Target, DrawList, self.Color)
    
    def DrawPIL(self, Target, Parameters):
        '''
        ######################################################
        PIL imaging technique
        ######################################################
        '''
        
        if self.Active and len(self.Coordinates)>0:
        
            #make the plot list
            DrawList = [(((self.Coordinates[j][0]-Parameters[0][0])*Parameters[1][0]
                          +Parameters[2][0]+Parameters[3][0])*Parameters[4]*Parameters[6],
                         (-(self.Coordinates[j][1]-Parameters[0][1])*Parameters[1][1]
                          +1-Parameters[2][1]-Parameters[3][1])*Parameters[5]*Parameters[6])
                        for j in range(0,len(self.Coordinates))]
            
                    
            #draw the objectmatplotlib.colors.rgb2hex(self.color[i])
            if self.Verbose:
                print 'Trying to draw:\n',DrawList
            try:
                Target.polygon(DrawList,
                               fill    =   self.Color)
            except:
                print DrawList
            #set the state
            self.CanvasObject   = False

    def DrawCanvas(self, Target, Parameters):
        
        '''
        ######################################################
        This is he classical imaging technique
        ######################################################
        '''
        self.Identifier = []
        
        if self.Active and len(self.Coordinates)>0:
        
            #make the plot list
            DrawList = [(((self.Coordinates[j][0]-Parameters[0][0])*Parameters[1][0]
                          +Parameters[2][0]+Parameters[3][0])*Parameters[4],
                         (-(self.Coordinates[j][1]-Parameters[0][1])*Parameters[1][1]
                          +1-Parameters[2][1]-Parameters[3][1])*Parameters[5])
                        for j in range(0,len(self.Coordinates))]

            #draw the object
            self.Identifier = Target.create_polygon(DrawList,
                                                    fill     =   "#{0:02x}{1:02x}{2:02x}".format(max(0, min(self.Color[0], 255)),
                                                                                                max(0, min(self.Color[1], 255)),
                                                                                                max(0, min(self.Color[2], 255))),
                                                    tag = 'Top')

            #set the state
            self.CanvasObject   = True
        
        return self.Identifier

class MeshClass:
    
    '''
    ######################################################
    These will be the polygones which only call a draw
    method inside
    ######################################################
    '''
    
    def __init__(self,Data,x,y):

        #grab the parameters
        self.Verbose        = False
        self.Active         = True
        self.Color          = 'black'
        self.CanvasObject   = False
        
        #set the position of the polygone
        self.x = x
        self.y = y
        self.Thickness = 1
        self.Type = 'Mesh'
        
        #run formating immediately
        self.PrepareData(Data)
    
    def PrepareData(self,Data):

        '''
        ######################################################
        Prepares the Data
        ######################################################
        '''
        
        #initialise the coordinate var
        self.Coordinates = []
        
        if Data == None:
        
            Active = False
        
        else:
            
            #run the formatting loop
            for i in range(0, len(Data)):

                self.Coordinates.append((Data[i][0],Data[i][1]))


            #log
            if self.Verbose:

                print 'The formated coordinates look like this:'
                print self.Coordinates


    def Check(self,xi,xf,yi,yf):

        '''
        ######################################################
        check if the point is withing the limits
        ######################################################
        '''
        Include = False
    
    
        if self.Active:
    
            if xi < self.x and xf >= self.x  and yi < self.y and yf >= self.y:

                Include = True
        
        
        return Include
        
    def DrawPyG(self, Target, Parameters):
        '''
        ######################################################
        PyGame imaging echnique. Note that this explicitly 
        calls an antialliassing method that is the line ...
        ######################################################
        '''
        if self.Active and len(self.Coordinates)>0:
            
            #make the plot list
            DrawList = [None]*len(self.Coordinates)
            
            for j in range(len(self.Coordinates)):
            
                DrawList[j] = ((self.Coordinates[j][0]-Parameters[0][0])*Parameters[4],
                               (self.Coordinates[j][1]-Parameters[0][1])*Parameters[5])
            
           
            if self.Verbose:
                
                print 'Trying to draw:\n',DrawList
                print Parameters
            
            
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
        pygame.gfxdraw.aapolygon(Target, (UL, UR, BR, BL), self.Color)
        pygame.gfxdraw.filled_polygon(Target, (UL, UR, BR, BL), self.Color)
        
        #draw the cicrle at first end
        pygame.gfxdraw.aacircle(Target, int(X0[0]), int(X0[1]), int((self.Thickness / 2)),  self.Color)
        pygame.gfxdraw.filled_circle(Target, int(X0[0]), int(X0[1]), int((self.Thickness / 2)),  self.Color)
        
        #draw the circle at the last end
        pygame.gfxdraw.aacircle(Target, int(X1[0]), int(X1[1]), int((self.Thickness / 2)),  self.Color)
        pygame.gfxdraw.filled_circle(Target, int(X1[0]), int(X1[1]), int((self.Thickness / 2)),  self.Color)
    
    
    def DrawPIL(self, Target, Parameters):
        '''
        ######################################################
        PIL imaging technique
        ######################################################
        '''
        
        if self.Active and len(self.Coordinates)>0:
        
            #make the plot list
            DrawList = [(((self.Coordinates[j][0]-Parameters[0][0])*Parameters[1][0]
                          +Parameters[2][0]+Parameters[3][0])*Parameters[4]*Parameters[6],
                         (-(self.Coordinates[j][1]-Parameters[0][1])*Parameters[1][1]
                          +1-Parameters[2][1]-Parameters[3][1])*Parameters[5]*Parameters[6])
                        for j in range(0,len(self.Coordinates))]
            
                    
            #draw the objectmatplotlib.colors.rgb2hex(self.color[i])
            if self.Verbose:
                print 'Trying to draw:\n',DrawList
            try:
                Target.line(DrawList,
                            fill    =   self.Color)
            except:
                print DrawList
            
            #set the state
            self.CanvasObject   = False

    def DrawCanvas(self, Target, Parameters):
        
        '''
        ######################################################
        This is he classical imaging technique
        ######################################################
        '''
        self.Identifier = []
        
        if self.Active and len(self.Coordinates)>0:
        
            #make the plot list
            DrawList = [(((self.Coordinates[j][0]-Parameters[0][0])*Parameters[1][0]
                          +Parameters[2][0]+Parameters[3][0])*Parameters[4],
                         (-(self.Coordinates[j][1]-Parameters[0][1])*Parameters[1][1]
                          +1-Parameters[2][1]-Parameters[3][1])*Parameters[5])
                        for j in range(0,len(self.Coordinates))]

            #draw the object
            self.Identifier = Target.create_line(DrawList,
                                                    fill     =   "#{0:02x}{1:02x}{2:02x}".format(max(0, min(self.Color[0], 255)),
                                                                                                max(0, min(self.Color[1], 255)),
                                                                                                max(0, min(self.Color[2], 255))),
                                                    tag = 'Top')

            #set the state
            self.CanvasObject   = True
        
        return self.Identifier

class ContourScannerClass:

    '''
    ######################################################
    This little guy will scann the array multiple times
    and see if he missed spots
    ######################################################
    '''
            
    def __init__(self,ContourClass):

        #intialise the variables
        self.ContourClass = ContourClass
        self.Verbose      = False #main part
        self.Verbose_2    = False #Scan part
        self.Verbose_3    = False #calculation part
        self.Type         = self.ContourClass.Type
        self.Processors   = self.ContourClass.Processors

    def Scan(self,State):
        
        '''
        ######################################################
        Scan and look at the result
        ######################################################
        '''
        
        
        #initialise polygones
        Surfaces = [[] for j in range(len(self.ContourClass.Range))]
        Meshes   = [[] for j in range(len(self.ContourClass.MeshRange))]
        
        #################################
        #We have a surface contour plot
        if self.Type == 'Surface':
            
            #initialise the variables
            self.SurfaceMatrix = [[None for i in range(len(self.ContourClass.Range)) ] for j in range((len(self.ContourClass.X)-1)*(len(self.ContourClass.X[0])-1))]
            
            #write time doyn
            start = time.time()

            #run as Surface
            self.RunInI('Surface')
        
            #print the time out
            end = time.time()
            print 'Surface calculation time: ', end-start
            
            #write time doyn
            start = time.time()
            
            for k in range(len(self.SurfaceMatrix)):
                
                for i in range(len(self.ContourClass.Range)):
                    
                    if not self.SurfaceMatrix[k][i] == None:
                    
                        #do we have a surface type of element
                        Surfaces[i].append(PolygoneClass(self.SurfaceMatrix[k][i][0],
                                                         self.SurfaceMatrix[k][i][1],
                                                         self.SurfaceMatrix[k][i][2]))
    
    
            #print the time out
            end = time.time()
            print 'Surface processing time: ', end-start
    
        #################################
        #We have a mesh contour plot
        elif self.Type == 'Mesh':
        
            #initialise the variables
            self.MeshMatrix = [[None for i in range(len(self.ContourClass.MeshRange)) ] for j in range((len(self.ContourClass.X)-1)*(len(self.ContourClass.X[0])-1))]
            
            #write time doyn
            start = time.time()

            #run as Surface
            self.RunInI('Mesh')
        
            #print the time out
            end = time.time()
            print 'Mesh calculation time: ', end-start
            
            #write time doyn
            start = time.time()
            
            for k in range(len(self.MeshMatrix)):
                
                for i in range(len(self.ContourClass.MeshRange)):
                    
                    if not self.MeshMatrix[k][i] == None:
                    
                        #do we have a mesh grid type of element
                        Meshes[i].append(MeshClass(self.MeshMatrix[k][i][0],
                                                   self.MeshMatrix[k][i][1],
                                                   self.MeshMatrix[k][i][2]))
        
            #print the time out
            end = time.time()
            print 'Surface processing time: ', end-start
                                                          
        #################################
        #We have a mesh and a surface contour plot
        elif self.Type == 'Double':
            
            #initialise the variables
            self.SurfaceMatrix = [[None for i in range(len(self.ContourClass.Range)) ] for j in range((len(self.ContourClass.X)-1)*(len(self.ContourClass.X[0])-1))]
            
            #write time doyn
            start = time.time()

            #run as Surface
            self.RunInI('Surface')
        
            #print the time out
            end = time.time()
            print 'Surface calculation time: ', end-start
            
            #write time doyn
            start = time.time()
            
            for k in range(len(self.SurfaceMatrix)):
                
                for i in range(len(self.ContourClass.Range)):
                    
                    if not self.SurfaceMatrix[k][i] == None:
                    
                        #do we have a surface type of element
                        Surfaces[i].append(PolygoneClass(self.SurfaceMatrix[k][i][0],
                                                         self.SurfaceMatrix[k][i][1],
                                                         self.SurfaceMatrix[k][i][2]))
        
            #print the time out
            end = time.time()
            print 'Surface processing time: ', end-start
    
            #initialise the variables
            self.MeshMatrix = [[None for i in range(len(self.ContourClass.MeshRange)) ] for j in range((len(self.ContourClass.X)-1)*(len(self.ContourClass.X[0])-1))]
            
            #write time doyn
            start = time.time()

            #run as Surface
            self.RunInI('Mesh')
        
            #print the time out
            end = time.time()
            print 'Mesh calculation time: ', end-start
            
            #write time doyn
            start = time.time()
            
            #put the lines
            for k in range(len(self.MeshMatrix)):
                
                for i in range(len(self.ContourClass.MeshRange)):
                    
                    if not self.MeshMatrix[k][i] == None:
                        
                        #do we have a mesh grid type of element
                        Meshes[i].append(MeshClass(self.MeshMatrix[k][i][0],
                                                   self.MeshMatrix[k][i][1],
                                                   self.MeshMatrix[k][i][2]))

            #print the time out
            end = time.time()
            print 'Mesh processing time: ', end-start
        
        return Surfaces,Meshes
                
    def RunInI(self,Type):
        '''
        ######################################################
        Run over all lines...
        ######################################################
        '''
        
        Data = self.ContourClass
        
        X = numpy.asarray(Data.X).astype(dtype = numpy.float64,order = 'C')
        Y = numpy.asarray(Data.Y).astype(dtype = numpy.float64,order = 'C')
        Z = numpy.asarray(Data.Z).astype(dtype = numpy.float64,order = 'C')
        
        Range = numpy.asarray(Data.Range).astype(dtype = numpy.float64,order = 'C')
        MeshRange = numpy.asarray(Data.MeshRange).astype(dtype = numpy.float64,order = 'C')
        Iterations = len(Data.X[0])
        
        
        
        if self.Processors == 1:
            
            #write time doyn
            start = time.time()
            
            output = []
            
            for i in range(len(self.ContourClass.X)-1):
            
                CCalc.RunInJ(i,Type,X,Y,Z,Range,MeshRange,Iterations,output)
    
            #print the time out
            end = time.time()
            print 'Ran the processes in: ', end-start

        elif self.Processors > 1:
            
            #Set the hwile variable
            Continue = True
            Index = 0
            Manager = multiprocessing.Manager()
            output = Manager.list()
            Pool = []
            
            ###################################
            ###################################
            #create all the runners thatwill be run eventually
            for m in range(0, len(self.ContourClass.X)):
            
                Pool.append(multiprocessing.Process(target = CCalc.RunInJ,
                                                    args = (m,Type,X,Y,Z,Range,MeshRange,Iterations,output)))
        
            ###################################
            ###################################
            #run the loop
            while Continue:

                #set the output method
                OldIndex = Index
                
                #processMatrix
                runners = []
        
                #populate process matrix
                for l in range(0,self.Processors):
        
                    if Index < len(self.ContourClass.X)-1:
            
                        runners.append(Pool[Index])
                    
                        Index += 1
                    
                    else:
                        
                        Continue = False
                        break
            
                #write time doyn
                start = time.time()
                
                #start all the processes
                for p in runners:
                    p.start()
        
                #wait for process to end
                for p in runners:
                    p.join()

                #print the time out
                end = time.time()
                print 'Ran the processes in: ', end-start
                
        ###################################
        ###################################
        #Convert the multiprocessing list
    
        #write time down
        start = time.time()
        
        #slowest part of them all
        Out = [p for p in output ]
        
        #print the time out
        end = time.time()
        print 'Convertion of the shared array took: ', end-start
        
        ###################################
        ###################################
        #Convert the multiprocessing list
        
        #write time down
        start = time.time()
        
        for m in range(0,len(Out)):
            
            #set j
            oo = m*(len(self.ContourClass.X[0])-1)
            
            for j in range(0,len(Out[m])):
                
                if Type == 'Surface':
                    
                    self.SurfaceMatrix[j+oo][:] = Out[m][j][:]
                
                elif Type == 'Mesh':
                    
                    self.MeshMatrix[j+oo][:] = Out[m][j][:]

        #print the time out
        end = time.time()
        print 'Unpacked in: ', end-start


    def RunInJ(self,i,Type,Data,Output = None):
        '''
        ######################################################
        run onver all columns
        ######################################################
        '''
        EndResult = []
        
        if self.Processors < 2 or not Output == None:
        
            for j in range(len(Data.X[0])-1):

                #run it
                Result = StartObjectScan(i,j,Type,Data)
                
                if Output == None:
                
                    #cycle through the result
                    for k in range(len(Result)):
                        
                        if not Result[k] == None:
                            
                            #Handle the polygone components
                            if not len(Result[k]) == 0:
                            
                                if Type == 'Surface':
                                    
                                    self.SurfaceMatrix[k][j+i*(len(Data.X[0])-1)] = Result[k]
                                
                                elif Type == 'Mesh':
                                    
                                    self.MeshMatrix[k][j+i*(len(Data.X[0])-1)] = Result[k]


                else:
            
                    EndResult.append(Result)

            if not Output == None:
                
                Output.put(EndResult)
            
            else:
    
                pass
                    
        elif self.Processors > 100:
            
            #Set the hwile variable
            Continue = True
            Index = 0
            
            #run the loop
            while Continue:
        
                #set the output method
                output = multiprocessing.Manager().Queue()
                OldIndex = Index
                
                #processMatrix
                runners = []
        
                #populate process matrix
                for l in range(0,self.Processors):
        
                    if Index < len(Data.X[0])-1:
            
                        runners.append(multiprocessing.Process(target = self.StartObjectScanMulti,
                                                               args = (i,Index,Type,output)))
                    
                        Index += 1
                    
                    else:
                        
                        Continue = False
                        break
            
                #start all the processes
                for p in runners:
                    p.start()
        
                #wait for process to end
                for p in runners:
                    p.join()

                #grab the outputs
                Out = [output.get() for p in runners]
        
                #finnaly calculate
                for Result in Out:
                    
                    #set j
                    j = OldIndex
                
                    #cycle through the result
                    for k in range(len(Result)):
                        
                        if not Result[k] == None:
                            
                            #Handle the polygone components
                            if not len(Result[k]) == 0:
                                
                                if Type == 'Surface':
                                    
                                    self.SurfaceMatrix[k][j+i*(len(Data.X[0])-1)] = Result[k]
                                
                                elif Type == 'Mesh':
                                    
                                    self.MeshMatrix[k][j+i*(len(Data.X[0])-1)] = Result[k]

                    #move j formward
                    OldIndex += 1

            
    def BackgroundHandler(self):
        '''
        ######################################################
        Once the Object scan has been completed he should
        return an array with elements. These element need
        to be classified as up and down polygones. 
        
        - Up polygones are referenced by main and clearly 
        indicate that the start slope indicapes a container
        it will be treated as colored polygone of the level
        
        - Down polygones are the empty areas and will be drawn
        when the drawer comes back down
        ######################################################
        '''
        
        #initialise
        Path = []
        
        Path.append(self.SinglePointCalc(Points,Value,0,0))
        Path.append(self.SinglePointCalc(Points,Value,0,len(self.ValOverBoolean[0])-1))
        Path.append(self.SinglePointCalc(Points,Value,len(self.ValOverBoolean)-1,len(self.ValOverBoolean[0])-1))
        Path.append(self.SinglePointCalc(Points,Value,len(self.ValOverBoolean)-1,0))
        
        self.SurfaceMatrix.append(Path)



    def SinglePointCalc(self,Points, Value, i):
    
        '''
        ######################################################
        Create and calculate Up polygones and return them
        ######################################################
        '''

        return [Points[i][0],
                Points[i][1]]
            
    def TwoPointCalc(self, Points, Value, i,j):
    
        '''
        ######################################################
        Create and calculate Up polygones and return them
        ######################################################
        '''
        return [Points[i][0]+((Points[j][0]-Points[i][0]))
                *(Value - Points[i][2])/(Points[j][2] - Points[i][2]),
                
                Points[i][1]+((Points[j][1]-Points[i][1]))
                *(Value - Points[i][2])/(Points[j][2] - Points[i][2])]
    
    
    def StartObjectScanMulti(self,i, j,Type,Data,output):

        '''
        ######################################################
        We changed the mode. It is now much more direct by
        drawing tons of polygones. This avoinds so many pro-
        blems
        
        We have now X and check only three o
        
        
            X --- o
            I \   I
            I   \ I
            o --- o
        ######################################################
        '''
        
        #initialise the 4 points
        Points  = [None]*4
        
        Points[0] =  [float(Data.X[i][j]),
                           float(Data.Y[i][j]),
                           float(Data.Z[i][j])]
                      
        Points[1] =  [float(Data.X[i+1][j]),
                           float(Data.Y[i+1][j]),
                           float(Data.Z[i+1][j])]
                      
        Points[2] =  [float(Data.X[i+1][j+1]),
                           float(Data.Y[i+1][j+1]),
                           float(Data.Z[i+1][j+1])]
                      
        Points[3] =  [float(Data.X[i][j+1]),
                           float(Data.Y[i][j+1]),
                           float(Data.Z[i][j+1])]
        
        
        #get the boundaries
        Min = numpy.min([Points[0][2],Points[1][2],Points[2][2],Points[3][2]])
        Max = numpy.max([Points[0][2],Points[1][2],Points[2][2],Points[3][2]])
        
        if Type == 'Surface':
        
            #initialise Output
            Output = [None]*len(Data.Range)
            
            for l in range(len(Data.Range)):
            
                #set the value
                Value = Data.Range[l]
                
                if Value >= Min and Value <= Max:
                
                    #set them locall
                    Pointer = [None]*4
                    
                    Pointer[0] = A = self.OverVal(Points,Value,0)
                    Pointer[1] = B = self.OverVal(Points,Value,1)
                    Pointer[2] = C = self.OverVal(Points,Value,2)
                    Pointer[3] = D = self.OverVal(Points,Value,3)
                    
                    #how many
                    Sum_1 = 0
                    Sum_2 = 0
                    
                    for k in range(0,4):
                    
                        if Pointer[k]:
                    
                            Sum_1 += 1
                
                            Sum_2 += 10**k
            
                    if Sum_1 == 0:
                        
                        if Output[l-1] == None:
                            
                            Output[l-1] = [self.Case_4(Points,Value), Points[0][0], Points[0][1]]
                        
                        break
                            
                    elif Sum_1 == 4 and l == len(self.ContourClass.Range)-1:
                        
                        Output[l] = [self.Case_4(Points,Value), Points[0][0], Points[0][1]]
                    
                    elif Sum_1 == 1:
                    
                        if Sum_2 == 1:
                            
                            Output[l] = [self.Case_1_a(Points,Value), Points[0][0], Points[0][1]]
                            
                        elif Sum_2 == 10:
                            
                            Output[l] = [self.Case_1_b(Points,Value), Points[0][0], Points[0][1]]
                        
                        elif Sum_2 == 100:
                            
                            Output[l] = [self.Case_1_c(Points,Value), Points[0][0], Points[0][1]]
                        
                        elif Sum_2 == 1000:
                            
                            Output[l] = [self.Case_1_d(Points,Value), Points[0][0], Points[0][1]]
                
                    elif Sum_1 == 2:
                    
                        if Sum_2 == 11:
                            
                            Output[l] = [self.Case_2_a(Points,Value), Points[0][0], Points[0][1]]
                            
                        elif Sum_2 == 110:
                            
                            Output[l] = [self.Case_2_b(Points,Value), Points[0][0], Points[0][1]]
                        
                        elif Sum_2 == 1100:
                            
                            Output[l] = [self.Case_2_c(Points,Value), Points[0][0], Points[0][1]]
                        
                        elif Sum_2 == 1001:
                            
                            Output[l] = [self.Case_2_d(Points,Value), Points[0][0], Points[0][1]]

                        elif Sum_2 == 101:
                            
                            Output[l] = [self.Case_2_e(Points,Value), Points[0][0], Points[0][1]]
                                
                        elif Sum_2 == 1010:
                            
                            Output[l] = [self.Case_2_f(Points,Value), Points[0][0], Points[0][1]]
                                
                    elif Sum_1 == 3:
                    
                        if Sum_2 == 1011:
                            
                            Output[l] = [self.Case_3_a(Points,Value), Points[0][0], Points[0][1]]
                            
                        elif Sum_2 == 111:
                            
                            Output[l] = [self.Case_3_b(Points,Value), Points[0][0], Points[0][1]]
                        
                        elif Sum_2 == 1110:
                            
                            Output[l] = [self.Case_3_c(Points,Value), Points[0][0], Points[0][1]]
                        
                        elif Sum_2 == 1101:
                            
                            Output[l] = [self.Case_3_d(Points,Value), Points[0][0], Points[0][1]]
                
                    if not Output[l] == None and Output[l-1] == None  and l > 0:
                        
                        Output[l-1] = [self.Case_4(Points,Value), Points[0][0], Points[0][1]]
            
        elif Type == 'Mesh':
        
            #initialise Output
            Output = [None]*len(Data.MeshRange)
            
            for l in range(len(Data.MeshRange)):
            
                #set the value
                Value = Data.MeshRange[l]
                
                if Value >= Min and Value <= Max:
                
                    #set them locall
                    Pointer = [None]*4
                    
                    Pointer[0] = A = self.OverVal(0)
                    Pointer[1] = B = self.OverVal(1)
                    Pointer[2] = C = self.OverVal(2)
                    Pointer[3] = D = self.OverVal(3)
                    
                    #how many
                    Sum_1 = 0
                    Sum_2 = 0
                    
                    for k in range(0,4):
                    
                        if Pointer[k]:
                    
                            Sum_1 += 1
                
                            Sum_2 += 10**k
                
                    if Sum_1 == 0:
                        
                        if Output[l-1] == None:
                            
                            Output[l-1] = [self.Case_4_Line(Points,Value), Points[0][0], Points[0][1]]
                        
                        break
                            
                    elif Sum_1 == 4 and l == len(self.ContourClass.Range)-1:
                        
                        Output[l] = [self.Case_4_Line(Points,Value), Points[0][0], Points[0][1]]
                    
                    elif Sum_1 == 1:
                    
                    
                        if Sum_2 == 1:
                            
                            Output[l] = [self.Case_1_a_Line(Points,Value), Points[0][0], Points[0][1]]
                            
                        elif Sum_2 == 10:
                            
                            Output[l] = [self.Case_1_b_Line(Points,Value), Points[0][0], Points[0][1]]
                        
                        elif Sum_2 == 100:
                            
                            Output[l] = [self.Case_1_c_Line(Points,Value), Points[0][0], Points[0][1]]
                        
                        elif Sum_2 == 1000:
                            
                            Output[l] = [self.Case_1_d_Line(Points,Value), Points[0][0], Points[0][1]]
                    elif Sum_1 == 2:
                    
                        if Sum_2 == 11:
                            
                            Output[l] = [self.Case_2_a_Line(Points,Value), Points[0][0], Points[0][1]]
                            
                        elif Sum_2 == 110:
                            
                            Output[l] = [self.Case_2_b_Line(Points,Value), Points[0][0], Points[0][1]]
                        
                        elif Sum_2 == 1100:
                            
                            Output[l] = [self.Case_2_c_Line(Points,Value), Points[0][0], Points[0][1]]
                        
                        elif Sum_2 == 1001:
                            
                            Output[l] = [self.Case_2_d_Line(Points,Value), Points[0][0], Points[0][1]]

                        elif Sum_2 == 101:
                            
                            Output[l] = [self.Case_2_e_Line(Points,Value), Points[0][0], Points[0][1]]
                    
                        elif Sum_2 == 1010:
                
                            Output[l] = [self.Case_2_f_Line(Points,Value), Points[0][0], Points[0][1]]
                
                    elif Sum_1 == 3:
                    
                        if Sum_2 == 1011:
                            
                            Output[l] = [self.Case_3_a_Line(Points,Value), Points[0][0], Points[0][1]]
                            
                        elif Sum_2 == 111:
                            
                            Output[l] = [self.Case_3_b_Line(Points,Value), Points[0][0], Points[0][1]]
                        
                        elif Sum_2 == 1110:
                            
                            Output[l] = [self.Case_3_c_Line(Points,Value), Points[0][0], Points[0][1]]
                        
                        elif Sum_2 == 1101:
                            
                            Output[l] = [self.Case_3_d_Line(Points,Value), Points[0][0], Points[0][1]]
                
                    if not Output[l] == None and Output[l-1] == None  and l > 0:
                        
                        Output[l-1] = [self.Case_4_Line(Points,Value), Points[0][0], Points[0][1]]

        output.put(Output)


    def StartObjectScan(self, i, j,Type, Data):

        '''
        ######################################################
        We changed the mode. It is now much more direct by
        drawing tons of polygones. This avoinds so many pro-
        blems
        
        We have now X and check only three o
        
        
            X --- o
            I \   I
            I   \ I
            o --- o
        ######################################################
        '''
        #initialise the 4 points
        Points  = [None]*4
        
        Points[0] =  [float(Data.X[i][j]),
                      float(Data.Y[i][j]),
                      float(Data.Z[i][j])]
                      
        Points[1] =  [float(Data.X[i+1][j]),
                      float(Data.Y[i+1][j]),
                      float(Data.Z[i+1][j])]
                      
        Points[2] =  [float(Data.X[i+1][j+1]),
                      float(Data.Y[i+1][j+1]),
                      float(Data.Z[i+1][j+1])]
                      
        Points[3] =  [float(Data.X[i][j+1]),
                      float(Data.Y[i][j+1]),
                      float(Data.Z[i][j+1])]
        
        
        #get the boundaries
        Min = numpy.min([Points[0][2],Points[1][2],Points[2][2],Points[3][2]])
        Max = numpy.max([Points[0][2],Points[1][2],Points[2][2],Points[3][2]])
        
        if Type == 'Surface':
        
            #initialise Output
            Output = [None]*len(Data.Range)
            
            for l in range(len(Data.Range)):
            
                #set the value
                Value = Data.Range[l]
                
                #if Value >= Min and Value <= Max:
                
                #set them locall
                Pointer = [None]*4
                
                Pointer[0] = A = self.OverVal(Points,Value,0)
                Pointer[1] = B = self.OverVal(Points,Value,1)
                Pointer[2] = C = self.OverVal(Points,Value,2)
                Pointer[3] = D = self.OverVal(Points,Value,3)
                
                #how many
                Sum_1 = 0
                Sum_2 = 0
                
                for k in range(0,4):
                
                    if Pointer[k]:
                
                        Sum_1 += 1
            
                        Sum_2 += 10**k
        
                if Sum_1 == 0:
                    
                    if Output[l-1] == None:
                        
                        Output[l-1] = [self.Case_4(Points,Value), Points[0][0], Points[0][1]]
                    
                    break
                        
                elif Sum_1 == 4 and l == len(self.ContourClass.Range)-1:
                    
                    Output[l] = [self.Case_4(Points,Value), Points[0][0], Points[0][1]]
                
                elif Sum_1 == 1:
                
                    if Sum_2 == 1:
                        
                        Output[l] = [self.Case_1_a(Points,Value), Points[0][0], Points[0][1]]
                        
                    elif Sum_2 == 10:
                        
                        Output[l] = [self.Case_1_b(Points,Value), Points[0][0], Points[0][1]]
                    
                    elif Sum_2 == 100:
                        
                        Output[l] = [self.Case_1_c(Points,Value), Points[0][0], Points[0][1]]
                    
                    elif Sum_2 == 1000:
                        
                        Output[l] = [self.Case_1_d(Points,Value), Points[0][0], Points[0][1]]
            
                elif Sum_1 == 2:
                
                    if Sum_2 == 11:
                        
                        Output[l] = [self.Case_2_a(Points,Value), Points[0][0], Points[0][1]]
                        
                    elif Sum_2 == 110:
                        
                        Output[l] = [self.Case_2_b(Points,Value), Points[0][0], Points[0][1]]
                    
                    elif Sum_2 == 1100:
                        
                        Output[l] = [self.Case_2_c(Points,Value), Points[0][0], Points[0][1]]
                    
                    elif Sum_2 == 1001:
                        
                        Output[l] = [self.Case_2_d(Points,Value), Points[0][0], Points[0][1]]

                    elif Sum_2 == 101:
                        
                        Output[l] = [self.Case_2_e(Points,Value), Points[0][0], Points[0][1]]
                            
                    elif Sum_2 == 1010:
                        
                        Output[l] = [self.Case_2_f(Points,Value), Points[0][0], Points[0][1]]
                            
                elif Sum_1 == 3:
                
                    if Sum_2 == 1011:
                        
                        Output[l] = [self.Case_3_a(Points,Value), Points[0][0], Points[0][1]]
                        
                    elif Sum_2 == 111:
                        
                        Output[l] = [self.Case_3_b(Points,Value), Points[0][0], Points[0][1]]
                    
                    elif Sum_2 == 1110:
                        
                        Output[l] = [self.Case_3_c(Points,Value), Points[0][0], Points[0][1]]
                    
                    elif Sum_2 == 1101:
                        
                        Output[l] = [self.Case_3_d(Points,Value), Points[0][0], Points[0][1]]
            
                if not Output[l] == None and Output[l-1] == None  and l > 0:
                    
                    Output[l-1] = [self.Case_4(Points,Value), Points[0][0], Points[0][1]]
        
        elif Type == 'Mesh':
        
            #initialise Output
            Output = [None]*len(Data.MeshRange)
            
            for l in range(len(Data.MeshRange)):
            
                #set the value
                Value = Data.MeshRange[l]
                
                #if Value >= Min and Value <= Max:
                
                #set them locall
                Pointer = [None]*4
                
                Pointer[0] = A = self.OverVal(0)
                Pointer[1] = B = self.OverVal(1)
                Pointer[2] = C = self.OverVal(2)
                Pointer[3] = D = self.OverVal(3)
                
                #how many
                Sum_1 = 0
                Sum_2 = 0
                
                for k in range(0,4):
                
                    if Pointer[k]:
                
                        Sum_1 += 1
            
                        Sum_2 += 10**k
            
                if Sum_1 == 0:
                    
                    if Output[l-1] == None:
                        
                        Output[l-1] = [self.Case_4_Line(Points,Value), Points[0][0], Points[0][1]]
                    
                    break
                        
                elif Sum_1 == 4 and l == len(self.ContourClass.Range)-1:
                    
                    Output[l] = [self.Case_4_Line(Points,Value), Points[0][0], Points[0][1]]
                
                elif Sum_1 == 1:
                
                
                    if Sum_2 == 1:
                        
                        Output[l] = [self.Case_1_a_Line(Points,Value), Points[0][0], Points[0][1]]
                        
                    elif Sum_2 == 10:
                        
                        Output[l] = [self.Case_1_b_Line(Points,Value), Points[0][0], Points[0][1]]
                    
                    elif Sum_2 == 100:
                        
                        Output[l] = [self.Case_1_c_Line(Points,Value), Points[0][0], Points[0][1]]
                    
                    elif Sum_2 == 1000:
                        
                        Output[l] = [self.Case_1_d_Line(Points,Value), Points[0][0], Points[0][1]]
                elif Sum_1 == 2:
                
                    if Sum_2 == 11:
                        
                        Output[l] = [self.Case_2_a_Line(Points,Value), Points[0][0], Points[0][1]]
                        
                    elif Sum_2 == 110:
                        
                        Output[l] = [self.Case_2_b_Line(Points,Value), Points[0][0], Points[0][1]]
                    
                    elif Sum_2 == 1100:
                        
                        Output[l] = [self.Case_2_c_Line(Points,Value), Points[0][0], Points[0][1]]
                    
                    elif Sum_2 == 1001:
                        
                        Output[l] = [self.Case_2_d_Line(Points,Value), Points[0][0], Points[0][1]]

                    elif Sum_2 == 101:
                        
                        Output[l] = [self.Case_2_e_Line(Points,Value), Points[0][0], Points[0][1]]
                
                    elif Sum_2 == 1010:
            
                        Output[l] = [self.Case_2_f_Line(Points,Value), Points[0][0], Points[0][1]]
            
                elif Sum_1 == 3:
                
                    if Sum_2 == 1011:
                        
                        Output[l] = [self.Case_3_a_Line(Points,Value), Points[0][0], Points[0][1]]
                        
                    elif Sum_2 == 111:
                        
                        Output[l] = [self.Case_3_b_Line(Points,Value), Points[0][0], Points[0][1]]
                    
                    elif Sum_2 == 1110:
                        
                        Output[l] = [self.Case_3_c_Line(Points,Value), Points[0][0], Points[0][1]]
                    
                    elif Sum_2 == 1101:
                        
                        Output[l] = [self.Case_3_d_Line(Points,Value), Points[0][0], Points[0][1]]
            
                if not Output[l] == None and Output[l-1] == None  and l > 0:
                    
                    Output[l-1] = [self.Case_4_Line(Points,Value), Points[0][0], Points[0][1]]
                        
        return Output

    def OverVal(self,Points,Value,val):
        '''
        ######################################################
        return true or false
        ######################################################
        '''
    
        if Value >= Points[val][2]:
    
            return False

        else:
    
            return True
    
    def Case_0(self,Points,Value):

        '''
        ######################################################
        We changed the mode. It is now much more direct by
        drawing tons of polygones. This avoinds so many pro-
        blems
        
        We have now X and check only three o
        
        
            o --- o
            I \   I
            I   \ I
            o --- o
        ######################################################
        '''
    
        #return
        return None

    def Case_1_a(self,Points,Value):

        '''
        ######################################################
        We changed the mode. It is now much more direct by
        drawing tons of polygones. This avoinds so many pro-
        blems
        
        We have now X and check only three o
        
        
            1 --- o
            I \   I
            I   \ I
            o --- o
        ######################################################
        '''

        return [self.SinglePointCalc(Points,Value,0),
                self.TwoPointCalc(Points,Value,0,1),
                self.TwoPointCalc(Points,Value,0,3)]

    def Case_1_b(self,Points,Value):

        '''
        ######################################################
        We changed the mode. It is now much more direct by
        drawing tons of polygones. This avoinds so many pro-
        blems
        
        We have now X and check only three o
        
        
            o --- 1
            I \   I
            I   \ I
            o --- o
        ######################################################
        '''

        return [self.SinglePointCalc(Points,Value,1),
                self.TwoPointCalc(Points,Value,1,2),
                self.TwoPointCalc(Points,Value,1,0)]


    def Case_1_c(self,Points,Value):

        '''
        ######################################################
        We changed the mode. It is now much more direct by
        drawing tons of polygones. This avoinds so many pro-
        blems
        
        We have now X and check only three o
        
        
            o --- o
            I \   I
            I   \ I
            o --- 1
        ######################################################
        '''

        return [self.SinglePointCalc(Points,Value,2),
                self.TwoPointCalc(Points,Value,2,3),
                self.TwoPointCalc(Points,Value,2,1)]


    def Case_1_d(self,Points,Value):

        '''
        ######################################################
        We changed the mode. It is now much more direct by
        drawing tons of polygones. This avoinds so many pro-
        blems
        
        We have now X and check only three o
        
        
            o --- o
            I \   I
            I   \ I
            1 --- o
        ######################################################
        '''

        return [self.SinglePointCalc(Points,Value,3),
                self.TwoPointCalc(Points,Value,3,0),
                self.TwoPointCalc(Points,Value,3,2)]


    def Case_2_a(self,Points,Value):

        '''
        ######################################################
        We changed the mode. It is now much more direct by
        drawing tons of polygones. This avoinds so many pro-
        blems
        
        We have now X and check only three o
        
        
            1 --- 1
            I \   I
            I   \ I
            o --- o
        ######################################################
        '''

        return [self.SinglePointCalc(Points,Value,0),
                self.SinglePointCalc(Points,Value,1),
                self.TwoPointCalc(Points,Value,1,2),
                self.TwoPointCalc(Points,Value,0,3)]


    def Case_2_b(self,Points,Value):

        '''
        ######################################################
        We changed the mode. It is now much more direct by
        drawing tons of polygones. This avoinds so many pro-
        blems
        
        We have now X and check only three o
        
        
            o --- 1
            I \   I
            I   \ I
            o --- 1
        ######################################################
        '''

        return [self.SinglePointCalc(Points,Value,1),
                self.SinglePointCalc(Points,Value,2),
                self.TwoPointCalc(Points,Value,2,3),
                self.TwoPointCalc(Points,Value,1,0)]

    def Case_2_c(self,Points,Value):

        '''
        ######################################################
        We changed the mode. It is now much more direct by
        drawing tons of polygones. This avoinds so many pro-
        blems
        
        We have now X and check only three o
        
        
            o --- 0
            I \   I
            I   \ I
            1 --- 1
        ######################################################
        '''
        
        return [self.SinglePointCalc(Points,Value,2),
                self.SinglePointCalc(Points,Value,3),
                self.TwoPointCalc(Points,Value,3,0),
                self.TwoPointCalc(Points,Value,2,1)]

    def Case_2_d(self,Points,Value):

        '''
        ######################################################
        We changed the mode. It is now much more direct by
        drawing tons of polygones. This avoinds so many pro-
        blems
        
        We have now X and check only three o
        
        
            1 --- o
            I \   I
            I   \ I
            1 --- o
        ######################################################
        '''
        
        #return
        return [self.SinglePointCalc(Points,Value,3),
                self.SinglePointCalc(Points,Value,0),
                self.TwoPointCalc(Points,Value,0,1),
                self.TwoPointCalc(Points,Value,3,2)]


    def Case_2_e(self,Points,Value):

        '''
        ######################################################
        We changed the mode. It is now much more direct by
        drawing tons of polygones. This avoinds so many pro-
        blems
        
        We have now X and check only three o
        
        
            1 --- o
            I \   I
            I   \ I
            o --- 1
        ######################################################
        '''

        #return
        return [self.SinglePointCalc(Points,Value,0),
                self.TwoPointCalc(Points,Value,0,1),
                self.TwoPointCalc(Points,Value,2,1),
                self.SinglePointCalc(Points,Value,2),
                self.TwoPointCalc(Points,Value,2,3),
                self.TwoPointCalc(Points,Value,0,3)]


    def Case_2_f(self,Points,Value):

        '''
        ######################################################
        We changed the mode. It is now much more direct by
        drawing tons of polygones. This avoinds so many pro-
        blems
        
        We have now X and check only three o
        
        
            o --- 1
            I \   I
            I   \ I
            1 --- o
        ######################################################
        '''

        return [self.SinglePointCalc(Points,Value,1),
                self.TwoPointCalc(Points,Value,1,2),
                self.TwoPointCalc(Points,Value,3,2),
                self.SinglePointCalc(Points,Value,3),
                self.TwoPointCalc(Points,Value,3,0),
                self.TwoPointCalc(Points,Value,1,0)]


    def Case_3_a(self,Points,Value):

        '''
        ######################################################
        We changed the mode. It is now much more direct by
        drawing tons of polygones. This avoinds so many pro-
        blems
        
        We have now X and check only three o
        
        
            1 --- 1
            I \   I
            I   \ I
            1 --- o
        ######################################################
        '''

        return [self.SinglePointCalc(Points,Value,0),
                self.SinglePointCalc(Points,Value,1),
                self.TwoPointCalc(Points,Value,1,2),
                self.TwoPointCalc(Points,Value,3,2),
                self.SinglePointCalc(Points,Value,3)]


    def Case_3_b(self,Points,Value):

        '''
        ######################################################
        We changed the mode. It is now much more direct by
        drawing tons of polygones. This avoinds so many pro-
        blems
        
        We have now X and check only three o
        
        
            1 --- 1
            I \   I
            I   \ I
            o --- 1
        ######################################################
        '''

        return [self.SinglePointCalc(Points,Value,1),
                self.SinglePointCalc(Points,Value,2),
                self.TwoPointCalc(Points,Value,2,3),
                self.TwoPointCalc(Points,Value,0,3),
                self.SinglePointCalc(Points,Value,0)]


    def Case_3_c(self,Points,Value):

        '''
        ######################################################
        We changed the mode. It is now much more direct by
        drawing tons of polygones. This avoinds so many pro-
        blems
        
        We have now X and check only three o
        
        
            o --- 1
            I \   I
            I   \ I
            1 --- 1
        ######################################################
        '''
        
        return [self.SinglePointCalc(Points,Value,2),
                self.SinglePointCalc(Points,Value,3),
                self.TwoPointCalc(Points,Value,3,0),
                self.TwoPointCalc(Points,Value,1,0),
                self.SinglePointCalc(Points,Value,1)]


    def Case_3_d(self,Points,Value):

        '''
        ######################################################
        We changed the mode. It is now much more direct by
        drawing tons of polygones. This avoinds so many pro-
        blems
        
        We have now X and check only three o
        
        
            1 --- o
            I \   I
            I   \ I
            1 --- 1
        ######################################################
        '''

        return [self.SinglePointCalc(Points,Value,3),
                self.SinglePointCalc(Points,Value,0),
                self.TwoPointCalc(Points,Value,0,1),
                self.TwoPointCalc(Points,Value,1,2),
                self.SinglePointCalc(Points,Value,2)]
    
    def Case_4(self,Points,Value):

        '''
        ######################################################
        We changed the mode. It is now much more direct by
        drawing tons of polygones. This avoinds so many pro-
        blems
        
        We have now X and check only three o
        
        
            1 --- 1
            I \   I
            I   \ I
            1 --- 1
        ######################################################
        '''
        return [self.SinglePointCalc(Points,Value,0),
                self.SinglePointCalc(Points,Value,1),
                self.SinglePointCalc(Points,Value,2),
                self.SinglePointCalc(Points,Value,3)]

        
    def Case_0_Line(self,Points,Value):

        '''
        ######################################################
        We changed the mode. It is now much more direct by
        drawing tons of polygones. This avoinds so many pro-
        blems
        
        We have now X and check only three o
        
        
            o --- o
            I \   I
            I   \ I
            o --- o
        ######################################################
        '''
    
        #return
        return None

    def Case_1_a_Line(self,Points,Value):

        '''
        ######################################################
        We changed the mode. It is now much more direct by
        drawing tons of polygones. This avoinds so many pro-
        blems
        
        We have now X and check only three o
        
        
            1 --- o
            I \   I
            I   \ I
            o --- o
        ######################################################
        '''

        return [self.TwoPointCalc(Points,Value,0,1),
                self.TwoPointCalc(Points,Value,0,3)]

    def Case_1_b_Line(self,Points,Value):

        '''
        ######################################################
        We changed the mode. It is now much more direct by
        drawing tons of polygones. This avoinds so many pro-
        blems
        
        We have now X and check only three o
        
        
            o --- 1
            I \   I
            I   \ I
            o --- o
        ######################################################
        '''

        return [self.TwoPointCalc(Points,Value,1,2),
                self.TwoPointCalc(Points,Value,1,0)]


    def Case_1_c_Line(self,Points,Value):

        '''
        ######################################################
        We changed the mode. It is now much more direct by
        drawing tons of polygones. This avoinds so many pro-
        blems
        
        We have now X and check only three o
        
        
            o --- o
            I \   I
            I   \ I
            o --- 1
        ######################################################
        '''

        return [self.TwoPointCalc(Points,Value,2,3),
                self.TwoPointCalc(Points,Value,2,1)]


    def Case_1_d_Line(self,Points,Value):

        '''
        ######################################################
        We changed the mode. It is now much more direct by
        drawing tons of polygones. This avoinds so many pro-
        blems
        
        We have now X and check only three o
        
        
            o --- o
            I \   I
            I   \ I
            1 --- o
        ######################################################
        '''

        return [self.TwoPointCalc(Points,Value,3,0),
                self.TwoPointCalc(Points,Value,3,2)]


    def Case_2_a_Line(self,Points,Value):

        '''
        ######################################################
        We changed the mode. It is now much more direct by
        drawing tons of polygones. This avoinds so many pro-
        blems
        
        We have now X and check only three o
        
        
            1 --- 1
            I \   I
            I   \ I
            o --- o
        ######################################################
        '''

        return [self.TwoPointCalc(Points,Value,1,2),
                self.TwoPointCalc(Points,Value,0,3)]


    def Case_2_b_Line(self,Points,Value):

        '''
        ######################################################
        We changed the mode. It is now much more direct by
        drawing tons of polygones. This avoinds so many pro-
        blems
        
        We have now X and check only three o
        
        
            o --- 1
            I \   I
            I   \ I
            o --- 1
        ######################################################
        '''

        return [self.TwoPointCalc(Points,Value,2,3),
                self.TwoPointCalc(Points,Value,1,0)]

    def Case_2_c_Line(self,Points,Value):

        '''
        ######################################################
        We changed the mode. It is now much more direct by
        drawing tons of polygones. This avoinds so many pro-
        blems
        
        We have now X and check only three o
        
        
            o --- 0
            I \   I
            I   \ I
            1 --- 1
        ######################################################
        '''
        
        return [self.TwoPointCalc(Points,Value,3,0),
                self.TwoPointCalc(Points,Value,2,1)]

    def Case_2_d_Line(self,Points,Value):

        '''
        ######################################################
        We changed the mode. It is now much more direct by
        drawing tons of polygones. This avoinds so many pro-
        blems
        
        We have now X and check only three o
        
        
            1 --- o
            I \   I
            I   \ I
            1 --- o
        ######################################################
        '''
        
        #return
        return [self.TwoPointCalc(Points,Value,0,1),
                self.TwoPointCalc(Points,Value,3,2)]


    def Case_2_e_Line(self,Points,Value):

        '''
        ######################################################
        We changed the mode. It is now much more direct by
        drawing tons of polygones. This avoinds so many pro-
        blems
        
        We have now X and check only three o
        
        
            1 --- o
            I \   I
            I   \ I
            o --- 1
        ######################################################
        '''

        #return
        return [self.TwoPointCalc(Points,Value,0,1),
                self.TwoPointCalc(Points,Value,2,1),
                self.TwoPointCalc(Points,Value,2,3),
                self.TwoPointCalc(Points,Value,0,3)]

    def Case_2_f_Line(self,Points,Value):

        '''
        ######################################################
        We changed the mode. It is now much more direct by
        drawing tons of polygones. This avoinds so many pro-
        blems
        
        We have now X and check only three o
        
        
            o --- 1
            I \   I
            I   \ I
            1 --- o
        ######################################################
        '''

        return [self.TwoPointCalc(Points,Value,1,2),
                self.TwoPointCalc(Points,Value,3,2),
                self.TwoPointCalc(Points,Value,3,0),
                self.TwoPointCalc(Points,Value,1,0)]
    
    def Case_3_a_Line(self,Points,Value):

        '''
        ######################################################
        We changed the mode. It is now much more direct by
        drawing tons of polygones. This avoinds so many pro-
        blems
        
        We have now X and check only three o
        
        
            1 --- 1
            I \   I
            I   \ I
            1 --- o
        ######################################################
        '''

        return [self.TwoPointCalc(Points,Value,1,2),
                self.TwoPointCalc(Points,Value,3,2)]


    def Case_3_b_Line(self,Points,Value):

        '''
        ######################################################
        We changed the mode. It is now much more direct by
        drawing tons of polygones. This avoinds so many pro-
        blems
        
        We have now X and check only three o
        
        
            1 --- 1
            I \   I
            I   \ I
            o --- 1
        ######################################################
        '''

        return [self.TwoPointCalc(Points,Value,2,3),
                self.TwoPointCalc(Points,Value,0,3)]


    def Case_3_c_Line(self,Points,Value):

        '''
        ######################################################
        We changed the mode. It is now much more direct by
        drawing tons of polygones. This avoinds so many pro-
        blems
        
        We have now X and check only three o
        
        
            o --- 1
            I \   I
            I   \ I
            1 --- 1
        ######################################################
        '''
        
        return [self.TwoPointCalc(Points,Value,3,0),
                self.TwoPointCalc(Points,Value,1,0)]


    def Case_3_d_Line(self,Points,Value):

        '''
        ######################################################
        We changed the mode. It is now much more direct by
        drawing tons of polygones. This avoinds so many pro-
        blems
        
        We have now X and check only three o
        
        
            1 --- o
            I \   I
            I   \ I
            1 --- 1
        ######################################################
        '''

        return [self.TwoPointCalc(Points,Value,0,1),
                self.TwoPointCalc(Points,Value,1,2)]
    
    def Case_4_Line(self,Points,Value):

        '''
        ######################################################
        We changed the mode. It is now much more direct by
        drawing tons of polygones. This avoinds so many pro-
        blems
        
        We have now X and check only three o
        
        
            1 --- 1
            I \   I
            I   \ I
            1 --- 1
        ######################################################
        '''
        return []

class Drawer:

    def __init__(self,Canvas,Multi = None, Verbose = False,ID = 0):
        
        #circular reference to the container canvas
        self.Canvas = Canvas
        self.Multi = Multi
        
        ##########################################
        #internal element indentifier
        self.identifier             = 0
        self.Rangeidentifier        = 0
        self.LineIndentifier        = 0
        self.Live                   = 0
        self.ID                     = ID
        
        ##########################################
        #Default Zoom identifiers
        self.SmartResize            = False
        self.SmartResizeFactor      = [1.0,0.90]
        
        ##########################################
        #Initialise different elements of the plot
        
        #The axes
        self.Axes       = Axes(self.Canvas)
        
        #Set the mouse
        self.Mouse      = Mouse(self.Canvas)
        
        #Set the keyboard
        self.Keyboard   = Keyboard(self.Canvas,Multi = self.Multi)
        
        #The pointer
        self.Pointer    = Pointer(self.Canvas)
        
        #The zoomer
        self.Zoomer     = Zoomer(self.Canvas)
        
        #the title
        self.Title      = None
        
        ##########################################
        #initialise drawing lists
        self.Plots      = []
        self.Ranges     = []
        self.Lines      = []
        self.Contours   = []
        
        '''
        ######################################################
        #bounding box parameters
        # - Thickness
        # - color
        # - X percentage offset (0 to 1) to out
        # - Y percentage offset (0 to 1) to out
        # - X percentage offset (0 to 1) to in
        # - Y percentage offset (0 to 1) to in
        ######################################################
        '''
    
        self.Verbose = Verbose
    
        '''
        ######################################################
        Zoom boundaries are expressed as a position and ranges
        Note that the ranges can be positive or negative
        as the four corners of the zoom box will be calculated
        
        If any of the four parametes is set to None the 
        default boundaries will be used
        
        Zooming will not influence the padding
        
        - XPos
        - YPos
        - XDelta
        - YDelta
        ######################################################
        '''
    
        self.ZoomBox = [None,None,None,None]
    
    def BindCursor(self):
    
        self.Pointer.BindCursor()
    
    def BindZoomer(self):
    
        self.Zoomer.Listen()
    
    def SetScale(self,wscale,hscale):
        '''
        ######################################################
        This factors a crucial as the permit redraying even
        when the window is not equal to 1 by 1 pixel
        ######################################################
        '''
        
        self.wScaleFactor = wscale
        self.hScaleFactor = hscale
    
    def isZoomX(self):
    
        '''
        ######################################################
        returns true if all zoom parameters are set
        ######################################################
        '''
    
        A = [self.ZoomBox[0],self.ZoomBox[2]]
        
        if A.count(None) >= 1:
            Zoom =  False
        else:
            Zoom =  True

        if Zoom:
            
            #reorder this stuff
            self.ZoomBox[0] = numpy.min(A)
            self.ZoomBox[2] = numpy.max(A)

        return Zoom
            
    def isZoomY(self):
    
        '''
        ######################################################
        returns true if all zoom parameters are set
        ######################################################
        '''
    
        A = [self.ZoomBox[1],self.ZoomBox[3]]
        
        if A.count(None) >= 1:
            Zoom =  False
        else:
            Zoom =  True
        
        if Zoom:
            
            #reorder this stuff
            self.ZoomBox[1] = numpy.min(A)
            self.ZoomBox[3] = numpy.max(A)
        return Zoom
            
    def DrawAll(self):
        
        '''
        ######################################################
        We needed to instaure a drawing method
        ######################################################
        '''
    
        #######################################################
        #draw the plots
        try:
            self.DrawAllPlot()
        except:
            print 'Could not Draw Plots...'
    
        #place the axes
        try:
            self.Axes.DrawAxes()
        except:
            print ' Counld not draw Axes...'
    
        #place the ticks
        try:
            self.Axes.PlaceAllTicks()
        except:
            print 'Could not place Ticks...'
    
        #Place tick labels
        try:
            self.Axes.PlaceAllLabels()
        except:
            print 'Could not place labels...'
    
        #activate the cursor
        try:
            self.BindCursor()
        except:
            print 'Could not bind the Cursor...'
    
        #actiavte the zomer
        try:
            self.BindZoomer()
        except:
            print 'Could not bind the zoomer...'

    def Zoom(self):
    
        '''
        ######################################################
        This will call all necesseray steps to zoom.
        Including destroyign all Ticks and labels
        
        reseting the factor evaluator
        ######################################################
        '''
        
        ###################
        #remove the plots
    
        #remove all Ticks
        self.Axes.RemoveTicks()
    
        #remove all labels
        self.Axes.RemoveLabels()
        
        #remove all labels
        self.Axes.RemoveGrids()
        
        #clear the cursor
        self.Pointer.UnbindCursor()
        self.Pointer.DeleteCursor()
        
        #redraw allplots
        self.RedrawPlots()
        
        #redraw allplots
        self.RedrawRange()
        
        #redraw allplots
        self.RedrawLines()
        
        #redraw allplots
        self.RedrawContours()
        
        ###################
        #draw axes
        self.Axes.DrawAxes()
        
        #redraw plots
        self.DrawAllPlot()
        
        #redraw all labels
        self.Axes.PlaceGrids()
        
        #redraw all Ticks
        self.Axes.PlaceAllTicks()
    
        #redraw all labels
        self.Axes.PlaceAllLabels()
    
        #rebind the cursor
        self.Pointer.BindCursor()
    
    def Zoom_Projection(self):
    
        #redraw allplots
        self.RedrawPlots()
        
        #redraw plots
        self.DrawAllPlot()
    
    def Reset(self):
    
        '''
        ######################################################
        This will call all necesseray steps to zoom.
        Including destroyign all Ticks and labels
        
        reseting the factor evaluator
        ######################################################
        '''
        
        ###################
        #remove the plots
    
        #remove all Ticks
        self.Axes.RemoveTicks()
    
        #remove all labels
        self.Axes.RemoveLabels()
        
        #remove all labels
        self.Axes.RemoveGrids()
        
        #clear the cursor
        self.Pointer.UnbindCursor()
        self.Pointer.DeleteCursor()
        
        #redraw allplots
        self.RedrawPlots()
        
        #redraw allplots
        self.RedrawRange()
        
        #redraw allplots
        self.RedrawLines()
        
        #redraw allplots
        self.RedrawContours()
        
        #redraw allplots
        self.RemoveAllPlots()
        
        #redraw allplots
        self.RemoveAllRanges()
                         
        #redraw allplots
        self.RemoveAllLines()
        
        #redraw allplots
        self.RemoveAllContours()
        
        ###################
        #draw axes
        self.Axes.DrawAxes()
        
        #redraw plots
        self.DrawAllPlot()
        
        #redraw all labels
        self.Axes.PlaceGrids()
        
        #redraw all Ticks
        self.Axes.PlaceAllTicks()
    
        #redraw all labels
        self.Axes.PlaceAllLabels()
    
        #rebind the cursor
        self.Pointer.BindCursor()

    def AddPlot(self,X,Y,
                Thickness = 1,
                color = 'black',
                Active = True,
                Name = '',
                style = ['',0,0]):

        '''
        ######################################################
        #Each plot has the folowing identifiers
        #
        # - X
        # - Y
        # - List of object IDs for segments
        # - Thickness
        # - collor
        # - Active state
        # - Drawn (To knbow if an item has been drawn)
        # - Name Not necessary (can be usefull)
        # - Do we use the scater points
        ######################################################
        '''
        #internal reference identifier
        self.identifier += 1
        
        #Load the parameters into the plot list
        self.Plots.append(PlotClass(X,Y,
                                    Thickness,
                                    color,
                                    Active,
                                    Name,
                                    style,
                                    Indentifier = self.identifier))

        return self.Plots[-1]
 
    def AddProjectionPlot(self,
                          Contour,
                          Thickness = 1,
                          Type = 'x',
                          Color = 'black',
                          Active = True,
                          Name = '',
                          style = ['',0,0]):

        '''
        ######################################################
        #Each plot has the folowing identifiers
        #
        # - X
        # - Y
        # - List of object IDs for segments
        # - Thickness
        # - collor
        # - Active state
        # - Drawn (To knbow if an item has been drawn)
        # - Name Not necessary (can be usefull)
        # - Do we use the scater points
        ######################################################
        '''
        
        #internal reference identifier
        self.identifier += 1
        
        #Load the parameters into the plot list
        self.Plots.append(OneDProjectionClass(Contour,
                                              Thickness,
                                              Color,
                                              Active,
                                              Type,
                                              Name,
                                              style,
                                              Indentifier = self.identifier))
    
        return self.Plots[-1]
    
    
    def AddLine(self,
                Value,
                Type = 'vertical',
                Dash = '',
                Thickness = 1,
                color = 'black',
                Active = True,
                Name = '',
                style = ['',0,0]):

        '''
        ######################################################
        #This will add a line to be drawn
        ######################################################
        '''
        
        #internal reference identifier
        self.identifier += 1
        
        #Load the parameters into the plot list
        self.Lines.append(LineClass(Value,
                                    Type,
                                    Dash,
                                    Thickness,
                                    color,
                                    Active,
                                    Name,
                                    style,
                                    Indentifier = self.identifier))
    
    
        return self.Lines[-1]
    
    def AddContour(self,
                   X,Y,Z,
                 
                   #General variables
                   Type = 'Surface',
                   Range = None,
                   Active = True,
                   Name = '',
                   style = [0,0,0],
                 
                   #Surface variables
                   ColorList = None,
                   Stepping  = 10,
                 
                   #Mesh variables
                   MeshColorList = None,
                   MeshStepping  = 10,
                   MeshThickness = 5):

        '''
        ######################################################
        #This will add a line to be drawn
        ######################################################
        '''
        
        #internal reference identifier
        self.identifier += 1
        
        #Load the parameters into the plot list
        self.Contours.append(ContourClass(X,Y,Z,
                 
                                          #General variables
                                          Type      = Type,
                                          Range     = Range,
                                          Active    = Active,
                                          Name      = Name,
                                          style     = style,
                                          Indentifier = self.identifier ,
                 
                                          #Surface variables
                                          ColorList = ColorList,
                                          Stepping  = Stepping,
                 
                                          #Mesh variables
                                          MeshColorList = MeshColorList,
                                          MeshStepping  = MeshStepping,
                                          MeshThickness = MeshThickness))
    
        return self.Contours[-1]
    
    def AddRange(self,Coordinates):

        '''
        ######################################################
        This allows to set ranges that wil be marked grey 
        to show the user that we don't use a region for
        whatever purpose he desires....
        ######################################################
        '''
        
        #internal reference identifier
        self.identifier += 1
        
        #Load the parameters into the plot list
        self.Ranges.append(RangeClass(Coordinates,self.identifier))
    
        return self.Rangeidentifier
    
    def DelPlot(self,ID):
    
        '''
        ######################################################
        This will proceed to the removal of a plot by the
        given ID.
        ######################################################
        '''

        for i in range(0,len(self.Plots)):
            
            if self.Verbose:
                
                print 'ID is ', ID
                print self.Plots[i][9]
                print 'Current ID is : ',self.Plots[i][9]
        
            if self.Plots[i][9] == ID:
                

                #delete the element
                #self.Canvas.delete(self.Plots[i][2][0])
                
                #remove the entry
                del self.Plots[i]

                return 0
    
    def EvalPlotFactors(self):
    
        '''
        ######################################################
        This function evaluate the bounding parameters
        before the plot is being done. 
        
        This includes bounding parameters as well as the 
        bounding box parameters
        ######################################################
        '''
        
        ######################################################
        #Evaluate boundaries and factors
        
        XMax = []
        XMin = []
        YMax = []
        YMin = []
        
        #did the user already define plots
        if  len(self.Plots) > 0  or len(self.Contours) > 0:
        
            ######################################################
            #cycle through the plot commands and grab extremes
            for i in range(0,len(self.Plots)):
            
                #grab extremes
                XMax.append(numpy.max(self.Plots[i].X))
                XMin.append(numpy.min(self.Plots[i].X))
                YMax.append(numpy.max(self.Plots[i].Y))
                YMin.append(numpy.min(self.Plots[i].Y))
            
            ######################################################
            #Add contour informationsto allow treatment
            for i in range(0,len(self.Contours)):
                
                #grab extremes
                XMax.append(self.Contours[i].XMax)
                XMin.append(self.Contours[i].XMin)
                YMax.append(self.Contours[i].YMax)
                YMin.append(self.Contours[i].YMin)
            
            #for deugging
            if self.Verbose:
                
                print 'This is YMax : ', YMax
                print 'This is YMin : ', YMin
        
        
            ######################################################
            self.BoundingBoxOffset = [None]*4
            self.BoundingBoxFactor = [None]*2
            
            
            ######################################################
            #cycle through the plot commands and grab extremes
            for i in range(0,len(self.Plots)):
            
                #grab extremes
                XMax.append(numpy.max(self.Plots[i].X))
                XMin.append(numpy.min(self.Plots[i].X))
            
            #grab the bounding box left bottom corner
            if self.isZoomX():
            
                #set the limits to the zoom bounding box
                self.BoundingBoxOffset[0] = self.ZoomBox[0]
                self.BoundingBoxOffset[2] = self.ZoomBox[2]
                
                #fetch the paddings from the axes variables
                self.BoundingBoxFactor[0] = ((1.0-self.Axes.PaddingIn[0]-self.Axes.PaddingOut[0]
                                             -self.Axes.PaddingIn[2]-self.Axes.PaddingOut[2])
                                             /(self.BoundingBoxOffset[2]-self.BoundingBoxOffset[0]))
            
            else:
                
                #set the optimal box to grab all informations
                self.BoundingBoxOffset[0] = numpy.min(XMin)
                self.BoundingBoxOffset[2] = numpy.max(XMax)
            
            
                #fetch the paddings from the axes variables
                self.BoundingBoxFactor[0] = ((1.0-self.Axes.PaddingIn[0]-self.Axes.PaddingIn[2]
                                              -self.Axes.PaddingOut[0]-self.Axes.PaddingOut[2])
                                             /(numpy.max(XMax)-numpy.min(XMin)))

            ######################################################
            #cycle through the plot commands and grab extremes
            for i in range(0,len(self.Plots)):
        
                #if self.Plots[i][0]>self.BoundingBoxOffset[0] and self.Plots[i][0]>self.BoundingBoxOffset[0]
                #grab extremes
                YMax.append(numpy.max(self.Plots[i].Y))
                YMin.append(numpy.min(self.Plots[i].Y))
            
            #grab the bounding box left bottom corner
            if self.isZoomY():
            
                #set the limits to the zoom bounding box
                self.BoundingBoxOffset[1] = self.ZoomBox[1]
                self.BoundingBoxOffset[3] = self.ZoomBox[3]
            
                #fetch the paddings from the axes variables
                self.BoundingBoxFactor[1] = ((1.0-self.Axes.PaddingIn[1]-self.Axes.PaddingOut[1]
                                              -self.Axes.PaddingIn[3]-self.Axes.PaddingOut[3])
                                             /(self.BoundingBoxOffset[3]-self.BoundingBoxOffset[1]))
                    
            else:
                
                #set the optimal box to grab all informations
                self.BoundingBoxOffset[1] = numpy.min(YMin)
                self.BoundingBoxOffset[3] = numpy.max(YMax)
                
                #fetch the paddings from the axes variables
                self.BoundingBoxFactor[1] = ((1.0-self.Axes.PaddingIn[1]-self.Axes.PaddingOut[1]
                                              -self.Axes.PaddingIn[3]-self.Axes.PaddingOut[3])
                                             /(numpy.max(YMax)-numpy.min(YMin)))
            
    
            #do some logicql fixing...
            if self.BoundingBoxOffset[2]== self.BoundingBoxOffset[0]:
                    
                self.BoundingBoxOffset[0] -= 1
                self.BoundingBoxOffset[2] += 1
                
            if self.BoundingBoxOffset[3]== self.BoundingBoxOffset[1]:
                
                self.BoundingBoxOffset[1] -= 1
                self.BoundingBoxOffset[3] += 1
        else:
        
            #set the optimal box to grab all informations
            self.BoundingBoxOffset = [0,
                                      0,
                                      1,
                                      1]
            #set dumies
            XMax = [1]
            XMin = [0]
            YMax = [1]
            YMin = [0]
            
            
            #fetch the paddings from the axes variables
            self.BoundingBoxFactor = [(1.0-self.Axes.PaddingIn[0]-self.Axes.PaddingIn[2]
                                        -self.Axes.PaddingOut[0]-self.Axes.PaddingOut[2])
                                      /(numpy.max(XMax)-numpy.min(XMin)),
                                      (1.0-self.Axes.PaddingIn[1]-self.Axes.PaddingOut[1]
                                        -self.Axes.PaddingIn[3]-self.Axes.PaddingOut[3])
                                      /(numpy.max(YMax)-numpy.min(YMin))]
        
        
        
        #for debugging
        if self.Verbose:
            
            print 'This is Offset : ',self.BoundingBoxOffset
            print 'This is Factor : ',self.BoundingBoxFactor

        #if smart is set reevaluate
        if self.SmartResize:

            #for debugging
            if self.Verbose:
            
                print 'Smart automatic resizing was chose'
                print 'The factor it: ',self.SmartResizeFactor
            
                print 'Old BoundingBoxOffset:',self.BoundingBoxOffset
                print 'Old BoundingBoxFactor:',self.BoundingBoxFactor
            
            #change the offset
            self.BoundingBoxOffset = [self.BoundingBoxOffset[0]
                                      -(1-self.SmartResizeFactor[0])
                                      *(self.BoundingBoxOffset[2]-self.BoundingBoxOffset[0])/2,
                                      #->change X0
                                      
                                      self.BoundingBoxOffset[1]
                                      -(1-self.SmartResizeFactor[1])
                                      *(self.BoundingBoxOffset[3]-self.BoundingBoxOffset[1])/2,
                                      #->change Y0
                                      
                                      self.BoundingBoxOffset[2]
                                      +(1-self.SmartResizeFactor[0])
                                      *(self.BoundingBoxOffset[2]-self.BoundingBoxOffset[0])/2,
                                      #->change X1
                                      
                                      self.BoundingBoxOffset[3]
                                      +(1-self.SmartResizeFactor[1])
                                      *(self.BoundingBoxOffset[3]-self.BoundingBoxOffset[1])/2]
                                      #->change Y1
            #change the factor
            self.BoundingBoxFactor = [(1.0-self.Axes.PaddingIn[0]-self.Axes.PaddingIn[2]
                                        -self.Axes.PaddingOut[0]-self.Axes.PaddingOut[2])
                                      /(self.BoundingBoxOffset[2]-self.BoundingBoxOffset[0]),
                                      (1.0-self.Axes.PaddingIn[1]-self.Axes.PaddingOut[1]
                                        -self.Axes.PaddingIn[3]-self.Axes.PaddingOut[3])
                                      /(self.BoundingBoxOffset[3]-self.BoundingBoxOffset[1])]
                
            #for debugging
            if self.Verbose:
            
                print 'New BoundingBoxOffset:',self.BoundingBoxOffset
                print 'New BoundingBoxFactor:',self.BoundingBoxFactor



    def DrawAllPlot(self):
        
        '''
        ########################################################################
        This function solely handles the plots and has no other particularity.
        It cycles though the bounding box and manages the lines with given
        thickess and color. Note that a line has to be loaded tought the 
        addPlot() method first before the drawer can catch it and present it
        ########################################################################
        '''
        ##################
        #rerun the evaluation
        self.EvalPlotFactors()
        
        '''
        ########################################################################
        We have two methods for drawing. They are determined by self.Live = 0
        or 1 or 2. 0 is the default and should use the PIL imaging library.
        Note that using Live = 2 will load the plots as canvas items and
        can decreae the sampling speed. an intermediary will be used to gererate
        a sucessive amount of images when Live = 1 is called. So it will draw
        X amounts of images and then just swap them accordingly...
        ########################################################################
        '''
        SamplingFactor = 2
        
        #try to remove the image if possible
        try:
            self.Canvas.delete(self.MainPlotID)
        except:
            pass
        
        draw = None
        
        #do we need a new image?
        if self.Live == 0:
            
            image   = Image.new("RGBA",
                                (self.wScaleFactor*SamplingFactor,
                                 self.hScaleFactor*SamplingFactor),
                                'white')
                
            draw    = ImageDraw.Draw(image)
        
        elif self.Live == 2:
            
            draw   = pyg.Surface((self.wScaleFactor,
                                self.hScaleFactor))
        
            draw.fill((255,255,255)) # fill background white
        
        
        
        else:
        
            pass
        
        #create the parameter array
        Parameters = [self.BoundingBoxOffset,
                      self.BoundingBoxFactor,
                      self.Axes.PaddingIn,
                      self.Axes.PaddingOut,
                      self.wScaleFactor,
                      self.hScaleFactor,
                      SamplingFactor]
        
        ##########################################################################################
        #Draw the Contour
        for i in range(0,len(self.Contours)):
            
            #Draw the elements in PIL
            if self.Live == 0:
                self.Contours[i].DrawPIL(draw, Parameters, self.ZoomBox[0], self.ZoomBox[2], self.ZoomBox[1], self.ZoomBox[3])
            
            #Draw the elements in PIL
            if self.Live == 1:
                self.Contours[i].DrawCanvas(self.Canvas, Parameters, self.ZoomBox[0], self.ZoomBox[2], self.ZoomBox[1], self.ZoomBox[3])
        
            #Draw the elements in PIL
            if self.Live == 2:
                self.Contours[i].DrawPyG(draw, Parameters, self.ZoomBox[0], self.ZoomBox[2], self.ZoomBox[1], self.ZoomBox[3])
        
        
        ##########################################################################################
        #Draw the Regions (note that regions have no impat on the width determinations)
        #They are drawn first as they will then be below the rest...
        for i in range(0,len(self.Ranges)):
            
            #is this plot active
            if self.Ranges[i].Active:
            
                #Draw the elements in PIL
                if self.Live == 0:
                    self.Ranges[i].DrawPIL(draw, Parameters)
                
                #Draw the elements in PIL
                if self.Live == 1:
                    self.Ranges[i].DrawCanvas(self.Canvas, Parameters)
                
                #Draw the elements in PIL
                if self.Live == 2:
                    self.Ranges[i].DrawPyG(draw, Parameters)

        ##########################################################################################
        #Draw the Lines
        for i in range(0,len(self.Lines)):
            
            #is this plot active
            if self.Lines[i].Active:

                #Draw the elements in PIL@
                if self.Live == 0:
                    self.Lines[i].DrawPIL(draw, Parameters)
                
                #Draw the elements in PIL
                if self.Live == 1:
                    self.Lines[i].DrawCanvas(self.Canvas, Parameters)
                
                #Draw the elements in PIL
                if self.Live == 2:
                    self.Lines[i].DrawPyG(draw, Parameters)
        
        ##########################################################################################
        #Draw the plot
        for i in range(0,len(self.Plots)):
            
            #is this plot active
            if self.Plots[i].Active:

                #Draw the elements in PIL
                if self.Live == 0:
                    self.Plots[i].DrawPIL(draw, Parameters)
                
                #Draw the elements in PIL
                if self.Live == 1:
                    self.Plots[i].DrawCanvas(self.Canvas, Parameters)
                
                #Draw the elements in PIL
                if self.Live == 2:
                    self.Plots[i].DrawPyG(draw, Parameters)
    
        
        if self.Live == 0:

            ##################################################
            #canvas have the disease of redrawing everything on move of the
            #pointer and so on. In order to fight this we save
            #plot as an image here and then redisplay it as a single bitmap
            #note that this obvioulsy means the object has to
            #be trashed before hand...
            
            # np.asarray(img) is read only. Wrap it in np.array to make it modifiable.
            
            if self.Axes.XGrid or self.Axes.YGrid:
                
                if not Tkinter.TclVersion < 8.5:
                    
                    threshold   =   225
                    dist        =   0
                    
                    arr = numpy.array(numpy.asarray(image))
                    
                    r,g,b,a = numpy.rollaxis(arr,axis = -1)
                    
                    mask = ((r>=threshold)
                            & (g>=threshold)
                            & (b>=threshold)
                            & (numpy.abs(r-g)<=dist)
                            & (numpy.abs(r-b)<=dist)
                            & (numpy.abs(g-b)<=dist)
                            )
                            
                    arr[mask,3] = 0
                    
                    image = Image.fromarray(arr,mode='RGBA')
            
            self.ResizedImage   = image.resize((self.wScaleFactor,self.hScaleFactor))
            
            self.Image          = ImageTk.PhotoImage(self.ResizedImage)
            
            self.MainPlotID     = self.Canvas.create_image(self.wScaleFactor/2,
                                                           self.hScaleFactor/2,
                                                           image = self.Image)
            
            
            try:
                self.Canvas.tag_lower(self.MainPlotID, 'Top')

            except:
                pass

        elif self.Live == 2:
        
        
            self.Image = pyg.image.tostring(draw, 'RGBA', True)
            
            #get the dimentiorns
            w, h       = draw.get_rect()[2:]
            
            self.ResizedImage = Image.frombytes('RGBA', (w, h), self.Image)
            
            self.Image  = ImageTk.PhotoImage(self.ResizedImage)
            
            #print self.Image
            
            self.MainPlotID     = self.Canvas.create_image(self.wScaleFactor/2,
                                                           self.hScaleFactor/2,
                                                           image = self.Image)
                
            try:
                self.Canvas.tag_lower(self.MainPlotID, 'Top')

            except:
                pass
        else:
            
            #change layer order for the elements
            for i in range(0,len(self.Plots)):
                
                for j in range(0,len(self.Plots[i].IdentifierList)):
                
                    self.Canvas.tag_lower(self.Plots[i].IdentifierList[j], 'Top')

            for i in range(0,len(self.Ranges)):
                
                self.Canvas.tag_lower(self.Ranges[i].Identifier, 'Top')
            
    def RemoveAllRanges(self):
    
        '''
        ########################################################################
        Similar to the draw routine it will go tough the plot definitions and
        then remove the elements. Note that it will only redraw the ones that
        have been set to drawn before
        ########################################################################
        '''
    
        self.Ranges = []

    def RedrawRange(self):

        '''
        ########################################################################
        When elements have been dawn in Tkinter canvas mode they can be deleted
        and then pushed out. This avoids having garbade presented.
        ########################################################################
        '''
        
        for i in range(0,len(self.Ranges)):
            
            if self.Ranges[i].CanvasObject:
            
                self.Canvas.delete(self.Ranges[i].Identifier)

    def RemoveAllLines(self):
    
        '''
        ########################################################################
        Similar to the draw routine it will go tough the plot definitions and
        then remove the elements. Note that it will only redraw the ones that
        have been set to drawn before
        ########################################################################
        '''
    
        self.Lines = []

    def RedrawLines(self):

        '''
        ########################################################################
        When elements have been dawn in Tkinter canvas mode they can be deleted
        and then pushed out. This avoids having garbade presented.
        ########################################################################
        '''
        
        for i in range(0,len(self.Lines)):
            
            if self.Lines[i].CanvasObject:
            
                self.Canvas.delete(self.Lines[i].Identifier)

    def RedrawPlots(self):

        '''
        ########################################################################
        When elements have been dawn in Tkinter canvas mode they can be deleted
        and then pushed out. This avoids having garbade presented.
        ########################################################################
        '''
        
        for i in range(0,len(self.Plots)):
            
            if self.Plots[i].CanvasObject:
            
                for j in range(0,len(self.Plots[i].IdentifierList)):
                
                    try:
                        self.Canvas.delete(self.Plots[i].IdentifierList[j])
    
                    except:
                        print 'Could not delete the element'

    
    def RemoveAllPlots(self):
        
        '''
        ########################################################################
        This will clear and delete the list of Plots and and allow them to be
        garbage collected. On the next draw all elements will disapar
        ########################################################################
        '''
    
        self.Plots = []


    def RedrawContours(self):

        '''
        ########################################################################
        When elements have been dawn in Tkinter canvas mode they can be deleted
        and then pushed out. This avoids having garbade presented.
        ########################################################################
        '''
        
        for i in range(0,len(self.Contours)):
            
            if self.Contours[i].CanvasObject:
            
                for j in range(0,len(self.Contours[i].IdentifierList)):
                
                    try:
                        self.Canvas.delete(self.Contours[i].IdentifierList[j])
    
                    except:
                        print 'Could not delete the element'

    
    def RemoveAllContours(self):
        
        '''
        ########################################################################
        This will clear and delete the list of Plots and and allow them to be
        garbage collected. On the next draw all elements will disapar
        ########################################################################
        '''
    
        self.Contours = []
    
    def Save(self,FileName = 'Untitled', color = 'color'):
        
        '''
        ########################################################################
        This routine allows to save the current canvas content. Note that the 
        cursor behaviour should be set prior to saving as this routine will gather
        anything on the screen...
        ########################################################################
        '''
        print 'I tried to save'
        print 'This is the filemane: ',FileName
        #chech if the proper extension is here
        if len(FileName.split('.eps')) < 2:
        
            FileName = FileName+'.eps'
        
        #save the content to postscript
        self.Canvas.postscript(file = FileName, colormode = color)


'''
I want a settings window to adjust padding and ticks and 
things like this dynamically...

class Settings:

'''

if __name__ == "__main__":
    #profile.run('main(); print')
    main()
