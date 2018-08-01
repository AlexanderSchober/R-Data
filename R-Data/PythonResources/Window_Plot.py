# -*- coding: utf-8 -*-

#-INFO-
#-Name-PlotWindow-
#-Version-0.1.0-
#-Date-30_April_2016-
#-Author-Alexander_Schober-
#-email-alex.schober@mac.com-
#-INFO-

print 'Loading Ploting dependencies...'

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

Here are the visual relaed imports 

Note thta this is the first time this is implemented in version 3
This could lead to some design inconsistencies
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

#numpy mathematical import
import numpy

#operating system import
import os

#decimal threatment import
import decimal

#######################################
#advanced imports

#Thread the fiting process to avoid ssytem lockup
from threading import Thread, Event
from Queue import Queue

#######################################
#advanced imports

#load this to pass on arguments into method names
from functools import *

######################################
#import matplotlib for colors
import matplotlib


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


"""
##################################################
These are the custome imports
##################################################
"""

#import the Utilities
import Utility_Main         as Utility

#import normalise
from Utility_Main           import normalize

#import main for the info Frame
import Main

#The terminal viual manager
import Utility_Out          as VisOut

#File and system management routines
import Utility_File         as File

#Import tht tooltip file
from Utility_ToolTip        import ToolTip

#import our own plotting interface
import SimplePlot.SimplePlot as SimplePlot


'''
##################################################
CLASS: Main_Fit_Class

DESCRIPTION:

This class is the host for the fitting window 
Frame. It has been carried along since the begining
of the UI implementation of the code. This is why
the laguage evovles accross the code. 

In the last version the hierachy got chnaged. The
two windows are now on the same level and taken
over by the Windiw management system. 

This is crucial as it will allow beter 
communication between the two.

All functions that were not related to window 
or display will be moved to this part

o------------------------------------------------o

PARAMETERS:

- None

##################################################
'''
class Main_Fit_Class:
    
    
    '''
    ##################################################
    FUNCTION: __init__
    
    DESCRIPTION:
    
    This will initialise the Windiw manager class and
    send out the first request.
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - Window_Manager: This is the manager structure.
    - DataClass: Data type strucure.
    
    ##################################################
    '''
        
    def __init__(self,Window_Manager, DataClass):


        ##################################################
        #set the local pointers
        self.Window_Manager = Window_Manager
        self.DataClass      = DataClass
        
        ##################################################
        #Ad dourselves to the dataclass to avoid being deleted
        self.DataClass.Add_Fit_Class(self)
        
        ##################################################
        #Load IO class
        self.IO_Manager = IO_Manager(self.DataClass,
                                     self)
        
        ##################################################
        #Run the analytical Preprocess
        self.PreProcess()
        
        ##################################################
        #Build the windows
        self.Build_Fit_Windows()

    


    '''
    ##################################################
    FUNCTION: PreProcess
    
    DESCRIPTION:
    
    Preprocess will initialize the whole Raman fittin
    analytical and computational assignements.
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - Window_Manager: This is the manager structure.
    - DataClass: Data type strucure.
    
    ##################################################
    '''

    def PreProcess(self):

        ##############################################
        #the input will be a projection from the
        if self.DataClass.Type == 'Depth' or self.DataClass.Type == 'Temperature':
            
            #initialise the contour
            if not self.DataClass.isContour:
                
                #initialise the contour class
                self.DataClass.LoadContour()
        
        ##############################################
        #try to delete the class
        try:
            del self.DataClass.RamFit
        except:
            pass
        
        #initialise the fit class
        self.DataClass.Load_RamFit()
        
        ##############################################
        #Depth, temp or all other need special treatment
        if self.DataClass.Type == 'Depth':
            
            for i in range(0,len(self.DataClass.Contour.Projection[1])):
                
                #initialise the fit
                self.DataClass.RamFit.AddFitData(self.DataClass.Contour.Projection[0],
                                                 self.DataClass.Contour.Projection[2][:,i],
                                                 self.DataClass.HeadStr)
                
                #initialise Lorrentzian definitions
                self.DataClass.RamFit.AddFit()
            
            
            #add visualisation class now defined globally in version 0.0.4
            self.DataClass.RamFit.AddFitVis()

        #Depth, temp or all other need special treatment
        if self.DataClass.Type == 'Temperature':
            
            for i in range(0,len(self.DataClass.Contour.Projection[1])):
                
                #initialise the fit
                self.DataClass.RamFit.AddFitData(self.DataClass.Contour.Projection[0],
                                                 self.DataClass.Contour.Projection[2][:,i],
                                                 self.DataClass.HeadStr)

                #initialise Lorrentzian definitions
                self.DataClass.RamFit.AddFit()
            
            
            #add visualisation class now defined globally in version 0.0.4
            self.DataClass.RamFit.AddFitVis()

        if self.DataClass.Type == 'Single':
        
            #here we don't pass thorugh a projection system...
            #as such the single specturm data is seen as corrupt for
            #further manipulaitons.
            #to avoid this case we suggest a simple array modification...
            OutZ = [self.DataClass.Z.Z[i,0,0,0][0] for i in range(self.DataClass.Z.Z.shape[0])]
            
            self.DataClass.RamFit.AddFitData(self.DataClass.X.X,
                                             OutZ,
                                             self.DataClass.HeadStr)
            
            #Make sure 0 values are set for the view range an duse them
            self.DataClass.RamFit.RawData[self.DataClass.RamFit.Current].Set0Values()
                
            #recheck if the viewdata change and load it up
            self.DataClass.RamFit.CompData[self.DataClass.RamFit.Current].LoadCalc()
                
            #initialise Lorrentzian definitions
            self.DataClass.RamFit.AddFit()
        
            #add visualisation class now defined globally in version 0.0.4
            self.DataClass.RamFit.AddFitVis()

        ##############################################
        #create the enhanced X for any type
        self.DataClass.RamFit.SetCreatedX()



    '''
    ##################################################
    FUNCTION: Build_Fit_Windiwows
    
    DESCRIPTION:
    
    This will initialise the Windiw manager class and
    send out the first request.
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - Window_Manager: This is the manager structure.
    - DataClass: Data type strucure.
    
    ##################################################
    '''
        
    def Build_Fit_Windows(self):

        ##############################################
        #Initialise a new manager
        self.Fitting_Window_Manager = self.Window_Manager.Add_Manager()
        
        ##############################################
        #The main window first
        
        #create the window
        self.IO_Fitting_Window = self.Fitting_Window_Manager.Add_Window()
        
        #initialise the class
        self.IO_Fitting_Class = IO_Window_Class(self.Fitting_Window_Manager,
                                                self)
        
        #Link the class to it
        self.IO_Fitting_Window.Link_to_Class(self.IO_Fitting_Class)


        ##############################################
        #Build the visual window window first
        
        #create the window
        self.Vis_Fitting_Window = self.Fitting_Window_Manager.Add_Window()
        
        #initialise the class
        self.Vis_Fitting_Class = Vis_Fitting_Class(self.Fitting_Window_Manager,
                                                   self)
        
        #Link the class to it
        self.Vis_Fitting_Window.Link_to_Class(self.Vis_Fitting_Class)



'''
##################################################
CLASS: IO_Manager

DESCRIPTION:

In an effort to keep the load and save routines
separated from the rest fo the routines, all of
them were gathered here.

o------------------------------------------------o

PARAMETERS:

- None

##################################################
'''
class IO_Manager:
    
    
    '''
    ##################################################
    FUNCTION: __init__
    
    DESCRIPTION:
    
    This will initialise the Windiw manager class and
    send out the first request.
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - Window_Manager: This is the manager structure.
    - DataClass: Data type strucure.
    
    ##################################################
    '''
        
    def __init__(self,DataClass, Parent):


        ##################################################
        #set the local pointers
        self.DataClass      = DataClass
        
        self.Parent         = Parent

        #the path at shich the selection starts
        self.PathofInterest = self.DataClass.Info.Root
        
        ##############################
        #The file and folder options
        self.file_opt = options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        options['initialdir'] = self.PathofInterest
        options['initialfile'] = 'myfile.txt'
        options['title'] = 'This is a title'
        
        self.dir_opt = options = {}
        options['initialdir'] = self.PathofInterest
        options['mustexist'] = False
        options['title'] = 'Select a folder'

    def Save(self, Value):
    
        '''
        ######################################################################
        This save routine will handle the general use interface:
        
        0 means spawn the normal window
        1 call single save
        2 call Fix Save
        3 call Parameter Save
        4 call Series save
        
        ######################################################################
        '''
    
        if Value == 0:
        
            #prompt the user what to do:
            self.SavePrompt = tk.Toplevel(self.master)
            
            #lanuch the window class dependency
            self.SavePrompt = SavePrompt(self.SavePrompt, self)
    
        if Value == 1:
            
            #save the spectrum
            self.Save_Single()

        if Value == 2:
            
            #save the spectrum
            self.Save_Values()
                
        if Value == 3:
            
            #save the spectrum
            self.Save_Fixes()
                
        if Value == 4:
            
            #save the spectrum
            self.Save_All()
                
                
    def Save_Single(self):

        '''
        ######################################################################
        This routine will be used to save single fits so for one depth or for
        a self.Type = 'Single' Measurement. For multiple spectra, we need a
        new system able to cope with the shear amoun of data generation. We 
        cannot simply write 300 text files for 300 fits.
        ######################################################################
        '''
        
        RawPointer  = self.DataClass.RamFit.RawData[self.DataClass.RamFit.Current]
        CompPointer = self.DataClass.RamFit.CompData[self.DataClass.RamFit.Current]
        LorrPointer = self.DataClass.RamFit.Function_Pointers[0][self.DataClass.RamFit.Current]
        FitPointer  = self.DataClass.RamFit.FitTot[self.DataClass.RamFit.Current]
        
        #create to numpy
        DataX = CompPointer.DataX
        DataY = CompPointer.DataY
        
        #The directory name will be related to the range we look at
        DirName = (str(round(numpy.min(DataX)))
                   + '_to_'
                   + str(round(numpy.max(DataX)))
                   + '_with_'
                   + str(len(self.DataClass.RamFit.Function_Pointers[0][self.DataClass.RamFit.Current]))
                   + '_Lorrentzians')
        
        #make a windows specific formating
        DirName = DirName.replace('.', ',')
        
        #We need to save all text files (because we have shitloads of space and why not)
        #There is the Original data file
        self.DataClass.Write.WriteFits(self.DataClass,
                                       DirName,
                                       RawPointer.X,
                                       RawPointer.Y,
                                       [numpy.min(RawPointer.XIni),
                                        numpy.max(RawPointer.XIni)],
                                       'Original',
                                       [0])
        
        #There is the baseline corrected data 
        if RawPointer.isBaseRemoved:
            
            #Write out the fit
            self.DataClass.Write.WriteFits(self.DataClass,
                                           DirName,
                                           RawPointer.XBase0,
                                           RawPointer.YBase0,
                                           [numpy.min(RawPointer.XBase0),
                                            numpy.max(RawPointer.XBase0)],
                                           'OriginalforBase',
                                           [0])

            #Write out the corrected output data
            self.DataClass.Write.WriteFits(self.DataClass,
                                           DirName,
                                           RawPointer.X,
                                           RawPointer.Y,
                                           [numpy.min(RawPointer.X),
                                            numpy.max(RawPointer.X)],
                                           'Original-Base',
                                           [0])

        #There is the baseline correcteted datafile minus the gaps used for the fit
        self.DataClass.Write.WriteFits(self.DataClass,
                                       DirName,
                                       DataX,
                                       DataY,
                                       [numpy.min(DataX),
                                        numpy.max(DataX)],
                                       'Original-Exclusions',
                                       [0])
        
        #Now we can write the total fit
        self.DataClass.Write.WriteFits(self.DataClass,
                                       DirName,
                                       FitPointer[0],
                                       FitPointer[1],
                                       [numpy.min(FitPointer[0]),
                                        numpy.max(FitPointer[0])],
                                       'Main Combined Fit',
                                       [0])
        

        for i in range(0,len(LorrPointer)):
            
            self.DataClass.Write.WriteFits(self.DataClass,
                                           DirName,
                                           LorrPointer[i].x,
                                           LorrPointer[i].yBis,
                                           [LorrPointer[i].Parameters[1]],
                                           'Lorrentzian_'
                                           +str(i+1).replace('.', ','),
                                           LorrPointer[i].Parameters)



        #Save parameters and fixes
        self.Save_Fixes(DirName = DirName)
        self.Save_Values(DirName = DirName)
        
    def Save_Values(self, DirName = None):
        
        #set the variables
        RawPointer  = self.DataClass.RamFit.RawData[self.DataClass.RamFit.Current]
        CompPointer = self.DataClass.RamFit.CompData[self.DataClass.RamFit.Current]
        LorrPointer = self.DataClass.RamFit.Function_Pointers[0][self.DataClass.RamFit.Current]
        FitPointer  = self.DataClass.RamFit.FitTot[self.DataClass.RamFit.Current]
        
        if DirName == None:
        
            DirName =  tkFileDialog.askdirectory(**self.dir_opt)
        
        
        #Latest addition write fit data into a nice readable file !!!
        Utility.WriteValues(self.DataClass,DirName,LorrPointer)
        
    def Save_Fixes(self, DirName = None):
        
        #set the variables
        RawPointer  = self.DataClass.RamFit.RawData[self.DataClass.RamFit.Current]
        CompPointer = self.DataClass.RamFit.CompData[self.DataClass.RamFit.Current]
        LorrPointer = self.DataClass.RamFit.Function_Pointers[0][self.DataClass.RamFit.Current]
        FitPointer  = self.DataClass.RamFit.FitTot[self.DataClass.RamFit.Current]
        
        if DirName == None:
        
            DirName =  tkFileDialog.askdirectory(**self.dir_opt)
        
        Utility.WriteFix(self.DataClass,DirName,LorrPointer)

    def Save_All(self):
        
        '''
        ######################################################################
        For sipmlicity reasons a browser from tkinter was integrated here
        instead of building our own. He os strong enough to allow for
        text, file diffrentiation etc....
            
        website: http://tkinter.unpythonic.net/wiki/tkFileDialog
        ######################################################################
        '''
        
        DirName =  tkFileDialog.askdirectory(**self.dir_opt)
        
        '''
        ######################################################################
        Saving the range parameters
        ######################################################################
        '''
        
        #grab the view data
        ValueString  = self.Parent.IO_Fitting_Class.ViewField[0].get()+' '
        ValueString += self.Parent.IO_Fitting_Class.ViewField[1].get()+' '
        
        #grab the calc data
        ValueString += self.Parent.IO_Fitting_Class.CalcField[0].get()+' '
        ValueString += self.Parent.IO_Fitting_Class.CalcField[1].get()+' '
        ValueString += self.Parent.IO_Fitting_Class.CalcField[2].get()
        
        #save out the file
        text_file = open(os.path.join(DirName,'Parameters.txt'),'w')
        text_file.write(ValueString)
        text_file.close()
        
        '''
        ######################################################################
        Saving the Function parameters for each function
        ######################################################################
        '''
        
        #first we need to create our three input arrays and names
        for kk in range(len(self.DataClass.RamFit.Function_Info_Pointers)):
            
            
            #initialise naming array
            Names = []
            
            #create the name array
            for mm in range(len(self.DataClass.RamFit.Function_Pointers[kk][0])):
            
                Names.append(self.DataClass.RamFit.Function_Pointers[kk][0][mm].Name)
    
            #initialize string
            ValueString = ''
            
            #launch the loop
            for i in range(0, len(self.DataClass.RamFit.Function_Pointers[kk][0])):
            
                #grab the view data
                if self.DataClass.RamFit.Function_Pointers[kk][0][i].Trace:
                
                    ValueString += ' - '+'True'+' - '
                
                else:
                    
                    ValueString += ' - '+'False'+' - '
                
                ValueString += self.DataClass.RamFit.Function_Pointers[kk][0][i].Color+' - '
                ValueString += str(self.DataClass.RamFit.Function_Pointers[kk][0][i].Group)+' - '
                ValueString += str(self.DataClass.RamFit.Function_Pointers[kk][0][i].Name)
                
                if i < len(self.DataClass.RamFit.Function_Pointers[kk][0]):
                
                    ValueString += '\n'
            
            #save out the file
            text_file = open(os.path.join(DirName,
                                          'Parameters_'
                                          + self.DataClass.RamFit.Function_Info_Pointers[kk].Name
                                          + '.txt'),
                             'w')
                             
            text_file.write(ValueString)
            text_file.close()
        
    
        #####################################################################
        #######################  Function      ##############################
        #####################################################################
        #first we need to create our three input arrays and names
        for kk in range(len(self.DataClass.RamFit.Function_Info_Pointers)):
            
            
            #initialise naming array
            Names = [0]
            
            #create the name array
            for mm in range(len(self.DataClass.RamFit.Function_Pointers[kk][0])):
            
                Names.append(self.DataClass.RamFit.Function_Pointers[kk][0][mm].Name.replace(" ", "_"))
            
            #per parameter
            for i in range(self.DataClass.RamFit.Function_Info_Pointers[kk].ParameterNumber):
            
                #Create the input
                Input_0 = numpy.zeros((len(self.DataClass.RamFit.Function_Pointers[kk])+1,
                                       len(self.DataClass.RamFit.Function_Pointers[kk][0])+1))
                Input_1 = numpy.zeros((len(self.DataClass.RamFit.Function_Pointers[kk])+1,
                                       len(self.DataClass.RamFit.Function_Pointers[kk][0])+1))
                                       
                
                #per fit set
                for j in range(0,len(self.DataClass.RamFit.Function_Pointers[kk])+1):
                
                    #per lor set
                    for k in range(0,len(self.DataClass.RamFit.Function_Pointers[kk][0])+1):
            
                        #first element 0
                        if j == 0 and k == 0:
                            
                            Input_0[j,k] = None
                            Input_1[j,k] = None
                        
                        #first Column (has to be fixed)
                        elif not j == 0 and k == 0:
            
                            Input_0[j,k] = j-1
                            Input_1[j,k] = j-1
            
                        #first Column (has to be fixed)
                        elif j == 0 and not k == 0:
            
                            Input_0[j,k] = k-1
                            Input_1[j,k] = k-1
                    
                        #first Column (has to be fixed)
                        else:
                            
                            Input_0[j,k] = self.DataClass.RamFit.Function_Pointers[kk][j-1][k-1].Parameters[i+1]
                            Input_1[j,k] = self.DataClass.RamFit.Function_Pointers[kk][j-1][k-1].ParametersFix[i+1]

                #Set the filename
                Tail_0 = (self.DataClass.RamFit.Function_Info_Pointers[kk].ParameterNames[i]
                          + '_'
                          + self.DataClass.RamFit.Function_Info_Pointers[kk].Name)
                          
                Tail_1 = ('Fix'
                          + self.DataClass.RamFit.Function_Info_Pointers[kk].ParameterNames[i]
                          + '_'
                          + self.DataClass.RamFit.Function_Info_Pointers[kk].Name)
                    
                
                        
                #Write out the result:
                self.DataClass.Write.Write2File(Input_0,
                                               0,
                                               len(Input_0),
                                               len(Input_0[0]),
                                               self.DataClass.HeadStrEx,
                                               self.DataClass.HeadStr,
                                               Tail_0,
                                               DirName,
                                               self.DataClass.RamInfo,
                                               self.DataClass.SamInfo,
                                               Names = Names)
    
                #Write out the result:
                self.DataClass.Write.Write2File(Input_1,
                                               0,
                                               len(Input_1),
                                               len(Input_1[0]),
                                               self.DataClass.HeadStrEx,
                                               self.DataClass.HeadStr,
                                               Tail_1,
                                               DirName,
                                               self.DataClass.RamInfo,
                                               self.DataClass.SamInfo,
                                               Names = Names)


    def Export(self):
        
        '''
        ######################################################################
        For sipmlicity reasons a browser from tkinter was integrated here
        instead of building our own. He os strong enough to allow for
        text, file diffrentiation etc....
            
        website: http://tkinter.unpythonic.net/wiki/tkFileDialog
        ######################################################################
        '''
        
        ######################################################################
        #grab the directory
        DirName =  tkFileDialog.askdirectory(**self.dir_opt)
    
        ######################################################################
        #Process the data
        Z = self.DataClass.RamFit.ComputeSubstraction(self.Parent.IO_Fitting_Class.ExportVar,
                                                      self.Parent.IO_Fitting_Class.ExportBool)
        
        ######################################################################
        #fecth the entry field value:
        try:
            
            EntryValues = [float(Element)
                           for Element in self.Entry_2[0].get().split(',')]
        
        except:
            
            EntryValues = []
        
        ######################################################################
        #define variables
        Axis = []
        ZBuffer = []
        
        for i in range(0, len(Z)):
        
            if self.DataClass.Type == 'Single':
            
                #add to axis
                ZBuffer.append(Z[i])
            
            else:
            
                if (not self.DataClass.Contour.Projection[1][i] in EntryValues):
                    
                    #add to axis
                    ZBuffer.append(Z[i])
        
                    #Build the axis
                    Axis.append(self.DataClass.Contour.Projection[1][i])
        
        #prpare next
        ZNext = [[ZBuffer[i][j] for i in range(0,len(ZBuffer))] for j in range(0,len(ZBuffer[0]))]

        ######################################################################
        #preapre the name of the file
        Tail = 'Substraction Export'

        if self.DataClass.Type == 'Depth':
        
            #Write out the result:
            self.DataClass.Write.Write2FileV2(self.DataClass,
                                              ZNext,
                                              Axis,
                                              [],
                                              [],
                                              [],
                                              self.DataClass.Type,
                                              0,
                                              self.DataClass.RamFit.CompData[self.DataClass.RamFit.Current].DataX,
                                              Tail,
                                              DirName)

        elif self.DataClass.Type == 'Temperature':
        
            #Write out the result:
            self.DataClass.Write.Write2FileV2(self.DataClass,
                                              ZNext,
                                              [],
                                              [],
                                              [],
                                              Axis,
                                              self.DataClass.Type,
                                              0,
                                              self.DataClass.RamFit.CompData[self.DataClass.RamFit.Current].DataX,
                                              Tail,
                                              DirName)

        elif self.DataClass.Type == 'Single':
        
            #Write out the result:
            self.DataClass.Write.Write2FileV2(self.DataClass,
                                              ZNext,
                                              [],
                                              [],
                                              [],
                                              [0],
                                              self.DataClass.Type,
                                              0,
                                              self.DataClass.RamFit.CompData[self.DataClass.RamFit.Current].DataX,
                                              Tail,
                                              DirName)
                
    def Load(self, Value):
    
        '''
        ######################################################################
        This save routine will handle the general use interface:
        
        0 means spawn the normal window
        1 call single save
        2 call Fix Save
        3 call Parameter Save
        4 call Series save
        
        ######################################################################
        '''
    
        if Value == 0:
        
            #prompt the user what to do:
            self.LoadPrompt = tk.Toplevel(self.master)
            
            #lanuch the window class dependency
            self.LoadPrompt = LoadPrompt(self.LoadPrompt, self)
    
        if Value == 1:
            
            #save the spectrum
            pass

        if Value == 2:
            
            #save the spectrum
            self.Load_Single(1)
                
        if Value == 3:
            
            #save the spectrum
            self.Load_Single(2)
                
        if Value == 4:
            
            #save the spectrum
            self.Load_All()


    def Load_Single(self,ID):

        '''
        ######################################################################
        For sipmlicity reasons a browser from tkinter was integrated here
        instead of building our own. He os strong enough to allow for 
        text, file diffrentiation etc....
        
        website: http://tkinter.unpythonic.net/wiki/tkFileDialog
        ######################################################################
        '''
        
        Path = tkFileDialog.askopenfilename( **self.file_opt)
        
        #We are reading fit values
        if ID == 1:
            
            #Readi it
            Utility.ReadValues(self.DataClass.RamFit.Function_Pointers[0][self.DataClass.RamFit.Current],Path)
        
            #Launch all resets
            for i in range(0,len(self.DataClass.RamFit.Function_Pointers[0][self.DataClass.RamFit.Current])):
                
                #rest
                self.Reset(i)
            
            
        #Weare processing fixed logical array
        if ID == 2:
            Utility.ReadFix(self.DataClass.RamFit.Function_Pointers[0][self.DataClass.RamFit.Current],Path)

    def Load_All_Preprocessing(self,Path, Add = [0,0,0,0]):
        '''
        ######################################################################
        This function will analyse the number of elements by the given path 
        and then create them.
        
        Path returns the supposed path of each position from each funciton.
        
        Path = [Path to positions x 4]
        ######################################################################
        '''
        
        #initiate the array
        HowMany = [0] * len(self.DataClass.RamFit.Function_Info_Pointers)
    
        #We selected a file now load it and find the instance 'Dist' that marks the start
        for i in range(0,len(Path)):
            
            ########################################
            #Here we read the file extract the lines
            #and close it again
            
            #open it
            try:
                
                #open file
                ToOpen  = open(Path[i], 'r')
                
                #set logical
                Pass = False
            
            except:
                
                #print it
                print 'Could not find the File',Path[i]
                
                #set logical
                Pass = True
        
            if not Pass:
                
                #reformat that shit real quick
                Read = []
                
                for Line in ToOpen:
                    Read.append(Line.strip())
                
                #The file is no longer recquired
                ToOpen.close()
        
                ########################################
                #Here we search for the spot that we
                #have the 'Dist' marker

                for j in range(0,len(Read)):
                    
                    #Split the line open over spaces
                    SplitLine = Read[j].split(' ')

                    #find the Y data positions in case the file is still version 1
                    if SplitLine[0] == 'Dist':

                        #write the position
                        Start = j
                        
                        #break the loop
                        break

                ########################################
                #Read through the data and get inject
                #the values into the appropriate array
                
                #strip the actual line
                line = Read[Start].strip()
                    
                #replace the end of the line (will cause problems in reading numbers
                line = line.replace('\t',' ', 1)
                
                #create tehe columns
                columns = line.split(' ')
                
                #run through
                for t in range(0,len(columns)):
                    
                    try:
                            
                        Value = float(columns[t])
                        HowMany[i] += 1
                    
                    except:
                        
                        pass

        ########################################
        #run through addition
        for i in range(0,len(Add)):
        
            HowMany[i] += Add[i]
        
        ########################################
        #run the construction
        self.Parent.IO_Fitting_Class.Create_Fit_Frame( HowMany = HowMany)

        return HowMany

    def Load_All(self):
        '''
        ######################################################################
        This was written to load a huge array of fits and apply them
        
        The load process will be similar to what we had in the classical 
        file type. Note taht a folder should be specified an that this
        folder should contain the text files :
        
        Position.txt
        HWHM.txt
        Factor.txt
        Minimum.txt
        ######################################################################
        '''
        #####################################################################
        #######################  FIND VERSION  ##############################
        #####################################################################
        
        #Select the directory
        DirName =  tkFileDialog.askopenfilename( **self.file_opt)
        
        DirName = os.path.dirname(DirName)
        
        try:
            
            ToOpen  = open(os.path.join(DirName,'Position.txt'), 'r')
            Version = 1
            ToOpen.close()
                    
        except:
                        
            print 'Could not find the File',os.path.join(DirName,'Position.txt')
            print 'Version is: ',2
            Version = 2


        #####################################################################
        #######################   SET  RANGES  ##############################
        #####################################################################


        #open it
        try:
            
            ToOpen  = open(os.path.join(DirName,'Parameters.txt'), 'r')
        
            #initialise read
            Read = []

            #set the lines
            for Line in ToOpen:
                
                Read.append(Line.strip())
                            
            #close the file
            ToOpen.close()
            
            if self.ImportVaues[0].get() == 1:
                
                #####################
                #first line is for the ranges
                
                Pointers = [self.Parent.IO_Fitting_Class.ViewField[0],
                            self.Parent.IO_Fitting_Class.ViewField[1],
                            self.Parent.IO_Fitting_Class.CalcField[0],
                            self.Parent.IO_Fitting_Class.CalcField[1],
                            self.Parent.IO_Fitting_Class.CalcField[2]]
                    
                Entries = Read[0].split(' ')
                
                #put the items
                for i in range(0, len(Entries)):
                    
                    Pointers[i].delete(0, tk.END)
                    Pointers[i].insert(0, Entries[i])
                        
                #launch routines
                self.Parent.IO_Fitting_Class.SetViewRange()
                self.Parent.IO_Fitting_Class.SetCalcRange()
        
        except:
            
            print 'Could not find the File',os.path.join(DirName,'Parameters.txt')

        
        
        #####################################################################
        #######################  PREPROCESSING ##############################
        #####################################################################
        
        
        if self.ImportVaues[1].get() == 1:
            
            #build the load string
            Path = []
            
            if Version == 2:
                
                #grab the pointer
                for i in range(0, len(self.DataClass.RamFit.Function_Pointers)):
            
                    #load the pointer
                    Path.append(os.path.join(DirName,
                                             'Position'
                                             +'_'
                                             +self.DataClass.RamFit.Function_Info_Pointers[i].Name
                                             +'.txt'))
            
                #create addidtion array
                Add = [0] * len(self.DataClass.RamFit.Function_Pointers)
            
            else:
            
                Path.append(os.path.join(DirName,'Position.txt'))
                                
                #grab the pointer
                for i in range(1, len(self.DataClass.RamFit.Function_Pointers)):
            
                    #load the pointer
                    Path.append(os.path.join(DirName,'Does_Not_Exist.txt'))
        
                #create addidtion array
                Add = [0] * len(self.DataClass.RamFit.Function_Pointers)
            
                #Add the linear
                Add[1] = 1
            
            #run the processing:
            HowMany = self.Load_All_Preprocessing(Path, Add = Add)
        
        if Version == 2:
        
            #set the variables
            Pointer     = []
            Path        = []
            
            #grab the pointer
            for i in range(0, len(self.DataClass.RamFit.Function_Pointers)):
            
                #load the pointer
                Pointer.append([self.DataClass.RamFit.Function_Pointers[i],
                                self.DataClass.RamFit.Function_Info_Pointers[i].ParameterNumber])
            
            
                #grab the name
                Name = self.DataClass.RamFit.Function_Info_Pointers[i].Name
                
                #initialise the path array
                Path.append([])
                
                #add the actual Paths of the parameters
                for j in range(self.DataClass.RamFit.Function_Info_Pointers[i].ParameterNumber):
            
                    Path[-1].append(os.path.join(DirName,
                                                 self.DataClass.RamFit.Function_Info_Pointers[i].ParameterNames[j]
                                                 +'_'
                                                 +Name
                                                 +'.txt'))
                
                #add the actual Paths of the fixes
                for j in range(self.DataClass.RamFit.Function_Info_Pointers[i].ParameterNumber):
            
                    Path[-1].append(os.path.join(DirName,
                                                 'Fix'
                                                 +self.DataClass.RamFit.Function_Info_Pointers[i].ParameterNames[j]
                                                 +'_'
                                                 +Name
                                                 +'.txt'))


        else:
        
            #set the variables
            Pointer = [None]*2
            Path = [[None]*8,[None]*6]
            
            #Lorrentzian
            Pointer[0] = [self.DataClass.RamFit.Function_Pointers[0],4]
            
            Path[0][0] = os.path.join(DirName,'Position.txt')
            Path[0][1] = os.path.join(DirName,'HWHM.txt')
            Path[0][2] = os.path.join(DirName,'Factor.txt')
            Path[0][3] = os.path.join(DirName,'Does_Not_Exist.txt')
            
            Path[0][4] = os.path.join(DirName,'FixPosition.txt')
            Path[0][5] = os.path.join(DirName,'FixHWHM.txt')
            Path[0][6] = os.path.join(DirName,'FixFactor.txt')
            Path[0][7] = os.path.join(DirName,'Does_Not_Exist.txt')
            
            #Linear
            Pointer[1] = [self.DataClass.RamFit.Function_Pointers[1],3]
            
            Path[1][0] = os.path.join(DirName,'Does_Not_Exist.txt')
            Path[1][1] = os.path.join(DirName,'Does_Not_Exist.txt')
            Path[1][2] = os.path.join(DirName,'Minimum.txt')
            
            Path[1][3] = os.path.join(DirName,'Does_Not_Exist.txt')
            Path[1][4] = os.path.join(DirName,'Does_Not_Exist.txt')
            Path[1][5] = os.path.join(DirName,'FixMinimum.txt')

        #####################################################################
        #######################  LOADING DATA  ##############################
        #####################################################################

        ########################################
        #Grab the pointer index
        for l in range(0,len(Pointer)):
        
            #We selected a file now load it and find the instance 'Dist' that marks the start
            for i in range(0,len(Path[l])):
                
                ########################################
                #Here we read the file extract the lines
                #and close it again
                #open it
                try:
                    
                    ToOpen  = open(Path[l][i], 'r')
                    Pass = False
                
                except:
                    
                    print 'Could not find the File',Path[l][i]
                    
                    Pass = True
            
                if not Pass:
                    
                    #reformat that shit real quick
                    Read = []
                    
                    for Line in ToOpen:
                        Read.append(Line.strip())
                    
                    #Set the path as self
                    self.Path = Path
                    
                    #The file is no longer recquired
                    ToOpen.close()
            
                    ########################################
                    #Here we search for the spot that we
                    #have the 'Dist' marker

                    for j in range(0,len(Read)):
                        
                        #Split the line open over spaces
                        SplitLine = Read[j].split(' ')

                        #find the Y data positions in case the file is still version 1
                        if SplitLine[0] == 'Dist':

                            #write the position
                            Start = j
                            
                            #break the loop
                            break

                    ########################################
                    #Read through the data and get inject
                    #the values into the appropriate array
                    
                    #set line index
                    Index = 0
                    u = 0

                    #go through all lines
                    for line in Read:
                        
                        #strip the actual line
                        line = line.strip()
                        
                        #replace the end of the line (will cause problems in reading numbers
                        line = line.replace('\t',' ', 1)
                        
                        #count the first line and check the number of elements
                        if  u > Start:
                            
                            #create tehe columns
                            columns = line.split(' ')
                            #print columns
                            
                            #set a run through variable
                            FoundFirst = False
                            gamma = 0
                            
                            #run through
                            for t in range(0,len(columns)):
                                
                                
                                if FoundFirst:
                                
                                    ##############################
                                    #try to put the value if succeeds move k one up
                                    try:
                                        
                                        ##############################
                                        #we aremanaging the values
                                        if i < Pointer[l][1]:
                                            
                                            if not Version == 2 and i == 2 and l == 1:
                                            
                                                Pointer[l][0][Index][gamma].Parameters[i+1] = float(columns[t]) * HowMany[0]
                                                Pointer[l][0][Index][gamma].ParametersIni[i+1] = float(columns[t]) * HowMany[0]
                                            
                                            else:
                                            
                                                Pointer[l][0][Index][gamma].Parameters[i+1] = float(columns[t])
                                                Pointer[l][0][Index][gamma].ParametersIni[i+1] = float(columns[t])
                                        
                                        ##############################
                                        #we aremanaging the fixes
                                        else:
                                            
                                            Pointer[l][0][Index][gamma].ParametersFix[i-Pointer[l][1]+1] = float(columns[t])
                                
                                        ##############################
                                        #move index forward
                                        gamma += 1
                                        
                                        
                                    ##############################
                                    #if we fail
                                    except:
                                        
                                        pass
                        
                                else:
                                
                                
                                    try:
                                        
                                        A = float(columns[t])
                                        FoundFirst = True
                                    
                                    except:
                                        
                                        pass
                                
                            #move forward
                            Index += 1
                        
                        #move u forward
                        u+= 1

        #####################################################################
        ####################### POST PROCESSING #############################
        #####################################################################

        if Version == 1:
    
            for i in range(0, len(self.DataClass.RamFit.Function_Pointers[1])):
        
                self.DataClass.RamFit.Function_Pointers[1][i][0].ParametersFix = [0,1,1,0,0]

        #run th econstuctor
        self.Parent.IO_Fitting_Class.CallConstructor(ID= 'All')

        #####################################################################
        ####################### GRAB PARAMETERS #############################
        #####################################################################
        if Version == 2:
        
            for kk in range(0, len(self.DataClass.RamFit.Function_Info_Pointers)):
                
                #Lorrentzian
                Pointer = self.DataClass.RamFit.Function_Pointers[kk]
                
                Path = os.path.join(DirName,'Parameters_'+self.DataClass.RamFit.Function_Info_Pointers[kk].Name+'.txt')
            
                    
                ########################################
                #Here we read the file extract the lines
                #and close it again
                
                #open it
                try:
                    
                    ToOpen  = open(Path, 'r')
                    Pass = False
                
                except:
                    
                    print 'Could not find the File',Path
                    Pass = True
            
                if not Pass:
                    
                    #reformat that shit real quick
                    Read = []
                    
                    for Line in ToOpen:
                        Read.append(Line.strip())
                    
                    #Set the path as self
                    self.Path = Path
                    
                    #The file is no longer recquired
                    ToOpen.close()
            
                    ########################################
                    #Here we search for the spot that we
                    #have the 'Dist' marker

                    for j in range(0,len(Read)):
                        
                        #Split the line open over spaces
                        SplitLine = Read[j].split(' - ')
                        
                        if len(SplitLine) == 1:
                        
                            SplitLine = Read[j].split(' ')

                        try:

                            #find the Y data positions in case the file is still version 1
                            for i in range(0, len(self.DataClass.RamFit.Function_Pointers[kk])):
                                
                                if SplitLine[0] == '- True':
                                
                                    self.DataClass.RamFit.Function_Pointers[kk][i][j].Trace = True
                                
                                else:
                
                                    self.DataClass.RamFit.Function_Pointers[kk][i][j].Trace = False
                                        
                                
                                self.DataClass.RamFit.Function_Pointers[kk][i][j].Color = SplitLine[1]
                                self.DataClass.RamFit.Function_Pointers[kk][i][j].Group = SplitLine[2]
                                
                                try:
                                
                                    self.DataClass.RamFit.Function_Pointers[kk][i][j].Name  = SplitLine[3]
                    
                                except:
                                    pass
                        except:
                            pass
        
        ########################################
        #process all residuals
        if self.ImportVaues[2].get() == 1:
        
            for i in range(0, len(self.DataClass.RamFit.Function_Pointers[0])):
            
                self.DataClass.RamFit.ComputeRestCalculation(i)
        
        
        #catch all the values after the import is finished
        self.Parent.IO_Fitting_Class.Fitting.Fetch_All()



