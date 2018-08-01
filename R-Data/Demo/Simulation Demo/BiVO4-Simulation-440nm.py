#--Simulation File--
# -*- coding: utf-8 -*-
"""
###########################################################################
This code aims to simulate the Ramaman emition of a depth profile.
Note that it is inspired from a paper found by mael entitled: 
confocal volume in laser Raman microscopy depth profiling.


we will create multiple classes handling the input outputs
The data is saved in dicitonaries with a intuitive naming.


###########################################################################
"""

#essential python updates for math
import math
import numpy
import scipy.integrate as integrate
import os
import sys
import multiprocessing

class LensManager:
    
    """
    ###########################################################################
    This Class will store all the parameters of the Lens System. This includes
    the depth of the focal first lens. and finnally the angular acceptance of 
    it. The angular acceptance will be prossed as such as it does not change
    for a given focal distance. 
    
    The folowwing funcitons will be present:
    - __init__() to initialise the class.

    - __str__() to print the details of the class
    
    - self.ChangeParameter(): This will allow the user to update a dictionary
        element of the parameters. ParametersDict are:
        -> Parameter: the parameter name to change
        -> Value: The associated value to change
    
    - self.ProcessAngular(): This will process the Angular acceptance of the 
        first lens in place. Note that this is not related to the intensity
        created by the Raman which will be processed in another class that 
        will indeed use elements of this class to calculate the final
        representation. It does not recquire any input as the values are
        fetched from the internal self. storage. Note that the algular limit
        is obvioulsy distance realted. This is why it should be input with 
        depth :)
        
    - self.RamanIn(): This class will process the Raman signal distribution
        It will be linked to the focal point position and the wavelength as
        well ad the numerical apperture
        
    ###########################################################################
    """

    def __init__(self, ParametersDict = None ):
        '''
        ##################################################
        Inititalisation fo the lens class. the following 
        Parameters will be aded to the dictionary:
        
        - Type
        - Lambda emission wavelength
        - FocalLenght
        - Distance
        - Lens Diameter
        - Focal Position
        - Detection Lambda
        - Waist of the laser
        - Intensity at peak
        - M square factor
        ##################################################
        '''
    
        #if the user passes on the ParametersDict externally just make them local
        if not ParametersDict == None:
    
            self.ParametersDict = ParametersDict

        #otherwise define the ParametersDict on it's own.
        #this allows stand alone usage
        else:
    
            self.ParametersDict = {}

            self.ParametersDict['Type']              = 'Raman Lens System'
            self.ParametersDict['LambdaIn']          = 633.e-9
            self.ParametersDict['FocalLength']       = 0.00025      #<- our instrument;from paper 1.3e-3
            self.ParametersDict['SlitLensFocalLength']  = 70.0e-3   #<- our instrument;from paper 252.e-3
            self.ParametersDict['SlitLensRadius']    = 8.5e-3       #<- our instrument;from paper 30.e-3
            self.ParametersDict['LensRadius']        = 0.75e-3      #<- our instrument;from paper 3.e-3
            self.ParametersDict['Distance']          = 0.58         #<- our instrument;from paper 1.0
            self.ParametersDict['LensDiameter']      = 100.e-3
            self.ParametersDict['FocalPosition']     = 0.
            self.ParametersDict['LambdaOut']         = 700.e-9
            self.ParametersDict['Waist']             = 0.35e-6
            self.ParametersDict['Intensity']         = 1.0
            self.ParametersDict['MSquare']           = 1.013
            self.ParametersDict['Environnement']     = False
            self.ParametersDict['PinHoleOn']         = True
            self.ParametersDict['PinHoleType']       = 'Circular'
            self.ParametersDict['PinHoleParameter']  = [60.e-6,0.]

        #Initaite the lenses
        self.ResetLenses()
            
        #create the preference list
        self.CreatePreferenceList()

    def CreatePreferenceList(self):
        '''
        ##################################################
        This routin has the purpose to create an identifi
        cation list of properties.
        
        It will give the following informaitons:
        
        - Label name
        - Dictionary name
        - Dictionary pointer
        - Type (ex.: 'float', 'int', 'bool', 'float_array')
        
        ##################################################
        '''
    
        #initialise the list
        self.PreferenceList = []


        self.PreferenceList.append(['Focal position',
                                   'FocalPosition',
                                   self.ParametersDict,
                                   'float'])
                                   
        self.PreferenceList.append(['Incomming Wavelength',
                                   'LambdaIn',
                                   self.ParametersDict,
                                   'float'])
                                   
        self.PreferenceList.append(['Outgoing Wavelength',
                                   'LambdaOut',
                                   self.ParametersDict,
                                   'float'])
    
        self.PreferenceList.append(['Laser waist',
                                   'Waist',
                                   self.ParametersDict,
                                   'float'])
    
        self.PreferenceList.append(['Intensity',
                                   'Intensity',
                                   self.ParametersDict,
                                   'float'])
    
    def __str__(self):
        
        '''
        ##################################################
        INtrinsic print funciton of the class
        This method is aimed at debuging
        ##################################################
        '''
        Output  = '#############################################'
        Output += '\n###############  LENS Para. #################'
        Output += '\n#############################################'
        
        Output += '\n    - Type is: '+str(self.ParametersDict['Type'])
        
        Output += '\n - These are the illumination parameters: '
        Output += '\n    - Main lens focal distance: '+str(self.ParametersDict['FocalLength'])+'m'
        Output += '\n    - Focal Position: '+str(self.ParametersDict['FocalPosition'])+'m'
        Output += '\n    - LensDiameter: '+str(self.ParametersDict['LensDiameter'])+'m'
        Output += '\n    - Raman wavelength: '+str(self.ParametersDict['LambdaIn'])+'m'
        Output += '\n    - Laser Waist0: '+str(self.ParametersDict['Waist'])+'m'
        Output += '\n    - Instensity: '+str(self.ParametersDict['Intensity'])
        Output += '\n    - M square: '+str(self.ParametersDict['MSquare'])
        Output += '\n    - Linked to Env.: '+str(self.ParametersDict['Environnement'])
        
        Output += '\n#############################################'
        Output += '\n############### ACQUISITION #################'
        Output += '\n#############################################'
        
        Output += '\n - These are the acquisition parameters: '
        Output += '\n    - Main lens focal distance: '+str(self.ParametersDict['FocalLength'])+'m'
        Output += '\n    - Slit lens focal distance: '+str(self.ParametersDict['SlitLensFocalLength'])+'m'
        Output += '\n    - Lens tube length: '+str(self.ParametersDict['Distance'])+'m'
        Output += '\n    - Detection Wavelength: '+str(self.ParametersDict['LambdaOut'])+'m'
        
        Output += '\n#############################################'
        Output += '\n###############   PINHOLE  ##################'
        Output += '\n#############################################'
        
        Output += '\n - These are the Pinhole parameters: '
        Output += '\n    - Is the pinhole activated: '+str(self.ParametersDict['PinHoleOn'])
        Output += '\n    - Type of the Pinhole: '+str(self.ParametersDict['PinHoleType'])
        Output += '\n    - Pinhole dimension 1: '+str(self.ParametersDict['PinHoleParameter'][0])+'m'
        Output += '\n    - Pinhole dimension 2: '+str(self.ParametersDict['PinHoleParameter'][1])+'m'
        
        Output += '\n#############################################'
        Output += '\n###############   LENSES   ##################'
        Output += '\n#############################################'
        
        #print the lenses
        for i in range( len( self.LensElements ) ):
        
            Output += self.LensElements[i].__str__()
        
        return Output
            
    def CreateLensSystem(self):
        '''
        ##################################################
        This system will create the lenses with the 
        appropriate lens parameters
        
        Th whole setups is writen such as that the first
        lens is the actual 0 point. This means that
        no corrections need to be done in the first
        ##################################################
        '''
        
        ####################
        #Process the first lens
        
        ParametersDict_0 = {}
        
        ParametersDict_0['Name']          = 'Objective Lens'
        ParametersDict_0['Type']          = 'Lens'
        ParametersDict_0['LambdaIn']      = self.ParametersDict['LambdaOut']
        ParametersDict_0['FocalLength']   = self.ParametersDict['FocalLength']
        ParametersDict_0['LensRadius']    = self.ParametersDict['LensRadius']
        ParametersDict_0['Position']      = 0.0

        self.CreateLens(ParametersDict_0)
        
        ####################
        #Process the Second lens
        
        ParametersDict_1 = {}
        
        ParametersDict_1['Name']          = 'Pinhole Lens'
        ParametersDict_1['Type']          = 'Lens'
        ParametersDict_1['LambdaIn']      = self.ParametersDict['LambdaOut']
        ParametersDict_1['FocalLength']   = self.ParametersDict['SlitLensFocalLength']
        ParametersDict_1['LensRadius']    = self.ParametersDict['SlitLensRadius']
        ParametersDict_1['Position']      = self.ParametersDict['Distance']

        self.CreateLens(ParametersDict_1)
    
        ####################
        #Process the Second lens
        
        ParametersDict_2 = {}
        
        ParametersDict_2['Name']          = 'Circular Pinhole'
        ParametersDict_2['Type']          = 'CPinhole'
        ParametersDict_2['Parameters']    = 100.#e-6
        ParametersDict_2['Position']      = self.ParametersDict['SlitLensFocalLength'] + self.ParametersDict['Distance']
        
        self.CreatePinhole(ParametersDict_2)

    def CreateLens(self, ParametersDict):
        '''
        ##################################################
        This system will create the lenses with the 
        appropriate lens parameters
        ##################################################
        '''

        #append a lens
        self.LensElements.append( Lens(self ,
                                       self.LensID ,
                                       ParametersDict ) )

        #set the index
        self.LensID += 1
    
    def CreatePinhole(self, ParametersDict):
        '''
        ##################################################
        This system will create the lenses with the 
        appropriate lens parameters
        ##################################################
        '''

        #append a lens
        self.LensElements.append( Pinhole(self ,
                                          self.LensID ,
                                          ParametersDict ) )

        #set the index
        self.LensID += 1

    def ResetLenses(self):
        '''
        ##################################################
        This little routine will simply delete all lenses
        present in the link effectively letting them 
        get garbage collected
        ##################################################
        '''
        
        #Reset the lens ID
        self.LensID = 0
        
        #try to delete it all
        try:
            
            del self.LensElements
        
        except:

            pass

        #create the lens link
        self.LensElements = []
        
        #Initaite the lenses
        self.CreateLensSystem()

    def ComputeObjects(self, Object):
        '''
        ##################################################
        This will process the image positions of the 
        elements of the lens. Note that this is going to
        process the entire system lenses in it's order
        ##################################################
        '''

        #Correct the cube positoning...
        Object.CorrectAbsPosition()

        '''
        ##################################################
        Here we have two options, either we check for the 
        value in the point or we do an integration between
        0 and 1 corresponding to the ratio along the z
        axis of the objet.
        ##################################################
        '''
        
        if Object.Parent.ParametersDict['Integration']:
            
            #send out the normal
            self.ComputeNormalObject(Object, True, True)
        
        else:
        
            #send out the normal
            self.ComputeNormalObject(Object, True)
    
        
    def ComputeNormalObject(self, Object, State, Ratio = False):
    
        '''
        ##################################################
        This routine will process to the creation of the 
        integration routines or simply process to one
        single calculation on the zone center of the 
        object.
        
        if theintegration is selected by Ratio = True
        the object will be moved solely along the Z axis 
        to perform a Z integraiton.
        ##################################################
        '''
        
        
        
        
        if not Ratio:
        
            OverlapRatio = self.ProcessOverlapPreparation(Object, State)
        
        else:
        
            OverlapRatio = integrate.quad(lambda Ratio: self.IntProcessOverlapPreparation(Object, State, Ratio), 0., 1.)[0]
 
 
        '''
        ##################################################
        Send out the overlap ratios to the obejct and 
        reset its position.
        ##################################################
        '''
        
        try:
        
            Object.AddEffectiveIntensityFact([OverlapRatio,OverlapRatio])

        except:
            
            Object.AddEffectiveIntensityFact([0, 0])


    def ProcessOverlapPreparation(self, Object, State):
        '''
        ##################################################
        Send out the overlap ratios to the obejct and 
        reset its position.
        ##################################################
        '''
        
        #first we reset the object set
        Object.ResetImages()
    
        #now that we are corrected grab the initial sets
        InitialObject = Object.GrabObject(State)
        CurrentObject = Object.GrabObject(State)
        
        #process the lenses
        for Lens in self.LensElements:

            if Lens.ParametersDict['Type'] == 'Lens':
            
                CurrentObject = Lens.Process(CurrentObject)
                
                Object.AddImage(CurrentObject)

        '''
        ##################################################
        It was found that some masks have to be computed 
        of the pinhole and of the Lens
        ##################################################
        '''
        
        Masks = []
        
        Masks.append(self.CreateMask([Object.Images[1],
                                      Object.Images[0]],
                                     [self.LensElements[2],
                                      self.LensElements[1],
                                      self.LensElements[0]]))
        
        Masks.append(self.CreateMask([Object.Images[0]],
                                     [self.LensElements[1],
                                      self.LensElements[0]]))
        
        Masks.append(self.CreateMask([],
                                    [self.LensElements[0]]))
        
        OverlapRatio = self.ProcessOverlap(Masks,Object,InitialObject)/(4.*math.pi*Object.AbsPositionCorrected[0]**2)
    
        return OverlapRatio
    
    
    def IntProcessOverlapPreparation(self, Object, State, Ratio):
        '''
        ##################################################
        Send out the overlap ratios to the obejct and 
        reset its position.
        ##################################################
        '''
    
        #first we reset the object set
        Object.ResetImages()
        
        #now that we are corrected grab the initial sets
        InitialObject = Object.GrabObject(State, Ratio)
        CurrentObject = Object.GrabObject(State, Ratio)
        
        #process the lenses
        for Lens in self.LensElements:

            if Lens.ParametersDict['Type'] == 'Lens':
            
                CurrentObject = Lens.Process(CurrentObject)
                
                Object.AddImage(CurrentObject)

        '''
        ##################################################
        It was found that some masks have to be computed 
        of the pinhole and of the Lens
        ##################################################
        '''
        
        Masks = []
        
        Masks.append(self.CreateMask([Object.Images[1],
                                      Object.Images[0]],
                                     [self.LensElements[2],
                                      self.LensElements[1],
                                      self.LensElements[0]]))
        
        Masks.append(self.CreateMask([Object.Images[0]],
                                     [self.LensElements[1],
                                      self.LensElements[0]]))
        
        Masks.append(self.CreateMask([],
                                    [self.LensElements[0]]))
        
        OverlapRatio = self.ProcessOverlap(Masks,Object,InitialObject)/(4.*math.pi*InitialObject[0]**2)
    
        return OverlapRatio
            
    def ProcessOverlap(self, Masks, Object, InitialObject):

        '''
        ##################################################
        This routine computes the overlap
        ##################################################
        '''
    
        #first we copy the masks
        Masks           = list(Masks)
    
        #create an exclusion list
        Exclusion = []
        
        #--------------------------------#
        #second we check for pair size
        for i in range(len(Masks)):
    
            #first the don't meet
            if numpy.abs(Masks[i-1][1]) + numpy.abs(Masks[i][1]) < math.sqrt((Masks[i-1][0][1] - Masks[i][0][1])**2 + (Masks[i-1][0][2] - Masks[i][0][2])**2):
    
                return 0.0
                    
            #oe is included
            elif numpy.abs(Masks[i][1]) > math.sqrt((Masks[i-1][0][1] - Masks[i][0][1])**2 + (Masks[i-1][0][2] - Masks[i][0][2])**2) + numpy.abs(Masks[i-1][1]):
    
                Exclusion.append(i)
            
            elif numpy.abs(Masks[i][1]) < math.sqrt((Masks[i-1][0][1] - Masks[i][0][1])**2 + (Masks[i-1][0][2] - Masks[i][0][2])**2) + numpy.abs(Masks[i-1][1]):
                
                if i-1 < 0:
                    
                    Exclusion.append(len(Masks)-1)
                
                else:
                
                    Exclusion.append(i-1)

            elif Masks[i-1][0][1] == Masks[i][0][1] and Masks[i-1][0][2] == Masks[i][0][2]:
    
                if numpy.abs(Masks[i][1]) > numpy.abs(Masks[i-1][1]):
        
                    Exclusion.append(i)
                        
                else:
     
                    if i-1 < 0:
                        
                        Exclusion.append(len(Masks)-1)
                    
                    else:
                    
                        Exclusion.append(i-1)
    
        
        #try to create the unique
        Exclusion = numpy.unique(Exclusion)
        Exclusion = sorted(Exclusion)
        
        #--------------------------------#
        #we remove some if biger than the rest
        if not len(Exclusion) == 0:
                
            for i in range(len(Exclusion)):

                del Masks[Exclusion[len(Exclusion)-1-i]]
    
        #--------------------------------#
        #if only one mask is left
        if len(Masks) == 1:
        
        
            #Set the parmeters
            D       = numpy.abs(InitialObject[0])
            Rho_0   = math.sqrt((Masks[0][0][1]-Object.Position[1])**2
                                + (Masks[0][0][2]-Object.Position[2])**2)
            Radius  = Masks[0][1]
            
            #calculate
            Surface = self.ProcessProjection(D,
                                             Rho_0,
                                             Radius)
            
            #print 'I am one',D,Rho_0,Radius
            return Surface
        
        if len(Masks) == 0:
        
            return 0.0

        #--------------------------------#
        #else we create a new referentiel
        #find in max
        
        #grab all posiiton
        PosX = Object.AbsPositionCorrected[1]
        PosY = Object.AbsPositionCorrected[2]
        
        #apply offsets
        for i in range(len(Masks)):
            
            #process offset
            Masks[i][0][1] -= PosX
            Masks[i][0][2] -= PosY

            #add the new coordinate
            Masks[i][0].append(math.sqrt((Masks[i][0][1])**2+
                                         (Masks[i][0][2])**2))
        
            if Masks[i][0][1] < 0 :
        
                Masks[i][0][3] *= -1.
        
        
        
        #--------------------------------#
        #order the list just in case
        PosD = [Masks[i][0][3] for i in range(len(Masks)) ]
            
        PosD, Masks = zip(*sorted(zip(PosD, Masks)))
        
        #--------------------------------#
        #We are sorted proceed intersection
        
        #initiate point matrix
        IntersectPoints = [Masks[0][1]]

        #enter the loop
        for i in range(len(PosD)-1):
            
            #compute
            IntersectPoints.append(  ((Masks[i+1][0][3] - Masks[i][0][3])**2 - Masks[i+1][1]**2 + Masks[i][1]**2)
                                   / ( 2. * (Masks[i+1][0][3] - Masks[i][0][3])) )

        #add the last limit
        IntersectPoints.append(Masks[i+1][1])
        
        #--------------------------------#
        #create the integration
        #beta use only two circles...
        #set the initial surface
        Surface = 0.0
    
        for i in range(len(IntersectPoints)-1):
            
            #Set the parmeters
            D       = numpy.abs(InitialObject[0])
            Rho_0   = math.sqrt((Masks[i][0][1]-Object.Position[1])**2
                                + (Masks[i][0][2]-Object.Position[2])**2)
            Radius  = Masks[i][1]
            Rho_lim = [IntersectPoints[i], IntersectPoints[i+1]]
            
            #calculate
            Surface += self.ProcessProjection(D,
                                              Rho_0,
                                              Radius,
                                              Rho_lim = Rho_lim)
    
        return Surface

    def ProcessProjection(self, D, Rho_0 ,Radius, Rho_lim = None):

        """
        ###########################################################################
        This method will process the actual projection. Note that the Arguments
        will be unpacked on start. They should include the following:
        
        D       -> the z distance from the object to the lens surface
        Rho_0   -> the radial distance of the circular element on the lens from D
        R       -> the radius of the circular object
        Rho_lim -> the limits of the integration. if none the max radius
        ###########################################################################
        """
        ##########################
        #check if rho_lim == None
        if Rho_lim == None:

            Rho_lim = [Rho_0 - Radius ,
                       Rho_0 + Radius ]
        
        if Rho_0 < 0:
        
            Buffer = Rho_lim[::-1]

            Rho_lim = [ -Buffer[0], -Buffer[1]]
                       
        if Rho_lim[0] < 0:

            Rho_lim[0] = 0.0

        ##########################
        #process the limits
        Theta_0 = math.asin( Rho_lim[0] / math.sqrt( Rho_lim[0] ** 2 + D ** 2 ))
        Theta_1 = math.asin( Rho_lim[1] / math.sqrt( Rho_lim[1] ** 2 + D ** 2 ))
        
        ##########################
        #integrate
        Result = integrate.quad(lambda Theta : self.Function(Theta,D,Rho_0,Radius,Rho_lim, Theta_0,Theta_1),Theta_0,Theta_1)

        return Result[0]/( 4. * math.pi * D ** 2 )

    def Function(self,Theta,D,Rho_0,Radius,Rho_lim, Theta_0,Theta_1):

        """
        ###########################################################################
        This method will process the actual projectionintegration iver the curved
        shape integration.
        Theta   -> the variable of integration
        D       -> the z distance from the object to the lens surface
        Rho_0   -> the radial distance of the circular element on the lens from D
        R       -> the radius of the circular object
        Rho_lim -> the limits of the integration. if none the max radius
        ###########################################################################
        """
        #this is the x coordinate
        x =  ( ( D * math.sin(Theta) ) ** 2 ) / ( 1 - math.sin(Theta) ** 2 )
        
        #this iss the processed A
        A =  Rho_0 ** 2 - Radius ** 2 + x
        
        #this is th eprocessed B
        B =  2. * Rho_0 * math.sqrt( x )
        

        try:
        
            Result = math.asin( A / B ) * D ** 2 * math.sin(Theta)
        
        except:
        
            if Theta < math.asin( numpy.abs(Rho_0 - Radius) / math.sqrt( numpy.abs(Rho_0 - Radius) ** 2 + D ** 2 )) and Rho_0 - Radius < 0:
            
                Result =  2. * math.pi * math.sin(Theta) * D **2
            
            else:
            
                Result = 0.
    
            
        return  Result

    def CreateMask(self, Objects , Elements):

        '''
        ##################################################
        This routine is deigned to grab the eliptical rep
        resentation of the lens onto the previous lens.
        
        The argument are the following:
        
        - Object: image object position to process
        - Element_0: the element to project
        - Element_1 the element to project to
        - Mask: the projection 
        
        N.B.: for now element_1 needs to be a Lens
        
        If a Mask is given it is already a projection. For
        example the projeciton of a circular pihole will
        give a mask that can then be proagated. It will have
        a center and a radius. 
        
        Object Parameters has to be formated as follows:
        
        Parameters[0] = z
        Parameters[1] = x
        Parameters[2] = y
        Parameters[3] = Anglexy (Aspect Ratio Angle)
        Parameters[4] = Angle (applies if z is infinite)
        Parameters[5] = Width (usualy cube height)
        Parameters[6] = Ratio (Solid angle calculation)
        ##################################################
        '''
        
        ###############
        #grab the elements
        Element_0 = Elements[0]
    
        ###############
        #grab the informations
        if Element_0.ParametersDict['Type'] == 'Lens':
    
            Center = [Element_0.ParametersDict['Position'],0,0]
            Radius = Element_0.ParametersDict['LensRadius']
    
        elif Element_0.ParametersDict['Type'] == 'CPinhole' :
        
            Center = [Element_0.ParametersDict['Position'],0,0]
            Radius = Element_0.ParametersDict['Parameters']

        
        #loop over objects
        for i in range(0, len(Objects)):
            
            #-------------------------------------------------------#
            ###############
            #grab the elements
            Element_1 = Elements[i+1]
        
            ###############
            #grab the informations
            if Element_1.ParametersDict['Type'] == 'Lens':
        
                EPos_1 = [Element_1.ParametersDict['Position'],0.0,0.0]
                ERad_1 = Element_1.ParametersDict['LensRadius']
        
            elif Element_1.ParametersDict['Type'] == 'CPinhole' :
            
                EPos_1 = [Element_1.ParametersDict['Position'],0.0,0.0]
                ERad_1 = Element_1.ParametersDict['Parameters']

            ###############
            #grab the object
            OPos  = Objects[i]
        
            #-------------------------------------------------------#
            
            #the case where the object is in the element
            if  OPos[0]  -  EPos_1[0]  == 0:
            
                Center = [0.0,0.0,0.0]
                Radius = numpy.inf
            
            elif OPos[0] == numpy.inf:
            
                Offset      = ( EPos_1[0] - Center[0] ) * math.sin(OPos[4])
                
                Angle       = OPos[3]
                
                Center[0]   = EPos_1[0]
                
                Center[1]   =  Offset * math.cos(Angle) + Center[1]
            
                Center[2]   =  Offset * math.sin(Angle) + Center[2]
                
                Radius = Radius
            
            elif ( Center[0] - OPos[0] ) == 0:
            
                return [[0.0,0.0,0.0], Radius, math.sqrt(Center[1]**2+Center[2]**2)]
            
            else:
                
                Ratio = ( EPos_1[0] - OPos[0] ) / ( Center[0] - OPos[0] )
                
                Radius      = numpy.abs(Radius * Ratio)

                Center[0]   = EPos_1[0]
                
                Center[1]   = ( ( Center[1] - OPos[1] ) * Ratio ) + Center[1]
            
                Center[2]   = ( ( Center[2] - OPos[2] ) * Ratio ) + Center[2]

        return [Center, Radius, math.sqrt(Center[1]**2+Center[2]**2)]
            

    def ChangeParameter(self, Parameter, Value):
        '''
        ##################################################
        by passing the attribute as an argument the user
        can change the value
        ##################################################
        '''

        #try to print the paramter
        try:
            
            #this serves as dialog but also check the coherence of the input
            print 'Trying to change: '+str(Parameter)+' from '+str(self.ParametersDict[Parameter])+' to '+str(Value)
                
            #change the parameter
            self.ParametersDict[Parameter] = Value
                
        except:

            print 'This attribute does not exist...'


    def LinkToEnvironnment(self, EnvironnementClass):
        '''
        ##################################################
        The user passes on the distance of the object. 
        Note that the distanc eis effective distance. This
        means that it is the distance at which the final
        setp sees the object...
        
        This means that one has to take into account
        the diffraction by surfaces.
        ##################################################
        '''
        
        #make the class locally available
        self.Environnement = EnvironnementClass
    
        #tell the system that we are linked
        self.ParametersDict['Environnement']     = True


