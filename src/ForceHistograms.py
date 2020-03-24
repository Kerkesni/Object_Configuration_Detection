from PIL import Image, ImageDraw
import os
import numpy as np
from fhistogram import fhistogram
#import matplotlib.pyplot as plt


#creates an image for each object in the image
def seperateObjects(image, filename, objects):
    imArray = np.asarray(image)
    blankIm = Image.new('L', (imArray.shape[1], imArray.shape[0]), 0)
    index = 0
    for obj in objects:
        index += 1
        # create mask
        maskIm = Image.new('L', (imArray.shape[1], imArray.shape[0]), 255)
        ImageDraw.Draw(maskIm).polygon(obj['pts'], outline=1, fill=1)
        Image.composite(blankIm, image, maskIm).save('../'+filename+'/objects/'+str(index)+'.pgm')


#Calculates and stores histogram of forces between each two objects in the image and stores it in a csv file + png representation
def generateHistograms(image, filename, objects):

    #Separating Objects in the image into multiple files 
    seperateObjects(image, filename, objects)

    dir = '../'+filename+'/objects/'
    objectFileNames = os.listdir(dir)
    #Storing object images as arrays
    objectsArrayRepresentation = []
    for fname in objectFileNames:
        obj = Image.open(dir+fname).convert('L')
        obj_array = np.asarray(obj)
        objectsArrayRepresentation.append(obj_array)

    #list of histograms
    histograms={}

    #plt.clf()   #Emptying the plot

    #Calculating histograms between each two objects
    for index in range(len(objectsArrayRepresentation)):
        for secIndex in range(index+1, len(objectsArrayRepresentation)):
            histo = fhistogram(objectsArrayRepresentation[index], objectsArrayRepresentation[secIndex])
            #plt.plot(histo)
            #histograms.append(histo)
            histograms[str(index+1)+'_'+str(secIndex+1)] = histo
            #np.savetxt('../'+filename+'/histograms/'+str(index+1)+'_'+str(secIndex+1)+'.csv', histo, delimiter=",")
            #plt.savefig('../'+filename+'/histograms/'+str(index+1)+'_'+str(secIndex+1)+'.png')
            #plt.clf()
    
    return histograms

