import pygame

class Arrow:
    SIZE = 100
    DEF_COLOR = (255, 255, 255)
    HOVER_COLOR = (0, 255, 0)

    def __init__(self, loc, flipped):
        self.loc = loc
        self.rect = pygame.Rect(0, 0, self.SIZE, self.SIZE)
        self.rect.center = loc
        self.orient = 1 if flipped == True else -1
        self.color = self.DEF_COLOR

    def check_mouse(self, mouse_coor):
        if self.rect.collidepoint(mouse_coor):
            self.color = self.HOVER_COLOR
        else:
            self.color = self.DEF_COLOR

    def draw(self, surf):
        #draw the base square
        pygame.draw.rect(surf, self.color, self.rect)

        #draw the inner triangle
        base_x = self.loc[0] - (self.SIZE / 3 * self.orient)
        tip_x = self.loc[0] + (self.SIZE / 3 * self.orient)

        up_base = (base_x , self.loc[1] - self.SIZE / 3)
        low_base = (base_x , self.loc[1] + self.SIZE / 3)
        tip = (tip_x, self.loc[1])
        pygame.draw.polygon(surf, (0, 0, 0), (up_base, low_base, tip))