class Lens:
    """
    ###########################################################################
    Moving away from the idea that the lens system can be processed at once 
    was maybe feasible but rendered the notations very strange. As Lens 
    classes were introduced that allow the transformation of planes along the
    axis. 
    
    This system will be based on an object and image formation method. The
    Computation will be done by self.ProcessLens()
    ###########################################################################
    """
    def __init__(self,LensManager,  ID , ParametersDict = None):
        '''
        ##################################################
        Note that the lens is set by a ParametersDict
        
        The parameters are straight forward when it comes
        to the Lens system.
        ##################################################
        '''
        
        #Set the parameters
        if ParametersDict == None :
        
            self.ParametersDict = {}
                
            self.ParametersDict['Type']              = 'Bifocal Lens'
            self.ParametersDict['LambdaIn']          = 633.e-9
            self.ParametersDict['FocalLength']       = 1.3e-3
            self.ParametersDict['LensRadius']        = 30.e-3
            self.ParametersDict['Position']          = 0.0
        
        else:
            
            self.ParametersDict         = ParametersDict
        
        #set the ID
        self.ID = ID
        self.Verbose = True
        
        #set the method dictionary
        self.Method = {}
            
        self.Method['Type_0'] = self.ProcessType_0
        self.Method['Type_1'] = self.ProcessType_1
        self.Method['Type_2'] = self.ProcessType_2
        self.Method['Type_3'] = self.ProcessType_3
        self.Method['Type_4'] = self.ProcessType_4
        self.Method['Type_5'] = self.ProcessType_7
        self.Method['Type_6'] = self.ProcessType_7
        self.Method['Type_7'] = self.ProcessType_7
        self.Method['Type_8'] = self.ProcessType_8
    
        #create the preference list
        self.CreatePreferenceList()

    def CreatePreferenceList(self):
        '''
        ##################################################
        This routin has the purpose to create an identifi
        cation list of properties.
        
        It will give the following informaitons:
        
        - Label name
        - Dictionary name
        - Dictionary pointer
        - Type (ex.: 'float', 'int', 'bool', 'float_array')
        
        ##################################################
        '''
    
        #initialise the list
        self.PreferenceList = []


        self.PreferenceList.append(['Focal length',
                                   'FocalLength',
                                   self.ParametersDict,
                                   'float'])
    
        self.PreferenceList.append(['Lens radius',
                                   'LensRadius',
                                   self.ParametersDict,
                                   'float'])
    
        self.PreferenceList.append(['Lens Position',
                                   'Position',
                                   self.ParametersDict,
                                   'float'])
    
    
    def __str__(self):
        '''
        ##################################################
        This will loop over the array and print each 
        indicidual sample information.
        ##################################################
        '''
        
        Output  = '\nLens ID: '+str(self.ID)
    
        for key, value in self.ParametersDict.iteritems():
        
            Output += '\n    - Parameter: '+str(key)+' => '+str(value)
        
        return Output
            
    def ChangeParameter(self, Parameter, Value):
        '''
        ##################################################
        by passing the attribute as an argument the user
        can change the value
        ##################################################
        '''

        #try to print the paramter
        try:
            
            #this serves as dialog but also check the coherence of the input
            print 'Trying to change: '+str(Parameter)+' from '+str(self.ParametersDict[Parameter])+' to '+str(Value)
                
            #change the parameter
            self.ParametersDict[Parameter] = Value
                
        except:

            print 'This attribute does not exist...'


    def Process(self, Parameters , Type = None):

        '''
        ##################################################
        This will grab the given Coordinates of the object
        and throw out split the processing depending to
        the focal scenario. 
        
        The object will be comprised of Position and a 
        width. Typically in the scope of cube representat.
        it will be the width aprameter chosen.
        
        Therefore we have:
        
            - Type_0 Object is coming from - infinity   DONE
            - Type_1 Object is located before -f        DONE
            - Type_2 Object is located at -f            DONE
            - Type_3 Object is between -f and 0         DONE
            - Type_4 Object is located at 0             DONE
            - Type_5 Object is between 0 and f          ABORTED
            - Type_6 Object is located at f             ABORTED
            - Type_7 Object is after f                  DONE
            - Type_8 Object is at infinity              DONE
            
        The output will vary depending on the position
        Type_2 for example will yield an Angle as it has
        an infinite image
        
        Nevertheless the idea is to allow for a lens series
        Therefore the Lens outpu needs to be immidiately 
        interpreted by the next lens...
        
        Parameters has to be formated as follows:
        
        Parameters[0] = z
        Parameters[1] = x
        Parameters[2] = y
        Parameters[3] = y
        Parameters[4] = Angle (applies if z is infinite)
        Parameters[5] = Width (usualy cube height)
        Parameters[6] = Ratio (Solid angle calculation)
        ##################################################
        '''
        
        Parameters = list(Parameters)
        
        #################################
        #Correct parameters on position
        Parameters[0] -= self.ParametersDict['Position']
        
        
        #################################
        #go through methods and cases
        if Type == None:
            
            if Parameters[0] == - numpy.inf:
                
                ParametersOut = self.ProcessType_0(Parameters)
            
            elif Parameters[0] < - self.ParametersDict['FocalLength'] and Parameters[0] > - numpy.inf:

                ParametersOut = self.ProcessType_1(Parameters)

            elif Parameters[0] == - self.ParametersDict['FocalLength']:

                ParametersOut = self.ProcessType_2(Parameters)

            elif Parameters[0] > - self.ParametersDict['FocalLength'] and Parameters[0] < 0:

                ParametersOut = self.ProcessType_3(Parameters)

            elif Parameters[0] == 0:

                ParametersOut = self.ProcessType_4(Parameters)
            
            elif Parameters[0] < self.ParametersDict['FocalLength'] and Parameters[0] > 0 :

                ParametersOut = self.ProcessType_7(Parameters)

            elif Parameters[0] == self.ParametersDict['FocalLength']:

                ParametersOut = self.ProcessType_7(Parameters)

            elif Parameters[0] > self.ParametersDict['FocalLength'] and Parameters[0] < numpy.inf:

                ParametersOut = self.ProcessType_7(Parameters)

            elif Parameters[0] == numpy.inf:
            
                ParametersOut = self.ProcessType_8(Parameters)

        else:
            
            ParametersOut = self.Method[Type]()

        #################################
        #Do the solid angle calculations
        #ParametersOut[6] *= 1

        #################################
        #Correct parameters on position
        ParametersOut[0] += self.ParametersDict['Position']

        return ParametersOut


    def ProcessType_0(self, Parameters):
        
        '''
        ##################################################
        This will grab the given Coordinates of the object
        and throw out split the processing depending to
        the focal scenario. 
        
        The object will be comprised of Position and a 
        width. Typically in the scope of cube representat.
        it will be the width aprameter chosen.
        
        Therefore we have:
        
        =>  - Type_0 Object is coming from - infinity
            - Type_1 Object is located before -f
            - Type_2 Object is located at -f
            - Type_3 Object is between -f and 0
            - Type_4 Object is located at 0
            - Type_5 Object is between 0 and f
            - Type_6 Object is located at f
            - Type_7 Object is after f
            - Type_8 Object is at infinity
            
        Parameters has to be formated as follows:
        
        Parameters[0] = z
        Parameters[1] = x
        Parameters[2] = y
        Parameters[3] = Anglexy (Aspect Ratio Angle)
        Parameters[4] = Angle (applies if z is infinite)
        Parameters[5] = Width (usualy cube height)
        Parameters[6] = Ratio (Solid angle calculation)
        ##################################################
        '''
        
        if self.Verbose:
        
            print 'Type_0'
        
        #we need the projected length
        l = self.ParametersDict['FocalLength'] / math.cos( Parameters[4] )
        
        #process out array
        ParametersOut = [self.ParametersDict['FocalLength'],
                         l * math.sin( Parameters[4] ) * math.cos( Parameters[3] ),
                         l * math.sin( Parameters[4] ) * math.sin( Parameters[3] ),
                         Parameters[3],
                         0.,
                         Parameters[5]]
                         
        return ParametersOut
            
    def ProcessType_1(self, Parameters):

        '''
        ##################################################
        This will grab the given Coordinates of the object
        and throw out split the processing depending to
        the focal scenario. 
        
        The object will be comprised of Position and a 
        width. Typically in the scope of cube representat.
        it will be the width aprameter chosen.
        
        Therefore we have:
        
            - Type_0 Object is coming from - infinity
         => - Type_1 Object is located before -f
            - Type_2 Object is located at -f
            - Type_3 Object is between -f and 0
            - Type_4 Object is located at 0
            - Type_5 Object is between 0 and f
            - Type_6 Object is located at f
            - Type_7 Object is after f
            - Type_8 Object is at infinity
            
        Parameters has to be formated as follows:
        
        Parameters[0] = z
        Parameters[1] = x
        Parameters[2] = y
        Parameters[3] = Anglexy (Aspect Ratio Angle)
        Parameters[4] = Angle (applies if z is infinite)
        Parameters[5] = Width (usualy cube height)
        Parameters[6] = Ratio (Solid angle calculation)
        ##################################################
        '''
        
        
        #Calculate the magnification using the focal length
        #we need to process the new point z
        zi = (  ( self.ParametersDict['FocalLength'] * numpy.abs( Parameters[0] ) )
              / ( numpy.abs( Parameters[0] ) - self.ParametersDict['FocalLength'] ) )
        
        M  = zi / numpy.abs( Parameters[0] )

        
        #we recquire only the angle (should be given in thhis case)
        ParametersOut = [ zi,
                          - Parameters[1] * M,
                          - Parameters[2] * M,
                         Parameters[3],
                         0.,
                         Parameters[5] * M]
                         
        return ParametersOut


    def ProcessType_2(self, Parameters):

        '''
        ##################################################
        This will grab the given Coordinates of the object
        and throw out split the processing depending to
        the focal scenario. 
        
        The object will be comprised of Position and a 
        width. Typically in the scope of cube representat.
        it will be the width aprameter chosen.
        
        Therefore we have:
        
            - Type_0 Object is coming from - infinity
            - Type_1 Object is located before -f
         => - Type_2 Object is located at -f
            - Type_3 Object is between -f and 0
            - Type_4 Object is located at 0
            - Type_5 Object is between 0 and f
            - Type_6 Object is located at f
            - Type_7 Object is after f
            - Type_8 Object is at infinity
            
        Parameters has to be formated as follows:
        
        Parameters[0] = z
        Parameters[1] = x
        Parameters[2] = y
        Parameters[3] = Anglexy (Aspect Ratio Angle)
        Parameters[4] = Angle (applies if z is infinite)
        Parameters[5] = Width (usualy cube height)
        Parameters[6] = Ratio (Solid angle calculation)
        ##################################################
        '''

        #we recquire only the angle (should be given in thhis case)
        ParametersOut = [numpy.inf,
                         Parameters[1],
                         Parameters[2],
                         Parameters[3],
                         math.acos(Parameters[0]/
                                   math.sqrt(Parameters[1]**2
                                             + Parameters[2]**2
                                             + Parameters[0]**2)),
                         Parameters[5]]
                         
        return ParametersOut
    
    def ProcessType_3(self, Parameters):

        '''
        ##################################################
        This will grab the given Coordinates of the object
        and throw out split the processing depending to
        the focal scenario. 
        
        The object will be comprised of Position and a 
        width. Typically in the scope of cube representat.
        it will be the width aprameter chosen.
        
        Therefore we have:
        
            - Type_0 Object is coming from - infinity
            - Type_1 Object is located before -f
            - Type_2 Object is located at -f
         => - Type_3 Object is between -f and 0
            - Type_4 Object is located at 0
            - Type_5 Object is between 0 and f
            - Type_6 Object is located at f
            - Type_7 Object is after f
            - Type_8 Object is at infinity
            
        Parameters has to be formated as follows:
        
        Parameters[0] = z
        Parameters[1] = x
        Parameters[2] = y
        Parameters[3] = Anglexy (Aspect Ratio Angle)
        Parameters[4] = Angle (applies if z is infinite)
        Parameters[5] = Width (usualy cube height)
        Parameters[6] = Ratio (Solid angle calculation)
        ##################################################
        '''
        #we need to process the new point z
        zi = (  ( self.ParametersDict['FocalLength'] * numpy.abs( Parameters[0] ) )
              / ( self.ParametersDict['FocalLength'] - numpy.abs( Parameters[0] ) ) )
        
        M  = zi / numpy.abs( Parameters[0] )
        
        #we recquire only the angle (should be given in thhis case)
        ParametersOut = [- zi,
                         Parameters[1] * M,
                         Parameters[2] * M,
                         Parameters[3],
                         0,
                         Parameters[5] * M]
                         
        return ParametersOut

    def ProcessType_4(self, Parameters):

        '''
        ##################################################
        This will grab the given Coordinates of the object
        and throw out split the processing depending to
        the focal scenario. 
        
        The object will be comprised of Position and a 
        width. Typically in the scope of cube representat.
        it will be the width aprameter chosen.
        
        Therefore we have:
        
            - Type_0 Object is coming from - infinity
            - Type_1 Object is located before -f
            - Type_2 Object is located at -f
            - Type_3 Object is between -f and 0
         => - Type_4 Object is located at 0
            - Type_5 Object is between 0 and f
            - Type_6 Object is located at f
            - Type_7 Object is after f
            - Type_8 Object is at infinity
            
        Parameters has to be formated as follows:
        
        Parameters[0] = z
        Parameters[1] = x
        Parameters[2] = y
        Parameters[3] = Angle (applies if z is infinite)
        Parameters[4] = Width (usualy cube height)
        Parameters[6] = Ratio (Solid angle calculation)
        ##################################################
        '''

        #we recquire only the angle (should be given in thhis case)
        ParametersOut = [None,
                         None,
                         None,
                         None,
                         None,
                         None]
        
        return ParametersOut


    def ProcessType_5(self, Parameters):

        '''
        ##################################################
        This will grab the given Coordinates of the object
        and throw out split the processing depending to
        the focal scenario. 
        
        The object will be comprised of Position and a 
        width. Typically in the scope of cube representat.
        it will be the width aprameter chosen.
        
        Therefore we have:
        
            - Type_0 Object is coming from - infinity
            - Type_1 Object is located before -f
            - Type_2 Object is located at -f
            - Type_3 Object is between -f and 0
            - Type_4 Object is located at 0
         => - Type_5 Object is between 0 and f
            - Type_6 Object is located at f
            - Type_7 Object is after f
            - Type_8 Object is at infinity
            
        Parameters has to be formated as follows:
        
        Parameters[0] = z
        Parameters[1] = x
        Parameters[2] = y
        Parameters[3] = Anglexy (Aspect Ratio Angle)
        Parameters[4] = Angle (applies if z is infinite)
        Parameters[5] = Width (usualy cube height)
        Parameters[6] = Ratio (Solid angle calculation)
        ##################################################
        '''
        
        return Parameters
    
    def ProcessType_6(self, Parameters):

        '''
        ##################################################
        This will grab the given Coordinates of the object
        and throw out split the processing depending to
        the focal scenario. 
        
        The object will be comprised of Position and a 
        width. Typically in the scope of cube representat.
        it will be the width aprameter chosen.
        
        Therefore we have:
        
            - Type_0 Object is coming from - infinity
            - Type_1 Object is located before -f
            - Type_2 Object is located at -f
            - Type_3 Object is between -f and 0
            - Type_4 Object is located at 0
            - Type_5 Object is between 0 and f
         => - Type_6 Object is located at f
            - Type_7 Object is after f
            - Type_8 Object is at infinity
         
        Parameters has to be formated as follows:
        
        Parameters[0] = z
        Parameters[1] = x
        Parameters[2] = y
        Parameters[3] = Anglexy (Aspect Ratio Angle)
        Parameters[4] = Angle (applies if z is infinite)
        Parameters[5] = Width (usualy cube height)
        Parameters[6] = Ratio (Solid angle calculation)
        ##################################################
        '''
        
        return Parameters

    def ProcessType_7(self, Parameters):

        '''
        ##################################################
        This will grab the given Coordinates of the object
        and throw out split the processing depending to
        the focal scenario. 
        
        The object will be comprised of Position and a 
        width. Typically in the scope of cube representat.
        it will be the width aprameter chosen.
        
        Therefore we have:
        
            - Type_0 Object is coming from - infinity
            - Type_1 Object is located before -f
            - Type_2 Object is located at -f
            - Type_3 Object is between -f and 0
            - Type_4 Object is located at 0
            - Type_5 Object is between 0 and f
            - Type_6 Object is located at f
         => - Type_7 Object is after f
            - Type_8 Object is at infinity
          
        Parameters has to be formated as follows:
        
        Parameters[0] = z
        Parameters[1] = x
        Parameters[2] = y
        Parameters[3] = Anglexy (Aspect Ratio Angle)
        Parameters[4] = Angle (applies if z is infinite)
        Parameters[5] = Width (usualy cube height)
        Parameters[6] = Ratio (Solid angle calculation)
        ##################################################
        '''
        
        #calculate new z:
        zi = (  ( numpy.abs( Parameters[0] ) * self.ParametersDict['FocalLength'] )
              / ( self.ParametersDict['FocalLength'] - numpy.abs(Parameters[0])) )
        
        M  = zi / numpy.abs( Parameters[0] )

        #we recquire only the angle (should be given in thhis case)
        ParametersOut = [zi,
                         Parameters[1] * M,
                         Parameters[2] * M,
                         Parameters[3],
                         0.,
                         Parameters[5] * M]
                    

        return ParametersOut

    def ProcessType_8(self, Parameters):

        '''
        ##################################################
        This will grab the given Coordinates of the object
        and throw out split the processing depending to
        the focal scenario. 
        
        The object will be comprised of Position and a 
        width. Typically in the scope of cube representat.
        it will be the width aprameter chosen.
        
        Therefore we have:
        
            - Type_0 Object is coming from - infinity
            - Type_1 Object is located before -f
            - Type_2 Object is located at -f
            - Type_3 Object is between -f and 0
            - Type_4 Object is located at 0
            - Type_5 Object is between 0 and f
            - Type_6 Object is located at f
            - Type_7 Object is after f
         => - Type_8 Object is at infinity
           
        Parameters has to be formated as follows:
        
        Parameters[0] = z
        Parameters[1] = x
        Parameters[2] = y
        Parameters[3] = Anglexy (Aspect Ratio Angle)
        Parameters[4] = Angle (applies if z is infinite)
        Parameters[5] = Width (usualy cube height)
        Parameters[6] = Ratio (Solid angle calculation)
        ##################################################
        '''

        #we recquire only the angle (should be given in thhis case)
        ParametersOut = [self.ParametersDict['FocalLength'],
                         math.tan( Parameters[4] ) * self.ParametersDict['FocalLength'],
                         math.tan( Parameters[4] ) * self.ParametersDict['FocalLength'],
                         Parameters[3],
                         0.,
                         Parameters[5]]
                         
        return ParametersOut