'''
##################################################
CLASS: IO_Window_Class

DESCRIPTION:

This is the first window of the fitting class. It
manages the fitting parameters as import and 
eport manipulations.

o------------------------------------------------o

PARAMETERS:

- None

##################################################
'''

class IO_Window_Class:
    
    
    '''
    ##################################################
    FUNCTION: __init__
    
    DESCRIPTION:
    
    Initiating class. This is where the layout is 
    created and all functions initalised. It wil then
    by initiated by the standard window manager
    procedure
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - Window_Manager: This is the manager structure.
    - DataClass: Data type strucure.
    
    ##################################################
    '''
    
    def __init__(self, Window_Manager, Parent):

        ##############################################
        #Local pointers
        self.Parent         = Parent
        self.Window_Manager = Window_Manager
    
    
    
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
    
        ##############################
        #Dataclass from the program becomes locally linked
        self.DataClass = self.Parent.DataClass
        

    
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
        
        #define base padding for the window
        self.padding = '10p'

        #to be sinvestigated wth this is
        self.BaseActive = [tk.IntVar(),
                           tk.IntVar(),
                           tk.IntVar(),
                           tk.IntVar(),
                           tk.IntVar()]

        
        #set the master Frame parameters
        self.Root.configure(background = 'black')
        
        self.Root.resizable(width=True,
                            height=True)
        
        self.Root.title("Main Fitting Window ("+self.DataClass.Info.GetInfoVal('Name')+")")
        
        self.Root.grid_columnconfigure(0, weight = 1)
        
        self.Root.grid_rowconfigure(0, weight = 1)
        
        ##############################################
        #declare the Frame
        self.Frame = ttk.Frame(self.Root)
        
        ##############################################
        #We call the populators
        
        #Populate the Frame
        self.Populate_Frame()
        
        self.Frame.grid(row         = 0 ,
                        column      = 0,
                        sticky      = tk.E+tk.W+tk.N+tk.S)
        
        ##############################################
        #Resizing options
        self.Frame.grid_columnconfigure(0,
                                        weight = 1)
        
        self.Frame.grid_rowconfigure(0,
                                     weight = 1)

    
    
    def Populate_Frame(self):
        '''
        ###########################################################################
        This function Populate steh Frame in order to process the button handling
        
        This will Populate the main window of the instance and leve the rest free. 
        Note that this will also spawn the third window on select to create the 
        fittings.
        ###########################################################################
        
        '''
        #set processing boolean
        self.isRunning = False
        
        ###########################################################################
        #All Frames been created we can finnally create the notefook and link
        #the associated Frames
        
        #add notebook capabilities into this Frame
        self.NoteBookFrame = self.Frame#ttk.Frame(self.Frame, padding = self.padding)
        self.NoteBook      = ttk.Notebook(self.NoteBookFrame)
        
        ###########################################################################
        #in version 0.1.02 the Frame creation routines
        #have been moved to separate functions to
        #allow for better editability
        
        #Launch the information Frame
        #creates self.InfoFrame Frame class
        self.Create_Info_Frame()
        
        #create the edit Frame
        #creates self.CapsuleFrame Frame class
        self.Create_Edit_Frame()
        
        #Load the PLot Load Frame
        #creates self.Fitting.Frame Frame class
        self.Create_Load_Frame()
        
        #Load the PLot entry Frame
        #creates self.Fitting.Frame Frame class
        self.Create_Fit_Frame_Hidden()
        
        #Load the PLot Save Frame
        #creates self.Fitting.Frame Frame class
        self.Create_Save_Frame()
        
        ###########################################################################
        #Finnally Populate the notebook
        self.NoteBookPage  = [None] * 5
        self.NoteBookTitle = ['Info','Edit', 'Load', 'Fit', 'Save']
        
        #set the pages Frames
        self.NoteBookPage[0] = self.InfoFrame
        self.NoteBookPage[1] = self.CapsuleFrame
        self.NoteBookPage[2] = self.LoadFrame
        self.NoteBookPage[3] = self.Fitting.Frame
        self.NoteBookPage[4] = self.SaveFrame
        
        #Build the notebooks
        k = 0
        for i in range(0,len(self.NoteBookPage)):
            
            #add the specific page
            self.NoteBook.add(self.NoteBookPage[i],
                              text = self.NoteBookTitle[i] )
        
        #We call the population routine putting all butons and entry fields
        self.NoteBook.grid(row = 0,
                           column = 0,
                           sticky= tk.E+tk.W+tk.N+tk.S)
        
        #give weight...
        self.NoteBookFrame.grid_columnconfigure(0, weight = 1)
        self.NoteBookFrame.grid_rowconfigure(0, weight = 1)
        
        #Place the Frame into the main Frame...
        self.NoteBookFrame.grid(row = 0,column = 0, sticky= tk.E+tk.W+tk.N+tk.S)
        

    def Create_Load_Frame(self):
        
        '''
        ######################################################################
        In version 0.1.02 it was decided to separate the load and save Frames
        from the main fitting trunk. This lead to txo distinc Frames beeing 
        created to accomodate for the handling
        ######################################################################
        '''
        #set the Frame
        self.LoadFrame = ttk.Frame(self.NoteBook, padding = self.padding)
        
        #configure the resizing behaviour
        self.LoadFrame.grid_rowconfigure(4, weight = 1)
    
        #set the containing subFrames
        self.LoadSubFrame = [None]*2
        
        self.LoadSubFrame[0] = ttk.LabelFrame(self.LoadFrame,
                                              text = 'New Set:',
                                              padding = self.padding )
                                              
        self.LoadSubFrame[1] = ttk.LabelFrame(self.LoadFrame,
                                              text = 'Import Set:',
                                              padding = self.padding )
        
        self.LoadSubFrame[0].grid(row       = 0,
                                  column    = 0,
                                  sticky    = tk.W+tk.E)
                                  
        self.LoadSubFrame[1].grid(row       = 1,
                                  column    = 0,
                                  sticky    = tk.W+tk.E)
        
        ############################
        #create the fields
        self.LorrLabels = []
        self.FunctionNumEntry  = []
        
        #go through
        for i in range(self.DataClass.RamFit.NumberOfFunction):
        
            #construct the visuals
            self.LorrLabels.append(ttk.Label( self.LoadSubFrame[0],
                                             anchor = tk.E,
                                             text  = self.DataClass.RamFit.Function_Info_Pointers[i].Name))
                                             
            self.FunctionNumEntry.append(ttk.Entry( self.LoadSubFrame[0],
                                                   justify = tk.RIGHT,
                                                   width = 3))

        #construct the visuals
        self.LorrBut    = ttk.Button(self.LoadSubFrame[0],
                                     text  = 'Set'  ,
                                     command = self.Create_Fit_Frame)
        
        #Populate values for entry fields
        for i in range(self.DataClass.RamFit.NumberOfFunction):
        
            if self.DataClass.RamFit.Function_Info_Pointers[i].Name == 'Lorrentzian':
            
                self.FunctionNumEntry[i].insert(0,'1')
        
            else:
        
                self.FunctionNumEntry[i].insert(0,'0')
        
        #grid the elements onto the fram
        for ii in range(self.DataClass.RamFit.NumberOfFunction):
        
            self.LorrLabels[ii].grid(row = ii, column = 0, sticky = tk.E + tk.W)
            self.FunctionNumEntry[ii].grid( row = ii, column = 1)
        
        #position the button
        self.LorrBut.grid(row = 0, column = 4)
            
        #configure weights:
        self.LoadSubFrame[0].grid_columnconfigure(3, weight = 1)
        
        ############################
        #create the buttons
        self.Button  = [None]*3
        ButtonWidth  = 70
        ButtonHeight = 70
        
                                       
        self.Button[0] = CustomeButton(self.LoadSubFrame[1],
                                        ImagePath   = os.path.join(File.GetRuntimeDir(),
                                                                   'Images',
                                                                   'Save_Parameters.jpg'),
                                        width       = ButtonWidth,
                                        height      = ButtonHeight,
                                        command     = partial(self.Parent.IO_Manager.Load,2))
        
        self.Button[1] = CustomeButton(self.LoadSubFrame[1],
                                        ImagePath   = os.path.join(File.GetRuntimeDir(),
                                                                   'Images',
                                                                   'Save_Fixes.jpg'),
                                        width       = ButtonWidth,
                                        height      = ButtonHeight,
                                        command     = partial(self.Parent.IO_Manager.Load,3))
        
        self.Button[2] = CustomeButton(self.LoadSubFrame[1],
                                        ImagePath   = os.path.join(File.GetRuntimeDir(),
                                                                   'Images',
                                                                   'Load_Series.jpg'),
                                        width       = ButtonWidth,
                                        height      = ButtonHeight,
                                        command     = partial(self.Parent.IO_Manager.Load,4))
    
    
        #Place them
        self.Button[0].grid(row = 0, column = 0)
        self.Button[1].grid(row = 1, column = 0)
        self.Button[2].grid(row = 2, column = 0)

        ############################
        #create the buttons
        self.Text   = [None]*3
        TextAnchor  = tk.W
        TextWrap    = 400
        TextSticky  = tk.W+tk.E
        
        #Populate the buttons
        self.Text[0] = ttk.Label(self.LoadSubFrame[1],
                                 text = ('This option allows the user to load the parameters of a single fit. This can be usefull when the '+
                                         'object used to make the element was a single data acquisition.'),
                                 wraplength = TextWrap,
                                 anchor = TextAnchor)
                                       
        self.Text[1] = ttk.Label(self.LoadSubFrame[1],
                                 text = ('This option allows the user to load the parameters of a single fit. This can be usefull when the '+
                                         'object used to make the element was a single data acquisition.'),
                                 wraplength = TextWrap,
                                 anchor = TextAnchor)
        
        self.Text[2] = ttk.Label(self.LoadSubFrame[1],
                                 text = ('This option allows the user to load an entire series. Note that the number of lorrentzians will '+
                                         'be evaluated automatically. It can then be modified in the fitting window.'),
                                 wraplength = TextWrap,
                                 anchor = TextAnchor)
        
    
    
        #Place them
        self.Text[0].grid(row = 0, column = 1, sticky = TextSticky)
        self.Text[1].grid(row = 1, column = 1, sticky = TextSticky)
        self.Text[2].grid(row = 2, column = 1, sticky = TextSticky)
    
        ############################
        #create the buttons
        self.ImportRadio    = [None]*3
        self.Parent.IO_Manager.ImportVaues    = [tk.IntVar(),tk.IntVar(),tk.IntVar()]
    
        self.ImportRadio[0] = ttk.Checkbutton(self.LoadSubFrame[1],
                                              variable = self.Parent.IO_Manager.ImportVaues[0],
                                              text = 'Import Ranges')
    
        self.ImportRadio[1] = ttk.Checkbutton(self.LoadSubFrame[1],
                                              variable = self.Parent.IO_Manager.ImportVaues[1],
                                              text = 'Set Number of functions')
                                              
        self.ImportRadio[2] = ttk.Checkbutton(self.LoadSubFrame[1],
                                              variable = self.Parent.IO_Manager.ImportVaues[2],
                                              text = 'Process residuals (long...)')
        
    
        self.ImportRadio[0].grid(row = 3, column = 1, sticky = TextSticky)
        self.ImportRadio[1].grid(row = 4, column = 1, sticky = TextSticky)
        self.ImportRadio[2].grid(row = 5, column = 1, sticky = TextSticky)
    
    def Create_Save_Frame(self):
        
        '''
        ######################################################################
        In version 0.1.02 it was decided to separate the load and save Frames
        from the main fitting trunk. This lead to txo distinc Frames beeing 
        created to accomodate for the handling
        ######################################################################
        '''
        #set the Frame
        self.SaveFrame = ttk.Frame(self.NoteBook, padding = self.padding)
        
        #configure the resizing behaviour
        self.SaveFrame.grid_rowconfigure(1, weight = 1)
    
        #set the containing subFrames
        self.SaveSubFrame = [None]*2
        
        self.SaveSubFrame[0] = ttk.LabelFrame(self.SaveFrame,
                                              text = 'Export Modified Dataset:',
                                              padding = self.padding )
                                              
        self.SaveSubFrame[1] = ttk.LabelFrame(self.SaveFrame,
                                              text = 'Save Fitting Set:',
                                              padding = self.padding )
        
        self.SaveSubFrame[0].grid(row = 1,
                                  column = 0,
                                  sticky = tk.W+tk.E)
        
        self.SaveSubFrame[1].grid(row = 0,
                                  column = 0,
                                  sticky = tk.W+tk.E)
        
        
        self.SaveSubFrame[0].grid_columnconfigure(1, weight = 1)
        ############################
        ############################
        #create the fields
        
        
        ############################
        #create the explanation
        self.Text_2     = [None]*2
        TextAnchor      = tk.W
        TextWrap        = 400
        TextSticky      = tk.W+tk.E
        
        #Populate the buttons
        self.Text_2[0] = ttk.Label(self.SaveSubFrame[0],
                                   text = ('This option allows the user to export a substracted dataset. '+
                                           'This can be especially usefull when showcasing the sample compared to the substre. '+
                                           'Note that this information on it\'s own can be missinterpreted and should alays be acompagnied with the total fit. '+
                                           'To proceed please select the Group you wish to substract...'),
                                   wraplength = TextWrap,
                                   anchor = TextAnchor)
        
        
        self.Text_2[1] = ttk.Label(self.SaveSubFrame[0],
                                   text = 'Exclude: ',
                                   wraplength = TextWrap,
                                   anchor = TextAnchor)
        
        self.Text_2[0].grid(row         = 0,
                            column      = 0,
                            columnspan  = 3,
                            sticky      = TextSticky)
                            
        self.Text_2[1].grid(row         = 2,
                            column      = 0,
                            columnspan  = 1,
                            sticky      = TextSticky)
        
        ############################
        ############################
        #create the buttons
        self.Button_2   = [None]*2
        ButtonWidth     = 70
        ButtonHeight    = 70
        
        #Populate the buttons
        self.Button_2[0] = ttk.Button(self.SaveSubFrame[0],
                                      text      = 'Export',
                                      command   = partial(self.Parent.IO_Manager.Export))
        
        self.Button_2[1] = ttk.Button(self.SaveSubFrame[0],
                                      text      = 'Search',
                                      command   = partial(self.Search))
                                        
        self.Button_2[0].grid(row = 1, column = 3 )
        
        self.Button_2[1].grid(row = 1, column = 0 )
        
        ############################
        ############################
        #Create the options
        self.Entry_2  = [None]*1
        
        #Populate the buttons
        self.Entry_2[0] = ttk.Entry(self.SaveSubFrame[0])
        
        self.Entry_2[0].grid(row        = 2,
                             column     = 1,
                             columnspan = 3 ,
                             sticky     = tk.E+tk.W )
        
        ############################
        ############################
        #create the buttons
        self.Drop_2     = [None]*2
        ButtonWidth     = 70
        ButtonHeight    = 70
        self.ExportVar  = tk.StringVar()
        self.ExportBool = tk.IntVar()
        self.lst1       = []
        
        self.ExportBool.set(1)
        
        #Populate the buttons
        self.Drop_2[0] = ttk.OptionMenu(self.SaveSubFrame[0],
                                        self.ExportVar,
                                        *self.lst1)
        self.Drop_2[0].grid(row     = 1,
                            column  = 1,
                            sticky  = tk.E+tk.W )
        
        #Populate the buttons
        self.Drop_2[1] = ttk.Checkbutton(self.SaveSubFrame[0],
                                         text = 'Remove Residue',
                                         variable = self.ExportBool)
        self.Drop_2[1].grid(row     = 1,
                            column  = 2,
                            sticky  = tk.E+tk.W )
        
        
        self.Search()
        
        ############################
        ############################
        #create the buttons
        self.Button  = [None]*4
        ButtonWidth  = 70
        ButtonHeight = 70
        
        #Populate the buttons
        self.Button[0] = CustomeButton(self.SaveSubFrame[1],
                                        ImagePath   = os.path.join(File.GetRuntimeDir(),
                                                                   'Images',
                                                                   'Save_Txt.jpg'),
                                        width       = ButtonWidth,
                                        height      = ButtonHeight,
                                        command     = partial(self.Parent.IO_Manager.Save,1))
                                       
        self.Button[1] = CustomeButton(self.SaveSubFrame[1],
                                        ImagePath   = os.path.join(File.GetRuntimeDir(),
                                                                   'Images',
                                                                   'Save_Parameters.jpg'),
                                        width       = ButtonWidth,
                                        height      = ButtonHeight,
                                        command     = partial(self.Parent.IO_Manager.Save,2))
        
        self.Button[2] = CustomeButton(self.SaveSubFrame[1],
                                        ImagePath   = os.path.join(File.GetRuntimeDir(),
                                                                   'Images',
                                                                   'Save_Fixes.jpg'),
                                        width       = ButtonWidth,
                                        height      = ButtonHeight,
                                        command     = partial(self.Parent.IO_Manager.Save,3))
        
        self.Button[3] = CustomeButton(self.SaveSubFrame[1],
                                        ImagePath   = os.path.join(File.GetRuntimeDir(),
                                                                   'Images',
                                                                   'Save_Series.jpg'),
                                        width       = ButtonWidth,
                                        height      = ButtonHeight,
                                        command     = partial(self.Parent.IO_Manager.Save,4))
    
    
        #Place them
        self.Button[0].grid(row = 0, column = 0)
        self.Button[1].grid(row = 1, column = 0)
        self.Button[2].grid(row = 2, column = 0)
        self.Button[3].grid(row = 3, column = 0)

        ############################
        #create the buttons
        self.Text   = [None]*4
        TextAnchor  = tk.W
        TextWrap    = 400
        TextSticky  = tk.W+tk.E
        
        #Populate the buttons
        self.Text[0] = ttk.Label(self.SaveSubFrame[1],
                                 text = ('This option allows the user to save the current fit and its associated lorrentzians as text files. '+
                                         'The ammount of files will be determined by the number of lorrentzians includicng the summed fit.'),
                                 wraplength = TextWrap,
                                 anchor = TextAnchor)
                                       
        self.Text[1] = ttk.Label(self.SaveSubFrame[1],
                                 text = ('This option allows the user to save only the parameters of the current lorrentzian. '),
                                 wraplength = TextWrap,
                                 anchor = TextAnchor)
        
        self.Text[2] = ttk.Label(self.SaveSubFrame[1],
                                 text = ('This option allows the user to save only the parameters of the current lorrentzian. '),
                                 wraplength = TextWrap,
                                 anchor = TextAnchor)
        
        self.Text[3] = ttk.Label(self.SaveSubFrame[1],
                                 text = ('This option allows the user to save the enteire series. This will result in a text file for each '+
                                         'parameter'),
                                 wraplength = TextWrap,
                                 anchor = TextAnchor)
    
    
        #Place them
        self.Text[0].grid(row = 0, column = 1, sticky = TextSticky)
        self.Text[1].grid(row = 1, column = 1, sticky = TextSticky)
        self.Text[2].grid(row = 2, column = 1, sticky = TextSticky)
        self.Text[3].grid(row = 3, column = 1, sticky = TextSticky)
    

    def Create_Info_Frame(self):
        
        '''
        ######################################################################
        In version 0.1.01 the information Frame was appended locally to fill 
        the smapce here. This means that the informations are available in the
        inforamtion tab.
        ######################################################################
        '''
        #set the Frame
        self.InfoFrame = ttk.Frame(self.NoteBook,
                                   padding = self.padding)
        
        #set the subfrmae
        self.InfoSubFrame = ttk.Frame(self.InfoFrame)
        
        self.InfoSubFrame.grid(row = 0,
                               column = 0,
                               sticky = tk.E + tk.W)
        
        #Load the information
        Main.InfoWindowClass(self.InfoSubFrame,
                             self.DataClass,
                             window = False)
        
        #configure the resizing behaviour
        self.InfoFrame.grid_rowconfigure(0, weight = 1)

    def Create_Edit_Frame(self):
        
        '''
        ######################################################################
        In version 0.1.01 the totality of the edit functions have been moved
        over to an edit Frame that contains the different options.
        
        - Baseline
        - Normalize/factorize
        - Range options
        
        This section has to be cleaned up despite it working as is
        ######################################################################
        '''
        
        #Launch the capsule Frame
        self.CapsuleFrame = ttk.Frame(self.NoteBook, padding= self.padding)
        
        #initialise the Frame
        self.BaseFrame = ttk.LabelFrame(self.CapsuleFrame, text = 'Baseline Options (has to be fixed):', padding = self.padding )
        self.BaseFrame.grid(row = 1, column = 0, columnspan = 2, sticky = tk.N+tk.S+tk.E+tk.W)
        
        #Placement variables
        LorrOffest  = 5
        BaseOffset  = 11
        BaseOffset2 = 14
        InputOffset = 8
        RowOffset   = 9+7
        RowLabels   = 12+7
        RowEntry    = 17
        
        #set arrays
        self.BaseLabels = [None]*9
        self.BaseEntry  = [None]*7
        self.BaseBut    = [None]*6
        
        #All initial labels
        self.BaseLabels[2] = ttk.Label(self.BaseFrame, text = 'Order:' , anchor = tk.E)
        self.BaseLabels[3] = ttk.Label(self.BaseFrame, text = 'Min.:'  , anchor = tk.E)
        self.BaseLabels[4] = ttk.Label(self.BaseFrame, text = 'Max.:'  , anchor = tk.E)
        self.BaseLabels[5] = ttk.Label(self.BaseFrame, text = 'Excl.:' , anchor = tk.E)
        self.BaseLabels[6] = ttk.Label(self.BaseFrame, text = 'Factor:', anchor = tk.E)
        
        self.BaseEntry[0] = ttk.Entry(self.BaseFrame,width = 8  , justify = tk.RIGHT)
        self.BaseEntry[1] = ttk.Entry(self.BaseFrame,width = 8  , justify = tk.RIGHT)
        self.BaseEntry[2] = ttk.Entry(self.BaseFrame,width = 8  , justify = tk.RIGHT)
        self.BaseEntry[3] = ttk.Entry(self.BaseFrame            , justify = tk.RIGHT)
        self.BaseEntry[4] = ttk.Entry(self.BaseFrame,width = 8  , justify = tk.RIGHT)
        
        self.BaseBut[0] = ttk.Checkbutton(self.BaseFrame, text = 'Polynomial:' , variable = self.BaseActive[0])
        self.BaseBut[1] = ttk.Checkbutton(self.BaseFrame, text = 'Statistical:', variable = self.BaseActive[1])
        self.BaseBut[2] = ttk.Button(     self.BaseFrame, text = 'Set'   , width = 3)
        
        #Populate values for entry fields
        self.BaseEntry[0].insert(0,'0')
        self.BaseEntry[1].insert(0,str(round(numpy.min(self.DataClass.RamFit.RawData[self.DataClass.RamFit.Current].X),4)))
        self.BaseEntry[2].insert(0,str(round(numpy.max(self.DataClass.RamFit.RawData[self.DataClass.RamFit.Current].X),4)))
        self.BaseEntry[3].insert(0,str(''))
        self.BaseEntry[4].insert(0,'0.95')
        
        #place the items
        self.BaseLabels[2].grid(row = 4 , column = 2 , sticky = tk.E+tk.W)
        self.BaseLabels[3].grid(row = 2 , column = 2 , sticky = tk.E+tk.W)
        self.BaseLabels[4].grid(row = 2 , column = 4 , sticky = tk.E+tk.W)
        self.BaseLabels[5].grid(row = 3 , column = 2 , sticky = tk.E+tk.W)
        self.BaseLabels[6].grid(row = 4 , column = 4 , sticky = tk.E+tk.W)
        
        self.BaseEntry[0].grid(row = 4 , column = 3 , sticky = tk.E+tk.W )
        self.BaseEntry[1].grid(row = 2 , column = 3 , sticky = tk.E+tk.W )
        self.BaseEntry[2].grid(row = 2 , column = 5 , sticky = tk.E+tk.W )
        self.BaseEntry[3].grid(row = 3 , column = 3 , columnspan = 3, sticky = tk.E+tk.W )
        self.BaseEntry[4].grid(row = 4 , column = 5 , sticky = tk.E+tk.W )
        
        self.BaseBut[0].grid(row = 4 , column = 1 , sticky = tk.E+tk.W )
        self.BaseBut[1].grid(row = 6 , column = 1 , sticky = tk.E+tk.W )
        self.BaseBut[2].grid(row = 10, column = 5 , sticky = tk.E+tk.W )
        
        #Set labels
        self.BaseLabels2 = [None]*4
        self.BaseEntry2  = [None]*2
        
        self.BaseLabels2[2] = ttk.Label(self.BaseFrame, text = 'Lambda:' , anchor = tk.E)
        self.BaseLabels2[3] = ttk.Label(self.BaseFrame, text = 'p:'      , anchor = tk.E)
        
        self.BaseEntry2[0] = ttk.Entry(self.BaseFrame, width = 8 )
        self.BaseEntry2[1] = ttk.Entry(self.BaseFrame, width = 8 )
        
        self.BaseEntry2[0].insert(0,'1000000')
        self.BaseEntry2[1].insert(0,'0.005')
        
        #place the items
        self.BaseLabels2[2].grid(row = 6 , column = 2 )
        self.BaseLabels2[3].grid(row = 6 , column = 4 )
        
        self.BaseEntry2[0].grid( row = 6 , column = 3 )
        self.BaseEntry2[1].grid( row = 6 , column = 5 )
        
        #Manage the grid
        self.BaseFrame.grid_columnconfigure(0, weight = 1)
        self.BaseFrame.grid_columnconfigure(6, weight = 1)
        
        self.BaseFrame.grid_rowconfigure(0, weight = 1)
        self.BaseFrame.grid_rowconfigure(3, weight = 1)
        
        ###########################################################################
        #in version 0.0.5 the extras have their own Frame to be placed in
        #Set entries
        
        #Set the Frame
        self.ManipulationFrame = ttk.LabelFrame(self.CapsuleFrame, text = 'Normalisation Options (has to be fixed):', padding = self.padding )
        self.ManipulationFrame.grid(row = 0, column = 1, sticky = tk.N+tk.S+tk.E+tk.W)
        
        #declare variables
        self.ManipulationBut   = [None]*3
        self.ManipulationEntry = [None]*2
        
        #Populate buttons
        self.ManipulationBut[0] = ttk.Checkbutton(self.ManipulationFrame, text = 'Normalize', variable = self.BaseActive[2])#, anchor = tk.W)
        self.ManipulationBut[1] = ttk.Checkbutton(self.ManipulationFrame, text = 'Factorise', variable = self.BaseActive[3])#, anchor = tk.W)
        self.ManipulationBut[2] = ttk.Checkbutton(self.ManipulationFrame, text = 'Offset   ', variable = self.BaseActive[4])#, anchor = tk.W)
        
        #grid th ebuttons
        self.ManipulationBut[0].grid(row = 1,column = 1, sticky = tk.E+tk.W)
        self.ManipulationBut[1].grid(row = 2,column = 1, sticky = tk.E+tk.W)
        self.ManipulationBut[2].grid(row = 3,column = 1, sticky = tk.E+tk.W)
        
        #Populate entries
        self.ManipulationEntry[0] = ttk.Entry(self.ManipulationFrame, width = 2, justify = tk.RIGHT)
        self.ManipulationEntry[1] = ttk.Entry(self.ManipulationFrame, width = 2, justify = tk.RIGHT)
        
        #grid buttons
        self.ManipulationEntry[0].grid(row = 2,column = 2, sticky = tk.E+tk.W)
        self.ManipulationEntry[1].grid(row = 3,column = 2, sticky = tk.E+tk.W)
        
        #Build run button
        self.NormBut2 = ttk.Button(self.ManipulationFrame, text = 'Set')
        
        #Grid the buttons
        self.NormBut2.grid(row = 6,column = 3)
        
        #Manage the grid
        self.ManipulationFrame.grid_columnconfigure(0, weight = 1)
        self.ManipulationFrame.grid_columnconfigure(3, weight = 1)
        self.ManipulationFrame.grid_rowconfigure(0, weight = 1)
        self.ManipulationFrame.grid_rowconfigure(4, weight = 1)
        
        
        ###########################################################################
        #in version 0.0.5 the extras have their own Frame to be placed in
        #this aims at using a notebook system
        
        #Set the Frame
        self.RangeFrame = ttk.LabelFrame(self.CapsuleFrame, text = 'Range Options:', padding = self.padding )
        self.RangeFrame.grid(row = 0, column = 0, sticky = tk.N+tk.S+tk.E+tk.W)
        
        #Create the initial view range and fit range fields with labels
        self.TopLabels    = [None]*7
        self.ViewField    = [None]*2
        self.CalcField    = [None]*3

        #Load the label dependencies
        self.TopLabels[0] = ttk.Label(self.RangeFrame, text = 'Minimum'            , anchor = tk.CENTER)
        self.TopLabels[1] = ttk.Label(self.RangeFrame, text = 'Maximum'            , anchor = tk.CENTER)
        self.TopLabels[4] = ttk.Label(self.RangeFrame, text = 'Exclusion :'    , anchor = tk.E)
        self.TopLabels[5] = ttk.Label(self.RangeFrame, text = 'Data View :'    , anchor = tk.E)
        self.TopLabels[6] = ttk.Label(self.RangeFrame, text = 'Calculation :' , anchor = tk.E)
        
        #Load the field dependencies
        self.ViewField[0] = ttk.Entry(self.RangeFrame, width = 5    )
        self.ViewField[1] = ttk.Entry(self.RangeFrame, width = 5    )
        self.CalcField[0] = ttk.Entry(self.RangeFrame, width = 5    )
        self.CalcField[1] = ttk.Entry(self.RangeFrame, width = 5    )
        self.CalcField[2] = ttk.Entry(self.RangeFrame, width = 5    )
        
        #Load yhr button dependencies
        self.ViewButton   = ttk.Button(self.RangeFrame, text = 'Set',   command = self.SetViewRange   )
        self.CalcButton   = ttk.Button(self.RangeFrame, text = 'Set',   command = self.SetCalcRange   )
        
        #place the elements using the grid method
        self.TopLabels[0].grid(row = 0 , column = 3 , sticky = tk.E+tk.W)
        self.TopLabels[1].grid(row = 0 , column = 5 , sticky = tk.E+tk.W)
        self.TopLabels[4].grid(row = 4 , column = 1 , sticky = tk.E+tk.W)
        self.TopLabels[5].grid(row = 1 , column = 1 , sticky = tk.E+tk.W)
        self.TopLabels[6].grid(row = 3 , column = 1 , sticky = tk.E+tk.W)
        
        self.ViewField[0].grid(row = 1 , column = 3 , sticky = tk.E+tk.W)
        self.ViewField[1].grid(row = 1 , column = 5 , sticky = tk.E+tk.W)
        self.CalcField[0].grid(row = 3 , column = 3 , sticky = tk.E+tk.W)
        self.CalcField[1].grid(row = 3 , column = 5 , sticky = tk.E+tk.W)
        self.CalcField[2].grid(row = 4 , column = 3 , columnspan = 3 , sticky = tk.E+tk.W)
        
        self.ViewButton.grid(row = 1 , column = 6)
        self.CalcButton.grid(row = 4 , column = 6)
        
        #Populate values for entry fields
        self.ViewField[0].insert(0,str(round(numpy.min(self.DataClass.RamFit.RawData[self.DataClass.RamFit.Current].X),4)))
        self.ViewField[1].insert(0,str(round(numpy.max(self.DataClass.RamFit.RawData[self.DataClass.RamFit.Current].X),4)))
        
        self.CalcField[0].insert(0,str(round(numpy.min(self.DataClass.RamFit.CompData[self.DataClass.RamFit.Current].X),4)))
        self.CalcField[1].insert(0,str(round(numpy.max(self.DataClass.RamFit.CompData[self.DataClass.RamFit.Current].X),4)))
        self.CalcField[2].insert(0,str(''))
        
        #Manage the grid
        self.RangeFrame.grid_columnconfigure(0, weight = 1)
        self.RangeFrame.grid_columnconfigure(7, weight = 1)
        
        self.RangeFrame.grid_rowconfigure(0, weight = 1)
        self.RangeFrame.grid_rowconfigure(4, weight = 1)
    

        
    def Create_Fit_Frame_Hidden(self):
        '''
        ######################################################################
        This instance should load the fitting window
        It has been separated in version 3 because it allows in app change of
        the ammount of lorrantzians
        
        ######################################################################
        '''
        ########################################
        #Catch the info from the entry field
        HowMany = [0,0,0,0,0,0,0,0,0,0,0,0]
        
        ########################################
        #Relaunch the dependencies
        self.Fitting = Variable_Management_Class(self.NoteBook,
                                                 self.DataClass,
                                                 HowMany,
                                                 self,
                                                 'Hidden',
                                                 isWindow = False)

    def Create_Fit_Frame(self, HowMany = None):
        '''
        ######################################################################
        This instance should load the fitting window
        It has been separated in version 3 because it allows in app change of
        the ammount of lorrantzians
        
        
        ######################################################################
        '''
        
        ########################################
        #Try to forget a notebook page
        try:
            self.NoteBook.forget(3)
            self.NoteBookPage[3] = [None]
        
        except:
            
            pass
        
        ########################################
        #Catch the info from the entry field
        if HowMany == None:
        
            try:
                
                HowMany = [None]*len(self.FunctionNumEntry)
                
                for i in range(0, len(self.FunctionNumEntry)):
                
                    HowMany[i] = int(self.FunctionNumEntry[i].get())
                                     
            except:
                
                self.NoteBookPage[3] = self.Create_Fit_Frame_Hidden()
            
        else:
        
            for i in range(0, len(self.FunctionNumEntry)):
                
                #delete old entry
                self.FunctionNumEntry[i].delete(0, tk.END)
            
                #set the value
                self.FunctionNumEntry[i].insert(0,HowMany[i])
        
        ########################################
        #Relaunch the dependencies
        self.Fitting = Variable_Management_Class(self.NoteBook,
                                        self.DataClass,
                                        HowMany,
                                        self,
                                        'Show',
                                        isWindow = False)
        
        #set the notebook
        self.NoteBookPage[3] = self.Fitting.Frame
            
        self.NoteBook.insert(3,self.NoteBookPage[3],text = self.NoteBookTitle[3])
        self.NoteBook.select(3)


    def Reload(self):
    
        '''
        ######################################################################
        reload all data here
        ######################################################################
        '''
        LastAct = ''
        #try to delete the class
        try:
            del self.DataClass.RamFit
        except:
            pass
        
        #initialise the fit class
        self.DataClass.Load_RamFit()
        
        #Depth, temp or all other need special treatment
        if self.DataClass.Type == 'Depth' or self.DataClass.Type == 'Temperature':
            
            for i in range(0,len(self.DataClass.Contour.Projection[1])):
                
                LastAct += self.DataClass.RamFit.AddFitData(self.DataClass.Contour.Projection[0],
                                                            self.DataClass.Contour.Projection[2][:,i],
                                                            self.DataClass.HeadStr)
                
                #Run first calc instance quietly
                LastAct += self.DataClass.RamFit.AddFitCalc(self.DataClass.RamFit.RawData[self.DataClass.RamFit.Current].X0,
                                                            self.DataClass.RamFit.RawData[self.DataClass.RamFit.Current].Y0)
        
                #Make sure 0 values are set for the view range an duse them
                self.DataClass.RamFit.RawData[self.DataClass.RamFit.Current].Set0Values()
            
                #recheck if the viewdata change and load it up
                self.DataClass.RamFit.CompData[self.DataClass.RamFit.Current].LoadCalc()
            
                #initialise Lorrentzian definitions
                self.DataClass.RamFit.AddFit()
            
            #add visualisation class now defined globally in version 0.0.4
            self.DataClass.RamFit.AddFitVis()
            
            self.DataClass.RamFit.SetCreatedX()
        
        
    
        if self.DataClass.Type == 'Single':
            
            
            #here we don't pass thorugh a projection system...
            #as such the single specturm data is seen as corrupt for
            #further manipulaitons.
            #to avoid this case we suggest a simple array modification...
            OutZ = [Data.Z.Z[i,0,0,0][0] for i in range(Data.Z.Z.shape[0])]
            
            LastAct += Data.RamFit.AddFitData(Data.X.X,OutZ,Data.HeadStr)
            
            #Run first calc instance quietly
            LastAct += Data.RamFit.AddFitCalc(Data.RamFit.RawData[0].X0,Data.RamFit.RawData[0].Y0)
            #Make sure 0 values are set for the view range an duse them
            self.DataClass.RamFit.RawData[self.DataClass.RamFit.Current].Set0Values()
                
            #recheck if the viewdata change and load it up
            self.DataClass.RamFit.CompData[self.DataClass.RamFit.Current].LoadCalc()
                
            #initialise Lorrentzian definitions
            self.DataClass.RamFit.AddFit()
            
            #add visualisation class now defined globally in version 0.0.4
            self.DataClass.RamFit.AddFitVis()

            self.DataClass.RamFit.SetCreatedX()

    
    def RefreshSet(self,ID,init = False):
        '''
        ######################################################################
        Variable passing asked for a seconf function called RefreshSet
        Similar to Refresh but takes ID as an argument
        ######################################################################
        '''
        
        
        #Set the self.RefreshVar
        self.RefreshVar = [ID,0,'',False]
        
        #create a second window
        self.Refresh(init = init, Update = False)
    
    def Refresh(self,init = False, Update = False):
        '''
        ######################################################################
        Send out the refresh command to the plot
        ######################################################################
        '''
        
        #create a second window
        self.Parent.Vis_Fitting_Class.Refresh(init = init, Update = Update)
    

    
    def Change(self,variation):
    
        self.ChangeUpdate(variation,Update = False)
    
    def ChangeUpdate(self,variation, Update = True):

        #CALL CHANGE
        self.ChangeCurrent(variation)
        
        if not self.DataClass.Type == 'Single':
        
            TextInput = ' Id: '+str(int(self.DataClass.RamFit.Current))+ ' ( '
            
            TextInput += str(round(self.DataClass.Contour.Projection[1][self.DataClass.RamFit.Current],4))
            
            if self.DataClass.Type == 'Depth':
            
                TextInput += ' mum )'
            
            elif self.DataClass.Type == 'Temperature':
            
                TextInput += ' K )'
        else:
        
            TextInput = ''
        
        #try to change other windows to ...
        
        
        try:
            
            self.Parent.Vis_Fitting_Class.NavLabel.config(text = TextInput)
            
            self.Fitting.NavLabel.config(text = TextInput)
            
            self.Fitting.UpdateContent()
            
            self.Fitting.Fetch_All()
        
        except:
            
            pass
        
        #apply refresh to parent
        self.Refresh(Update = Update)

    def ChangeCurrent(self,variation):
        
        if ((self.DataClass.RamFit.Current+int(variation) < len(self.DataClass.RamFit.CompData))
            and (self.DataClass.RamFit.Current+int(variation) >= 0)):
        
            #apply change:
            self.DataClass.RamFit.Current = self.DataClass.RamFit.Current+int(variation)


    def CallConstructor(self, ID = 'All'):
        '''
        ######################################################################
        The constructor method builds all the lorrentzians and then refreshes 
        the view.
        ######################################################################
        '''
        
        #if no ID it means we do them all
        if ID == 'All':
            
            #Set the logical variable as fitted
            for k in range(0,len(self.DataClass.RamFit.Function_Pointers[0])):
                
                #process ir
                self.DataClass.RamFit.Constructor(Num = k)
                
                #set it fitted
                self.DataClass.RamFit.CompData[k].isFitted = True

        else:
            
            self.Fitting.SubmitAll()
            self.Fitting.Fetch_All()
            
            #process ir
            self.DataClass.RamFit.Constructor(Num = self.DataClass.RamFit.Current)
                
            #set it fitted
            self.DataClass.RamFit.CompData[self.DataClass.RamFit.Current].isFitted = True

            #set it fitted
            self.Refresh()

    
    def Consolidate(self):
        
        '''
        ######################################################################
        This aimes to refit all the current data over a few times to make 
        it more accurate
        
        ######################################################################
        '''
        #set self.Current = 0
        
        
        for k in range(0, len(self.DataClass.RamFit.Function_Pointers[0])):
            
            #this is a consolidation so loop 5 times should be enough
            for o in range(0,5):

                #Fetch it all
                for num in range(0,len(self.DataClass.RamFit.Function_Info_Pointers[0].Fields)):
                
                    #loop over parameters
                    for i in range(0,4):
                        
                        #save ouput
                        self.DataClass.RamFit.Function_Pointers[0][self.DataClass.RamFit.Current][num].ParametersIni[i+1] = float(self.DataClass.RamFit.Function_Info_Pointers[0].Fields[num][2*i+1].get())
            
                #First launch of the fitting
                self.DataClass.RamFit.FitLorr(self.Fitting.CalcPercLabel)
                    
                #sendout the text
                Text = ''
                
                for num in range(0,len(self.DataClass.RamFit.Function_Info_Pointers[0].Fields)):
                    
                    Text += str(self.DataClass.RamFit.Function_Pointers[0][self.DataClass.RamFit.Current][num].Parameters[1])+' '+str(self.DataClass.RamFit.Function_Pointers[0][self.DataClass.RamFit.Current][num].Parameters[2])+' '+str(self.DataClass.RamFit.Function_Pointers[0][self.DataClass.RamFit.Current][num].Parameters[3])+' '+str(self.DataClass.RamFit.Function_Pointers[0][self.DataClass.RamFit.Current][num].Parameters[4])+'\n'
    
                #output
                VisOut.TextBox(Title = 'Consolidating Lorrentzian Fit n. '+str(self.DataClass.RamFit.Current), Text = Text, state = 1)
                
                #refreshes the current window
                self.Change(0)
        
            #finnally apply index change
            self.ChangeCurrent(1)

    
    def Recalculate(self,ID = 'Loop'):
        
        '''
        ######################################################################
        this function wil launch the calculation routine set for our plot
        
        eventually it shoudl grab all field entries and then set them as init
        Like a big set button (could allow for removing set button eventually.
        
        ######################################################################
        '''
        
        #just in case
        if self.isRunning:
            
            
            #if the fitting routine is running the user probably wants to stop it
            try:
                
                #set the stoping event to true
                self.event.set()
                
                #change the button back
                self.Fitting.fThis00Button.config(text = 'Fit')
                
                #notify that this is a stoped state
                self.Fitting.CalcPercLabel.config(text = 'Stopped')
                self.Fitting.pb["value"] = 0
                
                #notify that we can refit
                self.isRunning = False
            
                #move on back since we aborted
                self.ChangeUpdate(-self.Sign)
        
        
            except:
                pass
    
    
        else:
            
            #######################################################################
            #The input can have three different forms...
            #
            # - The first is END or START:
            #       This will complete the fit series until the start or the end
            #
            # - ID = 0:
            #       Just execute the current fit
            #
            # - ID != 0: is to process all a number of fits.
            #
            #
            # Compared to the previous function it will now call the next step
            # manually and the proceed to threads... This is to avoid the beachb-
            # ball effect observed on version 0.0.4 that cannot be halted in
            # the applicaiton mode of the developement...
            #
            #
            #
            #######################################################################
            
    
            #copy = true for now add a check mark
            Copy    = True
            CopyVal = True
            CopyFix = True
            
            #######################################################################
            #select the type
            
            if ID != 'Loop':
                
                #remove the move on variable and related here
                try:
                    del self.OldStoredMin
            
                except:
                    pass
                
 
                #We are going to the end
                if ID == 'Consolidate':
                
                    #save the type
                    self.Type = 10
                    
                    #set the direction
                    self.Sign = 1
                
                    #Set the boundaries
                    self.Start = 0
                    self.End   = len(self.DataClass.RamFit.CompData)
                
                    #Repeat
                    self.Repeat = 5
                    self.CurrentRepeat = 0
                
                elif ID == '!Consolidate':
                
                    #save the type
                    self.Type = 10
                    
                    #set the direction
                    self.Sign = -1
                
                    #Set the boundaries
                    self.Start = 0
                    self.End   = len(self.DataClass.RamFit.CompData)
                
                    #Repeat
                    self.Repeat = 5
                    self.CurrentRepeat = 0
                

                elif ID == 'END':
                    
                    #save the type
                    self.Type = 0
                    
                    #set the direction
                    self.Sign = 1
                
                    #Set the boundaries
                    self.Start = self.DataClass.RamFit.Current
                    self.End   = len(self.DataClass.RamFit.CompData)
            
                #We are going to the start
                elif ID == 'START':
                    
                    #save the type
                    self.Type = 1
                
                    #set the direction
                    self.Sign = -1
                
                    #Set the boundaries
                    self.Start = self.DataClass.RamFit.Current
                    self.End   = 0
        
                #We are going down
                elif ID < 0:

                    #save the type
                    self.Type = 2
                    
                    #set the direction
                    self.Sign = -1
                
                    #Set the boundaries
                    self.Start = self.DataClass.RamFit.Current
                    self.End   = self.Start + ID
                    
                    #if to long
                    if self.End < 0:
                        self.End = 0
                
                #We are going up
                elif ID > 0:
                    
                    #save the type
                    self.Type = 3
                    
                    #set the direction
                    self.Sign = 1
                
                    #Set the boundaries
                    self.Start = self.DataClass.RamFit.Current
                    self.End   = self.Start + ID
                
                    #if to long
                    if self.End >= len(self.DataClass.RamFit.CompData):
                        self.End = len(self.DataClass.RamFit.CompData) - 1
                        
                #We are going up
                elif ID == 0:
                    
                    #save the type
                    self.Type = 4
                    
                    #nothing needs to be done
                    #Set the boundaries
                    self.Sign  = 0
                    self.Start = self.DataClass.RamFit.Current
                    self.End   = self.Start

                
                #We do nothing
                else:
                    return
        
            #######################################################################
            #Consitency check
            
            if self.Type == 0 or self.Type == 3 or self.Type == 10:
                
                if self.DataClass.RamFit.Current+self.Sign > self.End:
                    
                    #stop
                    return
        
            if self.Type == 1 or self.Type == 2:
                
                if self.DataClass.RamFit.Current+self.Sign < self.End:
                    
                    #stop
                    return
        
            #######################################################################
            #What to do for movers
            #This section assumes that the user did the first fine tuning
            #therefore we are going to copy the current scheme and then
            #move onto the next item
            
            #Check if we have a minima stabilisator set..
            if self.Fitting.Stability.get() == 1:
                
                #grab the new value of the min and compare to the one stored previously
                try:
                    self.NewStoredMin = self.DataClass.RamFit.Function_Pointers[0][self.DataClass.RamFit.Current+self.Sign][0].Parameters[3]

                    if self.NewStoredMin - self.OldStoredMin < 1:
                        AllowedtoMove = True
                    else:
                        self.OldStoredMin = self.DataClass.RamFit.Function_Pointers[0][self.DataClass.RamFit.Current+self.Sign][0].Parameters[3]
                        AllowedtoMove = False
                        
                except:
                    self.OldStoredMin = self.DataClass.RamFit.Function_Pointers[0][self.DataClass.RamFit.Current+self.Sign][0].Parameters[3]
                    AllowedtoMove = False


            else:
                AllowedtoMove = True


            #normal movers
            if self.Type != 4 and self.Type != 10 and AllowedtoMove:
                
                #Be sure to copy variables
                self.Fitting.SubmitAll()
                
                #Do we copy over the values ????
                if self.Fitting.CopyVal.get() == 1:
                    
                    #start the iteration over all function
                    for k in range(len(self.DataClass.RamFit.Function_Info_Pointers)):
                        
                        if len(self.DataClass.RamFit.Function_Pointers[k][self.DataClass.RamFit.Current]) > 0:
                            
                            for num in range(0,len(self.DataClass.RamFit.Function_Info_Pointers[k].Fields)):

                                self.DataClass.RamFit.Function_Pointers[k][self.DataClass.RamFit.Current+self.Sign][num].Parameters = numpy.copy(self.DataClass.RamFit.Function_Pointers[k][self.DataClass.RamFit.Current][num].Parameters)
                    
                                self.DataClass.RamFit.Function_Pointers[k][self.DataClass.RamFit.Current+self.Sign][num].ParametersIni = numpy.copy(self.DataClass.RamFit.Function_Pointers[k][self.DataClass.RamFit.Current][num].Parameters)
                

                            
                #Are we copying fixed elements ???
                if self.Fitting.CopyFix.get() == 1:

                    #start the iteration over all function
                    for k in range(len(self.DataClass.RamFit.Function_Info_Pointers)):
                        
                        if len(self.DataClass.RamFit.Function_Pointers[k][self.DataClass.RamFit.Current]) > 0:
                            
                            for num in range(0,len(self.Fitting.Fix[k])):

                                #save ouput
                                self.DataClass.RamFit.Function_Pointers[k][self.DataClass.RamFit.Current+self.Sign][num].ParametersFix = numpy.copy(self.DataClass.RamFit.Function_Pointers[k][self.DataClass.RamFit.Current][num].ParametersFix)

                #Do we omit the first round of minima calculation
                #this is usefull in propagation runs.
                if self.Fitting.IgnoreFirstMin.get() == 1:
                    
                    #Set the variable to True else to False
                    self.DataClass.RamFit.IgnoreFirstMin = True
                
                else:
                    #Set the variable to True else to False
                    self.DataClass.RamFit.IgnoreFirstMin = False
                

                #move if allowed
                self.ChangeCurrent(self.Sign)
        
        
            elif self.Type == 4:
                
                self.Fitting.SubmitAll()
        
            #the consilation mover
            if self.Type == 10:
                
                #Do a check
                if self.CurrentRepeat == self.Repeat+1:
                    
                    #move on else redo again
                    self.ChangeCurrent(self.Sign)
                
                    #reset the variable
                    self.CurrentRepeat = 0
                
                else:
                    
                    #Move up of one
                    self.ChangeCurrent(0)
                    self.CurrentRepeat += 1

            #######################################################################
            #What to do for all
            #Run the calculations
            if not self.Type == 10:
                
                #Build an drun the thread and initilise the listener
                self.RunThread()

            else:

                #Built and run a multithread (not operational yet)
                self.RunMultiThread()


            #######################################################################
            #What was done after
            #sendout the text
            Text = ''
            
            Text += 'Paramters\n'
            
            for kk in range(0, len(self.DataClass.RamFit.Function_Info_Pointers)):
                
                if len(self.DataClass.RamFit.Function_Pointers[kk][self.DataClass.RamFit.Current]) > 0:
            
                    for num in range(0, len(self.DataClass.RamFit.Function_Info_Pointers[kk].Fields)):
                        
                        for ii in range(self.DataClass.RamFit.Function_Info_Pointers[kk].ParameterNumber):
                        
                            Text += (str(self.DataClass.RamFit.Function_Pointers[kk][self.DataClass.RamFit.Current][num].Parameters[ii])
                                     + ' ')
                
                        Text += '\n'
            
            Text += 'Fixed\n'
            
            
            for kk in range(0, len(self.DataClass.RamFit.Function_Info_Pointers)):
            
                if len(self.DataClass.RamFit.Function_Pointers[kk][self.DataClass.RamFit.Current]) > 0:
                    
                    for num in range(0, len(self.DataClass.RamFit.Function_Info_Pointers[kk].Fields)):
                        
                        for ii in range(self.DataClass.RamFit.Function_Info_Pointers[kk].ParameterNumber):
                        
                            Text += (str(self.DataClass.RamFit.Function_Pointers[kk][self.DataClass.RamFit.Current][num].ParametersFix[ii])
                                     + ' ')
                
                        Text += '\n'

            if self.Type == 10:
                
                #senfdout
                VisOut.TextBox(Title = 'Consolidating Lorrentzian Fit n.'
                               + str(self.DataClass.RamFit.Current)
                               + '('+str(self.CurrentRepeat)
                               + 'of'
                               + str(self.Repeat)
                               + ')',
                               Text = Text,
                               state = 1,
                               Target = self.Fitting.LogField)

            else:

                #output
                VisOut.TextBox(Title = 'Lorrentzian Fit n.'
                               + str(self.DataClass.RamFit.Current),
                               Text = Text,
                               state = 1,
                               Target = self.Fitting.LogField)



    def RunThread(self):
        
        '''
        ######################################################################
        This is the run function that is now called to run a process witout
        hindering the multi threatment. 
        
        
        
        ######################################################################
        '''
        #launch the container Builder
        Container = self.Fitting.GrabContainers()
    
        #First launch of the fitting
        self.Run, self.queue, self.event = self.DataClass.RamFit.ThreadedFit(Container = Container)
                
        #start and set
        self.Run.start()
        self.isRunning = True
                
        #configure the button to say stop
        self.Fitting.fThis00Button.config(text = 'o Stop o')
                
        #launch the process funciton
        self.Fitting.master.after(20,self.ProcessAdvance)
    
    def RunMultiThread(self):
        
        '''
        ######################################################################
        This is the run function that is now called to run a process witout
        hindering the multi threatment. 
        
        
        This section could later be modified to hold only a multithread 
        routine
        ######################################################################
        '''
        #launch the container Builder
        Container = self.Fitting.GrabContainers()
        
        #First launch of the fitting
        self.Run, self.queue, self.event = self.DataClass.RamFit.ThreadedFit(Container = Container)
                
        #start and set
        self.Run.start()
        self.isRunning = True
                
        #configure the button to say stop
        self.Fitting.fThis00Button.config(text = 'o Stop o')
                
        #launch the process funciton
        self.Fitting.master.after(20,self.ProcessAdvance)
    
    def ProcessAdvance(self):
        
        '''
        ######################################################################
        This function was introduced to manage the visual feedback of the 
        processing. 
        
        Later on it was also decided that this should callall the next Steps...
        invokers so to speek
        
        ######################################################################
        '''
        
        #self.Fitting.CalcPercLabel.config(text = self.queue.get(0))
        
        error = False
        queueLength = self.queue.qsize()
        
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
        
            if A[0] == 'Progress':
                
                #I0f the last queue element is 'Stop' we stop and we call the
                #Whatnext manager
                if A[1] == 'Stop':
                
                    #proceed to visuals 100%
                    self.Fitting.CalcPercLabel.config(text = '100.00%')
                    self.Fitting.pb["value"] = 100
                    
                    #set the button back to fitting
                    self.Fitting.fThis00Button.config(text = 'Fit')
                    
                    #refresh the visual
                    self.ChangeUpdate(0)
                    
                    #NEED THIS
                    self.Fitting.Fetch_All()
                    self.Fitting.SubmitAll()
                
                    #do checks...
                    if not self.Type == 4:
                        
                        #finish
                        self.isRunning = False
                        
                        #try to move on
                        self.Recalculate(ID = 'Loop')
                    
                    
                    else:
                        #finish
                        self.isRunning = False
                
                #Else we do the necessary changes to the signalers
                else:
                
                    #try to change the visual.
                    try:
                        
                        #If the code is runing to avoid some late update call...
                        if self.isRunning:

                            #start the update
                            self.Fitting.CalcPercLabel.config(text = str(A[1]))
                            
                            #set progressbar
                            self.Fitting.pb["value"] = float(A[1].split('%')[0])
                            
                            #restart listener
                            self.Fitting.master.after(20,self.ProcessAdvance)
                

                    except:
                        pass
        
        else:
            self.Fitting.master.after(20,self.ProcessAdvance)
    
    
    def SetViewRange(self):
        '''
        ######################################################################
        To set the view range will use a similar routine as used in 
        bersion 2.0. the difference being the Fetching from the input field
        We implement a try method to convert to float and 
        check that the min is greater than the max
        
        of conditions are not satified we change the input fields accordingly
        ######################################################################
        '''
        
        for i in range(0, len(self.DataClass.RamFit.RawData)):
            
            #Set Viewrange
            ViewRange   = [float(self.ViewField[0].get()),float(self.ViewField[1].get())]
                
            #Fix range into Frame
            if ViewRange[0] < numpy.min(self.DataClass.RamFit.RawData[i].X):
                ViewRange[0] = numpy.min(self.DataClass.RamFit.RawData[i].X)+0.2


            #Fix range into Frame
            if ViewRange[1] > numpy.max(self.DataClass.RamFit.RawData[i].X):
                ViewRange[1] = numpy.max(self.DataClass.RamFit.RawData[i].X)-0.2

            #Find associated indexes
            ViewIdx = Utility.FindIdxD(ViewRange[0],ViewRange[1],self.DataClass.RamFit.RawData[i].X)
        
            #Set
            self.DataClass.RamFit.RawData[i].RangeX = ViewRange
            self.DataClass.RamFit.RawData[i].IndexX = [ViewIdx[1],ViewIdx[0]]
               
            #process
            self.DataClass.RamFit.RawData[i].Set0Values()
    
            #Reprocess calc Data
            self.DataClass.RamFit.CompData[i].LoadCalc()
    
        self.DataClass.RamFit.SetCreatedX()
        
        #Replot
        self.RefreshSet(0)
                                                            
                                                  
    def SetCalcRange(self):
        '''
        ######################################################################
        To set the view range will use a similar routine as used in 
        bersion 2.0. the difference being the Fetching from the input field
        We implement a try method to convert to float and 
        check that the min is greater than the max
        
        of conditions are not satified we change the input fields accordingly
        ######################################################################
        '''
        
        for i in range(0, len(self.DataClass.RamFit.RawData)):
            #Set Viewrange
            self.DataClass.RamFit.CompData[i].ViewRange   = [float(self.CalcField[0].get()),float(self.CalcField[1].get())]
        
            #Set
            self.DataClass.RamFit.CompData[i].BaseExcl = self.CalcField[2].get()
        
            #
            self.DataClass.RamFit.CompData[i].LoadCalc()
        
            #Call remove range
            self.DataClass.RamFit.CompData[i].RemoveRanges()
        
        #Replot
        self.Refresh()
    
    
    def Reset(self,num):
        '''
        ######################################################################
        launch the lorr window reset routine
        ######################################################################
        '''
        
        self.Fitting.Reset(num)

    def Reset_All(self):
        '''
        ######################################################################
        loop over reset for all lorrentzians
        ######################################################################
        '''
    
        for i in range(0,len(self.DataClass.RamFit.Function_Pointers[0][self.DataClass.RamFit.Current])):
            self.Fitting.Reset(i)

    def Fetch_All(self):
        '''
        ######################################################################
        loop over Fetch for all lorrentzians
        ######################################################################
        '''
    
        for i in range(0,len(self.DataClass.RamFit.Function_Pointers[0][self.DataClass.RamFit.Current])):
            self.Fitting.Fetch(i)

    def Fetch(self,num):
        '''
        ######################################################################
        Go back to the initial values
        ######################################################################
        '''
        self.Fitting.Fetch(num)



    def Copy(self,num):
        '''
        ######################################################################
        loop over Fetch for all functions and copies their values over to the
        neighbours in the right direction. Note that the num here refers to 
        the amount of copies to pass and that the sign matters...
        ######################################################################
        '''
        if num < 0:
            Sign = -1
        else:
            Sign = 1
        
        #we now loop over all available function
        for kk in range(0, len(self.DataClass.RamFit.Function_Pointers)):
            
            if numpy.abs(num) == 1:
                
                #copy for one single
                for i in range(0,len(self.DataClass.RamFit.Function_Pointers[kk][self.DataClass.RamFit.Current+num])):
            
                    for j in range(0,self.DataClass.RamFit.Function_Info_Pointers[kk].ParameterNumber):
                        self.DataClass.RamFit.Function_Pointers[kk][self.DataClass.RamFit.Current+num][i].Parameters[j+1] = numpy.copy(self.DataClass.RamFit.Function_Pointers[kk][self.DataClass.RamFit.Current][i].Parameters[j+1])

            else:
                
                #copy for multiple
                for k in range(1,numpy.abs(num)):
                    
                    for i in range(0,len(self.DataClass.RamFit.Function_Pointers[kk][self.DataClass.RamFit.Current+Sign*k])):
            
                        for j in range(0,self.DataClass.RamFit.Function_Info_Pointers[kk].ParameterNumber):
                            self.DataClass.RamFit.Function_Pointers[kk][self.DataClass.RamFit.Current++Sign*k][i].Parameters[j+1] = numpy.copy(self.DataClass.RamFit.Function_Pointers[kk][self.DataClass.RamFit.Current][i].Parameters[j+1])


    def Search(self):
        
        try:
            
            self.lst1 = []
            
            for Pointer in self.DataClass.RamFit.Function_Pointers:
                
                try:
                
                    for Element in Pointer[0]:
                
                        if not Element.Group in self.lst1:
                            self.lst1.append(Element.Group)
        
                except:
                    pass
                        
            self.Drop_2[0]['menu'].delete(0,'end')
                
            for Element in self.lst1:
                   
                self.Drop_2[0]['menu'].add_command(label = Element , command =  tk._setit(self.ExportVar, Element))
        
        except:
        
                pass

