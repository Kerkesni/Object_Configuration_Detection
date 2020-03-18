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