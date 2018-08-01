# -*- coding: utf-8 -*-
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

This is the code related to the Simulation interface. It will probably be
changed later on to accomodate for the integration into R-Data. Note that
the profile calculations will be done for single wavelength for now. Later
a case by case accomodation will be provided.

###########################################################################
"""
################################
#default python imports
import numpy
from functools import partial
import os
import codecs

################################
#for mathematical visualization
# this in an in-house vis. Tool
import SimplePlot.SimplePlot as SimplePlot

################################
#import the computation routines
from RamSim.RamanSim import *

################################
#import Tkinter related
#libraries for wind processing.
from Tkinter import *
import ttk
import Tkinter as tk
import tkFileDialog

def DoNothing():

    pass



class SimulationEditor():
    """
    ###########################################################################
    This routine will build the general interface with contour support and 
    projections to analysis the beam shape at the interfaces. This is version
    0.2.0 and accomodates a more geometrical perception of the problem.
    ###########################################################################
    """
    
    def __init__(self,root):
    
        ####################################
        #initialise frames
        self.FigFrame       = ttk.Frame(root, padding = '10p')
        self.ButtonFrame    = ttk.Frame(root, padding = '10p')
        self.master         = root
        

        ####################################
        #create the button content
        self.SampleSet      = ttk.Button(self.ButtonFrame,
                                         text = 'Samples',
                                         command = self.SampleSet)

        self.RamanSet       = ttk.Button(self.ButtonFrame,
                                         text = 'Raman',
                                         command = self.RamanSet)
                                             
        self.Process        = ttk.Button(self.ButtonFrame,
                                         text = 'Processing',
                                         command = self.Process)
              
        self.Load           = ttk.Button(self.ButtonFrame,
                                         text = 'Load',
                                         command = self.Load)
                                         
        self.Create         = ttk.Button(self.ButtonFrame,
                                         text = 'Create',
                                         command = self.Create)
                                             
        ####################################
        #Place the buttons
        self.SampleSet.grid(    row = 0,
                                column = 0)
        
        self.RamanSet.grid(     row = 0,
                                column = 1)
        
        self.Process.grid(      row = 0,
                                column = 2)
              
        self.Load.grid(         row = 0,
                                column = 3)
                                
        self.Create.grid(       row = 0,
                                column = 4)
        
        ####################################
        #pack the frames
        self.FigFrame.grid(row = 1,
                           column = 0,
                           sticky = E+W+N+S)
                           
        self.ButtonFrame.grid(row = 0,
                              column = 0,
                              sticky = E+W+N+S)
        
        root.grid_rowconfigure(1, weight = 1)
        root.grid_columnconfigure(0, weight = 1)


        ####################################
        #initialise the frames
        self.InitialiseFrames()
        
        ####################################
        #self.InitialiseManagers()
    
    
    def Forgeter(self):
        """
        ###########################################################################
        This function will forget the currently loaded frame
        ###########################################################################
        """
    
        #try to forget a frame
        try:
    
            self.SampleFrame.grid_forget()

        except:
            
            pass

        #try to forget a frame
        try:
    
            self.RamanFrame.grid_forget()

        except:
            
            pass

        #try to forget a frame
        try:
    
            self.ProcessFrame.grid_forget()

        except:
            
            pass
    
    def SampleSet(self):
        """
        ###########################################################################
        This will load the sample frame into the editor...
        ###########################################################################
        """
    
        #call the forgeter
        self.Forgeter()
    
        #place the element on the grid
        self.SampleFrame.grid(row = 1, column = 0)
    

    def RamanSet(self):
        """
        ###########################################################################
        This will load the raman setup frame into the editor to allow setting
        Raman preferences...
        ###########################################################################
        """
    
        #call the forgeter
        self.Forgeter()
    
        #place the element on the grid
        self.RamanFrame.grid(row = 1, column = 0)
    
    def Process(self):
        """
        ###########################################################################
        This will allow to set the processing, like sharing of processor ressources
        and the range of the investigation. This will load the adequat frame into 
        the editor...
        ###########################################################################
        """
    
        #call the forgeter
        self.Forgeter()
    
        #place the element on the grid
        self.ProcessFrame.grid(row = 1, column = 0)
    
    def Load(self):
        """
        ###########################################################################
        This create the routine and put all files into the adequat folder.
        This script can then be called and the simulation will run independently...
        ###########################################################################
        """
        
        #set verbose
        Verbose = True
        
        #oath that will be lonked to opening the search path
        self.PathofInterest = os.getcwd()
        
        #set option
        self.file_opt = options = {}
        options['filetypes']    = [('all files', '.*'), ('Text Files', '.txt'), ('Raman Files', '.py')]
        options['initialdir']   = self.PathofInterest
        options['initialfile']  = 'myfile.py'
        options['title']        = 'Select a File'
    
        #ask the user
        self.LoadPath = tkFileDialog.askopenfilename( **self.file_opt)
        
        #do some processing
        FolderPath = os.path.dirname(self.LoadPath)
        FileName   = self.LoadPath.split(FolderPath)[1].split('/')[1]
    
        #count lines
        num_lines = sum(1 for line in open(self.LoadPath))
        if Verbose:
            print 'Number of Lines: ', num_lines
        
        #open the file
        f = codecs.open(self.LoadPath,
                       'r',
                       'utf-8')
        if Verbose:
            print 'Opened File: ', self.LoadPath
        
        #initialise array
        Content = []
        
        #open the text file
        for i in range(0, num_lines):
        
            #grab
            Content.append(f.readline())
                
        #cloe the file
        f.close()

        #####################################
        #####################################
        #go through for the executable
        
        #set logical positioner
        Execute = False
        Process = False
        
        for i in range(0, num_lines):
    
            if Execute:
                
                exec(Content[i].replace('LocalManager','self.Manager').replace(self.Tab(1),''))
            
            if Process:
            
                exec(Content[i].replace('LocalManager','self.Manager').replace(self.Tab(1),''))
    
            if Content[i] == self.Tab(1) + '#--LOADHEADER--\n':
                
                if Verbose:
                    print 'Found the Header at Line: ', i
                
                Execute = not Execute
            
            if Content[i] == self.Tab(1) + '#--PROCESS PARAMETERS--\n':

                if Verbose:
                    print 'Found the Parameters at Line: ', i
                
                Process = not Process
        
        
        #####################################
        #####################################
        #Set the values
        for i in range(3):
        
            self.ProcessClass.TargetSelector[i].set(TargetSelector_0[i])
            
            if not TargetSelector_1[i] == '':
            
                self.ProcessClass.TargetSelector_2[i].set(TargetSelector_1[i])
            
            if not TargetSelector_2[i] == '':
            
                self.ProcessClass.TargetSelector_3[i].set(TargetSelector_2[i])

        #run through routines
        for i in range(3):
        
            if not TargetSelector_1[i] == '':
            
                self.ProcessClass.Refresh_First( i, self.ProcessClass.TargetSelector_2[i].get() , delete = False)
            
            if not TargetSelector_2[i] == '':
            
                    self.ProcessClass.Refresh_Second( i, self.ProcessClass.TargetSelector_2[i].get() , delete = False)


        #set entries
        self.ProcessClass.PathEntries[0].delete(0,tk.END)
        self.ProcessClass.PathEntries[0].insert(0,FileName)
        self.ProcessClass.PathEntries[1].delete(0,tk.END)
        self.ProcessClass.PathEntries[1].insert(0,FolderPath)
        self.ProcessClass.PathEntries[2].delete(0,tk.END)
        self.ProcessClass.PathEntries[2].insert(0,BasePath)
        self.SampleClass.Fields[2][0].delete(0,tk.END)
        self.SampleClass.Fields[2][0].insert(0,len(self.Manager.SampleManager.SampleLinks))
        
        #set processing
        self.ProcessClass.ProcessEntries[0].delete(0,tk.END)
        self.ProcessClass.ProcessEntries[0].insert(0,Processors)
        self.ProcessClass.TargetVar.set(WhoMulti)
        self.ProcessClass.TargetFold.set(Fold)
        
        
        for i in range(0,3):

            for j in range(0,3):
        
                self.ProcessClass.ParameterEntries[i][j].delete(0,tk.END)
                
                self.ProcessClass.ParameterEntries[i][j].insert(0,Ranges[i][j])


        self.SampleClass.SetSamples()

    def Tab(self,Num):
        """
        ###########################################################################
        Returns tab
        ###########################################################################
        """
    
        #initialise special characters
        return '    '*Num
    
    def Create(self):
        """
        ###########################################################################
        This create the routine and put all files into the adequat folder.
        This script can then be called and the simulation will run independently...
        ###########################################################################
        """
    
    
        print 'Starting generate Lines'
        
        #set the first line
        Lines   = '#--Simulation File--\n'
        
        ################################
        ################################
        #grap the path of the actual simulation
        
        RunPath = os.path.dirname(sys.argv[0])
        self.Path = os.path.join(RunPath,
                                 'PythonResources',
                                 'RamSim',
                                 'RamanSim.py')
        
        #load the file and read it
        with codecs.open(self.Path) as f:
            
            SimLines = f.readlines()
        
        
        for Element in SimLines:
        
            Lines += Element
        
        ################################
        ################################
        #Set the header
        Lines  += '"""\n'
        Lines  += '###########################################################################\n'
        Lines  += 'This script was generated using the script generator of R-Data. It can run\n'
        Lines  += 'independently of R-Data if the datasctructure is intact...\n'
        Lines  += '###########################################################################\n'
        Lines  += '"""\n'
        Lines  += '\n'
        Lines  += '\n'
        
        ################################
        ################################
        #Set the function
        Lines  += 'def Main():\n'
        Lines  += self.Tab(1) + '\n'
        Lines  += self.Tab(1) + '################################\n'
        Lines  += self.Tab(1) + '################################\n'
        Lines  += self.Tab(1) + '#Proceed to general imports\n'
        Lines  += self.Tab(1) + '#import multiprocessing\n'
        
        
        
        Lines  += self.Tab(1) + '################################\n'
        Lines  += self.Tab(1) + '################################\n'
        Lines  += self.Tab(1) + '#Proceed to loading imports\n'
        Lines  += self.Tab(1) + 'LocalManager = Manager()\n'
        Lines  += self.Tab(1) + '\n'
        
        Lines  += self.Tab(1) + '\n'
        Lines  += self.Tab(1) + '#--LOADHEADER--\n'
        Lines  += self.Tab(1) + '\n'
        
        Lines  += self.Tab(1) + '################################\n'
        Lines  += self.Tab(1) + '################################\n'
        Lines  += self.Tab(1) + '#Set the number of Samples\n'
        Lines  += self.Tab(1) + 'LocalManager.SetSamples('+str(int(self.SampleClass.Fields[2][0].get()))+')\n'
        Lines  += self.Tab(1) + '\n'
        Lines  += self.Tab(1) + '################################\n'
        Lines  += self.Tab(1) + '################################\n'
        Lines  += self.Tab(1) + '#Set the Sample parameters\n'
        
        ################################
        ################################
        #go through the samples and apply the rules
        for i in range(0, len(self.Manager.SampleManager.SampleLinks)):
            
            #ease target
            Target = self.Manager.SampleManager.SampleLinks[i]
            
            Lines  += self.Tab(1) + '\n'
            Lines  += self.Tab(1) + '#Sample: '+str(i)+'\n'
            
            #set the line
            for j in range(0, len(Target.PreferenceList)):
            
                if isinstance(Target.PreferenceList[j][2][Target.PreferenceList[j][1]], basestring):
                
                    #write the change
                    Lines  += self.Tab(1) + 'LocalManager.SampleManager.ChangeParameter('+str(i)+',\''+str(Target.PreferenceList[j][1])+'\',\''+str(Target.PreferenceList[j][2][Target.PreferenceList[j][1]])+'\')\n'
                
                else:
                
                    #write the change
                    Lines  += self.Tab(1) + 'LocalManager.SampleManager.ChangeParameter('+str(i)+',\''+str(Target.PreferenceList[j][1])+'\','+str(Target.PreferenceList[j][2][Target.PreferenceList[j][1]])+')\n'
    
        ################################
        ################################
        #go through the samples and apply the rules
        Lines  += self.Tab(1) + '\n'
        Lines  += self.Tab(1) + '################################\n'
        Lines  += self.Tab(1) + '################################\n'
        Lines  += self.Tab(1) + '#Set the Lens parameters\n'
        
        #set the line
        for j in range(0, len(self.Manager.LensManager.PreferenceList)):
        
            #write the change
            Lines  += self.Tab(1) + 'LocalManager.LensManager.ChangeParameter(\''+str(self.Manager.LensManager.PreferenceList[j][1])+'\','+str(self.Manager.LensManager.PreferenceList[j][2][self.Manager.LensManager.PreferenceList[j][1]])+')\n'
    
        #go through the samples and apply the rules
        for i in range(0, len(self.Manager.LensManager.LensElements)):
            
            #ease target
            Target = self.Manager.LensManager.LensElements[i]
            
            Lines  += self.Tab(1) + '\n'
            Lines  += self.Tab(1) + '#LensElement: '+str(i)+'\n'
            
            #set the line
            for j in range(0, len(Target.PreferenceList)):
            
                #write the change
                Lines  += self.Tab(1) + 'LocalManager.LensManager.LensElements['+str(i)+'].ChangeParameter(\''+str(Target.PreferenceList[j][1])+'\','+str(Target.PreferenceList[j][2][Target.PreferenceList[j][1]])+')\n'
    
        Lines  += self.Tab(1) + '\n'
        Lines  += self.Tab(1) + '#--LOADHEADER--\n'
        Lines  += self.Tab(1) + '\n'
        Lines  += self.Tab(1) + '\n'
        Lines  += self.Tab(1) + '################################\n'
        Lines  += self.Tab(1) + '################################\n'
        Lines  += self.Tab(1) + '#Proceed to File Loading\n'
        Lines  += self.Tab(1) + 'for i in range(0, len(LocalManager.SampleManager.SampleLinks)):\n'
        Lines  += self.Tab(2) + '\n'
        Lines  += self.Tab(2) + '#check if there is a profile to load\n'
        Lines  += self.Tab(2) + 'if LocalManager.SampleManager.SampleLinks[i].ParametersDict[\'RamanProfileLoaded\']:\n'
        Lines  += self.Tab(3) + '\n'
        Lines  += self.Tab(3) + '#Load the profile\n'
        Lines  += self.Tab(3) + 'LocalManager.SampleManager.SampleLinks[i].LoadRamanResponseProfile()\n'
        Lines  += self.Tab(3) + '\n'
        Lines  += self.Tab(2) + '\n'
        Lines  += self.Tab(2) + '#check if there is a profile to load\n'
        Lines  += self.Tab(2) + 'if LocalManager.SampleManager.SampleLinks[i].ParametersDict[\'IndexProfileLoaded\']:\n'
        Lines  += self.Tab(3) + '\n'
        Lines  += self.Tab(3) + '#Load the profile\n'
        Lines  += self.Tab(3) + 'LocalManager.SampleManager.SampleLinks[i].LoadIndexResponseProfile()\n'
        Lines  += self.Tab(3) + '\n'
        Lines  += self.Tab(2) + '\n'
        Lines  += self.Tab(2) + '#check if there is a profile to load\n'
        Lines  += self.Tab(2) + 'if LocalManager.SampleManager.SampleLinks[i].ParametersDict[\'AbsorptionProfileLoaded\']:\n'
        Lines  += self.Tab(3) + '\n'
        Lines  += self.Tab(3) + '#Load the profile\n'
        Lines  += self.Tab(3) + 'LocalManager.SampleManager.SampleLinks[i].LoadAbsorptionResponseProfile()\n'
        Lines  += self.Tab(3) + '\n'
        Lines  += self.Tab(1) + '\n'
        Lines  += self.Tab(1) + '\n'
        Lines  += self.Tab(1) + '################################\n'
        Lines  += self.Tab(1) + '################################\n'
        Lines  += self.Tab(1) + '#Proceed to general printouts\n'
        Lines  += self.Tab(1) + 'print LocalManager.LensManager.LensElements[0]\n'
        Lines  += self.Tab(1) + 'print LocalManager.LensManager.LensElements[1]\n'
        Lines  += self.Tab(1) + 'print LocalManager.LensManager.LensElements[2]\n'
        Lines  += self.Tab(1) + 'print LocalManager.SampleManager\n'
        Lines  += '\n'
        Lines  += '\n'
        Lines  += self.Tab(1) + '#--PROCESS PARAMETERS--\n'
        
        
        ################################
        ################################
        #find and include the path
        
        #set the variables
        Compute = [False]               * len(self.ProcessClass.TargetSelector)
        Targets = [[None for i in range(0,2)] for j in range(0, len(self.ProcessClass.TargetSelector))]
        Ranges  = [[None for i in range(0,3)] for j in range(0, len(self.ProcessClass.TargetSelector))]
        

        #cycle over
        for l in range(0, len(self.ProcessClass.TargetSelector)):
            
            ##############################
            #check if void then we give up
            if self.ProcessClass.TargetSelector[l].get() == 'Void':
            
                pass
            
            elif self.ProcessClass.TargetSelector[l].get() == 'Sample Manager':
            
                #set compute to true
                Compute[l] = True
                
                #set the writtend target
                Targets[l][0] = 'LocalManager.SampleManager.SampleLinks['
                
                #set it to continue investigation
                LowLevelTarget = self.Manager.SampleManager.SampleLinks
            
                for i in range(0, len(LowLevelTarget)):

                    if self.ProcessClass.TargetSelector_2[l].get() == LowLevelTarget[i].ParametersDict['Name']:
                
                        Targets[l][0] += str(i)
                            
                #continue it it
                Targets[l][0] += ']'
                    
                #add second part
                Targets[l][1] = self.ProcessClass.TargetSelector_3[l].get()
            
            elif self.ProcessClass.TargetSelector[l].get() == 'Lens Manager':
            
                #set compute to true
                Compute[l] = True
                
                if self.ProcessClass.TargetSelector_2[l].get() == 'General Lens':
                
                    Targets[l][0] = 'LocalManager.LensManager'
                
                else:
                
                    #set the writtend target
                    Targets[l][0] = 'LocalManager.LensManager.LensElements['
                    
                    #set it to continue investigation
                    LowLevelTarget = self.Manager.LensManager.LensElements
            
                    for i in range(0, len(LowLevelTarget)):

                        if self.ProcessClass.TargetSelector_2[l].get() == LowLevelTarget[i].ParametersDict['Name']:
                    
                            Targets[l][0] += str(i)

                    #continue it it
                    Targets[l][0] += ']'
                        
                #add second part
                Targets[l][1] = self.ProcessClass.TargetSelector_3[l].get()
                            
            
            ##############################
            #grab the ranges
            for i in range(0, len(Ranges)):
                for j in range(0, len(Ranges[i])):
            
                    if self.ProcessClass.ParameterEntries[i][j].get() == '':
                        Ranges[i][j] = '\'\''
                    else:
                        Ranges[i][j] = str(self.ProcessClass.ParameterEntries[i][j].get())

        #esthetical correction of ranges
        for i in range(0,len(Ranges)):
        
            if Ranges[i][2] == '\'\'':
        
                Ranges[i][2] = '1'

        ################################
        ################################
        #write the variable
        
        Array = ['Compute    = [',
                 'Targets    = [',
                 'Parameter  = [',
                 'Ranges     = ['
                 ]
                 
                 
        #Add the values the lines
        for i in range(0, len(Compute)):
        
            #logical text
            if i == 0 :
                Start = ''
            else:
                Start = ','
            
            #add
            Array[0] += Start + str(Compute[i])
            Array[1] += Start + str(Targets[i][0])
            Array[2] += Start + '\'' + str(Targets[i][1]) + '\''
            Array[3] += Start + '['+str(Ranges[i][0]) + ',' + str(Ranges[i][1]) + ',' + str(Ranges[i][2]) + ']'
        
        #close the lines
        for i in range(0, len(Array)):
        
            Array[i] += ']\n'
        
        #wreite the liness
        for i in range(0, len(Array)):
            
            Lines  += self.Tab(1) + Array[i]

        ################################
        ################################
        #Set Dropdown, much easier to reload
        Lines  += self.Tab(1) + 'TargetSelector_0 = ['
        
        for i in range(0, len(self.ProcessClass.TargetSelector)):
        
            #logical text
            if i == 0 :
                Start = ''
            else:
                Start = ','
            
            Lines  += Start + '\'' + self.ProcessClass.TargetSelector[i].get()+ '\''
                
        Lines  += ']\n'
        
        Lines  += self.Tab(1) + 'TargetSelector_1 = ['
        
        for i in range(0, len(self.ProcessClass.TargetSelector_2)):
        
            #logical text
            if i == 0 :
                Start = ''
            else:
                Start = ','
            
            Lines  += Start + '\'' + self.ProcessClass.TargetSelector_2[i].get()+ '\''
                
        Lines  += ']\n'
        
        Lines  += self.Tab(1) + 'TargetSelector_2 = ['
        
        for i in range(0, len(self.ProcessClass.TargetSelector_3)):
        
            #logical text
            if i == 0 :
                Start = ''
            else:
                Start = ','
            
            Lines  += Start + '\'' + self.ProcessClass.TargetSelector_3[i].get()+ '\''
                
        Lines  += ']\n'
        
        ################################
        ################################
        #Drop folder
        Lines  += self.Tab(1) + 'BasePath   = \''+self.ProcessClass.PathEntries[2].get()+'\'\n'
        Lines  += self.Tab(1) + 'Processors = '+self.ProcessClass.ProcessEntries[0].get()+'\n'
        Lines  += self.Tab(1) + 'WhoMulti   = '+str(self.ProcessClass.TargetVar.get())+'\n'
        Lines  += self.Tab(1) + 'Fold       = '+str(self.ProcessClass.TargetFold.get())+'\n'
        Lines  += self.Tab(1) + '#--PROCESS PARAMETERS--\n'
        
        ################################
        ################################
        #generate output path
        
        Path  = 'OUTPUT_'
        Path += str(30)

        if Compute[0]:

            Path += '__'+str(Targets[0][1].split('->')[1])+'__'

            Path += 'X-0-X'
        
        if Compute[1]:

            Path += '__'+str(Targets[1][1].split('->')[1])+'__'

            Path += 'X-1-X'

        Path += '__'+str(Targets[2][1]).split('->')[1]+'__'
        Path += 'X-2-X.txt'

        Lines  += self.Tab(1) + '\n'
        Lines  += self.Tab(1) + '################################\n'
        Lines  += self.Tab(1) + '################################\n'
        Lines  += self.Tab(1) + '#Write path\n'
        Lines  += self.Tab(1) + 'Path = \''+Path+'\'\n'
        Lines  += self.Tab(1) + '\n'
        
        ################################
        ################################
        #Create the for loops
        
        
        Lines  += self.Tab(1) + 'Parameters = [Compute, Targets, Parameter, Ranges, [ProcessLoop_1,ProcessLoop_2,ProcessLoop_3], Path, BasePath, Processors, WhoMulti, Fold,LocalManager]\n'
        
        Lines  += self.Tab(1) + 'LocalManager.SampleManager.CreateCubes()\n'
        
        Lines  += self.Tab(1) + '\n'
        Lines  += self.Tab(1) + '################################\n'
        Lines  += self.Tab(1) + '################################\n'
        Lines  += self.Tab(1) + '#The dependencies should build themeselves\n'
        Lines  += self.Tab(1) + 'Parameters[4][0](Parameters, 0)\n'

        
        '''
        ################################
        FUNCTION 1
        ################################
        '''
        ################################
        ################################
        #set the loops
        Lines  += '"""\n'
        Lines  += '###########################################################################\n'
        Lines  += 'This script was generated using the script generator of R-Data. It can run\n'
        Lines  += 'independently of R-Data if the datasctructure is intact...\n'
        Lines  += '###########################################################################\n'
        Lines  += '"""\n'
        Lines  += 'def ProcessLoop_1(Parameters, Index, Multi = False):\n'
        
        ################################
        ################################
        #set parameters
        Lines  += self.Tab(1) + '################################\n'
        Lines  += self.Tab(1) + '################################\n'
        Lines  += self.Tab(1) + '#unpack the variables\n'
        Lines  += self.Tab(1) + 'Compute        = list(Parameters[0])\n'
        Lines  += self.Tab(1) + 'Targets        = list(Parameters[1])\n'
        Lines  += self.Tab(1) + 'Parameter      = list(Parameters[2])\n'
        Lines  += self.Tab(1) + 'Ranges         = list(Parameters[3])\n'
        Lines  += self.Tab(1) + 'TargetRoutine  = list(Parameters[4])\n'
        Lines  += self.Tab(1) + 'Path           = str(Parameters[5])\n'
        Lines  += self.Tab(1) + 'BasePath       = str(Parameters[6])\n'
        Lines  += self.Tab(1) + 'Processors     = int(Parameters[7])\n'
        Lines  += self.Tab(1) + 'WhoisMulti     = int(Parameters[8])\n'
        Lines  += self.Tab(1) + 'Fold           = Parameters[9]\n'
        Lines  += self.Tab(1) + 'LocalManager   = Parameters[10]\n'
        Lines  += self.Tab(2) + '\n'
        
        ################################
        ################################
        #set loop
        Lines  += self.Tab(1) + '################################\n'
        Lines  += self.Tab(1) + '################################\n'
        Lines  += self.Tab(1) + '#First variable loop\n'
        Lines  += self.Tab(1) + 'for i in range(0,Ranges[Index][2]):\n'
        Lines  += self.Tab(2) + '\n'
        Lines  += self.Tab(2) + 'if Compute[Index]:\n'
        Lines  += self.Tab(3) + '\n'
        Lines  += self.Tab(3) + 'Targets[Index].ChangeParameter(Parameter[Index].split(\'->\')[1], Ranges[Index][0]+((Ranges[Index][1] - Ranges[Index][0])/Ranges[Index][2] * i))\n'
        Lines  += self.Tab(3) + '\n'
        Lines  += self.Tab(2) + 'else:\n'
        Lines  += self.Tab(3) + '\n'
        Lines  += self.Tab(3) + 'pass\n'
        Lines  += self.Tab(2) + '\n'
        
        ################################
        ################################
        #Run the function
        Lines  += self.Tab(2) + '#Run the next routine\n'
        Lines  += self.Tab(2) + 'TargetRoutine[Index + 1](Parameters, Index + 1)\n'
        
        '''
        ################################
        FUNCTION 2
        ################################
        '''
        ################################
        ################################
        #Run Function
        Lines  += '"""\n'
        Lines  += '###########################################################################\n'
        Lines  += 'This script was generated using the script generator of R-Data. It can run\n'
        Lines  += 'independently of R-Data if the datasctructure is intact...\n'
        Lines  += '###########################################################################\n'
        Lines  += '"""\n'
        Lines  += 'def ProcessLoop_2(Parameters, Index, Multi = False):\n'
        
        ################################
        ################################
        #set parameters
        Lines  += self.Tab(1) + '################################\n'
        Lines  += self.Tab(1) + '################################\n'
        Lines  += self.Tab(1) + '#unpack the variables\n'
        Lines  += self.Tab(1) + 'Compute        = list(Parameters[0])\n'
        Lines  += self.Tab(1) + 'Targets        = list(Parameters[1])\n'
        Lines  += self.Tab(1) + 'Parameter      = list(Parameters[2])\n'
        Lines  += self.Tab(1) + 'Ranges         = list(Parameters[3])\n'
        Lines  += self.Tab(1) + 'TargetRoutine  = list(Parameters[4])\n'
        Lines  += self.Tab(1) + 'Path           = str(Parameters[5])\n'
        Lines  += self.Tab(1) + 'BasePath       = str(Parameters[6])\n'
        Lines  += self.Tab(1) + 'Processors     = int(Parameters[7])\n'
        Lines  += self.Tab(1) + 'WhoisMulti     = int(Parameters[8])\n'
        Lines  += self.Tab(1) + 'Fold           = Parameters[9]\n'
        Lines  += self.Tab(1) + 'LocalManager   = Parameters[10]\n'
        Lines  += self.Tab(2) + '\n'
        
        ################################
        ################################
        #set loop for single Processes
        Lines  += self.Tab(1) + '################################\n'
        Lines  += self.Tab(1) + '################################\n'
        Lines  += self.Tab(1) + '#Second variable loop\n'
        Lines  += self.Tab(1) + '\n'
        
        #---------------#
        #---------------#
        #Multi processor
        Lines  += self.Tab(1) + '#Multi processor\n'
        Lines  += self.Tab(1) + 'if WhoisMulti == 1 and Processors > 1:\n'
        Lines  += self.Tab(2) + '\n'
        Lines  += self.Tab(2) + '#Set the multiprocessing queue\n'
        Lines  += self.Tab(2) + 'output = multiprocessing.Manager().Queue()\n'
        
        Lines  += self.Tab(2) + '\n'
        Lines  += self.Tab(2) + '#Set the multiprocessing Loop\n'
        Lines  += self.Tab(2) + 'i = 0\n'
        Lines  += self.Tab(2) + 'while i <  Ranges[Index][2]:\n'
        
        Lines  += self.Tab(3) + '\n'
        Lines  += self.Tab(3) + '#Set the multiprocessing Array\n'
        Lines  += self.Tab(3) + 'Processes = []\n'
        
        #---------------#
        #Set the overshoot
        Lines  += self.Tab(3) + '\n'
        Lines  += self.Tab(3) + '#Set overshoot condition\n'
        Lines  += self.Tab(3) + 'if i + Processors > Ranges[Index][2]:\n'
            
        Lines  += self.Tab(4) + '\n'
        Lines  += self.Tab(4) + '#Append processe\n'
        Lines  += self.Tab(4) + 'for k in range(i, Ranges[Index][2]):\n'
    
        Lines  += self.Tab(5) + '\n'
        Lines  += self.Tab(5) + 'if Compute[Index]:\n'
        Lines  += self.Tab(6) + '\n'
        Lines  += self.Tab(6) + '#change the value\n'
        Lines  += self.Tab(6) + 'Targets[Index].ChangeParameter(Parameter[Index].split(\'->\')[1], Ranges[Index][0]+((Ranges[Index][1] - Ranges[Index][0])/Ranges[Index][2] * i))\n'
        Lines  += self.Tab(6) + '#set the processor\n'
        Lines  += self.Tab(6) + 'Processes.append(multiprocessing.Process(target=TargetRoutine[Index + 1],args=(Parameters, Index + 1, True, output)))\n'
        Lines  += self.Tab(6) + 'Processes[-1].start()\n'
        Lines  += self.Tab(6) + 'i += 1\n'
        
        #---------------#
        #Set Normal
        Lines  += self.Tab(3) + '\n'
        Lines  += self.Tab(3) + '#Set normal condition\n'
        Lines  += self.Tab(3) + 'else:\n'
            
        Lines  += self.Tab(4) + '\n'
        Lines  += self.Tab(4) + '#Append processe\n'
        Lines  += self.Tab(4) + 'for k in range(i, i + Processors):\n'
    
        Lines  += self.Tab(5) + '\n'
        Lines  += self.Tab(5) + 'if Compute[Index]:\n'
        Lines  += self.Tab(6) + '\n'
        Lines  += self.Tab(6) + '#change the value\n'
        Lines  += self.Tab(6) + 'Targets[Index].ChangeParameter(Parameter[Index].split(\'->\')[1], Ranges[Index][0]+((Ranges[Index][1] - Ranges[Index][0])/Ranges[Index][2] * i))\n'
        Lines  += self.Tab(6) + '#set the processor\n'
        Lines  += self.Tab(6) + 'Processes.append(multiprocessing.Process(target=TargetRoutine[Index + 1],args=(Parameters, Index + 1, True, output)))\n'
        Lines  += self.Tab(6) + 'Processes[-1].start()\n'
        Lines  += self.Tab(6) + 'i += 1\n'
        
        #---------------#
        #Set Gathering
        Lines  += self.Tab(3) + '\n'
        Lines  += self.Tab(3) + '#Set joining loop\n'
        Lines  += self.Tab(3) + 'for p in Processes:\n'
        
        Lines  += self.Tab(4) + '\n'
        Lines  += self.Tab(4) + '#join processes\n'
        Lines  += self.Tab(4) + 'p.join()\n'

        Lines  += self.Tab(3) + '\n'
        Lines  += self.Tab(3) + '#grab output\n'
        Lines  += self.Tab(3) + 'OutArray = [output.get() for p in Processes] \n'
        
        
        Lines  += self.Tab(3) + '\n'
        Lines  += self.Tab(3) + '#Write loop\n'
        Lines  += self.Tab(3) + 'for t in range(0,len(OutArray)):\n'
        Lines  += self.Tab(4) + '\n'
        Lines  += self.Tab(4) + '#proceed to the routine\n'
        Lines  += self.Tab(4) + 'Array = OutArray[t][0]\n'
        Lines  += self.Tab(4) + '\n'
        Lines  += self.Tab(4) + '#Path processing\n'
        Lines  += self.Tab(4) + 'NewPath = str(Path)\n'
        Lines  += self.Tab(4) + '\n'
        Lines  += self.Tab(4) + 'if Compute[0]:\n'
        Lines  += self.Tab(5) + '\n'
        Lines  += self.Tab(5) + 'NewPath = NewPath.replace(\'X-0-X\',str(Targets[0].ParametersDict[Parameter[0].split(\'->\')[1]]))\n'
        Lines  += self.Tab(5) + '\n'
        Lines  += self.Tab(5) + '\n'
        Lines  += self.Tab(4) + 'if Compute[1]:\n'
        Lines  += self.Tab(5) + '\n'
        Lines  += self.Tab(5) + 'NewPath = NewPath.replace(\'X-1-X\',str(OutArray[t][1]))\n'
        Lines  += self.Tab(4) + '\n'
        Lines  += self.Tab(4) + '################################\n'
        Lines  += self.Tab(4) + '#Save it\n'
        Lines  += self.Tab(4) + 'numpy.savetxt(os.path.join(BasePath,NewPath),Array)\n'
        Lines  += self.Tab(4) + '\n'
        Lines  += self.Tab(4) + '\n'

        #---------------#
        #---------------#
        #single processor
        Lines  += self.Tab(1) + '#Single processor\n'
        Lines  += self.Tab(1) + 'else:\n'
        Lines  += self.Tab(2) + 'for i in range(0,Ranges[Index][2]):\n'
        Lines  += self.Tab(3) + '\n'
        Lines  += self.Tab(3) + 'if Compute[Index]:\n'
        Lines  += self.Tab(4) + '\n'
        Lines  += self.Tab(4) + 'Targets[Index].ChangeParameter(Parameter[Index].split(\'->\')[1], Ranges[Index][0]+((Ranges[Index][1] - Ranges[Index][0])/Ranges[Index][2] * i))\n'
        Lines  += self.Tab(4) + '\n'
        Lines  += self.Tab(3) + 'else:\n'
        Lines  += self.Tab(4) + '\n'
        Lines  += self.Tab(4) + 'pass\n'
        Lines  += self.Tab(4) + '\n'
        
        
        
        ################################
        ################################
        #Run the function
        Lines  += self.Tab(2) + '#Run the next routine\n'
        Lines  += self.Tab(2) + 'Array = TargetRoutine[Index + 1](Parameters, Index + 1)\n'
        Lines  += self.Tab(2) + '\n'
        

        ################################
        ################################
        #Write the files
        Lines  += self.Tab(1) + '################################\n'
        Lines  += self.Tab(1) + '#Path processing\n'
        Lines  += self.Tab(1) + 'NewPath = str(Path)\n'
        Lines  += self.Tab(1) + '\n'
        Lines  += self.Tab(1) + 'if Compute[0]:\n'
        Lines  += self.Tab(2) + '\n'
        Lines  += self.Tab(2) + 'NewPath = NewPath.replace(\'X-0-X\',str(Targets[0].ParametersDict[Parameter[0].split(\'->\')[1]]))\n'
        Lines  += self.Tab(1) + '\n'
        Lines  += self.Tab(1) + '\n'
        Lines  += self.Tab(1) + 'if Compute[1]:\n'
        Lines  += self.Tab(2) + '\n'
        Lines  += self.Tab(2) + 'NewPath = NewPath.replace(\'X-1-X\',str(Targets[1].ParametersDict[Parameter[1].split(\'->\')[1]]))\n'

        Lines  += self.Tab(1) + '\n'
        Lines  += self.Tab(1) + '################################\n'
        Lines  += self.Tab(1) + '#Save it\n'
        Lines  += self.Tab(1) + 'numpy.savetxt(os.path.join(BasePath,NewPath),Array)\n'
        Lines  += self.Tab(1) + '\n'
        Lines  += self.Tab(1) + '\n'
  
        '''
        ################################
        FUNCTION 3
        ################################
        '''
        ################################
        ################################
        #Run Function
        Lines  += '"""\n'
        Lines  += '###########################################################################\n'
        Lines  += 'This script was generated using the script generator of R-Data. It can run\n'
        Lines  += 'independently of R-Data if the datasctructure is intact...\n'
        Lines  += '###########################################################################\n'
        Lines  += '"""\n'
        Lines  += 'def ProcessLoop_3(Parameters, Index, Multi = False, Queue = None):\n'
        
        #set parameters
        Lines  += self.Tab(1) + '################################\n'
        Lines  += self.Tab(1) + '################################\n'
        Lines  += self.Tab(1) + '#unpack the variables\n'
        Lines  += self.Tab(1) + 'Compute        = list(Parameters[0])\n'
        Lines  += self.Tab(1) + 'Targets        = list(Parameters[1])\n'
        Lines  += self.Tab(1) + 'Parameter      = list(Parameters[2])\n'
        Lines  += self.Tab(1) + 'Ranges         = list(Parameters[3])\n'
        Lines  += self.Tab(1) + 'TargetRoutine  = list(Parameters[4])\n'
        Lines  += self.Tab(1) + 'Path           = str(Parameters[5])\n'
        Lines  += self.Tab(1) + 'BasePath       = str(Parameters[6])\n'
        Lines  += self.Tab(1) + 'Processors     = int(Parameters[7])\n'
        Lines  += self.Tab(1) + 'WhoisMulti     = int(Parameters[8])\n'
        Lines  += self.Tab(1) + 'Fold           = Parameters[9]\n'
        Lines  += self.Tab(1) + 'LocalManager   = Parameters[10]\n'
        Lines  += self.Tab(2) + '\n'

        ################################
        ################################
        #set loop
        Lines  += self.Tab(1) + '################################\n'
        Lines  += self.Tab(1) + '################################\n'
        Lines  += self.Tab(1) + '#Third variable loop\n'
        
        Lines  += self.Tab(1) + '\n'
        Lines  += self.Tab(1) + '#set the variable\n'
        
        Lines  += self.Tab(1) + 'if Fold == 1:\n'
        Lines  += self.Tab(2) + 'Array = numpy.zeros((Ranges[Index][2],2))\n'
        Lines  += self.Tab(2) + '\n'
        
        Lines  += self.Tab(1) + 'else:\n'
        Lines  += self.Tab(2) + 'Array = numpy.zeros((Ranges[Index][2],len(LocalManager.SampleManager.SampleLinks) + 1))\n'
        Lines  += self.Tab(2) + '\n'
        
        Lines  += self.Tab(1) + 'for k in range(0,Ranges[Index][2]):\n'
        Lines  += self.Tab(1) + '\n'

        ################################
        ################################
        #Actual computation
        Lines  += self.Tab(2) + '################################\n'
        Lines  += self.Tab(2) + '#Process simulation\n'

        Lines  += self.Tab(2) + 'Targets[Index].ChangeParameter(Parameter[Index].split(\'->\')[1], Ranges[Index][0]+((Ranges[Index][1] - Ranges[Index][0])/Ranges[Index][2] * k))\n'
    
    
        Lines  += self.Tab(2) + 'LocalManager.RunIllumination()\n'
        Lines  += self.Tab(2) + 'LocalManager.SampleManager.CorrectCubes()\n'
        Lines  += self.Tab(2) + 'LocalManager.SampleManager.ResetCollectionIntensities()\n'
        Lines  += self.Tab(2) + 'LocalManager.SampleManager.CollectedIntensity()\n'
        Lines  += self.Tab(2) + '\n'

        ################################
        ################################
        #Process Output
        Lines  += self.Tab(2) + '################################\n'
        Lines  += self.Tab(2) + '#Process Output\n'
        Lines  += self.Tab(2) + 'if Parameter[2].split(\'->\')[1] == \'LambdaOut\':\n'
        Lines  += self.Tab(3) + '\n'
        Lines  += self.Tab(3) + 'Array[k][0]  = (  1. / (LocalManager.LensManager.ParametersDict[\'LambdaIn\'] *100.)-1. / (LocalManager.LensManager.ParametersDict[\'LambdaOut\'] *100.)) \n'
        Lines  += self.Tab(3) + '\n'
        Lines  += self.Tab(2) + 'else:\n'
        Lines  += self.Tab(3) + '\n'
        Lines  += self.Tab(3) + 'Array[k][0]  = Targets[2].ParametersDict[Parameter[2].split(\'->\')[1]]\n'
        Lines  += self.Tab(3) + '\n'
        Lines  += self.Tab(2) + '################################\n'
        Lines  += self.Tab(2) + '#Process Intensities\n'
        Lines  += self.Tab(2) + 'for Intensity in LocalManager.SampleManager.Intensity:\n'
        Lines  += self.Tab(3) + '\n'
        Lines  += self.Tab(3) + 'if Fold == 1:\n'
        Lines  += self.Tab(4) + 'Array[k][1] += Intensity\n'
        Lines  += self.Tab(4) + '\n'
        
        Lines  += self.Tab(3) + 'else:\n'
        Lines  += self.Tab(4) + 'for ii in range(0, len(LocalManager.SampleManager.SampleLinks)):\n'
        Lines  += self.Tab(5) + 'Array[k][ii + 1] = Intensity[ii]\n'
        Lines  += self.Tab(5) + '\n'

        ################################
        ################################
        #Some visual
        Lines  += self.Tab(2) + '################################\n'
        Lines  += self.Tab(2) + '#Process some verbose\n'
        Lines  += self.Tab(2) + 'print \'######################################################\'\n'
        Lines  += self.Tab(2) + 'print \'######################################################\'\n'
        Lines  += self.Tab(2) + 'print \'Current Depth: \',LocalManager.LensManager.ParametersDict[\'FocalPosition\'],\' m\'\n'
        Lines  += self.Tab(2) + 'print \'Current Wavenumber: \',Array[k][0], \' cm-1\'\n'
        Lines  += self.Tab(2) + 'print \'Current IntensityFactors: \',LocalManager.SampleManager.RetrieveFact()\n'
        Lines  += self.Tab(2) + 'print \'Current Intensity: \',LocalManager.SampleManager.Intensity\n'
        Lines  += self.Tab(2) + '\n'
        
        Lines  += self.Tab(1) + '#if we are multi process:\n'
        Lines  += self.Tab(1) + 'if Multi:\n'
        Lines  += self.Tab(2) + 'Queue.put([Array,Targets[Index-1].ParametersDict[Parameter[Index-1].split(\'->\')[1]] ])\n'
        Lines  += self.Tab(2) + '\n'
        Lines  += self.Tab(1) + 'else:\n'
        Lines  += self.Tab(2) + 'return Array\n'

        Lines  += '\n'
        Lines  += '\n'
        Lines  += '\n'
        Lines  += '\n'
        Lines  += '\n'

        ################################
        ################################
        #closing it
        Lines  += 'if __name__ == "__main__":\n'
        Lines  += self.Tab(1) + 'Main()\n'
        Lines  += '\n'
        Lines  += '\n'

        
        
        print 'Starting to generate script'
    
        #open the file as write
        SimScript = codecs.open(os.path.join(self.ProcessClass.PathEntries[1].get(),
                                            self.ProcessClass.PathEntries[0].get())
                               ,'w'
                               , 'utf-8')
    
        #addlines
        SimScript.writelines(Lines)
    
        #close the file
        SimScript.close()
    
    
    def InitialiseFrames(self):
        """
        ###########################################################################
        This create the routine and put all files into the adequat folder.
        This script can then be called and the simulation will run independently...
        ###########################################################################
        """
        
        ###########################
        #initialise manager
        self.Manager = Manager()
        
        ###########################
        #Set the clases first
        self.SampleClass    = SampleParameterFrame(self.master,
                                                   self.Manager)
                                                   
        self.RamanClass     = RamanParameterFrame(self.master,
                                                  self.Manager)
                                                  
        self.ProcessClass   = ProcessParameterFrame(self.master,
                                                    self.Manager)
        
        ###########################
        #Set the clases first
        self.SampleFrame    = self.SampleClass.GrabFrame()
        self.RamanFrame     = self.RamanClass.GrabFrame()
        self.ProcessFrame   = self.ProcessClass.GrabFrame()


