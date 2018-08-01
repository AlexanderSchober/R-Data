# -*- coding: utf-8 -*-
'''
######################################################
############## Simple Plot Methods  ##################
######################################################


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

#import basic libraris
import numpy
import math

#import imaging libraries
import PIL
from PIL import Image,ImageDraw
from PIL import ImageTk
from PIL import ImageFilter
from PIL import ImageColor as ColorLib

#the last 'fast visual'
import pygame as pyg
import pygame.gfxdraw



class CascadeClass:
    
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
                 Type           = 'Straight',
                 Range          = None,
                 Active         = True,
                 Name           = '',
                 style          = [0,0,0],
                 Indentifier    = None,
                 Stepping       = 0.1,
                 Thickness      = 1,
                 Normalize      = True,
                 
                 #Surface variables
                 ColorList = None):

        ########################
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
        self.Thickness  = 1
        self.Normalize  = True
        
        ########################
        ########################
        #set the parameters
        self.Active     = Active

        #set the style
        self.Style = style
    
        #identifier
        self.Identifier     = Indentifier
        self.IdentifierList = []
        self.CanvasObject   = False
        
        ########################
        ########################
        #set the Surface variables
        self.ColorList  = ColorList
        self.Stepping   = Stepping
        
        
        if self.Verbose:
            
            print X,Y,Z
            print Stepping
            print Type
            print Range
            print Active
            print Name
            print style
            print Indentifier
        
        ########################
        ########################
        #visual
        if self.Verbose:
        
            print self.Z
            print self.X
            print self.Y
        
        
        ########################
        ########################
        #build a color map
        if self.ColorList == None:
            self.ColorList = ['blue','green','yellow','red']
    
    
        #initialise the variabes
        self.RGB = []
        
        for i in range(0,len(self.ColorList)-1):
            
            First   =  ColorLib.getrgb(self.ColorList[i])
            Last    =  ColorLib.getrgb(self.ColorList[i+1])
        
            for k in range(0,int(len(self.ZIni)/(len(self.ColorList)-1))+1):
        
        
                self.RGB.append((k*(Last[0]-First[0])/int(len(self.ZIni)/(len(self.ColorList)-1))+First[0],
                                 k*(Last[1]-First[1])/int(len(self.ZIni)/(len(self.ColorList)-1))+First[1],
                                 k*(Last[2]-First[2])/int(len(self.ZIni)/(len(self.ColorList)-1))+First[2]))

        ########################
        ########################
        #run the routine
        self.Run()

    def Run(self):

        '''
        ######################################################
        This function will process the data input and then
        send them out to the
        ######################################################
        '''
    
        #first run the reset
        self.Reset()

        #then run a nomalization
        if self.NormalizeZ:
    
            self.NormalizeZ()
            
        #process to the ofset
        self.Offset()

        #process to the ofset
        self.ProcessBoundaries()

    def Reset(self):

        '''
        ######################################################
        This function will process the data input and then
        send them out to the
        ######################################################
        '''
    
        #first run the reset
        #Prepaer the new arrays
        self.X = numpy.asarray(self.XIni)
        self.Y = numpy.asarray(self.YIni)
        self.Z = numpy.asarray(self.ZIni)

        ##############
        #conver the basterd to lis
        self.X = self.X.tolist()
        self.Y = self.Y.tolist()
        self.Z = self.Z.tolist()
    

    def ProcessBoundaries(self):

        '''
        ######################################################
        This funciton processes the min and max to allow for 
        a better representation...
        ######################################################
        '''
    
        #compute boundaries once
        if self.Range == None:
        
            self.ZMax = max([max(self.Z[j]) for j in range(0,len(self.Z))])
            self.ZMin = min([min(self.Z[j]) for j in range(0,len(self.Z))])
        
        else:
        
            self.ZMax = Range[1]
            self.ZMin = Range[0]
        
        #set X boundaries
        self.XMax = max([max(self.XIni[j]) for j in range(0,len(self.XIni))])
        self.XMin = min([min(self.XIni[j]) for j in range(0,len(self.XIni))])

        #Set Y boundaries
        self.YMax = max([max(self.YIni[j]) for j in range(0,len(self.YIni))])
        self.YMin = min([min(self.YIni[j]) for j in range(0,len(self.YIni))])
        

    def NormalizeZ(self):

        '''
        ######################################################
        This function will process the data input and then
        send them out to the
        ######################################################
        '''
        ##############
        #process the minium of each row
        ZMin = [min(self.Z[j]) for j in range(0,len(self.Z))]
        
        #remove the minimum
        for i in range(len(self.Z)):

            self.Z[i] = [self.Z[i][j] - ZMin[i] for j in range(0,len(self.Z[i])) ]


        ##############
        #process the max of each row
        ZMax = [max(self.Z[j]) for j in range(0,len(self.Z))]
        
        #remove the minimum
        for i in range(len(self.Z)):

            self.Z[i] = [self.Z[i][j] / ZMax[i] for j in range(0,len(self.Z[i])) ]
    
    def Offset(self):

        '''
        ######################################################
        This function will process the offset of the data and 
        send it back to the internal values to display
        ######################################################
        '''
        ##############
        #process the minium of each row
        ZMin = [min(self.Z[j]) for j in range(0,len(self.Z))]

        ##############
        #process the max of each row
        ZMax = [max(self.Z[j]) for j in range(0,len(self.Z))]

        #remove the minimum
        for i in range(len(self.Z)):

            Offset = (ZMax[i]-ZMin[i])*self.Stepping*i
            self.Z[i] = [self.Z[i][j] + Offset for j in range(0,len(self.Z[i])) ]

    def DrawPIL(self, Target, Parameters):

        '''
        ######################################################
        all plot elements will have an implicit draw method
        that will prepare the method and arguments to be drawn
        This instance will output the content into PIL
        ######################################################
        '''
    
        for i in range(0,len(self.Z)):
    
            self.DrawPILLocal(self.X[i],self.Z[i], Target, Parameters, self.RGB[i])

    def DrawPyG(self, Target, Parameters):
        '''
        ######################################################
        PyGame imaging echnique. Note that this explicitly 
        calls an antialliassing method that is the line ...
        ######################################################
        '''
    
        for i in range(0,len(self.Z)):
    
            self.DrawPyGLocal(self.X[i],self.Z[i], Target, Parameters, self.RGB[i])

    def DrawCanvas(self,Target, Parameters):

        '''
        ######################################################
        all plot elements will have an implicit draw method
        that will prepare the method and arguments to be drawn
        This Method will use the canvas draw method
        ######################################################
        '''

    
        for i in range(0,len(self.Z)):
    
            self.DrawCanvasLocal(self.X[i],self.Z[i], Target, Parameters, self.RGB[i])


    def DrawPILLocal(self, X,Y, Target, Parameters, Color):

        '''
        ######################################################
        all plot elements will have an implicit draw method
        that will prepare the method and arguments to be drawn
        This instance will output the content into PIL
        ######################################################
        '''
                      
        #make the plot list
        DrawList = [((( X[j]-Parameters[0][0])*Parameters[1][0]
                      +Parameters[2][0]+Parameters[3][0])*Parameters[4]*Parameters[6],
                     (-( Y[j]-Parameters[0][1])*Parameters[1][1]
                      +1-Parameters[2][1]-Parameters[3][1])*Parameters[5]*Parameters[6])
                    for j in range(0,len(X))]
                
        #draw the object
        Target.line(DrawList,
                    fill    =   Color,
                    width   =   self.Thickness*Parameters[6])
    
    
        #Do we need scater circles
        if self.Style[0] == 'o':
            
            for j in range(0,len(DrawList)):
            
                #draw the circle
                Target.ellipse((DrawList[j][0]-self.Style[1]*Parameters[6],
                                DrawList[j][1]-self.Style[2]*Parameters[6],
                                DrawList[j][0]+self.Style[1]*Parameters[6],
                                DrawList[j][1]+self.Style[2]*Parameters[6]),
                                fill = Color)

        #set the state
        self.CanvasObject   = False
    
    
    def DrawPyGLocal(self, X,Y, Target, Parameters, Color):
        '''
        ######################################################
        PyGame imaging echnique. Note that this explicitly 
        calls an antialliassing method that is the line ...
        ######################################################
        '''
        if self.Active:
            
            ########################
            #make the plot list
            DrawList = [((( X[j]-Parameters[0][0])*Parameters[1][0]
                          +Parameters[2][0]+Parameters[3][0])*Parameters[4],
                         
                         (( Y[j]-Parameters[0][1])*Parameters[1][1]
                          +Parameters[2][1]+Parameters[3][1])*Parameters[5])
                        for j in range(0,len(X))]

            ########################
            #Draw the anti alliased elements
            for l in range(0,len(DrawList)-1):
            
                self.AntiAlliasLine(Target, DrawList[l],DrawList[l+1],Color)
            
            
            ########################
            #Do we need scater circles
            if self.Style[0] == 'o':
                
                for j in range(0,len(DrawList)-1):
                
                    self.AntiAlliasEllipse(Target, DrawList[l],[self.Style[1],self.Style[2]],Color)
    
            
            if self.Verbose:
                
                print 'Trying to draw:\n',DrawList
                print Parameters
        
            #set the state
            self.CanvasObject   = False

    def AntiAlliasLine(self, Target, X0,X1,Color):
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
        pygame.gfxdraw.aapolygon(Target, (UL, UR, BR, BL), Color)
        pygame.gfxdraw.filled_polygon(Target, (UL, UR, BR, BL),  Color)
        
        #draw the cicrle at first end
        pygame.gfxdraw.aacircle(Target, int(X0[0]), int(X0[1]), int((self.Thickness / 2)),   Color)
        pygame.gfxdraw.filled_circle(Target, int(X0[0]), int(X0[1]), int((self.Thickness / 2)),   Color)
        
        #draw the circle at the last end
        pygame.gfxdraw.aacircle(Target, int(X1[0]), int(X1[1]), int((self.Thickness / 2)),   Color)
        pygame.gfxdraw.filled_circle(Target, int(X1[0]), int(X1[1]), int((self.Thickness / 2)),   Color)
    
    def AntiAlliasEllipse(self, Target, X, R, Color):
        '''
        ######################################################
        This draws an anti alliased elipse according to the 
        gfx antia alliased method
        ######################################################
        '''
        
        #draw the circle at the last end
        pygame.gfxdraw.aaellipse(Target, int(X[0]), int(X[1]), R[0] / 2, R[1] / 2,   Color)
        pygame.gfxdraw.filled_ellipse(Target, int(X[0]), int(X[1]), R[0] / 2, R[1] / 2,   Color)
    
    def DrawCanvasLocal(self, X,Y, Target, Parameters, Color):

        '''
        ######################################################
        all plot elements will have an implicit draw method
        that will prepare the method and arguments to be drawn
        This Method will use the canvas draw method
        ######################################################
        '''
        
        self.IdentifierList = []
        
        #make the plot list
        DrawList = [((( X[j]-Parameters[0][0])*Parameters[1][0]
                      +Parameters[2][0]+Parameters[3][0])*Parameters[4],
                     (-( Y[j]-Parameters[0][1])*Parameters[1][1]
                      +1-Parameters[2][1]-Parameters[3][1])*Parameters[5])
                    for j in range(0,len(X))]


        try:
            
            #draw the object
            self.IdentifierList.append(Target.create_line(DrawList,
                                                          fill     =   "#{0:02x}{1:02x}{2:02x}".format(max(0, min(Color[0], 255)),
                                                                                                max(0, min(Color[1], 255)),
                                                                                                max(0, min(Color[2], 255))),
                                                          width    =   self.Thickness,
                                                          tag = 'Top'))
    
        except:
            print 'error plotting...'
            print 'the Dataformat is probably not suited...'
        
        #Do we need scater circles
        if self.Style[0] == 'o':
            
            for j in range(0,len(DrawList)):
            
                #draw the circle
                self.IdentifierList.append(Target.create_oval((DrawList[j][0]-self.Style[1],
                                                              DrawList[j][1]-self.Style[2],
                                                              DrawList[j][0]+self.Style[1],
                                                              DrawList[j][1]+self.Style[2]),
                                                              fill     =   "#{0:02x}{1:02x}{2:02x}".format(max(0, min(Color[0], 255)),
                                                                                                max(0, min(Color[1], 255)),
                                                                                                max(0, min(Color[2], 255))),
                                                              tag = 'Top'))

        #set the state
        self.CanvasObject   = True





