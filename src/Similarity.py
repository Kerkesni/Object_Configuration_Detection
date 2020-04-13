from scipy.spatial.distance import euclidean
import numpy as np
import re
from global_var import degrees, outputDir

#Returns an array of the histograms in the k-formule by original order
def getHistograms(raw_line):

    histograms = []
    index = 0

    line = raw_line.split(']')[:-1] #separation of the histograms

    for h in line:  #for each histogram in the line
        histo = h
        if(index == 0):
            histo = histo.split('[')[1]   #removing '['
        if(index != 0):
            histo = histo[2:]   #removing ',['
        index += 1
        histograms.append(np.fromstring(histo, dtype=float, sep=','))

    return histograms   #np.array of floats

#Reads the kforms in a file
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

#Function that returns the euclidean distance between two k-formla files
def calculateEuclideanDistance(ob1, ob2, angle, sangle):

    Histo_obj1 = readKforms(outputDir+str(ob1)+'/kformules/'+str(ob1)+'_'+str(angle)+'.txt')
    Histo_obj2 = readKforms(outputDir+str(ob2)+'/kformules/'+str(ob2)+'_'+str(sangle)+'.txt')
    #euclidean_distances = []
    euclidean_distances_sum = 0

    for kform in range(len(Histo_obj1)):#foreach k-formula
        for histo in range(len(Histo_obj1[kform])):#foreach histogram in a k-formula
            #euclidean_distances.append(euclidean(Histo_obj1[kform][histo], Histo_obj2[kform][histo]))
            euclidean_distances_sum += euclidean(Histo_obj1[kform][histo], Histo_obj2[kform][histo]) #calculating euclidean distance between the two hisograms

    return euclidean_distances_sum/10

#Calculates Euclidean distance between two images
#Arguments:the two filenames of the images (not the path, without the extension)
def getEuclideanDistance(filename1, filename2):
    distances = []
    for angle in range(len(degrees)):
        distances.append(calculateEuclideanDistance(filename1, filename2, degrees[0], degrees[angle]))
    return np.min(distances)

#Function that calculates the similarity ratio between two k-formula files
def calculateSimilarityRatio(ob1, ob2, angle, sangle):
    Histo_obj1 = readKforms(outputDir+str(ob1)+'/kformules/'+str(ob1)+'_'+str(angle)+'.txt')
    Histo_obj2 = readKforms(outputDir+str(ob2)+'/kformules/'+str(ob2)+'_'+str(sangle)+'.txt')
    ratios = []
    for kform in range(len(Histo_obj1)):#For each k-formule
        for histo in range(len(Histo_obj1[kform])):#for each of histograms in a formula
            buffer_min = 0
            cardA = 0
            cardB = 0
            for term in range(len(Histo_obj1[kform][histo])):# for each term in an histogram
                buffer_min += min(Histo_obj1[kform][histo][term], Histo_obj2[kform][histo][term])
                cardA += Histo_obj1[kform][histo][term]
                cardB += Histo_obj2[kform][histo][term]
            if(buffer_min == 0 and max(cardA, cardB) == 0):
                ratios.append(1)
            elif (buffer_min == 0 or max(cardA, cardB) == 0):
                ratios.append(0)
            else:
                ratios.append(buffer_min / max(cardA, cardB))  
    return sum(ratios) / 10

#Calculates the similarity ratio between two images
#Arguments:the two filenames of the images (not the path, without the extension)
def getSimilarityRatio(filename1, filename2):
    ratios = []

    for angle in range(len(degrees)):
        ratios.append(calculateSimilarityRatio(filename1, filename2, degrees[0], degrees[angle]))

    return np.max(ratios)