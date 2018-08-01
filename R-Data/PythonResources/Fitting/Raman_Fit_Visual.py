# -*- coding: utf-8 -*-
"""
Created on Mon May 11 10:30:43 2015

@author: Schober 
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




class DrawClass:
    '''
    ###############################################################################
    This class serves the purpose of accelerated redrawing of the plot and
    readjusting of the visual parameters such as the width, color ,shape,
    symbols and so on.
    
    Note that most of the function will be treated in links and types
    
    
    Note also that this class underwent a major rework to accomodate for the custon
    drqwer in version 0.1.0. This implies a complete chnage in the way draw
    elements were triggered.
    ###############################################################################
    '''

    def __init__(self, DataClass):

        #link it back
        self.DataClass = DataClass
        
        #take over deeper class adress
        self.Current         = self.DataClass.Current
        self.CompData        = self.DataClass.CompData
        self.RawData         = self.DataClass.RawData
        self.FitTot          = self.DataClass.FitTot
        self.Residual        = self.DataClass.ResidualData
        self.Functions       = self.DataClass.Function_Pointers
        self.FunctionInfos   = self.DataClass.Function_Info_Pointers
        
        #scatter plot logic variables
        self.ToggleLines()
        
        #To avoid recalling define length here
        self.Length = len(self.CompData)
    
        #Create all
        self.CreateAll()
    
    
    def CreateAll(self):
        '''
        ###############################################################################
        This will build all linkage of the classes
        ###############################################################################
        '''
        
        ###########################################################
        #Common pointers towards the lorrentzian parts
        
        #Fill raw Data Pointer
        self.RawPointer   = RawPlot(self.RawData,self.RawData)
            
        #Fill comp data
        self.CompPointer  = CompPlot(self.CompData,self.CompData)
        
        #Fill comp data
        self.RestPointer  = RestPlot(self.Residual,self.Residual)
            
        #fill total fit
        self.FitPointer   = FitPlot(self.FitTot)
        
        #Boxes instance
        self.BoxPointer   = BoxPlot(self.RawData,self.CompData)

        #fill total fitself.Fig
        self.Function_Pointers  = FunctionManager(self.Functions)
    
        ###########################################################
        #Common pointers towards the scatter parts
        
        #ScatterPOinter list
        self.ScatterPointerList = [None]*len(self.Functions)
        
        for kk in range(len(self.Functions)):

            self.ScatterPointerList[kk] = [None]*self.FunctionInfos[kk].ParameterNumber

            for ll in range(self.FunctionInfos[kk].ParameterNumber):
    
                self.ScatterPointerList[kk][ll] = ScatterClass(self.DataClass, Type = [kk,ll])
    
    def Place(self,Target, Type = [0, 0, '', False], Update = False):
        '''
        ###############################################################################
        The placer method is here to place an element on the plot if it has been
        selected.
        ###############################################################################
        '''
        
        self.FitType = Type
        Update = False
        
        ###########################################################################
        #These clases are to visualize to common Lorrentzian plots
        Target.Reset()
        
        
        if Type[0] < 9:
            
            #set pointer stickyness
            Target.Pointer.Sticky = 1
        
            #set the x axis to scientific
            Target.Axes.isXSci         = [False,False]
            Target.Pointer.isXSci      = [False,False]
                
        else:
        
        
            #set pointer stickyness
            Target.Pointer.Sticky = 2
        
            #set the x axis to scientific
            Target.Axes.isXSci         = [True,True]
            Target.Pointer.isXSci      = [True,True]
        
        #Raw show class
        if Type[0] == 0:
            
            if not Update:
            
                #Draw the data with the class
                self.RawPointer.Draw(Target,self.DataClass.Current)
            
            else:
                
                try:
                    #Update the data with the class
                    self.RawPointer.Update(self.DataClass.Current)
                        
                except:
                    
                    #clear all as we failed
                    Target.RemoveAllPlots()
                    self.ClearCurrentPLot(Target)
                
                    #draw the current plots
                    self.RawPointer.Draw(Target,self.DataClass.Current)
    
        if Type[0] == 1:

            if not Update:
                
                #try to draw the plots
                self.RawPointer.Draw(Target,self.DataClass.Current)
                self.CompPointer.Draw(Target,self.DataClass.Current)
                self.BoxPointer.Draw(Target)

            else:
                
                try:
                    #try to update the plots
                    self.RawPointer.Update(self.DataClass.Current)
                    self.CompPointer.Update(self.DataClass.Current)
                    self.BoxPointer.Draw(Target)

                except:
                    
                    #clear all as we failed
                    Target.RemoveAllPlots()
                    self.ClearCurrentPLot(Target)
                
                    #draw the current plots
                    self.RawPointer.Draw(Target,self.DataClass.Current)
                    self.CompPointer.Draw(Target,self.DataClass.Current)
                    self.BoxPointer.Draw(Target)

        if Type[0] == 2:


            if not Update:
            
                self.CompPointer.Draw(Target,self.DataClass.Current)
                self.BoxPointer.Draw(Target)
            
                if self.CompData[self.DataClass.Current].isFitted:
                
                    #load total
                    self.FitPointer.Draw(Target,self.DataClass.Current)
                
                    #load the lorrentzians
                    self.Function_Pointers.CallDraw(Target,self.DataClass.Current)
            else:
                
                #load the lorrentzians
                self.Function_Pointers.Update(self.DataClass.Current)
                
                try:
                    
                    self.CompPointer.Update(self.DataClass.Current)
                    self.BoxPointer.Draw(Target)
                
                    if self.CompData[self.DataClass.Current].isFitted:
                    
                        #load total
                        self.FitPointer.Update(self.DataClass.Current)
                    
                        #load the lorrentzians
                        self.Function_Pointers.Update(self.DataClass.Current)

                except:
                    
                    #clear all as we failed
                    Target.RemoveAllPlots()
                    self.ClearCurrentPLot(Target)
                
                    #draw the current plots
                    self.CompPointer.Draw(Target,self.DataClass.Current)
                    self.BoxPointer.Draw(Target)
            
                    if self.CompData[self.DataClass.Current].isFitted:
                
                        #load total
                        self.FitPointer.Draw(Target,self.DataClass.Current)
                
                        #load the lorrentzians
                        self.Function_Pointers.CallDraw(Target,self.DataClass.Current)

        if Type[0] == 3:
            
            if not Update:
                
                #try to draw the plots
                self.RestPointer.Draw(Target,self.DataClass.Current)
                self.BoxPointer.Draw(Target)

            else:
                
                try:
                    #try to update the plots
                    self.RestPointer.Update(self.DataClass.Current)
                    self.BoxPointer.Draw(Target)

                except:
                    
                    #clear all as we failed
                    Target.RemoveAllPlots()
                    self.ClearCurrentPLot(Target)
                
                    #draw the current plots
                    self.RestPointer.Draw(Target,self.DataClass.Current)
                    self.BoxPointer.Draw(Target)
        
        ###########################################################################
        #These plots are the scatter plots managing data visualisation
        
        #Raw show class
        if Type[0] > 9:

            #Call the draw method
            self.ScatterPointerList[Type[0] - 10][Type[1]].Draw(Target,
                                                                Normalised = Type[3],
                                                                Lines = self.ToggleLinesBool)


        Target.Zoom()
    

    def ClearCurrentPLot(self,Target):
        '''
        ###############################################################################
        A switch recquires a cleanup
        ###############################################################################
        '''
        self.RawPointer.Clear(Target)
        
        self.CompPointer.Clear(Target)
        
        self.FitPointer.Clear(Target)

        self.Function_Pointers.Clear(Target)
        
        self.Function_Pointers.WasDrawn = False

    def UpdateAll(self):
        '''
        ###############################################################################
        A switch recquires a cleanup
        ###############################################################################
        '''
        self.RawPointer.Update(self.DataClass.Current)
        
        self.CompPointer.Update(self.DataClass.Current)
        
        self.FitPointer.Update(self.DataClass.Current)

        self.Function_Pointers.Update(self.DataClass.Current)
            
    def SetWindow(self,Target):
        '''
        ###############################################################################
        A switch recquires a cleanup
        ###############################################################################
        '''
        #initialise
        XMin = []
        XMax = []
        YMin = []
        YMax = []
        
        
        if self.FitType == 0 or self.FitType == 1:
            #append
            XMin.append(self.RawPointer.XMin)
            YMin.append(self.RawPointer.YMin)
            XMax.append(self.RawPointer.XMax)
            YMax.append(self.RawPointer.YMax)
        
        if self.FitType == 1 or self.FitType == 2:
            #append comp min
            XMin.append(self.CompPointer.XMin)
            YMin.append(self.CompPointer.YMin)
            XMax.append(self.CompPointer.XMax)
            YMax.append(self.CompPointer.YMax)
        
        #try to append lorrentzian minima
        if self.FitType == 2:
            try:
                
                YMin.append(self.Function_Pointers.YMin)
                YMax.append(self.Function_Pointers.YMax)
            
            except:
                
                pass
    
    
        if self.FitType > 3 and self.FitType < 13:
        
            #grab it from the window
            YMin.append(self.ScatterPointerList[self.FitType-4].Min)
            YMax.append(self.ScatterPointerList[self.FitType-4].Max)
                
        if self.FitType > 13:
        
            #grab it from the window
            YMin.append(self.ScatterPointerList[self.FitType-14].Min)
            YMax.append(self.ScatterPointerList[self.FitType-14].Max)

        #set the x limit
        if self.FitType < 3:
            
            #set limits
            Target.set_xlim(numpy.min(XMin),numpy.max(XMax))
        
        if self.FitType > 3 and self.FitType < 13:
            
            #set limits
            Target.set_xlim(-1,len(self.ScatterPointerList[self.FitType-4].XArray))

        if self.FitType > 13:

            #set limits
            Target.set_xlim(-1,len(self.ScatterPointerList[self.FitType-14].XArray))
    
        #Set teh y limit
        if numpy.max(YMax)-numpy.min(YMin) > 0.1:
            Target.set_ylim(numpy.min(YMin) - 0.1 * (numpy.max(YMax)-numpy.min(YMin)),numpy.max(YMax) + 0.1 * (numpy.max(YMax)-numpy.min(YMin)))
        else:
            Target.set_ylim(numpy.min(YMin) - 0.1,numpy.max(YMax) + 0.1 )


    def ToggleLines(self, Toggle = False):
        
        '''
        ###############################################################################
        This method will callt the toggle on the scatter plot if it is asked
        
        Note that this will call the place method
        ###############################################################################
        '''
    
        if Toggle:
    
            self.ToggleLinesBool = not self.ToggleLinesBool

        else:
            
            self.ToggleLinesBool = False


class ScatterClass:
    
    '''
    ###############################################################################
    This will create the associated scatter plot
    
    Note that self.Type gives the variable index we ar elooking at
    
    0 : Position
    1 : HWHM
    2 : Factor
    3 : Minimum
    ###############################################################################
    '''
    
    def __init__(self, Pointers, Type = [10,0]):
        
        #Initialise
        self.Pointer  = Pointers
        self.Type     = Type
        self.Focus    = None
        
        #Grab the name of the function
        self.Name = self.Pointer.Function_Info_Pointers[Type[0]].ParameterNames[self.Type[1]]
    
        self.Function = self.Pointer.Function_Pointers[Type[0]]

    def Draw(self,Target , Normalised = False, Lines = False):
        
        #Initialise the Y array full of Y arrays
        try:
            del self.YArray
        except:
            pass
        
        
        #defien YArray
        self.YArray = []
        self.XArray = []
        self.Colors = []
        
        #define XArray
        #self.XArray = self.Pointer.XArray
        
        #cycles though all the lorrentzians and create the arrays
        for j in range(0,len(self.Function[0])):
            
            #Set Buffer
            Buffer = []
            Buffer_2 = []
                
            #go thourgh
            for i in range(0,len(self.Function)):
                
                if not self.Function[i][j].Zero:
                
                    #set it
                    Buffer.append(self.Function[i][j].Parameters[self.Type[1]+1])

                    #set it
                    Buffer_2.append(self.Pointer.XArray[i])
            
            #Debug visual
            #print 'This is the value set', Buffer
            self.YArray.append(list(Buffer))
            self.XArray.append(list(Buffer_2))
            self.Colors.append(self.Function[0][j].Color)
    

        #Draw it on the target
        self.MinList = [None]
        self.MaxList = [None]

        #put it on
        for i in range(len(self.Function[0])):
            
            #select if trace
            if self.Function[0][i].Trace:
                
                if  len(self.XArray[i])>0:
                    
                    #check norm condition
                    if not Normalised:
                        
                        #lines or not
                        if not Lines:
                            
                            #draw scatter plot
                            Target.AddPlot(self.XArray[i],
                                           self.YArray[i],
                                           color = self.Colors[i],
                                           Thickness = 0,
                                           style = ['o',4,4])
                        
                        else:
                            
                            #draw lineplot
                            Target.AddPlot(self.XArray[i],
                                           self.YArray[i],
                                           color = self.Colors[i],
                                           Thickness = int(2.5),
                                           style = ['o',4,4])
                        
                    
                        #grab max and min
                        self.MinList.append(numpy.min(self.YArray[i]))
                        self.MaxList.append(numpy.max(self.YArray[i]))
                
                    else:
                        
                        if not Lines:
                        
                            #use scatter plot
                            Target.AddPlot(self.XArray[i],
                                           Utility.normalize(self.YArray[i]),
                                           color = self.Colors[i],
                                           Thickness = 0,
                                           style = ['o',4,4])
                        
                        else:
                            
                            #draw lineplot
                            Target.AddPlot(self.XArray[i],
                                           Utility.normalize(self.YArray[i]),
                                           color = self.Colors[i],
                                           Thickness = int(2.5),
                                           style = ['o',4,4])
                        
                        #grab max and min
                        self.MinList.append(numpy.min(Utility.normalize(self.YArray[i])))
                        self.MaxList.append(numpy.max(Utility.normalize(self.YArray[i])))


        #if no focus display them all
        if self.Focus == None:
            
            #grab min
            self.Min = numpy.min(self.MinList)
            
            #grab the max
            self.Max = numpy.max(self.MaxList)

        #else grab focus
        else:

            #grab min
            self.Min = self.MinList[self.Focus]
            
            #grab the max
            self.Max = self.MaxList[self.Focus]


class RawPlot:

    '''
    ###############################################################################
    This will be the class for the raw plot
    
    It will be the first instalement.
    ###############################################################################
    '''

    def __init__(self, XPointer, YPointer):

        #define the
        self.X = XPointer
        self.Y = YPointer
        self.Color = 'blue'
        self.Thickness = 1.5

    def Draw(self, Target, Current):
        
        #try to clear the artists first
        self.Clear(Target)
        
        #here we call the draw method and return the artist
        self.Artist = Target.AddPlot(self.X[Current].XIni,
                                     self.Y[Current].YIni,
                                     color = self.Color,
                                     Name = 'Raw Data',
                                     Thickness = int(self.Thickness))
        
        #Limitscomputation
        self.XMin = numpy.min(self.X[Current].XIni)
        self.YMin = numpy.min(self.Y[Current].YIni)
        self.XMax = numpy.max(self.X[Current].XIni)
        self.YMax = numpy.max(self.Y[Current].YIni)

        return self

    def Update(self,Current):
        try:
            #here we call the draw method and return the artist
            self.Artist.X = numpy.copy(self.X[Current].XIni)
            self.Artist.Y = numpy.copy(self.Y[Current].YIni)
        
            #Limitscomputation
            self.XMin = numpy.min(self.X[Current].XIni)
            self.YMin = numpy.min(self.Y[Current].YIni)
            self.XMax = numpy.max(self.X[Current].XIni)
            self.YMax = numpy.max(self.Y[Current].YIni)
        
        except:
            pass

    
    def Clear(self,Target):


        try:

            Target.DelPlot(self.Artist)

        except:
            pass



class CompPlot:

    '''
    ###############################################################################
    This will be the class for the fit plot
    
    It will be the first instalement.
    ###############################################################################
    '''

    def __init__(self, XPointer, YPointer):


        #define the
        self.X = XPointer
        self.Y = YPointer
        
        self.Color = 'red'
        self.Thickness = 2.5

    def Draw(self, Target, Current, Line = False):

        #try to clear the artists first
        self.Clear(Target)
        
        #here we call the draw method and return the artist
        self.Artist = Target.AddPlot(self.X[Current].DataX,
                                     self.Y[Current].DataY,
                                     color = self.Color,
                                     Name = 'Used Data Range',
                                     Thickness = int(self.Thickness))
        
        #Limitscomputation
        self.XMin = numpy.min(self.X[Current].DataX)
        self.YMin = numpy.min(self.Y[Current].DataY)
        self.XMax = numpy.max(self.X[Current].DataX)
        self.YMax = numpy.max(self.Y[Current].DataY)
        
        return self

    def Update(self,Current):
        
        #here we call the draw method and return the artist
        self.Artist.X = numpy.copy(self.X[Current].DataX)
        self.Artist.Y = numpy.copy(self.Y[Current].DataY)
        
        #Limitscomputation
        self.XMin = numpy.min(self.X[Current].DataX)
        self.YMin = numpy.min(self.Y[Current].DataY)
        self.XMax = numpy.max(self.X[Current].DataX)
        self.YMax = numpy.max(self.Y[Current].DataY)
    
    def Clear(self,Target):

        try:
            Target.DelPlot(self.Artist)

        except:
            pass

class RestPlot:

    '''
    ###############################################################################
    This will be the class for the raw plot
    
    It will be the first instalement.
    ###############################################################################
    '''

    def __init__(self, XPointer, YPointer):

        #define the
        self.X = XPointer
        self.Y = YPointer
        self.Color = 'blue'
        self.Thickness = 1.5

    def Draw(self, Target, Current):
        
        #try to clear the artists first
        self.Clear(Target)
        
        #here we call the draw method and return the artist
        self.Artist = Target.AddPlot(self.X[Current][0],
                                     self.Y[Current][1],
                                     color = self.Color,
                                     Name = 'Residual Data',
                                     Thickness = int(self.Thickness))
        
        #Limitscomputation
        self.XMin = numpy.min(self.X[Current][0])
        self.YMin = numpy.min(self.Y[Current][1])
        self.XMax = numpy.max(self.X[Current][0])
        self.YMax = numpy.max(self.Y[Current][1])

        return self

    def Update(self,Current):
        try:
            #here we call the draw method and return the artist
            self.Artist.X = numpy.copy(self.X[Current][0])
            self.Artist.Y = numpy.copy(self.Y[Current][1])
        
            #Limitscomputation
            self.XMin = numpy.min(self.X[Current][0])
            self.YMin = numpy.min(self.Y[Current][1])
            self.XMax = numpy.max(self.X[Current][0])
            self.YMax = numpy.max(self.Y[Current][1])
        
        except:
            pass

    
    def Clear(self,Target):


        try:

            Target.DelPlot(self.Artist)

        except:
            pass

class FitPlot:

    '''
    ###############################################################################
    This will be the class for the fit plot
    
    It will be the first instalement.
    ###############################################################################
    '''

    def __init__(self, Pointer):


        #define the
        self.Pointer = Pointer
        
        
        self.Color = 'black'
        self.Thickness = 4

    def Draw(self, Target, Current):


        #try to clear the artists first
        self.Clear(Target)
        
        try:
        
            #here we call the draw method and return the artist
            self.Artist = Target.AddPlot(self.Pointer[Current][0],
                                         self.Pointer[Current][1],
                                         color = self.Color,
                                         Name = 'Fited Curve',
                                         Thickness = int(self.Thickness))
            
            #Limitscomputation
            self.XMin = numpy.min(self.Pointer[Current][0])
            self.YMin = numpy.min(self.Pointer[Current][1])
            self.XMax = numpy.max(self.Pointer[Current][0])
            self.YMax = numpy.max(self.Pointer[Current][1])
        
        except:
            pass
        return self

    def Update(self,Current):
        
        #here we call the draw method and return the artist
        self.Artist.X = numpy.copy(self.Pointer[Current][0])
        self.Artist.Y = numpy.copy(self.Pointer[Current][1])
        
        #Limitscomputation
        self.XMin = numpy.min(self.Pointer[Current][0])
        self.YMin = numpy.min(self.Pointer[Current][1])
        self.XMax = numpy.max(self.Pointer[Current][0])
        self.YMax = numpy.max(self.Pointer[Current][1])
    
    def Clear(self,Target):

        try:
            Target.DelPlot(self.Artist)

        except:
            pass


class FunctionManager:

    '''
    ###############################################################################
    This will be the class for the fit plot
    
    It will be the first instalement.
    ###############################################################################
    '''

    def __init__(self,Pointer):


        #define the
        self.Pointer    = Pointer
        self.isFit      = False
        self.WasDrawn   = False
    
        #call the builder
        self.CallBuild(Pointer)
    

    def CallBuild(self,Pointer):
        
        #This will be called by the fit function to assure linkage
        self.Pointer = Pointer
    
        #this is the build caller
        self.CallFunctionLinkBuilder()

    def CallFunctionLinkBuilder(self):
    
        #create the variable
        self.FunctionLink = []
        
        #cycle through all function
        for kk in range(len(self.Pointer)):
            if len(self.Pointer[kk]) > 0:
                
                #call the constructor
                for i in range(0,len(self.Pointer[kk][0])):
            
                    #initialise individual class
                    self.FunctionLink.append(FunctionPlot(self.Pointer[kk],i))

    def CallDraw(self,Target, Current):
        
        #try to clear
        try:
            self.Clear()
        except:
            pass
        
        #call the builder
        self.CallFunctionLinkBuilder()
        
        Artists = []
        
        #cycle through all function
        for j in range(len(self.FunctionLink)):
        
            #initialise individual class
            Artists.append(self.FunctionLink[j].Draw(Target,
                                                     Current))
    
    
        #get out the last
        self.WasDrawn = True

        
        #initialise
        self.XMin = []
        self.YMin = []
        self.XMax = []
        self.YMax = []
        
        #here we will cycle though the draws
        for i in range(len(self.FunctionLink)):
        
            try:
                #fetch all
                self.XMin.append(self.FunctionLink[i].XMin)
                self.YMin.append(self.FunctionLink[i].YMin)
                self.XMax.append(self.FunctionLink[i].XMax)
                self.YMax.append(self.FunctionLink[i].YMax)
        
            except:
                pass
    
        try:
        
            #now find min and max
            self.XMin = numpy.min(self.XMin)
            self.YMin = numpy.min(self.YMin)
            self.XMax = numpy.max(self.XMax)
            self.YMax = numpy.max(self.YMax)
        
        except:
            pass
        
        return self
    
    def Update(self, Current):
    
        #here we will cycle though the draws
        for i in range(len(self.FunctionLink)):
            
            #initialise individual class
            self.FunctionLink[i].Update(Current)
    
        #initialise
        self.XMin = []
        self.YMin = []
        self.XMax = []
        self.YMax = []
        
        #here we will cycle though the draws
        for i in range(len(self.FunctionLink)):
        
            #fetxh all
            self.XMin.append(self.FunctionLink[i].XMin)
            self.YMin.append(self.FunctionLink[i].YMin)
            self.XMax.append(self.FunctionLink[i].XMax)
            self.YMax.append(self.FunctionLink[i].YMax)
        
        try:
        
            #now find min and max
            self.XMin = numpy.min(self.XMin)
            self.YMin = numpy.min(self.YMin)
            self.XMax = numpy.max(self.XMax)
            self.YMax = numpy.max(self.YMax)
        
        except:
            pass
    
    def Clear(self,Target):

        #here we will cycle though the draws
        for i in range(0,len(self.Pointer[0])):
            
            #initialise individual class
            self.FunctionLink[i].Clear()


class FunctionPlot:

    '''
    ###############################################################################
    This will be the class for the fit plot
    
    It will be the first instalement.
    ###############################################################################
    '''

    def __init__(self,Pointer,Idx):


        #define the
        self.Pointer        = Pointer
        self.FunctionIdx    = Idx

    def Draw(self, Target, Current):
        
        #make current target self
        self.CurrentTarget = Target
        try:
        
            if self.Pointer[Current][self.FunctionIdx].Trace:
                
                #here we call the draw method and return the artist
                self.Artist = Target.AddPlot(self.Pointer[Current][self.FunctionIdx].x,
                                             self.Pointer[Current][self.FunctionIdx].yBis,
                                             Thickness = self.Pointer[Current][self.FunctionIdx].Thickness,
                                             color = self.Pointer[Current][self.FunctionIdx].Color)
                
                try:
                    self.XMin = numpy.min(self.Pointer[Current][self.FunctionIdx].x)
                    self.YMin = numpy.min(self.Pointer[Current][self.FunctionIdx].yBis)
                    self.XMax = numpy.max(self.Pointer[Current][self.FunctionIdx].x)
                    self.YMax = numpy.max(self.Pointer[Current][self.FunctionIdx].yBis)
                
                except:
                    pass
    
            else:
                
                self.Artist = None

        except:
                self.Artist = None
        
        return self.Artist

    def Update(self,Current):
        
        #here we call the draw method and return the artist
        self.Artist.X = numpy.copy(self.Pointer[Current][self.FunctionIdx].x)
        self.Artist.Y = numpy.copy(self.Pointer[Current][self.FunctionIdx].yBis)
        
        #Limitscomputation
        try:
            self.XMin = numpy.min(self.Pointer[Current][self.FunctionIdx].x)
            self.YMin = numpy.min(self.Pointer[Current][self.FunctionIdx].yBis)
            self.XMax = numpy.max(self.Pointer[Current][self.FunctionIdx].x)
            self.YMax = numpy.max(self.Pointer[Current][self.FunctionIdx].yBis)
        except:
            pass

    def Clear(self):

        try:
            self.CurrentTarget.DelPlot(self.Artist)

        except:
            pass

class TitleText:

    '''
    ###############################################################################
    This class will manage the default title setup
    ###############################################################################
    '''

    def __init__(self):
        pass


class LegendText:
    
    '''
        ###############################################################################
        This class will manage the default title setup
        ###############################################################################
        '''
    
    def __init__(self):
        pass

class SmallText:

    '''
    ###############################################################################
    This class will manage the default title setup
    ###############################################################################
    '''

    def __init__(self):
        pass

class BoxPlot:
    
    '''
        ###############################################################################
        This will be the class for the fit plot
        
        It will be the first instalement.
        ###############################################################################
        '''
    
    def __init__(self,Pointer_0,Pointer_1):
        
        
        #define the
        self.Gamma = 0.9
        
        self.Pointer_0 = Pointer_0
        self.Pointer_1 = Pointer_1
    
    
    def Draw(self, Target):
        
        #Do we have ranges
        if not self.Pointer_1[0].EditFitRange:
            pass
        
        #we have
        else:

            #Loop though ranges
            for i in range(0,len(self.Pointer_1[0].removalRange)):
                
                #Get the values
                R1 = self.Pointer_1[0].removalRange[i]
                
                #put the patches
                Target.AddRange([float(R1[0]),float(R1[1])])
               
        #Get the values
        R1 = numpy.min(self.Pointer_0[0].X0)
        R2 = numpy.min(self.Pointer_1[0].DataX)
        
        #put the patches
        Target.AddRange([R1,R2])
                
        #Get the values
        R1 = numpy.max(self.Pointer_0[0].X0)
        R2 = numpy.max(self.Pointer_1[0].DataX)

        #put the patches
        Target.AddRange([R1,R2])
        

    
    def Clear(self):
        
        try:
            pass
        
        except:
            pass

