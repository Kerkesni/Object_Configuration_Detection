import matplotlib
matplotlib.use('agg')
from fhistogram import fhistogram
import matplotlib.pyplot as plt
import os
from PIL import Image
import numpy as np


#Calculating histogram of forces between two images
a = Image.open('./im_1/objects/1.pgm').convert('L')
b = Image.open('./im_1/objects/2.pgm').convert('L')
c = Image.open('./im_1/objects/3.pgm').convert('L')

a_array = np.asarray(a)
'''
b_array = np.asarray(b)
c_array = np.asarray(b)


histo = fhistogram(a_array, b_array)
plt.plot(histo)
plt.savefig('h1.png')
histo2 = fhistogram(b_array, c_array)
plt.plot(histo2)
plt.savefig('h2.png')
'''
#np.savetxt("books_read.csv", histo, delimiter=",")

