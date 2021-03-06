import pygame

class CardData:
    CARD_WIDTH = 180
    CARD_HEIGHT = 300
    CARD_MARGIN = int(CARD_WIDTH / 16)
    HAND_MARGIN = 80


class Card(CardData):
    def __init__(self, id, y):
        self.id = id
        self.rect = pygame.Rect(0, y, self.CARD_WIDTH, self.CARD_HEIGHT)



class Hand(CardData):
    def __init__(self, y):
        self.cards = []
        self.y = y
        self.all_cards = []
        for i in range(42):
            self.all_cards.append(Card(i, y))

    def add(self, id):
        self.cards.append(self.all_cards[id])
        self._update()

    def _update(self):
        i = 0
        for card in self.cards:
            card.rect.left = self.HAND_MARGIN + (self.CARD_WIDTH + self.CARD_MARGIN) * i
            i += 1

    def draw(self, surf):
        for card in self.cards:
            pygame.draw.rect(surf, (255, 255, 255), card.rect)
