import math

def dist(pt1, pt2):
    x1, y1 = pt1
    x2, y2 = pt2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def find_intermediate_points(point1, point2, d):
    """
    computes a point between point1 and point2.
    the computed point is a distance, d, away from point1
    """
    x1, y1 = point1
    x2, y2 = point2
    
    deltaX = (x2 - x1)
    deltaY = (y2 - y1)
    
    if (deltaX != 0):
        #http://math.stackexchange.com/questions/656500/given-a-point-slope-and-a-distance-along-that-slope-easily-find-a-second-p
        m = deltaY / (deltaX * 1.0) # slope
        r = math.sqrt(1 + m**2)
        point3 = [ (x1 + d/r) , (y1 + (d * m)/r) ]
    else:
      # if deltaX = 0 then the line is a vertical line with undefined slope
        point3 = [x1, (y1 + d)]
    
    return point3

def estimate_unknown_points(centroid_coord_list):
    centroid_coords_with_estimates_list = list(centroid_coord_list)
    
    # iterate through centroid_coord_list and find unknown centroids
    i = 0
    while i < len(centroid_coord_list):
        # count is the number of unknown centroids that appear in succession (one after another)
        count = 0
        if (centroid_coord_list[i] == [-1,-1]):
            count += 1
            
            while(centroid_coord_list[i + count][0] == -1 and centroid_coord_list[i + count][0] == -1):
                count += 1
            
            first_known_coord = centroid_coord_list[i-1]
            second_known_coord = centroid_coord_list[i + count]
            
            d = dist(first_known_coord, second_known_coord)
                    
            for c in range(count):
                displacement = (d * (c + 1)) / (count + 1)
                centroid_coords_with_estimates_list[i + c] = find_intermediate_points(first_known_coord, second_known_coord, displacement)
                    
        i += (count + 1)

    return centroid_coords_with_estimates_list
