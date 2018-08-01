# -*- coding: utf-8 -*-

#-INFO-
#-Name-CPCA-
#-Version-0.1.0-
#-Date-11_May_2016-
#-Author-Alexander_Schober-
#-email-alex.schober@mac.com-
#-INFO-

print 'Loading PCA dependencies...'

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

The same file will now (version 0.0.4) include the contour analysis methods
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

#numpy mathematical import
import numpy

#######################################
#advanced imports

#function manipulation routines
from functools import *

#######################################
#scipy imports
import scipy.ndimage.filters as filt

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




class RamanDepthPCA:

    '''
    ###########################################################################
    This routine will launch the main window which is a child passed on by the
    parent on launch.
    
    
    This is used to analyse the components from the measurement series.
    ###########################################################################
    '''


    def __init__(self,Data,root):
        
        #set master
        self.master = root
        
        #set top level
        self.CompWindow = tk.Toplevel(self.master)
        
        #lanuch the window class dependency
        app = CompWindow(self.CompWindow ,Data)

class CompWindow(ttk.Frame):
    
    
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
        
        self.Fit            = None
        self.BaseActive     = tk.IntVar()
        self.PathofInterest = DataClass.Info.Root
        
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
        ttk.Frame.__init__(self, root)
        self.master = root
        self.master.title("PCA / NMF Interface ("+self.DataClass.Info.GetInfoVal('Name')+")")
        self.master.resizable(width=True, height=True)
        
        #configure the items
        self.master.grid_columnconfigure(0, weight = 1)
        self.master.grid_rowconfigure(0, weight = 1)
        
        ####################################################
        #build all small frames...
        self.padding = '10p'
        
        self.MasterFrame   = ttk.Frame(self.master)
        
        self.NoteBookFrame = ttk.Frame(self.MasterFrame, padding= '10p')
        self.NoteBook      = ttk.Notebook(self.NoteBookFrame)
        
        self.NoteBookPage  = [None] * 4
        self.NoteBookTitle = ['Settings','Visualisation', 'Information']
                          
        self.NoteBookPage[0] = self.frame   = ttk.Frame(self.NoteBook, padding = '10p')
        self.NoteBookPage[1] = self.frame_1 = ttk.Frame(self.NoteBook, padding = '10p')
        self.NoteBookPage[2] = self.frame_2 = ttk.Frame(self.NoteBook, padding = '10p')
        
        #artifact form previous window management
        self.Show()
        
        #Build the notebooks
        k = 0
        for i in range(0,3):
            self.NoteBook.add(self.NoteBookPage[i],text = self.NoteBookTitle[i] )
        
        #We call the population routine putting all butons and entry fields
        self.NoteBook.grid(row = 0, column = 0, sticky= tk.E+tk.W+tk.N+tk.S)
        
        #give weight...
        self.NoteBookFrame.grid_columnconfigure(0, weight = 1)
        self.NoteBookFrame.grid_rowconfigure(0, weight = 1)
        
        #Place the frame into the main frame...
        self.NoteBookFrame.grid(row = 0,column = 0, sticky= tk.E+tk.W+tk.N+tk.S)
        
        #We call the population routine putting all butons and entry fields
        self.populate(root)
        
        #Pack the frame
        self.MasterFrame.grid(row = 0, column = 0, sticky= tk.E+tk.W+tk.N+tk.S)
        
        #give weigth
        self.MasterFrame.grid_columnconfigure(0, weight = 1)
        self.MasterFrame.grid_rowconfigure(0, weight = 1)
        
    
        #Initialise the PCA and NMF within the class
        if not self.DataClass.isPCA:
            self.DataClass.LoadPCA()
        if not self.DataClass.isNMF:
            self.DataClass.LoadNMF()

        #Run initial PCA take  asecond
        self.PCACompute()
        self.app.Refresh()


    def populate(self,root):
        '''
        ####################################################################################
        This function populate steh frame in order to process the button handling
        
        This will populate the main window of the instance and leave the rest free.
        ####################################################################################    
        '''
        #Placement variables
        VisOffset  = 1
        PCAOffset  = 4
        NMFOffset  = 7
        RowOffset   = 9
        RowLabels   = 12
        RowEntry    = 13
        
        ##########################################################
        #first comes the information frame into the container
        self.InfoFrame = ttk.Frame(self.frame)
        
        #then comes the content from the infor class
        self.InfoClass = Main.InfoWindowClass(self.InfoFrame,self.DataClass, window = False)
        
        #place this infoframe
        self.InfoFrame.grid(row = 0, column = 0)
        
        ##########################################################
        #Create the initial view range and fit range fields with labels
        self.PCABut       = [None]*4

        #conteiner label frame
        self.PCAFrame = ttk.Labelframe(self.frame,
                                       padding = self.padding,
                                       text = 'Principal Component Analysis:')
        
        #Load yhr button dependencies
        self.PCABut[0] = ttk.Button(self.PCAFrame, text = 'Mean',   width = 5, command = self.PCAMean)
        self.PCABut[1] = ttk.Button(self.PCAFrame, text = 'Base',   width = 5, command = self.PCABase)
        self.PCABut[2] = ttk.Button(self.PCAFrame, text = 'Range',  width = 5, command = self.PCARange)
        self.PCABut[3] = ttk.Button(self.PCAFrame, text = 'Go',width = 14, command = self.PCACompute)
        
        #place the elements using the grid method
        self.PCABut[0].grid(row = PCAOffset+1,column = 2 ,columnspan = 1)
        self.PCABut[1].grid(row = PCAOffset+1,column = 3 ,columnspan = 1)
        self.PCABut[2].grid(row = PCAOffset+1,column = 4 ,columnspan = 1)
        self.PCABut[3].grid(row = PCAOffset+1,column = 5 ,columnspan = 2)
        
        #grid the container
        self.PCAFrame.grid(row = 1, column = 0, sticky = tk.E+tk.W)

        ##########################################################
        #Separator
        #ttk.Label(self.frame,text = ' ').grid(row = 6, column = 1)
                                      
        ##########################################################
        #Create the visual framework first
        self.NMFLabels = [None]*5
        self.NMFEntry  = [None]*4
        self.NMFBut    = [None]*4
        
        MODES2 = [
                 ("Block Pivot", "0"),
                 ("HALS       ", "3"),
                 ("Numpy      ", "2"),
                 ("Mu         ", "4"),
                 ]

        self.v2 = tk.StringVar()
        self.v2.set("2") # initialize
        
        self.NMFFrame = ttk.Labelframe(self.frame, text = 'Non-Negatif Matrix Factorization:')
        
        #create the buttons
        i = 0
        a = []
        for text, mode in MODES2:
            a.append(ttk.Radiobutton(self.NMFFrame, text=text,variable=self.v2, value=mode))

        a[0].grid(row = NMFOffset+3,column = 2, columnspan = 2)
        a[1].grid(row = NMFOffset+3,column = 4, columnspan = 2)
        a[2].grid(row = NMFOffset+4,column = 2, columnspan = 2)
        a[3].grid(row = NMFOffset+4,column = 4, columnspan = 2)
        
        #define the labels
        self.NMFLabels[1] = ttk.Label(self.NMFFrame, text = 'Vectors' )
        self.NMFLabels[2] = ttk.Label(self.NMFFrame, text = 'Iterations'   )
        self.NMFLabels[3] = ttk.Label(self.NMFFrame, text = 'Tries'   )
        self.NMFLabels[4] = ttk.Label(self.NMFFrame, text = 'CPUs'    )
        
        self.NMFEntry[0] = ttk.Entry(self.NMFFrame,width = 8)#)
        self.NMFEntry[1] = ttk.Entry(self.NMFFrame,width = 8)#)
        self.NMFEntry[2] = ttk.Entry(self.NMFFrame,width = 8)#)
        self.NMFEntry[3] = ttk.Entry(self.NMFFrame,width = 8)#)
        
        self.NMFBut[0] = ttk.Button(self.NMFFrame, text = 'Base', command = self.NMFBase)
        self.NMFBut[1] = ttk.Button(self.NMFFrame, text = 'Range', command = self.NMFRange)
        self.NMFBut[2] = ttk.Button(self.NMFFrame, text = 'Info', command = self.NMFInfo)
        self.NMFBut[3] = ttk.Button(self.NMFFrame, text = 'Go', command = self.NMFCompute)
        
        #place the items
        self.NMFLabels[1].grid(row = NMFOffset+1,   column = 2)
        self.NMFLabels[2].grid(row = NMFOffset+1,   column = 4)
        self.NMFLabels[3].grid(row = NMFOffset+2,   column = 2)
        self.NMFLabels[4].grid(row = NMFOffset+2,   column = 4)

        self.NMFEntry[0].grid(row = NMFOffset+1  ,column = 3)
        self.NMFEntry[1].grid(row = NMFOffset+1  ,column = 5)
        self.NMFEntry[2].grid(row = NMFOffset+2   ,column = 3)
        self.NMFEntry[3].grid(row = NMFOffset+2,column = 5)
        
        self.NMFBut[0].grid(row = NMFOffset+1  ,column = 6)
        self.NMFBut[1].grid(row = NMFOffset+2,column = 6)
        self.NMFBut[2].grid(row = NMFOffset+3,column = 6)
        self.NMFBut[3].grid(row = NMFOffset+4,column = 6)
   
        #grid the conteiner
        self.NMFFrame.grid(row = 2, column = 0, sticky = tk.E+tk.W)

        #insert entry field values
        self.NMFEntry[0].insert(0,'3')
        self.NMFEntry[1].insert(0,'1000')
        self.NMFEntry[2].insert(0,'4')
        self.NMFEntry[3].insert(0,'4')


        ##############################
        #introduce our new plot canvas here
        self.SingularValuesFrame = ttk.Frame(self.frame, relief = 'sunken')
        
        #grid it
        self.SingularValuesFrame.grid(row = 0,
                                      column = 9,
                                      rowspan = NMFOffset+6,
                                      sticky = tk.N+tk.S+tk.W+tk.E)
        
        #configure grid
        self.frame.grid_columnconfigure(9, weight =1)
        self.frame.grid_rowconfigure(NMFOffset+5, weight =1)
        
        self.FigCanvas = SimplePlot.MultiPlotCanvas(self.SingularValuesFrame,
                                                    grid = [[True]],
                                                    ratioX   = [1],
                                                    bg="white",
                                                    highlightthickness=0)
                                                    
        #grab the subplot definitions
        self.ax = self.FigCanvas.GetSubPlot(0,0)
        
        ######################################################
        #Set some padding parameters for ax
        self.ax.Axes.PaddingIn          = [0.0 , 0.0, 0.0 , 0.0 ]
        self.ax.Axes.PaddingOut         = [0.2, 0.1, 0.05, 0.05]
        self.ax.Axes.Thickness          = [2,2,2,2]
        self.ax.Axes.XTickSpacing       = 50
        self.ax.Axes.XTickType          = 1
        self.ax.Axes.XLabelRounding     = 0
        self.ax.SmartResize             = True
        self.ax.Axes.isYSci             = [True,True]
        self.ax.Pointer.isYSci          = True
        self.ax.Pointer.YSciPrecision   = '%.1e'
        self.ax.Pointer.Sticky          = 1
        self.ax.Axes.YSciPrecision      = ['%.1e','%.1e']
        
        #set the default imaging mode to Tkinter Canvas
        self.ax.Live = 1
        
        self.ax.Title.SetTitle(text = 'Singular Value Decomposition')
        #######################################################
        #draw the plots
        self.ax.DrawAllPlot()
    
        #place the axes
        self.ax.Axes.DrawAxes()
        
        #place the ticks
        self.ax.Axes.PlaceAllTicks()
        
        #Place tick labels
        self.ax.Axes.PlaceAllLabels()
        
        #activate the cursor
        self.ax.BindCursor()
        
        #actiavte the zomer
        self.ax.BindZoomer()
            
    def PCAMean(self):
        
        '''
        ######################################################################
        Toggle the mean computation in the PCA calculatiob routines
        ######################################################################
        '''
        #Inverse boolean PCA variable
        self.DataClass.PCA.Calc.CompMean = not self.DataClass.PCA.Calc.CompMean
    
    def PCABase(self):
        
        '''
        ######################################################################
        Should launch a little base line calculation window
        
        this should then allow for parameter fine tuning.
        ######################################################################
        '''
        #build the tk fit window dependencies
        self.BaseWindow = tk.Toplevel(self.master)
        
        #launch the fit window
        self.base = BaseWindowClass(self.BaseWindow,self.DataClass,self,'PCA')
    
    def PCARange(self):
        
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
        self.app3 = RangeWindow(self.RangeWindow,self.DataClass,self,'PCA')
    
    def PCACompute(self):
        
        '''
        ######################################################################
        This function processes loaclly the PCA and then should call the 
        show instance of the visualisation protocol.
        ######################################################################
        '''
        ###################################
        self.DataClass.PCA.RunPCACalculation()
        self.Current = 'PCA'
        
                
        #Plot the singulr values out
        self.ax.Reset()
        self.ax.AddPlot([i for i in range(0, len(self.DataClass.VCH.s[0]))],
                        numpy.log10(self.DataClass.VCH.s[0]),
                        color = 'black'  ,
                        style = ['o',4,4])
        
        #reset the view
        self.ax.ZoomBox = [0,None,20,None]
        self.ax.Zoom()
        
        #output
        VisOut.TextBox(Title = 'Action', Text = 'Computing components for the PCA', state = 1)
    
    def NMFBase(self):
        
        '''
        ######################################################################
        
        ######################################################################
        '''
        #build the tk fit window dependencies
        self.BaseWindow = tk.Toplevel(self.master)
        
        #launch the fit window
        self.base = BaseWindowClass(self.BaseWindow,self.DataClass,self,'NMF')
    
        #output
        VisOut.TextBox(Title = 'Action', Text = 'Launched NMF Baseline request', state = 1)

    def NMFRange(self):
        
        '''
        ######################################################################
        Launches the NMF range seter this option will be targeted at the NMF
        ######################################################################
        '''
        #Build infor window dependencies to root
        self.RangeWindow = tk.Toplevel(self.master)
        
        #lanuch the window class dependency
        self.app3 = RangeWindow(self.RangeWindow,self.DataClass,self,'NMF')
    
        #output
        VisOut.TextBox(Title = 'Action', Text = 'Launched NMF Range Window', state = 1)

    def NMFInfo(self):
        '''
        ######################################################################
        
        ######################################################################
        '''
        pass

    def NMFCompute(self):
        
        '''
        ######################################################################
        This function processes loaclly the NMF and then should call the
        show instance of the visualisation protocol.
        ######################################################################
        '''
        
        #set values
        self.DataClass.NMF.k      = int(self.NMFEntry[0].get())
        self.DataClass.NMF.Iter   = int(self.NMFEntry[1].get())
        self.DataClass.NMF.Repeat = int(self.NMFEntry[2].get())
        self.DataClass.NMF.CPUs   = int(self.NMFEntry[3].get())
        
        #Set algorithm
        self.DataClass.NMF.Algo = self.DataClass.NMF.alg_names[int(self.v2.get())]

        #compute
        self.DataClass.NMF.RunNMFCalculation()
        self.Current = 'NMF'
    
        #output
        VisOut.TextBox(Title = 'Action', Text = 'Computing Components for the NMF\nParameters are : '+str(int(self.NMFEntry[0].get()))+' '+str(int(self.NMFEntry[1].get()))+' '+str(int(self.NMFEntry[2].get()))+' '+str(int(self.NMFEntry[3].get()))+' ', state = 1)
    
    def Grid(self):
        
        '''
        ######################################################################
        
        ######################################################################
        '''
        pass


    def Line(self):
        
        '''
        ######################################################################
        
        ######################################################################
        '''
        pass
    
    def Show(self):
        
        '''
        ######################################################################
        
        ######################################################################
        '''
        
        #launch the fit window
        self.app = ComponentWindowClass(self.frame_1,self.DataClass,self,0, window = False)
    
        #output
        VisOut.TextBox(Title = 'Action', Text = 'Launching a Component Window', state = 1)



    def Reset(self):
        
        '''
        ######################################################################
        
        ######################################################################
        '''
        pass


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
        
        if self.Target == 'Contour':
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
        
        if self.Target == 'Contour':
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
        
        if self.Target == 'Contour':
            Upper = self.DataClass.Contour.Upper
            Lower = self.DataClass.Contour.Lower
            Activeset  = self.DataClass.Contour.Activeset
            CropTarget = self.DataClass.Contour
        
        #fetch the values
        try:
            Lower[0]   = float(self.RangeEntry[0].get())
            if self.Target == 'Contour':
                pass
            else:
                CropTarget.Lower[1] = Lower[0]
        except:
            pass

        try:
            Upper[0]   = float(self.RangeEntry[1].get())
            if self.Target == 'Contour':
                pass
            else:
                CropTarget.Upper[0] = Upper[0]
        except:
            pass
        
        if Activeset[0]:
            try:
                Lower[1] = float(self.RangeEntry[2].get())
                if self.Target == 'Contour':
                    pass
                else:
                    CropTarget.Lower[2] = Lower[1]
            except:
                pass
            try:
                Upper[1] = float(self.RangeEntry[3].get())
                if self.Target == 'Contour':
                    pass
                else:
                    CropTarget.Upper[3] = Upper[1]
            except:
                pass
                    
        if Activeset[1]:
            try:
                Lower[2] = float(self.RangeEntry[4].get())
                if self.Target == 'Contour':
                    pass
                else:
                    CropTarget.Lower[4] = Lower[2]
            except:
                pass
            try:
                Upper[2] = float(self.RangeEntry[5].get())
                if self.Target == 'Contour':
                    pass
                else:
                    CropTarget.Upper[5] = Upper[2]
            except:
                pass

        if Activeset[2]:
            try:
                Lower[3] = float(self.RangeEntry[0].get())
                if self.Target == 'Contour':
                    pass
                else:
                    CropTarget.Lower[6] = Lower[3]
            except:
                pass
            try:
                Upper[3] = float(self.RangeEntry[0].get())
                if self.Target == 'Contour':
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

        if self.Target == 'Contour':
            
            #copy the elements
            CropTarget.Lower = Lower
            CropTarget.Upper = Upper
            
            #rebuild projection
            CropTarget.BuildProjection()

            #reinitiate
            CropTarget.InitiateContourSpecial()
            
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
        self.DataClass.Contour.SetContour(Type = 'Data')
        
        #Call the refresh
        self.Parent.Navigator = False
        self.Parent.Switch    = True
        self.Parent.Refresh()

    def Apply(self):

        #self.DataClass.Contour.BuildProjection()
        
        #self.DataClass.Contour.InitiateContourSpecial()
        
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
        
        if self.Target == 'Contour':
            
            self.Labels[0] = ttk.Label(self.frame, text= 'Num. :')
            self.Labels[1] = ttk.Label(self.frame, text= 'Thickness:')
            self.Labels[3] = ttk.Label(self.frame, text= 'Color:')
            self.Labels[4] = ttk.Label(self.frame, text= 'Num. :')
        
            self.Entry[0] = ttk.Entry(self.frame,width = 8, justify = tk.RIGHT)
            self.Entry[1] = ttk.Entry(self.frame,width = 8, justify = tk.RIGHT)
            self.Entry[2] = ttk.Entry(self.frame,width = 8, justify = tk.RIGHT)
            self.Entry[3] = ttk.Entry(self.frame,width = 8, justify = tk.RIGHT)
    
            self.Entry[0].insert(0,str(self.Parent.Number))
            self.Entry[1].insert(0,str(self.Parent.CNumber))
            self.Entry[2].insert(0,str(self.Parent.CLineWidth))
            self.Entry[3].insert(0,str(self.Parent.CColorStr))
            
            self.ContourButton = ttk.Button(self.frame, text = 'Contour', width = 5, command = self.Contour)
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

            self.ContourButton.grid( row = 4, column = 0)
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
        
        if self.Target == 'Contour':
            
            #Set logical variables
            self.Parent.CPerform     = True
            self.Parent.CColorStr    = self.Entry[2].get()
            self.Parent.CLineWidth   = float(self.Entry[1].get())
            self.Parent.CNumber      = int(self.Entry[0].get())

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

    def Contour(self):
        
        #Set logical variables
        self.Parent.Perform     = True
        self.Parent.Number      = int(self.Entry[0].get())

        #turn off the lines
        self.Parent.CPerform = False
        
        #refresh
        self.Parent.Refresh()
    
    def Mesh(self):
        
        #turn off the contour
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
        self.Parent.Number      = int(self.Entry[0].get())

        #Set logical variables
        self.Parent.CPerform     = True
        self.Parent.CColorStr    = self.Entry[3].get()
        self.Parent.CLineWidth   = float(self.Entry[2].get())
        self.Parent.CNumber      = int(self.Entry[1].get())

        #refresh
        self.Parent.Refresh()
    
    def Remove(self):
        
        if self.Target == 'Contour':
            #remove
            self.Parent.CPerform     = False
        
        if self.Target == 'Grid':
            #remove
            self.Parent.PutGrid     = False

        self.Parent.Refresh()

