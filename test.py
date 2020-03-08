import matplotlib
matplotlib.use('agg')
from fhistogram import fhistogram
import matplotlib.pyplot as plt
import os
from PIL import Image
import numpy as np
import pandas as pd
from pandas import DataFrame

dir = "./im_1/histograms"
data = []

for file in os.listdir(dir):
    if file.endswith(".csv"):
        data.append(np.genfromtxt(dir+'/'+file, delimiter=','))

bigHisto = [0]*len(data[0])

for histogram in data:
    for index in range(len(histogram)):
        bigHisto[index]+=histogram[index]/len(data)

plt.plot(bigHisto)
plt.savefig("a.png")