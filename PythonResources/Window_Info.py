# -*- coding: utf-8 -*-

#-INFO-
#-Name-Window_Info-
#-Version-0.1.00-
#-Last_Modification-10_Nov_2017-
#-Date-22_April_2015-
#-Author-Alexander_Schober-
#-email-alex.schober@mac.com-
#-INFO-

print 'Initiating Main dependencies...'

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

This is the information window class. It is from previous older versions of
the code and therefore does nto provide the total flexibility that we are
looking for.

RECQUIRES MAJOR REWORK

###########################################################################
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



class InfoWindowClass:
    '''
    ####################################################################################
    Simple information window handler. This should always be used to launch the 
    current sample information...
    ####################################################################################
    '''


    def __init__(self,master,DataClass, window = True):
        
        #set ,aster
        if window:
            self.master = master
            master.title("Sample/Raman Informations")
            self.master.resizable(width=False, height=False)
        
        
        #set the frame
        self.frame = ttk.Frame(master)
        self.DataClass = DataClass
        self.padding = '2p'
        
        if os.name == 'nt':
            self.ClassFont =  tkFont.Font(weight = 'bold',
                                          underline = 0,
                                          size = 8)
        else:
            self.ClassFont =  tkFont.Font(weight = 'bold',
                                          underline = 0)
                    
        #add notebook capabilities into this frame
        self.NoteBook = ttk.Notebook(self.frame)
        
        #build all small frames...
        self.NoteBookPage = [None]*5
        self.NoteBookTitle = ['File','Raman','X,Y,Z,T','Sample','Notes']
                          
        self.NoteBookPage[0] = ttk.Frame(self.NoteBook)
        self.NoteBookPage[1] = ttk.Frame(self.NoteBook)
        self.NoteBookPage[2] = ttk.Frame(self.NoteBook)
        self.NoteBookPage[3] = ttk.Frame(self.NoteBook)
        self.NoteBookPage[4] = ttk.Frame(self.NoteBook)
        
        #Call all the frame populators...
        
        
        #Build the notebooks
        for i in range(0,len(self.NoteBookPage)):
            
            #add each page
            self.NoteBook.add(self.NoteBookPage[i],text = self.NoteBookTitle[i] )

        
        #We call the population routine putting all butons and entry fields
        self.NoteBook.pack(side = tk.TOP,expand = 1,fill = tk.X)
    
        if window:
            
            self.qframe = ttk.Frame(master, padding = '10p')
            
            #set buttons
            self.quitButton = ttk.Button(self.qframe,
                                         text = 'Close',
                                         command = self.close_windows,
                                         padding = self.padding)
            self.quitButton.grid(row = 0, column = 1)
            self.qframe.grid_columnconfigure(0, weight = 1)
        
            self.qframe.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        #pack all
        self.frame.pack( side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        
        #call all the methods
        self.BuildFile()
        self.BuildRaman()
        self.BuildPos()
        self.BuildSample()


    def BuildFile(self):
    
        '''
        ##########################################
        This will build the File information layout
        note that it is tricky to put the path
        into a proper format so we will just
        put it into a text box and the user can 
        then decide what he wants to do with it
        
        
        the method self.Data.Info.Call('value')
        will be used to fetch the proper element
        ##########################################
        '''

        #define alias
        Target = self.NoteBookPage[0]
        
        #build the central frame
        self.FileFrame = ttk.Frame(Target, padding = self.padding)
    
        #place and configure it
        self.FileFrame.grid(row = 1,
                            column = 1)
        
        #configure the suroundings
        Target.grid_columnconfigure(0,weight = 1)
        Target.grid_columnconfigure(2,weight = 1)
        Target.grid_rowconfigure(0,weight = 1)
        Target.grid_rowconfigure(2,weight = 1)
    
        self.FileFrame.grid_columnconfigure(1,weight = 1)
        
        #element matrix to be appended that will be placed
        #automatically at the end of this function through a loop
        self.PoisitionMatrix = []
    
    
        #add all labels
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'File Path:',
                                               anchor = tk.N+tk.E,
                                               font = self.ClassFont),
                                     0,
                                     0,
                                     tk.N+tk.S+tk.E+tk.W,
                                     1,
                                     1])
    
        
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text=self.DataClass.Info.GetInfo(Name = 'Folder Path')[1],
                                               justify=tk.LEFT,
                                               wraplength = 300
                                               ),
                                     0,
                                     1,
                                     tk.N+tk.S+tk.E+tk.W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Wire File Name:',
                                               anchor = tk.E,
                                               font = self.ClassFont,
                                               padding = self.padding),
                                     1,
                                     0,
                                     tk.N+tk.S+tk.E+tk.W,
                                     1,
                                     1])
        
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text=self.DataClass.Info.GetInfo(Name = 'Wire File')[1],
                                               justify=tk.LEFT,
                                               ),
                                     1,
                                     1,
                                     tk.N+tk.S+tk.E+tk.W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Processing Date',
                                               anchor = tk.E,
                                               font = self.ClassFont,
                                               padding = self.padding),
                                     2,
                                     0,
                                     tk.N+tk.S+tk.E+tk.W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text=self.DataClass.Info.GetInfo(Name = 'Proccessing time')[1],
                                               justify=tk.LEFT,
                                               ),
                                     2,
                                     1,
                                     tk.N+tk.S+tk.E+tk.W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Raman Meas. Type:',
                                               anchor = tk.E,
                                               font = self.ClassFont,
                                               padding = self.padding),
                                     3,
                                     0,
                                     tk.N+tk.S+tk.E+tk.W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text=self.DataClass.Info.GetInfo(Name = 'Data Type')[1],
                                               justify=tk.LEFT,
                                               ),
                                     3,
                                     1,
                                     tk.N+tk.S+tk.E+tk.W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'N. of Meas.:',
                                               anchor = tk.E,
                                               font = self.ClassFont,
                                               padding = self.padding),
                                     4,
                                     0,
                                     tk.N+tk.S+tk.E+tk.W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text=self.DataClass.Info.GetInfo(Name = 'Number of Measurements')[1],
                                               justify=tk.LEFT,
                                               ),
                                     4,
                                     1,
                                     tk.N+tk.S+tk.E+tk.W,
                                     1,
                                     1])
        
        #place everything
        for i in range(0,len(self.PoisitionMatrix)):
        
            self.PoisitionMatrix[i][0].grid(row         =  self.PoisitionMatrix[i][1],
                                            column      =  self.PoisitionMatrix[i][2],
                                            sticky      =  self.PoisitionMatrix[i][3],
                                            rowspan     =  self.PoisitionMatrix[i][4],
                                            columnspan  =  self.PoisitionMatrix[i][5])

    def BuildRaman(self):
    
        '''
        ##########################################
        
        the method self.Data.Info.Call('value')
        will be used to fetch the proper element
        ##########################################
        '''

        #define alias
        Target = self.NoteBookPage[1]
        
        #build the central frame
        self.FileFrame = ttk.Frame(Target, padding = self.padding)
    
        #place and configure it
        self.FileFrame.grid(row = 1,
                            column = 1)
        
        #configure the suroundings
        Target.grid_columnconfigure(0,weight = 1)
        Target.grid_columnconfigure(2,weight = 1)
        Target.grid_rowconfigure(0,weight = 1)
        Target.grid_rowconfigure(2,weight = 1)
    
        self.FileFrame.grid_columnconfigure(1,weight = 1)
        
        #element matrix to be appended that will be placed
        #automatically at the end of this function through a loop
        self.PoisitionMatrix = []
    
    
        #add all labels
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Laser Wavelength:',
                                               anchor = tk.E,
                                               font = self.ClassFont,
                                               padding = self.padding),
                                     0,
                                     0,
                                     tk.E+tk.W,
                                     1,
                                     1])
    
        
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text=self.DataClass.Info.GetInfo(Name = 'Laser Wavelength')[1]+' '+
                                                self.DataClass.Info.GetInfo(Name = 'Laser Wavelength')[2],
                                               justify=tk.LEFT,
                                               wraplength = 300
                                               ),
                                     0,
                                     1,
                                     tk.E+tk.W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Laser Power:',
                                               anchor = tk.E,
                                               font = self.ClassFont,
                                               padding = self.padding),
                                     1,
                                     0,
                                     tk.E+tk.W,
                                     1,
                                     1])
        
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text=self.DataClass.Info.GetInfo(Name = 'Laser Power')[1]+' '+self.DataClass.Info.GetInfo(Name = 'Laser Power')[2],
                                               justify=tk.LEFT,
                                               ),
                                     1,
                                     1,
                                     tk.E+tk.W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Grating Used:',
                                               anchor = tk.E,
                                               font = self.ClassFont,
                                               padding = self.padding),
                                     2,
                                     0,
                                     tk.E+tk.W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text=self.DataClass.Info.GetInfo(Name = 'Grating used')[1]+' '+self.DataClass.Info.GetInfo(Name = 'Grating used')[2],
                                               justify=tk.LEFT,
                                               ),
                                     2,
                                     1,
                                     tk.E+tk.W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Objectif used:',
                                               anchor = tk.E,
                                               font = self.ClassFont,
                                               padding = self.padding),
                                     3,
                                     0,
                                     tk.E+tk.W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text=self.DataClass.Info.GetInfo(Name = 'Objectif used')[1]+' '+self.DataClass.Info.GetInfo(Name = 'Objectif used')[2],
                                               justify=tk.LEFT,
                                               ),
                                     3,
                                     1,
                                     tk.E+tk.W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'N. of Meas.:',
                                               anchor = tk.E,
                                               font = self.ClassFont,
                                               padding = self.padding),
                                     4,
                                     0,
                                     tk.E+tk.W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text=self.DataClass.Info.GetInfo(Name = 'Number of Measurements')[1],
                                               justify=tk.LEFT,
                                               ),
                                     4,
                                     1,
                                     tk.E+tk.W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'N. of Acqu.:',
                                               anchor = tk.E,
                                               font = self.ClassFont,
                                               padding = self.padding),
                                     5,
                                     0,
                                     tk.E+tk.W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text=self.DataClass.Info.GetInfo(Name = 'Number of Acquisitions')[1],
                                               justify=tk.LEFT,
                                               ),
                                     5,
                                     1,
                                     tk.E+tk.W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Number of Acquisitions:',
                                               anchor = tk.E,
                                               font = self.ClassFont,
                                               padding = self.padding),
                                     5,
                                     0,
                                     tk.E+tk.W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text=self.DataClass.Info.GetInfo(Name = 'Number of Acquisitions')[1]+' '+self.DataClass.Info.GetInfo(Name = 'Number of Acquisitions')[2],
                                               justify=tk.LEFT,
                                               ),
                                     5,
                                     1,
                                     tk.E+tk.W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Acquisition time:',
                                               anchor = tk.E,
                                               font = self.ClassFont,
                                               padding = self.padding),
                                     6,
                                     0,
                                     tk.E+tk.W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text=self.DataClass.Info.GetInfo(Name = 'Duration per Acquisitions')[1]+' '+self.DataClass.Info.GetInfo(Name = 'Duration per Acquisitions')[2],
                                               justify=tk.LEFT,
                                               ),
                                     6,
                                     1,
                                     tk.E+tk.W,
                                     1,
                                     1])
                                     
        #place everything
        for i in range(0,len(self.PoisitionMatrix)):
        
            self.PoisitionMatrix[i][0].grid(row         =  self.PoisitionMatrix[i][1],
                                            column      =  self.PoisitionMatrix[i][2],
                                            sticky      =  self.PoisitionMatrix[i][3],
                                            rowspan     =  self.PoisitionMatrix[i][4],
                                            columnspan  =  self.PoisitionMatrix[i][5])
    
    def BuildPos(self):
    
        '''
        ##########################################
        
        the method self.Data.Info.Call('value')
        will be used to fetch the proper element
        ##########################################
        '''

        #define alias
        Target = self.NoteBookPage[2]
        
        #build the central frame
        self.FileFrame = ttk.Frame(Target, padding = self.padding)
    
        #place and configure it
        self.FileFrame.grid(row = 1,
                            column = 1)
        
        #configure the suroundings
        Target.grid_columnconfigure(0,weight = 1)
        Target.grid_columnconfigure(2,weight = 1)
        Target.grid_rowconfigure(0,weight = 1)
        Target.grid_rowconfigure(2,weight = 1)
    
        self.FileFrame.grid_columnconfigure(1,weight = 1)
        
        #element matrix to be appended that will be placed
        #automatically at the end of this function through a loop
        self.PoisitionMatrix = []
    
    
        #add all labels
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Z Range:',
                                               anchor = tk.E,
                                               font = self.ClassFont,
                                               padding = self.padding),
                                     0,
                                     0,
                                     tk.N+tk.S+tk.E+tk.W,
                                     1,
                                     1])
    
    
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text=self.DataClass.Info.GetInfo(Name = 'Z range')[1]+' '+
                                                self.DataClass.Info.GetInfo(Name = 'Z range')[2],
                                               justify=tk.LEFT
                                               ),
                                     0,
                                     1,
                                     tk.N+tk.S+tk.E+tk.W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'X Range:',
                                               anchor = tk.E,
                                               font = self.ClassFont,
                                               padding = self.padding),
                                     1,
                                     0,
                                     tk.N+tk.S+tk.E+tk.W,
                                     1,
                                     1])
        
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text=self.DataClass.Info.GetInfo(Name = 'X range')[1]+' '+self.DataClass.Info.GetInfo(Name = 'X range')[2],
                                               justify=tk.LEFT,
                                               ),
                                     1,
                                     1,
                                     tk.N+tk.S+tk.E+tk.W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Y Range',
                                               anchor = tk.E,
                                               font = self.ClassFont,
                                               padding = self.padding),
                                     2,
                                     0,
                                     tk.N+tk.S+tk.E+tk.W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text=self.DataClass.Info.GetInfo(Name = 'Y range')[1]+' '+self.DataClass.Info.GetInfo(Name = 'Y range')[2],
                                               justify=tk.LEFT,
                                               ),
                                     2,
                                     1,
                                     tk.N+tk.S+tk.E+tk.W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Temperature Range:',
                                               anchor = tk.E,
                                               font = self.ClassFont,
                                               padding = self.padding),
                                     3,
                                     0,
                                     tk.N+tk.S+tk.E+tk.W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text=self.DataClass.Info.GetInfo(Name = 'Temperature range')[1]+' '+self.DataClass.Info.GetInfo(Name = 'Temperature range')[2],
                                               justify=tk.LEFT,
                                               ),
                                     3,
                                     1,
                                     tk.N+tk.S+tk.E+tk.W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Raman Range:',
                                               anchor = tk.E,
                                               font = self.ClassFont,
                                               padding = self.padding),
                                     4,
                                     0,
                                     tk.N+tk.S+tk.E+tk.W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text=self.DataClass.Info.GetInfo(Name = 'Raman Range')[1]+' '+
                                               self.DataClass.Info.GetInfo(Name = 'Raman Range')[2],
                                               justify=tk.LEFT,
                                               ),
                                     4,
                                     1,
                                     tk.N+tk.S+tk.E+tk.W,
                                     1,
                                     1])
                                     
                                     
        #place everything
        for i in range(0,len(self.PoisitionMatrix)):
        
            self.PoisitionMatrix[i][0].grid(row         =  self.PoisitionMatrix[i][1],
                                            column      =  self.PoisitionMatrix[i][2],
                                            sticky      =  self.PoisitionMatrix[i][3],
                                            rowspan     =  self.PoisitionMatrix[i][4],
                                            columnspan  =  self.PoisitionMatrix[i][5])

    
    def BuildSample(self):
    
        '''
        ##########################################
        
        the method self.Data.Info.Call('value')
        will be used to fetch the proper element
        ##########################################
        '''

        #define alias
        Target = self.NoteBookPage[3]
        
        #build the central frame
        self.FileFrame = ttk.Frame(Target, padding = self.padding)
    
        #place and configure it
        self.FileFrame.grid(row = 1,
                            column = 1)
        
        #configure the suroundings
        Target.grid_columnconfigure(0,weight = 1)
        Target.grid_columnconfigure(2,weight = 1)
        Target.grid_rowconfigure(0,weight = 1)
        Target.grid_rowconfigure(2,weight = 1)
    
        self.FileFrame.grid_columnconfigure(1,weight = 1)
        
        #element matrix to be appended that will be placed
        #automatically at the end of this function through a loop
        self.PoisitionMatrix = []
    
    
        #add all labels
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Sample ID:',
                                               anchor = tk.E,
                                               font = self.ClassFont,
                                               padding = self.padding),
                                     0,
                                     0,
                                     tk.N+tk.S+tk.E+tk.W,
                                     1,
                                     1])
    
        
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text=self.DataClass.Info.GetInfo(Name = 'Sample ID')[1],
                                               justify=tk.LEFT,
                                               wraplength = 300
                                               ),
                                     0,
                                     1,
                                     tk.N+tk.S+tk.E+tk.W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Sample Name:',
                                               anchor = tk.E,
                                               font = self.ClassFont,
                                               padding = self.padding),
                                     1,
                                     0,
                                     tk.N+tk.S+tk.E+tk.W,
                                     1,
                                     1])
        
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text=self.DataClass.Info.GetInfo(Name = 'Sample Name')[1],
                                               justify=tk.LEFT,
                                               ),
                                     1,
                                     1,
                                     tk.N+tk.S+tk.E+tk.W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Sample Info:',
                                               anchor = tk.E,
                                               font = self.ClassFont,
                                               padding = self.padding),
                                     2,
                                     0,
                                     tk.N+tk.S+tk.E+tk.W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text=self.DataClass.Info.GetInfo(Name = 'Sample info')[1],
                                               justify=tk.LEFT,
                                               ),
                                     2,
                                     1,
                                     tk.N+tk.S+tk.E+tk.W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Substrate Name:',
                                               anchor = tk.E,
                                               font = self.ClassFont,
                                               padding = self.padding),
                                     3,
                                     0,
                                     tk.N+tk.S+tk.E+tk.W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text=self.DataClass.Info.GetInfo(Name = 'Substrate name')[1],
                                               justify=tk.LEFT,
                                               ),
                                     3,
                                     1,
                                     tk.N+tk.S+tk.E+tk.W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text = 'Substrate Info:',
                                               anchor = tk.E,
                                               font = self.ClassFont,
                                               padding = self.padding),
                                     4,
                                     0,
                                     tk.N+tk.S+tk.E+tk.W,
                                     1,
                                     1])
                                     
        self.PoisitionMatrix.append([ttk.Label(Target,
                                               text=self.DataClass.Info.GetInfo(Name = 'Substrate info')[1],
                                               justify=tk.LEFT,
                                               ),
                                     4,
                                     1,
                                     tk.N+tk.S+tk.E+tk.W,
                                     1,
                                     1])
                                     
                                     
        #place everything
        for i in range(0,len(self.PoisitionMatrix)):
        
            self.PoisitionMatrix[i][0].grid(row         =  self.PoisitionMatrix[i][1],
                                            column      =  self.PoisitionMatrix[i][2],
                                            sticky      =  self.PoisitionMatrix[i][3],
                                            rowspan     =  self.PoisitionMatrix[i][4],
                                            columnspan  =  self.PoisitionMatrix[i][5])
    
    def BuildNotes(self):
    
        '''
        ##########################################
        notes are not installed yet and should be
        added further down the line
        ##########################################
        '''
        pass
    
    
    def close_windows(self):
        
        #output
        VisOut.TextBox(Title = 'Action', Text = 'Closing the information window', state = 1)
        
        #destroy master window
        self.master.destroy()

