import argparse
import re
from math import *

DEFAULT_TEST_FILE = "./training_video1-centroid_data"

def parse_input_file(filepath):
    pattern = re.compile(r"(-?\d+)")
    pt_arr = []
    with open(filepath, 'r') as f:
        for line in f:
            x,y = pattern.findall(line)
            if x == "-1" or y == "-1":
                #skip (-1,-1) since these are bad points
                continue
            pt_arr.append((int(x), int(y)))      
    return pt_arr
    
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

if __name__ == "__main__":
    main()