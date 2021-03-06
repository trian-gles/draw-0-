import pygame

class Text(pygame.sprite.Sprite):
    def __init__(self, msg, loc, size, color):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.size = size
        self.msg = msg
        self.new_msg = msg
        self.font = pygame.font.SysFont(None, size)
        self.image = self.font.render(msg, 0, color)
        self.rect = self.image.get_rect().move(*loc)

    def change_msg(msg):
        if self.new_msg != self.msg:
            self.new_msg = msg
            self.image = self.font.render(msg, 0, color)



if __name__ == "__main__":
    pass
