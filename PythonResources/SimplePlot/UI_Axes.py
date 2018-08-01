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

#import Pointer definition classes
from Pointer_Pointer        import *
from Pointer_Modification   import *
from Pointer_Measurement    import *
from Pointer_Move_Object    import *

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
        self.PaddingIn  = [0.0, 0.0, 0.0, 0.0]
        self.PaddingOut = [0.1, 0.2, 0.05, 0.05]
        
        self.Type       = [True,True,True,True]
        self.Color      = ['black','black','black','black']
        self.Thickness  = [5,5,5,5]
        
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
        if os.name == 'nt':
            
            self.XLabelSize         = [('Helvetica', '9'),('Helvetica', '9')]
    
        else:
            
            self.XLabelSize         = [('Helvetica', '11'),('Helvetica', '11')]
        
        self.XLabelColor        = ['black','black']
        self.XLabelOffset       = [0.025,0.025]
        self.XLabelAdresses     = []
        self.XLabelRounding     = 1
    
        #XLabel variables
        if os.name == 'nt':
            
            self.YLabelSize         = [('Helvetica', '9'),('Helvetica', '9')]
    
        else:
            
            self.YLabelSize         = [('Helvetica', '11'),('Helvetica', '11')]
        
        self.YLabelColor        = ['black','black']
        self.YLabelOffset       = [0.05,0.05]
        self.YLabelAdresses     = []
        self.YLabelRounding     = 1
        
        #label formating
        self.isXSci             = [False,False]
        self.isYSci             = [False,False]
        self.XSciPrecision      = ['%.1e','%.1e']
        self.YSciPrecision      = ['%.1e','%.1e']
        
        #supported in TK/TLC 8.6
        self.XAngle             = [0,0]
        self.YAngle             = [0,0]
    
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
                                                             
                                                             fill  = self.Color[0],
                                                             width = self.Thickness[0],
                                                             tag = 'TopTop'))
        #Draw the bottom part
        if self.Type[1]:
            self.AxesAdresses.append(self.Canvas.create_line((self.PaddingOut[0])*self.Canvas.Drawer.wScaleFactor,
                                                             
                                                             (1.0-self.PaddingOut[1])*self.Canvas.Drawer.hScaleFactor,
                                                             
                                                             (1.0-self.PaddingOut[2])*self.Canvas.Drawer.wScaleFactor,
                                                             
                                                             (1.0-self.PaddingOut[1])*self.Canvas.Drawer.hScaleFactor,
                                                             
                                                             fill  = self.Color[1],
                                                             width = self.Thickness[1],
                                                             tag = 'TopTop'))
        #Draw the right part
        if self.Type[2]:
            self.AxesAdresses.append(self.Canvas.create_line((1.0-self.PaddingOut[2])*self.Canvas.Drawer.wScaleFactor,
                                                             
                                                             (1.0-self.PaddingOut[1])*self.Canvas.Drawer.hScaleFactor,
                                                             
                                                             (1.0-self.PaddingOut[2])*self.Canvas.Drawer.wScaleFactor,
                                                             
                                                             (self.PaddingOut[3])*self.Canvas.Drawer.hScaleFactor,
                                                             
                                                             fill  = self.Color[2],
                                                             width = self.Thickness[2],
                                                             tag = 'TopTop'))
        #Draw the top part
        if self.Type[3]:
            self.AxesAdresses.append(self.Canvas.create_line((1.0-self.PaddingOut[2])*self.Canvas.Drawer.wScaleFactor,
                                                             
                                                             (self.PaddingOut[3])*self.Canvas.Drawer.hScaleFactor,
                                                             
                                                             (self.PaddingOut[0])*self.Canvas.Drawer.wScaleFactor,
                                                             
                                                             (self.PaddingOut[3])*self.Canvas.Drawer.hScaleFactor,
                                                             
                                                             fill  = self.Color[3],
                                                             width = self.Thickness[3],
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
            
                '''
                #############################################
                #############################################
                ###### Set the travel to minimum
                #############################################
                #############################################
                '''
                
                ########################
                ########################
                #logical variable
                
                #location variable
                bellow  = True
                
                #index
                i       = 0
                
                #intialising the sign
                Sign_0  = 1
                
                #check the sign of advance
                if Min < 0:
                
                    Sign_0 = -1
                
                ########################
                #find min index
                while bellow:
                
                    #advance
                    if i * abs(Spacing) < Sign_0 * Min :
                
                        #move forward
                        i += 1
                    
                    #retrieve and break
                    else:
                        
                        #set the lower index
                        Low_index = i
                        
                        #break the loop
                        bellow = False
            
                '''
                #############################################
                #############################################
                ###### Set the travel to maximum
                #############################################
                #############################################
                '''
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
                
                '''
                #############################################
                #############################################
                ###### Create the ticks
                #############################################
                #############################################
                '''

                ########################
                #we go from negative to positive
                if Sign_0 < 0 and Sign_1 > 0:
                    
                    #build tick positions
                    for i in range(1,Low_index):
                        
                        #Create array
                        TickCoords.append(i * Sign_0 * abs(Spacing))
  
                    #build tick positions
                    for i in range(0,High_index):
                
                        #Create array
                        TickCoords.append(i * Sign_1 * abs(Spacing))
                      
                ########################
                #we stay positive
                elif Sign_0 > 0 and Sign_1 > 0:
                
                    #build tick positions
                    for i in range(Low_index,High_index):
                
                        #Create array
                        TickCoords.append(i*abs(Spacing))
                
                ########################
                #we stay negative
                elif Sign_0 < 0 and Sign_1 < 0:
                
                    #build tick positions
                    for i in range(High_index,Low_index,):
                
                        #Create array
                        TickCoords.append(-i*abs(Spacing))

                ########################
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

    def GrabTextAsImage(self,widget_Tag):
        
        '''
        ######################################################
        It was found very difficult intalling tk/tcl 8.6 on 
        windows therefore a more drastic approach is used
        to rotate the ticks.
        
        We are usign a converter to image format from text and
        then replacing the item on the canvas...
        
        
        ######################################################
        '''
        
        #grab item elements
        print 'this is the Tag: ',widget_Tag
        print 'This is the bbox ',self.Canvas.bbox(widget_Tag)
        
        BBox = self.Canvas.bbox(widget_Tag)
      
        XPos_1 = self.Canvas.winfo_rootx()+BBox[0]-20
        YPos_1 = self.Canvas.winfo_rooty()+BBox[1]-20
     
        XPos_2 = self.Canvas.winfo_rootx()+BBox[2]
        YPos_2 = self.Canvas.winfo_rooty()+BBox[3]
        
        print 'This is what i came up with: ',(XPos_1,YPos_1,XPos_2,YPos_2)
        
        #ImageGrab.grab().crop((XPos_1,YPos_1,XPos_2,YPos_2)).save('Hello.png')

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
            
            if self.isXSci[0]:
            
                Text = self.XSciPrecision[0] % self.XTicksCoord[i]
            
            else:
            
                Text = str(round(self.XTicksCoord[i],self.XLabelRounding))
            
            if TkVersion > 8.5:
            
                self.XLabelAdresses.append(self.Canvas.create_text(((self.XTicksCoord[i]-self.Canvas.Drawer.BoundingBoxOffset[0])*self.Canvas.Drawer.BoundingBoxFactor[0]
                                                                   +self.PaddingIn[0]+self.PaddingOut[0])*self.Canvas.Drawer.wScaleFactor,    #X0 point of the Tick
                                                                   (1.0-self.PaddingOut[1]+self.XLabelOffset[0])*self.Canvas.Drawer.hScaleFactor, #Y0 point of the Tick
                                                                   fill     = self.XLabelColor[0],
                                                                   font     = self.XLabelSize[0],
                                                                   text     = Text,
                                                                   tag      = 'Top',
                                                                   angle    = self.XAngle[0]))
            
            else:

                self.XLabelAdresses.append(self.Canvas.create_text(((self.XTicksCoord[i]-self.Canvas.Drawer.BoundingBoxOffset[0])*self.Canvas.Drawer.BoundingBoxFactor[0]
                                                                   +self.PaddingIn[0]+self.PaddingOut[0])*self.Canvas.Drawer.wScaleFactor,    #X0 point of the Tick
                                                                   (1.0-self.PaddingOut[1]+self.XLabelOffset[0])*self.Canvas.Drawer.hScaleFactor, #Y0 point of the Tick
                                                                   fill     = self.XLabelColor[0],
                                                                   font     = self.XLabelSize[0],
                                                                   text     = Text,
                                                                   tag      = 'Top'))
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
            
            if self.isXSci[1]:
            
                Text = self.XSciPrecision[1] % self.XTicksCoord[i]
            
            else:
            
                Text = str(round(self.XTicksCoord[i],self.XLabelRounding))
            
            if TkVersion > 8.5:
                
                self.XLabelAdresses.append(self.Canvas.create_text(((self.XTicksCoord[i]-self.Canvas.Drawer.BoundingBoxOffset[0])*self.Canvas.Drawer.BoundingBoxFactor[0]
                                                                   +self.PaddingIn[0]+self.PaddingOut[0])*self.Canvas.Drawer.wScaleFactor,    #X0 point of the Tick
                                                                   
                                                                   (self.PaddingOut[3]-self.XLabelOffset[1])*self.Canvas.Drawer.hScaleFactor,    #Y0 point of the Tick
                                                                   
                                                                   fill  = self.XLabelColor[1],
                                                                   font = self.XLabelSize[1],
                                                                   text = Text,
                                                                   tag = 'Top',
                                                                   angle = self.XAngle[1]))
                #self.GrabTextAsImage(self.XLabelAdresses[-1])
            else:

                #print 'Tk/Tcl is still not version 8.6'
            
                self.XLabelAdresses.append(self.Canvas.create_text(((self.XTicksCoord[i]-self.Canvas.Drawer.BoundingBoxOffset[0])*self.Canvas.Drawer.BoundingBoxFactor[0]
                                                                   +self.PaddingIn[0]+self.PaddingOut[0])*self.Canvas.Drawer.wScaleFactor,    #X0 point of the Tick
                                                                   
                                                                   (self.PaddingOut[3]-self.XLabelOffset[1])*self.Canvas.Drawer.hScaleFactor,    #Y0 point of the Tick
                                                                   
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
            
            if self.isYSci[0]:
            
                Text = self.YSciPrecision[0] % self.YTicksCoord[-1-i]
            
            else:
            
                Text = str(round(self.YTicksCoord[-1-i],self.YLabelRounding))
            
            
            if TkVersion > 8.5:
                self.YLabelAdresses.append(self.Canvas.create_text((self.PaddingOut[0]-self.YLabelOffset[0])*self.Canvas.Drawer.wScaleFactor,     #X0 point of the Tick
                                                                   
                                                                   ((self.YTicksCoord[i]-self.Canvas.Drawer.BoundingBoxOffset[1])*self.Canvas.Drawer.BoundingBoxFactor[1]
                                                                   +self.PaddingIn[3]+self.PaddingOut[3])*self.Canvas.Drawer.hScaleFactor,    #Y0 point of the Tick
                                                                   
                                                                   fill  = self.YLabelColor[0],
                                                                   font = self.YLabelSize[0],
                                                                   text = Text,
                                                                   tag = 'Top',
                                                                   angle = self.YAngle[0]))

            else:

                print 'Tk/Tcl is still not version 8.6'
                
                self.YLabelAdresses.append(self.Canvas.create_text((self.PaddingOut[0]-self.YLabelOffset[0])*self.Canvas.Drawer.wScaleFactor,     #X0 point of the Tick
                                                                   
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
            
            if self.isYSci[1]:
            
                Text = self.YSciPrecision[1] % self.YTicksCoord[i]
            
            else:
            
                Text = str(round(self.YTicksCoord[i],self.YLabelRounding))
            
            if TkVersion > 8.5:
            
                self.YLabelAdresses.append(self.Canvas.create_text((1-self.PaddingOut[2]+self.YLabelOffset[1])*self.Canvas.Drawer.wScaleFactor,     #X0 point of the Tick
                                                                   
                                                                   ((1-(self.YTicksCoord[i]-self.Canvas.Drawer.BoundingBoxOffset[1])
                                                                     *self.Canvas.Drawer.BoundingBoxFactor[1]
                                                                     -self.Canvas.Drawer.Axes.PaddingIn[1]-self.Canvas.Drawer.Axes.PaddingOut[1])
                                                                    *self.Canvas.Drawer.hScaleFactor
                                                                    ),#changes
                                                                   
                                                                   fill  = self.YLabelColor[1],
                                                                   font = self.YLabelSize[1],
                                                                   text = Text,
                                                                   tag = 'Top',
                                                                   angle = self.YAngle[1]))
            
            else:

                print 'Tk/Tcl is still not version 8.6'
                
                self.YLabelAdresses.append(self.Canvas.create_text((1-self.PaddingOut[2]+self.YLabelOffset[1])*self.Canvas.Drawer.wScaleFactor,     #X0 point of the Tick
                                                                   
                                                                   ((1-(self.YTicksCoord[i]-self.Canvas.Drawer.BoundingBoxOffset[1])
                                                                     *self.Canvas.Drawer.BoundingBoxFactor[1]
                                                                     -self.Canvas.Drawer.Axes.PaddingIn[1]-self.Canvas.Drawer.Axes.PaddingOut[1])
                                                                    *self.Canvas.Drawer.hScaleFactor
                                                                    ),#changes
                                                                   
                                                                   fill  = self.YLabelColor[1],
                                                                   font = self.YLabelSize[1],
                                                                   text = Text,
                                                                   tag = 'Top'))
            



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


