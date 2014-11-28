from copy import deepcopy

from box_world import *
from robot import robot

def predict(points, frames_to_predict=60):
    points = points_since_last_collision(points)
    path = smooth(points)
    heading = calculate_angle(points[-1], points[-2])
    speed = dist(points[-2], points[-1])
    x, y = points[-1]
    bot = robot(x, y, heading, speed)
    return ([bot.advance() for i in range(frames_to_predict)], path)

def smooth(path, a = 0.5, B = 0.5, tolerance = 0.000001):
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
