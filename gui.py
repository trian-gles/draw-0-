import pygame
import PySimpleGUI as sg
from socks import Client

WIDTH = 800
HEIGHT = 640
DARK_BLUE = (39, 44, 73)
WHITE = (255, 255, 255)
LIGHT_GREY = (191, 191, 191)

layout = [[sg.Text("Enter your username")],
[sg.InputText()],
[sg.Submit()]]
window = sg.Window("Draw", layout)

event, values = window.read()
username = values[0]
window.close()
print("Username : " + username)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("draw(0)")
font = pygame.font.SysFont(None, 24)

def main():
    run = True
    client = Client(username)
    clock = pygame.time.Clock()
    while run:
        chat_message = ""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        incoming_message = client.listen()
        if incoming_message:
            print(incoming_message)

        screen.fill(DARK_BLUE)
        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()
