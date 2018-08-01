# -*- coding: utf-8 -*-
#-INFO-
#-Name-SimplePlot_Ext-
#-Version-0.1.0-
#-Date-15_January_2016-
#-Author-Alexander_Schober-
#-INFO-

#import basic libraris
import numpy
import math


#c implementation
import ContourCalculations as CCalc


'''
######################################################
################Simple Plot Method####################
######################################################

'''


def RunInJ(i,Type,X,Y,Z,Range,MeshRange,Iterations,Output = None):
    '''
    ######################################################
    run onver all columns
    ######################################################
    '''
    EndResult = [None]*(Iterations-1)
    
    for j in range(Iterations-1):

        #run it
        Result = StartObjectScan(i,j,Type,X,Y,Z,Range,MeshRange)
        
        EndResult[j]= Result

    Output.append(EndResult)


def SinglePointCalc(Points, Value, i):

    '''
    ######################################################
    Create and calculate Up polygones and return them
    ######################################################
    '''

    return [Points[i][0],
            Points[i][1]]
        
def TwoPointCalc( Points, Value, i,j):

    '''
    ######################################################
    Create and calculate Up polygones and return them
    ######################################################
    '''
    return [Points[i][0]+((Points[j][0]-Points[i][0]))
            *(Value - Points[i][2])/(Points[j][2] - Points[i][2]),
            
            Points[i][1]+((Points[j][1]-Points[i][1]))
            *(Value - Points[i][2])/(Points[j][2] - Points[i][2])]


