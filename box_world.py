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
