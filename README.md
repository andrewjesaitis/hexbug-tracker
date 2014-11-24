hexbug-tracker
==============

Testing Usage
-------------

usage: predict.py [-i FILE]

Output a prediction to prediction.txt for the next 60 frames

optional arguments:
  -h, --help            show additional options
  -i FILE, --input FILE Specify an input file (default: training\_video1-centroid\_data)

The input file is a sequence of [x,y] pairs, one for each frame in the test video.

```
[[x1,y1], [x2,y2]...[xn,yn]]
```

Training Usage
--------------

* See `./predict.py --help` for additional options
* This project includes an ipython notebook that is useful for prototyping and examining functions. The notebook and the plotting code it contains do have external dependencies. These are enumerated in requirements.txt. These dependencies can be easily install using `pip` with the command `pip install -r requirements.txt`.

Algorithm
---------

Follow the trajectory given by the last 2 points in a straight line, moving the point into the box bounds if it exits.
This is temporary and does not implement any robotic AI algorithms.

Team
----

* Alfonso Hernandez (ahernandez44)
* Andrew Jesaitis ()
* Edward Anderson (eanderson73)