class SampleParameterFrame():
    
    '''
    ####################################################################################
    In an effort to unify the import window into one single class we will extract
    the frames of three provious windows and populate them here into a notebook...
    
    
    ####################################################################################
    '''
    
    def __init__(self,master,Manager):
        
        
        ######################################
        #link the DataClass
        self.Padding      = '10p'
        self.Manager      = Manager
        
        #set master
        self.master = master
    
        #create the main frame
        self.MainFrame = ttk.Frame(master,padding = self.Padding)
    
        #send out the general populator
        self.GeneralPopulate()
    
    def GrabFrame(self):

        '''
        ############################################
        This element will dispatch the various frme 
        populators and the place hte frame in
        the current loded frame network
        ############################################
        '''
    
        return self.MainFrame


    def GeneralPopulate(self):

        '''
        ############################################
        This element will dispatch the various frme 
        populators and the place hte frame in
        the current loded frame network
        ############################################
        '''
            
        #set the variables
        self.Frames = []
        self.Fields = []
        
        #initiate variables
        self.GenerateText()

        #send out the methods
        self.Frames.append([self.TextFrameCreator(),
                            0,
                            0,
                            1,
                            3,
                            tk.E+tk.W])
                            
                            
        self.Frames.append([ttk.Separator(self.MainFrame,
                                          orient = tk.HORIZONTAL),
                            1,
                            0,
                            1,
                            3,
                            tk.E+tk.W])


        self.Frames.append([self.SampleNumFrameCreator(),
                            2,
                            0,
                            1,
                            3,
                            tk.E+tk.W])
                            
        self.Frames.append([ttk.Separator(self.MainFrame,
                                          orient = tk.HORIZONTAL),
                            3,
                            0,
                            1,
                            3,
                            tk.E+tk.W])
                            
        self.Placeholder = ttk.Frame(self.MainFrame)
        
        self.Frames.append([self.Placeholder,
                            4,
                            0,
                            1,
                            3,
                            tk.E+tk.W])
                            
        #call the placer
        self.GeneralPlacer()

    def GeneralPlacer(self):
        '''
        ############################################
        This will run through self.Fields and 
        self.Frames and place all of them onto the 
        grid...
        ############################################
        '''

        #cycle through fields
        for Element in self.Fields:

            #place it
            Element[0].grid(row         = Element[1],
                            column      = Element[2],
                            rowspan     = Element[3],
                            columnspan  = Element[4],
                            sticky      = Element[5])


        #cycle through fields
        for Element in self.Frames:

            #place it
            Element[0].grid(row         = Element[1],
                            column      = Element[2],
                            rowspan     = Element[3],
                            columnspan  = Element[4],
                            sticky      = Element[5])

    def TextFrameCreator(self):
        '''
        ############################################
        This will create the initial label frame 
        with the explanations
        ############################################
        '''

        #create the frame
        self.TextFrame = ttk.Frame(self.MainFrame,
                                   padding = self.Padding)

        #load the text label
        self.Fields.append([ttk.Label(self.TextFrame,
                                      text = self.LabelText[0],
                                      wraplength = 400),
                            0,
                            0,
                            1,
                            1,
                            tk.E+tk.W])

        return self.TextFrame
    
    
    def SampleNumFrameCreator(self):
        '''
        ############################################
        This will create the initial label frame 
        with the explanations
        ############################################
        '''

        #create the frame
        self.SampleNumFrame = ttk.Frame(self.MainFrame,
                                        padding = self.Padding)

        #load the text label
        self.Fields.append([ttk.Label(self.SampleNumFrame,
                                      text = self.LabelText[1],
                                      wraplength = 300),
                            0,
                            0,
                            2,
                            1,
                            tk.E+tk.W])
                            
        self.Fields.append([ttk.Entry(self.SampleNumFrame,
                                      width = 5),
                            0,
                            1,
                            1,
                            1,
                            tk.E+tk.W])
                            
                            
        self.Fields.append([ttk.Button(self.SampleNumFrame,
                                       text = 'Set',
                                       comman = self.SetSampleNumber),
                            1,
                            1,
                            1,
                            1,
                            tk.E+tk.W])

        return self.SampleNumFrame

    def GenerateText(self):
        '''
        ############################################
        This will create the initial label frame 
        with the explanations
        ############################################
        '''

        self.LabelText = []

        self.LabelText.append(  'This is the Sample frame and intended to '
                              + 'set the parameters for the Samples. This allows '
                              + 'for setting the number of samples and their order. '
                              + 'Use the + buttons for more options')
                              
        self.LabelText.append(  'Please enter the number of samples. These will be '
                              + 'placed into the sample Manager and can be rearanged later ...')
    
        self.LabelText.append(  'Here are listed the samples and their name and order. '
                              + 'To rearange the order please enter the number and send submit. '
                              + 'T edit more specific information hit More Options.')


    def SetSampleNumber(self, Num = None):
    
        '''
        ############################################
        This function will call the manager and ask
        him to et sample
        ############################################
        '''
                
        ###############################
        #send out the manager
        
        if Num == None:
        
            self.Manager.SetSamples(int(self.Fields[2][0].get()))
        
        else:
        
            self.Manager.SetSamples(int(Num))
        
        #print the result
        print self.Manager.SampleManager
    
        #call visual obviously
        self.SetSamples()


    def SetSamples(self):
        '''
        ############################################
        This function will do the visual part of the
        sampke interface and allow for it to be 
        called from toplevel elements
        ############################################
        '''

        #try to destroy the sampleFrame
        try:

            self.SampleInfoFrame.destroy()

        except:

            pass

        ###############################
        #recretate the frame
        self.SampleInfoFrame = ttk.Frame(self.Placeholder,
                                         padding = self.Padding)


        ###############################
        #populate it
        self.OrderEntries  = []
        self.SampleLabels  = []
        self.SampleButtons = []
        
        #cycle over the samples
        for i in range(0, len(self.Manager.SampleManager.SampleLinks)):

            #------------------------------#
            #enter the order entry
            self.OrderEntries.append([ttk.Entry(self.SampleInfoFrame,
                                                width = 5),
                                      i,
                                      0,
                                      1,
                                      1,
                                      tk.E+tk.W])
                                      
                                      
            self.OrderEntries[-1][0].insert(0,str(i))

            #------------------------------#
            #enter the order entry
            self.SampleLabels.append([ttk.Label(self.SampleInfoFrame,
                                                text = self.Manager.SampleManager.SampleLinks[i].ParametersDict['Name']),
                                      i,
                                      1,
                                      1,
                                      1,
                                      tk.E+tk.W])

            #------------------------------#
            #enter the order entry
            self.SampleButtons.append([ttk.Button(self.SampleInfoFrame,
                                                  text = 'More Options',
                                                  command = partial(self.CallPrefWindow,i)),
                                      i,
                                      4,
                                      1,
                                      1,
                                      tk.E+tk.W])

        ###############################
        #grid it
        for ElementList in [self.OrderEntries,self.SampleLabels,self.SampleButtons]:

            #cycle through fields
            for Element in ElementList:

                #place it
                Element[0].grid(row         = Element[1],
                                column      = Element[2],
                                rowspan     = Element[3],
                                columnspan  = Element[4],
                                sticky      = Element[5])


        #grid the frame
        self.SampleInfoFrame.grid(row = 0, column = 0, sticky = tk.E+tk.W)


    def CallPrefWindow(self,Num):
        '''
        ############################################
        This function will call the manager and ask
        him to et sample
        ############################################
        '''
        #prompt the user what to do:
        self.ActionWindow = tk.Toplevel(self.master)
        
        #lanuch the window class dependency
        self.ActionWindow = ParameterFrame(self.ActionWindow,
                                           self.Manager.SampleManager.SampleLinks[Num],
                                           self,
                                           Window = True,
                                           SubmitMethod =  self.SetSamples)

