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
    m = str(int(floor(frame / 24) / 60))
    s = str(int(floor(frame / 24) % 60))

    if len(m) == 1:
        m = '0' + m

    if len(s) == 1:
        s = '0' + s

    return (m + ':' + s)


def output_coordinate_properties(centroid_coords):
    point_properties_list = []
    for i in range(1, len(centroid_coords)):

        frame = i
        time_stamp = frames_to_timestamp(frame)
        point = centroid_coords[i]
        angle = calculate_angle(centroid_coords[i-1], centroid_coords[i])
        distance = dist(centroid_coords[i-1], centroid_coords[i])
        where_am_i = where_is_point(centroid_coords[i], 15)

        point_properties_list.append([frame, time_stamp, point, angle, distance, where_am_i])

    print 'frame ' + '\t' + 'time_stamp' + '\t' +  'point' + '\t' +  'angle' + '\t' +  'distance ' + '\t' +  'where_am_i'
    for p in point_properties_list:
        print str(p)

