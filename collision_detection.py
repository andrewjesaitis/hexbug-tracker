import numpy as np

from box_world import *
from edit_centroid_list import fill_missing_points, remove_outlier_points

def where_is_point(point, wall_tolerance = 30):
    """
    detects if a point is away from boundary or close to a boundary
    the 'wall_tolerance' parameter gives some leeway in determining if you are to a boundary
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
    
        where_am_i = where_is_point(centroid_coords[i])

        if i >= angle_reach and i < len(centroid_coords) - angle_reach:
            heading_prior = calculate_angle(centroid_coords[i-angle_reach], centroid_coords[i-angle_reach+1])
            heading_after = calculate_angle(centroid_coords[i+angle_reach-1], centroid_coords[i+angle_reach])
            steering = heading_difference(heading_prior, heading_after)
        else:
            steering = 0.

        point_properties_list.append([frame, time_stamp, point, angle, steering, distance, where_am_i])
    
    return point_properties_list


def find_angles_before_after_collision(centroid_coords):
    before_left   = []
    after_left    = []
    before_top    = []
    after_top     = []
    before_bottom = []
    after_bottom  = []
    before_right  = []
    after_right   = []
    
    coord_props = output_coordinate_properties(centroid_coords)
    
    steering_indicating_collision = 0.7 # 0.7 radians ~= 40 degrees
    
    for i in range(0, len(coord_props)):
        steering = coord_props[i][4]
        where_am_i = coord_props[i][6]

        if steering >= steering_indicating_collision and where_am_i != 'away from boundary':
            if where_am_i == 'near left wall':
                before_ang = coord_props[i - 7][3]
                after_ang = coord_props[i + 7][3]
    
                before_left.append(before_ang)
                after_left.append(after_ang)
    
            if where_am_i == 'near top wall':
                before_ang = coord_props[i - 7][3]
                after_ang = coord_props[i + 7][3]

                before_top.append(before_ang)
                after_top.append(after_ang)

            if where_am_i == 'near right wall':
                before_ang = coord_props[i - 7][3]
                after_ang = coord_props[i + 7][3]
    
                before_right.append(before_ang)
                after_right.append(after_ang)

            if where_am_i == 'near bottom wall':
                before_ang = coord_props[i - 7][3]
                after_ang = coord_props[i + 7][3]

                before_bottom.append(before_ang)
                after_bottom.append(after_ang)

    return before_left, after_left, before_top, after_top, before_right, after_right, before_bottom, after_bottom


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

# hard coding regression coefficients:
def return_regression_coefficients():
    '''regression coefficients, pre-calculated from training'''
    return {'left':[0.75424812, 0.25551395],
            'top':[-0.1303246,  -1.26208828],
            'right':  [ 0.23168064, -0.09120714],
            'bottom': [-0.02879984,  0.68054395]
            }

"""
# scripting some experiments below -- will remove or integrate later
centroid_file = 'C:\\Users\\ahernandez\\Desktop\\centroidData.txt' 
with open(centroid_file, 'rb') as f:
    centroid_coords = eval(f.read())
centroid_coords = fill_missing_points(centroid_coords)
centroid_coords = remove_outlier_points(centroid_coords)
centroid_coords = fill_missing_points(centroid_coords)
before_left, after_left, before_top, after_top, before_right, after_right, before_bottom, after_bottom = find_angles_before_after_collision(centroid_coords)
regression_coefficients_left = basic_linear_regression(before_left, after_left)
regression_coefficients_top = basic_linear_regression(before_top, after_top)
regression_coefficients_right = basic_linear_regression(before_right, after_right)
regression_coefficients_bottom = basic_linear_regression(before_bottom, after_bottom)
print regression_coefficients_left
print regression_coefficients_top
print regression_coefficients_right
print regression_coefficients_bottom
"""