class Variable_Management_Class:
    
    '''
    ####################################################################################
    This class underwent major restructuration in version 0.1.02 It was decided that
    the interface recquires more felixibility and should therefore be scorllable
    and contain buttons that allow for adding or removing lorrentzians. 
    
    It was also decided that the Save/load interface should be separated into another
    tab that is not related to the saving window
    ####################################################################################
    '''

    def __init__(self, master,DataClass,HowMany,Parent,State, isWindow = True):
        
        ##############################
        ##############################
        #link the DataClass
        self.DataClass = DataClass
        self.Parent    = Parent
        self.HowMany   = HowMany
        
        #set master
        self.master = master
        
        ##############################
        ##############################
        #if it is a window set the title
        if isWindow:
            self.master.title("Lorrentzian Fitting Parameters")

            self.master.configure(background = 'black')
            self.master.resizable(width=False, height=False)
        
        #set the padding
        self.padding = '10p'
        
        #set the Frame
        self.Frame  = ttk.Frame(self.master)
        
        ##############################
        ##############################
        
        #Initiate the amount of lorrentzians in each dataclass
        for i in range(0, len(self.DataClass.RamFit.RawData)):
            
            self.DataClass.RamFit.AddFit(i,self.HowMany)
        
        #a reset si in order
        self.DataClass.RamFit.Fig.Reset()
        
        ##############################
        ##############################
        #Populate the manager
        self.Initialize_Variables()
        
        #call navigator populator
        self.Populate_Navigator(2)
        
        #call navigator populator
        self.Populate_Fitter(6)
        
        #Populate the thing
        self.Build_NoteBooks(4)
        
        
        ##############################
        ##############################
        #introduce the navigator if needed
        if isWindow:
            self.Frame.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.W+tk.E)
        
        ##############################
        ##############################
        #configure the Frame
        self.Frame.grid_columnconfigure(0, weight = 1)
        self.Frame.grid_rowconfigure(4, weight = 1)
        
        ##############################
        ##############################
        #Bind the hider
        
        #set the visibility parameter
        self.EntryFrameVisible = True
        
        #bind to hide
        self.Parent.Root.bind('<Control-d>', self.HideEntryGrid)
        
        #If the system asked to hide it
        if State == 'Hidden':
            
            self.HideEntryGrid(None)


    def Initialize_Variables(self):
        '''
        ####################################################################################
        This function was added to provide a safder way to create variables accross this
        class. This avoinds calling htem locally at random spots.
        ####################################################################################    
        '''
    
        ################################################
        #variables linked to the fitting routines
        self.IgnoreFirstMin = tk.IntVar()
        self.CopyVal        = tk.IntVar()
        self.CopyFix        = tk.IntVar()
        self.Stability      = tk.IntVar()

        ################################################
        #variables linked to the Lorrents boundary routines
        for Target in self.DataClass.RamFit.Function_Info_Pointers:
        
            #initialise the list
            Target.BoundariesVar = []
            
            #loop over
            for j in range(2 * Target.ParameterNumber):
            
                #set the vars
                Target.BoundariesVar.append(tk.IntVar())

    def Build_NoteBooks(self, Location):
        '''
        ####################################################################################
        In order to avoid having millions of buttons before release 0.0.5 we focus on 
        tabs rather than having tons of buttons...
        ####################################################################################    
        '''
        #add notebook capabilities into this Frame
        self.NoteBookFrame = ttk.Frame(self.Frame, padding= self.padding)
        self.NoteBook      = ttk.Notebook(self.NoteBookFrame)
        
        #build all small Frames...
        self.NoteBookPage  = [None] * 4
        self.NoteBookTitle = ['Funciton Parameters','Fit Para.','Edit Visual', 'Log']
                          
        self.NoteBookPage[0] = self.Populate_Entries(-1,self.NoteBook)
        self.NoteBookPage[1] = self.Populate_Boundaries(-1,self.NoteBook)
        self.NoteBookPage[2] = self.Populate_Visual_Editor()#tk.Frame(self.NoteBook)
        self.NoteBookPage[3] = self.Populate_Log()

        #Build the notebooks
        k = 0
        for i in range(0,len(self.NoteBookTitle)):
            self.NoteBook.add(self.NoteBookPage[i],text = self.NoteBookTitle[i] )
        
        #We call the population routine putting all butons and entry fields
        self.NoteBook.grid(row = 0, column = 0, sticky= tk.E+tk.W+tk.N+tk.S)
        
        #give weight...
        self.NoteBookFrame.grid_columnconfigure(0, weight = 1)
        self.NoteBookFrame.grid_rowconfigure(0, weight = 1)

        #Place the Frame into the main Frame...
        self.NoteBookFrame.grid(row = Location ,column = 0, sticky= tk.E+tk.W+tk.N+tk.S)

    def Populate_Visual_Editor(self,Location = 1, Parent = None):
        '''
        ####################################################################################
        This function will build and Populate the visual editor
        
        This load a Simpleplot routine and the default iPlot function will be used to allow
        for interaction.
        ####################################################################################
        '''
        #######################################
        #######################################
        #Create the container Frame
        self.VisualFrame = ttk.Frame(self.NoteBook)
        
        self.VisualFrame.grid_columnconfigure(0, weight = 1)
        self.VisualFrame.grid_rowconfigure(1, weight = 1)
    
        #######################################
        #######################################
        #Create the subFrame
        self.TopVisFrame = ttk.Frame(self.VisualFrame, padding = self.padding)
    
        self.MidPlotFrame = ttk.Frame(self.VisualFrame, padding = self.padding)
    
        self.BotVisFrame = ttk.Frame(self.VisualFrame, padding = self.padding)
    
        #######################################
        #######################################
        #place the subFrame
        self.TopVisFrame.grid(  row = 0, column = 0, sticky = tk.W + tk.E + tk.N + tk.S)
        self.MidPlotFrame.grid( row = 1, column = 0, sticky = tk.W + tk.E + tk.N + tk.S)
        self.BotVisFrame.grid(  row = 2, column = 0, sticky = tk.W + tk.E + tk.N + tk.S)
    
        #######################################
        #######################################
        #introduce The selectors here
        self.VisSelectors   = []
        self.VisButtons     = []
        self.VisLabels      = []
        self.VisStringVars  = [tk.StringVar(),tk.StringVar(),tk.StringVar()]
        self.VisSelectorList = []
        self.MakeFixed      = tk.IntVar()
    
        #######################################
        #######################################
        #set intvars
        self.VisStringVars[0].set('Lorentzian')
        self.VisStringVars[1].set('Position')
        self.VisStringVars[2].set('0')
        self.MakeFixed.set(1)
        
        #######################################
        self.VisButtons.append([ttk.Button(self.TopVisFrame,
                                           text = 'Load',
                                           command = self.LoadVis),
                                0,
                                6,
                                1,
                                1,
                                tk.E + tk.W])
                                
                                
        self.VisButtons.append([ttk.Button(self.BotVisFrame,
                                           text = 'Set',
                                           command = self.SetVis),
                                0,
                                1,
                                1,
                                1,
                                tk.E + tk.W])
                                
        self.VisButtons.append([ttk.Checkbutton(self.BotVisFrame,
                                           text = 'Make Fixed...',
                                           variable = self.MakeFixed),
                                0,
                                2,
                                1,
                                1,
                                tk.E + tk.W])
           
        #######################################
        self.VisLabels.append([ttk.Label(self.TopVisFrame,
                                           text = 'Function:'),
                                0,
                                0,
                                1,
                                1,
                                tk.E + tk.W])
                                
        self.VisLabels.append([ttk.Label(self.TopVisFrame,
                                           text = 'Parameter:'),
                                0,
                                2,
                                1,
                                1,
                                tk.E + tk.W])
              
        self.VisLabels.append([ttk.Label(self.TopVisFrame,
                                           text = 'Number:'),
                                0,
                                4,
                                1,
                                1,
                                tk.E + tk.W])
           
        #######################################
        self.ResetVisSelector()
                           
        #######################################
        #######################################
        #Place it all here
                           
        for List in [self.VisLabels , self.VisButtons]:
        
            for Element in List:
            
                Element[0].grid(row         = Element[1],
                                column      = Element[2],
                                rowspan     = Element[3],
                                columnspan  = Element[4],
                                sticky      = Element[5])
                                
        #######################################
        #######################################
        #introduce our new plot canvas here
        self.VisCanvas = SimplePlot.MultiPlotCanvas(self.MidPlotFrame,
                                                    grid = [[True]],
                                                    ratioX   = [1],
                                                    ratioY   = [1],
                                                    bg="white",
                                                    highlightthickness=0)
                                                    
        #grab the subplot definitions
        self.ax = self.VisCanvas.GetSubPlot(0,0)
        
        #######################################
        #######################################
        #Set some padding parameters
        self.ax.Axes.PaddingIn      = [0.0 , 0.0, 0.0 , 0.0 ]
        self.ax.Axes.PaddingOut     = [0.15, 0.1, 0.05, 0.05]
        self.ax.Axes.Thickness      = [2,2,2,2]
        self.ax.Axes.XTickSpacing   = 50
        self.ax.Axes.XTickType      = 1
        
        self.ax.Axes.isYSci         = [True,True]
        self.ax.Pointer.isYSci      = [True,True]
    
        self.ax.Pointer.YSciPrecision     = '%.1e'
        self.ax.Pointer.Sticky = 1
        self.ax.Axes.YSciPrecision        = ['%.1e','%.1e']
        self.ax.Axes.XSciPrecision        = ['%.1e','%.1e']
        
        
        
        #launch the drawer once will initialise all clases
        self.ax.DrawAll()
        
        #set the default imaging mode to Tkinter Canvas
        self.ax.Live = 1
    
        return self.VisualFrame
        
        
    def Populate_Boundaries(self,Location = 1, Parent = None):
        '''
        ####################################################################################
        This function will create the Frame linking all the boundaries to the fitter. 
        The boundaries can then be Fetched to build the containers in Ramfit.
        Please note that each conatainer can be tunred off or on to laod the default
        parameters.
        ####################################################################################
        '''
        #######################################
        #######################################
        #Create the container Frame
        #create the Frame which will sit in the scroll canvas
        self.BoundaryTempFrame = ttk.Frame(self.NoteBook)
        
        self.BoundaryTempFrame.grid_columnconfigure(0, weight = 1)
        self.BoundaryTempFrame.grid_rowconfigure(0, weight = 1)
        
        #create the canvas that will handle the scrolling
        self.Boundaryvscroll = tk.Scrollbar(self.BoundaryTempFrame)
        
        #######################################
        #######################################
        #Create the Canvas
        #we need to grab the system abckground for the canvas
        self.BoundaryCanvas = tk.Canvas(self.BoundaryTempFrame,
                                        bd=0,
                                        highlightthickness=0,
                                        background = '#EDEFF0',
                                        yscrollcommand = self.Boundaryvscroll.set)
        
        self.BoundaryCanvas.grid(row=0,column=0, sticky='news')
        
        self.Boundaryvscroll.grid(row = 0, column=1, sticky='ns')
        self.Boundaryvscroll.configure(command = self.BoundaryCanvas.yview)
        
        #create the Frame which will sit in the scroll canvas
        self.BoundaryFrame = ttk.Frame(self.BoundaryCanvas, padding = self.padding)
        
        #######################################
        #######################################
        #configure actions
        self.BoundaryCanvas.bind('<Configure>', self.OnFrameConfigure_2)
        self.BoundaryFrame.bind('<Configure>', self.FrameWidth_2)
        
        #######################################
        #######################################
        #Create the label Frames
        self.BoundariesGeneralFrame     = ttk.LabelFrame(self.BoundaryFrame,
                                                         text = 'General options:',
                                                         padding = self.padding )
                                                         
        self.BoundariesGeneralFrame.grid(row = 0, column = 0, sticky = tk.N+tk.S+tk.E+tk.W)
        self.BoundariesGeneralFrame.grid_columnconfigure(10, weight = 1)
        
        
        #######################################
        #######################################
        #Create the label Frames
        self.FunctionBoundaryFrames     = []
        
        for i in range(len(self.DataClass.RamFit.Function_Info_Pointers)):
        
            self.FunctionBoundaryFrames.append(ttk.LabelFrame(self.BoundaryFrame,
                                                              text = self.DataClass.RamFit.Function_Info_Pointers[i].Name+' options:',
                                                              padding = self.padding ))
        
        
        
            self.FunctionBoundaryFrames[i].grid(row = i+1,
                                                column = 0,
                                                sticky = tk.N+tk.S+tk.E+tk.W)
        
        
        
        
        self.BoundaryFrame.grid_columnconfigure(0, weight = 1)
        
        for i in range(len(self.DataClass.RamFit.Function_Info_Pointers)+1):
        
            self.BoundaryFrame.grid_rowconfigure(i, weight = 1)
        
        #######################################
        #######################################
        #Call Populaters of the label Frames
        
        self.Populate_BoundariesGeneral(self.BoundariesGeneralFrame)
        
        for i in range(len(self.DataClass.RamFit.Function_Info_Pointers)):
        
            self.Populate_BoundariesFunction(i, self.FunctionBoundaryFrames[i])
        
        #######################################
        #######################################
        #Call the reseters
        self.ResetBoundariesGeneral()
        
        for i in range(len(self.DataClass.RamFit.Function_Info_Pointers)):
            
            self.ResetBoundariesFunction(i)
        
        
        #set the system default
        if os.name == 'nt':
        
            self.SysEntryWidth = 10
            self.SysLabelWidth = 8
            self.SysButtonWidth = 5
        
        else:
        
            self.SysEntryWidth = 7
            self.SysLabelWidth = 6
            self.SysButtonWidth = 3
        
        self.BoundaryCanvas.create_window(0,
                                          0,
                                          window = self.BoundaryFrame)
                                       
        return self.BoundaryTempFrame

    def Populate_BoundariesGeneral(self, Parent):
        '''
        ####################################################################################
        This instance will Populate the general boundaries and options
        ####################################################################################
        '''
    
        ################################################
        ################################################
        #set all the Labels
        self.BoundariesGeneralLabels = [None]*4
        
        self.BoundariesGeneralLabels[0] =  [ttk.Label(Parent,
                                                       text = 'N. of total iterations:'  ,
                                                       #width = self.SysLabelWidth,
                                                       justify = tk.CENTER,
                                                       anchor = tk.E),
                                             0,
                                             0,
                                             1,1]
                                          
        self.BoundariesGeneralLabels[1] =  [ttk.Label(Parent,
                                                       text = 'Order:'  ,
                                                       #width = self.SysLabelWidth,
                                                       justify = tk.CENTER,
                                                       anchor = tk.E),
                                             1,
                                             0,
                                             1,1]
    
        self.BoundariesGeneralLabels[2] =  [ttk.Label(Parent,
                                                       text = 'Dry run on propagate:'  ,
                                                       #width = self.SysLabelWidth,
                                                       justify = tk.CENTER,
                                                       anchor = tk.E),
                                             2,
                                             0,
                                             1,1]
    
        self.BoundariesGeneralLabels[3] =  [ttk.Label(Parent,
                                                       text = 'Fit Precision:'  ,
                                                       #width = self.SysLabelWidth,
                                                       justify = tk.CENTER,
                                                       anchor = tk.E),
                                             3,
                                             0,
                                             1,1]
    
        ################################################
        ################################################
        #set all the entries
        self.BoundariesGeneralEntries = [None]*4
        
        self.BoundariesGeneralEntries[0] =  [ttk.Entry(Parent,
                                                       width = self.SysEntryWidth,
                                                       justify = tk.CENTER),
                                             0,
                                             1,
                                             1,1]
                                          
        self.BoundariesGeneralEntries[1] =  [ttk.Entry(Parent,
                                                       width = self.SysLabelWidth,
                                                       justify = tk.CENTER),
                                             1,
                                             1,
                                             1,1]
    
        self.BoundariesGeneralEntries[2] =  [ttk.Entry(Parent,
                                                       width = self.SysEntryWidth,
                                                       justify = tk.CENTER),
                                             2,
                                             1,
                                             1,1]
                                             
        self.BoundariesGeneralEntries[3] =  [ttk.Entry(Parent,
                                                       width = self.SysEntryWidth,
                                                       justify = tk.CENTER),
                                             3,
                                             1,
                                             1,1]
                                             
        ################################################
        ################################################
        #set all the entries
        self.BoundariesGeneralCheck = [None]*4
        
        self.BoundariesGeneralCheck[0]   = [ttk.Checkbutton(Parent,
                                                            variable = self.IgnoreFirstMin,
                                                            text = 'Skip First'),
                                            0,
                                            2,
                                            1,1]
                                          
        self.BoundariesGeneralCheck[1]   = [ttk.Checkbutton(Parent,
                                                            variable = self.CopyVal,
                                                            text = 'Copy Value'),
                                            1,
                                            2,
                                            1,1]
                                          
        self.BoundariesGeneralCheck[2]   = [ttk.Checkbutton(Parent,
                                                            variable = self.CopyFix,
                                                            text = 'Copy Fixes'),
                                            2,
                                            2,
                                            1,1]
                                          
        self.BoundariesGeneralCheck[3]   = [ttk.Checkbutton(Parent,
                                                            variable = self.Stability,
                                                            text = 'Check Stab'),
                                            3,
                                            2,
                                            1,1]
                                            
        ################################################
        ################################################
        #set all the entries
        self.BoundariesGeneralButton = [None]*1
        
        self.BoundariesGeneralButton[0]   = [ttk.Button(Parent,
                                                        command = self.ResetBoundariesGeneral,
                                                        text = 'Reset'),
                                            3,
                                            3,
                                            1,1]
                                            
        ################################################
        ################################################
        #run the final placement method
        for List in [self.BoundariesGeneralLabels,
                     self.BoundariesGeneralEntries,
                     self.BoundariesGeneralCheck,
                     self.BoundariesGeneralButton]:
                     
            for Element in List:
                
                Element[0].grid(row         = Element[1],
                                column      = Element[2],
                                rowspan     = Element[3],
                                columnspan  = Element[4],
                                sticky      = tk.E + tk.W)

    def Populate_BoundariesFunction(self, idx, Parent):
        '''
        ####################################################################################
        This instance will Populate the general boundaries and options
        ####################################################################################
        '''
        
        #grab the target
        Target = self.DataClass.RamFit.Function_Info_Pointers[idx]
        
        ################################################
        ################################################
        #set all the general Labels
        BoundariesLabels = [None]*(2 + 2 * Target.ParameterNumber)
        
        BoundariesLabels[0] =  [ttk.Label(Parent,
                                          text = 'N. of total iterations :'  ,
                                          justify = tk.CENTER,
                                          anchor = tk.E),
                                0,
                                0,
                                1,1]
                                             
        BoundariesLabels[1] =  [ttk.Label(Parent,
                                          text = 'Order :'  ,
                                          justify = tk.CENTER,
                                          anchor = tk.E),
                                1,
                                0,
                                1,1]
                                          
        ################################################
        ################################################
        #set all the variable
        for i in range(Target.ParameterNumber):
        
            BoundariesLabels[2 * i + 2] =  [ttk.Label(Parent,
                                                   text = 'Rel.'+Target.ParameterNames[i]+':'   ,
                                                   justify = tk.CENTER,
                                                   anchor = tk.E),
                                         2 * i + 2,
                                         0,
                                         1,1]
                                         
            BoundariesLabels[2 * i + 3] =  [ttk.Label(Parent,
                                                   text = 'Abs.'+Target.ParameterNames[i]+':'  ,
                                                   justify = tk.CENTER,
                                                   anchor = tk.E),
                                         2 * i + 3,
                                         0,
                                         1,1]

        ################################################
        #set all the entries
        BoundariesEntries = [None]* (Target.ParameterNumber * 4 + 2)
        
        #the iteration entry
        BoundariesEntries[0] =  [ttk.Entry(Parent,
                                                width = self.SysEntryWidth,
                                                justify = tk.CENTER),
                                      0,
                                      1,
                                      1,1]
                                          
        #the order
        BoundariesEntries[1] =  [ttk.Entry(Parent,
                                                width = self.SysLabelWidth,
                                                justify = tk.CENTER),
                                      1,
                                      1,
                                      1,1]
        
        for i in range(2 * Target.ParameterNumber):
        
            #the iteration entry
            BoundariesEntries[2*i+2] =  [ttk.Entry(Parent,
                                                   width = self.SysEntryWidth,
                                                   justify = tk.CENTER),
                                         i+2,
                                         2,
                                         1,1]
                                              
            #the order
            BoundariesEntries[2*i+3] =  [ttk.Entry(Parent,
                                                   width = self.SysLabelWidth,
                                                   justify = tk.CENTER),
                                        i+2,
                                        3,
                                        1,1]
                 

                                             
        ################################################
        ################################################
        #set all the entries
        BoundariesCheck = [None]*(Target.ParameterNumber * 2)
        
        for i in range(2 * Target.ParameterNumber):
        
            BoundariesCheck[i]   = [ttk.Checkbutton(Parent,
                                                    variable = Target.BoundariesVar[i],
                                                    text = 'On/Off'),
                                    2 + i,
                                    1,
                                    1,1]
                                          

                    
        ################################################
        ################################################
        #set all the entries
        BoundariesButton = [None]*1
        
        BoundariesButton[0]   = [ttk.Button(Parent,
                                            command = partial(self.ResetBoundariesFunction,0),
                                            text = 'Reset'),
                                2 * Target.ParameterNumber + 2,
                                4,
                                1,1]
                                    
        ################################################
        ################################################
        #run the final placement method

        for List in [BoundariesLabels,
                     BoundariesEntries,
                     BoundariesCheck,
                     BoundariesButton]:
                     
            for Element in List:
                
                Element[0].grid(row         = Element[1],
                                column      = Element[2],
                                rowspan     = Element[3],
                                columnspan  = Element[4],
                                sticky      = tk.E + tk.W)


        ################################################
        ################################################
        #Save this information into the appropriate class
        
        Target.BoundariesLabels     = BoundariesLabels
        Target.BoundariesEntries    = BoundariesEntries
        Target.BoundariesCheck      = BoundariesCheck
        Target.BoundariesButton     = BoundariesButton
        


    def ResetBoundariesGeneral(self):
        '''
        ####################################################################################
        This routine will reset theboundaries of the general fiting parameters
        ####################################################################################
        '''
        print 'Reseting the general boundary parameters'
    
        ##################################################
        #delete the values into the netry fields.
        self.BoundariesGeneralEntries[0][0].delete(0,tk.END)
        self.BoundariesGeneralEntries[1][0].delete(0,tk.END)
        self.BoundariesGeneralEntries[2][0].delete(0,tk.END)
        self.BoundariesGeneralEntries[3][0].delete(0,tk.END)
    
        ##################################################
        #insert the values into the netry fields.
        self.BoundariesGeneralEntries[0][0].insert(0, '5')
        
        #initialise
        string = '0'
        
        #generate the order list:
        for i in range(1,len(self.DataClass.RamFit.Function_Info_Pointers)):
            
            #add the next index
            string  += ','+str(i)
        
        self.BoundariesGeneralEntries[1][0].insert(0, string)
        self.BoundariesGeneralEntries[2][0].insert(0, '0')
        self.BoundariesGeneralEntries[3][0].insert(0, '10000')
    
        ##################################################
        #Set the boolean variables ...
        self.IgnoreFirstMin.set(0)
        self.CopyVal.set(0)
        self.CopyFix.set(0)
        self.Stability.set(0)
    
    
    def ResetBoundariesFunction(self, idx):
        '''
        ####################################################################################
        This will reset the boundaries of the lorrentz fitting parameters
        ####################################################################################
        '''
        
        #grab the target
        Target = self.DataClass.RamFit.Function_Info_Pointers[idx]
        
        #append the processing informations
        Default = [Target.ParameterProcessing[0], # <- Number of iteration
                   Target.ParameterProcessing[1], # <- Order of Processing
                   ]
            
        #append the boundaries
        for i in range(2*Target.ParameterNumber):
            
            Default.append(Target.ParameterBoundaries[i][0])
            Default.append(Target.ParameterBoundaries[i][1])
        
        ##################################################
        #delete the values into the netry fields.
        
        for i in range(0, len(Target.BoundariesEntries)):
        
            Target.BoundariesEntries[i][0].delete(0,tk.END)
    
        ##################################################
        #insert the values into the netry fields.
        
        for i in range(0, len(Target.BoundariesEntries)):
        
            Target.BoundariesEntries[i][0].insert(0,Default[i])
    
        ##################################################
        #Set the boolean variables ...
        for i in range(Target.ParameterNumber):
            
            Target.BoundariesVar[2 * i].set(0)
            Target.BoundariesVar[2 * i + 1].set(1)
    

    
    def GrabContainers(self):
        '''
        ####################################################################################
        This function provides the containers to the fiting functions. It return the 
        Container array and the order for the general fitting.
        ####################################################################################
        '''
        ##########################
        #initialise container
        Container = [self.GrabGeneralContainer()]
        
        ##########################
        #Fetch indivifual containers
        for i in range(len(self.DataClass.RamFit.Function_Info_Pointers)):
            
            Container.append(self.GrabFunctionContainer(i))
    
        #senf it out
        return Container
    
    def GrabGeneralContainer(self):
        '''
        ####################################################################################
        This grabs the general container:
        variables are 
        [number of iterations,
        Order]
        ####################################################################################
        '''
        
        #initialise container
        Container = [None]*3
    
        #grab the formated value:
        Container[0] = int(self.BoundariesGeneralEntries[0][0].get())
        Container[1] = [int(self.BoundariesGeneralEntries[1][0].get().split(',')[i]) for i in range(0, len(self.BoundariesGeneralEntries[1][0].get().split(',')))]
        Container[2] = int(self.BoundariesGeneralEntries[3][0].get())
    
        #senf it out
        return Container
                        
                        
    def GrabFunctionContainer(self,idx):
        '''
        ####################################################################################
        This grabs the general container:
        variables are 
        number of iterations,
        Order
        ####################################################################################
        '''
        ############################
        #set the target
        Target = self.DataClass.RamFit.Function_Info_Pointers[idx]
        
        ############################
        #initialise container
        Container = [None]*6
    
        #grab the two first values:
        Values = Target.BoundariesEntries[1][0].get().split(',')
        
        Container[0] = int(Target.BoundariesEntries[0][0].get())
        Container[1] = [int(Values[i]) for i in range(0, len(Values))]
        Container[2] = [int(Values[i]) for i in range(0, len(Values))]
        
        ############################
        #continue onto boundaries:
        Array = []
        Index = 2
                      
        #go through all lines
        for i in range(0,Target.ParameterNumber * 2):
                        
            TempArray = []
            
            #go through the line
            for j in range(0,3):
                       
                ###############
                #check button
                if j == 0:
                       
                    #logical check
                    if Target.BoundariesVar[i].get() == 1:
                    
                        TempArray.append(True)
                        
                    else:
                        
                        TempArray.append(False)
                        
                        
                else:
                    
                    #are we positive infinite
                    if Target.BoundariesEntries[Index][0].get() == 'Inf' or Target.BoundariesEntries[Index][0].get() == 'inf':
                        
                        TempArray.append(numpy.inf)
                        
                    
                    #are we negative infinite
                    elif Target.BoundariesEntries[Index][0].get() == '-Inf' or Target.BoundariesEntries[Index][0].get() == '-inf':
                        
                        TempArray.append(-numpy.inf)
                    
                    elif Target.BoundariesEntries[Index][0].get() == 'xmin':
                        
                        if self.DataClass.Type == 'Single':
                        
                            TempArray.append(numpy.min(self.DataClass.X.X[0]))
                        
                        else:
                            
                            TempArray.append(numpy.min(self.DataClass.Contour.Projection[0]))
                    
                    elif Target.BoundariesEntries[Index][0].get() == 'xmax':
                        
                        if self.DataClass.Type == 'Single':
                        
                            TempArray.append(numpy.min(self.DataClass.X.X[-1]))
                        
                        else:
                            
                            TempArray.append(numpy.max(self.DataClass.Contour.Projection[0]))
                        
                    #else put the value
                    else:
                        
                        TempArray.append(float(Target.BoundariesEntries[Index][0].get()))
                        
                    Index += 1
                        
                
            Array.append(TempArray)
                        
        #package it
        Container[4] = Array
                        
        ############################
        #multi element depreciated
        Container[5] = False
        
        ############################
        #send it out
        Target.Container = Container

        return Container

    def GrabInfo(self):
        
        '''
        ####################################################################################
        This function will grab the current coordiantes and display them in the visual Frame
        ####################################################################################
        '''
        
        #######################################
        #######################################
        #Create the lists
        FirstList = [Element.Name
                     for Element in self.DataClass.RamFit.Function_Info_Pointers]
                 
        # find and set second list
        for idx,Element in enumerate(FirstList):
            
            if self.VisStringVars[0].get() == Element:
    
                SecondList = self.DataClass.RamFit.Function_Info_Pointers[idx].ParameterNames
        
                Target = self.DataClass.RamFit.Function_Pointers[idx]
    
                # find and set second list
                for idx,Element in enumerate(SecondList):
    
                    if self.VisStringVars[1].get() == Element:
    
                        Idx = idx

        #st third list
        ThirdList = [str(idx) + ': ' + Element.Name for idx,Element in enumerate(Target[0])]
            
        # find and set second list
        for idx,Element in enumerate(ThirdList):

            if self.VisStringVars[2].get() == Element:

                Which = idx

        return Target, Idx, Which
                
    def SetVis(self, event = None):
        '''
        ####################################################################################
        This function will grab the current coordiantes and display them in the visual Frame
        ####################################################################################
        '''
        #######################################
        #######################################
        #grab info
        Target, Idx, Which = self.GrabInfo()

        #######################################
        #######################################
        #Extract the array
        ModificationList = self.ax.Modifier.Log

        for i in range(0, len(ModificationList)):

            Target[ModificationList[i][1]][Which].Parameters[Idx+1]     = ModificationList[i][4][1]
            Target[ModificationList[i][1]][Which].ParametersIni[Idx+1]  = ModificationList[i][4][1]
            
            if self.MakeFixed.get() == 1:

                Target[ModificationList[i][1]][Which].ParametersFix[Idx+1] = 1

        #######################################
        #######################################
        #Refresh it
        self.Parent.ChangeCurrent(0)
        
        #reset the modifier log
        self.ax.Modifier.Log = []


    def LoadVis(self, event = None):
        '''
        ####################################################################################
        This function will grab the current coordiantes and display them in the visual Frame
        ####################################################################################
        '''
        #######################################
        #######################################
        #grab info
        Target, Idx, Which = self.GrabInfo()
        
        #######################################
        #######################################
        #reset graph
        self.ax.Reset()
        
        #######################################
        #######################################
        #Prepare data
        
        #define XArray
        XArray = self.DataClass.RamFit.XArray
        
        #Set Buffer
        Buffer = []
            
        #go thourgh
        for i in range(0,len(Target)):
            
            #set it
            Buffer.append(Target[i][Which].Parameters[Idx+1])
    

        #set the color
        Color = Target[0][Which].Color
        
        #draw lineplot
        self.ax.AddiPlot(XArray,
                         Buffer,
                         color = Color,
                         Thickness = int(2.5),
                         style = ['o',4,4])


        #######################################
        #######################################
        #display
        self.ax.Zoom()

    def ResetVisSelector(self, event = None):
        '''
        ####################################################################################
        This function will create the Frame linking all the boundaries to the fitter. 
        The boundaries can then be Fetched to build the containers in Ramfit.
        Please note that each conatainer can be tunred off or on to laod the default
        parameters.
        ####################################################################################
        '''
        #######################################
        #######################################
        #grab defaults
        Default_1  = str(self.VisStringVars[0].get())
        Default_2  = str(self.VisStringVars[1].get())
        Default_3  = str(self.VisStringVars[2].get())
        
        #in case no selection is made
        Target = self.DataClass.RamFit.Function_Pointers[0]
        
        FirstList   = ['None']
        SecondList  = ['None']
        ThirdList   = ['None']
        
        #######################################
        #######################################
        #Create the lists
        FirstList = [Element.Name
                     for Element in self.DataClass.RamFit.Function_Info_Pointers]
                 
        # find and set second list
        for idx,Element in enumerate(FirstList):
            
            if self.VisStringVars[0].get() == Element:
    
                SecondList = self.DataClass.RamFit.Function_Info_Pointers[idx].ParameterNames
        
                Target = self.DataClass.RamFit.Function_Pointers[idx]
    
    
        #set the third list
        if len(Target) == 0:
        
            ThirdList = ['None']
        
        else:
        
            ThirdList = [str(idx) + ': ' + Element.Name for idx,Element in enumerate(Target[0])]
        
        #clean up before rebuilding
        try:
            
            for Element in self.VisSelectors:
        
                Element[0].destroy()

        except:
            pass

        self.VisSelectors = []

        #######################################
        #######################################
        #Create the elements
        
        self.VisSelectors.append([ttk.OptionMenu(self.TopVisFrame,
                                                 self.VisStringVars[0],
                                                 Default_1,
                                                 *FirstList,
                                                 command = self.ResetVisSelector),
                                  0,
                                  1,
                                  1,
                                  1,
                                  tk.E + tk.W])
                           
        
        self.VisSelectors.append([ttk.OptionMenu(self.TopVisFrame,
                                                 self.VisStringVars[1],
                                                 Default_2,
                                                 *SecondList,
                                                 command = self.ResetVisSelector),
                                  0,
                                  3,
                                  1,
                                  1,
                                  tk.E + tk.W])
                                

        self.VisSelectors.append([ttk.OptionMenu(self.TopVisFrame,
                                                 self.VisStringVars[2],
                                                 Default_3,
                                                 *ThirdList,
                                                 command = self.ResetVisSelector),
                                  0,
                                  5,
                                  1,
                                  1,
                                  tk.E + tk.W])
    
        #######################################
        #######################################
        #Place it all here
        
        for Element in self.VisSelectors:
        
            Element[0].grid(row         = Element[1],
                            column      = Element[2],
                            rowspan     = Element[3],
                            columnspan  = Element[4],
                            sticky      = Element[5])
    
        

    
    def Populate_Log(self, Location = 0):
        '''
        ####################################################################################
        To allow for a more coherent interface the log will b displayed in here rather than
        a termainal Window. This will allow for better app implementation...
        ####################################################################################
        '''
        
        #Define the Frame:
        self.LogFrame = ttk.Frame(self.NoteBook, padding= self.padding)
        
        #insert the textfield
        self.LogField = ScrolledText.ScrolledText(master = self.LogFrame, wrap=tk.WORD)
    
    
        #grid it
        self.LogField.grid(row = 0, column = 0, sticky= tk.E+tk.W+tk.N+tk.S)
        
        self.LogFrame.grid_columnconfigure(0, weight = 1)
        self.LogFrame.grid_rowconfigure(0, weight = 1)
        
        return self.LogFrame

    '''
    ##################################################
    FUNCTION: FrameWidth
    
    DESCRIPTION:
    
    This function and the following were introduced 
    to ensure a resizing of the canvas concerning the 
    entries. It was decided in 0.1.02 to move these 
    elements to allow for biger rnages
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - event: configure associated
    
    ##################################################
    '''
    
    def FrameWidth(self, Event):
        
        #fetch width
        canvas_width = Event.width
        
        #do something
        self.EntryCanvas.itemconfig(self.EntryCanvas,
                                    width = canvas_width)

    '''
    ##################################################
    FUNCTION: OnFrameConfigure
    
    DESCRIPTION:
    
    This function and the following were introduced 
    to ensure a resizing of the canvas concerning the 
    entries. It was decided in 0.1.02 to move these 
    elements to allow for biger rnages
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - event: configure associated
    
    ##################################################
    '''
    def OnFrameConfigure(self, Event):
        
        self.EntryCanvas.configure(scrollregion = self.EntryCanvas.bbox("all"))
    
    
    '''
    ##################################################
    FUNCTION: FrameWidth_2
    
    DESCRIPTION:
    
    This function and the following were introduced 
    to ensure a resizing of the canvas concerning the 
    entries. It was decided in 0.1.02 to move these 
    elements to allow for biger rnages
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - event: configure associated
    
    ##################################################
    '''
    def FrameWidth_2(self, Event):
        
        #fetch width
        canvas_width = Event.width
        
        #do something
        self.BoundaryCanvas.itemconfig(self.BoundaryCanvas,
                                       width = canvas_width)

        '''
    ##################################################
    FUNCTION: OnFrameConfigure
    
    DESCRIPTION:
    
    This function and the following were introduced 
    to ensure a resizing of the canvas concerning the 
    entries. It was decided in 0.1.02 to move these 
    elements to allow for biger rnages
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - event: configure associated
    
    ##################################################
    '''
    def OnFrameConfigure_2(self, Event):
        
        self.BoundaryCanvas.configure(scrollregion = self.BoundaryCanvas.bbox("all"))

    '''
    ##################################################
    FUNCTION: OnFrameConfigure
    
    DESCRIPTION:
    
    This method is introduced in version 0.1.02 to 
    accomodate for the change in lorr number count.
    This means that we need to be able to hotswap the 
    values. Please remember that the fixes are 
    managed in the parent and need to be reset.
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - event: configure associated
    
    ##################################################
    '''
    def Reset_Entry_Frame(self, Fixes = [True,True,True,True]):
        
        ########################################
        #Try to forget a notebook page
        try:
            
            self.NoteBook.forget(0)
            self.NoteBookPage[0] = [None]
            self.TempFrame.destroy()
        
        except:
            
            print 'Coudld not destroy an dobject that should be present in the first place...'
        
        ########################################
        #Catch the info from the entry field
        self.NoteBookPage[0] = self.Populate_Entries(self.HowMany,self.NoteBook, Fixes = Fixes)

        #reinsert the missing page
        self.NoteBook.insert(0,self.NoteBookPage[0],text = self.NoteBookTitle[0])

        #jump to the first page
        self.NoteBook.select(0)
            
        #finally correct
        self.Parent.Change(0)

    '''
    ##################################################
    FUNCTION: Populate_Entries
    
    DESCRIPTION:
    
    This method is introduced in version 0.1.02 to 
    accomodate for the change in lorr number count.
    This means that we need to be able to hotswap the 
    values. Please remember that the fixes are 
    managed in the parent and need to be reset.
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - event: configure associated
    
    ##################################################
    '''
    def Populate_Entries(self,Location = 1, Parent = None, Fixes = [True,True,True,True,True,True,True,True,True,True]):
        '''
        ####################################################################################
        In this instance we will generate the window layout to manage the fiting variables
        it was taken from version 2 and transposed into a separate window to allow for a 
        more clear grid and window management. It will also allow for more dynamic 
        Lorrentzian creation...
        
        The save option in version 3 should also finnally include the baseline modifications
        as well as a general info file to allow for more precise loggin for the future
        ####################################################################################
        '''
        #create the Frame which will sit in the scroll canvas
        self.TempFrame = ttk.Frame(self.Frame)
        self.TempFrame.grid_columnconfigure(0, weight = 1)
        self.TempFrame.grid_rowconfigure(0, weight = 1)
        
        #create the canvas that will handle the scrolling
        self.vscroll = tk.Scrollbar(self.TempFrame)
                                    
        #we need to grab the system abckground for the canvas
        self.EntryCanvas = tk.Canvas(self.TempFrame,
                                     bd=0,
                                     highlightthickness=0,
                                     background = '#EDEFF0',
                                     yscrollcommand = self.vscroll.set)
        
        self.EntryCanvas.grid(row=0,column=0, sticky='news')
        self.vscroll.grid(row = 0, column=1, sticky='ns')
        
        self.vscroll.configure(command = self.EntryCanvas.yview)
        
        #create the Frame which will sit in the scroll canvas
        self.EntryFrame = ttk.Frame(self.EntryCanvas)
        
        #configure actions
        self.EntryCanvas.bind('<Configure>', self.OnFrameConfigure)
        self.EntryFrame.bind('<Configure>', self.FrameWidth)
        
        #set the system default
        if os.name == 'nt':
        
            self.SysEntryWidth = 12
            self.SysLabelWidth = 8
            self.SysButtonWidth = 5
        
        else:
        
            self.SysEntryWidth = 9
            self.SysLabelWidth = 6
            self.SysButtonWidth = 3
        
        ####################################
        ####################################
        #create entry
        self.B          = []
        self.Fix        = [None]*len(self.DataClass.RamFit.Function_Pointers)
        self.Trace      = [None]*len(self.DataClass.RamFit.Function_Pointers)
        self.Offset     = 0
        
        #Populate the lorrentzians
        for idx,Pointer in enumerate(self.DataClass.RamFit.Function_Pointers):
        
            if self.HowMany[idx] > 0:
            
                self.GeneralPopulator(idx,Fixes = Fixes[idx])

        ####################################
        ####################################
        #run the final drid method
        for Row in self.B:
        
            for Element in Row:
                
                try:
                    
                    Element[0].grid(row     = Element[1],
                                    column  = Element[2],
                                    rowspan     = Element[3],
                                    columnspan  = Element[4],
                                    sticky = tk.E + tk.W)
        
                except:
            
                    pass
            
        ####################################
        ####################################
        #Set Frame weight
        self.EntryFrame.grid_columnconfigure(2, weight = 1)
        self.EntryFrame.grid_columnconfigure(4, weight = 1)
        self.EntryFrame.grid_columnconfigure(6, weight = 1)
        self.EntryFrame.grid_columnconfigure(8, weight = 1)
        
        self.EntryCanvas.create_window(0,
                                       0,
                                       window = self.EntryFrame)

        #Place it
        if Parent == None and not Location == -1:
            
            self.TempFrame.grid(row = Location, sticky= tk.E+tk.W)
        
        else:
            
            return self.TempFrame


    def GeneralPopulator(self,idx, Fixes = True):
    
        '''
        ######################################################################
        In version O.1.02 this was separated from the main window builder to 
        allow processing in the Framework of the dynamic lorrentzian
        management.
        
        Since version 0.1.03 we have local definitions of the fixed things
        ######################################################################
        '''
        
        ####################################
        ####################################
        #Take care of the fixes
        if Fixes == True:
            
            
            #set the trace variales
            self.Trace[idx] = [tk.IntVar() for l in range(0,len(self.DataClass.RamFit.Function_Pointers[idx][self.DataClass.RamFit.Current]))]
    
            #introduce tracing the varible
            for j in range(0,len(self.DataClass.RamFit.Function_Pointers[idx][self.DataClass.RamFit.Current])):
                    
                self.Trace[idx][j].set(1)


            #initialise fiting
            self.Fix[idx] = []
            
            for j in range(0,len(self.DataClass.RamFit.Function_Pointers[idx][self.DataClass.RamFit.Current])):
                
                #add fixed radion button logical variable
                self.Fix[idx].append([tk.IntVar() for l in range(0,self.DataClass.RamFit.Function_Info_Pointers[idx].ParameterNumber)])
    
    

        elif Fixes == False:
        
            #add fixed radion button logical variable
            self.Fix[idx].append([tk.IntVar() for l in range(0,self.DataClass.RamFit.Function_Info_Pointers[idx].ParameterNumber)])
            self.Trace[idx].append(tk.IntVar())
            self.Trace[idx][-1].set(1)
        
        #Placement variables
        LorrOffest  = 1
        BaseOffset  = 5
        InputOffset = 2
        RowOffset   = 9
        RowLabels   = 2 + self.Offset
        RowEntry    = 3 + self.Offset
        
        ####################################
        ####################################
        #Determine how much Cs we need
        #depends on the parameter length
        LengthList = []

        for ll in range(len(self.DataClass.RamFit.Function_Info_Pointers)):

            if len(self.DataClass.RamFit.Function_Pointers[ll][0]) > 0:
            
                LengthList.append(self.DataClass.RamFit.Function_Info_Pointers[ll].ParameterNumber)

            else:
                
                LengthList.append(0)
                    
        MaxLength = 2 * numpy.max(LengthList)
        
        ####################################
        ####################################
        #Create Labels
        A = []


        for i in range(self.DataClass.RamFit.Function_Info_Pointers[idx].ParameterNumber):

            A.append([ttk.Label(self.EntryFrame,
                                text = self.DataClass.RamFit.Function_Info_Pointers[idx].ParameterNames[i]  ,
                                width = self.SysLabelWidth,
                                justify = tk.CENTER),
                      RowLabels,
                      (i+1)*2,
                      1,1])
                  

        #----------------------------------------#
        #add the set button for a single row
        A.append([ttk.Button(self.EntryFrame,
                             text    = 'Set',
                             width   = self.SysButtonWidth,
                             command = self.SubmitAll),
                  RowLabels,
                  MaxLength + 1,
                  1,1])
        
        A.append([ttk.Label(self.EntryFrame,
                             text    = 'Trace'   ,
                             width   = self.SysLabelWidth,
                             justify  = tk.CENTER),
                  RowLabels,
                  MaxLength + 2,
                  1,1])
                  
        A.append([ttk.Label(self.EntryFrame,
                             text    = 'Color'   ,
                             width   = self.SysLabelWidth,
                             justify  = tk.CENTER),
                  RowLabels,
                  MaxLength + 3,
                  1,1])
                  
        A.append([ttk.Label(self.EntryFrame,
                             text    = 'Group'   ,
                             width   = self.SysLabelWidth,
                             justify  = tk.CENTER),
                  RowLabels,
                  MaxLength + 4,
                  1,1])
                  
        #append to the main arrays
        self.B.append(A)
        

        
        
        ####################################
        ####################################
        #Loop over the fields
        self.DataClass.RamFit.Function_Info_Pointers[idx].Fields = []
        j = 0
        
        #llop over the elements
        for j in range(0,len(self.DataClass.RamFit.Function_Pointers[idx][self.DataClass.RamFit.Current])):
            
            
            #we ar ein a single entry row create A
            C = [None]*MaxLength
            
            #loop over position HWHM, factor and min
            PutEntry = False
            l = 0
            k = 1
            
            for i in range(0,2*self.DataClass.RamFit.Function_Info_Pointers[idx].ParameterNumber):
                
                    
                #Logic
                if PutEntry:
                    
                    #Add an entry field
                    C[i] = [ttk.Entry(self.EntryFrame,
                                      width = self.SysEntryWidth,
                                      justify = tk.RIGHT),
                            RowEntry+j,
                            k,
                            1,1]
                    
                    #set the value

                    C[i][0].insert(0,str(round(self.DataClass.RamFit.Function_Pointers[idx][self.DataClass.RamFit.Current][j].ParametersIni[l],4)))
                    
                    #move index
                    k += 1
                    
                    #logic
                    PutEntry = False
        
                else:
                    
                    #Add an entry field
                    C[i] = [ttk.Checkbutton(self.EntryFrame,
                                            variable = self.Fix[idx][j][l]),
                            RowEntry+j,
                            k,
                            1,1]
                    
                    #configure
                    if self.DataClass.RamFit.Function_Pointers[idx][self.DataClass.RamFit.Current][j].ParametersFix[l] == 1:
                        
                        C[i][0].state(['selected'])
                    
                    else:
                        
                        C[i][0].state(['!selected'])
                    
                    
                    #bind it for multi purpose access
                    C[i][0].bind(File.RightClickStr(),
                                 lambda event, arg = [j,l], Pointer = self.DataClass.RamFit.Function_Pointers[idx]:  self.rClickerCheckButton(event, arg, Pointer))
                    
                    #move on
                    l += 1
                    k += 1
        
                    #logic
                    PutEntry = True
            
        
            ####################################
            ####################################
            #add the set button for a single row
            C.append([ttk.Button(self.EntryFrame,
                                 text       = 'Opt.',
                                 width      = self.SysButtonWidth,
                                 command    = partial(self.Remove, j)),
                      RowEntry+j,
                      MaxLength + 1,
                      1,1])

            #add the set button for a single row
            C.append([ttk.Checkbutton(self.EntryFrame,
                                      variable = self.Trace[idx][j]),
                      RowEntry+j,
                      MaxLength + 2,
                      1,1])
                      
            #add the set button for a single row
            C.append([SimplePlot.ColorCanvas(self.EntryFrame,
                                  color = self.DataClass.RamFit.Function_Pointers[idx][self.DataClass.RamFit.Current][j].Color),
                      RowEntry+j,
                      MaxLength + 3,
                      1,1])
                      
            #add the set button for a single row
            C.append([ttk.Entry(self.EntryFrame,
                                 width      = self.SysEntryWidth),
                      RowEntry+j,
                      MaxLength + 4,
                      1,1])

            C[-1][0].insert(0, str(self.DataClass.RamFit.Function_Pointers[idx][self.DataClass.RamFit.Current][j].Group))
                      
            #add the set button for a single row
            C.append([ttk.Entry(self.EntryFrame,
                                width =  self.SysEntryWidth),
                      RowEntry+j,
                      0,
                      1,1])

            C[-1][0].insert(0, str(self.DataClass.RamFit.Function_Pointers[idx][self.DataClass.RamFit.Current][j].Name))

            #add it to the main array
            self.DataClass.RamFit.Function_Info_Pointers[idx].Fields.append(C)
    
        for Element in self.DataClass.RamFit.Function_Info_Pointers[idx].Fields:
            
            self.B.append(Element)
        
        ####################################
        ####################################
        #set the addition button
        D = [[ttk.Button(self.EntryFrame,
                        text    = '+',
                        width   = self.SysButtonWidth,
                        command = self.AddLorrentz),
                  RowEntry+j+1,
                  0,
                  1,1]]
    
        self.B.append(D)

        ####################################
        ####################################
        #set an offset for later
        self.Offset = RowEntry+j+2
        
            
    def Populate_Navigator(self,Location = 0):
        '''
        ####################################################################################
        This function will call to Populate the navigator and will place it on the parent
        Frame if necessary...
        
        
        if not nothing will be drawn and the Frame discareded
        ####################################################################################
        '''

        #introduce the navigator if needed
        if not self.DataClass.Type == 'Single':
            
            #Apparently we recquire a navigator... link it to main Frame
            self.NavFrame     = ttk.Frame(self.Frame, padding= self.padding)
            
            #construct the visuals
            self.Next01Button = ttk.Button(self.NavFrame, text = '>' ,command = partial(self.Parent.ChangeUpdate,1))
            self.Prev01Button = ttk.Button(self.NavFrame, text = '<' ,command = partial(self.Parent.ChangeUpdate,-1))
            self.Next10Button = ttk.Button(self.NavFrame, text = '>>',command = partial(self.Parent.ChangeUpdate,10))
            self.Prev10Button = ttk.Button(self.NavFrame, text = '<<',command = partial(self.Parent.ChangeUpdate,-10))
            
            if os.name == 'nt':
                self.NavLabel     = ttk.Label(self.NavFrame,  text = str(int(self.DataClass.RamFit.Current)),width = 10, font=("Helvetica",13),anchor = tk.CENTER )
            else:
                
                self.NavLabel     = ttk.Label(self.NavFrame,  text = str(int(self.DataClass.RamFit.Current)),width = 10, font=("Helvetica",16),anchor = tk.CENTER )
            
            #grid the elements onto the fram
            #self.NavLabelTitle.grid(row = 0, column = 0, sticky= tk.E+tk.W)
            self.Prev10Button.grid( row = 0, column = 0, sticky= tk.E+tk.W)
            self.Prev01Button.grid( row = 0, column = 1, sticky= tk.E+tk.W)
            self.NavLabel.grid(     row = 0, column = 2, sticky= tk.E+tk.W)
            self.Next01Button.grid( row = 0, column = 3, sticky= tk.E+tk.W)
            self.Next10Button.grid( row = 0, column = 4, sticky= tk.E+tk.W)
            
            #configure weights:
            self.NavFrame.grid_columnconfigure(0, weight = 1)
            self.NavFrame.grid_columnconfigure(1, weight = 1)
            self.NavFrame.grid_columnconfigure(2, weight = 1)
            self.NavFrame.grid_columnconfigure(3, weight = 1)
            self.NavFrame.grid_columnconfigure(4, weight = 1)
            
            #Finnally grid the nav Frame
            self.NavFrame.grid(row = Location, column = 0, sticky= tk.E+tk.W)

    def Populate_Fitter(self,Location = 2):
        '''
        ####################################################################################
        This function will call to Populate the navigator and will place it on the parent
        Frame if necessary...
        
        
        if not nothing will be drawn and the Frame discareded
        ####################################################################################
        '''
        
        #In any case we will need a fitter class
        self.FitFrame = ttk.Frame(self.Frame, padding= self.padding)
        
        #Fetching instance
        self.cNext01Button = ttk.Button(self.FitFrame, text = '> Copy >',  command = partial(self.Parent.Copy,1))
        self.cPrev01Button = ttk.Button(self.FitFrame, text = '< Copy <',  command = partial(self.Parent.Copy,-1))
        
        #Fetching instance
        self.fNext01Button = ttk.Button(self.FitFrame, text = '> Fit >',  command = partial(self.Parent.Recalculate,1))
        self.fPrev01Button = ttk.Button(self.FitFrame, text = '< Fit <',  command = partial(self.Parent.Recalculate,-1))
        self.fThis00Button = ttk.Button(self.FitFrame, text = 'Fit',      command = partial(self.Parent.Recalculate,0))
        
        if os.name == 'nt':
            
            self.CalcPercLabel = ttk.Label(self.FitFrame, text = '00.00%',anchor = tk.CENTER, font=("Helvetica",13),width = 10 )
        
        else:
            
            self.CalcPercLabel = ttk.Label(self.FitFrame, text = '00.00%',anchor = tk.CENTER, font=("Helvetica",16),width = 10 )

        #Create the load label to be passed into the calc routines
        

        #introduce the navigator if needed
        if not self.DataClass.Type == 'Single':
        
            #pack copying buttons
            self.cPrev01Button.grid( row = 0, column = 0, sticky= tk.E+tk.W)
            self.cNext01Button.grid( row = 0, column = 4, sticky= tk.E+tk.W)
            
            #pack fit buttons
            self.fPrev01Button.grid( row = 0, column = 1, sticky= tk.E+tk.W)
            self.fThis00Button.grid( row = 0, column = 2, sticky= tk.E+tk.W)
            self.fNext01Button.grid( row = 0, column = 3, sticky= tk.E+tk.W)
        
            #distibute weight
            self.FitFrame.grid_columnconfigure(0, weight = 1)
            self.FitFrame.grid_columnconfigure(1, weight = 1)
            self.FitFrame.grid_columnconfigure(3, weight = 1)
            self.FitFrame.grid_columnconfigure(4, weight = 1)
        
            
            #Create the three boxes
            self.FitCheck01 = ttk.Checkbutton(self.FitFrame, variable = self.IgnoreFirstMin, text = 'Skip First')
            self.FitCheck02 = ttk.Checkbutton(self.FitFrame, variable = self.CopyVal,        text = 'Copy Value')
            self.FitCheck03 = ttk.Checkbutton(self.FitFrame, variable = self.CopyFix,        text = 'Copy Fixes')
            self.FitCheck04 = ttk.Checkbutton(self.FitFrame, variable = self.Stability,      text = 'Check Stab')
        
            #Places the three boxes
            self.FitCheck01.grid(row = 1, column = 0)
            self.FitCheck02.grid(row = 1, column = 1)
            self.FitCheck03.grid(row = 1, column = 3)
            self.FitCheck04.grid(row = 1, column = 4)
        
            #Create the jelper menues...
            ToolTip(self.FitCheck01, follow_mouse = 1, text = 'This Will allow to skip the first value of the minima to allow more stability')
            ToolTip(self.FitCheck02, follow_mouse = 1, text = 'This will copy the values onto the next fit try for more variation stability')
            ToolTip(self.FitCheck03, follow_mouse = 1, text = 'This will copy the fixed values on the fit for more variation stabilty')
            ToolTip(self.FitCheck04, follow_mouse = 1, text = 'This will stabilise the minimum over iterative fitting trials')
        
            #Create input field
            
            #place the input field
        
        else:
            
            #just put the fit button
            self.fThis00Button.grid( row = 0, column = 2, sticky= tk.E+tk.W)
        
            #give the weight
            self.FitFrame.grid_columnconfigure(2, weight = 1)
    
        #put the label
        self.CalcPercLabel.grid( row = 1, column = 2)
        
        
        #We want a progressbar:
        self.pb = ttk.Progressbar(self.FitFrame, orient="horizontal",length=600, mode="determinate")
        self.pb.grid(row = 2, column = 0,columnspan = 5)
        self.pb["value"] = 0
        self.pb["maximum"] = 100
        
        #Call eventual binding methods...

        #fit binding
        self.fThis00Button.bind(File.RightClickStr(),self.rClickerFit)
            
        #Bind the methonds on directional fits....
        self.fPrev01Button.bind(File.RightClickStr(),self.lClickerFitRight)
        self.fNext01Button.bind(File.RightClickStr(),self.lClickerFitLeft)
        
        #Bind the methonds on directional fits....
        self.cPrev01Button.bind(File.RightClickStr(),self.lClickerCopyRight)
        self.cNext01Button.bind(File.RightClickStr(),self.lClickerCopyLeft)
        
        #Finnally grid the nav Frame
        self.FitFrame.grid(row = Location, column = 0, sticky= tk.E+tk.W)
    

    def HideEntryGrid(self,event):
        ''' 
        ####################################################################################
        Minimise the entire window to a more reasonable size
        ####################################################################################
        '''
    
        if self.EntryFrameVisible:
            
            self.NoteBookFrame.grid_remove()
            self.EntryFrameVisible = False

        else:
            
            self.NoteBookFrame.grid()
            self.EntryFrameVisible = True
    
    def DoNothing(self):
        pass
    
    def ManageFix(self,Array,Type, Pointer):
        
        ''' 
        ####################################################################################
        This allows for transfering the valueof the fix
        On right click of a fix the options are displayed allowing the user to transfer the
        current fix value accross multiple instances...
        ####################################################################################
        '''
        
        #Do we do all ?
        if Type == 'oo':
            
            #SetParameters
            START = 0
            END   = len(Pointer)
        
        elif Type == '--':
        
            #SetParameters
            START = self.DataClass.RamFit.Current
            END   = 0
        
        elif Type == '++':
        
            #SetParameters
            START = self.DataClass.RamFit.Current
            END   = len(Pointer)
        
        elif Type < 0:
            
            #SetParameters
            START = self.DataClass.RamFit.Current
            END   = self.DataClass.RamFit.Current + Type
        
        elif Type > 0:
        
            #SetParameters
            START = self.DataClass.RamFit.Current
            END   = self.DataClass.RamFit.Current + Type
        
        else:
            
            return
        
        #FInally check the value to put...
        ValuetoPut = Pointer[self.DataClass.RamFit.Current][Array[0]].ParametersFix[Array[1]+1]

        #Summon the beast onto the selected nums
        for j in Utility.Range(START,END):
            
            #Put it
            Pointer[j][Array[0]].ParametersFix[Array[1]+1] = ValuetoPut
    
    def rClickerCheckButton(self,e, Link, Pointer):
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
        e.widget.focus()

        #Create main menue
        MainMenue = tk.Menu(None, tearoff=0, takefocus=0)
        
        #Create small menues
        SmallMenue1 = tk.Menu(None, tearoff=0, takefocus=0)
        SmallMenue2 = tk.Menu(None, tearoff=0, takefocus=0)
        SmallMenue3 = tk.Menu(None, tearoff=0, takefocus=0)
        SmallMenue4 = tk.Menu(None, tearoff=0, takefocus=0)
        SmallMenue5 = tk.Menu(None, tearoff=0, takefocus=0)
        
        #now fill small menues
        SmallMenue1.add_command(label = 'Previous 5', command = partial(self.ManageFix,Link,-5, Pointer))
        SmallMenue1.add_command(label = 'Next 5', command = partial(self.ManageFix,Link,5, Pointer))
        
        SmallMenue2.add_command(label = 'Previous 10', command = partial(self.ManageFix,Link,-10, Pointer))
        SmallMenue2.add_command(label = 'Next 10', command = partial(self.ManageFix,Link,10, Pointer))
        
        SmallMenue3.add_command(label = 'Previous 20', command = partial(self.ManageFix,Link,-20, Pointer))
        SmallMenue3.add_command(label = 'Next 20', command = partial(self.ManageFix,Link,20, Pointer))
        
        SmallMenue4.add_command(label = 'Previous 30', command = partial(self.ManageFix,Link,-30, Pointer))
        SmallMenue4.add_command(label = 'Next 30', command = partial(self.ManageFix,Link,30, Pointer))
        
        SmallMenue5.add_command(label = 'All Previous', command = partial(self.ManageFix,Link,'--', Pointer))
        SmallMenue5.add_command(label = 'All Next', command = partial(self.ManageFix,Link,'++', Pointer))
        SmallMenue5.add_command(label = 'All', command = partial(self.ManageFix,Link,'oo', Pointer))

        #Buid the cascade
        MainMenue.add_cascade(label = '5   Steps Fix', menu =  SmallMenue1)
        MainMenue.add_cascade(label = '10  Steps Fix', menu =  SmallMenue2)
        MainMenue.add_cascade(label = '20  Steps Fix', menu =  SmallMenue3)
        MainMenue.add_cascade(label = '30  Steps Fix', menu =  SmallMenue4)
        MainMenue.add_cascade(label = 'All Steps Fix', menu =  SmallMenue5)

        try:
            #spawn it
            MainMenue.tk_popup(e.widget.winfo_rootx(), e.widget.winfo_rooty()+10)
        except:
        
            return 'Could not spawn the menue...'
                
    def rClickerFit(self,e):
        ''' 
        ####################################################################################
        right click context menu for all Tk Entry and Text widgets
        This is done in an efoort of readibility...
        
        It will allow drop down when clicking a button
        ####################################################################################
        '''
        #Set the focus on the widget
        e.widget.focus()

        #prepare the drop down menue options
        nclst=[
               (' Simple Fit',     partial(self.Parent.Recalculate,0)),
               (' Consolidate increasing',   partial(self.Parent.Recalculate,'Consolidate')),
               (' Consolidate decreasing',   partial(self.Parent.Recalculate,'!Consolidate')),
               (' Redraw',   partial(self.Parent.CallConstructor,self.DataClass.RamFit.Current))
               ]

        rmenu = tk.Menu(None, tearoff=0, takefocus=0)

        for (txt, cmd) in nclst:
            rmenu.add_command(label=txt, command=cmd)

        rmenu.tk_popup(e.widget.winfo_rootx(), e.widget.winfo_rooty()+10)

    
    
    def lClickerFitRight(self,e):
        ''' 
        ####################################################################################
        right click context menu for all Tk Entry and Text widgets
        This is done in an efoort of readibility...
        
        It will allow drop down when clicking a button
        ####################################################################################
        '''

        try:
            
            #Set the focus on the widget
            e.widget.focus()

            #prepare the drop down menue options
            nclst=[
                   (' Fit Last  1 ',     partial(self.Parent.Recalculate,-1 )),
                   (' Fit Last 10 ',     partial(self.Parent.Recalculate,-10)),
                   (' Fit Last 20 ',     partial(self.Parent.Recalculate,-20)),
                   (' Fit Last 30 ',     partial(self.Parent.Recalculate,-30)),
                   (' Fit Until Start ', partial(self.Parent.Recalculate,'START'))
                   ]

            rmenu = tk.Menu(None, tearoff=0, takefocus=0)

            for (txt, cmd) in nclst:
                rmenu.add_command(label=txt, command=cmd)

            rmenu.tk_popup(e.widget.winfo_rootx(), e.widget.winfo_rooty()+10)

        finally:
            # make sure to release the grab (Tk 8.0a1 only)
            rmenu.grab_release()

        return "break"

    def lClickerFitLeft(self,e):
        ''' 
        ####################################################################################
        right click context menu for all Tk Entry and Text widgets
        This is done in an efoort of readibility...
        
        It will allow drop down when clicking a button
        ####################################################################################
        '''

        try:
            
            #Set the focus on the widget
            e.widget.focus()

            #prepare the drop down menue options
            nclst=[
                   (' Fit Next  1 ',   partial(self.Parent.Recalculate,1 )),
                   (' Fit Next 10 ',   partial(self.Parent.Recalculate,10)),
                   (' Fit Next 20 ',   partial(self.Parent.Recalculate,20)),
                   (' Fit Next 30 ',   partial(self.Parent.Recalculate,30)),
                   (' Fit Until End ', partial(self.Parent.Recalculate,'END'))
                   ]

            rmenu = tk.Menu(None, tearoff=0, takefocus=0)

            for (txt, cmd) in nclst:
                rmenu.add_command(label=txt, command=cmd)

            rmenu.tk_popup(e.widget.winfo_rootx(), e.widget.winfo_rooty()+10)

        finally:
            
            # make sure to release the grab (Tk 8.0a1 only)
            rmenu.grab_release()

        return "break"

    def lClickerCopyRight(self,e):
        ''' 
        ####################################################################################
        right click context menu for all Tk Entry and Text widgets
        This is done in an efoort of readibility...
        
        It will allow drop down when clicking a button
        ####################################################################################
        '''

        try:
            
            #Set the focus on the widget
            e.widget.focus()

            #prepare the drop down menue options
            nclst=[
                   (' Copy Last  1 ',     partial(self.Parent.Copy,-1 )),
                   (' Copy Last 10 ',     partial(self.Parent.Copy,-10)),
                   (' Copy Last 20 ',     partial(self.Parent.Copy,-20)),
                   (' Copy Last 30 ',     partial(self.Parent.Copy,-30))
                   ]

            rmenu = tk.Menu(None, tearoff=0, takefocus=0)

            for (txt, cmd) in nclst:
                rmenu.add_command(label=txt, command=cmd)

            rmenu.tk_popup(e.widget.winfo_rootx(), e.widget.winfo_rooty()+10)

        finally:
            # make sure to release the grab (Tk 8.0a1 only)
            rmenu.grab_release()

        return "break"

    def lClickerCopyLeft(self,e):
        ''' 
        ####################################################################################
        right click context menu for all Tk Entry and Text widgets
        This is done in an efoort of readibility...
        
        It will allow drop down when clicking a button
        ####################################################################################
        '''

        try:
            
            #Set the focus on the widget
            e.widget.focus()

            #prepare the drop down menue options
            nclst=[
                   (' Copy Next  1 ',   partial(self.Parent.Copy,1 )),
                   (' Copy Next 10 ',   partial(self.Parent.Copy,10)),
                   (' Copy Next 20 ',   partial(self.Parent.Copy,20)),
                   (' Copy Next 30 ',   partial(self.Parent.Copy,30))
                   ]

            rmenu = tk.Menu(None, tearoff=0, takefocus=0)

            for (txt, cmd) in nclst:
                rmenu.add_command(label=txt, command=cmd)

            rmenu.tk_popup(e.widget.winfo_rootx(), e.widget.winfo_rooty()+10)

        finally:
            # make sure to release the grab (Tk 8.0a1 only)
            rmenu.grab_release()

        return "break"
    
    def close_windows(self):
        
        #output
        VisOut.TextBox(Title = 'Action', Text = 'Closing Window', state = 1)
        
        #destroy master window
        self.master.destroy()

    def AddLorrentz(self):
        '''
        ######################################################################
        This fucntion is an addition in version 0.1.02
        
        it allows the user to add a lorrentzian into the system. Note that
        this means also resetign the fix array and probably reloading the 
        general interface fo entries as it is not proof to live additions
        ######################################################################
        '''
    
        ########################################
        #First add the new lorrentzian element
        for i in range(0, len(self.DataClass.RamFit.RawData)):
            self.DataClass.RamFit.AddFit(ID = i, Type = 0)
        
        ########################################
        #Reset fixes
        self.HowMany[0] += 1
        
        ########################################
        #Reset the Frame
        self.Reset_Entry_Frame(Fixes = [False,True,True,True])

        ########################################
        #Call fit vis routines
        self.DataClass.RamFit.Fig.Reset()
    
    def AddLinear(self):
        '''
        ######################################################################
        This fucntion is an addition in version 0.1.02
        
        it allows the user to add a lorrentzian into the system. Note that
        this means also resetign the fix array and probably reloading the 
        general interface fo entries as it is not proof to live additions
        ######################################################################
        '''
    
        ########################################
        #First add the new lorrentzian element
        for i in range(0, len(self.DataClass.RamFit.RawData)):
            self.DataClass.RamFit.AddFit(ID = i, Type = 1)
        
        ########################################
        #Reset fixes
        self.HowMany[1] += 1
        
        ########################################
        #Reset the Frame
        self.Reset_Entry_Frame(Fixes = [True,False,True,True])

        ########################################
        #Call fit vis routines
        self.DataClass.RamFit.Fig.Reset()

    def Remove(self,index):
        '''
        ######################################################################
        This fucntion is an addition in version 0.1.02
        
        It allows the user to remove a specific lorrentzian. This can be
        very usefull if to many have been created orloaded to that effect.
        ######################################################################
        '''
        pass
    
    def SubmitGeneral(self,idx,num):
        '''
        ######################################################################
        In version 2.01 the functions where made nameless therefore allowing 
        more felxibility when it comes to adding or editing the functions
        ######################################################################
        '''
        
        #loop over parameters
        for i in range(self.DataClass.RamFit.Function_Info_Pointers[idx].ParameterNumber):
            
            #save ouput
            self.DataClass.RamFit.Function_Pointers[idx][self.DataClass.RamFit.Current][num].ParametersIni[i+1] = float(self.DataClass.RamFit.Function_Info_Pointers[idx].Fields[num][2*i+1][0].get())
            self.DataClass.RamFit.Function_Pointers[idx][self.DataClass.RamFit.Current][num].Parameters[i+1] = self.DataClass.RamFit.Function_Pointers[idx][self.DataClass.RamFit.Current][num].ParametersIni[i+1]
            
            if self.Fix[idx][num][i].get() == 1:
                self.DataClass.RamFit.Function_Pointers[idx][self.DataClass.RamFit.Current][num].ParametersFix[i+1] = 1
            else:
                self.DataClass.RamFit.Function_Pointers[idx][self.DataClass.RamFit.Current][num].ParametersFix[i+1] = 0

        ###############################
        #set the Color
        
        for i in range(0,len(self.DataClass.RamFit.Function_Pointers[idx])):
                
            self.DataClass.RamFit.Function_Pointers[idx][i][num].Color = self.DataClass.RamFit.Function_Info_Pointers[idx].Fields[num][-3][0].GetColor()
            self.DataClass.RamFit.Function_Pointers[idx][i][num].Group = self.DataClass.RamFit.Function_Info_Pointers[idx].Fields[num][-2][0].get()
            self.DataClass.RamFit.Function_Pointers[idx][i][num].Name  = self.DataClass.RamFit.Function_Info_Pointers[idx].Fields[num][-1][0].get()

            if self.Trace[idx][num].get() == 1:
                
                self.DataClass.RamFit.Function_Pointers[idx][i][num].Trace = True

            else:

                self.DataClass.RamFit.Function_Pointers[idx][i][num].Trace = False


    def SubmitAll(self):
        '''
        ######################################################################
        loop over submit for all lorrentzians
        ######################################################################
        '''

        for j in range(0,len(self.DataClass.RamFit.Function_Pointers)):
        
            for i in range(0,len(self.DataClass.RamFit.Function_Pointers[j][self.DataClass.RamFit.Current])):
                
                self.SubmitGeneral(j,i)

    def Reset(self,num):
        '''
        ######################################################################
        Go back to the initial values
        ######################################################################
        '''
        
        #set the values
        for i in range(0,4):
            #delete old entry
            self.B[num][2*i+1][0].delete(0, tk.END)
            
            #,otify uer values hav been set
            self.B[num][2*i+1][0].insert(0,str(round(self.DataClass.RamFit.Function_Pointers[0][self.DataClass.RamFit.Current][num].ParametersIni[i+1],4)))

    def Reset_All(self):
        '''
        ######################################################################
        loop over reset for all lorrentzians
        ######################################################################
        '''
    
        for i in range(0,len(self.DataClass.RamFit.Function_Pointers[0][self.DataClass.RamFit.Current])):
            self.Reset(i)

    def FetchGeneral(self,idx,num):
        '''
        ######################################################################
        Go back to the initial values
        ######################################################################
        '''
        
        ###############################
        #set the values
        for i in range(self.DataClass.RamFit.Function_Info_Pointers[idx].ParameterNumber):
        
            #delete old entry
            self.DataClass.RamFit.Function_Info_Pointers[idx].Fields[num][2*i+1][0].delete(0, tk.END)
            
            #process the number into scientific
            Value = self.DataClass.RamFit.Function_Pointers[idx][self.DataClass.RamFit.Current][num].Parameters[i+1]
            
            if Value < 1:
            
                Value = str('%.4E' % decimal.Decimal(Value))
            
            else:
            
                Value = str( decimal.Decimal(Value))
            
            #Put the finished values
            self.DataClass.RamFit.Function_Info_Pointers[idx].Fields[num][2*i+1][0].insert(0,Value)
            
            if self.DataClass.RamFit.Function_Pointers[idx][self.DataClass.RamFit.Current][num].ParametersFix[i+1] == 1:
                
                #Set the logical
                self.Fix[idx][num][i].set(1)
                
                #set button state
                self.DataClass.RamFit.Function_Info_Pointers[idx].Fields[num][2*i][0].state(['selected'])
            
            else:
                
                #Set the logical
                self.Fix[idx][num][i].set(0)
                
                #Set the button state
                self.DataClass.RamFit.Function_Info_Pointers[idx].Fields[num][2*i][0].state(['!selected'])
    
        ###############################
        #set the Color
        self.DataClass.RamFit.Function_Info_Pointers[idx].Fields[num][-3][0].LoadColor(self.DataClass.RamFit.Function_Pointers[idx][self.DataClass.RamFit.Current][num].Color)
        
        self.DataClass.RamFit.Function_Info_Pointers[idx].Fields[num][-2][0].delete(0,tk.END)
        self.DataClass.RamFit.Function_Info_Pointers[idx].Fields[num][-2][0].insert(0,str(self.DataClass.RamFit.Function_Pointers[idx][self.DataClass.RamFit.Current][num].Group))
        
        self.DataClass.RamFit.Function_Info_Pointers[idx].Fields[num][-1][0].delete(0,tk.END)
        self.DataClass.RamFit.Function_Info_Pointers[idx].Fields[num][-1][0].insert(0,str(self.DataClass.RamFit.Function_Pointers[idx][self.DataClass.RamFit.Current][num].Name))
        
        if self.DataClass.RamFit.Function_Pointers[idx][self.DataClass.RamFit.Current][num].Trace:
                
            self.Trace[idx][num].set(1)

        else:

            self.Trace[idx][num].set(0)

    def Fetch_All(self):
        '''
        ######################################################################
        loop over Fetch for all lorrentzians
        ######################################################################
        '''
    
        for j in range(0,len(self.DataClass.RamFit.Function_Pointers)):
        
            for i in range(0,len(self.DataClass.RamFit.Function_Pointers[j][self.DataClass.RamFit.Current])):
            
                self.FetchGeneral(j,i)

    def UpdateContent(self):

        pass





