# -*- coding: utf-8 -*-

#-INFO-
#-Name-FileManagement-
#-Version-0.1.01-
#-Date-16_February_2016-
#-Author-Alexander_Schober-
#-email-alex.schober@mac.com-
#-INFO-

print 'Loading FileManagement dependencies...'

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
Created on Tue Feb 16 18:23:52 2016
This script will contain all functions for file management.
In the hope of having better management of quick file action.
This includes creating filpaths a checking the existence or 
even writing folders. Not that in the script we are not yet
invoking any methind that could delete files...

This is because these scrips are still in a development stage. 

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

#import platform specifications
import platform

#import global
import glob

#import zip manager
import zipfile
import itertools
import subprocess

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

#File and system management routines
import Utility_File     as File


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

    from Tkinter import *

else:
    
    import tkinter as tk

    from tkinter import *

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
FUNCTION: Class

DESCRIPTION:

this class aims at creating a list frame with 
frame elements it was inspired by:

http://stackoverflow.com/questions/5286093/display-
listbox-with-columns-using-tkinter

All variables have been rewritten to mathc the 
current style

Prerequesites:
import Tkinter as tk
import tkFont
import ttk

o------------------------------------------------o

PARAMETERS:

- None

##################################################
'''

class MultiColumnListbox():
    """
    ############################################################
    this class aims at creating a list frame with frame elements
    it was inspired from:
    
    http://stackoverflow.com/questions/5286093/display-
    listbox-with-columns-using-tkinter
    
    All variables have been rewritten to mathc the current style
    
    Prerequesites:
    import Tkinter as tk
    import tkFont
    import ttk
    ############################################################
    """
        
    '''
    ##################################################
    FUNCTION: __init__
    
    DESCRIPTION:
    
    This simply builds the pointer
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - Window_Manager: The window manager structure
    - Parent the Main type class
    
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
        self.Root.resizable(width=False, height=False)
        self.Root.title("Data Browser")
        
        ##############################################
        #declare the Frame
        self.Frame = ttk.Frame(self.Root)
        
        ##############################################
        #We call the populators
        
        #Populate the Frame
        self.Populate_Frame()
        
        ##############################################
        #Pack the Frame
        self.Frame.pack(side = tk.BOTTOM,
                        fill = tk.BOTH,
                        expand = True)

        ##############################################
        #Set positioning
        self.Window.Place( ['Center',
                            'Center'])

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
        
        #initialise
        self.tree           = None
        self.FolderPath     = None
        self.Gathered       = None
        self.Condensensed   = None
        self.LoadRoutine    = self.Parent.Load_Processed
    

        '''
    ##################################################
    FUNCTION: Populate_Frame
    
    DESCRIPTION:
    
    Populate thge brwoser window
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - None
    
    ##################################################
    '''
    def Populate_Frame(self):
        
        
        #############################################
        #Load the container frames
        self.Padding = '10p'
        
        #this will be the treeframe
        self.FolderFrame    = ttk.Frame(self.Frame,
                                        padding = self.Padding)
                                        
        self.FilterFrame    = ttk.Frame(self.Frame,
                                        padding = self.Padding)
                                        
        self.TreeFrame      = ttk.Frame(self.Frame,
                                        padding = self.Padding)
                                        
        self.LogFrame       = ttk.Frame(self.Frame,
                                        padding = self.Padding)
        
        #############################################
        #############################################
        #Top Path select frame
        self.FolderLabel = ttk.Label(self.FolderFrame,
                                     text = 'Selected Folder: ')
                                     
        self.FolderEntry = ttk.Entry(self.FolderFrame)
        
        self.FolderButton= ttk.Button(self.FolderFrame,
                                      text = '...',
                                      command = self.Browse)
                                      
        self.Run         = ttk.Button(self.FolderFrame,
                                      text = 'Run',
                                      command = self.Run)
        
        self.FolderLabel.grid(row = 0,
                              column = 0,
                              sticky = tk.N+tk.S+tk.E+tk.W)
                              
        self.FolderEntry.grid(row = 0,
                              column = 1,
                              sticky = tk.N+tk.S+tk.E+tk.W)
                              
        self.FolderButton.grid(row = 0,
                               column = 2,
                               sticky = tk.N+tk.S+tk.E+tk.W)
                               
        self.Run.grid(row = 0,
                      column = 3,
                      sticky = tk.N+tk.S+tk.E+tk.W)
        
        self.FolderFrame.grid_columnconfigure(1,weight = 1)
        
        #############################################
        #############################################
        #Top selector frame
        #initialise the variable
        self.SetFilters()
        
        #############################################
        #############################################
        # create a treeview with dual scrollbars
        
        #create the header array
        self.Header = ['Type',
                       'Laser',
                       'Power',
                       'Grating',
                       'Objectif',
                       'Time',
                       'N. x',
                       'Sam ID',
                       'Sample',
                       'Substrate',
                       'Sam. Info.',
                       'Sub. Info.']
                

        #create the tree
        self.tree = ttk.Treeview(self.TreeFrame,
                                 columns = self.Header,
                                 show="headings")
        
        for col in self.Header:
            
            self.tree.heading(col,
                              text=col.title(),
                              command=lambda c=col: self.SortBy(self.tree, c, 0))
                              
            # adjust the column's width to the header string
            self.tree.column(col,
                             width=tkFont.Font().measure(col.title())+20)


        #set the scrollbars
        vsb = ttk.Scrollbar(self.TreeFrame,
                            orient  =   "vertical",
                            command =   self.tree.yview)
                            
        hsb = ttk.Scrollbar(self.TreeFrame,
                            orient  =   "horizontal",
                            command =   self.tree.xview)
        
        #link the scrollbar
        self.tree.configure(yscrollcommand  =   vsb.set,
                            xscrollcommand  =   hsb.set)
        
        
        
        
        self.tree.bind("<1>", self.OnClick)
        self.tree.bind(File.RightClickStr(), self.rClick)
        
        #grid it all
        self.tree.grid(column=0, row=0, sticky='nsew')
        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')
        
        #cofigure the treeframe
        self.TreeFrame.grid_columnconfigure(0, weight=1)
        self.TreeFrame.grid_rowconfigure(0, weight=1)
    
        #############################################
        #############################################
        #Bottom scrolled text
        
        #insert the textfield
        self.LogField = ScrolledText.ScrolledText(master = self.LogFrame,
                                                  wrap=tk.WORD,
                                                  height = 12)
    
        #grid it
        self.LogField.grid(row = 0, column = 0, sticky= tk.E+tk.W+tk.N+tk.S)
        
        self.LogFrame.grid_columnconfigure(0, weight = 1)
        self.LogFrame.grid_rowconfigure(0, weight = 1)
    
    
        #############################################
        #############################################
        #grid and configure
        self.FolderFrame.grid(row = 0,
                              column = 0,
                              sticky = tk.N+tk.S+tk.E+tk.W)
                              
        self.FilterFrame.grid(row = 1,
                              column = 0,
                              sticky = tk.N+tk.S+tk.E+tk.W)
                              
        self.TreeFrame.grid(row = 2,
                            column = 0,
                            sticky = tk.N+tk.S+tk.E+tk.W)
                            
        self.LogFrame.grid(row = 3,
                           column = 0,
                           sticky = tk.N+tk.S+tk.E+tk.W)
                           
        self.Root.grid_rowconfigure(2,weight = 1)
        
        self.Root.grid_columnconfigure(0,weight = 1)

    def Run(self):
        
        """
        ############################################################
        This will run the search for the given folder...
        ############################################################
        """
        
        if not self.FolderPath == None:
        
            #run the folder manipulation routines...
            self.InitialList, out_0 = self.ReturnRamanFiles(self.FolderPath,'.txt')
            self.Condensensed = self.RamanDBCondenser(out_0)
            self.SetFilters()
            self.Gatherer(self.InitialList,out_0)
            self.BuildTree()
    
    def Browse(self):
        
        """
        ############################################################
        This will run the search for the given folder...
        ############################################################
        """
    
        #run the folder manipulation routines...
        self.dir_opt = options = {}
        options['mustexist'] = False
        options['title'] = 'Select a directory...'
    
        #launch the directory selector
        self.FolderPath =  tkFileDialog.askdirectory(**self.dir_opt)
        
        self.FolderPath = os.path.abspath(self.FolderPath)
        
        #set the folder path to the entry window
        self.FolderEntry.delete(0, tk.END)
        self.FolderEntry.insert(0, self.FolderPath)
    

    
    def SetFilters(self):
        
        """
        ############################################################
        This Routine will make sure that the filters get contructed
        properly...
        ############################################################
        """
        
        try:
        
            for Element in self.OptionMenuList:
        
                Element.destroy()
    
        except:
        
            pass
        
        self.OptionMenuList = []
        self.Variables = []
        self.ImagingTypeList = []
        
        self.DefaultList = ['',
                            'All Types',
                            'All Wavelength',
                            'All Powers',
                            'All Gratings',
                            'All Objectifs',
                            'All Durations',
                            'All N. Acquisis.',
                            'All Sample IDs',
                            'All Samples',
                            'All Substrates',
                            'All Sam. Info',
                            'All Sub. Info']
        
        if not self.Condensensed == None:
        
            for i in range(1,len(self.Condensensed)):
            
                #create the variable for this drop down
                self.Variables.append(StringVar())
                
                #create the two lists
                self.ImagingTypeList.append([self.DefaultList[i]])
                
                for j in range(0, len(self.Condensensed[i])):
                
                    self.ImagingTypeList[-1].append(self.Condensensed[i][j][0])
                
                #Create the two elements
                self.OptionMenuList.append(ttk.OptionMenu(self.FilterFrame,
                                                          self.Variables[-1],
                                                          self.ImagingTypeList[-1][0],
                                                          *self.ImagingTypeList[-1],
                                                          command = self.Filter))

                #set it
                self.OptionMenuList[-1].grid(column = (i-1)%6, row = (i-1)/6, sticky = 'ew')


            for i in range(6):

                self.FilterFrame.grid_columnconfigure(i, weight = 1)

    def rClick(self,event):
        ''' 
        ####################################################################################
        This method act onto the checkbuttons and allows for an interactive menue to 
        fix or release multiple...
        
        
        Note that it yill then proceed to checking or unchecking the buttons before or 
        after depenindingon what the user selected. It will copy the current selection
        most....
        ####################################################################################
        '''
            
        #Set the focus on the widget
        event.widget.focus()
        
        #identify the selected object
        item = self.tree.identify('item',event.x,event.y)

        ID = [element[0] for element in self.Input[0]].index(self.List[self.IDs.index(item)])
        
        Path = self.Input[0][ID][1]
        
        #Create main menue
        MainMenue = tk.Menu(None, tearoff=0, takefocus=0)
        
        #now fill small menues
        MainMenue.add_command(label = 'open ...', command = partial(self.Locate   ,Path))
        MainMenue.add_command(label = 'Load',       command = partial(self.Load   ,Path))
        
        try:
            #spawn it
            MainMenue.tk_popup(event.widget.winfo_rootx()+event.x, event.widget.winfo_rooty()+event.y)
        except:
        
            return "break"

    def Locate(self,Path):
    
        """
        ############################################################
        If done properly this should open the file in the machine 
        dependant file browser
        ############################################################
        """

        if platform.system() == "Windows":
            
            os.startfile(Path)
        
        elif platform.system() == "Darwin":
            
            subprocess.Popen(["open", Path])
        
        else:
            subprocess.Popen(["xdg-open", Path])


    def Load(self,Path):
    
        """
        ############################################################
        If done properly this should open the file in the machine 
        dependant file browser
        ############################################################
        """

        self.LoadRoutine(Path)

    def Filter(self,val):
        """
        ############################################################
        This will filter the data and reset the list with whihc the
        actual display is done...
        ############################################################
        """
        
        #set th elength of the lis to 0
        List            = [self.InitialList[i] for i in range(0,len(self.InitialList))]
        FilterValues    = [None]
        Grab            = [None]
        Headers         = []
        
        #create the quick index
        for i in range(len(self.Condensensed)):
        
            Headers.append([self.Condensensed[i][l][0] for l in range(len(self.Condensensed[i]))])
    
        #grab the values...
        for j in range(len(self.Variables)):
    
            FilterValues.append(self.Variables[j].get())

            if self.Variables[j].get().split(' ')[0] == 'All':
        
                Grab.append(False)
        
            else:
        
                Grab.append(True)
        
        #intermediate list to compare
        ToCompare = []
        
        for i in range(1,len(Grab)):
            
            if Grab[i]:
                
                #find the index
                l = Headers[i].index(FilterValues[i])
        
                #grab it
                ToCompare.append([self.Condensensed[i][l][m] for m in range(len(self.Condensensed[i][l]))])


        for i in range(0, len(ToCompare)):
                
            List = list(set(List).intersection(ToCompare[i]))

        #update the interface
        self.Gatherer(List,list(self.Input))
        self.BuildTree()
            
            
    def BuildTree(self):
        
        """
        ############################################################
        This will load the Data into the tree and was edited to 
        fit the Raman Data Style
        
        List will be the Element IDs to display
        while input refers to the entire input
        ############################################################
        """
        
        try:
        
            for ID in self.IDs:
        
                self.tree.delete(ID)
    
        except:
        
            pass
        
        
        self.IDs = []
        
        if self.Gathered == None:
        
            for col in self.Header:
                self.tree.heading(col,
                                  text=col.title(),
                                  command=lambda c=col: self.SortBy(self.tree, c, 0))
                                  
                # adjust the column's width to the header string
                self.tree.column(col,
                                 width=tkFont.Font().measure(col.title())+20)
        
        else:
            
            for col in self.Header:
                self.tree.heading(col,
                                  text=col.title(),
                                  command=lambda c=col: self.SortBy(self.tree, c, 0))
                                  
                # adjust the column's width to the header string
                self.tree.column(col,
                                 width=tkFont.Font().measure(col.title())+20)


            for item in self.Gathered:
                
                self.IDs.append(self.tree.insert('', 'end', values=item))

    def SortBy(self,tree, col, descending):
    
    
        """sort tree contents when a column header is clicked on"""
        
        # grab values to sort
        data = [(tree.set(child, col), child) for child in tree.get_children('')]
        
        # now sort the data in place
        data.sort(reverse=descending)
        
        for ix, item in enumerate(data):
            tree.move(item[1], '', ix)
        
        # switch the heading so it will sort in the opposite direction
        tree.heading(col,command=lambda col=col: self.SortBy(tree, col,int(not descending)))

    def Gatherer(self,List, Input):

        """
        ############################################################
        This list aims to grab from the Input the important elements
        
        it will send out a an array of lists
        ############################################################
        """
        
        #set the variables locally
        self.Input = Input
        self.List = List
        
        #initialise the output
        Output = [None]*len(List)
        
        #Search array
        SearchList = Input[0]
        
        #if input is none we can't do anything exit
        for i in range(0,len(List)):

            for j in range(0,len(SearchList)):

                if List[i] == SearchList[j][0]:
                    try:
                    
                        Output[i] = [Input[k][j][1] for k in range(1,len(Input))]
                    
                    except:
    
                        print "Error"
    
        self.Gathered = Output


    def OnClick(self,event):
        
        """
        ############################################################
        This routin aims at returning the proper item selected by
        a click on the treeview. It will then launch the item 
        display..
        ############################################################
        """
        
        item = self.tree.identify('item',event.x,event.y)

        self.UpdateText([element[0] for element in self.Input[0]].index(self.List[self.IDs.index(item)]))


    def UpdateText(self, ID):
        '''
        ####################################################################################
        To allow for a more coherent interface the log will b displayed in here rather than
        a termainal Window. This will allow for better app implementation...
        ####################################################################################
        '''
        
        #delete the content
        self.LogField.delete('1.0',tk.END)
        
        #grab the path
        Path = self.Input[0][ID][1]
        
        #open the file
        with open(Path) as myfile:
            
            for Line in myfile:
            
                self.LogField.insert(tk.END, Line)

        
    
    def ReturnRamanFiles(self,FolderPath,Extension):
        """
        ############################################################
        This routine has been designed to find all files with a 
        certain extension in a folder..
        ############################################################
        """
        
        #initialise filloc array
        FileLoc         = []
        
        #initialise all Raman arrays
        RamanType       = []
        RamanLaser      = []
        RamanPower      = []
        RamanGrating    = []
        RamanObjectif   = []
        RamanTime       = []
        RamanAcqisi     = []
        
        #initialise all Sample arrays
        SamID           = []
        SamSample       = []
        SamSubstr       = []
        SamSamInf       = []
        SamSubInf       = []
        
        #initialise the ID counter
        ID = 0
        List = []
        
        for dirpath, dirnames, filenames in os.walk(FolderPath):
            
            for filename in [f for f in filenames if f.endswith(Extension)]:
                
                #set the path
                Path = os.path.abspath(os.path.join(dirpath, filename))
                
                try:
                
                    #open the file
                    f = open(Path, 'r')
                    
                    #if the fist word is Raman
                    if f.readline().split(' ')[0] == 'Raman':
                        
                        #reset file iterations
                        f.seek(0)
                        
                        #append
                        List.append(ID)
                        FileLoc.append([ID,Path])
                        RamanType.append([ID,f.readline().split(' ')[1]])
                    
                        #find all the info
                        for Line in itertools.islice(f, 20):
                    
                            #check for Raman Lines
                            if Line.split(' ')[0] == 'Laser':
                
                                RamanLaser.append([ID,Line.split(' ')[1].strip()])
                            
                            if Line.split(' ')[0] == 'Power':
                
                                RamanPower.append([ID,Line.split(' ')[1].strip()])
            
                            if Line.split(' ')[0] == 'Grating':
                
                                RamanGrating.append([ID,Line.split(' ')[1].strip()])
                
                            if Line.split(' ')[0] == 'Objectif':
                
                                RamanObjectif.append([ID,Line.split(' ')[1].strip()])
                            
                            if Line.split(' ')[0] == 'Time':
                
                                RamanTime.append([ID,Line.split(' ')[1].strip()])
                                    
                            if Line.split(' ')[0] == 'N._Acqu.':
                
                                RamanAcqisi.append([ID,Line.split(' ')[1].strip()])
                                    
                            #check for sample lines
                            if Line.split(' ')[0] == 'Sample_ID':
                
                                SamID.append([ID,Line.split(' ')[1].strip()])
                            
                            if Line.split(' ')[0] == 'Sample':
                
                                SamSample.append([ID,Line.split(' ')[1].strip()])
            
                            if Line.split(' ')[0] == 'Substr':
                
                                SamSubstr.append([ID,Line.split(' ')[1].strip()])
                
                            if Line.split(' ')[0] == 'Sam._Inf.':
                
                                SamSamInf.append([ID,Line.split(' ')[1].strip()])
                            
                            if Line.split(' ')[0] == 'Sub._Inf.':
                
                                SamSubInf.append([ID,Line.split(' ')[1].strip()])
                            
                except:
                
                    print 'Could not open: ',Path
                
                #move the ID forward
                ID += 1

        return List,[FileLoc,
                     RamanType,
                
                     #the ramn data
                     RamanLaser,
                     RamanPower,
                     RamanGrating,
                     RamanObjectif,
                     RamanTime,
                     RamanAcqisi,
                    
                     #the actual Sample data
                     SamID,
                     SamSample,
                     SamSubstr,
                     SamSamInf,
                     SamSubInf]


    def RamanDBCondenser(self,InPut):
        """
        ############################################################
        This routine has been designed to condense the Raman Data
        by types. It will go throughh all the arrays and only pop-
        ulate the necessary amount. 
        
        for example if only two wavelength are available there will
        be two array elements withh all the corresponfing IDs atta
        ched...
        ############################################################
        """
        #create the variable
        Output = [None]*len(InPut)
        
        #set the first as hopefully paths
        #are not condensable ...
        Output[0] = InPut[0]
        
        #loop
        for i in range(len(InPut)):

            #initialise things I might need
            ValuesEncountered = []
            TempOut = []

            for j in range(len(InPut[i])):

                #If this identifier is not yet present create the array
                if InPut[i][j][1] in ValuesEncountered:

                    TempOut[ValuesEncountered.index(InPut[i][j][1])].append(InPut[i][j][0])

                #if th eidentifier didn't exist yet add it and the value!!!
                else:
                    
                    ValuesEncountered.append(InPut[i][j][1])
                    TempOut.append([InPut[i][j][1],InPut[i][j][0]])
                        
            #add the element
            Output[i] = TempOut[:]

        return Output



