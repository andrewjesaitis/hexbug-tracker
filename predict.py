#!/usr/bin/env python

import argparse
import json
import random
from collections import defaultdict
from math import *

from box_world import *
from collision_detection import *
from edit_centroid_list import fill_missing_points, remove_outlier_points
from hexbug_plot import plot_actual_vs_prediction
from hexbug_path import predict

DEFAULT_TEST_FILE = "./training_video1-centroid_data"
FRAMES_TO_PREDICT = 60

def main():
    parser = argparse.ArgumentParser(description='Default: Output a prediction to prediction.txt for the next 60 frames')
    parser.add_argument('-i', '--input', help='Specify an input file', metavar='FILE', default=DEFAULT_TEST_FILE)
    parser.add_argument('-b', '--bounds', action='store_true', help='Calculate and print the bounds of the box')
    parser.add_argument('-p', '--properties', action='store_true', help='Output the properties for each point sequentially including frame, timnestamp, and location group')
    parser.add_argument('-t', '--test', action='store_true', help='Use prior points to predict the last 60 known points; graph the comparison')
    parser.add_argument('-r', '--random-test', action='store_true', help='Use prior points to predict the following 60 known points, starting at a random location; graph the comparison; repeat')
    parser.add_argument('-e', '--error-test', action='store_true', help='Use the entire input dataset to generate an average L2 error')
    parser.add_argument('-rg', '--regression', action='store_true', help='Returns the regression coeffecients for the collision model')
    parser.add_argument('-n', '--iterations', default='1', metavar='N', help='For random tests, repeat N times')
    args = parser.parse_args()

    pt_arr = parse_input_file(args.input)

    if args.bounds:
        print "Box Bounds"
        print calculate_box_bounds(pt_arr)
    elif args.properties:
        pts_properties_list = output_coordinate_properties(pt_arr)
        print 'frame' + '\t' + 'time_stamp' + '\t' +  'point' + '\t' +  'angle' + '\t' +  'steering' + '\t' + 'distance' + '\t' +  'where_am_i'
        for p in pts_properties_list:
            print str(p)
    elif args.regression:
        before_left, after_left, before_top, after_top, before_right, after_right, before_bottom, after_bottom = find_angles_before_after_collision(pt_arr)
        regression_coefficients_left = basic_linear_regression(before_left, after_left)
        regression_coefficients_top = basic_linear_regression(before_top, after_top)
        regression_coefficients_right = basic_linear_regression(before_right, after_right)
        regression_coefficients_bottom = basic_linear_regression(before_bottom, after_bottom)

        print '  left coefficients: ' + str(regression_coefficients_left)
        print '   top coefficients: ' + str(regression_coefficients_top)
        print ' right coefficients: ' + str(regression_coefficients_right)
        print 'bottom coefficients: ' + str(regression_coefficients_bottom)
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
        chunk_offset = 15
        l2_err_arr = []
        cutoff_index = chunk_offset
        while(cutoff_index < len(pt_arr)-FRAMES_TO_PREDICT):
            preceding = pt_arr[:cutoff_index][-10:]
            predictions, smoothed_path = predict(preceding)
            actual = pt_arr[cutoff_index:cutoff_index+FRAMES_TO_PREDICT]
            l2_err_arr.append(calc_l2_error(predictions, actual))
            cutoff_index += chunk_offset
        print "Over " + str(len(pt_arr)/chunk_offset) + " iterations, the average L2 error was: " + str(sum(l2_err_arr)/len(l2_err_arr))
    else:
        actual = pt_arr[-FRAMES_TO_PREDICT:]
        output_predictions(actual)

def parse_input_file(filepath):
    """
    Read input file as a JSON array. The data is then cleaned and returned
    as at python list of coordinate pairs.
    """
    with open(filepath, 'r') as f:
        input_data = json.load(f)
        input_data = fill_missing_points(input_data)
        input_data = remove_outlier_points(input_data)
        input_data = fill_missing_points(input_data)
    return input_data

def output_predictions(predict_arr):
    """
    Output an array of points to prediction.txt file. The content of the file is
    formated so that each line contains "x,y"
    """
    assert len(predict_arr) == FRAMES_TO_PREDICT
    with open('prediction.txt', 'w') as f:
        for pt in predict_arr:
            f.write(",".join(map(str, pt))+"\n")

def calc_l2_error(prediction, actual):
    """
    Calculate the L2 error between two list of coordinates - the predicted and actual. The L2 error is
    defined as the square root of the sum of the squares of the distances between associated coordinates.
    """
    assert len(prediction) == len(actual)
    return round(sqrt(sum([dist(pt_predict,pt_actual)**2 for pt_predict,pt_actual in zip(prediction,actual)])), 2)

if __name__ == "__main__":
    main()
