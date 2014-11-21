#!/usr/bin/env python

import argparse
import json
from collections import defaultdict

from box_world import *
from edit_centroid_list import fill_missing_points
from hexbug_plot import plot_actual_vs_prediction

DEFAULT_TEST_FILE = "./training_video1-centroid_data"

def main():
    parser = argparse.ArgumentParser(description='Default: Output a prediction to prediction.txt for the next 60 frames')
    parser.add_argument('-i', '--input', help='Specify an input file', metavar='FILE', default=DEFAULT_TEST_FILE)
    parser.add_argument('-b', '--bounds', action='store_true', help='Calculate and print the bounds of the box')
    parser.add_argument('-p', '--properties', action='store_true', help='Output the properties for each point')
    parser.add_argument('-t', '--test', action='store_true', help='Use prior points to predict the last 60 known points; graph the comparison')
    args = parser.parse_args()

    pt_arr = parse_input_file(args.input)

    if args.bounds:
        print "Box Bounds"
        print calculate_box_bounds(pt_arr)
    elif args.properties:
        print "Property Dictionary"
        prop_dict = build_property_dict(pt_arr)
        print prop_dict
    elif args.test:
        actual = pt_arr[-60:]
        preceding = pt_arr[:-60]
        # predictions = predict(preceding)
        predictions = preceding
        plot_actual_vs_prediction(actual, predictions, calc_l2_error)
    else:
        actual = pt_arr[-60:]
        output_predictions(actual)

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

def calc_l2_error(prediction, actual):
    assert len(prediction) == len(actual)
    return round(sqrt(sum([dist(pt_predict,pt_actual)**2 for pt_predict,pt_actual in zip(prediction,actual)])), 2)


if __name__ == "__main__":
    main()
