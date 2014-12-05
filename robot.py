from math import *
from box_world import *
import random

class robot:
    def __init__(self, x = 0.0, y = 0.0, heading = 0.0, distance = 1.0, heading_delta = 0.0):
        """This function is called when you create a new robot. It sets some of
        the attributes of the robot, either to their default values or to the values
        specified when it is created."""
        self.x = x
        self.y = y
        self.heading = heading
        self.distance = distance # only applies to target bot, who always moves at same speed.
        self.distance_noise    = 0.0
        self.measurement_noise = 0.0
        self.heading_delta = heading_delta
        dims = bug_dimensions()
        self.length = dims['length']
        self.breadth = dims['breadth']


    def set_noise(self, new_d_noise, new_m_noise):
        """This lets us change the noise parameters, which can be very
        helpful when using particle filters."""
        self.distance_noise    = float(new_d_noise)
        self.measurement_noise = float(new_m_noise)

    def advance(self):
        """This function is used to advance the bot."""
        self.move(self.distance)
        return self.sense()

    def sense(self):
        """This function represents the robot sensing its location. When
        measurements are noisy, this will return a value that is close to,
        but not necessarily equal to, the robot's (x, y) position."""
        return (random.gauss(self.x, self.measurement_noise),
                random.gauss(self.y, self.measurement_noise))


    def move(self, distance, tolerance = 0.001):
        """This function turns the robot and then moves it forward."""
        distance = random.gauss(distance, self.distance_noise)

        # truncate to fit physical limitations
        distance = max(0.0, distance)

        # Execute motion
        self.heading = angle_trunc(self.heading + self.heading_delta)
        self.x += distance * cos(self.heading)
        self.y += distance * sin(self.heading)

        self.bounce()

    def bounce(self):
        # Naive bounce model based on angle to reflection
        bounds = box_bounds()
        bug_min_x = self.x - self.x_width()
        bug_max_x = self.x + self.x_width()
        bug_min_y = self.y - self.y_height()
        bug_max_y = self.y + self.y_height()
        if bug_min_x < bounds['min_x'] and abs(self.heading) > pi/2:
            # left wall bounce
            x_overstep = bug_min_x - bounds['min_x']
            self.x -= 2 * x_overstep
            self.heading = pi - self.heading
            self.heading_delta = 0
        if bug_max_x > bounds['max_x'] and abs(self.heading) < pi/2:
            # right wall bounce
            x_overstep = bug_max_x - bounds['max_x']
            self.x -= 2 * x_overstep
            self.heading = pi - self.heading
            self.heading_delta = 0
        if bug_min_y < bounds['min_y'] and self.heading < 0:
            # bottom wall bounce
            y_overstep = bug_min_y - bounds['min_y']
            self.y -= 2 * y_overstep
            self.heading = -1 * self.heading
            self.heading_delta = 0
        if bug_max_y > bounds['max_y'] and self.heading > 0:
            # top wall bounce
            y_overstep = bug_max_y - bounds['max_y']
            self.y -= 2 * y_overstep
            self.heading = -1 * self.heading
            self.heading_delta = 0

    def x_width(self):
        return abs(self.length * cos(self.heading) + self.breadth * sin(self.heading))

    def y_height(self):
        return abs(self.breadth * cos(self.heading) + self.length * sin(self.heading))

    def __repr__(self):
        """This allows us to print a robot's position"""
        return '[%.5f, %.5f]'  % (self.x, self.y)
