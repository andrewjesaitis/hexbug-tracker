from copy import deepcopy

def smooth(path, a = 0.5, B = 0.1, tolerance = 0.000001):
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
