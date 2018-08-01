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

#numpyy mathematical import
import numpy

#Date and time import
import datetime

#matplotlib
import matplotlib

#set at launch the matplotlib import
matplotlib.use("TkAgg")

#######################################
#advanced imports

#threading related imports
from threading import Thread, Event
from Queue import Queue

#function manipulation routines
from functools import *

"""
##################################################
These are the custome imports
##################################################
"""

#General Utility
import Utility_Main     as Utility

#This is the PCA window manager
import Window_PCA       as CPCA

#Contour plotting management system
import Window_Contour   as Contour

#This is the visual for the PCA/NMF rework
import Window_Cascade   as Cascade

#The terminal viual manager
import Utility_Out      as VisOut

#The dataclass management tool
import Data_DataClass   as DataClass

#The Plot Window manager
import Window_Plot      as PlotWindow

#import the simulation interface
import Window_Sim       as RamSimInterface

#File and system management routines
import Utility_File     as File

#load the Manager instances
import Window_Manager

#-------------------------------------------------

#import Windowclases
from Window_RawImport   import MainRawImportWindow

#integrate the button
from Mod_Buttons        import Custome_Button

#load the information window panel
from Window_Info        import InfoWindowClass

#load the warning window
from Window_Warning     import WarningWindowClass

#load the warning window
from Window_Action      import Action_Prompt

#load the warning window
from Window_Browser     import MultiColumnListbox

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
########################################################
version 0.0.4


This function will be run at launch and is the first 
interface that the user will be confronted to. It will
have basic options like import of a dataset and the 
various options. This function will load and construct
the window class.

