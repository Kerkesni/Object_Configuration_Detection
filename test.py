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

a = np.genfromtxt('./im_1/histograms/sum.csv', delimiter=',')
b = np.genfromtxt('./im_5/histograms/sum.csv', delimiter=',')

print(euclidean(a, b))