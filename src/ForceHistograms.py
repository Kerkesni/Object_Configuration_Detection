from PIL import Image, ImageDraw
import os
import numpy as np
from fhistogram import fhistogram
from global_var import outputDir


#creates an image for each object in the image
def seperateObjects(image, filename, objects):
    imArray = np.asarray(image)
    blankIm = Image.new('L', (imArray.shape[1], imArray.shape[0]), 0)
    for obj in objects:
        # create mask
        maskIm = Image.new('L', (imArray.shape[1], imArray.shape[0]), 255)
        ImageDraw.Draw(maskIm).polygon(obj['pts'], outline=1, fill=1)
        Image.composite(blankIm, image, maskIm).save(outputDir+filename+'/objects/'+obj['name']+'.pgm')


#Calculates and stores histogram of forces between each two objects in the image and stores it in a csv file + png representation
def generateHistograms(image, filename, objects):

    #Separating Objects in the image into multiple files 
    seperateObjects(image, filename, objects)

    dir = outputDir+filename+'/objects/'
    objectFileNames = os.listdir(dir)

    #Storing object images as arrays
    objectsArrayRepresentation = []
    for fname in objectFileNames:
        obj = Image.open(dir+fname).convert('1')
        obj_array = np.asarray(obj)
        tmp = {}
        tmp['array'] = obj_array
        tmp['name'] = fname[:1]
        objectsArrayRepresentation.append(tmp)

    #list of histograms
    histograms={}

    #Calculating histograms between each two objects
    for index in range(len(objectsArrayRepresentation)):
        for secIndex in range(index+1, len(objectsArrayRepresentation)):
            histo = fhistogram(objectsArrayRepresentation[index]['array'], objectsArrayRepresentation[secIndex]['array'])

            if(objectsArrayRepresentation[index]['name'] < objectsArrayRepresentation[secIndex]['name']):
                histograms[objectsArrayRepresentation[index]['name']+'_'+objectsArrayRepresentation[secIndex]['name']] = histo
            else:
                histograms[objectsArrayRepresentation[secIndex]['name']+'_'+objectsArrayRepresentation[index]['name']] = histo
    
    return histograms

