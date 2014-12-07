from copy import deepcopy

from box_world import *
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
        heading_delta = heading_delta/abs(heading_delta) * min(abs(heading_delta), 0.034)
    speed = 10
    x, y = path[-1]
    bot = robot(x, y, heading, speed, heading_delta)
    return ([bot.advance() for i in range(frames_to_predict)], path)

def smooth(path, a = 0.18, B = .64, tolerance = 0.000001):
    """
    Smooth a series of coordinates by minimizing the the error between the actual
    point its associated smoothed point and the distance between consecutive
    smoothed points. The function returns a list represented the smoothed coordinates.
    """
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
    """
    Detect if hexbug is stuck in a corner.
    """
    corner_size = 12
    stuck_duration = 2
    for point in points[0:stuck_duration]:
        if where_is_point(point, corner_size)[-6:] != 'corner':
            return False
    return True

def stall_in_corner(points):
    """
    Return a list of points identical to the last measured point
    """
    return [points[0] for i in range(60)]

def where_is_point(point, wall_tolerance = 30):
    """
    Detect if a point is away from boundary or close to a boundary.
    'Wall_tolerance' is a distance in pixels, call it w.
    A point is considered near a boundary if it falls within a distance w from the boundary.
    """

    bounds = box_bounds()
    where_am_i = 'away from boundary'

    # [min x, max x, min y, max y]
    # if list element is 0 then not near an extrema, i.e, not near either an extreme x and/or y value.
    # if list element is 1 then near the corresponding extrema, i.e, near either an extreme x and/or y value.
    near_extrema = [0, 0, 0, 0]

    if bounds['min_x'] - wall_tolerance <= point[0] <= bounds['min_x'] + wall_tolerance:
        near_extrema[0] = 1
        where_am_i = 'near left wall'

    if bounds['min_y'] - wall_tolerance <= point[1] <= bounds['min_y'] + wall_tolerance:
        near_extrema[2] = 1
        where_am_i = 'near top wall'

    if bounds['max_x'] - wall_tolerance <= point[0] <= bounds['max_x'] + wall_tolerance:
        near_extrema[1] = 1
        where_am_i = 'near right wall'

    if bounds['max_y'] - wall_tolerance <= point[1] <= bounds['max_y'] + wall_tolerance:
        near_extrema[3] = 1
        where_am_i = 'near bottom wall'

    if sum(near_extrema) > 1:
        if near_extrema == [1, 0, 1, 0]:
            where_am_i = 'near top left corner'
        elif near_extrema == [0, 1, 1, 0]:
            where_am_i = 'near top right corner'
        elif near_extrema == [1, 0, 0, 1]:
            where_am_i = 'near bottom left corner'
        else:
            where_am_i = 'near bottom right corner'

    return where_am_i