class Pinhole:
    """
    ###########################################################################
    In a similar effort to the Lens system it was decided to move the Pinhole
    to a separate class that keeps its aspects stored locally. The object
    manipulation follows the same pattern as the lens.
    ###########################################################################
    """
    def __init__(self,LensManager,  ID , ParametersDict = None):
        '''
        ##################################################
        Note that the lens is set by a ParametersDict
        
        The parameters are straight forward when it comes
        to the Lens system.
        ##################################################
        '''
        
        #Set the parameters
        if ParametersDict == None :
        
            self.ParametersDict = {}
                
            self.ParametersDict['Type']              = 'Circular Pinhole'
            self.ParametersDict['Parameters']        = 80.e-6
            self.ParametersDict['Position']          = 0.
        
        else:
            
            self.ParametersDict         = ParametersDict
        
        #set the ID
        self.ID = ID

        #create the preference list
        self.CreatePreferenceList()

    def CreatePreferenceList(self):
        '''
        ##################################################
        This routin has the purpose to create an identifi
        cation list of properties.
        
        It will give the following informaitons:
        
        - Label name
        - Dictionary name
        - Dictionary pointer
        - Type (ex.: 'float', 'int', 'bool', 'float_array')
        
        ##################################################
        '''
    
        #initialise the list
        self.PreferenceList = []

        self.PreferenceList.append(['Pinhole radius',
                                   'Parameters',
                                   self.ParametersDict,
                                   'float'])
    
        self.PreferenceList.append(['Pinhole position',
                                   'Position',
                                   self.ParametersDict,
                                   'float'])
    
    def __str__(self):
        '''
        ##################################################
        This will loop over the array and print each 
        indicidual sample information.
        ##################################################
        '''
        
        Output  = '\nLens ID: '+str(self.ID)
    
        for key, value in self.ParametersDict.iteritems():
        
            Output += '\n    - Parameter: '+str(key)+' => '+str(value)
        
        return Output
            
    def ChangeParameter(self, Parameter, Value):
        '''
        ##################################################
        by passing the attribute as an argument the user
        can change the value
        ##################################################
        '''

        #try to print the paramter
        try:
            
            #this serves as dialog but also check the coherence of the input
            print 'Trying to change: '+str(Parameter)+' from '+str(self.ParametersDict[Parameter])+' to '+str(Value)
                
            #change the parameter
            self.ParametersDict[Parameter] = Value
                
        except:

            print 'This attribute does not exist...'

    def Process(self, Parameters):
        '''
        ##################################################
        Nevertheless the idea is to allow for a lens series
        Therefore the Lens outpu needs to be immidiately 
        interpreted by the next lens...
        
        Parameters has to be formated as follows:
        
        Parameters[0] = z
        Parameters[1] = x
        Parameters[2] = y
        Parameters[3] = Angle (applies if z is infinite)
        Parameters[4] = Width (usualy cube height)
        ##################################################
        '''
        
        #circular Pinhole
        if self.ParametersDict['Type'] == 'Circular Pinhole':

            return (math.sqrt(Parameters[1] ** 2 + Parameters[2] ** 2) < self.ParametersDict['Parameters'])



