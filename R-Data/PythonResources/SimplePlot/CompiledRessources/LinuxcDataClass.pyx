# -*- coding: utf-8 -*-
"""
Created on Wed May 20 09:47:08 2015

@author: Alexander Schober
"""
import pdb
#pdb.set_trace()

#import the instances of python that should be installed
import numpy
import re
import sys
import os

import matplotlib
matplotlib.use("Agg")

#Import our custome instances
import VisOut    #Visualisation routines
import DataInfo  #Info handling class
import NMF_R     #Non negative routine fact management
import Utility   #utility -> will be reduced slowly and split into more subscripts
from Utility import Range
from PCAEdit import PCA as pca #PCA calculation methods
import FileManagement as File
import RamFit

#file management and export into zip files recquires to import zip
import zipfile

'''
##############################################################################
In this section of the class we would like to store all the vital informations
Compared to the old depth dataclass this one will not be initiated with a
dataset but rather empty. It can then be filled. Not that this class will then
incorporate the following subclasses:
    
- Class: Data
    - __init__  (status == BUILT)
        Data.isLoaded
        Data.isInfo
        Data.isContour
        Data.isPCA
        Data.isNMF
    
    - .Load        (BUILT): loads data at file path otherwise throws error and state not loaded
    - .LoadRaw     (BUILT): partly build misses specific parts for dıfferent fıl types
    - .LoadContour (BUILT)
    - .LoadPCA     (BUILT)
    - .LoadNMF     (BUILT)
    - .Cleanse     (ABORTED) not needed as the entire class can just be deleted and reloaded
    
    - .SetSample (BUILT): Helps to extract sample information
    - .SetRaman  (BUILT): Helps to extract raman information
    - .Info      (BUILT): All information abou the currently loaded dataset
    
    - .AxisZ     (BUILT): basically the spectra intensity points
    - .AxisX     (BUILT): basically the wavenumbers
    - .AxisY     (BUILT): all other axisses relevant to the data can be 0 for single spectra
    
- ContourClass: data to load and edit and ability to dump
    - .__init__        (BUILT)
    - .__print__
    - .BuildProjection (BUILT)
    - .InitiateContour (BUILT)
    - .DumpSpectrum
    - .DumpAll         (Needs to be implemented will be used to build the first sata file)
    
- VisualComponentHandler: To handle the components from multiple sources
    - __init__    (BUILT)
    - VCH.BuildOutput (BUILT) works for depth. Next step is to design for line XY
    
    #Variables loaded externally:
    VCH.Comp   -> Loaded from component finding routines
    VCH.CompX  -> Wavenumbers imported immediately from source X class
    VCH.Score  -> Loaded from component finding routines
    VCH.ScoreX -> Array of ZXY indices... needs to be computed for different visualisation
    
    VCH.DumpComponent
    VCH.DumpScore
    
- PCA: data loaded into PCA class
    PCA.__init__          (BUILT)
    PCA.__print__
    PCA.BuildPCASet       (BUILT) should work for all data types
    PCA.RunPCACalculation (BUILT) should work for all data types
    PCA.SetCropping       (BUILT) not supporting all datatypes yet

    
- NMF: data loaded into NMF class
    NMF.__init__
    NMF.__print__
    NMF.Data
    NMF.X
    NMF.Y
    NMF.Var as in variables
    NMF.Run initiate the run of the routine
    NMF.DumpComponent
    NMF.DumpScore
    
    Note that the maine use of these clases is to make the system more flexible
    as adding a class for another data type becomes easier. Note also that calling
    NMF and PCA previously passed through the Utility.py file and will now be
    rewritten as an instance specific action.
    
    On a further note we will also noad the figures into the class. and add here
    the figure manipulation classes
##############################################################################
'''

