#!/usr/bin/env python

import argparse
import json
from collections import defaultdict

from box_world import *
from edit_centroid_list import fill_missing_points

DEFAULT_TEST_FILE = "./training_video1-centroid_data"

def parse_input_file(filepath):
    with open(filepath, 'r') as f:
        input_data = json.load(f)
        input_data = fill_missing_points(input_data)
        input_data = map(tuple, input_data)
    return input_data

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
