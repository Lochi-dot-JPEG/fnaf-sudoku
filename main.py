# Import necessary modules
import pygame
import player_management
import ui
import globals

# Initialise pygame's sound mixer to enable audio
pygame.mixer.init()

# List of strings for the title buttons
title_options = ["Play Game", "Tutorial", "Quit"]

# Loop through showing the title screen, so when the game finishes running or tutorial ends it returns to the title
running = True
while running:
    # Play jukebox music for title screen
    pygame.mixer.music.load(globals.musicbox_music_path)
    pygame.mixer.music.play()

    # Disable returning_to_title so that the game does not immediately quit
    globals.returning_to_title = False

    # Display title screen with title decorations enabled
    selected_title_button = ui.ask("", title_options, True)

    # Handle whichever title button has been pressed
    match selected_title_button:
        case "Play Game":
            player_management.run_game()
        case "Tutorial":
            ui.tutorial()
        case _:
            pygame.quit()
            running = False
