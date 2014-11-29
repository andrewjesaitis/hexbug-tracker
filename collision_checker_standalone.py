"""
NOTE:
be sure to set your centroid_file and output_file variables below
after that you should be able to run this code from your local IDE

i will properly integrate this soon
"""


from math import *
import numpy as np

def find_intermediate_points(point1, point2, d):
    """
    computes a point between point1 and point2.
    the computed point is a distance, d, away from point1
    """
    x1, y1 = point1
    x2, y2 = point2

    deltaX = (x2 - x1)
    deltaY = (y2 - y1)

    if (deltaX != 0):
        #http://math.stackexchange.com/questions/656500/given-a-point-slope-and-a-distance-along-that-slope-easily-find-a-second-p
        m = deltaY / (deltaX * 1.0) # slope
        r = sqrt(1 + m**2)
        point3 = [ (x1 + d/r) , (y1 + (d * m)/r) ]
    else:
        # if deltaX = 0 then the line is a vertical line with undefined slope
        point3 = [x1, (y1 + d)]

    return point3

def fill_missing_points(centroid_coord_list):
    centroid_coords_with_estimates_list = list(centroid_coord_list)

    # iterate through centroid_coord_list and find unknown centroids
    i = 0
    while i < len(centroid_coord_list):
        # count is the number of unknown centroids that appear in succession (one after another)
        count = 0
        if (centroid_coord_list[i] == [-1,-1]):
            count += 1

            while(centroid_coord_list[i + count] == [-1,-1]):
                count += 1

            first_known_coord = centroid_coord_list[i-1]
            second_known_coord = centroid_coord_list[i + count]

            d = dist(first_known_coord, second_known_coord)
            angle = calculate_angle(second_known_coord, first_known_coord)
            if abs(angle) > pi/2 or angle == -1*pi/2 :
                second_known_coord, first_known_coord = first_known_coord, second_known_coord

            for c in range(count):
                displacement = (d * (c + 1)) / (count + 1)
                centroid_coords_with_estimates_list[i + c] = find_intermediate_points(first_known_coord, second_known_coord, displacement)

        i += (count + 1)

    return centroid_coords_with_estimates_list

def remove_outlier_points(centroid_coord_list):
    distance_list = []
    prev_pt = centroid_coord_list[0]
    for pt in centroid_coord_list:
        distance_list.append(dist(prev_pt, pt))
        prev_pt = pt
    distances = np.array(distance_list)
    cutoff_distance = np.percentile(distances, 98)

    filtered_arr = filter(lambda x: -1 not in x, centroid_coord_list)
    x_arr, y_arr = zip(*filtered_arr)
    x_cutoffs = np.percentile(x_arr, [2, 98])
    y_cutoffs = np.percentile(y_arr, [2, 98])
    #print x_cutoffs

    #doing an empty slice in python returns a deep copy of the list
    cleaned_centroid_coord_list = centroid_coord_list[:]
    prev_pt = centroid_coord_list[0]
    for idx, pt in enumerate(centroid_coord_list):
        if prev_pt == [-1,-1]:
            prev_pt = pt
            continue
        distance = dist(prev_pt, pt)
        # set any point more than 1 sd of the distance away from it's neighbor to (-1,-1)
        # set any point in the highest and lowest 2 percentiles to (-1,-1)
        if distance > cutoff_distance or pt[0] < x_cutoffs[0] or pt[0] > x_cutoffs[1] or pt[1] < y_cutoffs[0] or pt[1] > y_cutoffs[1]:
            cleaned_centroid_coord_list[idx] = [-1,-1]
        prev_pt = cleaned_centroid_coord_list[idx]
    return cleaned_centroid_coord_list


def dist(pt1, pt2):
    x1, y1 = pt1
    x2, y2 = pt2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def angle_trunc(a):
    """This maps all angles to a domain of [-pi, pi]"""
    while a < 0.0:
        a += pi * 2
    return ((a + pi) % (pi * 2)) - pi

