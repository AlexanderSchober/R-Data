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

'''
############################################################
This function will determine if the system is running on 
windows and then shape the volume part of the file path 
accordingly
############################################################
'''
def IsWindows():
    
    #check if os.name is a 'nt' systeme
    if os.name == 'nt':
        
        return True
    
    else:
        
        return False

def IsLinux():
    
    if os.name == 'posix' and not sys.platform == 'darwin':
        
        return True
    
    else:
        
        return False

'''
############################################################
As the name indicates this function will return the boolean 
value True or False depending on the fact that the path 
links either to a file or folder (redundency with IsFile 
as when a path is not a folder it probably links to a file 
but who knows)
############################################################
'''
def IsFolder(Path):
    
    #compute
    Bool = os.path.isdir(Path)
    
    return Bool
    
'''
############################################################
This function will return the boolean value depending if the 
path links to a file or folder.
############################################################
'''
def IsFile(Path):
    
    Bool = not os.path.isdir(Path)
    
    return Bool


'''
############################################################
This routine is to grab the folder form a specific path.
############################################################
'''

def GetFolderName(Path):
    
    Path, Filename = os.path.split(Path)
    
    return Path

'''
############################################################
This routine is to grab the file form a specific path.
############################################################
'''

def GetFileName(Path):
    
    Path, Filename = os.path.split(Path)
    
    return Filename

'''
############################################################
Simple check if the path to a folder exists on the 
current machine
############################################################
'''

def FolderExists(Path):
    
    Bool = os.path.exists(Path)
    
    return Bool

'''
############################################################
Simple check if the path to a file exists
############################################################
'''    
def FileExists(Path):
    
    Bool = os.path.exists(Path)
    
    return Bool



'''
############################################################
This will handle the preference file system read
############################################################
'''
#Changes dedefualt path txt files
def SetIni(home,n):
    
    #Set the folder Windows specific handling done within
    inTxt  = GetRuntimeTextFile(['Preferences.txt'], Parent = True)
    
    #if we handle the input folder
    if n == 0:

        #Write the text file        
        ReplaceLineContent(inTxt, '<-PathIn->', home)
        
    #if we handle the output folder
    if n == 1:
        
        #Write the text file
        ReplaceLineContent(inTxt, '<-PathOut->', home)


'''
############################################################
This will handle the preference file system read
############################################################
'''
#Changes default path txt files
def ReadIni(n):
    
    #Set the folder Windows specific handling done within
    inTxt  = GetRuntimeTextFile(['Preferences.txt'], Parent = True)
    
    #if we handle the input folder
    if n == 0:

        #Read the text file        
        Text = GrabLineContent(inTxt, '<-PathIn->')
        
    #if we handle the output folder
    if n == 1:
        
        #Read the text file        
        Text = GrabLineContent(inTxt, '<-PathOut->')
    
    if n == 2:
        
        #Read the text file        
        Text = GrabLineContent(inTxt, '<-Version->')
    
    return Text

'''
############################################################
This will find a line in a fiven text file path and return 
the text writen between two of the samemarkers, or no marker
at all since the classic spli method on a line will still 
give back an elemnt.
############################################################
'''    
def GrabLineContent(Path, Identifier):


    #Read the text file
    Read = open(Path,'r')

    #Read lines
    Lines = Read.readlines()
    
    #we close the file
    Read.close
    
    
    #we go thourgh the element
    for Element in Lines:
    
        #we split all the elements
        SplitElement = Element.split(Identifier)
    
        #we have found the line
        if len(SplitElement) > 1:
    
            #we return what we found
            return SplitElement[1]

    return 'VOID'
    
'''
############################################################
This ill rpelace a given line with the content provided
through Input variable at the location where the
Identifier is found. Furthermore it will wrap the input
by the identifier
############################################################
'''    
def ReplaceLineContent(Path, Identifier, Input):


    #Read the text file
    Read = open(Path,'r')

    #Read lines
    Lines = Read.readlines()
    
    #we close the file
    Read.close
    
    
    #we go thourgh the element
    for i in range(0,len(Lines)):
    
        #we split all the elements
        SplitElement = Lines[i].split(Identifier)
    
        #we have found the line
        if len(SplitElement) > 1:
    
            #we return what we found
            Lines[i] = Identifier+Input+Identifier+'\n'

            #stop the loop
            break

    #Write the text file
    Write = open(Path,'wb')

    #Insert the created text line
    Write.writelines(Lines)

    #close the file and write it
    Write.close


'''
############################################################
This will allow the system to jusdge wether a file is a
raw measurement file and if ir can be imported.
############################################################
'''    
def GrabRenishawRaw(PathArray):
    
    #initialise the output
    RealPathArray = []
    
    #loop over the elements in the array
    for i in range(len(PathArray)):
    
        #try to split it
        try:
    
            #try to split
            PathArray[i].split('__Time_')
    
            #if we splited we can add it
            RealPathArray.append(PathArray[i])

        except:
            
            #it failed do nothing nad move on
            pass
                
    return RealPathArray