class Data:

    def __init__(self):
        """
        #######################################################################
        Here we will simply define all the boolean variables and get the class 
        ready to accept data and treatment
        
        self.isLoaded indicates if data was loaded it will be the 
        argument to start any other routine or class initialisation
        
        self.isContour indicates if contours were already initialised
        self.isPCA indicates if the PCA has been initialised
        self.isNMF indicates if the NMF has been done
        #######################################################################
        """

        #Set logical variables
        self.isLoaded   = False
        self.isContour  = False
        self.isPCA      = False
        self.isNMF      = False
        self.isInfo     = False
    
    def LoadRamFit(self):
        """
        #######################################################################
        Loads the fiting class and clears it in case it is already defined
        #######################################################################
        """
    
        #Initialise RamFit here immidiately no betetr place found
        self.RamFit = RamFit.FitMainClass(self)
    
    def LoadNMF(self):
        """
        #######################################################################
        This instance is just a method winthin the class to start the loading
        of the NMF method
        
        this method can then be unloaded through self.cleanse()
        #######################################################################
        """
        #This will be initialised by PCA and both are loaded simultaneously
        #self.VCH = VisualComponentHandler(self)
        
        #Initiate NMF class
        self.NMF = NMFClass(self)

    def LoadPCA(self):
        """
        #######################################################################
        
        #######################################################################
        """
        
        #Initiate Component handler class
        self.VCH = VisualComponentHandler(self)
        
        #initiate PCA class
        self.PCA = PCAClass(self)


    def LoadContour(self):
        """
        #######################################################################
        Load the contour instance as self.Contour
        #######################################################################
        """

        self.Contour = ContourClass(self)
    
    def Reinitialise(self):
        """
        #######################################################################
        Detroys and reloads the pca and NMF instances
        #######################################################################
        """
        
        #destroy
        try:
            del self.PCA
        except:
            print 'The pca instance was already missing, why ?'

        try:
            del self.NMF
        except:
            print 'The nmf instance was already missing, why ?'
    
    
        #Load them
        self.PCA = PCAClass(self)
        self.NMF = NMFClass(self)
        
        
        
        
    def LoadRaw(self,Path,Input,Container,event,queue):
        """
        #######################################################################
        This was previsouly doen externally. Was is happening her is that 
        we will load the the raw raman data files and then build the according
        array, gathe the information from the user and finnally dump it. Note
        that this will also immediately call Load() on the exit path. In a
        first instance we will ask the user for the measurement type.
        
        Some historic atrefacts might be contained in the way things are done
        most will be clean though
        
        
        Depth (BUILT) but could use a polish process
        Single(BUILT) completed
        
        #######################################################################
        """
        
        try:
            #Initialise log
            LastAct = ''
            
            #Set a breaking condition
            BreakFree = False
            
            #make container self
            self.Container = Container
            
            #try raman info
            self.RamInfo = Container[0]
            self.SamInfo = Container[1]
            
            print Input[0]
            
            #Start logic break loop
            while not BreakFree:
                
                #Do we have a single file or multiple ones
                if int(Input[0]) == 5:
                    
                    #quick loading action function already written in Utility from version 2
                    XData,YData,Act = Utility.ReadSingleFile(Path)
                
                    #Build header
                    HeadStr,HeadStrEx = Utility.PrepWrite(Path,'Single')

                    #Send it out
                    #Define directory name
                    DirName = os.path.join(Utility.ReadIni(1),HeadStr)
                    
                    #Check if the directory exists, if not create it
                    if not os.path.exists(DirName):
                        os.makedirs(DirName)
                    
                    #filemane
                    DirName = os.path.join(DirName,HeadStr)
                
                    #write
                    Utility.WriteSingle2File(HeadStrEx+'\n'+self.RamInfo+self.SamInfo,XData,YData,DirName+'.txt')
                        
                        
                    #File location
                    FileLoc = os.path.join(Utility.ReadIni(1),DirName+'.txt')
                        
                    #Load the file into self class
                    LastAct += self.Load(FileLoc)
                
                
                #We have a depth series treat it
                elif int(Input[0]) == 1:
                    
                    #this is new in version 0.0.4 and finnaly goes to version 2 files writing
                    o       = 0
                    ID      = []
                    Z       = []
                    X       = []
                    Y       = []
                    T       = []
                    EleLoc  = []
                    PathListFix = []
                    
                    #This imports all filenames cotained in a goven folder
                    PathList = File.GetFileNames(Path,'.txt')
                        
                    #Check all the path for informations and append
                    for idx,Val in enumerate(PathList):
                        
                        #Set the file id to find it agains after sorting
                        ID.append(o)
                        o += 1

                        #Actually append the value
                        Z.append(float(Val.split(os.path.sep)[-1].split(self.temp[0])[1].split(self.temp[1])[0]))

                    #Depth measurement set to 0
                    X = [None]
                    Y = [None]
                    T = [None]
                    
                    #Build the Activeset
                    Activeset = [True,False,False,False]
                    
                    #Set the type
                    self.Type = 'Depth'
                            
                    #Depth measurement we only need to order according to Z
                    Z, PathListFix = zip(*sorted(zip(Z, PathList)))
                        
                    #hitorically the loading for Z is located in utilities to be change in a further version
                    omega, Data = self.ImportFileDataV2(PathListFix,Z,X,Y,T,event,queue)
                    
                    #Build the ouptu
                    LastAct += "\nData was successfully loaded and rearanged:"
                    LastAct += "\n- Dataset Range: "+str(numpy.min(Z))+" to "+str(numpy.max(Z))+" micrometer"
                    if int(Input[0]) == 0:
                        LastAct += "\n- Dataset Steping: "+str((numpy.max(Z)-numpy.min(Z))/len(Z))+" micrometer"
                    LastAct += "\n- Number of files: "+str(len(Z))
                        
                        
                    #Process Signal (version 0.0.4 omited the filtering options, can be readded maybe later... )
                    Data, omega = self.SignalProcV2(Data,omega,Z,X,Y,T,Activeset,event,queue)
            
                    #send it out
                    self.Export(Data,omega,Z,X,Y,T,Activeset,self.Type,PathListFix[0],event,queue)
                        
                    
                #We don't check for all complicated  types
                else:
                
                
                    #This imports all filenames cotained in a goven folder
                    PathList = File.GetFileNames(Path,'.txt')
                    
                    #Initialise what we need in any measurement type
                    o       = 0
                    ID      = []
                    Z       = []
                    X       = []
                    Y       = []
                    T       = []
                    EleLoc  = []
                    PathListFix = []
                    
                    #input 0 is depth measurement -> rest to come
                    if int(Input[0]) == 0 or int(Input[0]) == 5:
                        
                        #Check all the path for informations and append
                        for idx,Val in enumerate(PathList):
                            
                                #Set the id of the found value
                                ID.append(o)
                                o += 1
                                
                                
                                #Actually append the value
                                Z.append(float(Val.split(os.path.sep)[-1].split(self.temp[0])[1].split(self.temp[1])[0]))
                                
                                
                                
                                #Depth measurement set to 0
                                X.append(0)
                                Y.append(0)
                    


                        #sort it
                        Z, PathListFix = zip(*sorted(zip(Z, PathList)))


                        #hitorically the loading for Z is located in utilities to be change in a further version
                        omega,Data = Utility.ImportFileData(PathListFix,Z)
                        
                        LastAct += "\nData was successfully loaded and rearanged:"
                        LastAct += "\n- Dataset Range: "+str(numpy.min(Z))+" to "+str(numpy.max(Z))+" micrometer"
                        if int(Input[0]) == 0:
                            LastAct += "\n- Dataset Steping: "+str((numpy.max(Z)-numpy.min(Z))/len(Z))+" micrometer"
                        LastAct += "\n- Number of files: "+str(len(Z)*len(X)*len(Y)*len(T))
                        
                        
                        
                        #Process Signal (version 0.0.4 omited the filtering options, can be readded maybe later... )
                        #Buffer,ExitFilePath= Utility.SignalProc(Output,PathList[0],SigRangeMin=Min+1,SigRangeMax=Max-1,mult=5,Filter=False,Container = Container,Input = int(Input[0]))
                    
                        #For loging
                        #LastAct += Buffer

                        #File location
                        #FileLoc = os.path.join(Utility.ReadIni(1),ExitFilePath+'.txt')
                        
                        #Load the file into self class
                        #LastAct += self.Load(FileLoc)

                break
            queue.put('Stop')
            return LastAct
        
        except Exception,e:
            print str(e)
            queue.put('Stop')
            

    def ImportFileDataV2(self,DataPath,Z,X,Y,T,event,queue):
        '''
        ##############################################################################
        This function got carried over from the Utilities and is therefore still very 
        primitve.
        
        But it works and that matters
        ##############################################################################
        '''
        
        #For logging
        LastAct = ''
        
        #length of the data
        NumPoints = len(Z)*len(X)*len(Y)*len(T)
        
        #Count how many lines we have and create the first array
        Count     = open(DataPath[0], 'r')
        
        #Loop through
        LineCount = 0
        
        for i in Count:
            LineCount += 1

        #close for now
        Count.close()
        
        '''
        ##############################################################################
        This function got carried over from the Utilities and is therefore still very 
        primitve.
        
        But it works and that matters
        ##############################################################################
        '''

        #create the data matrix
        Data  = []
        omega = []
        
        #open the first element to read the omega
        f = open(DataPath[0], 'r')
        
        #read omega
        for Line in f:
            
            #create omega
            try:
                omega.append(float(Line.strip().replace('\t',' ', 1).split()[0]))
            except:
                pass
        
        #close the file
        f.close()
            
        
        '''
        ##############################################################################
        Cycyle over all of the variables and save it to a variabe called Data.
        Note that Data will always be of dimention 5... 4 of them are callable
        directly Z X Y T and finnally omega as implicite variabel
        ##############################################################################
        '''
        
        for i in range(0,len(Z)):
            
            for j in range(0,len(X)):
            
                for k in range(0,len(Y)):
            
                    for l in range(0,len(T)):
                        
                        #calculate index:
                        Index = (i+1)*(j+1)*(k+1)*(l+1)-1
                        
                        #make print out
                        #print '     | -> '+str(round(float(Index)/(float(NumPoints+1))*100,2)),'\r',
                        #sys.stdout.flush()
                        
                        ########################################
                        #Now we send stuff to the queue
                        queue.put(float(Index)/(float(NumPoints+1))*100)

                        #open the linked file
                        f = open(DataPath[Index], 'r')
                        
                        #initialise
                        transfer = []
                        
                        #write
                        for Line in f:
                            
                            #print float(Line.strip().replace('\t',' ', 1).split()[1])
                            try:
                                transfer.append(float(Line.strip().replace('\t',' ', 1).split()[1]))
                            except:
                                pass
                        #save the data
                        Data.append(numpy.copy(transfer))
                                         
                        #close the file
                        f.close()
            
        return omega,Data

                                         
    
    def FixOmegaData(self,omega):
                                         
        '''
        ##############################################################################
        This fucntion will fix the data array of the Dataset as it is not linear.
        ##############################################################################
        '''
        
        
        '''
        ##############################################################################
        Correct omega
        ##############################################################################
        '''
        #initialise
        Delta = []
        
        for g in range(1,len(omega)):
            
            #get difference
            Delta.append(omega[g]-omega[g-1])   #We take the position
        
            
        #take the average
        CorStep = numpy.mean(Delta)
        
        #Build the corrected 1D X Data array
        NotReachMin = True
        CorXPoints = []
        i = 0
        
        while NotReachMin:
            
            #check
            if (i)*CorStep+omega[0]<numpy.min(omega):
                NotReachMin = False
                break
            
            CorXPoints.append((i)*CorStep+omega[0])#Add an element to our new X Data array

            #indent
            i = i+1
            
        return CorXPoints
        


    def SignalProcV2(self,Data,omega,Z,X,Y,T,Activeset,event,queue):
        '''
        ##############################################################################
        This function was originally located in the utility section. It was transfered
        for version 2 into this section. 
        
        Note that in version 0.0.4 the signal processessing does not support any type
        of filters
        
        They are nevertheless present and will therefore be reintroduced in the futur
        
            
        ##############################################################################
        '''
        
        #######Variables that will not be used now#########
        self.Filter = None
        self.FilterInput = ''
        self.mult = 0
        
        '''
        ##############################################################################
        Filtering section
        ##############################################################################
        '''
        #if filtering has been chosen unpack environement variables
        if self.Filter and self.FilterInput != '':
            FilterType = self.FilterInput[0]
            
            #if conventional freq filter (careful introduces shifts)
            if FilterType == "freq":
                CutOff     = self.FilterInput[1]
                
            #if filter selected is Savitzky-Golay only in one dimention (best adapted)
            if FilterType == "1dsg":
                window     = self.FilterInput[1]
                order      = self.FilterInput[2]
            
            #if filter selected is Savitzky-Golay in two dimention (best adapted)
            if FilterType == "2dsg":
                window     = self.FilterInput[1]
                order      = self.FilterInput[2]
        else:
            FilterType = 'None'
        
        
        '''
        ##############################################################################
        Multiplication range section mostly usefull for filters
        
        Also corrects the wavenumber axis
        ##############################################################################
        '''
        #Set a high enough multiplication factor 5 minimum for statistical purposes
        if self.mult<5:
                self.mult =5
                
        mult = self.mult
        
        NumPoints = len(Z)*len(X)*len(Y)*len(T)
        
        #find the dataset we wil extract at the end of th emanipulations
        Middle = int(self.mult/2)
        
        #Find Index range in the provided 2D data array
        #omega, Data = self.FindIdxV2(omega,Data)
        omegaTemp = self.FixOmegaData(omega)
        
        #Create the enumeration Index list
        IdxList = Utility.MultIndex(self.mult,omegaTemp)
      
        #Create the long string for my X Data
        PreSigProcOutput = []
        SigProcOutput    = []
        
        '''
        ##############################################################################
        Send out log information
        ##############################################################################
        '''
        
        #Start the real Business
        VisOut.TextBox(Title='Action',Text = '-> Corrected Data Waveumber Array',L = 80,state = 1,close = False)
        LastAct = '-> Corrected Data Waveumber Array '
        VisOut.TextBox(Title='Action',Text = '-> Will Now proceed to Signal Processing: (percent done) ',L = 80,state = 1,close = False)
        sys.stdout.flush()
            
        '''
        ##############################################################################
        Correct the Data
        ##############################################################################
        '''
        
        for i in range(0,len(Z)):
            
            for j in range(0,len(X)):
            
                for k in range(0,len(Y)):
            
                    for l in range(0,len(T)):
                        
                        #index
                        Index = (i+1)*(j+1)*(k+1)*(l+1)-1
                            
                        #save the data
                        ToCorrectData = Data[Index]
                        
                        #Corrected Data saver
                        CorrectedData = numpy.zeros((len(IdxList)))
                                         
                        #make print out
                        #print '     | -> '+str(round(float((i+1)*(j+1)*(k+1)*(l+1)-1)/(float(NumPoints+1))*100,2)),'\r',
                        #sys.stdout.flush()
                        
                        ########################################
                        #Now we send stuff to the queue
                        number = float(Index)/(float(NumPoints+1))*100
                        queue.put(number)
    
                        #go over every point
                        for m in range(0,len(IdxList)):
                
                            #First we have to correct the output: catch the associated valu of X
                            omega0  = omegaTemp[int(IdxList[m])]
                
                            #Now we search for the two values around in XPoints
                            for n in range(1,len(omega)):
                    
                                #Check if the value is in between two consecutive points
                                if omega[n] == omega0:
                                    CorrectedData[m] = ToCorrectData[n]
                                
                                elif omega[n] <= omega0 and omega[n-1] >= omega0:

                                    #Get the spacing between our two points:
                                    XSpacing = omega[n]-omega[n-1]
                                    ZSpacing = ToCorrectData[n]-ToCorrectData[n-1]
                            
                                    #Get the actual offset
                                    XOffsetSpacing = omega0-omega[n-1]
                                    
                                    #buffer it
                                    CorrectedData[m] = (ZSpacing)*abs(XOffsetSpacing/XSpacing)+ToCorrectData[n-1]
                                    break
                    
                    
        
                        '''
                        ##############################################################################
                        INIACTIVE AT THE MOMENT

                        #if we selected a 1D frequency processing method:
                        if self.Filter and self.FilterType == "freq":
                            Feed = PreSigProcOutput[range(1,mult*(CorIdxRange+1)),i]
                            SigProcOutput[range(1,mult*(CorIdxRange)+1),i],Error = LowPassFilter(Feed,CutOff,CorStep,6)
                    
                        #if we select 1d sg method
                        elif self.Filter and self.FilterType == "1dsg":
                            Feed = PreSigProcOutput[range(1,mult*(CorIdxRange+1)),i]
                            SigProcOutput[range(1,mult*(CorIdxRange)+1),i] = sgolay1d(Feed,window,order)
                        
                        #Otherwise just copy and move on
                        else:
                            #Calculate the actal value
                            
                            PreSigProcOutput.append(CorrectedData[Middle*len(omegaTemp):(Middle+1)*len(omegaTemp)+1])
    
    
 
        
                        #if we select 2d sg method
                        if self.Filter and FilterType == "2dsg":
                            Feed = SigProcOutput[range(1,mult*(CorIdxRange)+1),1:NumPointsZ+1]
                            SigProcOutput[range(1,mult*(CorIdxRange)+1),1:NumPointsZ+1] = sgolay2d(Feed,window,order)

                        ##############################################################################
                        '''

        SigProcOutput = PreSigProcOutput
        
        
        VisOut.TextBox(Title='Action',Text = ' -> 100 % Completed',L = 80,state = 1,close = False)
        LastAct = LastAct+' -> 100 % Completed'
        
        
        '''
        ##############################################################################
        We found that the write method reads line ans not columns as such we need to
        convert SigProcOutput into SigProcOutputLines
        ##############################################################################
        '''
        SigProcOutputLines = []
        
        
        for u in range(0,len(SigProcOutput[0])):
            
            #Initialise the Buffer
            Buffer = []
            
            #build buffer
            for i in range(0,len(SigProcOutput)):
                
                #append to buffer
                Buffer.append(SigProcOutput[i][u])

            #save it
            SigProcOutputLines.append(Buffer)

        
        
        return SigProcOutputLines,omegaTemp

        '''

        if int(Input) == 0:
            
            HeadStr,HeadStrEx = PrepWrite(DataPath,'Depth')
        
        if int(Input) == 5:
            
            HeadStr,HeadStrEx = PrepWrite(DataPath,'Temperature')
       
        #The HeadStr Pre-Signal Processing File
        #First Will be the HeadStr string in the file
        #Last will be the name of the output file
       
        #Adding the variable Info is for depth and raman setup as well ans sample +sub info
       
        First = ["" for x in range(0,4)]
        LastL = ["" for x in range(0,4)]
        
        First[0] = HeadStrEx+"\n\n\n"  
        LastL[0] = HeadStr+"_Originial"
        
        First[1] = HeadStrEx+'\nThis is the Pre-Fourier file from'+str(SigRangeMin)+' to '+str(SigRangeMax)
        First[1] = First[1]+'\nReplicatio factor:'+str(mult)+'\n'
        LastL[1] = HeadStr+'_PreSignalProcessing_'+str(SigRangeMin)+'to'+str(SigRangeMax)+'_Filter_'+FilterType
        
        First[2] = HeadStrEx+'\nThis is the signal processing file from'+str(SigRangeMin)+' to '+str(SigRangeMax)
        
        #if we selected comon proessing
        if Filter and FilterType == "freq":
            First[2] = First[2]+'\nwith a '+FilterType+' at '+str(CutOff)+' and the replicatio factor:'+str(mult)+'\n'
            
        #if we select 1d sg method
        elif Filter and FilterType == "1dsg":
            First[2] = First[2]+'\nwith a '+FilterType+' with a window '+str(window)+' and order '+str(order)+' and the replicatio factor:'+str(mult)+'\n'
            
        #if we select 2d sg method
        elif Filter and FilterType == "2dsg":
            First[2] = First[2]+'\nwith a '+FilterType+' with a window '+str(window)+' and order '+str(order)+' and the replicatio factor:'+str(mult)+'\n'
            
        #Otherwise just copy and move on
        else:    
            First[2] = First[2]+'\nwith a '+FilterType+' and replication factor:'+str(mult)+'\n'

        LastL[2] = HeadStr+'_PostSignalProcessing_'+str(SigRangeMin)+'to'+str(SigRangeMax)+'_Filter_'+FilterType
        
        #Ask user to complete information (carried over since version 0.0.4)
        #RamInfo,SamInfo = GetInfo()
        RamInfo = Container[0]
        SamInfo = Container[1]
        
        #Write files    
        O        = Write2File(Output,0,LineCount+1,NumPointsZ+1,HeadStrEx,First[0],LastL[0],HeadStr,RamInfo,SamInfo)
        LastAct  = LastAct +'\n'+O
        
        O        = Write2File(PreSigProcOutput,Middle*CorIdxRange,(Middle+1)*CorIdxRange+1,NumPointsZ+1,HeadStrEx,First[1],LastL[1],HeadStr,RamInfo,SamInfo)
        LastAct  = LastAct +'\n'+O
        
        O        = Write2File(SigProcOutput,Middle*CorIdxRange,(Middle+1)*CorIdxRange+1,NumPointsZ+1,HeadStrEx,First[2],LastL[2],HeadStr,RamInfo,SamInfo)
        LastAct  = LastAct +'\n'+O
        
        return LastAct,os.path.join(HeadStr,LastL[2])


        '''

    def Export(self,Data,omega,Z,X,Y,T,Activeset,Type,Path,event,queue):
        """
        ###########################################################################################        
        This will export the current Dataset part of the loadRaw routine. 
        As such specific ajustements should be done. Note that the export routine is Datatype 
        dependent and therefore should be updated soon.
        
        This will include the new write routine
        ###########################################################################################
        """

        #Prep the write header
        self.HeadStr,self.HeadStrEx = Utility.PrepWrite(Path,Type)

        #Set tail
        Tail = self.HeadStr

        #Send it out
        Utility.Write2FileV2(self,Data,Z,X,Y,T,Activeset,omega,Tail,event = event,queue = queue)
    
    
    def Load(self,Path):
        """
        #######################################################################
        We decided to centralise the load function and to initialyse the data
        in this section of the class
        
        Note that Load will automatically seperate between:
        
        - Depth 
        - Line
        - Map
        - Volume
        
        This will be hardcoded in a setting associated calles self.Type
        and saved into a string. Note also that while X stays 1D, Y will be the
        collection of space vectors
        
        the sample informations and so on will be stored into a dictionary.
        it allows for easier string manipulation i guess
        
        note that the old dataformat was uni dimensional
        and therefore only Z was present in hte beginning
        this will be refered to as version 1
        
        The new data files can accomodate as much as 4 dimensions and will be
        reffered to as evrsion 2
        #######################################################################
        """
        
        #We build a while loop able to be broken and throwing out the error
        #This is dependant on which section of the import fails
        Broken = False
        
        while not Broken:
        
        
            #We are going to log the eintire process and then exit the process
            LastAct = ''
            slip = False
        
            #We selected a file now load it and find the instance 'Dist' that marks the start
            try:
                #if it is a RAM file we need to decompress it
                if len(Path.split('.RAM')) > 1:
                    archive = zipfile.ZipFile(Path)
                    File = archive.open(Path.split(os.path.sep)[-1].split('.RAM')[0]+'.txt','r')
                
                else:
                    #open it
                    File      = open(Path, 'r')
                    skip      = True
                
                #reformat that shit real quick
                Read = []
                i = 0
                
                for Line in File:
                    Read.append(Line.strip())
                
                #Set the path as self
                self.Path = Path
                
                #The file is no longer recquired
                File.close()
        
            except:
                LastAct += '\nCould not load the file as the path seems broken, aborting...'
                break
            
            #Initialise the line numbers for parameter storage
            FoundIdx     = [None]*6
            XArray       = []
            self.Version = 0
            
            #Initialise two strings used to determine the information position
            RamanData  = 'Raman Data'
            SampleData = 'Sample Data'
            self.RamInfo    = '**Raman_Information**'
            self.SamInfo    = '**Sample_Information**'
            
            #Go through lines and find the text strings indicating th estructure
            for i in range(0,len(Read)):
                
                #Split the line open over spaces
                SplitLine = Read[i].split(' ')
                
                ######################################################################
                #Find the raman and sample informations
        
                #find raman data
                if SplitLine[0] == '**Raman_Information**':
                    FoundIdx[0] = i
                    LastAct += '\nFound the Raman Information section in the selected file:\nLine number '+str(i)+', proceeding...'
                        
                #find the sample information
                if SplitLine[0] == '**Sample_Information**':
                    FoundIdx[1] = i
                    LastAct += '\nFound the Sample Information section in the selected file:\nLine number '+str(i)+', proceeding...'
                
                
                ######################################################################
                #Find the header Data

                #find the Y data positions in case the file is still version 1
                if SplitLine[0] == 'Dist':

                    #write the position
                    FoundIdx[2] = i
                    
                    #Set the version
                    self.Version = 1
                    
                    #Send it out
                    LastAct += '\nThe input file version is v.1.0'
                    LastAct += '\nFound Y parameter:\nLine number'+str(i)+', proceeding...'
                
                else:
                    
                    #Cycle through the split line to find the markers
                    for j in range(0,len(SplitLine)):
                        
                        #if found Z
                        if SplitLine[j] == 'DistZ':
                            FoundIdx[2] = i
                            self.Version = 2
                            LastAct += '\nThe input file version is v.2.0'
                        
                        #if found X
                        if SplitLine[j] == 'DistX':
                            FoundIdx[3] = i
                                
                        #if found Y
                        if SplitLine[j] == 'DistY':
                            FoundIdx[4] = i
                                
                        #if found T
                        if SplitLine[j] == 'DistT':
                            FoundIdx[5] = i
    
                ######################################################################
                #Initialise the X array
                
                #try to initialise the Xarray first column of data
                if i > FoundIdx[2] and self.Version == 1:
                    try:
                        add = float(Read[i].split(' ')[0])
                        XArray.append(add)
                    except:
                        pass
                            
                #try to initialise the Xarray first column of data
                if i > FoundIdx[5] and self.Version == 2:
                    try:
                        add = float(Read[i].split(' ')[0])
                        XArray.append(add)
                    except:
                        pass
        
            try:
                #Initiate the X class
                self.X = XAxis(XArray)
            except:
                pass
            
            ######################################################################
            #Load the version 1 file
            if self.Version == 1:
                

                #Please not that the version 1 format was only handling depth profiles
                #A new version of the data writer will be writen to support the new
                #multi-dimensional arrays up to 4 dimensions.
                
                #Initiate
                YList = []
                YCompute = []
                
                #get the values for Z and transform them into float:
                for i in range(1,len(Read[FoundIdx[2]].split())):
                    YCompute.append(float(Read[FoundIdx[2]].split()[i]))
                
                YList.append(YCompute)#Z is computed
                YList.append([None])#X space is none
                YList.append([None])#Y space is none
                
                #Create axis, we will have to simulate X and Y
                self.Y = YAxis(YList)
        
                #Create the temperature class
                self.T = TAxis([None])


            ######################################################################
            #Load the version 2 file
            elif self.Version == 2:

                #Initiate
                YList    = []
                TList    = []
                
                
                #go through the 3 lines of the postion
                for j in range(2,5):
                    
                    #Reset compute
                    YCompute = []
                    
                    for i in range(1,len(Read[FoundIdx[j]].split(' '))):
                        try:
                            YCompute.append(float(Read[FoundIdx[j]].split(' ')[i]))
                        except:
                            pass


                    YList.append(YCompute)
        
                
                #Create axis, we will have to simulate X and Y
                self.Y = YAxis(YList)


                for i in range(1,len(Read[FoundIdx[5]].split(' '))):
                    try:
                        TList.append(float(Read[FoundIdx[5]].split(' ')[i]))
                    except:
                        pass

                #Create the temperature class
                self.T = TAxis(TList)

            ######################################################################
            #Load Single type
            else:
                self.Version = 10
                LastAct += '\nThe input file version is unknow, must be single measurement...'
                #break


            ######################################################################
            #Define the Array we will populate
            try:
                ZArray = numpy.zeros((self.X.dim,self.Y.dim[0],self.Y.dim[1],self.Y.dim[2],self.T.dim))
                LastAct += '\nCreated the input array with right dimentionality, proceeding...'

            except:
                LastAct += '\nCould not create right array, internal error, must be single...'
            

            ######################################################################
            #Read the data

            #initiate parameter u
            u      = 0
            Offset = 0

            #go through all lines
            for line in Read:
                
                #strip the actual line
                line = line.strip()
                
                #replace the end of the line (will cause problems in reading numbers
                line = line.replace('\t',' ', 1)
                
                #if it's the first line we get the data type
                if u == 0:
                    
                    #account for components/score files
                    try:
                        self.Type = line.split(' ')[1]
                        self.HeadStrEx = line
                        LastAct += '\nDetermined that the file type is: '+self.Type
            
                    except:
                        Offset = 1
                        self.HeadStrEx = ''
                        self.Type = 'Single'
                        LastAct += '\nDetermined that the file type is: '+self.Type
                        
                
                #Extract the header information
                if u == 1+Offset:
                    
                    #Make it search vital information
                    HeadStrR  = re.compile('This file was generated from the Wire file: (.*?) at ')
                    HeadStrM  = HeadStrR.search(line)
                    
                    #Assign the two vital headerstrings
                    self.HeadStr   = HeadStrM.group(1)
                    self.HeadStrEx += '\n'+line

                
                
                if u == 2+Offset:
                    
                    self.HeadStrEx = self.HeadStrEx+'\n'+line
                ######################################################################
                #Raman Information
                if u >= FoundIdx[0]+1 and u < FoundIdx[1]:
                    RamanData += '**'+line
                    self.RamInfo    += '\n'+line
            
                #Sample information
                if u >= FoundIdx[1]+1 and u < FoundIdx[1]+6:
                    SampleData += '**'+line
                    self.SamInfo    += '\n'+line
                            
                try:
                    
                    ######################################################################
                    #Data extraction of Intensities
                    if self.Version == 1:
                    
                        if u > FoundIdx[2]:
                            k = 0
                            columns = line.split()
                            
                            #The Z array in space
                            for t in Range(0,self.T.dim):

                                #The Y array in space
                                for g in Range(0,self.Y.dim[2]):
                                    
                                    #The X array in space
                                    for h in Range(0,self.Y.dim[1]):
                                    
                                        #The Z array in space
                                        for j in Range(0,self.Y.dim[0]):
                                            
                                            #assign data
                                            ZArray[u-FoundIdx[2]-1,j,h,g,t] = float(columns[k+1])
                                            k += 1

                    ######################################################################
                    if self.Version == 2:
                        
                        if u > FoundIdx[5]:
                            k = 0
                            columns = line.split()
                            
                            #The Z array in space
                            for t in Range(0,self.T.dim):

                                #The Y array in space
                                for g in Range(0,self.Y.dim[2]):
                                    
                                    #The X array in space
                                    for h in Range(0,self.Y.dim[1]):
                                    
                                        #The Z array in space
                                        for j in Range(0,self.Y.dim[0]):
                                            
                                            #assign data
                                            ZArray[u-FoundIdx[5]-1,j,h,g,t] = float(columns[k+1])
                                            k += 1
                except:
                    #if it fails the local place is empty, how convenient :p
                    pass
                
                #move the index up by a notch
                u += 1


        
        
            break
                
        ######################################################################
        #single file handling
        if self.Version == 10:
            XData,YData,Act = Utility.ReadSingleFile(Path)
            
            #create and populate
            ZArray = numpy.zeros((len(XData),1,1,1,1))
            ZArray[:,0,0,0,0] = YData[:]
            
            self.Z = ZAxis(ZArray)
            self.X = XAxis(XData)
            self.T = TAxis([None])
        else:
            #Initiate the Zdata class
            self.Z = ZAxis(ZArray)


        LastAct += '\nSuceeded at initialising the multi dim. data array.'
        self.isLoaded = True
        
        #logging purpose
        LastAct += '\nWe successfully imported the file: '+Path
        LastAct += '\nNow we will proceed to the data Info treatment, proceeding...'
        LastAct += self.SetRaman(RamanData)
        LastAct += self.SetSample(SampleData)
        LastAct += self.SetTitle()
        LastAct += self.SampleInfoInit()
        
        self.Information = DataInfo.Info()
        self.isinfo      = True
        
        '''
        ###########################################################################################
        We are now done importing the data. We have now 5 main instances created
        
        INSTANCES:
        self.Z data array as nupy array in 4 dimentions [wavenumber,Z,X,Y]
        self.X data list basically the wevenumbers denoted as X in the entire script
        self.Y data list of lists as the positions of our data points in space
        
        self.Title instance used as header in most visualisations
        self.Info instance used as call for information
        
        VARIABLES:
        self.HeadStrEx
        self.HeadStr
        self.Path
        self.Version
        The rest will be discarded as the function ends now. 
        
        the dump function will function in a similar way but build the strings and dump them 
        accordingly. We will write the dump function in a way that it can also work as converter
        ###########################################################################################
        '''
        
        return LastAct

    def SetRaman(self,Input):
        """
        ###########################################################################################        
        This function will connvert the feeded information into Raman Inforations callable 
        in the class
        ###########################################################################################
        """
        
        #Create two strings as when we created the Data: Type of info, value, unit
        InputSplit = Input.split('**')
        InputLines = len(InputSplit)

        #Initialise arrays
        self.RamanID    = [0]*InputLines
        self.RamanVal   = [0]*InputLines
        self.RamanUn    = [0]*InputLines
        
        for i in range(1,len(InputSplit)):
            
            #Split line
            Info = InputSplit[i]
            TempInput = Info.split(' ')
            
            #check something
            if len(TempInput)<2:
                pass
            else:
            
                #Insert values
                self.RamanID[i]   = TempInput[0]
                self.RamanVal[i]  = TempInput[1]
                self.RamanUn[i]   = TempInput[2]
        
        #Load into local class variables
        self.RamLaser     = self.RamanVal[Utility.RetIdx('Laser'   ,self.RamanID)[0]]
        self.RamPower     = self.RamanVal[Utility.RetIdx('Power'   ,self.RamanID)[0]]
        self.RamGrating   = self.RamanVal[Utility.RetIdx('Grating' ,self.RamanID)[0]]
        self.RamObjectif  = self.RamanVal[Utility.RetIdx('Objectif',self.RamanID)[0]]
        self.RamTime      = self.RamanVal[Utility.RetIdx('Time'    ,self.RamanID)[0]]
        self.RamAcqisi    = self.RamanVal[Utility.RetIdx('N._Acqu.',self.RamanID)[0]]

        #For log purposes
        LastAct = '\nSet the Raman Data.'

        return LastAct

       
    def SetSample(self,Input):
        """
        ###########################################################################################        
        This function will connvert the feeded information into Raman Inforations callable 
        in the class
        ###########################################################################################
        """
        
        #Create two strings as when we created the Data: Type of info, value, unit
        InputSplit = Input.split('**')
        InputLines = len(InputSplit)
        
        #Initialise arrays
        self.SampleID    = [0]*InputLines
        self.SampleVal   = [0]*InputLines
        
        for i in range(1,len(InputSplit)):
            
            #Split line
            TempInput = InputSplit[i].split(' ')
            
            #Insert values
            self.SampleID[i]   = TempInput[0]
            self.SampleVal[i]  = TempInput[1]
        
        #Load into local class variables
        self.SamID       = self.SampleVal[Utility.RetIdx('Sample_ID',self.SampleID)[0]]
        self.SamSample   = self.SampleVal[Utility.RetIdx('Sample'   ,self.SampleID)[0]]
        self.SamSubstr   = self.SampleVal[Utility.RetIdx('Substr'   ,self.SampleID)[0]]
        self.SamSamInf   = self.SampleVal[Utility.RetIdx('Sam._Inf.',self.SampleID)[0]]
        self.SamSubInf   = self.SampleVal[Utility.RetIdx('Sub._Inf.',self.SampleID)[0]]

        #For log purposes
        LastAct = '\nSet the Sample Data'
    
        return LastAct
            
    def SetTitle(self):
        
        """
        ###########################################################################################        
        Build the title of the plot automatically
        This requires:
        - SetRaman
        - SetSample
        to run prior to execution
        ###########################################################################################
        """
        
        self.Title  = 'Data Identifier: '+self.HeadStr +Utility.Ret()
        self.Title += 'Raman Info: '+self.RamLaser+'nm '+self.RamPower+'p '
        self.Title += self.RamGrating+'cm-1 '+self.RamObjectif+'x '+self.RamAcqisi+'x'+self.RamTime+'s'+Utility.Ret()
        self.Title += 'Sample Info: '+str(self.SamID)+' '+str(self.SamSample)+' ('+str(self.SamSamInf)+') on '+str(self.SamSubstr)+' ('+str(self.SamSubInf)+')'
        
        #for log purpose
        LastAct = '\nThe Title was computed'
        
        return LastAct
    
    def SampleInfoInit(self):
    
        """
        #######################################################################
        Go through the info and send it to the info class and set gloabal
        This is to have a script wide accessible info of the data
        #######################################################################
        """
        
        #if the data exists delete it before initialising
        self.Info = DataInfo.Info()
        
        
        #Set values
        self.Info.Root = str(self.Path)
        
        #File Path
        self.Info.SampleInfoID.append('Folder Path')
        self.Info.SampleInfoVal.append(str(self.Path))
        self.Info.SampleInfoUnit.append(None)
        
        #Main inout file
        self.Info.SampleInfoID.append('Wire File')
        self.Info.SampleInfoVal.append(self.HeadStr)
        self.Info.SampleInfoUnit.append(None)
        
        #Creation time
        self.Info.SampleInfoID.append('Proccessing time')
        self.Info.SampleInfoVal.append(self.HeadStrEx.split(' at ')[1].split('\nThe first column')[0])
        self.Info.SampleInfoUnit.append(None)
        
        #Data type
        self.Info.SampleInfoID.append('Data Type')
        self.Info.SampleInfoVal.append(str(self.Type))
        self.Info.SampleInfoUnit.append(None)
        
        #Number of average measurements
        self.Info.SampleInfoID.append('Number of Measurements')
        try:
            self.Info.SampleInfoVal.append(str(self.Y.Num))
        except:
            #single measurement
            self.Info.SampleInfoVal.append(str(1))

        self.Info.SampleInfoUnit.append(None)

        #Number of Acquisitions per measurements
        self.Info.SampleInfoID.append('Number of Acquisitions')
        self.Info.SampleInfoVal.append(str(self.RamAcqisi))
        self.Info.SampleInfoUnit.append('x')
        
        #Time per Acquisition
        self.Info.SampleInfoID.append('Duration per Acquisitions')
        self.Info.SampleInfoVal.append(str(self.RamTime))
        self.Info.SampleInfoUnit.append('s')
        
        #Laser wavelength
        self.Info.SampleInfoID.append('Laser Wavelength')
        self.Info.SampleInfoVal.append(str(self.RamLaser))
        self.Info.SampleInfoUnit.append('nm')
        
        #Laser power
        self.Info.SampleInfoID.append('Laser Power')
        self.Info.SampleInfoVal.append(str(self.RamPower))
        self.Info.SampleInfoUnit.append('percent')
        
        #Gratting
        self.Info.SampleInfoID.append('Grating used')
        self.Info.SampleInfoVal.append(str(self.RamAcqisi))
        self.Info.SampleInfoUnit.append('cm-1')
        
        #Objectif
        self.Info.SampleInfoID.append('Objectif used')
        self.Info.SampleInfoVal.append(str(self.RamObjectif))
        self.Info.SampleInfoUnit.append('x')
        
        #Z
        self.Info.SampleInfoID.append('Z range')
        try:
            if not self.Y.Y[0] == [None]:
                
                #We can set the values
                self.Info.SampleInfoVal.append(str(self.Y.YMin[0])+' to '+str(self.Y.YMax[0]))
                self.Info.SampleInfoUnit.append('micrometer')
            
            else:
            
                #We don't set values
                self.Info.SampleInfoVal.append('Fixed')
                self.Info.SampleInfoUnit.append(None)
        except:
            self.Info.SampleInfoVal.append('Fixed')
            self.Info.SampleInfoUnit.append(None)
        
        #X
        self.Info.SampleInfoID.append('X range')
            
        try:
            if not self.Y.Y[1] == [None]:
            
                #We can set the values
                self.Info.SampleInfoVal.append(str(self.Y.YMin[1])+' to '+str(self.Y.YMax[1]))
                self.Info.SampleInfoUnit.append('micrometer')
            
            else:
            
                #We don't set values
                self.Info.SampleInfoVal.append('Fixed')
                self.Info.SampleInfoUnit.append('micrometer')

        except:
            self.Info.SampleInfoVal.append('Fixed')
            self.Info.SampleInfoUnit.append('micrometer')

        #Y
        self.Info.SampleInfoID.append('Y range')
            
        try:
            if not self.Y.Y[2] == [None]:
                
                #We can set the values
                self.Info.SampleInfoVal.append(str(self.Y.YMin[2])+' to '+str(self.Y.YMax[2]))
                self.Info.SampleInfoUnit.append('micrometer')
            
            else:
            
                #We don't set values
                self.Info.SampleInfoVal.append('Fixed')
                self.Info.SampleInfoUnit.append('micrometer')

        except:
            self.Info.SampleInfoVal.append('Fixed')
            self.Info.SampleInfoUnit.append('micrometer')
        #T
        self.Info.SampleInfoID.append('Temperature range')
        try:
            if not self.T.T == [None]:
                
                #We can set the values
                self.Info.SampleInfoVal.append(str(self.T.Min)+' to '+str(self.T.Max))
                self.Info.SampleInfoUnit.append('Kelvin')
            
            else:
            
                #We don't set values
                self.Info.SampleInfoVal.append('Room Temp')
                self.Info.SampleInfoUnit.append('Kelvin')

        except:
            #We don't set values
            self.Info.SampleInfoVal.append('Room Temp')
            self.Info.SampleInfoUnit.append('Kelvin')
        
        #Raman Range
        self.Info.SampleInfoID.append('Raman Range')
        self.Info.SampleInfoVal.append(str(self.X.XMin)+' to '+str(self.X.XMax))
        self.Info.SampleInfoUnit.append('cm-1')
        
        #Sample ID
        self.Info.SampleInfoID.append('Sample ID')
        self.Info.SampleInfoVal.append(str(self.SamID))
        self.Info.SampleInfoUnit.append(None)
        
        #Sample name
        self.Info.SampleInfoID.append('Sample Name')
        self.Info.SampleInfoVal.append(str(self.SamSample))
        self.Info.SampleInfoUnit.append(None)
        
        #Sample characteristic
        self.Info.SampleInfoID.append('Sample info')
        self.Info.SampleInfoVal.append(str(self.SamSamInf))
        self.Info.SampleInfoUnit.append(None)
        
        #Substrate name
        self.Info.SampleInfoID.append('Substrate name')
        self.Info.SampleInfoVal.append(str(self.SamSubstr))
        self.Info.SampleInfoUnit.append(None)
        
        #substrate charact
        self.Info.SampleInfoID.append('Substrate info')
        self.Info.SampleInfoVal.append(str(self.SamSubInf))
        self.Info.SampleInfoUnit.append(None)
        
        #time per acquisition
        self.Info.SampleInfoID.append('Number of Acquisitions')
        self.Info.SampleInfoVal.append(str(self.RamAcqisi))
        self.Info.SampleInfoUnit.append(None)
        
        #for log purpose
        LastAct = '\nSample information loaded into appropriate class'
        
        return LastAct

