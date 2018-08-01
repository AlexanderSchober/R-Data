# -*- coding: utf-8 -*-

#-INFO-
#-Window-Manager-
#-Version-0.1.01-
#-Last_Modification-17_January_2017-
#-Date-22_April_2017-
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

This has two puprposes. The first build a manager class that will keep 
track of windiws, their position, state, parent class. 

The second is to create a standardieation of methods. The initialization


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
##################################################
CLASS: HighLevel_WindowManager

DESCRIPTION:

This class is built in the hope of having a more 
stable and coherent definition of windows. Note
that this allows the main Manager class to check
on windiw presence and access directly the 
routines of it.

The reference HighLevel relates to the main
instance. Another lower level manager will be 
callable but always link back to the low level.

This distinction was made to allow classes to link
back to a specific manager rather the entire main
managing class.

o------------------------------------------------o

PARAMETERS:

- Parent -> Class type structure

##################################################
'''

class HighLevel_WindowManager:
    
    
    '''
    ##################################################
    FUNCTION: __init__
    
    DESCRIPTION:
    
    Initializer of the class, It will immediately call
    the first Managing instance to initialize a first
    window level. This will always be alive as it 
    contains the holder frame.
    
    The manager will also create root of the bat. 
    Tkinter build tge windows with dependance and
    root needs to be initialised from the start.
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - None
    
    ##################################################
    '''
    def __init__(self, Initializer_Class):
        
        #Link the topmost managing class
        self.Initializer_Class = Initializer_Class
        
        #Create the Manager Pointer List
        self.Managers   = []



    '''
    ##################################################
    FUNCTION: Add_Manager
    
    DESCRIPTION:
    
    Initializer of the class, It will immediately call
    the first Managing instance to initialize a first
    window level. This will always be alive as it 
    contains the holder frame.
    
    The manager will also create root of the bat. 
    Tkinter build tge windows with dependance and
    root needs to be initialised from the start.
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - PythonClass: Class it links to
    
    ##################################################
    '''
    def Add_Manager(self, PythonClass = None):
        
        #set master window parameters
        self.Managers.append(LowLevel_WindowManager(self))

        #send it out to the local saving mechanism
        return self.Managers[-1]

    '''
    ##################################################
    FUNCTION: Initialize
    
    DESCRIPTION:
    
    Starts the tkinter main loop and therefore the
    window management and interaction routines such 
    as the event handler. Note that root is the first
    high level window and needs to be set immediately.
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - None
    
    ##################################################
    '''
    def Initialize(self, PythonClass):
        
        
        ##############################################
        #initialise root
        self.Managers.append(Root_WindowManager(self))
        
        #grab back root as wew will need it
        self.Root_Window = self.Managers[0].Windows[0]
        self.Root       = self.Managers[0].Windows[0].Root
        
        ##############################################
        #set the application icon (does not work under mac os X)
        try:
            self.Root.iconbitmap(os.path.join(File.GetRuntimeDir(),
                                              'Images',
                                              'R-Logo.ico'))
        except:
            pass
        ##############################################
        #Python UI class associated to root
        self.Root_Window.Link_to_Class(PythonClass)



    '''
    ##################################################
    FUNCTION: Run
    
    DESCRIPTION:
    
    Starts the tkinter main loop and therefore the
    window management and interaction routines such 
    as the event handler. Note that root is the first
    high level window and needs to be set immediately.
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - None
    
    ##################################################
    '''
    def Run(self, *args):
        
        ##############################################
        #Create the Manager Pointer List
        self.Root.mainloop()

'''
##################################################
CLASS: LowLevel_WindowManager

DESCRIPTION:

This class is built in the hope of having a more 
stable and coherent definition of windows. Note
that this allows the main Manager class to check
on windiw presence and access directly the 
routines of it.

o------------------------------------------------o

PARAMETERS:

- Parent -> Class type structure

##################################################
'''
class LowLevel_WindowManager:
    
    
    '''
    ##################################################
    FUNCTION: __init__
    
    DESCRIPTION:
    
    Initializer of the class. This assumes the the 
    parent manager has already been initialised
    and that the high level root is loaded and defined
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - Parent -> Manager Class
    
    ##################################################
    '''
    def __init__(self,Parent):
        
        #set master window parameters
        self.Parent = Parent

        #define the root pointer
        self.Root   = self.Parent.Root
        
        #Create the Window Pointer List
        self.Windows = []

    '''
    ##################################################
    FUNCTION: Add_Window
    
    DESCRIPTION:
    
    Adds another window besides root
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - None
    
    ##################################################
    '''
    def Add_Window(self):

        #Create the Window Pointer List
        self.Windows.append(Window(self, Root = False))

        #send it out for the instance to save localy
        return self.Windows[-1]


'''
##################################################
CLASS: Root_WindowManager

DESCRIPTION:

This class is to manage the tkinter root window. 
This is a bit more delicate as the window manages
the menue bar and has a specific initialisation.

o------------------------------------------------o

PARAMETERS:

- Parent -> Class type structure

