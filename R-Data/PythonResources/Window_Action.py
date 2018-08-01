# -*- coding: utf-8 -*-

#-INFO-
#-Name-Main-
#-Version-0.1.01-
#-Last_Modification-17_January_2017-
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

This is the main environement function dedicated

It can launch the following procedure:
- read raw text data files
- read processed data with the associated parameters
- Proces the loaded data 
- launch the display and analysis environnement

An intesive rework was done in version 4 (0.0.4) associated to a visual interface.
This is associated to a more comprehensive Framework for the users. Until verion 5
a lot of unused items should removed from various .py files. Especially the Utility
file should see a major trimming. This will then allow for more comprehensive
debugging in the future.

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

#function manipulation routines
from functools import *


"""
##################################################
These are the custome imports
##################################################
"""


#File and system management routines
import Utility_File     as File

#The terminal viual manager
import Utility_Out      as VisOut


"""
##################################################
These Interface imports. The whole application is 
based on the Tkinter Framework which interfaces 
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
##################################################
CLASS: ActionPrompt

DESCRIPTION:

This class was created to allow quicker access to 
the actual treatment components.

o------------------------------------------------o

PARAMETERS:

- None

##################################################
'''

class Action_Prompt:
    
    '''
    ##################################################
    FUNCTION: __init__
    
    DESCRIPTION:
    
    This will initialise the Windiw manager class and
    send out the first request.
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - None
    
    ##################################################
    '''
    def __init__(self, Window_Manager, Parent):
        
        ##############################################
        #Local pointers
        self.Parent         = Parent
        self.Window_Manager = Window_Manager
    
    
    '''
    ##################################################
    FUNCTION: Init_Window
    
    DESCRIPTION:
    
    This will initialise the Windiw manager class and
    send out the first request.
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - None
    
    ##################################################
    '''
    def Init_Window(self, Window):
        
        ##############################################
        #Set Poiters
        self.Window = Window
        self.Root   = self.Window.Root
        
        
        ##############################################
        #window settings
        self.Root.resizable(width=False,
                            height=False)
        
        self.Root.title("Action")
        
        ##############################################
        #set the Frame
        self.Frame = ttk.Frame(self.Root,
                               padding = '10px')
    
        ##############################################
        #Populate the Frame
        self.Populate_Frame()
        
    '''
    ##################################################
    FUNCTION: Init_Parameters
    
    DESCRIPTION:
    
    Parameter initialisation routine. This is in the 
    hope of standardising the desing
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - None
    
    ##################################################
    '''
    def Init_Parameters(self):
    
    
        pass
    
    '''
    ##################################################
    FUNCTION: Populate_Frame
    
    DESCRIPTION:
    
    This routine will set the initial frame nicely.
    The main window is just a logo place holder
    with the menue and therefore has no function.
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - None
    
    ##################################################
    '''
    def Populate_Frame(self):
        
        #Import all the images
        ContourImage = Image.open(os.path.join(File.GetRuntimeDir(),
                                               'Images',
                                               'Contour.jpg'))
                                               
        ContourImage = ContourImage.resize((80, 80),
                                           Image.ANTIALIAS)
                                           
        ContourImage = ImageTk.PhotoImage(ContourImage)
        
        CascadeImage = Image.open(os.path.join(File.GetRuntimeDir(),
                                               'Images',
                                               'Cascade.png'))
                                               
        CascadeImage = CascadeImage.resize((80, 80),
                                           Image.ANTIALIAS)
                                           
        CascadeImage = ImageTk.PhotoImage(CascadeImage)
        
        PCANMFImage  = Image.open(os.path.join(File.GetRuntimeDir(),
                                               'Images',
                                               'PCANMF.jpg'))
                                               
        PCANMFImage  = PCANMFImage.resize((80, 80),
                                          Image.ANTIALIAS)
                                          
        PCANMFImage  = ImageTk.PhotoImage(PCANMFImage)
        
        FittingImage = Image.open(os.path.join(File.GetRuntimeDir(),
                                               'Images',
                                               'Fiting.jpg'))
                                               
        FittingImage = FittingImage.resize((80, 80),
                                           Image.ANTIALIAS)
                                           
        FittingImage = ImageTk.PhotoImage(FittingImage)
        
        InfoImage    = Image.open(os.path.join(File.GetRuntimeDir(),
                                               'Images',
                                               'Info.jpg'))
                                               
        InfoImage    = InfoImage.resize((80, 80), Image.ANTIALIAS)
        
        InfoImage    = ImageTk.PhotoImage(InfoImage)
        
        ##############################
        #set The Contour Button
        self.ContourButton = tk.Button(self.Frame,
                                       image = ContourImage,
                                       command = partial(self.Close_Window,0),
                                       padx = 5,
                                       pady = 5)
                                       
        self.ContourButton.image = ContourImage
        self.ContourButton.grid(row = 1, column = 0,sticky = tk.E+tk.W)
        
        ##############################
        #set The Contour Button
        self.CascadeButton = tk.Button(self.Frame,
                                       image = CascadeImage,
                                       command = partial(self.Close_Window,1),
                                       padx = 5,
                                       pady = 5)
                                       
        self.CascadeButton.image = CascadeImage
        self.CascadeButton.grid(row = 1, column = 1,sticky = tk.E+tk.W)
        
        ##############################
        #set The PCA NMF Button
        self.PCANMFButton = tk.Button(self.Frame,
                                       image = PCANMFImage,
                                       command = partial(self.Close_Window,2),
                                       padx = 5,
                                       pady = 5)
                                       
        self.PCANMFButton.image = PCANMFImage
        self.PCANMFButton.grid(row = 1, column = 2,sticky = tk.E+tk.W)
        
        ##############################
        #set The Fitting Button
        self.FitButton = tk.Button(self.Frame,
                                       image = FittingImage,
                                       command = partial(self.Close_Window,3),
                                       padx = 5,
                                       pady = 5)
                                       
        self.FitButton.image = FittingImage
        self.FitButton.grid(row = 1, column = 3,sticky = tk.E+tk.W)
        
        ##############################
        #set The Fitting Button
        self.InfoButton = tk.Button(self.Frame,
                                       image = InfoImage,
                                       command = partial(self.Close_Window,4),
                                       padx = 5,
                                       pady = 5)
                                       
        self.InfoButton.image = InfoImage
        self.InfoButton.grid(row = 1, column = 4,sticky = tk.E+tk.W)
        
        #pack all
        self.Frame.pack(side=tk.BOTTOM,
                        fill=tk.BOTH,
                        expand=True)

        ##############################################
        #Set positioning
        self.Window.Place( ['Center',
                            'Center'])
    
    
    '''
    ##################################################
    FUNCTION: Close_Window
    
    DESCRIPTION:
    
    Send it out and force window closing.
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - ActionIndex; which funciton to activate
    
    ##################################################
    '''
    def Close_Window(self, ActionIndex):
        
        #se the launching array
        Launcher = [self.Parent.Launch_Contour,
                    self.Parent.Launch_Cascade,
                    self.Parent.Launch_PCA,
                    self.Parent.Launch_Fit,
                    self.Parent.Info]
        #output
        VisOut.TextBox(Title = 'Action', Text = 'Closing the selector window', state = 1)
    
        #Start the kill method
        self.Window.Kill_Window(Force = True)
    
        #send out the proper method
        Launcher[ActionIndex]()
    