class RamanParameterFrame():
    
    '''
    ####################################################################################
    In an effort to unify the import window into one single class we will extract
    the frames of three provious windows and populate them here into a notebook...
    
    
    ####################################################################################
    '''
    
    def __init__(self,master,Manager):
        
        
        ######################################
        #link the DataClass
        self.Padding      = '10p'
        self.Manager      = Manager
        
        #set master
        self.master = master
    
        #create the main frame
        self.MainFrame = ttk.Frame(master,
                                   padding = self.Padding)
    
    
        #send out the general populator
        self.GeneralPopulate()
    

    def GrabFrame(self):

        '''
        ############################################
        This element will dispatch the various frme 
        populators and the place hte frame in
        the current loded frame network
        ############################################
        '''
    
        return self.MainFrame


    def GeneralPopulate(self):

        '''
        ############################################
        This element will dispatch the various frme 
        populators and the place hte frame in
        the current loded frame network
        ############################################
        '''
            
        #set the variables
        self.Frames = []
        self.Fields = []
        
        #initiate variables
        self.GenerateText()

        #send out the methods
        self.Frames.append([self.TextFrameCreator(),
                            0,
                            0,
                            1,
                            3,
                            tk.E+tk.W])
                            
        self.Frames.append([ttk.Separator(self.MainFrame,
                                          orient = tk.HORIZONTAL),
                            1,
                            0,
                            1,
                            3,
                            tk.E+tk.W])

        self.Frames.append([self.RamanInfoCreator(),
                            2,
                            0,
                            1,
                            3,
                            tk.E+tk.W])
                            
        self.Frames.append([ttk.Separator(self.MainFrame,
                                          orient = tk.HORIZONTAL),
                            3,
                            0,
                            1,
                            3,
                            tk.E+tk.W])

        self.Frames.append([self.SelectorFrameCreator(),
                            4,
                            0,
                            1,
                            3,
                            tk.E+tk.W])


        #call the placer
        self.GeneralPlacer()

    def GeneralPlacer(self):
        '''
        ############################################
        This will run through self.Fields and 
        self.Frames and place all of them onto the 
        grid...
        ############################################
        '''

        #cycle through fields
        for Element in self.Fields:

            #place it
            Element[0].grid(row         = Element[1],
                            column      = Element[2],
                            rowspan     = Element[3],
                            columnspan  = Element[4],
                            sticky      = Element[5])


        #cycle through fields
        for Element in self.Frames:

            #place it
            Element[0].grid(row         = Element[1],
                            column      = Element[2],
                            rowspan     = Element[3],
                            columnspan  = Element[4],
                            sticky      = Element[5])

    def SelectorFrameCreator(self):
        '''
        ############################################
        This will create the initial label frame 
        with the explanations
        ############################################
        '''

        ###############################
        #recretate the frame
        self.RamanInfoFrame = ttk.Frame(self.MainFrame,
                                         padding = self.Padding)


        ###############################
        #populate it
        self.OrderEntries   = []
        self.RamanLabels    = []
        self.RamanButtons   = []

        #cycle over the samples
        for i in range(0, len(self.Manager.LensManager.LensElements)):

            #------------------------------#
            #enter the order entry
            self.OrderEntries.append([ttk.Entry(self.RamanInfoFrame,
                                                width = 5),
                                      i,
                                      0,
                                      1,
                                      1,
                                      tk.E+tk.W])
                                      
                                      
            self.OrderEntries[-1][0].insert(0,str(i))

            #------------------------------#
            #enter the order entry
            self.RamanLabels.append([ttk.Label(self.RamanInfoFrame,
                                                text = self.Manager.LensManager.LensElements[i].ParametersDict['Name']),
                                      i,
                                      1,
                                      1,
                                      1,
                                      tk.E+tk.W])

            #------------------------------#
            #enter the order entry
            self.RamanButtons.append([ttk.Button(self.RamanInfoFrame,
                                                  text = 'More Options',
                                                  command = partial(self.CallPrefWindow,i)),
                                      i,
                                      4,
                                      1,
                                      1,
                                      tk.E+tk.W])

        ###############################
        #grid it
        for ElementList in [self.OrderEntries,self.RamanLabels,self.RamanButtons]:

            #cycle through fields
            for Element in ElementList:

                #place it
                Element[0].grid(row         = Element[1],
                                column      = Element[2],
                                rowspan     = Element[3],
                                columnspan  = Element[4],
                                sticky      = Element[5])


        return self.RamanInfoFrame
    
    
    def TextFrameCreator(self):
        '''
        ############################################
        This will create the initial label frame 
        with the explanations
        ############################################
        '''

        #create the frame
        self.TextFrame = ttk.Frame(self.MainFrame,
                                   padding = self.Padding)

        #load the text label
        self.Fields.append([ttk.Label(self.TextFrame,
                                      text = self.LabelText[0],
                                      wraplength = 400),
                            0,
                            0,
                            1,
                            1,
                            tk.E+tk.W])

        return self.TextFrame


    def RamanInfoCreator(self):
        '''
        ############################################
        This will create the initial label frame 
        with the explanations
        ############################################
        '''

        #create the frame
        self.InfoFrame = ttk.Frame(self.MainFrame,
                                   padding = self.Padding)

        #process parameters
        self.ParametrLink = ParameterFrame(self.InfoFrame,
                                           self.Manager.LensManager,
                                           self)

        #return it
        return self.InfoFrame
    
    def CallPrefWindow(self,Num):
        '''
        ############################################
        This function will call the manager and ask
        him to et sample
        ############################################
        '''
        #prompt the user what to do:
        self.ActionWindow = tk.Toplevel(self.master)
        
        #lanuch the window class dependency
        self.ActionWindow = ParameterFrame(self.ActionWindow,
                                           self.Manager.LensManager.LensElements[Num],
                                           self,
                                           Window = True)
    def GenerateText(self):
        '''
        ############################################
        This will create the initial label frame 
        with the explanations
        ############################################
        '''

        self.LabelText = []

        self.LabelText.append(  'This is the Raman setting frame and intended to '
                              + 'set the parameters for the Raman aparatus such as '
                              + 'the wavelength or the interfocal distances. '
                              + 'The values ar enot crosschecked and should make sense')

