
import pygame
import game
from game import play
import player_management

# pygame setup
pygame.init()
running = True

title_options = ["Play Game", "Tutorial"]


while running:

    selected_title_button = game.show_title(title_options)
    match selected_title_button:
        case "Play Game":
            player_management.run_game()
        case "Tutorial":
            pass
        case _:
            print("Error: Invalid title button pressed")

pygame.quit()
