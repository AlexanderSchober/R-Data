# -*- coding: utf-8 -*-

print 'Loading Utility dependencies...'

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

#text string management
import re

#numpyy mathematical import
import numpy

#Date and time import
import datetime

#Import time function for files so they don't overwrite (writefig)
from time import gmtime, strftime

#matplotlib
import matplotlib

#set at launch the matplotlib import
matplotlib.use("TkAgg")

#backend for figure export
from matplotlib.backends.backend_pdf import PdfPages

import glob

#####################################
#advanced imports

#threading related imports
from threading import Thread, Event
from Queue import Queue

#function manipulation routines
from functools import *

#####################################
#Scipy imports

#scipy signal treatment routines
import scipy.signal as signal
import scipy.sparse as sparse
from scipy.sparse.linalg import spsolve
import scipy

#factorial import from math
from math import factorial

"""
##################################################
These are the custome imports
##################################################
"""

#The terminal viual manager
import Utility_Out      as VisOut


#File and system management routines
import Utility_File     as File



"""
###############################################################################
############################FILE MANAGEMENT####################################
###############################################################################
"""

  

#Create a class with the data  
class RequestFile:
    
    #initialising function will read in the file and set it as lists
    def __init__(self):
        
        #File and folder management
        import FileManagement
        
        #Set the folder Windows specific handling done within
        inTxt  = FileManagement.GetRuntimeTextFile(['DEFAULT_IO_RESOURCES.txt'])
        
        #Read the request text file
        Read = open(inTxt,'r')
        
        #Read lines
        Lines = Read.readlines()
        
        
        #Remove empty lines
        while Lines.count('\n') > 0:
            Lines.remove('\n')
        
        
        #Create the initial List
        self.RequestList = [None]*len(Lines)
        
        #Now save the Data as a list formats
        for i in range(0,len(Lines)):
            
            #We save three things into a list:
            Buffer = [None]*6
            
            #The ID
            Buffer[0] = Lines[i].split('<ID>')[1]    
            
            #The Text
            Buffer[1] = Lines[i].split('<TEXT>')[1]
            
            #The Text
            Buffer[2] = Lines[i].split('<NAME>')[1]
            
            #The default values
            Buffer[3] = Lines[i].split('<DEFAULT>')[1]
            
            #The allowed choices
            Buffer[4] = Lines[i].split('<CHOICE>')[1]
            
            #The recquired input length
            Buffer[5] = Lines[i].split('<LEN>')[1]
            
            #Save it
            self.RequestList[i] = Buffer
    
    #We want to be able to get only the element required       
    def getRequest(self,ID):
        
        #find the proper index
        for i in range(0,len(self.RequestList)):
            if self.RequestList[i][0] == ID:
                ElementIdx = i
                break
        
        return self.RequestList[ElementIdx]
        
        
    #Change a default and print it out into the file  (later)  
    #def saveDefaults(self,ID,Values):

        
