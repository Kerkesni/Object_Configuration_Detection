from PIL import Image, ImageDraw
import json
import numpy as np
from shapely.geometry import Point, LineString 
from shapely import affinity
import math

# Calculates the centroid of an object
def calculate_centroid(coordinates):
    n = len(coordinates)
    x = y = 0
    for coord in coordinates:
        x += int(coord['x'])
        y += int(coord['y'])
    x /= n
    y /= n
    return (x, y)

# Extracting object names and points from the file
def extract_data(json_data):
    objects = []

    for obj in json_data['annotation']['object']:
        tmp = {}
        tmp['name'] = obj['name']
        tmp_points = obj['polygon']['pt']
        for pt in tmp_points:
            del pt['time']
        tmp['pts'] = tmp_points
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

#writes the kformules in a file
def writeKformules(objects, filename):
    ### Defining the K-formules
    k_formules = []
    for index in range(len(objects)-1):
        k_formule = objects[index]['name']+"("
        for index2 in range(index+1, len(objects)):
            k_formule+=objects[index2]['name']+","
        k_formule = k_formule[:-1]
        k_formule += ")"
        k_formules.append(k_formule)
    ###
        
    ### Writing K-formule in a file
    f= open(filename+".txt","w+")
    for formule in k_formules:
        f.write(formule+"\n")
    f.close()
    ###

file = open('./Ressources/Annotation/im_1.json')
json_data = json.load(file)

raw_objets = extract_data(json_data)#[{name, pts:[{x, y}, ...]}, ...]
objects = getObjectsFromRaw(raw_objets) #[{name, x, y}, ...]

### Displaying the image with the names of objects in the centroids ###
try:  
    im = Image.open('./Ressources/Images/im_1.jpg') 
except IOError: 
    print("error while opening the image")
    exit

draw = ImageDraw.Draw(im)

#image Size
imageSize = im.size

#0° Axis Coords (0° line across the middle of the screen)
init = (0, imageSize[1]/2)
end = (imageSize[0], imageSize[1]/2)

original_axis = LineString([init, end])

for angle in [0, 45, 90, 135, 180, 225, 270, 315, 360]:
    
    final_objects = []

    rotatedLine = rotateLine(original_axis, angle)
    #draw.line(rotatedLine.coords[:], fill=500)

    #Getting the coordinates
    for obj in objects:
        #draw.text((obj['x'], obj['y']), obj['name'], fill="white")
        point = Point(obj['x'], obj['y'])
        projection_point = Orthoprojection(point, rotatedLine)
        draw.line([(obj['x'], obj['y']), (projection_point[0], projection_point[1])], fill=200)

        tmp_object = {}
        tmp_object['name'] = obj['name']
        tmp_object['x'] = projection_point[0]
        tmp_object['y'] = projection_point[1]
        final_objects.append(tmp_object)
    
    #Sorting
    if angle <= 45 and angle >= 0:
        #sort by x
        final_objects.sort(key=lambda obj: obj['x'])
    elif angle > 45 and angle < 135:
        # sort by y
        final_objects.sort(key=lambda obj: obj['y'])
    elif angle >=135 and angle <= 225:
        #sort by -x
        final_objects.sort(key=lambda obj: obj['x'], reverse=True)
    elif angle > 225 and angle < 315:
        #sort by -y
        final_objects.sort(key=lambda obj: obj['y'], reverse=True)
    elif angle >= 315 and angle <= 360:
        #sort by -x
        final_objects.sort(key=lambda obj: obj['x'], reverse=True)

    writeKformules(final_objects, 'im_1'+'_'+str(angle))

im.show()
