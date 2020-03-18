'''
import matplotlib
matplotlib.use('agg')
from fhistogram import fhistogram
import matplotlib.pyplot as plt
import os
from PIL import Image
import pandas as pd
from pandas import DataFrame
'''
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
def calculateEuclideanDistanceForAngle(ob1, ob2, firstAngle, secondAngle):

    Histo_obj1 = readKforms('./im_'+str(ob1)+'/kformules/im_'+str(ob1)+'_'+str(firstAngle)+'.txt')
    Histo_obj2 = readKforms('./im_'+str(ob2)+'/kformules/im_'+str(ob2)+'_'+str(secondAngle)+'.txt')
    euclidean_distances = 0

    for kform in range(len(Histo_obj1)):
        kform_distances = 0
        for histo in range(len(Histo_obj1[kform])):
            kform_distances += euclidean(Histo_obj1[kform][histo], Histo_obj2[kform][histo])
        kform_distances /= len(Histo_obj1[kform])
        euclidean_distances += kform_distances

    euclidean_distances /= len(Histo_obj1)

    return euclidean_distances


def getEuclideanDistance(degrees, ob1, ob2):

    distance = 0
    nbDistances = 0

    for firstAngle in range(len(degrees)):
        for secondAngle in range(firstAngle, len(degrees)) :
            distance += calculateEuclideanDistanceForAngle(ob1, ob2, degrees[firstAngle], degrees[secondAngle])
            nbDistances += 1
            
    distance /= nbDistances
    return distance

ob1 = '2'
ob2 = '3'
degrees = [0, 45, 90, 135, 180, 225, 270, 315, 360]

print("%.3f" % getEuclideanDistance(degrees, ob1, ob2))