# -*- coding: utf-8 -*-

#-INFO-
#-Name-Cascade-
#-Version-0.1.0-
#-Date-11_May_2016-
#-Author-Alexander_Schober-
#-INFO-

print 'Loading Cascade dependencies...'

"""
###########################################################################
###########################################################################

     o---------------------------------------------------------o
     |    ##       ###              ..O,.  . .=OZ              |
     |    ##       ###            ?=?...   ?   ..Z~            |
     |    ##       ###         .?.O.       . .,. .Z.  .        |
     |    ##       ###        . .?. . ?Z    ...O7.ZZ. =        |
     |    ##       ###       . ,?:.:        . .  . Z. .?       |
     |    ##       ###       ..?Z         .ZZZZZ+ :Z:ZZZ.      |
     |    ##       ###      ~ .??     .ZZZ. .... ..Z+  ZI?     |
     |    ##       ###      ?$.?? ..OO????+,. .~???8?: .ZZ     |
     |    ######   ###      :..??OO+..           .ZZ?.?7 Z     |
     |    ######   ###     Z? 8O                 ZZ. ??O=      |
     |                     .Z?8??                ZZ..7O. ?I    |
     |    ###### #######   .ZO.?7:              =Z7?ZO.  ?Z    |
     |    ##  ##   ###     .O.. 77??~. .     ..$OOO?.?. .Z.    |
     |    ##       ###      Z7  .?????????????OOO... ?.?,Z     |
     |    ##       ###       ZO. ??   ..~?OZ.ZZ7  . .7.,Z.     |
     |    ######   ###       .Z7.?OOI:..  .$ZZ...+? .:ZZ.      |
     |        ##   ###       . ZZ$.??..~?OOZ.....   OZZ        |
     |    ##  ##   ###           ZZZOOOZZ.    . .ZZZZ          |
     |    ##  ##   ###            .ZZZOOZZZZZZZZZZZ..          |
     |    ######   ###                .?OOOZZZ+ :?             |
     o---------------------------------------------------------o

###########################################################################
###########################################################################

This file contains the PCA related section. 
the upgrade to version 0.0.4 changes the entire matplotlib
framework towards tkinter framework to support a friendlier
user interface. This means that the user is not confronted
anymore with terminal like input parameters.

Note that some function of version 0.0.3 might be temporary
ommited and readded later. This is because of the hard work
it takes to porting the entire system (And I am alone).

The same file will now (version 0.0.4) include the Cascade analysis methods
and windows to allow sharing of resources within the same file

###########################################################################
Created on Mon May 11 10:27:35 2015

@author: Alexander Michael Schober Turgut
Luxembourg Institute of Science and Technology

###########################################################################

"""


"""
##################################################
Default python lbrary imports
##################################################
"""

#######################################
#basic imports

#system import
import sys

#operating system variables
import os

#numpyy mathematical import
import numpy

#######################################
#advanced imports

#function manipulation routines
from functools import *


"""
##################################################
These Interface imports. The whole application is 
based on the Tkinter framework which interfaces 
Tk/Tcl cross platform elements with Python
##################################################
"""

#########################
#import Tk/Tcl interface to Python
if sys.version_info[0] < 3:
    
    import Tkinter as tk

else:
    
    import tkinter as tk

#Tk variable objects
import Tkconstants

#dialog for import saving
import tkFileDialog

#enhanced tkinter layout
import ttk

#import the font mofifer
import tkFont

#Special textbox arrangement
import ScrolledText

#########################
#import image management routines
from PIL import Image, ImageTk


'''
###########################################################################
These are the custome imports
###########################################################################
'''

#File and system management routines
import Utility_File     as File

#General Utility
import Utility_Main     as Utility

#import the main file
import Main

#The terminal viual manager
import Utility_Out      as VisOut

#Simpleplot import
import SimplePlot.SimplePlot as SimplePlot



class DrawCascade:

    '''
    ###########################################################################
    This routine will launch the main window which is a child passed on by the
    parent on launch.
    
    
    This is used to analyse the components from the measurement series.
    ###########################################################################
    '''
    def __init__(self,Data,root):
        
        #Check if the Cascade class exists already in Data
        if not Data.isContour:
        
            #if not load the Cascade
            Data.LoadContour()
    
        VisOut.TextBox(Title = 'Action', Text = Data.Contour.InitiateContour(), state = 1)
        
        #set master
        self.master = root
        
        self.CascadeWindow = tk.Toplevel(self.master)
        
        #binf the methofd to a destroy
        self.CascadeWindow.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        #lanuch the window class dependency
        app = CascadeWindow(self.CascadeWindow ,Data)

    def on_closing(self):
        
        print 'Destroy...'
        
        self.CascadeWindow.destroy()

        del self.CascadeWindow



