import pygame
import PySimpleGUI as sg
import sys
from socks import Client
from game_imgs import Arrow, Text, Timer, Hand



WIDTH = 1280
HEIGHT = 720


ARROW_R_COOR = (int(WIDTH * 7 / 16), int(HEIGHT * 13 / 16))
ARROW_L_COOR = (int(WIDTH * 9 / 16), int(HEIGHT * 13 / 16))

CLOCK_COOR = (int(WIDTH * 15 / 16), int(HEIGHT * 15 / 16))

DARK_BLUE = (39, 44, 73)
WHITE = (255, 255, 255)
LIGHT_GREY = (191, 191, 191)

def right():
    print("Right press")

def left():
    print("Left press")

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("draw(0)")

def main():
    run = True
    #client = Client(username)
    clock = pygame.time.Clock()
    hello_wrld = Text("Hello World", (30, 30), 24, WHITE)

    arrow_r = Arrow(ARROW_R_COOR, False, left)
    arrow_l = Arrow(ARROW_L_COOR, True, right)
    arrows = (arrow_r, arrow_l)
    timer = Timer(CLOCK_COOR)
    sprites = pygame.sprite.RenderPlain((hello_wrld,))
    hand = Hand(200)
    hand.add(4)
    hand.add(8)
    hand.add(9)
    hand.add(10)
    hand.add(11)
    hand.add(6)

    all_img = arrows + (timer,) + (sprites,) + (hand,)

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

        for img in all_img:
            img.draw(screen)

        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()
