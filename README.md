hexbug-tracker
==============

`predict.py` is a script that takes as it's input a file that list the positions of the centroid of a hexbug. The contents of the file should take the form:
```
[[x1,y1], [x2,y2]...[xn,yn]]
```
It's output is the parsed input list and a dictionary that contains the distance and angle between a point and the previous point.

Also included is an ipython notebook that is useful for prototyping and examining functions. The notebook and the plotting code it contains do have external dependencies. These are enumerated in requirements.txt. These dependencies can be easily install using `pip` with the command `pip install -r requirements.txt`. 