class CascadeWindow():
    
    
    '''
    ########################################################
    The main window class will group all the interesting
    parameters and stay accessible to all children windows
    As a result it will hold all the calculation aspects
    and initiate all the visual parts
    
    the plot construction will be done in a child function
    ########################################################
    '''
    
    def __init__(self, root, DataClass):
        '''
        ######################################################################
        Initiating class. this is used to set the framen and scroll bar and
        the basic layout. The ned fucntion calls populate which should then 
        create the buttons and input fields
        ######################################################################
        '''
        
        #Dataclass from the program becomes locally linked
        self.DataClass = DataClass
        
        self.Fit = None
        self.BaseActive = tk.IntVar()
        self.PathofInterest = DataClass.Info.Root
        self.padding = '5p'
        
        self.file_opt = options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        options['initialdir'] = self.PathofInterest
        options['initialfile'] = 'myfile.txt'
        options['parent'] = root
        options['title'] = 'This is a title'
        
        self.dir_opt = options = {}
        options['initialdir'] = self.PathofInterest
        options['mustexist'] = False
        options['parent'] = root
        options['title'] = 'This is a title'
        
        #frame creation
        self.master = root
        
        self.master.title("Cascade Interface ("+self.DataClass.Info.GetInfoVal('Name')+")")
        self.master.resizable(width=True, height=True)
        
       
        
        #Load the label dependencies
        self.frame  = ttk.Frame(self.master, relief = 'sunken' , padding = self.padding)
        self.frame0 = ttk.Frame(self.master, relief = 'sunken' , padding = self.padding)
        
        #populate
        self.populate(root)
        
        #Pack the frame
        self.frame.grid(row = 0, column = 1, sticky = tk.E+tk.W+tk.N+tk.S)
        self.frame0.grid(row = 0, column = 0, sticky = tk.E+tk.W+tk.N+tk.S)
        
        #give weight...
        self.master.grid_columnconfigure(1, weight = 1)
        self.master.grid_rowconfigure(   0, weight = 1)
        
        self.frame.grid_rowconfigure(0, weight = 1)
        self.frame.grid_columnconfigure(0, weight = 1)
        
        #save as buffer
        self.DataClass.Contour.ZPlotBuffer = numpy.copy(self.DataClass.Contour.ZPlot)
        self.DataClass.Contour.XPlotBuffer = numpy.copy(self.DataClass.Contour.XPlot)
        self.DataClass.Contour.YPlotBuffer = numpy.copy(self.DataClass.Contour.YPlot)

    
    def populate(self,root):
        
        '''
        ####################################################################################
        This function populate steh frame in order to process the button handling
        
        This will populate the main window of the instance and leave the rest free.
        ####################################################################################    
        '''
        #Placement variables
        VisOffset  = 1
        PCAOffset  = 0
        NMFOffset  = 6
        RowOffset   = 9
        RowLabels   = 12
        RowEntry    = 13
        
        #Set some depreciated variables that should be removed soon
        #Variables for the Lines Depreciated want to move this into the
        self.LineRange     = [0,0,0,0,0,'k',2]
        self.LineIdx       = [0,0,0,0]
        self.LineValues    = [0,0,0,0,0]
        self.LineWidth     = 1
        self.PickIdx       = [0,0]
                        
        #Boolean variables for plot
        self.PutLines      = False
        self.Manual        = False
        self.Navigator     = False
        self.Switch        = False
        self.ThreeDActive  = False
    
    
        #Variables for Cascade
        self.CPerform      = True
        self.CLineWidth    = 0
        self.CColorStr     = 'black'
        self.CNumber       = 0
        
        self.Perform       = False
        self.Number        = 0.1
        
        #Variables for Grid
        self.PutGrid       = False
        self.GridL         = 0.5
        self.GridCol       = 'white'
        
        
        #Ceate the figure
        self.CreateFigureSimplePlot()
        
        #Create the initial view range and fit range fields with labels
        self.PCALabels    = [None]*5
        self.PCABut       = [None]*10

        ############################
        ############################
        #Populate header Labelframe
        self.TopLabelFrame = ttk.Labelframe(self.frame0, text ='Selected:')
        self.TopLabelFrame.grid( row = 0 , column = 0, sticky = tk.E+tk.W)
        self.TopLabelFrame.grid_columnconfigure(0, weight = 1)
        
        self.PCALabels[1] = ttk.Label(self.TopLabelFrame, text = 'x = '        ,width = 8)
        self.PCALabels[2] = ttk.Label(self.TopLabelFrame, text = 'y = '        ,width = 8)
        
        self.PCALabels[1].grid( row = 1 , column = 0)
        self.PCALabels[2].grid( row = 2 , column = 0)
 
        ############################
        ############################
        #Populate Middle Labelframe
        self.MidLabelFrame = ttk.Labelframe(self.frame0, text ='Options:')
        self.MidLabelFrame.grid( row = 1 , column = 0, sticky = tk.E+tk.W)
        
        self.PCABut[0] = ttk.Button(self.MidLabelFrame, text = 'Navigator'    , style    = 'Toolbutton', command = self.NavigatorFun )
        self.PCABut[1] = ttk.Checkbutton(self.MidLabelFrame, text = 'Cascade'  )
        self.PCABut[2] = ttk.Checkbutton(self.MidLabelFrame, text = 'Grid'     )
        self.PCABut[3] = ttk.Checkbutton(self.MidLabelFrame, text = 'Ticks'    )
        self.PCABut[4] = ttk.Checkbutton(self.MidLabelFrame, text = 'Range'    )
        self.PCABut[5] = ttk.Checkbutton(self.MidLabelFrame, text = 'Color'    )
        
        self.PCABut[0].grid(    row = 1 , column = 0, sticky = tk.E+tk.W )
        self.PCABut[1].grid(    row = 3 , column = 0, sticky = tk.E+tk.W )#toggler
        self.PCABut[2].grid(    row = 5 , column = 0, sticky = tk.E+tk.W )#toggler
        self.PCABut[3].grid(    row = 7 , column = 0, sticky = tk.E+tk.W )#toggler
        self.PCABut[4].grid(    row = 9 , column = 0, sticky = tk.E+tk.W )#toggler
        self.PCABut[5].grid(    row = 11, column = 0, sticky = tk.E+tk.W )#toggler
        
        #create the frames here
        self.ToggleFrame = [None]*5
        
        self.ToggleFrame[0] = ttk.Frame(self.MidLabelFrame)
        self.ToggleFrame[1] = ttk.Frame(self.MidLabelFrame)
        self.ToggleFrame[2] = ttk.Frame(self.MidLabelFrame)
        self.ToggleFrame[3] = ttk.Frame(self.MidLabelFrame)
        self.ToggleFrame[4] = ttk.Frame(self.MidLabelFrame)
        
        #load the frame content here
        self.BuilderClass = [None]*5
        
        self.BuilderClass[0] = GridWindowClass(self.ToggleFrame[0],self.DataClass,self,'Cascade', isWindow = False )
        self.BuilderClass[1] = GridWindowClass(self.ToggleFrame[1],self.DataClass,self,'Grid'   , isWindow = False )
        self.BuilderClass[2] = GridWindowClass(self.ToggleFrame[2],self.DataClass,self,'Ticks'  , isWindow = False )
        self.BuilderClass[3] = RangeWindow(    self.ToggleFrame[3],self.DataClass,self,'Cascade', isWindow = False )
        self.BuilderClass[4] = ColorWindow(    self.ToggleFrame[4],self.DataClass,self          , isWindow = False )
        
        #Grid the frames
        self.ToggleFrame[0].grid(row = 4 , column = 0, sticky = tk.E+tk.W )
        self.ToggleFrame[1].grid(row = 6 , column = 0, sticky = tk.E+tk.W )
        self.ToggleFrame[2].grid(row = 8 , column = 0, sticky = tk.E+tk.W )
        self.ToggleFrame[3].grid(row = 10, column = 0, sticky = tk.E+tk.W )
        self.ToggleFrame[4].grid(row = 12, column = 0, sticky = tk.E+tk.W )
        
        #gather dimentions
        MaxWidth = numpy.max([self.ToggleFrame[i].winfo_width() for i in range(0, len(self.ToggleFrame))])
        
        for i in range(0, len(self.ToggleFrame)):
            
            self.ToggleFrame[i].grid_propagate(0)
        
        #and forget them
        self.ToggleFrame[0].grid_remove()
        self.ToggleFrame[1].grid_remove()
        self.ToggleFrame[2].grid_remove()
        self.ToggleFrame[3].grid_remove()
        
        self.frame0.grid_rowconfigure(22, weight = 1)
        self.MidLabelFrame.grid_columnconfigure(0, weight = 1)
        
        #create the buttons here
        self.CommandList = [partial(self.Cascade,0),
                            partial(self.Cascade,1),
                            partial(self.Cascade,2),
                            partial(self.Cascade,3)]
                            
        MainToggler = ToggledViewMode([self.PCABut[1],self.PCABut[2],self.PCABut[3],self.PCABut[4],self.PCABut[5]], self.Toggle, [0,1,2,3,4])
        
        ############################
        ############################
        #Populate Bottom Labelframe
        self.BotLabelFrame = ttk.Labelframe(self.frame0, text ='Save:')
        self.BotLabelFrame.grid( row = 2 , column = 0, sticky = tk.E+tk.W)
        self.BotLabelFrame.grid_columnconfigure(0, weight = 1)
        
        self.PCABut[6] = ttk.Button(self.BotLabelFrame, text = 'Baseline'     , style    = 'Toolbutton' , command = self.Spectra     )
        self.PCABut[7] = ttk.Button(self.BotLabelFrame, text = 'Refresh'      , style    = 'Toolbutton' , command = self.Refresh     )
        self.PCABut[8] = ttk.Button(self.BotLabelFrame, text = 'Selected'     , style    = 'Toolbutton' , command = self.SaveSelect  )
        self.PCABut[9] = ttk.Button(self.BotLabelFrame, text = 'Figure'       , style    = 'Toolbutton' , command = self.SaveFig     )
        
        self.PCABut[6].grid(    row = 1, column = 0, sticky = tk.E+tk.W )
        self.PCABut[7].grid(    row = 2, column = 0, sticky = tk.E+tk.W )
        self.PCABut[8].grid(    row = 3, column = 0, sticky = tk.E+tk.W )
        self.PCABut[9].grid(    row = 4, column = 0, sticky = tk.E+tk.W )
        
        #Send out the drawer
        self.FigDraw()

    def CreateFigureSimplePlot(self):
    
    
        '''
        ####################################################################################
        This is the new plotting interface specially developerd for memory efficiency and
        interactivity
        
        SimplePlot
        ####################################################################################    
        '''
        ################################
        #set the figure frame
        self.FigFrame = ttk.Frame(self.frame)
        
        ################################
        #create the plot content
        mycanvas = SimplePlot.MultiPlotCanvas(self.FigFrame,
                                              grid     = [[True]],
                                              ratioX   = [1],
                                              ratioY   = [1],
                                              width    = 200,
                                              height   = 250,
                                              bg       = "white",
                                              NoTitle  = True,
                                              highlightthickness = 0)
        
        ################################
        #Define the subplot
        self.ax = mycanvas.GetSubPlot(0,0)
        Thickness = [2,2,2,2]
        
        ################################
        #initialise the Cascade plot
        self.ax.Axes.Type            = [False,True,False,False]
        self.ax.Axes.isYSci          = [False,False]
        self.ax.Axes.isXSci          = [False,False]
        
        self.ax.Axes.XTickSpacing         = 50
        self.ax.Axes.YTickSpacing         = 0.2
        self.ax.Axes.XTickType            = 1
        
        self.ax.Pointer.YSciPrecision = '%.2e'
        self.ax.Pointer.XSciPrecision = '%.2e'
        
        self.ax.Axes.TicksActiveGrid  = [False, True, False, False]
        self.ax.Axes.LabelsActiveGrid = [False, True, False, False]
        self.ax.Axes.PaddingOut       = [0.1, 0.05, 0.002, 0.002]
        
        self.ax.Pointer.Sticky = 1
        self.ax.Axes.Thickness = Thickness
        
        ################################
        #Launch the plot setup
        self.ax.DrawAllPlot()
        self.ax.Axes.DrawAxes()
        self.ax.Axes.PlaceAllLabels()
        self.ax.BindCursor()
        self.ax.Axes.PlaceGrids()
        self.ax.BindZoomer()
    
        ################################
        #describe the types
        self.ax.Live = 2
        
        #mount the frame
        self.FigFrame.grid(row = 0, column = 0, sticky = tk.E+tk.W+tk.N+tk.S)
 
    def Toggle(self, ID):
    
        for i in range(0, len(self.ToggleFrame)):
            
            self.ToggleFrame[i].grid_remove()

        self.ToggleFrame[ID].grid()

    
    def Spectra(self):
        
        '''
        ######################################################################
        View all spectra in a spectral analyser derived from the base remover
        for components
        ######################################################################
        '''
        #build the tk fit window dependencies
        self.BaseWindow = tk.Toplevel(self.master)
        
        #launch the fit window
        self.base = BaseWindowClass(self.BaseWindow,self.DataClass,self,'Cascade')
    
    def SaveSelect(self):
    
        '''
        ######################################################################
        Saves the current Selected Data to text files that can be fited
        afterwards in our special reader + fiting interface
        
        The file format will be like components as it is a similar 
        datatype
        ######################################################################
        '''
        Named = self.DataClass.Info.Root
        
        #preapre the writing
        Output = self.DataClass.HeadStr
        Output += Utility.Ret()+self.DataClass.HeadStrEx
        Output += Utility.Ret()+'Taken at '+str(self.LineRange[0])+' '+str(self.LineRange[1])+'from the raw data file'+Utility.Ret()
        
        #Get out the spectra
        FilePath = os.path.join(os.path.dirname(Named),self.DataClass.HeadStr+'_Spectra_'+str(self.LineRange[0])+' '+str(self.LineRange[1])+'.txt')
        Utility.WriteSingle2File(Output,self.XSidePlotY,self.ZSidePlotY,FilePath)
        
        #Get out the Score
        FilePath = os.path.join(os.path.dirname(Named),self.DataClass.HeadStr+'_Score_'+str(self.LineRange[0])+' '+str(self.LineRange[1])+'.txt')
        Utility.WriteSingle2File(Output,self.YSidePlotX,self.ZSidePlotX,FilePath)
    
        VisOut.TextBox(Title = 'Action', Text = 'User saved the spectra and score to :\n'+str(FilePath), state = 1)
    
    def SaveFig(self):
        '''
        ######################################################################
        This will save the currently displayed figure to a datafile
        ######################################################################
        '''
        if self.Navigator:
            Tail = self.DataClass.HeadStr+'_PostSignalProcessing_Pick_'+str(round(float(self.LineRange[0]),2))+'_'+str(round(float(self.LineRange[1]),2))+'.pdf'
        else:
            Tail = self.DataClass.HeadStr+'_PostSignalProcessing_Pick.pdf'
            
            
        #write the file
        Utility.WriteFig(self.DataClass,self.f,Tail)
            
        VisOut.TextBox(Title = 'Action', Text = 'User saved the layout to :\n'+str(Tail), state = 1)
            

    def ViewBuilder(self):
        '''
        ######################################################################
        obsolete function now all handled by the drawer
        ######################################################################
        '''
        #Send out the drawer
        self.FigDraw()

    def ResetFocus(self, event):
    
        self.canvas.figure.canvas._tkcanvas.focus_set()

    def FigDraw(self):
        
        
        '''
        ######################################################################
        This function will disconnect all the event handlers then redraw
        the frame accordingly then try to reset all event handlers
        with the new set of parameters
        ######################################################################
        '''
        
        self.Refreshax()
    
    
    def DeleteSubPlots(self):
    
            try:
                del self.ax
            except:
                pass
    

    
    
    def Refreshax(self):
        '''
        ######################################################################
        Refresh the main Cascade
        ######################################################################
        '''
        
        #delete all we had
        self.ax.Reset()

        #build the Cascade plot in ax
        self.Cascade = self.ax.AddCascade(#The Data input
                                          
                                          self.DataClass.Contour.XPlot.transpose().tolist(),
                                          self.DataClass.Contour.YPlot.tolist(),
                                          self.DataClass.Contour.ZPlot.transpose().tolist(),
                                          
                                          #Select the type
                                          Type = 'Straight',
                                              
                                          Stepping = self.Number,
                                          Name = 'Cascade')
        
        #finally zoom to rebuild all
        self.ax.Zoom()

    
    def NavigatorFun(self):
        
        '''
        ######################################################################
        Toggle the Navigator
        ######################################################################
        '''
        
        self.Navigator = not self.Navigator
        self.Switch = True

        self.ViewBuilder()
    
    def Cascade(self,Target):
        
        '''
        ######################################################################
        Seting the Cascades for furthe utilisation
        ######################################################################
        '''
        
        #Build infor window dependencies to root
        self.CWindow = tk.Toplevel(self.master)
        
        #lanuch the window class dependency
        self.app2 = GridWindowClass(self.CWindow,self.DataClass,self,Target)
    
    def Range(self):
        
        '''
        ######################################################################
        This will prompt the range select window, This will allow the user to
        specify the range he wants to use for the pca. Note that the same
        window will be used fir the NMF, but obviously stored elsewhere...
        ######################################################################
        '''
        #Build infor window dependencies to root
        self.RangeWindow = tk.Toplevel(self.master)
        
        #lanuch the window class dependency
        self.app3 = RangeWindow(self.RangeWindow,self.DataClass,self,'Cascade')
    
    def Color(self):
    
        '''
        ######################################################################
        two sliders window creation to adjust the coloring
        ######################################################################
        '''
        #Build infor window dependencies to root
        self.ColorWindow = tk.Toplevel(self.master)
        
        #lanuch the window class dependency
        self.app3 = ColorWindow(self.ColorWindow,self.DataClass,self)
    
    
    def Refresh(self):
        
        '''
        ######################################################################
        This function processes loaclly the PCA and then should call the 
        show instance of the visualisation protocol.
        ######################################################################
        '''
        self.ViewBuilder()
    


    def Info(self):
        
        '''
        ######################################################################
        On click of the Build method a new window will be spawned containing
        the current informations of the loaded sample file if they exist. 
        
        
        Note that anyway all files loaded into this fitting programm will
        have been processed beforehand. 
        
        We could think of adding a special feature before to allow for 
        automatic compilation and data class creation
        
        like FitWindow -File should create autamitcally the work....
        later maybe version 4
        
        ######################################################################
        '''
        
        #Build infor window dependencies to root
        self.InfoWindow = tk.Toplevel(self.master)
        
        #lanuch the window class dependency
        self.app2 = Main.InfoWindowClass(self.InfoWindow,self.DataClass)

        #output
        VisOut.TextBox(Title = 'Action', Text = 'Launching information Window', state = 1)

