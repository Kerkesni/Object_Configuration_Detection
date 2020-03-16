'''
import matplotlib
matplotlib.use('agg')
from fhistogram import fhistogram
import matplotlib.pyplot as plt
import os
from PIL import Image
import pandas as pd
from pandas import DataFrame
from scipy.spatial.distance import euclidean
'''
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

with open('./im_1/kformules/im_1_0.txt', 'r') as fp:
    line = fp.readline()

    histograms = []     #array of all histograms in the k-formules by original order

    while line:
        histograms.append(getHistograms(line))
        line = fp.readline()

