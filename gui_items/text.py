import pygame

class Text:
    def __init__(self, msg, loc, size=20, color=(255, 255, 255)):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.msg = msg
        self.new_msg = msg
        self.loc = loc
        self.font = pygame.font.SysFont(None, size)
        self.image = self.font.render(msg, 0, color)

    def change_msg(self, msg):
        if self.new_msg != self.msg:
            self.new_msg = msg
            self.image = self.font.render(msg, 0, self.color)

    def draw(self, surf):
        surf.blit(self.image, self.loc)