class SampleManager:
    """
    ###########################################################################
    As multiple subsamples might be present in the Sample a manager class will
    take care of them
    
    The folowwing funcitons will be present:
    - __init__() to initialise the class.
    
    - __str__() to print the details of the class
    
    - self.DeleteAll() to print the details of the class
    
    - self.AddSample() Add a sample to the list
    
    - self.ChangeOrder() change the order of the smple arrangement
    
    - self.ChangeParameter(): This will allow the user to update a dictionary
        element of the parameters. 
    
    - self.CreateCubes(): This routine will be used to discretise the sample
        Volume. Note that the Volums parameters should be given to allow a
        computation with the angular acceptance
        
    
    ###########################################################################
    """
    def __init__(self):
        '''
        ##################################################
        This class initialises the manager. Note that it
        will also automatically create the first Sample 
        as it is the environement of the lens...
        
        This also means that this sample needs to be
        modified as the zoom is launched. 
        
        This will be handled in the Manager class for the 
        whole calculaiton...
        
        ##################################################
        '''
        
        #define he link array
        self.SampleLinks    = []
        self.ID             = 0
        self.LensManager    = None
        
        #add the first sample auomatically
        #the default is air...
        self.AddSample()
    
    def __str__(self):
        '''
        ##################################################
        This will loop over the array and print each 
        indicidual sample information.
        ##################################################
        '''
        
        Output  = '###########################################'
        Output += '\n###########################################'
        Output += '\n    - Currently '+str(len(self.SampleLinks))+' samples are defined'
    
        for Sample in self.SampleLinks:
        
            Output += Sample.__str__()
        
        return Output
    
    def LinkToEnvironnment(self, EnvironnementClass):
        '''
        ##################################################
        The user passes on the distance of the object. 
        Note that the distanc eis effective distance. This
        means that it is the distance at which the final
        setp sees the object...
        
        This means that one has to take into account
        the diffraction by surfaces.
        ##################################################
        '''
        
        #make the class locally available
        self.LensManager = EnvironnementClass

    def DeleteAll(self):
        '''
        ##################################################
        This function will delete all samples and reset
        the array self.SampleLinks
        ##################################################
        '''
    
        #reset the array
        self.SampleLinks = []
    
    def AddSamples(self, Num, Parameters):
        '''
        ##################################################
        This function will set  number Num of samples
        ##################################################
        '''
        for i in range(0,Num):
    
            self.AddSample()
        
    def AddSample(self, ParameterDict = None):
        '''
        ##################################################
        This will add a sample usiong the sample class
        
        The parameterDict is optional...
        It is supposed to contain the parameters that
        will be added when the class is initialised
        
        obviously the sample class will be smart enought
        to try loading the parameters and notify the
        user if something failed
        ##################################################
        '''
        
        #Add the element
        self.SampleLinks.append(Sample(self, self.ID,ParameterDict))
    
        #change the ID so whatever happens two elements never have the same ID
        self.ID += 1

    def ChangeOrder(self, Parameter, Value):
        '''
        ##################################################
        by passing the attribute as an argument the user
        can change the value
        ##################################################
        '''

        pass
    
    def Coordinates(self):
        '''
        ##################################################
        Once all samples are defined a proper coordinate
        calculaiton can be done to allow the global 
        calcultions of intensities through multiple layers
        
        The zero will always be between the two first
        samples
        ##################################################
        '''
    
        #cycle through
        for i in range(0,len(self.SampleLinks)):
            
            if i == 0:
                    
                #set the cubes
                self.SampleLinks[i].SetAbsPosition()

                #set the new position
                Position = 0
            
            else:
                
                
                
                #set the position
                self.SampleLinks[i].ParametersDict['Position'] = Position
                    
                #set the cubes
                self.SampleLinks[i].SetAbsPosition()

                #set the new position
                Position += self.SampleLinks[i].ParametersDict['Depth']

    

    def ChangeParameter(self, Num, Parameter, Value):
        '''
        ##################################################
        by passing the attribute as an argument the user
        can change the value
        ##################################################
        '''

        #try to print the paramter
        self.SampleLinks[Num].ChangeParameter(Parameter,Value)

    def CreateCubes(self, Num = 'All', Parameter = None):
        '''
        ##################################################
        by passing the attribute as an argument the user
        can change the value
        ##################################################
        '''
        if Num == 0:
        
            #try to print the paramter
            self.SampleLinks[Num].CreateVoidCubes(Parameter)

        elif Num == 'All':
        
            for i in range(0, len(self.SampleLinks)):
                
                if i == 0:
        
                    #try to print the paramter
                    self.SampleLinks[i].CreateVoidCubes(Parameter)
                
                else:
        
                    #try to print the paramter
                    self.SampleLinks[i].CreateCubes(Parameter)
        else:
        
            #try to print the paramter
            self.SampleLinks[Num].CreateCubes(Parameter)

    def ResetCollectionIntensities(self):
        
        '''
        ##################################################
        This routine will allow to set all collection
        cubes to 0. To avoind to much addition
        ##################################################
        '''

        #cycle through
        for Sample in self.SampleLinks:
        
            Sample.ResetCollectionIntensities()

    def CorrectCubes(self):
        
        '''
        ##################################################
        This routine will allow to set all collection
        cubes to 0. To avoind to much addition
        ##################################################
        '''

        #cycle through
        for i in range(1, len( self.SampleLinks ) ) :
        
            self.SampleLinks[i].CorrectCubes()

    def CollectedIntensity(self):
        
        '''
        ##################################################
        This routine will allow to set all collection
        cubes to 0. To avoind to much addition
        ##################################################
        '''
        self.Intensity = []
        
        #cycle through
        for i in range(0, len( self.SampleLinks ) ) :
        
            self.Intensity.append(self.SampleLinks[i].CollecTotalIntensity())

    def RetrieveFact(self):
        
        '''
        ##################################################
        This funciton will loop and retrieve the current
        input factor...
        ##################################################
        '''
        self.Fact = []
        
        #cycle through
        for i in range(0, len( self.SampleLinks ) ) :
        
            try:
                self.Fact.append(self.SampleLinks[i].ProcessRamanIntensityFactor(self.LensManager.ParametersDict['LambdaIn'],
                                                                            self.LensManager.ParametersDict['LambdaOut']))
            except:
                pass
    
        return self.Fact

