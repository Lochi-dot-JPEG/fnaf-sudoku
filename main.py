import pygame
# Initialise pygame before importing other modules so fonts can load
pygame.init()
import game
import player_management

# pygame setup
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