class ProcessParameterFrame():
    
    '''
    ####################################################################################
    In an effort to unify the import window into one single class we will extract
    the frames of three provious windows and populate them here into a notebook...
    
    
    ####################################################################################
    '''
    
    def __init__(self,master,Manager):
        
        
        ######################################
        #link the DataClass
        self.Padding      = '10p'
        self.Manager      = Manager
        
        #set master
        self.master = master
    
        #create the main frame
        self.MainFrame = ttk.Frame(master,
                                   padding = self.Padding)
    
        #send out the general populator
        self.GeneralPopulate()
    

    def GrabFrame(self):

        '''
        ############################################
        This element will dispatch the various frme 
        populators and the place hte frame in
        the current loded frame network
        ############################################
        '''
    
        return self.MainFrame


    def GeneralPopulate(self):

        '''
        ############################################
        This element will dispatch the various frme 
        populators and the place hte frame in
        the current loded frame network
        ############################################
        '''
            
        #set the variables
        self.Frames = []
        self.Fields = []
        
        #initiate variables
        self.GenerateText()

        #send out the methods
        self.Frames.append([self.TextFrameCreator(),
                            0,
                            0,
                            1,
                            3,
                            tk.E+tk.W])
                            
        self.Frames.append([ttk.Separator(self.MainFrame,
                                          orient = tk.HORIZONTAL),
                            1,
                            0,
                            1,
                            3,
                            tk.E+tk.W])

        self.Frames.append([self.ParameterFrameCreator(),
                            2,
                            0,
                            1,
                            3,
                            tk.E+tk.W])

        self.Frames.append([ttk.Separator(self.MainFrame,
                                          orient = tk.HORIZONTAL),
                            3,
                            0,
                            1,
                            3,
                            tk.E+tk.W])

        self.Frames.append([self.PathFrameCreator(),
                            4,
                            0,
                            1,
                            3,
                            tk.E+tk.W])
                            
        self.Frames.append([ttk.Separator(self.MainFrame,
                                          orient = tk.HORIZONTAL),
                            5,
                            0,
                            1,
                            3,
                            tk.E+tk.W])

        self.Frames.append([self.ProcessingFrameCreator(),
                            6,
                            0,
                            1,
                            3,
                            tk.E+tk.W])

        #call the placer
        self.GeneralPlacer()

    def GeneralPlacer(self):
        '''
        ############################################
        This will run through self.Fields and 
        self.Frames and place all of them onto the 
        grid...
        ############################################
        '''

        #cycle through fields
        for Element in self.Fields:

            #place it
            Element[0].grid(row         = Element[1],
                            column      = Element[2],
                            rowspan     = Element[3],
                            columnspan  = Element[4],
                            sticky      = Element[5])


        #cycle through fields
        for Element in self.Frames:

            #place it
            Element[0].grid(row         = Element[1],
                            column      = Element[2],
                            rowspan     = Element[3],
                            columnspan  = Element[4],
                            sticky      = Element[5])

    def TextFrameCreator(self):
        '''
        ############################################
        This will create the initial label frame 
        with the explanations
        ############################################
        '''

        #create the frame
        self.TextFrame = ttk.Frame(self.MainFrame,
                                   padding = self.Padding)

        #load the text label
        self.Fields.append([ttk.Label(self.TextFrame,
                                      text = self.LabelText[0],
                                      wraplength = 400),
                            0,
                            0,
                            1,
                            1,
                            tk.E+tk.W])

        return self.TextFrame

    def ProcessingFrameCreator(self):
        '''
        ############################################
        This will create the initial label frame 
        with the explanations
        ############################################
        '''

        ###############################
        #set variables
        
        self.Names = ['Number of Processors: ',
                      'Variable to Parallelize: ',
                      'Fold Result: ']
                      
        self.ProcessEntries     = [None]*1
        self.ProcessDropMenue   = [None]*1
        self.ProcessBool        = [None]*1
        self.ProcessDrop        = [None]*3
        
        self.TargetVar = tk.StringVar()
        self.TargetVar.set('1')
        self.TargetFold = tk.IntVar()
        self.TargetFold.set(0)
        self.ProcessDropList = ['0',
                                '1',
                                '2']
                                
        ###############################
        #recretate the frame
        self.ProcessFrame = ttk.Frame(self.MainFrame,
                                      padding = self.Padding)



        ###############################
        #process them
        
        #process the labels
        for i in range(0,3):
            
            self.Fields.append([ttk.Label(self.ProcessFrame,
                                          text = self.Names[i]) ,
                                i,
                                0,
                                1,
                                1,
                                tk.E+tk.W])
        
        #process the processorss
        self.ProcessEntries[0] = ttk.Entry(self.ProcessFrame,
                                           width = 3)
                
        self.ProcessEntries[0].insert(0, '1')
        
        self.Fields.append([self.ProcessEntries[0],
                            0,
                            1,
                            1,
                            1,
                            tk.E+tk.W])
                            
        #process the processorss
        self.ProcessDropMenue[0] = ttk.OptionMenu(self.ProcessFrame,
                                                self.TargetVar,
                                                *self.ProcessDropList)
                
        self.Fields.append([self.ProcessDropMenue[0],
                            1,
                            1,
                            1,
                            1,
                            tk.E+tk.W])
                            
        #process the processorss
        self.ProcessBool[0] = ttk.Checkbutton(self.ProcessFrame,
                                              variable = self.TargetFold)
                
        
        self.Fields.append([self.ProcessBool[0],
                            2,
                            1,
                            1,
                            1,
                            tk.E+tk.W])
                
        ###############################
        #send them out
        return self.ProcessFrame


    def PathFrameCreator(self):
        '''
        ############################################
        This will create the initial label frame 
        with the explanations
        ############################################
        '''

        ###############################
        #set variables
        
        self.Names = ['Simulation Name',
                      'Simulation script Folder Path',
                      'Simulation Output Path']
                      
        self.PathEntries = [None]*3
        self.PathButtons = [None]*3
        
        ###############################
        #recretate the frame
        self.PathFrame = ttk.Frame(self.MainFrame,
                        padding = self.Padding)



        ###############################
        #process them
        for i in range(0,3):
            
            self.Fields.append([ttk.Label(self.PathFrame,
                                          text = self.Names[i]) ,
                                i,
                                0,
                                1,
                                1,
                                tk.E+tk.W])
        


        for i in range(0,3):
            
            self.PathEntries[i] = CustomePathEntry(self.PathFrame,
                                                   width = 20)
                    
            self.Fields.append([self.PathEntries[i],
                                i,
                                1,
                                1,
                                1,
                                tk.E+tk.W])
        
        for i in range(1,3):
            
            self.PathButtons[i] = CustomePathButton(self.PathFrame,
                                                    self.PathEntries[i],
                                                    Type = 'Folder')
                    
            self.Fields.append([self.PathButtons[i],
                                i,
                                2,
                                1,
                                1,
                                tk.E+tk.W])
                
        ###############################
        #send them out
        return self.PathFrame

    def ParameterFrameCreator(self):
        '''
        ############################################
        This will create the initial label frame 
        with the explanations
        ############################################
        '''
        
        ###############################
        #set the selector string var
        self.TargetSelector   = []
        self.TargetSelector_2 = []
        self.TargetSelector_3 = []

        for i in range(0, 3):
        
            Var_1 = tk.StringVar()
            self.TargetSelector.append(Var_1)
                
            Var_2 = tk.StringVar()
            self.TargetSelector_2.append(Var_2)
                
            Var_3 = tk.StringVar()
            self.TargetSelector_3.append(Var_3)
                           
        for i in range(0,len(self.TargetSelector)):
        
            self.TargetSelector[i].set('Void')
        
        TargetDrop      = ['Lens Manager',
                           'Sample Manager',
                           'Void']
            
        #set the dropdown arrays
        self.SecondLevelDropDown = [None for i in range(0, len(self.TargetSelector))]
        self.ThirdLevelDropDown = [None for i in range(0, len(self.TargetSelector))]
        
        #set the Entry Arrays
        self.ParameterEntries = [[None]*3 for i in range(0, len(self.TargetSelector))]
        
        ###############################
        #recretate the frame
        self.ProcesParameterFrame = ttk.Frame(self.MainFrame,
                                              padding = self.Padding)

        self.FirstLevelDropDown = []
        
        for i in range(0,len(self.TargetSelector)):
            
            self.FirstLevelDropDown.append(tk.OptionMenu(self.ProcesParameterFrame,
                                                    self.TargetSelector[i],
                                                    *TargetDrop,
                                                    command = partial(self.Refresh_First,i)))
        
        ###############################
        #process them
        for i in range(0,len(self.TargetSelector)):
            
            self.Fields.append([self.FirstLevelDropDown[i] ,
                                i,
                                1,
                                1,
                                1,
                                tk.E+tk.W])
        
        ###############################
        #process them
        for i in range(0,len(self.TargetSelector)):
            
            self.Fields.append([ttk.Label(self.ProcesParameterFrame,
                                          text = 'Var '+str(i)+':',
                                          anchor = tk.E) ,
                                i,
                                0,
                                1,
                                1,
                                tk.E+tk.W])
        
        self.Fields.append([ttk.Separator(self.ProcesParameterFrame,
                                          orient = tk.HORIZONTAL),
                            len(self.TargetSelector),
                            0,
                            1,
                            4,
                            tk.E+tk.W])
                            
        for i in range(0,len(self.TargetSelector)):
            
            self.Fields.append([ttk.Label(self.ProcesParameterFrame,
                                          text = 'Var '+str(i)+' Bounds:',
                                          anchor = tk.E) ,
                                len(self.TargetSelector)+1+i,
                                0,
                                1,
                                1,
                                tk.E+tk.W])
        
        for i in range(0,len(self.ParameterEntries)):
            
            for j in range(0,len(self.ParameterEntries[i])):
        
                self.ParameterEntries[i][j] = ttk.Entry(self.ProcesParameterFrame,
                                                        width = 5)
                    
                self.Fields.append([self.ParameterEntries[i][j],
                                    len(self.TargetSelector)+1+i,
                                    j+1,
                                    1,
                                    1,
                                    tk.E+tk.W])
    
        ###############################
        #compute griding
        self.ProcesParameterFrame.grid_columnconfigure(1, weight = 1)
        self.ProcesParameterFrame.grid_columnconfigure(2, weight = 1)
        self.ProcesParameterFrame.grid_columnconfigure(3, weight = 1)
        
        ###############################
        #send them out
        return self.ProcesParameterFrame
    
    def Refresh_First(self, Num, Element, delete = True):
        '''
        ############################################
        This will create the initial label frame 
        with the explanations
        ############################################
        '''
        ###########################
        #first we try to delete
        #the current second level elements
        try:
    
            for i in range(0, len(self.SecondLevelDropDown)):

                self.SecondLevelDropDown[Num].destroy()
            
        except:

            pass
               
        try:
    
            for i in range(0, len(self.SecondLevelDropDown)):

                self.ThirdLevelDropDown[Num].destroy()
            
        except:

            pass
        
        
        ###########################
        #set the variables
        if not delete:
        
            Element = self.TargetSelector[Num].get()
        
        
        if Element == 'Void':
        
            return 0
        
        elif Element == 'Lens Manager':

            TargetDrop = ['General Lens']

            for i in range(0, len(self.Manager.LensManager.LensElements)):

                TargetDrop.append(self.Manager.LensManager.LensElements[i].ParametersDict['Name'])

        elif Element == 'Sample Manager':


            TargetDrop = []

            for i in range(0, len(self.Manager.SampleManager.SampleLinks)):

                TargetDrop.append(self.Manager.SampleManager.SampleLinks[i].ParametersDict['Name'])
    
    
        ###########################
        #create the object
        
        #set the default
        if delete:
        
            self.TargetSelector_2[Num].set(TargetDrop[0])
        
        else:
        
            pass
        
        #set the ioptionMenu
        self.SecondLevelDropDown[Num] = tk.OptionMenu(self.ProcesParameterFrame,
                                                      self.TargetSelector_2[Num],
                                                      *TargetDrop,
                                                      command = partial(self.Refresh_Second,Num))
        
        ###########################
        #Place the object
        self.SecondLevelDropDown[Num].grid(row = Num, column = 2, sticky = tk.E+tk.W)
    
    
    def Refresh_Second(self, Num, Element, delete = True):
        '''
        ############################################
        This will create the initial label frame 
        with the explanations
        ############################################
        '''
        ###########################
        #first we try to delete
        #the current second level elements
     
        try:
    
            for i in range(0, len(self.SecondLevelDropDown)):

                self.ThirdLevelDropDown[Num].destroy()
            
        except:

           pass
        
        
        ###########################
        #Create the dictionary
        if not delete:
        
            Element = self.TargetSelector_2[Num].get()
        
        self.Dictionary = {}
                    
        if self.TargetSelector[Num].get() == 'Sample Manager':
        
            LowLevelTarget = self.Manager.SampleManager
        
            for i in range(0, len(LowLevelTarget.SampleLinks)):

                self.Dictionary[LowLevelTarget.SampleLinks[i].ParametersDict['Name']] = LowLevelTarget.SampleLinks[i]
        
        
        elif self.TargetSelector[Num].get() == 'Lens Manager':
        
            LowLevelTarget = self.Manager.LensManager
            
            self.Dictionary['General Lens'] = LowLevelTarget

            for i in range(0, len(LowLevelTarget.LensElements)):

                self.Dictionary[LowLevelTarget.LensElements[i].ParametersDict['Name']] = LowLevelTarget.LensElements[i]
        
        ###########################
        #set the variables
        TargetDrop = []

        for i in range(0, len(self.Dictionary[self.TargetSelector_2[Num].get()].PreferenceList)):

            #only grab numerical values
            if self.Dictionary[self.TargetSelector_2[Num].get()].PreferenceList[i][3] == 'float':
            
                TargetDrop.append(self.Dictionary[self.TargetSelector_2[Num].get()].PreferenceList[i][0]
                                  +'->'+
                                  self.Dictionary[self.TargetSelector_2[Num].get()].PreferenceList[i][1])


    
        ###########################
        #create the object
        
        #set the default
        if delete:
        
            self.TargetSelector_3[Num].set(TargetDrop[0])
        
        else:
        
            pass
        
        #set the ioptionMenu
        self.ThirdLevelDropDown[Num] = tk.OptionMenu(self.ProcesParameterFrame,
                                                      self.TargetSelector_3[Num],
                                                      *TargetDrop)
        
        ###########################
        #Place the object
        self.ThirdLevelDropDown[Num].grid(row = Num, column = 3, sticky = tk.E+tk.W)
            
    def GenerateText(self):
        '''
        ############################################
        This will create the initial label frame 
        with the explanations
        ############################################
        '''

        self.LabelText = []

        self.LabelText.append(  'This is the processing frame and intended to '
                              + 'set the parameters for the simulation such as '
                              + 'the variable that should be investigated and '
                              + 'the way processors should be used ...')



