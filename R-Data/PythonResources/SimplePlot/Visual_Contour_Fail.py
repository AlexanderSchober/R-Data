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

#import this contour C class call
from matplotlib import _cntr as cntr


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
                 Type           = 'Surface',
                 Range          = None,
                 Active         = True,
                 Name           = '',
                 style          = [0,0,0],
                 Indentifier    = None,
                 
                 #Surface variables
                 ColorList      = None,
                 Stepping       = 10,
                 
                 #Mesh variables
                 MeshColorList  = None,
                 MeshStepping   = 10,
                 MeshThickness  = 5):

        ############################################################
        ############################################################
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
        ############################################################
        #set the parameters
        self.Active     = Active

        #set the style
        self.Style      = style
    
        #identifier
        self.Identifier     = Indentifier
        self.IdentifierList = []
        self.CanvasObject   = False
        
        ############################################################
        ############################################################
        #set the Surface variables
        self.ColorList  = ColorList
        self.Stepping   = Stepping
        self.MeshStepping = MeshStepping
        
        ############################################################
        ############################################################
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

        #build a color map
        if self.ColorList == None:
            
            self.ColorList = ['blue',
                              'green',
                              'turquoise',
                              'yellow',
                              'red']
        
        if self.MeshColorList == None:
            
            self.MeshColorList = ['black',
                                  'black']
        
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
        ############################################################
        ############################################################
        #first check if the dimentionality is right
        if not self.X.shape == self.Y.shape or not self.Y.shape == self.Z.shape:
            
            #break right here
            if self.Verbose:
            
                print 'Dimentionality test failed'
            
            return 0

        
        ############################################################
        ############################################################
        #compute boundaries
        Max = self.ZMax
        Min = self.ZMin
        
        #break right here
        if self.Verbose:
                
            print 'This is the found Max: ',Max
            print 'This is the found Min: ',Min
        
        ############################################################
        ############################################################
        #compute boundaries
        self.Range      = [Min - 1e-10 + float(i) * (Max - Min)/float(self.Stepping)
                           for i in range(0,self.Stepping)]
        self.MeshRange  = [Min - 1e-10 + float(i) * (Max - Min)/float(self.MeshStepping)
                           for i in range(0,self.MeshStepping)]
        
        if self.Verbose:
                
            print 'This is the Range:\n ',self.Range
        
        ############################################################
        ############################################################
        #create scanner clases
            
        #create scanner class
        self.Scanner = ContourScannerClass(self)

        #run him
        self.Surfaces,self.Meshes = self.Scanner.Scan('Normal')
        
        #Set the color
        for l in range(len(self.Surfaces)):
            
            for k in range(len(self.Surfaces[l])):
                
                #set the parameters
                self.Surfaces[l][k].Color = [self.RGB[l],self.RGB[l-1]]
                
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
        ######################################################
        ######################################################
        #make sure the image has a high enough resolution for drwing
        self.XPixels      = 4000
        self.YPixels      = 4000
        
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
        
        
        ######################################################
        ######################################################
        #write the graphical elements


        #Grab the maximum order to draw
        Order = 0
        
        for Level in self.Surfaces:

            for Surface in Level:
                
                if Surface.MaxOrder > Order:
                
                    Order = Surface.MaxOrder
        
        
        
        ######################################################
        #draw up the surfaces
        for k in range(0, Order):
            
            for Level in self.Surfaces:

                for Surface in Level:
                    
                    Surface.DrawPyG(self.DrawSurface,
                                    Parameters,
                                    k)
        
        
        ######################################################
        #draw up the meshes
        for Meshes in self.Meshes:

            for Mesh in Meshes:
                
                Mesh.DrawPyG(self.DrawSurface,
                             Parameters)
            
        
        #set logic
        self.CanvasObject = False

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
                
                self.Surfaces[i][j].DrawPIL(Target, Parameters)
    
    
        #draw up
        for i in range(len(self.Meshes)):

            for j in range(len(self.Meshes[i])):
                
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
                
                self.IdentifierList.append(self.Surfaces[i][j].DrawCanvas(Target, Parameters))
    
        #draw up
        for i in range(0, len(self.Meshes)):

            for j in range(0, len(self.Meshes[i])):
                
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
    
    def __init__(self,Data,Polygones, Order):

        #grab the parameters
        self.Verbose        = False
        self.Active         = True
        self.Color          = ['black','black']
        self.CanvasObject   = False
        
        #set the position of the polygone
        self.Polygones      = numpy.copy(Polygones)
        self.Order          = numpy.copy(Order)
        self.MaxOrder       = numpy.max(Order)
        self.Type           = 'Surface'

        
    def DrawPyG(self, Target, Parameters, Order_idx):
        '''
        ######################################################
        PyG imaging technique
        ######################################################
        '''
        
        #loop over the available polygones
        for idx,Polygone in enumerate(self.Polygones):
            
            if self.Order[idx] == Order_idx:
            
                #make a draw list per polygone list
                DrawList = Polygone
                
                #loop over the points
                DrawList = [((DrawList[j][0]
                              - Parameters[0][0])
                             * Parameters[4],
                             
                            (DrawList[j][1]
                             - Parameters[0][1])
                             *Parameters[5])
                            
                            for j in range(len(DrawList))]
                
               
                if self.Verbose:
                    
                    print 'Trying to draw:\n',DrawList
                    print Parameters
                
                #drw the polygones
                self.AntiAlliasPolygone(Target,
                                        Parameters,
                                        DrawList,
                                        Order_idx)
                
                self.CanvasObject   = False


    def AntiAlliasPolygone(self, Target, Parameters, DrawList,Order_idx):
        '''
        ######################################################
        This converts the default method into a anti aliassed
        one. This particular case is for lines. Note that
        this allows the contour lines to be rather slooth
        ######################################################
        '''
        if len(DrawList) <= 2:
        
            return
    
        #draw
        pygame.gfxdraw.aapolygon(Target,
                                 DrawList,
                                 self.Color[Order_idx % 2])
                                 
        pygame.gfxdraw.filled_polygon(Target,
                                      DrawList,
                                      self.Color[Order_idx % 2])
    
    def DrawPIL(self, Target, Parameters, Order_idx):
        '''
        ######################################################
        PIL imaging technique
        ######################################################
        '''
        #loop over the available polygones
        for idx,Polygone in enumerate(self.Polygones):
            
            if self.Order[idx] == Order_idx:
            
                #make a draw list per polygone list
                DrawList = Polygone
            
                #make the plot list
                DrawList = [(((DrawList[j][0]
                               -Parameters[0][0])
                              *Parameters[1][0]
                              +Parameters[2][0]
                              +Parameters[3][0])
                             *Parameters[4]
                             *Parameters[6],
                             
                             (-(DrawList[j][1]
                                -Parameters[0][1])
                              *Parameters[1][1]
                              +1
                              -Parameters[2][1]
                              -Parameters[3][1])
                             *Parameters[5]
                             *Parameters[6])
                            
                            for j in range(0,len(DrawList))]
                
                        
                #draw the objectmatplotlib.colors.rgb2hex(self.color[i])
                if self.Verbose:
                    print 'Trying to draw:\n',DrawList
                
                try:
                    
                    Target.polygon(DrawList,
                                   fill    =   self.Color[Order_idx % 2])
                except:
                    
                    print DrawList
                
                #set the state
                self.CanvasObject   = False

    def DrawCanvas(self, Target, Parameters, Order_idx):
        
        '''
        ######################################################
        This is he classical imaging technique
        ######################################################
        '''
        self.Identifier = []
        
        #loop over the available polygones
        for Polygone in self.Polygones:
            
            #make a draw list per polygone list
            DrawList = Polygone
            
            #make the plot list
            DrawList = [(((DrawList[j][0]
                           -Parameters[0][0])
                          *Parameters[1][0]
                          +Parameters[2][0]
                          +Parameters[3][0])
                         *Parameters[4],
                         
                         (-(DrawList[j][1]
                            -Parameters[0][1])
                          *Parameters[1][1]
                          +1-Parameters[2][1]
                          -Parameters[3][1])
                         *Parameters[5])
                        
                        for j in range(0,len(DrawList))]

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
    
    def __init__(self,Data,Meshes):

        #grab the parameters
        self.Verbose        = False
        self.Active         = True
        self.Color          = 'black'
        self.CanvasObject   = False
        
        #set the position of the polygone
        self.Meshes         = Meshes
        self.Thickness      = 1
        self.Type           = 'Mesh'

        
    def DrawPyG(self, Target, Parameters):
        '''
        ######################################################
        PyGame imaging echnique. Note that this explicitly 
        calls an antialliassing method that is the line ...
        ######################################################
        '''
        
        #loop over the available polygones
        for Mesh in self.Meshes:
            
            #make a draw list per polygone list
            DrawList = Mesh.tolist()
            
            #loop over the points
            DrawList = [((DrawList[j][0]
                          - Parameters[0][0])
                         * Parameters[4],
                         
                        (DrawList[j][1]
                         - Parameters[0][1])
                         *Parameters[5])
                        
                        for j in range(len(DrawList))]
           
            if self.Verbose:
                
                print 'Trying to draw:\n',DrawList
                print Parameters
            
            
            ###########################
            #send out antialliassing
            [self.AntiAlliasLine(Target,
                                 Parameters,
                                 DrawList[i-1],
                                 DrawList[i])
             
             for i in range(len(DrawList))]
            
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
        pygame.gfxdraw.aapolygon(Target,
                                 (UL, UR, BR, BL),
                                 self.Color)
                                 
        pygame.gfxdraw.filled_polygon(Target,
                                      (UL, UR, BR, BL),
                                      self.Color)

    def DrawPIL(self, Target, Parameters):
        '''
        ######################################################
        PIL imaging technique
        ######################################################
        '''
        
        #loop over the available polygones
        for Mesh in self.Meshes:
            
            #make a draw list per polygone list
            DrawList = Mesh.tolist()
            
            #loop over the points
            DrawList = [(((DrawList[j][0]
                           -Parameters[0][0])
                          *Parameters[1][0]
                          +Parameters[2][0]
                          +Parameters[3][0])
                         *Parameters[4]
                         *Parameters[6],
                         
                         (-(DrawList[j][1]
                            -Parameters[0][1])
                          *Parameters[1][1]
                          +1-Parameters[2][1]
                          -Parameters[3][1])
                         *Parameters[5]
                         *Parameters[6])
                        
                        for j in range(0,len(DrawList))]
            

            try:
                
                Target.line(DrawList,
                            fill    =   self.Color,
                            width = int(self.Thickness))
            
            except:
                
                pass
            
            #set the state
            self.CanvasObject   = False

    def DrawCanvas(self, Target, Parameters):
        
        '''
        ######################################################
        This is he classical imaging technique
        ######################################################
        '''
        #loop over the available polygones
        for Mesh in self.Meshes:
            
            #make a draw list per polygone list
            DrawList = Mesh.tolist()
            
            #loop over the points
            DrawList = [(((DrawList[j][0]
                           -Parameters[0][0])
                          *Parameters[1][0]
                          +Parameters[2][0]
                          +Parameters[3][0])
                         *Parameters[4]
                         *Parameters[6],
                         
                         (-(DrawList[j][1]
                            -Parameters[0][1])
                          *Parameters[1][1]
                          +1-Parameters[2][1]
                          -Parameters[3][1])
                         *Parameters[5]
                         *Parameters[6])
                        
                        for j in range(0,len(DrawList))]

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
        self.Type         = self.ContourClass.Type
        self.Processors   = self.ContourClass.Processors

    def Scan(self,State):
        
        '''
        ######################################################
        Scan and look at the result
        ######################################################
        '''

        
        ######################################################
        #Make a list copy for fast serching
        self.XasList    = self.ContourClass.X[:, 0]
        self.YasList    = self.ContourClass.Y[0, :]
        self.Z          = self.ContourClass.Z
        
        self.Boundaries = [self.ContourClass.XMin,
                           self.ContourClass.XMax,
                           self.ContourClass.YMin,
                           self.ContourClass.YMax]
        
        #initialise polygone managers (per range)
        Surfaces = []
        Meshes   = []
        
        #################################
        #We have a surface contour plot
        if self.Type == 'Surface':
            
            Surfaces = self.Process_Surfaces()
        

        #################################
        #We have a mesh contour plot
        elif self.Type == 'Mesh':
        
            #loop over the range
            for i in range(len(self.ContourClass.MeshRange)):
                
                #grab segments
                Processed_Segments = Contour_Porcessor.trace(self.ContourClass.MeshRange[i])
            
                #only hafl the outputs are segments (why we don't know)
                Processed_Segments = Processed_Segments[: len(Processed_Segments) / 2 ]
            
                #do we have a surface type of element
                Meshes[i + 1].append(MeshClass(self.ContourClass,
                                               Processed_Segments))
    
    
        #################################
        #We have a mesh and a surface contour plot
        elif self.Type == 'Double':
            
            
            #take care of the background
            Surfaces[0].append(PolygoneClass(self.ContourClass,
                                             [self.GrabBackground()]))
            
            
            #loop over the range
            for i in range(len(self.ContourClass.Range)):
                
                #grab segments
                Processed_Segments = Contour_Porcessor.trace(self.ContourClass.Range[i])
            
                #only hafl the outputs are segments (why we don't know)
                Processed_Segments = Processed_Segments[: len(Processed_Segments) / 2 ]
                
                #process corrections here
                Processed_Segments = self.Segments_to_Polygones(Processed_Segments)
            
                #do we have a surface type of element
                Surfaces[i + 1].append(PolygoneClass(self.ContourClass,
                                                     Processed_Segments))
    
    
            #loop over the range
            for i in range(len(self.ContourClass.MeshRange)):
                
                #grab segments
                Processed_Segments = Contour_Porcessor.trace(self.ContourClass.MeshRange[i])
            
                #only hafl the outputs are segments (why we don't know)
                Processed_Segments = Processed_Segments[: len(Processed_Segments) / 2 ]
            
                #do we have a surface type of element
                Meshes[i + 1].append(MeshClass(self.ContourClass,
                                               Processed_Segments))
    
        
        return Surfaces,Meshes


    def Process_Surfaces(self):
    
        '''
        ######################################################
        Do the surface processing
        ######################################################
        '''
        ######################################################
        #Grab the C contour class
        Contour_Porcessor = cntr.Cntr(self.ContourClass.X,
                                      self.ContourClass.Y,
                                      self.ContourClass.Z)
        
        
        ######################################################
        #initiate the polygone matrix
        Polygone_Matrix = []
        Draw_Level      = []
        Surfaces        = []
        
        ######################################################
        #take care of the background as low level first poly
        Polygone_Matrix.append([self.GrabBackground()])
        Surfaces.append([PolygoneClass(self.ContourClass,
                                       Polygone_Matrix[0],
                                       [0])])
        
        ######################################################
        #Build a loop with the polygones per range
        for i in range(len(self.ContourClass.Range)):
            
            #grab segments
            Processed_Segments = Contour_Porcessor.trace(self.ContourClass.Range[i])
            
            #only hafl the outputs are segments (why we don't know)
            Processed_Segments = Processed_Segments[: len(Processed_Segments) / 2 ]
            
            #process corrections here
            Processed_Segments = self.Segments_to_Polygones(Processed_Segments)
                
            #who is in whome
            Draw_Level = self.Fetch_Order(Processed_Segments)
            
            #do we have a surface type of element
            Polygone_Matrix = Processed_Segments
        
            #special case no polygones
            if len(Draw_Level) == 0:
            
                Draw_Level = [0]
            
            ######################################################
            #Link all and see what happens
            Surfaces.append([PolygoneClass(self.ContourClass,
                                           Polygone_Matrix,
                                           Draw_Level)])
        
        
        return Surfaces


    def Fetch_Order(self, Segments ):
        
        '''
        ######################################################
        Fetch in how many polygones it is
        ######################################################
        '''
        
        #initialise
        Order_Array = [0] * len(Segments)
        
        
        #grab the array
        for idx,Segment in enumerate(Segments):
        
            #grab a point (radome...)
            Point  = Segment[int(len(Segment)/2)]
        
            #check hwere it is inside
            Order = 0
        
            for idx_2,Segment_2 in enumerate(Segments):
        
                if not idx_2 == idx:
    
                    if self.Is_Point_Inside(Point, Segment_2):

                        Order   += 1
    
            #set the value
            Order_Array[idx] = Order

        return Order_Array


    def GrabBackground(self):
        
        '''
        ######################################################
        Scan and look at the result
        ######################################################
        '''
        
        #grab the array
        self.Edge_Coords = numpy.zeros((4,2))
    
    
        #fill X
        self.Edge_Coords[0,0] = numpy.min(self.ContourClass.X[:,0])
        self.Edge_Coords[1,0] = numpy.min(self.ContourClass.X[:,0])
        self.Edge_Coords[2,0] = numpy.max(self.ContourClass.X[:,0])
        self.Edge_Coords[3,0] = numpy.max(self.ContourClass.X[:,0])
        
        self.Edge_Coords[0,1] = numpy.min(self.ContourClass.Y[0,:])
        self.Edge_Coords[1,1] = numpy.max(self.ContourClass.Y[0,:])
        self.Edge_Coords[2,1] = numpy.max(self.ContourClass.Y[0,:])
        self.Edge_Coords[3,1] = numpy.min(self.ContourClass.Y[0,:])

        return self.Edge_Coords.tolist()


    
    def Segments_to_Polygones(self, Processed_Segments):
        
        '''
        ######################################################
        This will be a patcher to find which polygones 
        actually belong together. The contour method of
        matplotlib returns in fact countour lines that can 
        be used for mesh lines but can create issues when used
        to make polygones.
        ######################################################
        '''
        ######################################################
        #convert all
        Processed_Segments = [[Processed_Segments[i][j].tolist()
                               for j in range(len(Processed_Segments[i]))]
                              for i in range(len(Processed_Segments))]
     
        ######################################################
        #initialize a boolean to make a check of edges
        To_Remove = [self.Check_Edges(Segment)
                     for Segment in Processed_Segments]

        
        ######################################################
        New_Segments = self.Close_Segments(Processed_Segments,
                                           To_Remove)

        return New_Segments

    def Check_Edges(self, Segment):
        
        '''
        ######################################################
        This method will check if both the start and end point
        are located on edges which lays the assumption that
        connecting them will yield in a uncorrect polygone.
        ######################################################
        '''

        ######################################################
        #grab the first and the last points
        if  Segment[0][0] == Segment[-1][0] and Segment[0][1] == Segment[-1][1]:
            
            #log it out if we are verbose
            if self.Verbose:
            
                #log it out
                print 'This Segments start: ',Segment[0],' is equal to this end: ', Segment[-1]
            
            #return true we have to build this
            return True
    
        ######################################################
        #grab the first and the last points
        if  ((Segment[0][0] == numpy.max(self.XasList)
              or Segment[0][0] == numpy.min(self.XasList) )
             and (Segment[0][0] == Segment[-1][0])):

            
            #log it out if we are verbose
            if self.Verbose:
            
                #log it out
                print 'This Segments start: ',Segment[0],' is equal to this end: ', Segment[-1]
            
            #return true we have to build this
            return True

        ######################################################
        #grab the first and the last points
        if  ((Segment[0][1] == numpy.max(self.YasList)
              or Segment[0][1] == numpy.min(self.YasList) )
             and (Segment[0][1] == Segment[-1][1])):

            
            #log it out if we are verbose
            if self.Verbose:
            
                #log it out
                print 'This Segments start: ',Segment[0],' is equal to this end: ', Segment[-1]
            
            #return true we have to build this
            return True

        ######################################################
        #else return false
        return False

    def Close_Segments(self, Segments, To_Remove):
        
        '''
        ######################################################
        This method will check if both the start and end point
        are located on edges which lays the assumption that
        connecting them will yield in a uncorrect polygone.
        ######################################################
        '''
        ######################################################
        #extract all emements that we want to keep
        
        #initialise
        New_Segments    = []
        Initial_Length  = len(Segments)
        
        #loop over backwards and delete
        for i in range(Initial_Length):
        
            #is the Segment to consider
            if To_Remove[Initial_Length-1-i]:
                
                #fill the new segments
                New_Segments.append(numpy.copy(Segments[Initial_Length-1-i]))
                
                #delete the old segments
                del Segments[Initial_Length-1-i]
    
    
    
        ######################################################
        #Build an array of indexes of the end positions
        Idx_Array       = []
        
        #loop over the Segments
        for idx, Segment in enumerate(Segments):
            
            ##################
            #Process the value of interest and axis
            Idx_Array.append([[self.Process_Axis([numpy.argmin(numpy.abs(self.XasList
                                                                         - Segment[0][0])),
                                                  numpy.argmin(numpy.abs(self.YasList
                                                                         - Segment[0][1]))]),
                               idx,
                               0],
                                   
                              [self.Process_Axis([numpy.argmin(numpy.abs(self.XasList
                                                                         - Segment[-1][0])),
                                                  numpy.argmin(numpy.abs(self.YasList
                                                                         - Segment[-1][1]))]),
                               idx,
                               1]])

        
        ######################################################
        #Restructure into proper elements
        if len(Idx_Array) > 0:
        
            New_Segments.extend(self.Restructure(Segments,
                                                 Idx_Array))

        #else return false
        return New_Segments


    def Process_Axis(self, Array):
        
        '''
        ######################################################
        This method will check simple conditions to evaluate
        on which axis the point is at the edge and then pro-
        cess a direction to follow...
        
        First the axis
        
        - 0 for X = 0
        - 1 for X = Max
        - 2 for Y = 0
        - 3 for Y = Max
        
        The pointer towards the direction
        
        - 0 for X
        - 1 for Y
        
        The directions
        
        -  1 for the positive direction
        - -1 for the negative direction
        
        Then the position:
        
        - Simply give the index
        ######################################################
        '''
        
        #initialise
        Idx_Array = [None] * 5
        Limits    = [self.XasList.shape[0]-1,
                     self.YasList.shape[0]-1]
        
        ######################################################
        #process the axis finder
        
        #--------------------#
        if Array[0] == 0:
        
            Idx_Array[0] = 2
            Idx_Array[1] = 1
            Idx_Array[3] = list(Array)
            Idx_Array[4] = Array[1]
        
        if Array[0] == self.XasList.shape[0]-1:
        
            Idx_Array[0] = 3
            Idx_Array[1] = 1
            Idx_Array[3] = list(Array)
            Idx_Array[4] = Array[1]
        
        #--------------------#
        if Array[1] == 0:
        
            Idx_Array[0] = 0
            Idx_Array[1] = 0
            Idx_Array[3] = list(Array)
            Idx_Array[4] = Array[0]

        if Array[1] == self.YasList.shape[0]-1:
        
            Idx_Array[0] = 1
            Idx_Array[1] = 0
            Idx_Array[3] = list(Array)
            Idx_Array[4] = Array[0]
        
        ######################################################
        #Process direction
        New_Array_1 = list(Array)
        New_Array_2 = list(Array)
        
        
        if New_Array_1[Idx_Array[1]] + 1 > Limits[Idx_Array[1]]:
        
            if Idx_Array[0] == 0 or Idx_Array[0] == 2:
            
                New_Array_1[numpy.abs(Idx_Array[1]-1)] += 1
            
            else:
            
                New_Array_1[numpy.abs(Idx_Array[1]-1)] -= 1
        else:
        
            New_Array_1[Idx_Array[1]] += 1
        
        if New_Array_2[Idx_Array[1]] - 1 < 0:
        
            if Idx_Array[0] == 0 or Idx_Array[0] == 2:
            
                New_Array_2[numpy.abs(Idx_Array[1]-1)] += 1
            
            else:
            
                New_Array_2[numpy.abs(Idx_Array[1]-1)] -= 1
        
        else:
        
            New_Array_2[Idx_Array[1]] -= 1

        if self.Verbose:

            print 'First Array: ',New_Array_1
            print 'Second Array: ',New_Array_2

        #check
        if (self.Z[Array[0], Array[1]] <= self.Z[New_Array_1[0], New_Array_1[1]]
            
            and self.Z[Array[0], Array[1]] >= self.Z[New_Array_2[0], New_Array_2[1]]):
    
            Idx_Array[2] = 1

        else:

            Idx_Array[2] = -1

        ######################################################
        #Send the result out
        return Idx_Array


    def Restructure(self, Segments, Idx_Array):
        
        '''
        ######################################################
        This methods will remodel the segmentseithr into biger
        Segments or clsoe the appropriately woth the porders
        ######################################################
        '''
        ######################################################
        #Initialise the variables
        Assimilated     = [False] * len(Segments)
        New_Segments    = []
        
        ######################################################
        #start the loop
        for idx,Segment in enumerate(Segments):
        
            ##################################################
            #Is the segment already assimilated ?
            if Assimilated[idx]:
        
                pass
    
            #since not ddo something
            else:
    
                ##############################################
                #initialise variables
                Not_Finished        = True
                New_Segment         = list(Segment)
                CornerCount         = 0
                
                #initialise the segments and order
                Segments_To_Process = [[idx, 1, Segment]]
                
                #initialise the point matrix
                Points_To_Process   = [Idx_Array[idx][0],
                                       Idx_Array[idx][1]]
            

                ##############################################
                #loop over the stuff
                while Not_Finished:
                
                    #grab points to select
                    Next_Point      = self.Get_Next(Points_To_Process[-1],
                                                    Idx_Array)
                    
                    #verbode
                    if self.Verbose:
                    
                        print 'This is the point we grabed: '
                        print Next_Point
                    
                    #do we have a corner?
                    if Next_Point[1] == None:
                        
                        #do some checking
                        CornerCount += 1
                        
                        if CornerCount > 4:
                        
                            print 'Cornering problem'
                            break
                        
                        #process the edge in the polygone drawing
                        New_Segment.append([self.XasList[Next_Point[0][3][0]],
                                            self.YasList[Next_Point[0][3][1]]])
                    
                        #add the point and proceeed
                        Points_To_Process.append(Next_Point)
                
                
                    elif (      Next_Point[0][3][0] == Points_To_Process[0][0][3][0]
                          and   Next_Point[0][3][1] == Points_To_Process[0][0][3][1]):
                    
                        #verbode
                        if self.Verbose:
                    
                            print 'Case closed '
                            print 'QQQQQQQQQQQQQQQQQQQQQQQQQQ'
                        
                        #process the edge in the polygone drawing
                        New_Segment.append([self.XasList[Next_Point[0][3][0]],
                                            self.YasList[Next_Point[0][3][1]]])
                    
                        #add the point and proceeed
                        Points_To_Process.append(Next_Point)
                        
                        Not_Finished == False
                        break
            
                    
                    else:
                        
                        #verbode
                        if self.Verbose:
                        
                            print '#####ANOTHER GUY######'
                            print 'Segments before'
                            print New_Segment
                        
                        #is it in the right direction
                        if Next_Point[2] == 0:
    
                            #add the arry in the right direction
                            New_Segment.extend(Segments[Next_Point[1]])
                        
                            #add the two points
                            Points_To_Process.append(Idx_Array[Next_Point[1]][0])
                            Points_To_Process.append(Idx_Array[Next_Point[1]][1])
                        
                        #is it in the wrong direction
                        if Next_Point[2] == 1:
    
                            #add the arry in the other direction
                            New_Segment.extend(Segments[Next_Point[1]][::-1])
    
                            #add the two points
                            Points_To_Process.append(Idx_Array[Next_Point[1]][1])
                            Points_To_Process.append(Idx_Array[Next_Point[1]][0])
                        
                        #verbode
                        if self.Verbose:
                        
                            print 'Segments after'
                            print New_Segment
            
                ##############################################
                #Loop is done process what was used
                for Element in Points_To_Process:
    
                    if not Element[1] == None:
    
                        Assimilated[Element[1]] = True

                ##############################################
                #send out the new segment
                New_Segments.append(New_Segment)
                
        ######################################################
        #Process direction
        

        ######################################################
        #Send the result out
        return New_Segments


    def Get_Next(self, Point, Idx_Array):
        
        '''
        ######################################################
        This methods will remodel the segmentseithr into biger
        Segments or clsoe the appropriately woth the porders
        
        Point Structure
        First the axis
        
        - 0 for X = 0
        - 1 for X = Max
        - 2 for Y = 0
        - 3 for Y = Max
        
        The pointer towards the direction
        
        - 0 for X
        - 1 for Y
        
        The directions
        
        -  1 for the positive direction
        - -1 for the negative direction
        
        Then the position:
        
        - Simply give the index
        ######################################################
        '''
        ######################################################
        #initialize
        Point_Array = []
        Temp        = []
        
        #verbose
        if self.Verbose:
                    
            print '------------------------------------'
            print 'We are looking to complete this guy:'
            print 'Main Point: ',Point
            print 'Idx: ',Point[1]
        
        ######################################################
        #Grab all the ones on the same axis
        for idx,Point_in_Array in enumerate(Idx_Array):
            
            #verbose
            if self.Verbose:
                    
                print 'Available: ',Point_in_Array
                print 'Idx ',Point_in_Array[0][1]
        
            #------------------------------------------------#
            #are we on the same axis
            if Point[0][0] == Point_in_Array[0][0][0]:
        
                if (    Point[0][2] == 1
                    and Point[0][4] < Point_in_Array[0][0][4]
                    ):#and Point_in_Array[0][0][2] == -1):
            
                    Temp.append(Point_in_Array[0])
        
                if (    Point[0][2] == -1
                    and Point[0][4] > Point_in_Array[0][0][4]
                    ):#and Point_in_Array[0][0][2] == 1):
            
                    Temp.append(Point_in_Array[0])
    
            #------------------------------------------------#
            #are we on the same axis
            if Point[0][0] == Point_in_Array[1][0][0]:
        
                if (    Point[0][2] == 1
                    and Point[0][4] < Point_in_Array[1][0][4]
                    ):#and Point_in_Array[1][0][2] == -1):
            
                    Temp.append(Point_in_Array[1])
        
                if (    Point[0][2] == -1
                    and Point[0][4] > Point_in_Array[1][0][4]
                    ):#and Point_in_Array[1][0][2] == 1):
            
                    Temp.append(Point_in_Array[1])
    
        if self.Verbose:
                    
            print 'This i Temp:'
            print Temp
        
        ######################################################
        #Grab Process the ones in the right direction
        if len(Temp) > 0:
        
            Next_Point = Temp[numpy.argmin(numpy.abs(numpy.asarray([Element[0][4]
                                                                    for Element in Temp])
                                                     - Point[0][4]))]
        
        else:
        
            Next_Point = self.Grab_Corner(Point[0])


        ######################################################
        #Send the result out
        return Next_Point

    def Grab_Corner(self, Initial_Point):
        
        '''
        ######################################################
        When a corner needs to be processed ...
        
        There is only four corners obviously so we need to 
        check which one we take and then the direction to
        folow after this. 
        
        The direction will be a 90 rotaation and change of 
        index
        ######################################################
        '''
        
        ######################################################
        #go through cases
        
        #----------------------------------------------------#
        #the botom axis
        if Initial_Point[0] == 0:
        
            #bottom right
            if Initial_Point[2] == 1:
            
                Corner_Point = [3,
                                1,
                                1,
                                [self.XasList.shape[0]-1, 0],
                                0]
    
            #bottom left
            if Initial_Point[2] == -1:
            
                Corner_Point = [2,
                                1,
                                1,
                                [0, 0],
                                0]
        #----------------------------------------------------#
        #the top axis
        if Initial_Point[0] == 1:
            
            #top right
            if Initial_Point[2] == 1:
            
                Corner_Point = [3,
                                1,
                                -1,
                                [self.XasList.shape[0]-1, self.YasList.shape[0]-1],
                                self.YasList.shape[0]-1]
    
            #top left
            if Initial_Point[2] == -1:
            
                Corner_Point = [2,
                                1,
                                -1,
                                [0, self.YasList.shape[0]-1],
                                self.YasList.shape[0]-1]
    
        #----------------------------------------------------#
        #the left axis
        if Initial_Point[0] == 2:
        
            #right top
            if Initial_Point[2] == 1:
            
                Corner_Point = [1,
                                0,
                                1,
                                [0, self.YasList.shape[0]-1],
                                0]
    
            #ritght bottom
            if Initial_Point[2] == -1:
            
                Corner_Point = [0,
                                0,
                                1,
                                [0, 0],
                                0]
        #----------------------------------------------------#
        #the right axis
        if Initial_Point[0] == 3:
            
            #left top
            if Initial_Point[2] == 1:
            
                Corner_Point = [1,
                                0,
                                -1,
                                [self.XasList.shape[0]-1, self.YasList.shape[0]-1],
                                self.YasList.shape[0]-1]
    
            #left bottom
            if Initial_Point[2] == -1:
            
                Corner_Point = [0,
                                0,
                                -1,
                                [self.XasList.shape[0]-1, 0],
                                self.XasList.shape[0]-1]
        
        
        ######################################################
        #Send the result out
        return [Corner_Point, None, None]


    def Is_Point_Inside(self,Point, Polynome):
        '''
        ######################################################
        x, y -- x and y coordinates of point
        poly -- a list of tuples [(x, y), (x, y), ...]
        ######################################################
        '''
        
        if len(Polynome) > 10:
            
            Polynome = [Polynome[i * 10] for i in range(int(len(Polynome) / 10) - 2)]
        
        #initialise
        num = len(Polynome)
        
        i = 0
        
        j = num - 1
        
        #oolean
        c = False
        
        for i in range(num):
            
            if (((Polynome[i][1] > Point[1])
                != (Polynome[j][1] > Point[1]))
                
                and
                (Point[0] < Polynome[i][0]
                 + (Polynome[j][0]  - Polynome[i][0])
                 * (Point[1]        - Polynome[i][1])
                 / (Polynome[j][1]  - Polynome[i][1]))):
                    
                c = not c
                     
            j = i
                
        return c

class OneDProjectionClass:
    
    '''
    ######################################################
    This function aims at grabing the line from a contour
    plot data when requested and redraws it on request
    ######################################################
    '''
    
    def __init__(self,
                 Contour,
                 Thickness  = 1,
                 Color      = 'black',
                 Active     = True,
                 Type       = 'x',
                 Name       = '',
                 style      = ['',0,0],
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