class RangeWindow:
    '''
    ######################################################################
    This wibdow is here to set calculation ranges of all parameters...
    ######################################################################
    '''
    
    def __init__(self,master,DataClass,Parent,Target, isWindow = True):
        
        #link the DataClass
        self.DataClass = DataClass
        self.Parent    = Parent
        self.Target    = Target
        self.isWindow  = isWindow
        self.master    = master
        
        #set master
        if self.isWindow:
            
            self.master.title("Select Range for "+Target)
            self.master.configure(background = 'black')
            self.master.resizable(width=True, height=True)
        
        #initialise the  arrays
        self.RangeLabels = [None]*5
        self.RangeEntry  = [None]*8
        self.RangeBut    = [None]*3
        
        
        self.frame = ttk.Frame(self.master, relief = 'sunken', padding = '15p')
        
        #prepare labels
        self.RangeLabels[0] = ttk.Label(self.frame, text = 'Enter limits:')
        self.RangeLabels[1] = ttk.Label(self.frame, text = 'Wavenumber' ,width = 8)
        self.RangeLabels[2] = ttk.Label(self.frame, text = 'Z Limits'   ,width = 8)
        self.RangeLabels[3] = ttk.Label(self.frame, text = 'X Limits'   ,width = 8)
        self.RangeLabels[4] = ttk.Label(self.frame, text = 'Y Limits'   ,width = 8)
        
        self.RangeLabels[0].grid(row = 0, column = 0, columnspan = 2, sticky = tk.E+tk.W)
        self.RangeLabels[1].grid(row = 1, column = 0, columnspan = 2, sticky = tk.E+tk.W)
        self.RangeLabels[2].grid(row = 3, column = 0, columnspan = 2, sticky = tk.E+tk.W)
        self.RangeLabels[3].grid(row = 5, column = 0, columnspan = 2, sticky = tk.E+tk.W)
        self.RangeLabels[4].grid(row = 7, column = 0, columnspan = 2, sticky = tk.E+tk.W)
        
        #prepare entry fields
        self.RangeEntry[0] = ttk.Entry(self.frame,width = 8)
        self.RangeEntry[1] = ttk.Entry(self.frame,width = 8)
        self.RangeEntry[2] = ttk.Entry(self.frame,width = 8)
        self.RangeEntry[3] = ttk.Entry(self.frame,width = 8)
        self.RangeEntry[4] = ttk.Entry(self.frame,width = 8)
        self.RangeEntry[5] = ttk.Entry(self.frame,width = 8)
        self.RangeEntry[6] = ttk.Entry(self.frame,width = 8)
        self.RangeEntry[7] = ttk.Entry(self.frame,width = 8)
        
        self.RangeEntry[0].grid(row = 2, column = 0, sticky = tk.E+tk.W)
        self.RangeEntry[1].grid(row = 2, column = 1, sticky = tk.E+tk.W)
        self.RangeEntry[2].grid(row = 4, column = 0, sticky = tk.E+tk.W)
        self.RangeEntry[3].grid(row = 4, column = 1, sticky = tk.E+tk.W)
        self.RangeEntry[4].grid(row = 6, column = 0, sticky = tk.E+tk.W)
        self.RangeEntry[5].grid(row = 6, column = 1, sticky = tk.E+tk.W)
        self.RangeEntry[6].grid(row = 8, column = 0, sticky = tk.E+tk.W)
        self.RangeEntry[7].grid(row = 8, column = 1, sticky = tk.E+tk.W)

        #prepare buttons
        self.RangeBut[0] = ttk.Button(self.frame, text = 'Apply',  width = 5, command = self.Apply)
        self.RangeBut[1] = ttk.Button(self.frame, text = 'Reset',  width = 5, command = self.Reset)
        
        
        self.RangeBut[0].grid(row = 9, column = 0, sticky = tk.E+tk.W)
        self.RangeBut[1].grid(row = 9, column = 1, sticky = tk.E+tk.W)
        
        
        self.frame.grid_columnconfigure(0, weight = 1)
        self.frame.grid_columnconfigure(1, weight = 1)
        
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        #Set the current range values (grab them)
        
                #Set the current range values (grab them)
        if self.Target == 'PCA':
            CropTarget = self.DataClass.PCA
            
        if self.Target == 'NMF':
            CropTarget = self.DataClass.NMF
        
        if self.Target == 'Cascade':
            CropTarget = self.DataClass.Contour
        
        if self.Target == 'PCA' or self.Target == 'NMF':
            self.RangeEntry[0].insert(0,str(CropTarget.CropVal[1]))
            self.RangeEntry[1].insert(0,str(CropTarget.CropVal[0]))
            self.RangeEntry[2].insert(0,str(CropTarget.CropVal[2]))
            self.RangeEntry[3].insert(0,str(CropTarget.CropVal[3]))
            self.RangeEntry[4].insert(0,str(CropTarget.CropVal[4]))
            self.RangeEntry[5].insert(0,str(CropTarget.CropVal[5]))
            self.RangeEntry[6].insert(0,str(CropTarget.CropVal[6]))
            self.RangeEntry[7].insert(0,str(CropTarget.CropVal[7]))
        
        else:
            self.RangeEntry[0].insert(0,str(CropTarget.Lower[0]))
            self.RangeEntry[1].insert(0,str(CropTarget.Upper[0]))
            self.RangeEntry[2].insert(0,str(CropTarget.Lower[1]))
            self.RangeEntry[3].insert(0,str(CropTarget.Upper[1]))
            self.RangeEntry[4].insert(0,str(CropTarget.Lower[2]))
            self.RangeEntry[5].insert(0,str(CropTarget.Upper[2]))
            self.RangeEntry[6].insert(0,str(CropTarget.Lower[3]))
            self.RangeEntry[7].insert(0,str(CropTarget.Upper[3]))
                
    def close_windows(self):
        
        #output
        VisOut.TextBox(Title = 'Action', Text = 'Closing the information window', state = 1)
        
        #destroy master window
        self.master.destroy()


    def Reset(self):
    
        #Set the current range values (grab them)
        if self.Target == 'PCA':
            CropTarget = self.DataClass.PCA
            
        if self.Target == 'NMF':
            CropTarget = self.DataClass.NMF
        
        if self.Target == 'Cascade':
            CropTarget = self.DataClass.Contour
        
        #clear and fill
        for i in range(0,8):
            self.RangeEntry[i].delete(0, tk.END)
        
        if self.Target == 'PCA' or self.Target == 'NMF':
            #fill
            self.RangeEntry[0].insert(0,str(CropTarget.CropVali[1]))
            self.RangeEntry[1].insert(0,str(CropTarget.CropVali[0]))
            self.RangeEntry[2].insert(0,str(CropTarget.CropVali[2]))
            self.RangeEntry[3].insert(0,str(CropTarget.CropVali[3]))
            self.RangeEntry[4].insert(0,str(CropTarget.CropVali[4]))
            self.RangeEntry[5].insert(0,str(CropTarget.CropVali[5]))
            self.RangeEntry[6].insert(0,str(CropTarget.CropVali[6]))
            self.RangeEntry[7].insert(0,str(CropTarget.CropVali[7]))

        else:
            
            self.RangeEntry[0].insert(0,str(CropTarget.Lower[0]))
            self.RangeEntry[1].insert(0,str(CropTarget.Upper[0]))
            self.RangeEntry[2].insert(0,str(CropTarget.Lower[1]))
            self.RangeEntry[3].insert(0,str(CropTarget.Upper[1]))
            self.RangeEntry[4].insert(0,str(CropTarget.Lower[2]))
            self.RangeEntry[5].insert(0,str(CropTarget.Upper[2]))
            self.RangeEntry[6].insert(0,str(CropTarget.Lower[3]))
            self.RangeEntry[7].insert(0,str(CropTarget.Upper[3]))

    def Apply(self):

        #check the target application
        if self.Target == 'PCA':
            Upper = self.DataClass.PCA.Upper
            Lower = self.DataClass.PCA.Lower
            Activeset  = self.DataClass.PCA.Activeset
            CropTarget = self.DataClass.PCA
        
        if self.Target == 'NMF':
            Upper = self.DataClass.NMF.Upper
            Lower = self.DataClass.NMF.Lower
            Activeset  = self.DataClass.NMF.Activeset
            CropTarget = self.DataClass.NMF
        
        if self.Target == 'Cascade':
            Upper = self.DataClass.Contour.Upper
            Lower = self.DataClass.Contour.Lower
            Activeset  = self.DataClass.Contour.Activeset
            CropTarget = self.DataClass.Contour
        
        #fetch the values
        try:
            Lower[0]   = float(self.RangeEntry[0].get())
            if self.Target == 'Cascade':
                pass
            else:
                CropTarget.Lower[1] = Lower[0]
        except:
            pass

        try:
            Upper[0]   = float(self.RangeEntry[1].get())
            if self.Target == 'Cascade':
                pass
            else:
                CropTarget.Upper[0] = Upper[0]
        except:
            pass
        
        if Activeset[0]:
            try:
                Lower[1] = float(self.RangeEntry[2].get())
                if self.Target == 'Cascade':
                    pass
                else:
                    CropTarget.Lower[2] = Lower[1]
            except:
                pass
            try:
                Upper[1] = float(self.RangeEntry[3].get())
                if self.Target == 'Cascade':
                    pass
                else:
                    CropTarget.Upper[3] = Upper[1]
            except:
                pass
                    
        if Activeset[1]:
            try:
                Lower[2] = float(self.RangeEntry[4].get())
                if self.Target == 'Cascade':
                    pass
                else:
                    CropTarget.Lower[4] = Lower[2]
            except:
                pass
            try:
                Upper[2] = float(self.RangeEntry[5].get())
                if self.Target == 'Cascade':
                    pass
                else:
                    CropTarget.Upper[5] = Upper[2]
            except:
                pass

        if Activeset[2]:
            try:
                Lower[3] = float(self.RangeEntry[0].get())
                if self.Target == 'Cascade':
                    pass
                else:
                    CropTarget.Lower[6] = Lower[3]
            except:
                pass
            try:
                Upper[3] = float(self.RangeEntry[0].get())
                if self.Target == 'Cascade':
                    pass
                else:
                    CropTarget.Upper[7] = Upper[3]
            except:
                pass

        #Initiate the next recalculation
        if self.Target == 'PCA':
            
            CropTarget.BuildPCASet()
            self.Parent.PCACompute()

        if self.Target == 'NMF':
            
            #self.Parent.NMFCompute()
            CropTarget.BuildNMFSet()

        if self.Target == 'Cascade':
            
            #copy the elements
            CropTarget.Lower = Lower
            CropTarget.Upper = Upper
            
            #rebuild projection
            CropTarget.BuildProjection()

            #reinitiate
            CropTarget.InitiateCascadeSpecial()
            
            #save as buffer
            self.Parent.ZPlotBuffer = numpy.copy(CropTarget.ZPlot)
            self.Parent.XPlotBuffer = numpy.copy(CropTarget.XPlot)
            self.Parent.YPlotBuffer = numpy.copy(CropTarget.YPlot)
            
            #set parents parameetrs and refresh
            self.Parent.Navigator = False
            self.Parent.Switch    = True
            self.Parent.Refresh()

