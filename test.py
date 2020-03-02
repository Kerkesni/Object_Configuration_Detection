from PIL import Image, ImageDraw
import json
import numpy as np
from shapely.geometry import Point
from shapely.geometry import LineString
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
for obj in objects:
    #draw.text((obj['x'], obj['y']), obj['name'], fill="white")

    degree = (2100, 0)
    init = (0, 1500)

    point = Point(obj['x'], obj['y'])
    line = LineString([init, degree])

    x = np.array(point.coords[0])

    u = np.array(line.coords[0])
    v = np.array(line.coords[len(line.coords)-1])

    n = v - u
    n /= np.linalg.norm(n, 2)

    P = u + n*np.dot(x - u, n)
    draw.text((P[0], P[1]), obj['name'], fill="black")
    #draw.line(init + degree, fill=128)

    '''unit_vector_1 = init / np.linalg.norm(init)
    unit_vector_2 = degree / np.linalg.norm(degree)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    angle = np.arccos(dot_product)
    print(angle)'''

    radians = math.radians(45)
    c, s = np.cos(radians), np.sin(radians)
    j = np.matrix([[c, s], [-s, c]])
    m = np.dot(j, [init[0], init[1]])
    draw.line(init + m, fill=128)

im.show()
###
