# -*- coding: utf-8 -*-

print 'Loading VisOut dependencies...'

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

This file is for outputs visual instances into the terminal
No need to print it

This file contains the following routines
- Navigation
- TextBox(Title = '',Text='',L=60,state=0,close=True,Box = True)
    textbox utility will puteverything out nicely
- Ret(n)
    this instance prints out back to the lines as string
- Indent(n)
    this will create a small indent t the start of each line to make the shell view nicer
- Wiper()
    this will clear the console
- PrintHeader(Header,Text)
    This will be initialised at the start of the program
- MyLogo()
    Custome Logo (change on occasion)
    
"""


import glob
import os
import Utility_Main as Utility

#NAVIGATION ROUTINE THROUGH FOLDERS AND SUBFOLDERS
#This returns the selected path on any device.
def Navigation(home,SearchFormat = 'Folder'):
    
    #Variables
    ExitNav  = 0
    Path     = ""
    Select   = False
    
    
    
    #Set menue
    Menu     = ''
    Menu     = Menu+' - "M" to change mode between folders and files\n' 
    Menu     = Menu+' - "V" to change volume\n' 
    Menu     = Menu+' - ".." to go back one folder\n'
    Menu     = Menu+' - "S" to select this folder\n'
    Menu     = Menu+' - "SI/SO" to select this folder as Default Input/Output\n'
    Menu     = Menu+' - "JI/JO" to jump to the Default Input/Output\n'
    Menu     = Menu+' - "S" to select this folder\n'
    Menu     = Menu+' - "n" number to open folder\n'
    Menu     = Menu+' - "E" to exit.'
    
    
    while ExitNav == 0:
        
        #Send out the visuals
        Wiper()        
        TextBox(Title='',Text = MyLogo(),state = 4,close=False)
        TextBox(Title='The current Folder is',Text = home,state = 1,close = False)
        
        #Get an array of path files               
        DataPath   = glob.glob(os.path.join(home,'*'))
        PathList   = []
        IndexList  = []
        i          = 0
        
        if SearchFormat == 'Folder':
            
            for Idx,Val in enumerate(DataPath):
                
                if os.path.isdir(Val):
                    
                    #how many folders are in the file three
                    DataPath_Split = Val.split(os.path.sep)
                    
                    #get integer of that information
                    PathIdx = len(DataPath_Split)
    
                    #save name and index of last folder
                    PathList.append(DataPath_Split[PathIdx-1])
                    IndexList.append(Idx)
                    
                    #move on
                    i = i+1 
            
            #Set header
            Header = 'This folder contains '+str(i)+' subfolders'
            
        if SearchFormat == 'File':
            
            for Idx,Val in enumerate(DataPath):
                
                if not os.path.isdir(Val):
                    
                    #how many folders are in the file three
                    DataPath_Split = Val.split(os.path.sep)
                    
                    #get integer of that information
                    PathIdx = len(DataPath_Split)
    
                    #save name and index of last folder
                    PathList.append(DataPath_Split[PathIdx-1])
                    IndexList.append(Idx)
                    
                    #move on
                    i = i+1
            
            #Set header
            Header = 'This folder contains '+str(i)+' files'
            

        VisPath = ""
            
        for idx,Val in enumerate(PathList):
            
            #Set the initial value
            VisPath += str(idx)+': '+Val+Ret()
            
        
        #Prin menue frame
        if not VisPath ==  "":
            TextBox(Title=Header,Text = VisPath,state = 1,close = False)
        else:
            TextBox(Title=Header,Text = 'Nothing present here',state = 1,close = False)
            
        TextBox(Title='Options',Text = Menu,state = 1,close = True)

        #Ask for user input
        Input = raw_input()
        
        #The user wants to change volume
        if Input == "M":
            
            if SearchFormat == 'Folder':
                SearchFormat = 'File'
            elif SearchFormat == 'File':
                SearchFormat = 'Folder'
                
        if Input == "V":
            
            #print query
            print 'Please enter volume name:'
            
            #Ask for user input
            Ask = raw_input()
            
            #Set is as path
            home = Ask+":"+os.path.sep
            
        #The user wants to set the current folder as starting point
        if Input == "S":
            
            #Set the return variable
            Path = home
            
            #set boolean if a change is recquired
            Select = True
            
            #get output
            LastAct = 'File Path changed'
            
            #set exit variable
            ExitNav = 1

        #The user wants to leave
        if Input == "E":
            LastAct = 'File Path change aborted'
            ExitNav = 1
            
        #the user wants to set current folder as default input
        if Input == "SI":
            
            #Launch the routine that will edit the text file
            Utility.SetIni(home,0)
            
            #get output
            LastAct = 'Default Input Path modified'
            
            #set exit variable
            ExitNav = 1
           
        #the user wants to set current folder as default output
        if Input == "SO":
            
            #Launch the routine that will edit the text file
            Utility.SetIni(home,1)
            
            #get output
            LastAct = 'Default Output Path modified'
            
            #set exit variable
            ExitNav = 1
            
        if Input == "JI":
            
            #Launch the routine that will load the text file
            home = Utility.ReadIni(0)
            
            #get output
            LastAct = 'Jumped to default Input modified'
            
            
        if Input == "JO":
            
            #Launch the routine that will load the text file
            home = Utility.ReadIni(1)
            
            #get output
            LastAct = 'Jumped to default Input modified'
            
            
        if Input == "..":
            HomeSplit = home.split(os.path.sep)
            if len(HomeSplit)==1:
                print 'At root'
            else:
                home = HomeSplit[0]
                for g in range(1,len(HomeSplit)-1):
                    home = home+os.path.sep+HomeSplit[g]
        for g in range(0,i):
            if Input == str(g):
                home = DataPath[IndexList[g]]                    

    return Path,SearchFormat,Select,LastAct

def TextBox(Title = '',Text='',L=60,state=0,close=True,Box = True, Top = True, Select = 0, Target = None):
    
    '''
    ###########################################################################
    In this instance we will redirect the workflow to what is ultimatively in 
    charge depending on the variable 'state'. Note that all options are
    'optional input'. All data will be built into an obejct for easier passing
    
    #State 0 defines textbox with comon text -> PlainText(obj)
    #State 1 is for information display
    #State 2 is for menues
    #State 4 is Logo :)
    #State 5 is for menu listing
    #State 6 for droping the border top alone
    
    The variable Object has the following strucutre
    
    0: L
    1: Box
    2: Close
    3: Title
    4: Text
    5: Top/bottom
    6: Left
    7: Right
    8: Indent

    
    ###########################################################################
    '''
    
    #create an empty list that will be filled with instances
    Object = [None]*12
    
    '''
    ########################
    Check and set parameters
    ########################
    '''
    #Set minimum width
    Object[0] = 60
    
    #set Box boolean
    Object[1] = Box
    
    #set close boolean
    Object[2] = close
        
    #check text and title
    if Title == '':
        Object[3] = None
    else:
        Object[3] = Title
              
    #check for text
    if Text == '':
        Object[4] = ''
    else:
        Object[4] = Text
        
    '''
    #################
    Create others
    #################
    '''
    #set the indentation variable
    Object[8] = 5
    

    
    #Change first and last character to "o"
    if Top:
        Line            = "-"*(Object[0]+2-Object[8])
        Object[5]       = Indent(Object[8])+"o"+Line+"o"
    else:
        Line            = "-"*(Object[0]+2-Object[8])
        Object[5]       = Indent(Object[8])+"o"+Line+"o" 
    
    
    #Define border characters
    if Box:
        Object[6] = "|"
        Object[7] = "|"
    else:
        Object[6] = " "
        Object[7] = " "   
        
    Object[9] = Select

    if not Target == None:
        Object[10] = True
    else:
        Object[10] = False

    #we have plain text
    if state == 0:
        OutText = PlainText(Object)
        
    #we have a menue
    if state == 1:
        
        OutText = Menues_1(Object)

    #we have plain text
    if state == 2:

        OutText = Menues_2(Object)

    #we popup text
    if state == 3:
        
        #print out info
        OutText = Menues_1(Object)
        
        #wait to not clear
        #aw_input()

    #we have plain text
    if state == 4:

        OutText = Logo(Object)

    #we have another menue
    if state == 5:
        pass            

#    #we have request in spacer
#    if state == 6:
#        RequestIn()      
#
#    #we have separator
#    if state == 7:
#        RequestOut()      `

    if not Target == None:

        Target.insert('insert', OutText)
        Target.see('end')
    else:
        print OutText

def Ret(n = 1):
    '''
    ###########################################################################
    This little routine will go back to the line n times. 
    if called witout argument it acts like '\n'
    ###########################################################################
    '''
    
    #initialise Out
    Out = ''
    
    #start looping
    for i in range(0,n):
        Out += '\n'
        
    #send result
    return Out
        
def Indent(L = 0):

    '''
    ###########################################################################
    This little function is puting an indent to the start of lines
    if served witout argument it will return '' to avoid any undefined errors
    ###########################################################################
    '''
    
    #set indentation
    Indent = " "*L
    
    #return output
    return Indent    

    

def Wiper():
    '''
    ###########################################################################
    This function returns 1000 x '\n'
    This will clear the visual of the console
    ###########################################################################
    '''
    print '\n'*1000

#FUNCTION TO PRINT THE HEADER OF OUR PROGRAM
def PrintHeader(Text = '',L = 60):
    '''
    ###########################################################################
    This function returns the header of the visual output
    
    Note that it constructs at the same time the text as the logo
    ###########################################################################
    '''
    #Wiper()
    
    if not Text == '':
        
        TextBox(Title='',Text = Text,L = L,state = 0,close = False)
        
    TextBox(Title='',Text = MyLogo(),L = L,state = 4,close=False)
    
    TextBox(Title='',Text = MyLicense(),L = L,state = 0,close=False)



def MyLogo():

    '''
    ###########################################################################
    This function returns the header of the visual output
    
    Note that it constructs at the same time the text as the logo
    ###########################################################################
    '''
    
    LogoTxt = [""]*20

    LogoTxt[0]  ='##       ###              ..O,.  . .=OZ          '
    LogoTxt[1]  ='##       ###            ?=?...   ?   ..Z~        '
    LogoTxt[2]  ='##       ###         .?.O.       . .,. .Z.  .    '
    LogoTxt[3]  ='##       ###        . .?. . ?Z    ...O7.ZZ. =    '
    LogoTxt[4]  ='##       ###       . ,?:.:        . .  . Z. .?   '
    LogoTxt[5]  ='##       ###       ..?Z         .ZZZZZ+ :Z:ZZZ.  '
    LogoTxt[6]  ='##       ###      ~ .??     .ZZZ. .... ..Z+  ZI? '
    LogoTxt[7]  ='##       ###      ?$.?? ..OO????+,. .~???8?: .ZZ '
    LogoTxt[8]  ='######   ###      :..??OO+..           .ZZ?.?7 Z '
    LogoTxt[9]  ='######   ###     Z? 8O                 ZZ. ??O=  '
    LogoTxt[10] ='                 .Z?8??                ZZ..7O. ?I'
    LogoTxt[11] ='###### #######   .ZO.?7:              =Z7?ZO.  ?Z'
    LogoTxt[12] ='##  ##   ###     .O.. 77??~. .     ..$OOO?.?. .Z.'
    LogoTxt[13] ='##       ###      Z7  .?????????????OOO... ?.?,Z '
    LogoTxt[14] ='##       ###       ZO. ??   ..~?OZ.ZZ7  . .7.,Z. '
    LogoTxt[15] ='######   ###       .Z7.?OOI:..  .$ZZ...+? .:ZZ.  '
    LogoTxt[16] ='    ##   ###       . ZZ$.??..~?OOZ.....   OZZ    '
    LogoTxt[17] ='##  ##   ###           ZZZOOOZZ.    . .ZZZZ      '
    LogoTxt[18] ='##  ##   ###            .ZZZOOZZZZZZZZZZZ..      '
    LogoTxt[19] ='######   ###                .?OOOZZZ+ :?         '
    
    return LogoTxt

def MyLicense():

    '''
    ###########################################################################
    This function returns the header of the visual output
    
    Note that it constructs at the same time the text as the logo
    ###########################################################################
    '''

    LogoTxt ='- This code has been written by Alexander Schober at the luxembourg Institute of Science and Technology. All usage should be done under prior approval of the author and chnages should reference the original implementations.'
    LogoTxt +=' - Author: Alexander Michael Schober.'
    LogoTxt +=' - email: alex.schober@mac.com.'
    LogoTxt +=' - Institution Luxembourg Institute for Science and Technology LIST.'
    LogoTxt +=' - Address: 41 Rue du Brill, 4422 Sanem, Luxembourg.'
    
    return LogoTxt
    
def Logo(Object):
    '''    
    This is the most complicated instance as it will try to truncate text
    
    The variable Object has the following strucutre
    
    0: L
    1: Box
    2: Close
    3: Title
    4: Text
    5: Top/bottom
    6: Left
    7: Right
    8: Indent
    '''      
    #Load the top delimiter
    Output = Object[5]
    
    for Idx,Val in enumerate(Object[4]):
        
        #Calculate Gap to center logo 
        Gap = (Object[0]-len(Object[6])-len(Object[7])-len(Val))/2
        
        if int(Gap) == Gap:
            Output += Ret()+Indent(Object[8])+Object[6]+" "*int(Gap)+Val+" "*int(Gap)+Object[7]
        else:
            Output += Ret()+Indent(Object[8])+Object[6]+" "*int(Gap)+Val+" "*(int(Gap)+1)+Object[7]

    #Are we closing the box
    if Object[2]:
        #Close the string
        if Object[1]:
            Output += Ret()+Indent(Object[8])+Object[5]
        else:
            Output += Ret()   
            
    return Output
                
def Menues_1(Object):
    '''    
    Goes and checks lines if lines to long truncates the value and put '...'
    
    The variable Object has the following strucutre
    
    0: L
    1: Box
    2: Close
    3: Title
    4: Text
    5: Top/bottom
    6: Left
    7: Right
    8: Indent
    9: Turn on Nice or not
    '''
    #remove the unnecessary stuf
    if Object[10]:
        Object[8] = 0
        Object[6] = ''
        Object[7] = ''
        Spacing   = ''
    else:
        Spacing = ' '

    #initialise the writing field size
    WriteLength = Object[0]-len(Object[6])-len(Object[7])-1
    
    #Load the top delimiter
    Output = Object[5]
    
    #Load the text and split it
    TextSplit = Object[4].split(" ")

    
    if not Object[3] == None:
        Output += Ret()+Indent(Object[8])+Object[6]+Object[3]+':'+Spacing*(WriteLength-1-len(Object[3]))+Object[7]
        
    #Add a buffer line
    Output    += Ret()+Indent(Object[8])+Object[6]+Spacing*WriteLength+Object[7]
    
    #Build Information lines
    TextSplit = Object[4].split('\n')

    #go through all lines
    for i in range(0,len(TextSplit)):
        
        #is it smaller than the space available
        if len(TextSplit[i])>WriteLength-Object[8]:
            Pass  = TextSplit[i]
            Line  = Pass[0:10]+'...'+Pass[len(Pass)-(Object[0]-10-3-15):len(Pass)]
            Gap   = Spacing*(WriteLength-len(Line)-len(Indent(Object[8])))
        else:
            Line  = TextSplit[i]
            Gap   = Spacing*(WriteLength-len(Line)-len(Indent(Object[8])))
            
        Output += Ret()+Indent(Object[8])+Object[6]+Indent(Object[8])+Line+Gap+Object[7]

    #Are we closing the box
    if Object[2]:
        #Close the string
        if Object[1]:
            Output += Ret()+Object[5]
        else:
            Output += Output+Ret()
            
    #dump the visual
    return Output


def Menues_2(Object):
    '''    
    Goes and checks lines if lines to long truncates the value and put '...'
    
    The variable Object has the following strucutre
    
    0: L
    1: Box
    2: Close
    3: Title
    4: Text
    5: Top/bottom
    6: Left
    7: Right
    8: Indent
    '''    
    
    #initialise the writing field size
    WriteLength = Object[0]-len(Object[6])-len(Object[7])-1
    
    #Load the top delimiter
    Output = Object[5]
    
    #Load the text and split it
    TextSplit = Object[4].split(" ")
    
    if not Object[3] == None:
        Output += Ret()+Indent(Object[8])+Object[6]+Object[3]+':'+' '*(WriteLength-1-len(Object[3]))+Object[7]
        
    #Add a buffer line
    Output    += Ret()+Indent(Object[8])+Object[6]
    
    #Build Information lines
    TextSplit = Object[4].split(' ')
    
    #initialise line
    Line = ''

    #go through all lines
    for i in range(0,len(TextSplit)):
        
        #is it smaller than the space available
        if i == Object[9]:
            Line += " "*5+str(i+1)+': '+'█'+TextSplit[i]+'█'
        else:
            Line += " "*5+str(i+1)+': '+TextSplit[i]
            
    Output    += Line +" "*(WriteLength - len(Line)+4)+Object[7]
    #Are we closing the box
    if Object[2]:
        #Close the string
        if Object[1]:
            Output += Ret()+Object[5]
        else:
            Output += Output+Ret()
            
    #dump the visual
    return Output
    
def PlainText(Object):
    '''    
    This is the most complicated instance as it will try to truncate text
    
    The variable Object has the following strucutre
    
    0: L
    1: Box
    2: Close
    3: Title
    4: Text
    5: Top/bottom
    6: Left
    7: Right
    8: Indent
    '''
    #initialise the writing field size
    WriteLength = Object[0]-len(Object[6])-len(Object[7])-1
    
    #Load the top delimiter
    Output = Object[5]
    
    #Set title in case
    if not Object[3] == None:
        Output += Ret()+Indent(Object[8])+Object[6]+Object[3]+':'+' '*(WriteLength-1-len(Object[3]))+Object[7]
    
    #Search for '-' as a paragraph delimiter
    TextHighLevel = Object[4].split(" - ")
    
    for j in range(0,len(TextHighLevel)):
        #Load the text and split it
        TextSplit = TextHighLevel[j].split(" ")
            
        #initiate words
        #Output    += Ret()+Indent(Object[8])+Object[6]
        if j > 0:
            LastWord  = " -"+TextSplit[0]
            Output   += Ret()+Indent(Object[8])+Object[6]+" "*(WriteLength)+Object[7]   
        else:
            LastWord  = TextSplit[0]
            
        NextWord  = TextSplit[0]
        
        #In english we will not cut words smaller than 'and' (3 characters)
        for i in range(1,len(TextSplit)):
            
            
            NextWord = LastWord+' '+TextSplit[i]
            
            #we have three essential param
            LengthLast = len(LastWord)
            LengthNext = len(NextWord)
            LengthIn   = len(TextSplit[i])
            
            #Check if cheking is necessary
            if LengthNext <= WriteLength:
                
                #Don't do anything just move forth
                LastWord = NextWord
                
            else:
                #We have 4 cases displayed
                # - First the Lastword is exactly the legth of the line
                # - Second the lastword is exactly length of the lien minus one space
                # - The added word is smaller or equal to 4 letters
                # - We truncate the last word
            
                #if Delta == 0 we fit perfectly
                if LengthLast == WriteLength:
                    
                    #perfect just format line and send out
                    Output   += Ret()+Indent(Object[8])+Object[6]+LastWord+Object[7]
                    
                    #restart the buffer line
                    LastWord = TextSplit[i]
                    
                #if Delta == 1 we have a space at the end basically
                elif LengthLast == WriteLength-1:
                    
                    #perfect add bland and format and out
                    Output   += Ret()+Indent(Object[8])+Object[6]+LastWord+' '+Object[7]
                    
                    #restart the buffer line
                    LastWord = TextSplit[i]
                    
                
                #Delta < 0 and len(TextSplit[i])<= 3 we have a small word at the end
                else:
                    
                    #check the word length
                    if LengthIn <5:
                    
                        #print line as is
                        Output   += Ret()+Indent(Object[8])+Object[6]+LastWord+" "*(WriteLength - LengthLast)+Object[7]
    
                        #send word to the buffer for next line instead                
                        LastWord = TextSplit[i]
                        
                    else:  
                        if LengthIn-(WriteLength - LengthLast)-1 > 2:
                            #The word is apparently longer than 3 characters so plit it wit '-'                    
                            Output   += Ret()+Indent(Object[8])+Object[6]+LastWord+" "+TextSplit[i][0:LengthIn-(WriteLength - LengthLast)-1]+"-"+Object[7]
    
                            #Send out the word to the buffer
                            LastWord = TextSplit[i][LengthIn-(WriteLength-LengthLast)-1:LengthIn] 
                            
                        else:
                            
                            #print line as is
                            Output   += Ret()+Indent(Object[8])+Object[6]+LastWord+" "*(WriteLength - LengthLast)+Object[7]
        
                            #send word to the buffer for next line instead                
                            LastWord = TextSplit[i]                        

        #reload variables
        LengthLast = len(LastWord)
        LengthNext = len(NextWord) 
               
        #Dump the last line into the information and add gap    
        Output += Ret()+Indent(Object[8])+Object[6]+LastWord+" "*(WriteLength-LengthLast)+Object[7] 
    
    #Are we closing the box
    if Object[2]:
        #Close the string
        if Object[1]:
            Output = Output+Ret()+Object[5]
        else:
            Output = Output+Ret()
            
    #dump the line 
    return Output
    
    #exit
    
    
    
    
    
def RawInput(ID, Data = None):
    '''
    ###########################################################################
    We create a more custome raw inoput method to account for eventual help 
    Note that this is just to allow for custome helps for now
    It could be that more general parameters are intorduced
    
    Depreciated
    ###########################################################################
    '''
    return 0