class ParameterFrame():
    
    '''
    ####################################################################################
    In an effort to unify the import window into one single class we will extract
    the frames of three provious windows and populate them here into a notebook...
    
    
    ####################################################################################
    '''
    
    def __init__(self,master,Manager, Parent, Window = False, SubmitMethod = DoNothing):
        
        
        ######################################
        #link the DataClass
        self.padding      = '10p'
        self.Manager      = Manager
        self.Parent       = Parent
        
        #set master
        self.master = master
        self.Window = Window
        self.SubmitMethod = SubmitMethod
    
        #create the main frame
        self.MainFrame = ttk.Frame(master)
    
        #send out the general populator
        self.GeneralPopulate()
    
        #place maineFrame
        self.MainFrame.grid(row = 0, column = 0)

    def GrabFrame(self):

        '''
        ############################################
        This element will dispatch the various frme 
        populators and the place hte frame in
        the current loded frame network
        ############################################
        '''
    
        return self.MainFrame
    
    def GeneralPopulate(self):

        '''
        ############################################
        This element will dispatch the various frme 
        populators and the place hte frame in
        the current loded frame network
        ############################################
        '''
        
        #initialise frame array
        self.Frames = []
        
        #initialise entry list
        self.EntryList = []
        
        #cycle
        self.Frames.append(self.SpecificPopulator(self.Manager.PreferenceList))

        #submit frame
        self.Frames.append(self.SubmitPopulator())

        #grid the frames
        for i in range(0, len(self.Frames)):
            self.Frames[i].grid(row = i, column = 0)
            
    def SpecificPopulator(self,Preferences):
        '''
        ############################################
        This element will dispatch the various frme 
        populators and the place hte frame in
        the current loded frame network
        ############################################
        '''

        #initialise a frame
        Frame = ttk.Frame(self.MainFrame,
                          padding = self.padding)
        
        for i in range(len(Preferences)):

            ttk.Label(Frame, text = Preferences[i][0]+': ',anchor = tk.E).grid(row = i,column = 0,sticky = tk.E+tk.W)
            
            if Preferences[i][3] == 'float' or  Preferences[i][3] == 'int' or  Preferences[i][3] == 'str':
            
                self.EntryList.append(CustomeEntry(Frame,Preferences[i] ))
                self.EntryList[-1].grid(row = i,
                                        column = 1,
                                        sticky = tk.E+tk.W)
    
            elif Preferences[i][3] == 'Path':
                
                self.EntryList.append(CustomePathEntry(Frame,Preferences[i] ))
                self.EntryList.append(CustomePathButton(Frame,self.EntryList[-1]))
                self.EntryList[-2].grid(row = i,
                                        column = 1,
                                        sticky = tk.E+tk.W)
                self.EntryList[-1].grid(row = i,
                                        column = 2,
                                        sticky = tk.E+tk.W)
        
            elif Preferences[i][3] == 'bool':
                
                self.EntryList.append(CustomeCheckButton(Frame,Preferences[i] ))
                self.EntryList[-1].grid(row = i,
                                        column = 1,
                                        sticky = tk.E+tk.W)
                    
        return Frame

    def SubmitPopulator(self):
        '''
        ############################################
        This element will dispatch the various frme 
        populators and the place hte frame in
        the current loded frame network
        ############################################
        '''

        #initialise a frame
        Frame = ttk.Frame(self.MainFrame, padding = self.padding)
        
        #create the submit button
        ttk.Button(Frame,text = 'Submit', command = self.Submit).grid(row = 0, column = 0)
        
        return Frame

    def Submit(self):
        '''
        ############################################
        This element will dispatch the various frme 
        populators and the place hte frame in
        the current loded frame network
        ############################################
        '''

        #initialise a frame
        for Entry in self.EntryList:
        
            Entry.Submit()


        #process submit method
        self.SubmitMethod()
        
        #if a window
        if self.Window:
            
            #call destroy
            self.master.destroy()


