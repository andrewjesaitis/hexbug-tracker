#!/usr/bin/env python

import argparse
import json
import random
from collections import defaultdict
from math import *

from box_world import *
from edit_centroid_list import fill_missing_points, remove_outlier_points
from hexbug_plot import plot_actual_vs_prediction
from hexbug_path import predict

DEFAULT_TEST_FILE = "./training_video1-centroid_data"
FRAMES_TO_PREDICT = 60

def main():
    parser = argparse.ArgumentParser(description='Default: Output a prediction to prediction.txt for the next 60 frames')
    parser.add_argument('-i', '--input', help='Specify an input file', metavar='FILE', default=DEFAULT_TEST_FILE)
    parser.add_argument('-b', '--bounds', action='store_true', help='Calculate and print the bounds of the box')
    parser.add_argument('-p', '--properties', action='store_true', help='Output the properties for each point')
    parser.add_argument('-t', '--test', action='store_true', help='Use prior points to predict the last 60 known points; graph the comparison')
    parser.add_argument('-r', '--random-test', action='store_true', help='Use prior points to predict the following 60 known points, starting at a random location; graph the comparison; repeat')
    parser.add_argument('-e', '--error-test', action='store_true', help='Use the entire input dataset to generate an average L2 error')
    parser.add_argument('-n', '--iterations', default='1', metavar='N', help='For random tests, repeat N times')
    args = parser.parse_args()

    pt_arr = parse_input_file(args.input)

    if args.bounds:
        print "Box Bounds"
        print calculate_box_bounds(pt_arr)
    elif args.properties:
        print "Property Dictionary"
        prop_dict = build_property_dict(pt_arr)
        print prop_dict
    elif args.test or args.random_test:
        actual_arr, predictions_arr, preceding_arr, smoothed_arr = [], [], [], []
        for i in range(int(args.iterations)):
            if args.random_test:
                cutoff_index = random.randint(2, len(pt_arr) - FRAMES_TO_PREDICT)
            else:
                cutoff_index = len(pt_arr) - FRAMES_TO_PREDICT
            preceding = pt_arr[:cutoff_index][-10:]
            predictions, smoothed_path = predict(preceding)
            actual_arr.append(pt_arr[cutoff_index:cutoff_index+FRAMES_TO_PREDICT])
            preceding_arr.append(preceding)
            predictions_arr.append(predictions)
            smoothed_arr.append(smoothed_path)
        plot_actual_vs_prediction(actual_arr, predictions_arr, preceding_arr, smoothed_arr, calc_l2_error)
    elif args.error_test:
        #carve input data in 1 min (1440 frame) pieces
        l2_err_arr = []
        cutoff_index = 1440
        while(cutoff_index < len(pt_arr)-FRAMES_TO_PREDICT):
            preceding = pt_arr[:cutoff_index][-10:]
            predictions, smoothed_path = predict(preceding)
            actual = pt_arr[cutoff_index:cutoff_index+FRAMES_TO_PREDICT]
            l2_err_arr.append(calc_l2_error(predictions, actual))
            cutoff_index += 1440
        print "Over " + str(len(pt_arr)/1440) + " iterations, the average L2 error was: " + str(sum(l2_err_arr)/len(l2_err_arr))
    else:
        actual = pt_arr[-FRAMES_TO_PREDICT:]
        output_predictions(actual)

def parse_input_file(filepath):
    with open(filepath, 'r') as f:
        input_data = json.load(f)
        input_data = fill_missing_points(input_data)
        input_data = remove_outlier_points(input_data)
        input_data = fill_missing_points(input_data)
    return input_data

def build_property_dict(pts):
    property_dict = defaultdict(list)
    pts = map(tuple, pts)
    prev_pt = pts[0]
    for pt in pts:
        property_dict[pt].append({"dist": dist(prev_pt, pt), "angle": calculate_angle(prev_pt, pt)})
        prev_pt = pt
    return property_dict

def output_predictions(predict_arr):
    assert len(predict_arr) == FRAMES_TO_PREDICT
    with open('prediction.txt', 'w') as f:
        for pt in predict_arr:
            f.write(",".join(map(str, pt))+"\n")

def calc_l2_error(prediction, actual):
    assert len(prediction) == len(actual)
    return round(sqrt(sum([dist(pt_predict,pt_actual)**2 for pt_predict,pt_actual in zip(prediction,actual)])), 2)

if __name__ == "__main__":
    main()