class ColorWindow:
    '''
    ######################################################################
    This wibdow is here to set calculation ranges of all parameters...
    ######################################################################
    '''
    
    def __init__(self,master,DataClass,Parent, isWindow = True):
        
        #link the DataClass
        self.DataClass = DataClass
        self.Parent = Parent
        
        #set master
        self.master = master
        
        if isWindow:
            self.master.title("Color Bondaries")
            self.master.configure(background = 'black')
            self.master.resizable(width = False, height = False)
        
        self.frame = ttk.Frame(self.master, relief = 'sunken', padding = '5p')
        
        
        #initialise the  arrays
        self.Sliders  = [None]*2
        self.RangeBut = [None]*3
        
        self.Min = tk.DoubleVar()
        self.Max = tk.DoubleVar()
        
        self.Sliders[0] = ttk.Scale(self.frame,
                                    from_ = numpy.min(self.DataClass.Contour.ZSPlot),
                                    to = numpy.max(self.DataClass.Contour.ZSPlot),
                                    variable = self.Min,
                                    value = numpy.min(self.DataClass.Contour.ZSPlot),
                                    orient=tk.VERTICAL)
                                    
        self.Sliders[1] = ttk.Scale(self.frame,
                                    from_= numpy.min(self.DataClass.Contour.ZSPlot),
                                    to = numpy.max(self.DataClass.Contour.ZSPlot),
                                    variable = self.Max,
                                    value = numpy.max(self.DataClass.Contour.ZSPlot),
                                    orient=tk.VERTICAL)
        
        #prepare buttons
        self.Sliders[0].pack(side=tk.LEFT, fill=tk.BOTH)
        self.Sliders[1].pack(side=tk.LEFT, fill=tk.BOTH)
        
        self.RangeBut[0] = ttk.Button(self.frame, text = 'Apply',  width = 5, command = self.Apply)
        self.RangeBut[1] = ttk.Button(self.frame, text = 'Reset',  width = 5, command = self.Reset)
        #self.RangeBut[2] = ttk.Button(self.frame, text = 'Close',  width = 5, command = self.close_windows)
        
        #self.RangeBut[2].pack(side=tk.TOP)
        self.RangeBut[1].pack(side=tk.TOP)
        self.RangeBut[0].pack(side=tk.TOP)
        
        #set default values
        self.Sliders[1].set(numpy.max(self.DataClass.Contour.ZSPlot))
        
        #pack all
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx = 5, pady = 5)

                
    def close_windows(self):
        
        #output
        VisOut.TextBox(Title = 'Action', Text = 'Closing the information window', state = 1)
        
        #destroy master window
        self.master.destroy()


    def Reset(self):
        
        #reset it all
        self.DataClass.Contour.SetCascade(Type = 'Data')
        
        #Call the refresh
        self.Parent.Navigator = False
        self.Parent.Switch    = True
        self.Parent.Refresh()

    def Apply(self):

        #self.DataClass.Contour.BuildProjection()
        
        #self.DataClass.Contour.InitiateCascadeSpecial()
        
        #save as buffer
        self.DataClass.Contour.ZPlot = numpy.copy(self.Parent.ZPlotBuffer)
        self.DataClass.Contour.XPlot = numpy.copy(self.Parent.XPlotBuffer)
        self.DataClass.Contour.YPlot = numpy.copy(self.Parent.YPlotBuffer)
        
        
        self.DataClass.Contour.ZBound[0] = float(self.Min.get())
        self.DataClass.Contour.ZBound[1] = float(self.Max.get())
        
        for i in range(0,len(self.DataClass.Contour.ZPlot)):
            for j in range(0,len(self.DataClass.Contour.ZPlot[0])):
                
                if self.DataClass.Contour.ZPlot[i,j] < float(self.Min.get()):
                    self.DataClass.Contour.ZPlot[i,j] = float(self.Min.get())

                if self.DataClass.Contour.ZPlot[i,j] > float(self.Max.get()):
                    self.DataClass.Contour.ZPlot[i,j] = float(self.Max.get())


        self.Parent.Navigator = False
        self.Parent.Switch    = True
        self.Parent.Refresh()