def StartObjectScanMulti(i,j,Type,X,Y,Z,Range,MeshRange,output):

    '''
    ######################################################
    We changed the mode. It is now much more direct by
    drawing tons of polygones. This avoinds so many pro-
    blems
    
    We have now X and check only three o
    
    
        X --- o
        I \   I
        I   \ I
        o --- o
    ######################################################
    '''
    
    #initialise the 4 points
    Points  = [None]*4
    
    Points[0] =  [float(X[i][j]),
                       float(Y[i][j]),
                       float([i][j])]
                  
    Points[1] =  [float(Data.X[i+1][j]),
                       float(Y[i+1][j]),
                       float(Z[i+1][j])]
                  
    Points[2] =  [float(X[i+1][j+1]),
                       float(Y[i+1][j+1]),
                       float(Z[i+1][j+1])]
                  
    Points[3] =  [float(X[i][j+1]),
                       float(Y[i][j+1]),
                       float(Z[i][j+1])]
    
    
    #get the boundaries
    Min = numpy.min([Points[0][2],Points[1][2],Points[2][2],Points[3][2]])
    Max = numpy.max([Points[0][2],Points[1][2],Points[2][2],Points[3][2]])
    
    if Type == 'Surface':
    
        #initialise Output
        Output = [None]*len(Range)
        
        for l in range(len(Range)):
        
            #set the value
            Value = Range[l]
            
            if Value >= Min and Value <= Max:
            
                #set them locall
                Pointer = [None]*4
                
                Pointer[0] = A = OverVal(Points,Value,0)
                Pointer[1] = B = OverVal(Points,Value,1)
                Pointer[2] = C = OverVal(Points,Value,2)
                Pointer[3] = D = OverVal(Points,Value,3)
                
                #how many
                Sum_1 = 0
                Sum_2 = 0
                
                for k in range(0,4):
                
                    if Pointer[k]:
                
                        Sum_1 += 1
            
                        Sum_2 += 10**k
        
                if Sum_1 == 0:
                    
                    if Output[l-1] == None:
                        
                        Output[l-1] = [Case_4(Points,Value), Points[0][0], Points[0][1]]
                    
                    break
                        
                elif Sum_1 == 4 and l == len(Range)-1:
                    
                    Output[l] = [Case_4(Points,Value), Points[0][0], Points[0][1]]
                
                elif Sum_1 == 1:
                
                    if Sum_2 == 1:
                        
                        Output[l] = [Case_1_a(Points,Value), Points[0][0], Points[0][1]]
                        
                    elif Sum_2 == 10:
                        
                        Output[l] = [Case_1_b(Points,Value), Points[0][0], Points[0][1]]
                    
                    elif Sum_2 == 100:
                        
                        Output[l] = [Case_1_c(Points,Value), Points[0][0], Points[0][1]]
                    
                    elif Sum_2 == 1000:
                        
                        Output[l] = [Case_1_d(Points,Value), Points[0][0], Points[0][1]]
            
                elif Sum_1 == 2:
                
                    if Sum_2 == 11:
                        
                        Output[l] = [Case_2_a(Points,Value), Points[0][0], Points[0][1]]
                        
                    elif Sum_2 == 110:
                        
                        Output[l] = [Case_2_b(Points,Value), Points[0][0], Points[0][1]]
                    
                    elif Sum_2 == 1100:
                        
                        Output[l] = [Case_2_c(Points,Value), Points[0][0], Points[0][1]]
                    
                    elif Sum_2 == 1001:
                        
                        Output[l] = [Case_2_d(Points,Value), Points[0][0], Points[0][1]]

                    elif Sum_2 == 101:
                        
                        Output[l] = [Case_2_e(Points,Value), Points[0][0], Points[0][1]]
                            
                    elif Sum_2 == 1010:
                        
                        Output[l] = [Case_2_f(Points,Value), Points[0][0], Points[0][1]]
                            
                elif Sum_1 == 3:
                
                    if Sum_2 == 1011:
                        
                        Output[l] = [Case_3_a(Points,Value), Points[0][0], Points[0][1]]
                        
                    elif Sum_2 == 111:
                        
                        Output[l] = [Case_3_b(Points,Value), Points[0][0], Points[0][1]]
                    
                    elif Sum_2 == 1110:
                        
                        Output[l] = [Case_3_c(Points,Value), Points[0][0], Points[0][1]]
                    
                    elif Sum_2 == 1101:
                        
                        Output[l] = [Case_3_d(Points,Value), Points[0][0], Points[0][1]]
            
                if not Output[l] == None and Output[l-1] == None  and l > 0:
                    
                    Output[l-1] = [Case_4(Points,Value), Points[0][0], Points[0][1]]
        
    elif Type == 'Mesh':
    
        #initialise Output
        Output = [None]*len(MeshRange)
        
        for l in range(len(MeshRange)):
        
            #set the value
            Value = MeshRange[l]
            
            if Value >= Min and Value <= Max:
            
                #set them locall
                Pointer = [None]*4
                
                Pointer[0] = A = OverVal(Points,Value,0)
                Pointer[1] = B = OverVal(Points,Value,1)
                Pointer[2] = C = OverVal(Points,Value,2)
                Pointer[3] = D = OverVal(Points,Value,3)
                
                
                #how many
                Sum_1 = 0
                Sum_2 = 0
                
                for k in range(0,4):
                
                    if Pointer[k]:
                
                        Sum_1 += 1
            
                        Sum_2 += 10**k
            
                if Sum_1 == 0:
                    
                    if Output[l-1] == None:
                        
                        Output[l-1] = [Case_4_Line(Points,Value), Points[0][0], Points[0][1]]
                    
                    break
                        
                elif Sum_1 == 4 and l == len(Range)-1:
                    
                    Output[l] = [Case_4_Line(Points,Value), Points[0][0], Points[0][1]]
                
                elif Sum_1 == 1:
                
                
                    if Sum_2 == 1:
                        
                        Output[l] = [Case_1_a_Line(Points,Value), Points[0][0], Points[0][1]]
                        
                    elif Sum_2 == 10:
                        
                        Output[l] = [Case_1_b_Line(Points,Value), Points[0][0], Points[0][1]]
                    
                    elif Sum_2 == 100:
                        
                        Output[l] = [Case_1_c_Line(Points,Value), Points[0][0], Points[0][1]]
                    
                    elif Sum_2 == 1000:
                        
                        Output[l] = [Case_1_d_Line(Points,Value), Points[0][0], Points[0][1]]
                elif Sum_1 == 2:
                
                    if Sum_2 == 11:
                        
                        Output[l] = [Case_2_a_Line(Points,Value), Points[0][0], Points[0][1]]
                        
                    elif Sum_2 == 110:
                        
                        Output[l] = [Case_2_b_Line(Points,Value), Points[0][0], Points[0][1]]
                    
                    elif Sum_2 == 1100:
                        
                        Output[l] = [Case_2_c_Line(Points,Value), Points[0][0], Points[0][1]]
                    
                    elif Sum_2 == 1001:
                        
                        Output[l] = [Case_2_d_Line(Points,Value), Points[0][0], Points[0][1]]

                    elif Sum_2 == 101:
                        
                        Output[l] = [Case_2_e_Line(Points,Value), Points[0][0], Points[0][1]]
                
                    elif Sum_2 == 1010:
            
                        Output[l] = [Case_2_f_Line(Points,Value), Points[0][0], Points[0][1]]
            
                elif Sum_1 == 3:
                
                    if Sum_2 == 1011:
                        
                        Output[l] = [Case_3_a_Line(Points,Value), Points[0][0], Points[0][1]]
                        
                    elif Sum_2 == 111:
                        
                        Output[l] = [Case_3_b_Line(Points,Value), Points[0][0], Points[0][1]]
                    
                    elif Sum_2 == 1110:
                        
                        Output[l] = [Case_3_c_Line(Points,Value), Points[0][0], Points[0][1]]
                    
                    elif Sum_2 == 1101:
                        
                        Output[l] = [Case_3_d_Line(Points,Value), Points[0][0], Points[0][1]]
            
                if not Output[l] == None and Output[l-1] == None  and l > 0:
                    
                    Output[l-1] = [Case_4_Line(Points,Value), Points[0][0], Points[0][1]]

    output.put(Output)