##################################################
'''
class Root_WindowManager:
    
    
    '''
    ##################################################
    FUNCTION: __init__
    
    DESCRIPTION:
    
    Initializer of the class
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - Parent -> Manager Class
    
    ##################################################
    '''
    def __init__(self,Parent):
        
        #set master window parameters
        self.Parent = Parent

        #Create the Window Pointer List
        self.Windows = []
    
        #add the root window
        self.Add_Root()
    

    '''
    ##################################################
    FUNCTION: Add_Root
    
    DESCRIPTION:
    
    Adds the first window root
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - None
    
    ##################################################
    '''
    def Add_Root(self):

        #Create the Window Pointer List
        self.Windows.append(Window(self, Root = True))

    '''
    ##################################################
    FUNCTION: Add_Window
    
    DESCRIPTION:
    
    Adds another window besides root
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - None
    
    ##################################################
    '''
    def Add_Window(self):

        #Create the Window Pointer List
        self.Windows.append(Window(self, Root = False))

        #send it out for the instance to save localy
        return self.Windows[-1]


'''
##################################################
CLASS: LowLevel_WindowManager

DESCRIPTION:

This Class is meant to be the standart window. It
will have some unique characteristics and methods.
For example reading and seting positions such as
saving these positions etc...

o------------------------------------------------o

PARAMETERS:

- Parent -> Class type structure

##################################################
'''
class Window:
    
    
    '''
    ##################################################
    FUNCTION: __init__
    
    DESCRIPTION:
    
    Initializer of the class. Note that if Root is 
    True, the system will not reprocess a new root but
    take the existing one.
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - Parent -> Manager Class
    
    ##################################################
    '''
    def __init__(self,Parent, Root = False):
        
        ##############################################
        #set master window parameters
        self.Parent = Parent
    
        self.Manager = Parent.Parent
    
        ##############################################
        #Process root
        if Root:
    
            self.Root = tk.Tk()
        
        else:
    
            self.Root = tk.Toplevel(self.Manager.Root)
    
    
    
    '''
    ##################################################
    FUNCTION: Link_to_Class
    
    DESCRIPTION:
    
    This function allows the system to establish a 
    link to a defined window class. This can be 
    helpfull to make communication easy.
    
    A try will be made to run the window initializer
    in this class.
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - Python_Class -> Python_Class
    
    ##################################################
    '''
    def Link_to_Class(self,Python_Class):


        #save the class locally
        self.Python_Class = Python_Class
        
        #Developement to be removed
        self.Python_Class.Init_Parameters()
        self.Python_Class.Init_Window(self)
        
        #try to run the initializer
        try:
            
            self.Python_Class.Init_Parameters()
        
        except:
            
            VisOut.TextBox(Title='Warning',
                           Text = 'No initializer for Parameters ',
                           L = 20,
                           state = 1,
                           close = False)
        
        #try to run the initializer
        try:

            self.Python_Class.Init_Window(self)

        except:
            
            VisOut.TextBox(Title='Warning',
                           Text = 'No initializer for window ',
                           L = 20,
                           state = 1,
                           close = False)
                

    '''
    ##################################################
    FUNCTION: Kill_Window
    
    DESCRIPTION:
    
    destroy hte window. Eventually force will be an 
    option to know if the user should be warned again.
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - Python_Class -> Python_Class
    
    ##################################################
    '''
    def Kill_Window(self, Force = True):
        
        #destroy master window
        self.Root.after(50,self.Root.destroy)
#    
#    
#    def On_Closing():
#        pass
#    # if messagebox.askokcancel("Quit", "Do you want to quit?"):
#    #    root.destroy()

    
    '''
    ##################################################
    FUNCTION: Position
    
    DESCRIPTION:
    
    Advanced management of the windows recquires
    placement methods. The inpout will be a tuple and
    contain either strings or integers. 
    
    Strings will be handled as:
    Top
    Center
    Bottom
    Left
    Right
    
    While the integers will simply give the positions
    
    Note that Tkinter functions on widget center
    position, meaning that the width and heigh of the 
    window should be defined prior to that.
    o------------------------------------------------o
    
    PARAMETERS:
    
    - Position -> 2 value array, either string or int
    
    ##################################################
    '''
    
    def Place(self, Position):

        
        ###############################################
        #update all tasks
        self.Root.update_idletasks()
        
        ###############################################
        #grab screen parameters
        Screen_Width    = self.Root.winfo_screenwidth()
        Screen_Height   = self.Root.winfo_screenheight()
        
        ###############################################
        #Windiw size
        Size = tuple(int(_) for _ in self.Root.geometry().split('+')[0].split('x'))
        
        
        ###############################################
        #Proces positioning
        
        #horizontal position
        if Position[0] == 'Left':
            
            Position[0] = 0

        if Position[0] == 'Right':
            
            Position[0] = ( Screen_Width
                           - Size[0] )

        if Position[0] == 'Center':
            
            Position[0] = ( Screen_Width / 2
                           - Size[0]/2)
        
        #vertical position
        if Position[1] == 'Top':
        
            Position[1] = 0
        
        if Position[1] == 'Bot':
            
            Position[1] = ( Screen_Height
                           - Size[1])
        
        if Position[1] == 'Center':
            
            Position[1] = ( Screen_Height / 2
                           - Size[1]/2)
        
        ###############################################
        #send it out
        self.Root.geometry("%dx%d+%d+%d" % (Size[0],Size[1], Position[0], Position[1]))