class GridWindowClass:

    '''
    ######################################################################
    Simple information display window 
    
    This instance is copied ofer from plot window and could in theory be
    pointed towards there (maybe next releases)
    ######################################################################
    '''

    def __init__(self,master,DataClass,Parent,Target, isWindow = True):
        
        #link the DataClass
        self.DataClass = DataClass
        self.Target    = Target
        self.Parent    = Parent
        
        #set ,aster
        self.master = master
        
        if isWindow:
            self.master.title(self.Target)
            self.master.configure(background = 'black')
            self.master.resizable(width = False, height = False)
        
        
        #set the frame
        self.frame = ttk.Frame(self.master, relief = 'sunken', padding = '15p')
        
        self.Labels = [None]*6
        self.Entry = [None]*4
        
        if self.Target == 'Cascade':
            
            self.Labels[0] = ttk.Label(self.frame, text= 'Spacing:')
            self.Labels[1] = ttk.Label(self.frame, text= 'Thickness:')
            self.Labels[3] = ttk.Label(self.frame, text= 'None')
            self.Labels[4] = ttk.Label(self.frame, text= 'None')
        
            self.Entry[0] = ttk.Entry(self.frame,width = 8, justify = tk.RIGHT)
            self.Entry[1] = ttk.Entry(self.frame,width = 8, justify = tk.RIGHT)
            self.Entry[2] = ttk.Entry(self.frame,width = 8, justify = tk.RIGHT)
            self.Entry[3] = ttk.Entry(self.frame,width = 8, justify = tk.RIGHT)
    
            self.Entry[0].insert(0,str(self.Parent.Number))
            self.Entry[1].insert(0,str(self.Parent.CNumber))
            self.Entry[2].insert(0,str(self.Parent.CLineWidth))
            self.Entry[3].insert(0,str(self.Parent.CColorStr))
            
            self.CascadeButton = ttk.Button(self.frame, text = 'Cascade', width = 5, command = self.Cascade)
            self.MeshButton    = ttk.Button(self.frame, text = 'Mesh'   , width = 5, command = self.Mesh)
            self.BothButton    = ttk.Button(self.frame, text = 'Both'   , width = 5, command = self.Both)
        
            self.Labels[4].grid(row = 0, column = 0)
            self.Labels[0].grid(row = 1, column = 0)
            self.Labels[1].grid(row = 1, column = 1)
            self.Labels[3].grid(row = 3, column = 0)
            
            self.Entry[0].grid( row = 0, column = 1)
            self.Entry[1].grid( row = 2, column = 0)
            self.Entry[2].grid( row = 2, column = 1)
            self.Entry[3].grid( row = 3, column = 1)

            self.CascadeButton.grid( row = 4, column = 0)
            self.MeshButton.grid( row = 4, column = 1)
            self.BothButton.grid( row = 5, column = 1)
        
        if self.Target == 'Grid':
            self.Labels[0] = ttk.Label(self.frame, text= 'Thickness:')
            self.Labels[1] = ttk.Label(self.frame, text= 'Color:')
        
            self.Entry[0] = ttk.Entry(self.frame,width = 8, justify = tk.RIGHT)
            self.Entry[1] = ttk.Entry(self.frame,width = 8, justify = tk.RIGHT)
                
            self.Entry[0].insert(0,'2')
            self.Entry[1].insert(0,'white')
        
            self.SetButton = ttk.Button(self.frame, text = 'Set'   , width = 5, command = self.Set)
            self.RemButton = ttk.Button(self.frame, text = 'Remove', width = 5, command = self.Remove)
            
            self.Labels[0].grid(row = 0, column = 0)
            self.Entry[0].grid( row = 1, column = 0)
            self.Labels[1].grid(row = 0, column = 1)
            self.Entry[1].grid( row = 1, column = 1)
            
            self.SetButton.grid( row = 4, column = 0)
        
        if self.Target == 'Ticks':
            self.Labels[0] = ttk.Label(self.frame, text= 'X Ticks:')
            self.Labels[1] = ttk.Label(self.frame, text= 'Y Ticks:')
        
            self.Entry[0] = ttk.Entry(self.frame,width = 8, justify = tk.RIGHT)
            self.Entry[1] = ttk.Entry(self.frame,width = 8, justify = tk.RIGHT)
                
            self.Entry[0].insert(0,'50')
            self.Entry[1].insert(0,'2')
        
            self.SetButton = ttk.Button(self.frame, text = 'Set'   , width = 5, command = self.Set)
            self.RemButton = ttk.Button(self.frame, text = 'Remove', width = 5, command = self.Remove)
            
            self.Labels[0].grid(row = 0, column = 0)
            self.Entry[0].grid( row = 1, column = 0)
            self.Labels[1].grid(row = 0, column = 1)
            self.Entry[1].grid( row = 1, column = 1)
        
            self.SetButton.grid( row = 4, column = 0)
            self.RemButton.grid( row = 4, column = 1)


        self.frame.grid_columnconfigure(0, weight = 1)
        self.frame.grid_columnconfigure(1, weight = 1)

        #pack all
        self.frame.pack(fill=tk.BOTH, expand=True)
    
    def close_windows(self):
        
        #output
        VisOut.TextBox(Title = 'Action', Text = 'Closing the Selection window', state = 1)
        
        #destroy master window
        self.master.destroy()

    def Set(self):
        
        if self.Target == 'Cascade':
            
            #Set logical variables
            self.Parent.CNumber      = float(self.Entry[0].get())

        if self.Target == 'Grid':
            
            #Set logical variables
            self.Parent.PutGrid     = True
            self.Parent.GridCol     = self.Entry[1].get()
            self.Parent.GridL       = float(self.Entry[0].get())
        
        if self.Target == 'Ticks':
            
            #Set logical variables
            self.DataClass.Contour.TickStepX = float(self.Entry[0].get())
            self.DataClass.Contour.TickStepY = float(self.Entry[1].get())
        
            #Run instance
            self.DataClass.Contour.SetTick()


        #refresh
        self.Parent.Refresh()

    def Cascade(self):
        
        #Set logical variables
        self.Parent.Perform     = True
        self.Parent.Number      = float(self.Entry[0].get())

        #turn off the lines
        self.Parent.CPerform = False
        
        #refresh
        self.Parent.Refresh()
    
    def Mesh(self):
        
        #turn off the Cascade
        self.Parent.Perform     = False
        
        #Set logical variables
        self.Parent.CPerform     = True
        self.Parent.CColorStr    = self.Entry[3].get()
        self.Parent.CLineWidth   = float(self.Entry[2].get())
        self.Parent.CNumber      = int(self.Entry[1].get())
    
        #refresh
        self.Parent.Refresh()
    
    def Both(self):
        
        #Set logical variables
        self.Parent.Perform     = True
        self.Parent.Number      = float(self.Entry[0].get())

        #Set logical variables
        self.Parent.CPerform     = True
        self.Parent.CColorStr    = self.Entry[3].get()
        self.Parent.CLineWidth   = float(self.Entry[2].get())
        self.Parent.CNumber      = int(self.Entry[1].get())

        #refresh
        self.Parent.Refresh()
    
    def Remove(self):
        
        if self.Target == 'Cascade':
            #remove
            self.Parent.CPerform     = False
        
        if self.Target == 'Grid':
            #remove
            self.Parent.PutGrid     = False

        self.Parent.Refresh()