#Let's create a routine using info from a text file to start requests
def Request(ID, Method = None, MethodArgs = None, TextMethod = None, TextMethodArgs = None ,Numbers = False, Data = None, Default = None):
    
    
    #chech if the global request class was already loaded
    if not 'RequestClass' in globals():
        
        #it doesnt exist create the global
        global RequestClass      
        
        #run the initialisation
        RequestClass = RequestFile()

    #Get the Data as a list
    RequestOut = RequestClass.getRequest(ID)
    
    #Initialise satisfaction loop variables (for asking pure number)
    Satisfied = False

    #Do we need to use choice check
    if RequestOut[4].split(',')[0] == '-':
        NeedChoiceCheck = False
    else:
        NeedChoiceCheck = True

    #Do we need to use length check
    if RequestOut[5] == '-':
        NeedLengthCheck = False
    else:
        NeedLengthCheck = True
        
    #Create a boolean Proceed to avoid to many conditional loops
    Proceed = True
    
    #Make the request delimiters (does not exists randome exit)
    #VisOut.TextBox(Text = 'REQUEST',state = 6)
    
    #Start loop
    while not Satisfied:
        
        #Launch user method
        AddText = ''
        
        if TextMethod:
            if TextMethodArgs:
                AddText = TextMethod(TextMethodArgs)
            else:
                AddText = TextMethod()
            
        #Print the text from the user
        
        if not AddText == '':
            VisOut.TextBox(Title='Request',Text = RequestOut[1],state = 0, close = False, Box = True)
            VisOut.TextBox(Title='',Text = AddText,state = 1, close = False, Box = True)
        else:
            VisOut.TextBox(Title='Request',Text = RequestOut[1],state = 0, close = False, Box = True)
        
        #Get the names
        Names = RequestOut[2].split(",")
        
        #Get the defaults
        if Default == None:
            Defaults = RequestOut[3].split(",")
        else:
            Defaults = Default
    
        #Initialise the default:
        OutText = "The default values are: "
        
        #Get the names and default into text

        if not Defaults[0] == '-':
            try:
                for i in range(0,len(Names)):
                    
                    #make the string
                    OutText += Names[i]+'='+str(Defaults[i])+' '
                
                #print the result
                VisOut.TextBox(Text = OutText,state = 0, close = True, Box = True)

            except:
                VisOut.TextBox(Text = 'Default Values missmatch.',state = 0)
    

        #Send request
        Request = VisOut.RawInput(ID,Data = Data)
        

        
        #start conditions. Enter by user will load defaults
        if Request == "":
            
            #check if this action is allowed
            if RequestOut[4].split(',').count('') > 0:
                    
                #Send defaults
                Out = Defaults
                
                #Leave
                Satisfied = True
                
            else:
                VisOut.TextBox(Text = 'Error : Default selection not permited in this request!!!',state = 0)
        
        else:
            #check the input on alloawed and length
            if NeedLengthCheck:
                if not len(Request.split(' ')) == int(RequestOut[5]):
                    Proceed = False
                    VisOut.TextBox(Text = 'Error : please input the same ammount of parameters as requested!!!',state = 0)
            
            #split the request with space
            RequestSplit = Request.split(' ')
            
            #check if the inputs are allowed
            if NeedChoiceCheck:
                for i in range(0,len(RequestSplit)):
                    if RequestOut[4].split(',').count(RequestSplit[i]) == 0:
                        Proceed = False
                        VisOut.TextBox(Text = 'Error : One of the values entered did not match the allowed inputs!!!',state = 0)
                        
                    
            #check if number if the user wants it
            if Numbers and Proceed:
                result = areNumbers(RequestSplit)
                
                #satisfied ?
                if result:
                    Out = RequestSplit
                    
                    #Leave
                    Satisfied = True

                else:
                    VisOut.TextBox(Text = 'Enter numbers please',state = 0)
                    
            elif Proceed:
                Out = RequestSplit
                
                #Leave
                Satisfied = True

    #Initialise the default:
    OutText = "The user selected values are: "
                
    for i in range(0,len(Out)):
                
        #make the string
        try:
            OutText += Names[i]+'='+str(Out[i])+' '
        except:
            OutText += 'Value '+str(i)+'='+str(Out[i])+' '
            
    #print the result
    VisOut.TextBox(Text = OutText,state = 0, close = True, Box = True)
            
    return Out
            

#to check if a list if composed of only numbers
def areNumbers(List):
    
    #loop over all elements:
    try:
        for i in range(0,len(List)):
                float(List[i])
        areNumbers = True
    except:
        areNumbers = False
    
    return areNumbers