class ZAxis:
    """
    #######################################################################
    This is the data class and basically the intensity.
    #######################################################################
    """
    def __init__(self,NumpyArray):
        try:
            self.Z = NumpyArray
            LastAct = '\nSuccessfully initialised Z'
        except:
            LastAct = '\nUnsuccessfull at loading Z'

    def getSpectraAtIdx(self,IdxArray,Spec, Range = None):
        
        #introduced temperature later on to avoid compatibility problems
        if len(IdxArray) == 3:
            IdxArray = numpy.append(IdxArray,[0],axis = 0)
        
        
        #fetch the array
        if Range == None:
            if Spec == 0:
                Spectrum = self.Z[:,IdxArray[0],IdxArray[1],IdxArray[2],IdxArray[3]]
            elif Spec == 1:
                Spectrum = self.Z[IdxArray[0],:,IdxArray[1],IdxArray[2],IdxArray[3]]
            elif Spec == 2:
                Spectrum = self.Z[IdxArray[0],IdxArray[1],:,IdxArray[2],IdxArray[3]]
            elif Spec == 3:
                Spectrum = self.Z[IdxArray[0],IdxArray[1],IdxArray[2],:,IdxArray[3]]
            elif Spec == 4:
                Spectrum = self.Z[IdxArray[0],IdxArray[1],IdxArray[2],IdxArray[3],:]
            else:
                Spectrum = None
            #return the array
            return Spectrum
    
        else:
            if Spec == 0:
                Spectrum = self.Z[Range[0]:Range[1],IdxArray[0],IdxArray[1],IdxArray[2],IdxArray[3]]
            elif Spec == 1:
                Spectrum = self.Z[IdxArray[0],Range[0]:Range[1],IdxArray[1],IdxArray[2],IdxArray[3]]
            elif Spec == 2:
                Spectrum = self.Z[IdxArray[0],IdxArray[1],Range[0]:Range[1],IdxArray[2],IdxArray[3]]
            elif Spec == 3:
                Spectrum = self.Z[IdxArray[0],IdxArray[1],IdxArray[2],Range[0]:Range[1],IdxArray[3]]
            elif Spec == 4:
                Spectrum = self.Z[IdxArray[0],IdxArray[1],IdxArray[2],IdxArray[3],Range[0]:Range[1]]
            else:
                Spectrum = None
            
            return Spectrum
            
    #One step further than get spectra is get datapoint :) just a single value
    def getDataPoint(self,IdxArray):

        #introduced temperature later on to avoid compatibility problems
        if len(IdxArray) == 4:
            IdxArray = numpy.append(IdxArray,[0],axis = 0)
        
        DataPoint = self.Z[:,IdxArray[1],IdxArray[2],IdxArray[3],IdxArray[4]]
        
        return DataPoint