'''
##################################################
CLASS: NavigatorWindowClass

DESCRIPTION:

This class will manage the fit visualisation windw.
Note that it should be linked to the the other 
windiw throught the Parent class exchange.

o------------------------------------------------o

PARAMETERS:

- None

##################################################
'''


class Vis_Fitting_Class:
    
    '''
    ##################################################
    FUNCTION: __init__
    
    DESCRIPTION:
    
    Initiating class. This is where the layout is 
    created and all functions initalised. It wil then
    by initiated by the standard window manager
    procedure
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - Window_Manager: This is the manager structure.
    - DataClass: Data type strucure.
    
    ##################################################
    '''
    
    def __init__(self, Window_Manager, Parent):

        ##############################################
        #Local pointers
        self.Parent         = Parent
        self.Window_Manager = Window_Manager
    
    
    
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
    
        ##############################
        #Dataclass from the program becomes locally linked
        self.DataClass = self.Parent.DataClass
    
        #Set parameters
        self.padding = '5p'
    
        self.CheckSelected = False
        self.NormalizeBool = False
        self.SelectedVar   = 0
    
        #Reset Selection
        self.ResetSelect()
    
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
        #set Root
        
        self.Root.title("Fitting Visualisation ("
                        + self.DataClass.Info.GetInfoVal('Name')
                        + ")")
        
        self.Root.configure(background = 'black')
        
        self.Root.resizable(width       = True,
                              height    = True)
        
        ##############################################
        #set the Frame
        self.Frame = ttk.Frame(self.Root,
                               padding = self.padding)
        
        
        ##############################################
        #Populate the Frame
        self.Populate_Frame()
        
        
        
    '''
    ##################################################
    FUNCTION: Populate_Frame
    
    DESCRIPTION:
    
    This routine will set the initial Frame nicely.
    The main window is just a logo place holder
    with the menue and therefore has no function.
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - None
    
    ##################################################
    '''
    def Populate_Frame(self):
        
        
        

        
        ##############################################
        #button Frame
        self.Start = ttk.Frame(self.Frame,
                               relief = 'sunken' ,
                               padding = self.padding)
        
        #set buttons
        self.But01   = ttk.Checkbutton(self.Start,
                                       text = 'Navigator'  )
                                       
        self.But02   = ttk.Checkbutton(self.Start,
                                       text = 'Information')
                                       
        self.But03   = ttk.Checkbutton(self.Start,
                                       text = 'Selector'   )
                                       
        self.But04   = ttk.Checkbutton(self.Start,
                                       text = 'Graph'      )
        
        #grid the buttons
        self.But01.grid( row = 0, column = 1, sticky = tk.E+tk.W)
        
        self.But02.grid( row = 0, column = 2, sticky = tk.E+tk.W)
        
        self.But03.grid( row = 0, column = 3, sticky = tk.E+tk.W)
        
        self.But04.grid( row = 0, column = 4, sticky = tk.E+tk.W)
        
        #finnaly grid the main Frame
        self.Start.grid( row = 0 , column = 0 , sticky = tk.E+tk.W+tk.N+tk.S , pady = 5)
        
        ##############################################
        #This is the top navigator Frame to be used
        
        #create the Frame
        self.NavFrame = ttk.Frame(self.Frame,
                                  relief = 'sunken' ,
                                  padding = self.padding)
        
        #introduce the navigator if needed
        if not self.DataClass.Type == 'Single':
            
            #set buttons
            self.NextButton   = ttk.Button(self.NavFrame,
                                           text = '>',
                                           width = 4,
                                           command = partial(self.Parent.IO_Fitting_Class.Change,
                                                             1))
            
            self.PrevButton   = ttk.Button(self.NavFrame,
                                           text = '<',
                                           width = 4,
                                           command = partial(self.Parent.IO_Fitting_Class.Change,
                                                             -1))
            
            self.Next10Button = ttk.Button(self.NavFrame,
                                           text = '>>',
                                           width = 4,
                                           command = partial(self.Parent.IO_Fitting_Class.Change,
                                                             10))
            
            self.Prev10Button = ttk.Button(self.NavFrame,
                                           text = '<<',
                                           width = 4,
                                           command = partial(self.Parent.IO_Fitting_Class.Change,
                                                             -10))
            
            self.NavLabel     = ttk.Label( self.NavFrame,
                                          text = str(int(self.DataClass.RamFit.Current)),
                                          anchor = tk.CENTER)
            
            #grid the buttons onto the Frame
            self.Prev10Button.grid(row = 0,
                                   column = 1,
                                   sticky = tk.E+tk.W)
            
            self.PrevButton.grid(row = 0,
                                 column = 2,
                                 sticky = tk.E+tk.W)
            
            self.NavLabel.grid(row = 0,
                               column = 3,
                               sticky = tk.E+tk.W)
            
            self.NextButton.grid(row = 0,
                                 column = 4,
                                 sticky = tk.E+tk.W)
            
            self.Next10Button.grid(row = 0,
                                   column = 5,
                                   sticky = tk.E+tk.W)
    
            #set the gridcongiure
            self.NavFrame.grid_columnconfigure(1,
                                               weight = 1)
            
            self.NavFrame.grid_columnconfigure(2,
                                               weight = 1)
            
            self.NavFrame.grid_columnconfigure(3,
                                               weight = 1)
            
            self.NavFrame.grid_columnconfigure(4,
                                               weight = 1)
            
            self.NavFrame.grid_columnconfigure(5,
                                               weight = 1)
        
        
        
        else:
        
            self.NavLabel     = ttk.Label(self.NavFrame,
                                          text = 'Single Measurement',
                                          anchor = tk.CENTER)
                                          
            self.NavLabel.grid(     row = 0, column = 0, sticky = tk.E+tk.W+tk.N+tk.S)
        
        
        #finnaly place the created grid
        self.NavFrame.grid( row = 0 , column = 1, sticky = tk.E+tk.W+tk.N+tk.S, padx = 5,  pady = 5)
        
        ##############################################
        ##############################################
        #This is the top information Frame Frame to be used
        
        #create the Frame
        self.InfoFrame = ttk.Frame(self.Frame, relief = 'sunken' , padding = self.padding)
        
        #put investigator interface
        self.CheckButton    = [None]*4
        self.InfoLabel      = [None]*8
        self.SelectLabel    = [None]*8
            
        ################################
        #set the selection labels and information layout
        self.InfoLabel[0] = ttk.Label(self.InfoFrame, text = 'Name:'            , anchor = tk.CENTER)
        self.InfoLabel[1] = ttk.Label(self.InfoFrame, text = 'Position:'        , anchor = tk.CENTER)
        self.InfoLabel[2] = ttk.Label(self.InfoFrame, text = 'HWHM:'            , anchor = tk.CENTER)
        self.InfoLabel[3] = ttk.Label(self.InfoFrame, text = 'Amplitude:'       , anchor = tk.CENTER)
        self.InfoLabel[4] = ttk.Label(self.InfoFrame, text = 'Assymetry:'       , anchor = tk.CENTER)
        self.InfoLabel[5] = ttk.Label(self.InfoFrame, text = ''                 , anchor = tk.CENTER)
        self.InfoLabel[6] = ttk.Label(self.InfoFrame, text = ''                 , anchor = tk.CENTER)
        self.InfoLabel[7] = ttk.Label(self.InfoFrame, text = ''                 , anchor = tk.CENTER)
    
        self.SelectLabel[0] = ttk.Label(self.InfoFrame, text = str(self.Selected[0]),width = 10 , anchor = tk.CENTER)
        self.SelectLabel[1] = ttk.Label(self.InfoFrame, text = str(self.Selected[1]),width = 10 , anchor = tk.CENTER)
        self.SelectLabel[2] = ttk.Label(self.InfoFrame, text = str(self.Selected[2]),width = 10 , anchor = tk.CENTER)
        self.SelectLabel[3] = ttk.Label(self.InfoFrame, text = str(self.Selected[3]),width = 10 , anchor = tk.CENTER)
        self.SelectLabel[4] = ttk.Label(self.InfoFrame, text = str(self.Selected[4]),width = 10 , anchor = tk.CENTER)
        self.SelectLabel[5] = ttk.Label(self.InfoFrame, text = str(self.Selected[5]),width = 10 , anchor = tk.CENTER)
        self.SelectLabel[6] = ttk.Label(self.InfoFrame, text = str(self.Selected[6]),width = 10 , anchor = tk.CENTER)
        self.SelectLabel[7] = ttk.Label(self.InfoFrame, text = str(self.Selected[7]),width = 10 , anchor = tk.CENTER)
        
        ################################
        #Grid the content
        for i in range(len(self.SelectLabel)):
            
            #pace the stuff
            self.InfoLabel[i].grid(row = 2*i, column =  0 , sticky = tk.E+tk.W)
            self.SelectLabel[i].grid(row = 2*i+1, column = 0 , sticky = tk.E+tk.W)
        
        #configure the ssociated grid
        self.InfoFrame.grid_rowconfigure(2*i+2 , weight = 1)
        
        #finnaly place the created grid
        self.InfoFrame.grid(row = 0, column = 2, rowspan = 4, columnspan= 1, sticky = tk.E+tk.W+tk.N+tk.S, pady = 5)
        
        ##############################################
        ##############################################

        self.PopulateSelector()
        self.SelectorFrame.grid(row = 1, column = 0, columnspan = 2, sticky = tk.E+tk.W)
        self.SelectorFrame.grid_columnconfigure(8, weight = 1)
        self.ResetSelector()


        ##############################################
        #This is the top information Frame Frame to be used
        
        #initiate the button Frame
        self.FigFrame = ttk.Frame(self.Frame, relief = 'sunken' , padding = self.padding,takefocus=1)
        self.FigFrame.focus_force()
        
        ##############################
        #introduce our new plot canvas here
        self.FigCanvas = SimplePlot.MultiPlotCanvas(self.FigFrame,
                                                    grid = [[True]],
                                                    ratioX   = [1],
                                                    ratioY   = [1],
                                                    bg="white",
                                                    highlightthickness=0)
                                                    
        #grab the subplot definitions
        self.ax = self.FigCanvas.GetSubPlot(0,0)
        
        ######################################################
        #Set some padding parameters
        self.ax.Axes.PaddingIn              = [0.0 , 0.0, 0.0 , 0.0 ]
        self.ax.Axes.PaddingOut             = [0.15, 0.1, 0.05, 0.05]
        self.ax.Axes.Thickness              = [2,2,2,2]
        self.ax.Axes.XTickSpacing           = 50
        self.ax.Axes.XTickType              = 1
        
        self.ax.Axes.isYSci                 = [True,True]
        self.ax.isYSci                      = True
    
        self.ax.Pointer.YSciPrecision       = '%.1e'
        self.ax.Axes.YSciPrecision          = ['%.2e','%.1e']
        
        #launch the drawer once will initialise all clases
        self.ax.DrawAll()
        
        #set the default imaging mode to Tkinter Canvas
        self.ax.Live = 1
        self.ax.Pointer.BindMethod(self.OnSelect)
        
        #put the Frame
        self.FigFrame.grid( row = 3,
                           column = 0,
                           columnspan = 2,
                           sticky = tk.E+tk.W+tk.N+tk.S,
                           pady = 5)
        
        self.FigFrame.grid_rowconfigure(0,
                                        weight = 1)
                                        
        self.FigFrame.grid_columnconfigure(0,
                                           weight = 1)
        
        ##############################################
        #configure all the the columns and rows of Frame now anf pack it
        self.Frame.grid_rowconfigure(3,
                                     weight = 1)
        self.Frame.grid_columnconfigure(1,
                                        weight = 1)
        
        #plcae Frame
        self.Frame.grid(row = 0 ,
                        column = 0,
                        sticky = tk.E+tk.W+tk.N+tk.S )

        #give weight...
        self.Root.grid_columnconfigure(0, weight = 1)
        self.Root.grid_rowconfigure(   0, weight = 1)
        
        #Make them all toggable
        self.ToggleNav = ToggledFrame(self.But01,
                                      self.NavFrame,
                                      focus = None)
                                      
        self.ToggleInf = ToggledFrame(self.But02,
                                      self.InfoFrame,
                                      focus = None)
                                      
        self.ToggleInf = ToggledFrame(self.But03,
                                      self.SelectorFrame,
                                      focus = None)
                                      
        self.ToggleFig = ToggledFrame(self.But04,
                                      self.FigFrame,
                                      focus = None)
        
        #refresh/create the fit
        self.Refresh(init = True)


    def PopulateSelector(self,Location = 1, Parent = None):
        '''
        ####################################################################################
        This function will build and Populate the visual editor
        
        This load a Simpleplot routine and the default iPlot function will be used to allow
        for interaction.
        ####################################################################################
        '''
        #######################################
        #######################################
        #Create the container Frame
        self.SelectorFrame = ttk.Frame(self.Frame, relief = 'sunken' , padding = self.padding)
    
        #######################################
        #######################################
        #introduce The selectors here
        self.Selectors              = []
        self.SelectorButtons        = []
        self.SelectorLabels         = []
        self.SelectorStringVars     = [tk.StringVar(),tk.StringVar(),tk.StringVar()]
        self.SelectorList           = []
        self.Normalize              = tk.IntVar()
    
        #######################################
        #######################################
        #set intvars
        self.SelectorStringVars[0].set('Spectra')
        self.SelectorStringVars[1].set('Raw Data')
        self.SelectorStringVars[2].set('None')
        self.Normalize.set(1)
        
        #######################################
                                
        self.SelectorButtons.append([ttk.Button(self.SelectorFrame,
                                                text = 'Set',
                                                command = self.GrabSelector),
                                     0,
                                     7,
                                     1,
                                     1,
                                     tk.E + tk.W])
                                
        self.SelectorButtons.append([ttk.Checkbutton(self.SelectorFrame,
                                                     text = 'Normalize',
                                                     variable = self.Normalize),
                                     0,
                                     6,
                                     1,
                                     1,
                                     tk.E + tk.W])
                                
        #######################################
        self.SelectorLabels.append([ttk.Label(self.SelectorFrame,
                                              text = 'Type:'),
                                    0,
                                    0,
                                    1,
                                    1,
                                    tk.E + tk.W])
                                
        self.SelectorLabels.append([ttk.Label(self.SelectorFrame,
                                              text = 'Spec.:'),
                                    0,
                                    2,
                                    1,
                                    1,
                                    tk.E + tk.W])
              
        self.SelectorLabels.append([ttk.Label(self.SelectorFrame,
                                              text = 'Parameter:'),
                                    0,
                                    4,
                                    1,
                                    1,
                                    tk.E + tk.W])
           
        #######################################
        self.ResetSelector()
                           
        #######################################
        #######################################
        #Place it all here
                           
        for List in [self.SelectorLabels , self.SelectorButtons]:
        
            for Element in List:
            
                Element[0].grid(row         = Element[1],
                                column      = Element[2],
                                rowspan     = Element[3],
                                columnspan  = Element[4],
                                sticky      = Element[5])
                                

    
    
    def GrabSelector(self):
        
        '''
        ####################################################################################
        This function will grab the current coordiantes and display them in the visual Frame
        ####################################################################################
        '''
        
        #######################################
        #######################################
        #is it the sectra
        
        if self.SelectorStringVars[0].get() == 'Spectra':
        
            if self.SelectorStringVars[1].get() == 'Raw Data':
        
                Idx = [0,0,'Raw Data',            False]
    
            elif self.SelectorStringVars[1].get() == 'Selected Data Range':
        
                Idx = [1,0,'Selected Data Range', False]
    
            elif self.SelectorStringVars[1].get() == 'Fit':
        
                Idx = [2,0,'Fit',                 False]
                    
            elif self.SelectorStringVars[1].get() == 'Residual':
        
                Idx = [3,0,'Residual',            False]
        
        #######################################
        #######################################
        #is it the parameters
        elif self.SelectorStringVars[0].get() == 'Parameters':
            
            ##############################
            #if the whole is lorrentzian
            for kk in range(0, len(self.DataClass.RamFit.Function_Info_Pointers)):
            
                if self.SelectorStringVars[1].get() == self.DataClass.RamFit.Function_Info_Pointers[kk].Name:
                    
                    for ll in range(0, self.DataClass.RamFit.Function_Info_Pointers[kk].ParameterNumber):
                    
                        if self.SelectorStringVars[2].get() == self.DataClass.RamFit.Function_Info_Pointers[kk].ParameterNames[ll]:
                
                            if self.Normalize.get() == 0:
                                
                                Idx = [10 + kk, ll, self.DataClass.RamFit.Function_Info_Pointers[kk].ParameterNames[ll], False]
                    
                            else:
            
                                Idx = [10 + kk, ll, self.DataClass.RamFit.Function_Info_Pointers[kk].ParameterNames[ll], True]
                
    
        self.Parent.IO_Fitting_Class.RefreshVar = Idx
            
        self.Refresh()
    
    def SetSelector(self, event = None):
        '''
        ####################################################################################
        This function will grab the current coordiantes and display them in the visual Frame
        ####################################################################################
        '''
        #######################################
        #######################################
        #grab info
        Target, Idx, Which = self.GrabInfo()

        #######################################
        #######################################
        #Extract the array
        ModificationList = self.ax.Modifier.Log

        for i in range(0, len(ModificationList)):

            Target[ModificationList[i][1]][Which].Parameters[Idx] = ModificationList[i][4][1]

            if self.MakeFixed.get() == 1:

                Target[ModificationList[i][1]][Which].ParametersFix[Idx] = 1

        #######################################
        #######################################
        #Refresh it
        self.Parent.IO_Fitting_Class.ChangeCurrent(0)
        
        #reset the modifier log
        self.ax.Modifier.Log = []


    def ResetSelector(self, event = None):
        '''
        ####################################################################################
        This function will create the Frame linking all the boundaries to the fitter. 
        The boundaries can then be Fetched to build the containers in Ramfit.
        Please note that each conatainer can be tunred off or on to laod the default
        parameters.
        ####################################################################################
        '''
        #######################################
        #######################################
        #grab defaults
        Default_1  = str(self.SelectorStringVars[0].get())
        Default_2  = str(self.SelectorStringVars[1].get())
        Default_3  = str(self.SelectorStringVars[2].get())
        
        
        #######################################
        #######################################
        #Create the lists
        FirstList = ['Spectra',
                     'Parameters']
                     
        ThirdList = ['None']
                     
        if self.SelectorStringVars[0].get() == 'Spectra':
        
            SecondList = ['Raw Data',
                          'Selected Data Range',
                          'Fit',
                          'Residual']
        
        
        elif self.SelectorStringVars[0].get() == 'Parameters':
        
            SecondList = [self.DataClass.RamFit.Function_Info_Pointers[ll].Name
                          
                          if len(self.DataClass.RamFit.Function_Pointers[ll][0])>0 else 'None'
                          
                          for ll in range(0, len(self.DataClass.RamFit.Function_Info_Pointers)) ]
        
                       
            for kk in range(0, len(self.DataClass.RamFit.Function_Info_Pointers)):
            
                if self.SelectorStringVars[1].get() == self.DataClass.RamFit.Function_Info_Pointers[kk].Name:
                       
                    ThirdList =  self.DataClass.RamFit.Function_Info_Pointers[kk].ParameterNames
        

        try:
            for Element in self.VisSelectors:
        
                Element[0].destroy()

        except:
            pass

        self.VisSelectors = []

        #######################################
        #######################################
        #Create the elements
        
        self.Selectors.append([ttk.OptionMenu(self.SelectorFrame,
                                                 self.SelectorStringVars[0],
                                                 Default_1,
                                                 *FirstList,
                                                 command = self.ResetSelector),
                                  0,
                                  1,
                                  1,
                                  1,
                                  tk.E + tk.W])
                           
        
        self.Selectors.append([ttk.OptionMenu(self.SelectorFrame,
                                                 self.SelectorStringVars[1],
                                                 Default_2,
                                                 *SecondList,
                                                 command = self.ResetSelector),
                                  0,
                                  3,
                                  1,
                                  1,
                                  tk.E + tk.W])
                                

        self.Selectors.append([ttk.OptionMenu(self.SelectorFrame,
                                                 self.SelectorStringVars[2],
                                                 Default_3,
                                                 *ThirdList,
                                                 command = self.ResetSelector),
                                  0,
                                  5,
                                  1,
                                  1,
                                  tk.E + tk.W])
    
        #######################################
        #######################################
        #Place it all here
        
        for Element in self.Selectors:
        
            Element[0].grid(row         = Element[1],
                            column      = Element[2],
                            rowspan     = Element[3],
                            columnspan  = Element[4],
                            sticky      = Element[5])


    def close_windows(self):
        
        #destroy master window
        self.Root.destroy()


    def ResetSelect(self):
    
        #set the 4 values
        self.Selected = ['']*8
    
    
    def Refresh(self,init = False, Update = False):
        '''
        ##########################################################################################
        This might very well be the main function of the entire Frame. 
        
        Note that this function splits of and manages event handlers throughout the matplotlib
        interface through bindings...
        
        - The crosshair binding
        - The shift binding
        - The click binding
        ##########################################################################################
        '''
        
        ##############################################
        #Prepare the refresh
        #select the path to go
        
        #grab var
        if init:
            self.Parent.IO_Fitting_Class.RefreshVar = [1,0,'',False]
            self.Update = False
            self.ID = self.Parent.IO_Fitting_Class.RefreshVar
        
        if self.ID == self.Parent.IO_Fitting_Class.RefreshVar and not init:
            
            Update = True
        
        self.ID = self.Parent.IO_Fitting_Class.RefreshVar
        
        #####################################
        #The user wants to show the raw data
        
        if self.ID[0] == 0:
            
            #Send out the raw fit
            self.DataClass.RamFit.Fig.BuildLowerGraph(self.ax, Update = Update)
            self.ax.Title.SetTitle(text = 'Raw Data Plot at '+str(self.DataClass.RamFit.Current))
        
        elif self.ID[0] == 1:
            
            #Send out the comp fit
            self.DataClass.RamFit.Fig.BuildLowerGraph(self.ax, Update = Update)
            self.ax.Title.SetTitle(text = 'Data Range used for the fit at '+str(self.DataClass.RamFit.Current))
        
        elif self.ID[0] == 2:
            
            #Send out request
            self.DataClass.RamFit.Fig.BuildUpperGraph(self.ax,self.DataClass.RamFit, Update = Update)
            self.ax.Title.SetTitle(text = 'Resulting Fit Plot at '+str(self.DataClass.RamFit.Current))
                
        elif self.ID[0] == 3:
            
            #Send out request
            self.DataClass.RamFit.Fig.BuildRestGraph(self.ax, Update = Update)
            self.ax.Title.SetTitle(text = 'Residual Plot at '+str(self.DataClass.RamFit.Current))
                
        #######################################
        #The user wants to show the point Data

        elif self.ID[0] > 9:
                
            #Send out the Position
            self.DataClass.RamFit.Fig.BuildScatter(self.ax, Type = self.ID)
            self.ax.Title.SetTitle(text = 'Scattered '+self.ID[2]+' Plot')
            

    def OnSelect(self,IDX, PointerPosition):
        '''
        ##########################################################################################
        This function will allow the editing of the information pane in the fitting window class. 
        Note that it counts available functions and then retunrs the identification from the 
        SimplePlot function binding.
        ##########################################################################################
        '''
        if self.ID[0] < 9:
        
            Select = self.DataClass.RamFit.Current
        
        else:
            
            #create the X array to investigate
            X = numpy.asarray(self.DataClass.Contour.Projection[1])
            
            Select = (numpy.abs(X - PointerPosition[0])).argmin()
        
        #functions are drawn in order but avoid the trace
        IDs = []
        
        if self.ID[0] < 9:
        
            for kk in range(0,len(self.DataClass.RamFit.Function_Pointers)):
                
                for i in range(0,len(self.DataClass.RamFit.Function_Pointers[kk][Select])):
                
                    if self.DataClass.RamFit.Function_Pointers[kk][Select][i].Trace:
                
                        IDs.append(self.DataClass.RamFit.Function_Pointers[kk][Select][i])
        
        else:
        
            for kk in range(0,len(self.DataClass.RamFit.Function_Pointers)):
                
                for i in range(0,len(self.DataClass.RamFit.Function_Pointers[kk][Select])):
                
                    if self.DataClass.RamFit.Function_Pointers[kk][Select][i].Trace and not self.DataClass.RamFit.Function_Pointers[kk][Select][i].Zero:
                
                        IDs.append(self.DataClass.RamFit.Function_Pointers[kk][Select][i])
    
        #set the pointers
        if self.ID[0] < 9:
        
            self.SelectedFunction = IDs[IDX-2]
            
        else:
            
            self.SelectedFunction = IDs[IDX]
            
        self.SelectedPrameter = self.SelectedFunction.Parameters
        
        if IDX > 1 and self.ID[0] < 9:
        
            
            self.SelectLabel[0].config(text = str(self.SelectedFunction.Name))
            
            #change labels
            for i in range(self.SelectedFunction.Info.ParameterNumber):
                
                self.InfoLabel[i+1].config(text = str(self.SelectedFunction.Info.ParameterNames[i]))
                self.SelectLabel[i+1].config(text = str(round(self.SelectedPrameter[i+1],2)))
        
            for i in range(self.SelectedFunction.Info.ParameterNumber, len(self.InfoLabel)-1):

                self.InfoLabel[i+1].config(text = '')
                self.SelectLabel[i+1].config(text = '')

        elif IDX < 2 and self.ID[0] < 9:

            self.SelectLabel[0].config(text = 'Data')
            
            for i in range(0, len(self.InfoLabel)-1):

                self.InfoLabel[i+1].config(text = '')
                self.SelectLabel[i+1].config(text = '')

        elif self.ID[0] > 9:
        
            
            self.SelectLabel[0].config(text = str(self.SelectedFunction.Name))
            
            #change labels
            for i in range(self.SelectedFunction.Info.ParameterNumber):
                
                self.InfoLabel[i+1].config(text = str(self.SelectedFunction.Info.ParameterNames[i]))
                self.SelectLabel[i+1].config(text = str(round(self.SelectedPrameter[i+1],2)))

            for i in range(self.SelectedFunction.Info.ParameterNumber, len(self.InfoLabel)-1):

                self.InfoLabel[i+1].config(text = '')
                self.SelectLabel[i+1].config(text = '')
        else:
    
            #In our precise case the first two plots are the data and fit range
            #change labels
            self.SelectLabel[0].config(text = '-')
            self.SelectLabel[1].config(text = '-')
            self.SelectLabel[2].config(text = '-')
            self.SelectLabel[3].config(text = '-')


    def LineToggler(self,event):
        '''
        ##########################################################################################
        Calls the toggler in the line method from teh draw class this will switch betwenn
        scatter to normal plots with 'o' type markers. Note that this method
        should be linked to the canvas with mpl and the reference key 'l'
        ##########################################################################################
        '''
        
        if event.key == 'l':
        
            #toggle
            self.DataClass.RamFit.Fig.DrawClass.ToggleLines(Toggle = True)

            #refresh
            self.Refresh()

