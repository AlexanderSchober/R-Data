# -*- coding: utf-8 -*-
'''
######################################################
################Simple Plot Method####################
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

class InteractivePlotClass:
    
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

        try:
            
            #draw the object
            self.IdentifierList.append(Target.create_line(DrawList,
                                                          fill     =   self.Color,
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
                                                              fill = self.Color,
                                                              tag = 'Top'))

        #set the state
        self.CanvasObject   = True
