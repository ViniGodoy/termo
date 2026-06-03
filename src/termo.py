import pygame
from pygame import Vector2

from game.constants import BG_COLOR, SCREEN_SIZE
from game.keyboard import Keyboard
from game.letter import Letter
from game.util import write
from game.word import Word

# pygame setup
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Termo")
clock = pygame.time.Clock()
running = True
dt= 0

x = 350
palavra1 = Word(Vector2(x, 20+65*1))
palavra2 = Word(Vector2(x, 20+65*2))
palavra3 = Word(Vector2(x, 20+65*3))
palavra4 = Word(Vector2(x, 20+65*4))
palavra5 = Word(Vector2(x, 20+65*5))
palavra6 = Word(Vector2(x, 20+65*6))
palavra1.set_typing()

keyboard = Keyboard(Vector2(150, 20+65*8))
keyboard.reveal("praça", "arcas")
keyboard.reveal("termo", "praça")

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                palavra1.type('a')
            elif event.key == pygame.K_w:
                palavra1.backspace()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(BG_COLOR)
    write(screen,Vector2(0,10), "TERMO", "WHITE", Vector2(SCREEN_SIZE[0], 65))
    palavra1.paint(screen)
    palavra2.paint(screen)
    palavra3.paint(screen)
    palavra4.paint(screen)
    palavra5.paint(screen)
    palavra6.paint(screen)
    keyboard.paint(screen)

    keys = pygame.key.get_pressed()

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
