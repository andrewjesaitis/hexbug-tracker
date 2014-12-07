from copy import deepcopy

from box_world import *
from collision_detection import where_is_point
from robot import robot

def predict(points, frames_to_predict=60):
    """
    Since the points may contain noise, reduce the error by smoothing the
    points along a path.
    Return a tuple of size 2, containing an array of the predicted points
    and the smoothed path.
    """
    if stuck_in_corner(points):
        return (stall_in_corner(points), stall_in_corner(points))
    path = smooth(points[-10:])
    prev_heading = calculate_angle(path[-2], path[-3])
    heading = calculate_angle(path[-1], path[-2])
    heading_delta = heading - prev_heading
    if heading_delta != 0:
        heading_delta = heading_delta/abs(heading_delta) * min(abs(heading_delta), 0.037)
    speed = 10
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

def stuck_in_corner(points):
    corner_size = 12
    stuck_duration = 2
    for point in points[0:stuck_duration]:
        if where_is_point(point, corner_size)[-6:] != 'corner':
            return False
    return True

def stall_in_corner(points):
    return [points[0] for i in range(60)]
