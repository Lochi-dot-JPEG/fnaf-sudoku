import pygame
# Initialise pygame before importing other modules so fonts can load
pygame.init()
# Initialise pygame's sound mixer to enable audio
pygame.mixer.init()
# Import necessary modules
import player_management
import ui
import globals


title_options = ["Play Game", "Tutorial", "Quit"]

# Play and loop music infinitely
pygame.mixer.music.load("assets/music_box.ogg")
pygame.mixer.music.play(-1)

running = True
while running:

    globals.returning_to_title = False

    # Display title screen with title decorations enabled
    selected_title_button = ui.ask("", title_options, True)

    # Handle whichever button has been pressed
    match selected_title_button:
        case "Play Game":
            player_management.run_game()
        case "Tutorial":
            pass
        case _:
            pygame.quit()
            running = False