def StartObjectScan( i, j,Type, X,Y,Z,Range,MeshRange):

    '''
    ######################################################
    We changed the mode. It is now much more direct by
    drawing tons of polygones. This avoinds so many pro-
    blems
    
    We have now X and check only three o
    
    
        X --- o
        I \   I
        I   \ I
        o --- o
    ######################################################
    '''
    #initialise the 4 points
    Points  = [None]*4
    
    Points[0] =  [float(X[i][j]),
                  float(Y[i][j]),
                  float(Z[i][j])]
                  
    Points[1] =  [float(X[i+1][j]),
                  float(Y[i+1][j]),
                  float(Z[i+1][j])]
                  
    Points[2] =  [float(X[i+1][j+1]),
                  float(Y[i+1][j+1]),
                  float(Z[i+1][j+1])]
                  
    Points[3] =  [float(X[i][j+1]),
                  float(Y[i][j+1]),
                  float(Z[i][j+1])]
    
    
    #get the boundaries
    Min = numpy.min([Points[0][2],Points[1][2],Points[2][2],Points[3][2]])
    Max = numpy.max([Points[0][2],Points[1][2],Points[2][2],Points[3][2]])
    
    if Type == 'Surface':
    
        #initialise Output
        Output = [None]*len(Range)
        
        for l in range(len(Range)):
            
            #set the value
            Value = Range[l]
        
            #set them locall
            Pointer = [None]*4
            
            Pointer[0] = A = OverVal(Points,Value,0)
            Pointer[1] = B = OverVal(Points,Value,1)
            Pointer[2] = C = OverVal(Points,Value,2)
            Pointer[3] = D = OverVal(Points,Value,3)
            
            #how many
            Sum_1 = 0
            Sum_2 = 0
            k     = 0
            
            for P in Pointer:
            
                if P:
            
                    Sum_1 += 1
        
                    Sum_2 += 10**k
                
                k+=1
    
            if Sum_1 == 0:
                
                if Output[l-1] == None:
                    
                    Output[l-1] = [Case_4(Points,Value), Points[0][0], Points[0][1]]
                
                break
                    
            elif Sum_1 == 4 and l == len(Range)-1:
                
                Output[l] = [Case_4(Points,Value), Points[0][0], Points[0][1]]
            
            elif Sum_1 == 1:
            
                if Sum_2 == 1:
                    
                    Output[l] = [Case_1_a(Points,Value), Points[0][0], Points[0][1]]
                    
                elif Sum_2 == 10:
                    
                    Output[l] = [Case_1_b(Points,Value), Points[0][0], Points[0][1]]
                
                elif Sum_2 == 100:
                    
                    Output[l] = [Case_1_c(Points,Value), Points[0][0], Points[0][1]]
                
                elif Sum_2 == 1000:
                    
                    Output[l] = [Case_1_d(Points,Value), Points[0][0], Points[0][1]]
        
            elif Sum_1 == 2:
            
                if Sum_2 == 11:
                    
                    Output[l] = [Case_2_a(Points,Value), Points[0][0], Points[0][1]]
                    
                elif Sum_2 == 110:
                    
                    Output[l] = [Case_2_b(Points,Value), Points[0][0], Points[0][1]]
                
                elif Sum_2 == 1100:
                    
                    Output[l] = [Case_2_c(Points,Value), Points[0][0], Points[0][1]]
                
                elif Sum_2 == 1001:
                    
                    Output[l] = [Case_2_d(Points,Value), Points[0][0], Points[0][1]]

                elif Sum_2 == 101:
                    
                    Output[l] = [Case_2_e(Points,Value), Points[0][0], Points[0][1]]
                        
                elif Sum_2 == 1010:
                    
                    Output[l] = [Case_2_f(Points,Value), Points[0][0], Points[0][1]]
                        
            elif Sum_1 == 3:
            
                if Sum_2 == 1011:
                    
                    Output[l] = [Case_3_a(Points,Value), Points[0][0], Points[0][1]]
                    
                elif Sum_2 == 111:
                    
                    Output[l] = [Case_3_b(Points,Value), Points[0][0], Points[0][1]]
                
                elif Sum_2 == 1110:
                    
                    Output[l] = [Case_3_c(Points,Value), Points[0][0], Points[0][1]]
                
                elif Sum_2 == 1101:
                    
                    Output[l] = [Case_3_d(Points,Value), Points[0][0], Points[0][1]]
        
            if not Output[l] == None and Output[l-1] == None  and l > 0:
                
                Output[l-1] = [Case_4(Points,Value), Points[0][0], Points[0][1]]
    
    elif Type == 'Mesh':
    
        #initialise Output
        Output = [None]*len(MeshRange)
        
        for l in range(len(MeshRange)):
            
            #set the value
            Value = MeshRange[l]
            
            #set them locall
            Pointer = [None]*4
            
            Pointer[0] = A = OverVal(Points,Value,0)
            Pointer[1] = B = OverVal(Points,Value,1)
            Pointer[2] = C = OverVal(Points,Value,2)
            Pointer[3] = D = OverVal(Points,Value,3)
            
            #how many
            Sum_1 = 0
            Sum_2 = 0
            k     = 0
            
            for P in Pointer:
            
                if P:
            
                    Sum_1 += 1
        
                    Sum_2 += 10**k
                
                k+=1
        
            if Sum_1 == 0:
                
                if Output[l-1] == None:
                    
                    Output[l-1] = [Case_4_Line(Points,Value), Points[0][0], Points[0][1]]
                
                break
                    
            elif Sum_1 == 4 and l == len(Range)-1:
                
                Output[l] = [Case_4_Line(Points,Value), Points[0][0], Points[0][1]]
            
            elif Sum_1 == 1:
            
            
                if Sum_2 == 1:
                    
                    Output[l] = [Case_1_a_Line(Points,Value), Points[0][0], Points[0][1]]
                    
                elif Sum_2 == 10:
                    
                    Output[l] = [Case_1_b_Line(Points,Value), Points[0][0], Points[0][1]]
                
                elif Sum_2 == 100:
                    
                    Output[l] = [Case_1_c_Line(Points,Value), Points[0][0], Points[0][1]]
                
                elif Sum_2 == 1000:
                    
                    Output[l] = [Case_1_d_Line(Points,Value), Points[0][0], Points[0][1]]
            elif Sum_1 == 2:
            
                if Sum_2 == 11:
                    
                    Output[l] = [Case_2_a_Line(Points,Value), Points[0][0], Points[0][1]]
                    
                elif Sum_2 == 110:
                    
                    Output[l] = [Case_2_b_Line(Points,Value), Points[0][0], Points[0][1]]
                
                elif Sum_2 == 1100:
                    
                    Output[l] = [Case_2_c_Line(Points,Value), Points[0][0], Points[0][1]]
                
                elif Sum_2 == 1001:
                    
                    Output[l] = [Case_2_d_Line(Points,Value), Points[0][0], Points[0][1]]

                elif Sum_2 == 101:
                    
                    Output[l] = [Case_2_e_Line(Points,Value), Points[0][0], Points[0][1]]
            
                elif Sum_2 == 1010:
        
                    Output[l] = [Case_2_f_Line(Points,Value), Points[0][0], Points[0][1]]
        
            elif Sum_1 == 3:
            
                if Sum_2 == 1011:
                    
                    Output[l] = [Case_3_a_Line(Points,Value), Points[0][0], Points[0][1]]
                    
                elif Sum_2 == 111:
                    
                    Output[l] = [Case_3_b_Line(Points,Value), Points[0][0], Points[0][1]]
                
                elif Sum_2 == 1110:
                    
                    Output[l] = [Case_3_c_Line(Points,Value), Points[0][0], Points[0][1]]
                
                elif Sum_2 == 1101:
                    
                    Output[l] = [Case_3_d_Line(Points,Value), Points[0][0], Points[0][1]]
        
            if not Output[l] == None and Output[l-1] == None  and l > 0:
                
                Output[l-1] = [Case_4_Line(Points,Value), Points[0][0], Points[0][1]]
                    
    return Output

