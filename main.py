import pygame
# Initialise pygame before importing other modules so fonts can load
pygame.init()
import game
import player_management

# pygame setup
running = True

title_options = ["Play Game", "Tutorial", "Quit"]

while running:

    selected_title_button = game.ask("", title_options, True)
    match selected_title_button:
        case "Play Game":
            player_management.run_game()
        case "Tutorial":
            pass
        case _: # This option will run when quit is pressed or an error occurs in ask e.g. player quitting
            running = False


pygame.quit()
