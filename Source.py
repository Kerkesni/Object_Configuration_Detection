import json
from PIL import Image, ImageDraw

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


### Opening and parsing the json file
file = open('./Ressources/Annotation/shapes_1.json')
json_data = json.load(file)

raw_objets = extract_data(json_data)#[{name, pts:[{x, y}, ...]}, ...]
objects = getObjectsFromRaw(raw_objets) #[{name, x, y}, ...]
###

### Getting image Size from the file ###
image_size_x = json_data['annotation']['imagesize']['ncols']
image_size_y = json_data['annotation']['imagesize']['nrows']
###

### Freeing memory
file.close()
del json_data
###

### Sorting objects according to the x axis
objects.sort(key=lambda obj: obj['x'])
###

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
f= open("k-formules.txt","w+")
for formule in k_formules:
    f.write(formule+"\n")
f.close()
###

### Displaying the image with the names of objects in the centroids ###
try:  
    im = Image.open('./Ressources/Images/shapes_1.jpg') 
except IOError: 
    print("error while opening the image")
    exit

draw = ImageDraw.Draw(im)

for obj in objects:
    draw.text((obj['x'], obj['y']), obj['name'], fill="white")
im.show()
###