def OverVal(Points,Value,val):
    '''
    ######################################################
    return true or false
    ######################################################
    '''

    if Value >= Points[val][2]:

        return False

    else:

        return True

def Case_0(Points,Value):

    '''
    ######################################################
    We changed the mode. It is now much more direct by
    drawing tons of polygones. This avoinds so many pro-
    blems
    
    We have now X and check only three o
    
    
        o --- o
        I \   I
        I   \ I
        o --- o
    ######################################################
    '''

    #return
    return None

def Case_1_a(Points,Value):

    '''
    ######################################################
    We changed the mode. It is now much more direct by
    drawing tons of polygones. This avoinds so many pro-
    blems
    
    We have now X and check only three o
    
    
        1 --- o
        I \   I
        I   \ I
        o --- o
    ######################################################
    '''

    return [SinglePointCalc(Points,Value,0),
            TwoPointCalc(Points,Value,0,1),
            TwoPointCalc(Points,Value,0,3)]

def Case_1_b(Points,Value):

    '''
    ######################################################
    We changed the mode. It is now much more direct by
    drawing tons of polygones. This avoinds so many pro-
    blems
    
    We have now X and check only three o
    
    
        o --- 1
        I \   I
        I   \ I
        o --- o
    ######################################################
    '''

    return [SinglePointCalc(Points,Value,1),
            TwoPointCalc(Points,Value,1,2),
            TwoPointCalc(Points,Value,1,0)]


