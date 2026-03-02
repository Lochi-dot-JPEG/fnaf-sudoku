
import pygame
from game import play
import player_management

# pygame setup
pygame.init()
running = True




while running:

    player_management.run_game()
    # poll for events


pygame.quit()