class BaseWindowClass:


    '''
    ######################################################################
    This class is made to handle the baseline correction routines and
    should also be called later in the Fit window class. 
    
    A slider is put in pase to handle the scrolling though different 
    spectra. Note that this will always handle the base before any 
    further processing like the PCA...
    ######################################################################
    '''

    def __init__(self, master,DataClass,Parent,Target):
        
        #link the DataClass
        self.DataClass = DataClass
        self.Parent    = Parent
        self.Current   = 0
        self.which     = 0
        self.Target    = Target
        
        if self.Target == 'PCA':
            self.LocalCopy = numpy.copy(self.DataClass.PCA.PCADataSet)
        if self.Target == 'NMF':
            self.LocalCopy = numpy.copy(self.DataClass.NMF.NMFDataSet)
        if self.Target == 'Cascade':
            self.LocalCopy = numpy.copy(self.DataClass.Contour.Projection)
        
        #set ,aster
        self.master = master
        self.master.title("Fitting Visualisation")
        self.master.resizable(width = True, height = True)
        
        #set the frame
        self.frame  = ttk.Frame(self.master)
        self.frame0 = ttk.Frame(self.master)
    
        #Set labels
        self.BaseLabels = [None]*2
        
        self.BaseLabels[0] = ttk.Label(self.frame0, text = 'Lambda' ,width = 9)
        self.BaseLabels[1] = ttk.Label(self.frame0, text = 'p' ,width = 9)
        
        #Set entries
        self.BaseEntry = [None]*2
        
        self.BaseEntry[0] = ttk.Entry(self.frame0,width = 12)
        self.BaseEntry[1] = ttk.Entry(self.frame0,width = 12)
        
        self.BaseEntry[0].insert(0,'1000000')
        self.BaseEntry[1].insert(0,'0.005')
        
        #Build run button
        self.RunButton = ttk.Button(self.frame0, text = 'Run', width = 9, command = self.Run)
        
        #pack it all
        self.BaseLabels[0].pack(side = tk.TOP)
        self.BaseEntry[0].pack(side = tk.TOP)
        self.BaseLabels[1].pack(side = tk.TOP)
        self.BaseEntry[1].pack(side = tk.TOP)
        self.RunButton.pack(side = tk.TOP)
        
        #set buttons
        self.PrevButton = ttk.Button(self.frame0, text = '--',    width = 9, command = self.prev)
        self.NextButton = ttk.Button(self.frame0, text = '++',    width = 9, command = self.next)
        
        #refresh buttons
        self.RefreshButton = [None]*3
        self.RefreshButton[0] = ttk.Button(self.frame0, text = 'View Raw',   width = 9, command = self.RefreshRaw)
        self.RefreshButton[1] = ttk.Button(self.frame0, text = 'View All',   width = 9, command = self.RefreshAll)
        self.RefreshButton[2] = ttk.Button(self.frame0, text = 'View Proc',  width = 9, command = self.RefreshBase)
        
        #info button
        self.InfoButton = ttk.Button(self.frame0, text = 'Info',   width = 9, command = self.Info)
        
        #end buttons
        self.CloseButton = ttk.Button(self.frame0, text = 'Close', width = 9, command = self.Close)
        self.SaveButton  = ttk.Button(self.frame0, text = 'Submit',  width = 9, command = self.Save)

        #pack the buttons
        self.PrevButton.pack(side = tk.TOP)
        self.NextButton.pack(side = tk.TOP)
        
        self.RefreshButton[0].pack(side = tk.TOP)
        self.RefreshButton[1].pack(side = tk.TOP)
        self.RefreshButton[2].pack(side = tk.TOP)
        self.InfoButton.pack(side = tk.TOP)

        self.CloseButton.pack(side = tk.TOP)
        self.SaveButton.pack(side = tk.TOP)
        
        #add scrollbar
        self.slider = ttk.Scale(self.frame, from_=0, to=len(self.LocalCopy[2].transpose())-1,command = self.ScrollRefresh,orient=tk.VERTICAL)
        self.slider.pack(side=tk.LEFT, fill=tk.BOTH)
        
        ##############################
        #initiate the contaienr frame for the plot
        self.Figframe = ttk.Frame(self.frame)
        
        ##############################
        #introduce our new plot canvas here
        self.FigCanvas = SimplePlot.PlotCanvas(self.Figframe, bg="white", highlightthickness=0)
        
        ######################################################
        #Set some padding parameters
        self.FigCanvas.Drawer.Axes.PaddingIn  = [0.0 , 0.0, 0.0 , 0.0 ]
        self.FigCanvas.Drawer.Axes.PaddingOut = [0.15, 0.1, 0.05, 0.05]
        self.FigCanvas.Drawer.Axes.Thickness  = [2,2,2,2]
        self.FigCanvas.Drawer.Axes.XTickSpacing         = 50
        self.FigCanvas.Drawer.Axes.XTickType            = 1
        
        self.FigCanvas.Drawer.Axes.isYSci               = [True,True]
        self.FigCanvas.Drawer.isYSci                    = True
    
        self.FigCanvas.Drawer.Pointer.YSciPrecision     = '%.1e'
        self.FigCanvas.Drawer.Axes.YSciPrecision        = ['%.1e','%.1e']
        
        #make pointer for backwards compatibility
        self.Base = self.FigCanvas.Drawer
        
        #launch the drawer once will initialise all clases
        self.FigCanvas.Drawer.DrawAll()
        
        #pack the fig canvas
        self.FigCanvas.pack( fill=tk.BOTH, expand=tk.YES)
        
        #put the frame
        self.Figframe.pack( side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
        
        ##############################
        #Pack all
        self.frame0.pack(side=tk.LEFT, fill = tk.Y)
        self.frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    
    def Close(self):
        
        #output
        VisOut.TextBox(Title = 'Action', Text = 'Closing Window', state = 1)
        
        #destroy master window
        self.master.destroy()

    def RefreshRaw(self):
        
        #will select previous component
        self.which = 0
        
        #output
        VisOut.TextBox(Title = 'Action', Text = 'Set View to the Input Spctra', state = 1)
        
        self.Refresh()
    
    def RefreshBase(self):
        
        #will select previous component
        self.which = 2
        
        #output
        VisOut.TextBox(Title = 'Action', Text = 'Set View to the Substracted Spectra', state = 1)
        
        self.Refresh()
    
    def RefreshAll(self):
        
        #will select previous component
        self.which = 1
        
        #output
        VisOut.TextBox(Title = 'Action', Text = 'Set View to see input with computed Baselines', state = 1)
        
        self.Refresh()
    
    def ScrollRefresh(self,Current):
        
        #will select previous component
        self.Current = int(float(Current))
    
        self.Refresh()
    
    def prev(self):
        
        #will select previous component
        self.Current += -1
        self.slider.set(self.Current)
        
        #output
        VisOut.TextBox(Title = 'Action', Text = 'Set View one spectra back', state = 1)
        
        self.Refresh()
    
    def next(self):
        
        #will select next component
        self.Current += +1
        self.slider.set(self.Current)
        
        #output
        VisOut.TextBox(Title = 'Action', Text = 'Set View one spectra forward', state = 1)
        
        self.Refresh()
    
    def Info(sefl):
        
        #gather the info were this data comes from
        pass
    
    def Run(self):
        
        #gather the info were this data comes from
        self.Result,self.BaseLine = Utility.TakeBase(self.LocalCopy[2].transpose(),float(self.BaseEntry[0].get()),float(self.BaseEntry[1].get()),0.95)
    
        #output
        VisOut.TextBox(Title = 'Action', Text = 'Ran successfully the Baseline correction script', state = 1)
    
    def Refresh(self):
        
        #build output
        self.BaseBuilder()

    def BaseBuilder(self):
        
        #clear
        self.Base.Reset()
        
        #we only want to see the raw input
        if self.which == 0:
            
            #send out
            self.Base.AddPlot(self.LocalCopy[0],
                              self.LocalCopy[2].transpose()[self.Current],
                              Thickness = 2,
                              color = 'blue')
        
        #we want to see the raw input and the calculated baseline
        if self.which == 1:
            
            #send out
            self.Base.AddPlot(self.LocalCopy[0],
                              self.LocalCopy[2].transpose()[self.Current],
                              Thickness = 2,
                              color = 'blue')
            #send out
            self.Base.AddPlot(self.LocalCopy[0],
                              self.BaseLine[self.Current],
                              Thickness = 2,
                              color = 'black')
        
        #We want to see the resulting new signal
        if self.which == 2:
            
            #send out
            self.Base.AddPlot(self.LocalCopy[0],
                              self.Result[self.Current],
                              Thickness = 2,
                              color = 'red')
        #Send it out
        self.Base.Zoom()
                              
                              
    def Save(self):

        #Save the baseline parametrisation
        
        #he target is the pca processing
        if self.Target == 'PCA':
            self.DataClass.PCA.PCADataSet[2] = numpy.copy(self.Result.transpose())+numpy.abs(numpy.amin(self.Result.transpose()))*1.2
        
        #the target is the NMF processing
        if self.Target == 'NMF':
            self.DataClass.NMF.NMFDataSet[2] = numpy.copy(self.Result.transpose())+numpy.abs(numpy.amin(self.Result.transpose()))*1.2
        
        #the target is the Cascade processing
        if self.Target == 'Cascade':
            
            #save it
            self.DataClass.Contour.Projection[2] = numpy.copy(self.Result.transpose())+numpy.abs(numpy.amin(self.Result.transpose()))*1.2
            self.DataClass.Contour.InitiateCascadeSpecial()
            
            #save as buffer
            self.DataClass.Contour.ZPlotBuffer = numpy.copy(self.DataClass.Contour.ZPlot)
            self.DataClass.Contour.XPlotBuffer = numpy.copy(self.DataClass.Contour.XPlot)
            self.DataClass.Contour.YPlotBuffer = numpy.copy(self.DataClass.Contour.YPlot)
            
            
            self.Parent.Switch = True
            self.Parent.ViewBuilder()

        #output
        VisOut.TextBox(Title = 'Action', Text = 'Saved to the '+self.Target+' Dataset', state = 1)


class ToggledViewMode():

    '''
    ##########################################################################################
    This is a contracted frame method and will be used to allow contracting  hiding the inside
    of a given frame
    
    note the passed on button needs to be a chuckbutton 
    the passed on frame neesd to be a ttk.frame
    ##########################################################################################
    '''
    def __init__(self, buttonList, TargetFunction, Array, Link = None):

        #catch the variables and make them class
        self.buttonList         = buttonList
        self.TargetFunction     = TargetFunction
        self.Actif              = [None]*len(buttonList)
        self.Array              = Array
        self.Link               = Link
        
        #create in class varible to show or hide
        for i in range(0, len(self.buttonList)):
        
            #create all variables
            self.Actif[i] = tk.IntVar()
            
            #set them inactive
            self.Actif[i].set(0)
        
        for i in range(0, len(self.buttonList)):
        
            #Set the button
            self.buttonList[i].config(command  = partial(self.Toggle,i) )
            self.buttonList[i].config(variable = self.Actif[i] )
            self.buttonList[i].config(style    = 'Toolbutton'  )

        #toggle once
        #self.Toggle(0)

    def Toggle(self, ID):
        
        #cycle
        for i in range(0,len(self.buttonList)):
        
            if ID == i:
            
                #grid the object into place.
                self.Actif[i].set(1)
        
            else:
            
                #grid the object into place.
                self.Actif[i].set(0)
    
        if not self.Link == None:
        
            #linkage
            for i in range(len(self.Link)):
        
                self.Link[i].Reset()

        self.TargetFunction(self.Array[ID])

    def Reset(self):

        #cycle
        for i in range(0,len(self.buttonList)):
        
            #grid the object into place.
            self.Actif[i].set(0)