class ToggledFrame():

    '''
    ##########################################################################################
    This is a contracted Frame method and will be used to allow contracting  hiding the inside
    of a given Frame
    
    note the passed on button needs to be a chuckbutton 
    the passed on Frame neesd to be a ttk.Frame
    ##########################################################################################
    '''
    def __init__(self, button , Frame, focus = None):

        #catch the variables and make them class
        self.button  = button
        self.Frame   = Frame
        self.focus   = focus
        
        #create in class varible to show or hide
        self.show = tk.IntVar()
        self.show.set(0)
        
        #Set the button
        self.button.config(command=self.Toggle)
        self.button.config(variable=self.show )
        self.button.config(style='Toolbutton' )
        
        #load the Frame
        self.Frame.config(relief="sunken")
        self.Frame.config(borderwidth=1  )
    
        #toggle once
        self.Toggle()

    def Toggle(self):
        
        if bool(self.show.get()):
            
            #grid the object into place.
            self.Frame.grid()
            
            #see if we have to set a focus
            if not self.focus == None:
                
                self.focus.focus_set()
        
        else:
            
            #hide the object
            self.Frame.grid_remove()

            #see if we have to set a focus
            if not self.focus == None:
                self.focus.focus_set()


class ToggledViewMode():

    '''
    ##########################################################################################
    This is a contracted Frame method and will be used to allow contracting  hiding the inside
    of a given Frame
    
    note the passed on button needs to be a chuckbutton 
    the passed on Frame neesd to be a ttk.Frame
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

class InfoWindowClass:
    

    def __init__(self,master,DataClass):
        
        #link the DataClass
        self.DataClass = DataClass
        
        #set ,aster
        self.master = master
        self.master.title("Sample/Raman Informations")
        
        #set the Frame
        self.Frame = tk.Frame(self.master)
        
        self.Info = tk.Label(self.Frame, text=DataClass.Info.CallInfo(Tk = True))
        self.Info.pack()
    
        #set buttons
        self.quitButton = tk.Button(self.Frame, text = 'Quit', width = 25, command = self.close_windows)
        self.quitButton.pack()
        
        #pack all
        self.Frame.pack(padx=20, pady=20, side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    
    def close_windows(self):
        
        #output
        VisOut.TextBox(Title = 'Action', Text = 'Closing the information window', state = 1)
        
        #destroy master window
        self.master.destroy()

class CustomeButton(tk.Button):

    '''
    ######################################################
    The code to select to create a button with an image 
    at the heart being quiet repetitve, it was decided to
    generalise it
    ######################################################
    '''
    
    def __init__(self, parent,width = 10,height = 10, ImagePath = '',**kwargs):


        #Import all the images
        self.Image = Image.open(ImagePath)
        self.Image = self.Image.resize((width, height), Image.ANTIALIAS)
        self.Image = ImageTk.PhotoImage(self.Image)


        tk.Button.__init__(self,
                           parent,
                           image = self.Image,
                           padx = 2,
                           pady = 2,
                            **kwargs)