def Case_1_c(Points,Value):

    '''
    ######################################################
    We changed the mode. It is now much more direct by
    drawing tons of polygones. This avoinds so many pro-
    blems
    
    We have now X and check only three o
    
    
        o --- o
        I \   I
        I   \ I
        o --- 1
    ######################################################
    '''

    return [SinglePointCalc(Points,Value,2),
            TwoPointCalc(Points,Value,2,3),
            TwoPointCalc(Points,Value,2,1)]


def Case_1_d(Points,Value):

    '''
    ######################################################
    We changed the mode. It is now much more direct by
    drawing tons of polygones. This avoinds so many pro-
    blems
    
    We have now X and check only three o
    
    
        o --- o
        I \   I
        I   \ I
        1 --- o
    ######################################################
    '''

    return [SinglePointCalc(Points,Value,3),
            TwoPointCalc(Points,Value,3,0),
            TwoPointCalc(Points,Value,3,2)]


def Case_2_a(Points,Value):

    '''
    ######################################################
    We changed the mode. It is now much more direct by
    drawing tons of polygones. This avoinds so many pro-
    blems
    
    We have now X and check only three o
    
    
        1 --- 1
        I \   I
        I   \ I
        o --- o
    ######################################################
    '''

    return [SinglePointCalc(Points,Value,0),
            SinglePointCalc(Points,Value,1),
            TwoPointCalc(Points,Value,1,2),
            TwoPointCalc(Points,Value,0,3)]


