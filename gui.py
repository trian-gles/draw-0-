import pygame
import PySimpleGUI as sg
import sys
import os
from socks import Client
from gui_items import Arrow, Text, Timer, Hand, MessageBox

def load_resource(filename):
    return os.path.join('resources', filename)

WIDTH = 1280
HEIGHT = 720


ARROW_R_COOR = (int(WIDTH * 7 / 16), int(HEIGHT * 13 / 16))
ARROW_L_COOR = (int(WIDTH * 9 / 16), int(HEIGHT * 13 / 16))
CLOCK_COOR = (int(WIDTH * 15 / 16), int(HEIGHT * 15 / 16))
CARD_NOTIF_COOR = (int(WIDTH / 16), int(HEIGHT * 3 / 4))
EXTERN_CARD_COOR = (CARD_NOTIF_COOR[0], CARD_NOTIF_COOR[1] + 60)

BLACK = (55, 55, 55)
DARK_BLUE = (39, 44, 73)
WHITE = (255, 255, 255)
LIGHT_GREY = (191, 191, 191)
GREEN = (58, 255, 58)
RED = (255, 58, 58)

SCALING = 1280/2339


bkg_staff = pygame.image.load(load_resource('bkg_staff.jpg'))
bkg_staff = pygame.transform.rotozoom(bkg_staff, 0, SCALING)



pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("draw(0)")

def right():
    print("Right press")

def left():
    print("Left press")

def draw_bkg(surf):
    surf.blit(bkg_staff, (0, int(HEIGHT / 3)))


def main():
    run = True
    #client = Client(username)
    clock = pygame.time.Clock()


    card_info = MessageBox("The card info will go here", CARD_NOTIF_COOR, size=26, bkg_color=GREEN, text_color=BLACK)
    extern_card_info = MessageBox("External card info here", EXTERN_CARD_COOR, size=26, bkg_color=RED, text_color=BLACK)


    arrow_r = Arrow(ARROW_R_COOR, False, left)
    arrow_l = Arrow(ARROW_L_COOR, True, right)
    arrows = (arrow_r, arrow_l)
    timer = Timer(CLOCK_COOR)
    hand = Hand(200)
    hand.add(4)
    hand.add(8)
    hand.add(9)
    hand.add(10)
    hand.add(11)
    hand.add(6)

    all_img = arrows + (timer,) + (hand,) + (card_info,) + (extern_card_info,)

    while run:
        chat_message = ""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    right()
                if event.key == pygame.K_LEFT:
                    left()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                for arrow in arrows:
                    if arrow.check_mouse(mouse_pos):
                        arrow.callback()

        #incoming_message = client.listen()
        #if incoming_message:
        #    print(incoming_message)

        screen.fill(DARK_BLUE)

        if timer.update():
            print("RESET")

        mouse_pos = pygame.mouse.get_pos()

        for arrow in arrows:
            arrow.check_mouse(mouse_pos)

        draw_bkg(screen)
        for img in all_img:
            img.draw(screen)

        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()
