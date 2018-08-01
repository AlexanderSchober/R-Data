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

#The terminal viual manager
import Utility_Out      as VisOut

#The dataclass management tool
import Data_DataClass   as DataClass

#File and system management routines
import Utility_File     as File

#-------------------------------------------------

#integrate the button
from Mod_Buttons        import Custome_Button

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



class MainRawImportWindow:
    
    '''
    ####################################################################################
    In an effort to unify the import window into one single class we will extract
    the frames of three provious windows and populate them here into a notebook...
    
    
    ####################################################################################
    '''
    
    def __init__(self,master,DataClass,Parent):
        
        #link the DataClass
        self.DataClass    = DataClass
        self.padding      = '10p'
        self.Parent       = Parent
        
        #set ,aster
        self.master = master
        
        #put the name
        self.master.title("Import Dialog")
        
        #set the frame
        self.frame = ttk.Frame(self.master)
        
        #Build the notebook frame and prepare to populate
        self.BuildNoteBooks()
        
        #call the notebook
        self.frame.grid(row = 0, column = 0, sticky= tk.E+tk.W+tk.N+tk.S)
    
        #give weight...
        self.master.grid_columnconfigure(0, weight = 1)
        self.master.grid_rowconfigure(   0, weight = 1)

    def BuildNoteBooks(self, Location = 0):
        '''
        ####################################################################################
        In order to avoid having millions of buttons before release 0.0.5 we focus on 
        tabs rather than having tons of buttons...
        ####################################################################################    
        '''
        #add notebook capabilities into this frame
        self.NoteBookFrame = ttk.Frame(self.frame, padding= self.padding)
        self.NoteBook      = ttk.Notebook(self.NoteBookFrame)
        
        #build all small frames...
        self.NoteBookPage  = [None] * 4
        self.NoteBookTitle = ['Location','Type', 'Info','Dialog']
        
        self.NoteBookPage[0] = self.PopulateText()
        self.NoteBookPage[1] = self.PopulateType()
        self.NoteBookPage[2] = self.PopulateInfo()
        self.NoteBookPage[3] = self.PopulateLog()

        #Call all the frame populators...
        
        
        #Build the notebooks
        k = 0
        for i in range(0,4):
            self.NoteBook.add(self.NoteBookPage[i],text = self.NoteBookTitle[i] )
        
        #We call the population routine putting all butons and entry fields
        self.NoteBook.grid(row = 0, column = 0, sticky = tk.E+tk.W+tk.N+tk.S)
        
        #give weight...
        self.NoteBookFrame.grid_columnconfigure(0, weight = 1)
        self.NoteBookFrame.grid_rowconfigure(0, weight = 1)
        
        #Place the frame into the main frame...
        self.NoteBookFrame.grid(row = Location ,column = 0 , sticky = tk.E+tk.W+tk.N+tk.S)
        
        #give weight...
        self.frame.grid_columnconfigure(0, weight = 1)
        self.frame.grid_rowconfigure(0, weight = 1)

    def PopulateText(self, Location = 0):
        '''
        ####################################################################################
        Set the text select window here.
        
        To be consistent we will launch a class like the previous tabs...
        ####################################################################################
        '''

        #Define the frame:
        self.TextFrame = ttk.Frame(self.NoteBook, padding= self.padding)
        
        #fetch the frame...
        self.TextframeClass = TxtSelect(self.TextFrame, self.DataClass, self.NoteBook, isWindow = False, Parent = self)
        
        #grid it
        self.TextframeClass.frame.grid(row = 0, column = 0, sticky= tk.E+tk.W+tk.S+tk.N)
        self.TextFrame.grid_columnconfigure(0, weight = 1)
        self.TextFrame.grid_rowconfigure(0, weight = 1)
        
        
        return self.TextFrame


    def PopulateLog(self, Location = 0):
        '''
        ####################################################################################
        To allow for a more coherent interface the log will b displayed in here rather than
        a termainal Window. This will allow for better app implementation...
        ####################################################################################
        '''
        
        #Define the frame:
        self.LogFrame      = ttk.Frame(self.NoteBook, padding= self.padding)
        
        #insert the textfield
        self.LogField = ScrolledText.ScrolledText(master = self.LogFrame, wrap=tk.WORD, height=10, width = 15)
        
        #grid it
        self.LogField.grid(row = 0, column = 0, columnspan = 4, sticky= tk.E+tk.W+tk.N+tk.S)
    
        #We want a progressbar:
        self.pb = ttk.Progressbar(self.LogFrame, orient="horizontal",length=300, mode="determinate")
        self.pb.grid(row = 1, column = 0,columnspan = 3)
        self.pb["value"] = 0
        self.pb["maximum"] = 100
        
        self.pbLabel = ttk.Label(self.LogFrame, text = '00.00%', anchor = tk.CENTER)
        self.pbLabel.grid(row = 1, column = 3, sticky= tk.E+tk.W+tk.N+tk.S)
        
        #insert the selct button
        self.SelectButton = ttk.Button(self.LogFrame, text = 'Close'   , command = self.Close   )
        self.SelectButton.grid(row = 2, column = 1 )
        self.SelectButton = ttk.Button(self.LogFrame, text = 'Previous', command = self.Previous)
        self.SelectButton.grid(row = 2, column = 2 )
        self.SelectButton = ttk.Button(self.LogFrame, text = 'Apply'   , command = self.Process )
        self.SelectButton.grid(row = 2, column = 3 )
        
        self.LogFrame.grid_columnconfigure(0, weight = 1)
        self.LogFrame.grid_rowconfigure(0, weight = 1)
        
        return self.LogFrame

    def PopulateType(self, Location = 0):
        '''
        ####################################################################################
        To allow for a more coherent interface the log will b displayed in here rather than
        a termainal Window. This will allow for better app implementation...
        ####################################################################################
        '''
        
        #Define the frame:
        self.TypeFrame = ttk.Frame(self.NoteBook, padding= self.padding)
        
        #fetch the frame...
        self.TypeframeClass = StrSelect(self.TypeFrame, self.DataClass, self.NoteBook, isWindow = False, Parent = self)
        
        #grid it
        self.TypeframeClass.frame.grid(row = 0, column = 0, sticky= tk.E+tk.W+tk.S+tk.N)
        
        self.TypeFrame.grid_columnconfigure(0, weight = 1)
        self.TypeFrame.grid_rowconfigure(0, weight = 1)
        
        
        return self.TypeFrame

    def PopulateInfo(self, Location = 0):
        '''
        ####################################################################################
        To allow for a more coherent interface the log will b displayed in here rather than
        a termainal Window. This will allow for better app implementation...
        ####################################################################################
        '''
        
        #Define the frame:
        self.InfoFrame = ttk.Frame(self.NoteBook, padding= self.padding)
        
        #fetch the frame...
        self.InfoframeClass = InfoSelect(self.InfoFrame, self.DataClass,self.Parent, isWindow = False, Parent = self)
        
        #grid it
        self.InfoframeClass.frame.grid(row = 0, column = 0, sticky= tk.E+tk.W+tk.S+tk.N)
        
        self.InfoFrame.grid_columnconfigure(0, weight = 1)
        self.InfoFrame.grid_rowconfigure(0, weight = 1)
        
        return self.InfoFrame

    def Close(self):
        '''
        ####################################################################################
        Unilateral window killer can be called by the children through the parent frame
        ####################################################################################
        '''
        #output
        VisOut.TextBox(Title = 'Action', Text = 'Closing Application', state = 1)
                
        #destroy master window
        self.master.destroy()
            
    def Previous(self):
        
        pass

    def Process(self):
        '''
        ####################################################################################
        Launch the calculations in the thread framework
        ####################################################################################
        '''

        #Create the package..
        check = ['Please select ...',
                 'Depth Measurement - only Z',
                 'Line Measurement - only X Y Bound',
                 'Surface Measurement - only X Y Unbound',
                 'Volume Measurement - Z X Y Unbound',
                 'Single Measurement - X Y Z T Bound',
                 'Temperature Measurement - only T ',
                 'Patch Measurement - Othe Variable ']
        
        for i in range(len(check)):
            if self.TypeframeClass.var1.get() == check[i]:
                Select = i
                break
        
        #create the threaded environement
        self.progress = ('%.2f' % float(0)+'%')
        
        #set different communication elements
        self.queue = Queue()
        self.event = Event()
        self.Run   = Thread(target = self.DataClass.LoadRaw,
                            args = (self.TextframeClass.EntryInput.get(),
                                    self.TextframeClass.EntryOutput.get(),
                                    [Select],
                                    self.Parent.Container,
                                    self.event,
                                    self.queue))
        
        #spawn file type request
        self.Run.start()
        
        #launch the process funciton
        self.master.after(20,self.ProcessAdvance)
    
