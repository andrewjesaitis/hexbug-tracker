from math import *

def dist(pt1, pt2):
    """
    Calculates distance between two points in the x-y plane
    """
    x1, y1 = pt1
    x2, y2 = pt2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def angle_trunc(a):
    """
    This maps all angles to a domain of [-pi, pi]
    """
    while a < 0.0:
        a += pi * 2
    return ((a + pi) % (pi * 2)) - pi

def heading_difference(head1, head2):
    """
    Calculates the angle between two headings. This difference is mapped to
    the domain of [-pi, pi].
    """
    return abs(angle_trunc(head2 - head1))

def calculate_angle(point1, point2):
    """
    Calculates the angle of the between line created by two points and the x axis.
    """
    x1, y1 = point1
    x2, y2 = point2
    return angle_trunc(atan2((y1-y2),(x1-x2)))

def calculate_box_bounds(pt_arr):
    """
    Calculate the minima and maxima of the x-y data set and return the
    4 corners of the box.
    """
    x_arr, y_arr = zip(*pt_arr)
    min_x = min(x_arr)
    max_x = max(x_arr)
    min_y = min(y_arr)
    max_y = max(y_arr)
    return ((min_x,min_y), (min_x, max_y), (max_x, min_y), (max_x, max_y))

def box_bounds():
    '''Return pre-calculated box bounds from training'''
    return {
        'min_x': 148,
        'max_x': 677,
        'min_y': 88,
        'max_y': 419
    }

def where_is_point(point, wall_tolerance = 30):
    """
    Detect if a point is away from boundary or close to a boundary.
    'Wall_tolerance' is a distance in pixels, call it w.
    A point is considered near a boundary if it falls within a distance w from the boundary.
    """

    bounds = box_bounds()
    where_am_i = 'away from boundary'

    # [min x, max x, min y, max y]
    # if list element is 0 then not near an extrema, i.e, not near either an extreme x and/or y value.
    # if list element is 1 then near the corresponding extrema, i.e, near either an extreme x and/or y value.
    near_extrema = [0, 0, 0, 0]

    if bounds['min_x'] - wall_tolerance <= point[0] <= bounds['min_x'] + wall_tolerance:
        near_extrema[0] = 1
        where_am_i = 'near left wall'

    if bounds['min_y'] - wall_tolerance <= point[1] <= bounds['min_y'] + wall_tolerance:
        near_extrema[2] = 1
        where_am_i = 'near top wall'

    if bounds['max_x'] - wall_tolerance <= point[0] <= bounds['max_x'] + wall_tolerance:
        near_extrema[1] = 1
        where_am_i = 'near right wall'

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

def frames_to_timestamp(frame):
    '''
    Convert a frame index to a timestamp, assuming 24 frames per second.
    '''
    m = str(int(floor(frame / 24) / 60)).zfill(2)
    s = str(int(floor(frame / 24) % 60)).zfill(2)
    return (m + ':' + s)

def output_coordinate_properties(centroid_coords):
    """
    centroid coords parameter is the training data.
    Upon running this method, the following properties of every coordinate will be printed:
    frame, time_stamp, point, angle, steering, distance, where_am_i
    """
    angle_reach = 7
    point_properties_list = []
    for i in range(1, len(centroid_coords)):

        frame = i
        time_stamp = frames_to_timestamp(frame)
        point = centroid_coords[i]
        angle = calculate_angle(centroid_coords[i-1], centroid_coords[i])
        distance = dist(centroid_coords[i-1], centroid_coords[i])

        where_am_i = where_is_point(centroid_coords[i])

        if i >= angle_reach and i < len(centroid_coords) - angle_reach:
            heading_prior = calculate_angle(centroid_coords[i-angle_reach], centroid_coords[i-angle_reach+1])
            heading_after = calculate_angle(centroid_coords[i+angle_reach-1], centroid_coords[i+angle_reach])
            steering = heading_difference(heading_prior, heading_after)
        else:
            steering = 0.

        point_properties_list.append([frame, time_stamp, point, angle, steering, distance, where_am_i])

    return point_properties_list


