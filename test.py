import matplotlib
matplotlib.use('agg')
from fhistogram import fhistogram
import matplotlib.pyplot as plt
import os
from PIL import Image
import numpy as np
import pandas as pd
from pandas import DataFrame
from scipy.spatial.distance import euclidean
import re

#a = np.genfromtxt('./im_1/histograms/sum.csv', delimiter=',')
#b = np.genfromtxt('./im_5/histograms/sum.csv', delimiter=',')

a = np.asarray(Image.open('./im_1/objects/1.pgm'))
b = np.asarray(Image.open('./im_1/objects/2.pgm'))



histo = fhistogram(a, b)
k = re.sub(r'\s+', '',np.array2string(histo, threshold=np.inf, max_line_width=np.inf, separator=',').replace('\n', ''))
print(k)
#np.savetxt('histo.txt', histo, )