def calculate_angle(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return angle_trunc(atan2((y1-y2),(x1-x2)))

def calculate_box_bounds(pt_arr):
    x_arr, y_arr = zip(*pt_arr)
    min_x = min(x_arr)
    max_x = max(x_arr)
    min_y = min(y_arr)
    max_y = max(y_arr)

    return ((min_x,min_y), (min_x, max_y), (max_x, min_y), (max_x, max_y))

def box_bounds():
    """
    box bounds, pre-calculated from training
    """
    return {
        'min_x': 142,
        'max_x': 680,
        'min_y': 79,
        'max_y': 425
    }
    
    
def where_is_point(point, wall_tolerance):
    """
    detects if a point is away from boundary or close to a boundary
    
    the 'wall_tolerance' parameter gives somes leeway in determining if you are to a boundary
    for example if min_x = 142 and wall_tolerance = 10,
    then you are near the left boundary if your point's x value is within 10 pixels plus or minus the min_x  
    """

    bounds = box_bounds()
    where_am_i = 'away from boundary'
    
    # [min x, max x, min y, max y]
    # if list element is 0 then not near an extrema, i.e, not near either an extreme x and/or y value. 
    # if list element is 1 then near the corresponding extrema, i.e, near either an extreme x and/or y value.
    near_extrema = [0, 0, 0, 0] 
    
    if bounds['min_x'] - wall_tolerance <= point[0] <= bounds['min_x'] + wall_tolerance:
        near_extrema[0] = 1
        where_am_i = 'near left_wall'
    
    if bounds['max_x'] - wall_tolerance <= point[0] <= bounds['max_x'] + wall_tolerance:
        near_extrema[1] = 1
        where_am_i = 'near right wall'
        
    if bounds['min_y'] - wall_tolerance <= point[1] <= bounds['min_y'] + wall_tolerance:
        near_extrema[2] = 1
        where_am_i = 'near top wall'

    if bounds['max_y'] - wall_tolerance <= point[1] <= bounds['max_y'] + wall_tolerance:
        near_extrema[3] = 1
        where_am_i = 'near bottom wall'
        
    if sum(near_extrema) > 1:
        if near_extrema == [1, 0, 1, 0]:
            where_am_i = 'near top left corner'
        elif near_extrema == [0, 1, 1, 0]: 
            where_am_i = 'near top right corner'
        elif near_extrema == [1, 0, 0, 1]:
            where_am_i = 'near bottom left corner'
        else: 
            where_am_i = 'near bottom right corner'
        
    return where_am_i

centroid_file = 'C:\\Users\\ahernandez\\Desktop\\centroidData.txt' 
with open(centroid_file, 'rb') as f:
    centroid_coords = eval(f.read())


centroid_coords = fill_missing_points(centroid_coords)
centroid_coords = remove_outlier_points(centroid_coords)
centroid_coords = fill_missing_points(centroid_coords)


def frames_to_timestamp(frame):
    m = str(int(floor(frame / 24) / 60))
    s = str(int(floor(frame / 24) % 60))
    
    if len(m) == 1:
        m = '0' + m
        
    if len(s) == 1:
        s = '0' + s
    
    return (m + ':' + s)


# iterate through points and list out properties
point_properties_list = []
for i in range(1, len(centroid_coords)):
    
    frame = i
    time_stamp = frames_to_timestamp(frame)
    point = centroid_coords[i]
    angle = calculate_angle(centroid_coords[i-1], centroid_coords[i])
    distance = dist(centroid_coords[i-1], centroid_coords[i])
    where_am_i = where_is_point(centroid_coords[i], 15)    
    
    point_properties_list.append([frame, time_stamp, point, angle, distance, where_am_i])


# clear file before writing
output_file = 'C:\\Users\\ahernandez\\Desktop\\centroidDataouput.txt'
open(output_file, 'w').close()
    
f = open(output_file,'w')

# write out the points and their properties
f.write('frame ' + '\t' + 'time_stamp' + '\t' +  'point' + '\t' +  'angle' + '\t' +  'distance ' + '\t' +  'where_am_i' + '\n')
for p in point_properties_list:
    f.write(str(p) +'\n')

f.close()