def Case_2_b(Points,Value):

    '''
    ######################################################
    We changed the mode. It is now much more direct by
    drawing tons of polygones. This avoinds so many pro-
    blems
    
    We have now X and check only three o
    
    
        o --- 1
        I \   I
        I   \ I
        o --- 1
    ######################################################
    '''

    return [SinglePointCalc(Points,Value,1),
            SinglePointCalc(Points,Value,2),
            TwoPointCalc(Points,Value,2,3),
            TwoPointCalc(Points,Value,1,0)]

def Case_2_c(Points,Value):

    '''
    ######################################################
    We changed the mode. It is now much more direct by
    drawing tons of polygones. This avoinds so many pro-
    blems
    
    We have now X and check only three o
    
    
        o --- 0
        I \   I
        I   \ I
        1 --- 1
    ######################################################
    '''
    
    return [SinglePointCalc(Points,Value,2),
            SinglePointCalc(Points,Value,3),
            TwoPointCalc(Points,Value,3,0),
            TwoPointCalc(Points,Value,2,1)]

def Case_2_d(Points,Value):

    '''
    ######################################################
    We changed the mode. It is now much more direct by
    drawing tons of polygones. This avoinds so many pro-
    blems
    
    We have now X and check only three o
    
    
        1 --- o
        I \   I
        I   \ I
        1 --- o
    ######################################################
    '''
    
    #return
    return [SinglePointCalc(Points,Value,3),
            SinglePointCalc(Points,Value,0),
            TwoPointCalc(Points,Value,0,1),
            TwoPointCalc(Points,Value,3,2)]


def Case_2_e(Points,Value):

    '''
    ######################################################
    We changed the mode. It is now much more direct by
    drawing tons of polygones. This avoinds so many pro-
    blems
    
    We have now X and check only three o
    
    
        1 --- o
        I \   I
        I   \ I
        o --- 1
    ######################################################
    '''

    #return
    return [SinglePointCalc(Points,Value,0),
            TwoPointCalc(Points,Value,0,1),
            TwoPointCalc(Points,Value,2,1),
            SinglePointCalc(Points,Value,2),
            TwoPointCalc(Points,Value,2,3),
            TwoPointCalc(Points,Value,0,3)]


def Case_2_f(Points,Value):

    '''
    ######################################################
    We changed the mode. It is now much more direct by
    drawing tons of polygones. This avoinds so many pro-
    blems
    
    We have now X and check only three o
    
    
        o --- 1
        I \   I
        I   \ I
        1 --- o
    ######################################################
    '''

    return [SinglePointCalc(Points,Value,1),
            TwoPointCalc(Points,Value,1,2),
            TwoPointCalc(Points,Value,3,2),
            SinglePointCalc(Points,Value,3),
            TwoPointCalc(Points,Value,3,0),
            TwoPointCalc(Points,Value,1,0)]


def Case_3_a(Points,Value):

    '''
    ######################################################
    We changed the mode. It is now much more direct by
    drawing tons of polygones. This avoinds so many pro-
    blems
    
    We have now X and check only three o
    
    
        1 --- 1
        I \   I
        I   \ I
        1 --- o
    ######################################################
    '''

    return [SinglePointCalc(Points,Value,0),
            SinglePointCalc(Points,Value,1),
            TwoPointCalc(Points,Value,1,2),
            TwoPointCalc(Points,Value,3,2),
            SinglePointCalc(Points,Value,3)]


def Case_3_b(Points,Value):

    '''
    ######################################################
    We changed the mode. It is now much more direct by
    drawing tons of polygones. This avoinds so many pro-
    blems
    
    We have now X and check only three o
    
    
        1 --- 1
        I \   I
        I   \ I
        o --- 1
    ######################################################
    '''

    return [SinglePointCalc(Points,Value,1),
            SinglePointCalc(Points,Value,2),
            TwoPointCalc(Points,Value,2,3),
            TwoPointCalc(Points,Value,0,3),
            SinglePointCalc(Points,Value,0)]


