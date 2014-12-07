hexbug-tracker
==============

Testing Usage
-------------

### Usage:
predict.py [-i FILE]

The input file is a sequence of [x,y] pairs, one for each frame in the test
video. The input file must take the form of:

```
[[x1,y1], [x2,y2]...[xn,yn]]
```

Output a prediction to prediction.txt for the next 60 frames. This file takes
the form of:

```
x1,y1
x2,y2
...
x60,y60
```

### Optional arguments:

  `-h`, `--help`: show additional options

  `-i FILE`, `--input FILE`: Specify an input file (default: training\_video1-centroid\_data)

### Environment:
* Python 2.7.x

### External dependencies:
* Numpy
* Matplotlib

Training Usage
--------------

* See `./predict.py --help` for additional options
* This project includes an iPython notebook that is useful for visualizing data,
prototyping tracking strategies and   examining functions. The notebook and its
plotting code have additional external   dependencies which are enumerated in
requirements.txt. These dependencies can   be installed using pip: `pip install
-r requirements.txt`.

Algorithm
---------

### Summary

* Fill in missing/erroneous data using equidistant points on the hexbug's path.
* Use path smoothing on the tail of the given centroids to help account for noise.
* Assume the most probable behavior given the last known trajectory.
* Get stuck in corners.
* Bounce off of walls to stay within the box boundaries found in training.

### Path Smoothing

We observed that the hexbug generally moves in a smooth path while traveling
inside the box, except when striking a wall. We also observed noise in the
centroid data, sometimes moving a point near but outside the path, sometimes
moving a point outside the region of the box. For the former, more common type
of noise, we found that applying a path smoothing algorithm reduced our average
L2 error on training data by 7.3%.

See hexbug\_path.py

### Trajectory Calculation

The last three points on the smoothed path approximate the hexbug's current
heading and turning angle. Using these, we advance the hexbug prediction for 60
frames, keeping the turning angle until it bounces off a wall, after which it
moves in a straight line. The median speed in the training data is 10 pixels per
frame, which we use for the distance between predicted points, except as
described in the Bouncing section below.

See hexbug\_path.py

Although the hexbug does not typically travel in a straight line, it is nearly
impossible to predict how it will turn. Thus a straight line is the most
probable guess, lacking any other information. We did however find that a hexbug
traveling on a curve is likely to continue on the same curve for some period of
time. Continuing on the curve until hitting a wall decreased our L2 error by
5.4%.

See heading\_delta in robot.py

#### Corners

The hexbug often gets stuck in corners. Therefore when it approaches a corner at
such an angle or it is already stuck in a corner, we predict that it will remain
there for the next 60 frames. Sticking in corners decreased L2 error by 8.2%.

See hexbug\_path.py and collision\_detection.py

#### Bouncing

The training data (excluding outliers) gives us the minimum and maximum centroid
positions in each dimension. For our simulation, we assume that the box
boundaries are perfectly rectangular and are not rotated.

When the simulated hexbug leaves the boundaries, we simulate a reflective
bounce, as a billiard ball would bounce. This is a naive approximation.

See hexbug\_path.py

At each bounce, we decrease the simulated hexbug's speed and allow it to
accelerate back to normal speed. The acceleration rate is slower than a real
hexbug's acceleration, which keeps the predicted points closer to the estimated
bounce point longer, thus slowing it from speeding off in a direction with
decreased certainty. This decreased L2 error by 4.0%.

See robot.py

### Reducing Noise

In addition to path smoothing, we exclude outlying points whose distance from
neighboring points is too far to be possible. These points are removed and
treated as if the data was missing for that video frame. Then we fill in missing
data with equidistant points along the line segment connecting the nearest known
points.

See edit\_centroid\_list.py

### Attempted Alternatives

####Kalman Filter
As an alternative to path smoothing, we also implemented a Kalman filter. Using
a simple Kalman filter assumes that the robot's motion can be modeled in a
linear system. The is a major assumption, but over short intervals the robot's
motion is generally linear. The motion was modeled as a system of 4 linear
equations using the robots x and y coordinates as well as the robot's velocity
in the x and y dimensions. An acceleration (external motion) term  was also
included.

Without modifying the algorithm to keep predictions within the bounds of the
box, using a Kalman filter to predict trajectory increased L2 error by 212.7%.

Once modified to to stay within the box bounds in an analogous manner to the
trajectory calculation, discussed above, we observed that the L2 error was not
significantly better than the path smoothing algorithm. Due to the increased
complexity of the Kalman filter's implementation, we chose to reduce noise with
a path smoothing approach.

####Linear Regression

Wall Bounce Model As an alternative to the naive billiard ball bounce model, we
attempted to implement a simple linear regression bounce model. In the model,
the centroid coordinates immediately before and after a wall bounce were
isolated. The headings of the centroid coordinates were then used to create an
equation of the type: <br> ```angle of reflection = m * angle of incidence +
b```,  where m and b are the regression coefficients produced by the regression
analysis. Four equations were created for bounces off of the left, top, right,
and bottom walls.

Implementing this model proved difficult, and upon manual inspection, regression
did not improve the L2 error. While the bounce angle was slightly more accurate,
the predicted path leading up to the bounce needs refinement. The naive approach
worked better to reduce the L2 error.

On a future release, refining the predicted path of a hexbug as it approaches a
wall would improve the accuracy of the regression model. Also, considering the
speed of the hexbug as it bounces and extending the model from simple to
multiple linear regression would likely yield more accurate bounce angles.

Team
----

* Alfonso Hernandez (ahernandez44)
* Andrew Jesaitis (ajesaitis3)
* Edward Anderson (eanderson73)
