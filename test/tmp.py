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

#Function that returns the euclidean distance between two k-formlues files of the same image (between different angles)
def calculateEuclideanDistanceForAngle(ob1, ob2, angle):

    Histo_obj1 = readKforms('../'+str(ob1)+'/kformules/'+str(ob1)+'_'+str(angle)+'.txt')
    Histo_obj2 = readKforms('../'+str(ob2)+'/kformules/'+str(ob2)+'_'+str(angle)+'.txt')
    #euclidean_distances = []
    euclidean_distances_sum = 0
    distance = 0

    for kform in range(len(Histo_obj1)):
        for histo in range(len(Histo_obj1[kform])):
            #euclidean_distances.append(euclidean(Histo_obj1[kform][histo], Histo_obj2[kform][histo]))
            euclidean_distances_sum += euclidean(Histo_obj1[kform][histo], Histo_obj2[kform][histo])
            distance += 1

    return euclidean_distances_sum/distance

#Calculates the average Euclidean distance between all the histograms of an image
def getEuclideanDistance(degrees, ob1, ob2):
    distances = []
    for angle in range(len(degrees)):
        distances.append(calculateEuclideanDistanceForAngle(ob1, ob2, degrees[angle]))
    return np.min(distances)


def rapportSimilitude(ob1, ob2, fAngle, sAngle):
    Histo_obj1 = readKforms('../'+str(ob1)+'/kformules/'+str(ob1)+'_'+str(fAngle)+'.txt')
    Histo_obj2 = readKforms('../'+str(ob2)+'/kformules/'+str(ob2)+'_'+str(sAngle)+'.txt')
    ratio = 0
    counter = 0
    for kform in range(len(Histo_obj1)):
        for histo in range(len(Histo_obj1[kform])):
            for term in range(len(Histo_obj1[kform][histo])):

                if(Histo_obj1[kform][histo][term] < Histo_obj2[kform][histo][term]):
                    rt = Histo_obj1[kform][histo][term] / Histo_obj2[kform][histo][term]
                else:
                    rt = Histo_obj2[kform][histo][term] / Histo_obj1[kform][histo][term]

                if(not np.isnan(rt) and not np.isinf(rt)):
                    ratio += rt
                    counter += 1

    return ratio / counter


degrees = [0, 45, 90, 135, 180, 225, 270, 315, 360]
ob1 = 'im_11'
ob2 = 'im_15'

ratios = []

for fAngle in range (len(degrees)):
    for sAngle in range(len(degrees)):
        ratios.append(rapportSimilitude(ob1, ob2, degrees[fAngle], degrees[sAngle]))

print(np.max(ratios))