class CustomeEntry(ttk.Entry):

    '''
    ######################################################
    The code to select to create a button with an image 
    at the heart being quiet repetitve, it was decided to
    generalise it
    ######################################################
    '''
    
    def __init__(self, parent, Manager,**kwargs):


        #save the Manager localu
        self.Manager = Manager
        
        #Import all the images
        ttk.Entry.__init__(self,parent, **kwargs)

        #populate
        self.insert(0,str(self.Manager[2][self.Manager[1]]))

    def Submit(self):
        '''
        ############################################
        Submit the value depending on the data type
        ############################################
        '''
        if self.Manager[3] == 'float':
            
            self.Manager[2][self.Manager[1]] = float(self.get())
                
        elif self.Manager[3] == 'int':
        
            self.Manager[2][self.Manager[1]] = int(self.get())

        elif self.Manager[3] == 'str':
        
            self.Manager[2][self.Manager[1]] = str(self.get())
        
        else:

            print 'Nothing done'


class CustomeCheckButton(ttk.Checkbutton):

    '''
    ######################################################
    The code to select to create a button with an image 
    at the heart being quiet repetitve, it was decided to
    generalise it
    ######################################################
    '''
    
    def __init__(self, parent, Manager,**kwargs):


        #save the Manager local
        self.Manager = Manager
        
        #set variable
        self.Var = tk.IntVar()

        #check value
        if self.Manager[2][self.Manager[1]]:
        
            self.Var.set(1)
        
        else:
        
            self.Var.set(0)
        
        #save the Manager localu
        self.Manager = Manager
        
        #Import all the images
        ttk.Checkbutton.__init__(self,parent,variable = self.Var, **kwargs)


    def Submit(self):
        '''
        ############################################
        Submit the value
        ############################################
        '''
        
        if self.Var.get() == 1:
        
            self.Manager[2][self.Manager[1]] = True
        
        else:

            self.Manager[2][self.Manager[1]] = False

