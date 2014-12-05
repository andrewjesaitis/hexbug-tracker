from math import *
from box_world import *
import random

class robot:
    def __init__(self, x = 0.0, y = 0.0, heading = 0.0, speed = 1.0, heading_delta = 0.0):
        """This function is called when you create a new robot. It sets some of
        the attributes of the robot, either to their default values or to the values
        specified when it is created."""
        self.x = x
        self.y = y
        self.heading = heading
        self.speed = speed
        self.heading_delta = heading_delta

    def move(self, speed, tolerance = 0.001):
        """This function turns the robot and then moves it forward."""
        # truncate to fit physical limitations
        speed = max(0.0, speed)

        # Naive bounce model based on angle to reflection
        bounds = box_bounds()
        #Top Edge
        if self.x < bounds['min_x']:
            self.heading = pi - self.heading
            self.heading_delta = 0
        #Right Edge
        elif self.y < bounds['min_y']:
            self.heading = -1 * self.heading
            self.heading_delta = 0
        #Bottom Edge
        if self.x > bounds['max_x']:
            self.heading = pi - self.heading
            self.heading_delta = 0
        #Left Edge
        if self.y > bounds['max_y']:
            self.heading = -1 * self.heading
            self.heading_delta = 0

        # Execute motion
        self.heading = angle_trunc(self.heading + self.heading_delta)
        self.x += speed * cos(self.heading)
        self.y += speed * sin(self.heading)

    def advance(self):
        """This function is used to advance the bot."""
        self.move(self.speed)
        return self.sense()

    def sense(self):
        """This function represents the robot sensing its location."""
        return (self.x, self.y)

    def __repr__(self):
        """This allows us to print a robot's position"""
        return '[%.5f, %.5f]'  % (self.x, self.y)
