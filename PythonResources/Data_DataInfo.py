# -*- coding: utf-8 -*-
#-INFO-
#-Name-DataInfo-
#-Version-0.1.0-
#-Date-01_February_2016-
#-Author-Alexander_Schober-
#-email-alex.schober@mac.com-
#-INFO-

print 'Loading DataInfo dependencies...'

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

#The terminal viual manager
import Utility_Out      as VisOut

class Info:
    
    def __init__(self):
        
        #Initialise variables
        self.SampleInfoID   = []
        self.SampleInfoVal  = []
        self.SampleInfoUnit = []
        
    def CallInfo(self,Tk = False):
        
        #initialise the output variable:
        Text = ''
        
        #we will go through and make a string
        for i in range(0,len(self.SampleInfoID)):

            #two forst parts
            Text += self.SampleInfoID[i]+': '+self.SampleInfoVal[i]
            
            #if the last part is not none
            if not self.SampleInfoUnit[i] == None:
                Text += ' '+self.SampleInfoUnit[i]+VisOut.Ret()
            else:
                Text += VisOut.Ret()
                
        #Send to VisOut as list:
        if not Tk:
            #termiunal output method
            VisOut.TextBox(Title = 'Sample Information', Text = Text, state = 3)
        else:
            #tkinter passing method
            return Text


    def GetInfo(self, Name = ''):

        for i in range(0,len(self.SampleInfoID)):

            if Name == self.SampleInfoID[i]:
                
                return  [self.SampleInfoID[i],self.SampleInfoVal[i],self.SampleInfoUnit[i]]

    def GetInfoVal(self, Name = ''):

        for i in range(0,len(self.SampleInfoID)):

            if Name == self.SampleInfoID[i]:
                
                
                return  self.SampleInfoVal[i]