'''
#################################################################################
Read a test text file and load the data into a 3 classes:

- first class will be the intrument information to build the intensity mask
- Seconf class wil be the sample
- Third class the substrate 
#################################################################################
'''
def LoadTestFile(FileLoc):    
    
    #We selected a file now load it and find the instance 'Dist' that marks the start    
    Count = open(FileLoc, 'r')
    
    #Initialise parameters
    LineCount   = 0
    
    InstCount   = 0
    SubCount    = 0
    SamCount    = 0
    
    InstStateStr   = []
    SampleInfStr   = []
    SubstrInfStr   = []
    
    InstStateVal   = []
    SampleInfVal   = []
    SubstrInfVal   = []
        
    InstStateLin   = []
    SampleInfLin   = []
    SubstrInfLin   = []
    

    #Find when the actual data array starts
    for Idx,line in enumerate(Count):
        
        columns = line.split(' ')
        
        #Found Raman Data
        if columns[0] == "*":
            LineCount = LineCount+1
            
        
        #Found Instrument string info
        if columns[0] == "I":
            #Append to matrix
            InstStateStr.append(1)
            InstStateVal.append(1)
            InstStateLin.append(1)
            
            #Populate
            InstStateStr[InstCount] = columns[1]
            
            try:
                InstStateVal[InstCount] = float(columns[2])
            except:
                Pass  = columns[2]
                Split = Pass.split('\n')
                InstStateVal[InstCount] = Split[0]
                
            InstStateLin[InstCount] = LineCount
            
            #Advance
            InstCount += 1
            
            
        #Found Sample string info
        if columns[0] == "S":
            #Append to matrix
            SampleInfStr.append(1)
            SampleInfVal.append(1)
            SampleInfLin.append(1)
            
            #Populate
            SampleInfStr[SamCount] = columns[1]
            try:
                SampleInfVal[SamCount] = float(columns[2])
            except:
                Pass  = columns[2]
                Split = Pass.split('\n')
                SampleInfVal[SamCount] = Split[0]
                
            SampleInfLin[SamCount] = LineCount
            
            #Advance
            SamCount += 1
            
        #Found Substarte string info
        if columns[0] == "P":
            #Append to matrix
            SubstrInfStr.append(1)
            SubstrInfVal.append(1)
            SubstrInfLin.append(1)
            
            #Populate
            SubstrInfStr[SubCount] = columns[1]
            try:
                SubstrInfVal[SubCount] = float(columns[2])
            except:
                Pass  = columns[2]
                Split = Pass.split('\n')
                SubstrInfVal[SubCount] = Split[0]
                
            SubstrInfLin[SubCount] = LineCount
            
            #Advance
            SubCount += 1

            
        # Count
        #Advance line
        LineCount = LineCount+1
        
    print InstStateStr,SampleInfStr,SubstrInfStr,InstStateVal,SampleInfVal,SubstrInfVal,InstStateLin,SampleInfLin,SubstrInfLin
            
    Count.close()
    

        


#IMPORTS DATA FROM THE ARRAY WITH PATH NAMES
def ImportFileData(DataPath,Z):
    
    #For logging
    LastAct = ''
    
    #length of the data
    NumPointsZ  = len(Z)
    
    #Count how many lines we have and create the first array
    Count     = open(DataPath[0], 'r')
    
    #Loop through
    LineCount = 0
    for i in Count:
        LineCount = LineCount+1
    
    #create the data matrix
    Output = numpy.zeros((LineCount+1,len(Z)+1))

    #close for now
    Count.close()
    
    #Initialise array both X and Y
    u = 0
    f = open(DataPath[0], 'r')
    for line in f:
        u = u+1
        line = line.strip()
        line = line.replace('\t',' ', 1)
        columns = line.split()
        Output[u,0] = float(columns[0])#That is X
    f.close()
    
    for idx,Val in enumerate(Z):
        Output[0,idx+1] = Val#That is Y
        
        
    for o in range(0,NumPointsZ):
        u = 0
        f = open(DataPath[o], 'r')
        for line in f:
            u = u+1
            line = line.strip()
            line = line.replace('\t',' ', 1)
            columns = line.split()
            Output[u,o+1] = float(columns[1])#That is the data in each point
        f.close()

    return Output,LineCount
        