class ComponentWindowClass:


    '''
    ######################################################################
    This class is made to handle the pca visualisation window. It can be
    called remotely by the master class and has full access to the Data 
    Class.
    
    Note that this instance was trasposed from the plotwindow manager 
    of version 0.0.3.
    ######################################################################
    '''

    def __init__(self, master,DataClass,Parent,Current, window = True):
        
        #link the DataClass
        self.DataClass = DataClass
        self.Parent    = Parent
        self.Current   = Current
        self.padding   = '10p'
        
        #set ,aster
        if window:
            self.master = master
            self.master.title("Fitting Visualisation")
            self.master.configure(background = 'black')
            self.master.resizable(width = True, height = True)
        else:
            self.master = ttk.Frame(master)
        
        #set the frame
        self.frame  = ttk.Frame(self.master, padding = self.padding)
        self.frame0 = ttk.Frame(self.master, padding = self.padding)
        self.frame1 = ttk.Frame(self.master, padding = self.padding)
        self.frame2 = ttk.Frame(self.master, padding = self.padding)
        
        #set buttons
        self.PrevButton = ttk.Button(self.frame0, text = '<-',      width = 3, command = self.prev)
        self.QuitButton = ttk.Button(self.frame0, text = 'Refresh', width = 9, command = self.Refresh)
        self.NextButton = ttk.Button(self.frame0, text = '->',      width = 3, command = self.next)
        self.RemNoise   = ttk.Button(self.frame0, text = 'Noise',   width = 9, command = self.RemoveNoise)
        
        
        #self.GridButton = ttk.Button(self.frame1, text = 'Grid',    width = 5, command = self.Grid)
        #self.LineButton = ttk.Button(self.frame1, text = 'Line',    width = 5, command = self.Line)
        self.InveButton = ttk.Button(self.frame0, text = 'Invert',  width = 5, command = self.Invert)
        self.InfoButton = ttk.Button(self.frame0, text = 'Info',    width = 5, command = self.Info)
        
        self.CloseButton = ttk.Button(self.frame2, text = 'Close', width = 9, command = self.Close)
        self.SaveButton  = ttk.Button(self.frame2, text = 'Save',  width = 9, command = self.Save)

        
        #pack the buttons
        self.PrevButton.pack(side = tk.LEFT)
        self.QuitButton.pack(side = tk.LEFT)
        self.NextButton.pack(side = tk.LEFT)
        self.RemNoise.pack(side = tk.LEFT)
        
        #self.GridButton.pack(side = tk.LEFT)
        #self.LineButton.pack(side = tk.LEFT)
        self.InveButton.pack(side = tk.LEFT)
        self.InfoButton.pack(side = tk.LEFT)

        self.CloseButton.pack(side = tk.RIGHT)
        self.SaveButton.pack(side = tk.RIGHT)
        
        #plot default
        self.Inverter = 1
        
        ##############################
        #introduce our new plot canvas here
        self.FigCanvas = SimplePlot.MultiPlotCanvas(self.frame,
                                                    grid = [[True,True]],
                                                    ratioX   = [1],
                                                    ratioY   = [1,1],
                                                    bg="white",
                                                    highlightthickness=0)
                                                    
        #grab the subplot definitions
        self.ax = self.FigCanvas.GetSubPlot(0,0)
        self.bx = self.FigCanvas.GetSubPlot(0,1)
        
        ######################################################
        #Set some padding parameters for ax
        self.ax.Axes.PaddingIn          = [0.0 , 0.0, 0.0 , 0.0 ]
        self.ax.Axes.PaddingOut         = [0.15, 0.1, 0.05, 0.05]
        self.ax.Axes.XLabelOffset       = [0.05,0.05]
        self.ax.Axes.YLabelOffset       = [0.08,0.08]
        self.ax.Axes.Thickness          = [2,2,2,2]
        self.ax.Axes.XTickSpacing       = 50
        self.ax.Axes.XTickType          = 1
        self.ax.Axes.XLabelRounding     = 0
        self.ax.SmartResize             = True
        
        self.ax.Axes.isYSci             = [True,True]
        self.ax.Pointer.isYSci          = True
        self.ax.Pointer.Sticky          = 1
        self.ax.Pointer.YSciPrecision   = '%.1e'
        self.ax.Axes.YSciPrecision      = ['%.1e','%.1e']
        
        #set the default imaging mode to Tkinter Canvas
        self.ax.Live = 1
    
        ######################################################
        #Set some padding parameters for ax
        self.bx.Axes.PaddingIn          = [0.0 , 0.0, 0.0 , 0.0 ]
        self.bx.Axes.PaddingOut         = [0.15, 0.1, 0.05, 0.05]
        self.bx.Axes.XLabelOffset       = [0.05,0.05]
        self.bx.Axes.YLabelOffset       = [0.08,0.08]
        self.bx.Axes.Thickness          = [2,2,2,2]
        self.bx.Axes.XTickSpacing       = 1
        self.bx.Axes.XTickType          = 1
        self.bx.Axes.XLabelRounding     = 0
        self.bx.SmartResize             = True
        self.bx.Pointer.Sticky          = 1
        self.bx.Axes.isYSci             = [True,True]
        self.bx.Axes.isXSci             = [True,True]
        
        self.bx.Pointer.isYSci          = True
        self.bx.Pointer.isXSci          = True
        self.bx.Pointer.YSciPrecision   = '%.1e'
        self.bx.Axes.YSciPrecision      = ['%.1e','%.1e']
        
        #set the default imaging mode to Tkinter Canvas
        self.bx.Live = 1
        
        #######################################################
        #draw the plots
        self.ax.DrawAllPlot()
        self.bx.DrawAllPlot()
    
        #place the axes
        self.ax.Axes.DrawAxes()
        self.bx.Axes.DrawAxes()
        
        #place the ticks
        self.ax.Axes.PlaceAllTicks()
        self.bx.Axes.PlaceAllTicks()
        
        #Place tick labels
        self.ax.Axes.PlaceAllLabels()
        self.bx.Axes.PlaceAllLabels()
        
        #activate the cursor
        self.ax.BindCursor()
        self.bx.BindCursor()
        
        #actiavte the zomer
        self.ax.BindZoomer()
        self.bx.BindZoomer()
        
        #pack all frames
        self.frame0.grid(row = 1, column = 1, sticky   = tk.E+tk.W)
        self.frame1.grid(row = 1, column = 2, sticky   = tk.E+tk.W)
        self.frame2.grid(row = 4, column = 1, columnspan = 2, sticky   = tk.E+tk.W)
        self.frame.grid( row = 3, column = 1, columnspan = 2, sticky   = tk.N+tk.S+tk.E+tk.W)
        
        #configure weights
        self.master.grid_columnconfigure(1, weight = 1)
        self.master.grid_rowconfigure(3, weight = 1)
        
        if not window:

            self.master.grid(row = 0 , column = 0, sticky   = tk.N+tk.S+tk.E+tk.W)
            
            master.grid_columnconfigure(0, weight = 1)
            master.grid_rowconfigure(0, weight = 1)

            master.grid(row = 0 , column = 0, sticky   = tk.N+tk.S+tk.E+tk.W)
        
        try:
            self.Refresh()
        except:
            pass

    def RemoveNoise(self):
        '''
        ####################################################################################
        This function is imported and tweaked from version 3 to act as a noise remover. Note
        that it will remove the componnets after including the selected one from the dataset
        
        then it will create a typical depth file and add NoiseCompRem to the name
        
        it will then dump the data class and load this file and finnally reinitialise the
        current PCA and NMF framework. 
        
        The created fil will be marked as a version 1 file. version 2 files do not exist yet
        though they should come in version 0.0.5
        
        Note that this option will only be available when it is a PCA
        Noise remoal on a NMF data sample makes no sense...
        ####################################################################################
        '''

        #set the input list
        InputSplitNum = range(self.Current,len(self.DataClass.VCH.PC))
        VisOut.TextBox(Title = 'Action', Text = 'Successfully created array to remove', state = 1)
        
        #proceed with fixing data
        self.DataClass.PCA.Remove(InputSplitNum)
        VisOut.TextBox(Title = 'Action', Text = 'Successfully removed the components', state = 1)
    
        #export
        self.Path = self.DataClass.PCA.Export()
        VisOut.TextBox(Title = 'Action', Text = 'Successfully Exported the current Dataset', state = 1)
                
        #Reset
        #self.DataClass.Reset(self.Path)
        VisOut.TextBox(Title = 'Action', Text = 'Successfully Reloaded the whole Dataset and reinitialised the whole Dataclass', state = 1)
    
    def Close(self):
        
        #destroy master window
        self.master.destroy()
    
        #output
        VisOut.TextBox(Title = 'Action', Text = 'Closing Window', state = 1)

    def Invert(self):
        
        #will select previous component
        self.Inverter = -1*self.Inverter
        self.Refresh()
    
        #output
        VisOut.TextBox(Title = 'Action', Text = 'Inverted Component in the Window', state = 1)
    
    def prev(self):
        
        #will select previous component
        self.Current += -1
        self.Refresh()
    
        #output
        VisOut.TextBox(Title = 'Action', Text = 'Switching to previous Component', state = 1)
    
    def next(self):
        
        #will select next component
        self.Current += +1
        self.Refresh()
    
        #output
        VisOut.TextBox(Title = 'Action', Text = 'Switching to next Component', state = 1)
    
    def Grid(self):
        
        #will toggle the Grid on off in the general dataclass
        self.DataClass.VCH.GridOn = not self.DataClass.VCH.GridOn
        self.Refresh()
    
        #output
        VisOut.TextBox(Title = 'Action', Text = 'Switching Grid on or off', state = 1)
    
    def Line(self):
        
        #will toggle the line on off in the general dataclass
        self.DataClass.VCH.LineOn = not self.DataClass.VCH.LineOn
        self.Refresh()
    
        #output
        VisOut.TextBox(Title = 'Action', Text = 'Switching Line on or off', state = 1)
    
    def Info(sefl):
        
        #gather the info were this data comes from
        pass
    
    def Refresh(self):

        #Load the information
        self.DataClass.VCH.BuildOutput(self.Current,
                                       self.ax,
                                       self.bx,
                                       self.Inverter)
        
        #Set titles for all Components
        TitlePC1 = str('Principal component Data '+str(int(self.Current+1)))

        
        #Set title for all scores
        TitleSc1 = str('Principal component Score '+str(int(self.Current+1)))

            
        #Set the titles for Components
        self.ax.Title.SetTitle(text = TitlePC1)
        
        #Set the titles for the scores
        self.bx.Title.SetTitle(text = TitleSc1)
        
        

    def Save(self):

        #Load Data and prepare for export
        #print len(Data.PCA.InversePC),len(Data.PCA.PC)
        ExpComponentY = self.Inverter*self.DataClass.VCH.PC[self.Current]
        ExpComponentX = self.DataClass.VCH.PCX
        ExpScoreY     = self.Inverter*self.DataClass.VCH.Score[self.Current]
                    
        #To be fixed eventually error in handling this part (dirty)
        X = numpy.asarray(self.DataClass.VCH.ScoreX)
        X = X[:,0].tolist()
        X1 = X[0]
        X2 = X[len(X)-1]
        ExpScoreX  = self.DataClass.VCH.DataClass.Y.Y[0][X1:X2+1]
                        
        #Call component to file writing routine
        self.DataClass.Write.WriteComponent(self.DataClass,
                                            int(self.Current),
                                            ExpComponentX,
                                            ExpComponentY,
                                            ExpScoreX,
                                            ExpScoreY)
                                            

        #output
        VisOut.TextBox(Title = 'Action',
                       Text = 'Wrote the component to file',
                       state = 1)



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
        if self.Target == 'Contour':
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
        
        #the target is the contour processing
        if self.Target == 'Contour':
            
            #save it
            self.DataClass.Contour.Projection[2] = numpy.copy(self.Result.transpose())+numpy.abs(numpy.amin(self.Result.transpose()))*1.2
            self.DataClass.Contour.InitiateContourSpecial()
            
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



