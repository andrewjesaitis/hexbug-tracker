from copy import deepcopy

from box_world import *
from robot import robot

def predict(points, frames_to_predict=60):
    points = points_since_last_collision(points)
    path = smooth(points)
    prev_heading = calculate_angle(path[-2], path[-3])
    heading = calculate_angle(path[-1], path[-2])
    heading_delta = heading - prev_heading
    if heading_delta != 0:
        heading_delta = heading_delta/abs(heading_delta) * min(abs(heading_delta), 0.05)
    speed = dist(path[-2], path[-1])
    x, y = path[-1]
    bot = robot(x, y, heading, speed, heading_delta)
    return ([bot.advance() for i in range(frames_to_predict)], path)

def smooth(path, a = 0.18, B = .65, tolerance = 0.000001):
    x = path
    y = deepcopy(path)
    delta = tolerance
    while delta >= tolerance:
        delta = 0
        for i, point in list(enumerate(y))[1:-1]:
            for j, yi in enumerate(point):
                yinit = yi
                xi = path[i][j]
                yi = yi + a * (xi - yi) + B * (y[i+1][j] + y[i-1][j] - 2 * yi)
                y[i][j] = yi
                delta += abs(yi - yinit)
    return y

def points_since_last_collision(points):
    '''Return the subset of points at the tail of points, up until the final collision'''
    return points[-7:]
