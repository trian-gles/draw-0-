import argparse
import pygame
import sys
import os
from socks import Client
from gui_items import Arrow, Text, TimeTimer, Hand, MessageBox, MessageButton
from setup_prompt import retrieve_username

#Need to add: FIX THE TIMER!!!! make it rely on time.time, for now.
#NEED TO FIX HAND NAMESPACE ISSUES!


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--debug', action='store_true',
                    help='run the gui without a client')

args = parser.parse_args()
if args.debug:
    print("DEBUG MODE")

def load_resource(filename):
    return os.path.join('resources', filename)

WIDTH = 1280
HEIGHT = 720

START_COOR = (int(WIDTH * 1 / 32), int(HEIGHT * 1 / 32))
QUIT_COOR = (START_COOR[0], START_COOR[1] + 60)
ARROW_R_COOR = (int(WIDTH * 9 / 16), int(HEIGHT * 13 / 16))
ARROW_L_COOR = (int(WIDTH * 7 / 16), int(HEIGHT * 13 / 16))
CLOCK_COOR = (int(WIDTH * 15 / 16), int(HEIGHT * 15 / 16))
CARD_NOTIF_COOR = (int(WIDTH / 16), int(HEIGHT * 3 / 4))
EXTERN_CARD_COOR = (CARD_NOTIF_COOR[0], CARD_NOTIF_COOR[1] + 60)
DEBUG_COOR = (int(WIDTH * 1/2), int(HEIGHT * 1 / 16))

BLACK = (55, 55, 55)
DARK_BLUE = (39, 44, 73)
WHITE = (255, 255, 255)
LIGHT_GREY = (191, 191, 191)
GREEN = (58, 255, 58)
RED = (255, 58, 58)

SCALING = 1280/2339

if not args.debug:
    username = retrieve_username()
    client = Client(username)



pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("draw(0)")
hand = Hand(200)


def right():
    print("Right press")
    hand.cycle_right()
    if not args.debug:
        client.cycle_right()


def left():
    print("Left press")
    hand.cycle_left()
    if not args.debug:
        client.cycle_left()


def start_call():
    client.send_start()


def quit_call():
    client.send_quit()


def main():
    run = True

    clock = pygame.time.Clock()


    card_info = MessageBox("The card info will go here", CARD_NOTIF_COOR, size=26, bkg_color=GREEN, text_color=BLACK)
    extern_card_info = MessageBox("External card info here", EXTERN_CARD_COOR, size=26, bkg_color=RED, text_color=BLACK)

    debug_dialogue = MessageBox("", DEBUG_COOR, size=12)
    if args.debug:
        debug_dialogue.change_msg("DEBUG MODE")

    timer = TimeTimer(CLOCK_COOR)

    hand.add(4)
    hand.add(8)
    hand.add(9)
    hand.add(10)

    start_btn = MessageButton("Start", START_COOR, start_call, bkg_color=GREEN)
    quit_btn = MessageButton("Quit", QUIT_COOR, quit_call, bkg_color=RED)

    arrow_r = Arrow(ARROW_R_COOR, True, right)
    arrow_l = Arrow(ARROW_L_COOR, False, left)
    arrows = (arrow_r, arrow_l)
    buttons = arrows + (start_btn, quit_btn)

    all_img = buttons + (timer,) + (hand,) + (card_info,) + (extern_card_info,) + (debug_dialogue,)

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
                for btn in buttons:
                    if btn.check_mouse(mouse_pos):
                        btn.callback()

        if not args.debug:
            client_msg = client.listen()
            if client_msg:
                debug_dialogue.change_msg(client_msg)
                print(client_msg)


        screen.fill(DARK_BLUE)

        if timer.update():
            print("RESET")

        mouse_pos = pygame.mouse.get_pos()

        for arrow in arrows:
            arrow.check_mouse(mouse_pos)

        for img in all_img:
            img.draw(screen)

        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()
