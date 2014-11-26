from math import *

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
    '''box bounds, pre-calculated from training'''
    return {
        'min_x': 142,
        'max_x': 680,
        'min_y': 79,
        'max_y': 441
    }
