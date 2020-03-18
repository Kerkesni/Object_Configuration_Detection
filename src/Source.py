import matplotlib
matplotlib.use('agg')
import os
import json
from PIL import Image
from FilesParser import extract_data, getObjectsFromRaw
from ForceHistograms import generateHistograms
from Kformules import generateKformule
from EuclideanDistance import getEuclideanDistance

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
    #os.mkdir('./'+filename+'/histograms')

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

    dist = getEuclideanDistance(degrees, filename.split('_')[1])
    distances.append(dist)
    distancesFile.write(filename+' : {:.2f}'.format(dist)+'\n')


degrees = [0, 45, 90, 135, 180, 225, 270, 315, 360]
distancesFile = open('../EuclideanDistances', 'a+')
distances = []

files = os.listdir('../Ressources/Annotation/')

for file in files:
    base=os.path.basename(file)
    filename = os.path.splitext(base)[0]
    processFile(filename)

distancesFile.write('************************************** \n')
distancesFile.write('Difference: \n')

for index in range(len(distances)-1):
    for index2 in range(index+1, len(distances)):
        distancesFile.write('im_'+str(index+1)+' and '+'im_'+str(index2+1)+' : ')
        distancesFile.write("{:.2f}".format(abs(distances[index]-distances[index2]))+'\n')
