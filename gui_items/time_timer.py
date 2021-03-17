import pygame
from math import cos, sin, radians
import time

# Timer should be adjusted to reset on reception of new card!!


class TimeTimer:
    RADIUS = 20
    SEC_LENGTH = 8

    def __init__(self, loc):
        self.loc = loc
        self.start_time = time.time()
        self.lap = 0

    def update(self):
        self.lap = time.time() - self.start_time
        if self.lap > 8:
            self.start_time = time.time()
            return True

    def draw(self, surf):

        # Draw the base circle
        pygame.draw.circle(surf, (255, 255, 255), self.loc, self.RADIUS)

        # Draw the 12 o clock line
        line_top = (self.loc[0], self.loc[1] - self.RADIUS)
        pygame.draw.line(surf, (0, 0, 0), self.loc, line_top)

        # Draw the moving hand
        angle = radians((self.lap / self.SEC_LENGTH) * 360 - 180)
        x_arm = int(sin(angle * -1) * self.RADIUS) + self.loc[0]
        y_arm = int(cos(angle) * self.RADIUS) + self.loc[1]
        pygame.draw.line(surf, (255, 0, 0), self.loc, (x_arm, y_arm))
