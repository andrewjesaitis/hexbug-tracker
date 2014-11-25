#!/usr/bin/env python

import argparse
import json
import random
from collections import defaultdict

from box_world import *
from edit_centroid_list import fill_missing_points, remove_outlier_points
from hexbug_plot import plot_actual_vs_prediction
from path import smooth
from robot import robot

DEFAULT_TEST_FILE = "./training_video1-centroid_data"

def main():
    parser = argparse.ArgumentParser(description='Default: Output a prediction to prediction.txt for the next 60 frames')
    parser.add_argument('-i', '--input', help='Specify an input file', metavar='FILE', default=DEFAULT_TEST_FILE)
    parser.add_argument('-b', '--bounds', action='store_true', help='Calculate and print the bounds of the box')
    parser.add_argument('-p', '--properties', action='store_true', help='Output the properties for each point')
    parser.add_argument('-t', '--test', action='store_true', help='Use prior points to predict the last 60 known points; graph the comparison')
    parser.add_argument('-r', '--random-test', action='store_true', help='Use prior points to predict the following 60 known points, starting at a random location; graph the comparison; repeat')
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
        for i in range(int(args.iterations)):
            if args.random_test:
                start_index = random.randint(7, len(pt_arr) - 60)
                actual = pt_arr[start_index+7:start_index+67]
                preceding = pt_arr[:start_index+7]
            else:
                actual = pt_arr[-60:]
                preceding = pt_arr[:-60]
            # TODO: Instead of the last 7, smooth all the points up to the last collision
            path = smooth(preceding[-7:])
            predictions = predict(path)
            plot_actual_vs_prediction(actual, predictions, calc_l2_error)
    else:
        actual = pt_arr[-60:]
        output_predictions(actual)

def predict(points):
    heading = calculate_angle(points[-1], points[-2])
    speed = dist(points[-2], points[-1])
    x, y = points[-1]
    bot = robot(x, y, heading, speed)
    return [bot.advance() for i in range(60)]

def parse_input_file(filepath):
    with open(filepath, 'r') as f:
        input_data = json.load(f)
        input_data = fill_missing_points(input_data)
        input_data = remove_outlier_points(input_data)
        input_data = fill_missing_points(input_data)
    return input_data

def build_property_dict(pts):
    property_dict = defaultdict(list)
    prev_pt = pts[0]
    for pt in pts:
        property_dict[pt].append({"dist": dist(prev_pt, pt), "angle": calculate_angle(prev_pt, pt)})
        prev_pt = pt
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
