import argparse
import json
from math import *
from collections import defaultdict

from edit_centroid_list import fill_missing_points

DEFAULT_TEST_FILE = "./training_video1-centroid_data"

def parse_input_file(filepath):
    with open(filepath, 'r') as f:
        input_data = json.load(f)
        input_data = fill_missing_points(input_data)
        input_data = map(tuple, input_data)
    return input_data

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
    property_dict = defaultdict(list)
    prev_pt = None
    for pt in pts:
        if not prev_pt:
            prev_pt = pt
            continue
        property_dict[pt].append({"dist": dist(prev_pt, pt), "angle": calculate_angle(prev_pt, pt)})
    return property_dict

def output_predictions(predict_arr):
    assert len(predict_arr) == 60
    with open('prediction.txt', 'w') as f:
        for pt in predict_arr:
            f.write(",".join(map(str, pt))+"\n")

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
    output_predictions(pt_arr[-60:])
    print "Point List"
    print pt_arr
    print "Property Dictionary"
    print prop_dict
    print "Box Bounds"
    print get_box_bounds(pt_arr)

if __name__ == "__main__":
    main()