'''
############################################################
Create a folder in case it is not yet present. 
(includes FolderExists check)
############################################################
'''
def CreateFolder(Path):

    #Make the directory    
    os.makedirs(Path)
    
    LastAct = '\nFile: '+Path+' was written.'
    return LastAct
    

def GetRuntimeTextFile(PathArray, Parent = False):
    
    '''
    ############################################################
    to load text files containing viable runtime info this
    includes files like IO text files etc.
    
    Ata later stage we would like to build a user specific runtime.
    This would allow multiple users to use the runtime.
    ############################################################
    '''
    
    #check if windows
    RunPath = GetRuntimeDir(Parent = Parent)
        
    #Then build rest with arguments as a list of strings add system specific separators
    #We will not chek here if this folder exists as we trust the developer knows what he is doing
    PathString = os.path.join(RunPath,*PathArray)
    
    return PathString


def GetRuntimeDir(Parent = False):
    
    '''
    ############################################################
    This function is here to build system invariant paths able 
    to load text files containing viable runtime info this 
    includes files like IO text files etc.
    
    Ata later stage we would like to build a user specific runtime.
    This would allow multiple users to use the runtime.
    ############################################################
    '''
    
    #check if windows
    if IsWindows():# or IsLinux():
        
        if not Parent:
        
            RunPath = os.path.dirname(os.path.abspath(__file__)).split(os.path.sep)

            del(RunPath[-1])

            RunPath = os.path.join(*RunPath)

            RunPath = RunPath.split(':')

            RunPath = os.path.join(RunPath[0],os.path.sep, os.path.sep, *RunPath[1:])

        else:
            
            RunPath = os.path.dirname(os.path.abspath(__file__)).split(os.path.sep)

            del(RunPath[-1])

            RunPath = os.path.join(*RunPath)

            RunPath = RunPath.split(':')

            RunPath = os.path.join(RunPath[0],os.path.sep, os.path.sep, *RunPath[1:])


    elif IsLinux():

        if not Parent:
        
            RunPath = os.path.dirname(os.path.abspath(__file__)).split(os.path.sep)
            
            del(RunPath[-1])

            RunPath = os.path.join(os.path.sep,*RunPath)

        else:
            
            RunPath = os.path.dirname(os.path.abspath(__file__)).split(os.path.sep)
            
            del(RunPath[-1])

            RunPath = os.path.join(os.path.sep,*RunPath)

    else:
        
        if not Parent:
        
            RunPath = os.path.dirname(os.path.abspath(__file__)).split(os.path.sep)
            
            del(RunPath[-1])
            
            RunPath = os.path.join(os.path.sep,*RunPath)

        else:
            
            RunPath = os.path.dirname(os.path.abspath(__file__)).split(os.path.sep)
            
            del(RunPath[-1])
            
            RunPath = os.path.join(os.path.sep,*RunPath)

    return RunPath

'''
############################################################
This function is here to build a proper path invariant on 
all platforms. Note that the system will basically fix the 
error on windows machines associated to the volume 
':\\' spacer.
############################################################
'''
def BuildPath(PathArray):
    
    #check if windows
    if IsWindows():
        
        Path = PathArray[0]
        for i in range(1,len(PathArray)):
        
            Path += '\\'+PathArray[i]
        
    else:
        
        Path   = os.path.join(*PathArray)
        #Path   = os.path.sep+Path+os.path.sep+PathArray[-1]

    return Path


'''
############################################################
This will return th einfamouse array of the path
############################################################
'''

def GetPathArray(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts


'''
############################################################
This function returns in an array all files of a foler 
having the conditions met of before and after text.
This is mainly used to find text files in a folder for 
processing.
############################################################
'''
def GetFileNames(Before, After):

    print 'This is the get method:'
    print Before, After
    #if the format is windows  separator is missing
    if IsWindows():
    
        Before = Before+os.path.sep
    
    Paths = glob.glob(os.path.join(Before,'*'+After))

    #Correct the path management on Linux
    if IsLinux():

        for Element in Paths:

            Element.replace('\\', os.path.sep)

    return Paths


def makeArchive(fileList, archive, root):
    """
    ###########################################################
    'fileList' is a list of file names - full path each name
    'archive' is the file name for the archive with a full path
    ############################################################
    """
    a = zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, allowZip64=True)

    #write it
    for f in fileList:
        
        #VisOut.TextBox(Title = 'Action',Text = str("archiving file %s" % (f)),state = 1,close = False)
        a.write(f, os.path.relpath(f, root))
    
    a.close()
    
    #remove the source
    for f in fileList:
        
        #VisOut.TextBox(Title = 'Action',Text = str("removing file %s" % (f)),state = 1,close = False)
        os.remove(f)



def RightClickStr():
    """
    ###########################################################
    Returns the string of the right click depending on the 
    righ operating system...
    
    mac <Button-2> windows <Button-3>
    ############################################################
    """

    if IsWindows():
        return "<3>"

    else:

        return "<2>"




