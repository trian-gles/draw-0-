import pygame
from math import cos, sin, radians

class Timer:
    RADIUS = 20
    LENGTH = 240

    def __init__(self, loc):
        self.count = self.LENGTH
        self.loc = loc

    def update(self):
        self.count = (self.count - 1) % self.LENGTH
        if self.count == 0:
            return True

    def draw(self, surf):

        # Draw the base circle
        pygame.draw.circle(surf, (255, 255, 255), self.loc, self.RADIUS)

        # Draw the 12 o clock line
        line_top = (self.loc[0], self.loc[1] - self.RADIUS)
        pygame.draw.line(surf, (0, 0, 0), self.loc, line_top)

        # Draw the moving hand
        angle = radians((self.count / self.LENGTH) * 360 - 180)
        x_arm = int(sin(angle) * self.RADIUS) + self.loc[0]
        y_arm = int(cos(angle) * self.RADIUS) + self.loc[1]
        pygame.draw.line(surf, (255, 0, 0), self.loc, (x_arm, y_arm))