class Sample:
    """
    ###########################################################################
    This Classwill posess all the parameters of the given Sample System. 
    This includes it's thickness and
    
    The folowwing funcitons will be present:
    - __init__() to initialise the class.
    
    -__str__() to print the details of the class
    
    - self.ChangeParameter(): This will allow the user to update a dictionary
        element of the parameters. 
    
    - self.CreateCubes(): This routine will be used to rasterize the sample
        Volume. Note that the Volums parameters should be given to allow a
        computation with the angular acceptance
        
    
    ###########################################################################
    """
    def __init__(self, Parent, ID, ParametersDict):
    
        #define the parameters of the sample
        self.Parent         = Parent
        self.LensManager    = Parent.LensManager
        self.ID             = ID
        self.Cubes          = []
        self.CubeDim        = '_x_x_'
        self.Verbose        = False
        
        
        #unpackage the parameetrs
        if not ParametersDict == None:
    
            self.ParametersDict = dict(ParametersDict)

        else:
            
            #default parameters
            self.ParametersDict = {}

            #set them
            self.ParametersDict['Index']        = 1.0
            self.ParametersDict['Depth']        = 1.e-6
            self.ParametersDict['Absorption']   = 0.0 #intensity per distance for now
            self.ParametersDict['Raman']        = False
        
        
            self.ParametersDict['ZSteps'] = 1000    #defines the amount of cubes in Z
            self.ParametersDict['XSteps'] = 01      #defines the amount of cubes in X
            self.ParametersDict['YSteps'] = 01      #defines the amount of cubes in Y
            
            self.ParametersDict['ZDim'] = self.ParametersDict['Depth'] #defines the dimension of the cube
            self.ParametersDict['XDim'] = 1.e-6     #defines the dimension of the cube
            self.ParametersDict['YDim'] = 1.e-6
        
        #---------------------------#
        #will be set later
        self.ParametersDict['Name']             = 'No Name Set'
        self.ParametersDict['Illuminated']      = True
        self.ParametersDict['Abs']              = False
        self.ParametersDict['Cubes']            = False
        self.ParametersDict['Position']         = 'unknown'
        self.ParametersDict['CubeDimension']    = self.CubeDim
        self.ParametersDict['Cubenumber']       = 0
        self.ParametersDict['Integration']      = False
        
        #---------------------------#
        #profile paths
        self.ParametersDict['RamanProfileLoaded']       = False
        self.ParametersDict['RamanProfilePath']         = ''
        self.ParametersDict['AbsorptionProfileLoaded']  = False
        self.ParametersDict['AbsorptionProfilePath']    = ''
        self.ParametersDict['IndexProfileLoaded']       = False
        self.ParametersDict['IndexProfilePath']         = ''
    
    
        #---------------------------#
        #Create the preference Lise
        self.CreatePreferenceList()

    def CreatePreferenceList(self):
        '''
        ##################################################
        This routin has the purpose to create an identifi
        cation list of properties.
        
        It will give the following informaitons:
        
        - Label name
        - Dictionary name
        - Dictionary pointer
        - Type (ex.: 'float', 'int', 'bool', 'float_array')
        
        ##################################################
        '''
    
        #initialise the list
        self.PreferenceList = []

        self.PreferenceList.append(['Sample Name',
                                   'Name',
                                   self.ParametersDict,
                                   'str'])
    
    
        self.PreferenceList.append(['Sample index',
                                   'Index',
                                   self.ParametersDict,
                                   'float'])
    
        self.PreferenceList.append(['Absorbing',
                                   'Abs',
                                   self.ParametersDict,
                                   'bool'])
                                   
        self.PreferenceList.append(['Absorption',
                                   'Absorption',
                                   self.ParametersDict,
                                   'float'])
                                   
        self.PreferenceList.append(['Raman active',
                                   'Raman',
                                   self.ParametersDict,
                                   'bool'])
                                   
        self.PreferenceList.append(['ZSteps',
                                   'ZSteps',
                                   self.ParametersDict,
                                   'int'])

        self.PreferenceList.append(['XSteps',
                                   'XSteps',
                                   self.ParametersDict,
                                   'int'])
    
        self.PreferenceList.append(['Depth',
                                   'Depth',
                                   self.ParametersDict,
                                   'float'])

        self.PreferenceList.append(['XDim',
                                   'XDim',
                                   self.ParametersDict,
                                   'float'])

        self.PreferenceList.append(['Integration',
                                   'Integration',
                                   self.ParametersDict,
                                   'bool'])
    
        self.PreferenceList.append(['Raman Profile Loaded',
                                   'RamanProfileLoaded',
                                   self.ParametersDict,
                                   'bool'])
    
        self.PreferenceList.append(['Raman Profile Path',
                                   'RamanProfilePath',
                                   self.ParametersDict,
                                   'Path'])
    
        self.PreferenceList.append(['Index Profile Loaded',
                                   'IndexProfileLoaded',
                                   self.ParametersDict,
                                   'bool'])
    
        self.PreferenceList.append(['Index Profile Path',
                                   'IndexProfilePath',
                                   self.ParametersDict,
                                   'Path'])
    
        self.PreferenceList.append(['Absorption Profile Loaded',
                                   'AbsorptionProfileLoaded',
                                   self.ParametersDict,
                                   'bool'])
    
        self.PreferenceList.append(['Absorption Profile Path',
                                   'AbsorptionProfilePath',
                                   self.ParametersDict,
                                   'Path'])
    
    
    
    def __str__(self):
        '''
        ##################################################
        This will loop over the array and print each 
        indicidual sample information.
        ##################################################
        '''
        
        Output  = '\n-------------'
        Output  = '\nSample ID: '+str(self.ID)
    
        for key, value in self.ParametersDict.iteritems():
        
            Output += '\n    - Parameter: '+str(key)+' => '+str(value)
        
        return Output
    
    def ChangeParameter(self, Parameter, Value):
        '''
        ##################################################
        by passing the attribute as an argument the user
        can change the value
        ##################################################
        '''
    
        #try to print the paramter
        try:
            
            #this serves as dialog but also check the coherence of the input
            print 'Trying to change: '+str(Parameter)+' from '+str(self.ParametersDict[Parameter])+' to '+str(Value)
                
            #change the parameter
            self.ParametersDict[Parameter] = Value
                
        except:

            print 'This attribute does not exist...'


    def LoadRamanResponseProfile(self):
        '''
        ##################################################
        This routine will load an intensity profile into
        the sample class an then allow for wave number
        dependant raman calculations.
        ##################################################
        '''
        #count lines
        num_lines = sum(1 for line in open(os.path.join(os.getcwd(),self.ParametersDict['RamanProfilePath'])))
        
        #open the file
        f = open(os.path.join(os.getcwd(),self.ParametersDict['RamanProfilePath']))
        
        #initialise array
        Content = []
        
        #open the text file
        for i in range(0, num_lines):
        
            #grab
            Content.append(f.readline())
                
        #cloe the file
        f.close()
        
        #initialise the arrays
        self.omega = []
        self.Val = []
        
        #read the values
        for i in range(0, len(Content)):
            
            try:
                
                #split all
                self.omega.append(float(Content[i].split(' ')[0]))
                self.Val.append(float(Content[i].split(' ')[1].strip('\n')))
            except:
                pass

        print 'Loaded the definition file...'
        
        #set the boolean value
        self.ParametersDict['RamanProfileLoaded'] = True


    def ProcessRamanIntensityFactor(self, InWavelength, OutWavelength):
        '''
        ##################################################
        This routine will fetch the closest value of the
        intensity factor from the loaded profile to
        perform the analysis...
        
        given is input and output wavelengths
        ##################################################
        '''
        #calculate the wavenumber
        Val = ((1. / (InWavelength * 100.))
               - (1. / (OutWavelength * 100.)))
               
            
        if self.Verbose:
            print '######################'
            print 'This is InWavelength: ',InWavelength
            print 'This is OutWavelength: ',OutWavelength
            print 'This is the wavenumber: ',Val
            print 'This is the index: ', (numpy.abs(numpy.asarray(self.omega)-Val)).argmin()
            print 'This is final number value: ',self.Val[(numpy.abs(numpy.asarray(self.omega)-Val)).argmin()]
        
        #set ou the value
        return self.Val[(numpy.abs(numpy.asarray(self.omega)-Val)).argmin()]
    
    
    def LoadIndexResponseProfile(self):
        '''
        ##################################################
        This routine will load an intensity profile into
        the sample class an then allow for wave number
        dependant raman calculations.
        ##################################################
        '''
        #count lines
        num_lines = sum(1 for line in open(os.path.join(os.getcwd(),self.ParametersDict['IndexProfilePath'])))
        
        #open the file
        f = open(os.path.join(os.getcwd(),self.ParametersDict['IndexProfilePath']))
        
        #initialise array
        Content = []
        
        #open the text file
        for i in range(0, num_lines):
        
            #grab
            Content.append(f.readline())
                
        #cloe the file
        f.close()
        
        #initialise the arrays
        self.IndexLambda = []
        self.IndexVal = []
        
        #read the values
        for i in range(0, len(Content)):
            
            try:
                
                #split all
                self.IndexLambda.append(float(Content[i].split(' ')[0]))
                self.IndexVal.append(float(Content[i].split(' ')[1].strip('\n')))
            except:
                pass

        print 'Loaded the definition file...'
        
        #set the boolean value
        self.ParametersDict['IndexProfileLoaded'] = True


    def ProcessCurrentIndex(self, OutWavelength):
        '''
        ##################################################
        This routine will fetch the closest value of the
        intensity factor from the loaded profile to
        perform the analysis...
        
        given is input and output wavelengths
        ##################################################
        '''
        #calculate the wavenumber
        if self.ParametersDict['IndexProfileLoaded']:
            
            #grab the index
            Index = (numpy.abs(numpy.asarray(self.IndexLambda)-OutWavelength)).argmin()
            
            #if the index is a border
            if (OutWavelength < self.IndexVal[0]) or (OutWavelength < self.IndexVal[-1]):
        
                return self.IndexVal[Index]
    
            else:
                
                #if the value is below
                if OutWavelength < self.IndexVal[Index]:
    
                    return (    (self.IndexVal[Index] - self.IndexVal[Index-1])
                            /   (self.IndexLambda[Index] - self.IndexLambda[Index - 1])
                            * OutWavelength
                            + self.IndexVal[Index-1])
                        
                #if the value is above
                elif OutWavelength > self.IndexVal[Index]:
    
                    return (    (self.IndexVal[Index+1] - self.IndexVal[Index])
                            /   (self.IndexLambda[Index+1] - self.IndexLambda[Index])
                            * OutWavelength
                            + self.IndexVal[Index])
                #if equal
                else:
                    return self.IndexVal[Index]
        else:
    
            return self.ParametersDict['Index']

    def LoadAbsorptionResponseProfile(self):
        '''
        ##################################################
        This routine will load an intensity profile into
        the sample class an then allow for wave number
        dependant raman calculations.
        ##################################################
        '''
        #count lines
        num_lines = sum(1 for line in open(os.path.join(os.getcwd(),self.ParametersDict['AbsorptionProfilePath'])))
        
        #open the file
        f = open(os.path.join(os.getcwd(),self.ParametersDict['AbsorptionProfilePath']))
        
        #initialise array
        Content = []
        
        #open the text file
        for i in range(0, num_lines):
        
            #grab
            Content.append(f.readline())
                
        #cloe the file
        f.close()
        
        #initialise the arrays
        self.AbsLambda = []
        self.AbsVal = []
        
        #read the values
        for i in range(0, len(Content)):
            
            try:
                
                #split all
                self.AbsLambda.append(float(Content[i].split(' ')[0]))
                self.AbsVal.append(float(Content[i].split(' ')[1].strip('\n')))
            except:
                pass

        print 'Loaded the definition file...'
        
        #set the boolean value
        self.ParametersDict['AbsorptionProfileLoaded'] = True


    def ProcessCurrentAbsorption(self, OutWavelength):
        '''
        ##################################################
        This routine will fetch the closest value of the
        intensity factor from the loaded profile to
        perform the analysis...
        
        given is input and output wavelengths
        ##################################################
        '''
        #calculate the wavenumber
        if self.ParametersDict['AbsorptionProfileLoaded']:
        
            #grab the index
            Index = (numpy.abs(numpy.asarray(self.AbsLambda)-OutWavelength)).argmin()
            
            #if the index is a border
            if (OutWavelength < self.AbsVal[0]) or (OutWavelength > self.AbsVal[-1]):
        
                Val =  self.AbsVal[Index]
    
            else:
                
                #if the value is below
                if OutWavelength < self.AbsVal[Index]:
    
                    Val =   (    (self.AbsVal[Index] - self.AbsVal[Index-1])
                            /   (self.AbsLambda[Index] - self.AbsLambda[Index - 1])
                            * OutWavelength
                            + self.AbsVal[Index-1])
                        
                #if the value is above
                elif OutWavelength > self.AbsVal[Index]:
    
                    Val =   (    (self.AbsVal[Index+1] - self.AbsVal[Index])
                            /   (self.AbsLambda[Index+1] - self.AbsLambda[Index])
                            * OutWavelength
                            + self.AbsVal[Index])
                #if equal
                else:
                    Val =   self.AbsVal[Index]
                
        else:
    
            Val =   self.ParametersDict['Absorption']

        return Val
    

    def CreateCubes(self, Parameters = None ):
        
        '''
        ##################################################
        This fucniton will launch the cube creation. the
        only parameters to be handed is a dictionary
        as folows:
        
        Parameters = {}
        
        Parameters['ZSteps'] = 10 #defines the amount of cubes in Z
        Parameters['XSteps'] = 10 #defines the amount of cubes in X
        Parameters['YSteps'] = 01 #defines the amount of cubes in Y
        Parameters['XDim'] = 0.1e-6 #defines the dimension of the cube
        Parameters['YDim'] = 0.1e-6 #defines the dimension of the cube
        
        Note that the sample Z = 0 position is set to the
        surface. This also means that the cube position
        will be determined in an absolute manner.
        
        The X and Y positions ont he other hand are
        relatif to the beam axis. This allows for simetry
        treatment.
        ##################################################
        '''
        
        #if the parameters have not been given set them with default
        if Parameters == None:
        
            pass

        else:
        
            self.ParametersDict['ZSteps'] = Parameters['ZSteps'] #defines the amount of cubes in Z
            self.ParametersDict['XSteps'] = Parameters['XSteps'] #defines the amount of cubes in X
            self.ParametersDict['YSteps'] = Parameters['YSteps'] #defines the amount of cubes in Y
            
            self.ParametersDict['ZDim'] = self.ParametersDict['Depth'] #defines the dimension of the cube
            self.ParametersDict['XDim'] = Parameters['XDim'] #defines the dimension of the cube
            self.ParametersDict['YDim'] = Parameters['YDim'] #defines the dimension of the cube
                        
        #defines the dimension of the cube along Z will be overwriten
        self.ParametersDict['ZDim'] = self.ParametersDict['Depth']
        
        #create the list of pointer to the cubes
        self.Cubes = [[[None for i in range(self.ParametersDict['YSteps'])]
                       for j in range(self.ParametersDict['XSteps'])]
                      for j in range(self.ParametersDict['ZSteps'])]
        
        #create the cubes
        for i in range(self.ParametersDict['ZSteps']):
            
            for j in range(self.ParametersDict['XSteps']):
                
                for k in range(self.ParametersDict['YSteps']):

                    self.Cubes[i][j][k] = SampleCube(self,
                                                     [float(i) * float(self.ParametersDict['ZDim'])/float(self.ParametersDict['ZSteps']),
                                                      float(j) * float(self.ParametersDict['XDim'])/float(self.ParametersDict['XSteps']),
                                                      float(k) * float(self.ParametersDict['YDim'])/float(self.ParametersDict['YSteps'])],
                                                     
                                                     [float(self.ParametersDict['ZDim'])/float(self.ParametersDict['ZSteps']),
                                                      float(self.ParametersDict['XDim'])/float(self.ParametersDict['XSteps']),
                                                      float(self.ParametersDict['YDim'])/float(self.ParametersDict['YSteps'])])
                                                      
        #send it out
        self.ParametersDict['Cubes'] = True
        self.ParametersDict['CubeDimension'] = str(self.ParametersDict['ZDim'])+'x'+str(self.ParametersDict['XDim'])+'x'+str(self.ParametersDict['YDim'])
        self.ParametersDict['Cubenumber'] = float(self.ParametersDict['ZSteps']) * float(self.ParametersDict['XSteps']) * float(self.ParametersDict['YSteps'])

        #create the preference list
        self.CreatePreferenceList()
    
    def CreateVoidCubes(self, Parameters = None ):
        
        '''
        ##################################################
        This fucniton will launch the cube creation. the
        only parameters to be handed is a dictionary
        as folows:
        
        Parameters = {}
        
        Parameters['ZSteps'] = 10 #defines the amount of cubes in Z
        Parameters['XSteps'] = 10 #defines the amount of cubes in X
        Parameters['YSteps'] = 01 #defines the amount of cubes in Y
        Parameters['XDim'] = 0.1e-6 #defines the dimension of the cube
        Parameters['YDim'] = 0.1e-6 #defines the dimension of the cube
        
        Note that the sample Z = 0 position is set to the
        surface. This also means that the cube position
        will be determined in an absolute manner.
        
        The X and Y positions ont he other hand are
        relatif to the beam axis. This allows for simetry
        treatment.
        ##################################################
        '''

        #if the parameters have not been given set them with default
        if Parameters == None:

            pass

        else:
        
            self.ParametersDict['ZSteps'] = Parameters['ZSteps'] #defines the amount of cubes in Z
            self.ParametersDict['XSteps'] = Parameters['XSteps'] #defines the amount of cubes in X
            self.ParametersDict['YSteps'] = Parameters['YSteps'] #defines the amount of cubes in Y
            
            self.ParametersDict['ZDim'] = Parameters['ZDim'] #defines the dimension of the cube
            self.ParametersDict['XDim'] = Parameters['XDim'] #defines the dimension of the cube
            self.ParametersDict['YDim'] = Parameters['YDim'] #defines the dimension of the cube


        #create the list of pointer to the cubes
        self.Cubes = [[[None
                        for i in range(self.ParametersDict['YSteps'])]
                       for j in range(self.ParametersDict['XSteps'])]
                      for j in range(self.ParametersDict['ZSteps'])]
        
        #create the cubes
        for i in range(self.ParametersDict['ZSteps']):
            
            for j in range(self.ParametersDict['XSteps']):
                
                for k in range(self.ParametersDict['YSteps']):

                    self.Cubes[i][j][k] = SampleCube(self,
                                                     
                                                     [ - float(i) * float(self.ParametersDict['ZDim']) / float(self.ParametersDict['ZSteps']) ,
                                                         float(j) * float(self.ParametersDict['XDim']) / float(self.ParametersDict['XSteps']) ,
                                                         float(k) * float(self.ParametersDict['YDim']) / float(self.ParametersDict['YSteps']) ] ,
                                                     
                                                     [ -     float(self.ParametersDict['ZDim']) / float(self.ParametersDict['ZSteps']) ,
                                                             float(self.ParametersDict['XDim']) / float(self.ParametersDict['XSteps']) ,
                                                             float(self.ParametersDict['YDim']) / float(self.ParametersDict['YSteps']) ] )

    
        #reverse Z
        self.Cubes = self.Cubes[::-1]
        
        #send it out
        self.ParametersDict['Cubes'] = True
        self.ParametersDict['CubeDimension'] = str(-self.ParametersDict['ZDim'])+'x'+str(self.ParametersDict['XDim'])+'x'+str(self.ParametersDict['YDim'])
        self.ParametersDict['Cubenumber'] = float(self.ParametersDict['ZSteps']) * float(self.ParametersDict['XSteps']) * float(self.ParametersDict['YSteps'])

        #give to this sample a final prameter swhich is position
        self.ParametersDict['Position'] = 0.#- Parameters['ZDim']
        self.ParametersDict['Depth'] = self.ParametersDict['ZDim']

        #create the preference list
        self.CreatePreferenceList()
    
    def SetAbsPosition(self):
        
        '''
        ##################################################
        This will update or set the absolute position of
        the cubes to make sure they have a correct 
        distance set.
        ##################################################
        '''

        #cycle through
        for i in range(len(self.Cubes)):
        
            for j in range(len(self.Cubes[i])):

                for k in range(len(self.Cubes[i][j])):

                    #copy the position
                    self.Cubes[i][j][k].AbsPosition = list(self.Cubes[i][j][k].Position)

                    #set the new position
                    self.Cubes[i][j][k].AbsPosition[0] += float(self.ParametersDict['Position'])#+0.0001*10e-10

    def CorrectCubes(self):
        
        '''
        ##################################################
        This will update or set the absolute position of
        the cubes to make sure they have a correct 
        distance set.
        ##################################################
        '''

        #cycle through
        for i in range(len(self.Cubes)):
        
            for j in range(len(self.Cubes[i])):

                for k in range(len(self.Cubes[i][j])):

                    #copy the position
                    self.Cubes[i][j][k].CorrectAbsPosition()
                    self.LensManager.ComputeObjects(self.Cubes[i][j][k])


    def ResetCollectionIntensities(self):
        
        '''
        ##################################################
        This routine will allow to set all collection
        cubes to 0. To avoind to much addition
        ##################################################
        '''
        pass

    def CollecTotalIntensity(self):
        '''
        ##################################################
        This aims at collecting the total intensity
        of the sampel to provide the ability of doing 
        depth profile curves :)
        ##################################################
        '''
        self.TotalIntensity = 0.0

        for i in range(len(self.Cubes)):
        
            for j in range(len(self.Cubes[i])):

                for k in range(len(self.Cubes[i][j])):

                    #copy the position
                    self.TotalIntensity += self.Cubes[i][j][k].CollectedIntensity * self.Cubes[i][j][k].EffectiveVolume


        return self.TotalIntensity


