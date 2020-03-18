from scipy.spatial.distance import euclidean
import numpy as np
import re

#Returns an array of the histograms in the k-formule by original order
def getHistograms(raw_line):

    histograms = []
    index = 0

    line = raw_line[2:-2].split(']') #separation of the histograms

    for h in line:  #for each histogram in the line
        histo = h
        if(index == 0):
            histo = histo[1:]   #removing '['
        if(index != 0):
            histo = histo[2:]   #removing ',['
        index += 1
        histograms.append(np.fromstring(histo, dtype=float, sep=','))

    histograms.pop()    #removing empty item
    return histograms   #np.array of floats

#function that reads the kforms in a file
#must be called for each file
#path = k-formlule file path
#returns an array of arrays, each array contains the histograms in a k-formule ordered according to the original file
def readKforms(path):
    with open(path, 'r') as fp:
        line = fp.readline()

        histograms = []     #array of all histograms in the k-formules by original order

        while line: #Reads the file line by line
            histograms.append(getHistograms(line))
            line = fp.readline()
        
        return histograms   #np.array


#Function that returns the euclidean distance between two k-formlues files
def calculateEuclideanDistance_AllAngles_AllTerms(ob1, ob2, firstAngle, secondAngle):

    Histo_obj1 = readKforms('../im_'+str(ob1)+'/kformules/im_'+str(ob1)+'_'+str(firstAngle)+'.txt')
    Histo_obj2 = readKforms('../im_'+str(ob2)+'/kformules/im_'+str(ob2)+'_'+str(secondAngle)+'.txt')
    euclidean_distances = 0
    distance = 0

    for kform in range(len(Histo_obj1)):
        kform_distances = 0
        for histo in range(len(Histo_obj1[kform])):
            for histo2 in range(histo+1, len(Histo_obj1[kform])):
                kform_distances += euclidean(Histo_obj1[kform][histo], Histo_obj2[kform][histo2])
                distance += 1
        kform_distances /= distance
        euclidean_distances += kform_distances

    euclidean_distances /= len(Histo_obj1)

    return euclidean_distances

#Function that returns the euclidean distance between two k-formlues files
def calculateEuclideanDistance_AllAngles_SameTerms(ob1, ob2, firstAngle, secondAngle):

    Histo_obj1 = readKforms('../im_'+str(ob1)+'/kformules/im_'+str(ob1)+'_'+str(firstAngle)+'.txt')
    Histo_obj2 = readKforms('../im_'+str(ob2)+'/kformules/im_'+str(ob2)+'_'+str(secondAngle)+'.txt')
    euclidean_distances = 0
    distance = 0

    for kform in range(len(Histo_obj1)):
        kform_distances = 0
        for histo in range(len(Histo_obj1[kform])):
            kform_distances += euclidean(Histo_obj1[kform][histo], Histo_obj2[kform][histo])
            distance += 1
        kform_distances /= distance
        euclidean_distances += kform_distances

    euclidean_distances /= len(Histo_obj1)

    return euclidean_distances

#Function that returns the euclidean distance between two k-formlues files
def calculateEuclideanDistance_SameAngles_AllTerms(ob1, ob2, Angle):

    Histo_obj1 = readKforms('../im_'+str(ob1)+'/kformules/im_'+str(ob1)+'_'+str(Angle)+'.txt')
    Histo_obj2 = readKforms('../im_'+str(ob2)+'/kformules/im_'+str(ob2)+'_'+str(Angle)+'.txt')
    euclidean_distances = 0
    distance = 0

    for kform in range(len(Histo_obj1)):
        kform_distances = 0
        for histo in range(len(Histo_obj1[kform])):
            for histo2 in range(histo+1, len(Histo_obj1[kform])):
                kform_distances += euclidean(Histo_obj1[kform][histo], Histo_obj2[kform][histo2])
                distance += 1
        kform_distances /= distance
        euclidean_distances += kform_distances

    euclidean_distances /= len(Histo_obj1)

    return euclidean_distances

#Function that returns the euclidean distance between two k-formlues files
def calculateEuclideanDistance_SameAngles_SameTerms(ob1, ob2, Angle):

    Histo_obj1 = readKforms('../im_'+str(ob1)+'/kformules/im_'+str(ob1)+'_'+str(Angle)+'.txt')
    Histo_obj2 = readKforms('../im_'+str(ob2)+'/kformules/im_'+str(ob2)+'_'+str(Angle)+'.txt')
    euclidean_distances = 0
    distance = 0

    for kform in range(len(Histo_obj1)):
        kform_distances = 0
        for histo in range(len(Histo_obj1[kform])):
            kform_distances += euclidean(Histo_obj1[kform][histo], Histo_obj2[kform][histo])
            distance += 1
        kform_distances /= distance
        euclidean_distances += kform_distances

    euclidean_distances /= len(Histo_obj1)

    return euclidean_distances



#Calculates the average Euclidean distance between all the histograms of an image
def getEuclideanDistance(degrees, ob1, ob2):

    distance = 0
    nbDistances = 0
    
    #AllAngles
    for firstAngle in range(len(degrees)):
        for secondAngle in range(firstAngle, len(degrees)) :
            #distance += calculateEuclideanDistance_AllAngles_AllTerms(ob1, ob2, degrees[firstAngle], degrees[secondAngle]) #3274.232
            #distance += calculateEuclideanDistance_AllAngles_SameTerms(ob1, ob2, degrees[firstAngle], degrees[secondAngle]) #2986.789
            nbDistances += 1
    '''
    #SameAngles
    for firstAngle in range(len(degrees)):
        #distance += calculateEuclideanDistance_SameAngles_AllTerms(ob1, ob2, degrees[firstAngle])  #3708.616
        #distance += calculateEuclideanDistance_SameAngles_SameTerms(ob1, ob2, degrees[firstAngle]) #153.407
        nbDistances += 1
    '''       
    distance /= nbDistances
    return distance

ob1 = '2'
ob2 = '3'
degrees = [0, 45, 90, 135, 180, 225, 270, 315, 360]

print("%.3f" % getEuclideanDistance(degrees, ob1, ob2))