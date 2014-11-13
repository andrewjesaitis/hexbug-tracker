import argparse
import json
from math import *

DEFAULT_TEST_FILE = "./training_video1-centroid_data"

def parse_input_file(filepath):
    with open(filepath, 'r') as f:
        input_data = json.load(f)
        filtered_data = filter(lambda x: -1 not in x, input_data)  
        filtered_data = map(tuple, filtered_data)
    return filtered_data
    
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

def get_box_bounds(pt_arr):
    x_arr, y_arr = zip(*pt_arr)
    min_x = min(x_arr)
    max_x = max(x_arr)
    min_y = min(y_arr)
    max_y = max(y_arr)
    
    return ((min_x,min_y), (min_x, max_y), (max_x, min_y), (max_x, max_y))
    
    
def build_property_dict(pts):
    property_dict = {}
    prev_pt = None
    for pt in pts:
        if not prev_pt:
            prev_pt = pt
            continue
        property_dict[pt] = {"dist": dist(prev_pt, pt), "angle": calculate_angle(prev_pt, pt)}
    return property_dict

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    args = parser.parse_args()
    if args.input:
        filepath = args.input
    else:
        filepath = DEFAULT_TEST_FILE
    
    pt_arr = parse_input_file(DEFAULT_TEST_FILE)
    prop_dict = build_property_dict(pt_arr)
    print "Point List"
    print pt_arr
    print "Property Dictionary"
    print prop_dict
    print "Box Bounds"
    print get_box_bounds(pt_arr)

if __name__ == "__main__":
    main()