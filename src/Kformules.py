import numpy as np
import re
from shapely.geometry import Point, LineString 
from shapely import affinity



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
            if(int(objects[index]['name']) < int(objects[index2]['name'])):
                k_formule+=re.sub(r'\s+', '',np.array2string(histograms[objects[index]['name']+'_'+objects[index2]['name']], threshold=np.inf, max_line_width=np.inf, separator=',').replace('\n', '')+",")
            else:
                k_formule+=re.sub(r'\s+', '',np.array2string(histograms[objects[index2]['name']+'_'+objects[index]['name']], threshold=np.inf, max_line_width=np.inf, separator=',').replace('\n', '')+",")
        k_formule = k_formule[:-1]
        k_formule += ")"
        k_formules.append(k_formule)
    ###
        
    ### Writing K-formule in a file
    f= open('../'+filename+'/kformules/'+filename+"_"+str(angle)+".txt","w+")
    for formule in k_formules:
        f.write(formule+"\n")
    f.close()
    ###

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