class SampleCube:
    """
    ###########################################################################
    This Classwill posess all the parameters of the given Sample System. 
    This includes it's thickness and
    
    The folowwing funcitons will be present:
    - __init__() to initialise the class.
        
        The initialisation process will tell the cube these parameters:
        - Parent: To whome does he belong ? 
        - DImensions: What size does it have.
        - Position: Where am I ? (important for computation)
        - Who is illuminating me
    
    ###########################################################################
    """
    def __init__(self, Parent, Position, Dimensions):

        #defien the parent sampel that will contain this cube
        self.Parent = Parent
        self.Verbose = True
        
        #link lens manager
        self.LensManager = Parent.LensManager

        #save the dimensions of this cube
        self.Dimensions = list(Dimensions)

        #compute the surface from this
        self.EffectiveVolume = self.Dimensions[1] * self.Dimensions[2] * self.Dimensions[0]
        
        #Position
        self.Position = list(Position)

        #Was thsi cube computed?
        self.Computed = False

        #for calculation reasons
        self.Intensity = 0.0

        #Does it get collected
        self.CollectedIntensity = 0.0
        self.CheaterCollectedIntensity = 0.0


    def CorrectAbsPosition(self):
        '''
        ##################################################
        Correct the object...
        ##################################################
        '''
        
        #################################################
        #fetch the new position
        
        ####################################
        ####################################
        #grab the Cube variables
        zCube  = self.AbsPosition[0]
        
        ####################################
        ####################################
        #intilise the loop with the Sample
        #Manager. This list will tell the
        #system what is to be considered
        #in the path computation
        
        #set the target
        Target = self.Parent.Parent.SampleLinks
        
        #set the list variable
        ToConsider = [[Target[0],0]]
        
        #loop and add
        for i in range(1,len(Target)):
            
            
            #set the local sample boundaries
            First   = Target[i].ParametersDict['Position']
            Second  = (Target[i].ParametersDict['Position']
                       +Target[i].ParametersDict['Depth'])
        
            #we pass through
            if (    First  < zCube
                and Second < zCube) :

                ToConsider.append([Target[i],0])
            
            #we end in this element
            elif (    First  <  zCube
                  and Second >= zCube) :

                ToConsider.append([Target[i],1])
            
            #this is after
            else:

                pass
    
    
        ######################
        #Get the depth
        
        #grab Z
        Z       = ToConsider[0][0].ParametersDict['Depth']
        Compare = ToConsider[0][0].ParametersDict['Depth']
        self.AbsFactor = 0
    
        ######################
        #get the corrected depth
        #cycle over it all
        for i in range(1,len(ToConsider)):

            if ToConsider[i][1] == 0:
                
                #append the distance
                Dist = ToConsider[i][0].ParametersDict['Depth']* ToConsider[i][0].ProcessCurrentIndex(self.Parent.Parent.LensManager.ParametersDict['LambdaOut']) /ToConsider[i-1][0].ProcessCurrentIndex(self.Parent.Parent.LensManager.ParametersDict['LambdaOut'])
                Z += Dist
                
                #set the value
                Compare += ToConsider[i][0].ParametersDict['Depth']
            
                #if the sample is raman active
                if ToConsider[len(ToConsider)-1-i][0].ParametersDict['Abs']:
                        
                    #absorb
                    self.AbsFactor  += self.Parent.ProcessCurrentAbsorption(self.Parent.Parent.LensManager.ParametersDict['LambdaOut']) * Dist
        
            if ToConsider[i][1] == 1:

                #append the distance
                Z += self.Position[0]* ToConsider[i][0].ProcessCurrentIndex(self.Parent.Parent.LensManager.ParametersDict['LambdaOut'])/ToConsider[i-1][0].ProcessCurrentIndex(self.Parent.Parent.LensManager.ParametersDict['LambdaOut'])
                
                #set the value
                Compare += self.Position[0]


        #send out the distance
        self.AbsPositionCorrected = [-Z,
                                     self.AbsPosition[1],
                                     self.AbsPosition[2]]

    def AddEffectiveIntensityFact(self,Mask):
        '''
        ##################################################
        This routine allows to set a computation surface
        this is reverse engeneing to only compute what 
        actually appsss theough the lens
        ##################################################
        '''
    
        self.MaskFactor = Mask
        self.CollectedIntensity = self.Intensity * Mask[0] * 10**(- self.AbsFactor)
    
    def GrabObject(self, State, Ratio = 0):
        '''
        ##################################################
        In the spirit of a image creation class to calc
        ulate the ray propagation path, this routine will
        express the information of the cube in the right
        format:
        
        Parameters[0] = z
        Parameters[1] = x
        Parameters[2] = y
        Parameters[3] = Angle (x,y)
        Parameters[4] = Angle (applies if z is infinite)
        Parameters[5] = Width (usualy cube height)
        Parameters[6] = Ratio (Solid angle calculation)
        
        ##################################################
        '''
        if State:
        
            return [self.AbsPositionCorrected[0] + Ratio * self.Dimensions[0],
                    self.AbsPositionCorrected[1],
                    self.AbsPositionCorrected[2],
                    0.,
                    0.,
                    self.Dimensions[0],
                    1.]
                
        else:
            return [self.AbsPositionCorrected[0] + Ratio * self.Dimensions[0],
                    - self.AbsPositionCorrected[1],
                    - self.AbsPositionCorrected[2],
                    0.,
                    0.,
                    self.Dimensions[0],
                    1.]

    def AddImage(self, Parameters):
        '''
        ##################################################
        
        ##################################################
        '''
        
    
        self.Images.append(Parameters)

    def ResetImages(self):
        '''
        ##################################################
        
        ##################################################
        '''
        
        try:
        
            del self.Images

        except:

            pass

        self.Images = []



class IntensityManager:

    """
    ###########################################################################
    This class can only be initialised once the SampleManager class has been 
    set. It will the be link to this last one ans the Lens class. This will 
    allow this class to process intnsities once the cubes have been created
    in the samples
    
    The folowwing funcitons will be present:
    - __init__() to initialise the class.
        - Give it the Lens class
        - Give it the sample Manager
    
    - SeedIntensity()
    
        This will Seed the already calculated cubes with the according
        intensities. Note that this will check wheter each sample is Raman
        acitve with the self.Raman == True setup. Wfterwars it will grab the 
        position and extent of each cube and apply the intenstiy mapping.
    
    ###########################################################################
    """

    def __init__(self, LensManager, SampleManager):

        #set the local lens
        self.LensManager = LensManager

        #set the local sample maager link
        self.SampleManager = SampleManager
    
        #log option
        self.Verbose = False


    def RunIllumination(self, FocalPosition = 0.0):
        '''
        ##################################################
        This will calculate the intentsity in a given 
        cube. To do this the following order will be 
        followed. 
        
        - Check if the sample is Raman activated
        - grab the cube list
        - cycle through the cubes by grabing their position
        
        - Inject the intensity
        
        ##################################################
        '''
        #set the focal position local
        self.FocalPosition = self.LensManager.ParametersDict['FocalPosition']
        
        #fix the depth of the lens environnement
        self.LensManager.Environnement.ParametersDict['Depth'] = self.LensManager.ParametersDict['FocalLength'] - self.FocalPosition
        
        #At this stage run the Coordinate routine
        self.SampleManager.Coordinates()
    
        #intilise the loop with the Sample Manager
        Target = self.SampleManager.SampleLinks
    
        #cycle through all samples
        for l in range(len(Target)):
        
            #assign the sample
            Sample = Target[l]
            
            #check if the sample has to be processed
            if Sample.ParametersDict['Illuminated']:
                
                #create a list of previsou samples to be considered in the wais calculations
                for i in range(len(Sample.Cubes)):
            
                    for j in range(len(Sample.Cubes[i])):
                
                        for k in range(len(Sample.Cubes[i][j])):
    
                            self.Gaussian(Sample.Cubes[i][j][k],self.FocalPosition)


                            
    def Gaussian(self,Cube,FocalPosition):
    
        '''
        ##################################################
        This will return the intensity of to the cube
        using the samples it passed through and their 
        indices.
        
        Note that once the wais position ans factor have 
        been processed it will apply the intensity 
        integration for thisexact point by integrating the
        photon function over the path length with changing
        z only.
        ##################################################
        '''
    
    
        if not Cube.Parent.ParametersDict['Integration']:
        

            Cube.Intensity = self.ComputeNormal(Cube,FocalPosition)

        else:
            
            Cube.Intensity = integrate.quad(lambda Ratio: self.ComputeIntegration(Cube,FocalPosition, Ratio), 0., 1.)[0]
    
        #set the logical variable
        Cube.Computed = True
        

    def ComputeNormal(self,Cube,FocalPosition):
        '''
        ##################################################
        This will return the intensity of to the cube
        using the samples it passed through and their 
        indices.
        
        Note that once the wais position ans factor have 
        been processed it will apply the intensity 
        integration for thisexact point by integrating the
        photon function over the path length with changing
        z only.
        ##################################################
        '''
        
    
        ##############################
        ##############################
        #Compute the intensity
        
        #grab the waist
        self.Waist_z = self.Waist(Cube.AbsPosition[0],
                                  FocalPosition,
                                  Cube)
        
        #Caluclate the intensity
        Intensity = (self.LensManager.ParametersDict['Intensity']
                          *(self.LensManager.ParametersDict['Waist']
                            /self.Waist_z)**2
                          *math.exp(-(2.*(Cube.AbsPosition[1]**2+Cube.AbsPosition[2]**2))
                                    /(self.Waist_z**2)))
        
        ##############################
        ##############################
        #Compute the path length
        Intensity = Intensity*10.**(-self.GetIlluminationAbsorption(Cube))
    
        ##############################
        ##############################
        #grab the spectral intensity...
        
        #check if an intensity profile has been loaded
        if Cube.Parent.ParametersDict['RamanProfileLoaded']:
        
            #ask the sample manager to process the factor
            SpectralFactor = Cube.Parent.ProcessRamanIntensityFactor(self.LensManager.ParametersDict['LambdaIn'],
                                                                self.LensManager.ParametersDict['LambdaOut'])
        
            #proces the factor
            Intensity *= SpectralFactor
        
        #send it out
        return Intensity
    
    def ComputeIntegration(self,Cube,FocalPosition,Ratio):
        '''
        ##################################################
        This will return the intensity of to the cube
        using the samples it passed through and their 
        indices.
        
        Note that once the wais position ans factor have 
        been processed it will apply the intensity 
        integration for thisexact point by integrating the
        photon function over the path length with changing
        z only.
        ##################################################
        '''
        
        #set the logical variable
        Cube.Computed = True
    
    
        ##############################
        ##############################
        #Compute the intensity
        
        #grab the waist
        self.Waist_z = self.Waist(Cube.AbsPosition[0]+Ratio*Cube.Dimensions[0],
                                  FocalPosition,
                                  Cube)
        
        #Caluclate the intensity
        Intensity = (self.LensManager.ParametersDict['Intensity']
                          *(self.LensManager.ParametersDict['Waist']
                            /self.Waist_z)**2
                          *math.exp(-(2.*(Cube.AbsPosition[1]**2+Cube.AbsPosition[2]**2))
                                    /(self.Waist_z**2)))
        
        ##############################
        ##############################
        #Compute the path length
        Intensity = Intensity * 10.**(-self.GetIlluminationAbsorption(Cube,Ratio))
    
        ##############################
        ##############################
        #grab the spectral intensity...
        
        #check if an intensity profile has been loaded
        if Cube.Parent.ParametersDict['RamanProfileLoaded']:
        
            #ask the sample manager to process the factor
            SpectralFactor = Cube.Parent.ProcessRamanIntensityFactor(self.LensManager.ParametersDict['LambdaIn'],
                                                                self.LensManager.ParametersDict['LambdaOut'])
        
            #proces the factor
            Intensity *= SpectralFactor
        
        #send it out
        
        return Intensity
    
    def Waist(self,z,FocalPosition,Cube):
        '''
        ##################################################
        This function aims to compute the waist over z
        and over Delta.
        
        The offset will be needed further to calculate
        the absorption and is therefore saved into the
        cube itself. (just to be sure it is avaibale)
        ##################################################
        '''
        
        #get the offset of the focus
        if z < 0:
        
            Offset = 0.0
            Z = z
        
        else:
        
            FocalPosition,Z = self.GetOffset(z, FocalPosition)
        
        if self.Verbose:
            print 'This was z: ', z
            print 'This is the calculated Offset: ',Offset
            print 'This was the focal position:',FocalPosition

        #save into the sample the waist position
        Cube.Parent.ParametersDict['NewWaistPos'] = float(FocalPosition)
        
        #get the waist
        Waist = (self.LensManager.ParametersDict['Waist']
                 *math.sqrt(1.+((Z - Cube.Parent.ParametersDict['NewWaistPos'])
                                *self.LensManager.ParametersDict['LambdaIn']
                                *self.LensManager.ParametersDict['MSquare']
                                /(self.LensManager.ParametersDict['Waist']**2
                                  *numpy.pi)
                                )**2))
        
        return Waist

    def GetOffset(self,z, FocalPosition):
        '''
        ##################################################
        This function aims to compute the offset induced 
        by the previous layers
        
        we don't consider the first one as it is considered
        the starting medium and thereofre the lens should
        be in th emedium
        ##################################################
        '''
        
        ####################################
        ####################################
        #intilise th eloop with the Sample Manager
        Target = self.SampleManager.SampleLinks
        
        #set the list variable
        ToConsider = [[Target[0],0]]
        
        #loop and add
        for i in range(1,len(Target)):
            
            ################
            #we pass through
            if Target[i].ParametersDict['Position'] < z and Target[i].ParametersDict['Position']+Target[i].ParametersDict['Depth'] <= z :

                ToConsider.append([Target[i],0])
            
            ################
            #we end in this element
            elif Target[i].ParametersDict['Position'] <= z and Target[i].ParametersDict['Position']+Target[i].ParametersDict['Depth'] > z:

                ToConsider.append([Target[i],1])
            
            ################
            #this is after
            else:

                pass
                    
        
        ####################################
        ####################################
        #Apply the correction of the focal distance...
        Offset  = 0.
        Z       = 0.
        

        if len(ToConsider) == 1:
        
            pass
        
        else:
            
            #cycle over it all
            for i in range(1,len(ToConsider)):

                if ToConsider[i][1] == 0:

                    #correct the actual focal position
                    Offset += ((1.-ToConsider[i][0].ParametersDict['Index']/ToConsider[i-1][0].ParametersDict['Index'])
                               * Target[i].ParametersDict['Depth'])
                if ToConsider[i][1] == 1:
                    
                    #correct the actual focal position
                    Offset += ((1.-ToConsider[i][0].ParametersDict['Index']/ToConsider[i-1][0].ParametersDict['Index'])
                               * (z - Target[i].ParametersDict['Position']))
    
        #process
        FocalPosition = FocalPosition + Offset
        
        #send it out
        return FocalPosition,z

    def GetIlluminationAbsorption(self,Cube, Ratio = 0):
        '''
        ##################################################
        This function aims to compute the offset induced 
        by the previous layers
        
        we don't consider the first one as it is considered
        the starting medium and thereofre the lens should
        be in th emedium
        ##################################################
        '''
        
        ####################################
        ####################################
        #grab the variables
        z = Cube.AbsPosition[0]+Ratio*Cube.Dimensions[0]
        r = math.sqrt(Cube.AbsPosition[1]**2 + Cube.AbsPosition[2]**2)
        R = math.sqrt(r**2 + (Cube.Parent.ParametersDict['NewWaistPos'] - z)**2)
        
        ####################################
        ####################################
        #intilise the loop with the Sample
        #Manager. This list will tell the
        #system what is to be considered
        #in the path computation
        
        #set the target
        Target = self.SampleManager.SampleLinks
        
        #set the list variable
        ToConsider = []
        
        #loop and add
        for i in range(1,len(Target)):
            
            #we pass through
            if Target[i].ParametersDict['Position'] < z and Target[i].ParametersDict['Position']+Target[i].ParametersDict['Depth'] < z :

                ToConsider.append([Target[i],0])
            
            #we end in this element
            elif Target[i].ParametersDict['Position'] < z and Target[i].ParametersDict['Position']+Target[i].ParametersDict['Depth'] >= z:

                ToConsider.append([Target[i],1])
            
            #this is after
            else:

                pass
                    
        ####################################
        ####################################
        #initialise the offset
        Absorption  = 0.0
        Dist        = 0.0
        Angle       = 0.0

        #if we have no Absorption
        if len(ToConsider) == 0:
        
            #pass it
            pass
        
        #if we have absorption
        else:
        
            #cycle over it all
            for i in range(0,len(ToConsider)):
                
                #We start by the first noamly that has 1
                if ToConsider[len(ToConsider)-1-i][1] == 1:
                
                    #get the actual focal position
                    WaistPosition = Cube.Parent.ParametersDict['NewWaistPos']
                
                    #get the angle
                    if r == 0:
                        
                        Angle = 0.0
                    
                    else:
                        
                        Angle = R * (1. + ((math.pi * self.LensManager.ParametersDict['Waist']**2)
                                          /(self.LensManager.ParametersDict['LambdaIn'] * R))**2
                                     )
                
                    #Distance Traveled
                    Dist = Cube.Position[0] / math.cos(Angle)
                    
                    #if the sample is raman active
                    if ToConsider[len(ToConsider)-1-i][0].ParametersDict['Abs']:
                        
                        #absorb
                        Absorption += Cube.Parent.ProcessCurrentAbsorption(self.LensManager.ParametersDict['LambdaIn']) * Dist
            
            
                #we stop by the last which should be a 0
                if ToConsider[len(ToConsider)-1-i][1] == 0:
                    
                    #get the new angle
                    Angle = numpy.abs(math.asin( math.sin( Angle )
                                                * ToConsider[len(ToConsider)-i][0].ParametersDict['Index']
                                                / ToConsider[len(ToConsider)-1-i][0].ParametersDict['Index']))
                                 
                    #Distance Traveled
                    Dist = ToConsider[len(ToConsider)-1-i][0].ParametersDict['Depth'] / math.cos(Angle)
                
                
                    
                    #if the sample is raman active
                    if ToConsider[len(ToConsider)-1-i][0].ParametersDict['Abs']:
                        
                        #absorb
                        Absorption += ToConsider[len(ToConsider)-1-i][0].ProcessCurrentAbsorption(self.LensManager.ParametersDict['LambdaIn']) * Dist
        
        return Absorption

