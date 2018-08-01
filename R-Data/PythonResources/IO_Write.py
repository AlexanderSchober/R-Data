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

The growing complexity of the package called for buiding an Input File
writing routine. Note that the functions were taken over from very early
parts of the code before class implementations. This is why the writing can
seem a bit off puting.

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
##################################################
After multiple designs it was deemed reasonable to 
consolidate the Input Output function into a
callable class that will be initialised in the 
assigned Dataclass. 

The initialisation just links back to the 
dataclass for adressing purposes.
##################################################
"""
class Write:


    '''
    ##################################################
    FUNCTION: __init__
    
    DESCRIPTION:
    
    Initializer of the class
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - DataClass -> DataClass structure passed to link
    
    ##################################################
    '''
    
    def __init__(self,DataClass):
    
    
        self.DataClass = DataClass


    '''
    ##################################################
    FUNCTION: PrepWrite
    
    DESCRIPTION:
    
    this function is built to prepare the writing 
    process.
    
    This consists of formating and building the file 
    headers.
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - DataFix -> string
    - Type -> string
    
    ##################################################
    '''
    def PrepWrite(self,
                  DataFix,
                  Type):

        ######################################
        #String manipulations to build the start
        HeadEle0  = DataFix
        HeadEle0  = os.path.split(HeadEle0)
        HeadEle   = HeadEle0[-1]
        HeadEle   = HeadEle.split('_')
        HeadStr   = ''
        HeadStr   = HeadEle[0]
        
        ######################################
        #Datatype specific addistions
        if Type == 'Depth':
            HeadStrEx = 'Raman Depth Measurement'
            HeadStrEx +='\n'+'This file was generated from the Wire file: '+HeadStr+' at '+str(datetime.datetime.now())
            HeadStrEx +='\n'+'The first column is the Wavenumber and the first row the scan depth'
        
        if Type == 'Single':
            HeadStrEx = 'Raman Single Measurement'
            HeadStrEx +='\n'+'This file was generated from the Wire file: '+HeadStr+' at '+str(datetime.datetime.now())
            HeadStrEx +='\n'+'The first column is the Wavenumber and the second columns the associated intensities'
        
        if Type == 'Temperature':
            HeadStrEx = 'Raman Temperature Measurement'
            HeadStrEx += '\n'+'This file was generated from the Wire file: '+HeadStr+' at '+str(datetime.datetime.now())
            HeadStrEx += '\n'+'The first column is the Wavenumber and the second columns the associated intensities'
        
        ######################################
        #send it out
        return HeadStr,HeadStrEx
    
    '''
    ##################################################
    FUNCTION: Write2File
    
    DESCRIPTION:
    
    Note that this function is from version 0.0.1 and 
    therefore some of the terms in it might be wrong 
    leading and specific. It is advised to disregard
    them and to focus on the result.
    
    This function is to write data ou into text files
    
    Please note that there will be different file 
    types:
    
    - Depth scan (finished)
    - Temperature scan (finshed)
    - Line scan (in progress)
    - Map scan (in progress)
    - Volume scan (in progress)
    - Temperature (finished)
    
    - Lorrentzian parametrisation output added
    
    The file type is written in the header and will 
    then be set as lass atribute upon import.
    
    All files will be exported into a directory with 
    the proper name related to the header of the files
    related to the experimental nomination. This will
    avoid clutering the current working directory.
    
    Dir name was now built to take the default path 
    out.
    
    WARNING:
    
    This method is kept alive to write out the fit 
    parameters in the fit routines
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - Input -> The value array (2D float array)
    - Start -> Start index of the write process (int)
    - NumberOfLines -> Number of lines present (int)
    - NumberOfRows  -> Number of rows present (int)
    - HeadStrEx -> Generated Headers (str)
    - HeadStr   -> Generated Headers (str)
    - Tail -> the Filename to be used
    - Dir -> The irectory to be used
    
    - RamInfo -> Raman Information (str)
    - SamInfo -> Sample Information (str)
    - Names -> Name of each columns
    
    ##################################################
    '''
    
    def Write2File(self,
                   Input,
                   Start,
                   NumberOfLines,
                   NumberOfRows,
                   HeadStrEx,
                   Header,
                   Tail,
                   Dir,
                   RamInfo,
                   SamInfo,
                   Names = [None]):
        

        
        ######################################
        #run repairs on the firectory name
        DirName = Dir.replace('.', ',')
        
        ######################################
        #Check if the directory exists, if not create it
        if not os.path.exists(DirName):
            
            #should prompt directory select instead...
            os.makedirs(DirName)
        
        ######################################
        #Initialize Data Array
        TextStr = ["" for x in range(0,NumberOfLines+1-Start)]
        TextStr[0] = Header+RamInfo+SamInfo
        
        ######################################
        #Find Longest string in our tabelk of
        #values (formating purposes)
        LargestStr = self.LongestStr(Input)

        ######################################
        #initilize the indenter
        a=0
        #Prepare the string array
        for i in range(Start,NumberOfLines):
            
            #This is simply a print out of the advance on the writing
            print round(float(a)/(float(NumberOfLines-Start))*100,2),'\r',
            sys.stdout.flush()
            
            #move up
            a += 1
            
            #run over the rows
            for l in range(0,NumberOfRows):
                
                #if we are in the first row and first column of the data
                #write 'Dist' as a marker to find this position
                if i==Start and l==0:
                    
                    TextStr[i-Start+1] = TextStr[i-Start+1]+'\nDist '
                    
                    for p in range(0,LargestStr-4+1):
                        
                        TextStr[i-Start+1] = TextStr[i-Start+1]+' '
            
                elif i==Start and l>0:
                    
                    Diff = LargestStr-len(str(Input[0,l]))
                    
                    for g in range(0,Diff):
                        
                        TextStr[i-Start+1] = TextStr[i-Start+1]+' '
                    
                    TextStr[i-Start+1] = TextStr[i-Start+1]+str(Input[0,l])+' '
                        
                else:
                    
                    Diff = LargestStr-len(str(Input[i,l]))
                    
                    for g in range(0,Diff):
                        
                        TextStr[i-Start+1] = TextStr[i-Start+1]+' '
                    
                    TextStr[i-Start+1] = TextStr[i-Start+1]+str(Input[i,l])+' '
                        
            TextStr[i-Start+1] = TextStr[i-Start+1]+'\n'

        ######################################
        #is there names to add
        if not Names[0] == None:

            Unfold = '\nNames    '
            
            for j in range(1,len(Names)):
            
                Unfold += Names[j]+'   '
            
            TextStr.insert(1,Unfold)
        
        ######################################
        #write the file
        
        #Write the text file
        Write = open(os.path.join(DirName,Tail+'.txt'),'wb')
        
        #Insert the created text line
        Write.writelines(TextStr)

        #flush output
        Write.flush()
        
        #close the file and write it
        Write.close


        ######################################
        #Assign the action to the action string to pass onto the main loop
        LastActStr = '\n100 % Completed: Data '+Tail+'.txt was written'
        
        ######################################
        #send the log out
        return LastActStr


    '''
    ##################################################
    FUNCTION: Write2FileV2
    
    DESCRIPTION:
    
    This function was the new addition after the above
    was depreciated for dataclass usage. This method
    gives more flexibility for the input and for the 
    data treatment.
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - Input -> The value array (2D float array)
    - Start -> Start index of the write process (int)
    - NumberOfLines -> Number of lines present (int)
    - NumberOfRows  -> Number of rows present (int)
    - HeadStrEx -> Generated Headers (str)
    - HeadStr   -> Generated Headers (str)
    - Tail -> the Filename to be used
    - Dir -> The irectory to be used
    
    - RamInfo -> Raman Information (str)
    - SamInfo -> Sample Information (str)
    - Names -> Name of each columns
    
    ##################################################
    '''
    def Write2FileV2(self,
                     DataClass,
                     Data,
                     Z,
                     X,
                     Y,
                     T,
                     Type,
                     ActiveSet,
                     omega,
                     Tail,
                     PathOut,
                     event = None,
                     queue = None):

        
        if PathOut == None:
        
            #Define directory name
            PathOut = os.path.join(ReadIni(1),DataClass.HeadStr)
        
        #Check if the directory exists, if not create it
        if not os.path.exists(PathOut):
            
            #should prompt directory select instead...
            os.makedirs(PathOut)
            
        #Initialize Data Array
        TextStr = ['' for x in range(0,5+len(omega))]
        
        #'Raman '+DataClass.Type+' Measurement'+'\n'+
        TextStr[0] = DataClass.HeadStrEx+'\n'+DataClass.RamInfo+'\n'+DataClass.SamInfo+'\n'+DataClass.MeasInfo+'\n'
        
        #Find Longest string in our tabelk of values (formating purposes)
        LargestStr = self.LongestStrV2(Data,Z,X,Y,T,omega, Type)
        
        a=0
        
        #prepare dataset length
        DataSetLength = len(Data[0])+1
        
        #Prepare the string array
        for i in range(1,len(TextStr)):
            
            
            ########################################
            #Now we send stuff to the queue
            try:
                queue.put(float(a)/(float(len(TextStr)))*100)
            except:
                pass
            
            a += 1
            
            for l in range(0,DataSetLength):
                
                ############################################################
                #write the omega
                
                if i > 4 and l == 0:
                    
                    #calculate the difference
                    Diff = LargestStr-len(str(omega[i-5]))
                    
                    #put space
                    for g in range(0,Diff):
                        TextStr[i] += ' '
                    
                    #write it
                    TextStr[i] += str(omega[i-5])+' '
                
                ############################################################
                #write the distances in space
                
                #Set dist for Z
                elif i==1 and l==0:
                    
                    
                    #put spaces
                    for p in range(0,LargestStr-5):
                        TextStr[i] += ' '
                            
                            
                    TextStr[i] += 'DistZ '
            
                #set Dist for X
                elif i==2 and l==0:
                    
                    
                    #put spaces
                    for p in range(0,LargestStr-5):
                        TextStr[i] += ' '
                
                    TextStr[i] += 'DistX '
                
                #Set Dist for Y
                elif i==3 and l==0:
                    
                    
                    #put spaces
                    for p in range(0,LargestStr-5):
                        TextStr[i] += ' '
                            
                    TextStr[i] += 'DistY '
                
                #Set Dist for T
                elif i==4 and l==0:
                    
                    
                    #put spaces
                    for p in range(0,LargestStr-5):
                        TextStr[i] += ' '
                            
                    TextStr[i] += 'DistT '
                            
                ############################################################
                #Write the position headers
                
                #Put Z
                elif i==1 and l>0:
                    
                    #try to write if not pass as there is probably no value
                    try:
                        
                        #calculate the difference
                        Diff = LargestStr-len(str(Z[l-1]))
                        
                        #put space
                        for g in range(0,Diff):
                            TextStr[i] += ' '
                        
                        #write it
                        TextStr[i] += str(Z[l-1])+' '
                
                    except:
                        pass

                #Put X
                elif i==2 and l>0:
                    
                    #try to write if not pass as there is probably no value
                    try:
                        
                        #calculate the difference
                        Diff = LargestStr-len(str(X[l-1]))
                        
                        #put space
                        for g in range(0,Diff):
                            TextStr[i] += ' '
                        
                        #write it
                        TextStr[i] += str(X[l-1])+' '

                    except:
                        pass

                #Put Y
                elif i==3 and l>0:
                    
                    #try to write if not pass as there is probably no value
                    try:
                    
                        #calculate the difference
                        Diff = LargestStr-len(str(Y[l-1]))
                        
                        #put space
                        for g in range(0,Diff):
                            TextStr[i] += ' '
                        
                        #write it
                        TextStr[i] += str(Y[l-1])+' '

                    except:
                        pass

                #Put T
                elif i==4 and l>0:
                    
                    #try to write if not pass as there is probably no value
                    try:
                        
                        #calculate the difference
                        Diff = LargestStr-len(str(T[l-1]))
                        
                        #put space
                        for g in range(0,Diff):
                            TextStr[i] += ' '
                        
                        #write it
                        TextStr[i] += str(T[l-1])+' '

                    except:
                        pass
                
                ############################################################
                #Write the actual Data

                else:
                    try:
                    
                    
                        #calculate the difference
                        Diff = LargestStr-len(str(Data[i-5][l-1]))
                            
                            
                        for g in range(0,Diff):
                            TextStr[i] += ' '
                            
                        #write it
                        TextStr[i] += str(Data[i-5][l-1])+' '
                    
                    except:
                        print i,l


            #close the line
            TextStr[i] += '\n'

            
        try:
            del Write
        except:
            pass


        #Write the text file        
        Write = open(os.path.join(PathOut,Tail+'.txt'),'wb')
        
        #write it
        Write.writelines(TextStr)

        #flush output
        Write.flush()
        
        #close the file and write it
        Write.close


    #SAVE FIGURE WITH THE SPECIFIED NAME TAIL
    def WriteFig(self,
                 Data,
                 fig,
                 Tail):

        #save fig there
        pp = PdfPages(os.path.join(os.path.dirname(DataClass.Info.Root),
                                   Tail
                                   + strftime("%Y_%m_%d %H&%M&%S",
                                              gmtime())
                                   + '.pdf'))
        
        #save to pdf class object
        pp.savefig(fig)
        
        #close the whole thing
        pp.close()

        #Set log action
        LastAct ='\n100 % Completed: Figure '+str(Tail)+'.Pdf was written'
        
        return LastAct


    '''
    ##################################################
    FUNCTION: WriteSingle2File
    
    DESCRIPTION:
    
    This funciton is built ti send out single X, Y 
    type clumns files with a provided header. This
    can be the case for PCA component exports for
    example but is not exclusive.
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - Header  -> Generated Headers (str)
    - DataX   -> X Data array (1D float)
    - DataY   -> Y Data array (1D float)
    
    - RamInfo -> Raman Information (str)
    - SamInfo -> Sample Information (str)
    - Names -> Name of each columns
    
    ##################################################
    '''
    #Write to file X Y
    def WriteSingle2File(self,
                         Header,
                         DataX,
                         DataY,
                         PathName):

        
        #Initialise Component info
        Output = Header

        
        #Add Data of component
        for i in range(0,len(DataX)):
            
            Output += '\n'+str(DataX[i])+' '+str(DataY[i])

        #Write the text file        
        Write = open(PathName,'wb')
        
        #Insert the created text lineWriteComponent
        Write.writelines(Output) 
        
        #close the file and write it
        Write.close
        
        #Send it out
        return PathName

    '''
    ##################################################
    FUNCTION: WriteComponent
    
    DESCRIPTION:
    
    This funciton is built to send out single X, Y
    type column files with a provided header. This
    can be the case for PCA component exports for
    example but is not exclusive.
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - DataClass -> structure
    - Number -> The component number to be saved (str)
    - ExpComponentX -> The component X Data (float 1D)
    - ExpComponentY -> The component Y Data (float 1D)
    - ExpScoreX -> The score X Data (float 1D)
    - ExpScoreY -> The score Y Data (float 1D)
    
    ##################################################
    '''
    def WriteComponent(self,
                       DataClass,
                       Number,
                       ExpComponentX,
                       ExpComponentY,
                       ExpScoreX,
                       ExpScoreY):
        
        #Initialise Component info
        CTextStr  = 'Raman Component'
        CTextStr += '\n'+DataClass.HeadStr
        CTextStr += '\n'+DataClass.HeadStrEx
        CTextStr += '\n'+DataClass.RamInfo+'\n'
        CTextStr += '\n'+DataClass.SamInfo+'\n'
        
        ToModify_1 = str(DataClass.MeasInfo)
        ToModify_2 = ToModify_1.split('\n')[1].split(' ')[1]
        print ToModify_2
        ToModify_1 = ToModify_1.replace(ToModify_2,
                                        ToModify_2+'_Component_'+str(Number))
        
        CTextStr += '\n'+ToModify_1+'\n'
        CTextStr += '\n'+'Dist'
        
        #Initialise Score info
        STextStr  = 'Raman Score'
        STextStr += '\n'+DataClass.HeadStr
        STextStr += '\n'+DataClass.HeadStrEx
        STextStr += '\n'+DataClass.RamInfo+'\n'
        STextStr += '\n'+DataClass.SamInfo+'\n'
        
        ToModify_1 = str(DataClass.MeasInfo)
        ToModify_2 = ToModify_1.split('\n')[1].split(' ')[1]
        ToModify_1 = ToModify_1.replace(ToModify_2,
                                        ToModify_2+'_Score_'+str(Number))
        
        STextStr += '\n'+ToModify_1+'\n'
        STextStr += '\n'+'Dist'

        '''
        ###########################################################################
        Write Intensity ratio file
        ###########################################################################
        '''       
        #Write the text file        
        PathName = os.path.join(os.path.dirname(DataClass.Info.Root),
                                DataClass.HeadStr
                                + '_Component_'
                                + str(Number)
                                + '_Ratio.txt')
        
        #Insert the created text line
        self.WriteSingle2File(CTextStr,
                              ExpComponentX,
                              ExpComponentY,
                              PathName)

        '''
        ###########################################################################
        Write Score file
        ###########################################################################
        '''       
        #Write the text file        
        PathName = os.path.join(os.path.dirname(DataClass.Info.Root),
                                DataClass.HeadStr
                                + '_Component_'
                                + str(Number)
                                + '_Score.txt')
        
        #Insert the created text line
        self.WriteSingle2File(STextStr,
                              ExpScoreX,
                              ExpScoreY,
                              PathName)


        
    '''
    ##################################################
    FUNCTION: Write2DComponent
    
    DESCRIPTION:
    
    This funciton is built to send out single X, Y
    type column files with a provided header. This
    can be the case for PCA component exports for
    example but is not exclusive.
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - DataClass -> structure
    - Number -> The component number to be saved (str)
    - ExpComponentX -> The component X Data (float 1D)
    - ExpComponentY -> The component Y Data (float 1D)
    - ExpScoreX -> The score X Data (float 1D)
    - ExpScoreY -> The score Y Data (float 1D)
    
    ##################################################
    '''
    def Write2DComponent(self,
                         DataClass,
                         Number,
                         ExpComponentX,
                         ExpComponentY,
                         ExpScoreX,
                         ExpScoreY):
 
        #Initialise Component info
        CTextStr  = 'Component times score'
        CTextStr += '\n'+DataClass.HeadStr
        CTextStr += '\n'+DataClass.HeadStrEx
        CTextStr += '\n'+DataClass.RamInfo
        CTextStr += '\n'+DataClass.SamInfo
        CTextStr += '\n'+'Wavenumber IntensityRatio'
        CTextStr += '\n'+'Data'

        
        #Add Data of component
        
        for j in range(0,len(ExpScoreX)):
            CTextStr +=' '+str(ExpScoreX[j])
                
        for i in range(0,len(ExpComponentX)):
            CTextStr += '\n'+str(ExpComponentX[i])
            
            for j in range(0,len(ExpScoreX)):
                CTextStr +=' '+str(ExpComponentY[i]*ExpScoreY[j])

        '''
        ###########################################################################
        Write Intensity ratio file
        ###########################################################################
        '''       

        
        #Write the text file        
        Write = open(os.path.join(os.path.dirname(DataClass.Info.Root),
                                  DataClass.HeadStr
                                  + '_ComponentScore_'
                                  + str(Number)
                                  + '.txt'),
                     'wb')
        
        #Insert the created text line
        Write.writelines(CTextStr)
        
        #close the file and write it
        Write.close

        
    '''
    ##################################################
    FUNCTION: WriteFits
    
    DESCRIPTION:
    
    This routine handles the writing of fits in the 
    fiting framework.
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - DataClass -> structure
    - Number -> The component number to be saved (str)
    - XData -> The component X Data (float 1D)
    - YData -> The component Y Data (float 1D)
    
    ##################################################
    '''
    def WriteFits(self,
                  DataClass,
                  DirName,
                  XData,
                  YData,
                  PeakorRange,
                  State,
                  FitResult):
        '''
        ###########################################################################
        This method is designed to save the fit text files for later use
        ###########################################################################
        '''    
        
        #Check if it is a peak or a range
        if len(PeakorRange) == 1:
            CTextStr  = 'Raman Fit '+str(State)+'_Peak_'+str(PeakorRange)
            CTextStr += '\n'+DataClass.HeadStr
            CTextStr += '\n'+DataClass.HeadStrEx
            CTextStr += '\n'+DataClass.RamInfo
            CTextStr += '\n'+DataClass.SamInfo
            CTextStr += '\n'+' Pos. = '+str(FitResult[1])+'FWHM = '+str(FitResult[2])+' Fact. = '+str(FitResult[3])+' y0 = '+str(FitResult[4])
        else:
            CTextStr  = 'Raman Fit '+str(State)+'_Range_'+str(PeakorRange[0])+'_'+str(PeakorRange[1])
            CTextStr += '\n'+DataClass.HeadStr
            CTextStr += '\n'+DataClass.HeadStrEx
            CTextStr += '\n'+DataClass.RamInfo
            CTextStr += '\n'+DataClass.SamInfo
        
        #Initialise Component info
        CTextStr += '\n'+'Wavenumber IntensityRatio'

        #Add Data of component
        for i in range(0,len(XData)):
            CTextStr += '\n'+str(XData[i])+' '+str(YData[i])

        #Directory path name
        if len(DirName.split(os.path.sep))==1:
            DirName = os.path.join(os.path.dirname(DataClass.Info.Root),DirName)
        
        #Check if the folder exists and create it if not
        if not os.path.exists(DirName):
            os.makedirs(DirName)

        '''
        ###########################################################################
        Write File
        ###########################################################################
        '''       
        #Write the text file  
        if len(PeakorRange) == 1:
            
            Write = open(os.path.join(DirName,
                                      DataClass.HeadStr
                                      + '_Peak_'
                                      + str(round(FitResult[1])).replace('.', ',')
                                      + '_'
                                      + str(State)
                                      + '.txt'),
                         'wb')
        
        else:
            
            Write = open(os.path.join(DirName,
                                      DataClass.HeadStr
                                      + '_Range_'
                                      + str(round(PeakorRange[0],2)).replace('.', ',')
                                      + ' '
                                      + str(round(PeakorRange[1],2)).replace('.', ',')
                                      + '_'+str(State)
                                      + '.txt'),
                         'wb')
        
        #Insert the created text line
        Write.writelines(CTextStr)
        
        #close the file and write it
        Write.close

    '''
    ##################################################
    FUNCTION: WriteValues
    
    DESCRIPTION:
    
    WARNING: Depreciated
    o------------------------------------------------o
    
    PARAMETERS:
    
    
    ##################################################
    '''
    def WriteValues(self,
                    Data,
                    DirName,
                    A):
        '''
        ##############################################
        This method is designed to save the fit text 
        files for later use
        ##############################################
        '''

        #initialise
        CTextStr = ''
        
        #Add Data of component
        for i in range(0,len(A)):
            CTextStr += (str(A[i].Parameters[1])
                         + ' '
                         + str(A[i].Parameters[2])
                         + ' '
                         + str(A[i].Parameters[3])
                         + ' '
                         + str(A[i].Parameters[4])
                         + '\n')

        #Directory path name
        DirName = os.path.join(os.path.dirname(DataClass.Info.Root),
                               DirName)
        
        #Check if the folder exists and create it if not
        if not os.path.exists(DirName):
            
            os.makedirs(DirName)

        '''
        ##############################################
        Write File
        ##############################################
        '''       
        #Write the text file  
        Write = open(os.path.join(DirName,
                                  '_Values_'
                                  + '.txt'),
                     'wb')
        
        #Insert the created text line
        Write.writelines(CTextStr)
        
        #close the file and write it
        Write.close

    '''
    ##################################################
    FUNCTION: WriteFix
    
    DESCRIPTION:
    
    WARNING: Depreciated
    o------------------------------------------------o
    
    PARAMETERS:
    
    
    ##################################################
    '''
    def WriteFix(self,
                 Data,
                 DirName,
                 A):
        '''
        ##############################################
        This method is designed to save the fit text 
        files for later use
        ##############################################
        '''

        #initialise
        CTextStr = ''
        
        #Add Data of component
        for i in range(0,len(A)):
            CTextStr += (str(A[i].ParametersFix[1])
                         + ' '
                         + str(A[i].ParametersFix[2])
                         + ' '
                         + str(A[i].ParametersFix[3])
                         + ' '
                         + str(A[i].ParametersFix[4])
                         + '\n')

        #Directory path name
        DirName = os.path.join(os.path.dirname(DataClass.Info.Root),DirName)
        
        #Check if the folder exists and create it if not
        if not os.path.exists(DirName):
            os.makedirs(DirName)

        '''
        ###########################################################################
        Write File
        ###########################################################################
        '''       
        #Write the text file  
        Write = open(os.path.join(DirName,'_Fix_Values_'+'.txt'),'wb')
        
        #Insert the created text line
        Write.writelines(CTextStr)
        
        #close the file and write it
        Write.close

    '''
    ##################################################
    FUNCTION: LongestStr
    
    DESCRIPTION:
    
    Provides the longest string in a 2D float array.
    This will allow for better processing of the 
    output files later on.
    
    WARNING: Depreciated
    o------------------------------------------------o
    
    PARAMETERS:
    
    - DataClass -> structure
    
    ##################################################
    '''
    def LongestStr(self,
                   DataClass):
        
        #initialise
        Longest = 0
        
        #loop over one shape
        for o in range(0,DataClass.shape[1]):
            
            #loop ove the other shape
            for g in range(0,DataClass.shape[0]):
                
                #check if longer
                if len(str(DataClass[g,o]))>Longest:
                    
                    #assign new value
                    Longest = len(str(DataClass[g,o]))
    
        #end it out
        return Longest


    '''
    ##################################################
    FUNCTION: LongestStrV2
    
    DESCRIPTION:
    
    Provides the longest string in a 2D float array.
    This will allow for better processing of the 
    output files later on.
    
    o------------------------------------------------o
    
    PARAMETERS:
    
    - DataClass -> structure
    - Z -> Intensity structure
    - X -> Position structure
    - Y -> Position strucutre
    - T -> Temperature structure
    - omega -> Wavenumber structure
    - Type -> Type of the measurement (string)
    
    ##################################################
    '''
    def LongestStrV2(self,
                     Data,
                     Z,
                     X,
                     Y,
                     T,
                     omega,
                     Type):
        
        #set 0
        Longest = 0
        
        #check Data
        for o in range(0,len(Data)):
            
            for g in range(0,len(Data[0])) :
                if len(str(Data[o][g]))>Longest:#check for longest value
                    Longest = len(str(Data[o][g]))

        #check Z
        for g in range(0,len(Z)) :
            if len(str(Z[g]))>Longest:#check for longest value
                Longest = len(str(Z[g]))
        #check X
        for g in range(0,len(X)) :
            if len(str(Y[g]))>Longest:#check for longest value
                Longest = len(str(Y[g]))
        #check Y
        for g in range(0,len(Y)) :
            if len(str(Y[g]))>Longest:#check for longest value
                Longest = len(str(Y[g]))
        #check omega
        for g in range(0,len(omega)) :
            if len(str(omega[g]))>Longest:#check for longest value
                Longest = len(str(omega[g]))
        #check Temp
        for g in range(0,len(T)) :
            if len(str(T[g]))>Longest:#check for longest value
                Longest = len(str(T[g]))
        #send it out
        return Longest



