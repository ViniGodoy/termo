from __future__ import annotations

import pygame

from dict.wordlist import WordList
from game.constants import BG_PRIMARY, SCREEN_SIZE
from game.game_screen import GameScreen

# pygame setup
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Termo")
clock = pygame.time.Clock()
running = True

word_list = WordList()
word_list.load()

game_screen = GameScreen(word_list)
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            game_screen.on_key_down(event)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(BG_PRIMARY)
    game_screen.paint(screen)

    keys = pygame.key.get_pressed()

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    game_screen.update(dt)

pygame.quit()
