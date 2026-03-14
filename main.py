import pygame
# Initialise pygame before importing other modules so fonts can load
pygame.init()
pygame.mixer.init()
import player_management
import ui

# pygame setup
running = True

title_options = ["Play Game", "Tutorial", "Quit"]

# Play and loop music infinitely
pygame.mixer.music.load("assets/music_box.ogg")
pygame.mixer.music.play(-1)

while running:


    # Display title screen with title decorations enabled
    selected_title_button = ui.ask("", title_options, True)

    # Handle whichever button has been pressed
    match selected_title_button:
        case "Play Game":
            player_management.run_game()
        case "Tutorial":
            pass
        case _: # This option will run when quit is pressed or an error occurs in ask e.g. player quitting
            running = False

pygame.quit()
