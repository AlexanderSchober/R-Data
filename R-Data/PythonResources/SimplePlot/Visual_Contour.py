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

#c implementation
try:
    try:
        print 'trying mac import'
        import CompiledRessources.MaccContourCalculations as CCalc

    except:
        
        print 'Mac import Failed'
        import CompiledRessources.LinuxcContourCalculations as CCalc
except:

    print 'both mac and Linux failed'
    import ContourCalculations as CCalc




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
        

        ##############
        #conver the basterd to lis
        self.X = list(self.XIni)
        self.Y = list(self.YIni)
        self.Z = list(self.ZIni)
        
        
    
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
        self.Range      = [Min - 1e-10 + float(i) * (Max - Min)/float(self.Stepping)
                           for i in range(0,self.Stepping)]
                           
        self.MeshRange  = [Min - 1e-10 + float(i) * (Max - Min)/float(self.MeshStepping)
                           for i in range(0,self.MeshStepping)]
        
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
        self.DrawSurface.fill((255,255,255))
        
        if self.Verbose_2:
            print 'This is the DrawSurface size: ', self.DrawSurface.get_rect()

        
        ######################################################
        ######################################################
        #write the graphical elements
        
        ######################################################
        #draw up the surfaces
        for Level in self.Surfaces:

            for Surface in Level:
                
                Surface.DrawPyG(self.DrawSurface,
                                Parameters)
        
        
        ######################################################
        #draw up the meshes
        for Meshes in self.Meshes:

            for Mesh in Meshes:
                
                Mesh.DrawPyG(self.DrawSurface,
                             Parameters)
        
        #set logic
        self.CanvasObject = False


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
            DrawList = [
                        #the X coordinate change
                        ((( self.Coordinates[j][0]
                           -Parameters[0][0])
                          *Parameters[1][0]
                          +Parameters[2][0]
                          +Parameters[3][0])
                         *Parameters[4]
                         *Parameters[6],
                         
                         #the y coordinate change
                         (- ( self.Coordinates[j][1]
                            - Parameters[0][1])
                          * Parameters[1][1]
                          + 1
                          - Parameters[2][1]
                          - Parameters[3][1])
                         * Parameters[5]
                         * Parameters[6])
                        
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
            self.MeshMatrix = [[None for i in range(len(self.ContourClass.MeshRange)) ]
                               for j in range((len(self.ContourClass.X)-1)*(len(self.ContourClass.X[0])-1))]
            
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
            self.SurfaceMatrix = [[None for i in range(len(self.ContourClass.Range)) ]
                                  for j in range((len(self.ContourClass.X)-1)*(len(self.ContourClass.X[0])-1))]
            
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
            self.MeshMatrix = [[None for i in range(len(self.ContourClass.MeshRange)) ]
                               for j in range((len(self.ContourClass.X)-1)*(len(self.ContourClass.X[0])-1))]
            
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
                                                    
                                                    args = (m,
                                                            Type,
                                                            X,
                                                            Y,
                                                            Z,
                                                            Range,
                                                            MeshRange,
                                                            Iterations,
                                                            output)))
        
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
        
            for j in range(len(Data.X[0])):

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