#        self.DataClass.LoadRaw(self.TextframeClass.EntryInput.get(),
#                                    self.TextframeClass.EntryOutput.get(),
#                                    [Select],
#                                    self.Parent.Container,
#                                    )



    def ProcessAdvance(self):
        
        '''
        ######################################################################
        This function was introduced to manage the visual feedback of the 
        processing. 
        
        Later on it was also decided that this should callall the next Steps...
        invokers so to speek
        
        ######################################################################
        '''
        
        error = False
        queueLength = self.queue.qsize()
        
        #print 'I am trying; length is:',queueLength
        A = ''
        
        #empty the queue and keep the last value
        for i in range(0,queueLength):
    
            try:
                A = self.queue.get()
            
            except:
                error = True
                break
        
        
        #try to do things
        if not A =='':
        
            #I0f the last queue element is 'Stop' we stop and we call the
            #Whatnext manager
            if A == 'Stop':
            
                #proceed to visuals 100%
                self.pbLabel.config(text = '100.00%')
                self.pb["value"] = 100
            
            #Else we do the necessary changes to the signalers
            else:
            
                #try to change the visual.
                try:

                    #start the update
                    self.pbLabel.config(text = str(('%.2f' % float(A)+'%')))
                    
                    #set progressbar
                    self.pb["value"] = float(A)
                    
                    #restart listener
                    self.master.after(20,self.ProcessAdvance)
            

                except:
                    pass
        
        else:
            self.master.after(20,self.ProcessAdvance)

