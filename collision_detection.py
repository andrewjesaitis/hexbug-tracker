import numpy as np

from box_world import *
from edit_centroid_list import fill_missing_points, remove_outlier_points
from hexbug_plot import plot_actual_vs_prediction
from hexbug_path import predict

def where_is_point(point, wall_tolerance):
    """
    detects if a point is away from boundary or close to a boundary

    the 'wall_tolerance' parameter gives somes leeway in determining if you are to a boundary
    for example if min_x = 142 and wall_tolerance = 10,
    then you are near the left boundary if your point's x value is within 10 pixels plus or minus the min_x
    """
    
    bounds = box_bounds()
    where_am_i = 'away from boundary'

    # [min x, max x, min y, max y]
    # if list element is 0 then not near an extrema, i.e, not near either an extreme x and/or y value.
    # if list element is 1 then near the corresponding extrema, i.e, near either an extreme x and/or y value.
    near_extrema = [0, 0, 0, 0]

    if bounds['min_x'] - wall_tolerance <= point[0] <= bounds['min_x'] + wall_tolerance:
        near_extrema[0] = 1
        where_am_i = 'near left_wall'

    if bounds['max_x'] - wall_tolerance <= point[0] <= bounds['max_x'] + wall_tolerance:
        near_extrema[1] = 1
        where_am_i = 'near right wall'

    if bounds['min_y'] - wall_tolerance <= point[1] <= bounds['min_y'] + wall_tolerance:
        near_extrema[2] = 1
        where_am_i = 'near top wall'

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


def frames_to_timestamp(frame):
    m = str(int(floor(frame / 24) / 60)).zfill(2)
    s = str(int(floor(frame / 24) % 60)).zfill(2)
    return (m + ':' + s)

def output_coordinate_properties(centroid_coords):
    angle_reach = 7
    point_properties_list = []
    for i in range(1, len(centroid_coords)):

        frame = i
        time_stamp = frames_to_timestamp(frame)
        point = centroid_coords[i]
        angle = calculate_angle(centroid_coords[i-1], centroid_coords[i])
        distance = dist(centroid_coords[i-1], centroid_coords[i])
        
        wall_tolerance = 30 # pixels
        
        where_am_i = where_is_point(centroid_coords[i], wall_tolerance)

        if i >= angle_reach and i < len(centroid_coords) - angle_reach:
            heading_prior = calculate_angle(centroid_coords[i-angle_reach], centroid_coords[i-angle_reach+1])
            heading_after = calculate_angle(centroid_coords[i+angle_reach-1], centroid_coords[i+angle_reach])
            steering = heading_difference(heading_prior, heading_after)
        else:
            steering = 0.

        point_properties_list.append([frame, time_stamp, point, angle, steering, distance, where_am_i])
        
    return point_properties_list


def find_angles_before_after_collision(centroid_coords):
    before = []
    after = []
    
    coord_props = output_coordinate_properties(centroid_coords)
    
    steering_indicating_collision = 0.7 # 0.7 radians ~= 40 degrees
    
    for i in range(0, len(coord_props)):
        steering = coord_props[i][4]
        relative_loc = coord_props[i][6]
        
        if steering >= steering_indicating_collision and relative_loc != 'away from boundary':
            before_ang = coord_props[i - 7][3]
            after_ang = coord_props[i + 7][3]
            
            before.append(before_ang)
            after.append(after_ang)
        
    assert len(before) == len(after)
    
    return before, after


def basic_linear_regression(x, y):
    """
    this functions returns the regressions coefficients, a and b
    the regression equation used is: reflection_angle = a * incidence_angle + b
    """
    regression_coeffecients = np.polyfit(x, y, 1)
    return regression_coeffecients

def incident_reflection_regression_formula(inc_ang, regression_coefficients):
    """
    feed the angle of incidence and the regression_coeffecients as parameters
    will return the angle of reflection
    """
    ref_ang = regression_coefficients[0] * inc_ang + regression_coefficients[1]
    return ref_ang