import matplotlib
matplotlib.use('agg')
import os
import json
from PIL import Image
from FilesParser import extract_data, getObjectsFromRaw
from ForceHistograms import generateHistograms
from Kformules import generateKformule

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

files = os.listdir('../Ressources/Annotation/')

for file in files:
    base=os.path.basename(file)
    processFile(os.path.splitext(base)[0])