class XAxis:
    """
    #######################################################################
    This is the data class and basically the wavenumber and will be a 
    single list. this is the most basic data structure.
    #######################################################################
    """
    def __init__(self,List):
        try:
            self.X = List
            LastAct = '\nSuccessfully initialised X'
            self.dim = len(self.X)
        except:
            print '\nUnsuccessfull at loading X'

        #Compute min and max of items
        self.XMin = numpy.min(self.X)
        self.XMax = numpy.max(self.X)

    def getIdx(self,Val):

        try:
            #Catch the idx for the value
            idx = Utility.FindIdx2(Val,self.X)
            LastAct = '\nSuccessfully retrieved the idx of datapoint'
        
        except:
            print '\nDimension unknown please check the value, aborting...'

        return idx,LastAct

class TAxis:
    """
    #######################################################################
    This class shares the structures with the X axis class but is dedicated
    to the temperature variable
    #######################################################################
    """
    def __init__(self,List):
        
        #if empty
        if len(List) == 0:
            List = [None]
        
        #try to fill it
        try:
            self.T = List
            LastAct = '\nSuccessfully initialised X'
            self.dim = len(self.T)
        except:
            print '\nUnsuccessfull at loading T'

        #Compute min and max of items
        self.TMin = numpy.min(self.T)
        self.TMax = numpy.max(self.T)

    def getIdx(self,Val):

        try:
            #Catch the idx for the value
            idx = Utility.FindIdx2(Val,self.T)
            LastAct = '\nSuccessfully retrieved the idx of datapoint'
        
        except:
            print '\nDimension unknown please check the value, aborting...'

        return idx,LastAct

class YAxis:
    """
    #######################################################################
    This will be the spacial steps
    it is initialised with a List
    
    List[0] should contain the depth (so Z)
    List[1] should contain the X position
    List[2] should contain the Y position
    
    Note that both other dimensions can be left empty
    
    getIdx is set to retrieve the index for a deimension. Note that the
    Idx is inportant to retrieve the associated Z values stored in Zaxis.
    comapred to X it will recquire the specification of the dimensionality
    being investigated.
    #######################################################################
    """
    def __init__(self,List):
        
        #Define the data array
        self.Y = [None]*3
        
        
        #if empty
        if len(List[0]) == 0:
            List[0] = [None]
        if len(List[1]) == 0:
            List[1] = [None]
        if len(List[2]) == 0:
            List[2] = [None]
        
        
        #try to define Z
        try:
            self.Y[0] = List[0]
        except:
            self.Y[0] = [None]

        #try to define X
        try:
            self.Y[1] = List[1]
        except:
            self.Y[1] = [None]

        #try to define X
        try:
            self.Y[2] = List[2]
        except:
            self.Y[3] = [None]

        #Introduce dimensionality as a default call
        try:
            self.dim = [len(self.Y[0]),len(self.Y[1]),len(self.Y[2])]
        except:
            print 'Dimentionallity failed, should not happen...'

        #Total number of points (measurements)
        self.Num = len(self.Y[0])*len(self.Y[1])*len(self.Y[2])

        #Compute min and max of items
        self.YMin = [numpy.min(self.Y[0]),numpy.min(self.Y[1]),numpy.min(self.Y[2])]
        self.YMax = [numpy.max(self.Y[0]),numpy.max(self.Y[1]),numpy.max(self.Y[2])]
        
    def getIdx(self,Val):
        
        
        """
        #######################################################################
        Can be used if only one index is recquired same functioning as 
        GetMultIdx
        #######################################################################

        try:
            #Catch the idx for the value
            #idx = Utility.FindIdx2(Val,self.Y[Dim])
            LastAct = '\nSuccessfully retrieved the idx of datapoint'

        except:
            LastAct = '\nDimension unknown please check the value, aborting...'

        return idx,LastAct

        """
        pass

    def getMultIdx(self,ValArray):
        
        """
        #######################################################################
        We want a fucntion capable of geting all associated index values
        
        you enter three positions as arguments and become the three associated
        indexes that you can then send to the ZAxis instance as is immidiately
        
        so getSpectraAtIdx(getMultIdx(ValArray)[0]) can be called as is
        #######################################################################
        """

        try:
            #Catch the idx for the value
            idx = [0]*3
            
            #Go through input array
            for i in range(0,3):
                try:
                    idx[i] = int(Utility.FindIdx2(ValArray[i],self.Y[i]))
                except:
                    pass
    
            LastAct = '\nSuccessfully retrieved the idx of datapoint in space'

        except:
            LastAct = '\nDimension unknown please check the value, aborting...'

        return idx[0],idx[1],idx[2],LastAct

class FigureManager:

    def __init__():
        pass

class VisualComponentHandler:

    def __init__(self,DataClass):
        """
        #######################################################################
        This class is written to handle the components from both PCA and NMF
        This allows for easier code handling afterwards as the source class
        will be the same throughout the code.
        #######################################################################
        """
        
        #make link to access data class backwards
        self.DataClass = DataClass
        self.Type = self.DataClass.Type
        
        #when the class is barely created it will be empty. To avoid conflict...
        isReady = False
    
        #Lines and grid
        self.LineOn = True
        self.GridOn = True


    def BuildOutput(self,CompNum,ax,bx,inverter):
        '''
        #######################################################################
        This function will build the selected output depending on two which 
        component is called. Note that the ouput will return a subplot
        
        the component data is stored in:
        
        The datatype is actualy depth and the scores will be treated as 1 D
        Note that this is the easiest case and could be treated along the case
        of lines X and Y Maybe it will...
        #######################################################################
        '''
    
        if self.Type == 'Depth' or self.Type == 'Temperature':
        
            #calculate coordinates
            X = self.PCX
            Y = float(inverter)*self.PC[CompNum]
            Y = Y.tolist()
            
            #reset it
            ax.Reset()
            
            #add the info
            ax.AddPlot(X,
                       Y,
                       color = 'blue',
                       Thickness = 2)
            
            #draw it
            ax.Zoom()
            
            #process it
            
            
#                #Does the user want a line at 0 ?
#                if self.LineOn:
#                    CompSubPlot.axhline(inverter*numpy.mean(self.PC[CompNum]), color ='k',linewidth=1)
#            
#                    #Log it
#                    LastAct = '\nProcessed lines, proceeding...'
#                
#                #Correct the range
#                CompSubPlot.set_xlim([numpy.min(self.PCX), numpy.max(self.PCX)])
#                
#                #Log it
#                LastAct = '\nProcessed view range, proceeding...'
#                
#                #Set the grid
#                if self.GridOn:
#                    CompSubPlot.xaxis.grid(True,'major',linewidth=1,color='k')
#                    CompSubPlot.yaxis.grid(True,'major',linewidth=1,color='k')
#                    
#                    #Log it
#                    LastAct = '\nProcessed grid, proceeding...'

            #process the score
            #Note that we are in the depth class so no special treatment is recquired
            #this will be different for highre class elements
            
            #calculate coordinates
            X = numpy.asarray(self.ScoreX)
            X = X[:,0].tolist()
            X1 = X[0]
            X2 = X[len(X)-1]
            self.Y  = self.DataClass.Y.Y[0][X1:X2+1]
            
            X = self.Y
            Y = float(inverter)*self.Score[CompNum]
            Y = Y.tolist()
            
            #prepare the subplot
            bx.Reset()
            
            #add the info
            bx.AddPlot(X,
                       Y,
                       color = 'blue',
                       Thickness = 2)
                       
            #process it
            bx.Zoom()

#                #Does the user want a line at 0 ?
#                if self.LineOn:
#                    ScoreSubplot.axhline(0, color ='k',linewidth=1)
#                
#                    #Log it
#                    LastAct = '\nProcessed lines, proceeding...'
#                        
#                #Set the grid
#                if self.GridOn:
#                    ScoreSubplot.xaxis.grid(True,'major',linewidth=1,color='k')
#                    ScoreSubplot.yaxis.grid(True,'major',linewidth=1,color='k')
#        
#                    #Log it
#                    LastAct = '\nProcessed grid, proceeding...'