class Manager:

    """
    ###########################################################################
    To avoid having to many floating items a manager is called. This one will
    keep all links in one place and make sure everything is accessible thtough
    him. This willl ensure a better cohesion and easier management for further
    calls.
    ###########################################################################
    """

    def __init__(self):

        #set verbose
        self.Verbose = False
        
        #create the smpleManager
        self.SampleManager = SampleManager()
        
        #create the lens
        self.LensManager = LensManager()
        
        #link the lens environnement
        self.LensManager.LinkToEnvironnment(self.SampleManager.SampleLinks[0])
        
        self.SampleManager.LinkToEnvironnment(self.LensManager)
        
        #call the intensity manager
        self.IntensityManager = IntensityManager(self.LensManager, self.SampleManager)


    def SetSamples(self, Num):
        """
        ###########################################################################
        This routine will generate the samples recquired in the simultion
        ###########################################################################
        """
        
        #load default parameetrs
        Parameters = {}
        Parameters['ZSteps'] = 1000  #defines the amount of cubes in Z
        Parameters['XSteps'] = 01    #defines the amount of cubes in X
        Parameters['YSteps'] = 01    #defines the amount of cubes in Y
        Parameters['XDim']   = 1.e-6 #defines the dimension of the cube
        Parameters['YDim']   = 1.e-6 #defines the dimension of the cube
        
        #delete preexisting samples
        self.SampleManager.DeleteAll()
    
        #send out the creation information
        self.SampleManager.AddSamples(Num, Parameters)
    

    def DefaultRunIllumination(self):
        """
        ###########################################################################
        This is the default run algorythm and will just run through the following
        script. Note that if the properties are manged externaly, the self.Run()
        function has to be used to avoid overwriting of the parameters.
        ###########################################################################
        """


        Parameters = {}
        
        Parameters['ZSteps'] = 100  #defines the amount of cubes in Z
        Parameters['XSteps'] = 1  #defines the amount of cubes in X
        Parameters['YSteps'] = 01   #defines the amount of cubes in Y
        
        Parameters['ZDim'] = 2.e-6 #defines the dimension of the cube
        Parameters['XDim'] = 1.e-6  #defines the dimension of the cube
        Parameters['YDim'] = 1.e-6  #defines the dimension of the cube
        
        #modify the samples throught the manager
        self.SampleManager.ChangeParameter(0, 'Illuminated',True)
        self.SampleManager.CreateCubes(0, Parameters)
        
        Parameters = {}
        Parameters['ZSteps'] = 1000  #defines the amount of cubes in Z
        Parameters['XSteps'] = 01    #defines the amount of cubes in X
        Parameters['YSteps'] = 01    #defines the amount of cubes in Y
        Parameters['XDim']   = 1.e-6 #defines the dimension of the cube
        Parameters['YDim']   = 1.e-6 #defines the dimension of the cube
        
        #modify the samples throught the manager
        self.SampleManager.ChangeParameter(1, 'Raman',True)
        self.SampleManager.ChangeParameter(1, 'Illuminated',True)
        self.SampleManager.ChangeParameter(1, 'Depth',float(100.e-6))
        self.SampleManager.ChangeParameter(1, 'Absorption',10000.0)
        self.SampleManager.ChangeParameter(1, 'Abs',True)
        self.SampleManager.ChangeParameter(1, 'Index',1.5)
        self.SampleManager.ChangeParameter(1, 'Integration',True)
        self.SampleManager.CreateCubes(1, Parameters)
        

    def RunIllumination(self):
        """
        ###########################################################################
        Assumes that all the processign has been done before hand. including the 
        creation of cubes...
        ###########################################################################
        """
        
        self.SampleManager.CreateCubes(0)
        self.SampleManager.CreateCubes(1)
        #self.SampleManager.CreateCubes(2)
        
        self.IntensityManager.RunIllumination()
        
        #print it
        if self.Verbose:
            print self.LensManager
            print self.SampleManager


    def CreatePlotableIllumination(self):
        """
        ###########################################################################
        This function will handle the set samples and cube creations to send this 
        to drop the arrays for plotting. This means that the creation of X Y and
        Z will be supervised here.
        ###########################################################################
        """
        
        #create a list of length
        LengthList = [[len(self.SampleManager.SampleLinks[i].Cubes) for i in range(len(self.SampleManager.SampleLinks))],
                      [len(self.SampleManager.SampleLinks[i].Cubes[0]) for i in range(len(self.SampleManager.SampleLinks))]]

        #grab the cube dimentionality in each direciton
        self.Z = numpy.zeros((sum(LengthList[0]),LengthList[1][0]*2-1))
        self.X = numpy.zeros((sum(LengthList[0]),LengthList[1][0]*2-1))
        self.I = numpy.zeros((sum(LengthList[0]),LengthList[1][0]*2-1))
        
        #iterations paramters
        o = 0
        OffsetIndex = []
        
        #create quick offset index list
        for i in range(len(LengthList[0])):
            
            #append te value
            OffsetIndex.append(o)
        
            #change the offset
            o += LengthList[0][i]
        
        #create the Y list:
        YList = [-LengthList[1][0]+1+i for i in range(LengthList[1][0]*2-1)]
        
        #loop over the samples
        for i in range(len(LengthList[0])):
            
            #loop over z
            for k in range(LengthList[0][i]):
                
                #loop over X
                for l in range(LengthList[1][0]*2-1):
                    
                    if YList[l] > 0:
                    
                        self.Z[k+OffsetIndex[i]][l] = self.SampleManager.SampleLinks[i].Cubes[k][YList[l]][0].AbsPosition[0]
                        self.X[k+OffsetIndex[i]][l] = self.SampleManager.SampleLinks[i].Cubes[k][YList[l]][0].AbsPosition[1]
                        self.I[k+OffsetIndex[i]][l] = self.SampleManager.SampleLinks[i].Cubes[k][YList[l]][0].Intensity
                    
                    else:
                    
                        self.Z[k+OffsetIndex[i]][l] = self.SampleManager.SampleLinks[i].Cubes[k][l][0].AbsPosition[0]
                        self.X[k+OffsetIndex[i]][l] = - self.SampleManager.SampleLinks[i].Cubes[k][-YList[l]][0].AbsPosition[1]
                        self.I[k+OffsetIndex[i]][l] = self.SampleManager.SampleLinks[i].Cubes[k][-YList[l]][0].Intensity



    def CreatePlotableCollection(self):
        """
        ###########################################################################
        This function will handle the set samples and cube creations to send this 
        to drop the arrays for plotting. This means that the creation of X Y and
        Z will be supervised here.
        ###########################################################################
        """
                
        #create a list of length
        LengthList = [[len(self.SampleManager.SampleLinks[i].Cubes) for i in range(1,len(self.SampleManager.SampleLinks))],
                      [len(self.SampleManager.SampleLinks[i].Cubes[0]) for i in range(1,len(self.SampleManager.SampleLinks))]]

        #grab the cube dimentionality in each direciton
        self.Z = numpy.zeros((sum(LengthList[0]),LengthList[1][0]*2-1))
        self.X = numpy.zeros((sum(LengthList[0]),LengthList[1][0]*2-1))
        self.I = numpy.zeros((sum(LengthList[0]),LengthList[1][0]*2-1))
        
        #iterations paramters
        o = 0
        OffsetIndex = []
        
        #create quick offset index list
        for i in range(len(LengthList[0])):
            
            #append te value
            OffsetIndex.append(o)
        
            #change the offset
            o += LengthList[0][i]
        
        #create the Y list:
        YList = [-LengthList[1][0]+1+i for i in range(LengthList[1][0]*2-1)]
        
        #loop over the samples
        for i in range(len(LengthList[0])):
            
            #loop over z
            for k in range(LengthList[0][i]):
                
                #loop over X
                for l in range(LengthList[1][0]*2-1):
                    
                    if YList[l] > 0:
                    
                        self.Z[k+OffsetIndex[i]][l] = self.SampleManager.SampleLinks[i + 1].Cubes[k][YList[l]][0].AbsPosition[0]
                        self.X[k+OffsetIndex[i]][l] = self.SampleManager.SampleLinks[i + 1].Cubes[k][YList[l]][0].AbsPosition[1]
                        try:
                            self.I[k+OffsetIndex[i]][l] = (self.SampleManager.SampleLinks[i + 1].Cubes[k][YList[l]][0].CollectedIntensity)
                        except:
                            self.I[k+OffsetIndex[i]][l] = .0
                    else:
                        
                        self.Z[k+OffsetIndex[i]][l] = self.SampleManager.SampleLinks[i + 1].Cubes[k][l][0].AbsPosition[0]
                        self.X[k+OffsetIndex[i]][l] = - self.SampleManager.SampleLinks[i + 1].Cubes[k][-YList[l]][0].AbsPosition[1]
                        try:
                            self.I[k+OffsetIndex[i]][l] = (self.SampleManager.SampleLinks[i + 1].Cubes[k][-YList[l]][0].CollectedIntensity)
                        except:
                            self.I[k+OffsetIndex[i]][l] = .0


"""
###########################################################################
This script was generated using the script generator of R-Data. It can run
independently of R-Data if the datasctructure is intact...
###########################################################################
"""


