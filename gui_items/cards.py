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
        try:
            self.img = pygame.image.load(f"resources/card_{id}.jpg")
        except FileNotFoundError:
            self.img = pygame.image.load(f"resources/test_card.jpg")
        self.rect = pygame.Rect(0, y, self.CARD_WIDTH, self.CARD_HEIGHT)
        self.select = False
        self.msg = None
        msg = card_msgs.get(id)
        if msg:
            self.msg = msg


class Hand(CardData):
    def __init__(self, y):
        self.cards = []
        self.y = y
        self.all_cards = [Card(i, y) for i in range(42)]
        self.selected = None
        bkg_staff = pygame.image.load('resources/bkg_staff.jpg')
        self.bkg_staff = pygame.transform.rotozoom(bkg_staff, 0, self.SCALING)

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

    def update(self, cards):
        # space the Rects of the cards
        self.cards = [Card(card, self.y) for card in cards]
        i = 0
        for card in self.cards:
            card.rect.left = self.HAND_MARGIN + (self.CARD_WIDTH + self.CARD_MARGIN) * i
            i += 1

        # select the first drawn card
        if len(self.cards) == 1:
            self.selected = 0
            self.cards[self.selected].select = True

        # if the selected card is the last in the hand and is deleted
        if self.selected != None:
            if self.selected > len(self.cards) - 1:
                self.selected = len(self.cards) - 1
            self.cards[self.selected].select = True

    def draw(self, surf):
        surf.blit(self.bkg_staff, (0, self.y + 40))
        for card in self.cards:
            #draw a border around the selected card
            if card.select:
                pygame.draw.rect(surf, (255, 0, 0), card.rect.inflate(10, 10))
            pygame.draw.rect(surf, (255, 255, 206), card.rect)
            surf.blit(card.img, (card.rect.left, card.rect.top + 40))


card_msgs = {}
for i in range(19):
    card_msgs[i] = f"This is the message for card {i}"
