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



class Custome_Button(tk.Button):

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