########################################################
'''

class Main:
    
    
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
    
    def __init__(self):
        

        #Write out to environement
        VisOut.PrintHeader('',20)

        #initalize the window manager
        self.HighLevel_WindowManager = Window_Manager.HighLevel_WindowManager(self)
    
        #initialize the specific class
        self.Main_Window = MainWindow(self.HighLevel_WindowManager, self)
        
        #initialize
        self.HighLevel_WindowManager.Initialize(self.Main_Window)
                                
        #Set the manager to start runing Tkinter backend
        self.HighLevel_WindowManager.Run( )



class MainWindow:
    
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
    FUNCTION: __init__
    
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
                            
        self.Root.title("Raman Manager")
        
        ##############################################
        #declare the Frame
        self.Frame = ttk.Frame(self.Root)
        
        ##############################################
        #declare the Menue
        self.Menu = tk.Menu(self.Root)
        self.Root.config(menu = self.Menu)
        
        ##############################################
        #We call the populators
        
        #Populate the Frame
        self.Populate_Frame()
        
        #Menue populator
        self.Populate_Menue()
        
        ##############################################
        #Pack the Frame
        self.Frame.pack(side = tk.BOTTOM,
                        fill = tk.BOTH,
                        expand = True)

        ##############################################
        #Set positioning
        self.Window.Place( ['Left',
                            'Top'])
    
                
        self.file_opt = options = {}
        options['filetypes']    = [('all files', '.*'),
                                   ('Text Files', '.txt'),
                                   ('Raman Files', '.RAM')]
                                   
        options['initialdir']   = self.PathofInterest
        #options['initialfile']  = 'myfile.txt'
        options['parent']       = self.Root
        options['title']        = 'Select a File'
        
        self.dir_opt = options  = {}
        options['initialdir']   = self.PathofInterest
        options['mustexist']    = False
        options['parent']       = self.Root
        options['title']        = 'Select a Directory'

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

        #invoking the dataclass on setup launch
        self.DataClassList  = []
        self.DataSubMenues  = []
        self.Selected       = 0
        self.Numerator      = 0

        #oath that will be lonked to opening the search path
        self.PathofInterest = os.getcwd()

    
    
    '''
    ##################################################
    FUNCTION: Populate_Menue
    
    DESCRIPTION:
    
    In version 0.0.5 we do visual clean up and 
    introduce everything into the Menus
    
    it will contain:
    - FILE
        - Convert new Raw Data
        - --------------
        - Open Browser
        - Load Processed
        - --------------
        - Settings ... (does not exist yet)
        - --------------
        - Quit the app
        
    - Info
    
    - Analyse
        - Visualize
        - Calculate
        - Fit
    
    - Data
    
    - Help
    
    This menues will allow quicker navigation throuhg
    the different program possibilities.
    o------------------------------------------------o
    
    PARAMETERS:
    
    - None
    
    ##################################################
    '''
    
    def Populate_Menue(self):

    
        ##################################################
        #Here we build the cascade subMenues
        
        self.FileSubMenu      = tk.Menu(self.Menu,
                                        tearoff=False,
                                        bg = 'white')
                                        
        self.InfoSubMenu      = tk.Menu(self.Menu,
                                        tearoff=False,
                                        bg = 'white')
                                        
        self.AnalysisSubMenu  = tk.Menu(self.Menu,
                                        tearoff=False,
                                        bg = 'white')
                                        
        self.DataSubMenu      = tk.Menu(self.Menu,
                                        tearoff=False,
                                        bg = 'white')
                                        
        self.HelpSubMenu      = tk.Menu(self.Menu,
                                        tearoff=False,
                                        bg = 'white')
        
        
        
        ##################################################
        #Here we declare the cascades
    
        self.Menu.add_cascade(label = 'File',
                              menu = self.FileSubMenu)
                              
        self.Menu.add_cascade(label = 'Info',
                              menu = self.InfoSubMenu)
                              
        self.Menu.add_cascade(label = 'Analysis',
                              menu = self.AnalysisSubMenu)
                              
        self.Menu.add_cascade(label = 'Data',
                              menu = self.DataSubMenu)
                              
        self.Menu.add_cascade(label = 'Help',
                              menu = self.HelpSubMenu)
        
    
        ##################################################
        #Add the commands
        
        if File.IsWindows() or File.IsLinux():
            
            self.FileSubMenu.add_command(label = 'Convert New Raw Data ...',
                                         command = self.Load_Raw)
                                         
            self.FileSubMenu.add_separator()
            
            self.FileSubMenu.add_command(label = 'Open Processed Data',
                                         command = self.Load_Processed)
                                         
            self.FileSubMenu.add_command(label = 'Open Data Browser',
                                         command = self.Launch_Browser)
                                         
            self.FileSubMenu.add_separator()
            
            self.FileSubMenu.add_command(label = 'Signal Generator (in work)')
            
            self.FileSubMenu.add_command(label = 'Simulation Generator',
                                         command = self.Launch_Sim_Interface  )
                                         
            self.FileSubMenu.add_command(label = 'Signal Generator (in work)')
            
            self.FileSubMenu.add_separator()
            
            self.FileSubMenu.add_command(label = 'Settings',
                                         command = self.Do_Nothing)
                                         
            self.FileSubMenu.add_command(label = 'Set Input',
                                         command = self.SetIn)
                                         
            self.FileSubMenu.add_command(label = 'Set Output',
                                         command = self.SetOut)
                                         
            self.FileSubMenu.add_separator()
            
            self.FileSubMenu.add_command(label = 'Quit',
                                         command = self.Exit)
            
            self.InfoSubMenu.add_command(label = 'Data Info',
                                         command = self.Info)
                                         
            self.InfoSubMenu.add_command(label = 'Application Info',
                                         command = self.Do_Nothing)
                                         
            self.InfoSubMenu.add_command(label = 'Developer Info',
                                         command = self.Do_Nothing)
            
            self.AnalysisSubMenu.add_command(label = 'Visualize Contour',
                                             command = partial(self.Launch_Contour))
                                             
            self.AnalysisSubMenu.add_command(label = 'Visualize Cascade',
                                             command = partial(self.Launch_Cascade))
                                             
            self.AnalysisSubMenu.add_command(label = 'Launch PCA/NMF',
                                             command = partial(self.Launch_PCA))
                                             
            self.AnalysisSubMenu.add_command(label = 'Launch Fit',
                                             command = partial(self.Launch_Fit))
            
            self.DataSubMenu.add_command(label = 'Loaded Datasets ...',
                                         state = tk.DISABLED)
            
            self.HelpSubMenu.add_command(label = 'How To',
                                         command = self.Do_Nothing)
                                         
            self.HelpSubMenu.add_command(label = 'Version History',
                                         command = self.Do_Nothing)



        
        else:
            
            self.FileSubMenu.add_command(label = 'Convert New Raw Data ...',
                                         command = self.Load_Raw)
                                         
            self.FileSubMenu.add_separator()
            
            self.FileSubMenu.add_command(label = 'Open Processed Data',
                                         command = self.Load_Processed)
                                         
            self.FileSubMenu.add_command(label = 'Open Data Browser',
                                         command = self.Launch_Browser)
                                         
            self.FileSubMenu.add_separator()
            
            self.FileSubMenu.add_command(label = 'Signal Generator (in work)')
            
            self.FileSubMenu.add_command(label = 'Simulation Generator',
                                         command = self.Launch_Sim_Interface  )
            
            self.FileSubMenu.add_command(label = 'Signal Generator (in work)')
            
            self.FileSubMenu.add_separator()
            
            self.FileSubMenu.add_command(label = 'Settings',
                                         command = self.Do_Nothing)
                                         
            self.FileSubMenu.add_command(label = 'Set Input',
                                         command = self.SetIn)
                                         
            self.FileSubMenu.add_command(label = 'Set Output',
                                         command = self.SetOut)
                                         
            self.FileSubMenu.add_separator()
                                         
            self.FileSubMenu.add_command(label = 'Quit',
                                         command = self.Exit)
            
            self.InfoSubMenu.add_command(label = 'Data Info',
                                         command = self.Info)
                                         
            self.InfoSubMenu.add_command(label = 'Application Info',
                                         command = self.Do_Nothing)
                                         
            self.InfoSubMenu.add_command(label = 'Developer Info',
                                         command = self.Do_Nothing)
            
            self.AnalysisSubMenu.add_command(label = 'Visualize Contour',
                                             command = partial(self.Launch_Contour)  )
                                             
            self.AnalysisSubMenu.add_command(label = 'Visualize Cascade',
                                             command = partial(self.Launch_Cascade))
                                             
            self.AnalysisSubMenu.add_command(label = 'Launch PCA/NMF',
                                             command = partial(self.Launch_PCA)  )
                                             
            self.AnalysisSubMenu.add_command(label = 'Launch Fit',
                                             command = partial(self.Launch_Fit)  )

            self.DataSubMenu.add_command(label = 'Loaded Datasets ...',
                                         state = tk.DISABLED)
            
            
            self.HelpSubMenu.add_command(label = 'How To',
                                         command = self.Do_Nothing)
                                         
            self.HelpSubMenu.add_command(label = 'Version History',
                                         command = self.Do_Nothing)
                                         
            
            self.HelpSubMenu.add_command(label = 'How To',
                                         command = self.Do_Nothing)
        

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
        
        ##############################################
        #Load and process logo
        Logo = Image.open(os.path.join(File.GetRuntimeDir(),
                                        'Images',
                                        'R-Data_Logo.jpg'))
                                        
        Logo = Logo.resize((370, 200),
                           Image.ANTIALIAS)
                           
        Logo = ImageTk.PhotoImage(Logo)
        
        ##############################################
        #Create the panel and palce it
        Logo_Panel          = tk.Label(self.Frame,
                                       image = Logo)
        
        Logo_Panel.image    = Logo
        
        Logo_Panel.grid(    row         = 0,
                            column      = 0,
                            columnspan  = 10,
                            rowspan     = 1)
                            
        ##############################################
        #Create the Version apanel and place it
        Version_Panel    = ttk.Label(self.Frame,
                                    text = 'version: '+File.ReadIni(2),
                                    anchor = tk.W)
                                    
        Version_Panel.grid(row          = 1,
                           column       = 0,
                           columnspan   = 10,
                           sticky       = tk.E+tk.W)
    


    '''
    ##################################################
    FUNCTION: Do_Nothing
    
    DESCRIPTION:
    
    Developement placeholder function
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - None
    
    ##################################################
    '''
    def Do_Nothing(self):
        
        pass

    '''
    ##################################################
    FUNCTION: Select
    
    DESCRIPTION:
    
    Select the actual Data Menue item and then rebuild
    the entire menu tree...
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - None
    
    ##################################################
    '''
    def Menu_Select_Data(self, ID):
        
        #set the variable
        self.Selected = ID
    
        #change the text in the label
        self.Menu_Data_Process(ID)
    
    
    '''
    ##################################################
    FUNCTION: Delete
    
    DESCRIPTION:
    
    The menu tree has to be deleted to be reused later
    on properly
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - ID: integer
    
    ##################################################
    '''
    def Menu_Delete(self, ID):
    
        #delete the array element
        del self.DataClassList[ID]
    
        #change selected in case
        if self.Selected < ID or self.Selected == 0:
    
            pass

        elif self.Selected == ID or self.Selected > ID:
            
            self.Selected = ID - 1

        else:
            
            pass

        #rebuild Menues
        self.Menu_Data_Process(self.Selected)
    
    '''
    ##################################################
    FUNCTION: Menu_Data_Process
    
    DESCRIPTION:
    
    This mthods rebuilds the Menue option to allow a
    proper display. It erases all and redraws all 
    elements. This allows for array free regeneration.
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - ID: integer
    
    ##################################################
    '''
    def Menu_Data_Process(self, ID = 0):
        
        #set the selected
        self.Selected = ID
        
        #delete all children in the subMenue
        self.DataSubMenu.delete(0,
                                len(self.DataClassList)+1)
        
        #add the heading
        self.DataSubMenu.add_command(label = 'Loaded Datasets ...',
                                     state = tk.DISABLED)
        
        #initialise the list
        self.DataSubMenues = []
        
        #rebuild it
        for i in range(0, len(self.DataClassList)):
        
            #add the item
            self.DataSubMenues.append(tk.Menu(self.Menu,
                                              tearoff   = False,
                                              bg        = 'white'))
            
            #is this one selected ?
            if self.Selected == i:
            
                try:
                    
                    self.DataSubMenu.add_cascade(label = '•  '+str(self.DataClassList[i].Info.GetInfoVal('Name')),
                                                 menu = self.DataSubMenues[i])
                
                    self.DataSubMenues[i].add_command(label = 'Type: '+str(self.DataClassList[i].Type)+' measurement',
                                                      state = tk.DISABLED)
                                                      
                    self.DataSubMenues[i].add_command(label = 'Measured: '+str(self.DataClassList[i].Info.GetInfoVal('Acquisisiton date'))
                                                      , state = tk.DISABLED)
                                                      
                    self.DataSubMenues[i].add_command(label = 'Processed: '+str(self.DataClassList[i].Info.GetInfoVal('Processing date'))
                                                      , state = tk.DISABLED)
                                                      
                    self.DataSubMenues[i].add_separator()
                
                except:
                
                    self.DataSubMenu.add_cascade(label = '•  Data '+str(i), menu = self.DataSubMenues[i])
        
            else:
                
                try:
                    
                    self.DataSubMenu.add_cascade(label = '  '+str(self.DataClassList[i].Info.GetInfoVal('Name')),
                                                 menu = self.DataSubMenues[i])
                    
                    self.DataSubMenues[i].add_command(label = 'Type: '+str(self.DataClassList[i].Type)+' measurement',
                                                      state = tk.DISABLED)
                                                      
                    self.DataSubMenues[i].add_command(label = 'Measured: '+str(self.DataClassList[i].Info.GetInfoVal('Acquisisiton date')),
                                                      state = tk.DISABLED)
                                                      
                    self.DataSubMenues[i].add_command(label = 'Processed: '+str(self.DataClassList[i].Info.GetInfoVal('Processing date')),
                                                      state = tk.DISABLED)
                                                      
                    self.DataSubMenues[i].add_separator()
                
                except:
                
                    self.DataSubMenu.add_cascade(label = '   Data '+str(i),
                                                 menu = self.DataSubMenues[i])
                        
            self.DataSubMenues[i].add_command(label = 'Select' ,
                                              command = partial(self.Menu_Select_Data , i))
                                              
            self.DataSubMenues[i].add_command(label = 'Delete' ,
                                              command = partial(self.Menu_Delete , i))
                                              
            self.DataSubMenues[i].add_command(label = 'Info'   ,
                                              command = partial(self.Info   , i))

    '''
    ##################################################
    FUNCTION: Load_Raw
    
    DESCRIPTION:
    
    This will ask the user for a folder in which the 
    files are present. It should then allow for loading 
    the files and processing the data.
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - Path: Path string
    
    ##################################################
    '''
    def Load_Raw(self):
        
        #Build infor window dependencies to Root
        self.RequestWindow = tk.Toplevel(self.Root)

        #Create a new dataclass
        self.Phantom = DataClass.Data()
        
        #lanuch the window class dependency
        self.Load_Raw = MainRawImportWindow(self.RequestWindow,
                                            self.Phantom, self)



    '''
    ##################################################
    FUNCTION: Load_Processed
    
    DESCRIPTION:
    
    This instance will load processed text files.
    This includes all file types and the manager
    should then determine which type it is before 
    doing further processing.
    
    version 0.1.01 introduced a new check to aoid 
    deleting a loaded dataset without the
    remote chance of loading a new one.
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - Path: Path string
    
    ##################################################
    '''

    def Load_Processed(self,Path = None):
        
        ######################################################
        #zmpty path
        if Path == None:
        
            #interface to ask for path
            Paths = tkFileDialog.askopenfilenames( **self.file_opt)
        
            print Paths
        ######################################################
        #full path
        for Path in Paths:
            
            #check if the path corresponds to a file
            if File.IsFile(Path):
                
                #Create a new dataclass
                self.DataClassList.append(DataClass.Data())
            
                #Routine to load the actual fil
                VisOut.TextBox(Title='log',Text = self.DataClassList[-1].Load(Path),
                               L = 20,
                               state = 1,
                               close = False)
            
                #push it out
                VisOut.TextBox(Title='log',Text = 'Raman depth measurement file was loaded from:\n'+Path,
                               L = 20,
                               state = 1,
                               close = False)
                
                #process the submenu
                self.Menu_Data_Process(ID = len(self.DataClassList) - 1)
            
            else:
            
                pass

        ######################################################
        #prompt the user what to do:
        
        #let us add a window manager as a differnet group
        self.Action_Prompt_Manager = self.Window_Manager.Add_Manager()
        
        #create the window
        self.Action_Prompt_Window = self.Action_Prompt_Manager.Add_Window()
        
        #initialise the class
        self.Action_Prompt_Class = Action_Prompt(Action_Prompt,
                                                 self)
        
        #Link the class to it
        self.Action_Prompt_Window.Link_to_Class(self.Action_Prompt_Class)

    def Launch_Browser(self):
        
        '''
        ######################################################
        This invokes the PCA method from version 0.0.3 and we be updated very soon.
        
        For now this method is enought...
        ######################################################    
        '''
        
        #let us add a window manager as a differnet group
        self.Browser_Window_Manager = self.Window_Manager.Add_Manager()
        
        #create the window
        self.Browser_Window = self.Browser_Window_Manager.Add_Window()
        
        #initialise the class
        self.Browser_Class = MultiColumnListbox(self.Browser_Window_Manager,
                                                self)
        
        #Link the class to it
        self.Browser_Window.Link_to_Class(self.Browser_Class)
    
    
    def Launch_Sim_Interface(self):
        
        '''
        ######################################################
        This method is there to launch the simulation script generator
        ######################################################    
        '''

        EditorWindow = tk.Toplevel(self.Root)
        
        SimulationInterface = RamSimInterface.SimulationEditor(EditorWindow)
        

    def Launch_PCA(self):
        
        '''
        ######################################################
        This invokes the PCA method from version 0.0.3 and we be updated very soon.
        
        For now this method is enought...
        ######################################################    
        '''
        
        #set the processing ID
        ID = self.Selected
        
        if  not self.DataClassList[ID].isLoaded:
        
            #set warning
            warning = 'No Data has been loaded...\nPlease load a processed data set using the Load Proc. button.'
            
            #Build infor window dependencies to Root
            self.WarningWindow = tk.Toplevel(self.Root)
        
            #lanuch the window class dependency
            self.temp = WarningWindowClass(self.WarningWindow,warning)
        
        elif self.DataClassList[ID].Type == 'Single':
            
            #set warning
            warning = 'Single Spectrum loaded...\nPlease load a multifile set using the Load Proc. button.'
            
            #Build infor window dependencies to Root
            self.WarningWindow = tk.Toplevel(self.Root)
        
            #lanuch the window class dependency
            self.temp = WarningWindowClass(self.WarningWindow,warning)
        else:
            Debug = 0
            CPCA.RamanDepthPCA(self.DataClassList[ID],self.Root)
    

    def Launch_Contour(self):
        
        '''
        ######################################################
        This invokes the contour method from version 0.0.2 and we be updated very soon. 
        
        For now this method is enought...
        
        ######################################################    
        '''
        
        #set the processing ID
        ID = self.Selected
        
        if  not self.DataClassList[ID].isLoaded:
        
            #set warning
            warning = 'No Data has been loaded...\nPlease load a processed data set using the Load Proc. button.'
            
            #Build infor window dependencies to Root
            self.WarningWindow = tk.Toplevel(self.Root)
        
            #lanuch the window class dependency
            self.temp = WarningWindowClass(self.WarningWindow,warning)
        
        elif self.DataClassList[ID].Type == 'Single':
            
            #set warning
            warning = 'Single Spectrum loaded...\nPlease load a multifile set using the Load Proc. button.'
            
            #Build infor window dependencies to Root
            self.WarningWindow = tk.Toplevel(self.Root)
        
            #lanuch the window class dependency
            self.temp = WarningWindowClass(self.WarningWindow,warning)
        
        else:
            Debug = 0
            Contour.DrawContour(self.DataClassList[ID],Debug)


    def Launch_Cascade(self):
        
        '''
        ######################################################
        This invokes the contour method from version 0.0.2 and we be updated very soon. 
        
        For now this method is enought...
        
        ######################################################    
        '''
        
        #set the processing ID
        ID = self.Selected
        
        if  not self.DataClassList[ID].isLoaded:
        
            #set warning
            warning = 'No Data has been loaded...\nPlease load a processed data set using the Load Proc. button.'
            
            #Build infor window dependencies to Root
            self.WarningWindow = tk.Toplevel(self.Root)
        
            #lanuch the window class dependency
            self.temp = WarningWindowClass(self.WarningWindow,warning)
        
        elif self.DataClassList[ID].Type == 'Single':
            
            #set warning
            warning = 'Single Spectrum loaded...\nPlease load a multifile set using the Load Proc. button.'
            
            #Build infor window dependencies to Root
            self.WarningWindow = tk.Toplevel(self.Root)
        
            #lanuch the window class dependency
            self.temp = WarningWindowClass(self.WarningWindow,warning)
        
        else:
            
            Debug = 0
            
            Cascade.DrawCascade(self.DataClassList[ID],Debug)

    def Launch_Fit(self):
        
        '''
        ######################################################
        This function will launch the fit manager. he was the 
        first instance to have window
        management built in since version 0.0.3
        ######################################################
        '''
        
        #set the processing ID
        ID = self.Selected
        
        #create the main class
        PlotWindow.Main_Fit_Class(self.Window_Manager,
                                  self.DataClassList[ID])
        
        
        VisOut.TextBox(Title='Action',Text = 'Launched Fitting Routine',L = 20,state = 1,close = False)

    def Info(self):
        
        '''
        ######################################################
        On click of the Build method a new window will be spawned containing
        the current informations of the loaded sample file if they exist. 
        
        
        Note that anyway all files loaded into this fitting programm will
        have been processed beforehand. 
        
        We could think of adding a special feature before to allow for 
        automatic compilation and data class creation
        
        like FitWindow -File should create autamitcally the work....
        later maybe version 4
        
        ######################################################
        '''
        
        #set the processing ID
        ID = self.Selected
        
        if  not self.DataClassList[ID].isLoaded:
            
            #set warning
            warning = 'No Data has been loaded...\nPlease load a processed data set using the Load Proc. button.'
            
            #Build infor window dependencies to Root
            self.WarningWindow = tk.Toplevel(self.Root)
            
            #lanuch the window class dependency
            self.temp = WarningWindowClass(self.WarningWindow,warning)
        
        else:
        
            #Build infor window dependencies to Root
            self.InfoWindow = tk.Toplevel(self.Root)
            
            #lanuch the window class dependency
            self.app2 = InfoWindowClass(self.InfoWindow,self.DataClassList[ID])

    def Exit(self):
        
        '''
        ######################################################
        Close the main window and exit the app
        ######################################################    
        '''
        
        #output
        VisOut.TextBox(Title = 'Action', Text = 'Closing Application', state = 1)
        
        #destroy Master window
        self.Root.destroy()
        
    def SetIn(self):
        
        '''
        ######################################################
        This routine will ask for a folder to be set default in folder
        ######################################################    
        '''
        DirName =  tkFileDialog.askdirectory(**self.dir_opt)
        File.SetIni(DirName,0)
        VisOut.TextBox(Title='log',Text = 'Set the default in folder to '+DirName,L = 20,state = 1,close = False)
    
    def SetOut(self):
        
        '''
        ######################################################
        This will ask for a folder to be set dfault out folder.
        ######################################################    
        '''
        DirName =  tkFileDialog.askdirectory(**self.dir_opt)
        File.SetIni(DirName,1)
        VisOut.TextBox(Title='log',Text = 'Set the default out folder to '+DirName,L = 20,state = 1,close = False)