def ReadSingleFile(FileLoc):
    '''
    ###########################################################################
    This method reads simple text files and sends them as DataX and DataY:
    
    - PCA data file
    - PCA score file
    
    - Conventional raman files
    ###########################################################################
    '''    
    try:
        #Read the text file
        Read = open(FileLoc,'r')
        
        #Read lines
        Lines = Read.readlines()
    
        #close the file and write it
        Read.close
        
        #Initialise
        XData = []
        YData = []
        
        for idx,Val in enumerate(Lines):

            #split into space
            ValSplit = Val.split('\n')[0].split()
            try:
                
                #try this
                X = float(ValSplit[0])
                Y = float(ValSplit[1])
                
                #Check if we have two numbers
                XData.append(X)
                YData.append([Y])
                
            except:
                pass
    
        LastAct = "\nSuccessfully Loaded File: "+FileLoc
        
    except:
        LastAct = "\nUnsuccessfull to load File: "+FileLoc
        
    return XData,YData,LastAct

def ReadValues(A,FileLoc):
    '''
    ###########################################################################
    This method reads simple text files and retrieves values for fit
    ###########################################################################
    '''    
    try:
        #Read the text file        
        Read = open(FileLoc,'r')
    
        #Read lines
        Lines = Read.readlines()
    
        #close the file and write it
        Read.close
        
        
        for idx,Val in enumerate(Lines):
            
            #split into space
            ValSplit = Val.split('\n')[0].split(' ')
            try:
                
                #try this
                A[idx].ParametersIni[1] = float(ValSplit[0])
                A[idx].ParametersIni[2] = float(ValSplit[1])
                A[idx].ParametersIni[3] = float(ValSplit[2])
                A[idx].ParametersIni[4] = float(ValSplit[3])
                
            except:
                pass
    
        LastAct = "\nSuccessfully Loaded File: "+FileLoc
        
    except:
        LastAct = "\nUnsuccessfull to load File: "+FileLoc
    return LastAct


def ReadFix(A,FileLoc):
    '''
    ###########################################################################
    This method reads simple text files and retrieves values for fit
    ###########################################################################
    '''    
    try:
        #Read the text file        
        Read = open(FileLoc,'r')
    
        #Read lines
        Lines = Read.readlines()
    
        #close the file and write it
        Read.close
        
        
        for idx,Val in enumerate(Lines):
            
            #split into space
            ValSplit = Val.split('\n')[0].split(' ')
            try:
                
                #try this
                A[idx].ParametersFix[1] = int(ValSplit[0])
                A[idx].ParametersFix[2] = int(ValSplit[1])
                A[idx].ParametersFix[3] = int(ValSplit[2])
                A[idx].ParametersFix[4] = int(ValSplit[3])
                
            except:
                pass
    
        LastAct = "\nSuccessfully Loaded File: "+FileLoc
        
    except:
        LastAct = "\nUnsuccessfull to load File: "+FileLoc
    return LastAct



#FORCES THE SHAPES OF SAMPLE AND SUBSTRATE COMPOUND
def FitRemSub(DataX,DataY,First,Last,Compound):

    R          = len(DataX)-1
    DataYTrans = numpy.zeros(R+1)
    Rest       = numpy.zeros(R+1)
   
    if Compound == "substrate":       
        #Now fit that 
        for i in range(0,R):
            DataYTrans[i] = (DataX[i]*(First-Last))+Last
            Rest[i]       = DataY[i]-DataYTrans[i]
    if Compound == "sample": 
        #Now fit that 
        for i in range(0,R):
            DataYTrans[i] = (DataX[i]*(First-Last))+Last
            Rest[i]       = DataY[i]-DataYTrans[i]
    
    return DataYTrans,Rest