class PCAClass:

    def __init__(self,DataClass):
        
        #Load dataclass as self to allow backward injection
        self.DataClass = DataClass
        
        #Load the dataclass type into local class
        self.Type = DataClass.Type
        
        #We load the PCA calculation dependencies locally here
        self.Calc = pca(None, copy = True, whiten = False)
        #this initialises the pca calculation class and allows it to be called
        #by self.Calc.function() or by Data.PCA.Calc.function() outside of the class
        
        """
        #######################################################################
        Initialise eventual PCA or data manipulation arrays
        We initialise this part as the userr might not be fundamentally
        interested in the croping he just chose for the data processing
        #######################################################################
        """
        #Satte parameter
        self.PCAInit      = True
        self.PCASelect    = False
        self.Croped       = False
        
        #Initilise log variable
        LastAct = '\nInitialised boolean variables, proceeding...'
        
        #Initial croping boundaries (ill cause problems)
        self.CropIdxi = [0]*8
        
        self.CropIdxi[0] = 0
        self.CropIdxi[1] = len(DataClass.X.X)-1
        self.CropIdxi[2] = 0
        self.CropIdxi[3] = len(DataClass.Y.Y[0])-1
        self.CropIdxi[4] = 0
        self.CropIdxi[5] = len(DataClass.Y.Y[1])-1
        self.CropIdxi[6] = 0
        self.CropIdxi[7] = len(DataClass.Y.Y[2])-1
        
        #Will caus eproblems when otherht than 'Depth'
        self.CropVali = [0]*8
        
        self.CropVali[0] = DataClass.X.X[self.CropIdxi[0]]
        self.CropVali[1] = DataClass.X.X[self.CropIdxi[1]]
        self.CropVali[2] = DataClass.Y.Y[0][self.CropIdxi[2]]
        self.CropVali[3] = DataClass.Y.Y[0][self.CropIdxi[3]]
        self.CropVali[4] = DataClass.Y.Y[1][self.CropIdxi[4]]
        self.CropVali[5] = DataClass.Y.Y[1][self.CropIdxi[5]]
        self.CropVali[6] = DataClass.Y.Y[2][self.CropIdxi[6]]
        self.CropVali[7] = DataClass.Y.Y[2][self.CropIdxi[7]]

        LastAct      += '\nSet the cropping values'
        
        #Copy the second set for ediitng
        self.CropIdx  = numpy.copy(self.CropIdxi)
        self.CropVal  = numpy.copy(self.CropVali)
        
        #Log it
        LastAct         += '\nProcessed the cropping index, proceeding...'
        
        """
        #######################################################################
        Here we initialise the visual characteristic of the PCA plot.
        This includes:
        - Grid
        - Figure height and width
        - Title
        - Information box
        #######################################################################
        """
        #Do we want to inverse the data visualisation
        self.DataClass.VCH.InversePC   = [1,1,1,1]
        
        #Log it
        LastAct         += '\nSet the visual inverters, proceeding...'
        
        #Tick index
        self.PCATickStepX = 100
        self.PCATickStepY = 2
        
        #Log it
        LastAct         += '\nSet the tick steps, proceeding...'
        
        #Grid parameters (obsolete)
        self.PCAPutGrid   = False
        self.PCAGridCol   = ""
        self.PCAGridL     = 0
        
        #Log it
        LastAct         += '\nSet estethics, proceeding...'
        
        #Figure height and width
        self.PCAFigWidth  = 16
        self.PCAFigHeight = 10

        #Log it
        LastAct         += '\nSet figure dimensions, proceeding...'
        
        #Define the initial upper and lower (first representation always spectral)
        self.Lower = [DataClass.X.XMin,DataClass.Y.YMin[0],DataClass.Y.YMin[1],DataClass.Y.YMin[2]]
        self.Upper = [DataClass.X.XMax,DataClass.Y.YMax[0],DataClass.Y.YMax[1],DataClass.Y.YMax[2]]
        
        #Log it
        LastAct         += '\nSet the initial boundaries for PCA, proceeding...'
    
    
    
        #It is imperative to know that when an axis is deactivated like in a
        #depth scan the value of the axis ill be [None] this throws an error
        #wehn trying to retrieve the Idx So we make an activation routine
        self.Activeset = [True,True,True,True]
        
        ZZ = self.DataClass.Y.Y[0]
        XX = self.DataClass.Y.Y[1]
        YY = self.DataClass.Y.Y[2]
        TT = self.DataClass.T.T
        
        if ZZ == [None]:
            self.Activeset[0] = False
        if XX == [None]:
            self.Activeset[1] = False
        if YY == [None]:
            self.Activeset[2] = False
        if TT == [None]:
            self.Activeset[3] = False
        
        del ZZ,XX,YY,TT
        
        #Initiate the first projection building
        LastAct += self.BuildPCASet()
        
        #Log it
        LastAct         += '\nExited building process normally, proceeding...'
    
        #Set the boolean state
        DataClass.isPCA = True
    
        #Log it
        LastAct         += '\nSent out the process, proceeding...'
    
        print LastAct
    
    def BuildPCASet(self):

        """
        #######################################################################
        This is a partial copy of the build projection routine. The difference
        is that we do not want a projection. In contrary we want a a reasonable
        folowwing of the spectral data. So instead of jumping on edges, we want
        a smooth boundary. There will be one main parameter which will go from
        his min and max. the second will oscilate back and ofrth at each
        iteration of this parameter. The last will then again oscillate back and
        forth at each iteration. This should result in a smooth PCA map. For 
        the verision 1 files this has no impact at all as we will simply
        read the Z array one way.
        
        #######################################################################
        """
        #Take the upper and lower from self
        Lower = self.Lower
        Upper = self.Upper
        
        #Locally load the data, X and Y [0,1,2] and perform some checking
        Omega = self.DataClass.X.X
        
        Z = self.DataClass.Y.Y[0]
        X = self.DataClass.Y.Y[1]
        Y = self.DataClass.Y.Y[2]

        
        #For loging purposes
        LastAct  = '\nTransfered the dimensions from the dataclass'
        LastAct += '\nDetermined the activeset of dimensions'
        
        #Note that in the current version [0] is Z [1] is X and [2] is Y
        #in space, again this is due to historical development reasons
    
        #Build two numpy arrays
        Val = numpy.zeros((5,2))
        Idx = numpy.zeros((5,2))

        #Build the value array line
        Val[0,:] = [Lower[0],Upper[0]]
        Val[1,:] = [Lower[1],Upper[1]]
        Val[2,:] = [Lower[2],Upper[2]]
        Val[3,:] = [Lower[3],Upper[3]]
            
        #For loging purposes
        LastAct += '\nExtracted boundaries'

        #Get the index values from space and from X
        Idx[0,0],Buffer = self.DataClass.X.getIdx(Lower[0])
        
        #log it
        LastAct += Buffer
        
        Idx[0,1],Buffer = self.DataClass.X.getIdx(Upper[0])
        
        #log it
        LastAct += Buffer
        
        Idx[1,0],Idx[2,0],Idx[3,0],Buffer = self.DataClass.Y.getMultIdx(Lower[1:3])
        Idx[1,1],Idx[2,1],Idx[3,1],Buffer = self.DataClass.Y.getMultIdx(Upper[1:3])
        
        #Log it
        LastAct += Buffer
        
        #Perform corrections if activeset is false
        for i in range(1,len(self.Activeset)+1):
            if not self.Activeset[i-1]:
                Idx[i,:] = None
        
        #Log it
        LastAct += '\nPerformed corrections depending on the activeset'
        
        
        '''
        #######################################################################
        The last section was simply all the extratctions of the border and
        some other logic computations. Now we will perform the actual Data 
        creation.
        
        
        the output will be a 3D X array a 3D Y array a 3D Z array and finnaly 
        a 4D spectral aaray.
        
        the output will be a 3D ZXY array and the 1D arrays
        will serve as index matrix to transit from one to the other
        
        [Z1 X1 Y1] ->index
        [Z1 X1 Y2]
             .
             .
             .
             
        #######################################################################
        '''
        
        PCAYIdx = []
        
        #go through Z loop
        for i in Range(Idx[1,0],Idx[1,1]+1):
            
            ZIdx = i
        
            #go through X loop
            for j in Range(Idx[2,0],Idx[2,1]+1):
                
                XIdx = j
        
                #go through Y loop
                for k in Range(Idx[3,0],Idx[3,1]+1):
        
                    YIdx = k
                
                    PCAYIdx.append([ZIdx,YIdx,XIdx,0])
        
        LastAct += '\nSuccessfully built the PCA index array, proceeding...'
        
        #Build Z with the get spectra method of Z class
        #Build the 2D intensity map
        #initiate Z
        Z = []
                
        #Catch Z from the data
        A =  int(numpy.min([Idx[0,0],Idx[0,1]]))
        B =  int(numpy.max([Idx[0,0],Idx[0,1]]))
                 
        for i in Range(0,len(PCAYIdx)):
                 Z.append(self.DataClass.Z.getSpectraAtIdx(PCAYIdx[i],0)[A:B])
            
        #Send as array to have numpy support
        Z = numpy.asarray(Z)
        
        #transpose for historical reason
        Z = Z.transpose()
        
        #log it
        LastAct += '\nSuccesfully created the Data array, proceeding...'
        
        
        #Package and send it
        self.PCADataSet = [self.DataClass.X.X[A:B],PCAYIdx,Z]
        
        #Duplicate for reset conditions
        self.PCADataSetInit = numpy.copy(self.PCADataSet)
        
        #log it
        LastAct += '\nSuccessfully packaged the data ready to initiate graphical framework.'
        
        #print LastAct
        
        return LastAct
            
    def RunPCACalculation(self):
        
        """
        #######################################################################
        Imported as is from version 1. Note that minor adjustements were done
        to allow dor the adaptability
        #######################################################################
        """

        #initialise the PCA class
        PCAInput = numpy.transpose(self.PCADataSet[2])
        
        #log it
        LastAct = '\nFormated to for PCA calculations, proceeding...'
        
        #Perform the PCA
        self.Calc.fit(PCAInput)
        
        #log it
        LastAct = '\nCalculated PCA, proceeding...'
        
        #Now we can gether the components and the scores
        self.DataClass.VCH.PC      = self.Calc.Components
        self.DataClass.VCH.PCX     = self.PCADataSet[0]
        self.DataClass.VCH.Score   = self.Calc.Scores
        self.DataClass.VCH.ScoreX  = self.PCADataSet[1]
        self.DataClass.VCH.isReady = True
        
        self.DataClass.VCH.s = [None]*3
        self.DataClass.VCH.s[0] = self.Calc.ExplainedVariance
        self.DataClass.VCH.s[1] = self.Calc.ExplainedVarianceRatio
        self.DataClass.VCH.s[1] = self.Calc.ExplainedVarianceRatio_1
        
        #log it
        LastAct = '\nTransfered result to the appropriate class, proceeding...'
        
        return LastAct

    def SetCroping(self,Type = 'PCA'):
        
        """
        #######################################################################
        This function is a modified version of the function from
        #######################################################################
        """
        
        #Loop variable for safe exit
        Exit = 0
        
        #Initialise parameters
        CropVal = [0,0,0,0]
        CropIdx = [0,0,0,0]
        
        #Log Variable
        LastAct = ''
        
        #Loop for wavenumber (always ask)
        #Start the loop askign for user input and exited on satifactory conditions or user abort
        while Exit == 0:
            
            #Send out request
            Input = Utility.Request('PCA_10',Data = self.DataClass)
            CropIdx = self.CropIdx
            
            if Input == "R":

                #The user wants to Reset al boundaries
                self.CropIdx  = self.CropIdxi
                
                #Send out log 
                LastAct = 'The User decided to reset the Data Boundaries'
            
                    
                #Job done exit
                Exit = 1
                
            elif Input[0] == "-":
                
                #The user gave up exit this stage witout modification
                Exit = 1
                
            else:     
                
                #Now we need this 
                InputSplit = Input
                
                if len(InputSplit) == 2:
                    if float(InputSplit[0])<float(InputSplit[1]):
                        if float(InputSplit[0])>=self.CropVali[1] and float(InputSplit[1])<=self.CropVali[0]:
                            
                            #Convert user entries into floating point values from string
                            self.CropVal[0] = float(InputSplit[0])
                            self.CropVal[1] = float(InputSplit[1])
                            
                            self.Lower[0] = self.CropVal[0]
                            self.Upper[0] = self.CropVal[1]
                            
                            #Initiate search for these values and their associated index
                            self.CropIdx[0] = Utility.FindIdx2(CropVal[0],self.DataClass.X.X)
                            self.CropIdx[1] = Utility.FindIdx2(CropVal[1],self.DataClass.X.X)

                            #Job done exit
                            Exit = 1
                            
                        else:
                            VisOut.TextBox(Text = 'ERROR: Range out of initial Boundaries',state = 0)
                    else:
                        VisOut.TextBox(Text = 'ERROR: Invalid range order',state = 0)
                else:
                    VisOut.TextBox(Text = 'ERROR: Invalid data format',state = 0)
                
                #Write the action to a log file
                LastAct = '\nThe user set the Croping Values for Data to: '
             
            #Loop for Z (only ask when it is depth, Zslice or volume measurement)
            if self.Type == 'Depth' or self.Type == 'ZSlice' or self.Type == 'Volume' or self.Type == 'Temperature':
            
            
                Exit = 0
                #Start the loop askign for user input and exited on satifactory conditions or user abort
                while Exit == 0:
                    
                    #Send out request
                    Input = Utility.Request('PCA_11',Data = self.DataClass)
                    CropIdx = self.CropIdx
                    
                    if Input == "R":

                        #The user wants to Reset al boundaries
                        self.CropIdx  = self.CropIdxi
                        
                        #Send out log 
                        LastAct = 'The User decided to reset the Data Boundaries'
                    
                            
                        #Job done exit
                        Exit = 1
                        
                    elif Input[0] == "-":
                        
                        #The user gave up exit this stage witout modification
                        Exit = 1
                        
                    else:     
                        
                        #Now we need this 
                        InputSplit = Input
                        
                        if len(InputSplit) == 2:
                            if float(InputSplit[0])<float(InputSplit[1]):
                                if float(InputSplit[0])>=self.CropVali[2] and float(InputSplit[1])<=self.CropVali[3]:
                                    
                                    #Convert user entries into floating point values from string
                                    self.CropVal[2] = float(InputSplit[0])
                                    self.CropVal[3] = float(InputSplit[1])
                                    
                                    self.Lower[1] = self.CropVal[2]
                                    self.Upper[1] = self.CropVal[3]
                                    
                                    #Initiate search for these values and their associated index
                                    self.CropIdx[2] = Utility.FindIdx2(CropVal[2],self.DataClass.Y.Y[0])
                                    self.CropIdx[3] = Utility.FindIdx2(CropVal[3],self.DataClass.Y.Y[0])

                                    #Job done exit
                                    Exit = 1
                                    
                                else:
                                    VisOut.TextBox(Text = 'ERROR: Range out of initial Boundaries',state = 0)
                            else:
                                VisOut.TextBox(Text = 'ERROR: Invalid range order',state = 0)
                        else:
                            VisOut.TextBox(Text = 'ERROR: Invalid data format',state = 0)
                        
                        #Write the action to a log file
                        LastAct = '\nThe user set the Croping Values for Data to: '
                            
                #Loop for X (only ask when it is depth, Zslice or volume measurement)
                if self.Type == 'XYLine' or self.Type == 'ZSlice' or self.Type == 'Volume' or self.Type == 'Temperature':
                    pass
                #Loop for Y (only ask when it is depth, Zslice or volume measurement)
                if self.Type == 'XYLine' or self.Type == 'ZSlice' or self.Type == 'Volume' or self.Type == 'Temperature':
                    pass
                        
        #proceed computation:
        self.BuildPCASet()
        
        return LastAct


    def Remove(self,CompNum):
        """
        ###########################################################################################        
        Remove single components from the Data or a list of them
        CompNum should be passed as a list
        
        WARNING: permanently chnages the dataset. Needs to be reset to come back to original
        ###########################################################################################
        """
        #buffer in the data
        ZDATA = numpy.copy(self.PCADataSet[2]).transpose()
        
        #transpose it
        
        #start the loop over components
        for i in range(0,len(ZDATA)):
        
            #get the mean value
            PCAInputMean = numpy.mean(ZDATA[i])
            
            #calculate array
            DataMeanSub = ZDATA[i]-PCAInputMean
        
            #Go through components and remove it
            for j in range(0,len(CompNum)):
                
                DataMeanSub = (DataMeanSub-self.DataClass.VCH.PC[CompNum[j]]*self.DataClass.VCH.Score[CompNum[j]][i])
    
            ZDATA[i] = DataMeanSub+PCAInputMean
        
        #Send it out
        self.PCADataSet[2] = ZDATA.transpose()

    def Export(self):
        """
        ###########################################################################################        
        This will export the current Dataset part of the loadRaw routine. 
        As such specific ajustements should be done. Note that the export routine is Datatype 
        dependent and therefore should be updated soon.
        
        This will include the new write routine
        ###########################################################################################
        """
        
        
        #input 0 is depth measurement -> rest to come
        #if self.Type == 'Depth' or self.Type == 'Temperature':
        
        
        #write the coordinates
        #check Z
        if self.Activeset[0]:
            Z    = [self.DataClass.Y.Y[0][self.PCADataSet[1][i][0]] for i in range(0,len(self.PCADataSet[1]))]
            Zidx = [self.PCADataSet[1][i][0] for i in range(0,len(self.PCADataSet[1]))]
        else:
            Z = [None]
        
        #check X
        if self.Activeset[1]:
            X    = [self.DataClass.Y.Y[1][self.PCADataSet[1][i][1]] for i in range(0,len(self.PCADataSet[1]))]
            Xidx = [self.PCADataSet[1][i][1] for i in range(0,len(self.PCADataSet[1]))]
        else:
            X = [None]
        
        #check Y
        if self.Activeset[2]:
            Y    = [self.DataClass.Y.Y[2][self.PCADataSet[1][i][2]] for i in range(0,len(self.PCADataSet[1]))]
            Yidx = [self.PCADataSet[1][i][2] for i in range(0,len(self.PCADataSet[1]))]
        else:
            Y = [None]
        
        #check T
        if self.Activeset[3]:
            T    = [self.DataClass.T.T[self.PCADataSet[1][i][3]] for i in range(0,len(self.PCADataSet[1]))]
            Tidx = [self.PCADataSet[1][i][3] for i in range(0,len(self.PCADataSet[1]))]
        
        else:
            T = [None]

        #check omega
        omega = numpy.copy(self.PCADataSet[0])

        #Take the Data
        Data = numpy.copy(self.PCADataSet[2])

        #Prep the write header
        self.HeadStr,self.HeadStrEx = Utility.PrepWrite(self.DataClass.Path,self.Type)

        #Set tail
        Tail = 'NoiseProc'

        #Send it out
        Utility.Write2FileV2(self.DataClass,Data,Z,X,Y,T,self.Activeset,omega,Tail)