class CustomePathEntry(ttk.Entry):

    '''
    ######################################################
    The code to select to create a button with an image 
    at the heart being quiet repetitve, it was decided to
    generalise it
    ######################################################
    '''
    
    def __init__(self, parent, Manager = None,**kwargs):


        #save the Manager local
        self.Manager = Manager
        
        #Import all the images
        ttk.Entry.__init__(self,parent, **kwargs)

        if not Manager == None:
            #populate
            self.insert(0,str(self.Manager[2][self.Manager[1]]))

    def Submit(self):
        '''
        ############################################
        Submit the value
        ############################################
        '''
        self.Manager[2][self.Manager[1]] = str(self.get())


class CustomePathButton(ttk.Button):

    '''
    ######################################################
    The code to select to create a button with an image 
    at the heart being quiet repetitve, it was decided to
    generalise it
    ######################################################
    '''
    
    def __init__(self, parent, Target , Type = 'File',**kwargs):


        #save the Manager local
        self.Target = Target
        self.Type    = Type
        
        #Import all the images
        ttk.Button.__init__(self,parent,
                            text = '...',
                            command = self.GetPath,
                            **kwargs)

        if self.Type == 'File':
            
            #oath that will be lonked to opening the search path
            self.PathofInterest = os.getcwd()
            
            self.file_opt = options = {}
            options['filetypes']    = [('all files', '.*'), ('Text Files', '.txt'), ('Raman Files', '.RAM')]
            options['initialdir']   = self.PathofInterest
            options['initialfile']  = 'myfile.txt'
            options['title']        = 'Select a File'
        
        if self.Type == 'Folder':
            
            #oath that will be lonked to opening the search path
            self.PathofInterest = os.getcwd()
            
            self.dir_opt = options  = {}
            options['initialdir']   = self.PathofInterest
            options['mustexist']    = False
            options['title']        = 'Select a Directory'
    
    
    def GetPath(self):
        '''
        ############################################
        Asks for a path and sends it to the linked
        target to reinject it
        ############################################
        '''
        
        if self.Type == 'File':
        
            self.Path = tkFileDialog.askopenfilename( **self.file_opt)
    
        if self.Type == 'Folder':
        
            self.Path = tkFileDialog.askdirectory(**self.dir_opt)
        
        self.Target.delete(0, tk.END)
        self.Target.insert(0, self.Path)

    def Submit(self):
        '''
        ############################################
        The submit method is not supported for this
        class and therefore ommited
        ############################################
        '''
        pass


