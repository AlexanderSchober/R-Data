# -*- coding: utf-8 -*-
"""
Created on Mon May 11 10:30:43 2015

@author: Schober 
"""

print 'Loading Fitting dependencies...'

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

##################################################
Default python lbrary imports
##################################################
"""

#######################################
#basic imports

#system import
import sys

#numpyy mathematical import
import numpy

#scipy import
import scipy

#######################################
#advanced imports

#Thread the fiting process to avoid ssytem lockup
from threading import Thread, Event
from Queue import Queue

#######################################
#advanced imports

#fitting routines
from scipy.optimize import least_squares

from scipy.optimize import leastsq

from scipy.sparse.linalg import spsolve

######################################
#import matplotlib for colors
import matplotlib

matplotlib.use("TkAgg")



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


"""
##################################################
These are the custome imports
##################################################
"""

#import Utility for requests
from .. import Utility_Main         as Utility
from .. import Utility_File         as File

#import dispatecher
from Raman_Fit_Dispatcher   import FitDispatcher



class FitMainClass:
    '''
    ###############################################################################
    This class is instored to have a more viable fit management. All fit 
    information will be saved locally in this class. All calculations of
    lorrentzians will be done locally. Note that version 1 had also a single
    lorrentzian fit routine that will not exist anymore in version 2. This routine
    was due to historicall reason because of the unability to understand the fitting
    procedure. 
    
    Note that a new approach to avoid instability will be implemented here. 
    Throwing in to many variables into the solve procedure creates to many non-
    local minimas and is therefore very instable when fitting multiples picks. 
    
    Note that this class was once created to be used in the PCA framework. But
    due to recent interest it will now be buitl as a stand alone functioning 
    routine. Allowing ultimately to treat single dimension datasets
    
    Even further all fits will be stored in a database scheme and callable into
    this main class which will then rebuild the entire setup windows figures
    and so on.
    
    
    - Create a window manager
    - Create a dumping hiearchy
    - Create a read hiearchy
    
    Note that the fit hiearchy should be unlinked from the from teh PCA side
    
    Top most structure will include:
    Raw Data X and Y
    
    note that in case of the PCA this routine instance should be called in PCA
    initialisation to allow for a global pasing of the pointers.
    
    ###############################################################################
    '''

    def __init__(self,DataClass):

        ########################
        #Build the initial datastructures
        self.DataClass = DataClass
        self.Verbose = False
        
        try:
            self.XArray = self.DataClass.Contour.Projection[1]
        except:
            pass
        
        ########################
        #Initialise list of classes for raw data
        self.Info               = []
        self.RawData            = []
        self.ResidualData       = []
        
        ########################
        #Initilise Arrays of computation
        self.CompData           = []


        '''
        #####################################
        Set up the function environnements
        #####################################
        '''

        ########################
        #How many function files is there
        
        #create path array
        PathArray = [File.GetRuntimeDir(),
                     'PythonResources',
                     'Fitting']
                
        #process it
        Path = File.BuildPath(PathArray)
        
        #grab all the .py file in this folder
        PathArray = File.GetFileNames(Path, '.py')
        
        print 'These are the function'
        print Path
        print PathArray
        ########################
        #Who is a function
        TempPaths = []
        
        #cyce through
        for Path in PathArray:
        
            with open(Path, 'r') as f:
                
                first_line = f.readline()
    
                if len(first_line.split( '--FUNCTION--')) > 1:
    
                    TempPaths.append(Path)
    
        #set the number of function
        self.NumberOfFunction = len(TempPaths)
        
        ########################
        #What are the class names
        TempClassNames = []
        
        for Path in TempPaths:
        
            #grab the lines
            lines = [line.rstrip('\n') for line in open(Path)]
        
            for line in lines:
        
                if len(line.split('class')) > 1:

                    if len(line.split('class')[1].split(':')) > 1:

                        TempClassNames.append(line.split('class')[1].split(':')[0])

        ########################
        #Process the import
        for i in range(0, self.NumberOfFunction):

            #grab the file name
            Name = File.GetFileName(TempPaths[i])

            #import
            exec('from '+Name.split('.py')[0]+' import '+TempClassNames[2*i]+','+TempClassNames[2*i+1])

        ########################
        #set it all up

        #Initilise The associated arrays to Lorrentzian fitting
        self.Function_Pointers       = [None] * self.NumberOfFunction
        self.Function_Info_Pointers  = [None] * self.NumberOfFunction
        self.Class_Pointer           = [None] * self.NumberOfFunction
        self.Function_Order          = [None] * self.NumberOfFunction
        
        for i in range(0,self.NumberOfFunction):

            self.Function_Pointers[i] = []
            
            exec('self.Function_Info_Pointers[i] = '+TempClassNames[2*i]+'()')

            exec('self.Class_Pointer[i] = '+TempClassNames[2*i+1])
        
            self.Function_Order[i] = self.Function_Info_Pointers[i].Order
        
        ########################
        #Order them
        self.Function_Pointers        = [x for _,x in sorted(zip(self.Function_Order,self.Function_Pointers ))]
        self.Function_Info_Pointers   = [x for _,x in sorted(zip(self.Function_Order,self.Function_Info_Pointers ))]
        self.Class_Pointer            = [x for _,x in sorted(zip(self.Function_Order,self.Class_Pointer ))]
        
        
        '''
        #####################################
        Finish initialisation
        #####################################
        '''

        ########################
        #initialise the fit output
        self.FitTot             = []
        
        ########################
        #Initialise the goodness of fit
        self.ChiSquareLorr      = []
        
        #Link special variables
        self.IgnoreFirstMin     = False
    
        #Current fit
        self.Current            = 0
            
        #avoid bugs
        self.ParClass           = None
        self.ParPick            = None
    
    def AddFitData(self,X,Y,Info):
        '''
        ###############################################################################
        This function has been installed to add a fit to the present environement
        This will initialise the arrays
        ###############################################################################
        '''
        
        ###########################
        #Set log variable
        LastAct = ''
        
        ###########################
        #Append info array
        self.Info.append(Info)
        LastAct += '\nAdded informations, proceeding...'

        ###########################
        #Build the data
        self.RawData.append(ViewData(X,Y,self))
        self.CompData.append(CalcData(self.RawData[-1]))
        self.CompData[-1].LoadCalc()
        
        ###########################
        #log it
        LastAct += '\Loaded View and Calculation data, proceeding...'
    
        ###########################
        #Change current by default to the last added lements
        self.Current = len(self.Info)-1
        
        return LastAct
    
    def AddFitVis(self):
        '''
        ###############################################################################
        This initialises and links the visual class to the lorrentzian one. Effectively 
        it tells it how to process the lorrentzian information to produce viable
        fits that can be called through SimplePlot commands
        ###############################################################################
        '''
        #initialise figure class
        self.Fig = FitDispatcher(self)
    
        ##link it to vis class
        self.Fig.DrawClass.Function_Pointers.CallBuild(self.Function_Pointers[0])
    
    
    def AddFit(self, ID = None , HowMany = None, Type = None):
        '''
        ###############################################################################
        This section build the lorrentzian subclasses all isted within 
        self.Function_Pointers[0]. Note that this instance is not called initially anymore
        since version 3 as the lorrentzian initialisation does not have to be done 
        beforehand anymore...
        
        So now all is done live and this function will be called as needed from the
        Plotwindow class
        
        ###############################################################################
        '''
        #################################
        #initalise the catalogue
        CreationCatalogue = []
        
        for i in range(0, self.NumberOfFunction):
        
            CreationCatalogue.append([self.Function_Pointers[i],
                                      self.CreateGeneralFit,
                                      self.Class_Pointer[i]])
        
    
        
        if Type == None:
        
            #################################
            #set the how many correction
            if HowMany == None:
            
                HowMany = [0 for i in range(len(CreationCatalogue))]
            
            
            
            #################################
            #go through the creation catalogue
            if ID == None:
            
                #individual creators
                for ii in range(len(CreationCatalogue)):
            
                    self.AddFitGeneralised(ii,
                                           CreationCatalogue[ii][0],
                                           CreationCatalogue[ii][1],
                                           HowMany = HowMany[ii])

                    #launch the local creator and set to 0
                    self.FitTot.append(None)
                    
                    #add the residual
                    self.ResidualData.append(None)
                    
                    #Calculate the goodness of fit
                    self.ChiSquareLorr.append(None)
                
            else:
                
                for ii in range(len(CreationCatalogue)):
            
                    if not HowMany[ii] == 0:
                        
                        self.AddFitGeneralised(ii,
                                               CreationCatalogue[ii][0],
                                               CreationCatalogue[ii][1],
                                               ID = ID,
                                               HowMany = HowMany[ii])
        else:
        
        
            #################################
            #go through the creation catalogue
            self.AppendFitGeneralised(CreationCatalogue[Type], ID = ID)
                
    def AppendFitGeneralised(self, Target  ,ID = None):
    
        '''
        ###############################################################################
        This function constitutes n effort to make the system more flexible and easier
        to upgrade in the future. The generalised fit helper will grab the information
        depeindingon the passed kewords.
        
        ###############################################################################
        '''
        
        ###################################
        ###################################
        
        #Launch the creator
        
        #Set log variable
        LastAct = ''
        
        #We added the case were we want to recalculate the entire range
        Target[0][ID].append(Target[2](self.CompData[ID]))
        
        LastAct += '\nInitialised the fit array, proceeding...'
        
        self.VoidFitManager(Num = ID)


    def AddFitGeneralised(self,idx, TargetList, TargetCreator ,ID = None, HowMany = 1):
    
        '''
        ###############################################################################
        This function constitutes n effort to make the system more flexible and easier
        to upgrade in the future. The generalised fit helper will grab the information
        depeindingon the passed kewords.
        
        ###############################################################################
        '''
        
        ###################################
        ###################################
        #Launch the creator
        
        #Set log variable
        LastAct = ''
        
        #load the lorrentzian part
        if ID == None:
            
            #Does not exist yet, case of initialisation
            TargetList.append(1)
            LastAct += '\nInitialised the fit array, proceeding...'
            Buffer,HowMany = TargetCreator(idx,len(self.Info)-1,HowMany)
            
            #it's the last one
            DataX = self.CompData[-1].DataX
            DataY = self.CompData[-1].DataY
        
        else:
            
            #We added the case were we want to recalculate the entire range
            
            TargetList[ID] = 1
            LastAct += '\nInitialised the fit array, proceeding...'
            Buffer,HowMany = TargetCreator(idx,ID,HowMany)
        
            #Set the future plot here already
            self.FitTot[ID]   = None
                
            #Calculate the goodness of fit
            self.ChiSquareLorr[ID] = None
        
            #set data
            DataX = self.CompData[ID].DataX
            DataY = self.CompData[ID].DataY

        ###################################
        ###################################
        #Set the procedures
        #create to numpy
        DataX = numpy.asarray(DataX)
        DataY = numpy.asarray(DataY)
        
        #Launch the fit creator
        LastAct += Buffer
        LastAct += '\nSuccessfully launched and finalysed the fit creator, proceeding...'
        
        #Set range parameter
        FitRangeMax = numpy.max(DataX)
        FitRangeMin = numpy.min(DataX)
        
        FitFrameMax = numpy.max(DataY)
        FitFrameMin = numpy.min(DataY)
        
        FitRangeFac = (FitRangeMax-FitRangeMin)
        FitFrameFac = (FitFrameMax-FitFrameMin)
        
        FitHWHM     = 5
        Steps       = (FitRangeFac)/(HowMany+1)
        
        #set the coloraray
        self.Color = matplotlib.cm.rainbow(numpy.linspace(0,1,int(HowMany)))
        
        if  ID == None:
        
            for i in range(0,int(HowMany)):
                
                if TargetList == self.Function_Pointers[0]:
                    
                    #Set values automatically
                    TargetList[self.Current][i].ParametersIni = [0,
                                                                 FitRangeMin+Steps*(i+1),
                                                                 FitHWHM,
                                                                 FitFrameFac,
                                                                 0]
                
                else:
                
                
                    #Set values automatically
                    TargetList[self.Current][i].ParametersIni = [0 for j in range(self.Function_Info_Pointers[idx].ParameterNumber + 1)]
                
                #copy initial values onto default starting valeus
                TargetList[self.Current][i].Parameters = list(TargetList[self.Current][i].ParametersIni)
            
                #add fixed radion button logical variable
                TargetList[self.Current][i].Fix = [tk.IntVar() for j in range(self.Function_Info_Pointers[idx].ParameterNumber + 1)]
    
                #######
                #set the assymetric to fixed
                if TargetList == self.Function_Pointers[0]:
                
                    TargetList[self.Current][i].Fix[3].set(1)
    
                #######
                #set the color
                TargetList[self.Current][i].SetVisuals()
                TargetList[self.Current][i].Color = matplotlib.colors.rgb2hex(self.Color[i])
    
        else:
            
            for i in range(0,int(HowMany)):
                
                if TargetList == self.Function_Pointers[0]:
                    
                    #Set values automatically
                    TargetList[ID][i].ParametersIni = [0,
                                                       FitRangeMin+Steps*(i+1),
                                                       FitHWHM,
                                                       FitFrameFac,
                                                       0]
                
                else:
                
                    #Set values automatically
                    TargetList[ID][i].ParametersIni = [0 for j in range(self.Function_Info_Pointers[idx].ParameterNumber + 1)]
                
                #copy initial values onto default starting valeus
                TargetList[ID][i].Parameters = list(TargetList[ID][i].ParametersIni)
            
                #add fixed radion button logical variable
                TargetList[ID][i].Fix = [tk.IntVar() for j in range(self.Function_Info_Pointers[idx].ParameterNumber +1 )]
    
                
                #######
                #set the assymetric to fixed
                if TargetList == self.Function_Pointers[0]:
                    
                    TargetList[ID][i].Fix[3].set(1)
                        
                #######
                #set the color
                TargetList[ID][i].SetVisuals()
                TargetList[ID][i].Color = matplotlib.colors.rgb2hex(self.Color[i])
                    
        return LastAct


    def FitList(self):
        '''
        ###############################################################################
        returns formated list of fits stored in the main class
        
        1: fit Info 1
        2: Fit info 2
          .
          .
          .
        
        ###############################################################################
        '''
        #Initialise the output
        Out = ''
        
        #Logical check
        if len(self.Info) == 0:
            
            #Nothing has beenloaded yet
            Out = 'Nothing stored in fits yet'
        
        else:
            
            #Loop and fill
            for i in range(0,len(self.Info)):
                Out += '\n'+self.Info[i]
    
        #send it out
        return Out
                
    def SetCreatedX(self):
        
        self.temp = FitX(self.DataClass.RamFit)
            
        self.CreatedX = self.temp.CreatedX
    
    def ThreadedFit(self, Container = None):
    
        '''
        ###############################################################################
        This is used to launchthe fit lorr as thread to avoid eternal beachball
        scenarios when heavy fits are running.
        
        it will pass the method to Run, the queue and the event selector
        ###############################################################################
        '''
    
        self.progress = ('%.2f' % float(0)+'%')
    
        #set different communication elements
        self.queue = Queue()
        self.event = Event()
        self.Run   = Thread(target = self.FitManager, args = (self.event,
                                                              self.queue,
                                                              Container))
    
        #start the thread
        #self.Run.start()
        
        return self.Run, self.queue, self.event
#    
#    def DrawLorr(self):
#        '''
#        ###############################################################################
#        This will simulate a fit by just throwing the initial values into the result
#        ###############################################################################
#        '''
#        for j in range(0,len(self.Function_Pointers[0][self.Current])):
#            
#            #make sure parameters get copied over
#            self.Function_Pointers[0][self.Current][j].Parameters = list(self.Function_Pointers[0][self.Current][j].ParametersIni)

    def FitManager(self, event , queue, Container = None , Order = None):
        '''
        ###############################################################################
        Version 0.1.4 wants to accomodate for different curve types. therefore we
        introduce a fit handler method that is here.
        
        He will call indicidually the fiters as they are asked:
        
        - Lorrentzian fitter 
        - Linear fitter
        - polynomila fitter
        - gaussian fitter
        
        Note that the container will be spearated into:
        
        Container[0] will be the local loop parameters 
        while all the other will be contain the local fit parameters
        This can be the orders or repetitions
        
        - LorrContainer     = Container [1]
        - LinearContainer   = Container [2]
        - PolyContainer     = Container [3]
        - GaussContainer    = Container [4]
        
        The routine will include a setup and then load the indicudal parts of the 
        data to be fited first
        
        ###############################################################################
        '''
        
        #set upt hte potential log
        LastAct = ''
        
        ################################################
        ################################################
        #fetch the data to fit
        
        #process to the range removal
        self.CompData[self.Current].RemoveRanges()
        
        #grab DataX
        DataX = self.CompData[self.Current].DataX
        
        #grab DataY
        DataY = self.CompData[self.Current].DataY
 
        ################################################
        ################################################
        #Do the order if not given by the fit
        
        ######
        Order = Container[0][1]
        ######
        
        i = 0
        
        if Container[0][1] == None:
            
            #initialise the order
            Order = []
            
            #add if defined
            if not len(self.Function_Pointers[0][0]) == 0:
        
                Order.append(i)
                
            i += 1
    
            #add if defined
            if not len(self.Function_Pointers[1][0]) == 0:
        
                Order.append(i)
                
            i += 1
                    
            #add if defined
            if not len(self.Function_Pointers[2][0]) == 0:
        
                Order.append(i)
                
            i += 1
                    
            #add if defined
            if not len(self.Function_Pointers[3][0]) == 0:
        
                Order.append(i)
                
            i += 1
        


        ################################################
        ################################################
        #set th efit precision
        self.FitPrecision = Container[0][2]
        
        ################################################
        ################################################
        #fetch the datat to fit

        #cycle over the repetition parameter
        for ii in range(Container[0][0]):
            
            for jj in range(0,len(Order)):
                
                ##################
                #create the element without the actual function
                #to optimize

                Buffer = self.Constructor(Ignore = jj,
                                          Data = list(DataY),
                                          X = DataX)
    
                #re-expressing the
                self.FitGeneral(Order[jj],
                                event,
                                queue,
                                DataX,
                                numpy.asarray(Buffer),
                                Container[Order[jj] + 1],
                                self.PolyFunction)

        ################################################
        ################################################
        #log it
        LastAct += '\nSucessfully finished fitting run, proceeding...'
        
        
        self.FitTot[self.Current] = [numpy.copy(self.CreatedX),self.AllFunctions(self.CreatedX,0)]
        
        ####################################
        #Calculat the residual
        self.ComputeRestCalculation(self.Current)
        #self.ChiSquareLorr[self.Current] = self.ChiSquare(DataY,self.PolyLorentzianFunction(DataX,0))
        
        ################################################
        #compute all functions
        self.Constructor(Data = list(DataY), X = DataX)
        self.isFitted = True
        
        ####################################
        #Notify this class about fited state
        self.CompData[self.Current].isFitted = True

        ####################################
        queue.put(['Progress','Stop'])

        ####################################
        return LastAct


    def VoidFitManager(self, Num = 0):
        '''
        ###############################################################################
        
        
        ###############################################################################
        '''
        
        
        ################################################
        ################################################
        #fetch the data to fit
        
        #process to the range removal
        self.CompData[Num].RemoveRanges()
        
        #grab DataX
        DataX = self.CompData[Num].DataX
        
        #grab DataY
        DataY = self.CompData[Num].DataY

        ####################################
        #Calculat the residual
        self.ComputeRestCalculation(Num)
        
        ################################################
        ################################################
        #compute all lorrentzians
        self.Constructor(Num = Num, X = DataX)
        self.isFitted = True

        ####################################
        #Notify vis class about fited state
        self.CompData[Num].isFitted = True


    def Constructor(self,Ignore = None , Data = None, Num = None, X = None):
        '''
        ###############################################################################
        This constructor will manage the different subconstructors and avoid the 
        constructor with ID = Ignore. Note that then the Constructor will substract
        Data with the resulting function. What should be returned is the Data to fit
        with the ingored fit method.
        
        If Ignore is None then the constructor will just call the constructor methods
        witout subdivisiion
        ###############################################################################
        '''
        
        if not Data == None:
            
            #copy data locally
            Data = numpy.array(Data)
            
            ####################################
            #cycle through the constructor methods
            #ommit the one that we try to fit
            if not Ignore == None:
                
                for i in range(0,self.NumberOfFunction):
            
                    if i == Ignore:

                        pass

                    else:
                        
                        #we need to check if i is represented...
                        if len(self.Function_Pointers[i][0]) == 0:
                        
                            pass
                    
                        #now we can remove the rest
                        else:
                            
                            Data =  numpy.array(Data) - numpy.array(self.GeneralConstructor(i,
                                                                               Data = Data,
                                                                               Num = Num,
                                                                               X = X))
                
            ####################################
            #final computation of all functions
            else:
                
                
                for i in range(0,self.NumberOfFunction):
            
                    Data =  numpy.array(Data) - numpy.array(self.GeneralConstructor(i,
                                                                                    Data = Data,
                                                                                    Num = Num,
                                                                                    X = X))
                             
                #set the FitTot
                self.FitTot[self.Current] = [numpy.copy(self.CreatedX),
                                             self.AllFunctions(self.CreatedX,0)]
        
            try:
                
                if len(self.Function_Pointers[1]) > 0 :
                
                    self.RaiseLinear(self.CreatedX,0)
            
            except:
            
                print 'Could not raise linear yet'
            
            return Data
    
        else:
            
            for i in range(0,self.NumberOfFunction):
            
                self.GeneralConstructor(i, Num = Num, X = X)
                self.FitTot[Num] = [numpy.copy(self.CreatedX),self.AllFunctions(self.CreatedX,0, Num = Num)]

            try:
                
                self.RaiseLinear(self.CreatedX,0, Num = Num)
            
            except:
            
                print 'Could not raise linear yet'



    def GeneralConstructor(self,idx,Data = None, Num = None, X = None):
        '''
        ###############################################################################
        This constructs all lorrentzians associate to a fit This constructor takes an
        input = None when all lorrentzians have to be called. Note that this will be
        the case mostly. The Gaussian constructor will be similar.
        ###############################################################################
        '''
    
        #the way that variables are checked in python changed
        #this is why we have to adjust a few things
        
        #defien nonetype
        NoneType = type(None)

        Proceed_1 = None
        Proceed_2 = None
        
        #set the according rray element
        if isinstance(Num, basestring):
        
            Proceed_1 = 'STR'
        
        if isinstance(Num, NoneType):
        
            Proceed_1 = 'NONE'
        
        if isinstance(X, basestring):
        
            Proceed_2 = 'STR'
        
        if isinstance(X, NoneType):
        
            Proceed_2 = 'NONE'
        
        #logical variable
        if Proceed_1 == 'NONE':
            
            #Loop over all lorentzians
            for j in range(0,len(self.Function_Pointers[idx][self.Current])):
                
                #fetch the minimum
                Para = float(self.Function_Pointers[idx][self.Current][j].Parameters[-1])

                #Process it
                self.Function_Pointers[idx][self.Current][j].Compute(self.CreatedX)

            if Proceed_2 == 'NONE':
                
                return self.PolyFunction(idx,self.CreatedX,0)
            
            else:
                
                return self.PolyFunction(idx,X,0)

        #if user wants to process a specific
        elif not Proceed_1 == 'NONE' and not Proceed_1 == 'STR':
            
            #Loop over all lorentzians
            for j in range(0,len(self.Function_Pointers[idx][Num])):
                
                #fetch the minimum
                Para = float(self.Function_Pointers[idx][Num][j].Parameters[-1])

                #Process it
                self.Function_Pointers[idx][Num][j].Compute(self.CreatedX)

            if Proceed_2 == 'NONE':
                
                return self.PolyFunction(idx,self.CreatedX,0)
            
            else:
                
                return self.PolyFunction(idx,X,0)
    
        elif  Proceed_1 == 'STR':
            
            #loop over all
            for m in range(0, self.Function_Pointers[idx]):
                
                #set the FitTot
                self.FitTot[m] = [numpy.copy(self.CreatedX), self.PolyFunction(idx,self.CreatedX,0, Num = m)]
                
                #Loop over all lorentzians
                for j in range(0,len(self.Function_Pointers[idx][m])):
                    
                    #fetch the minimum
                    Para = float(self.Function_Pointers[idx][m][j].Parameters[-1])

                    #Process it
                    self.Function_Pointers[idx][m][j].Compute(self.CreatedX,Offset = Offset)

                return self.PolyFunction(idx,self.CreatedX,Num = m)

    def FetchBounds(self, Para,RelBoundsBool,RelBounds,AbsBoundsBool,AbsBounds):
        '''
        ###############################################################################
        A more sofiticated method was recquired to check the bounds as we now compare
        the relative and absolute bounds.
        ###############################################################################
        '''
        ##############################
        #reoarganise if the order is wrong
        if AbsBounds[0] > AbsBounds[1]:
            
            AbsBounds[0] , AbsBounds[1]  = AbsBounds[1] , AbsBounds[0]
    
        #reoarganise if the order is wrong
        if RelBounds[0] > RelBounds[1]:
            
            RelBounds[0] , RelBounds[1]  = RelBounds[1] , RelBounds[0]
    
        #ouput is necessary
        if self.Verbose:
            print '## This is the bounding system ##'
            print 'The parameter inputvalue: ',Para
            print 'The Boolean Rel: ', RelBoundsBool
            print 'The reative bounds: ', RelBounds
            print 'The Boolean Abs: ', AbsBoundsBool
            print 'The absolute bounds: ', AbsBounds
        
        
        ##############################
        #CCheck if the parameters is in the bounds
        if AbsBoundsBool:
            
            #process
            if Para < AbsBounds[0]:
        
                Para = AbsBounds[0] + 0.1 * AbsBounds[0]
    
            if Para > AbsBounds[1]:
        
                Para = AbsBounds[1] - 0.1 * AbsBounds[1]
    
        ##############################
        #Compute the Bounds bound
        if RelBoundsBool and not AbsBoundsBool:
    
            LowerBound = Para + RelBounds[0]
            UpperBound = Para + RelBounds[1]

        elif AbsBoundsBool and RelBoundsBool:
        
            LowerBound = Para + RelBounds[0]
            UpperBound = Para + RelBounds[1]
        
            if LowerBound < AbsBounds[0]:
        
                LowerBound = AbsBounds[0]

            if UpperBound > AbsBounds[1]:
        
                UpperBound = AbsBounds[1]

        elif AbsBoundsBool and not RelBoundsBool:

            LowerBound = AbsBounds[0]
            UpperBound = AbsBounds[1]

        else:

            return [-numpy.inf, numpy.inf], Para

        return [LowerBound, UpperBound], Para

    def FitGeneral(self, idx, event, queue, DataX, DataY, Container = None, Target = None):
        '''
        ###############################################################################
        Here will be a main change compared to version 1. We want to manage the
        different parts of the fitting independently. This means that adjusting the
        width should not be done at the same time as adjusting the amplitude or the
        position. or it should be done in intermittance. and it shoudl be done one peak
        at a time over few itterations
        
        Loop over parameter type
            make iterations
                make few per pick and move etc...
                
                
                
        #This part was severely uopdated in version 0.0.5
        ###############################################################################
        '''
        #for the log
        LastAct = ''
        
        ##########################################################
        ##########################################################
        #Grab parameters
        
        for j in range(0,len(self.Function_Pointers[idx][self.Current])):
            
            #make sure parameters get copied over
            self.Function_Pointers[idx][self.Current][j].Parameters = list(self.Function_Pointers[idx][self.Current][j].ParametersIni)
        
        #log it
        LastAct += '\nSucessfully generated fiting planes, proceeding...'
    
        ##########################################################
        ##########################################################
        #This si the main fitting loop
        #note that the parameters can be caught by the container
        #
        # Container[0] = loop repetition
        # Container[1] = Parameter Order for the first calculations [0, 1, 2, ...]
        # Container[2] = Parameter Order for next calculations [0, 1, 2, ...]
        # Container[3] = Empty
        # Container[4] = Bounds = [True/False,[None/Val, None,Val]]
        #
        # a interface needs to be created to account for this


        ##########################################################
        ##########################################################
        #visual debuger in case of need
        Init = True
        
        #avoid recalculation
        Length = len(self.Function_Pointers[idx][self.Current])
        
        ##########################################################
        ##########################################################
        #visual debuger in case of need
        #Select the lorrentzian
            
        #create arrays
        Val = []
        ID = []
        
        #append values
        for hh in range(0,Length):
                
            #add
            ID.append(hh)
            Val.append(float(self.Function_Pointers[idx][self.Current][hh].Parameters[0]))


        ##########################################################
        ##########################################################
        #Loop n times over it all
        for k in range(0,Container[0]):
        
        
            ##########################################################
            #We allow the user to chose a start different than
            #the following computation
            
            if Init:
                
                #Specify the pointer
                Pointer = Container[1]
                
                #Set back te variable
                Init = False
            
            else:
                
                #Specify the pointer
                Pointer = Container[2]
            
            ##########################################################
            #The pointer is now set proceed to the loop and use the
            #pointer length and values
            
            for l in range(0, len(Pointer)):
                
                #grab the pointer value that we were about to compute
                i = Pointer[l]
                
                #set parclass
                self.ParClass = i
                
                
                if not Container[5]:
                                   
                    ##########################################################
                    ############## Single parameter fit can ##################
                    ##########################################################
                    
                    #now loop over peak
                    for j in range(0,Length):
                        
                        ####################################
                        #check if the kill event has been called
                        if not event.is_set():
                            pass
                        else:
                            return
                        
                        ####################################
                        #Select next lorrentzian
                        self.ParPick = ID[j]
                        
                        ####################################
                        #prepare the output for processing
                        self.shared = ('%.2f' % (float((float(k)*100/Container[0]))
                                       +(float(l)*100/(Container[0]*len(Container[2])))
                                       +(float(j)*100/(Container[0]*len(Container[2])*float(Length)))))+'%'
                        
                        #Set it into the queu
                        queue.put(['Progress',self.shared])
                        
                        ####################################
                        #computing something different than
                        #the minimum
                        
                        #Run LeastSquare the parameter is not fixed:
                        if not self.Function_Pointers[idx][self.Current][self.ParPick].ParametersFix[i+1] == 1:
                            
                            ####################################
                            ####################################
                            #Store parameter as array
                            Para = [float(self.Function_Pointers[idx][self.Current][self.ParPick].Parameters[i+1])]
                        
                            ####################################
                            ####################################
                            #fetch the bounds
                            
                            if Container[4][2*i][0]:
                                
                                RelBoundsBool = True
                                RelBounds = [Container[4][2*i][1],Container[4][2*i][2]]
                            
                            else:
                                
                                RelBoundsBool   = False
                                RelBounds       = [0,0]

                            if Container[4][2*i+1][0]:
                                
                                AbsBoundsBool = True
                                AbsBounds = [Container[4][2*i+1][1],Container[4][2*i+1][2]]

                            else:
                            
                                AbsBoundsBool   = False
                                AbsBounds       = [0,0]
                        
                            #launch the logic
                            LocalBounds, Para[0] = self.FetchBounds(Para[0],
                                                                    RelBoundsBool,
                                                                    RelBounds,
                                                                    AbsBoundsBool,
                                                                    AbsBounds)
                            
                            ####################################
                            #Finnally run the computation of
                            #Lorrentzians
                            #Compute
                            try:
                            
                                self.Function_Pointers[idx][self.Current][self.ParPick].Parameters[i+1] = float(least_squares(self.Residuals,
                                                                                                                             Para,
                                                                                                                             args=(Target,
                                                                                                                                   idx,
                                                                                                                                   DataY,
                                                                                                                                   DataX),
                                                                                                                             bounds = LocalBounds,
                                                                                                                             verbose=0).x[0])
                        
                            except:
                                
                                print 'ERROR in fitting:'
                                print 'Parameter: '+str(i+1)+' of the lorrentzian could not be fitted'

        ####################################
        #computing the minimum
        
        self.ParClass = None
        self.ParPick  = None


    def Residuals(self,p,Fun,idx,y,x):
        '''
        ###############################################################################
        This is ht eresidual function that evaluates the deference bewteen the data
        aand the fit. This functon needs:
        - Fun: the function (Lorr, Linea ...) it will fit.
        - p: the parameter to evaluate
        - y: the curve to compare
        - x: the axis to feed.
        ###############################################################################
        '''
        #calculate error
        err = numpy.sum([abs(l) for l in y - Fun(idx,x,p)])*self.FitPrecision
        
        return err
            
    def AllFunctions(self,x,p, Num = None):
        '''
        ###############################################################################
        Draw all the elements
        ###############################################################################
        '''
        #initialise...
        Data  = self.PolyFunction(0,x,p,Num = Num)
        
        for i in range(1,self.NumberOfFunction):
        
            Data  += self.PolyFunction(i,x,p,Num = Num)
        
        return Data
     
    def RaiseLinear(self,x,p, Num = None):
        '''
        ###############################################################################
        Draw all the elements
        ###############################################################################
        '''
        
        if Num == None:
        
            for k in range(0,self.NumberOfFunction):
            
                if not k == 1:
                    
                    for i in range(0,len(self.Function_Pointers[k][self.Current])):

                        self.Function_Pointers[k][self.Current][i].yBis += self.PolyFunction(1,x,p,Num = Num)
    
        else:
        
            for k in range(0,self.NumberOfFunction):
            
                if not k == 1:
                    
                    for i in range(0,len(self.Function_Pointers[k][self.Current])):
            
                        self.Function_Pointers[k][Num][i].yBis += self.PolyFunction(1,x,p,Num = Num)



    
    def ComputeRestCalculation(self, Num):
        '''
        ###############################################################################
        This function cmputes the effective substraction after the fitting has been 
        done and allows the user to export the data...
        ###############################################################################
        '''
        
        #create the initial list
        TargetList = [self.Function_Pointers[0],
                      self.Function_Pointers[1],
                      self.Function_Pointers[2],
                      self.Function_Pointers[3]]
        
        #grab DataX
        DataX = self.CompData[Num].DataX
    
        #grab DataY
        self.ResidualData[Num]  =  [list(self.CompData[Num].DataX),list(self.CompData[Num].DataY)]
    
        #set the target
        for Target in TargetList:
        
            for j in range(0,len(Target[Num])):

                self.ResidualData[Num][1] =  [self.ResidualData[Num][1][l] - Target[Num][j].ReturnData(self.ResidualData[Num][0])[l] for l in range(0,len(self.ResidualData[Num][0]))]
    
    
    def ComputeSubstraction(self,Key, Bool):
        '''
        ###############################################################################
        This function cmputes the effective substraction after the fitting has been 
        done and allows the user to export the data...
        ###############################################################################
        '''
        
        
        #initialise the array
        FinalData = []
        
        #process to the range removal
        for i in range(0,len(self.Function_Pointers[0])):
        
            #grab DataX
            DataX = self.CompData[i].DataX
        
            #grab DataY
            FinalData.append(list(self.CompData[i].DataY))
            
            for kk in range(0,len(self.Function_Info_Pointers)):
                
                for j in range(0,len(self.Function_Pointers[kk][i])):
                    
                    if self.Function_Pointers[kk][i][j].Group == Key.get():
        
                        FinalData[-1] =  [FinalData[-1][l]
                                          - self.Function_Pointers[kk][i][j].ReturnData(DataX)[l]
                                          for l in range(0,len(FinalData[-1]))]
        
                FinalData[-1] = list(FinalData[-1])
                    
#            #fo we process the residue ?
#            if Bool.get() == 1:
#                
#                FinalData[-1] =  [FinalData[-1][l]
#                                  - self.ResidualData[i][l]
#                                  
#                                  for l in range(0,len(FinalData[-1]))]

        #send it out
        return FinalData
    
    def ChiSquare(self,Data,Fit):
        
        '''
        ###############################################################################
        This funciton calculates the left chi square of the funciton
        ###############################################################################
        '''
        
        Variable = Data[:]-Fit[:]
        Variable2 = sum(Variable)/len(Variable)
        
        SSTot = 0
        for i in range(0,len(Data)):
            SSTot += (Data[i]-Variable2)**2
            
        SSRes = 0
        for i in range(0,len(Data)):
            SSRes += (Fit[i]-Data[i])**2
            

        return 1-(SSRes/SSTot)



    def CreateGeneralFit(self,IDNumber,Idx,HowMany):
        '''
        ###############################################################################
        This function is here to create the lorrentzian fits to be introduced 
        into the claculation later on. Changing this sks for recreating a new fit
        and deleting the previous
        
        eventually a speciall command will be put into place to reset simply.
        ###############################################################################
        '''

        #Initiate logging
        LastAct = ''
        
        #Create a while loop for exiting faulty commands
        Stop = False

        while not Stop:

            #check if the index is not out of range to avoid hanging up
            if Idx > len(self.Info):
                LastAct += '\nThe requested fit does not exist, exiting forcefully...'
                Stop = True
                break
        
            #rezero the array
            self.Function_Pointers[IDNumber][Idx] = []

            
            #initiate the fits
            for i in range(0,int(HowMany)):
                
                #initiate the lorentzian class
                self.Function_Pointers[IDNumber][Idx].append(self.Class_Pointer[IDNumber](self.CompData[Idx], self.Function_Info_Pointers[IDNumber]))
                
            #launch a logical variable .isFitted
            self.isFitted = False
            
            LastAct += '\nSucessfully initialisd all fit classes, proceeding...'
            
            break

        return LastAct,HowMany


    def PolyFunction(self,idx,x,p, Num = None):
        '''
        ###############################################################################
        This is the function in charge of building the lorrentzian function
        Note that this version only accepts one parameter at a time
        
        #a new version will be developed in version 0.0.5 allowing for multiple
        inputs.
        ###############################################################################
        '''
        #Initialise the function     
        ytot = numpy.zeros((len(x)))
        xNumPy = numpy.array(x)
            
        #if nothing given
        if Num == None:
        
            ID = self.Current
        
        else:
        
            ID = Num

        for i in range(0,len(self.Function_Pointers[idx][ID])):
            
            #set the parameters
            Parameters = [xNumPy]
            
            #loop
            for j in range(1,len(self.Function_Pointers[idx][ID][i].Parameters)):
                
                #grab the value
                PutIn = float(self.Function_Pointers[idx][ID][i].Parameters[j])
                
                #check are we a variable or a parameter
                if self.ParClass == j - 1 and self.ParPick == i:
                    
                    #we are variable
                    Parameters.append(p[0])
                
                else:
                    
                    #we are parameter
                    Parameters.append(PutIn)

            #fetch the function
            ypar = self.Function_Pointers[idx][ID][i].Function(Parameters)

            #FInalise and send it out
            ytot = ypar + ytot
  
        return ytot



class FitX:
    
    def __init__(self,Parent):
        
        self.CreatedX = []
        
        Factor = 2
        
        for i in range(0,Factor*len(Parent.RawData[Parent.Current].X[Parent.RawData[Parent.Current].IndexX[0]:Parent.RawData[Parent.Current].IndexX[1]])):
            self.CreatedX.append(((numpy.max(Parent.RawData[Parent.Current].X[Parent.RawData[Parent.Current].IndexX[0]:Parent.RawData[Parent.Current].IndexX[1]])-numpy.min(Parent.RawData[Parent.Current].X[Parent.RawData[Parent.Current].IndexX[0]:Parent.RawData[Parent.Current].IndexX[1]]))/(len(Parent.RawData[Parent.Current].X[Parent.RawData[Parent.Current].IndexX[0]:Parent.RawData[Parent.Current].IndexX[1]])*Factor))*i+numpy.min(Parent.RawData[Parent.Current].X[Parent.RawData[Parent.Current].IndexX[0]:Parent.RawData[Parent.Current].IndexX[1]]))


        self.CreatedX = numpy.asarray(self.CreatedX)



class ViewData:
    '''
    ###############################################################################
    In this class we will store the croped data used for the calculation
    this data can be modified once the class is loaded to fit the needs
    
    This is the main fit data class that will be loaded and created for any fit
    instance. In the past the hadnling was messy as it relied on not processing
    properly the information. 
    
    Now we wil linstall a few new self. variables to allow for resizing the 
    parameters
    
    The main paramaters:
    self.isBaseRemoved
    self.WhichBase
    self.isNorm
    self.isMult
    
    All associated parameters
    self.p
    self.Lambda
    self.BaseRange
    self.BaseOrder (only for self.whichBase = 1)
    self.BaseExcl  (only for self.whichBase = 1)
    self.BaseFac
    
    
    
    ###############################################################################
    '''
    
    def __init__(self,X,Y,DataClass):
        
        #copy addreses over localy
        self.DataClass = DataClass
        
        #Saves the initial data for reseting ...
        self.XIni = numpy.copy(X)
        self.YIni = numpy.copy(Y)
        
        #Base information
        self.isBaseRemoved = False
        self.WhichBase     = False
        self.isNorm        = False
        self.isMult        = False
        self.MultFact      = 1
        self.isOffset      = False
        self.Offset        = 0
        
        #initiate reset
        self.Reset()
    
    
    def Set0Values(self):
    
        '''
        ###############################################################################
        #These two variables will determine the range on self.X and self.Y
        #they are the visual backbone and should not be touched
        #Any changes should be performed onto self.X and self.Y as
        #they can be reseted easily.
        ###############################################################################
        '''
        
        #whatever the case always call the SetBaseValues first
        #self.SetBaseValues()
            
        #Fix range into frame
        if self.RangeX[0] < numpy.min(self.X):
            
            self.RangeX[0] = numpy.min(self.X)+0.2

        #Fix range into frame
        if self.RangeX[1] > numpy.max(self.X):
            
            self.RangeX[1] = numpy.max(self.X)-0.2

        #Find associated indexes
        ViewIdx = Utility.FindIdxD(self.RangeX[0],self.RangeX[1],self.X)
        
        
        if ViewIdx[1] < ViewIdx[0]:
            
            self.IndexX = [ViewIdx[1],ViewIdx[0]]
        
        else:
            
            self.IndexX = [ViewIdx[0],ViewIdx[1]]
        
        #set them
        self.X0 = numpy.copy(self.X[self.IndexX[0]:self.IndexX[1]])
        self.Y0 = numpy.copy(self.Y[self.IndexX[0]:self.IndexX[1]])


    def SetBaseValues(self):
    
        '''
        ###############################################################################
        Note that while self.Set0Values() feeds of the X and Y, self.SetBaseValues()
        feeds of self.XIni and self.YIni which are locked throughout the process of the
        scrips until new ones are loaded in. As such it should be noted that 
        
        sel.X and self.Y should be independanttly valid
        ###############################################################################
        '''

        #if base processing is acivated run it
        if self.isBaseRemoved:
            
            #set them
            self.XBase0 = numpy.copy(self.XIni[self.BaseIndexX[0]:self.BaseIndexX[1]])
            self.YBase0 = numpy.copy(self.YIni[self.BaseIndexX[0]:self.BaseIndexX[1]])
            
            #call the procedure
            self.CallBaseRem()
                                       
        else:
            
            #reset
            self.BaseIndexX = [0,len(self.XIni)-1]
            
            #set them
            self.XBase0 = numpy.copy(self.XIni[self.BaseIndexX[0]:self.BaseIndexX[1]])
            self.YBase0 = numpy.copy(self.YIni[self.BaseIndexX[0]:self.BaseIndexX[1]])
            
            #move on manually
            self.X = self.XBase0
            self.Y = self.YBase0

        #check if norm processing is recquired (can be imporeved
        if self.isNorm:
            self.ProcessNorm()
    
        #check if norm processing is recquired (can be imporeved
        if self.isMult:
            self.ProcessMult()

        #check if norm processing is recquired (can be imporeved
        if self.isOffset:
            self.ProcessOffset()

    
    def ProcessNorm(self):
        '''
        ###############################################################################
        Norm processing routine can be imporved further down the road
        ###############################################################################
        '''
        self.Y = self.Y/(numpy.max(self.Y))
        
        print 'Normalised the Data'
                                       
    def ProcessMult(self):
        '''
        ###############################################################################
        Mult processing routine can be imporved further down the road
        ###############################################################################
        '''
        self.Y = self.Y*self.MultFact
        print 'Multiplied the Data'
    
                                           
    def ProcessOffset(self):
        '''
        ###############################################################################
        Mult processing routine can be imporved further down the road
        ###############################################################################
        '''
        self.Y = self.Y+self.Offset
        print 'Set Offset'
                                   
    def Reset(self):
        
        '''
        ###############################################################################
        This reset function will set self.X and self.Y back towards XIni and YIni
        Note that this does not affect the range and as a result set0Values will be
        called at the end of the function
        ###############################################################################
        '''

        #Set a set of initial values
        self.X = numpy.copy(self.XIni)
        self.Y = numpy.copy(self.YIni)
        
        #set the boundaries range
        self.RangeX = [numpy.min(self.X),numpy.max(self.X)]
        self.RangeY = [numpy.min(self.Y),numpy.max(self.Y)]

        #Set the index
        self.IndexX = [0,len(self.X)-1]
        self.IndexY = [0,len(self.Y)-1]
        
        #Do the same for the baseline
        self.BaseIndexX = [0,len(self.XIni)-1]
        
        #Set obs val
        self.Set0Values()
    
    
    def CallBaseRem(self):

        '''
        ###############################################################################
        This is the base removal routine. Not that many function before were called
        externally and this was just imported from the Utility function pool. 
        
        This is now different in order to stay clean. The base removal can be called
        internally witout any arguments
        ###############################################################################
        '''
        
        #Make sure initial view is loaded with the proper boundaries:
        #self.SetBaseValues()

        #Assign/reset our new variables
        self.XBFit = numpy.copy(self.XBase0)
        self.YBFit = numpy.copy(self.YBase0)
        
        #check if we have to work
        if not self.BaseExcl == '':
        
            #transfer from version 2
            self.BaseExclSplit = self.BaseExcl.split(',')

            #Check if the input has an even number of values
            if len(BaseExclSplit) % 2 == 0:

                #Create the removalRange array
                BRemovalRange = []
                Idx = 0
                for i in range(0,int(len(BaseExclSplit)/2)):
                    BRemovalRange.append([BaseExclSplit[Idx],BaseExclSplit[Idx+1]])
                    Idx += 2
                
                #needed variable to keep track or remobval position
                J = 0 
                
                #Remove stuff 
                for i in range(0,len(BRemovalRange)):
                    
                    #find the index
                    RemIdx = Utility.FindIdxD(float(BRemovalRange[i][0]),float(BRemovalRange[i][1]),self.X0)
                    
                    for j in range(RemIdx[1],RemIdx[0]):
                        
                        #Delete from both arrays
                        self.XBFit = numpy.delete(self.XBFit,RemIdx[1]-J,None)
                        self.YBFit = numpy.delete(self.YBFit,RemIdx[1]-J,None)
            else:
                
                #send out problem in case the exclusion range is wrongly formated
                print 'Wrong format, nothing will be changed'
        
        
        #Initialise the string to avoi errors
        BaseText = ''

        '''
        ##########################################
        This is the polynomial baseline handling.
        ##########################################
        '''
        if self.WhichBase == 0:
            
            #Set initial values
            Degree  = self.BaseOrder
            XOffset = [0,0]
            IniPar  = numpy.zeros(1000)
            IniFix  = numpy.zeros(1000)

            #Store old Values or the default initial set of 0's
            oldIniPar = numpy.copy(IniPar)
            oldIniFix = numpy.copy(IniFix)
                
            #Create associated array of variables
            IniPar  = numpy.zeros(int(Degree)+1)
            IniFix  = numpy.zeros(int(Degree)+1)
                
            #calculate
            self.PolynomialFitLorrentz(Degree,XOffset,IniPar,IniFix)
                
            #plot it to have a look
            self.Container = []
            self.Container.append(numpy.copy(self.XBase0))
            self.Container.append(numpy.copy(self.YBase0))
            self.Container.append(numpy.copy(self.XBFit))
            self.Container.append(numpy.copy(self.YBFit))
            self.Container.append(numpy.copy(self.X))
            self.Container.append(numpy.copy(self.BasefitTot))
            
            #convert
            FacVal = float(self.BaseFac)
            
            #Proceed to remove the base
            self.Container.append((FacVal)*numpy.max(self.BasefitTot))
            
            self.BasefitTot = self.BasefitTot - (1-FacVal)*numpy.max(self.BasefitTot)
            self.Y         += -self.BasefitTot
            
            
            #build string
            BaseText += '\nThe baseline was substracted with a polynome of the '+str(Degree)+' degree:\n'
            for i in range(0,len(self.FinalPar)):
                if i == 0:
                    BaseText += str(round(self.FinalPar[i],4))
                else:
                    BaseText += '+'+str(self.FinalPar[i])+'(x-'+str(round(self.FinalXOffset[0],4))+')**'+str(i)

            BaseText += '\nThe goodness of fit is evaluated at'+str(self.ChiSquarePoly)+'\n'

            self.Container.append(BaseText)
        
        '''
        ##########################################
        This is the statistical base remover.
        ##########################################
        '''
        if self.WhichBase == 1:
            
            #define a pointer:
            Result,BaseLine = Utility.TakeBase(self.YBase0.transpose(),self.Lambda,self.p,self.BaseFac)

            self.Container = []
            self.Container.append(numpy.copy(self.XBase0))
            self.Container.append(numpy.copy(self.YBase0))
            self.Container.append(numpy.copy(self.XBase0))
            self.Container.append(numpy.copy(self.YBase0))
            self.Container.append(numpy.copy(self.XBase0))
            self.Container.append(numpy.copy(BaseLine))
            self.Container.append(Result)
            
            self.X = self.XBase0
            self.Y = Result
            
            BaseText += '\nThe baseline was computed and subrstracted'
        print BaseText

    def PolynomialFitLorrentz(self,Degree,XOffset,IniPar,IniFix):
    
        #Fill our two variables with the list of parameters
        self.VarList = IniPar
        self.isPara  = IniFix
        self.XThing  = XOffset
        
        #Create infamouse values list
        self.Values = []
        Index = 0
        
        #fill it by checking if an entry is a variable or parameter
        for i in range(0,len(self.VarList)):
            if self.isPara[i] == 0:
                self.Values.append(float(self.VarList[i]))
                Index +=1
    
        #Add or not the XOffset as a parameter at the start of Values
        if self.XThing[1] == 0:
            self.Values = numpy.concatenate(([self.XThing[0]],self.Values),0)
        
        #Run th eleast square routine
        best_parameters = leastsq(self.Polynomeresiduals,self.Values,args=(self.YBFit,self.XBFit),full_output = 1)[0]
        
        #compute base
        self.BasefitTot = self.Polynome(self.X,best_parameters)
        
        #We need to rebuild the output arrays from Values and isPara
        self.FinalPar = numpy.zeros(len(IniFix))
        self.FinalFix = IniFix
        
        #Fetch the data  
        Index = 0
            
        if self.XThing[1] == 1:
            self.FinalXOffset = self.XThing
            for i in range(0,len(IniFix)):
                if IniFix[i] == 0:
                    self.FinalPar[i] = best_parameters[Index]
                    Index += 1
                else:
                    self.FinalPar[i] = self.IniPar[i]
        else:
            self.FinalXOffset = [best_parameters[0],0]
            for i in range(0,len(IniFix)):
                if IniFix[i] == 0:
                    self.FinalPar[i] = best_parameters[Index+1]
                    Index += 1
                else:
                    self.FinalPar[i] = self.IniPar[i]
                    
        #Calculate goodness of fit
        self.ChiSquarePoly = self.ChiSquare(self.YBFit,self.Polynome(self.XBFit,best_parameters))
    
    def Polynomeresiduals(self,p,y,x):
        
        err = y - self.Polynome(x,p)
        
        return err

    def Polynome(self,x,p):
        #Build the lorrentzian functions in a for loop
        ypar   = 0

        if self.XThing[1] == 0:
            
            for j in range(1,len(p)):
                
                if self.isPara[j-1] == 0:
                    
                    ypar += p[j]*(x-p[0])**(j-1)
                
                else:
                    
                    ypar += self.VarList[j-1]*(x-p[0])**(j-1)
        else:
            
            for j in range(0,len(p)-1):
                
                if self.isPara[j] == 0:
                    
                    ypar += p[j]*(x-self.XThing[0])**(j)
                
                else:
                    ypar += self.VarList[j]*(x-self.XThing[0])**(j)
        #print ypar
        return ypar

    def ChiSquare(self,Data,Fit):
        Variable = Data[:]-Fit[:]
        Variable2 = sum(Variable)/len(Variable)
        
        SSTot = 0
        for i in range(0,len(Data)):
            SSTot += (Data[i]-Variable2)**2
            
        SSRes = 0
        for i in range(0,len(Data)):
            SSRes += (Fit[i]-Data[i])**2
            

        return 1-(SSRes/SSTot)

class CalcData:
    '''
    ###############################################################################
    In this class we will store the croped data used for the calculation
    this data can be modified once the class is loaded to fit the needs
    ###############################################################################
    '''

    def __init__(self,RawData):
    
        #link up the two classes
        self.RawData = RawData
    
        #init
        self.Init = True
        
        #init
        self.BaseExcl = ''
        
        #launch the load fucntion
        self.LoadCalc()
    
        #Load remove range
        self.RemoveRanges()
    
    def LoadCalc(self):
    
        '''
        ###############################################################################
        In this function we want to load all the according elements into place
        This function can also be used later to reset the Calc range if the 
        view range has been changed
        
        Recalling it will obviously clean the previous data
        ###############################################################################
        '''
        
        #for loging
        LastAct = ''
        
        #Set numbers
        self.X = numpy.copy(self.RawData.X0)
        self.Y = numpy.copy(self.RawData.Y0)
        
        LastAct += '\nLoaded calculation arrays localy, proceeding...'

        #set the boundaries range
        if self.Init:
            
            self.ViewRange = [numpy.min(self.X),numpy.max(self.X)]
            self.Init = False

        LastAct += '\nInitialised ranges, proceeding...'
        
        #Set the index
        #Fix range into frame
        
        if self.ViewRange[0] < numpy.min(self.X):
            self.ViewRange[0] = numpy.min(self.X)+0.2


        #Fix range into frame
        if self.ViewRange[1] > numpy.max(self.X):
            self.ViewRange[1] = numpy.max(self.X)-0.2

        #Find associated indexes
        ViewIdx = Utility.FindIdxD(self.ViewRange[0],self.ViewRange[1],self.X)

        if ViewIdx[1] < ViewIdx[0]:
        
            self.IndexX = [ViewIdx[1],ViewIdx[0]]
    
        else:
        
            self.IndexX = [ViewIdx[0],ViewIdx[1]]

        #Set the index range
        self.IndexXTot = range(0,len(self.X)-1)
        self.EditFitRange = False
        self.removalRange = []
        LastAct += '\nInitialised Indexi, proceeding...'
        
        #safety measure
        self.isFitted  = False
        
        return LastAct

    def ResetIdx(self):
        
        '''
        ###############################################################################
        Some regions can be omited for calculations. As a result we have here a reset
        routine allowing us to take all into account again. 
        
        it basically resets the range from the first element to the last of self.X
        ###############################################################################
        '''

        #for loging
        LastAct = ''
        
        #Set the index range
        #self.IndexX = [0,len(self.X)-1]
        self.EditFitRange = False
        self.removalRange = []
        LastAct += '\nMade a reset of the index, proceeding...'

        return LastAct


    def RemoveRanges(self):
    
        '''
        ###############################################################################
        Cleans regions of the plot using the exclusion routine
        this should be only called after reinitilising the arrays oblviously
        ###############################################################################
        '''

        #initialise
        self.DataX = numpy.copy(self.X[self.IndexX[0]:self.IndexX[1]])
        self.DataY = numpy.copy(self.Y[self.IndexX[0]:self.IndexX[1]])
        
        #check if we have to work
        if not self.BaseExcl == '':
        
            #transfer from version 2
            self.BaseExclSplit = self.BaseExcl.split(',')
            
            #Check if the input has an even number of values
            if len(self.BaseExclSplit) % 2 == 0:

                #Create the removalRange array
                self.BRemovalRange = []
                Idx = 0
                for i in range(0,int(len(self.BaseExclSplit)/2)):
                    self.BRemovalRange.append([self.BaseExclSplit[Idx],self.BaseExclSplit[Idx+1]])
                    Idx += 2
                
                #Set J
                J = 0
                
                #Remove stuff
                for i in range(0,len(self.BRemovalRange)):
                    
                    #find the index
                    Buffer = Utility.FindIdxD(float(self.BRemovalRange[i][0]),float(self.BRemovalRange[i][1]),self.DataX)
                    
                    
                    #check
                    if Buffer[0] > Buffer[1]:
                    
                        self.RemIdx = [Buffer[1], Buffer[0]]
                    
                    else:
                    
                        self.RemIdx = [Buffer[0], Buffer[1]]
                    
                    #execute
                    for j in range(self.RemIdx[0],self.RemIdx[1]):
                        
                        #Delete from both arrays
                        self.DataX = numpy.delete(self.DataX,self.RemIdx[0]-J,None)
                        self.DataY = numpy.delete(self.DataY,self.RemIdx[0]-J,None)
            
                self.EditFitRange = True
                self.removalRange = self.BRemovalRange
        
            else:
                
                #send out problem in case the exclusion range is wrongly formated
                self.EditFitRange = False

        else:
            self.EditFitRange = False
    
        #create to numpy
        self.DataX = numpy.asarray(self.DataX)
        self.DataY = numpy.asarray(self.DataY)