class ContourClass:
    
    def __init__(self,DataClass):
    
        #We need to transfer a few informations from the data class into the Contour Class
        self.Type = DataClass.Type
    
        
        """
        #######################################################################
        Here we initialise the visual characteristic of the data plot. 
        This includes:
        - Grid
        - Figure height and width
        - Title
        - Information box
        #######################################################################
        """
        
        #transmit the instance into the contour class
        self.DataClass = DataClass
        
        #Grid parameters
        self.PutGrid   = False
        self.GridCol   = ""
        self.GridL     = 0
        
        #Figure height and width
        self.FigWidth  = 10
        self.FigHeight = 12
    
        #Define the initial upper and lower (first representation always spectral)
        self.Lower = [DataClass.X.XMin,DataClass.Y.YMin[0],DataClass.Y.YMin[1],DataClass.Y.YMin[2], DataClass.T.TMin]
        self.Upper = [DataClass.X.XMax,DataClass.Y.YMax[0],DataClass.Y.YMax[1],DataClass.Y.YMax[2], DataClass.T.TMax]
        
        
    
        #It is imperative to know that when an axis is deactivated like in a
        #depth scan the value of the axis ill be [None] this throws an error
        #wehn trying to retrieve the Idx So we make an activation routine
        self.Activeset = [True,True,True,True]
        
        ZZ = self.DataClass.Y.Y[0]
        XX = self.DataClass.Y.Y[1]
        YY = self.DataClass.Y.Y[2]
        TT = self.DataClass.T.T
        
        if ZZ == [None]:
            self.Activeset[0] = False
        if XX == [None]:
            self.Activeset[1] = False
        if YY == [None]:
            self.Activeset[2] = False
        if TT == [None]:
            self.Activeset[3] = False
        
        del ZZ,XX,YY,TT
        
        #Initiate the first projection building
        self.BuildProjection()
    
        #Set the boolean state
        DataClass.isContour = True

    def BuildProjection(self,Option = 'Omega'):

        """
        #######################################################################
        Building the projection used in the visualisation framework
        We have these builders to create depending on the initial class and
        on what the user wants to see.
        
        The user
        
        Spectral representation:
        Z depth scan (build first)
        XY line scan
        XYZ line scan
        
        XY Map
        
        
        
        the output wwill always be:
        
        ZContour -> the intensity map
        XContour -> the X axis
        YContour -> the Y axis
        
        XYContourDependance -> how X and Y relate to X and Y from the dataclass
        
        #######################################################################
        """
    
        #Locally load the data, X and Y [0,1,2] and perform some checking
        Omega = self.DataClass.X.X
        
        Z = self.DataClass.Y.Y[0]
        X = self.DataClass.Y.Y[1]
        Y = self.DataClass.Y.Y[2]

        #For loging purposes
        LastAct  = '\nTransfered the dimensions from the dataclass'
        LastAct += '\nDetermined the activeset of dimensions'
        
        #Note that in the current version [0] is Z [1] is X and [2] is Y
        #in space, again this is due to historical development reasons
    
        #Build two numpy arrays
        Val      = numpy.zeros((5,2))
        self.Idx = numpy.zeros((5,2))

        #Build the value array line
        Val[0,:] = [self.Lower[0],self.Upper[0]]
        Val[1,:] = [self.Lower[1],self.Upper[1]]
        Val[2,:] = [self.Lower[2],self.Upper[2]]
        Val[3,:] = [self.Lower[3],self.Upper[3]]
            
        #For loging purposes
        LastAct += '\nExtracted boundaries'

        #Get the index values from space and from X
        self.Idx[0,0],Buffer = self.DataClass.X.getIdx(self.Lower[0])
        
        #log it
        LastAct += Buffer
        
        self.Idx[0,1],Buffer = self.DataClass.X.getIdx(self.Upper[0])
        
        #log it
        LastAct += Buffer
        
        self.Idx[1,0],self.Idx[2,0],self.Idx[3,0],Buffer = self.DataClass.Y.getMultIdx(self.Lower[1:3])
        self.Idx[1,1],self.Idx[2,1],self.Idx[3,1],Buffer = self.DataClass.Y.getMultIdx(self.Upper[1:3])
        
        #Log it
        LastAct += Buffer
        
        #Perform corrections if activeset is false
        for i in range(1,len(self.Activeset)+1):
            if not self.Activeset[i-1]:
                self.Idx[i,:] = None

        #Log it
        LastAct += '\nPerformed corrections depending on the activeset'


        '''
        #######################################################################
        option comes in as it will tell us which dimension to display as X and
        which dimensions to display as Y. bascally we will fold 3 dimensions
        into 1 and leave the last one as such. So we need a folding matrix
         X       Y
        [0]  [0][0][0]
        [1]  [1][0][0]
        [2]  [2][0][0]
        
        Y will be built from a custome Value array that will be created through
        the divistion of the longest Note that the mixing of omega makes only
        sense in one point so anyway self.Idx[0,0] = self.Idx[0,1] in canse this component 
        is selected. Actually in this case only two vectors will egt mixed from
        space and omega stays unchnaged.
        #######################################################################
        '''
        #build the ranges with the custome range function
        if Option == 'Omega':
            #The user decided to compress all but the omega arrray
            X = Omega[int(numpy.min(self.Idx[0,:]))-1:int(numpy.max(self.Idx[0,:]))]
            X = numpy.asarray(X)
            
            #Now we construct the Y array, first check longest in termes of index
            Max = 0
            for i in Range(1,4):
                
                #if it is bigger
                if numpy.abs(self.Idx[i,1]-self.Idx[i,0]) > Max:
                    Max     = numpy.abs(self.Idx[i,1]-self.Idx[i,0])
                    Longest = i
        
            #Log it
            LastAct += '\nThe Longest space dimention is: '+str(Longest)
            
            #Steps
            StepZ  = (Val[1,1]-Val[1,0])/Max
            StepX  = (Val[2,1]-Val[2,0])/Max
            StepY  = (Val[3,1]-Val[3,0])/Max
            
            Max += 1
            #Log it
            LastAct += '\nComputed the steping for the virtual axis'
            
            print 'This is the maximum: '+str(Max)
            #Axis
            YIdxList = [None]*(Max)
            YValList = [None]*(Max)
            
            #Compute it
            for i in Range(0,int(Max)):
                YValList[i] = [Val[1,0]+i*StepZ,Val[2,0]+i*StepX,Val[3,0]+i*StepY]
                A,B,C       = self.DataClass.Y.getMultIdx(YValList[i])[0:3]
                YIdxList[i] = [A,B,C]
            
            #remove None from array
            YValList_Array = numpy.nan_to_num(YValList)
            YIdxList_Array = numpy.asarray(YIdxList)

            #Create virtual distances
            Y = []
            for i in Range(0,int(Max)):
                Y.append(numpy.sqrt((YValList_Array[i,0]-YValList_Array[0,0])**2+(YValList_Array[i,1]-YValList_Array[0,1])**2+(YValList_Array[i,2]-YValList_Array[0,2])**2))
            
            
            #Convert to numpy array object
            Y = numpy.asarray(Y)
            
            #log it
            LastAct += '\nSuccessfully computed new virtual axis'
            
            #Build the 2D intensity map
            if self.Type == 'Depth' or self.Type == 'Temperature':
                
                #initiate Z
                Z = []
                RangeFetch = [int(numpy.min(self.Idx[0,:]))-1,int(numpy.max(self.Idx[0,:]))]
                
                #Catch Z from the data
                for i in Range(0,int(Max)):
                    Z.append(self.DataClass.Z.getSpectraAtIdx(YIdxList_Array[i],0,Range = RangeFetch))
                
                
                #Send as array to have numpy support
                Z = numpy.asarray(Z)
                
                #transpose for historical reason of the contour management
                Z = Z.transpose()
                
                #log it
                LastAct += '\nSuccesfully created the Data array'
    
    
            #Package and send it
            try:
                del self.Projection
            except:
                pass
            
            #new one in case old existed
            self.Projection = [X,Y,Z]
            
            #log it
            LastAct += '\nSuccessfully packaged the data ready to initiate graphical framework'


        else:
            print 'Condition not met'
    
        return LastAct

            
            
    def InitiateContour(self):
    
        """
        #######################################################################
        in this version 2 we have separated the contour PCA and NMF data
        capabilities in different classes. Note that this will also allow the 
        whole system to switch between all three instances in a seemingless 
        manner
        
        The passed on data projection should be only 3 dimentional
        Projection[0] should be the X axis computed (relative)
        Projection[1] should be the Y axis computed (relative)
        Projection[2] should be the intensity map for these points
        
        #######################################################################
        """
        
        #Initiate log output
        LastAct = ''
        
        #Data of object
        self.Z        = self.Projection[2]
        LastAct      += '\nImported the Data dimension'
        
        #Row information
        self.X        = self.Projection[0]
        self.XLen     = len(self.X)
        LastAct      += '\nImported the X dimension'
        
        #Column information
        self.Y        = self.Projection[1]
        self.YLen     = len(self.Y)
        LastAct      += '\nImported the Y dimension'
        
        #Initial croping boundaries
        self.CropIdxi = [0,len(self.X)-1,0,len(self.Y)-1]
        self.CropVali = [self.X[self.CropIdxi[0]],self.X[self.CropIdxi[1]],self.Y[self.CropIdxi[2]],self.Y[self.CropIdxi[3]]]
        LastAct      += '\nSet the cropping values'
        
        #Copy the second set for ediitng
        self.CropIdx  = numpy.copy(self.CropIdxi)
        self.CropVal  = numpy.copy(self.CropVali)
        LastAct      += '\nCopied the cropping values into editing array'
        
        #Initial color Map boundaries     
        self.ColorMapIni   = [self.X[self.CropIdxi[0]],self.X[self.CropIdxi[1]],self.Y[self.CropIdxi[2]],self.Y[self.CropIdxi[3]]]
        self.ColorMap      = numpy.copy(self.ColorMapIni)
        self.ColorMapCor   = [1,1]
        LastAct      += '\nSet the colomap parameters'
        
        #initialise the tick routine. Note that here we have to check a reasonable tick
        #dependign on the field of view
        
        #For X
        if numpy.max(self.X)-numpy.min(self.X) > 30:
            self.TickStepX = 100
        else:
            self.TickStepX = 2
        LastAct      += '\nSet the ticks for X'
        
        #For Y
        if numpy.max(self.Y)-numpy.min(self.Y) > 30:
            self.TickStepY = 100
        else:
            self.TickStepY = 2
        LastAct      += '\nSet the ticks for Y'
        
        #Create uncroped contour
        self.SetContour(Type = 'Data')
        LastAct      += '\nSurvived the contour building method'
        
        #Save these values for navigation view
        #They will not change anymore
        self.XSPlot = self.XPlot
        self.YSPlot = self.YPlot
        self.ZSPlot = self.ZPlot
        LastAct      += '\nassigned visual data'
  

        return LastAct

    def InitiateContourSpecial(self):
    
        """
        #######################################################################
        in this version 2 we have separated the contour PCA and NMF data
        capabilities in different classes. Note that this will also allow the 
        whole system to switch between all three instances in a seemingless 
        manner
        
        The passed on data projection should be only 3 dimentional
        Projection[0] should be the X axis computed (relative)
        Projection[1] should be the Y axis computed (relative)
        Projection[2] should be the intensity map for these points
        
        #######################################################################
        """
        
        #Initiate log output
        LastAct = ''
        
        #Data of object
        self.Z        = self.Projection[2]
        LastAct      += '\nImported the Data dimension'
        
        #Row information
        self.X        = self.Projection[0]
        self.XLen     = len(self.X)
        LastAct      += '\nImported the X dimension'
        
        #Column information
        self.Y        = self.Projection[1]
        self.YLen     = len(self.Y)
        LastAct      += '\nImported the Y dimension'
        
        #Initial croping boundaries
        self.CropIdx = [0,len(self.X)-1,0,len(self.Y)-1]
        self.CropVal = [self.X[self.CropIdx[0]],self.X[self.CropIdx[1]],self.Y[self.CropIdx[2]],self.Y[self.CropIdx[3]]]
        LastAct      += '\nSet the cropping values'
        
        #Initial color Map boundaries     
        self.ColorMap      = numpy.copy(self.ColorMapIni)
        self.ColorMapCor   = [1,1]
        LastAct      += '\nSet the colomap parameters'
        
        #initialise the tick routine. Note that here we have to check a reasonable tick
        #dependign on the field of view

        
        #Create uncroped contour
        self.SetContour(Type = 'Data')
        
        LastAct      += '\nSurvived the contour building method'
        LastAct      += '\nassigned visual data'
  

        return LastAct

    def SetTick(self,Type = 'Data'):
        """
        #######################################################################
        This function will be called on the class when ticks need to be updated
        This allows for better tick management after croping
        #######################################################################
        """
        if Type == 'Data':
            self.XTicks    = self.TickBuilder(numpy.min(self.XPlot),numpy.max(self.XPlot),self.TickStepX)
            self.YTicks    = self.TickBuilder(numpy.min(self.YPlot),numpy.max(self.YPlot),self.TickStepY)
            
        if Type == 'PCA':
            self.XPCATicks = self.TickBuilder(numpy.min(self.XPCA),numpy.max(self.XPCA),self.PCATickStepX)
            self.YPCATicks = self.TickBuilder(numpy.min(self.YPCA),numpy.max(self.YPCA),self.PCATickStepY)
            


    def SetCroping(self,Type = 'Data'):
        
        """
        #######################################################################
        This function will compute the indexes needed for the crop.
        It searches in a methodic way the croping borders etc...
        
        This methods can comput croping for both the data and the pca map. 
        The initial croping values 'self.CropVali' are inherited automatically
        from the raw data as both should have the same starting conditions.
        #######################################################################
        """
        
        #Loop variable for safe exit
        Exit = 0
        
        #Initialise parameters
        CropVal = [0,0,0,0]
        CropIdx = [0,0,0,0]
        
        #Log Variable
        LastAct = ''
        
        #Start the loop askign for user input and exited on satifactory conditions or user abort
        while Exit == 0:
            
            #Send out request
            Input = Utility.Request('PCA_7',Data = self.DataClass)
            CropIdx = self.CropIdx
            
            if Input == "R":

                #The user wants to Reset al boundaries
                self.CropIdx  = self.CropIdxi
                
                #Send out log 
                LastAct = 'The User decided to reset the Data Boundaries'
            
                    
                #Job done exit
                Exit = 1
                
            elif Input[0] == "-":
                
                #The user gave up exit this stage witout modification
                Exit = 1
                
            else:     
                
                #needed this with old input method
                #InputSplit = Input.split(" ")
                
                #Now we need this 
                InputSplit = Input
                
                if len(InputSplit) == 4:
                    if float(InputSplit[0])<float(InputSplit[1]) and float(InputSplit[2])<float(InputSplit[3]):
                        if float(InputSplit[0])>=self.CropVali[1] and float(InputSplit[1])<=self.CropVali[0] and float(InputSplit[2])>=self.CropVali[2] and float(InputSplit[3])<=self.CropVali[3]:
                            
                            #Convert user entries into floating point values from string
                            CropVal[0] = float(InputSplit[0])
                            CropVal[1] = float(InputSplit[1])
                            CropVal[2] = float(InputSplit[2])
                            CropVal[3] = float(InputSplit[3])

                            #Initiate search for these values and their associated index
                            CropIdx[0] = Utility.FindIdx2(CropVal[0],self.X)
                            CropIdx[1] = Utility.FindIdx2(CropVal[1],self.X)
                            CropIdx[2] = Utility.FindIdx2(CropVal[2],self.Y)
                            CropIdx[3] = Utility.FindIdx2(CropVal[3],self.Y)
                            
                            #Job done exit
                            Exit = 1
                            
                            #For some reason I did not update the clas variable .... Let's do this for read out
                            self.CropVal = (CropVal[0],CropVal[1],CropVal[2],CropVal[3])
                            
                        else:
                            VisOut.TextBox(Text = 'ERROR: Range out of initial Boundaries', state = 0)
                    else:
                        VisOut.TextBox(Text = 'ERROR: Invalid range order', state = 0)
                elif len(InputSplit) == 2:
                    if float(InputSplit[0])<float(InputSplit[1]):
                        if float(InputSplit[0])>=self.CropVali[1] and float(InputSplit[1])<=self.CropVali[0]:
                            
                            #Convert user entries into floating point values from string
                            CropVal[0] = float(InputSplit[0])
                            CropVal[1] = float(InputSplit[1])
                            
                            #Initiate search for these values and their associated index
                            CropIdx[0] = Utility.FindIdx2(CropVal[0],self.X)
                            CropIdx[1] = Utility.FindIdx2(CropVal[1],self.X)

                            #Job done exit
                            Exit = 1
                            
                        else:
                            VisOut.TextBox(Text = 'ERROR: Range out of initial Boundaries',state = 0)
                    else:
                        VisOut.TextBox(Text = 'ERROR: Invalid range order',state = 0)
                else:
                    VisOut.TextBox(Text = 'ERROR: Invalid data format',state = 0)
                    

                    
                #Process the entries into the class variables
                self.CropIdx    = CropIdx
                
                #Write the action to a log file
                LastAct = '\nThe user set the Croping Values for Datato: '+str(CropVal[0])+' '+str(CropVal[1])+' '+str(CropVal[2])+' '+str(CropVal[3])
                    
                    
        return LastAct
                
    def SetContour(self,Type='Data'):
        
        #define visual arrays
        XPlot       = numpy.zeros((abs(self.CropIdx[1]-self.CropIdx[0])+1,abs(self.CropIdx[3]-self.CropIdx[2])+1))
        YPlot       = numpy.zeros((abs(self.CropIdx[1]-self.CropIdx[0])+1,abs(self.CropIdx[3]-self.CropIdx[2])+1))
        ZPlot       = numpy.zeros((abs(self.CropIdx[1]-self.CropIdx[0])+1,abs(self.CropIdx[3]-self.CropIdx[2])+1))
        FoundIdx    = numpy.zeros((abs(self.CropIdx[1]-self.CropIdx[0])+1,abs(self.CropIdx[3]-self.CropIdx[2])+1))
        
        #Create man min arrays to avoid recomputation on every iteration
        Array = [numpy.min([self.CropIdx[0],self.CropIdx[1]]),numpy.max([self.CropIdx[0],self.CropIdx[1]]),numpy.min([self.CropIdx[2],self.CropIdx[3]]),numpy.max([self.CropIdx[2],self.CropIdx[3]])]

        #fill Y visual arrays:
        for i in Range(Array[0],Array[1]+1):
            YPlot[i-Array[0],:] = self.Y[Array[2]:Array[3]+1]
        
        #Fill X visual arrays
        for j in Range(Array[2],Array[3]+1):
            XPlot[:,j-Array[2]] = numpy.transpose(self.X[Array[0]:Array[1]+1])

        #Fill Z
        ZPlot = self.Z[Array[0]:Array[1]+1,Array[2]:Array[3]+1]

        #Initialize some parameters
        self.ZBound = [0,0]
        
        ######################################################################################################
        #Now done in the windo management class
        Array = [numpy.min([self.ColorMap[0],self.ColorMap[1]]),numpy.max([self.ColorMap[0],self.ColorMap[1]]),numpy.min([self.ColorMap[2],self.ColorMap[3]]),numpy.max([self.ColorMap[2],self.ColorMap[3]])]
        
        #Start first loop
        for i in Range(0,abs(self.CropIdx[3]-self.CropIdx[2])-1):
            
            #Start second loop
            for g in Range(0,abs(self.CropIdx[1]-self.CropIdx[0])-1):
                                
                #Are we in the Z scale
                if ZPlot[g,i] < self.ZBound[0]:
                    self.ZBound[0] = ZPlot[g,i]
                                
                #Are we in the Z scale
                if ZPlot[g,i] > self.ZBound[1]:
                    self.ZBound[1] = ZPlot[g,i]
            
        #transmit to the class
        self.XPlot    = XPlot
        self.YPlot    = YPlot
        self.ZPlot    = ZPlot
        self.FoundIdx = FoundIdx
            
        #Create the appropriate tick maping
        self.SetTick(Type = 'Data')
         

                    
    def SetColor(self):
        
        
        """
        ###########################################################################################
        This function is here to ask for the range of the color visualisation. Note that it is 
        operation al only acts on self. But a Lastact method should be implemented...
        
        Also the request layout should be ported to version 2 interface.
        
        Fully functional version 2
        ###########################################################################################
        """
        
        #Set loop parameter to 0
        Exit = 0
        
        while Exit == 0:
            
            #Build the string
            print 'Specify either Coefficients or Range (use space between values)'
            
            #Save string for readibility
            A = str(round(numpy.min([self.ColorMapIni[0],self.ColorMapIni[1]])))
            B = str(round(numpy.max([self.ColorMapIni[0],self.ColorMapIni[1]])))
            C = str(round(numpy.min([self.ColorMapIni[2],self.ColorMapIni[3]])))
            D = str(round(numpy.max([self.ColorMapIni[2],self.ColorMapIni[3]])))
            
            #Build the string
            print 'Boundaries are:'+A+' to '+B+' and '+C+' to '+D
                                        
            Ask1 = raw_input()
            AskSplit = Ask1.split(" ")
            
            if Ask1 == "":
                Exit = 1
            else:
                
                if len(AskSplit) == 4:
                    if float(AskSplit[0])<float(AskSplit[1]):
                        
                        if float(AskSplit[2])<float(AskSplit[3]):
                            
                            if float(AskSplit[0])>=numpy.min([self.ColorMapIni[0],self.ColorMapIni[1]]):
                                
                                if float(AskSplit[1])<=numpy.max([self.ColorMapIni[0],self.ColorMapIni[1]]):
                                    
                                    if float(AskSplit[2])>=numpy.min([self.ColorMapIni[2],self.ColorMapIni[3]]):
                                        
                                        if float(AskSplit[3])<=numpy.max([self.ColorMapIni[2],self.ColorMapIni[3]]):
                                
                                            self.ColorMap[0] = float(AskSplit[0])
                                            self.ColorMap[1] = float(AskSplit[1]) 
                                            self.ColorMap[2] = float(AskSplit[2])
                                            self.ColorMap[3] = float(AskSplit[3])
                            
                                            Exit = 1
                                        else:
                                            VisOut.TextBox(Text ='ERROR: Range out of initial Boundaries', state = 0)
                                    else:
                                        VisOut.TextBox(Text ='ERROR: Range out of initial Boundaries', state = 0)
                                else:
                                    VisOut.TextBox(Text ='ERROR: Range out of initial Boundaries', state = 0)
                            else:
                                VisOut.TextBox(Text ='ERROR: Range out of initial Boundaries', state = 0)
                        else:
                            VisOut.TextBox(Text ='ERROR: Invalid range order', state = 0)
                    else:
                        VisOut.TextBox(Text ='ERROR: Invalid range order', state = 0)
            
                elif len(AskSplit) == 2:
                    if float(AskSplit[0])<float(AskSplit[1]):
                        
                        self.ColorMapCor[0] = float(AskSplit[0])
                        self.ColorMapCor[1] = float(AskSplit[1])
                        
                        Exit = 1
                    else:
                        VisOut.TextBox(Text = 'ERROR: Invalid range order', state = 0)
                else:
                    VisOut.TextBox(Text ='ERROR: Invalid data format', state = 0)
                
        LastAct = '\nThe user set the Color Values to: '+str(self.ColorMap[0])+' '+str(self.ColorMap[1])+' '+str(self.ColorMap[2])+' '+str(self.ColorMap[3])                  
        return LastAct


    def TickBuilder(self,Min,Max,Stepping):
        """
        ###########################################################################################        
        This function will build ticks with the ptoper interval between them.
        Min is the minimal boundary
        Max is the maximal boundary    
        Steping is the value between two consecutive ticks
        ###########################################################################################
        """
        
        #Loop parameters
        MaxTicks     = int(100000/Stepping)
        RawTicks     = numpy.zeros(MaxTicks)
        TicksIdx     = [0,0]
        
        #Ticks finding parameters
        FoundMinTick = 0
        FoundMaxTick = 0
        
        #Build Raw aray of ticks
        for i in range(0,MaxTicks):
            RawTicks[i] = float(Stepping*i-50000)
        
        #Find the range inside the array
        for Idx,Val in enumerate(RawTicks):
            
            if Val>=float(Min) and FoundMinTick==0:
                FoundMinTick = 1
                TicksIdx[0]  = Idx
                
            if Val>=float(Max) and FoundMaxTick==0:
                FoundMaxTick = 1
                TicksIdx[1]  = Idx
                
            
        #Assign Y Ticks to the whole figure   
        TickArray = RawTicks[range(TicksIdx[0],TicksIdx[1])]
   
        return TickArray
        



    
