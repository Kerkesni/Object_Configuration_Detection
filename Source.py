import matplotlib
matplotlib.use('agg')
import os
import json
import math
import numpy as np
from PIL import Image, ImageDraw
from shapely.geometry import Point, LineString 
from shapely import affinity
from fhistogram import fhistogram
import matplotlib.pyplot as plt
import re


# Extracting object names and points from the file
def extract_data(json_data):
    objects = []

    for obj in json_data['annotation']['object']:
        tmp = {}
        tmp['pts'] = []
        tmp['name'] = obj['name']
        tmp_points = obj['polygon']['pt']
        for pt in tmp_points:
            del pt['time']
            tmp['pts'].append((int(pt['x']), int(pt['y'])))
        objects.append(tmp)

    return objects

#Returns an array of objects containing the name and centroid of objects
def getObjectsFromRaw(raw_objects_data):
    objects = []
    for obj in raw_objects_data:
        centroid = calculate_centroid(obj['pts'])
        tmp_obj = {
            'name': obj['name'],
            'x': centroid[0],
            'y': centroid[1]
        }
        objects.append(tmp_obj)
    return objects

# Calculates the centroid of an object
def calculate_centroid(coordinates):
    n = len(coordinates)
    x = y = 0
    for coord in coordinates:
        x += int(coord[0])
        y += int(coord[1])
    x /= n
    y /= n
    return (x, y)

#Projects a point into a line and returns the point, returns tuple
def Orthoprojection(point, line):
    x = np.array(point.coords[0])

    u = np.array(line.coords[0])
    v = np.array(line.coords[len(line.coords)-1])

    n = v - u
    n /= np.linalg.norm(n, 2)

    return u + n*np.dot(x - u, n)

#rotates a line by an angle, returns lineString object
def rotateLine(line, angle):
    coords = []
    for coord in affinity.rotate(line, angle).coords[:]:
        x = coord[0]
        y = coord[1]
        if(x > 2100):
            x = 2100
        if(x < 0):
            x = 0
        if(y > 1500):
            y = 1500
        if(y < 0):
            y = 0
        coords.append(tuple((x,y)))
    return LineString(coords)

#sorts the list of objects acording to the axis angle
def sortObjects(objects, angle):
    if angle <= 45 and angle >= 0:
        #sort by x
        objects.sort(key=lambda obj: obj['x'])
    elif angle > 45 and angle < 135:
        # sort by y
        objects.sort(key=lambda obj: obj['y'])
    elif angle >=135 and angle <= 225:
        #sort by -x
        objects.sort(key=lambda obj: obj['x'], reverse=True)
    elif angle > 225 and angle < 315:
        #sort by -y
        objects.sort(key=lambda obj: obj['y'], reverse=True)
    elif angle >= 315 and angle <= 360:
        #sort by -x
        objects.sort(key=lambda obj: obj['x'], reverse=True)

#writes the kformules in a file
def writeKformules(objects, filename, angle, histograms):

    ### Defining the K-formules
    k_formules = []
    for index in range(len(objects)-1):
        k_formule = objects[index]['name']+"("
        for index2 in range(index+1, len(objects)):
            #k_formule+=objects[index2]['name']+","
            if(index < index2):
                k_formule+=re.sub(r'\s+', '',np.array2string(histograms[str(index+1)+'_'+str(index2+1)], threshold=np.inf, max_line_width=np.inf, separator=',').replace('\n', '')+",")
            else:
                k_formule+=re.sub(r'\s+', '',np.array2string(histograms[str(index2+1)+'_'+str(index1+1)], threshold=np.inf, max_line_width=np.inf, separator=',').replace('\n', '')+",")
        k_formule = k_formule[:-1]
        k_formule += ")"
        k_formules.append(k_formule)
    ###
        
    ### Writing K-formule in a file
    f= open('./'+filename+'/kformules/'+filename+"_"+str(angle)+".txt","w+")
    for formule in k_formules:
        f.write(formule+"\n")
    f.close()
    ###

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
        Image.composite(blankIm, image, maskIm).save('./'+filename+'/objects/'+str(index)+'.pgm')

#Creates a file for each k-formules
def generateKformule(filename, image, objects, histograms):

    #image Size
    imageSize = image.size

    #0 degree Axis Coords (0 degree line across the middle of the screen)
    init = (0, imageSize[1]/2)
    end = (imageSize[0], imageSize[1]/2)
    original_axis = LineString([init, end])

    #Axis Rotation Degrees
    degrees = [0, 45, 90, 135, 180, 225, 270, 315, 360]

    for angle in degrees:
        listOfObjects = []
        rotatedAxis = rotateLine(original_axis, angle)

        #Getting the coordinates
        for obj in objects:
            point = Point(obj['x'], obj['y'])
            projection_point = Orthoprojection(point, rotatedAxis)

            tmp_object = {}
            tmp_object['name'] = obj['name']
            tmp_object['x'] = projection_point[0]
            tmp_object['y'] = projection_point[1]
            listOfObjects.append(tmp_object)

        #Sorting The objects
        sortObjects(listOfObjects, angle)

        #writing the k-formules into a file
        writeKformules(listOfObjects, filename, angle, histograms)

#Calculates and stores histogram of forces between each two objects in the image and stores it in a csv file + png representation
def generateHistograms(filename):
    dir = './'+filename+'/objects/'
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
            #np.savetxt('./'+filename+'/histograms/'+str(index+1)+'_'+str(secIndex+1)+'.csv', histo, delimiter=",")
            #plt.savefig('./'+filename+'/histograms/'+str(index+1)+'_'+str(secIndex+1)+'.png')
            #plt.clf()
    
    return histograms

#main function
def processFile(filename):
    ### Opening and parsing the json file
    file = open('./Ressources/Annotation/'+filename+'.json')
    json_data = json.load(file)

    raw_objets = extract_data(json_data)#[{name, pts:[(x, y), ...]}, ...]
    objects = getObjectsFromRaw(raw_objets) #[{name, x, y}, ...]
    ###

    ## Creating k-formules folder
    os.mkdir(filename)
    os.mkdir('./'+filename+'/kformules')
    os.mkdir('./'+filename+'/objects')
    #os.mkdir('./'+filename+'/histograms')

    ### Freeing memory
    file.close()
    del json_data
    ###

    try:  
        im = Image.open('./Ressources/Images/'+filename+'.jpg').convert('1')
    except IOError: 
        print("error while opening the image")
        exit
    
    #Separating objects
    seperateObjects(im, filename, raw_objets)

    #Generating histograms of forces between the objects
    histograms = generateHistograms(filename)

    #Generating k-formules
    generateKformule(filename, im, objects, histograms)

files = os.listdir('./Ressources/Annotation/')

for file in files:
    base=os.path.basename(file)
    processFile(os.path.splitext(base)[0])