def Case_3_c(Points,Value):

    '''
    ######################################################
    We changed the mode. It is now much more direct by
    drawing tons of polygones. This avoinds so many pro-
    blems
    
    We have now X and check only three o
    
    
        o --- 1
        I \   I
        I   \ I
        1 --- 1
    ######################################################
    '''
    
    return [SinglePointCalc(Points,Value,2),
            SinglePointCalc(Points,Value,3),
            TwoPointCalc(Points,Value,3,0),
            TwoPointCalc(Points,Value,1,0),
            SinglePointCalc(Points,Value,1)]


def Case_3_d(Points,Value):

    '''
    ######################################################
    We changed the mode. It is now much more direct by
    drawing tons of polygones. This avoinds so many pro-
    blems
    
    We have now X and check only three o
    
    
        1 --- o
        I \   I
        I   \ I
        1 --- 1
    ######################################################
    '''

    return [SinglePointCalc(Points,Value,3),
            SinglePointCalc(Points,Value,0),
            TwoPointCalc(Points,Value,0,1),
            TwoPointCalc(Points,Value,1,2),
            SinglePointCalc(Points,Value,2)]

def Case_4(Points,Value):

    '''
    ######################################################
    We changed the mode. It is now much more direct by
    drawing tons of polygones. This avoinds so many pro-
    blems
    
    We have now X and check only three o
    
    
        1 --- 1
        I \   I
        I   \ I
        1 --- 1
    ######################################################
    '''
    return [SinglePointCalc(Points,Value,0),
            SinglePointCalc(Points,Value,1),
            SinglePointCalc(Points,Value,2),
            SinglePointCalc(Points,Value,3)]

    
def Case_0_Line(Points,Value):

    '''
    ######################################################
    We changed the mode. It is now much more direct by
    drawing tons of polygones. This avoinds so many pro-
    blems
    
    We have now X and check only three o
    
    
        o --- o
        I \   I
        I   \ I
        o --- o
    ######################################################
    '''

    #return
    return None

def Case_1_a_Line(Points,Value):

    '''
    ######################################################
    We changed the mode. It is now much more direct by
    drawing tons of polygones. This avoinds so many pro-
    blems
    
    We have now X and check only three o
    
    
        1 --- o
        I \   I
        I   \ I
        o --- o
    ######################################################
    '''

    return [TwoPointCalc(Points,Value,0,1),
            TwoPointCalc(Points,Value,0,3)]

def Case_1_b_Line(Points,Value):

    '''
    ######################################################
    We changed the mode. It is now much more direct by
    drawing tons of polygones. This avoinds so many pro-
    blems
    
    We have now X and check only three o
    
    
        o --- 1
        I \   I
        I   \ I
        o --- o
    ######################################################
    '''

    return [TwoPointCalc(Points,Value,1,2),
            TwoPointCalc(Points,Value,1,0)]


def Case_1_c_Line(Points,Value):

    '''
    ######################################################
    We changed the mode. It is now much more direct by
    drawing tons of polygones. This avoinds so many pro-
    blems
    
    We have now X and check only three o
    
    
        o --- o
        I \   I
        I   \ I
        o --- 1
    ######################################################
    '''

    return [TwoPointCalc(Points,Value,2,3),
            TwoPointCalc(Points,Value,2,1)]


def Case_1_d_Line(Points,Value):

    '''
    ######################################################
    We changed the mode. It is now much more direct by
    drawing tons of polygones. This avoinds so many pro-
    blems
    
    We have now X and check only three o
    
    
        o --- o
        I \   I
        I   \ I
        1 --- o
    ######################################################
    '''

    return [TwoPointCalc(Points,Value,3,0),
            TwoPointCalc(Points,Value,3,2)]


def Case_2_a_Line(Points,Value):

    '''
    ######################################################
    We changed the mode. It is now much more direct by
    drawing tons of polygones. This avoinds so many pro-
    blems
    
    We have now X and check only three o
    
    
        1 --- 1
        I \   I
        I   \ I
        o --- o
    ######################################################
    '''

    return [TwoPointCalc(Points,Value,1,2),
            TwoPointCalc(Points,Value,0,3)]


def Case_2_b_Line(Points,Value):

    '''
    ######################################################
    We changed the mode. It is now much more direct by
    drawing tons of polygones. This avoinds so many pro-
    blems
    
    We have now X and check only three o
    
    
        o --- 1
        I \   I
        I   \ I
        o --- 1
    ######################################################
    '''

    return [TwoPointCalc(Points,Value,2,3),
            TwoPointCalc(Points,Value,1,0)]