def FindMinIndex(Arr):
    '''
    ###########################################################################
    Returns the index position of the minimum from input 1D array
    ###########################################################################
    '''
    Min = numpy.min(Arr)
    for Idx,Val in enumerate(Arr):
        if Val == Min:
            Out = Idx
            break
    
    return Out
    
    


    
'''
###############################################################################
Wavenumber axis interpolation
###############################################################################
'''    
#FIX X ARRAY ORDER AND SPACING
def FixXData(Data,IdxRange,MaxIdx,RangeMin):
    #the X data array from the raman spectrometer is not necesseraly linear 
    #As a result we want to correct the data with the average spacing.

    XPoints      = numpy.zeros(IdxRange)
    CorXPoints   = []
    DeltaXPoints = numpy.zeros(IdxRange)
    
    #Calculate the Stepping between two consecutive points and calcualte the average
    cycle       = 0
    NotReachMin = 0
    for g in range(0,IdxRange):
        XPoints[cycle]      = Data[g+MaxIdx]    #We take the position
        DeltaXPoints[cycle] = Data[g]-Data[g+1] #We take the distance to next point
        cycle               = cycle+1           #Skip to next point
        
    #take the average
    CorStep = numpy.mean(DeltaXPoints)
    
    #Build the corrected 1D X Data array    
    i = 0
    while NotReachMin==0:
        
        CorXPoints.append(1)#Add an element to our new X Data array
        CorXPoints[i] = (-i)*CorStep+XPoints[0]
        
        if CorXPoints[i]<RangeMin:
            NotReachMin=1
        i = i+1
        
    CorIdxRange = len(CorXPoints)    
    return XPoints,CorXPoints,DeltaXPoints,CorIdxRange,CorStep

    
"""
###############################################################################
##############################DATA INDEXING####################################
###############################################################################
"""
def RetIdx(Value,Data):
    '''
    ###########################################################################
    Returns the exit index of an array where the exact value is located
    
    This can only if the user requires the exact value to be found
    
    State is equal to 0 if nothing is found
    ###########################################################################
    '''
    
    idx   = 0
    State = 0
    
    for i in range(0,len(Data)):
        if Data[i] == Value:
            idx   = i
            State = 1
    
    return idx,State
    
    
#FINDS INDEX VALUES FOR 2D CONTOUR DATA WITH SPECIFIED AXIS ORIENTATION
def FindIdx(Data,Limit,axis):
    
    #String orientation Correction
    if axis == "X":
        DataPro = Data[:,0]
    if axis == "Y":
        DataPro = Data[0,:]
     
    #Go search
    for idx,Val in enumerate(DataPro):
        
        if axis == "X":
            if Val <= Limit:
                Out = idx
                break
            
        if axis == "Y":
            if Val >= Limit:
                Out = idx
                break
                
    return Out    

def normalize(array):


    min = numpy.min(array)
    max = numpy.max(array)
    
    if max - min == 0:
        
        array = [0.5 for i in range(0,len(array))]
        
        return array
    else:
        array = (array-min)/(max-min)

        return array

def FindIdx2(Value,Data):
    '''
    #################################################################
    Returnd the index of a value in a list as long as both other 
    values around it are bigger and smaller. So bounded localisation
    #################################################################
    '''
    if len(Data) == 1:
        ID = 0
    else:
        Inverse = False
    
        #Might recquire chirurgical inversion in case the order is wrong
        if Data[len(Data)-1] < Data[0]:
            
            Data = Data[::-1]
            
            Inverse = True
        
        #check the length of the list
        Length = len(Data)

        #Loop thourgh it
        for i in range(0,Length):
            
            #We reached the end
            if i == Length-1:
                
                #print "Assumed that the point is the last one to exist"
                ID = len(Data)-1
                break
            
            #We found it
            if Data[i]<=Value and Data[i+1] > Value :
                ID = i
                break
            
        #In case we had to inverse the array in the begining
        if Inverse:
            ID = Length - ID
    

    #return
    return ID

