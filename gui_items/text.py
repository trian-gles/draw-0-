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

    def change_msg(self, new_msg):
        self.msg = new_msg
        self.image = self.font.render(msg, 0, self.color)

    def draw(self, surf):
        surf.blit(self.image, self.loc)



class MessageBox(Text):
    def __init__(self, msg, loc, size=20, bkg_color=(0, 0, 0), text_color=(255, 255, 255)):
        super().__init__(msg, loc, size, text_color)
        self.bkg_color = bkg_color
        self._build_rect()

    def _build_rect(self):
        self.rect = self.image.get_rect().move(*self.loc)
        self.rect.inflate_ip(30, 30)

    def change_msg(self, msg):
        super().change_msg(msg)
        self._build_rect()

    def draw(self, surf):
        #draw the background rectangle
        pygame.draw.rect(surf, self.bkg_color, self.rect)
        #draw the overlaid text
        super().draw(surf)
