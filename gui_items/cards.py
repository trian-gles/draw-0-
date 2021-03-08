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
        self.selected = None
        for i in range(42):
            self.all_cards.append(Card(i, y))

    def add(self, id):
        self.cards.append(self.all_cards[id])
        self._update()

    def remove(self, id):
        self.cards.remove(self.all_cards[id])
        self._update()

    def cycle_right(self):
        if self.selected != None:
            self.selected = (self.selected + 1) % len(self.cards)

    def cycle_left(self):
        if self.selected != None:
            self.selected = (self.selected - 1) % len(self.cards)

    def _update(self):
        i = 0
        for card in self.cards:
            card.rect.left = self.HAND_MARGIN + (self.CARD_WIDTH + self.CARD_MARGIN) * i
            i += 1
        if len(self.cards) == 1:
            self.selected = 0

        #if the selected card is the last in the hand and is deleted
        if self.selected != None:
            if self.selected > len(self.cards) - 1:
                self.selected = len(self.cards) - 1

    def draw(self, surf):
        for card in self.cards:
            pygame.draw.rect(surf, (255, 255, 206), card.rect)
