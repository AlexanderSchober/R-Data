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
This is associated to a more comprehensive framework for the users. Until verion 5
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





class WarningWindowClass:
    '''
    ####################################################################################
    This class is a simple error messag handler. it will display warning as a window 
    as well as on the terminal. This is importan to understand why some functions
    migght hang on launch when the types of file is not correct.
    ####################################################################################
    '''

    def __init__(self,master,warning):
        
        #output
        VisOut.TextBox(Title = 'Warning', Text = warning, state = 1)
        
        #set master window parameters
        self.master = master
        self.master.resizable(width=False, height=False)
        self.master.title("Warning")
        
        #set the frame
        self.frame = ttk.Frame(self.master, padding = '10px')
        
        #Load logo in the begining
        image           = tk.PhotoImage( file = os.path.join(File.GetRuntimeDir(),'Images','warning.gif'))
        image           = image.subsample(3,3)
        panel           = ttk.Label(self.frame, image = image, width = 80)#,width = 300, height = 100
        panel.image     = image
        panel.grid(row  = 0,column = 0, rowspan = 2)
        
        #set label
        self.Info1 = ttk.Label(self.frame, text =  warning ,justify = tk.LEFT, wraplength = 300)
        
        #pack it
        self.Info1.grid(row = 1, column = 1, columnspan = 2)
    
        #set buttons
        self.quitButton = ttk.Button(self.frame, text = 'OK', command = self.close_windows)
        
        self.quitButton.grid(row = 2, column = 2,sticky = tk.E+tk.W)
        
        #self.frame.bind('<Enter>',self.close_windows)
        
        #pack all
        self.frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    
        #center the window
        self.center()
    
    def close_windows(self):
        
        #output
        VisOut.TextBox(Title = 'Action', Text = 'Closing the warning window', state = 1)
        
        #destroy master window
        self.master.destroy()

    def center(self):
        toplevel = self.master
        toplevel.update_idletasks()
        w = toplevel.winfo_screenwidth()
        h = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = w/2 - size[0]/2
        y = h/2 - size[1]/2
        toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

