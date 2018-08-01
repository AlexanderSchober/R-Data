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

class SettingsClass:
    
    '''
    ########################################################################
    This settings class is a window creator on standbye. it will launch when
    the call is made
    ########################################################################
    '''
    
    def __init__(self,Parent,MultiPlotCanvas):

        #store local
        self.Parent = Parent
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
        self.WindowFrame = SettingWindow(self.Parent,
                                         self.MultiPlotCanvas,
                                         self.frame,
                                         self)
        
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
    
    def __init__(self,Parent,MultiPlotCanvas,frame,ParentClass):

        #store local
        self.Parent             = Parent
        self.MultiPlotCanvas    = MultiPlotCanvas
        self.ParentClass        = ParentClass
    
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

        self.ParentClass.on_closing()
            
            
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
        #options['Parent'] = Window
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
        
        self.Invert = IntVar()
        self.Invert.set(0)
        
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
                                     
        self.PoisitionMatrix.append([ttk.Checkbutton(Target,
                                                     variable = self.Invert,
                                                     text = 'Invert X and Y'),
                                     3+self.RowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,2])
            
            
        self.PoisitionMatrix.append([ttk.Button(Target,
                                                text = 'Save Image',
                                                command = self.SaveImage),
                                     4+self.RowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
                                     
        self.PoisitionMatrix.append([ttk.Button(Target,
                                                text = 'Save Data',
                                                command = self.SaveData),
                                     4+self.RowOffset,
                                     1+self.ColumnOffset,
                                     E+W,1,1])
        
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
        This routine will output the current plot as 
        an image file
        ######################################################
        '''
    
        #send it out to the appropriate method
        self.Object.SaveImage(self.DirName,
                              FileName = os.path.join(self.Path,self.NameEntry.get()+'.eps'))
    
    def SaveData(self):
        '''
        ######################################################
        This function tries to save the presently represented
        data as a text file...
        ######################################################
        '''
    
        #send it out to the appropriate method
        self.Object.SaveText(self.DirName,
                             FileName = os.path.join(self.Path,self.NameEntry.get()+'.eps'),
                             Invert = self.Invert.get())
    
    def SelectDir(self):
        '''
        ######################################################
        This selects the directoy string
        ######################################################
        '''
        #ask
        self.DirName =  tkFileDialog.askdirectory(**self.dir_opt)
    
        #set
        self.DirLabel.configure(text = self.DirName)
    
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
                                                  width = 5)
                                                  
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
                                                 width = 5)
                                                 
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
        
        self.ColumnWeight       = [1,0,0,0,0,0,0,1]
        
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
                                                   width = 5)
                                                 
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
                                               text = 'Angle',
                                               anchor = CENTER),
                                     11+self.RowOffset,
                                     5+self.ColumnOffset,
                                     E+W,1,1])
           
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Offset',
                                               anchor = CENTER),
                                     11+self.RowOffset,
                                     6+self.ColumnOffset,
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
                                          width = 5)
                                          
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
                                          width = 8)
                                          
            self.PoisitionMatrix.append([self.FontEntry[i],
                                         12+i+self.RowOffset,
                                         4+self.ColumnOffset,
                                         E+W,1,1])

        ################################
        #Put font and size entry fields
        self.AngleEntry   = [None]*4
        
        for i in range(0,len(self.AngleEntry)):
        
        
            #create the entry
            self.AngleEntry[i] = ttk.Entry(Target,
                                          width = 3)
                                          
            self.PoisitionMatrix.append([self.AngleEntry[i],
                                         12+i+self.RowOffset,
                                         5+self.ColumnOffset,
                                         E+W,1,1])
        
        ################################
        #Put font and size entry fields
        self.OffsetEntry   = [None]*4
        
        for i in range(0,len(self.AngleEntry)):
        
        
            #create the entry
            self.OffsetEntry[i] = ttk.Entry(Target,
                                          width = 3)
                                          
            self.PoisitionMatrix.append([self.OffsetEntry[i],
                                         12+i+self.RowOffset,
                                         6+self.ColumnOffset,
                                         E+W,1,1])
        
        ################################
        #Build the scientific entry fields
        self.ScientificOnOff        = [None]*4
        self.ScientificOnOffVal     = [IntVar(),IntVar(),IntVar(),IntVar()]
        self.ScientificPrecision    = [None]*4
        
        for i in range(0,len(self.ScientificOnOff)):
        
        
            #create the entry
            self.ScientificOnOff[i] = ttk.Checkbutton(Target,
                                                      variable = self.ScientificOnOffVal[i])
                                                 
            self.PoisitionMatrix.append([self.ScientificOnOff[i],
                                        18+i+self.RowOffset+self.TicksRowOffset,
                                        1+self.ColumnOffset,
                                        E+W,1,1])
        
            #create the entry
            self.ScientificPrecision[i] = ttk.Entry(Target,
                                                    width = 5)
                                             
            self.PoisitionMatrix.append([self.ScientificPrecision[i],
                                         18+i+self.RowOffset+self.TicksRowOffset,
                                         3+self.ColumnOffset,
                                         E+W,1,1])
        
        ##############################
        #Toggle header
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = '',
                                               anchor = CENTER),
                                     17+self.RowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Scientific',
                                               anchor = W,
                                               font = tkFont.Font(weight = 'bold',
                                                                  underline = 0)),
                                     17+self.RowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'On/Off',
                                               anchor = CENTER),
                                     17+self.RowOffset,
                                     1+self.ColumnOffset,
                                     E+W,1,2])
                                    
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Precision',
                                               anchor = CENTER),
                                     17+self.RowOffset,
                                     3+self.ColumnOffset,
                                     E+W,1,1])
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Bot X',
                                               anchor = CENTER),
                                     18+self.RowOffset+self.TicksRowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
                                    
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Top X',
                                               anchor = CENTER),
                                     19+self.RowOffset+self.TicksRowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
                                    
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Left Y',
                                               anchor = CENTER),
                                     20+self.RowOffset+self.TicksRowOffset,
                                     0+self.ColumnOffset,
                                     E+W,1,1])
                                    
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Right Y',
                                               anchor = CENTER),
                                     21+self.RowOffset+self.TicksRowOffset,
                                     0+self.ColumnOffset,
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
        
            Target.grid_columnconfigure(i,weight = self.ColumnWeight[i])
        
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
        
        #####
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
        
        #####
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
        
        #####
        #delete entry content
        self.AngleEntry[0].delete(0,END)
        
        #fill entry content
        self.AngleEntry[0].insert(0,str(Object.Axes.YAngle[0]))

        #delete entry content
        self.AngleEntry[1].delete(0,END)

        #fill entry content
        self.AngleEntry[1].insert(0,str(Object.Axes.YAngle[1]))
          
        #delete entry content
        self.AngleEntry[2].delete(0,END)

        #fill entry content
        self.AngleEntry[2].insert(0,str(Object.Axes.XAngle[1]))

        #delete entry content
        self.AngleEntry[3].delete(0,END)

        #fill entry content
        self.AngleEntry[3].insert(0,str(Object.Axes.XAngle[0]))
        
        #####
        #delete entry content
        self.OffsetEntry[0].delete(0,END)
        
        #fill entry content
        self.OffsetEntry[0].insert(0,str(Object.Axes.XLabelOffset[0]))

        #delete entry content
        self.OffsetEntry[1].delete(0,END)

        #fill entry content
        self.OffsetEntry[1].insert(0,str(Object.Axes.XLabelOffset[1]))
          
        #delete entry content
        self.OffsetEntry[2].delete(0,END)

        #fill entry content
        self.OffsetEntry[2].insert(0,str(Object.Axes.YLabelOffset[1]))

        #delete entry content
        self.OffsetEntry[3].delete(0,END)

        #fill entry content
        self.OffsetEntry[3].insert(0,str(Object.Axes.YLabelOffset[0]))
        
        ##############################
        #Set scientific on off
        if Object.Axes.isXSci[0]:
            
            #set var
            self.ScientificOnOffVal[0].set(1)
            
            #set button state
            self.ScientificOnOff[0].state(['selected'])

        else:
            
            #set var
            self.ScientificOnOffVal[0].set(0)
            
            #set button state
            self.ScientificOnOff[0].state(['!selected'])
        
        #####
        if Object.Axes.isXSci[1]:
            
            #set var
            self.ScientificOnOffVal[1].set(1)
            
            #set button state
            self.ScientificOnOff[1].state(['selected'])

        else:
            
            #set var
            self.ScientificOnOffVal[1].set(0)
            
            #set button state
            self.ScientificOnOff[1].state(['!selected'])

        #####
        if Object.Axes.isYSci[0]:
            
            #set var
            self.ScientificOnOffVal[2].set(1)
            
            #set button state
            self.ScientificOnOff[2].state(['selected'])

        else:
            
            #set var
            self.ScientificOnOffVal[2].set(0)
            
            #set button state
            self.ScientificOnOff[2].state(['!selected'])
        
        #####
        if Object.Axes.isYSci[1]:
            
            #set var
            self.ScientificOnOffVal[3].set(1)
            
            #set button state
            self.ScientificOnOff[3].state(['selected'])

        else:
            
            #set var
            self.ScientificOnOffVal[3].set(0)
            
            #set button state
            self.ScientificOnOff[3].state(['!selected'])
                
        ##############################
        #Grab scientific precision
        
        #delete entry content
        self.ScientificPrecision[0].delete(0,END)

        #fill entry content
        self.ScientificPrecision[0].insert(0,str(Object.Axes.XSciPrecision[0].split('%.')[1].split('e')[0]))

        #delete entry content
        self.ScientificPrecision[1].delete(0,END)

        #fill entry content
        self.ScientificPrecision[1].insert(0,str(Object.Axes.XSciPrecision[1].split('%.')[1].split('e')[0]))

        #delete entry content
        self.ScientificPrecision[2].delete(0,END)

        #fill entry content
        self.ScientificPrecision[2].insert(0,str(Object.Axes.YSciPrecision[0].split('%.')[1].split('e')[0]))
            
        #delete entry content
        self.ScientificPrecision[3].delete(0,END)

        #fill entry content
        self.ScientificPrecision[3].insert(0,str(Object.Axes.YSciPrecision[1].split('%.')[1].split('e')[0]))

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
        Object.Axes.XLabelSize[1] = (self.FontEntry[2].get(),self.SizeEntry[2].get())

        #fill entry content
        Object.Axes.XLabelSize[0] = (self.FontEntry[3].get(),self.SizeEntry[3].get())

        Object.Axes.YLabelColor[1] = self.LabelColor[0].GetColor()
        Object.Axes.YLabelColor[0] = self.LabelColor[1].GetColor()
        Object.Axes.XLabelColor[1] = self.LabelColor[2].GetColor()
        Object.Axes.XLabelColor[0] = self.LabelColor[3].GetColor()


        #fill entry content
        Object.Axes.XAngle = [float(self.AngleEntry[3].get()),
                              float(self.AngleEntry[2].get())]

        #fill entry content
        Object.Axes.YAngle = [float(self.AngleEntry[0].get()),
                              float(self.AngleEntry[1].get())]

        #fill entry content
        Object.Axes.XLabelOffset = [float(self.OffsetEntry[3].get()),
                                    float(self.OffsetEntry[2].get())]

        #fill entry content
        Object.Axes.YLabelOffset = [float(self.OffsetEntry[0].get()),
                                    float(self.OffsetEntry[1].get())]
        
        ##############################
        #Set scientific on off
        ##############################
        #Set the logical variables for the ticks
        if self.ScientificOnOffVal[0].get() == 1:
            
            #set var
            Object.Axes.isXSci[0] = True

        else:
            
            #set var
            Object.Axes.isXSci[0] = False

        if self.ScientificOnOffVal[1].get() == 1:
            
            #set var
            Object.Axes.isXSci[1] = True

        else:
            
            #set var
            Object.Axes.isXSci[1] = False

        if self.ScientificOnOffVal[2].get() == 1:
            
            #set var
            Object.Axes.isYSci[0] = True

        else:
            
            #set var
            Object.Axes.isYSci[0] = False

        if self.ScientificOnOffVal[3].get() == 1:
            
            #set var
            Object.Axes.isYSci[1] = True

        else:
            
            #set var
            Object.Axes.isYSci[1] = False
        
        ##############################
        #Grab scientific precision
        
        Object.Axes.XSciPrecision[0]        = '%.'+self.ScientificPrecision[0].get()+'e'
        Object.Axes.XSciPrecision[1]        = '%.'+self.ScientificPrecision[1].get()+'e'

        Object.Axes.YSciPrecision[0]        = '%.'+self.ScientificPrecision[2].get()+'e'
        Object.Axes.YSciPrecision[1]        = '%.'+self.ScientificPrecision[3].get()+'e'


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
                                             width = 2)
                                                 
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
                                             width = 2)
                                                 
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
                                width = 2)
                                                 
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
                                width = 2)
                                                 
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
                                width = 2)
                                                 
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
    
    def __init__(self, Parent,width = 10,height = 10, color = None,**kwargs):

        Canvas.__init__(self,
                        Parent,
                        width = 10,
                        height = 10,
                        background = 'black',
                        **kwargs)

        #set parameters
        self.Verbose    = True
        self.Parent = Parent
        
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