class StrSelect:
    
    '''
    ####################################################################################
    This window instance asks the user what the file type is to be injected later into
    the data processing method.
    
    the result should be retunr and call a children destroy method
    ####################################################################################
    '''
    
    def __init__(self,master,DataClass,WindowClass,textString = 'Nothing selected yet...', isWindow = True, Parent = None):
        
        #link the DataClass
        self.DataClass    = DataClass
        self.WindowClass  = WindowClass
        self.isWindow     = isWindow
        self.Parent       = Parent
        
        
        self.textString   = textString
        self.Pos          = [0,0,len(textString),len(textString)]
        
        #set ,aster
        self.master = master
        
        if self.isWindow:
            self.master.title("Specify strings around the values")
        
        #set the frame
        self.frame = ttk.Frame(self.master)
        
        self.Info = ttk.Label(self.frame, text = 'Specify the measurement type')
        self.Info = ttk.Label(self.frame, text = 'Using the buttons specify the strings\nbefore and after the values of interest')
        
        #create the drop down selection
        lst1 = ['Please select ...','Depth Measurement - only Z','Line Measurement - only X Y Bound','Surface Measurement - only X Y Unbound','Volume Measurement - Z X Y Unbound','Single Measurement - X Y Z T Bound','Temperature Measurement - only T ','Patch Measurement - Othe Variable ']
        
        self.var1 = tk.StringVar()
        
        TextLabel_1 = ttk.Label( self.frame, text = 'Please select the measurement type that we are investigating. Currently only Depth and temperature measurements are supported.', wraplength = 400, anchor = tk.W)
        drop = ttk.OptionMenu(self.frame,self.var1,*lst1)
        TextLabel_2 = ttk.Label( self.frame, text = 'Using the corresponding buttons on the left hand side navigate the different cursor in the text to select identify the variable. For the software to recognize the numerical value, a constant string before and after it are recquired.', wraplength = 400, anchor = tk.W)
        
        
        TextLabel_1.grid(row = 0, column = 0, columnspan = 4,sticky= tk.E+tk.W)
        drop.grid(row = 1, column = 0, columnspan = 1,sticky= tk.E+tk.W)
        TextLabel_2.grid(row = 2, column = 0, columnspan = 4,sticky= tk.E+tk.W)
        
        #Place these options into a special frame...
        self.StrSelectFrame = ttk.Frame(self.frame)
        
        #grid it
        self.Button  = [None]*9
        self.Button1 = [None]*8
        
        ButtonRow1 = 4
        RowOffset1 = 0
        ButtonRow2 = 2
        RowOffset2 = 0
        
        ButtonWidth  = 50
        ButtonHeight = 10
        
        #set Labels
        self.Label     = ttk.Label( self.StrSelectFrame, text = self.textString , anchor = tk.CENTER)
        self.LabelT_0  = ttk.Label( self.StrSelectFrame, text = 'Before: '      , anchor = tk.E)
        self.LabelT_1  = ttk.Label( self.StrSelectFrame, text = 'Constant: '    , anchor = tk.E)
        self.LabelT_2  = ttk.Label( self.StrSelectFrame, text = 'Value: '       , anchor = tk.E)
        self.LabelT_3  = ttk.Label( self.StrSelectFrame, text = 'Constant: '    , anchor = tk.E)
        self.LabelT_4  = ttk.Label( self.StrSelectFrame, text = 'After: '       , anchor = tk.E)

        self.LabelV_0  = ttk.Label( self.StrSelectFrame, text = ''              , anchor = tk.W)
        self.LabelV_1  = ttk.Label( self.StrSelectFrame, text = ''              , anchor = tk.W)
        self.LabelV_2  = ttk.Label( self.StrSelectFrame, text = ''              , anchor = tk.W)
        self.LabelV_3  = ttk.Label( self.StrSelectFrame, text = ''              , anchor = tk.W)
        self.LabelV_4  = ttk.Label( self.StrSelectFrame, text = ''              , anchor = tk.W)
        
        ##########################################
        ##########################################
        #Set the buttons
        self.Button[0] = Custome_Button(self.StrSelectFrame,
                                        ImagePath   = os.path.join(File.GetRuntimeDir(),
                                                                   'Images',
                                                                   'Left_normal_1.jpg'),
                                        width       = ButtonWidth,
                                        height      = ButtonHeight,
                                        command     = partial(self.Back,0))
                                       
                                       
        self.Button[1] = Custome_Button(self.StrSelectFrame,
                                        ImagePath   = os.path.join(File.GetRuntimeDir(),
                                                                   'Images',
                                                                   'Right_normal_1.jpg'),
                                        width       = ButtonWidth,
                                        height      = ButtonHeight,
                                        command     = partial(self.Front,0))
                                       
        self.Button[2] = Custome_Button(self.StrSelectFrame,
                                        ImagePath   = os.path.join(File.GetRuntimeDir(),
                                                                   'Images',
                                                                   'Left_normal_2.jpg'),
                                        width       = ButtonWidth,
                                        height      = ButtonHeight,
                                        command     = partial(self.Back,1))
        
        self.Button[3] = Custome_Button(self.StrSelectFrame,
                                        ImagePath   = os.path.join(File.GetRuntimeDir(),
                                                                   'Images',
                                                                   'Right_normal_2.jpg'),
                                        width       = ButtonWidth,
                                        height      = ButtonHeight,
                                        command     = partial(self.Front,1))
        
        self.Button[4] = Custome_Button(self.StrSelectFrame,
                                        ImagePath   = os.path.join(File.GetRuntimeDir(),
                                                                   'Images',
                                                                   'Left_normal_3.jpg'),
                                        width       = ButtonWidth,
                                        height      = ButtonHeight,
                                        command     = partial(self.Back,2))
        
        self.Button[5] = Custome_Button(self.StrSelectFrame,
                                        ImagePath   = os.path.join(File.GetRuntimeDir(),
                                                                   'Images',
                                                                   'Right_normal_3.jpg'),
                                        width       = ButtonWidth,
                                        height      = ButtonHeight,
                                        command     = partial(self.Front,2))
        
        self.Button[6] = Custome_Button(self.StrSelectFrame,
                                        ImagePath   = os.path.join(File.GetRuntimeDir(),
                                                                   'Images',
                                                                   'Left_normal_4.jpg'),
                                        width       = ButtonWidth,
                                        height      = ButtonHeight,
                                        command     = partial(self.Back,3))
        
        self.Button[7] = Custome_Button(self.StrSelectFrame,
                                       ImagePath    = os.path.join(File.GetRuntimeDir(),
                                                                   'Images',
                                                                   'Right_normal_4.jpg'),
                                       width        = ButtonWidth,
                                       height       = ButtonHeight,
                                       command      = partial(self.Front,3))
        
        ##########################################
        ##########################################
        
        self.Button1[0] = Custome_Button(self.StrSelectFrame,
                                         ImagePath  = os.path.join(File.GetRuntimeDir(),
                                                                   'Images',
                                                                   'Left_Double_1.jpg'),
                                         width      = ButtonWidth,
                                         height     = ButtonHeight,
                                         command    = partial(self.Back10,0))
                                       
        self.Button1[1] = Custome_Button(self.StrSelectFrame,
                                         ImagePath  = os.path.join(File.GetRuntimeDir(),
                                                                   'Images',
                                                                   'Right_double_1.jpg'),
                                         width      = ButtonWidth,
                                         height     = ButtonHeight,
                                         command    = partial(self.Front10,0))
        
        self.Button1[2] = Custome_Button(self.StrSelectFrame,
                                         ImagePath  = os.path.join(File.GetRuntimeDir(),
                                                                   'Images',
                                                                   'Left_double_2.jpg'),
                                         width      = ButtonWidth,
                                         height     = ButtonHeight,
                                         command    = partial(self.Back10,1))
        
        self.Button1[3] = Custome_Button(self.StrSelectFrame,
                                         ImagePath  = os.path.join(File.GetRuntimeDir(),
                                                                   'Images',
                                                                   'Right_double_2.jpg'),
                                         width      = ButtonWidth,
                                         height     = ButtonHeight,
                                         command    = partial(self.Front10,1))
        
        self.Button1[4] = Custome_Button(self.StrSelectFrame,
                                         ImagePath  = os.path.join(File.GetRuntimeDir(),
                                                                    'Images',
                                                                   'Left_double_3.jpg'),
                                         width      = ButtonWidth,
                                         height     = ButtonHeight,
                                         command    = partial(self.Back10,2))
        
        self.Button1[5] = Custome_Button(self.StrSelectFrame,
                                         ImagePath  = os.path.join(File.GetRuntimeDir(),
                                                                   'Images',
                                                                   'Right_double_3.jpg'),
                                         width      = ButtonWidth,
                                         height     = ButtonHeight,
                                         command    = partial(self.Front10,2))
        
        self.Button1[6] = Custome_Button(self.StrSelectFrame,
                                         ImagePath  = os.path.join(File.GetRuntimeDir(),
                                                                   'Images',
                                                                   'Left_double_4.jpg'),
                                         width      = ButtonWidth,
                                         height     = ButtonHeight,
                                         command    = partial(self.Back10,3))
        
        self.Button1[7] = Custome_Button(self.StrSelectFrame,
                                         ImagePath  = os.path.join(File.GetRuntimeDir(),
                                                                   'Images',
                                                                   'Right_double_4.jpg'),
                                         width      = ButtonWidth,
                                         height     = ButtonHeight,
                                         command    = partial(self.Front10,3))
        
        #pack all
        
        
        #self.Info.grid( row = 2, column = 0 , sticky= tk.E+tk.W)
        
        self.Label.grid(row = 0, column = 0 , columnspan = 10, sticky= tk.E+tk.W)
        
        self.LabelT_0.grid(row = ButtonRow1-1, column = 2 , columnspan = 2, rowspan = 2)
        self.LabelT_1.grid(row = ButtonRow1+1, column = 2 , columnspan = 2, rowspan = 2)
        self.LabelT_2.grid(row = ButtonRow1+3, column = 2 , columnspan = 2, rowspan = 2)
        self.LabelT_3.grid(row = ButtonRow1+5, column = 2 , columnspan = 2, rowspan = 2)
        self.LabelT_4.grid(row = ButtonRow1+7, column = 2 , columnspan = 2, rowspan = 2)
        
        self.LabelV_0.grid(row = ButtonRow1-1, column = 4 , columnspan = 6, sticky= tk.E+tk.W, rowspan = 2)
        self.LabelV_1.grid(row = ButtonRow1+1, column = 4 , columnspan = 6, sticky= tk.E+tk.W, rowspan = 2)
        self.LabelV_2.grid(row = ButtonRow1+3, column = 4 , columnspan = 6, sticky= tk.E+tk.W, rowspan = 2)
        self.LabelV_3.grid(row = ButtonRow1+5, column = 4 , columnspan = 6, sticky= tk.E+tk.W, rowspan = 2)
        self.LabelV_4.grid(row = ButtonRow1+7, column = 4 , columnspan = 6, sticky= tk.E+tk.W, rowspan = 2)
        
        self.Button[0].grid(row = ButtonRow1+0, column = 0+RowOffset1 , columnspan = 1)#, sticky= tk.E+tk.W)
        self.Button[1].grid(row = ButtonRow1+0, column = 1+RowOffset1 , columnspan = 1)#, sticky= tk.E+tk.W)
        self.Button[2].grid(row = ButtonRow1+2, column = 0+RowOffset1 , columnspan = 1)#, sticky= tk.E+tk.W)
        self.Button[3].grid(row = ButtonRow1+2, column = 1+RowOffset1 , columnspan = 1)#, sticky= tk.E+tk.W)
        self.Button[4].grid(row = ButtonRow1+4, column = 0+RowOffset1 , columnspan = 1)#, sticky= tk.E+tk.W)
        self.Button[5].grid(row = ButtonRow1+4, column = 1+RowOffset1 , columnspan = 1)#, sticky= tk.E+tk.W)
        self.Button[6].grid(row = ButtonRow1+6, column = 0+RowOffset1 , columnspan = 1)#, sticky= tk.E+tk.W)
        self.Button[7].grid(row = ButtonRow1+6, column = 1+RowOffset1 , columnspan = 1)#, sticky= tk.E+tk.W)
        
        
        self.Button1[0].grid(row = ButtonRow1+1, column = 0+RowOffset1 , columnspan = 1)#, sticky= tk.E+tk.W)
        self.Button1[1].grid(row = ButtonRow1+1, column = 1+RowOffset1 , columnspan = 1)#, sticky= tk.E+tk.W)
        self.Button1[2].grid(row = ButtonRow1+3, column = 0+RowOffset1 , columnspan = 1)#, sticky= tk.E+tk.W)
        self.Button1[3].grid(row = ButtonRow1+3, column = 1+RowOffset1 , columnspan = 1)#, sticky= tk.E+tk.W)
        self.Button1[4].grid(row = ButtonRow1+5, column = 0+RowOffset1 , columnspan = 1)#, sticky= tk.E+tk.W)
        self.Button1[5].grid(row = ButtonRow1+5, column = 1+RowOffset1 , columnspan = 1)#, sticky= tk.E+tk.W)
        self.Button1[6].grid(row = ButtonRow1+7, column = 0+RowOffset1 , columnspan = 1)#, sticky= tk.E+tk.W)
        self.Button1[7].grid(row = ButtonRow1+7, column = 1+RowOffset1 , columnspan = 1)#, sticky= tk.E+tk.W)
        
        #make the coloumn configure
        self.StrSelectFrame.grid_columnconfigure(9, weight = 1)
        
        #put the button grid
        self.StrSelectFrame.grid(row = 3, column = 0, columnspan = 4, sticky= tk.E+tk.W)
        
        #insert the selct button
        self.SelectButton = ttk.Button(self.frame, text = 'Close',  width = 5, command = self.Close)
        self.SelectButton.grid(row = 5, column = 1 )
        self.SelectButton = ttk.Button(self.frame, text = 'Previous',  width = 5, command = self.Previous)
        self.SelectButton.grid(row = 5, column = 2 )
        self.SelectButton = ttk.Button(self.frame, text = 'Next',  width = 5, command = self.Next)
        self.SelectButton.grid(row = 5, column = 3 )
        
        self.frame.grid_columnconfigure(0, weight = 1)
        self.frame.grid_rowconfigure(4, weight = 1)
        
        #pack all in case this is called as a window
        #otherwise we will just use the frame included self.frame
        if self.isWindow:
            self.frame.pack(padx=20, pady=20, side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def Previous(self):
        
        #jump to before
        self.Parent.NoteBook.select(tab_id = 0)
    
    def Close(self):
        
        #output
        VisOut.TextBox(Title = 'Action', Text = 'Closing Application', state = 1)
                
        #destroy master window
        self.Parent.master.destroy()
    
    def Next(self):
        
        #set temp and leave
        self.DataClass.temp = [self.textString[self.Pos[0]:self.Pos[1]],self.textString[self.Pos[2]:self.Pos[3]]]

        #destroy master window
        self.Parent.NoteBook.select(tab_id = 2)

    def Back(self,Select):
        
        #Put it at right position
        self.Pos[Select] = self.Pos[Select]-1
    
        #Send out the refresh
        self.Refresh()
    
        
    def Front(self,Select):

        #Put it at right position
        self.Pos[Select] = self.Pos[Select]+1

        #Send out the refresh
        self.Refresh()


    def Back10(self,Select):
        
        #Put it at right position
        self.Pos[Select] = self.Pos[Select]-5
    
        #Send out the refresh
        self.Refresh()
    
        
    def Front10(self,Select):

        #Put it at right position
        self.Pos[Select] = self.Pos[Select]+5

        #Send out the refresh
        self.Refresh()
    
    def Refresh(self):


        #check the sanity
        if self.Pos[0] < 0:
    
            self.Pos[0] = 0
        
        if self.Pos[0] > len(self.textString)-4:
        
            self.Pos[0] = len(self.textString)-4
        
        if self.Pos[1] <= self.Pos[0]:
        
            self.Pos[1] = self.Pos[0]+1
        
        if self.Pos[2] <= self.Pos[1]:
        
            self.Pos[2] = self.Pos[1]+1
        
        if self.Pos[3] <= self.Pos[2]:
        
            self.Pos[3] = self.Pos[2]+1


        #build the new texts
        self.TextOut = [None]*6
        
        #Fixed text before:
        self.TextOut[0] = self.textString[0:self.Pos[0]]+'...'
        
        #first fixed:
        self.TextOut[1] = '...'+self.textString[self.Pos[0]:self.Pos[1]]+'...'

        #number of interest
        self.TextOut[2] = '...'+self.textString[self.Pos[1]:self.Pos[2]]+'...'
        
        #Fixed text before:
        self.TextOut[3] = '...'+self.textString[self.Pos[2]:self.Pos[3]]+'...'
        
        #first fixed:
        self.TextOut[4] = '...'+self.textString[self.Pos[3]:len(self.textString)]
        
        self.TextOut[5] = self.textString[0:self.Pos[0]]+'[-1-]'+self.textString[self.Pos[0]:self.Pos[1]]+'[-2-]'+self.textString[self.Pos[1]:self.Pos[2]]+'[-3-]'+self.textString[self.Pos[2]:self.Pos[3]]+'[-4-]'+self.textString[self.Pos[3]:len(self.textString)]

        #update it
        self.LabelV_0.config(text = self.TextOut[0])
        self.LabelV_1.config(text = self.TextOut[1])
        self.LabelV_2.config(text = self.TextOut[2])
        self.LabelV_3.config(text = self.TextOut[3])
        self.LabelV_4.config(text = self.TextOut[4])
        
        self.Label.config(text = self.TextOut[5])


class TxtSelect:
    
    '''
    ####################################################################################
    This window instance asks the user what the file type is to be injected later into
    the data processing method.
    
    the result should be retunr and call a children destroy method
    ####################################################################################
    '''
    
    def __init__(self,
                 master,
                 DataClass,
                 WindowClass,
                 textString = 'Nothing selected yet...',
                 isWindow = True,
                 Parent = None):
        
        ###################################
        #link the DataClass
        self.DataClass    = DataClass
        self.WindowClass  = WindowClass
        self.isWindow     = isWindow
        self.Parent       = Parent
        
        ###################################
        #Set the path variables
        
        #oath that will be lonked to opening the search path
        self.PathofInterest = os.getcwd()
        
        self.file_opt = options = {}
        #options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('Text Files', '.txt'), ('Raman Files', '.RAM')]
        options['initialdir'] = self.PathofInterest
        options['initialfile'] = 'myfile.txt'
        #options['parent'] = self.PathofInterest
        options['title'] = 'Select a File'
        
        self.dir_opt = options = {}
        options['initialdir'] = self.PathofInterest
        options['mustexist'] = False
        #options['parent'] = root
        options['title'] = 'Select a Directory'
        
        
        self.textString   = textString
        self.Pos          = [0,0,len(textString),len(textString)]
        
        ###################################
        #start window management
        
        #set the master
        self.master = master
        
        #set the frame
        self.frame = ttk.Frame(self.master)
        
        #Place these options into a special frame...
        self.StrSelectFrame = ttk.Frame(self.frame)
        
        #set buttons
        self.LabelInput     = ttk.Label( self.StrSelectFrame, text = 'Select the input Path:\nThis consist of telling the software in which folder the Raman spectra are located. Note that nothing else should be contained in this folder as it might result in an error when reading the information from the filename.' ,wraplength = 300, anchor = tk.W)
        self.LabelOutput    = ttk.Label( self.StrSelectFrame, text = 'Select the output path:\nThis is the folder in which the resulting single file processed Raman signal will be stored. If no Path is selected the folder of the input path will be used.',wraplength = 300, anchor = tk.W)
        
        self.LabelInputErr  = ttk.Label( self.StrSelectFrame, text = '' , anchor = tk.W)
        self.LabelOutputErr = ttk.Label( self.StrSelectFrame, text = '' , anchor = tk.W)
        
        self.EntryInput     = ttk.Entry( self.StrSelectFrame, width = 7)
        self.EntryOutput    = ttk.Entry( self.StrSelectFrame, width = 7)
        
        self.ButtonInput    = ttk.Button(self.StrSelectFrame, text = '...', command = partial(self.SelectPath,self.EntryInput))
        self.ButtonOutput   = ttk.Button(self.StrSelectFrame, text = '...', command = partial(self.SelectPath,self.EntryOutput))
        
        self.LabelInput.grid( row = 0, column = 0  , columnspan = 2, sticky= tk.E+tk.W)
        self.LabelOutput.grid(row = 3, column = 0  , columnspan = 2, sticky= tk.E+tk.W)
        
        self.LabelInputErr.grid( row = 2, column = 0  , columnspan = 2, sticky= tk.E+tk.W)
        self.LabelOutputErr.grid(row = 5, column = 0  , columnspan = 2, sticky= tk.E+tk.W)
        
        self.EntryInput.grid( row = 1, column = 0  , columnspan = 1, sticky= tk.E+tk.W)
        self.EntryOutput.grid(row = 4, column = 0  , columnspan = 1, sticky= tk.E+tk.W)
        
        self.ButtonInput.grid( row = 1, column = 1 , columnspan = 2, sticky= tk.E+tk.W)
        self.ButtonOutput.grid(row = 4, column = 1 , columnspan = 2, sticky= tk.E+tk.W)
        
        #make the coloumn configure
        self.StrSelectFrame.grid_columnconfigure(0, weight = 1)
        
        #put the button grid
        self.StrSelectFrame.grid(row = 0, column = 0, columnspan = 4, sticky= tk.E+tk.W)
        
        #insert the selct button
        self.SelectButton = ttk.Button(self.frame, text = 'Close',  width = 5, command = self.Close)
        self.SelectButton.grid(row = 2, column = 1 )
        self.SelectButton = ttk.Button(self.frame, text = 'Clear',  width = 5, command = self.Clear)
        self.SelectButton.grid(row = 2, column = 2 )
        self.SelectButton = ttk.Button(self.frame, text = 'Next',  width = 5, command = self.Next)
        self.SelectButton.grid(row = 2, column = 3 )
        
        self.frame.grid_columnconfigure(0, weight = 1)
        self.frame.grid_rowconfigure(1, weight = 1)
        
        #otherwise we will just use the frame included self.frame
        if self.isWindow:
            self.frame.pack(padx=20, pady=20, side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def Close(self):
        
        #output
        VisOut.TextBox(Title = 'Action', Text = 'Closing Application', state = 1)
                
        #destroy master window
        self.Parent.master.destroy()

    def Clear(self):
        
        #delete a insert into the target field
        self.EntryInput.delete(0,tk.END)
        self.LabelInputErr.config(text='')
    
        #delete a insert into the target field
        self.EntryOutput.delete(0,tk.END)
        self.LabelOutputErr.config(text='')
    
    def SelectPath(self,Target):
        '''
        ####################################################################################
        In version O.1.03 the choice was made to use the file select dialog. This made
        indeed more sense for windows as it the folder dialog is absolutely horrible.
        ####################################################################################
        '''
        
        #Spawn directory request
        FileName =  tkFileDialog.askopenfilename(**self.file_opt)
        
        #now that we have the filename, we have to find it's folder:
        DirName = File.GetFolderName(FileName)
        
        #This imports all filenames cotained in a given folder
        PathList = File.GetFileNames(DirName,'.txt')
        
        #Set the default
        self.dir_opt['initialdir'] = DirName

        #delete a insert into the target field
        Target.delete(0,tk.END)
        Target.insert(0,DirName)

    def Next(self):
        
        #Check for the text str in this folder:
        PathList = File.GetFileNames(self.EntryInput.get(),'.txt')
        
        #grab only raw files
        PathList = File.GrabRenishawRaw(PathList)
        
        try:
            
            #put it in
            self.Parent.TypeframeClass.Label.config( text =  PathList[0].split(os.path.sep)[-1])
            self.Parent.TypeframeClass.textString = PathList[0].split(os.path.sep)[-1]

            #change tab on the notebook
            self.Parent.NoteBook.select(tab_id = 1)
        
            #revert error just in case
            self.LabelInputErr.config(text='')

        except:
            
            #set color to red to show that a problem occured
            self.LabelInputErr.config(text='Invalid input path. Please select another...')




class TypeRequest:
    
    '''
    ####################################################################################
    This window instance asks the user what the file type is to be injected later into
    the data processing method.
    
    the result should be retunr and call a children destroy method
    ####################################################################################
    '''
    
    def __init__(self,master,DataClass,WindowClass):
        
        #link the DataClass
        self.DataClass = DataClass
        self.WindowClass = WindowClass
        
        #set ,aster
        self.master = master
        self.master.title("Specify type...")
        
        #set the frame
        self.frame = tk.Frame(self.master)
        self.Info = tk.Label(self.frame, text = 'Please select the file type \nyou just selected to import')
        
        #pack it
        self.Info.pack()
    
        self.Button = [None]*6
        
        #set buttons
        self.Button[0] = tk.Button(self.frame, text = 'Depth Measurement', width = 25, command = partial(self.Type,0))
        self.Button[1] = tk.Button(self.frame, text = 'Line Measurement', width = 25, command = partial(self.Type,1))
        self.Button[2] = tk.Button(self.frame, text = 'Surface Measurement', width = 25, command = partial(self.Type,2))
        self.Button[3] = tk.Button(self.frame, text = 'Volume Measurement', width = 25, command = partial(self.Type,3))
        self.Button[4] = tk.Button(self.frame, text = 'Single Measurement', width = 25, command = partial(self.Type,4))
        self.Button[5] = tk.Button(self.frame, text = 'Temperature Measurement', width = 25, command = partial(self.Type,5))
        
        #pack all
        self.Button[0].pack()
        self.Button[1].pack()
        self.Button[2].pack()
        self.Button[3].pack()
        self.Button[4].pack()
        self.Button[5].pack()
        
        #pack all
        self.frame.pack(padx=20, pady=20, side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    
    def Type(self,Select):
        
        #output
        VisOut.TextBox(Title = 'Action', Text = 'Selected Type '+str(Select), state = 1)
        
        #Send to window Class
        self.WindowClass.Select = Select
        
        #destroy master window
        self.master.destroy()


class InfoSelect:
    
    '''
    ####################################################################################
    This method is a call to the sample and raman informations. In versions 0.0.1 - 0.0.3
    this was done by the function . The call of this method will be
    canceled in the loading routine.
    ####################################################################################
    '''
    
    def __init__(self,master,DataClass,Container, isWindow = False, Parent = None):
        
        #link the DataClass
        self.DataClass = DataClass
        self.Container = Container
        self.isWindow  = isWindow
        self.Parent    = Parent
        
        #set ,aster
        self.master = master
        
        if isWindow:
            self.master.title("Enter Measurement parameters...")
        
        #set the frame
        self.frame = ttk.Frame(self.master)
        self.Info = ttk.Label(self.frame, text = 'Please enter the measurement parameters. The Raman specifications are to be given in their respective units while the sample specific informations can be given as the user pleases. Note that forward slashes and other python non recommended characters are to be avoided. ',wraplength = 400, anchor = tk.W)
        
        #pack it
        self.Info.grid(row = 0, column = 0, columnspan = 4, sticky = tk.E+tk.W)
    
        #Create a frame for entering the parameters
        self.EtryFrame   = ttk.Frame(self.frame)
        self.EtryFrame_1 = ttk.Frame(self.EtryFrame)
        self.EtryFrame_2 = ttk.Frame(self.EtryFrame)
        
        #Raman Labels
        self.RLabels = [None]*12
        
        #set Raman Labels
        self.RLabels[0]  = ttk.Label(self.EtryFrame_1, text = 'Laser'     , anchor = tk.E)
        self.RLabels[1]  = ttk.Label(self.EtryFrame_1, text = 'Power'     , anchor = tk.E)
        self.RLabels[2]  = ttk.Label(self.EtryFrame_1, text = 'Gratting'  , anchor = tk.E)
        self.RLabels[3]  = ttk.Label(self.EtryFrame_1, text = 'Objective' , anchor = tk.E)
        self.RLabels[4]  = ttk.Label(self.EtryFrame_1, text = 'Duration'  , anchor = tk.E)
        self.RLabels[5]  = ttk.Label(self.EtryFrame_1, text = 'N._Acqu.'  , anchor = tk.E)
        self.RLabels[6]  = ttk.Label(self.EtryFrame_1, text = 'nm'        , anchor = tk.W)
        self.RLabels[7]  = ttk.Label(self.EtryFrame_1, text = 'perc.'     , anchor = tk.W)
        self.RLabels[8]  = ttk.Label(self.EtryFrame_1, text = 'cm-1'      , anchor = tk.W)
        self.RLabels[9]  = ttk.Label(self.EtryFrame_1, text = 'x'         , anchor = tk.W)
        self.RLabels[10] = ttk.Label(self.EtryFrame_1, text = 's'         , anchor = tk.W)
        self.RLabels[11] = ttk.Label(self.EtryFrame_1, text = 'x'         , anchor = tk.W)
        
        
        
        #Place raman Labels
        self.RLabels[0].grid(row = 1,column = 1, sticky = tk.E+tk.W)
        self.RLabels[1].grid(row = 2,column = 1, sticky = tk.E+tk.W)
        self.RLabels[2].grid(row = 3,column = 1, sticky = tk.E+tk.W)
        self.RLabels[3].grid(row = 4,column = 1, sticky = tk.E+tk.W)
        self.RLabels[4].grid(row = 5,column = 1, sticky = tk.E+tk.W)
        self.RLabels[5].grid(row = 6,column = 1, sticky = tk.E+tk.W)
        self.RLabels[6].grid(row = 1,column = 3, sticky = tk.E+tk.W)
        self.RLabels[7].grid(row = 2,column = 3, sticky = tk.E+tk.W)
        self.RLabels[8].grid(row = 3,column = 3, sticky = tk.E+tk.W)
        self.RLabels[9].grid(row = 4,column = 3, sticky = tk.E+tk.W)
        self.RLabels[10].grid(row = 5,column = 3, sticky = tk.E+tk.W)
        self.RLabels[11].grid(row = 6,column = 3, sticky = tk.E+tk.W)
        
        
        #Raman Entries
        self.REntry = [None]*7
        
        #Create Raman entries
        self.REntry[0] = ttk.Entry(self.EtryFrame_1,width = 10)
        self.REntry[1] = ttk.Entry(self.EtryFrame_1,width = 10)
        self.REntry[2] = ttk.Entry(self.EtryFrame_1,width = 10)
        self.REntry[3] = ttk.Entry(self.EtryFrame_1,width = 10)
        self.REntry[4] = ttk.Entry(self.EtryFrame_1,width = 10)
        self.REntry[5] = ttk.Entry(self.EtryFrame_1,width = 10)
        
        #Place Raman entries
        self.REntry[0].grid(row = 1,column = 2)
        self.REntry[1].grid(row = 2,column = 2)
        self.REntry[2].grid(row = 3,column = 2)
        self.REntry[3].grid(row = 4,column = 2)
        self.REntry[4].grid(row = 5,column = 2)
        self.REntry[5].grid(row = 6,column = 2)
        
        #Insert Default Values:
        self.REntry[0].insert(0,'633')
        self.REntry[1].insert(0,'05')
        self.REntry[2].insert(0,'2400')
        self.REntry[3].insert(0,'100')
        self.REntry[4].insert(0,'60')
        self.REntry[5].insert(0,'30')
        
        #Sample Labels
        self.SLabels = [None]*5
        
        #set Sample Labels
        self.SLabels[0] = ttk.Label(self.EtryFrame_2, text = 'ID'        , anchor = tk.E)
        self.SLabels[1] = ttk.Label(self.EtryFrame_2, text = 'Sample'    , anchor = tk.E)
        self.SLabels[2] = ttk.Label(self.EtryFrame_2, text = 'Substrate' , anchor = tk.E)
        self.SLabels[3] = ttk.Label(self.EtryFrame_2, text = 'Sam._Info.', anchor = tk.E)
        self.SLabels[4] = ttk.Label(self.EtryFrame_2, text = 'Sub._Info.', anchor = tk.E)

        #Place Sample Labels
        self.SLabels[0].grid(row = 1,column = 5, sticky = tk.E+tk.W)
        self.SLabels[1].grid(row = 2,column = 5, sticky = tk.E+tk.W)
        self.SLabels[2].grid(row = 3,column = 5, sticky = tk.E+tk.W)
        self.SLabels[3].grid(row = 4,column = 5, sticky = tk.E+tk.W)
        self.SLabels[4].grid(row = 5,column = 5, sticky = tk.E+tk.W)
        
        #Sample Entries
        self.SEntry = [None]*5
        
        #Create Sample entries
        self.SEntry[0] = ttk.Entry(self.EtryFrame_2,width = 10)
        self.SEntry[1] = ttk.Entry(self.EtryFrame_2,width = 10)
        self.SEntry[2] = ttk.Entry(self.EtryFrame_2,width = 10)
        self.SEntry[3] = ttk.Entry(self.EtryFrame_2,width = 10)
        self.SEntry[4] = ttk.Entry(self.EtryFrame_2,width = 10)

        #Place Raman entries
        self.SEntry[0].grid(row = 1,column = 6)
        self.SEntry[1].grid(row = 2,column = 6)
        self.SEntry[2].grid(row = 3,column = 6)
        self.SEntry[3].grid(row = 4,column = 6)
        self.SEntry[4].grid(row = 5,column = 6)
        
        #Insert Default Values:
        self.SEntry[0].insert(0,'NaN')
        self.SEntry[1].insert(0,'NaN')
        self.SEntry[2].insert(0,'NaN')
        self.SEntry[3].insert(0,'NaN')
        self.SEntry[4].insert(0,'NaN')
        
        #grid the frame
        self.EtryFrame_1.grid(row = 4, column = 0, columnspan = 3)
        self.EtryFrame_2.grid(row = 4, column = 3, columnspan = 3)
        
        self.EtryFrame_1.grid_columnconfigure(1, weight = 1)
        self.EtryFrame_2.grid_columnconfigure(5, weight = 1)
        
        #do the name field
        self.NameLabel = [None]*4
        self.NameEntry = [None]*3
        
        self.NameLabel[0] = ttk.Label(self.EtryFrame, text = 'Measurement Name' , anchor = tk.W)
        self.NameLabel[0].grid(row = 0,column = 0, sticky = tk.E+tk.W)
        self.NameLabel[0] = ttk.Label(self.EtryFrame, text = 'Measurement Date' , anchor = tk.W)
        self.NameLabel[0].grid(row = 1,column = 0, sticky = tk.E+tk.W)
        self.NameLabel[0] = ttk.Label(self.EtryFrame, text = 'Processing Date'  , anchor = tk.W)
        self.NameLabel[0].grid(row = 2,column = 0, sticky = tk.E+tk.W)
        self.NameLabel[1] = ttk.Label(self.EtryFrame, text = '' , anchor = tk.W)
        self.NameLabel[1].grid(row = 3,column = 0, sticky = tk.E+tk.W)
        
        self.NameEntry[0] = ttk.Entry(self.EtryFrame)
        self.NameEntry[1] = ttk.Entry(self.EtryFrame)
        self.NameEntry[2] = ttk.Entry(self.EtryFrame)
        
        self.NameEntry[0].grid(row = 0,column = 1, columnspan = 5, sticky = tk.E+tk.W)
        self.NameEntry[1].grid(row = 1,column = 1, columnspan = 5, sticky = tk.E+tk.W)
        self.NameEntry[2].grid(row = 2,column = 1, columnspan = 5, sticky = tk.E+tk.W)
        
        #set time
        now = datetime.datetime.now()
        
        self.NameEntry[0].insert(0,'No Name Set')
        self.NameEntry[1].insert(0,str(now.year)+'/'+str(now.month)+'/'+str(now.day)+' at '+str(now.hour)+':'+str(now.minute))
        self.NameEntry[2].insert(0,str(now.year)+'/'+str(now.month)+'/'+str(now.day)+' at '+str(now.hour)+':'+str(now.minute))
        
        self.EtryFrame.grid(row = 1, column = 0, columnspan = 4, sticky = tk.E+tk.W)
        
        self.EtryFrame.grid_columnconfigure(0, weight = 1)
        self.EtryFrame.grid_columnconfigure(1, weight = 1)
        self.EtryFrame.grid_columnconfigure(7, weight = 1)
        
        #Build and pack button
        #insert the selct button
        self.SelectButton = ttk.Button(self.frame, text = 'Close',  width = 5, command = self.Close)
        self.SelectButton.grid(row = 3, column = 1 )
        self.SelectButton = ttk.Button(self.frame, text = 'Previous',  width = 5, command = self.Previous)
        self.SelectButton.grid(row = 3, column = 2 )
        self.SelectButton = ttk.Button(self.frame, text = 'Next',  width = 5, command = self.Set)
        self.SelectButton.grid(row = 3, column = 3 )
        
        #configure the stuff
        self.frame.grid_columnconfigure(0, weight = 1)
        self.frame.grid_rowconfigure(2, weight = 1)
    

    def Previous(self):
        
        #change tab on the notebook
        self.Parent.NoteBook.select(tab_id = 1)
    
    def Close(self):
        
        #output
        VisOut.TextBox(Title = 'Action', Text = 'Closing Application', state = 1)
                
        #destroy master window
        self.Parent.master.destroy()
    
    def Set(self):
        
        #Default informations
        RamPropID    = ['Laser','Power','Grating','Objectif','Time','N._Acqu.']
        RamPropUnit  = ['nm'   ,'perc' ,'cm-1'   ,'x'       ,'s'   ,'x'       ]
        SamPropID    = ['Sample_ID', 'Sample'  ,'Substr'   ,'Sam._Inf.','Sub._Inf.']
        MeasPropID   = ['Name', 'Date_0', 'Date_1']
        
        #Format the Raman info into one string
        RamInfo  = ''
        Text1    = ''
        RamInfo += '**Raman_Information**'+VisOut.Ret()
        
        #build the text
        for i in range(0,len(RamPropID)):
            
            #grab the string
            RamInfo += str(RamPropID[i])+' '+str(self.REntry[i].get())+' '+str(RamPropUnit[i])+VisOut.Ret()
            
            #text for verbose
            Text1 += '   -'+str(RamPropID[i])+': '+str(self.REntry[i].get())+' '+str(RamPropUnit[i])
            
            #finish up
            if i < len(RamPropID)-1:
                
                Text1 += '\n'
                
        #Format the Sample info into one string
        SamInfo  = ''
        Text2    = ''
        SamInfo += '**Sample_Information**'+VisOut.Ret()
        
        #build the text
        for i in range(0,len(SamPropID)):
            
            #grab the string
            SamInfo += str(SamPropID[i])+' '+str(self.SEntry[i].get())+VisOut.Ret()
            
            #text for verbose
            Text2 += '   -'+str(SamPropID[i])+': '+str(self.SEntry[i].get())+'\n'
            
            #finish up
            if i < len(SamPropID)-1:
                
                Text2 += '\n'
    
        #Format the Sample info into one string
        MeasInfo  = ''
        Text3    = ''
        MeasInfo += '**Measurement_Information**'+VisOut.Ret()
        
        #build the text
        for i in range(0,len(MeasPropID)):
            
            #grab the string
            MeasInfo += str(MeasPropID[i])+' '+str(self.NameEntry[i].get())+VisOut.Ret()
            
            #text for verbose
            Text3 += '   -'+str(MeasPropID[i])+': '+str(self.NameEntry[i].get())+'\n'
            
            #finish up
            if i < len(MeasPropID)-1:
                
                Text3 += '\n'
        
        #prepare container
        self.Container.Container = [RamInfo,SamInfo, MeasInfo]
        
        VisOut.TextBox(Title = 'RAMAN INFORMATION',Text = Text1,state = 1,close = False, Target = self.Parent.LogField)
        VisOut.TextBox(Title = 'SAMPLE INFORMATION ',Text = Text2,state = 1,close = False, Target = self.Parent.LogField)
        VisOut.TextBox(Title = 'MEASUREMENT INFORMATION ',Text = Text2,state = 1,close = False, Target = self.Parent.LogField)
        
        #output
        VisOut.TextBox(Title = 'Action', Text = 'Information Set', state = 1,close = False, Target = self.Parent.LogField)

        #destroy master window
        #change tab on the notebook
        self.Parent.NoteBook.select(tab_id = 3)

