import matplotlib
matplotlib.use('agg')
import os
import json
from PIL import Image
from FilesParser import extract_data, getObjectsFromRaw
from ForceHistograms import generateHistograms
from Kformules import generateKformule
from EuclideanDistance import getEuclideanDistance, getRapportSimilitude

#main function
def processFile(filename):
    ### Opening and parsing the json file
    file = open('../Ressources/Annotation/'+filename+'.json')
    json_data = json.load(file)

    raw_objets = extract_data(json_data)#[{name, pts:[(x, y), ...]}, ...]
    objects = getObjectsFromRaw(raw_objets) #[{name, x, y}, ...]
    ###

    ## Creating k-formules folder
    os.mkdir('../'+filename)
    os.mkdir('../'+filename+'/kformules')
    os.mkdir('../'+filename+'/objects')
    #os.mkdir('../'+filename+'/histograms')

    ### Freeing memory
    file.close()
    del json_data
    ###

    try:  
        im = Image.open('../Ressources/Images/'+filename+'.jpg').convert('1')
    except IOError: 
        print("error while opening the image")
        exit

    #Generating histograms of forces between the objects
    histograms = generateHistograms(im, filename, raw_objets)

    #Generating k-formules
    generateKformule(filename, im, objects, histograms)


degrees = [0, 45, 90, 135, 180, 225, 270, 315, 360]
distancesFile = open('../EuclideanDistances', 'a+')

files = os.listdir('../Ressources/Annotation/')

for fileIndex in range(len(files)):
    base=os.path.basename(files[fileIndex])
    filename = os.path.splitext(base)[0]
    processFile(filename)

for fileIndex in range(len(files)):
    base=os.path.basename(files[fileIndex])
    filename = os.path.splitext(base)[0]
    for fileIndex2 in range(fileIndex+1, len(files)):
        base=os.path.basename(files[fileIndex2])
        filename2 = os.path.splitext(base)[0]

        distancesFile.write(filename+' and '+filename2+' : ')
        distancesFile.write('Euclidean distance: ')
        distancesFile.write("{0:.3f}".format(getEuclideanDistance(degrees, filename, filename2)))
        distancesFile.write("\t Rapport de Similitude: ")
        distancesFile.write("{0:.3f}".format(getRapportSimilitude(degrees, filename, filename2))+'\n')