def Case_2_c_Line(Points,Value):

    '''
    ######################################################
    We changed the mode. It is now much more direct by
    drawing tons of polygones. This avoinds so many pro-
    blems
    
    We have now X and check only three o
    
    
        o --- 0
        I \   I
        I   \ I
        1 --- 1
    ######################################################
    '''
    
    return [TwoPointCalc(Points,Value,3,0),
            TwoPointCalc(Points,Value,2,1)]

def Case_2_d_Line(Points,Value):

    '''
    ######################################################
    We changed the mode. It is now much more direct by
    drawing tons of polygones. This avoinds so many pro-
    blems
    
    We have now X and check only three o
    
    
        1 --- o
        I \   I
        I   \ I
        1 --- o
    ######################################################
    '''
    
    #return
    return [TwoPointCalc(Points,Value,0,1),
            TwoPointCalc(Points,Value,3,2)]


def Case_2_e_Line(Points,Value):

    '''
    ######################################################
    We changed the mode. It is now much more direct by
    drawing tons of polygones. This avoinds so many pro-
    blems
    
    We have now X and check only three o
    
    
        1 --- o
        I \   I
        I   \ I
        o --- 1
    ######################################################
    '''

    #return
    return [TwoPointCalc(Points,Value,0,1),
            TwoPointCalc(Points,Value,2,1),
            TwoPointCalc(Points,Value,2,3),
            TwoPointCalc(Points,Value,0,3)]

def Case_2_f_Line(Points,Value):

    '''
    ######################################################
    We changed the mode. It is now much more direct by
    drawing tons of polygones. This avoinds so many pro-
    blems
    
    We have now X and check only three o
    
    
        o --- 1
        I \   I
        I   \ I
        1 --- o
    ######################################################
    '''

    return [TwoPointCalc(Points,Value,1,2),
            TwoPointCalc(Points,Value,3,2),
            TwoPointCalc(Points,Value,3,0),
            TwoPointCalc(Points,Value,1,0)]

def Case_3_a_Line(Points,Value):

    '''
    ######################################################
    We changed the mode. It is now much more direct by
    drawing tons of polygones. This avoinds so many pro-
    blems
    
    We have now X and check only three o
    
    
        1 --- 1
        I \   I
        I   \ I
        1 --- o
    ######################################################
    '''

    return [TwoPointCalc(Points,Value,1,2),
            TwoPointCalc(Points,Value,3,2)]


def Case_3_b_Line(Points,Value):

    '''
    ######################################################
    We changed the mode. It is now much more direct by
    drawing tons of polygones. This avoinds so many pro-
    blems
    
    We have now X and check only three o
    
    
        1 --- 1
        I \   I
        I   \ I
        o --- 1
    ######################################################
    '''

    return [TwoPointCalc(Points,Value,2,3),
            TwoPointCalc(Points,Value,0,3)]


def Case_3_c_Line(Points,Value):

    '''
    ######################################################
    We changed the mode. It is now much more direct by
    drawing tons of polygones. This avoinds so many pro-
    blems
    
    We have now X and check only three o
    
    
        o --- 1
        I \   I
        I   \ I
        1 --- 1
    ######################################################
    '''
    
    return [TwoPointCalc(Points,Value,3,0),
            TwoPointCalc(Points,Value,1,0)]


def Case_3_d_Line(Points,Value):

    '''
    ######################################################
    We changed the mode. It is now much more direct by
    drawing tons of polygones. This avoinds so many pro-
    blems
    
    We have now X and check only three o
    
    
        1 --- o
        I \   I
        I   \ I
        1 --- 1
    ######################################################
    '''

    return [TwoPointCalc(Points,Value,0,1),
            TwoPointCalc(Points,Value,1,2)]

def Case_4_Line(Points,Value):

    '''
    ######################################################
    We changed the mode. It is now much more direct by
    drawing tons of polygones. This avoinds so many pro-
    blems
    
    We have now X and check only three o
    
    
        1 --- 1
        I \   I
        I   \ I
        1 --- 1
    ######################################################
    '''
    return []