def FindIdx3(Value,Data):
    '''
    #################################################################
    Returnd the index of a value in a list as long as both other 
    values around it are bigger and smaller. So bounded localisation
    #################################################################
    '''
    if len(Data) == 1:
        ID = 0
    else:
        Inverse = False
    
        #Might recquire chirurgical inversion in case the order is wrong
        if Data[len(Data)-1] < Data[0]:
            Data = Data[::-1]
            Inverse = True
        
        #check the length of the list
        Length = len(Data)

        #Loop thourgh it
        for i in range(0,Length):
            
            #We reached the end
            if i == Length-1:
                
                #print "Assumed that the point is the last one to exist"
                ID_1 = len(Data)-2
                ID_2 = len(Data)-1
                break
            
            #We found it
            if Data[i]<=Value and Data[i+1]>Value:
                ID_1 = i
                ID_2 = i + 1
                break

        #In case we had to inverse the array in the begining
        if Inverse:
            ID_1 = Length - ID_1 - 1
            ID_2 = Length - ID_2 - 1
    
    #return
    return ID_1,ID_2

#RETURNS RANGE INDEX ON DATA ARRAY INPUT 
def FindIdxD(RangeMin,RangeMax,Data):
    
    #set a default to antciate error handling
    if Data[0]>Data[-1]:

        MaxIdx = 0
        MinIdx = len(Data)
    
    else:
    
        MaxIdx = len(Data)
        MinIdx = 0
    
    #set the logocal variables
    FoundMin = 0
    FoundMax = 0
    
    #if the array is inverted
    if Data[0]>Data[-1]:
        
        for idx,Val in enumerate(Data):
            
            if Val<RangeMin and FoundMin==0:
                
                FoundMin = 1
                MinIdx   = idx
            
            if Val<RangeMax and FoundMax==0:
                
                FoundMax = 1
                MaxIdx   = idx

    else:
        
        for idx,Val in enumerate(Data):
            
            if Val>RangeMin and FoundMin==0:
                FoundMin = 1
                MinIdx   = idx
            
            if Val>RangeMax and FoundMax==0:
                
                FoundMax = 1
                MaxIdx   = idx

    return MinIdx,MaxIdx,FoundMin,FoundMax
    


#CREATES AN ARRAY WITH INDEX ASSIGNEMETS
#TO GET THE DATA MUTIPLIED BEFORE DATA PROCESSING
def MultIndex(mult,CorIdxRange):
    
    sign     = 1  #Sign of evolution for the list
    skip     = 0  #Indent for skiping a value
    counting = int(0)  #The main counting index variable
    IdxList  = numpy.zeros(mult*len(CorIdxRange))
    
    for g in range(0,mult*len(CorIdxRange)-mult):
        
        IdxList[g+skip] = int(counting)
        
        #Counting Up
        if sign ==  1: 
            counting = counting+1   
        #Counting Down    
        if sign == -1:
            counting = counting-1
        
        #Check for border reach
        if counting == len(CorIdxRange)-1 or counting ==0 :
            skip = skip+1
            IdxList[g+skip] = int(counting)
            sign = -sign
            
    return IdxList    

def Range(Start,End):
    
    if Start == None or End == None or numpy.isnan(Start) or numpy.isnan(End):
        Out = [0]
    else:
        if Start >= End:
            
            Out = range(int(Start), int(End), -1)
        else:
            Out = range(int(Start),int(End))
    return Out

""" 
###############################################################################
###########################LAYOUT MANAGEMENT###################################
###############################################################################
"""

#Provides a steady indent is usefull when text organisation is being done    
def Indent(L):
    Indent = " "*L
    return Indent
  
#Going back to the line to make the code nicer  
def Ret():
    Return = '\n'*1
    return Return
