from math import *
import random

from box_world import *
from collision_detection import where_is_point

class robot:
    def __init__(self, x = 0.0, y = 0.0, heading = 0.0, speed = 1.0, heading_delta = 0.0):
        """This function is called when you create a new robot. It sets some of
        the attributes of the robot, either to their default values or to the values
        specified when it is created."""
        self.x = x
        self.y = y
        self.heading = heading
        self.speed = speed
        self.target_speed = speed
        self.heading_delta = heading_delta

    def advance(self):
        """This function is used to advance the bot."""
        self.move()
        return self.sense()

    def sense(self):
        """This function represents the robot sensing its location."""
        return (self.x, self.y)

    def move(self):
        """This function turns the robot and then moves it forward."""
        # Accelerate up to the target speed
        self.speed *= 1.075
        self.speed = min(self.speed, self.target_speed)

        # truncate to fit physical limitations
        self.speed = max(0.0, self.speed)

        # Execute motion
        self.heading = angle_trunc(self.heading + self.heading_delta)
        self.x += self.speed * cos(self.heading)
        self.y += self.speed * sin(self.heading)

        self.bounce()

    def bounce(self):
        # Naive bounce model based on angle to reflection
        bounds = box_bounds()
        bounce_speed = 3
        if self.x < bounds['min_x'] and abs(self.heading) > pi/2:
            # left wall bounce
            x_overstep = self.x - bounds['min_x']
            self.x -= 2 * x_overstep
            self.heading = pi - self.heading
            self.heading_delta = 0
            self.speed = bounce_speed
        if self.x > bounds['max_x'] and abs(self.heading) < pi/2:
            # right wall bounce
            x_overstep = self.x - bounds['max_x']
            self.x -= 2 * x_overstep
            self.heading = pi - self.heading
            self.heading_delta = 0
            self.speed = bounce_speed
        if self.y < bounds['min_y'] and self.heading < 0:
            # bottom wall bounce
            y_overstep = self.y - bounds['min_y']
            self.y -= 2 * y_overstep
            self.heading = -1 * self.heading
            self.heading_delta = 0
            self.speed = bounce_speed
        if self.y > bounds['max_y'] and self.heading > 0:
            # top wall bounce
            y_overstep = self.y - bounds['max_y']
            self.y -= 2 * y_overstep
            self.heading = -1 * self.heading
            self.heading_delta = 0
            self.speed = bounce_speed
        if where_is_point(self.sense(), 25)[-6:] == 'corner':
            self.target_speed = 0
            self.speed = 0

    def __repr__(self):
        """This allows us to print a robot's position"""
        return '[%.5f, %.5f]'  % (self.x, self.y)
