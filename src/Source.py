import matplotlib
matplotlib.use('agg')
import os
import json
from PIL import Image
from FilesParser import extract_data, getObjectsFromRaw
from ForceHistograms import generateHistograms
from Kformules import generateKformule
from Similarity import getEuclideanDistance, getSimilarityRatio
from global_var import degrees, outputDir, annotationDir, imagesDir

#Fuction That Generate K-formulas for a single image
#Takes image name as parameter (not the full path)
#Annotation file and image file have to have the same name
#Global variables are set in global_var.py, there you can set the input and output directories as well as the angles to consider
#Annotation file must be a json file (labelme xml -> json)
#Image should be jpg
def generate(filename):
    ### Opening and parsing the json file
    file = open(annotationDir+filename+'.json')
    json_data = json.load(file)

    raw_objets = extract_data(json_data)#[{name, pts:[(x, y), ...]}, ...]
    objects = getObjectsFromRaw(raw_objets) #[{name, x, y}, ...]
    ###

    ## Creating data folder
    os.mkdir(outputDir+filename)
    os.mkdir(outputDir+filename+'/kformules')
    os.mkdir(outputDir+filename+'/objects')

    ### Freeing memory
    file.close()
    del json_data
    ###

    try:  
        im = Image.open(imagesDir+filename+'.jpg').convert('1')
    except IOError: 
        print("error while opening the image")
        exit

    #Generating histograms of forces between the objects
    histograms = generateHistograms(im, filename, raw_objets)

    #Generating k-formules
    generateKformule(filename, im, objects, histograms)

#Euclidean distance between two file can calculated using the function getEuclideanDistance()
#Similarity Ratio can be calculated using the methode getSimilarityRatio()

#-------------------------------------------------------------------
distancesFile = open(outputDir+'EuclideanDistances', 'a+')
files = os.listdir(annotationDir)

distancesFile.write('*****************************\n')

#K-formule Generation of all images in a folder
for fileIndex in range(len(files)):
    base=os.path.basename(files[fileIndex])
    filename = os.path.splitext(base)[0]
    generate(filename)

#Calculating similarity ratios and euclidean distances and storing them in a text file
for fileIndex in range(len(files)):
    base=os.path.basename(files[fileIndex])
    filename = os.path.splitext(base)[0]
    for fileIndex2 in range(fileIndex+1, len(files)):
        base=os.path.basename(files[fileIndex2])
        filename2 = os.path.splitext(base)[0]

        distancesFile.write(filename+' and '+filename2+' : ')
        distancesFile.write('Euclidean distance: ')
        distancesFile.write("{0:.3f}".format(getEuclideanDistance(filename, filename2)))
        distancesFile.write("\t Rapport de Similitude: ")
        distancesFile.write("{0:.3f}".format(getSimilarityRatio(filename, filename2)))
        distancesFile.write("\t Erreur: ")
        distancesFile.write("{0:.3f}".format(1-getSimilarityRatio(filename, filename2))+'\n')