def Main():
    
    ################################
    ################################
    #Proceed to general imports
    #import multiprocessing
    ################################
    ################################
    #Proceed to loading imports
    LocalManager = Manager()
    
    
    #--LOADHEADER--
    
    ################################
    ################################
    #Set the number of Samples
    LocalManager.SetSamples(2)
    
    ################################
    ################################
    #Set the Sample parameters
    
    #Sample: 0
    LocalManager.SampleManager.ChangeParameter(0,'Name','Air')
    LocalManager.SampleManager.ChangeParameter(0,'Index',1.0)
    LocalManager.SampleManager.ChangeParameter(0,'Abs',False)
    LocalManager.SampleManager.ChangeParameter(0,'Absorption',0.0)
    LocalManager.SampleManager.ChangeParameter(0,'Raman',False)
    LocalManager.SampleManager.ChangeParameter(0,'ZSteps',1000)
    LocalManager.SampleManager.ChangeParameter(0,'XSteps',1)
    LocalManager.SampleManager.ChangeParameter(0,'Depth',1e-06)
    LocalManager.SampleManager.ChangeParameter(0,'XDim',1e-06)
    LocalManager.SampleManager.ChangeParameter(0,'Integration',False)
    LocalManager.SampleManager.ChangeParameter(0,'RamanProfileLoaded',False)
    LocalManager.SampleManager.ChangeParameter(0,'RamanProfilePath','')
    LocalManager.SampleManager.ChangeParameter(0,'IndexProfileLoaded',False)
    LocalManager.SampleManager.ChangeParameter(0,'IndexProfilePath','')
    LocalManager.SampleManager.ChangeParameter(0,'AbsorptionProfileLoaded',False)
    LocalManager.SampleManager.ChangeParameter(0,'AbsorptionProfilePath','')
    
    #Sample: 1
    LocalManager.SampleManager.ChangeParameter(1,'Name','BiVO4')
    LocalManager.SampleManager.ChangeParameter(1,'Index',1.0)
    LocalManager.SampleManager.ChangeParameter(1,'Abs',True)
    LocalManager.SampleManager.ChangeParameter(1,'Absorption',0.0)
    LocalManager.SampleManager.ChangeParameter(1,'Raman',True)
    LocalManager.SampleManager.ChangeParameter(1,'ZSteps',1000)
    LocalManager.SampleManager.ChangeParameter(1,'XSteps',1)
    LocalManager.SampleManager.ChangeParameter(1,'Depth',0.0001)
    LocalManager.SampleManager.ChangeParameter(1,'XDim',1e-06)
    LocalManager.SampleManager.ChangeParameter(1,'Integration',True)
    LocalManager.SampleManager.ChangeParameter(1,'RamanProfileLoaded',True)
    LocalManager.SampleManager.ChangeParameter(1,'RamanProfilePath','D:/Dropbox/Dropbox/Data/G - Reports/2017 - Projects/2017_06_19 - Depth Absorption Simulations/Simulated Spectra/BiVO4/Definitions/Raman_File_1.txt')
    LocalManager.SampleManager.ChangeParameter(1,'IndexProfileLoaded',True)
    LocalManager.SampleManager.ChangeParameter(1,'IndexProfilePath','D:/Dropbox/Dropbox/Data/G - Reports/2017 - Projects/2017_06_19 - Depth Absorption Simulations/Simulated Spectra/BiVO4/Definitions/Index_1.txt')
    LocalManager.SampleManager.ChangeParameter(1,'AbsorptionProfileLoaded',True)
    LocalManager.SampleManager.ChangeParameter(1,'AbsorptionProfilePath','D:/Dropbox/Dropbox/Data/G - Reports/2017 - Projects/2017_06_19 - Depth Absorption Simulations/Simulated Spectra/BiVO4/Definitions/Absorption_1.txt')
    
    ################################
    ################################
    #Set the Lens parameters
    LocalManager.LensManager.ChangeParameter('FocalPosition',0.0)
    LocalManager.LensManager.ChangeParameter('LambdaIn',4.4e-07)
    LocalManager.LensManager.ChangeParameter('LambdaOut',7e-07)
    LocalManager.LensManager.ChangeParameter('Waist',3.5e-07)
    LocalManager.LensManager.ChangeParameter('Intensity',1e+15)
    
    #LensElement: 0
    LocalManager.LensManager.LensElements[0].ChangeParameter('FocalLength',0.00025)
    LocalManager.LensManager.LensElements[0].ChangeParameter('LensRadius',0.00075)
    LocalManager.LensManager.LensElements[0].ChangeParameter('Position',0.0)
    
    #LensElement: 1
    LocalManager.LensManager.LensElements[1].ChangeParameter('FocalLength',0.07)
    LocalManager.LensManager.LensElements[1].ChangeParameter('LensRadius',0.0085)
    LocalManager.LensManager.LensElements[1].ChangeParameter('Position',0.58)
    
    #LensElement: 2
    LocalManager.LensManager.LensElements[2].ChangeParameter('Parameters',100.0)
    LocalManager.LensManager.LensElements[2].ChangeParameter('Position',0.65)
    
    #--LOADHEADER--
    
    
    ################################
    ################################
    #Proceed to File Loading
    for i in range(0, len(LocalManager.SampleManager.SampleLinks)):
        
        #check if there is a profile to load
        if LocalManager.SampleManager.SampleLinks[i].ParametersDict['RamanProfileLoaded']:
            
            #Load the profile
            LocalManager.SampleManager.SampleLinks[i].LoadRamanResponseProfile()
            
        
        #check if there is a profile to load
        if LocalManager.SampleManager.SampleLinks[i].ParametersDict['IndexProfileLoaded']:
            
            #Load the profile
            LocalManager.SampleManager.SampleLinks[i].LoadIndexResponseProfile()
            
        
        #check if there is a profile to load
        if LocalManager.SampleManager.SampleLinks[i].ParametersDict['AbsorptionProfileLoaded']:
            
            #Load the profile
            LocalManager.SampleManager.SampleLinks[i].LoadAbsorptionResponseProfile()
            
    
    
    ################################
    ################################
    #Proceed to general printouts
    print LocalManager.LensManager.LensElements[0]
    print LocalManager.LensManager.LensElements[1]
    print LocalManager.LensManager.LensElements[2]
    print LocalManager.SampleManager


    #--PROCESS PARAMETERS--
    Compute    = [False,True,True]
    Targets    = [None,LocalManager.LensManager,LocalManager.LensManager]
    Parameter  = ['None','Focal position->FocalPosition','Outgoing Wavelength->LambdaOut']
    Ranges     = [['','',1],[-1e-5,1e-5,100],[4.41944e-7,4.60251e-7,400]]
    TargetSelector_0 = ['Void','Lens Manager','Lens Manager']
    TargetSelector_1 = ['','General Lens','General Lens']
    TargetSelector_2 = ['','Focal position->FocalPosition','Outgoing Wavelength->LambdaOut']
    BasePath   = 'D:/Dropbox/Dropbox/Data/G - Reports/2017 - Projects/2017_06_19 - Depth Absorption Simulations/Simulated Spectra/BiVO4/Data 440nm/NewData'
    Processors = 8
    WhoMulti   = 1
    Fold       = 1
    #--PROCESS PARAMETERS--
    
    ################################
    ################################
    #Write path
    Path = 'OUTPUT_30__FocalPosition__X-1-X__LambdaOut__X-2-X.txt'
    
    Parameters = [Compute, Targets, Parameter, Ranges, [ProcessLoop_1,ProcessLoop_2,ProcessLoop_3], Path, BasePath, Processors, WhoMulti, Fold,LocalManager]
    LocalManager.SampleManager.CreateCubes()
    
    ################################
    ################################
    #The dependencies should build themeselves
    Parameters[4][0](Parameters, 0)
"""
###########################################################################
This script was generated using the script generator of R-Data. It can run
independently of R-Data if the datasctructure is intact...
###########################################################################
"""
def ProcessLoop_1(Parameters, Index, Multi = False):
    ################################
    ################################
    #unpack the variables
    Compute        = list(Parameters[0])
    Targets        = list(Parameters[1])
    Parameter      = list(Parameters[2])
    Ranges         = list(Parameters[3])
    TargetRoutine  = list(Parameters[4])
    Path           = str(Parameters[5])
    BasePath       = str(Parameters[6])
    Processors     = int(Parameters[7])
    WhoisMulti     = int(Parameters[8])
    Fold           = Parameters[9]
    LocalManager   = Parameters[10]
        
    ################################
    ################################
    #First variable loop
    for i in range(0,Ranges[Index][2]):
        
        if Compute[Index]:
            
            Targets[Index].ChangeParameter(Parameter[Index].split('->')[1], Ranges[Index][0]+((Ranges[Index][1] - Ranges[Index][0])/Ranges[Index][2] * i))
            
        else:
            
            pass
        
        #Run the next routine
        TargetRoutine[Index + 1](Parameters, Index + 1)
"""
###########################################################################
This script was generated using the script generator of R-Data. It can run
independently of R-Data if the datasctructure is intact...
###########################################################################
"""
def ProcessLoop_2(Parameters, Index, Multi = False):
    ################################
    ################################
    #unpack the variables
    Compute        = list(Parameters[0])
    Targets        = list(Parameters[1])
    Parameter      = list(Parameters[2])
    Ranges         = list(Parameters[3])
    TargetRoutine  = list(Parameters[4])
    Path           = str(Parameters[5])
    BasePath       = str(Parameters[6])
    Processors     = int(Parameters[7])
    WhoisMulti     = int(Parameters[8])
    Fold           = Parameters[9]
    LocalManager   = Parameters[10]
        
    ################################
    ################################
    #Second variable loop
    
    #Multi processor
    if WhoisMulti == 1 and Processors > 1:
        
        #Set the multiprocessing queue
        output = multiprocessing.Manager().Queue()
        
        #Set the multiprocessing Loop
        i = 0
        while i <  Ranges[Index][2]:
            
            #Set the multiprocessing Array
            Processes = []
            
            #Set overshoot condition
            if i + Processors > Ranges[Index][2]:
                
                #Append processe
                for k in range(i, Ranges[Index][2]):
                    
                    if Compute[Index]:
                        
                        #change the value
                        Targets[Index].ChangeParameter(Parameter[Index].split('->')[1], Ranges[Index][0]+((Ranges[Index][1] - Ranges[Index][0])/Ranges[Index][2] * i))
                        #set the processor
                        Processes.append(multiprocessing.Process(target=TargetRoutine[Index + 1],args=(Parameters, Index + 1, True, output)))
                        Processes[-1].start()
                        i += 1
            
            #Set normal condition
            else:
                
                #Append processe
                for k in range(i, i + Processors):
                    
                    if Compute[Index]:
                        
                        #change the value
                        Targets[Index].ChangeParameter(Parameter[Index].split('->')[1], Ranges[Index][0]+((Ranges[Index][1] - Ranges[Index][0])/Ranges[Index][2] * i))
                        #set the processor
                        Processes.append(multiprocessing.Process(target=TargetRoutine[Index + 1],args=(Parameters, Index + 1, True, output)))
                        Processes[-1].start()
                        i += 1
            
            #Set joining loop
            for p in Processes:
                
                #join processes
                p.join()
            
            #grab output
            OutArray = [output.get() for p in Processes] 
            
            #Write loop
            for t in range(0,len(OutArray)):
                
                #proceed to the routine
                Array = OutArray[t][0]
                
                #Path processing
                NewPath = str(Path)
                
                if Compute[0]:
                    
                    NewPath = NewPath.replace('X-0-X',str(Targets[0].ParametersDict[Parameter[0].split('->')[1]]))
                    
                    
                if Compute[1]:
                    
                    NewPath = NewPath.replace('X-1-X',str(OutArray[t][1]))
                
                ################################
                #Save it
                numpy.savetxt(os.path.join(BasePath,NewPath),Array)
                
                
    #Single processor
    else:
        for i in range(0,Ranges[Index][2]):
            
            if Compute[Index]:
                
                Targets[Index].ChangeParameter(Parameter[Index].split('->')[1], Ranges[Index][0]+((Ranges[Index][1] - Ranges[Index][0])/Ranges[Index][2] * i))
                
            else:
                
                pass
                
        #Run the next routine
        Array = TargetRoutine[Index + 1](Parameters, Index + 1)
        
    ################################
    #Path processing
    NewPath = str(Path)
    
    if Compute[0]:
        
        NewPath = NewPath.replace('X-0-X',str(Targets[0].ParametersDict[Parameter[0].split('->')[1]]))
    
    
    if Compute[1]:
        
        NewPath = NewPath.replace('X-1-X',str(Targets[1].ParametersDict[Parameter[1].split('->')[1]]))
    
    ################################
    #Save it
    numpy.savetxt(os.path.join(BasePath,NewPath),Array)
    
    
"""
###########################################################################
This script was generated using the script generator of R-Data. It can run
independently of R-Data if the datasctructure is intact...
###########################################################################
"""
def ProcessLoop_3(Parameters, Index, Multi = False, Queue = None):
    ################################
    ################################
    #unpack the variables
    Compute        = list(Parameters[0])
    Targets        = list(Parameters[1])
    Parameter      = list(Parameters[2])
    Ranges         = list(Parameters[3])
    TargetRoutine  = list(Parameters[4])
    Path           = str(Parameters[5])
    BasePath       = str(Parameters[6])
    Processors     = int(Parameters[7])
    WhoisMulti     = int(Parameters[8])
    Fold           = Parameters[9]
    LocalManager   = Parameters[10]
        
    ################################
    ################################
    #Third variable loop
    
    #set the variable
    if Fold == 1:
        Array = numpy.zeros((Ranges[Index][2],2))
        
    else:
        Array = numpy.zeros((Ranges[Index][2],len(LocalManager.SampleManager.SampleLinks) + 1))
        
    for k in range(0,Ranges[Index][2]):
    
        ################################
        #Process simulation
        Targets[Index].ChangeParameter(Parameter[Index].split('->')[1], Ranges[Index][0]+((Ranges[Index][1] - Ranges[Index][0])/Ranges[Index][2] * k))
        LocalManager.RunIllumination()
        LocalManager.SampleManager.CorrectCubes()
        LocalManager.SampleManager.ResetCollectionIntensities()
        LocalManager.SampleManager.CollectedIntensity()
        
        ################################
        #Process Output
        if Parameter[2].split('->')[1] == 'LambdaOut':
            
            Array[k][0]  = (  1. / (LocalManager.LensManager.ParametersDict['LambdaIn'] *100.)-1. / (LocalManager.LensManager.ParametersDict['LambdaOut'] *100.)) 
            
        else:
            
            Array[k][0]  = Targets[2].ParametersDict[Parameter[2].split('->')[1]]
            
        ################################
        #Process Intensities
        for Intensity in LocalManager.SampleManager.Intensity:
            
            if Fold == 1:
                Array[k][1] += Intensity
                
            else:
                for ii in range(0, len(LocalManager.SampleManager.SampleLinks)):
                    Array[k][ii + 1] = Intensity[ii]
                    
        ################################
        #Process some verbose
        print '######################################################'
        print '######################################################'
        print 'Current Depth: ',LocalManager.LensManager.ParametersDict['FocalPosition'],' m'
        print 'Current Wavenumber: ',Array[k][0], ' cm-1'
        print 'Current IntensityFactors: ',LocalManager.SampleManager.RetrieveFact()
        print 'Current Intensity: ',LocalManager.SampleManager.Intensity
        
    #if we are multi process:
    if Multi:
        Queue.put([Array,Targets[Index].ParametersDict[Parameter[Index-1].split('->')[1]] ])
        
    else:
        return Array





if __name__ == "__main__":
    Main()


