import pygame
import os

class CardData:
    CARD_WIDTH = 260
    CARD_HEIGHT = 300
    CARD_MARGIN = int(CARD_WIDTH / 16)
    HAND_MARGIN = 100
    SCALING = 1280/2339


class Card(CardData):
    def __init__(self, id, y):
        self.id = id
        self.img = pygame.image.load("resources/test_card.jpg")
        self.rect = pygame.Rect(0, y, self.CARD_WIDTH, self.CARD_HEIGHT)
        self.select = False



class Hand(CardData):
    def __init__(self, y):
        self.cards = []
        self.y = y
        self.all_cards = []
        self.selected = None
        bkg_staff = pygame.image.load('resources/bkg_staff.jpg')
        self.bkg_staff = pygame.transform.rotozoom(bkg_staff, 0, self.SCALING)
        for i in range(42):
            self.all_cards.append(Card(i, y))

    def add(self, id):
        self.cards.append(self.all_cards[id])
        self._update()

    def remove(self):
        drawn = self.cards.pop(self.selected)
        self._update()
        return drawn.id

    def cycle_right(self):
        if self.selected != None:
            self.cards[self.selected].select = False
            self.selected = (self.selected + 1) % len(self.cards)
            self.cards[self.selected].select = True

    def cycle_left(self):
        if self.selected != None:
            self.cards[self.selected].select = False
            self.selected = (self.selected - 1) % len(self.cards)
            self.cards[self.selected].select = True

    def _update(self):
        #space the Rects of the cards
        i = 0
        for card in self.cards:
            card.rect.left = self.HAND_MARGIN + (self.CARD_WIDTH + self.CARD_MARGIN) * i
            i += 1

        #select the first drawn card
        if len(self.cards) == 1:
            self.selected = 0
            self.cards[self.selected].select = True

        #if the selected card is the last in the hand and is deleted
        if self.selected != None:
            if self.selected > len(self.cards) - 1:
                self.selected = len(self.cards) - 1

    def draw(self, surf):
        surf.blit(self.bkg_staff, (0, self.y + 40))
        for card in self.cards:
            #draw a border around the selected card
            if card.select:
                pygame.draw.rect(surf, (255, 0, 0), card.rect.inflate(10, 10))
            pygame.draw.rect(surf, (255, 255, 206), card.rect)
            surf.blit(card.img, (card.rect.left, card.rect.top + 40))