class NMFClass:
    
    def __init__(self,DataClass):
        
        #Load dataclass as self to allow backward injection
        self.DataClass = DataClass
        
        #Load the dataclass type into local class
        self.Type = DataClass.Type
        
        #this initialises the pca calculation class and allows it to be called
        #by self.Calc.function() or by Data.PCA.Calc.function() outside of the class
        
        """
        #######################################################################
        Initialise eventual PCA or data manipulation arrays
        We initialise this part as the userr might not be fundamentally
        interested in the croping he just chose for the data processing
        #######################################################################
        """
        #boolean Values
        self.Init          = False
        self.PickInit      = False
        self.PickInitScore = False
        
        #initialise algorythm definition
        self.Algo      = None
        self.alg_names = ['NMF_ANLS_BLOCKPIVOT','NMF_ANLS_AS_GROUP','NMF_ANLS_AS_NUMPY', 'NMF_HALS', 'NMF_MU']
        self.algs      = [ NMF_R.NMF_ANLS_BLOCKPIVOT , NMF_R.NMF_ANLS_AS_GROUP , NMF_R.NMF_ANLS_AS_NUMPY ,  NMF_R.NMF_HALS ,  NMF_R.NMF_MU ]
        
        #initialise the three NMF parameters
        self.k      = 0
        self.Iter   = 0
        self.Repeat = 0
        
        #Initialisation index
        self.CompInit  = []
        self.ScoreInit = []
        
        #Initialisation Values
        self.CompInitVal  = []
        self.ScoreInitVal = []
        
        #Loaded Components
        self.Loaded_Comps  = []
        self.Loaded_Scores = []
        
        #cpu info 
        self.cores = 2
        
        #Satte parameter
        self.PCAInit      = True
        self.PCASelect    = False
        self.Croped       = False
        
        #Initilise log variable
        LastAct = '\nInitialised boolean variables, proceeding...'
        
        #Initial croping boundaries (ill cause problems)
        self.CropIdxi = [0]*8
        
        self.CropIdxi[0] = 0
        self.CropIdxi[1] = len(DataClass.X.X)-1
        self.CropIdxi[2] = 0
        self.CropIdxi[3] = len(DataClass.Y.Y[0])-1
        self.CropIdxi[4] = 0
        self.CropIdxi[5] = len(DataClass.Y.Y[1])-1
        self.CropIdxi[6] = 0
        self.CropIdxi[7] = len(DataClass.Y.Y[2])-1
        
        #Will caus eproblems when otherht than 'Depth'
        self.CropVali = [0]*8
        
        self.CropVali[0] = DataClass.X.X[self.CropIdxi[0]]
        self.CropVali[1] = DataClass.X.X[self.CropIdxi[1]]
        self.CropVali[2] = DataClass.Y.Y[0][self.CropIdxi[2]]
        self.CropVali[3] = DataClass.Y.Y[0][self.CropIdxi[3]]
        self.CropVali[4] = DataClass.Y.Y[1][self.CropIdxi[4]]
        self.CropVali[5] = DataClass.Y.Y[1][self.CropIdxi[5]]
        self.CropVali[6] = DataClass.Y.Y[2][self.CropIdxi[6]]
        self.CropVali[7] = DataClass.Y.Y[2][self.CropIdxi[7]]

        LastAct      += '\nSet the cropping values'
        
        #Copy the second set for ediitng
        self.CropIdx  = numpy.copy(self.CropIdxi)
        self.CropVal  = numpy.copy(self.CropVali)
        
        #Log it
        LastAct         += '\nProcessed the cropping indexi, proceeding...'
        
        """
        #######################################################################
        Here we initialise the visual characteristic of the PCA plot.
        This includes:
        - Grid
        - Figure height and width
        - Title
        - Information box
        #######################################################################
        """
        #Do we want to inverse the data visualisation
        self.DataClass.VCH.InversePC   = [1,1,1,1]
        
        #Log it
        LastAct         += '\nSet the visual inverters, proceeding...'
        
        #Grid parameters (obsolete)
        self.PCAPutGrid   = False
        self.PCAGridCol   = ""
        self.PCAGridL     = 0
        
        #Log it
        LastAct         += '\nSet estethics, proceeding...'
        
        #Figure height and width
        self.PCAFigWidth  = 16
        self.PCAFigHeight = 10

        #Log it
        LastAct         += '\nSet figure dimensions, proceeding...'
        
        #Define the initial upper and lower (first representation always spectral)
        self.Lower = [DataClass.X.XMin,DataClass.Y.YMin[0],DataClass.Y.YMin[1],DataClass.Y.YMin[2]]
        self.Upper = [DataClass.X.XMax,DataClass.Y.YMax[0],DataClass.Y.YMax[1],DataClass.Y.YMax[2]]
        
        #Log it
        LastAct         += '\nSet the initial boundaries for PCA, proceeding...'
    
    
        #It is imperative to know that when an axis is deactivated like in a
        #depth scan the value of the axis ill be [None] this throws an error
        #wehn trying to retrieve the Idx So we make an activation routine
        
        self.Activeset = [True,True,True,True]
        
        ZZ = self.DataClass.Y.Y[0]
        XX = self.DataClass.Y.Y[1]
        YY = self.DataClass.Y.Y[2]
        TT = self.DataClass.T.T
        
        if ZZ == [None]:
            self.Activeset[0] = False
        if XX == [None]:
            self.Activeset[1] = False
        if YY == [None]:
            self.Activeset[2] = False
        if TT == [None]:
            self.Activeset[3] = False
        
        del ZZ,XX,YY,TT
        
        #Initiate the first projection building
        LastAct += self.BuildNMFSet()
        
        #Log it
        LastAct         += '\nExited building process normally, proceeding...'
    
        #Set the boolean state
        DataClass.isPCA = True
    
        #Log it
        LastAct         += '\nSent out the process, proceeding...'
    
        print LastAct
    
    def BuildNMFSet(self):

        """
        #######################################################################
        This is a partial copy of the build projection routine. The difference
        is that we do not want a projection. In contrary we want a a reasonable
        folowwing of the spectral data. So instead of jumping on edges, we want
        a smooth boundary. There will be one main parameter which will go from
        his min and max. the second will oscilate back and ofrth at each
        iteration of this parameter. The last will then again oscillate back and
        forth at each iteration. This should result in a smooth PCA map. For 
        the verision 1 files this has no impact at all as we will simply
        read the Z array one way.
        
        #######################################################################
        """
        #Take the upper and lower from self
        Lower = self.Lower
        Upper = self.Upper
        
        #Locally load the data, X and Y [0,1,2] and perform some checking
        Omega = self.DataClass.X.X
        
        Z = self.DataClass.Y.Y[0]
        X = self.DataClass.Y.Y[1]
        Y = self.DataClass.Y.Y[2]
        
        #For loging purposes
        LastAct  = '\nTransfered the dimensions from the dataclass'
        LastAct += '\nDetermined the activeset of dimensions'
        
        #Note that in the current version [0] is Z [1] is X and [2] is Y
        #in space, again this is due to historical development reasons
    
        #Build two numpy arrays
        Val = numpy.zeros((5,2))
        Idx = numpy.zeros((5,2))

        #Build the value array line
        Val[0,:] = [Lower[0],Upper[0]]
        Val[1,:] = [Lower[1],Upper[1]]
        Val[2,:] = [Lower[2],Upper[2]]
        Val[3,:] = [Lower[3],Upper[3]]
            
        #For loging purposes
        LastAct += '\nExtracted boundaries'

        #Get the index values from space and from X
        Idx[0,0],Buffer = self.DataClass.X.getIdx(Lower[0])
        
        #log it
        LastAct += Buffer
        
        Idx[0,1],Buffer = self.DataClass.X.getIdx(Upper[0])
        
        #log it
        LastAct += Buffer
        
        Idx[1,0],Idx[2,0],Idx[3,0],Buffer = self.DataClass.Y.getMultIdx(Lower[1:3])
        Idx[1,1],Idx[2,1],Idx[3,1],Buffer = self.DataClass.Y.getMultIdx(Upper[1:3])
        
        #Log it
        LastAct += Buffer
        
        #Perform corrections if activeset is false
        for i in range(1,len(self.Activeset)+1):
            if not self.Activeset[i-1]:
                Idx[i,:] = None
        
        #Log it
        LastAct += '\nPerformed corrections depending on the activeset'
        
        
        '''
        #######################################################################
        The last section was simply all the extratctions of the border and
        some other logic computations. Now we will perform the actual Data 
        creation.
        
        
        the output will be a 3D X array a 3D Y array a 3D Z array and finnaly 
        a 4D spectral aaray.
        
        the output will be a 3D ZXY array and the 1D arrays
        will serve as index matrix to transit from one to the other
        
        [Z1 X1 Y1] ->index
        [Z1 X1 Y2]
             .
             .
             .
             
        #######################################################################
        '''
        
        NMFYIdx = []
        
        #go through Z loop
        for i in Range(Idx[1,0],Idx[1,1]+1):
            
            ZIdx = i
        
            #go through X loop
            for j in Range(Idx[2,0],Idx[2,1]+1):
                
                XIdx = j
        
                #go through Y loop
                for k in Range(Idx[3,0],Idx[3,1]+1):
        
                    YIdx = k
                
                    NMFYIdx.append([ZIdx,YIdx,XIdx])
        
        LastAct += '\nSuccessfully built the PCA index array, proceeding...'
        
        #Build Z with the get spectra method of Z class
        #Build the 2D intensity map
        #initiate Z
        Z = []
                
        #Catch Z from the data
        A =  int(numpy.min([Idx[0,0],Idx[0,1]]))
        B =  int(numpy.max([Idx[0,0],Idx[0,1]]))

        
        for i in Range(0,len(NMFYIdx)):
                 Z.append(self.DataClass.Z.getSpectraAtIdx(NMFYIdx[i],0)[A:B])
            
        #Send as array to have numpy support
        Z = numpy.asarray(Z)
        
        #transpose for historical reason
        Z = Z.transpose()
        
        #log it
        LastAct += '\nSuccesfully created the Data array, proceeding...'
        
        
        #Package and send it
        self.NMFDataSet = [self.DataClass.X.X[A:B],NMFYIdx,Z]
        
        #Duplicate for reset conditions
        self.NMFDataSetInit = numpy.copy(self.NMFDataSet)
        
        #log it
        LastAct += '\nSuccessfully packaged the data ready to initiate graphical framework.'
        
        #print LastAct
        
        return LastAct
            
    def RunNMFCalculation(self):
        
        """
        #######################################################################
        NMF calculation routine
        
        #######################################################################
        """
        for i in range(0,len(self.alg_names)):
            if self.alg_names[i] == self.Algo:
                self.Algo = self.algs[i]()
                break
        
        #initialise the PCA class
        NMFInput = numpy.transpose(self.NMFDataSet[2])
        
        #set randomeness
        trialBest     = 0
        elapsedBest   = 0
        rel_errorBest = 1
        
        #run the NMF   
        if self.DataClass.NMF.Repeat == 0:
            Scores,Components,r = self.Algo.run(self.DataClass.NMF,NMFInput, 1 , trialBest,elapsedBest, rel_errorBest)
        else:
            Scores,Components,r = self.Algo.run_repeat(self.DataClass.NMF, NMFInput)

        try:
            del self.DataClass.VCH.PC,self.DataClass.VCH.PCX,self.DataClass.VCH.Score,self.DataClass.VCH.ScoreX
        except:
            print 'Was not able to delete variables that should exist'
            
        #Now we can gether the components and the scores
        self.DataClass.VCH.PC     = Components.transpose()
        self.DataClass.VCH.PCX    = self.NMFDataSet[0]
        
        self.DataClass.VCH.Score  = Scores.transpose()
        self.DataClass.VCH.ScoreX = self.NMFDataSet[1]
        
        
        #log it
        LastAct = '\nCalculated NMF, proceeding...'
        
        
        return LastAct

    def SetCroping(self,Type = 'PCA'):
        
        """
        #######################################################################
        This function is a modified version of the function from
        #######################################################################
        """
        
        #Loop variable for safe exit
        Exit = 0
        
        #Initialise parameters
        CropVal = [0,0,0,0]
        CropIdx = [0,0,0,0]
        
        #Log Variable
        LastAct = ''
        
        #Loop for wavenumber (always ask)
        #Start the loop askign for user input and exited on satifactory conditions or user abort
        while Exit == 0:
            
            #Send out request
            Input = Utility.Request('PCA_10',Data = self.DataClass)
            CropIdx = self.CropIdx
            
            if Input == "R":

                #The user wants to Reset al boundaries
                self.CropIdx  = self.CropIdxi
                
                #Send out log 
                LastAct = 'The User decided to reset the Data Boundaries'
            
                    
                #Job done exit
                Exit = 1
                
            elif Input[0] == "-":
                
                #The user gave up exit this stage witout modification
                Exit = 1
                
            else:     
                
                #Now we need this 
                InputSplit = Input
                
                if len(InputSplit) == 2:
                    if float(InputSplit[0])<float(InputSplit[1]):
                        if float(InputSplit[0])>=self.CropVali[1] and float(InputSplit[1])<=self.CropVali[0]:
                            
                            #Convert user entries into floating point values from string
                            self.CropVal[0] = float(InputSplit[0])
                            self.CropVal[1] = float(InputSplit[1])
                            
                            self.Lower[0] = self.CropVal[0]
                            self.Upper[0] = self.CropVal[1]
                            
                            #Initiate search for these values and their associated index
                            self.CropIdx[0] = Utility.FindIdx2(CropVal[0],self.DataClass.X.X)
                            self.CropIdx[1] = Utility.FindIdx2(CropVal[1],self.DataClass.X.X)

                            #Job done exit
                            Exit = 1
                            
                        else:
                            VisOut.TextBox(Text = 'ERROR: Range out of initial Boundaries',state = 0)
                    else:
                        VisOut.TextBox(Text = 'ERROR: Invalid range order',state = 0)
                else:
                    VisOut.TextBox(Text = 'ERROR: Invalid data format',state = 0)
                
                #Write the action to a log file
                LastAct = '\nThe user set the Croping Values for Data to: '
             
            #Loop for Z (only ask when it is depth, Zslice or volume measurement)
            if self.Type == 'Depth' or self.Type == 'ZSlice' or self.Type == 'Volume' or self.Type == 'Temperature':
            
            
                Exit = 0
                #Start the loop askign for user input and exited on satifactory conditions or user abort
                while Exit == 0:
                    
                    #Send out request
                    Input = Utility.Request('PCA_11',Data = self.DataClass)
                    CropIdx = self.CropIdx
                    
                    if Input == "R":

                        #The user wants to Reset al boundaries
                        self.CropIdx  = self.CropIdxi
                        
                        #Send out log 
                        LastAct = 'The User decided to reset the Data Boundaries'
                    
                            
                        #Job done exit
                        Exit = 1
                        
                    elif Input[0] == "-":
                        
                        #The user gave up exit this stage witout modification
                        Exit = 1
                        
                    else:     
                        
                        #Now we need this 
                        InputSplit = Input
                        
                        if len(InputSplit) == 2:
                            if float(InputSplit[0])<float(InputSplit[1]):
                                if float(InputSplit[0])>=self.CropVali[2] and float(InputSplit[1])<=self.CropVali[3]:
                                    
                                    #Convert user entries into floating point values from string
                                    self.CropVal[2] = float(InputSplit[0])
                                    self.CropVal[3] = float(InputSplit[1])
                                    
                                    self.Lower[1] = self.CropVal[2]
                                    self.Upper[1] = self.CropVal[3]
                                    
                                    #Initiate search for these values and their associated index
                                    self.CropIdx[2] = Utility.FindIdx2(CropVal[2],self.DataClass.Y.Y[0])
                                    self.CropIdx[3] = Utility.FindIdx2(CropVal[3],self.DataClass.Y.Y[0])

                                    #Job done exit
                                    Exit = 1
                                    
                                else:
                                    VisOut.TextBox(Text = 'ERROR: Range out of initial Boundaries',state = 0)
                            else:
                                VisOut.TextBox(Text = 'ERROR: Invalid range order',state = 0)
                        else:
                            VisOut.TextBox(Text = 'ERROR: Invalid data format',state = 0)
                        
                        #Write the action to a log file
                        LastAct = '\nThe user set the Croping Values for Data to: '
                            
                #Loop for X (only ask when it is depth, Zslice or volume measurement)
                if self.Type == 'XYLine' or self.Type == 'ZSlice' or self.Type == 'Volume' or self.Type == 'Temperature':
                    pass
                #Loop for Y (only ask when it is depth, Zslice or volume measurement)
                if self.Type == 'XYLine' or self.Type == 'ZSlice' or self.Type == 'Volume' or self.Type == 'Temperature':
                    pass
                        
        #proceed computation:
        self.BuildNMFSet()
        
        return LastAct
        


    def PickInitFunc(self,Data):
        
        #transfer array
        self.CompInitVal  = []
        self.ScoreInitVal = []
        
        #Reset
        self.CompInit  = []
        self.ScoreInit = []
        
        #go through elements
        for i in range(0,self.k):
            
            #Check
            try:
                #append comp values
                self.CompInitVal.append(self.Loaded_Comps[i]) 
                
                #Set
                self.CompInit.append(True)
                
                #The score addition needs to happen here if selected
                if self.PickInitScore:
                    
                    #go get the score
                    self.PickInitScoreFunc(i)
                    
                else:
                    
                    #else just append even tough it is useless (who knows what next)
                    self.ScoreInitVal.append(self.Loaded_Scores[i])
                
            except:
                
                #exception raises to put -1 in CompInit
                self.CompInit.append(False)
                
                #The score addition needs to happen here if selected
                if self.PickInitScore:
                    self.ScoreInit.append(False)
    
    
    def PickInitScoreFunc(self,i,Data):
        #pick the list of scores to add previously computed
        Pick = self.ScoreInit[i]
        
        #Initialise Sum
        Sum = Data.Score[Pick[1]]
        
        #Go through elements
        if len(Pick) > 1:
            for o in range(1,len(Pick)):
                
                #Sum scores
                Sum += Data.Score[Pick[o]]
                
        #append score values
        self.InitScoresVal.append(Sum)
