hexbug-tracker
==============

Testing Usage
-------------

usage: predict.py [-i FILE]

Output a prediction to prediction.txt for the next 60 frames

optional arguments:
  `-h`, `--help`:            show additional options
  `-i FILE`, `--input FILE`: Specify an input file (default: training\_video1-centroid\_data)

The input file is a sequence of [x,y] pairs, one for each frame in the test video.

```
[[x1,y1], [x2,y2]...[xn,yn]]
```

Training Usage
--------------

* See `./predict.py --help` for additional options
* This project includes an ipython notebook that is useful for prototyping and
  examining functions. The notebook and its plotting code has external
  dependencies which are enumerated in requirements.txt. These dependencies can
  be installed using pip: `pip install -r requirements.txt`.

Algorithm
---------

### Summary

* Use path smoothing on the tail of the given centroids to help account for noise.
* Assume the most probable behavior given the last known trajectory.
* Get stuck in corners.
* Bounce off of walls to stay within the box boundaries found in training.
* Fill in missing/erroneous data using equidistant points on the hexbug's path.

### Path Smoothing

We observed that the hexbug generally moves in a smooth path while traveling
inside the box, except when striking a wall. We also observed significant noise
in the centroid data, sometimes moving a point near but outside the path,
sometimes moving a point outside the region of the box. For the former, more
common type of noise, we found that applying a path smoothing algorithm reduced
our average L2 error on training data by 7.3%. Because the path before and after
striking the wall is not necessarily smooth, we attempt to detect when the wall
has been struck and only smooth the path up to that point.

See hexbug\_path.py

### Trajectory Calculation

The last three points on the smoothed path approximate the hexbug's current
velocity and turning angle. Using these, we advance the hexbug prediction for 60
frames, keeping the turning angle until it bounces off a wall, after which it
moves in a straight line.

See hexbug\_path.py

Although the hexbug does not typically travel in a straight line, it is nearly
impossible to predict how it will turn. Thus a straight line is the most
probable guess, lacking any other information. We did however find that a hexbug
traveling on a curve is likely to continue on the same curve for some period of
time. Continuing on the curve until hitting a wall decreased our L2 error by 5.4%.

See heading\_delta in robot.py

#### Corners

The hexbug often gets stuck in corners if approached near a 45 degree angle.
Therefore when it approaches a corner at such an angle or it is already stuck in
a corner, we predict that it will remain there for the next 60 frames.

#### Bouncing

The training data (excluding outliers) gives us the minimum and maximum centroid
positions in each dimension. For our simulation, we assume that the box
boundaries are perfectly rectangular and are not rotated.

When the simulated hexbug leaves the boundaries, we simulate a reflective
bounce, as a billiard ball would bounce. This is a naive approximation.

See hexbug\_path.py

### Reducing Noise

In addition to path smoothing, we exclude outlying points whose distance from
neighboring points is too far to be possible. These points are removed and
treated as if the data was missing for that video frame. Then we fill in missing
data with equidistant points along the line segment connecting the nearest known
points.

### Attempted Alternative

*[Describe our Kalman filter attempt]*

Without modifying it to keep predictions within the bounds of the box, using a
Kalman filter to predict trajectory increased L2 error by 212.7%.

Team
----

* Alfonso Hernandez (ahernandez44)
* Andrew Jesaitis (ajesaitis3)
* Edward Anderson (eanderson73)
