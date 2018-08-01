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
from Tkinter  import *
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

#import visual element classes
import Visual_Contour  as ContourClass
import Visual_Cascade  as CascadeClass
import Visual_Plot     as PlotClass
import Visual_Int_Plot as InteractivePlotClass
import Visual_Line     as LineClass
import Visual_Range    as RangeClass

#import UI element classes
import UI_Axes           as AxesClass
import UI_Interaction    as InteractionClass
import UI_Keyboard       as KeyboardClass
import UI_Title          as TitleClass
import UI_Zoomer         as ZoomerClass
import UI_Legend         as LegendClass

#import Pointer definition classes
import Pointer_Pointer       as PointerClass
import Pointer_Modification  as ModificationClass
import Pointer_Measurement   as MeasurementClass
import Pointer_Move_Object   as MoveClass


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
        self.Ghost                  = False
        
        ##########################################
        #Default Zoom identifiers
        self.SmartResize            = False
        self.SmartResizeFactor      = [1.0,0.90]
        
        ##########################################
        #Initialise different elements of the plot
        
        #The axes
        self.Axes       = AxesClass.Axes(self.Canvas)
        
        #Set the mouse
        self.Mouse      = InteractionClass.Mouse(self.Canvas)
        
        #Set the keyboard
        self.Keyboard   = KeyboardClass.Keyboard(self.Canvas,Multi = self.Multi)
        
        #The pointer
        self.Pointer    = PointerClass.Pointer(self.Canvas)
        
        #The zoomer
        self.Zoomer     = ZoomerClass.Zoomer(self.Canvas)
        
        #the measurement Tool
        self.Measurer   = MeasurementClass.Measure(self.Canvas)
        
        #The Modifier
        self.Modifier   = ModificationClass.Modify(self.Canvas)
        
        #the title
        self.Title      = None #TitleClass.TitleClass(self.Canvas)
        
        ##########################################
        #initialise drawing lists
        self.Plots      = []
        self.iPlots     = []
        self.Ranges     = []
        self.Lines      = []
        self.Contours   = []
        self.Cascades   = []
        
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
    
        '''
        ######################################################
        Binds the zoomer to the current system. Note that 
        unbind can be called to silence it.
        ######################################################
        '''
        self.Zoomer.Listen()
    
    def UnbindZoomer(self):
    
        '''
        ######################################################
        Binds the zoomer to the current system. Note that 
        unbind can be called to silence it.
        ######################################################
        '''
        self.Zoomer.Quiet()
    
    def BindMeasurer(self):
    
        '''
        ######################################################
        Binds the zoomer to the current system. Note that 
        unbind can be called to silence it.
        ######################################################
        '''
        self.Measurer.Listen()
    
    def UnbindMeasurer(self):
    
        '''
        ######################################################
        Binds the zoomer to the current system. Note that 
        unbind can be called to silence it.
        ######################################################
        '''
        self.Measurer.Quiet()
    
    def BindModifier(self):
    
        '''
        ######################################################
        Binds the zoomer to the current system. Note that 
        unbind can be called to silence it.
        ######################################################
        '''
        self.Modifier.Listen()
    
    def UnbindModifier(self):
    
        '''
        ######################################################
        Binds the zoomer to the current system. Note that 
        unbind can be called to silence it.
        ######################################################
        '''
        self.Modifier.Quiet()
    
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
        
        #redraw Plots
        self.RedrawPlots()
        
        #redraw allplots
        self.RedrawiPlots()
        
        #redraw Ranges
        self.RedrawRange()
        
        #redraw Lines
        self.RedrawLines()
        
        #redraw Contours
        self.RedrawContours()
        
        #redraw Contours
        self.RedrawCascades()
        
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
    
    def MakeGhost(self):
    
        ###################
        #remove the plots
    
        self.Ghost = True
    
    
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
        self.RedrawiPlots()
        
        #redraw allplots
        self.RedrawRange()
        
        #redraw allplots
        self.RedrawLines()
        
        #redraw allplots
        self.RedrawContours()
        
        #redraw allplots
        self.RedrawCascades()
        
        #redraw allplots
        self.RemoveAllPlots()
        
        #redraw allplots
        self.RemoveAlliPlots()
        
        #redraw allplots
        self.RemoveAllRanges()
                         
        #redraw allplots
        self.RemoveAllLines()
        
        #redraw allplots
        self.RemoveAllContours()
        
        #redraw allplots
        self.RemoveAllCascades()
        
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
        # - color
        # - Active state
        # - Drawn (To knbow if an item has been drawn)
        # - Name Not necessary (can be usefull)
        # - Do we use the scater points
        ######################################################
        '''
        #internal reference identifier
        self.identifier += 1
        
        #Load the parameters into the plot list
        self.Plots.append(PlotClass.PlotClass(X,Y,
                                    Thickness,
                                    color,
                                    Active,
                                    Name,
                                    style,
                                    Indentifier = self.identifier))

        return self.Plots[-1]
 
 
    def AddiPlot(self,X,Y,
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
        # - color
        # - Active state
        # - Drawn (To knbow if an item has been drawn)
        # - Name Not necessary (can be usefull)
        # - Do we use the scater points
        ######################################################
        '''
        #internal reference identifier
        self.identifier += 1
        
        #Load the parameters into the plot list
        self.iPlots.append(InteractivePlotClass.InteractivePlotClass(X,Y,
                                                          Thickness,
                                                          color,
                                                          Active,
                                                          Name,
                                                          style,
                                                          Indentifier = self.identifier))

        return self.iPlots[-1]
    
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
        self.Plots.append(ContourClass.OneDProjectionClass(Contour,
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
        self.Lines.append(LineClass.LineClass(Value,
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
        self.Contours.append(ContourClass.ContourClass(X,Y,Z,
                 
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
    
    
    def AddCascade(self,
                   X,Y,Z,
                 
                   #General variables
                   Type = 'Surface',
                   Range = None,
                   Active = True,
                   Name = '',
                   style = [0,0,0],
                   Stepping = 0.1,
                 
                   #Surface variables
                   ColorList = None):

        '''
        ######################################################
        #This will add a line to be drawn
        ######################################################
        '''
        
        #internal reference identifier
        self.identifier += 1
        
        #Load the parameters into the plot list
        self.Cascades.append(CascadeClass.CascadeClass(X,Y,Z,
                 
                                                       #General variables
                                                       Type      = Type,
                                                       Range     = Range,
                                                       Active    = Active,
                                                       Name      = Name,
                                                       style     = style,
                                                       Indentifier = self.identifier,
                                                       Stepping = Stepping,
                 
                                                       #Surface variables
                                                       ColorList = ColorList))
    
        return self.Cascades[-1]
    
    
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
        self.Ranges.append(RangeClass.RangeClass(Coordinates,self.identifier))
    
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
        if  len(self.Plots) > 0  or len(self.iPlots) > 0  or len(self.Contours) > 0 or len(self.Cascades) > 0:
        
            ######################################################
            #cycle through the plot and iplots commands and grab extremes
            for i in range(0,len(self.Plots)):
            
                #grab extremes
                XMax.append(numpy.max(self.Plots[i].X))
                XMin.append(numpy.min(self.Plots[i].X))
                YMax.append(numpy.max(self.Plots[i].Y))
                YMin.append(numpy.min(self.Plots[i].Y))
            
            for i in range(0,len(self.iPlots)):
            
                #grab extremes
                XMax.append(numpy.max(self.iPlots[i].X))
                XMin.append(numpy.min(self.iPlots[i].X))
                YMax.append(numpy.max(self.iPlots[i].Y))
                YMin.append(numpy.min(self.iPlots[i].Y))
            
            ######################################################
            #Add contour informationsto allow treatment
            for i in range(0,len(self.Contours)):
                
                #grab extremes
                XMax.append(self.Contours[i].XMax)
                XMin.append(self.Contours[i].XMin)
                YMax.append(self.Contours[i].YMax)
                YMin.append(self.Contours[i].YMin)
            
            ######################################################
            #Add contour informationsto allow treatment
            for i in range(0,len(self.Cascades)):
            
                #grab extremes
                XMax.append(self.Cascades[i].XMax)
                XMin.append(self.Cascades[i].XMin)
                YMax.append(self.Cascades[i].ZMax)
                YMin.append(self.Cascades[i].ZMin)
            
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
            
                #do a check if equal
                if self.BoundingBoxOffset[0] == self.BoundingBoxOffset[2]:
                
                    self.BoundingBoxOffset[0] -= 1e-6
                    self.BoundingBoxOffset[2] += 1e-6
                
                #fetch the paddings from the axes variables
                self.BoundingBoxFactor[0] = ((1.0-self.Axes.PaddingIn[0]-self.Axes.PaddingIn[2]
                                              -self.Axes.PaddingOut[0]-self.Axes.PaddingOut[2])
                                             /(self.BoundingBoxOffset[2]
                                               -self.BoundingBoxOffset[0]))

            ######################################################
            #cycle through the plot commands and grab extremes
            for i in range(0,len(self.Plots)):
        
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
                
                #do a check if equal
                if self.BoundingBoxOffset[1] == self.BoundingBoxOffset[3]:
                
                    self.BoundingBoxOffset[1] -= 1e-6
                    self.BoundingBoxOffset[3] += 1e-6
                
                #fetch the paddings from the axes variables
                self.BoundingBoxFactor[1] = ((1.0-self.Axes.PaddingIn[1]-self.Axes.PaddingOut[1]
                                              -self.Axes.PaddingIn[3]-self.Axes.PaddingOut[3])
                                             /(self.BoundingBoxOffset[3]-self.BoundingBoxOffset[1]))
            

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
        #Draw the Cascades
        for i in range(0,len(self.Cascades)):
            
            #Draw the elements in PIL
            if self.Live == 0:
                self.Cascades[i].DrawPIL(draw, Parameters)
            
            #Draw the elements in PIL
            if self.Live == 1:
                self.Cascades[i].DrawCanvas(self.Canvas, Parameters)
        
            #Draw the elements in PIL
            if self.Live == 2:
                self.Cascades[i].DrawPyG(draw, Parameters)
        
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
    
        ##########################################################################################
        #Draw the interactive plot (only supports canvas draw)
        for i in range(0,len(self.iPlots)):
            
            #is this plot active
            if self.iPlots[i].Active:

                #Draw the elements in PIL
                if self.Live == 1:
                    self.iPlots[i].DrawCanvas(self.Canvas, Parameters)
                
        
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
        
            for i in range(0,len(self.iPlots)):
                
                for j in range(0,len(self.iPlots[i].IdentifierList)):
                
                    self.Canvas.tag_lower(self.iPlots[i].IdentifierList[j], 'Top')
            

            for i in range(0,len(self.Ranges)):
                
                self.Canvas.tag_lower(self.Ranges[i].Identifier, 'Top')
            


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
    
    def RemoveAllRanges(self):
    
        '''
        ########################################################################
        Similar to the draw routine it will go tough the plot definitions and
        then remove the elements. Note that it will only redraw the ones that
        have been set to drawn before
        ########################################################################
        '''
    
        self.Ranges = []

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

    def RemoveAllLines(self):
    
        '''
        ########################################################################
        Similar to the draw routine it will go tough the plot definitions and
        then remove the elements. Note that it will only redraw the ones that
        have been set to drawn before
        ########################################################################
        '''
    
        self.Lines = []

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

    def RedrawiPlots(self):

        '''
        ########################################################################
        When elements have been dawn in Tkinter canvas mode they can be deleted
        and then pushed out. This avoids having garbade presented.
        ########################################################################
        '''
        
        for i in range(0,len(self.iPlots)):
            
            if self.iPlots[i].CanvasObject:
            
                for j in range(0,len(self.iPlots[i].IdentifierList)):
                
                    try:
                        self.Canvas.delete(self.iPlots[i].IdentifierList[j])
    
                    except:
                        print 'Could not delete the element'

    
    def RemoveAlliPlots(self):
        
        '''
        ########################################################################
        This will clear and delete the list of Plots and and allow them to be
        garbage collected. On the next draw all elements will disapar
        ########################################################################
        '''
    
        self.iPlots = []

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
    
    def RedrawCascades(self):

        '''
        ########################################################################
        When elements have been dawn in Tkinter canvas mode they can be deleted
        and then pushed out. This avoids having garbade presented.
        ########################################################################
        '''
        
        for i in range(0,len(self.Cascades)):
            
            if self.Cascades[i].CanvasObject:
            
                for j in range(0,len(self.Cascades[i].IdentifierList)):
                
                    try:
                        self.Canvas.delete(self.Cascades[i].IdentifierList[j])
    
                    except:
                        print 'Could not delete the element'

    
    def RemoveAllCascades(self):
        
        '''
        ########################################################################
        This will clear and delete the list of Plots and and allow them to be
        garbage collected. On the next draw all elements will disapar
        ########################################################################
        '''
    
        self.Cascades = []
    
    def SaveImage(self,DirName, FileName = 'Untitled', color = 'color'):
        
        '''
        ########################################################################
        This routine allows to save the current canvas content. Note that the 
        cursor behaviour should be set prior to saving as this routine will gather
        anything on the screen...
        ########################################################################
        '''
        print 'I tried to save to image'
        print 'This is the filemane: ',FileName
        #chech if the proper extension is here
        if len(FileName.split('.eps')) < 2:
        
            FileName = FileName+'.eps'
        
        #save the content to postscript
        self.Canvas.postscript(file = os.path.join(DirName,FileName), colormode = color)



    def SaveText(self,DirName, FileName = 'Untitled', color = 'color', Invert = 0):
        
        '''
        ########################################################################
        This routine allows to save the current canvas content. Note that the 
        cursor behaviour should be set prior to saving as this routine will gather
        anything on the screen...
        ########################################################################
        '''
        
        print 'I am trying to save the data in text files...'
        
        
        #chech if the proper extension is here
        if len(FileName.split('.txt')) < 2:
        
            FileName = FileName+'.txt'
        
        ##########################################################################################
        #Draw the plot
        for i in range(0,len(self.Plots)):
            
            #is this plot active
            if self.Plots[i].Active:

                #grab the plot put into numpy array and save it to text
                if Invert == 0:
                
                    X = self.Plots[i].X
                    Y = self.Plots[i].Y
                
                else:
                
                    X = self.Plots[i].Y
                    Y = self.Plots[i].X
                
                #set the exit array
                ExitArray = numpy.zeros((len(X),2))
            
                #loop over and fill it
                for j in range(len(X)):
            
                    ExitArray[j,0] = X[j]
                    ExitArray[j,1] = Y[j]
            
                #save it out
                numpy.savetxt(os.path.join(DirName,FileName+'_Plot_'+str(i)+'.txt'), ExitArray)
                
                print 'This is the filemane: ',os.path.join(DirName,FileName+'_Plot_'+str(i)+'.txt')
        ##########################################################################################
        #Draw the interactive plot (only supports canvas draw)
        for i in range(0,len(self.iPlots)):
            
            #is this plot active
            if self.iPlots[i].Active:

                #grab the plot put into numpy array and save it to text
                X = self.iPlots[i].X
                Y = self.iPlots[i].Y
        
                #set the exit array
                ExitArray = numpy.zeros((len(X),2))
            
                #loop over and fill it
                for j in range(len(X)):
            
                    ExitArray[j,0] = X[j]
                    ExitArray[j,1] = Y[j]
            
                #save it out
                numpy.savetxt(os.path.join(DirName,FileName+'_iPlot_'+str(i)+'.txt'), ExitArray)

                print 'This is the filemane: ',os.path.join(DirName,FileName+'_iPlot_'+str(i)+'.txt')
